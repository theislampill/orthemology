# P03 bounded research and proposal execution plan

Goal: discharge as much of U03, U04 and Q1f as the exact source and runtime permit, without changing accepted source or integration state.

Architecture: retain the input ZIP and its exact preimages; run new finite falsification probes against the mounted source; describe ordinary proof obligations independently of those probes; test any patch only on a separate copy. Q1f is a separate guarded-transport target, not an alias of CV-O. No owner, historical-recovery, independent-review or kernel credit is inferred.

Inputs/specification: the unchanged input INDEX.md, OBLIGATIONS.json, DEPENDENCY_DAG.json, scope/boundary documents, and source/evidence bindings. Supplemental exact frozen-main VCT/TRC source was read through the GitHub connector; it must be preserved with its blob identity before relying on portable exact-source credit.

## Work units

1. Verify archive CRC, every manifest/receipt binding, source Git blobs and accepted projections. Record the runtime and fixed canonical identity.
2. U03: compare strict decoding, native structural validation, shifts/substitution, finite checking, reduction-trace encoding and text export. Falsify the proposed total transport round-trip at the empty-container depth boundary. Run a separate finite checker mirror as an experiment, not Lean proof. Preserve successful-step and refusal distinctions.
3. U04: inventory the complete engine state, every public transition, full positive/negative read dependencies, records and issuer identity. Test the native observation setter's snapshot boundary under a controlled schedule. Test currentness/ABA/absence/resource refusals and full logical-state preservation under declared Rejection paths. Keep crash/OOM and hostile-private-state changes outside any proved scope.
4. For reproduced defects only, preserve exact preimages and make minimal patch proposals on an isolated source copy. First retain red regression evidence, then run the same regressions and the supplied suite against the proposal. No patch is applied to canonical source.
5. Q1f: bind the eleven exact VCT guards and the VCT/TRC source statuses. Give a non-tautological, explicitly scoped transport proof/countermodel analysis with typed DAG and witness boundaries. Do not perform P12's game/fixed-point research. Provide unverified Lean candidate source only if no exact compiler can be executed.
6. Package exact statements/statuses, dependencies, source comparison, proposals, raw commands/logs and a Codex handoff. Reopen the completed ZIP in a fresh verifier and hash every payload and sealing member. Recheck the original inputs for mutation.

## Review focus

- Empty deepest containers: dump success must not be conflated with decode-domain membership.
- Caller-owned mutable native revision arguments: copying after validation leaves a scheduling window.
- Rejection versus arbitrary interruption: logical failure atomicity is not crash-atomic durability.
- Registry stamps: missing keys, implicit need:key defaults, first creation, full snapshots and issuer scope matter.
- DAG transport: dependency-preserving maps alone do not preserve acyclicity; independent target/revalidation semantics may not be replaced by supplied Boolean claims.
