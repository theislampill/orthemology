# Graded Representations, Witnessed Revision, and Inquiry Landscapes

**Version 1 — 8 September 2026.** A conditional mathematical extension of Orthemology, formalising the accompanying dialogue. Research draft; not repository adoption or a Lean/kernel-verified development.

## Read

- `orthing_formalisation_v1.pdf`: 35-page typeset manuscript, including contents, source register, correction ledger and verification scope.
- `orthing_formalisation_v1.tex`: complete, editable, standalone LaTeX source.
- `orthing_formalisation_v1.md`: the same substantive manuscript in Markdown with LaTeX mathematics.

The manuscript contains 9 theorems, 17 propositions, 3 corollaries, 4 numbered counterexamples and 5 numbered definitions. These include classical and elementary results; the counts are not claims of mathematical novelty.

The central constructions are the finite-record/interaction encoder, target-preserving and future-safe compression criteria, witnessed obligation-history retention, independent inquiry landscapes, optional finite games, and conditional dynamical certificates. The chat itself remains an informal exemplar, not a retrospectively certified canonical episode or game.

## Verify the examples

Python 3.10 or later; standard library only:

```sh
python verify_examples.py --output verification.json
```

The delivered receipt records 11 passing finite test groups. The script aborts on a failed assertion. It does not prove the manuscript, authenticate semantic witnesses, run an empirical Orthemology programme, or audit a fluid proof.

## Build the PDF from the delivered LaTeX

Use a TeX installation with LuaLaTeX, Latin Modern fonts, and the ordinary packages listed in the preamble:

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error orthing_formalisation_v1.tex
```

No external bibliography, figures, local font files or repository checkout is required. Standard font packages are dependencies; no font files are included in this delivery.

## Regenerate LaTeX from Markdown

The delivered LaTeX was generated using Pandoc 3.1.11.1 with the included layout template and filter:

```sh
pandoc orthing_formalisation_v1.md \
  --from=markdown+tex_math_dollars+smart --to=latex \
  --standalone --number-sections \
  --template=build_support/template.tex \
  --lua-filter=build_support/layout.lua \
  -o orthing_formalisation_v1.tex
```

The layout filter preserves prose and mathematics while adding page-break controls, breakable code paths and unnumbered appendix headings. Changes to the title should also update the template's three-line title display. Compilation on another TeX version may change pagination and PDF bytes; byte-reproducibility across systems is not claimed.

## Provenance and checksums

`provenance.json` identifies the repository basis, source scopes, uploaded-paper hash and production checks. `SELF_REVIEW.md` records the mathematical and delivery checks without claiming an independent review. `MANIFEST.sha256` hashes all delivered files except the manifest itself. Verify from this directory with:

```sh
sha256sum -c MANIFEST.sha256
```

Repository basis: `theislampill/orthemology@f50dc1aee52356cc6adbef342387576b02afc124`. Sources are cited, not bundled as a full repository copy. No GitHub content, owner ledger, experimental arm, or adoption status was changed.
