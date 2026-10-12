# Reviewed dynamic V2 finite-history safety kernel

This archive preserves the exact reviewed candidate and its frozen controlling
source/review bytes in their original relative layout. No predecessor was edited.
The independent disposition and precise scope are in:

tranche7-restart/formal/interlock-history-kernel/independent-review-v2/REVIEW.md

The extension proves finite multi-epoch history safety, durable cancellation
exclusion and stable whole-table goal preservation at the original dynamic V2
root/table interface. It does not prove complete liveness, covering/randomized
search, physical realization, or automatic transport to other interfaces.

Replay after extracting with an archive tool that preserves executable modes:

bash tranche7-restart/formal/interlock-history-kernel/verify.sh replay

Dependencies remain external: exact Lean 4.19.0 at the documented path and the
read-only Mathlib c44e0c8 cache under private-locator:351b8592ab6e0e21df70. The compiler hash is
checked. This is source-portable across extraction directories with those pinned
dependencies available; it is not a self-contained toolchain distribution.

V1 inputs are preserved under frozen-candidate-v1. The root candidate is V2 and
is bound by REVIEW_SNAPSHOT_V2.json; the V1 receipt applies to the preserved V1
inputs, not to the corrected root candidate.

The original candidate README's pending-review sentence is historical metadata;
the separately bound independent review sidecar records the later disposition.
