#!/usr/bin/env bash
set -euo pipefail
# Run only in an isolated external research environment. Does not touch a repository.
command -v elan >/dev/null || { printf '%s\n' 'Install an authenticated Elan distribution first; no pipe-to-shell bootstrap is supplied.' >&2; exit 2; }
elan toolchain install leanprover/lean4:v4.19.0
elan run leanprover/lean4:v4.19.0 lean --version
elan run leanprover/lean4:v4.19.0 lake --version
# Expected: Lean 4.19.0, commit 6caaee842e94; Lake 5.0.0-6caaee8.
# execute_formal.py independently rejects a mismatch before dependency/build work.
