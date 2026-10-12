# Independent review of repeated null evidence dynamics

9 October 2026 UTC. Separate mathematical review. No integration, release, or closure authority is asserted.

## Bound snapshot and outcome

- Report SHA-256: d95d4afbda647ffbd71683b9b6356bdf8ad710323785632d0f8003ad8ff4d5f9
- Author verification script SHA-256: 6a9ab36a3527b01a584c541a56c33a9f178708345159b7de2a23e932f39c5162
- Outcome: no blocking mathematical issue found after a complete report read, independent derivation, complete script inspection, fresh replay, and separate diagnostics. The script already contains the cleaned final asymptote assertion.

## Proof findings

The weighted-entropy projection formula and inherited composition law give the stated continuous interpolation and discrete recursion. Both fair-coin outcomes have the same likelihood vector, so the forecast is the same for every observed sequence; no rare-outcome event is being selected.

For the concentration proof, delta=lambda-at lies between zero and -a log P_M. The higher-weight terms vanish uniformly on this interval, giving the asserted limit of delta and the prior-ratio-preserving limit on the minimum-weight set. This covers both tied and unique minima, and reduces to the stationary prior for common weights.

The divergence formula is correct for the full weighted Bregman score, including its affine-in-report terms. Differentiating normalization gives lambda'=H_q and A_q'=H_q-A_q. Strict harmonic-arithmetic inequality holds at every finite time for unequal weights because every coordinate remains positive. Consequently regret increases strictly for t>0. In fact its second derivative is A_q-H_q>0. The asymptotic constant and slope are correct; the per-observation rate includes log 2.

Every individual repair stage has exactly the stated positive equal reduction in statewise losses relative to its own halved raw input. The three-point identity applies because both the repaired forecast and each categorical outcome have coordinate sum one. This does not imply improvement over the unchanged coherent prior, and the report maintains that distinction.

The two-hypothesis radical expression is exact, including its rationalized form 2/(1+sqrt(1+2^(k+3))). The limit is taken through finite interior reports; the report does not improperly evaluate divergence with the boundary limit as its second argument.

## Verification evidence

The complete author script was freshly executed with exit code zero. It reported PASS for 1,029 numerical checks across 129 finite steps at Decimal precision 100, using tolerance 1e-85. The retained stdout is AUTHOR_REPLAY.json. These are high-precision numerical controls, not exact symbolic checks or a proof of the limit.

A separate independently written solver and direct-divergence check is retained as independent_diagnostics.py. It checks 903 path points in three families, including tied minima, and 80 comparisons with the radical formula. All retained diagnostics pass; maximum radical comparison error is 5.551115123125783e-17. Results are retained in INDEPENDENT_RESULTS.json.

An exploratory binary-float check initially lost strict positivity when subtracting A_q-H_q extremely near concentration. This was a cancellation artifact, not a counterexample. The retained diagnostic uses the equivalent nonnegative pairwise formula for the mean gap; no mathematical premise or theorem was changed.

## Scope

This is a written mathematical review, not proof-assistant/kernel certification, empirical validation, or field-wide novelty assessment. The prescribed operation is multiply-then-project with fixed unequal weighted-entropy geometry, a positive declared prior, and a stipulated independent coin channel. The conclusions do not apply to ordinary Bayesian updates evaluated by other proper scores, nor establish any actual noetic or human-manipulation claim.
