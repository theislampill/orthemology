# Finite-history interlock safety: bounded kernel extension

Owner source: accepted frozen base-v2 MODEL_AND_PROOFS.md and dynamic_interlock.py, plus its accepted independent review. No predecessor changes.

1. Record source/statement correspondence and pin read-only Lean 4.19.0 / Mathlib c44e0c8.
2. Model root-local descriptor, persistent revocation/cancellation memory, commitments, serial requested/effective epochs, authenticated local certificate delivery, arbitrary lifetime-budget root faults, and same-command live serial gates.
3. Prove authentic-history and durable-memory invariants by actual transition/trace induction; derive current/authorized/exact landing and cancellation exclusion using finite-root intersection.
4. Prove plant safety and target preservation in an unchanged epoch. Keep reservation, actor policy, physical mediation, and bounded independent control service separate; no complete liveness/search claim here.
5. Replay kernel negative controls for omitted duties, produce axiom/compile logs and source-bound statement map; hand off for cold review before 17:45 UTC if possible.

Fault abstraction: F is an arbitrary fixed superset of all roots ever faulty in the finite trace, |F| <= B. Root behavior inside F is unrestricted; no actor or good gate reads F. This is a proof bound, not an instantaneous/mobile-fault guarantee.
