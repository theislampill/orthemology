# R3 PDF visual and structural QA

**Date:** 2026-07-20 · **Pipeline:** `scripts/build_pdfs.py` v2 — markdown-it-py structural parse (`scripts/md_to_typst.py`, strict: any unhandled Markdown construct raises; content can never be silently skipped) → Typst 0.15.0 (pinned PyPI compiler wheel), `ignore_system_fonts=True` so only Typst's embedded OFL fonts (New Computer Modern family; DejaVu Sans Mono) are visible — no private fonts, and the build is machine- and OS-independent.

## Reproducibility (the R2 defect, fixed)

- **No wall-clock value enters any artifact.** The document date derives from `SOURCE_DATE_EPOCH` (env override, else the source commit's committer time); metadata shows `CreationDate = ModDate = D:<date>000000Z` from that epoch.
- **Double build enforced in-process:** every `build` compiles each document twice and fails unless byte-identical — PASS for all four.
- **Clean-rebuild gate in CI:** `--check` re-derives each PDF from the sidecar's recorded provenance inputs and requires byte-equality with the committed artifact (plus source-hash drift detection and the full text QA) — PASS locally; verified again on Linux CI (cross-OS byte identity is the point of `ignore_system_fonts`).
- **Two-stage provenance:** sidecars record the **source revision** (`source_commit`, `source_date_epoch`, per-source SHA-256) and state explicitly that the **artifact revision** is the git commit introducing the artifact (`git log -- artifacts/`), removing the R2 ambiguity.

## Automated text-structure QA (every build and every `--check`)

Per PDF: no `|---|` pipe-table rows, no literal `> ` blockquote markers, no raw `[text](http…)` Markdown links, no standalone `---` rules in the extracted text — all PASS (each of these was PRESENT in the R2 artifacts); every source H1/H2 heading present in the PDF text layer (alphanumeric-normalized; smart-quote aware) — PASS; page counts recorded in sidecars.

## Visual pass (every page rendered to PNG at 110 ppi via `--png`; inspected)

| Artifact | Pages | Findings |
|---|---|---|
| orthemma-ortheme-systems-draft | 30 | clean title page with all five DRAFT/status lines, source revision, SOURCE_DATE_EPOCH line, and a real two-level TOC with page numbers; real ruled tables (contributions; verdict tables); inline code properly set in mono; no artifacts |
| orthemic-core-reference-draft | 20 | dense formal pages verified: `∩ ∈ ∉ ⟹ ∅ ≠ →` and script letters (`𝒦 𝒲`) all render; code blocks and the implication table clean |
| orthability-ground-of-intelligibility-draft | 10 | block quotes properly indented; rivals table renders as a real table; transliteration diacritics correct |
| orthability-divine-speech-athari-draft | 7 | §2 block quote and sense note clean; corrected 20:11–12 citation visible; transliteration (ʿ, ā, ī, Ḥ, ṣ) renders correctly |

## Documented rendering rules (disclosed, not silent)

- Internal repository links (relative `.md` targets) render as *emphasized link text* — no in-PDF target exists; in this corpus the text is the path or document title. External `http(s)` links are real, working PDF links (typst `#link`).
- Typst applies smart quotes to prose (curly quotes in output for straight quotes in source) — typographic improvement, accounted for in the heading QA.
- Two cosmetic notes carried from R2 are **resolved**: the combining-arrow and ⊨ glyph warnings of the fpdf2 pipeline do not recur (New Computer Modern coverage); title spacing is proper.

## Comparison to the R2 baseline

R2 (fpdf2 line-printer): all four hashes changed across builds seconds apart; live `/CreationDate`; raw Markdown throughout; silent line-skip path; `--check` verified only sidecar source-hashes. R3: byte-reproducible; deterministic metadata; structural rendering with hard failure on unhandled constructs; `--check` rebuilds and compares bytes. The fpdf2 implementation survives only in git history.
