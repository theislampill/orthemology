# Independent review: frozen shared-alias simulation v1

Disposition: PASS for the bounded weak forward safety simulation and its
stated generic corollaries. No blocker found. This is independent review
evidence for the parent; it does not accept a tranche, change a lifecycle,
release a package, or claim the separate typed/runtime deliverable is finished.

## Exact object and replay

- Candidate: `tranche8/research/alias-runtime/milestones/simulation-v1`.
- Manifest SHA-256: `ec8c27090492a603ea7daa7d33b6e2d24c1bfe51e1efbe0b47367ad0c684c93b`.
- All 23 manifest entries match. All 21 input-binding entries and all 20
  accepted typed-history-v2 manifest entries match.
- `AliasModel.lean` and `AliasObstruction.lean` are byte-identical to reviewed
  model-v1. `ModelControls.lean` changes only the proof style of the receipt
  equality, without altering its theorem statement. Specification/input/import
  identities are unchanged.
- Independently cold-compiled the 4 frozen attribution imports, 8 candidate
  modules, and 3 interface/axiom controls: 15 sequential official Lean 4.19.0
  `-j1` stages, all exit 0.
- The 53 printed candidate theorem closures cover all 53 top-level theorem
  declarations in the 8 candidate modules. Every closure uses only `propext`,
  `Classical.choice`, and `Quot.sound` or subsets. No candidate proof holes,
  custom axioms, unsafe definitions, or native truth escapes were found.
- Mathlib c44e0c8 and the independently verified accepted common build are
  read-only reused dependencies. The full dependency cache was not rebuilt.
- Replay evidence: `simulation-v1-replay/replay.py`, `RECEIPT.json`, and `logs/`.

## Semantic review

### Relation and gate direction

`RootRefines` demands exact descriptor equality, abstract commitments equal to
concrete commitments masked by whether the individual label is selected by the
complete command, and abstract revoked/cancelled sets contained in concrete
sets. These directions are correct:

- At a selected good label, a concrete commitment supplies the abstract one.
- A concrete absence from the larger veto set gives abstract absence.
- An unselected alias is not forced to hold an unreachable abstract commitment.
- Additional shared concrete vetoes may reject an action the abstract permits;
  reverse gate implication is neither proved nor required.

`Refines` preserves every common control coordinate, the complete plant,
actual real label receipt sets/functions, and certificate function exactly. It
leaves faulty-label stores unconstrained, while correlated fault membership
ensures no good alias can share a corruptible actual root.

### Initiality and absence of a hidden safety premise

The relation contains abstract `damaged = false`, but this does not assume the
concrete safety result: `initial_refines` proves it initially. The step theorem
uses accepted structural `Consistent` history facts, and finite simulation
obtains/preserves these from accepted `consistent_initial` and `consistent_trace`.

Concrete landing still checks local shared-store permits and performs `I.effect`
without a damage oracle. Its matching abstract landing invokes the accepted
current-authorization theorem to establish the non-damage branch, then proves
exact plant-effect equality. The reachable concrete `admitted_current` corollary
therefore derives requester, current epoch, and full source-policy admission.
No desired admission or current-authorization field has been added to the
concrete state/step interface.

### Root-wide expansion

Preparation expands exactly over selected labels in the addressed root's
fiber. Every good alias has the same concrete descriptor, and concrete
permission supplies each abstract envelope. Preparation does not change plant,
policy, revocations, or tombstones, so all later internal guards remain valid.
The insertion lemma is idempotent even when a label is repeated; finite-set
induction supplies a finite legal trace.

Delivery expands over the addressed root's full fiber, preserving the original
`0 < e <= epoch` guard. The same certified source policy is delivered to each
alias. Each label independently takes the newer-policy branch or stale-policy
identity branch. Exact good-label descriptor equality ensures all good aliases
match the single shared-store result, including delayed/repeated delivery.

The batch states preserve both receipt sets/functions and certificates
literally. The constructed trace uses only prepare or deliver events, so it
introduces no acknowledgement events or landing events. Those internal events
are proof witnesses and may reveal the fiber if exposed; observational equality
or a hidden-map actor interface is explicitly outside the theorem.

### One real acknowledgement and cancellation

The acknowledgment/cancellation branches use exactly one corresponding common
label event. The concrete action may add vetoes at other aliases, which only
enlarges the concrete veto sets and preserves the one-way relation. No alias
receipt is synthesized. Completion consumes exactly the unchanged accumulated
r-label set, including its exact function update into certificates. Close uses
the same k-label threshold and full-command cancellation ledger.

### Corruption and stuttering

A concrete bad-root corruption changes no good-store projection, so a common
empty trace is sufficient. Concrete hold also stutters. This is appropriate to
the relation and safety-only observation boundary; no equivalence of bad-state
contents, event counts, or controller observations follows.

### Finite traces and landing identities

Each concrete event has a finite common trace with the same projected list of
landings. `landings` retains the complete command value, requester and time,
in order. The landing branch uses exactly one identical common landing, and
all other branches introduce none. Concatenation and finite induction preserve
that list exactly; this is stronger than bare landing-count equality.

The initial theorem supplies a common trace from the corresponding actual
initial plant, not merely an arbitrary safe abstract state. Reachability
witnesses and persistent certified cancellation are then transported through
accepted common-history theorems with exact cancellation receipt equality.
For cancellation, the conclusion covers arbitrary lawful finite continuations
and arbitrary later requester/time for that same complete command.

## Controls and independent pressure

The author's controls distinguish the valid gate direction from the converse,
reject reversed revocation inclusion, reject missing selected commitment
coverage, and prove receipt-free preparation/delivery batch endpoints.

The reviewer additionally compiled five fixture theorems in
`simulation-v1-replay/ReviewerSimulationControls.lean`:

1. A concrete command is present at its good unselected alias while the related
   abstract alias correctly masks it out.
2. One real acknowledgment leaves an unmatched shared veto at the other good
   alias and still relates to a common state with exactly one label receipt.
3. Preparing a command selecting both aliases is a lawful concrete step.
4. Both selected aliases acquire abstract commitments in its batch endpoint.
5. That lawful concrete step has a common reachable witness with exactly empty
   owner/cancellation receipt sets and no landings.

These provide non-vacuous seven-label tests of the two contrasting alias cases.
All five reviewer theorem closures are standard-only. The first reviewer draft
left one simplification goal open; its failed log is retained separately, and
only the corrected kernel-checked final source/log is credited.

## Claim boundary retained

- This realizes an explicit shared-store reference model. It is not a theorem
  about every implementation with correlated failures.
- Fixed root map/fault set, authentic serial source, coherent shared storage,
  and same plant/time observation remain mathematical/model premises.
- No physical routing, crypto authentication, wall-clock service, progress,
  observation opacity, native 21-path controller, lower bound, or optimality
  transfer is established.
- Full typed envelope instantiation, frame/custody/counter/fixed-action
  consequences and compiled runtime snapshot adaptation remain separate.
- The general arbitrary receipt-preserving revocation-history impossibility
  remains ordinary analysis, as the candidate scope explicitly acknowledges.
- No accepted or canonical source/dependency was modified. Review artifacts
  are confined to `tranche8/reviews/alias-runtime`.

## Packaging observation

The frozen `verify_development.py` and `lean.sh` are author working-layout
helpers, not standalone replay entrypoints for this snapshot. In particular,
`verify_development.py` derives the accepted source path relative to the research
working directory and writes build/evidence outputs. The snapshot's extra
`milestones/simulation-v1` depth does not satisfy that path assumption. The author
explicitly confirmed this boundary and intends to omit or repair those helpers
before public packaging. This review used its own isolated replay script, and
used the frozen Lean wrapper for extra reviewer controls only with an explicit
review-build override. No standalone distribution or public replay claim is
credited; this observation does not invalidate the scientific source proof.
