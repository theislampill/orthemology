# Reading and replaying the countable-signature stage

Start with RESULT.md. The mathematical files separate the main finite theorem,
the factorisation-free improvement, finitude assumptions, and oracle/coefficient
extensions. They are not one unrestricted metaphysical identification claim.

From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python src/test_countable_support.py
PYTHONDONTWRITEBYTECODE=1 python src/test_gcd_decoder.py
PYTHONDONTWRITEBYTECODE=1 python src/test_oracle_boundaries.py
PYTHONDONTWRITEBYTECODE=1 python src/export_results.py
```

The suites have15,6 and8 control groups. All runtime dependencies are Python
standard-library code in this sibling. `src/verify_evidence.py`, run in the full
retained evidence layout, also checks predecessor bindings, primary source hashes,
an isolated copied replay, and deterministic result equality.

`results/RESULTS.json` contains primitive-order witnesses, descending decoder
traces, gcd selector certificates, the finite greedy prefix and its proved error
bounds, the candidate-dependent second-query gap, and the mixture grouping values.
Its large exact integers describe mathematical readouts, not measured data.

The original1892 source is public domain and included with exact provenance.
The modern2010 article is delivered by direct source URL and hash; its full local
PDF/text/page image are excluded from the distributable manifest. The verifier
reports that deliberate link-only disposition if those inspection files are absent.

Independent review is in the sibling countable-signature-review package. Any
subsequent finite-mixture work is separate. A resource-inconclusive result is not
a no-model verdict. Earlier frozen stages remain unchanged; T20 remains open.
