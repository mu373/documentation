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


class HideCellProcessor(Preprocessor):
    """
    This preprocessor removes cells based on cell type and metadata:
    - Code cells with metadata 'hide_input: true' are removed.
    - Markdown cells with metadata 'hide: true' are removed.
    """
    def preprocess(self, nb, resources):
        """
        Process the notebook by filtering out cells based on the specified conditions.
        """
        filtered_cells = []
        for cell in nb.cells:
            # Skip code cells that have 'hide_input' set to True in metadata.
            if cell.cell_type == 'code':
                if cell.get('metadata', {}).get('hide_input', False) is True or cell.get('metadata', {}).get('hide', False) is True:
                    continue

            # Skip markdown cells that have 'hide' set to True in metadata.
            if cell.cell_type == 'markdown' and cell.get('metadata', {}).get('hide', False) is True:
                continue

            filtered_cells.append(cell)
        nb.cells = filtered_cells
        return nb, resources


class EscapePreprocessor(Preprocessor):
    def escape_html(self, text):
        """
        Escape HTML special characters in the given text.
        """
        return escape_html(text)

    def preprocess_cell(self, cell, resources, cell_index):
        if cell.cell_type == "markdown":

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
            # Handle output media
            cell["outputs"] = self._process_output_media(cell["outputs"])
            
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
                    
                    # Save image only if it doesn't exist
                    img_file = self.assets_dir / filename
                    if not img_file.exists():
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
    
    def _process_output_media(self, outputs: List[Dict]) -> List[Dict]:
        """Process and save images and videos in cell outputs.

        This function processes image and video data from cell outputs and saves them 
        in the same asset directory. For videos, not only direct MIME types ("video/...") 
        are handled but also those embedded within HTML (MIME type "text/html") containing 
        <source src="data:video/...">.
        """
        import re
        import base64
        import hashlib

        new_outputs = []
        for output in outputs:
            if "data" in output:
                new_data = {}
                for mime_type, data in output["data"].items():
                    # For images or direct video data
                    if mime_type.startswith("image/") or mime_type.startswith("video/"):
                        # Determine the file extension from the MIME type
                        ext = mime_type.split('/')[-1]
                        # Decode base64 data from a data URL or a raw base64 string
                        if isinstance(data, str):
                            if data.startswith("data:"):
                                # Handle data URLs
                                b64_data = data.split(",", 1)[1]
                                media_data = base64.b64decode(b64_data)
                            else:
                                # Handle raw base64 strings
                                media_data = base64.b64decode(data)
                        else:
                            media_data = data

                        # Generate a filename from the content hash
                        filename = hashlib.md5(media_data).hexdigest()[:12] + '.' + ext

                        # Use the same asset directory for both images and videos
                        asset_dir = self.assets_dir
                        url_prefix = "/img/notebooks"

                        # Create the asset directory if it does not exist
                        asset_dir.mkdir(parents=True, exist_ok=True)

                        # Save the media file if not already present
                        media_file = asset_dir / filename
                        if not media_file.exists():
                            print(f"saving to {media_file}")
                            media_file.write_bytes(media_data)

                        # Update the reference with the new URL
                        new_data[mime_type] = f"{url_prefix}/{self.notebook_name}/{filename}"
                    # For video sources embedded in HTML output
                    elif mime_type == "text/html":
                        # Retrieve the HTML content as a string
                        html_content = data if isinstance(data, str) else ""
                        # Use a regex to detect <source> tags with a video data URL
                        pattern = r'<source\s+([^>]*?)src=["\'](data:video/[^"\']+)["\']'

                        def replace_source(match):
                            pre_attrs = match.group(1)
                            data_url = match.group(2)
                            # Verify that the data URL is in the correct format (e.g., data:video/mp4;base64,...)
                            try:
                                header, b64_str = data_url.split(",", 1)
                            except Exception:
                                return match.group(0)
                            # Example header: "data:video/mp4;base64"
                            mime = header.split(";")[0].split(":")[1]
                            ext = mime.split("/")[-1]
                            try:
                                video_data = base64.b64decode(b64_str)
                            except Exception:
                                return match.group(0)

                            # Generate a filename from the content hash
                            filename = hashlib.md5(video_data).hexdigest()[:12] + '.' + ext

                            # Save the file in the same img directory
                            asset_dir = self.assets_dir
                            url_prefix = "/docs/img/notebooks"
                            asset_dir.mkdir(parents=True, exist_ok=True)
                            video_file = asset_dir / filename
                            if not video_file.exists():
                                print(f"saving to {video_file}")
                                video_file.write_bytes(video_data)
                            new_url = f"{url_prefix}/{self.notebook_name}/{filename}"
                            # Update the src attribute in the <source> tag and return the new tag
                            return f'<source {pre_attrs}src="{new_url}"'

                        new_html = re.sub(pattern, replace_source, html_content)
                        new_data[mime_type] = new_html
                    else:
                        new_data[mime_type] = data
                output["data"] = new_data
            new_outputs.append(output)
        return new_outputs

def setup_exporter(static_dir: Path, notebook_name: str) -> MarkdownExporter:
    """Create and configure a markdown exporter with the necessary preprocessors."""
    return MarkdownExporter(
        preprocessors=[
            HideCellProcessor,
            EscapePreprocessor,
            ResourceProcessor(static_dir, notebook_name)
        ],
        template_name="mdoutput",
        extra_template_basedirs=["./scripts/notebook_convert_templates"],
    )

def export_notebook_cell_to_mdx(
    nb: nbformat.NotebookNode, 
    output_path: Path, 
    static_dir: Path, 
    notebook_name: str,
    frontmatter: str = None,
    notebook_path: str = None
) -> Path:
    """Convert a notebook to a single MDX file with frontmatter.
    
    Args:
        nb: The notebook object
        output_path: Path where the MDX file will be written
        static_dir: Directory for static assets like images
        notebook_name: Name of the notebook (used for image paths)
        frontmatter: Optional frontmatter string. If None, extracted from notebook.
        notebook_path: Path to the notebook file (to construct the edit URL)
    """
    # Make a copy of the notebook to avoid modifying the original
    nb_copy = nbformat.v4.new_notebook(metadata=nb.metadata)
    nb_copy.cells = [cell for cell in nb.cells]
    
    # Extract frontmatter if not provided
    if frontmatter is None:
        frontmatter, frontmatter_idx = extract_frontmatter(nb_copy, notebook_path)
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


def extract_edit_url_from_frontmatter(frontmatter: str) -> str:
    """Extract custom_edit_url from frontmatter if it exists."""
    if not frontmatter:
        return None
        
    match = re.search(r'custom_edit_url:\s*"([^"]+)"', frontmatter)
    if match:
        return match.group(1)
    return None


def ensure_ipynb_extension(url: str) -> str:
    """Ensure the URL points to an .ipynb file."""
    if not url:
        return url
    
    # If URL ends with .mdx, change to .ipynb
    if url.endswith('.mdx'):
        return url[:-4] + '.ipynb'
    # If URL doesn't have an extension, add .ipynb
    elif not url.endswith('.ipynb'):
        return url + '.ipynb'
    return url


def generate_chapter_index_md(
    nb: nbformat.NotebookNode, 
    output_dir: Path, 
    static_dir: Path,
    notebook_path: str = None
) -> Tuple[Path, str]:
    """Generate index.md file for a chapter with content up to first pagebreak."""
    # Extract frontmatter with the notebook path (to get correct edit URL)
    frontmatter, frontmatter_idx = extract_frontmatter(nb, notebook_path)
    
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
        return export_notebook_cell_to_mdx(
            index_nb, 
            index_path, 
            static_dir, 
            notebook_name, 
            frontmatter=frontmatter
        ), frontmatter
    else:
        # Just write frontmatter if no content cells
        with open(index_path, "w") as f:
            f.write(frontmatter)
        return index_path, frontmatter


def split_notebook_cells(nb: nbformat.NotebookNode) -> List[Tuple[List[nbformat.NotebookNode], Optional[str]]]:
    """Split notebook cells into sections based on # !pagebreak markers, returning cells and frontmatter."""
    # Find all indices of cells containing pagebreaks
    pagebreak_indices = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "raw" and "# !pagebreak" in cell.source:
            pagebreak_indices.append(i)
    
    # If no pagebreaks found, return the entire notebook as one section
    # (excluding chapter frontmatter)
    if not pagebreak_indices:
        return [([cell for cell in nb.cells if "# !chapter" not in cell.source], None)]
    
    # Split cells into sections
    sections = []
    
    # Process each pagebreak
    for i, pb_idx in enumerate(pagebreak_indices):
        # Get the raw cell with pagebreak
        pb_cell = nb.cells[pb_idx]
        
        # Extract content after pagebreak
        parts = pb_cell.source.split("# !pagebreak", 1)
        content_after_pb = parts[1].strip() if len(parts) > 1 else ""
        
        # Extract frontmatter if it exists
        section_frontmatter = None
        if content_after_pb:
            # Check if the content has frontmatter
            if content_after_pb.startswith("---"):
                # Extract frontmatter between --- markers
                fm_end = content_after_pb.find("---", 3)
                if fm_end > 0:
                    section_frontmatter = content_after_pb[:fm_end + 3]
                    content_after_pb = content_after_pb[fm_end + 3:].strip()
        
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
            sections.append((section_cells, section_frontmatter))
    
    return sections


def add_edit_url_to_frontmatter(frontmatter: str, edit_url: str) -> str:
    """Add custom_edit_url to section frontmatter."""
    if not frontmatter:
        return f"---\ncustom_edit_url: \"{edit_url}\"\n---\n"
    
    # Check if frontmatter already has custom_edit_url
    if "custom_edit_url:" in frontmatter:
        return frontmatter
        
    # Add custom_edit_url before closing ---
    if frontmatter.endswith("---\n"):
        return frontmatter[:-4] + f"custom_edit_url: \"{edit_url}\"\n---\n"
    elif frontmatter.endswith("---"):
        return frontmatter[:-3] + f"custom_edit_url: \"{edit_url}\"\n---"
    else:
        # If no closing ---, add it
        return frontmatter + f"\ncustom_edit_url: \"{edit_url}\"\n---\n"


def convert_notebook(notebook_path: Path, notebook_dir: Path, root_dir: Path) -> List[Path]:
    """Convert a notebook to markdown files, handling both single and multi-page notebooks."""
    # Read notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Setup static directory for resources
    notebook_name = notebook_path.stem
    static_dir = root_dir / "_intermediate" / "static" / "img"
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate relative path for GitHub edit URL - always use the original notebook path
    original_notebook_path = str(notebook_path.relative_to(root_dir))
    
    # Check if this is a single-pager notebook (no pagebreaks)
    if not has_pagebreaks(nb):
        # For single-pagers, create a single MDX file in the same directory
        output_path = notebook_dir / f"{notebook_name}.mdx"
        result = export_notebook_cell_to_mdx(
            nb, 
            output_path, 
            static_dir, 
            notebook_name, 
            notebook_path=original_notebook_path
        )
        append_to_gitignore(output_path)
        return [result]
    
    # For multi-page notebooks, we need a subdirectory
    multi_page_dir = notebook_dir / notebook_name
    multi_page_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate .gitignore for the generated notebook directory
    generate_directory_gitignore(multi_page_dir)
    
    # Generate index.md with content up to first pagebreak - pass the original notebook path
    index_path, chapter_frontmatter = generate_chapter_index_md(
        nb, 
        multi_page_dir, 
        static_dir, 
        notebook_path=original_notebook_path
    )
    
    # Extract edit URL from chapter frontmatter - this will be the URL to the original notebook
    edit_url = extract_edit_url_from_frontmatter(chapter_frontmatter)
    
    # Split notebook into sections
    sections = split_notebook_cells(nb)
    
    if not sections:
        print(f"Warning: No valid sections found in {notebook_path}")
        return [index_path]
    
    # Process each section - use the same edit URL for all sections
    output_paths = [index_path]
    for i, (section, section_frontmatter) in enumerate(sections, 1):
        try:
            # Create new notebook with just this section's cells
            section_nb = nbformat.v4.new_notebook(metadata=nb.metadata)
            section_nb.cells = section
            
            # Add edit URL to section frontmatter if available
            if edit_url and section_frontmatter:
                section_frontmatter = add_edit_url_to_frontmatter(section_frontmatter, edit_url)
            elif edit_url:
                section_frontmatter = f"---\ncustom_edit_url: \"{edit_url}\"\n---\n"
            
            # Convert to markdown
            output_path = multi_page_dir / f"autogen-page-{i}.mdx"
            export_notebook_cell_to_mdx(
                section_nb, 
                output_path, 
                static_dir, 
                notebook_name, 
                frontmatter=section_frontmatter
            )
            
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