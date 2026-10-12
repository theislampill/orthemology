# Independent scientific review: actual batch v1

Verdict: **PASS within the stated source-model scope.** No core source correction
is required. This review does not close the pending two-batch native-controller
increment, exact-four-envelope freshness refinement, public replay packaging,
alias-runtime composition, physical progress, or the larger research tranche.

Candidate manifest: `actual-batch-v1/MANIFEST.json`, SHA256
`83e6449ce32bb6ecd3688c33592c0357f014aa075eabffa9290f7fbca000af45`.
All 68 bound files match their identities and the complete inventory. Every
file covered by the accepted v6 manifest remains byte-identical, including the
literal original `Composition.lean`. The copied predecessor manifest is exact.
The predecessor manifest SHA256 is
`58798e94a43d42595c58f61de8c0ec42be89275530d00b52e4f31024b4e7f611`.

## Independent evidence

The reviewer first derived the source specification and adversarial controls
without inspecting the new author proof. The initial direct-source controls
were compiled before receiving this immutable candidate. Source inspection of
the nine new modules then compared their exact declarations and proofs with
that independently derived specification.

The final candidate replay freshly compiled the complete 50-module custom
closure: nine exact accepted imports, 32 inherited common-model modules, and
nine additive batch modules. No author or previous reviewer scientific object
directory entered `LEAN_PATH`; the custom output tree started empty. The same
run compiled five independent reviewer modules and one generated axiom-audit
module. All 56 compiler invocations returned zero with no warnings or errors.
Their combined compiler time was 294.170 seconds.

The nine additions contain 76 theorem declarations, producing 388 cumulative
author theorem declarations. All 388 author closures and 27 independent reviewer
closures were checked. Every closure uses only a subset of `propext`,
`Classical.choice`, and `Quot.sound`. The comment/string-aware token check found
no `sorry`, `axiom`, `native_decide`, or `unsafe` in the counted author or reviewer
modules. The reviewer theorems are separate evidence and receive no author
theorem credit.

Official Lean 4.19.0, commit `6caaee842e94`, was used with `-j1 -s65536`.
Executable SHA256:
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The full 5,065-entry official Lean distribution, 6,816 Mathlib source records,
and 34,230 dependency-cache entries were reverified. Exactly five official
cache-fetcher `.trace` files have compiler-path-only relocation differences.
Actual trace bytes were preserved, and comparison-only normalization reproduces
their original hashes. All scientific `.olean`/`.ilean` cache entries match the
pins. These are verified restored official dependencies, not an independent
Mathlib rebuild. No old packet was modified to satisfy a pin.

Cold replay receipt: `actual-batch-v1-cold/RECEIPT.json`, SHA256
`af48183cfef6ae23fc826524ad4bf6d63622f1ac4a9aec78665dace0bd4d0ee9`.
The candidate was reverified after compilation. The receipt binds source,
commands, compiler, output objects, diagnostic logs and the complete axiom
inventory. `replay_actual_batch.py` is a local scientific provenance harness,
not an accepted standalone distribution wrapper.

## Literal aggregate correspondence

`runBatch_eq_fold` is definitional equality to the unchanged imported fold.
Its named body is not a substitute controller. It retains the actor's stored
plant, policy and observed time, uses actor.nonce plus the current record count,
and always visits all four original paths. The record length, ordered path
sequence, and nonce sequence are proved directly from this body.

For a successful proposal, the extracted trace calls actual preparation with
bad-sign true, calls actual attempt with bad-open false exactly when preparation
returns true, and then always calls actual cancellation on the complete ordered
path. A false prepare keeps `prepared.1`, including partial commitments. Both
success and failure are cleaned up. A rejected proposal produces an empty
runtime trace even though its log has `closed=true`.

`runBatch_runtime_trace` constructs the genuine finite old-runtime event list;
the desired trace is not a premise. `runBatch_refines_history` composes that
extraction with the accepted cancellation simulation from an aligned reachable
four-root state. The result retains the complete existing `Aligned` relation:
full plant and effective policy, bounded root-policy and full-envelope memory
representation, thresholds, taint correspondence and completed-certificate
provenance. Existing memory representation is membership-based; no new claim
about abstract preservation of raw list multiplicity or insertion order is made.

The actor is arbitrary in the refinement theorem. A bad identity, stale actor
view, failed proposal, or unsuccessful batch is not excluded by a hidden
progress hypothesis. Existing current-full-policy admission and genuine
full-envelope cancellation transport through the aggregate output. The latter
requires an actual true `cancelWith` return, never a synthetic log bit.
The reference-clock-prefix theorem preserves the accepted clock scope without
inserting a clock update inside the service.

## Source-specific uniqueness

The unconditional at-most-one result is correct for this literal controller.
Because every faulty execution gate is passed `badOpen=false`, a successful
nonempty path supplies an intact live gate even without a global fault-budget
premise. Its actual local step changes the relevant version/history state, and
the imported fixed-action theorem excludes the same action under every policy
and time from that resulting plant. An induction transports this fact through
the remaining actual trials. Zero landings preserve the full plant, not
necessarily the full World; commitments and tombstones can still grow.

This is not a budget-free Byzantine architecture theorem. The reviewer proves
that with all four roots tainted and permissive faulty execution, the actual
lower-level service can report repeated landings of the same fixed envelope,
even after a true cancellation reply, while literal `runBatch` withholds all
four times. The fault bound remains essential to the broader architecture's
safety arguments when faulty gates may open.

## Conditional stable completion

The completion theorem has two separate exact source-admission obligations:
the actor's stored observation admits a predicted successor, and the actual
initial plant/full effective policy/World.now admit that same full successor.
`ReadyFor` additionally requires the requester to own the action, every bounded
intact root to hold the full current effective policy, and that action's epoch
not to be revoked. These are explicit model premises, not inferred knowledge
or authority for the actor.

With n=4, q=3, and actual taint cardinality at most one, the proof derives an
intact member of the unchanged four-path portfolio. It does not give the actor
the witness, a fault map, or a gate-outcome oracle. Rejected preceding trials
retain readiness, and the intact eligible trial prepares and lands. Combining
existence with source-specific uniqueness gives exactly one recorded actual
landing and equality of the entire final plant to the predicted successor.

`FreshAbove w actor.nonce` is a conservative sufficient high-water premise over
all prior cancelled full envelopes at bounded intact roots. It is stronger than
absence of the four actual future envelopes. The proof correctly increments
that high-water mark after each cancellation; the original actor itself is not
returned with an updated nonce. Finite memories imply existence of a mathematical
maximum but do not supply an actor observation or allocation algorithm.

The semantics-only progress theorem deliberately has no constraint on the
numerical `World.budget`. That value controls cancellation replies, not whether
an intact path lands. The reviewer applies the new theorem at budget 3 and
proves exactly one landing while all four cleanup replies are false. Completion
therefore must not be described as successful cancellation of every trial.
The separate history theorem retains its full original Authority/alignment
fault and quorum conditions.

Stable completion concerns one total finite source-function evaluation. The
service model excludes interleaved changes inside that fold, and keeps World.now
constant. It gives no physical service-latency bound, clock authenticity,
external service-availability proof, arbitrary interruption tolerance, unbounded
controller convergence, or mobile-fault theorem.

## Non-vacuity and adversarial premise tests

The 27 reviewer theorems cover the independently specified log and partial-effect
cases, all sixteen four-root taint patterns, necessity of the full four-path
portfolio for one-fault coverage, no early stop, and repeated actor nonce reuse.
The stronger new controls establish:

1. A true cancellation of the exact fourth envelope reaches a genuinely aligned,
   reachable native state where current local admission still holds but all
   four aggregate trials fail. Fresh-envelope availability is not supplied by
   structural alignment or reachability.
2. A genuine accepted runtime prefix stops after certification and before
   delivery. The current repair is locally admissible under the effective
   policy and all intact-root tombstone lists are empty, but root policies are
   still old and the actual aggregate repair stalls. Delivery/current-root
   readiness is an independent obligation.
3. A nonce-100 unrelated tombstone violates the exact new `FreshAbove` predicate
   for actor nonce 0 while the actual aggregate still succeeds. The high-water
   premise is not necessary.
4. An arbitrary failed actor proposal leaves the entire World unchanged despite
   four synthetic closed records. No-cancellation and failed-cancellation cases
   remain distinct.
5. The new stable-completion theorem applies to the unchanged full native
   installation fixture and proves exactly one aggregate landing with the full
   final plant equal to the accepted `installed` record. This is a four-path
   batch, not the earlier selected-intact-path witness.

The native source remains exactly 3,013 bytes, SHA256
`e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359`;
its embedded byte list was checked against that file. Small `[65]` payload
controls are separately labelled and do not substitute for the native binding.

## Preserved boundaries and next increment

The v1 result is a genuine new actual-batch bridge and explicit conditional
progress theorem. It does not authenticate external policy issuance, grants,
source interpretation, observations, physical root mediation or clocks.
`receiveActor` shape checking is not certificate authentication. Full actual
raw2-to3 installation-plus-repair batching, successful cleanup classification,
and the sharper exact-four-envelope freshness theorem are declared pending
additive work and are not accepted by this receipt. Alias-runtime lifecycle
transport and the N2/T0/R5 burdens remain unchanged.
