# Hidden target standards can require infinite memory under ongoing observations

## 1. A finite plant with an infinite-memory almost-sure winner

A standard h∈{0,1} is fixed initially and is not directly observed. At every step the plant emits a fresh bit Y_t. Conditional on h, the acquisitions are independent and identically distributed, with

`P(Y_t=1 | h=0)=1/3`, `P(Y_t=1 | h=1)=2/3`.

The controller sees each bit and chooses response a_t∈{0,1}. Both responses are stipulated safe and licensed under both standards. The plant's current observation and most recent response form a finite fully observed physical state. The hidden standard fixes the target:

`Target_h ⇔ a_t=h`.

Restoration means that responses are eventually always correct for that fixed standard. This is a synthetic identification/control contract. The statistical association between h and its response law, and the normative association between h and its target, are supplied separately; the example proves no actual norm from measured frequency.

### Theorem HS1 exact strategy-class separation

For this finite model:

1. No policy is sure winning under both standards
2. A deterministic policy with unbounded memory is almost-sure winning under both
3. No finite-memory time-homogeneous controller, deterministic or randomized, is almost-sure winning under both
4. For every ε>0 there is a finite-memory controller whose restoration probability is at least 1−ε under both standards
5. No finite-time stopping declaration can identify h with zero error under both standards while terminating almost surely

An unbounded external clock, changing transition table, or increasing-precision register counts as additional memory; it is not hidden inside “finite memory.”

### Proof of 1 sure impossibility

Every infinite observation word, including `0^ω`, is an allowed support word in both environments. Along that same word a deterministic controller emits the same responses. They cannot be eventually always zero and eventually always one. Hence the policy loses on a support path in at least one environment. Randomization does not help sure winning: fixing a supported random-choice sequence gives the same contradiction.

### Proof of 2 a constructive almost-sure policy

After every 2m acquisitions, choose the majority bit, breaking ties toward zero, and hold that choice until the next update. Under h=0, let K be the number of ones in those 2m acquisitions. Markov's inequality applied to `2^K` gives

`P(K≥m) ≤ E[2^K]/2^m = (4/3)^{2m}/2^m = (8/9)^m`.

By symmetry, this also bounds the error under h=1, including its adverse tie. The sum over m is finite. The first Borel–Cantelli lemma, which requires no independence between these overlapping error events, implies only finitely many wrong majority updates almost surely. Each update is held for only two plant steps, so there are only finitely many wrong responses. The controller retains an unbounded acquisition count and tally.

The expected number of wrong update blocks is at most `Σ_{m≥1}(8/9)^m=8`; this is a coarse bound under the declared iid model, not a latency or physical resource certificate. A finite number of initial steps does not affect the co-Büchi objective.

### Proof of 3 finite-memory impossibility

Fix a finite-memory time-homogeneous controller, including any random action and memory-update choices. Compile its memory, observed plant state and actual selected response into a finite Markov chain for each h. All observation probabilities are positive in both environments, and the controller is the same observation-based mechanism. Therefore the two chains have identical support graphs, identical reachable states, and identical reachable bottom strongly connected components.

Almost-sure co-Büchi success in a finite Markov chain requires every reachable bottom component to be target-contained. Under h=0 every state in each such component must output zero. Under h=1 every state in those same nonempty components must output one. That is impossible. Randomized choices do not evade the argument: their positive supports are part of the common product graph.

This proof is structural and covers every finite memory size. Enumerating small controllers below only verifies examples of it.

### Proof of 4 finite-memory limit-sure approximation

Choose m large enough that `(8/9)^m≤ε`. Sample 2m bits, retain their count, then commit forever to the majority standard. The probability of an incorrect commitment is at most ε in either environment. The finite sample counter and tally need at most `(2m+1)(2m+2)/2+2` states in a simple implementation; this is an upper bound, not a memory-optimal construction.

Thus each positive accuracy threshold is attainable with some finite memory, while no single finite-memory controller attains probability one. This is a strategy-class quantifier distinction; the unbounded-memory policy in item 2 does attain probability one in the unrestricted class.

### Proof of 5 no finite zero-error declaration

Every finite observation word has positive probability under both standards. The finite-history laws are mutually absolutely continuous. If a stopping rule declares a standard on some finite history with positive probability, that same declaration event has positive probability under the other standard, where it is wrong. A randomized rule has the same problem because its randomization law is shared across the models. A countable union over finite stopping times cannot yield almost-sure terminating zero-error declarations under both.

This does not contradict asymptotic stabilization. The successful infinite-memory policy keeps revising; it never acquires a finite publicly justified statement that no future revision could be needed.

## 2. The authority deletion changes the answer

Now change eligibility while retaining the same observation laws. Response h is eligible only when h is the actual standard; add a safe, universally licensed `abstain` response that is never target. At every finite public history both standards remain in exact support. Under the robust menu

`Γ(c,B)={a:J(c,B,a) and ∀x∈B E(c,x,a)}`,

neither guess is eligible. Only abstention remains, and restoration is impossible in that licensed action system.

An empirical error bound, even one tending to zero, does not set a still-positive alternative's probability to zero or create authority to act against it. A risk-tolerant permission contract could permit a different policy, but that would be a new substantive authorization assumption. The successful policy of HS1 deliberately stipulated both candidate responses to be safe and licensed; deleting that premise must change the conclusion.

## 3. The root-copy deletion also changes the answer

Replace fresh acquisitions by one bit Z drawn initially with the appropriate bias, copied at every step: `Y_t=Z`. The one-time marginal distribution of every report is unchanged. Yet the entire observation is now only `0^ω` or `1^ω`, and each has positive probability under both standards.

No policy can be almost-surely eventually correct under both standards: conditioning on either common positive-probability observation word leaves the same controller behavior required to be eventually zero in one model and eventually one in the other. The iid tally argument no longer applies.

The required independence is over genuine acquisition events conditional on h. Repeated reports, aliases, or copied records of one event do not produce those acquisitions. Conversely, independent acquisitions may come from one physical device if that stochastic and provenance model is separately warranted; device count is not the theorem's variable.

## 4. Transition support is insufficient for unrestricted learning

The two biased iid environments have identical one-step support. If their biases are made equal, their complete observation laws become equal and no policy can be almost-surely eventually correct for both opposing targets. Thus unrestricted almost-sure solvability changes while the transition supports remain the same.

There is no contradiction with finite-controller bottom-component verification: for a **fixed finite controller**, qualitative success is controlled by its finite support graph and labels. An unbounded controller can extract frequency information that does not appear in a finite support quotient.

## 5. The common-objective MEMDP theorem has an exact boundary

Chatterjee, Doyen, Raskin and Sankur's [ICALP 2025 paper](https://doi.org/10.4230/LIPIcs.ICALP.2025.150) treats multiple-environment MDPs with a finite, unknown but fixed environment, a fully observed common state space, and one common parity objective. Theorem 4 gives decidable almost-sure parity analysis and finite-memory pure winners. The paper separately distinguishes revealing zero-error transitions from frequency-based small-error environment guesses.

HS1 is not a counterexample: its target predicate depends on the hidden environment. The action-zero and action-one target sets are disjoint, and no single observed-state parity labeling represents both without exposing or retaining the hidden standard in the acceptance semantics.

### A legitimate licensed specialization

When the plant state s is fully observed, the environment h is fixed, public custody c is finite, and the desired parity/target predicate is common across environments, compile the exact live environment set H_t into the observed state:

`q_t=(s_t,c_t,H_t)`.

After observing a transition, remove only environments under which that transition has zero probability. The public menu `Γ(q_t)` incorporates all current pointwise and warrant constraints. It is then a common state-dependent action set. Dead ends can be represented as losing analysis sinks, without pretending a physical action was authorized. This finite compilation is an MEMDP to which the common-objective theorem applies.

The compilation may enlarge the explicit state space, so the cited theorem's complexity bounds must be measured on the compiled representation. No tight complexity claim for an arbitrary succinct warrant language is inferred.

An objective requiring simultaneous satisfaction of all candidate targets, as in Deep CQ, can be a common observed-state predicate. An objective requiring eventual satisfaction only of the actual hidden standard is different and may fall into HS1's harder regime. Noisy observations that hide ongoing physical state, genuinely switching environments, unbounded custody/time, or a changed objective likewise invalidate this direct specialization.

## 6. A precise CV-R nonconflation control

For either Bernoulli bias strictly between zero and one, each finite-prefix observation has a finite atomic law. Its CV-R positive-singleton defect is zero. The complete infinite bit trace has no positive-probability singleton: a particular length-n prefix has probability at most `(2/3)^n`, tending to zero. The infinite trace's defect is one.

Nevertheless the **specific** hidden-standard target is almost-surely determined by empirical limiting frequency under the stipulated two-model family. Under any full-support mixture of the two model laws, a measurable limit-frequency decoder equals h almost surely. It is not a pointwise decoder on every admitted support trace and does not produce a finite zero-error stopping certificate.

Thus CV-R defect one is not “no useful information” or “every decision target fails.” It concerns the full event-repertoire quantifier, whereas this identification claim concerns one separately declared target. The source/world and authority guards remain independent of either mathematical result.

## 7. Exact executable checks

`probe_hidden_standard.py` checks:

- all 2, 64 and 5,832 pure Moore controllers with respectively 1, 2 and 3 local information states, action chosen from the local state, and deterministic update on each observed bit
- all 59,049 qualitative support tables for two-local-state randomized Moore controllers, including action-dependent randomized updates; positive uniform probabilities represent each support pattern
- zero controllers in either enumerated class win almost surely in both environments
- 60 exact binomial error bounds against `(8/9)^m`
- finite positive-error constructions for error bounds 1/10, 1/100, 1/1000 and 1/1,000,000, using respectively 40, 80, 118 and 236 samples under the deliberately conservative bound

A “local information state” includes what that controller stores from its observations. A convention that gives a controller the current observed state separately changes the small-M enumeration count, not the all-finite-memory impossibility proof. The probe is not a general POMDP solver, an empirical test of cognition, or authentication of the supplied acquisition model.

## 8. Mathematical ancestry and scope

The ingredients are classical statistical identification, elementary Chernoff bounds, Borel–Cantelli, finite-chain recurrence, and the known strategy-class boundaries for partial observation. The contribution here is the explicit connection among hidden target standards, persistent authority, acquisition-root dependence, and the scope of a recent common-objective MEMDP theorem. No new general learning theorem or metaphysical norm-fixing principle is claimed.
