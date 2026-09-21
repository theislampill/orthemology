# R7E Sol generic arXiv compatibility verification

Status: `TASK_13_READY_FOR_INDEPENDENT_REVIEW`

This record verifies the declared venue-neutral publication profile. It does
not claim submission, endorsement, acceptance, publication, or compatibility
with an unselected venue-specific template.

## Source and toolchain boundary

- Authoritative source commit:
  `1db15916a3965ccbba101969341bad4cb44ba22b`
- Authoritative source tree:
  `7c7a22d83b9dd86702978bae00c1e3f15d826195`
- Independently reviewed equivalent source commit:
  `1db15916a3965ccbba101969341bad4cb44ba22b`
- Equivalent source tree:
  `7c7a22d83b9dd86702978bae00c1e3f15d826195`
- Source epoch: `1790007430`
- Container:
  `texlive/texlive@sha256:ccf0168bb3dc1e5ba18094131ebb57177f90eca37ab2727bc2d2afb54ad60a51`
- Container configuration:
  `sha256:58b5c7718b4fd239c651873cd267b6c7c82caa5d9a25fe22845d1b8720fff6b1`
- Platform and network: `linux/amd64`, network disabled
- TeX tools: latexmk `4.87`, pdfTeX `1.40.28`, BibTeX `0.99d`,
  kpathsea `6.4.1`
- QA tools: Python `3.11.9`, pypdf `6.14.2`, Poppler `25.07.0`

The authoritative command was:

```text
python scripts/build_pdfs.py --source-commit 1db15916a3965ccbba101969341bad4cb44ba22b
```

The command builds each closed source archive twice in independent clean
directories and requires byte-identical PDFs and bibliography records. A
second invocation with `--check` rebuilt every artifact twice again and
required byte parity with the repository artifacts. Both invocations returned
`TOTAL: 0 failures`.

## Final artifact evidence

| Artifact | Pages | PDF SHA-256 | Source archive SHA-256 | Source manifest SHA-256 |
|---|---:|---|---|---|
| `orthemma-ortheme-systems-draft` | 26 | `e98bd813ce177af6f8a080f7cf5fe1786beb1b3971748717b4b2de727314fce8` | `e10fb927abc26165011094bdfbf10a85e38360181c9eeadef80213622cbfc51d` | `caba109fe72371468a2fba6b3fb50bd7c6d222da0b76c48268824db78ac17a87` |
| `orthemic-core-reference-draft` | 15 | `9a9f814feb6062cf49332bb5deb4edfe31c58b9503b75395c14edd2bafba46da` | `b7b39a02fd007dde8af4104ea61b2ca6fe4a88ef44ca25f1c9eb11856fbf8837` | `ce2457888b9e6ed2a4aeb8a5fa3f2f964d4fd9beb1e1ffa1984a9a99ce743abe` |
| `orthability-ground-of-intelligibility-draft` | 8 | `dc2e04ed58e581fb0cecb9fdd7619f04143d68ad5f48a7c803070f67a1d03ef3` | `bdc2b1d8ddb05a41ff23b071cca7df985db4465cc24226c11cfdf0c63442e94e` | `d0e6dfd866b285c5b762461ced436e26b5168da23eb922ab45f05a19475ef7fc` |
| `orthability-divine-speech-athari-draft` | 6 | `4affb68da10224c70d63db923397f19ca14fed242faa39e1f5dbdfe43ab28474` | `f3204c6ce69478c7e654e4a31a8f00478de6c506c9735c426dcac10215fd6df3` | `cb5d1c4299de41a985a5c7626282c625216a82ce3732cf88331158d2d6644fcd` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `23f6ede49277396073752570ca8b6a9942c5aba84fa0700dd58140ae4e81c896` | `2945d60a169059cdcbfd20941968d51a970ab1ea9e5007bd39f4a9bb005ed9a1` | `73a212d395825927141320fc0892cd351cf096e89446fcf35a94f66dd83d24c6` |
| `notation-gallery` | 2 | `ec057d86ac5f3edc37ea85c3d54ddf5d5e1f3ce7b828f4a5f615bc789692928f` | `4ad1b67a22d9583adb58048e564c6faa7b51b4fd5bc2884c9b2db2e9cf4989ac` | `a4e3354d2434dfc1e0000da6b031e949fce228e9bbfc9a40e2b6139fb68dbc68` |

Total final page count: `62`.

## Verified gates

- The seven authoritative Markdown sources map exactly to six declared
  artifacts.
- The ordered source-heading inventory contains exactly 162 H2-H4 headings.
  The test-pinned ordered digest is
  `624cfd2a6d166ba73b432a54bbfc9179ede988fe24c9c3fde6f5ef830e655dd3`.
- PDF heading matching is ordered, duplicate-sensitive, Unicode NFKD and
  casefold normalized, and rejects empty normalized source keys.
- The main manuscript preserves the source-owned starred section 15 appendix:
  `\onecolumn` immediately precedes the section 15 heading, and `\twocolumn`
  immediately precedes the section 16 heading. A fabricated `\appendix`
  command is rejected.
- Every generated non-ASCII code point has a package-local mapping. UTF-8
  diagnostic output is explicit.
- The closed package policy separates the eight ordered packages declared
  directly by every generated `main.tex` (`amsmath`, `amssymb`, `booktabs`,
  `geometry`, `hyperref`, `microtype`, `natbib`, and `xcolor`) from the single
  compatibility-only declaration, `fvextra`, in
  `pdftex-unicode-compat.tex`. The direct and compatibility sets are
  disjoint, their union is the exact supported set, and transitive TeX
  dependencies remain lock identities rather than direct source declarations.
- Every source archive has sorted repository-relative regular-file members,
  normalized metadata, declared dependencies, no links or devices, no path
  traversal, no shell escape, and no stale auxiliary files.
- Every archive clean-build records the expected `main.tex` and generated
  `main.bbl`. The exact empty-bibliography disposition is
  `EMPTY_BIBLIOGRAPHY_NO_CITATIONS`.
- Every PDF parses, is unencrypted, contains no JavaScript, has no image
  XObjects, and has extractable text on every page.
- Structure validation found zero issues. Link counts by artifact are
  `1, 7, 11, 9, 3, 0` in the table order above.
- All fonts reported by Poppler are embedded and subset Type 1 fonts with
  Unicode maps. No Type 3 font occurs.
- Build-log validation rejects unresolved references or citations, multibyte
  verbatim corruption, runaway page output, and any overfull box above the
  declared `5 pt` tolerance.
- The final all-page raster review is recorded in
  `R7E-SOL-PDF-VISUAL-QA.md`.
