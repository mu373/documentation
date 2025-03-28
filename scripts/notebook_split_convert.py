import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import shutil

import nbformat
from nbconvert.exporters import MarkdownExporter
from nbconvert.preprocessors import Preprocessor

# Import utility functions
from notebook_utils import (
    escape_html, extract_frontmatter, has_pagebreaks, 
    append_to_gitignore, generate_directory_gitignore
)


class EscapePreprocessor(Preprocessor):
    def escape_html(self, text):
        """
        Escape HTML special characters in the given text.
        """
        return escape_html(text)

    def preprocess_cell(self, cell, resources, cell_index):
        if cell.cell_type == "markdown":

            # Don't include cells with {"hide": true} in metadata
            if "hide" in cell.get("metadata", {}) and cell.metadata.hide == True:
                cell.source = ""
            else:
                # Rewrite .ipynb links to .md links.
                cell.source = re.sub(
                    r"\[([^\]]*)\]\((?![^\)]*//)([^)]*)\.ipynb\)",
                    r"[\1](\2.md)",
                    cell.source,
                )

                # Heading levels
                cell.source = re.sub(
                    r"(^#)(#.*) (.*)",
                    r"\2 \3",
                    cell.source,
                )

        elif cell.cell_type == "code":
            # Escape triple backticks in code cells.
            cell.source = cell.source.replace("```", r"\`\`\`")

            if "outputs" in cell:
                filter_out = set()
                for i, output in enumerate(cell["outputs"]):
                    if "text" in output:
                        if not output["text"].strip():
                            filter_out.add(i)
                            continue
                        # First replace triple backticks, then escape HTML special characters.
                        escaped_text = self.escape_html(output["text"].replace("```", r"\`\`\`"))
                        output["text"] = escaped_text
                    elif "data" in output:
                        for key, value in output["data"].items():
                            if isinstance(value, str):
                                if key == "text/html":
                                   # Only replace triple backticks in HTML output.
                                   escaped_value = value.replace("```", r"\`\`\`")
                                   output["data"][key] = escaped_value
                                else: 
                                    # Replace triple backticks, then escape HTML special characters.
                                    escaped_value = self.escape_html(value.replace("```", r"\`\`\`"))
                                    output["data"][key] = escaped_value
                cell["outputs"] = [
                    output
                    for i, output in enumerate(cell["outputs"])
                    if i not in filter_out
                ]

        return cell, resources


class ResourceProcessor(Preprocessor):
    """Handle notebook resources like images."""
    
    def __init__(self, static_dir: Path, notebook_name: str):
        super().__init__()
        self.notebook_name = notebook_name
        self.assets_dir = static_dir / "notebooks" / notebook_name
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
    def preprocess_cell(self, cell, resources, cell_index):
        if cell.cell_type == "markdown":
            # Handle embedded images
            cell.source = self._process_markdown_images(cell.source)
        elif cell.cell_type == "code" and "outputs" in cell:
            # Handle output images
            cell["outputs"] = self._process_output_images(cell["outputs"])
            
        return cell, resources
    
    def _process_markdown_images(self, source: str) -> str:
        """Process and save images in markdown content."""
        def replace_image(match):
            img_path = match.group(2)
            if img_path.startswith("data:"):
                # Handle base64 embedded images
                import base64
                import hashlib
                
                # Extract mime type and data
                mime_match = re.match(r"data:([^;]+);base64,(.+)", img_path)
                if mime_match:
                    mime_type, b64_data = mime_match.groups()
                    ext = mime_type.split('/')[-1]
                    
                    # Generate filename from content hash
                    data = base64.b64decode(b64_data)
                    filename = hashlib.md5(data).hexdigest()[:12] + '.' + ext
                    
                    # Save image
                    img_file = self.assets_dir / filename
                    img_file.write_bytes(data)
                    
                    # Return relative path
                    return f"![{match.group(1)}](/notebooks/{self.notebook_name}/{filename})"
            else:
                # Handle regular image files
                src_path = Path(img_path)
                if src_path.exists():
                    new_name = src_path.name
                    dst_path = self.assets_dir / new_name
                    shutil.copy2(src_path, dst_path)
                    return f"![{match.group(1)}](/notebooks/{self.notebook_name}/{new_name})"
            return match.group(0)
        
        # Find and process all image references
        return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, source)
    
    def _process_output_images(self, outputs: List[Dict]) -> List[Dict]:
        """Process and save images in cell outputs."""
        new_outputs = []
        for output in outputs:
            if "data" in output:
                new_data = {}
                for mime_type, data in output["data"].items():
                    if mime_type.startswith("image/"):
                        # Save image data
                        import base64
                        import hashlib
                        
                        ext = mime_type.split('/')[-1]
                        if isinstance(data, str):
                            if data.startswith("data:"):
                                # Handle data URLs
                                b64_data = data.split(",", 1)[1]
                                img_data = base64.b64decode(b64_data)
                            else:
                                # Handle base64 directly
                                img_data = base64.b64decode(data)
                        else:
                            img_data = data
                            
                        # Generate filename from content hash
                        filename = hashlib.md5(img_data).hexdigest()[:12] + '.' + ext
                        
                        # Save image
                        img_file = self.assets_dir / filename
                        print(f"saving to {img_file}")
                        img_file.write_bytes(img_data)
                        
                        # Update reference
                        new_data[mime_type] = f"/img/notebooks/{self.notebook_name}/{filename}"
                    else:
                        new_data[mime_type] = data
                output["data"] = new_data
            new_outputs.append(output)
        return new_outputs


def setup_exporter(static_dir: Path, notebook_name: str) -> MarkdownExporter:
    """Create and configure a markdown exporter with the necessary preprocessors."""
    return MarkdownExporter(
        preprocessors=[
            EscapePreprocessor,
            ResourceProcessor(static_dir, notebook_name)
        ],
        template_name="mdoutput",
        extra_template_basedirs=["./scripts/notebook_convert_templates"],
    )

def convert_single_file(
    nb: nbformat.NotebookNode, 
    output_path: Path, 
    static_dir: Path, 
    notebook_name: str,
    frontmatter: str = None
) -> Path:
    """Convert a notebook to a single MDX file."""
    # Make a copy of the notebook to avoid modifying the original
    nb_copy = nbformat.v4.new_notebook(metadata=nb.metadata)
    nb_copy.cells = [cell for cell in nb.cells]
    
    # Extract frontmatter if not provided
    if frontmatter is None:
        frontmatter, frontmatter_idx = extract_frontmatter(nb_copy)
        # Remove frontmatter cell if found
        if frontmatter_idx is not None:
            nb_copy.cells.pop(frontmatter_idx)
    
    # Set up exporter
    exporter = setup_exporter(static_dir, notebook_name)
    
    # Convert to markdown
    body, resources = exporter.from_notebook_node(nb_copy)
    
    # Write markdown file with frontmatter
    with open(output_path, "w") as f:
        f.write(frontmatter + "\n\n" + body)
    
    print(f"Created {output_path}")
    return output_path


def generate_chapter_index_md(
    nb: nbformat.NotebookNode, 
    output_dir: Path, 
    static_dir: Path
) -> Path:
    """Generate index.md file for a chapter with content up to first pagebreak."""
    # Extract frontmatter
    frontmatter, frontmatter_idx = extract_frontmatter(nb)
    
    # Create directories
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find first pagebreak
    first_pagebreak_idx = None
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "raw" and "# !pagebreak" in cell.source:
            first_pagebreak_idx = i
            break
    
    # Create a notebook with cells up to first pagebreak for index.md
    index_nb = nbformat.v4.new_notebook(metadata=nb.metadata)
    
    # Add cells between chapter frontmatter and first pagebreak (or end)
    if frontmatter_idx is not None:
        start_idx = frontmatter_idx + 1
        end_idx = first_pagebreak_idx if first_pagebreak_idx is not None else len(nb.cells)
        index_nb.cells = nb.cells[start_idx:end_idx]
    
    # Output file
    index_path = output_dir / "index.mdx"
    
    # Convert to markdown if we have cells
    if index_nb.cells:
        notebook_name = output_dir.name  # Get notebook name from directory
        return convert_single_file(
            index_nb, 
            index_path, 
            static_dir, 
            notebook_name, 
            frontmatter=frontmatter
        )
    else:
        # Just write frontmatter if no content cells
        with open(index_path, "w") as f:
            f.write(frontmatter)
        return index_path


def split_notebook_cells(nb: nbformat.NotebookNode) -> List[List[nbformat.NotebookNode]]:
    """Split notebook cells into sections based on # !pagebreak markers."""
    # Find all indices of cells containing pagebreaks
    pagebreak_indices = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "raw" and "# !pagebreak" in cell.source:
            pagebreak_indices.append(i)
    
    # If no pagebreaks found, return the entire notebook as one section
    # (excluding chapter frontmatter)
    if not pagebreak_indices:
        return [[cell for cell in nb.cells if "# !chapter" not in cell.source]]
    
    # Split cells into sections
    sections = []
    
    # Process each pagebreak
    for i, pb_idx in enumerate(pagebreak_indices):
        # Get the raw cell with pagebreak
        pb_cell = nb.cells[pb_idx]
        
        # Extract content after pagebreak
        content_after_pb = pb_cell.source.split("# !pagebreak", 1)[1].strip()
        
        # Start a new section
        section_cells = []
        
        # Add the content after pagebreak as a new raw cell if it exists
        if content_after_pb:
            new_cell = nbformat.v4.new_raw_cell(content_after_pb)
            section_cells.append(new_cell)
        
        # Add all cells until the next pagebreak (or end of notebook)
        next_pb_idx = pagebreak_indices[i + 1] if i + 1 < len(pagebreak_indices) else len(nb.cells)
        section_cells.extend(nb.cells[pb_idx + 1:next_pb_idx])
        
        # Add the section if it has cells
        if section_cells:
            sections.append(section_cells)
    
    return sections


def convert_notebook(notebook_path: Path, notebook_dir: Path, root_dir: Path) -> List[Path]:
    """Convert a notebook to markdown files, handling both single and multi-page notebooks."""
    # Read notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Setup static directory for resources
    notebook_name = notebook_path.stem
    static_dir = root_dir / "_intermediate" / "static" / "img"
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if this is a single-pager notebook (no pagebreaks)
    if not has_pagebreaks(nb):
        # For single-pagers, create a single MDX file in the same directory
        output_path = notebook_dir / f"{notebook_name}.mdx"
        result = convert_single_file(nb, output_path, static_dir, notebook_name)
        append_to_gitignore(output_path)
        return [result]
    
    # For multi-page notebooks, we need a subdirectory
    multi_page_dir = notebook_dir / notebook_name
    multi_page_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate .gitignore for the generated notebook directory
    generate_directory_gitignore(multi_page_dir)
    
    # Generate index.md with content up to first pagebreak
    index_path = generate_chapter_index_md(nb, multi_page_dir, static_dir)
    
    # Split notebook into sections
    sections = split_notebook_cells(nb)
    
    if not sections:
        print(f"Warning: No valid sections found in {notebook_path}")
        return [index_path]
    
    # Process each section
    output_paths = [index_path]
    for i, section in enumerate(sections, 1):
        try:
            # Create new notebook with just this section's cells
            section_nb = nbformat.v4.new_notebook(metadata=nb.metadata)
            section_nb.cells = section
            
            # Convert to markdown
            output_path = multi_page_dir / f"autogen-page-{i}.mdx"
            convert_single_file(section_nb, output_path, static_dir, notebook_name)
            
            output_paths.append(output_path)
            
        except Exception as e:
            print(f"Error processing section {i}: {e}")
            continue
    
    return output_paths


if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Convert Jupyter notebooks to multiple markdown files")
    parser.add_argument("notebook", type=Path, help="Input notebook path")
    parser.add_argument("root_dir", type=Path, help="Root directory of the project")
    
    args = parser.parse_args()
    
    if not args.notebook.exists():
        print(f"Error: Notebook {args.notebook} does not exist")
        sys.exit(1)
    
    notebook_dir = args.notebook.parent
    output_paths = convert_notebook(args.notebook, notebook_dir, args.root_dir)
    print(f"\nCreated {len(output_paths)} files")