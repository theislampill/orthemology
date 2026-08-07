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
| `orthemma-ortheme-systems-draft` | 26 | `1ff1b5f2c6b1930d333088cc1150219319d1d14315c2327c8fff9f42420d2dc0` | `3fdcffc3f1aa799070a696791781986421f2b7a268c1f889cbee198682ec0937` | `3b79ecc0fefee830507869f4c3036d8b537ef2b928dc2dec5dafb0dcfeae5892` |
| `orthemic-core-reference-draft` | 15 | `776cbe9915d6d7ad80fd622d8835031566077cce7cd47d0246731210655966f7` | `27699db523b307c3284bc92255604ba966ad65fa33dc448b95679fc02c21ddcd` | `98b52ca100ed8abccaba1de338c0734fbb1454ed4a3fb87cb7996fbc8430dbdd` |
| `orthability-ground-of-intelligibility-draft` | 8 | `93e42076d086a8c2731709930b5b6e525898a509e54575bf9fca65a8c7d5c354` | `2b5e4a6dbe41c33f18a80c9e3e1253faf33d330b35318d83b29afd684faba732` | `684b3619e58f323cf62afe91af63ce48412b64ba257ac23e466ae6bf9dedd99e` |
| `orthability-divine-speech-athari-draft` | 6 | `ba66cb32871e4885a0ba68aadcf6311cf74ab103fc06266a45b86e2855c5b105` | `c9f52def959abf36ab31d4403c79de74a3da4259b63bc026eb7d6a1a4b8c7e90` | `5cc1a6d4014b38d1840d7308175ad1c38f572608606bcc6d1738f66c41dd1c69` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `644c5fc2c5e5efc552bff6502a29b06772cccdf23503919448c85abe7dadf258` | `f9b2b77f2b2686e007835950909477675d72929ca8406626a1252f1df0fb9006` | `74b48d52644835d5da5e9b8d835d6e8df3ae42d3e6c2c842af0f43e1e8d47f2c` |
| `notation-gallery` | 2 | `8d31c02b684297c891612f8fcac9aa70de007de9c2618ef550392ce746f2677f` | `9e11c76a13c660d5df27eacad93fd5737701172ff4cd8033a97559264f7a1c8b` | `75fb29ecb3eae06af94e1e4bcd69ac36b5538ed38521472d16476fdeab6c79d8` |

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
