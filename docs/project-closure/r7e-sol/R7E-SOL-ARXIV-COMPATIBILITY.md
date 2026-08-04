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
| `orthemma-ortheme-systems-draft` | 26 | `062137cfd8c80b874822517b85cbe35aaa713abf73e9900cf4bb415f795ddf7a` | `1284192f10605a8377826e02c625d53a6e745e7db28e54778b45bd517dc94711` | `1a3ae3c4ebab98c0157aec30a47eb2d2b03886e4f0278e46e131a3847a51c936` |
| `orthemic-core-reference-draft` | 14 | `667cebbb0032f987c71112d6a004e1c030b21cc74afb3ed62ea03546e773bdba` | `ee8c4b63b59265b3c0990912f6ecefa0d701f2e738cdbcbe6dc56eb57b7ad825` | `01edfc30626760ea87b2c4a8b65cdaa633c99967abbb047edf5ca3c06c442f09` |
| `orthability-ground-of-intelligibility-draft` | 8 | `12b22767ff6be7aab84cfa1e2fd6e5c39b1c802fd69ca70c55009211d99e0387` | `9c8927ec710163c8c803fad3d2613c647f4bb034992aa4464a9c423aa53c5f4b` | `4e98b2f634636befc2a3d4266e3be7284203fa8dd1335b317980bc83cfbb311b` |
| `orthability-divine-speech-athari-draft` | 6 | `7c3fff6c977b8f3219fbebe8c996e9cb311f2c1392c53dca2b85fe316f06e7d8` | `d54ded998bd6d56ca10a80cf59730db7e88b8af9d0edd65db9cd5c11b72d63d2` | `6f7ab27904e59710a9115a30ba8c53e01420003ba3db30e0096e999d4baf463e` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `f9886b2fe006cabace084c5817f860c6ce2cb111a5169628f26a7870a2e4ec9a` | `943cc309904bb0889ae6fa8fae89fdf4598b8ce4975fe6a43ddbca328dfc9120` | `454935a75e8be2c972b024a1cf76d220d9f1a8ac923fb52a2704e4e082c9ac07` |
| `notation-gallery` | 2 | `69febd35f76e081101a219b9ce5265747f50a9e4dfc1ff57e79e8f0cf9cd4ea7` | `c585c05cffa5344e4381e8a88c846bdbe6681549ea5286f23b14245fe34b4c66` | `682961de624f889cb4a9c5eebac26bcd3ddb397450dff5463cc9820245ba1031` |

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
