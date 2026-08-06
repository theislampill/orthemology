# AR8R PDF visual QA and formatting repair V2

## Scope and authority

This receipt covers the six public publication PDFs rebuilt from the exact
repository source state below. It is a visual-formatting and deterministic-build
receipt. It does not alter theorem, source, adoption, novelty, historical-recovery,
champion, meniscus, or natural-closure authority.

```text
source commit: d7309d30612ff85ed8f94b93d4a5a610c18b3ea9
source tree: cded0130b092d2d13e288d6829298ec3f651e982
SOURCE_DATE_EPOCH: 1786022580
toolchain: publication/toolchain-lock.yaml
visual page coverage: 62 / 62
accessibility tagging: ACCESSIBILITY_TAGGING_DEFERRED_BOUNDED
```

The pinned pdfLaTeX toolchain does not provide the PDF tagging support needed
for a truthful tagged-PDF claim. All six PDFs remain untagged. This is a bounded
toolchain limitation, not a publication-readiness PASS.

## Exact rebuilt artifacts

| Artifact | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| `artifacts/orthemma-ortheme-systems-draft.pdf` | 26 | 391631 | `1ff1b5f2c6b1930d333088cc1150219319d1d14315c2327c8fff9f42420d2dc0` |
| `artifacts/orthemic-core-reference-draft.pdf` | 15 | 308462 | `776cbe9915d6d7ad80fd622d8835031566077cce7cd47d0246731210655966f7` |
| `artifacts/orthability-ground-of-intelligibility-draft.pdf` | 8 | 232010 | `93e42076d086a8c2731709930b5b6e525898a509e54575bf9fca65a8c7d5c354` |
| `artifacts/orthability-divine-speech-athari-draft.pdf` | 6 | 188379 | `ba66cb32871e4885a0ba68aadcf6311cf74ab103fc06266a45b86e2855c5b105` |
| `artifacts/dynamic-orthing-noetic-learning-orthability-draft.pdf` | 5 | 187398 | `644c5fc2c5e5efc552bff6502a29b06772cccdf23503919448c85abe7dadf258` |
| `artifacts/notation-gallery.pdf` | 2 | 172802 | `8d31c02b684297c891612f8fcac9aa70de007de9c2618ef550392ce746f2677f` |

## Repairs

The Markdown-to-LaTeX generator and manuscript sources were repaired at their
source-of-truth surfaces, then the committed LaTeX derivatives and all public
artifacts were regenerated.

- Prose ASCII quotation marks now render as paired TeX opening and closing
  quotes, including pairs whose contents cross emphasis or other Markdown token
  boundaries. Literal quotation marks inside code remain literal.
- Seven display-mathematics blocks in the core manuscript were migrated from raw
  monospace code to rich display math. Wide formulas received reviewed alignment
  and line breaks rather than overflowing a column.
- Long list items and table rows receive page-space guards. Tables with seven or
  more rows use the breakable row layout, which repaired the cramped dependency
  and reason/revelation tables.
- Reference sections use ragged-right composition in narrow columns to avoid
  excessive interword expansion.
- Raw less-than ordering prose that produced corrupt inverted glyphs was replaced
  with explicit prose ordering.
- The precedence display was reflowed so no operator is duplicated or stranded.
- A compatibility display was made self-contained across a page boundary.
- Long custody and source paths use tested compact verbatim tiers. The longest
  exact path now remains readable without the former stray right-edge fragment.
- Sparse final pages were checked for content completeness. They are short
  terminal sections or bibliography continuations, not clipped or abruptly
  truncated content.

## Visual review chain

The first independent 62-page review returned `BLOCK` and identified corrupt
ordering glyphs, reversed closing quotes, a path-edge fragment, a stranded
precedence operator, cramped tables, over-expanded reference prose, and sparse
terminal pages requiring completeness checks. Those findings were preserved as
the repair checklist rather than overridden by the successful build.

After repair, the main review inspected the newly rendered exact pages containing
every reported defect. A second independent reviewer then rendered the exact six
hashes listed above at 240 DPI and directly inspected all 62 pages without using
prior-render identity shortcuts. The rereview found no remaining visual defect.
Its cross-document text checks found 217 paired opening and closing curly quotes,
zero reversed quote sequences, zero straight double quotes, zero U+230B or U+00A1
corruption markers, zero replacement glyphs, and zero compressed `V2bP` aliases.
All 62 pages had nonempty Poppler text.

```text
initial independent visual review: BLOCK
repair implementation: COMPLETE
exact-artifact independent rereview: PASS
exact pages independently inspected: 62 / 62
remaining visual defects: 0
```

## Automated gates

At this repair boundary:

```text
LaTeX generator tests: 59 / 59 PASS
six-PDF deterministic build: 6 / 6 PASS
PDF build failures: 0
PDF math-glyph regression gate: PASS
math-source strict-subset and inventory gate: PASS
```

The whole-repository validation, generated-state convergence, privacy scan, and
exact-head CI are separate pre-merge gates and are not implied by this receipt.
