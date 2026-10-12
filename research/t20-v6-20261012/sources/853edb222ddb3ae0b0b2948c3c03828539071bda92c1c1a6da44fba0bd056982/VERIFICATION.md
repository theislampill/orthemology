# Author-stage verification

All checks passed on 11 October 2026 UTC. The checker uses explicit failures, so optimization cannot remove its checks.

- Standard Python, with predecessor originals checked: 75 passes
- Optimized Python, with predecessor originals checked: 75 passes
- Standard standalone replay without predecessor files required: 65 passes
- The standard and optimized full-control JSON outputs match byte-for-byte
- Ten predecessor snapshots and ten still-present originals match their baseline hashes

Each full replay consists of 52 exact symbolic/rational controls, 3 labelled floating-point calls to the unchanged inherited Gaussian implementation, and 20 input integrity checks. Standalone replay drops only the ten external-original checks.

Controls cover the invertible-positive finite kernel analogy; conditional Bayes and normalized-power composition; separate evidence normalizers; unchanged Dirac audit and changed two-point audit; successive conditional factors; an actual continuous OU two-atom density-ratio discriminator; exact noncommuting Gaussian transport and input recovery; singular inputs; both inverse-image covariance guards; the restricted fixed-covariance class; the two-fibre global-normalizer discriminator; and the actual Gaussian implementation.

The universal law-level and obstruction proofs are in RESULT.md. Finite tests do not establish these by enumeration. The first mathematical replay passed; no counterexample was repaired by weakening a check. A README version typo was corrected before the author freeze. Only the new packet was written. No protected input or inherited implementation was modified.

This is author verification. A separate reviewer must decide acceptance; this document does not claim that review has occurred.
