# Bounded operation log

Date: 2026-10-08 UTC.
Scope: independently verify the parent-supplied uniform baseline second/cross moments and their compensated-count/active-score application; create only a new scratch sibling.

1. Read the retained skyline likelihood, skyline count information, and active likelihood-score RESULT.md files. Their consumed SHA-256 digests are recorded in SOURCE_AUDIT.md.
2. Independently partitioned the two-query integral into comparable/incomparable orientations. Checked the appended-label exchangeability factor and the one-orientation exclusion for the cross moment.
3. Derived the exact compensated-count remainder in m=n+1, H_m, H_m^(2), and checked its algebra with Sympy. An initial ad hoc Sympy command had an unmatched closing parenthesis and failed before calculation; the corrected command executed. This execution typo did not alter files or supply mathematical evidence.
4. Constructed exact rational controls from independent finite polynomial integration over comparable and incomparable query-pair coordinates. Independently enumerated lower-record counts over permutations for the finite count controls. Added the n=0/1 controls and deliberately wrong-formula rejection checks.
5. Wrote RESULT.md, controls.py, SOURCE_AUDIT.md, and the generated CONTROL_RESULTS.json. RESULT.md states all baseline-only and non-KL/non-testing limitations.
6. Fresh verification: python controls.py completed with exit code zero. All rational controls n=0..32, all permutation controls N=1..8, ten product-integral quadratures, and seven scaling evaluations passed. Complete console output is retained in CONTROL_RUN.log. python -m py_compile controls.py also completed with exit code zero.
7. Recomputed all three consumed source digests and verified exact agreement. No source mathematical error was found, and no earlier packet was edited.
8. Generated SHA256SUMS for the bounded packet's text and data artifacts. This is an integrity manifest, not independent project-wide acceptance or a kernel proof.

No GitHub action, protected integration, archive/tenth-assembly overwrite, physical measurement, or project closure occurred. Historical floor remains UNVERIFIED.
