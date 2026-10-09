# Exact author controls and grid witness

Run `python exact_controls.py` in this directory. It uses Python's standard library and writes results/exact_controls.json and results/GRID_WITNESS.json. Saved stdout is results/exact_controls.log.

Thirteen exact deterministic control families pass:

1. Uniform atom floor, within-world gap and zero-atom margin through M=200 at endpoint and midpoint rates.
2. Hausdorff separation of distinct primitive targets and unique matching checks over finite support/calibration pairs.
3. Exact squared-annihilator expectations, coefficient bounds and the moment margin.
4. Normalized factorial-statistic range and moment identities.
5. Exact finite-grid quantization, including the relaxed w/2 candidate floor and the core Delta formula.
6. One fully specified synthetic grid witness with nonzero weight and rate rounding.
7. The separate weight budget, exact Lagrange interpolation, coefficient norm and product-rule derivative certificates.
8. Component-specific calibration counterfeiting nonproportional supports while every component's actual rate stays in the claimed interval.
9. Fresh-resampling counterfeiting a pure count while its common actual rate also stays in that interval.
10. Rare zero-mass coupling failure without a floor on the zero component.
11. A fixed-rate unbounded-count primitive-target obstruction, separate from the frozen changing-rate approximation example.
12. The inherited absolute-count ambiguity radius lying below the present calibration tolerance.
13. Fully rational, power-of-two sample-budget selection.

## What the grid witness actually contains

The witness uses M=3, C=2, w=1/4, support {1,3}, true weights 2/7 and 5/7, and survival 7/10. The exact prescribed Q determines concrete integer weight numerators and a survival-grid index. Both parameter roundings are nonzero. The record verifies all candidate constraints and its moment discrepancy.

A synthetic integer aggregate of group-count frequencies is then constructed from the exact binomial-mixture population law, using a total that meets the sufficient budget and is a common multiple of its probability denominators. Its factorial empirical moments equal the chosen population moments exactly, and the displayed grid witness passes the 2tau acceptance rule. This is an arithmetic witness, not a report of random samples, an observed calibration, or a likely exact-frequency outcome.

The enormous full candidate list was not exhaustively enumerated. The complete finite estimator is specified in RESULT.md, and the quantization proof establishes a qualifying candidate on the statistical good event. The witness exercises that constructive step and its exact acceptance arithmetic without pretending to execute an astronomical search.

## Preserved initial control failure

The first harness run omitted the import of math.prod and stopped in the rare-zero control after nine families. Its partial stdout and error explanation are retained. The import was corrected, all controls were rerun with pipe-failure propagation, and the additional fixed-rate unbounded-count control was included before the final pass. No mathematical constant or predecessor result was changed to bypass a failed inequality.

Finite controls do not replace the all-M proof, authenticate any stochastic premise, or establish practical runtime. No simulation, numerical optimization or empirical experiment was performed.
