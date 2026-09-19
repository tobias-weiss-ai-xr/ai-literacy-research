#!/bin/bash
# Launch or resume the incremental fetch round on this host.
# Env: MAILTO (OpenAlex contact), FROM_IDX (resume query index, optional)
pkill -f '[f]etch_openalex.py' 2>/dev/null
sleep 1
cd /tmp/fetch || exit 1
export PYTHONUTF8=1
export OPENALEX_MAILTO="${MAILTO:-ki-kompetenz-training@tobias-weiss.org}"
args=(--months 2 --sleep 0.5)
if [ -n "${FROM_IDX:-}" ]; then args+=(--from "$FROM_IDX"); fi
nohup python3 scripts/fetch/fetch_openalex.py "${args[@]}" \
  > /tmp/fetch/run.log 2>&1 &
echo "PID=$!"
