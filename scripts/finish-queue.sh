#!/usr/bin/env bash
# Run scripts/finish-city.sh for each line of a queue file, one at a time, waiting for new lines; a line "STOP" ends it.
#   line format: <id> "<atlas>:<title>:<period>" ...
cd "$(dirname "$0")/.."
Q="${1:-tools/blender/baked/finish_queue.txt}"
touch "$Q"
while true; do
  line=$(head -n1 "$Q")
  if [[ -z "$line" ]]; then sleep 20; continue; fi
  tail -n +2 "$Q" > "$Q.tmp" && mv "$Q.tmp" "$Q"
  [[ "$line" == "STOP" ]] && break
  while pgrep -f "scripts/finish-city.sh" >/dev/null; do sleep 15; done
  id="${line%% *}"
  echo "$(date +%H:%M) start $id"
  eval "scripts/finish-city.sh $line" > "tools/blender/baked/finish_$id.log" 2>&1
  echo "$(date +%H:%M) done $id: $(tail -3 tools/blender/baked/finish_$id.log | tr '\n' ' ')"
done
