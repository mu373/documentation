#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import shutil

import nbformat
from nbconvert.exporters import MarkdownExporter
from nbconvert.preprocessors import Preprocessor
import yaml


class EscapePreprocessor(Preprocessor):
    def escape_html(self, text):
        """
        Escape HTML special characters in the given text.

        Args:
            text (str): The text to escape.

        Returns:
            str: The escaped text with special HTML characters replaced
                 by their corresponding HTML entities.
        """
        # The ampersand must be replaced first to avoid double-escaping.
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        # text = text.replace('"', "&quot;")
        # text = text.replace("'", "&#39;")
        return text

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
                        print("saving to {}".format(img_file))
                        img_file.write_bytes(img_data)
                        
                        # Update reference
                        new_data[mime_type] = f"/img/notebooks/{self.notebook_name}/{filename}"
                    else:
                        new_data[mime_type] = data
                output["data"] = new_data
            new_outputs.append(output)
        return new_outputs


def parse_frontmatter(cell_source: str) -> Optional[Dict]:
    """Parse YAML frontmatter from a cell if it exists."""
    if not cell_source.startswith('---\n'):
        return None
    
    parts = cell_source.split('---\n', 2)
    if len(parts) < 3:
        return None
    
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

def generate_chapter_index_md(nb, output_dir: Path, static_dir: Path):
    """Generate index.md file for a chapter with content up to first pagebreak."""
    # Find chapter frontmatter and first pagebreak
    chapter_frontmatter_index = None
    index_frontmatter = None
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "raw" and "# !chapter" in cell.source:
            index_frontmatter = cell.source.split("# !chapter", 1)[1].strip()
            chapter_frontmatter_index = i
            break
    
    # Check if frontmatter exists 
    if index_frontmatter is None:
        print("Warning: No chapter frontmatter found in notebook")
        index_frontmatter = "---\ntitle: Untitled\n---\n"
    else:
        # Replace "chapter-title:" with "title:" in frontmatter
        index_frontmatter = index_frontmatter.replace("chapter-title:", "title:")
    
    # Create directories
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find first pagebreak
    first_pagebreak_index = None
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "raw" and "# !pagebreak" in cell.source:
            first_pagebreak_index = i
            break
    
    # Create a notebook with cells up to first pagebreak for index.md
    index_nb = nbformat.v4.new_notebook(metadata=nb.metadata)
    
    # Add cells between chapter frontmatter and first pagebreak (or end)
    if chapter_frontmatter_index is not None:
        start_index = chapter_frontmatter_index + 1
        end_index = first_pagebreak_index if first_pagebreak_index is not None else len(nb.cells)
        index_nb.cells = nb.cells[start_index:end_index]
    
    # Write the index file with preprocessed content if there are cells
    index_path = output_dir / "index.mdx"
    
    # Use preprocessors if we have cells to process
    if index_nb.cells:
        notebook_name = output_dir.name  # Get notebook name from directory
        
        # Setup exporters with the same preprocessors used for regular conversions
        exporter = MarkdownExporter(
            preprocessors=[
                EscapePreprocessor,
                ResourceProcessor(static_dir, notebook_name)
            ],
            template_name="mdoutput",
            extra_template_basedirs=["./scripts/notebook_convert_templates"],
        )
        
        # Convert to markdown
        body, resources = exporter.from_notebook_node(index_nb)
        
        # Write with frontmatter + processed body
        with open(index_path, "w") as f:
            f.write(index_frontmatter + "\n\n" + body)
    else:
        # Just write frontmatter if no content cells
        with open(index_path, "w") as f:
            f.write(index_frontmatter)
    
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
    
    # Skip the first section since it's included in index.mdx
    # Process each pagebreak instead
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


def convert_section_to_markdown(
    original_nb: nbformat.NotebookNode, 
    cells: List[nbformat.NotebookNode], 
    notebook_dir: Path,
    static_dir: Path,
    notebook_name: str,
    section_num: int
) -> Tuple[str, Path]:
    """Convert a section of cells to markdown."""
    # Create new notebook with just this section's cells
    nb = nbformat.v4.new_notebook(metadata=original_nb.metadata)
    nb.cells = cells

    
    # Setup exporters with resource handling
    exporter = MarkdownExporter(
        preprocessors=[
            EscapePreprocessor,
            ResourceProcessor(static_dir, notebook_name)
        ],
        template_name="mdoutput",
        extra_template_basedirs=["./scripts/notebook_convert_templates"],
    )
    
    # Convert to markdown
    body, resources = exporter.from_notebook_node(nb)
    
    # Determine output path
    output_path = notebook_dir / f"autogen-page-{section_num}.mdx"
    
    return body, output_path


def generate_gitignore(dir: Path):
    gitignore_path = dir / ".gitignore"

    # This ignores auto-generated markdown files
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write("autogen-*.mdx\n")
            f.write("index.mdx\n")
    
    return gitignore_path

def convert_notebook(notebook_path: Path, notebook_dir: Path, root_dir: Path) -> List[Path]:
    """Convert a notebook to multiple markdown files based on pagebreak splits."""
    # Read notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Setup directory structure
    notebook_name = notebook_path.stem
    notebook_dir = notebook_dir / notebook_name
    static_dir = root_dir / "_intermediate" / "static"
    
    # Create directories
    notebook_dir.mkdir(parents=True, exist_ok=True)
    static_dir.mkdir(parents=True, exist_ok=True)

    # Generate .gitignore for the generated notebook directory
    generate_gitignore(notebook_dir)
    
    # Generate index.md with content up to first pagebreak
    generate_chapter_index_md(nb, notebook_dir, static_dir)
    
    # Split notebook into sections (starting after first pagebreak)
    sections = split_notebook_cells(nb)

    if not sections:
        print(f"Warning: No valid sections found in {notebook_path}")
        return []
    
    # Process each section
    output_paths = []
    for i, section in enumerate(sections, 1):
        try:
            body, output_path = convert_section_to_markdown(
                nb,
                section, 
                notebook_dir,
                static_dir,
                notebook_name,
                i
            )
            
            # Write markdown file
            with open(output_path, "w") as f:
                f.write(body)
            
            output_paths.append(output_path)
            print(f"Created {output_path}")
            
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