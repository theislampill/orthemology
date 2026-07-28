# R7B — mathematical source/typesetting pipeline: design comparison (Decision 0023)

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE

The design spike compared the four options the audit named. Decision criteria:
GitHub renders source math; PDF renders publication-quality math; deterministic
clean rebuild; current tables/citations/links survive; no missing glyph; source
stays reviewable; the notation registry can drive checks; prose/accessibility
survives; Windows/Linux reproducibility is practical; external tooling is pinned
by version/hash where practical.

## Environment constraint (decisive)

- `pandoc`: **not installed**; no `pypandoc`; no `choco`/`scoop`; only `winget`
  (interactive/admin, unpinned). CI runs on `ubuntu-latest` and installs only the
  Python lock. A pinned pandoc binary would be a real, reviewable CI change.
- `typst` **Python package 0.15.0**: present (drives the current build). It has a
  full math mode. Verified: `$ hat(p)_(A,alpha,t)(m) in Pi_A^partial $` compiles
  to a valid PDF with the math font — real math, zero notdef.

So P2's tooling cannot be provisioned deterministically here; P1's can.

## Options

### P1 — extend the in-repo Markdown→Typst converter (ADOPTED)

`scripts/latex_to_typst_math.py`: a strict, bounded LaTeX-subset → Typst-math
translator wired into `md_to_typst.py` for `$...$` / `$$...$$` / ` ```math `.

| Criterion | Result |
|---|---|
| GitHub renders source math | yes — canonical source is `$...$`/`$$...$$`/```math (MathJax) |
| PDF publication-quality math | yes — Typst math mode; gallery renders every symbol, **zero notdef** |
| Deterministic clean rebuild | yes — unchanged pinned `typst` package; double-build byte-equal preserved |
| Tables/citations/links survive | yes — converter behavior for non-math tokens is unchanged (4 corpus PDFs byte-identical) |
| No missing glyph | yes on the gallery; corpus notdef pinned + tracked until migration |
| Source reviewable | yes — LaTeX is familiar; strict translator fails loudly on unknown constructs |
| Registry-driven checks | yes — `render_map` + `validate_math_source.py` + `validate_pdf_math.py` |
| Prose/accessibility | yes — prose unchanged; math has GitHub text fallback |
| Win/Linux reproducibility | yes — pure Python + pinned typst package; no OS binary |
| External tooling pinned | n/a — no new external tooling |

Cost: the translator is a bounded subset (not a general LaTeX engine); extending
it is a deliberate, tested act. Accepted — the corpus notation is a small,
enumerable inventory (the 33-symbol `render_map`), all of which the translator
covers (proven by the gallery + `tests/test_math_pipeline.py`).

### P2 — GitHub LaTeX → pinned Pandoc Typst writer → pinned Typst (RECOMMENDED TARGET, not adopted here)

The audit's preferred architecture. Pandoc's Typst writer is a mature, general
TeX-math→Typst-math translator, so it would remove the need to maintain an
in-repo subset. **Blocked in this environment:** `pandoc` is not installable
deterministically (see above), and adding a pinned pandoc binary + hash to CI is
a change a candidate pass must not make unilaterally. **Recommendation:** adopt
P2 in the fresh-Fable merged CI if a pinned pandoc is added, running P1 and P2
in parallel with a drift check during transition. Same canonical `$...$` source
serves both, so migrating P1→P2 later requires no source change.

### P3 — Pandoc + LaTeX PDF (rejected)

Highest conventional math quality, but abandons the deterministic Typst/PDF
provenance system (`SOURCE_DATE_EPOCH`, embedded-OFL-font byte-equality,
sidecars), adds a large TeX dependency, and has weaker cross-platform byte
determinism. Not worth discarding the established reproducibility apparatus.

### P4 — canonical Typst source + generated Markdown (rejected)

Typst native math is excellent for the PDF but **does not render on GitHub**, so
the canonical source would not be readable there — violating the "one source,
both surfaces" goal. Acceptable only if one direction is generated and drift-
checked; two hand-authored sources are rejected outright (drift risk). P1 already
gives one canonical source that serves both surfaces, so P4 adds nothing.

## Decision

Adopt **P1** now; record **P2** as the target for the merged CI. Prove P1 on the
notation gallery; gate it with `validate_math_source.py` / `validate_pdf_math.py`;
pin the corpus notdef in `docs/math-migration-status.yaml`; defer the in-place
corpus migration to the reviewed continuation. Tooling pinned: `typst` 0.15.0
(existing lock), `markdown-it-py` 4.0.0 (existing lock); no new dependency.
