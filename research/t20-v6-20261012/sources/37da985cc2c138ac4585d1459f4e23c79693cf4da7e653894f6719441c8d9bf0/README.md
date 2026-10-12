# T17 to T19 public reading projections

This package contains the nine reviewed reading projections of the final T17–T19 DOCX deliverables, prepared on 7 October 2026. It preserves the original authored research, mathematical companions, source guides and Arabic reading index. The originals remain the custody authority. No repository file has been changed by this preparation.

The public documents are in `documents/`. `PROJECTION_MANIFEST.json` identifies each original DOCX, original SHA-256 and byte length, public Markdown SHA-256 and byte length, and its exact conversion-diff and mathematical-map bindings. `CONTENT_REVIEWS.json` records the bounded conversion reviews. `SHA256SUMS` binds every other file in this package.

## Reading and integration scope

These are derived historical reading projections, not a new edition of the research claims. They retain AI authorship, the 5–6 October 2026 source dates, original qualifications, source voices, unresolved questions, disagreement and inherited assurance limits. The leading notice in each document is new custody and rendering context; the source body follows in its original order. Preparing these files adds no new theorem, kernel verification, empirical replay, primary-source reading, outside human-specialist endorsement or canonical adoption.

The full original body census covers 1,757 nonempty paragraphs, 853 native mathematical objects and 390 hyperlinks. The body text and equation positions match the original paragraph sequence under whitespace normalization. The two equation maps preserve every original native mathematical tree and its projected TeX. All 271 Arabic-index internal links resolve to the same original bookmark heading text; external link labels and destinations are retained.

The nine Markdown files use GitHub-flavoured Markdown with TeX mathematics. Supported heading, list, link and emphasis structure is retained. Directional spans and bookmark anchors use HTML where needed. The original Word fonts, page layout, line wrapping, empty-paragraph geometry and page-number fields are not reproduced. Internal references to document pages still refer to the original DOCX. Native page images were used selectively for conversion review, not to certify full layout equivalence.

## Explicit conversion repairs

Three defects in a plain Pandoc export were corrected:

1. The converter places title and subtitle paragraphs in metadata that a non-standalone Markdown export omits. The source title blocks, including AI attribution and dates, were restored before the body.
2. Some native mathematical spacing becomes a spacing command inside a TeX text block. The projection moves only those spacing commands into math mode with a terminating space. There are 49 such replacements in T17 and 35 in T18.
3. The converter substitutes an apostrophe for native U+2032 PRIME. The projection restores the native prime character in five T17 positions across three objects and two T18 positions across two objects.

The math fixes affect 39 T17 and 23 T18 objects. Every before/after TeX string appears in the applicable conversion-diff. All 853 final equations convert to MathML without warnings. Each native-to-MathML mathematical token sequence was compared after removal of layout-only spacing; no mathematical-token difference remains. This is a conversion check, not an independent mathematical proof or a guarantee about every downstream Markdown/TeX renderer.

Direct hyperlink underline is represented by ordinary Markdown hyperlink styling. Word internal bookmark names are mapped to their actual heading anchors, with every mapping recorded. The GFM reader canonically composes three decomposed accented-name occurrences in one T19 paragraph during round-trip checking; the Markdown itself retains the original character sequence. The audit records that parser normalization explicitly.

There are no source body tables, images, tracked changes, footnote or endnote references in these nine documents. The empty comments and separator-only note parts were inspected. Running page-number fields and blank footer text are omitted as layout. The Arabic index’s substantive running title and AI-author credit are retained in its notice as well as in the source body.

## Publication boundary

Only the authored final-document content, its original identities, the declared conversion records and scoped reviews are included here. This package contains no source books, source PDFs, OCR, page images, attached conversation transcript, private review bodies, participant-level data, credentials, machine logs or recovery notes. Bibliographic links, including the six inherited Drive identity locators in T17, do not assert public access or grant permission to redistribute their targets.

T16 is already projected and is not repeated. T20 work, evidence ZIP members and the final verification JSON files are outside this nine-document projection package. Their distinct publication and review decisions remain separate. The existing scientific and source-acquisition holds are not lifted by conversion.

The current successor public-text check, including decoded JSON strings, is applied to this exact package and recorded in `VERIFICATION.json`. This is not a full successor-registry validation. Any later repository admission must bind these exact bytes to the corresponding source and review records without changing historical evidence or extending acceptance.
