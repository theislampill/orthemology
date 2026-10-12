# Central v2: review clarifications and stronger control

Central-v1 is preserved unchanged. Every one of its ten main Lean source files and both copied attribution dependencies is byte-identical in v2.

1. Added RepairStateBridge.lean after independent review requested explicit defective-start interpretation. It proves the canonical identity-or-repair target coordinate is true after N attempts iff it was initially true or a successful hit occurred before N. The lower-bound target-achievement interpretation therefore selects a defective start. A correct initial target is explicitly achieved at zero attempts. SPEC, theorem map and README state this limit; 126 bounded state cases corroborate it.
2. Improved the missing-opacity mutation. V1 replaced its equality by True, causing binder inference to fail too early. V2 replaces it by the reflexive failedReply=failedReply equality, preserving the type-correct interface while deleting observation information. Compilation reaches the intended equality obligation and fails there. The mutation harness checks for that diagnostic and rejects an early field-inference failure.
3. Added the state bridge to the clean full replay and theorem-axiom checks. All previous covering, complete-action, root-realization and randomized proofs remain unchanged. This is no change to accepted scientific scope or previous source bytes.

Independent review remains pending for the exact v2 manifest until its own receipt is issued.
