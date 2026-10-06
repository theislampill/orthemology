# Independent review: frozen typed shared-alias safety v1

Disposition: PASS for the stated mathematical typed-safety and source-gate
snapshot scope. No scientific blocker found. This is review evidence for the
parent, not tranche closure, lifecycle acceptance, public release, or a
standalone replay-packet claim.

## Exact object and independent verification

- Candidate: `tranche8/research/alias-runtime/milestones/typed-v1`.
- Manifest SHA-256: `1b88370e522b085349c6da4c0aab1b3763b557e02c3c4eb6d631f9d4ab4636d7`.
- All 38 candidate manifest entries match their sizes/hashes. All 21
  input-binding entries and all 20 accepted typed-history-v2 entries match.
- The eight generic/model/simulation modules are byte-identical to reviewed
  simulation-v1. The four new modules are `AliasTyped`, `AliasRuntime`,
  `AliasTypedWitness`, and `AliasTypedControls`.
- Cold-compiled 4 frozen attribution imports, 12 candidate modules, and 4
  target/axiom controls: 20 sequential official Lean 4.19.0 `-j1` stages,
  all exit 0 and no warnings.
- The 88 candidate axiom prints cover all 88 top-level theorem declarations
  in those 12 modules. All closures contain only `propext`, `Classical.choice`,
  `Quot.sound`, or subsets; there are no proof holes, custom axioms, unsafe
  definitions, or native truth escapes.
- Shared Mathlib c44e0c8 and the already independently verified accepted common
  build were reused read-only. This is a cold candidate/import replay, not a
  fresh rebuild of the entire dependency cache.
- Evidence: `typed-v1-replay/RECEIPT.json`, `replay.py`, and `logs/`.
- Five additional reviewer theorem controls compile with standard-only axioms.
  All five frozen source mutants were independently rejected in isolated output
  directories, with the expected scientific elaboration failures.

## Typed consequences

### Full typed source admission and effect

The environment specializes the unchanged accepted `interface m` with full
`BoundedEnvelope m`. The subtype retains the complete envelope, including
ordered path, nonce, actor, action and entire successor; its separate path
projection is a finite set only for membership/quorum reasoning. No weakening
to nonce identity, path support, or target-only state occurs.

`finite_history_admission` consumes the already derived generic reachable
admission and recovers the current authentic source `localStep`, requester and
epoch. The concrete effect is the entire supplied successor, and the accepted
local-step theorem restricts that successor to the whole lawful source effect.
`install_full_effect` and `repair_full_effect` therefore preserve the complete
frame while performing precisely their respective rule/draft updates and
version/history changes.

### Custody and exact histories

Custody transports complete equality of source, destination, standard and
unrelated plant coordinates from the common witness. Installation and repair
counts are explicitly factored through the full ordered landing list. Because
the generic simulation preserves that list, internal preparation/delivery steps
cannot add a count. The four exact counter laws hold over arbitrary lawful
finite concrete continuations from a reachable concrete state.

Goals persistence is conditional on the goals already holding, and fixed-action
exclusion is conditional on an accepted original local step and a reachable
state whose plant is that action's successor. These are accurate premises, not
claims that every trace achieves a goal or that an arbitrary command becomes
replay-proof without being executed. Under those premises the same action stays
rejected after every lawful finite continuation, including arbitrary later
policy/time annotations.

## Source-gate adapter: correct separation of two abstract views

`rawRoot` converts the shared finite memories to source lists with exact
membership preservation. `Subtype.ext` preserves complete raw-envelope identity;
list enumeration order is irrelevant only to root-memory membership, not to
command-path identity.

`literalSnapshot` pulls every actual store back to every label literally. It
is used only for the exact source gate representation theorem and is expressly
not assumed common-reachable. That limitation is essential: the reviewed
out-of-path obstruction applies to such snapshots. The reachable common witness
is instead supplied by the separate asymmetric weak relation.

`gateWorld` has m observable labels, budget k, actual pulled-back taints, the
actual modeled plant/time, and one shared-store view at each alias. Out-of-range
source indexes use padding but cannot occur in a well-formed typed path. Its
completed-certificate list is empty and intentionally not a lifecycle model.
Inspection of the unchanged `ComposedExecution.attempt` confirms that it checks
path validity and live gates, then either installs the complete successor or
leaves the world unchanged; it does not inspect completed certificates or
`effectivePolicy`.

The original single `badOpen` Boolean is retained throughout:

- Source success implies concrete `Lands` for either Boolean value.
- With that one Boolean true, source success is equivalent to concrete `Lands`.
- False can additionally withhold at selected faulty labels.

No independent per-root bad-choice interface is silently substituted. On a
concrete reachable state, source success gives current-policy local admission
through the weak witness and the exact concrete plant effect. Source rejection
preserves the full gate snapshot. No whole-runtime prepare/cancel/certify macro
refinement or gate-snapshot reachability is asserted.

These are kernel-checked theorems about the source Boolean functions. The
review does not claim a native executable controller run, measured timing, or
a physical gate implementation.

## Non-vacuity and identity/receipt controls

The typed fixture uses the accepted compact three-byte source unchanged with
7 labels, the good shared alias class {0,1}, one faulty actual singleton at 6,
B=1, k=2, and q=r=5. Its full command path is [0,1,2,3,4]. Four lawful concrete
preparation events at actual roots addressed by 0,2,3,4 make all five selected
label gates ready. The source attempt is proved true with the exact installed
plant. The witness is an installation at raw epoch 0, not a two-stage unknown-
class controller or an executed 21-path search.

The separate still-unlanded cancellation branch records precisely {0,2,3}.
Alias 1 shares the tombstone but is not counted as a reply. The old localStep
remains version-valid at the cancelled plant, so rejection is genuinely due
to cancellation, not accidentally explained by a prior installation. The
k+1-label certificate and generic theorem exclude future concrete landings.
A reviewer corollary additionally checks the resulting source attempt is false
for arbitrary lawful continuations, time, requester and `badOpen`.

Reordered [1,0,2,3,4] has the same nonce and support but is proved a different
complete command and is not the original command's tombstone. That is exactly
the required identity boundary; it does not claim a reordered command will
necessarily be admitted.

## Independent reviewer controls

`typed-v1-replay/ReviewerTypedControls.lean` proves:

1. The fixture has a complete lawful concrete preparation-plus-landing trace.
2. That concrete trace increments only ruleVersion and ruleHistory length,
   each by exactly one, and preserves draftRevision/draftHistory length.
3. The same concrete trace preserves the entire custody frame.
4. A typed compiled attempt is false after any certified concrete cancellation
   and arbitrary lawful finite continuation, for any later requester/time and
   either source Boolean.
5. A full typed literal shared-store pullback with an unselected good alias is
   not common-reachable, confirming why gate representation and weak reachable
   simulation cannot be conflated.

All five compile in the independent typed build without warnings or nonstandard
axioms.

## Mutation evidence and its limits

The exact frozen mutations independently fail as follows:

- Actual B substituted for k: existing configuration proofs no longer typecheck
  against the fault/quorum obligations.
- Alias receipts invented: the exact one-real-label receipt theorem fails.
- Cancellation writes `some i` instead of the actual root address: shared
  cancellation cannot be proved.
- Revocation subset reversed: concrete-to-abstract envelope transfer fails.
- Selected commitment mask removed: the existing gate proof's selected-coverage
  construction no longer matches its relation type.

These are real source-sensitivity controls, not just copied author failure logs;
all imports were available and errors occurred at the intended proof obligations.
However, a source mutant rejected by its unchanged proof is not a theorem that
no alternative implementation or adapted proof could work. In particular, the
mask mutation first fails on proof-constructor shape; the substantive necessity
for this chosen reachable shared-store relation is supplied separately by the
trace-wide out-of-path obstruction. The controls are bounded, not exhaustive
fault-model or architectural validation. Rejected output directories never
enter any successful proof import path.

## Remaining limits and packaging

The packet preserves its scope: explicit shared storage, fixed map and lifetime
fault set, authentic serial policy source, source legality, actual modeled
plant/time, and durable root-wide vetoes. It proves no observer equivalence,
map secrecy/noninterference, controller/selector realization, service/progress
or clock-authenticity bound, physical routing, opaque-search premise, or
optimality transfer. It imports no mutable raw2-to3 lifecycle extension.

The general receipt-preserving revocation-history impossibility remains ordinary
analysis. The generic commitment/tombstone obstruction and exact receipt updates
are the formal claims.

The misleading working-layout helpers from simulation-v1 are absent here.
Standalone fail-closed source-only replay packaging is a separate forthcoming
object and must get its own identity and review. Nothing in this scientific
review certifies such a wrapper or fresh full-dependency rebuild.

No accepted or canonical source/dependency was modified. Review artifacts are
confined to `tranche8/reviews/alias-runtime`.
