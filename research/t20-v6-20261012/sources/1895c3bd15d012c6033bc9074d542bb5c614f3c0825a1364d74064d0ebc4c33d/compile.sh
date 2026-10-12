#!/bin/bash
set -euo pipefail
cd [OMITTED_PRIVATE_MACHINE_PATH]
source hase-source-family-computability-20261010/env.sh >/dev/null
export LEAN_PATH="$PWD/hase-actual-source-enumerability-20261010/validation:$PWD/hase-coded-rule-templates-20261010/validation:$PWD/hase-certificate-code-validity-20261010/validation:$PWD/hase-auxiliary-checker-computability-20261010/validation:$PWD/hase-telescope-code-validity-20261010/validation:$PWD/hase-coded-mixed-transformations-20261010/validation:$PWD/hase-exact-syntax-validity-20261010/validation:$PWD/hase-coded-poly-transformations-20261010/validation:$PWD/hase-coded-scope-computability-20261010/validation:$LEAN_PATH"
for m in "$@"; do
 .toolchains/lean-4.19.0-linux/bin/lean --trust=0 -o hase-actual-source-enumerability-20261010/validation/$m.olean hase-actual-source-enumerability-20261010/$m.lean > hase-actual-source-enumerability-20261010/validation/$m.log 2>&1 || { cat hase-actual-source-enumerability-20261010/validation/$m.log; exit 1; }
 cat hase-actual-source-enumerability-20261010/validation/$m.log
done
