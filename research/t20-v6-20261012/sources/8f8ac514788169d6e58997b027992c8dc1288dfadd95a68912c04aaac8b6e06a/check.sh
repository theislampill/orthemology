#!/usr/bin/env bash
set -euo pipefail
ROOT=private-locator:8f24556a330b05a11a95
export LEAN_PATH="$(cat "$ROOT/hase-graph-bridge-assembly-20261010/lean_path.txt")"
exec "$ROOT/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 "$@"
