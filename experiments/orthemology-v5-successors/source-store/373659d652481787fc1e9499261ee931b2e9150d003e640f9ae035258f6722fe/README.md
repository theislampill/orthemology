# Unchanged Python JSON reference

`certificate_checker.py`, the three example JSON files and the original 10-test author suite are exact accepted v1 bytes. The 12 independent tests have only their local checker path adapted for this package.

Run:

    python3 -m unittest discover -s verification -p 'test*.py' -v
    python3 certificate_checker.py decide < examples/piecewise_instance.json
    python3 certificate_checker.py verify < examples/piecewise_certificate.json

This implementation validates a strict canonical JSON certificate representation. The separately kernel-checked Lean verifier accepts typed finite lists, including harmless reorderings, duplicate coefficient entries, zero coefficients and extra/duplicate rows if every required mask has valid coverage. These are deliberately different representations. No parser correctness or Python-to-Lean refinement theorem is asserted.

The tests include normalization, arithmetic/conditional branches, finite masks, arity zero, forged coefficients, malformed data, random regressions and finite-grid witness checks. They establish these concrete tests only. The general degree-plus-one finite-grid theorem and witness-search guarantee remain written mathematics; the Lean semantic decision proof uses coefficient equality instead.
