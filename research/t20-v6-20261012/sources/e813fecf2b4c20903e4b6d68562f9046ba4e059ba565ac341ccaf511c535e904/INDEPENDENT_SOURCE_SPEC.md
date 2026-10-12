# Independent source specification for the actual batch

Status: source-first analysis, with 17 accompanying independent control theorems
subsequently replayed successfully. This is not candidate-extension acceptance.
The bound sources are in `PRE_AUTHOR_SOURCE_BINDING.json`. Only the new review
directory is owned by this reviewer. No original, accepted milestone, or author
source was changed. The author supplied intended theorem scope after this
reviewer had read the original batch; no new author proof has been inspected.

## Literal transition sequence

`Composition.lean:439-453` executes exactly the listed `fourPaths`, in the order
`[0,1,2]`, `[0,1,3]`, `[0,2,3]`, `[1,2,3]`. The fold has no early-stop branch.
The actor's policy, observed plant, identity and observed time remain the same
throughout; only a temporary actor nonce is replaced by the original nonce plus
the number of records already produced. Each branch appends exactly one record.
Consequently record nonces are actor.nonce+1 through actor.nonce+4, including
when proposal fails, and the four records have the four exact ordered paths.

Proposal calls `localStep` on the unchanged actor observation. It does not query
the current world or fault set. Its success/none branch is therefore the same
on every trial, and successful proposals all predict the same full plant.
Success in an earlier actual trial does not refresh the actor observation.

For a proposal `some e`, each trial performs:

1. `prepare current e actor.identity true`, including its partial root effects.
2. Exactly when preparation returned true, `attempt prepared.1 e identity false`.
   Otherwise the intermediate world is **prepared.1**, not the pre-trial world.
3. `cancelWith landed.1 e identity e.path`, regardless of preparation or landing.
4. Record the actual three return booleans and post-cancellation version/revision.

For proposal `none`, the world is unchanged and the record is
`prepared=false, landed=false, closed=true`. There is no prepare, attempt,
cancellation, certificate, or envelope in this branch. `closed=true` here is
synthetic logging, and cannot by itself certify a cancellation acknowledgement.

No source operation advances `World.now`. The same full effective policy,
thresholds, taint predicate, completed certificate list, and each root's policy
and revoked-epoch list persist across a batch. Plant changes only through a
successful attempt. Commitments and cancelled-envelope lists can grow, including
when a service returns false. Cancellation never rolls back a successful plant.

## Simulation target and non-goals

A sensible first theorem fixes `Authority base 4`, starts from `Aligned a w s`
and `Reachable a.config s`, and derives a common `Trace a.config s events next`
with `Aligned a (runBatch w actor action).1 next`, for arbitrary actor and action.
The executable fold must first be linked literally to the old
`RuntimeWithCancellationTrace`, rather than replaced by a convenient new
controller. Proposal-none is an empty trace; proposal-some emits preparation,
an optional actual attempt, and cancellation. No synthesized certificate or
gate-success assumption is needed.

The fixed paths are bounded when n=4; this is why `BoundedEnvelope 4` fits.
The simulation does not need a successful proposal, actor correctness, q=3, or
an uncancelled-envelope assumption. `Authority` and full alignment retain their
existing fault, quorum, serial source, certificate provenance, and idle-boundary
conditions. Those are refinement assumptions, not operations in the batch.

The theorem is a forward simulation of a specific deterministic fold. It does
not imply progress, a converse simulation, physical timing, hidden policy
refresh, root recovery, an actor fault-discovery oracle, or external authority.
The accepted runtime cancellation and reference-clock continuation theorems
apply after a genuinely true cancellation return, not merely a `closed` log bit.

## Progress: load-bearing sufficient premises

For this n=4, q=3 portfolio and fixed withholding behavior, at most one tainted
root ensures an all-intact path among the four. This is a proof-side cardinality
argument; no actor inspection of taint is permitted. A successful local proposal
alone does not ensure an actual trial can land.

A transparent sufficient progress theorem can require:

- `w.n=4`, `w.q=3`, and at most one tainted root within those four.
- An actual source-derived `localStep observed policy time action = some next`.
- Observed full plant equals the initial actual plant; actor identity equals
  the action's actor; observed time equals actual World.now.
- On intact roots, full local policy equals the admitting policy, the action's
  raw epoch is not revoked, and each of the four exact proposed full envelopes
  is absent from prior tombstones.

Requiring equal times/full policies is sufficient rather than logically
minimal: actual admission at every relevant root and actual time is the real
condition. State the convenient equalities honestly, without calling them
necessary. Requiring every intact root is likewise stronger than requiring one
intact portfolio path whose roots remain eligible until its turn. Root policy
equality alone omits revocation and full-envelope cancellation.

Under those premises, a preceding failed attempt leaves the full plant
unchanged. Preparation and cancellation preserve the plant, root policies,
revocations and time. Earlier cancellations concern different full envelopes
(increasing nonce and also distinct ordered path), and cannot cancel a later
trial. At the intact eligible trial, fresh preparation creates all commitments,
the live gates admit, and the full predicted successor becomes actual. Once
that successor is actual, fixed expected version/revision prevents any later
landing of the same action. No early stop or observation refresh is required.

If the theorem includes successful cancellation for every actual trial, it must
also have an adequate cancellation threshold, e.g. `w.budget=1` (or `budget<3`),
and the owner identity premise. A fault count of at most one and q=3 by themselves
do not constrain the numerical cancellation threshold.

`Aligned` and `Reachable` provide current-policy safety. They do not provide a
live grant, matching actor observation, delivered root policies, a locally
admissible action, an unrevoked current epoch, or global nonce freshness.

## Adversarial controls compiled independently

1. Proposal-none produces four closed=true records while leaving all root
   commitments and tombstones untouched.
2. Wrong requester still permits the actor to propose; false prepares record
   dishonest commitments, but no intact commitment or landing is obtained.
3. Actual world at lease end with actor observation inside the lease produces
   all false preparations, partial dishonest commitments, and true owner cleanup.
4. With zero faults the first trial lands and all three remaining trials still
   appear, with false preparations after the fixed action becomes stale.
5. With one bad root, the intact trial is respectively at position 4, 3, 2, or 1
   for bad root 0, 1, 2, or 3. No early stop is inserted.
6. Two withholding faulty roots meet every three-root path, so all attempts fail
   despite successful actor proposal and preparation. Budget=1 is then violated.
7. Pre-cancelling only the exact fourth envelope (nonce+4, path [1,2,3]) defeats
   the only intact path for bad root 0. Intrabatch nonce growth does not establish
   absence from prior tombstones.
8. Rerunning with the same actor starts the same nonce sequence. A log-only claim
   of globally fresh nonce generation is false.
9. Changing q to 2 rejects every fixed three-root path before mutation; closed
   returns are then false on proposal-some branches.
10. Increasing budget to 3 makes owner cancellation false even though an intact
    attempt can succeed; honest tombstones are still recorded.

## Review acceptance gates for the eventual immutable milestone

After the source-first derivation, the author proposed replacing exact
observation/time equalities by two explicit admission obligations: the stored
actor observation and the actual initial plant/effective-policy/time each give
the same full successor under `localStep`. This is a sound weaker sufficient
formulation if the remaining root-policy, requester, revocation and tombstone
conditions are retained. It permits stale-but-still-valid observations and
does not infer an authentic or refreshed observation. The planned progress
lemma is semantics-only; the separate simulation lemma supplies common history
under its full alignment and authority assumptions.

At-most-once landing can be separated from availability even more strongly.
Literal `badOpen=false` means any successful nonempty path has an intact live
gate, regardless of the global fault cardinality. Every successful proposal
predicts the same successor, and the fixed-action theorem blocks that action
from the landed successor under every later root policy and time. Thus fault
budget premises are needed to ensure an eligible intact portfolio path exists,
not to establish uniqueness in this specific withholding controller. This is
an independently derived target, not a claimed compiled theorem.

The author later selected `FreshAbove w actor.nonce`: every preexisting
cancelled full envelope at every bounded intact root has nonce at most the
actor's initial nonce. This is stronger than absence of the four exact future
envelopes and is appropriate only as an explicit sufficient premise. Finite
root memories imply a mathematical maximum, but do not give the actor access
to those memories or an algorithm for discovering that maximum. External
nonce initialization remains an obligation. A new independent source control
pre-cancels an unrelated nonce-100 envelope while using actor nonce 0, then
shows the actual batch still lands. This distinguishes sufficiency from
necessity without importing the author's new predicate.

- Match every inherited source digest, including literal `Composition.lean`.
- Verify the candidate manifest and exact source/import inventory before and
  after independent compilation; use a separate reviewer output directory.
- Read exact theorem declarations and proof dependencies; no added desired
  conclusion in an interface law, gate-success premise, oracle, or surrogate
  definition receives credit as actual-batch progress.
- Compile the new modules and independent challenges sequentially with the
  pinned Lean toolchain. Verify reused dependency objects and disclose reuse.
- Audit all new theorem closures, comments-aware forbidden proof tokens, and
  all diagnostics. No success claim while compiler evidence is unavailable.
- Preserve full-record plant/custody/audit-history effects, full policy identity,
  lifetime fault-union scope, exact cancellation-envelope identity, and the
  native byte/epoch binding. Progress remains conditional in the source model.
