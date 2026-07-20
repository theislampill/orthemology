# R4 Review E — instrumentation and empirical-claim reviewer (adversarial)

> **CANDIDATE REVIEW — REQUIRES INDEPENDENT REVIEW.** Performed as a fresh read-only pass after the corresponding implementation phase, but by the same run that implemented it; it is therefore *not* the independent sign-off the R4 program requires. Model provenance is disputed and unresolved (see `../AUTONOMOUS-R4-STATE.json`).

**Posture: assume an experiment got described as run.**

- Corpus-wide scan: **no** experiment reported, **no** utility estimate, **no** simulated result presented as real, **no** term adopted. Power-simulation placeholders remain marked synthetic.
- Terminology status is stated uniformly as **INSTRUMENT-READY PENDING BLIND HUMAN MATCHING REVIEW; NOT RUN; NO TERM ADOPTED**, and the blind human review is listed as an **owner-gated** step, never as complete.
- The pilot-0 v2 matching audit is deterministic and surface-level (tokens, structure, byte-identity); it is **not** evidence of semantic equivalence, and the note says so.
- Latent-state fixtures are **conceptual consistency artifacts**, not empirical data; the validator's 190 checks are consistency checks and are described that way.
- **SELF-1 correction** (freeze-hash mis-reporting) is instrumentation-adjacent and is recorded rather than quietly fixed: the packet was always correct; two closeouts and three documents were not.

**Residual:** the deterministic matching audit cannot detect a semantic asymmetry that survives token/structure matching — exactly what the pending human blind review is for.
