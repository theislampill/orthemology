# Separate digest-bound independent reviews

Both mathematical documents received independent scoped PASS verdicts, with no unresolved corrections. The reviews provide no empirical certification, integration, owner-acceptance, or T20-closure authority.

## Main threshold theorem

- Author source: `RESULT.md`
- SHA-256: `ec620e491fd1c58cdc9dc0bcc8700784b79b4b399247ca1e2a235438138cf827`
- Review: `../global-calibration-ambiguity-review/REVIEW.md`
- Receipt: `../global-calibration-ambiguity-review/REVIEW_RECEIPT.json`
- Receipt SHA-256: `405182b0516be264847c7fa8a25605e3db948c8823ec649d47f7c82eb6bc8cb7`

The review covers the adjacent-count sharp threshold, static monotone construction, all-command adaptive/stopped equivalence, strict-below-threshold decoder, full fixed-count catalogue extension, near-threshold necessary budget divergence, endpoint cases, and scope distinctions. The reviewer replayed all 14,125 author assertions in a separate copy and ran 17,480 independently implemented assertions, including rational tests, high-precision inversion diagnostics, and exact randomized early-stopping transcript checks.

Before final binding, the definition of failure was clarified to include abstention and nontermination, or to restrict attention to procedures that return a count almost surely. The theorem's mathematics did not change. The main review expressly excludes the separately added efficiency appendix.

## Polynomial-efficiency appendix

- Author source: `POLYNOMIAL_EFFICIENCY_APPENDIX.md`
- SHA-256: `4242d8cbcc9fd576266e2ee01f902b45c93e6701b5c01d07a5a0c3909f97f0f4`
- Review: `../global-calibration-ambiguity-review/APPENDIX_REVIEW.md`
- Receipt: `../global-calibration-ambiguity-review/APPENDIX_REVIEW_RECEIPT.json`
- Receipt SHA-256: `830a91e43492efe7024695504cbac8cf8aece34a56a229c8b07068eb171a04c5`

The separate review covers clipping and admissibility of the hard maps, the exact rate-error envelope, adaptive exponential lower bound, finite-domain sufficient command and gap bound, constants in the simplified sample budget, and the fixed-confidence sufficiently-large-M polynomial-budget characterization. The reviewer freshly replayed all 33,840 author assertions and ran 22,073 independent assertions, using exact rational checks and high-precision exponential/logarithmic diagnostics.

The final appendix changed one confidence-domain phrase from `delta>0` to the explicit `0<delta<1/2`. The reviewer verified that this was the only proof-file change, repeated the appendix checks, and rebound the appendix receipt and manifest. The main source and main receipt were unchanged.

## Frozen review checkpoint

The final review `../global-calibration-ambiguity-review/MANIFEST.json` has SHA-256 `fa053545ba06d46656455e45824741915679e36b3afe16e8bb76aaf278911e05`. Its artifact and author-source bindings were reverified by the author before the author-stage manifest was frozen.

Finite exact and high-precision controls remain diagnostics; they do not replace the general written proofs. Neither review audits the frozen predecessor's source provenance or validates the model physically.
