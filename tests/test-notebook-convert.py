import os
import sys
import shutil
import tempfile
from pathlib import Path
import pytest
import nbformat

# Add parent directory to path to import our module
sys.path.append(str(Path(__file__).parent.parent))
# Make sure scripts directory is in the path for notebook_utils import
scripts_dir = Path(__file__).parent.parent / "scripts"
if scripts_dir not in sys.path:
    sys.path.append(str(scripts_dir))

# Import with explicit path to make sure notebook_utils can be found
from scripts.notebook_convert import convert_notebook, export_notebook_cell_to_mdx, extract_frontmatter

@pytest.fixture
def setup_test_environment():
    """Set up test environment with temporary directories and paths."""
    # Create temporary directory for test outputs
    temp_dir = Path(tempfile.mkdtemp())
    test_dir = Path(__file__).parent
    notebooks_dir = test_dir / "notebooks"
    
    # Ensure the notebook directory exists
    notebooks_dir.mkdir(exist_ok=True)
    
    # Path to store intermediate static files
    static_dir = temp_dir / "_intermediate" / "static" / "img"
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Return all necessary paths
    yield {
        'temp_dir': temp_dir,
        'test_dir': test_dir,
        'notebooks_dir': notebooks_dir,
        'static_dir': static_dir
    }
    
    # Clean up temp directory after tests
    shutil.rmtree(temp_dir)

def test_single_page_conversion(setup_test_environment):
    """Test conversion of a notebook without page breaks."""
    env = setup_test_environment
    
    # Use the existing notebook file
    notebook_path = env['notebooks_dir'] / "single-page.ipynb"
    
    # Skip test if the file doesn't exist
    if not notebook_path.exists():
        pytest.skip(f"Notebook file {notebook_path} not found")
    
    # Call convert_notebook directly, similar to running the script from command line
    # This is like running: python3 scripts/notebook_convert.py tests/notebooks/single-page.ipynb
    output_paths = convert_notebook(notebook_path, notebook_path.parent, env['test_dir'].parent)
    
    # Check that a single output file was created
    assert len(output_paths) == 1
    
    # Check the output file has the correct name
    expected_path = notebook_path.parent / f"{notebook_path.stem}.mdx"
    assert output_paths[0] == expected_path
    
    # Check the file exists
    assert expected_path.exists()
    
    # Check the file content
    with open(expected_path) as f:
        content = f.read()
        # Verify frontmatter is present
        assert "title: Single Page Test" in content
        # Verify content is present
        assert "# Test heading" in content
    
    # Check for extracted images
    static_dir = env['test_dir'].parent / "_intermediate" / "static" / "img"
    assert static_dir.exists(), "Static directory wasn't created"
    
    # Look for PNG images
    png_images = list(static_dir.glob("**/single-page/*.png"))
    assert len(png_images) > 0, "No PNG images were extracted"
    
    # Clean up the output file after the test
    expected_path.unlink(missing_ok=True)

def test_multi_page_conversion(setup_test_environment):
    """Test conversion of a notebook with page breaks."""
    env = setup_test_environment
    
    # Use the existing notebook file
    notebook_path = env['notebooks_dir'] / "multi-page.ipynb"
    
    # Skip test if the file doesn't exist
    if not notebook_path.exists():
        pytest.skip(f"Notebook file {notebook_path} not found")
    
    # Call convert_notebook directly, similar to running the script from command line
    # This is like running: python3 scripts/notebook_convert.py tests/notebooks/multi-page.ipynb
    output_paths = convert_notebook(notebook_path, notebook_path.parent, env['test_dir'].parent)
    
    # Check that multiple output files were created
    assert len(output_paths) > 1
    
    # Check that a subdirectory was created
    notebook_dir = notebook_path.parent / notebook_path.stem
    assert notebook_dir.exists()
    
    # Check index.mdx
    index_path = notebook_dir / "index.mdx"
    assert index_path.exists()
    with open(index_path) as f:
        content = f.read()
        # Verify chapter title is present in frontmatter
        assert "title: Multi page chapter title" in content
        # Verify index content
        assert "# Chapter Heading" in content
    
    # Check for page files
    page_files = list(notebook_dir.glob("autogen-page-*.mdx"))
    assert len(page_files) >= 2
    
    # Sort the files to ensure we check them in the right order
    page_files.sort()
    
    # Check content of first page
    with open(page_files[0]) as f:
        content = f.read()
        assert "title: Section 1" in content
    
    # Check content of second page
    with open(page_files[1]) as f:
        content = f.read()
        assert "title: Section 2" in content
    
    # Check for extracted images
    static_dir = env['test_dir'].parent / "_intermediate" / "static" / "img"
    assert static_dir.exists(), "Static directory wasn't created"
    
    # Look for images
    notebook_images = list(static_dir.glob("**/multi-page/*.*"))
    assert len(notebook_images) > 0, "No images were extracted"
    
    # Clean up the output directory after the test
    if notebook_dir.exists():
        shutil.rmtree(notebook_dir)

def test_frontmatter_extraction():
    """Test that frontmatter is correctly extracted from notebooks."""
    notebook = nbformat.v4.new_notebook()
    frontmatter = "---\ntitle: Test Frontmatter\nslug: /test\n---\n"
    notebook.cells.append(nbformat.v4.new_raw_cell(f"# !chapter\n{frontmatter}"))
    notebook.cells.append(nbformat.v4.new_markdown_cell("# Test"))
    
    extracted, idx = extract_frontmatter(notebook)
    assert idx == 0  # Should find frontmatter in first cell
    assert "title: Test Frontmatter" in extracted, "Title incorrect"
    assert "slug: /test" in extracted, "Content incorrect"
