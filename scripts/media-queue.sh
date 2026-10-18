#!/usr/bin/env bash
# Fetch Commons pictures for each city id listed in the media queue, one at a time; "STOP" ends it.
cd "$(dirname "$0")/.."
Q=tools/blender/baked/media_queue.txt
touch "$Q"
while true; do
  id=$(head -n1 "$Q")
  if [[ -z "$id" ]]; then sleep 30; continue; fi
  tail -n +2 "$Q" > "$Q.tmp" && mv "$Q.tmp" "$Q"
  [[ "$id" == "STOP" ]] && break
  echo "$(date +%H:%M) media $id"
  python3 tools/content/fetch_media.py "$id" > "tools/blender/baked/media_$id.out" 2>&1
  echo "$(date +%H:%M) done $id: $(tail -1 tools/blender/baked/media_$id.out)"
done
