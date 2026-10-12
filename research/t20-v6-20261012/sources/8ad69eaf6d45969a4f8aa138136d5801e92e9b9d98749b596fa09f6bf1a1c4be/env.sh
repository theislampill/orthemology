W=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
R=$W/hase-mixed-substitution-independent-review-20261010
export LEAN_PATH="$R/fresh-lib:$W/hase-dependent-substitution-20261010/validation:$W/hase-church-structural-20261010/validation:$(cat "$W/hase-generic-rigidity-review-20261010/lean_path.txt"):$W/hase-closed-church-completeness-review-20261010/fresh-lib:$W/hase-complete-development-review-20261010/fresh-lib:$W/hase-effective-instance-assessment-20261010/validation"
LEAN=$W/.toolchains/lean-4.19.0-linux/bin/lean
