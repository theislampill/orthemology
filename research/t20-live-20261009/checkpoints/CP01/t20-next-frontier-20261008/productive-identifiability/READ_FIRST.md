# Read and replay the productive identifiability results

`RESULT.md` gives the two-root and multi-effect findings and their source limits.
`THEOREMS.md` contains the exact deductions, restricted-oracle lower bounds,
intervention semantics and finite-sample qualifications.
`general-roots/RESULT.md` gives the prime-matrix criterion, failed probe,
repairs, universal subset-mask design and all-profile guard theorem.

The independently reviewed mathematical/code files are stable. The independent
receipts are in the sibling `identification-review` directory, including
`GENERAL_ROOT_REVIEW.md` and `results/FINAL_REVIEW_BINDINGS.sha256`.
They cover separate reviewer implementations, not just reruns of author tests.

From the common extracted evidence root:

```sh
PYTHONDONTWRITEBYTECODE=1 python t20-next-frontier-20261008/productive-identifiability/src/test_identifiability.py
PYTHONDONTWRITEBYTECODE=1 python t20-next-frontier-20261008/productive-identifiability/general-roots/src/test_design_rank.py
PYTHONDONTWRITEBYTECODE=1 python t20-next-frontier-20261008/productive-identifiability/src/verify_evidence.py
```

The first two commands run twenty and eight new controls. The final command
checks input hashes, replays both suites locally and in an isolated copied
layout, and verifies deterministic exported result equality. It writes only
successor results and temporary copied files. Retain the two runtime dependencies
at their exact paths listed in `DELIVERY_DEPENDENCIES.json`.

`results/RESULTS.json` contains exact rational model panels, gate comparisons,
higher-order examples, design matrices and ranks, lifted guarded collisions and
finite-sample separation values. `results/VERIFICATION.json` records exit codes
and integrity checks. No external Python packages are required.

`KERNEL_TARGET.md` is a precise specification supplied to the separately assigned
formalisation worker. It is not a compiled Lean certificate. Any later kernel
artifact must carry its own scope, toolchain and verification record.

All identification is relative to the declared generative and observation law.
No hidden-route labels are read by the decoder; no actual causal ontology,
physical actuator, source-complete willing, or metaphysical uniqueness is thereby
certified. Prior checkpoints remain preserved and T20 remains open.
