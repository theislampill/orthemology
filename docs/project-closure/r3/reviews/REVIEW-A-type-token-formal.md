# R3 Review A — type/token and formal semantics (adversarial)

**Posture: assume the project is wrong.** Every attack surface from the R3 mandate §13, tried against the current tree.

| Attack | Result | Disposition |
|---|---|---|
| Ortheme vs placement collapse anywhere in current prose | Corpus grep: "concrete ortheme/metaortheme/sound ortheme" occur only in negating/analyzing contexts and historical files; the companion now types diagnoses as concrete placement tokens; validator enforces with role checks | **FIXED** (0009; validator in CI) |
| Metaortheme vs metaorthemma collapse | Companion re-typed; schema requires nonempty binding + governed component; CR-6/CR-8 separate binding from execution and honor the zero-burden rule | **FIXED** |
| "Concrete" secretly pejorative | CR-1 (concrete AND sound) is a first-class fixture; Q1 of the 15 answered | **FIXED** |
| Soundness as a hidden scalar | Strict soundness derived, claim-wise, factive; no `SOUND_REASON` primitive; per-claim mixed episodes representable (Q13/Q14) | **FIXED** |
| Orthability senses | L/O/R split; bridge explicit; sense guard in validator; Atharī paper sense-annotated | **FIXED** (0010) |
| Profile completeness: inapplicable vs empty vs unresolved | Definition 10 R3 separates five states; CE-R1/CE-R2 | **FIXED** |
| Vacuous applicability / discretionary ReqPath | Machine derivation + omission attack RP-5; declared ≠ derived fails | **FIXED within the shipped instance** |
| Factivity leakage into the pathway | V2b-T outside CorePath (unchanged, D3); N4 schema-encoded | **HOLDS** |
| Aggregation ambiguity | V1 claim-wise conjunction; V3c per-token + aggregate recompute (cross-record validator) | **HOLDS/FIXED** |
| Cross-analysis typing | Version transport + fusion mapping must be declared; fusion non-uniqueness stays an open parameter (CE-R8) | **RISK-ACCEPTED, documented** |
| Evaluator privilege | CR-7: the auditor's audit is reified and scored identically | **FIXED** |

**Residual findings (honestly kept):**
1. The banned-phrase validator's negating-context allowlist could in principle mask a genuine collapse on a line that also contains a negation word. Judged low-risk (the phrases are also caught at review time; the allowlist is required to let analysis prose discuss the defect) — **risk-accepted with this note**.
2. `RequiredBy` beyond the shipped table, evidence-class exhaustiveness, fusion non-uniqueness, `Δ_A` idealizations — open parameters, stated in the manuscript §15.1, the core §4.1, and the formal audit. **Not closed; not claimed closed.**

**Verdict:** the formal lane supports exactly the §16 formula — *R3 internally consistent specification under the declared definitions, fixtures, negative tests, and acknowledged open parameters* — and nothing stronger.
