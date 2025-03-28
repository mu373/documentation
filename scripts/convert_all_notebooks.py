#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import argparse
import time
from typing import List, Dict

# Import the convert_notebook function from the notebook_split_convert module
from notebook_split_convert import convert_notebook

def find_notebooks(directory: Path) -> List[Path]:
    """Find all Jupyter notebook files recursively in a directory."""
    notebooks = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('.'):
                notebooks.append(Path(root) / file)
    return notebooks

def convert_all_notebooks(root_dir: Path) -> Dict:
    """Convert all notebooks in the directory to markdown files."""
    notebooks = find_notebooks(root_dir)
    
    start_time = time.time()
    if not notebooks:
        print(f"No notebooks found in {root_dir}")
        elapsed_time = time.time() - start_time
        return {"total": 0, "success": 0, "failed": 0, "files_created": 0, "elapsed_time": elapsed_time }
    
    print(f"Found {len(notebooks)} notebooks to convert")
    
    stats = {
        "total": len(notebooks),
        "success": 0,
        "failed": 0,
        "files_created": 0
    }
    
    
    for i, notebook_path in enumerate(notebooks, 1):
        print(f"\n[{i}/{len(notebooks)}] Converting {notebook_path.relative_to(root_dir)}...")
        
        try:
            notebook_dir = notebook_path.parent
            output_paths = convert_notebook(notebook_path, notebook_dir, root_dir)
            
            stats["success"] += 1
            stats["files_created"] += len(output_paths)
            
            print(f"  ✓ Created {len(output_paths)} files")
        except Exception as e:
            stats["failed"] += 1
            print(f"  ✗ Failed: {str(e)}")
    
    elapsed_time = time.time() - start_time
    
    return {**stats, "elapsed_time": elapsed_time}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert all Jupyter notebooks in a directory to markdown files")
    parser.add_argument("root_dir", type=Path, help="Root directory of the documentation project")
    parser.add_argument("--dry-run", action="store_true", help="Only find notebooks without converting them")
    
    args = parser.parse_args()
    
    if not args.root_dir.exists() or not args.root_dir.is_dir():
        print(f"Error: {args.root_dir} is not a valid directory")
        sys.exit(1)
    
    print(f"Documentation root directory: {args.root_dir}")
    
    if args.dry_run:
        notebooks = find_notebooks(args.root_dir)
        print(f"Found {len(notebooks)} notebooks:")
        for nb in notebooks:
            print(f"  - {nb.relative_to(args.root_dir)}")
        sys.exit(0)
    
    stats = convert_all_notebooks(args.root_dir)
    
    print("\n" + "="*60)
    print(f"Conversion completed in {stats['elapsed_time']:.2f} seconds")
    print(f"Total notebooks: {stats['total']}")
    print(f"Successfully converted: {stats['success']}")
    print(f"Failed: {stats['failed']}")
    print(f"Total markdown files created: {stats['files_created']}")
    print("="*60)
    
    if stats['failed'] > 0:
        sys.exit(1)
