# PR #21 — PDF layout repair report V1 (Codex finding 4)

All repairs were made in the Markdown-to-LaTeX generator and the Markdown
sources; no generated PDF or generated `main.tex` was hand-edited. All six PDFs
were regenerated through the pinned container pipeline
(`scripts/build_pdfs.py`, exit 0, `TOTAL: 0 failures`), and every page of every
regenerated PDF was rendered and visually inspected — see
`AR8R-FABLE-R1-PDF-PAGE-BY-PAGE-VISUAL-QA-V1.csv` (61 pages: 25 + 15 + 8 + 6 +
5 + 2; the totals changed from 26/14 to 25/15 for the two repaired documents).

## Generator repairs (`scripts/generate_latex_sources.py`)

1. **Orphan/widow guards** — `\clubpenalty`, `\widowpenalty`,
   `\displaywidowpenalty`, `\brokenpenalty` at 10000, plus `\raggedbottom` so
   the penalties can bind in the two-column flushbottom layout. Repairs the
   stranded "causes." (orthemma p1) and stranded-bullet (divine-speech p5)
   class.
2. **Heading keep-with-next** — `\needspace{4\baselineskip}` emitted before
   every section/subsection/subsubsection, skipped when the heading
   immediately follows a `\onecolumn`/`\twocolumn` switch (the arxiv source
   validator requires that adjacency). Repairs the isolated-§1.5 class.
3. **Clean part boundaries** — `\clearpage` before every `part*`, so companion
   papers start on a fresh page. Repairs the orthemic-core p12 concatenation.
4. **Breakable tables at ≥3 columns** — `BREAKABLE_TABLE_COLUMN_THRESHOLD`
   lowered 5 → 3, so wide tables render as the pipeline's existing
   normal-flow labeled row blocks instead of fragmented narrow `tabular`s.
   Repairs the orthemma p3/p6/p7 class.
5. **Contained verbatim** — remaining code fences render inside a
   `\needspace{3\baselineskip}` + `\small` group, so machine-readable blocks
   stay visually contained.
6. `needspace` added to the closed package policy in lockstep:
   `EXPECTED_DIRECT_PACKAGES`, `docs/publication-profile.yaml`
   (direct + supported), and `scripts/validate_arxiv_source_package.py`.

## Source repairs (typography only; no meaning changes)

- `manuscript/orthemma-ortheme-systems-revised-draft.md`: all eleven raw
  indented pseudo-math blocks converted to proper typesetting — the fibre
  formula, apprehension flow (ASCII diagram → two display-math chains plus a
  feedback sentence), encounter line, successor set, indexed-notation list
  (→ itemized inline math), merger-gap formula, evidence-channel record
  (→ stacked displays), mis-scoped-pass equivalence, metaortheme record,
  residual-disposition set (→ prose), and revision operator. The
  machine-managed somnus claim-status projection block is deliberately
  retained verbatim as machine-readable form (required repair 8).
- `theory/orthemic-multi-actor-conflict-note.md`: the seven-entry raw derived-
  definitions block converted to an itemized list with inline math.

The PDF source-provenance pin (`source_commit` / tree / epoch in
`docs/publication-profile.yaml` and `publication/toolchain-lock.yaml`) was
advanced with each source change, as the pipeline's custody design requires.

## Verification

- `python scripts/build_pdfs.py` — all six PASS, exit 0.
- `python scripts/build_pdfs.py --check` — deterministic rebuild convergence
  (run in Phase E validation on the final head).
- 61/61 regenerated pages visually inspected by the reviewer recorded in the
  CSV; every defect in the Codex page ledger and both additional Fable
  findings from the pre-repair audit are repaired.
- Accepted cosmetic residual (recorded, not repaired): notation-gallery p2's
  episode-signature display ends with a short ragged final line.

## Accessibility disposition — explicit bounded deferral

All six PDFs remain **untagged** (no PDF structure tree): the pinned
latexmk/pdfLaTeX container pipeline does not load a tagging package, and
retrofitting tagged-PDF support (e.g. LaTeX tagpdf) would change the locked
toolchain and is out of scope for this repair. Recorded disposition:
`ACCESSIBILITY_TAGGING_DEFERRED_BOUNDED` — the PDFs are draft research
artifacts, are not presented as publication-ready for accessibility purposes,
and the reading order verified here is visual only. Closing the deferral
requires a toolchain decision (owner-gated, alongside FABLE-R1-CI-01-style
lock amendments).
