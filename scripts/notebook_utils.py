#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib
import base64
import shutil

import nbformat
import yaml

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

def extract_frontmatter(nb: nbformat.NotebookNode) -> Tuple[str, int]:
    """Extract frontmatter from notebook if it exists.
    
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

