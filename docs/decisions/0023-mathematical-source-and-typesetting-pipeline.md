# Decision 0023 — Mathematical source and typesetting pipeline

**Date:** 2026-07-21 · **Authority:** R7B owner authorization (Opus candidate pass) · **Status:** adopted · **Reopens nothing:** Decisions 0001–0022 stand; this is a typography/rendering layer over the existing notation (Decision 0005), not a notation redesign — every symbol keeps its meaning.

**Provenance:** produced under model substitution to Opus 4.8 (R7B requested Opus; surfaced = Opus). OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

## Problem

`scripts/md_to_typst.py` mapped every inline-code and fenced-code token to Typst
`#raw` monospace. The publication sources carry mathematics in backtick code
spans (manuscript 351 / formal core 390 inline-code spans, the majority
math-like; `docs/project-closure/r7b/R7B-PDF-MATH-BASELINE.md`). Consequences,
reproduced this pass:

- GitHub renders the notation as code, never as mathematics;
- the PDF renders underscores/stars/ASCII arrows literally and, worse, renders
  the formal-core episode-signature vectors `μ⃗` and `C⃗` as `\x00\x00`
  (notdef): base letter *and* combining arrow U+20D7 lost (26 notdef glyphs in
  the core PDF, 6 in the manuscript PDF);
- the green QA suite never caught it — it checks deterministic bytes and raw-
  Markdown leakage, not mathematical semantics or glyph completeness.

## Decision

**Canonical mathematical source is GitHub-compatible LaTeX.** Mathematics is
written as `$...$` (inline), `$$...$$` (display), or a ` ```math ` fence.
GitHub renders these through MathJax; the PDF pipeline renders them as real
Typst math. Backticks are reserved for code identifiers, file paths, JSON/YAML
keys, semantic registry IDs discussed as literal strings, and shell commands —
never for mathematics. One canonical source renders correctly in both places;
there is no second authoritative notation.

**Rendering path — P1 (implemented):** a strict, bounded in-repo translator,
`scripts/latex_to_typst_math.py`, converts the LaTeX subset the corpus uses into
Typst math markup, compiled by the already-pinned `typst` PyPI package (0.15.0).

- **Zero new dependencies.** The pinned toolchain and byte-reproducibility
  (double-build equality, `SOURCE_DATE_EPOCH`) are unchanged.
- **Strict, no silent fallthrough.** An unknown LaTeX command raises
  `MathConvertError`, which surfaces as a build `ConversionError` — a typo fails
  the build rather than mis-rendering. This mirrors the converter's existing
  no-silent-skip contract.
- **Combining accents are banned in publication math source** (U+0300–U+036F,
  U+20D7): math must use `\hat` / `\bar` / `\vec`. This removes the exact source
  antipattern behind the notdef defect.

**Recommended target — P2 (not adopted here):** a pinned Pandoc Typst-writer
pipeline is the audit's preferred long-term architecture (mature TeX→Typst math
translation). It is **recorded as the migration target for the fresh-Fable
merged CI if and when a pinned `pandoc` binary + hash is added**, with a drift
check against P1. It is **not adopted in this pass** because `pandoc` cannot be
provisioned deterministically in the R7B environment (see
`docs/project-closure/r7b/MATH-PIPELINE-DESIGN-COMPARISON.md`); a candidate pass
must not unilaterally add an un-pinnable non-Python binary to CI.

## Guarantees and gates

- **Notation gallery.** `docs/notation-gallery.md` → `artifacts/notation-gallery.pdf`
  renders every normative symbol (registry `render_map`) and every structural
  construct from the design spike (episode signature, aligned equations, set
  comprehensions, underbraces, labeled arrows, a table with inline math) as real
  mathematics with **zero notdef** — the audit's proof-of-concept, repo-
  integrated and byte-reproducible. The core `μ⃗`/`C⃗` defect renders correctly
  here as `$\vec\mu$`/`$\vec C$`.
- **`scripts/validate_math_source.py`** — render_map↔symbol bijection, gallery
  drift, translation coverage, and the combining-accent ban across all math
  source.
- **`scripts/validate_pdf_math.py`** — every PDF's notdef count must equal the
  value pinned in `docs/math-migration-status.yaml`; migrated documents must be
  notdef-free; no U+FFFD; gallery equation-loss guard.
- **`docs/math-migration-status.yaml`** — the migration ledger. It pins the
  known corpus notdef counts so the defect is tracked, cannot silently grow, and
  cannot be silently declared fixed.

## Scope and boundary (candidate)

- The four existing corpus PDFs are **untouched this pass** and remain
  byte-identical (verified): the pipeline is proven on the gallery without
  risking the fragile corpus.
- **In-place corpus migration is the reviewed continuation.** Migrating the
  ~480 meaning-bearing formulas is deliberately deferred to a fresh-Fable-
  reviewed pass, where each hunk's meaning-preservation is checked — precisely
  because "a typography migration must not become a notation redesign." The
  validators make that migration safe and mechanical: a migrated document sets
  `migrated: true` / `expected_notdef: 0` in the same commit that migrates its
  source, and verdict labels (e.g. `V3c`) must be wrapped `\operatorname{...}`.
- No empirical, human, or theological claim is created. This is typography.
