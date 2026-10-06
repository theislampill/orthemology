# Independent review: protected shared-root controller progress

Verdict: ACCEPT the exact `progress-core-v1` milestone as a conditional,
single-action, finite mathematical reference-controller result. No remaining
semantic blocker was found within the scope below. This is not acceptance of
an asynchronous implementation, a native 21-path executable, or any later
sharpness/corruption extension.

## Exact reviewed boundary

- Milestone: `tranche8/research/shared-root-progress/milestones/progress-core-v1`
- Manifest SHA-256:
  `fffebbef80cac51557b7bcc7751b135999e5cd6f2dfe2eae816e447b624b403a`
- Input binding SHA-256:
  `296da61cf3564d2f8905668cb88400917d8176513455480c52eaa7650aa81ebf`
- Eight new source modules, 23 exact copied accepted dependencies, 84 new
  theorem axiom closures. The optional `ControllerWorstCase` extension is not
  in this review boundary.

The reviewer checked every frozen manifest entry and every bound source
before and after replay, and compared all 23 copied accepted dependencies
byte-for-byte to their stated accepted origins. All 31 modules were compiled
from source into an initially empty reviewer build with official Lean 4.19.0,
one job, and only restored pinned Mathlib/library caches on the import path.
No accepted custom `.olean` was imported by this cold core replay. All module
logs were warning-free. The exact 84-name axiom inventory and six additional
reviewer theorem closures contain only `propext`, `Classical.choice`, and
`Quot.sound`.

Receipt: `evidence/CORE_V1_REVIEW_RECEIPT.json`.
Driver: `review_progress_core.py`.
Cold build, module logs and frozen replay receipt: `core-v1-cold/`.
Independent controls: `ReviewerControllerControls.lean` and
`evidence/ReviewerControllerControls.log`.

The full compiler distribution and Mathlib source/cache identity are covered
by the separately verified restoration receipt. Mathlib was not rebuilt by
this review. The only cache-pin differences are five explicitly bounded
path-only Cache trace metadata relocations; `.olean`/`.ilean` bytes match the
pins. Both restoration receipts are hashed into the reviewer receipt.

## What the new theorem actually establishes

`seven_protected_window_progress` computes a run of 21 public source-proposed
commands and proves its exact successor. It also constructs a lawful trace
of the unchanged root-indexed `SharedAlias.Step`: seven synchronization slots
plus 21 trials of five preparation slots, one live attempt slot, five
cancellation slots and one legal close, for 259 reference transitions.

The final theorem does not take successful landing or a successful trace as
an assumption. Its intermediate `Clear` premise is discharged from authentic
current-policy synchronization, a new direct reachable-history revocation
invariant, initial idle status, and absence of the exact future envelopes from
good-root tombstones. The remaining work premise is the unchanged source
`localStep` admission for the initial plant throughout the authority window.
The source gate decides the actual landing. Before any success the plant is
unchanged; an all-good scheduled path therefore prepares and lands. Once the
successor is reached, continued enumeration preserves it.

The proof uses the same accepted actual-root state and fixed canonical map.
It derives the bad-label cardinality through the accepted map/fault transport.
The all-good path is a proof witness inside an already fixed portfolio; it is
never returned to the actor or used to choose the next request. The exact
source `attempt` retains its one arbitrary `badOpen` Boolean. On an all-good
path, the reviewer verified that its value is irrelevant rather than silently
set to the favorable value.

`uniform_unknown_world_installation` provides non-vacuity: one fixed public
actor and installation action, source-admitted over the non-singleton window
[2,22], work for every eligible fixed hidden environment with q=5 and the same
authentic initial policy, and every allowed bad synchronization/preparation/
attempt/cancellation response schedule. It ends at the full accepted installed
plant, not just at a weak goal predicate.

## Controller and identity audit

- `program` takes actor, action and public paths. It computes the full source
  successor from the actor's source `localStep`; neither E nor a response
  schedule is an argument.
- `compile_public_program` erases all environmental time/reply annotations to
  that same public program. The reviewer additionally proved equality between
  the erased programs for two arbitrary annotation schedules.
- `publicPrelude` uses the actor's supplied policy epoch and public labels.
  `actorSynchronize_eq` derives correspondence with the current source epoch.
  The prelude does not require the actor to read hidden `C.epoch`.
- Bad synchronization labels may withhold; the reviewer independently proved
  their completed silent slots are identity transitions. No cooperation by a
  bad root is assumed for delivery.
- Nonces and full command identities are fixed by public input and trial
  index. No hidden maximum-tombstone search chooses a nonce origin.
- Freshness concerns exactly the full envelopes in `publicCommands`, rather
  than a larger nonce/path cross-product. It is initial good-store veto
  freshness plus pairwise within-run command distinction, not an unproved
  claim of lifetime-global nonce uniqueness.
- Ordered path lists remain inside the complete envelope. Preparations and
  cancellation keys do not collapse full equality to unordered support or
  nonce equality.

The new handlers update the original shared root store. They do not replace
it with independent per-label memory. The accepted inequalities imply q>2k,
so every path receives more than k genuine good-label cancellation replies
even if every bad label withholds. The appended `close` step uses that exact
accepted guard. Sharing a tombstone never invents another label's receipt.

## Independent bridge controls beyond author proofs

Six additional controls compiled against the cold-built frozen sources:

1. Two arbitrary service/time annotation schedules produce exactly the same
   erased list of complete actor commands.
2. A silent bad synchronization label contributes a completed hold, not a
   forced descriptor update.
3. A cancellation at label i cannot create label j's receipt when j≠i and j
   was absent beforehand.
4. The same cancellation really creates a root-wide veto at alias j while
   leaving j's receipt absent. Shared mutation and honest receipt accounting
   are checked together.
5. At seven labels, actual B=1 and class cardinality 2 give lifted k=2; with
   q=5 the accepted inequalities force r=5. The public family has 21 paths of
   five labels each.
6. The accepted shared typed trace-counter theorem yields exactly one actual
   installation and zero repairs in the complete all-world fixture trace.
   This independently excludes hidden repeated effects from the run-all
   suffix, even though the actor never stops on a claimed success reply.

The separate `ContractControls.lean` was also compiled over the exact frozen
accepted AliasModel and has eight standard-axiom obstruction statements.
They establish arbitrary finite holds, constant infinite failure, arbitrary
finite delay before any admitted continuation, and pending current-epoch veto
propagation to an unacknowledged alias. Its receipt is
`evidence/CONTRACT_CONTROLS_RECEIPT.json`. Thus the negative baseline and the
new conditional positive result are both source-grounded.

## Essential limits on use

1. The result is about the output of the newly defined, protected, total
   service interpreter for every allowed response schedule. The trace is
   its legality witness. It is not a theorem about every accepted trace, nor
   every asynchronous execution of requests.
2. Every designated slot is assumed to finish with a legal reply, timeout or
   public phase-end indication. A false response bit means a completed
   withheld-response slot. Unobservable silence or an unfinished blocking
   wait is not thereby converted into a completed hold. This completion
   contract is built into the reference interpreter and disclosed in scope;
   physical availability is not derived from totality of a Lean function.
3. Weak eventual fairness cannot supply the 259 bound. The bound counts
   completed reference transitions and logical work, not elapsed waiting or
   wall-clock duration. Trial times are monotone sampled annotations after
   the actor's observation; all checks in one trial use its common sample.
   The model does not establish an authentic physical clock.
4. The protected horizon excludes extra owner operations, foreign cancellation,
   competing landing, corrupt events and unbounded extra holds. Bad response
   bits are arbitrary within the stated handlers, but this is not arbitrary
   adversarial interleaving robustness. Reachable initial history may still
   contain the accepted operations, including fixed-bad-root corruption.
5. The main theorem is single-action. The installation fixture has zero
   repairs, and it does not by itself establish two-stage install-and-repair
   completion. Such a composition needs its separately authorized source
   transition, delivery and fresh next proposal.
6. The unchanged native `Composition.fourPaths`/`runBatch` still uses four paths
   and label-local storage. Reusing its source proposal and live gate does not
   turn it into an executed native 21-path shared-store macro.
7. Neither map secrecy/noninterference nor an observation-compatible opacity
   theorem was proved here. No opaque search lower bound, randomized lower
   bound, optimality claim, or fixed-list sharpness extension is transported
   by this acceptance.

All of these limits are consistent with frozen `CORE_SCOPE.md`. Widening any
of them requires a separately reviewed extension; the present acceptance
applies only to the exact manifest above.
