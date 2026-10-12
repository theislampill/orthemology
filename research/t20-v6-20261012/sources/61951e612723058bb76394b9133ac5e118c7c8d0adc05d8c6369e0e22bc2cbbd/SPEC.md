# Shared-store alias refinement: frozen design v1

This is an additive mathematical reference model and weak forward safety
simulation into the accepted typed-history-v2 kernel. It is not a physical
implementation, observer-equivalence theorem, or progress/optimality result.
The design is the concrete shared-store alternative in ASSESSMENT.md §§3–5.

## Mathematical environment

For a finite label type `Fin m`, use the exact accepted canonical
`AttributionKernel.rootMap A` for one nonempty class A. The actual root domain
is its image; any unused ambient Option names carry no charged role and are
unreachable through a label. The fixed actual faulty set lies in that image
and has cardinality at most B. Require B≥1 and B<m−|A|+1. Let k=B+|A|−1.
Derive the pulled-back bad-label cardinality from the accepted attribution
theorem, never a new axiom. The common configuration has m labels, budget k,
q+r>m+k, q+k≤m and r+k≤m, and the identical authentic serial policy source.

The map/class and fixed fault set are environment/proof parameters. Concrete
events carry only label addresses and complete commands, never root identity
or a map-query result. No controller, strategy, or observation-equivalence
claim is included. Parameter availability to the proof is not an actor oracle.

## State and transitions

The generic reference model uses the accepted `OperationalJoin.Interface m`.
Concrete state contains one `RootState I` per actual root, shared by every
alias, and the common epoch/pending/label-ack/certificate/cancel-ack/plant
coordinates. There is no damage oracle in concrete landing: successful concrete
landing sets the imported interface effect. Every source check observes the
same plant/time. Initial root stores have source policy 0 and empty memories.

Events: request; one real label revocation acknowledgement; completion at
exactly r distinct label receipts; delivery of any certified source policy
with 0<e≤current epoch (including delayed/repeated older policies, which leave
the shared store unchanged when its descriptor epoch is already at least e);
selected-label preparation guarded by the concrete envelope; selected
full-command cancellation acknowledgement with the exact recipient check;
close at more than k label cancellation receipts; admitted landing; hold;
corruption of a fixed bad actual root. Corruption is an environment event, not
an actor operation. Extra standalone closure/clock events are not needed for
the first package and will not be silently added.

A good acknowledgement changes its actual root's shared revocations but only
the real responding label's receipt. Good cancellation analogously changes
the whole root's full-command tombstone store and records only the responding
selected label. Preparation and policy delivery update the one shared store.
The pending acknowledgement set is preserved literally. Completion is enabled
only when its cardinality equals r, matching the accepted common rule; this
model does not silently discard extra real receipts or choose an r-subset.

## Refinement relation

All control coordinates and plant are exact; the reached abstract state is
safe. At every good label i: policies are equal; abstract commitments equal
shared concrete commitments filtered to commands whose paths select i;
abstract revocations are a subset of shared concrete revocations; abstract
tombstones are a subset of shared concrete tombstones. Bad-store contents
are unrestricted in the relation.

Each concrete transition must have a finite common trace preserving this
relation. Root-wide preparation expands into internal prepare steps at the
selected aliases of its actual root. Delivery expands into internal delivery
steps at all its aliases using the same already certified source policy.
Neither expansion adds a label reply or owner acknowledgement. A concrete
landing maps to exactly one abstract landing of the same complete command;
all other expansions contain no landings. The direction of gate implication
is concrete permit → abstract permit. No converse is expected.

The trace is a proof witness, not an observable transcript. Real receipt sets
remain equal at every related endpoint. The expanded common event list is not
given to the actor, and no opacity claim is derived from it.

## Typed specialization and claims

Specialize to the unchanged full `BoundedEnvelope m`, imported Plant and
source localStep. Derive current full-policy admission, whole successor/frame
effect, finite custody, exact install/repair counters, fixed-action exclusion
through continuations, and permanent certified cancellation exclusion.
Connect compiled live gate decisions only at the explicit flattened concrete
snapshot, preserving the source's single `badOpen` Boolean. Do not assert that
unchanged label-local runtime storage macros implement shared-root updates.

Formalize the literal-pullback obstruction: from Initial, an intact label
cannot acquire a commitment or tombstone for a command not selecting it.
A good shared root can acquire such a literal pulled-back store at an
unselected alias. Also formalize that shared closure must not add fake labels
to acknowledgement sets.

## Verification and exclusions

Use official Lean 4.19.0 and pinned Mathlib read-only. New modules and logs live
only under this research directory; accepted sources are copied exactly or
imported from verified accepted read-only builds. Freeze immutable milestones
with input/source manifests for independent review. Audit every new theorem's
axioms and admit only propext, Classical.choice, Quot.sound. No proof holes,
custom axioms, unsafe/native truth escapes, or hidden admission assumptions.

No canonical/product edits, new dependencies, physical-world warrant, moving
fault/map envelope, R5 expansion, 21-path native execution, progress/service
bound, observer-equivalence, opaque search lower bound, or optimality transfer.
The mutable raw2-to3 extension is not an imported dependency.
