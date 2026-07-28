# R7B — Phase A2: mathematical-typesetting baseline (read-only reproduction)

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE
**Pass:** R7B (Opus 4.8 requested = surfaced; no substitution)
**Tree:** child branch `candidate/r7b-deep-noetic-latent-math` off PR #8 head `b053860`
**Method:** deterministic, offline. The counts below use the *same* tokenizer the
build converter uses (`markdown-it-py`, CommonMark + table + strikethrough), so a
"code_inline" span here is exactly what `scripts/md_to_typst.py` sees.

This is a read-only reproduction of the independent audit's §7 (and prompt A2.1–A2.7).
No source was edited to produce it.

## Finding matrix

| # | Audit claim | Verdict | Evidence |
|---|---|---|---|
| A2.1 | `md_to_typst.py` maps inline code to `#raw` | **reproduced** | `scripts/md_to_typst.py:39` — `code_inline` → `"#raw(" + _typst_str(t.content) + ")"`; fences/`code_block` → `#raw(block: true, …)` (line 135). The converter has **no math mode**; it never emits Typst `$…$`. |
| A2.2 | math-like notation is encoded mainly in inline-code spans | **reproduced** | Of the publication sources' inline-code spans, the majority are typed formulas, not identifiers. Samples: `` `TokenAdequate(μ̄, e) ⟺ MetaInst(μ̄, μ) ∧ Compatible(μ̄, A(e)) ∧ …` ``, `` `AdequatePathError(e) := ¬V1(e) ∧ PathwayAdequate(e)` ``, `` `μ⃗ = (μ₁,…,μ_k; ≼)` ``. |
| A2.3 | ~351/212 (manuscript) and ~385/217 (core) math-like inline-code spans | **reproduced (approx.)** | manuscript **351** total (audit: 351 — exact), **229** math-like; formal core **390** total (audit: 385, +5), **253** math-like. Totals match within ~1%; the math-like subset is heuristic-dependent (this pass's heuristic is slightly broader than the audit's, hence 229/253 vs 212/217 — same magnitude, same conclusion). |
| A2.4 | rendered PDFs show raw underscores / stars / ASCII arrows | **reproduced** | The `#raw` path renders monospace literals: the core PDF episode-signature line shows `hand_in, hand_out` with literal underscores; `O*(m; A)` renders its `*` literally; ASCII process arrows (`-->`, `->`, `↪`) render as literal glyphs, not typeset relations. |
| A2.5 | `μ⃗` and `C⃗` lose/misrender the base glyph in the core PDF | **reproduced — worse than stated** | `pypdf` text extraction of `artifacts/orthemic-core-reference-draft.pdf` renders the episode signature `μ⃗` and `C⃗` as `\x00\x00` (NUL / notdef): base letter **and** combining arrow are both lost. U+20D7 (combining arrow above) appears **0** times in the extracted text. By contrast `p̂` (p + U+0302 circumflex) *does* survive — so the specific failure is the combining **arrow** over μ/C hitting a mono font with no composed glyph and no U+20D7. |
| A2.6 | current QA still passes | **reproduced** | Full `validate.yml` run from clean checkout: **40/40 green** (39 `run:` blocks; the manifest step is one block, two commands). PDFs rebuild byte-identical; `RELEASE-MANIFEST.sha256` matches the tree. |
| A2.7 | GitHub renders the source as code, not math | **reproduced** | The formulas in A2.2 are all single-backtick `code_inline` spans; GitHub renders `` `…` `` as inline `<code>`, never as MathJax. GitHub math requires `$…$` / `$$…$$` / ```` ```math ```` fences, none of which appear in the corpus. |

## Why the green suite does not catch this

`validate_repo.py` and the PDF QA in `build_pdfs.py --check` verify **deterministic
bytes**, **no raw-Markdown leakage**, and **text-structure** — not mathematical
semantics or glyph completeness. A page can be byte-reproducible and still render
`\x00\x00` for `μ⃗`. The defect is therefore invisible to the current gates, which is
exactly why Phase C must add `validate_math_source.py` and `validate_pdf_math.py`
(math-in-code detection, combining-accent ban in publication math, tofu/notdef
detection in extracted PDF text, notation-gallery drift).

## Source → PDF map (for Phase C targeting)

| Target | Sources |
|---|---|
| `orthemma-ortheme-systems-draft` (manuscript) | `manuscript/orthemma-ortheme-systems-revised-draft.md` |
| `orthemic-core-reference-draft` (formal core) | `theory/orthemic-core-formalization.md`, `theory/orthemic-multi-actor-conflict-note.md` |
| `orthability-ground-of-intelligibility-draft` | `companion/orthability-and-the-ground-of-intelligibility.md` |
| `orthability-divine-speech-athari-draft` | `companion/orthability-divine-attributes-and-speech-athari.md` |

Per-file inline-code / math-like counts (this pass): manuscript 351/229; core
`orthemic-core-formalization.md` 390/253; `orthemic-multi-actor-conflict-note.md`
14/11; companion (neutral) 31/16; companion (Atharī) 16/2.

## Disposition

The mathematical-typesetting defect is **real and publication-blocking** (A2.5 in
particular). It is a *rendering/source-discipline* defect, **not** a notation
redesign: the established meanings (`O*(m; A)`, `Inst_A`, `μ̄`, `p̂`, `μ⃗`, `C⃗`,
episode signature, verdict formulas) must be preserved exactly through any
migration. Phase B decides the pipeline before any corpus edit.
