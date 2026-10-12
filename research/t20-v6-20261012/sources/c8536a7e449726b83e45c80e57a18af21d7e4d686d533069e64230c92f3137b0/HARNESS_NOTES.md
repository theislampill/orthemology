# Review-only verifier corrections and boundaries

The independent verification script reads the immutable extracted packet and writes
only this report's receipts. Its early attempts exposed assumptions in the review
script, not new product failures. They were corrected against the actual schema:

1. The thirty-clause index includes HANDOFF.md; the first attempt assumed only
   README/DESIGN. The revised verifier uses each declared target basename.
2. Generated fetchWeather includes the known guarded CP9 accepted-elevation hook.
   The verifier admits that exact additional text and preserves surrounding bytes,
   rather than asserting false whole-function equality with authored source.
3. The source's six-hour constant is written `6*3600e3`; the literal check initially
   used another equivalent spelling and was changed to the actual spelling.
4. The raw native readiness status is lowercase `ready`; the first schema assumption
   was corrected without modifying the original result.
5. The status counter omits keys with zero occurrences. Comparison now explicitly
   includes the declared zero READY value; actual counts remain unchanged.

Saved failed-attempt logs are retained as reviewer-harness history. The final run
passes all 1,000 read-only byte/binding/recorded-observation checks. Subsequent
checks added explicit raw privacy-log counts and five root-admission bindings;
these are not executions of the retained tests or producer scripts.

`receipts/supplied-custody-verifier.json` is the result of the supplied read-only
VERIFY.py, inspected before execution. `verify_review.py` is independently authored
and performs additional in-memory/source/recorded-state checks. Neither imports
or invokes the incoming product, test oracle, native driver or producer tools.

To repeat the independent read-only checks after extracting the exact input ZIP:

```text
python -I -S -B verify_review.py --input /absolute/path/to/extracted-delta --output /new/review-receipt.json
```

The optional byte comparison to a previous local report executes only when that
old local file is available; the original records are also retained inside this
packet and the input archive. No external connection, Git operation or input
mutation is required.
