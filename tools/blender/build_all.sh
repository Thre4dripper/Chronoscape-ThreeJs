#!/usr/bin/env bash
# Rebuild all landmark GLBs headlessly. Set BLENDER to your binary if it is not on PATH.
set -euo pipefail
BLENDER="${BLENDER:-/Users/ijlalahmad/Applications/Blender.app/Contents/MacOS/Blender}"
cd "$(dirname "$0")/../.."
"$BLENDER" -b -P tools/blender/build_all.py -- "${1:-}"
