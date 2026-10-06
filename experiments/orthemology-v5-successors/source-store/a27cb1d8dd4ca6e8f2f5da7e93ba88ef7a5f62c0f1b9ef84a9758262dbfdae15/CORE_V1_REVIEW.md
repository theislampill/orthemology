# Common operational model: core review

## Verdict

PASS for the exact core statements identified by candidate manifest SHA-256 `a54653b4207b15fcb2079f6bc3094a71cf026aeee9a56d8426f05ac604862b98`.

This is a scoped result: the original binary-table history system is recovered by an exact state and event translation, and the typed system has source-bound local-gate and successful-attempt plant-effect correspondence. The core does not establish whole-runtime lifecycle refinement, a non-vacuous installation-to-repair trace, progress, or physical implementation.

## Verification

All eight imported Lean sources match the pinned accepted predecessor bytes. The three repeated criterion/dynamic imports also match their accepted standalone components. The predecessor evidence archive identity is `f56dab60b87068ce9be4f3b13aa8dc6958bc3d2962467beb580fcd2cd352b553`.

A fresh sequential compilation of those eight imports and all six new modules passed using official Lean 4.19.0, commit `6caaee842e94`, executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. All 6,816 pinned Mathlib source files were checked against their accepted manifest. Its supplied compiled cache was consumed read-only; no independent cache rebuild is claimed.

A separate audit printed the axiom closure of all 85 new theorems. Every closure is contained in `propext`, `Classical.choice` and `Quot.sound`; no custom axiom or proof-hole dependency occurs. Frozen source identities were checked before and after replay. See the replay receipt for exact commands, file hashes and log identities.

## Statement assessment

### Generic kernel

The two interface laws expose only requester and epoch equality already checked by local admission. They do not assume global currentness, plant safety, goal preservation or effect correctness. The structural consistency invariant contains authentic stored policy, non-future epochs, durable revocation memories, selected cancellation acknowledgers and durable full-command tombstones. Its preservation is proved across every event constructor.

The landing-currentness theorem uses an intact path member, source authenticity and revocation-certificate overlap. Equal numerical epochs alone are not treated as equal policies. The separate `authentic_same_epoch` theorem explicitly uses equality to the serial authority source.

The fault set is fixed throughout each complete trace, so the count is a bound on the continuing lifetime union of tainted roots. This does not support an arbitrary moving instantaneous fault budget. Cancellation certificates count distinct selected roots, and the proof depends on an intact selected root's persistent tombstone for the entire command.

The generic `trace_preserves` theorem is an honest conditional proof rule. It does not establish a particular plant invariant until the specialization proves its local admitted-effect preservation obligation.

### Original history correspondence

`lower_step` and `lift_step` cover all ten original event constructors, including arbitrary allowed bad-root corruption. `lower_land` is exact on damaged and unauthorized states as well as reachable safe ones. `trace_iff_lift_exists` is quantified over arbitrary source states and finite event lists, with no reachability or safety restriction. Timestamp erasure is valid because this specialization ignores time; every original trace can be lifted with constant annotations.

This is a correspondence to the exact accepted binary-table system. It does not encode the full typed plant into the four binary-table values.

### Typed specialization and runtime snapshots

The types and operational decisions are the unchanged `ComposedExecution.Plant`, `Policy`, full `Envelope` and `localStep`. The typed command is a subtype requiring a duplicate-free, in-range ordered path. The full ordered path remains part of command identity. `path_card` proves the extracted finite-root set has the original list length; malformed paths are not silently admitted.

Root memories are related extensionally by membership. `rootView_represents` constructs that representation for every actual runtime root, so the local representation obligation is not empty. `root_gate_iff` relates the exact full-envelope live gate at the same plant and time. `successful_attempt_lands` consumes the compiled success guard and its one shared `badOpen` Boolean. `open_attempt_iff_lands` states equivalence specifically for `badOpen = true`; arbitrary false faulty gates may additionally withhold.

`successful_attempt_exact_effect` compares the entire plant successor at a reached common state. Its event timestamp is exactly `World.now`, the argument used by the compiled attempt. The common damage classifier is proved inactive. The theorem does not equate whole runtime states.

The snapshot relation does not bind `World.effectivePolicy`, its budget or revocation threshold, or its completed-certificate list to common control state. Independent proof confirms that changing only the runtime effective policy leaves the relation intact. Consequently these core theorems cannot alone establish current admission under the runtime's effective policy or preservation by every runtime lifecycle operation.

Typed finite-history admission derives the unchanged `localStep` under the common model's current full policy. Complete installation/repair effect records are proved using imported source theorems. Goal persistence discharges its actual source preservation obligation. The core's fixed-action rejection theorem applies to the immediate exact successor under arbitrary later policy and annotation, rather than to every plant after intervening writes.

## Independent boundary checks

The separate `CoreChallenges.lean` kernel-checks the following distinctions:

- Runtime effective-policy changes preserve the core snapshot relation and do not alter the local gate.
- Equal nonce, action and path do not identify envelopes with different complete successors.
- A tombstone for one full envelope does not alias an altered successor.
- Ordered paths `[0,1]` and `[1,0]` give the same finite-root set while retaining different command identities.
- Original-event timestamp erasure is exact for arbitrary annotations.
- Every runtime root has a concrete finite-memory representation.

These checks have only standard Lean logical axiom dependencies.

## Remaining scope

A complete typed history witness, source/custody frame persistence, exact history-count accounting and rejection after arbitrary intervening writes require their separate proofs. Whole-runtime lifecycle or batch refinement is not implied by a snapshot relation. Arbitrary-root-count mathematical results do not expand the existing four-root portfolio's executed coverage.

Event timestamps are unrestricted annotations; the model does not establish their monotonicity or authenticity. Lawful grants, actual consent/reservation, trustworthy source identity, atomic same-plant/time observations, physical mediation, and bounded service remain external premises. No N2, T0 or R5 conclusion follows.
