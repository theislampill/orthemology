# Replaying the effect production controls

Preserve the common evidence-root layout listed in `DELIVERY_DEPENDENCIES.json`.
The runtime imports are exactly two preserved Python files; no external package is needed.

From the common root:

```sh
PYTHONDONTWRITEBYTECODE=1 python t20-continuation-20261008/effect-production/src/test_production_contract.py
PYTHONDONTWRITEBYTECODE=1 python t20-continuation-20261008/effect-production/src/export_results.py
```

For local input bindings plus an isolated copied-layout replay:

```sh
PYTHONDONTWRITEBYTECODE=1 python t20-continuation-20261008/effect-production/src/verify_evidence.py
```

The verification script checks the 15 bound inputs, runs the 19 tests, copies only
successor code and the two runtime dependencies to an isolated temporary layout,
checks actual import paths, reruns the tests and compares exported result bytes.
It creates results only under the successor directory. It does not run recovered
module main functions or write to the recovered checkpoint.

`results/VERIFICATION.json` records exit codes, test output and integrity checks.
`results/RESULTS.json` is the deterministic finite evidence. Initial files and red
logs are developmental evidence, not the current implementation. Cache files are
excluded from the delivery manifest.

The declared tests do not verify a metaphysical causal ontology, numerical
identity across every possible world, source-complete original efficacy, or the
truth of a supplied productive-ground interpretation.
