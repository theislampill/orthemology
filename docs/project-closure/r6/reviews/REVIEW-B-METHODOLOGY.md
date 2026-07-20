# R6 Review B — experiment methodology (confounds)

Surfaced model: `claude-fable-5`. Assumed posture: the benchmark cannot distinguish machinery benefit from verbosity, compute, vocabulary exposure, or scoring leakage.

- **Verbosity:** REAL FINDING — the baseline arm instruction was 130 words against the treatment's 240 while the protocol claimed a ±15% length band. Repaired: the baseline instruction was expanded with content-neutral elaboration of its same four steps (now 261 vs 240 words, ratio 1.09); the packet was re-frozen and the index hash updated. Residual verbosity in *outputs* is guarded by the F9 negative-control structure-overhead harm rule.
- **Compute:** both arms share sampling parameters, budget, and executor version by design (DESIGN.yaml); no confound found.
- **Vocabulary exposure:** zero coined-vocabulary tokens in any arm or fixture material (grep-verified); benefiting from the treatment cannot require the coinages.
- **Scoring leakage:** scoring is programmatic against frozen keys; the executor never sees ground truth, family labels, or keys; the parser is shared between arms. ER-1's free-text normalization synonym table ships inside the frozen parser (recorded residual: synonym-table adequacy is itself instrument risk, surfaced honestly in SCORING-RUBRIC.md and adjudicable at run time via the deviation ledger).

No unrepaired blocking confound; residuals recorded above.
