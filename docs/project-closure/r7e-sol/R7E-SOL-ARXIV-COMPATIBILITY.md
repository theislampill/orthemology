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
| `orthemma-ortheme-systems-draft` | 25 | `95544b575504eb3afff26b32feac501eac22b72d9f563b4bf32c170bee1c5139` | `ef200aaa1fc278fb11aebebc2adb2d3cba74086a6c6e37864c6eb6f79c63864f` | `746ec21ab037db1e668200a4c870758f3ef37fcb0284c27a203f96f135a815f4` |
| `orthemic-core-reference-draft` | 14 | `a38a76910dbb0b59ee2ae111d4e74b1e1c5e5d8fb4e10af768d2d72ba684a7c0` | `6141fcac788f1ff4a773a2e5d9562b0355ef927a915c0939744b10b4262a8ce9` | `1d72dfcaaf6074884a6832eefee0ca78ce04d4a31d7c6bc103cdf4791ef04d22` |
| `orthability-ground-of-intelligibility-draft` | 8 | `ba7cb6752e879836c9badca373e831d10c32e708dee47146caed45ecba3e4da1` | `940139d8c3df5fbc25dbdddd7cbb6227996f10d2f7514566fd85c7c0b8612ef7` | `2a5272a84a95164d5247a76f5f393e6e846a8ce28e456cc5e2c7f483f6f02017` |
| `orthability-divine-speech-athari-draft` | 6 | `5fd9f883baa76b0bf638e90aef824c294f1af6b83c2d29d46063ec68941b951d` | `d8fa557f8682404bfab565bcf1d59229d6f9a5ac32d6a16fe7e2885996d6adde` | `323c0db994f3eb229b86a127aded8a070d8bc2446f34809df6a65b52073ed750` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `cefec0261302c27f791a5c4148d51a3a6674be80ce7a7759350769a5ca5df9de` | `3b6842709a44c3f97b13288d967499066a8cf3d4fdbb4017a3154188a21f4180` | `37eca51e9e3303141889d352184f9fbaa824e70363f78391f444c4e43067da03` |
| `notation-gallery` | 2 | `8bfa4e4dd966fa16e910a1adb0c8e8cbf4bd5bb2fc22b0b493557f8cc62fedad` | `d4011b632320a33d432d17af51187d9dd506c9ca40d6d7e38df2d784503ca9d3` | `0b68ad49791fdaa8561e49cd4505433bc0fc8fd4dabbbf02b6496bc270788814` |

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
