# Independent review: finite bad-store corruption erasure

Verdict: ACCEPT the exact additive `finite-corruption-v1` milestone for
arbitrary finite legal bad-root store rewrites inserted into the prescribed
reference service trace, with one fixed environment. Core and fixed-order
sharpness acceptances are unchanged.

## Exact accepted identities and verification

- Milestone: `tranche8/research/shared-root-progress/milestones/finite-corruption-v1`
- Manifest SHA-256:
  `b763dd865ee497ab6c8cbe52e63bd5eefb00e4b5d8baa062b0d7cd106040395b`
- `BadStoreErasure.lean` SHA-256:
  `d24e15ad5a890aca297fd3ef7b8ea6246c97241d9797714720d51bfd0eb44fdd`
- Required accepted core manifest SHA-256:
  `fffebbef80cac51557b7bcc7751b135999e5cd6f2dfe2eae816e447b624b403a`
- Reviewer receipt: `evidence/CORRUPTION_V1_REVIEW_RECEIPT.json`, SHA-256
  `2f399598e8524112a2df51725403f720224b0dc3f39d177c6a4bbdf3da7438ed`

The reviewer cold-compiled the one new module with verified official Lean
4.19.0 and one job against the review-owned, independently cold-built accepted
core. The unchanged core was not unnecessarily rebuilt again. All 33 exact
author theorem names and five additional reviewer controls compiled
warning-free with only `propext`, `Classical.choice`, and `Quot.sound`.
Frozen source hashes, accepted core files/receipt, and all review-owned core
object hashes were checked before and after. No accepted source or cache was
changed by this review.

Driver: `review_finite_corruption.py`.
Independent source: `ReviewerCorruptionControls.lean`.
Logs: `evidence/corruption-v1-source.log`, `corruption-v1-axioms.log`, and
`corruption-v1-controls.log`.

## Semantic audit

`SameGoodState` is a proof-side equivalence containing equality of every common
state coordinate: epoch, pending flag, owner receipts, certificate function,
full-command cancellation receipt function, and plant. At every good label it
requires equality of the entire actual root store, including descriptor,
commitments, revocations and full-command tombstones. It does not erase good
store mutations, common-coordinate changes, or new real receipts.

The environment and its actual-root map/fault set are fixed. A `Corruption E`
contains a label, arbitrary replacement `RootState`, and proof that its label
belongs to the fixed faulty set. Accepted root coherence ensures that no good
label addresses that actual root. The only inserted event is the unchanged
accepted `.corrupt` event, so corrupt contents may change freely without
inventing a new write capability or corrupting common control state.

`step_transport` preserves the identical complete event: label, complete
command, requester, policy-delivery epoch, and time annotation. It proves all
original guards again in the related state. Source `applied_congr` retains the
unchanged source `attempt` and its original arbitrary single `badOpen` Boolean;
it does not substitute favorable gates. `prepareAllowed_congr` proves actual
preparation decisions agree. Prepare/cancel/attempt/sync handler congruence
then preserves the same service choice and good state. Internal changes to a
bad delivery store may differ, but cannot affect the good-state quotient or
source result.

`Weave` admits any finite corruption block before each prescribed event and a
final block. Each block may have arbitrary finite length and arbitrary legal
bad-root replacement contents. It leaves all prescribed service events in
their original order. The generic erasure law removes corruption events from
both lists; it does not incorrectly promise that a generic reference list was
itself corruption-free.

The proof has both necessary strengths:

1. `finite_weave_transport` constructs a legal realized trace for every finite
   weave, with the reference good-state endpoint. This is not merely a
   conditional assertion about a possibly impossible realized trace.
2. Given a current state and one exact event, accepted `Step` has a unique
   endpoint; hence an exact event list has a unique endpoint. Combining this
   determinism with transport makes `finite_weave_erasure` universal over
   every actual realization of the same weave, rather than selecting a
   favorable successful execution.

Determinism here is conditional on the event or event list. Choosing and
scheduling the next event remains nondeterministic in the accepted relation;
no fairness or service guarantee follows from these determinism theorems.

The concrete wrapper `every_woven_installation_has_exact_effect` first obtains
the reference program and its lawful trace from the accepted uniform
installation result. The caller does not supply a successful reference trace,
a selected good path, or a desired final-state equality. Handler congruence and
transport preserve that source-derived service sequence under every finite
bad-store weave. The actor's requests, map, fault set, policy, action, source
clock annotations and reply schedule remain fixed.

## Independent adversarial boundary controls

Five reviewer theorems were compiled against the frozen extension:

- A genuinely changed good-root store cannot satisfy the erasure relation.
- A new label acknowledgement receipt cannot be erased, even though an
  acknowledgement may otherwise be a legal accepted event.
- One arbitrary legal bad-root rewrite preserves the exact source attempt
  Boolean for arbitrary `badOpen`, not only the favorable true case.
- Any positive number of insertions makes the raw event count strictly
  greater than 259. Effect erasure does not make adversarial events free.
- For every actual realized weave supplied by the source-derived uniform
  wrapper, accepted typed counters give exactly one installation and zero
  repairs, as well as the exact full installed plant and event count.

The last control is universally quantified over actual lists, insertion
counts and final states. Its conclusion is derived from the accepted typed
history counters, rather than trusting only the extension's endpoint wording.

## Scope and accounting that must be retained

The prescribed program still has 21 trials and 259 completed service
transitions. With `added` inserted corruptions, actual length is exactly
`259 + added`. There is no uniform 259 bound on raw events after insertion.
`arbitrary_corruption_delay` independently shows that, when a legal bad-root
rewrite exists, arbitrarily many such events can delay progress without
changing the plant.

Only finite store-rewrite insertions are covered. There is no result for an
infinite adversarial prefix or suffix that prevents completion, arbitrary
extra holds, mobile faults/maps, good-root writes, extra owner requests or
acknowledgements, foreign cancellation, or competing plant landings. Generic
transport may preserve an operation already in a reference trace; that is
not permission to insert those operations into this protected controller run.

The original completed-slot service/timeout contract, authentic authority,
full-command freshness and source-admission/time-window conditions remain
necessary. Insertions do not create a wall-clock or physical-clock guarantee.
The original trial time annotations are retained; no elapsed-time advance or
physical feasibility is inferred from a counted corruption event.

These are noncomputable/classical mathematical reference definitions. No
21-path extraction, code generation or native execution is proved. There is
no new observation model, map-opacity theorem, search lower bound, or
optimality transfer.

The concrete wrapper continues to use the three-byte ABC source fixture,
initial draft ABC+LF, source window [2,22], and one criterion installation with
zero repairs. It does not complete source-text repair and is distinct from
the separate 3013-byte label-local native batch witness.

The accepted `CORRUPTION_SCOPE.md` and `EXECUTION_CLARIFICATION.md` state these
limits. No correction to the frozen scientific milestone is required.
