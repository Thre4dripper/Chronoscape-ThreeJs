#!/usr/bin/env bash
# After tools/blender/bake_all.py: footprints from the new models, validate, re-bake the map plates, build.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/content/build_rome.py
pnpm validate
pnpm plates:bake
pnpm exec tsc -p tsconfig.json --noEmit
pnpm exec vite build >/dev/null && echo "build ok"
