# Independent mathematical readback

A separate research worker read `research.md`, `CERTIFICATE_SPEC.md`, `IMPLEMENTATION_HANDOFF.md` and `gap_disclosure.py` before sealing. This is internal adversarial readback, not external peer review or canonical approval.

The readback accepted the sign-cell completeness argument, 2k+3 bound, strict/tie boundaries, Boolean induction, empty-class handling, finite ascent bound, symmetry restriction and faithful inheritance of P14's repaired results. It did not rerun the tests and does not claim implementation verification beyond the read files.

Two hardening suggestions were accepted and implemented with failing tests before the change:

1. Rename the misleadingly broad `base_is_purely_descriptive` field to `base_declared_purely_descriptive`. The adjacent semantic-certification warning remains. This minimizes the risk of consumers stripping the warning and presenting a self-declaration as a checked fact.
2. Bound the regime identifier to 128 characters, matching the bounded-input claim.

The final 17 unit tests, 42,500 exact ranking/conjunction reference comparisons, dynamic probes and schema/example validation passed after these changes. The earlier Boolean/integer coercion flaw had separately been caught and repaired by author-side test-first review. Both red and green logs remain available.
