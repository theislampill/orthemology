#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for program in pandoc xelatex python; do
  command -v "$program" >/dev/null || { echo "Missing dependency: $program" >&2; exit 1; }
done
python -m unittest discover -s verification -p 'test_*.py'
python verification/verify_modal_frontier.py
python verification/verify_uniform_foundation.py
python verification/verify_integrated_models.py
python verification/verify_audit_game.py
python formal/make_certificates.py
python formal/nd_checker.py
pandoc orthability_modal_grounding.md \
  --from=markdown+tex_math_dollars --to=latex --standalone \
  --template=build_support/template.tex --lua-filter=build_support/layout.lua \
  --top-level-division=section -o orthability_modal_grounding.tex
xelatex -interaction=nonstopmode -halt-on-error orthability_modal_grounding.tex
xelatex -interaction=nonstopmode -halt-on-error orthability_modal_grounding.tex
