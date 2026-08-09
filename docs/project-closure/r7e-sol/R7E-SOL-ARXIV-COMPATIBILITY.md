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
| `orthemma-ortheme-systems-draft` | 26 | `30ee85f4f03e835b112744f8dbfec18cb040154ce883eb3f19727258f1dade2d` | `4c1cf063fbbaf21d418b109209e6308af2a7a9b9a6d564112291245ca1b8cc49` | `c9c22952a79ad3e878f41eab5d74e2977e60e3197f6bb73b00e95704c0889b54` |
| `orthemic-core-reference-draft` | 15 | `e9d06ca5823cb446997ad344c79b65ccc633a631ae43dde5edc1fcc0f400e660` | `8f8296bab21a70154cf98401fcedf0516a81bdfb353d6ce18d943691f333e697` | `fa44ee04565663adf6c8c897a5414832b2da2a5ab4d0ba110c79630cf4cc784a` |
| `orthability-ground-of-intelligibility-draft` | 8 | `4eb35f434ee44063a62edbcc0fe9b97a62375cbf50d452f78432dd7507746150` | `7d8f4f411e67585259637a5a1552a6ffa408e720ca9f70903b720ede3795c841` | `97dfeb6dde2ca37ba5f82c6cfd2f53a2b564662bfe1243738001813ceaa72b3a` |
| `orthability-divine-speech-athari-draft` | 6 | `d29ca3ab9082810bf8fa0526537e7e380b1385db63ebea54fb63ff062761ac9a` | `ed8a4df949856b61aad3f980dd1ca384546a683048ab67b5e85438e518cd8686` | `c6770f329c75e8b51625d97f39297c66a44b306284b82df2d100079934829e5e` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `349f2c67882b0c2995a56c3fb487559405fc9d10c6ab8ab77c9d2e68ceecad21` | `9f7bc721c8972f92f01f75d44c4412cd6d313abd2fe0e2e0ee1266a7c7d5fb78` | `1ba0c376658b87c8d85648db48fc0259d15d154cd8cebc949287524e4f482186` |
| `notation-gallery` | 2 | `6b0cd1f5b1292b560d6472b33b0ba54614ce2b92b0297acebe555da4df958eff` | `863275421be792cc725b0da79d641f1b1fdddd7773d97d4935486b79442e0669` | `dc22131725fa6114c636fd9abe7bb612f0f4470e9a1e1427da6b665ef7569b3a` |

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
