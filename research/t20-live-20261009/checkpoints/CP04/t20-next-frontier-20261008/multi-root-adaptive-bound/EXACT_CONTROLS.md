# Exact author controls

Run `python exact_controls.py` from this directory. Only Python's standard library is required. The script writes results/exact_controls.json; results/exact_controls.log records its observed output.

Ten deterministic control families pass:

1. Exact rational Bernoulli chi-square algebra, both denominator relaxations, the separable factors, squared AM-GM and the final C(r,k) bound, including interior and boundary rate vectors through six roots.
2. Every proper issued profile through six roots, with several per-root counts and rate vectors, gives equal hard-pair endpoint laws.
3. Total-bound bookkeeping and the coarse k^(-2r) envelope through twenty roots.
4. Exhaustive issued-profile/mask counts through eight roots, the inherited upper menu's inclusion in the allowed menu, and the hard pair's probability floor at p=1/(2L).
5. Twenty-four exact adaptive transcript trees with randomized-seed choices, depth five, proper profiles, full profiles, interior rates and rates zero/one. Conditional chi-square envelopes are accumulated with exact transcript probabilities and obey N*C. This control does not claim exact evaluation of logarithms or replace the written KL chain proof.
6. The rate-one bypass of the unbalanced baseline, with a scaled chi-square bounded below rather than exhibiting the proposed higher-dimensional decay.
7. Perfectly shared random-root gates collapse the balanced pair, while the declared independent-route probabilities differ.
8. Explicit rates approaching both boundaries disprove a positive rate-uniform Bernoulli variance floor.
9. Exact k=1 and r=2 constant checks.
10. The whole-effect-bundle embedding preserves a two-outcome endpoint law even when the catalogue contains multiple effects.

All calculations use integers and rational fractions. No numerical optimization, random simulation, empirical endpoints or physical calibration was performed. The all-rate proof and same-class upper comparison are in RESULT.md, not inferred from the finite grids. Independent reviewer controls and any unsuccessful certificate attempts remain in their separate sibling.
