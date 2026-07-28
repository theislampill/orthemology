# R7C — Phase H1: P1 vs P2 mathematical-pipeline parity audit

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE

The R7B pipeline decision (Decision 0023) chose the in-repo translator (P1) partly
because pandoc was absent from PATH. The audit (B4) correctly held that this does
not establish deterministic non-provisionability. R7C settles it with evidence.

## Provisioning (refutes R7B's premise)

Pandoc **3.6.4** was downloaded from the official release
(`github.com/jgm/pandoc/releases/download/3.6.4/pandoc-3.6.4-windows-x86_64.zip`),
`sha256 = a9e5feb3d56d2fb0e3e765d1c33b8ee6b72e6963d7de31504edeec8cd1be34b1`
(37,790,321 bytes), extracted, run (`pandoc.exe 3.6.4`), and its **Typst writer**
confirmed. Pandoc **is** deterministically provisionable with a pinned,
checksum-verified binary. Audit B4 is upheld; R7B's "not provisionable" premise is
refuted.

## Parity test (evidence, not PATH availability)

Both pipelines were run over 36 representative corpus formulas (the 33 registry
`render_map` symbols + the episode signature + a `TokenAdequate` equivalence + a
set comprehension). Each output was compiled by the pinned `typst` package and its
extracted text scanned for notdef (NUL) glyphs.

| Pipeline | compile + zero notdef | strict-reject | notdef / other |
|---|---|---|---|
| **P1** (in-repo `latex_to_typst_math.py`) | **36 / 36** | 0 | 0 |
| **P2** (pandoc 3.6.4 → typst writer) | 34 / 36 | n/a | 2 |

## Decision criteria and verdict

| Criterion | P1 | P2 |
|---|---|---|
| corpus coverage (zero notdef) | 36/36 | 34/36 |
| determinism | pure Python, pinned | pinned binary + hash |
| dependency footprint | **zero new deps** | +37 MB binary in CI |
| control over output | full (tuned to the notation) | general translator; 2 edge cases |
| strict-fail on unknown constructs | **yes** (a feature: typos fail the build) | no (renders best-effort) |
| maintenance | in-repo subset, tested | external tool version tracking |
| source portability (GitHub MathJax) | identical `$…$` source serves both | identical |

**Verdict: retain P1** for the implemented pipeline — it achieves full corpus
coverage with zero notdef, is deterministic and zero-dependency, and strict-fails
on unknown constructs. **P2 (pinned pandoc 3.6.4) is now a proven, viable
alternative** and is recorded as a portability/fallback option; it is not adopted
because it adds a large binary to CI and did not beat P1 on the corpus. The
canonical `$…$` source is pipeline-agnostic, so a future switch to P2 needs no
source change. This decision now rests on **measured coverage/determinism/
maintenance**, not PATH availability.
