# R7E Sol generic arXiv compatibility verification

Status: `TASK_13_READY_FOR_INDEPENDENT_REVIEW`

This record verifies the declared venue-neutral publication profile. It does
not claim submission, endorsement, acceptance, publication, or compatibility
with an unselected venue-specific template.

## Source and toolchain boundary

- Authoritative source commit:
  `aee5c7389b57ec7c3150d8fee3b3e398195d1395`
- Authoritative source tree:
  `766a3cfd57058d56538a0571fcff176ca44288b3`
- Independently reviewed equivalent source commit:
  `aee5c7389b57ec7c3150d8fee3b3e398195d1395`
- Equivalent source tree:
  `766a3cfd57058d56538a0571fcff176ca44288b3`
- Source epoch: `1785167892`
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
python scripts/build_pdfs.py --source-commit aee5c7389b57ec7c3150d8fee3b3e398195d1395
```

The command builds each closed source archive twice in independent clean
directories and requires byte-identical PDFs and bibliography records. A
second invocation with `--check` rebuilt every artifact twice again and
required byte parity with the repository artifacts. Both invocations returned
`TOTAL: 0 failures`.

## Final artifact evidence

| Artifact | Pages | PDF SHA-256 | Source archive SHA-256 | Source manifest SHA-256 |
|---|---:|---|---|---|
| `orthemma-ortheme-systems-draft` | 25 | `f6ec5827674e97614f5040134e8e6bc65407c9b76cbb1e4c14d461f60876c29b` | `84d1736e78486ecc1c91c64aa5a5cc4f98e1414a581ecbe684eba3ad09be8608` | `d9dd0d6f8889ea1db75eeda8c80c24ba68091ae24e0647795561a58973c3ffe6` |
| `orthemic-core-reference-draft` | 14 | `caaa008ce2f7fc26f060a291fdc4f2e0102445b37fb5204e0bef0d3271eadaec` | `e1eb737006855ab9e26bf71d1f21051c61ee244bb827adb1616a24ddfdf18fce` | `360fea9d56f46782725f8d738e7e259bbddbd5cd9ae5a054ea8f841161770f81` |
| `orthability-ground-of-intelligibility-draft` | 8 | `73f258620e52e72f4eec2c220cbae1f6b51d6ed7c1ee950753ca2f42a9dff9e3` | `a9f32faf4b7f5a09aa7ddbb60dca63461eb268e4b0221e2c7a65cda3093fda29` | `4e33495b8c1430be00f73e95d1be79cff48fa00442a8335fa551384284f62082` |
| `orthability-divine-speech-athari-draft` | 6 | `b52c20c2a56f894196ad8f3c96a2d09dcda1a9bb4484dbc9d59894d3c6786be9` | `0e6644ca794761be2ccf215c0f6dc89f417e77a7806fe18c00c1e0828f49ea2e` | `ed640c8431186bcb4049c169b44946071ebd01edc93946399a89c6abb78cf1f0` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `d751b33900cfdee6c6de97df3fcec6f0704bd2a2ff707e59efa2da343b93c403` | `9134851ff363fe4a29120458092260b20cda3074e54245899c0c04b445ddc791` | `60ef089a6d5ff816e927e8a71c4aded7c22bd9a0862c44d36501c3fd8bba5421` |
| `notation-gallery` | 2 | `3afc21e00ae807d18d1c5158e82f698c5a90a179b08d77c501ed1480051ea8f4` | `fdfe18c6f193ae9e5e655611995a5c286a5fbd08dd79880871a869e816e3730a` | `160c5e47098ef23336223b93d2ad8fb733d21c219bf82fa2555181d469671946` |

Total final page count: `60`.

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
