# Replaying the universal single calibration

`RESULT.md` contains the arbitrary finite-root proof and scope boundaries.
`results/RESULTS.json` contains exact rates, CRT selectors, private-prime matrices
and sample decodings through four roots, plus the six-root nonunit valuation control.

The implementation is standalone Python standard-library code. From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python src/test_crt_calibration.py
PYTHONDONTWRITEBYTECODE=1 python src/export_results.py
```

From the retained common evidence layout, `src/verify_evidence.py` also checks
predecessor hashes and compares a copied isolated replay's exported result bytes.
It writes only this successor's evidence and temporary files. Eleven author
control groups pass. Independent review receipts are in the sibling
`single-calibration-review` directory; those are separate evidence, not a new
count of discoveries.

A later bounded-count, noise-aware mask design is a separate investigation.
It does not mutate this stage or turn its exact probabilities into measurements.
The previous productive-identifiability manifest and all its 24 entries remain
unchanged. No protected integration or T20 closure is authorised here.
