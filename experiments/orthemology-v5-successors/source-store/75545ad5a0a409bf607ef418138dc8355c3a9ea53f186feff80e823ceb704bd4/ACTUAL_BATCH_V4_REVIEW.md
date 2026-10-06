# Independent scientific review: exact batch availability v4

Verdict: **PASS for the stated conditional, source-specific characterization.**
No scientific source correction is required. This is the final accepted science
increment in this batch branch; standalone source packaging and its acceptance
companion remain separate verification work. It is not whole-tranche closure.

Candidate manifest SHA256:
`186281d14d0ea41e7ac49aa7a392a6cf05cb92047670f7d639420720785ecf0e`.
All 99 bound files and the complete inventory match. Every earlier v1, v2 and
v3 bound byte is preserved. The explicit corrected retry note and its accepted
prose projection are retained without altering the frozen original science.

## Exact accepted statement

`AdmissionReady` supplies three source-record obligations:

1. The supplied requester string equals the action's actor string.
2. The actual starting plant, the policy stored in `World.effectivePolicy`, and
   actual numerical time admit the action to the predicted full successor.
3. Every bounded root whose taint flag is false has that same full policy and
   has not revoked the action's epoch.

The separate actor-observed `localStep` premise must also admit the same full
successor. The world has n=4 and q=3. There is no fault-cardinality hypothesis,
numerical cancellation-budget hypothesis, global nonce high-water hypothesis,
or requirement that all four future envelopes be fresh.

Under those exact conditions, `runBatch_survival_iff` proves that the unchanged
actual batch has exactly one landing iff at least one of its four predicted
complete envelopes has only untainted selected roots and no prior tombstone
for that same complete envelope at any selected root. The predicate concerns
the original World. It does not assume success at a future intermediate world.
`runBatch_survival_effect_iff` adds full final plant equality to the predicted
successor. `runBatch_zero_iff_no_surviving_trial` gives the exact zero-landing dual.

This is a necessary-and-sufficient condition for this finite source function
under the listed premises. The preceding v1/v3 high-water and all-four freshness
theorems remain correct stronger sufficient conditions.

## Source-field policy is not authenticated current authority

The iff is stated for arbitrary raw Worlds; it has no `Authority`, `Aligned`
or `Reachable` argument. Its readiness predicate explicitly assumes full root
policy equality with the field named `World.effectivePolicy`. That record-field
equality is supplied as a premise, not derived as a provenance theorem.

In particular, neither agreement among policy copies nor a successful local
grant check establishes that this field is the authentic currently effective
owner-issued policy. The iff does not establish certified issuance, correct
certificate provenance, legitimate requester authentication, or lifecycle
reachability. Merely calling a record field effectivePolicy does not prove those
external facts.

The separate accepted history/alignment theorem retains the full Authority
source-stream, fault/quorum, aligned-state and reachable-history assumptions.
Current-authority conclusions use that theorem. A combined conclusion requires
both sets of premises explicitly; this review does not import reachability or
authenticity silently into the semantics-only iff.

## Proof and interface inspection

The source-first criteria are recorded in `AVAILABILITY_IFF_PRE_REVIEW.md`,
written before the new author proof was inspected. The frozen code matches
those criteria.

Necessity extracts a real successful actual trial. Hard-coded badOpen=false
forces every selected gate to be intact, and each live gate checks absence of
the exact envelope in its cancellation memory. Preparation leaves cancelled
memory unchanged, attempts preserve roots, and cancellation only adds entries.
Those facts transport absence back to the original state. The actual record's
envelope is matched to its exact predicted action/successor/nonce/ordered path.
The necessary direction itself needs no readiness, n/q or fault-count premise
beyond the separately stated successful actor proposal and real positive result;
the reviewer type-checks that stronger boundary directly.

Sufficiency selects an available envelope only in the proof. If an earlier
actual trial lands, count monotonicity gives progress while the real source
continues its fold. Otherwise the actual plant is unchanged and admission/root
conditions persist. Earlier cleanup cannot cancel the chosen later envelope,
because the unchanged source generates distinct natural-number nonces. The
available intact path then genuinely prepares and lands. The accepted literal
controller uniqueness theorem supplies the exact count and fixed successor.

No actor field, proposal parameter, port selection, service call, or imported
runtime definition changes. `HasSurvivingTrial` is not an actor oracle. The
source still visits all four original paths and does not stop on a receipt.
There is no gate-success assumption hidden in the availability predicate.

The all-good-path necessity remains specific to the literal withholding flag.
It must not be generalized to a controller that opens faulty execution gates.
The previously compiled permissive-fault counter-control demonstrates that
boundary outside the architecture's fault-budget assumptions.

## Independent adversarial controls

Ten new reviewer theorems were compiled in addition to the accepted 37 controls.
Their material outcomes are:

- Starting with zero faults, four genuine singleton-ack cancellation calls
  each return false at B=1. They concern four different prospective envelopes,
  and each stores a tombstone at a selected intact root. The resulting World
  is proved aligned and reachable from an accepted initial state.
- This World still satisfies `AdmissionReady`, including actual local admission
  and matching full root policies. Nevertheless no trial satisfies the exact
  new availability predicate, and the new iff derives zero actual landings.
  Thus a false cancellation reply cannot be treated as clean selected memory.
- At numerical budget 7, the iff proves exactly one landing and the full expected
  plant while all four cleanup replies are false. Effect availability and the
  current-call cancellation threshold remain distinct.
- An actor whose stored time makes its proposal fail can face an actually ready
  world and an intact uncancelled path, yet land zero times. The separate actor
  proposal hypothesis is load-bearing.
- The exact iff's public type is instantiated without a taint-cardinality,
  high-water, or all-four-freshness argument. Its necessary direction is checked
  without a hidden current-admission or synchronization premise.

The author additionally supplies exact-native controls for cancellation of a
faulty first trial versus cancellation of the unique intact fourth trial,
delayed versus fresh retry availability, and availability without policy
delivery. The unselected-root tombstone example is correctly labelled a raw
World coordinate test, not a new service or a reached lifecycle state. The
reviewer's singleton-ack counter-control supplies the separate genuine-history
case; these two kinds of evidence are not conflated.

## Incremental replay evidence

The three additive author modules contain 31 theorem declarations. The final
cumulative census is 476 author theorems, of which 164 are batch-extension
theorems, plus 47 independent reviewer theorems. All those closures were audited
and use only subsets of `propext`, `Classical.choice`, and `Quot.sound`.
The comment/string-aware proof-token audit passes.

The replay freshly compiled three author modules, two reviewer modules and one
new cumulative axiom-audit module. All six invocations returned zero without
warnings or errors, with combined compiler time 57.753 seconds. It reused 58
exact previously accepted scientific objects and seven reviewer objects,
read-only, across the accepted cold-v1 and incremental-v3 builds. Their two old
axiom-audit objects were checked but not imported. No author-built object entered
the review path. The complete current custom science closure has 61 modules.

Official Lean 4.19.0, commit `6caaee842e94`, executable SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`,
was used with `-j1 -s65536`. Full compiler-distribution and pinned Mathlib
source/cache inventories were reverified, with only the same five explicitly
bound, preserved compiler-path trace metadata relocations. This is not a fresh
Mathlib rebuild or a fresh rebuild of the unchanged 58 science modules.

Replay receipt: `actual-batch-v4-incremental/RECEIPT.json`, SHA256
`fdbc289dd4a4d30098f3a37dd16fe9afa1c47fd5d9c0bd0b2bb384fdb1066687`.
It binds the prior cold-build lineage, new source/object/log identities,
dependency checks and complete theorem closure inventory. The candidate was
verified again after compilation. Earlier sealed scientific reviews remain
unchanged.

`REVIEW_SOURCE_ORDER_V4.json`, SHA256
`b3caf1d93d2d96566d46442f1fac185b8ac9772a8eb12bc3b0a6099e382a9c43`,
lists all nine reviewer modules in valid import order, exact namespaces,
source hashes and counts. It includes 47 reviewer theorems and 78 named explicit
reviewer declarations. The present scientific axiom audit covers the theorem
closures; the planned standalone companion's broader named-declaration audit
is separate and has not been credited in this receipt.

## Final science boundary

The finite stable source-specific batch gap is closed to the extent precisely
stated: exact actual history refinement, actual aggregate admission under the
separate authority/history assumptions, literal-controller uniqueness,
conditional completion, the exact availability iff, and the pinned concrete
two-batch/retry/projection controls.

Physical identity/authentication, authentic observations and clocks, actual
owner authority, source interpretation, atomic mediation, real service latency,
asynchronous or interfering execution, an actor-visible availability algorithm,
unbounded controller behavior and shared-alias lifecycle composition remain
outside these claims. N2/T0/R5 and the broader research-tranche conclusions are
not altered by this scoped acceptance.
