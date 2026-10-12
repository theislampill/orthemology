# Reviewed exact-reset continuation core: delivery package

9 October 2026 UTC. This is packaging of a fresh kernel verification and an independent review. It is not new scientific research, protected-repository integration, or T20 closure.

## What is verified

The general theorem holds for every full finite Boolean product, all independent Boolean resets, arbitrary declared total coupled actions, arbitrary outputs, and every common finite action word. Continuation equivalence is proved equivalent to agreement on the independently defined backward semantic dependency closure. Finite-stage-union correspondence, least closure, projection summary correctness, universal summary refinement, and recovery/factorization are included.

The projection-summary existence and recovery constructions are noncomputable/classical. This package verifies their mathematical existence and correctness. It does not extract an executable dependency-discovery algorithm.

## Contents and provenance

- `constructive-t20-lean-20261009/`: the original source package, preserved byte-for-byte from the author ZIP, with source, replay scripts, successful logs, negative-control logs, and honest attempt ledger.
- `constructive-t20-lean-review-20261009/`: independent review receipt, independently copied source, fresh verification logs, and the additional `IndependentAudit.lean` restatement/axiom audit. No build cache is included.
- `mathematical-inputs/`: the bound ordinary theorem and its earlier ordinary mathematical review.
- `REVIEWED_VERIFICATION.json`: current reviewed status and scope.
- `MANIFEST.json`: SHA-256 hashes and lengths for all payload files, excluding this manifest itself.

The original author `VERIFICATION.json` records that review was pending when that package was sealed. This historical record is deliberately unchanged. The separate independent review receipt and the top-level reviewed verification record supersede that pending status.

The independent reviewer found no blocking definition-faithfulness or proof-verification issue, freshly compiled a cache-free copy with Lean path overrides cleared, and checked an explicit all-finite-words/stage-union restatement. Both author and reviewer used official Lean 4.19.0 (commit 6caaee842e94), with zero external packages. Their successful axiom receipts contain only Lean's standard propext, Classical.choice, and Quot.sound; no custom domain axiom or admitted proof.

## Explicit ceiling

Cardinality/fixed-width bit arithmetic, finite stabilization/depth bounds, distinguishing-word lengths, and the positive-certificate antichain specialization are not formalized here. No scientific novelty, metaphysical possibility, human warrant, source truth, reset authorization, deployed implementation correctness, or project closure is established.

Use `constructive-t20-lean-20261009/verify.sh` with Lean 4.19.0 on PATH for the author replay. For the independent audit, run `lake build ResetContinuation Checks Verify` and then `lake env lean -DwarningAsError=true IndependentAudit.lean` in `constructive-t20-lean-review-20261009/package/`.
