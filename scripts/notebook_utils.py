from pathlib import Path
from typing import Tuple
import nbformat

# GitHub configuration
GITHUB_USERNAME = "mu373"
GITHUB_REPO = "documentation"

def escape_html(text):
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

def extract_frontmatter(nb: nbformat.NotebookNode, notebook_path: str = None) -> Tuple[str, int]:
    """Extract frontmatter from notebook if it exists.
    
    Args:
        nb: The notebook object
        notebook_path: Path to the original notebook file (to construct the edit URL)
    
    Returns:
        Tuple[str, int]: The frontmatter content and the index of the frontmatter cell.
    """
    frontmatter = ""
    cell_index = None
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "raw" and "# !chapter" in cell.source:
            frontmatter = cell.source.split("# !chapter", 1)[1].strip()
            # Replace "chapter-title:" with "title:" in frontmatter
            frontmatter = frontmatter.replace("chapter-title:", "title:")
            cell_index = i
            break
    
    # Default frontmatter if none found
    if not frontmatter:
        frontmatter = "---\ntitle: Untitled\n---\n"
    
    # Add custom edit URL if notebook path is provided
    if notebook_path:
        # Make sure frontmatter has the proper format
        if not frontmatter.startswith("---\n"):
            frontmatter = "---\n" + frontmatter
        if not "---" in frontmatter[3:]:
            frontmatter = frontmatter + "\n---\n"
        
        # Remove trailing "---" to add our custom_edit_url
        if frontmatter.endswith("---\n"):
            frontmatter = frontmatter[:-4]
        
        # Insert custom_edit_url before the closing "---"
        # Always use the original notebook path for the edit URL
        edit_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}/blob/main/{notebook_path}"
        frontmatter_lines = frontmatter.split("\n")
        
        # Find the position to insert the custom_edit_url
        insert_pos = -1
        for i, line in enumerate(frontmatter_lines):
            if line.strip() == "---" and i > 0:
                insert_pos = i
                break
        
        if insert_pos > 0:
            frontmatter_lines.insert(insert_pos, f"custom_edit_url: \"{edit_url}\"")
        else:
            # If no closing "---" found, add it at the end
            frontmatter_lines.append(f"custom_edit_url: \"{edit_url}\"")
            frontmatter_lines.append("---")
        
        frontmatter = "\n".join(frontmatter_lines)
    
    return frontmatter, cell_index

def has_pagebreaks(nb: nbformat.NotebookNode) -> bool:
    """Check if notebook contains pagebreak markers."""
    for cell in nb.cells:
        if cell.cell_type == "raw" and "# !pagebreak" in cell.source:
            return True
    return False


def append_to_gitignore(file_path: Path):
    """Append a file pattern to .gitignore in the same directory."""
    gitignore_path = file_path.parent / ".gitignore"
    
    # Create gitignore if it doesn't exist
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write(f"{file_path.name}\n")
    else:
        # Append to existing gitignore if the pattern isn't already there
        with open(gitignore_path, "r") as f:
            content = f.read()
        
        if file_path.name not in content:
            with open(gitignore_path, "a") as f:
                f.write(f"\n{file_path.name}\n")
    
    return gitignore_path


def generate_directory_gitignore(dir: Path):
    """Create .gitignore file for multi-page notebook directories."""
    gitignore_path = dir / ".gitignore"

    # This ignores auto-generated markdown files
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write("autogen-*.mdx\n")
            f.write("index.mdx\n")
    
    return gitignore_path

