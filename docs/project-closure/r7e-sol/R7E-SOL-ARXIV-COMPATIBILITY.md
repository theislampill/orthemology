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
| `orthemma-ortheme-systems-draft` | 26 | `ceb2dc682547667dde20ec95150b7581670d836b2d1f9ea3e804767f54e3d2c9` | `c716d26698667a48100494614f71eb399c418449ec251c399b6ddfd02c15764d` | `06f7fa17cd39e364a1a2ca4e2ecb6d71b2aa2e990fcb06324e07d138fe703a2d` |
| `orthemic-core-reference-draft` | 14 | `d3c405415f82702247a96fab1865c63a1b3c62789d6b3e9e3e6076eca21f481c` | `daf01421420553ce243bf44802979862407d4df7d6cc1089f4b3bd2333dafdb3` | `91de8f5c23edcdca8d57287232581b45e243c0258bc67b0dc527d70707386a32` |
| `orthability-ground-of-intelligibility-draft` | 8 | `a6a2de01830781834c60f1775bd257b5b426b1307cfea422261776b58de0a9ee` | `47ac696e329f36f6543a93fd9fcd1ac1c37227af7ef4a362ae891c2d48df7cdf` | `8ebe230236d2a738a1858a90faa7cbccc015ead09e1847912008e6f09e2625bb` |
| `orthability-divine-speech-athari-draft` | 6 | `ab22cd7d7a467c24c52e59f530c52af73f9416591cb2a0a8e2eef5c3a6ea53f7` | `29d8be14a117470c2f3ac82d12b0fba2c6a94293e9d6112cbcc426689cd92fd8` | `df4a022bb37de39015e131778b469dbe61de41b8bcb96a5ced72f33d604e17e3` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `752697fb702e3cd0fa3a0af577041945f095e87913cd47513d2bd5135752114e` | `6439e620492209dd7a0f07a2cb37c2e5b0894b837e2c64ed0e7dabb5c6e9ab03` | `a20c150855e5141cb7f5e8657dbf50c24bb2a566633be6af6ad785986caf3136` |
| `notation-gallery` | 2 | `3d5cddca2c72b3bb8169d6cc9cfb6764c6cb22815ff35109fc82a1c8fc8ec824` | `f0faa65a739dc4767c0b803c53db1306a60e13a92df517f66c81fa1071a527f3` | `2999c9d2197f60e88632691a850c8992f22b99d936da7659e40f6f4a729879cf` |

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
