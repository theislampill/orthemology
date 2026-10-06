# Typed finite-history milestone review

## Verdict and binding

PASS for the scientific statements in immutable `typed-history-v2`, manifest SHA-256 `8fef9a6bca00d9cfaeb4dda16dceb441307e90341de2ef96f0900bf001ab2f82`.

This extends the reviewed common core with complete per-event plant effects, finite-history custody and exact counter laws, permanent fixed-action rejection, an explicit two-stage existence witness, and focused negative controls. The six core modules are byte-identical to core-v1. Distribution-wrapper acceptance and raw2-to3 runtime lifecycle refinement are separate questions and receive no verdict here.

## Independent verification

A fresh sequential official Lean 4.19.0 build passed all 19 modules: eight exact accepted imports and eleven new modules. Compiler identity was checked against SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, commit `6caaee842e94`. All 6,816 pinned Mathlib source files matched the accepted source manifest; its supplied compiled cache was used read-only.

The axiom closure of every theorem in the eleven new modules was separately printed: 134 declarations in total, including the 85 already reviewed core theorems. All dependencies lie within `propext`, `Classical.choice` and `Quot.sound`. No custom axiom, proof-hole dependency, unsafe declaration or native truth oracle was introduced. Candidate and accepted-import hashes matched before and after replay.

The independent `TypedV2Challenges.lean` checks also compile with only standard logical axioms. The replay receipt binds source hashes, commands and logs. No independent rebuild of the Mathlib cache or whole native runtime execution is claimed.

## Findings

### Complete effects, custody and counters

`step_plant` separates accepted landing from every non-landing primitive event. For a landing it establishes the exact imported `localStep` result under the common current policy, plus equality of the entire resulting plant to the bound envelope successor. Every other primitive event leaves the plant unchanged. The pre-state consistency and non-damage hypotheses are explicitly required and derived for reachable histories.

`finite_history_custody` proves exact preservation of source, destination, standard and unrelated fields from any initial plant through every allowed finite trace. Source equality includes the complete source record, rather than only its label or payload. Its local preservation obligation is discharged by the unchanged accepted-source frame theorem.

`trace_counters` proves four exact equalities: final rule version and rule-history length equal their initial values plus the number of installation landings; final draft revision and draft-history length equal their initial values plus the number of repair landings. These are event counts, not receipt counts. An admitted landing increments the corresponding audit structure even when the displayed rule or draft value is unchanged. History contents are governed by the complete per-event source effects; the counter theorem itself concerns their lengths.

### Permanent fixed-action exclusion

`fixed_action_excluded_after_continuation` strengthens the immediate-successor core theorem. After a successful local action, from a reachable common state containing its exact successor, every lawful finite continuation leaves the action's expected revision/version strictly behind the actual applicable counter. A second successful source step would contradict the exact trace counter law. The result quantifies over arbitrary later policies and time annotations and requires no cancellation certificate.

This concerns the fixed action, including its expected version or revision. Fresh correctly versioned operations remain available when separately authorized and valid.

### Non-vacuous two-stage history

The existence witness fixes four roots, fault budget one, repair/revocation thresholds three, and lifetime-faulty set `{0}`. Its chosen path is the intact ordered list `[1,2,3]`.

The 16-event trace explicitly performs three preparations and installation, a request with three acknowledgements and completion, three policy deliveries, then three preparations and repair. It uses raw policy epochs 0 and 1 and a compact three-value source fixture. The installation and repair have distinct operation-specific grants.

The complete final plant equals the specified repaired record. The result checks non-damage, both goals, custody, rule version 4, draft revision 9, rule history `[normalizedLF]`, draft history `[[88],[65,66,67,10]]`, and exactly one landing of each operation. This is a genuine trace existence result. It provides neither a scheduling guarantee nor a simulation of the earlier compiled raw2-to3 fixture.

The subsequent cancellation trace includes acknowledgements from two distinct selected roots and a close event. Its complete-envelope certificate excludes landing after every further allowed finite continuation and at every later annotation.

### Controls and their precise force

- `no_full_plant_table_injection` rules out an injective encoding of the entire unbounded `Plant` type into the predecessor's four binary-table values. It leaves weaker abstractions open and does not itself construct infinitely many reachable plant states.
- Fresh same-rule installation demonstrably changes version and history. The old action rejects from its successor.
- Equal nonce and equal selected-root set do not identify a tampered successor envelope. Ordered list paths remain distinct command identities even when their finite-root sets agree.
- The live full-successor comparison blocks an overwrite that would erase an intervening rule audit update from a cached plant observation.
- The expiry example establishes different admission outcomes at the two stated annotations; it does not establish authenticity of either observation.
- External reservation is shown to be an additional premise using an actually reachable admitted operation.
- The dropped-revocation control starts from a reachable state. A fresh, still-version-valid old-epoch action is prepared before certified revocation. The actual gate rejects it afterward, while the otherwise identical predicate with the revocation check removed admits it. Thus rejection is not accidentally explained by prior execution of that same action.

The supplied `grant_scope_is_separate` example changes epoch and policy scope as well as grant operation. It proves the two shown mismatches reject; it does not isolate a single grant check. The independent challenges remove that ambiguity by holding the successful fixture's epoch and policy scope fixed and changing only `grant.operation`; both installation and repair reject while `policyAllows` remains true.

## Independent adversarial challenges

`TypedV2Challenges.lean` additionally establishes:

1. Duplicate and out-of-range raw paths cannot inhabit the typed bounded-envelope subtype.
2. A prepared, still-unlanded installation reaches a state with a valid two-root cancellation certificate.
3. The full gate rejects that unlanded operation, while removing only the cancellation check admits it. Its version remains current, so fixed-action replay rejection cannot mask the cancellation control.
4. That complete-envelope cancellation persists through arbitrary finite continuations regardless of future timestamp annotations.

These supplement the unchanged core checks for full-envelope identity, memory representation and the effective-policy limitation of the runtime snapshot relation.

## Scope retained

All history theorems concern the common reference event system with a fixed lifetime fault union, an authentic serial policy source, full-envelope identity, and the modeled atomic plant/time observation. The existing runtime relation remains a snapshot gate/plant-effect correspondence and does not bind every compiled control field or prove preservation by aggregate runtime operations.

No whole-runtime lifecycle, `runBatch`, progress, actual-time authenticity, physical mediation, external grant legitimacy or consent theorem is established by this milestone. N2, T0 and R5 remain outside its conclusions. Public distribution safeguards require their own review independently of these scientific source results.
