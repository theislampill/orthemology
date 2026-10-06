# Independent review: frozen shared-alias model v1

Disposition: PASS for the explicit mathematical model, derived budget,
selected-memory obstruction, and bounded model controls only. This is review
evidence for the parent, not a tranche acceptance, release, lifecycle transition,
or completion claim. No safety simulation, typed consequence, implementation
refinement, observational equivalence, progress, or optimality is credited here.

## Exact object and verification

- Candidate: `tranche8/research/alias-runtime/milestones/model-v1`.
- Manifest SHA-256: `57051ce8043da3054e56afd685b49a3619c94388e501a0a1c48c89d2b8c81181`.
- All 11 manifest entries match their recorded sizes and hashes.
- Approved design-v1 manifest: `bbf2a99b414232c48268c291e813bebb22ffa4a1cf708097da3eac128e80eca2`; all 4 entries match.
- The candidate specification adds explicit delayed/repeated source-policy
  delivery and exact-r/no-receipt-discard semantics. Those changes match the
  parent's review instruction and the unchanged common kernel. They also occur
  in design-v2, manifest `61f3e0a7c9926529daea1206d024cf77d14f561e866388d486e901707788a70e`.
- All 21 input-binding entries and all 20 accepted typed-history-v2 manifest
  entries match. The four frozen attribution imports match their accepted
  central-v1 source files byte-for-byte, including `FixedFamilies.lean`, which
  is bound by the candidate manifest rather than listed separately in its input
  binding.
- Independently compiled the four frozen attribution imports, `AliasModel`,
  `AliasObstruction`, `ModelControls`, and both model control files, in sequence
  with official Lean 4.19.0 and `-j1`. All 9 stages exited 0.
- All 21 candidate theorem axiom closures contain only `propext`,
  `Classical.choice`, and `Quot.sound` (or subsets). No candidate proof hole,
  custom axiom, unsafe definition, or native truth escape was found.
- Shared pinned Mathlib and the already independently verified accepted common
  build were read-only. This replay cold-built the candidate and attribution
  imports; it did not independently rebuild the full dependency cache.
- Evidence: `model-v1-replay/RECEIPT.json`, `replay.py`, and `logs/`.

## Findings and challenges

### 1. Actual roots and fault cardinalities: pass

`Environment` fixes one nonempty canonical alias class and one lifetime actual
fault set contained in the root-map image with cardinality at most B. The
common label configuration uses k = B + |A| - 1, not B. `label_budget` actually
uses accepted `tainted_label_budget`; the upper bound is not an assumed field.
`label_budget_lt` uses the declared non-saturation condition and class size.
`good_same_root` prevents a single actual root from being simultaneously good
and bad at different aliases.

The concrete storage function has the ambient type `Option (Fin m)`, rather
than an image subtype. This is harmless within the stated model: only labels
address stores, every such address lies in the actual image, and faults are
restricted to that image. Reviewer kernel controls additionally prove every
legal step leaves every unused ambient root coordinate unchanged. Unused names
are not charged as roots and cannot affect a gate.

### 2. Shared state versus label receipts: pass

Preparation, delivery, good revocation acknowledgements and good cancellation
acknowledgements modify one actual root's shared store. Acknowledgement and
cancellation receipt updates use precisely the supplied real label. They never
insert its aliases. The candidate's seven-label controls exercise both shared
veto propagation and one-label receipt sets.

Reviewer controls additionally establish that preparation and delivery preserve
both complete receipt functions/sets, and that one real cancellation reply
cannot enable a close event at k=2. These support the required distinction
between store propagation and actual authenticated replies; they do not prove
an external network emitted or authenticated any message.

### 3. Out-of-path literal pullback: pass within shared-store scope

`SelectedMemory` is a genuine invariant of every accepted common trace from
`Initial`, proved by exhaustive accepted-step induction. At a good label it
prevents both commitments and tombstones for commands that do not select the
label. `no_reachable_literal_prepare` and `no_reachable_literal_cancel` thus
exclude even a one-command membership match with the shared store of a good,
unselected alias. This is stronger than merely showing a single common step
fails to match.

The generic obstruction statements allow arbitrary concrete prestate and pure
update functions; the seven-label fixtures separately show lawful preparation
and cancellation from an initial state. The review adds the explicit seven-label
cancellation obstruction as well. These are real reachable shared-store
examples, not generic proof schemata with impossible premises.

The controls use a simple generic interface, not the full typed envelope.
The later typed specialization must preserve complete ordered command identity.
This obstruction is not an impossibility theorem for every architecture with
correlated faults. Separate label-local memories under one failure unit remain
outside its scope.

### 4. Completion and delivery boundaries: pass

The completion constructor requires exactly r distinct accumulated labels.
There is no subset selection or receipt deletion to recover an overshot round.
The reviewer control proves a state with six receipts cannot complete when r=5.
This is a potentially restrictive progress behavior, but the package correctly
makes no progress claim and matches the accepted kernel.

Delivery allows every source epoch satisfying 0 < e <= current epoch. The
shared descriptor advances only when its stored epoch is less than e. Delayed
or repeated older policy delivery is allowed and then does nothing. Reviewer
controls prove the old-policy identity case. The guard is a certified-history
abstraction inherited from the accepted kernel; it is not a cryptographic
certificate-verification implementation. Relating reachable concrete histories
to those certified common histories remains the next milestone's obligation.

### 5. Landing and model boundary: pass with claims held

Concrete landing has no damage classifier or desired safety premise; it uses
local shared-store permission at good selected labels and performs the imported
interface effect. Its successful landing rule treats bad selected labels as
non-vetoing, an adversarial upper-safety abstraction. A later runtime gate
correspondence must retain the source's single `badOpen` Boolean explicitly.

Environment access to the map, fixed faults, source, plant and annotated time
is mathematical parameterization. The files do not prove that an actor is
unable to inspect any of it, nor do they formalize observable transcripts,
clock authenticity, physical routing, bounded service, or a controller.

## Independent reviewer controls

`model-v1-replay/ReviewerControls.lean` cold-compiles with 8 standard-only axiom
closures:

1. Every label address is in the actual root image.
2. Every step leaves unused ambient roots unchanged.
3. Stale/repeated delivery is the identity when the descriptor is already new enough.
4. Delivery preserves both receipt sets/functions.
5. Preparation preserves both receipt sets/functions.
6. Excess real receipts cannot complete an exact-r round.
7. One real reply cannot manufacture the k+1 cancellation certificate.
8. A lawful shared cancellation has the unselected-alias literal-pullback obstruction.

The first reviewer draft had constructor-pattern naming errors; the final
source and `ReviewerControls.log` compile without errors and contain no
`sorryAx`. The failed draft log is retained separately and is not credited.

## Remaining milestones and interpretation limits

- Pending: initial/step/finite-trace refinement, correct selected commitment
  mask and veto subset directions, root-wide preparation/delivery expansions,
  exact control/plant preservation, and one-for-one command-preserving landings.
- Pending: full typed safety, successor/frame effects, custody, exact counters,
  fixed-action continuation exclusion, permanent cancellation, and the flattened
  compiled snapshot gate boundary.
- The stronger prose claim that no arbitrary receipt-preserving common trace
  can reproduce an exact shared revocation pullback is not a separate candidate
  theorem. What is kernel-checked here is exact one-reply updates, shared
  revocation at aliases, and the trace-wide commitment/tombstone obstruction.
  Do not silently promote the stronger revocation-history claim to formal status.
- No accepted/canonical source or dependency was modified. New review files
  are confined to `tranche8/reviews/alias-runtime`.
