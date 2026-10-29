#!/usr/bin/env bash
# After a city's data and model builders are written (tools/content/cities/<id>/, tools/blender/models/cities/<id>.py):
# bake its models, render plans (footprints) and elevations, rebuild its content, fetch pictures, list it, bake its plates.
#   scripts/finish-city.sh <id> "<atlas-id>:<map title>:<period-id>" [...]
# The plates go to .plate-cache/ (build output; the baker starts its own dev server). Steps can be skipped with SKIP="bake media plates".
set -euo pipefail
cd "$(dirname "$0")/.."
id="$1"; shift
export BAKE_CPU="${BAKE_CPU:-1}"
BLENDER="${BLENDER:-/Users/ijlalahmad/Applications/Blender.app/Contents/MacOS/Blender}"
skip() { [[ " ${SKIP:-} " == *" $1 "* ]]; }
python3 tools/content/build_city.py "$id"
if ! skip bake; then
  "$BLENDER" -b -P tools/blender/bake_all.py -- "$id/" > "tools/blender/baked/bake_$id.out" 2>&1
  grep -c '"tris"' tools/blender/baked/bake_log.jsonl >/dev/null
  python3 tools/content/build_city.py "$id"   # footprints from the rendered plans
fi
if ! skip elevations; then
  "$BLENDER" -b -P tools/blender/render_elevations.py -- "$id/" > "tools/blender/baked/elev_$id.out" 2>&1 || echo "elevations failed (see tools/blender/baked/elev_$id.out)"
fi
if ! skip media; then
  # pictures come from Wikimedia, which rate-limits: a separate runner (scripts/media-queue.sh) fetches them one city at a time
  echo "$id" >> tools/blender/baked/media_queue.txt
fi
python3 tools/content/register_city.py "$id" "$@"
if ! skip plates; then
  node scripts/bake-plates.mjs "$id"
fi
npm run validate 2>&1 | grep -E "^(error|ok) .*$id|error\(s\)" || true
