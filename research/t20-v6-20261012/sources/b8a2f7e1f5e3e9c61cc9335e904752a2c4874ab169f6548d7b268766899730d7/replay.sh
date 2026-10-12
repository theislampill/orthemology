#!/bin/bash
set -euo pipefail
exec python3 "$(dirname "$0")/replay.py"
