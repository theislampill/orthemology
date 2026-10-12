# Controller-chain examination for T20 v6

## Status and reading scope

This is a fresh source examination, not a fresh Lean verification. The exact read events are in `READ_LOG.jsonl`; their SHA256-deduplicated, current-byte-normalized union is `SOURCE_COVERAGE.json`. `INVENTORY.json` preserves individual source IDs, member names, row families and local source locations. An API-mode read means definitions, context, comments and theorem contracts plus explicitly retained proof lines; it does **not** mean every theorem proof was read. Full-source reads are separately classified. No endpoint is credited as a reading of its import closure.

Original allocation: T5-SCC, T5-CONTINUATION, T6-COST/CONCENTRATION/ROTOR/HISTORY/MOMENTS, S6F-23 and S6F-25. Their source-ID union has 177 distinct hashes: 175 accessible bodies and two unavailable non-public custody JSON records. Every accessible body was individually examined in full, including every theorem proof body. The initial API/selected pass was followed by exact complementary-range readings; its former 128 selected Lean-source gaps are now closed. Ordinary mathematical arguments and reviews were also read in full. Navigation metadata and generated controls are not counted as mathematical discoveries. Across the expanded allocation there are 213 fully read hashes, one shared reader examined exactly at the assigned papers, two excluded navigation objects and two unavailable custody records. Full reading means source examination, not fresh kernel verification.

Added by agreement: T16-SIGNED-SERVICE and T16-DIRECT-CONTROLLER. All 21 new production Lean modules were read **in full**, as were the relevant ordinary exposition (FULL_READER_TEXT_v5, lines 1685–2170), executable-dependency audit, control/mutation sources and scope note. The seven signed-service source bodies were absent from that row's assigned source-ID union but were recovered by module name from the original content-addressed catalogue. Their exact hashes are now in this inventory; reading a public registry alone would have missed them. T4 support-changing Markov theorem, deterministic round-robin successor, computable allowance and both ordinary reviews were also read in full after transfer from the early-source worker.

Some first fetched source copies had precisely one extra terminal newline. The source custodian removed it only when that restoration yielded the expected SHA256. Each affected read is explicitly rebound as unchanged nonterminal lines plus one removed final newline. No unexplained content-hash mismatch is accepted. The two missing JSON records are not missing mathematical proof bodies; their historical cold/seal assertions remain inherited, not independently reauthenticated here.

## 1. What the original theorem actually solves

The experiment has finite observed states and actions, a finite initial family of static hidden models, known normalized rational **full** transition rows, hidden model-relative state/action priorities, and support/state-dependent hard menus. One policy and one independent private-seed law are selected before the actual model is quantified. It receives the complete action/receipt history. It does not receive the actual hidden model, hidden badness label, an unrestricted timing side channel or hidden evolving state.

The generic necessity theorem permits arbitrary measurable private-seed spaces and unbounded history. The constructed sufficient witness has Unit seed, but this is an existence-class result. It does not turn every supplied randomized policy into a law-identical deterministic policy. Lawfulness concerns all feasible compatible histories with nonempty live support; the probability formulation shows zero illegal-next-action mass at every positive finite history. A null prefix is not a normalized continuation probability law.

The semantic winning region is not defined by the new solver or compiler succeeding. Original necessity first proves safe all-branch continuation and actual recurrent support facts, then places semantic winners in the computed support/state fixed point. Sufficiency independently constructs a history policy and proves its actual-law parity. The SCC implementation is connected by an equality theorem, not a refinement premise given by its caller.

### Source mechanisms inspected

- Indices 0–14: causal finite-query locality; actual product stack/full-row observation measures; transcript fiber factorization; cylinder probabilities; reconstruction of whole finite history-path prefixes from the last accumulated history; equality with the actual canonical all-query law; stack/action transport.
- 15–34: recurrent-set combinatorics, actual supported/recurrent raw tapes, sequential nonreused tape consumption, full-row target pruning, end components, killed actual Markov histories, relative finite-prefix domination, self-verifying support and finite-chain reachability.
- 48–65: actual stage necessity, conditional residual policies, lawful restart, AS tail preservation, all-branch semantic safety and support/state fixed-point necessity.
- 66–93: actual SCC deletion/cluster construction and equality, deterministic source-departure cycling, generated controller and empirical tests, phase/mode stabilization and global iff.

These are research-bearing modules, not standard-library proof lines. Imports from Lean/Mathlib were treated as external standard-library dependencies; no new library reproof or cold build is asserted.

## 2. The actual-law bridge is stronger, and more specific, than a Markov slogan

`PolicyCylinderProbability` derives the probability of a full transcript as compatible-seed mass times the product of recorded transition probabilities. The factorization comes from the deterministic history-fiber split and actual independent product coordinates. Distinct observed samples use distinct pair/index cells; merely carrying equal-looking copies of observations would not establish independence.

`PolicyObservedLaw` proves equality of the whole infinite observed-path laws. One-coordinate marginals suffice here only because the coordinate is the **entire accumulated history** and earlier coordinates are reconstructed by dropping its newest entries. This is not the generally false claim that arbitrary one-time marginal equality determines a process.

The conditional continuation is first defined as the original actual law restricted to the full positive observed prefix, normalized and shifted. In newest-first notation the continued policy receives `tail ++ oldPrefix`. `ConditionalPrefix` cancels the old row-likelihood factor and derives the common residual seed distribution. Old prefix probabilities can differ between models. The seed posterior is common because policy compatibility, not model likelihood, determines the residual seed weighting after the full transcript is fixed.

For a retained continuation set, killing happens **after** deleting the old prefix and removes the first outside receipt at its acquisition. An old prefix outside that set is allowed. Equality of killed laws transfers exact recurrent-tail events on the never-leaving restriction, a subprobability law. It does not assert that survival has probability one or identify every latent unused tape tail as fresh iid. Later lawful/AS restart lemmas close their respective earlier gaps, without strengthening unrelated latent-law claims.

### New discriminating continuation control

Take one observed state, two actions, a fair private seed r, deterministic identical receipts and a policy that always chooses action r. After the positive one-step transcript with action 0 or action 1, the observed state and live support are identical. Their residual seed laws are respectively δ0 and δ1, and their next-action laws have total variation 1. Thus state plus live support cannot faithfully restart this given policy. This does not disprove existence of another winning finite-memory policy. It isolates the exact migration interface: preserve the continuation-relevant state and residual distribution, rather than reinitialize the prior.

This control is complementary to T16's four-state delay and noncomputable-coherence results. It is a statistical-law obstruction to a proposed quotient, not a new proof of the T16 computability obstruction.

## 3. SCC computation, existence witnesses and submitted-body compilation

The SCC sources define a genuine SCC-backed target and region recursion, not a public name that hides exhaustive powerset calls. Preservation of every valid subcomponent through repeated deletion and recomputation is essential: deleting pairs can expose new row-matching rivals. Stable components have the required internal closure and strong connectivity, and maximal valid components have disjoint state sets. The SCC/reference equality holds throughout support recursion. This removes the old contract paragraph's separation of SCC substitution from the global iff.

The SCC theorem does not automatically extract its existential classical controller. Its historical review explicitly qualifies the witness as a mathematical Unit-seed policy inherited from the reference construction. Outer support recursion has no new polynomial-time claim.

T16 supplies a genuinely different positive increment. `SubmittedFamily` reads literal submitted node and target-component lists; its first containing component is chosen in submitted order. `CertifiedStageFamily` contains five local graph/safety requirements only: availability, menu membership, all-positive-successor closure, target qualification/containment and target-or-exit reachability. It contains no success, fairness or convergence field. All five are derived from accepted syntax. `OrderedCycle` replaces arbitrary finite equivalences with increasing-order finite lists. `RationalTest` computes half the minimum positive rational coordinate gap (or 1 if all rows agree), then proves exact equality of its runtime rational test with the real-valued proof test on every finite history, including malformed/unreachable histories and zero counts.

All direct safety, run, dynamics, cycling, stabilization, parity and actual-law proof bodies were inspected. The new proof adapts the old policy-parametric mechanisms; it does not invoke an old controller theorem after silently changing the controller. `Direct.compile` accepts only an input-validity proof as erased dimension evidence. `compiled_parity` applies to that literal function under each original `markovHistoryLaw`. Different accepted bodies can yield different actions. There is still no cost, finite-memory, deadline, parser/backend or actuator theorem for this compiled successor.

## 4. Signed negative evidence has an explicit completeness mechanism

T16's negative side is not failure to find a witness in an arbitrary search list. Accepted syntax itself bounds paths by n−1, component links by n, obligations by nq and body length by 2^q−1. The latter bound includes unused valid nodes. The constructive domain retains every allowed list order; it overenumerates malformed bodies, and the inherited positive checker remains decisive.

`PositiveFormula` reconstructs every checker branch using a closed exact atomic language. No semantic-winning, aggregate checker, reachability or arbitrary Boolean oracle is stored as an atom. The formula-to-checker equality is unconditional, so invalid branches are not hidden by an acceptance premise. A conjunction refutation needs a false branch; a disjunction refutation must cover both branches. `IndexedCoverage` enforces the exact complete increasing index span and exact tail length against the independently reconstructed domain. Input identity includes interpretation/source/authority fields as data, plus support and start query.

`negativeCheck_excludes_certificate` uses full accepted-body domain coverage, local refutation soundness and reflection. Arbitrary measurable-seed policies are excluded by inherited Ninth necessity producing a positive certificate. This is a valid-model policy nonexistence theorem, not adversarial sure loss, finite-horizon failure or an invalid-input verdict. Empty support and invalid input stay separate. `solveCompiled_correct` binds the returned body and exact returned `Direct.compile` function, rather than substituting an existential policy.

Finite signed search can be astronomically large. The ordinary exposition identifies the only native fully enumerated domain as q=n=k=1, containing 49 bodies. That inherited finite execution is not universal complexity evidence. The 21 production source proofs have now been read; none was recompiled in this pass.

## 5. Counter persistence is a theorem-specific resource

Three distinct constructions must remain separate:

1. T4's support-changing Markov ordinary proof uses fresh statistical stages and randomized uniform navigation/operation. Its deterministic successor uses finite source-rotor vectors retained throughout a stage, resetting at actual new stages. Fresh counters and divided error allowances are part of that proof. Hidden mismatch milestones are analysis stopping times, never reset instructions.
2. The likelihood/reset-budget modules use local likelihood memory and a strict support/rank descent. Their killed subprobability affinity retains exit mass, including loss by missing mass. This is another specific restart argument.
3. T5/T6's literal generated phase controller reconstructs **global cumulative** source-departure and empirical pair/receipt counts from the entire acquired history. Support or phase changes do not reset those counts. This convention drives the later linear whole-run charging argument.

Therefore “all counter resets are invalid” is false. Resetting after every action or every anchor return can starve a required rotor action; stage resets can be legitimate under the T4 construction. Importing T6's linear whole-run bound into a reset variant is unsupported.

### New positive finite-memory subinterface

For a fixed menu F, the action scheduler needs only each source's departure count modulo |F|. If the menu can change, an old menu modulus may lose information: counts 0 and 2 agree modulo 2 but select different actions modulo 3. A universal scheduler quotient is available: let L=lcm(1,…,a), where a bounds every menu size. Store the departure count modulo L at each source. Since every k≤a divides L, the exact cycle position for every later menu is recoverable; increment only at the actual source departure.

This is an elementary exact transfer for the scheduler with fixed menu ordering. It does not compress empirical counts, the phase index, seed posterior or selected certificate. An interface-level test collision has counts 1 and 3 with zero successes, phase 1, candidate probability 1/2 and tolerance 1/4: the rotor parity agrees, but the strict empirical count gate is false then true. It is not claimed that these histories produce equal entire controller states.

## 6. Cost, concentration and stopping-time discipline

The target cost is the ENNReal total number of executed bad state/action pairs, including the first real action. For the coBüchi encoding bad=priority1, good=priority2, a matching qualifying component is entirely good. General parity is not finite odd-priority visitation: a component with recurrent priorities 0 and 1 can satisfy parity while incurring infinitely many odd charges.

The earlier ordinary stopped-cost proof uses a raw deterministic-count good event G_n and a last-error count K. K need not be a stopping time. Its quadratic interval budget yields all moments through shell Cauchy–Schwarz, with no independence of shell events and costs. It does not condition an iid estimate on a random acquired count, nor multiply a random event count by a dependent mean interval as if they were independent.

`GlobalCountBudget` strengthens the actual cumulative controller: time maps injectively to the consumed (pair, tape-index) cell. Across all phases together, low completed counts contribute at most q(L−1), not that bound separately in each phase. Combined with support/phase accounting, the ordinary concentration addendum gives

J_n* = (q+2m)n + q(m−1) + 2m(m+1).

Here q counts state/action pairs and m counts initially live models. With D=s a^s, r=p^D and λ=−log(1−r/2), chronological interval starts have a conditional geometric domination and conditional exponential moment at most 2 for exp(λ L/D). Iterated conditioning gives an at-most-2^J product bound without requiring interval independence. Large raw-prefix deviations have an exponential count cutoff bound. Consequently a two-parameter estimate of the form

P(C>t) ≤ A exp(−cn) + 2^(αn+β) exp(−λt/D)

yields an affine high-probability bound and a positive exponential moment by choosing n as a function of the confidence parameter. No condition c>α log 2 is necessary. Summing a fixed-MGF shell bound directly would spuriously require it and fail for small row separation.

This closes the **ordinary** positive-exponential-moment frontier for the same cumulative generated controller described in that addendum. The earlier prior-art memo's “still open” sentence and earlier quadratic proof's negative exponential-status statement are superseded in that precise ordinary scope. Later formal characterizations have separate source identity. The operational-successor worker now reports direct examination of D06 `ActualExponentialMoments` (hash prefix 20cd0fcf), deriving the actual generated coBüchi positive-exponential endpoint under finite support, positive tolerance, strict finite-row separation and initial winning-region membership. That is a separately examined successor, not an inference from this ordinary addendum or from the conditional `ActualCostTailMoments` endpoint.

### Formal subinterfaces and their still-visible premises

- `RawWordLaw` derives the finite Boolean word law using injective deterministic stack coordinates and actual product independence. `RawPrefixDeviation`, `RawExponentialTail` and the unrestricted-tolerance clamp give the actual all-count tail bound. The earlier BernoulliWord, CentredBernoulli and EmpiricalGeometry originals were fully read by the early-source worker, with exact hashes/ranges supplied separately; no foreign concentration oracle is assumed.
- `FrozenRotorKernel` is the pushforward of actual row draws through deterministic rotor updates and an absorbing kill state. Closed-class projection requires every prescribed action at a recurrent source, proven by returning to the same full residue vector. State alone need not be Markov, and the augmented chain need not be irreducible.
- `ActualGeneratedSliceTail` derives actual conditional continuing-slice probabilities after every positive **complete** acquired history. It starts from the full-history rotor snapshot, obtains compatibility and live support almost surely, proves actual action agreement, then uses monitored domination. An arbitrary disagreement monitor by itself would only bound an artificially shrunken event.
- `TailMoments` derives expectation, all finite moments and strict-subcritical exponential integrability from a supplied affine-tail envelope for an ENNReal cost. It separately proves a.s. finiteness before using `toReal`; `toReal(∞)=0` cannot hide an infinite-cost atom. `ActualCostTailMoments` still visibly takes the actual total-cost tail premise. The chronological charging/total stopped-tail integration is not supplied merely by that endpoint.

No bound on the physical time of the last bad action follows from a bad-count moment. A policy may wait arbitrarily long between its finitely many bad actions. Nor does existence of an integrable winning witness make every almost-sure winner integrable.

## 7. Sampling, timing and output projection

The rational sampler allocates a common denominator D and fixed bit width L, rejects codes outside D, and freezes logical history on a rejected proposal. Exact fair-bit cylinder calculations give both the adaptive accepted-history law and the waiting-count law. Because the rejection set is common, the actual finite history and waiting-count events factor into their marginals. This is stronger than observing equal clocks marginally, and depends on the actual common allocation/updates.

The literal P02 runtime binding derives receipt events from actual serialized output bits, with exact framing/decimation. Almost surely all finite receipt prefixes complete, although the all-one forever-rejecting tape exists. A measurable total decoder uses a fallback only on noncompletion; execution does not fabricate a receipt. Full canonical history-law equality is obtained via finite report probabilities, completion and whole-prefix reconstruction. The decoder is common and output-only, with no actual-model or raw-input-tape argument.

The final Boolean full-phase binding still assumes its exact supplied selector certificate, the fixed 1/3-versus-2/3 simulated-kernel match and false initial state. It is not an arbitrary rational-environment compiler. Computed tolerance replaces two rational fields while preserving selector bindings, but need not preserve the old policy's finite-history actions.

The source counterexamples show why a single general “projection preserves correctness” bridge is impossible:

- An acknowledgment-rich physical stream can be atomless while its accepted receipt stream is constant.
- More strongly, the two-state held-output machine has no extra acknowledgment or random payload. Random positive finite stuttering of a deterministic alternating logical stream preserves parity for **every** priority assignment almost surely, while nonatomic defect changes from 0 to 1.
- Measurable deterministic projection cannot increase nonatomic defect; countable fibers suffice for equality. Lossy receipt/stutter compression need not have countable fibers.
- A physical policy allowed to observe unmodeled timing or raw sampler bits can gain model information absent from the logical-history contract, invalidating a negative-policy transfer. A frozen history-only policy can still enjoy the proved positive simulation.

Thus exact logical receipt-law identity, parity preservation, physical bad-tick cost and nonatomic-defect preservation are separate obligations. None of the supplied source bindings proves practical fuel, CPU, latency or an acquisition-clock bound.

## 8. Connections to later inquiry, proof cost and tensor information

These are discriminating maps and open obligations, not claims of equivalence between programmes.

**Finite memory and committed continuation.** A representation suitable for one current output need not preserve future history laws. The posterior control above separates state/support from the actual residual policy. The rotor LCM quotient positively identifies one finite subinterface that can be preserved; empirical counts and residual information remain separate. T16's accepted-body compiler is a finite program operating on unbounded histories, not a finite-state strategy. Its branch closure is operationally important: every positive receipt's surviving child must be licensed, not just the favorable revealing successor named in a witness.

**Inquiry and disclosure.** Hard-menu lawfulness survives arbitrary rejection tests because all active pairs and every proper child branch are already licensed. This separates “permitted experiment” from “experiment eventually distinguishes models.” A wrong global candidate may permanently succeed if all relevant recurrent rows match and its submitted component certifies every matching rival's objective. Therefore success is not equivalent to identifying the actual model. An active inquiry transfer must preserve the emitted action, observed receipt, allowed-menu update and the actual distinction available to the agent; an authentication or source label alone supplies none of these.

**Proof cost and timed realization.** T16 finite AST completeness gives mathematical termination of a signed service and exact binding of the returned function. It does not bound computation or acquisition time. The earlier finite rotor proof bounds a stochastic logical event wait, and the ordinary cost proof controls bad action count. Later clock/window results need their own admission, freshness, stable observation and action-update contracts. The operational-successor worker reports exact full-history/failure-spine lower-bound interfaces and ServiceClock window bounds; these must be composed through their declared channels, not interpreted as automatic consequences of controller integrability. A finite source description or C generation likewise does not verify compiler backend or physical actuator semantics.

**Tensor information.** Hellinger and raw-concentration modules obtain tensor products only from independent latent coordinate use. Duplicate source objects or repeated report copies cannot be counted as independent evidence. For Bernoulli(1/4) versus Bernoulli(3/4), one observation has squared affinity 3/4; duplicating that observation leaves squared affinity 3/4, whereas two genuinely independent observations have squared affinity 9/16. The exact finite control records these values. In killed/subprobability comparisons, missing/exit mass must also remain; conditioning and renormalizing away it changes the discrimination problem. This supplies a concrete provenance requirement for later tensor-information work: identify distinct generated observations and their joint law, not just a tensor-shaped data container.

**Prior art and bounded novelty.** The supplied comparison correctly distinguishes latent model-relative badness from common observable objectives. Finite-state common-objective synthesis plus elementary finite-chain absorption already implies an exponential bad-count moment in its subclass. The two-Bernoulli-model same-support graph obstruction rules out an autonomous time-invariant finite-state common learner for latent opposite good actions; arbitrary external time invalidates the unqualified memory claim. These are classical mechanisms. This pass examines the supplied source comparison and does not constitute a new exhaustive external priority search.

The fixed-codebook frontier source and independent review are ancillary S6F-25 dependencies. Their arbitrary-real lower bound uses partition-Kneser plus a residue-transfer lemma; combinatorial copies retain original root multiplicity and are not new operational observations. The original note's fixed-private frontier pending label is superseded by the later scoped complete review; shared-random ratio qualifications and external topological dependency remain. The early-source worker retains primary ownership of that result, so it is not credited again as a new controller theorem.

## 9. Failure and supersession register

1. Conditional continuation initially lacked AS preservation/lawful support induction; the inspected successors close those named interfaces. They do not retroactively prove fresh iid latent unused tails.
2. SCC-to-global iff was separate in the retained predecessor contract; `SCCGlobalParityIff` and its composition review close that connection only. Its mathematical winning witness remains choice-based.
3. Quadratic stopped-cost/all-moment analysis was sharpened by the linear cumulative-count ordinary concentration argument. Do not preserve the old “no positive exponential result” boundary as current ordinary status.
4. Frozen rotor tail was initially a finite-kernel frontier. The history-frontier successor closes the actual conditional generated-slice bridge by deriving support, compatibility and action agreement. Total charging remains separately required.
5. Tail-to-moment conversion is fully stated for ENNReal cost with explicit tail premises and strict exponential parameter. It is not a hidden proof of the premise.
6. Runtime cylinder uniqueness was later strengthened to direct canonical history-law identity. Fixed kernel/initial state, selectors and decoder remain explicit.
7. T16 removes the literal returned-policy extraction gap with a submitted-body compiler and new actual-law proof. No old cost theorem was transported to it.
8. Review harness/probe failures are distinguished from author theorem failures: the SCC namespace/path issues and rotor reviewer coercion issue were corrected reviewer controls, not counterexamples to the frozen source. Existing reported mutation rejections are inherited, not freshly executed here.
9. T4 stage-reset construction and T6 cumulative construction are not semantic or quantitative aliases. Equality of winning regions does not identify policies or costs.

## 10. New checks, precise residuals and completion boundary

`interface_checks.py` was freshly executed with exact rational arithmetic. `INTERFACE_CHECKS.json` records the seed-posterior collision, menu-modulus collision and universal LCM scheduler quotient (31,209 finite checks through menu bound 8), empirical gate collision, copied-versus-product affinity and cumulative-cell/reset distinction. The elementary arguments above, not those finite counts, justify the universally stated quotient/countermodels. These checks are not additional Lean declarations or reruns of historical suite receipts.

Remaining obligations genuinely not closed by this examination:

- There are no unread proof-body lines in the 175 accessible original hashes or the 21 new T16 production modules. The sole partially read source is the shared 2,208-line T16 reader: assigned Papers 12–13 are fully examined at lines 1685–2170. Lines 1–1684 and 2171–2208 concern other assigned workers’ papers and the HasC appendix; they receive no reading credit here.
- The complete Lean/Mathlib standard-library and compiled-object graph was not reread or rebuilt. Historical source-bound receipts are reported at their original cold/compositional scopes only.
- Two nonpublic custody JSON records remain unavailable. No mathematical source body in the allocated original 177-hash union remains unread.
- The later D06 formal positive-exponential theorem is owned and directly examined by the operational-successor worker. This source pass does not replay its Lean build or transport its bound to the new T16 submitted-body compiler.
- A law-preserving finite-memory implementation of the whole cumulative learner is not obtained; autonomous finite-state impossibility depends on the latent-objective model and external-clock exclusion.
- Faithful compression/migration needs a proof for residual distributions, accumulated statistics, chosen body/menu ordering and every observation channel. The positive rotor quotient discharges only its scheduler part.
- Neither the T16 compiler nor the fixed Boolean runtime theorem verifies arbitrary physical environments, input-model adequacy, source truth, authority, parser/backend, deployments or deadlines.
- No global novelty claim, full external literature recheck, new human specialist endorsement, canonical adoption, T21 or repository change follows.

The assigned mathematical routes have been examined in full at their research-bearing source bodies, including all 21 new T16 production modules and the five original T4 ancestry texts. Further work should target a stated transfer obligation or an independently assigned original source, rather than inflate theorem counts by re-proving completed endpoints.
