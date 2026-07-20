# R3 Review D — experiment and instrument design (adversarial)

**Posture: assume the instrument is confounded and the readiness claim fake.**

| Attack | Result | Disposition |
|---|---|---|
| Unequal information across arms | v1: confirmed (B−A +14…+35 words; B taught the answer at item time) — v1 superseded for inference. v2: teaching moved to exposure-matched primers; framings length-matched (B/C/C′ ±2 tokens; A ±4); stems identical; deterministic audit in CI | **FIXED in v2; v1 immutably preserved as history** |
| Answer leakage | Leakage phrases banned by the audit; framings name a construct without stating the answer; scenario/stem shared verbatim | **FIXED** |
| Sham mismatch | C′ machine-generated from C by the 1:1 sham map (primer AND framings); audit verifies `C′ == sham(C)` byte-wise; label-independent items flagged ineligible (the v1 FC-1 defect) | **FIXED** |
| Negative-control drift | v1: not arm-identical. v2: byte-identical across all four arms, audited | **FIXED** |
| Synonym stacking | v1's triple-alias B item replaced by three single-formulation variants rotated one-per-run | **FIXED** |
| Unblinded scoring | Execution spec: labels stripped AND construct nouns masked with per-answer masking maps; Latin-square rater assignment; comprehension quiz; majority adjudication with escalation notes | **SPECIFIED** (execution owner-gated) |
| Construct confounding | Framings differ from A by exactly one construct-naming sentence — a *disclosed* design: E3 (B−A) estimates the naming/teaching effect, E1 (C−B) the vocabulary effect, E2 (C−C′) label-specificity on eligible items only | **DISCLOSED; estimands separate the effects** |
| Post-freeze endpoint drift | Three-outcome decision rule frozen in the spec before any run; v2 packet hash frozen; any edit = new version | **GUARDED** |
| Fake readiness claim | Blind human matching review explicitly **pending** (requires humans; owner-gated) — the readiness label is "matched instrument-ready under the deterministic audit; blind review pending at execution; NOT RUN" | **HONESTLY QUALIFIED** |
| Smuggled utility result | Corpus grep: no result, estimate, or simulated-as-real number anywhere; power script placeholders remain marked synthetic | **CLEAN** |

**Residual:** the deterministic audit measures surface matching (tokens, structure, byte-identity), not semantic informativeness — that is exactly what the pending blind human review is for; recorded, not hidden.

**Verdict:** terminology lane = *matched instrument-ready v2, not run; no term adopted* — precisely the §16 formula.
