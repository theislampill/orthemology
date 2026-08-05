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
| `orthemma-ortheme-systems-draft` | 25 | `60b96b6ef13e2350d5f4b671829784c9b04a86f5f457a626d8730dad11bc12db` | `30dcd4dfb647d9f0c5a47262edb82a3047440385ceca11026fb78bdf16e394ab` | `f1033337a942df285ff475a824f17c9b21cf7a127f266d8a341b28a4413a1b1d` |
| `orthemic-core-reference-draft` | 15 | `d6154668d5cb084f1e43c098656a8546335e7fc64bea9c0f3a0cb665d9abb663` | `88fa3aacac7c032fe9e55cc261a4620b3b52623564dfa89caae3e3d4597cc345` | `ff7c1c810d73da3d67e93c1991c4335a41855c28e642fec1f4753ab502745bf5` |
| `orthability-ground-of-intelligibility-draft` | 8 | `0852d5ef0a4f86720613a9964261f5c7e0c3c992230f8fd6d1440ab35136dfb8` | `ef0fcaf1d2b6256318554e69c2f6501d1d28357f10ef0ce0849c96e01bfd3600` | `8c4429d16d9054daca9b71a7771aa71deb0a41187e105e60f633c97a46272c80` |
| `orthability-divine-speech-athari-draft` | 6 | `93a860a95687f2be5fc74e57c389902e60e7e7fc0c1035c2caae31bbdeacc5e7` | `95749bd1e83dde73f230b275403e88f0748a8b9abe9fc7ea6016112cbf3c79c6` | `11fdc4df53e9c660f2ac2a673492a5a8d7c04c76dee44ecdc431a5b77f65efd7` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `074b00e16ad47583c396e81722ca3b7d187f048a2358ac7a3e9c9222b784a588` | `3adc903262f5a34270cda28e8db4ed307e96bc5d3d9ada18f4b307b934c64970` | `e38d11fd718d67d5ba8629bf37f93956d0139cc1d1e9b2cd0ded1b2267f2720d` |
| `notation-gallery` | 2 | `576d4ee578484aff4b1d72dc554a66c711ced3c74b90ff5a7197a6f8f0e842b0` | `223a13dafbb31fbf4b2e2430b7ece572a09d019ccd4fb045b07fd5a8f06d5ecf` | `23a49a0395961fbbe58441da1bd0b05515b85d7e183075e5c7eacb88f7770c77` |

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
