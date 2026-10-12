# Reproduce the new finite diagnostic

This is a self-contained Python-standard-library reference construction. It does not import Orthemology's or DAEE's production code and does not claim correspondence with those implementations.

From the package root:

```sh
python3 -B -m unittest discover -s research -p 'test_contracts.py' -v
python3 -O -B -m unittest discover -s research -p 'test_contracts.py' -v
python3 -B research/exhaustive_oracle.py
python3 -O -B research/exhaustive_oracle.py
```

The oracle exhausts a family of three-state deterministic labelled/costed systems and all their partitions, rather than simply asking the refinement code whether its own output is correct. It also checks rational finite-horizon and conditioning inequalities. These are finite corroborations of the written arguments.

`Contract` accepts exact integers and `fractions.Fraction`, rejects floating-point probabilities and invalid row masses, and freezes its validated mappings. A label is a supplied immutable value. The code does not determine whether that label is epistemically warranted.

The finite-value method assumes the declared state is fully observed; a partially observed application needs an adequately justified information-state model first. The almost-sure check is for a fixed stationary policy on a finite system, not unrestricted synthesis of an optimal policy.

The moment controls are static finite square-positivity obstructions. They do not implement the predecessor infinite ODE, interval arithmetic, or its stronger determinate-initial-state counterexample.

No elapsed time in a log supplies research-duration compliance. Resource exhaustion is not a failed theorem. Read the exit codes, output scope and relevant assumptions separately.
