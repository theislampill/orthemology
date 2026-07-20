# R4 Review F — closure/publication/privacy reviewer (adversarial)

> **CANDIDATE REVIEW — REQUIRES INDEPENDENT REVIEW.** Performed as a fresh read-only pass after the corresponding implementation phase, but by the same run that implemented it; it is therefore *not* the independent sign-off the R4 program requires. Model provenance is disputed and unresolved (see `../AUTONOMOUS-R4-STATE.json`).

**Posture: assume the state drifted again, a burden got inflated onto the owner, and something private leaked.**

| Check | Result |
|---|---|
| Current-state consistency | Generated + drift-checked; VERSION/README/STATUS/OPEN-DECISIONS and five headers agree with `docs/current-state.yaml`. **FIXED** |
| Version/header consistency | All primary documents name R4 and carry the candidate qualifier. **FIXED** |
| Owner-only list | Six standing items plus one added by this run's circumstances (**resolve the provenance dispute and commission independent review — merging is an owner action**). Research residuals kept separate with triggers. **CLEAN** |
| Private material | Repository hygiene validator green: no absolute paths, private patterns, secrets, archives, or session dumps; casebook and transcripts remain unpublished. **CLEAN** |
| Invented license/identity | None. No LICENSE, no CITATION.cff, no author identity. **CLEAN** |
| External-publication claim | None. **CLEAN** |
| Stale closure wording | R2/R3 claims superseded by dated notice; R4's own wording is bounded and carries the candidate banner throughout. **CLEAN** |
| Artifact/source-revision consistency | Two-stage provenance retained; PDFs rebuilt after the final textual edits and re-verified. |
| Force-push / history rewrite / merge | **None.** R1/R2/R3 bodies untouched. The R3 merge predates the provenance override and is recorded, not rolled back. **CLEAN** |

**Blocking residual by design:** this pass is a **candidate**. Final sign-off requires an independent reviewer the owner commissions; this review does not substitute for it and does not claim to.
