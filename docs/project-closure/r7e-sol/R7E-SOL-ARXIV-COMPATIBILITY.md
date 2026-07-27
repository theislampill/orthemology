# R7E Sol generic arXiv compatibility verification

Status: `TASK_13_READY_FOR_INDEPENDENT_REVIEW`

This record verifies the declared venue-neutral publication profile. It does
not claim submission, endorsement, acceptance, publication, or compatibility
with an unselected venue-specific template.

## Source and toolchain boundary

- Authoritative source commit:
  `1703a783d9b25a9cfa93370c4a1a0b568fa497d0`
- Authoritative source tree:
  `8edff88e8df79e8d0792d441c65227b9729403a9`
- Independently reviewed equivalent source commit:
  `9dc0094cc6df908fbba1b965bb36d5f3f00979c0`
- Equivalent source tree:
  `8edff88e8df79e8d0792d441c65227b9729403a9`
- Source epoch: `1785161731`
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
python scripts/build_pdfs.py --source-commit 1703a783d9b25a9cfa93370c4a1a0b568fa497d0
```

The command builds each closed source archive twice in independent clean
directories and requires byte-identical PDFs and bibliography records. A
second invocation with `--check` rebuilt every artifact twice again and
required byte parity with the repository artifacts. Both invocations returned
`TOTAL: 0 failures`.

## Final artifact evidence

| Artifact | Pages | PDF SHA-256 | Source archive SHA-256 | Source manifest SHA-256 |
|---|---:|---|---|---|
| `orthemma-ortheme-systems-draft` | 26 | `b729627330f6bf8db89e29ad3395aa99a2e1dd88a39658f0bde3abf36f0e101d` | `8163233681f8fa7f3b0ac36b3920fe76b6f83e6d5f3d1b6645515dcfa133f26d` | `4787ab1676b7e45c6501dc115399763f7e0b70452717209ecdc83caf8cd7a01a` |
| `orthemic-core-reference-draft` | 14 | `e6ed45e667aafdafc742c675236135d893f8f789f3a73cda2f0e148cc3103d03` | `9397141987cf5c64327eff7c04970010e0e29ef47668b130ca578a2141ed93e5` | `c6b7cc22cf101252d29017617d15af0b7fb4bc1fa01bcb617aab70291daa54e8` |
| `orthability-ground-of-intelligibility-draft` | 8 | `ee3de78b45ac91dd12300b53e28c6cfbadbeb9791c539d721c8f377cb0d318f9` | `ea12982363894706f209ac6e4580e8181d3b71adf99bd22b9ef6faa8301022e9` | `db415681662b88ac55cc4ecf5cfb79172847177f3a8cd7fc21594ed40205b485` |
| `orthability-divine-speech-athari-draft` | 6 | `52089693b97b606b1f5b35525965df76fbc620a882dda9c36a7c623315f2414e` | `75f85ed682c3418c8699bd37a5da90ab0bfc549687979571dfdc08db5eaded0a` | `22594cb99a871ec455f1ca955708a80c46a5b4fbd412fa56334d50b8866e25e4` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `cf333a15261a01c2acddccff240a5c601a9e1760df6e592947e58aed355e2474` | `34f3405493264dfbb699b6a7a633a655a87ea300fa2382db8c6df83eab565993` | `fedf2c8116cfd48763afbaaaf1dec5ac75e7df67fe4d539633a19904c18eff8f` |
| `notation-gallery` | 2 | `5a707c3c8b7c4b6d8149f79a115fbbbec95f8e27b81206806a89dc6b21d69142` | `224ce76340e29288d5c1e9f39332a2be93b601986381a8a2d2f4b903a2ca8584` | `15b02e1f29031f56c61a06fe8216dae8b70773a8df467e5897c18b80c9114bdd` |

Total final page count: `61`.

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
