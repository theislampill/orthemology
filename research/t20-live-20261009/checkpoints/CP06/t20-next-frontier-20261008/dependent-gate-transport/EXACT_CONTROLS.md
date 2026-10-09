# Exact control scope

`exact_controls.py` passes 3,618 assertions across 30 named families. It uses standard-library Python integers, Fraction arithmetic, and 96-step certified rational bisection for algebraic roots. It does not use floating-point evidence or empirical trials.

The controls include:

- 1,176 strict-positive Bernoulli cells, with associated total-mass and marginal interval consistency checks, for six valid c values and 49 interior command pairs each;
- 600 nondegenerate rectangle masses, including boundary rectangles, with strict positive lower bounds;
- 55 exact rational endpoint-equality witnesses, one for every 1<=n<=m<=10, with rational commands chosen so the relevant power is exactly rational;
- 45 Joe reparameterization checks of the exact rational inside expression and its root interval, with correctly oriented theta=1/c;
- independence at c=1, exact invalid c=2 upper/interior rectangle masses, and a positive low rectangle for that same invalid surface;
- a strict dependent c=1/2 example and the four-value separability-panel distinction;
- 66 exact rational contradictions to m<n for the heterogeneous-joint/shared-marginal product bound;
- inherited shared-gate and cross-talk examples, marked as ancestry rather than new discoveries.

`results/exact_controls.json` contains the named assertion counts, the 55 endpoint witnesses, the 66 Frechet-bound controls and explicit rational interval evidence. `results/exact_controls.log` is the captured author run.

Rational interval overlap in the table-sum/margin diagnostics is a consistency check, not a general equality decision procedure. The general equalities and CDF/threshold realization are proved in RESULT.md. Finite-grid positivity does not prove positivity everywhere, and the script does not present it that way. The mixed-derivative proof and continuity argument supply global rectangular nonnegativity. None of these controls validates any physical or psychological gate mechanism, arbitrary software implementation, or the source-level causal interpretation.
