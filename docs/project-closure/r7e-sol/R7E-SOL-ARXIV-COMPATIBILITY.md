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
| `orthemma-ortheme-systems-draft` | 25 | `3736ca0afe610a662ce8d64f216b420f9fd6cc0348a692751e80fae82ec62e51` | `0809a0ba1be85ff15689e49ad5ae40a0db45ce690795c70375ef1bd3cf43fd69` | `6371242300cd4f6e35b96322edada5f8e9b92c2e3b712b1e4a3f23708d6b8068` |
| `orthemic-core-reference-draft` | 15 | `d4bb7f40442f2dcd33f6c132bd2fa96f8208e480dbe5a5ae5384949dc73cec3c` | `a0c35d9b7716570c811d9ae4ac831445217bd39ba7cf1256c6fa40c13092e310` | `230332534c0589c8e374237eb13218be53ba3c6e0fbb38c20415ae37f4c1a8bf` |
| `orthability-ground-of-intelligibility-draft` | 8 | `1fdf1a8e8a56176eb9ee5df132b7ae6352f5a73441a48f927d3773f492733455` | `ed9b4f46c4fefa1d6e00eae2c6ca3b5ef52eb26c11a24010e1119bcc821e7b0a` | `0c5a69948eb73fea1edb691885acc85ee433afae43dade0d2926a605de784d20` |
| `orthability-divine-speech-athari-draft` | 6 | `2c47c8bde898e097056af42d0eed1d6332dc3a9ce784d2febe19bb30c5deb9c6` | `0d23e66f2fcb846d567302eed5ea24edd1f1b37192cd32ff747d0a4d16050b91` | `87c7998b6e8537a638eca682ef4f23ceecff0eb27f928ec6078a2ff7853cedc2` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `5defa82f7618920a0952967f28a83cabc0f9d151b91ebf5af1e5af34264382ac` | `d353a74c7f72df941372cb51a11db2809933a6c6346965cd4a0733a384b75144` | `e009f73ef8631c0a0d9ea2a9eb71a4dcfe62686ac9164d8fd55d95e8e34cd8af` |
| `notation-gallery` | 2 | `31063a7008516677056a71e5559c15ccc39e5668361f9608ede20452cd52a6bf` | `e7866bb5f4655ee019d0bf038cbff4152d06b0a7867cd5d366cb0d650e3df8ac` | `400d205d6e2682a5e38839428d33fa309c33c0e32d9f96fc72c7a39be8c8d9e0` |

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
