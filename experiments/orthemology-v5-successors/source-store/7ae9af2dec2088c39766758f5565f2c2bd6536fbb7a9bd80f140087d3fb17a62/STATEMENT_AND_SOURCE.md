# Finite-history safety for the accepted dynamic V2 interlock

## Exact scope

This is an additive kernel extension of the **original dynamic V2 finite-root,
whole binary-table interface**. Its controlling sources are the frozen accepted
`base-v2/MODEL_AND_PROOFS.md` and `base-v2/dynamic_interlock.py`, with the accepted
`review/BASE_REVIEW_V2.md` sidecar. Exact bytes are recorded in
`SOURCE_BINDING.json` and checked before and after replay. No predecessor,
accepted proof, protocol, threshold or claim is changed.

It is **not** a proof of the separately typed version/history-changing compiled
composition, any unknown-label attribution-map interface, complete search/covering
optimality, randomized search, physical hardware, external consent, unbounded
mobile-fault tolerance, or R5 defeat. There is no new novelty claim.

## Quantified result

For arbitrary `n,B,q,r`, the model retains the accepted full threshold contract:

- `0 ≤ B < n`, a finite set `F ⊆ Fin n`, and `|F| ≤ B`;
- `n+B < q+r`, `q+B ≤ n`, and `r+B ≤ n`;
- an externally authoritative serial source `source e` with control epoch `e`.

A finite trace starts with all root descriptors equal to `source 0`, empty
revocation/commitment/cancellation stores, no pending owner proposal, and a
non-damaged plant with an arbitrary whole table (therefore including every
allowed defective initial table). The trace may contain arbitrarily many:

- serial owner requests and individual root acknowledgements;
- effective transitions only after exactly `r` distinct acknowledgements;
- delayed, repeated, out-of-order local deliveries of completed authentic
  certificates;
- individual command preparations, including stale deliveries and attempted
  replay;
- authenticated selected-root cancellation acknowledgements, and close events
  only after more than `B` distinct selected acknowledgements;
- same-command atomic live landings, holds/blocked attempts, and arbitrary state
  changes at roots in `F`.

`finite_history_safety` proves by actual transition/finite-trace induction that:

1. every reached good-root state remains consistent with the authentic serial
   history;
2. the plant never enters absorbing damage `X`;
3. at the pre-state of **every admitted landing in the trace**, the command's
   epoch equals the effective epoch, its requester equals its bound recipient,
   and the complete command equals the allowed current descriptor in target ID,
   target version, recipient, scope and both table entries.

The authorization conclusion is `AuthorizedTrace`, a proof over the same step
sequence. `step_deterministic` proves an event has only one successor, so this
certificate cannot select a safer alternative execution. `finite_history_admission`
also gives the direct universal result for any actual reached finite-prefix
pre-state and any admitted command. It is not a field assumed of the transition system or of the induction
invariant. A guard never consults that proof.

`no_landing_after_cancellation` proves that after a completed cancellation
certificate, **every arbitrary finite allowed continuation** still prevents the
same full command/nonce/path from landing, for every requester.

`admitted_repair_restores` proves that an admitted repair establishes the whole
current table. `stable_trace_preserves_goal` proves that once restored, every
finite allowed continuation with the same effective epoch preserves that table
and absence of damage. Endpoint epoch equality suffices because epoch
monotonicity is separately proved. This is conditional persistence, not a
claim that a successful landing must occur.

## Why the central induction is not circular

`Consistent` contains only six structural history facts, all established from
`Initial` and preserved separately for each explicit `Step` constructor:

1. each root outside `F` stores `source e` for its actual local epoch `e`;
2. that local epoch is at most the effective epoch;
3. for every completed old epoch, an actual stored `r`-certificate exists and
   every good acknowledger retains that old epoch in its revoked set;
4. every good pending acknowledger has already recorded the current epoch as
   revoked, before the certificate completes;
5. every recorded cancellation acknowledger belongs to that command's actual
   path;
6. every good cancellation acknowledger already has that full command in its
   durable tombstone set.

The invariant does **not** assume that landings are safe, that gates know the
current global epoch, that local descriptors equal the latest descriptor, or
that an old command has already been ruled out.

The proof first extracts a good member of each actual `q`-path using finite set
cardinality. That member's *local* checks show the command matches some authentic
completed epoch and cannot be future. If that epoch is old, cardinality provides
a good overlap with the actual stored revocation certificate for that epoch.
Its still-present revocation tombstone contradicts the claimed live opening.
Only then is global-current authorization concluded. Cancellation similarly
extracts one good selected acknowledger from more than `B` replies, and uses its
actual persistent tombstone to contradict live opening.

`step_memory` and `trace_memory` separately prove monotonicity of good-root
revoked and cancelled stores. `step_cancelAcks` and `trace_cancelled` prove that
recorded cancellation evidence remains available. Neither theorem takes
monotonicity as an unproved trace premise.

## Source-to-model correspondence

| Accepted source | Formal representation | Qualification |
|---|---|---|
| §2.1 `D_e`, whole two-input rule and X | `Descriptor`, `Table := Bool × Bool`, `State.table`, `State.damaged` | Identifiers are equality-only natural tokens; the two table entries are unchanged. Control epochs are numbered from the session's initial epoch. |
| §2.1 legitimate serial owner, one pending proposal | `Config.source`, `State.pending`, `Step.request`, `Step.complete` | A fixed source sequence is an arbitrary authoritative serial sequence quantified by the theorem, not a future-knowledge oracle. The pending next descriptor is implicit as `source (epoch+1)` because there are no competing proposals. |
| §2.2 lifetime union and root duties | `Config.faulty`, `Good`, `Step.corrupt` | `F` is a proof-side fixed superset of roots ever faulty in the entire claimed finite history. All root duties share it. |
| §2.3 serial actual-path gates | `Command.path : Finset (Fin n)`, `ValidPath`, `Lands`, `Step.land` | Every good actual-path gate checks the same actual command at the instant of landing. Bad gates may choose opening; their withholding is represented by no landing/hold. |
| §2.4 full command and exact commitment | `Command`, `RootState.commitments`, `Envelope`, `Permits`, `Step.prepare` | Equality of commands includes nonce and actual path. The authenticated requester is a semantic input, not authentication inferred from a printed identity. |
| `Root.local`; `Root.prepare`; `Root.permits` | `RootState.descriptor`, `Envelope`, `Permits` | The guard reads only root-local descriptor, commitments, revocations, cancellations and requester. It reads neither the global epoch, `source`, nor `F`. |
| §2.5 close before acknowledge | `acknowledge`, `Step.acknowledge` | Every good acknowledger inserts the current epoch before its label enters `acks`. No new descriptor is installed at this point. |
| `World.revoke` | `request`; individual `acknowledge`; `complete` | This refines the Python atomic operation into the allowed ordinary-proof microsteps, permitting early close and interleavings. It does not enable an early new epoch. |
| `World.completed`; `World.deliver` | `certificates`, `Step.deliver` | An epoch can be delivered only after completion. Old delivery cannot rewind a local descriptor. Local delivery is per root as allowed by §2.5; Python's all-good bulk delivery is a sequence of these steps. |
| `World.attempt` | `Lands` followed by `land` | The global descriptor is consulted **only after admission**, to classify the effect as damage or exact repair. It cannot veto the landing. |
| §2.6 root cancellation and retained cleanup right | `cancelAck`, `Step.cancelAck`, `Cancelled`, `Step.close` | The good root requires requester=original recipient, independently of current action permission. Tombstone is installed before acknowledgement. |
| §2.7 safety and stable persistence | `finite_history_safety`, `no_landing_after_cancellation`, `stable_trace_preserves_goal` | Arbitrary finite histories and continuations; all writes remain mediated. No progress/service scheduler is encoded. |

There is no separately mechanized Python-to-Lean compiler/refinement proof.
The source correspondence above is an explicit mathematical/modeling argument,
with seven bounded original-source replays in `source_replay.py` and independent
cold review requested. The kernel proves the displayed Lean transition system.

The model's `Step.corrupt` permits arbitrary root-local changes only within `F`.
A faulty root may mimic an honest one, erase memory, or keep old commitments.
Granting it that freedom even before its first real fault is a conservative
safety overapproximation. `F` is not exposed to any actor or good gate, is not
inferred from successful behavior, and does not reset between epochs.

Serial ordering, certificate authentication and authority are source premises.
The formal source schedule does not select or establish a legitimate owner.
Since the descriptor sequence is arbitrary, fixing it as a parameter expresses
all possible serial owner choices, rather than requiring that actors predict
future choices. `source` is only installed locally after actual completion.

## Operational premises kept separate

### Coherent root-wide veto, beyond shared failure correlation

Each root's descriptor and durable stores are consulted by **every relevant
physical gate copy it owns**. An epoch acknowledgement closes all of that root's
old-epoch commitments across all paths; a cancellation tombstone closes every
copy of the exact nonce/path command. This operational coherence is represented
by the single `RootState` per root used at each gate occurrence.

Sharing a failure cause or sharing a label does not establish this behavior.
Cardinality supplies an intact overlapping root; the declared root-wide
close-before-acknowledge and persistent live veto supply the actual physical
block. If a purported root has independently openable stale gate copies that do
not share this contract, it is faulty or the proposed root map is inapplicable.

### Non-bypassable atomic physical mediation

The only plant-changing constructor is `Step.land`, which requires the actual
same-command live conjunction. This is the accepted mechanism boundary, not an
extra trusted certificate combiner. Bad roots cannot override another root's
veto, swap the command after checking, or introduce an autonomous downstream
write. `dropped_mediation` and `dropped_same_command_binding` show the failures
when those interfaces are changed. Nothing here certifies an external physical
implementation.

### External reservation, authority and target adequacy

`source e` is an independently warranted descriptor. `Reservation` is a
**separate premise**, restricted to actual valid `q`-root paths, linking actual external permission to the certified-effective
current descriptor. `admitted_externally_authorized` consumes it explicitly. The
proof does not infer actual consent from a certificate or define away immediate
external revocation. Whole-table equality is the formal goal; its adequacy as a
real-world goal remains an external source warrant.

### Honest actor and independently bounded service

Correct actor policy, fresh nonces, phase scheduling, direct all-good path
addressability, and independently bounded authenticated per-root control ports
are unchanged accepted premises for **progress**, and remain distinct from
safety mediation. The safety trace permits arbitrary command scheduling,
including malicious dispatch attempts, and proves only that admitted writes are
safe. Holds may continue indefinitely. No theorem in this package forces an
actor to run the portfolio, supplies a service bound, completes a blocked
macro-attempt on time, counts `3N` phases, or proves eventual delivery/repair.
Those are not silently supplied by finite-trace induction.

### Horizon

Each theorem concerns an arbitrary finite trace and a single continuing
lifetime-union budget over that whole trace. A finite declared horizon is not
extended by the proof. An infinite-prefix interpretation would require one
continuing valid bound and all mechanism/institution premises for every finite
prefix; this package does not formalize complete infinite liveness.

## Negative controls

All are concrete kernel-reduced witnesses in `NegativeControls.lean`, starting
from the same accepted `n=4, B=1, q=r=3`, actual path `{0,1,2}`, faulty set `{0}`.
Actual preparation, revocation and cancellation prefixes have formal `Trace`
proofs. The seven separately compiled false-claim mutations must be rejected.

1. Remove only epoch-revocation checking while leaving local descriptor,
   requester, commitment and cancellation checks intact: a permission-only
   transition leaves stale local descriptors, the broken path admits the old
   command, and the actual landing classifier enters X.
2. Match the source simulator's target-only authorization deletion after
   certificate delivery: unchanged bytes/version do not preserve permission.
   This deliberately removes the live authorization envelope, not solely one
   redundant equality test. Correct durable revocation alone would still block
   this trace if retained.
3. Remove only cancellation checking: after a valid `B+1` selected certificate,
   a late command is admitted despite its honest root's tombstone.
4. Weaken cancellation to `c=B`: the one faulty acknowledger closes nothing and
   the full original good-gate contract still permits a late landing.
5. Add a bypass controlled by the same already-budgeted faulty root: damage
   occurs while the proper live path remains blocked.
6. Check the approved command but land substituted bytes: proper gates reject
   the actual substituted tuple, while the broken effect reaches X.
7. Assert the old command remains authorized after revocation: rejected against
   the unchanged current-descriptor classifier.

The negative controls demonstrate essential mechanisms at the declared
interface; they do not claim that every syntactic check is individually
necessary under every alternative redundant implementation.
