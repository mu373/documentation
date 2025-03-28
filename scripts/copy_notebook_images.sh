#!/bin/bash

set -euo pipefail

# Copy notebook images from _intermediate/static/notebooks to static/notebooks
# This script should be run from the root of the documentation directory

# Check if running from the correct directory
if [ ! -d "_intermediate/static/img/notebooks" ]; then
  echo "Error: _intermediate/static/img/notebooks directory not found."
  echo "Please run this script from the root of the documentation directory."
  exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "static/img/notebooks"

# Use rsync to copy files
# -a: archive mode (preserves permissions, timestamps, etc.)
# -v: verbose output
# --progress: show progress during transfer
# -z: compress file data during transfer
# --prune-empty-dirs: don't create directories that don't have files
echo "Copying notebook images to static directory..."

rsync -avz --prune-empty-dirs "_intermediate/static/img/notebooks/" "static/img/notebooks/"

if [ $? -eq 0 ]; then
  echo "Images successfully copied to static/img/notebooks/"
else
  echo "Error: Failed to copy images."
  exit 1
fi

echo "Done."
exit 0
