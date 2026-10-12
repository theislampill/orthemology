# Continuation-Complete Orthings

Research supplement v1 — 8 September 2026.

## Read

- `continuation_complete_orthing.pdf`: typeset research supplement.
- `continuation_complete_orthing.md`: principal mathematical source.
- `continuation_complete_orthing.tex`: complete generated LaTeX source.
- `verification.json`: exact coverage and limits of the finite checks.
- `horizon_dimensions.json`: tested horizon-dependent dimensions.
- `SELF_REVIEW.md`: self-review, repaired checker issue, remaining review gates.
- `provenance.json`: input hashes, repository pin, source and authority scope.

This is a supplement to *Graded Representations, Witnessed Revision, and Inquiry Landscapes* v1, not a silent replacement or repository edit. The prior packet and supplied fluid manuscripts are referenced rather than redistributed.

## Main addition

Witnessed discharge receives a continuation-sensitive information contract. The manuscript proves a sharp minimax summary defect, an action-observation completion criterion, a minimum exact continuous memory dimension, and an exact horizon law for pairwise binary updates. It derives approximate-memory and augmentation bounds, a hidden-game equilibrium obstruction, and independent-mixing safety constraints.

The general ingredients have substantial prior art, explicitly compared in Appendix C. This is not a claim of new general duality, predictive-state, Nash, or nonnegative-rank theory. No formal MENISCUS_CANDIDATE/MENISCUS_REACHED status, independent review, empirical validation, or Lean verification is claimed.

## Reproduce finite checks

Use Python 3.11 or later, preferably the versions recorded in `provenance.json`:

```sh
python -m venv .venv
# Activate the environment using the command appropriate for your OS.
python -m pip install -r requirements.txt
python verify_frontier.py
```

The script writes `verification.json` and `horizon_dimensions.json`. A failed assertion exits unsuccessfully. Only a fresh successful run licenses a PASS claim: an old receipt may remain on disk after an interrupted run. SciPy proposes LP witnesses; rational arithmetic checks the stated inequalities/equalities. Floating proposals are not proof authority.

The topological lower bounds and the entropy argument are paper proofs, not certified by enumeration. The approximate-dimension LP checks certify rational upper bounds and do not claim generic exact optimisation. The separate sharp-defect tests require exact primal-dual equality.

## Build from Markdown

Requirements: Pandoc with Lua filters, XeLaTeX, and the standard TeX packages named in the preamble. Latin Modern OpenType fonts are requested by installed filenames; no font files are included.

```sh
pandoc continuation_complete_orthing.md --from=markdown+tex_math_dollars --to=latex --standalone --template=build_support/template.tex --lua-filter=build_support/layout.lua --top-level-division=section -o continuation_complete_orthing.tex
xelatex -interaction=nonstopmode -halt-on-error continuation_complete_orthing.tex
xelatex -interaction=nonstopmode -halt-on-error continuation_complete_orthing.tex
```

The delivered LaTeX can also be compiled directly without Pandoc. PDF byte-for-byte reproducibility is not claimed because TeX metadata may vary; exact regeneration of the LaTeX source was checked. The release PDF was rendered and visually inspected.

## Authority

Repository basis: `theislampill/orthemology@f50dc1aee52356cc6adbef342387576b02afc124`. Read-only. No commit, issue, release, scientific adoption, representation-arm promotion, or owner-controlled ledger was changed. The mathematical reference model is not identified with mental experience or physical reality.
