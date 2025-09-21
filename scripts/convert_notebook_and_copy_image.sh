#!/usr/bin/env bash
# Usage: ./scripts/run_convert.sh <notebook_path>

set -e  # stop if any command fails

FILEPATH="$1"

bun run nb-convert-single "$FILEPATH"
bun run nb-copy-image