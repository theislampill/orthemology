# Physical realisation and continuation

## 1. The problem: continuing a computation through a change of support

A computation can depend on a particular device without depending on that device's material composition as a matter of definition. Conversely, an abstract description of a computation does not establish that some other physical system can implement it. The question developed here is precise: **under what declared physical, informational and temporal conditions can an existing stateful computation continue after a specified support is removed?**

The answer requires several connected results. A sender must be able to produce a receiver-distinguishable effect. A receiving system must implement the required state transitions and outputs. The handover must convey enough of the particular current state, not merely a description of the task. The channel, computation, memory, clock, power supply and controller must coexist within one resource and failure model. Finally, continued safety must be accompanied by the progress demanded by the task. Each requirement can hold separately while their conjunction fails.

The development consolidates *The Last Moat, Third Edition: Physical Realisability, Cross-Substrate Communication, and Holarchic Agency* [LM]. Its positive results are conditional mathematical statements and, where expressly identified, reports of other researchers' physical demonstrations. Its own bistable construction is a model with a proof and reported finite computations, not a newly demonstrated apparatus. The distinction matters: a useful research programme can contain proved consequences without having established that an arbitrary present-day model, an autonomous agent, or a large trained network can be transferred into an arbitrary environment.

### 1.1 Four objects of continuity

An **organisation type** specifies a state space, transitions, observable outputs and relevant constraints. An **organisation instance** has a particular initial state and history. A **continuation relation** says which later state and trace preserve the chosen instance's contractual obligations. **Numerical personal identity** is a further philosophical claim. Equality of input-output organisation, successful copying, and a causal chain of state transfers do not by themselves settle that fourth question.

This separation prevents two mistakes. A device that can implement the same parity function as another device need not contain the parity accumulated by the first device's actual input history. Conversely, changing a state coordinate need not change the organisation at all. When two copies receive different inputs, their subsequent states can diverge while each remains a correct instance of the same type. Selecting one copy as the authoritative successor can be a legitimate institutional or protocol decision; it is not derived from behavioural equivalence alone.

A stored checkpoint is not an active process. To become active it requires an interpreter, admissible initialisation, energy, timing and a functioning interface. Dormant preservation and uninterrupted service are therefore different contracts. A task can explicitly allow a pause, a bounded outage or delayed delivery; it cannot obtain those allowances retrospectively from a successful final output.

### 1.2 A physical ecology and a declared boundary

Represent the surrounding system by a state x, admissible control u, disturbance w and observation y:

```math
x_{t+1}=F_\theta(x_t,u_t,w_t),
\qquad
y_t=H_\theta(x_t,v_t).
```

The parameter θ indexes a declared model family; v represents observation error. Continuous-time components can be included between interfaces. The boundary of the state must include every component on which the proposed execution actually depends: interconnects, stored code, control logic, clocks, actuators and readout devices as well as the named processor. Energy, power, time, storage, access, precision and maintenance are separate resources. A battery and a clock are not made independent merely by giving them different names in a diagram.

A physical influence graph records possible causal effects. A **usable communication edge** additionally requires admissible actuation, a readout, a code, a decoder, a timing convention and error bounds. Even usable edges need not be usable simultaneously. A joint rate region or a scheduled resource model is needed when edges share power, spectrum, hardware or deadlines. Summing independently measured capacities can describe a physically impossible joint configuration.

A failure domain is a set of components whose availability can fail together under the declared threat or environment model. Material, mechanism, architecture and failure domain are distinct axes. Moving a computation from a CPU to a GPU changes architecture without necessarily changing the power domain. An optical mechanism can be fabricated on silicon. A service running on another machine can remain dependent on the first machine's clock, state server or credentials.

The dependence question is always relative to a fixed task and declared exclusions. For every named support there might be a different admissible replacement, without there being a single arrangement independent of all supports:

```math
\forall h\ \exists r\,[r\text{ avoids }h]
\quad\not\Rightarrow\quad
\exists r\ \forall h\,[r\text{ avoids }h].
```

Nor does the existence of a replacement prove that a feasible, state-preserving campaign can reach it from the present configuration.

### 1.3 Holarchies, interfaces and authority

A holon is a whole for one task and a constituent of a larger whole for another. This is a useful relational description of nested organisation. Nesting alone establishes neither fractal self-similarity nor approximate dynamical independence. Claims of self-similarity require a specified rescaling and preserved structure; claims of near-decomposability require coupling, time-scale or contraction conditions. Bousquet and Slotine supply one explicitly conditioned contraction and singular-perturbation treatment, rather than a theorem that all hierarchies are modular [BS].

Terms such as a “kernel above an ecology” can be given a limited operational meaning: a fixed abstract contract is realised by different joint physical configurations. They need not assert a disembodied process or an additional planetary subject. “Orchestration” then concerns permitted observation, scheduling, adaptation and allocation among components. It does not follow from a graph's size, a large fan-out or a shared name that its components have one goal or form one conscious agent.

Physical possibility, evidential warrant and permission are also independent. A proof that a controller could keep running does not authorize it to do so. An operator's legitimate stop instruction is not an adversarial disturbance to be defeated. Human participation requires a specified, observable and consented interface; private cognition is not silently included as a readable machine state. These boundaries constrain the admissible controls and supports in the mathematics rather than appearing as exceptions after a theorem has been applied.

## 2. Fixing what a replacement must preserve

### 2.1 A contract before an experiment

Let a deterministic kernel be

```math
K=(Q,A,O,\Delta,\Lambda),
\qquad
\Delta:Q\times A\to Q,\quad
\Lambda:Q\to O.
```

Here Q is the logical state, A the accepted input alphabet and O the output space. A fuller contract Γ specifies admitted initial states Q₀, admitted input histories, state and output metrics, tolerances, a horizon, resource budgets, allowed failures and permissions. If responses have deadlines, their timing is part of Γ. Freezing these choices before testing prevents a failed state transfer from being reclassified as a successful transfer of a simpler task.

The state is task-relative. A fixed program's parameters may be constants in Δ rather than mutable members of Q. A contract for updating, preserving provenance of, or reproducing an exact parameter file can make those parameters part of the required state. A contract for one fixed input-output behaviour can be weaker. Neither convention is universally right; changing between them changes the claim being assessed.

For a fixed transformer, an exact behavioural contract may need to name the tokenizer, model version, arithmetic, context handling, output distribution, randomisation and mutable cache. Reproducing selected benchmark answers is a different contract. Relearning an equivalent function and directly copying parameters are different methods, either of which can be relevant once the required equivalence is fixed. The label “same model” does not supply the missing definition.

### 2.2 Realisation includes outputs, memory and the actual interface

A physical realisation r has an admissible interface-state domain Dᵣ, an execution map Φᵣ and a decoding map ρᵣ into Q. Exact transition preservation requires, for every admitted physical state, input and disturbance,

```math
\Phi_r(x,a,w)\in D_r,
\qquad
\rho_r(\Phi_r(x,a,w))
   =\Delta(\rho_r(x),a).
```

The physical output map λᵣ must also satisfy

```math
\lambda_r(x)=\Lambda(\rho_r(x)).
```

The second equation is not redundant. A machine can update its internal bit correctly while displaying the inverted bit. Transition correspondence would then hold and the observable contract would fail. If output noise is admitted, the output condition is imposed on the specified decoder and noise family, or replaced by the declared metric or distributional tolerance.

The state x is the complete operative state within the boundary. If an external controller stores the history and supplies the next answer, that controller is part of the implementation. A decoder fixed in advance can be useful; an unrestricted decoder that consults an uncharged answer oracle makes the realisation claim vacuous. Readout computation, stored tables, calibration and access have to be included in the resource account.

This formulation belongs with refinement and approximate simulation, not with an assertion that every interpretation is physically realisable. Abadi and Lamport study conditions for refinement mappings; Girard, Julius and Pappas study approximate simulation with metric observation guarantees; contract theory treats assumptions, guarantees and compatibility explicitly [AL], [GJP], [BC]. The elementary results below expose the particular conditions needed here. They do not claim to replace those broader theories.

### 2.3 Coordinate freedom and substantive memory

A bijection h between two physical state domains gives a simple positive equivalence construction. Define

```math
\Phi_s=h\circ\Phi_r\circ h^{-1},
\qquad
\rho_s=\rho_r\circ h^{-1},
\qquad
\lambda_s=\lambda_r\circ h^{-1}.
```

Substitution shows that the transition and output equations for s follow from those for r. This is a change of coordinates. It proves no bound on the cost of implementing h, and many valid realisations contain extra physical variables and are not related by a bijection of their whole state spaces. Coordinate conjugacy is sufficient in this special construction, not a necessary definition of all substitution.

A task is genuinely stateful when two admitted histories can leave different required states whose outputs differ under a common future input sequence. Such a pair supplies a memory test. Suppose a deterministic purported implementation has the same complete operative state after both histories. Under the same next input it has the same next physical state and output. Induction gives the same future trace for every common continuation. It therefore cannot meet both requirements.

This proves a memory necessity statement relative to the specified histories and future observations. It does not prove that memory must reside in the component bearing the “processor” label. An external state register, a persistent readout circuit or an environmental degree of freedom can carry it if it is admitted and counted. For stochastic implementations, the corresponding comparison concerns conditional laws, not whether two independent samples happen to agree.

A useful negative control holds the proposed memory-bearing variable fixed or removes it while retaining the readout protocol. If performance persists, the actual memory may be elsewhere. Failure of that control can locate a dependency without proving a unique smallest physical implementation.

### 2.4 Existing mathematical context

Three earlier results in this collection clarify the scope of these conditions. [Information and Inquiry](information-and-inquiry.md), sections 2 and 9.1, constructs predictive quotients and a coarsest finite information partition relative to specified observations, actions, costs and transition laws. Those are precise task-relative reductions; continuous coordinate dimension is not automatically a bit count. [Collective Inquiry and Strategic Coordination](collective-inquiry-and-strategic-coordination.md), sections 2.1–2.3, separates numerical encoding, order, interpretive meaning and implementability from local observations.

The same collective work's sections 7.5–7.6 establish a stronger stochastic controller-transfer result with matched full joint laws, initial couplings, information restrictions and interface composition. A deterministic physical commuting square here is a useful special situation, not a substitute for those stochastic and observational obligations. In particular, preservation of possible outcomes without preservation of their probabilities can destroy a progress guarantee. The new question is what physical controls, margins, supports and state exports make the interface equations true.

### 2.5 Certified representation changes do not repair a mismatched decoder

A change of coordinates can preserve an implementation exactly while preserving a defect in how its output is interpreted. The finite-selector development gives a precise example. Its A1–A3 results concern the delivered sparse fixture and the original selector certificate, not arbitrary semantic choices or an executable method for extracting selectors from an arbitrary environment. The certificate compares **raw digit numerals**, rather than merely the values of a decoder on a few examples. It covers all sixteen cycle cells, sixteen target cells and four stage cells. Target payload0 means absence; payload1 means a present empty set. Payloads17 through31 cannot satisfy that original contract. Finite code injectivity and complete cell coverage justify reconstructing the record from its digits. [Selector classification and scope][SEL8]

For that fixture, the unique bounded normal form uses moduli $`2^{16}`$, $`2^{80}`$ and $`2^{16}`$ for the cycle, target and stage records. A record is certified exactly when its normal form is the literal record for the retained initial orientation. All certified unbounded records are obtained from that literal by adding arbitrary multiples of those three moduli. This classification does not choose the orientation: for **supplied certified data**, it recovers the orientation from cycle bit12. Certifying one preselected literal would itself require the corresponding retained-choice equality. The two orientation cases and their many high-digit encodings are not independent semantic counterexamples.

The restriction to actual calls is essential. A malformed support code4 reads cycle bit16, so it can distinguish certified records agreeing on every legitimate cell. Normalisation therefore does not imply extensional equality of the selector functions on arbitrary natural arguments. `SelectorCallDomains` supplies the missing operational premise rather than assuming it: initialization from an encoded acquired history establishes the register invariant; every real history-fold step preserves it; the interpreter's fresh loop-index write is included; and every prefix of the exact eighteen-component parallel collection preserves the protected old argument vector. Exhausted sentinel padding performs no source step. At actual calls, support codes are below4, Boolean fields below2, optional target payloads at most16, and cycle/target addresses below16. The final readout is proved to use these derived source arguments. These are properties of the actual compiler boundary, not of an arbitrarily fabricated register store. [Derived call domains][SEL197]

With those premises, normalisation preserves the full certificate and the source action on every encoded acquired history. It also preserves every physical output coordinate on **every** input tape in the existing runtime wrapper, including tapes on which sampling never finishes. The reviewer controls explicitly include an all-one forever-rejection tape and equality of the output law under every input measure. Report extraction and the total receipt decoder remain equal even where a report does not complete. Equality of the physical outputs is stronger than equality only on a successful sampling event, but it still does not identify the execution configuration with the decoder configuration. [Transport boundaries][SEL91]

Let the executed and decoder configurations be separate parameters. Normalising their selector representations preserves their mixed decoded histories and the exact measure of the inherited old-execution/computed-decoder failure event. Consequently the inherited positive-measure mixed failure survives, while the matching computed-execution/computed-decoder control retains its positive result. The mixed and matching histories remain distinct. It would be an error to describe representation normalisation as fixing the old/computed mismatch, or to move its failure to the matching pair. None of these comparisons establishes that an arbitrary kernel environment satisfies the original implementation premises.

`CertifiedSelectorFamily` packages **every supplied record** satisfying the original sparse-fixture certificate. It retains that selector record literally, while the other configuration fields retain the fixture kernel, initial state, full initial support and winningness premises. The false literal used as a record template supplies no false-orientation hypothesis: its whole selector field is replaced. Normalisation yields the exact literal configuration indexed by the recovered orientation. That recovered model is fixed from the record **before** the quantifiers over tapes and fallback pairs. The actual-law mixed failure therefore holds for every supplied certified representation and every fallback pair, including arbitrary ignored high-digit additions. [Supplied certified family][SEL42]

The independent supplied-record controls verify that this packaging neither strengthens nor weakens the original certificate, that the recovered model is bit12 without a tape argument, and that ignored high digits do not change it. They also retain the old action's constant-model identity on acquired histories, measurability of the mixed failure event, the matching positive control and the nonidentity of mixed and matching readouts. The conclusion is a uniform representation-family corollary of one inherited mechanism, not a collection of new policies or a closed evaluation of the opaque original selector. [Supplied-record consumer][SEL217]

The scope source reports historical independent rebuilding of the167-module inherited positive-runtime closure, thirteen endpoint axiom readbacks,138 added declarations and45 independent control theorems. Its axiom boundary retains the pinned official external cache and the declared uses of `propext`, `Classical.choice` and `Quot.sound`. Those are attributed historical observations, not fresh executions here. A public receipt view or an object-identity check is not a kernel replay. No equality of bytes, meters, costs or finite-fuel thresholds, arbitrary-kernel selector extraction, arbitrary-raw-input equivalence, Python/CPython refinement or compiler correctness is added. Historical timeouts and interrupted whole-denotation probes remain inconclusive, and corrected proof-script or namespace failures are not promoted into mathematical refutations. [SEL8]

<a id="third-cohort-b-radix-proof"></a>

The finite-radix provider explains the arithmetic behind this bounded-record classification. For natural a,c,b,n, equality of the residues a mod bⁿ and c mod bⁿ is equivalent to equality of every used digit, (a div bⁱ) mod b=(c div bⁱ) mod b for i<n, using the source's natural-arithmetic conventions. A digit below n is unchanged by reduction modulo bⁿ because b^(i+1) divides bⁿ. Conversely, induction on n reconstructs the residue from the lower-width residue and the next digit. If a,c<bⁿ, the residue equality is exactly a=c. The binary selector application uses b=2. [T750B650]

This proof does not require a no-leading-zero convention or evaluate a retained selector. It removes unused high digits while retaining all used digits; it does not select an orientation or equate arbitrary off-domain executions. The separate selector-certificate construction supplies existence by packing all finite support/state cells, including off-target cells, but its target choices and `certifiedData` remain noncomputable. Arithmetic normal form and existence of a certified table therefore do not by themselves produce a callable extractor. The predecessor's `labelList` native-evaluation probe marks a further code-generation boundary, not a semantic counterexample to the policy propositions. No native evaluation is performed here. [T750B624] [T750B642]

[T750B624]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a98dd426230e649153162c405065e69fad46c538b56cb5dd73064f59532a3efc/SelectorCertificateConstruction.lean
[T750B642]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ae0d5b1e2e0bb5c4bfb7a07c54aa77ea787d07ef3e60fb671751a6bb225a12c1/PredecessorCallableFailure.lean
[T750B650]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b031dccba7de3cf461cf46caa84bb8c3dad71593b149622775bd7f9300058541/FiniteRadixNormalForm.lean

The direct `SelectorSemanticTransport` source proves a reusable congruence behind §2.5. `normalizeConfig` changes only the selector representation, is idempotent, preserves the certificate, and commutes definitionally with `withComputedTolerance`; its induced policy and representation are definitionally unchanged. The actual source-program equality is required only at encoded acquired histories. `normalization_with_derived_domains` keeps **both** original and normalized compiled call-domain derivations beside that equality and the runtime-output equation. Agreement on malformed arbitrary register inputs is unnecessary. [T750-C688]

More generally, if p implements executed policy a and q implements executed policy b, equality of their acquired-history policies gives equality of each runtime frame at `4*n+j` and hence of their complete output functions. Decoder-policy equality is a separate premise. The mixed readout congruence allows the executed and decoder configurations to have different kernels, menus, priorities and tolerances, provided each has its own certificate and each normalization comparison is made within its own role. Pointwise equality gives equal mapped laws under every input measure and equal preimages of every event. In particular it preserves the exact old-execution/computed-decoder parity-failure event and the equivalence of its positive-measure claims; this equality uses literal function rewriting, not an extra measurability assumption. It does not itself establish positivity, configuration correctness or a runtime resource bound. [T750-C688]

The associated raw-contract control preserves the distinction between payload 0 for no target and payload 1 for a present empty target, and exhibits why unused high digits can affect malformed raw calls. The padding control establishes that the exhausted sentinel and every below-four guard execute `skip`; duplicate-free collection also retains the protected low source registers. Together these controls locate the domain on which the semantic transport operates rather than claiming arbitrary-input extensionality, byte identity, finite fuel, Python refinement or wall time. [T750-C695] [T750-C729]

[T750-C688]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b9a5504f7519646341af9c2cbef93848bb364fce87a1dc701d44450b70018ecb/SelectorSemanticTransport.lean
[T750-C695]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bdf5d1569d2339f324b19171b1b40ee82fabff6f15d00d41d05cd8d1e310bd9f/ReviewerRawContract.lean
[T750-C729]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c53801c0426e6ec2b350efe41064804469092355a24b090475d743eece8e8299/ReviewerPaddingBoundary.lean


<a id="final189-b08-nontrivial-fixture-and-mixed-law"></a>

The earlier permissive fixture has a separate nontrivial mathematical role. Both modes have full-support rows and both actions are permitted, so observation never eliminates either mode. Priority is2 when the action equals the candidate and1 otherwise. Each candidate has exactly its good-action component, both states lie in the winning region, and the selector/configuration certificate exists. Nevertheless tolerance2 exceeds every possible empirical row discrepancy, making rejection false on every finite history. The old source policy consequently keeps its initial candidate and its corresponding component forever. The initial orientation is a noncomputable retained choice in this source, not a computed Boolean. These facts expose a tolerance-sensitive behavior omitted by the selector certificate; they do not deny existence of a correctly calibrated winning policy. [F189B-846](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e655233c8119f0f41b897f230ca2bca528955237e040d9f391f0f955aac83dcc/NontrivialFixture.lean)

The mixed receipt-law theorem proves why an output-law match need not identify that executed policy. It gives the implementation certificate only to a₀, whose actual action is constantly the actual model. Its physical receipt row is the fixed blind row (false:2/3, true:1/3). An independent decoder a may label those same receipts by its own action history. Row-likelihood equality, exact finite marginals and reconstruction from the last history give equality of the complete decoder-labelled history law with the blind Markov law for a. Measurability and the implementation/constant-action premises remain explicit; no implementation certificate for a or equality a=a₀ is inferred. This is a constructive whole-law ambiguity, not just a comparison of a few displayed outputs. [F189B-854](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e8d177b38fd63681f5402805f7ee237e113cbea9e75d2d7b58bb693f1570e5c1/MixedReceiptLaw.lean)

#### Local contracts compile the complete acquired history

The history compiler supplies a local route to that full source-policy identity. The empty acquired action/receipt history has code 1; adjoining (a,y) replaces the code h by 4h+2·bit(a)+bit(y). This newest-first encoding is injective and retains neither rejection symbols nor timing. The compiler reverses its digits, initializes a finite statistic vector, replays accepted pairs in chronological order and applies a final readout. Initialization, one-step preservation and readout contracts suffice to derive the result for every encoded history; a complete observed-law equality is not an input. The history numeral bounds the loop, and exhausted sentinel padding skips the source step. This is a totality construction, not a practical fuel or polynomial-time guarantee.

For the Boolean full controller, the vector has eighteen entries: phase index, retained target, live support, observed state, two global departure counts, four pair counts and eight pair/receipt counts. The newly completed receipt updates the full-history statistics before the old-phase test; phase or target changes do not reset the counts. Supplied selector digits are bound to the exact retained choices. The empirical code tests all eight coordinates using natural arithmetic: for row u/v and tolerance t/d with positive denominators, the rejection condition is k<n and tnv≤d((mv−un)+(un−mv)), where subtraction is truncated natural subtraction. Thus equality at the tolerance rejects, whereas a zero count fails the strict gate. The program does not divide by the empirical count or call a real-comparison oracle.

The source contracts then yield the complete arity-one retained policy on encoded histories. The separate callable parser/stack API returns its value with sufficient fuel and returns none, rather than zero, on parse, arity or fuel failure. This API does not change the binary observer's conventions. In the existing 1/3-versus-2/3 environment, the full-runtime theorem further binds every physical frame to the retained history dynamics on the same input tape, with false initial state. This fixed-wrapper result is not an arbitrary-row environment compiler. To invoke the matching positive law below, the computed tolerance is installed in both the executed program and the decoder; this replacement need not preserve the old policy. Source compilation does not erase the old/computed mismatch. [C250-069] [C250-077] [C250-079] [C250-080] [C250-081] [C250-085] [C250-087] [C250-088] [C250-090]

[C250-069]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/ed52e6e170f60c295433db53d6b22b3e68ecda53576135f341fda5d751124d1d.lean
[C250-077]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/f31458f71160f08b4497d557e7d580003a6a81938fef24d98120826d659fd2be.lean
[C250-079]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/4907343c789529a0d38244b1e7ecf5a97ff269e0d5c8ce6c04deac9b4b2faa7a.lean
[C250-080]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/8454e9786174b72ef57354a017e54d715eb3ab47a33f6625ba640f75decbc913.lean
[C250-081]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/e08cce6cdc7034ed6ffa1ff45a7f1d056f75a9c5ec2924fa80a9207fc37c96d9.lean
[C250-085]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/e5925724cb9f32deffc6aac3c06d23d6026fea14b34280016b7e3f0240d91b56.lean
[C250-087]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/68ac15406f7ddcb72a17283643ebb19b5f18a0818cebd40f20e38d1af9ca6db9.lean
[C250-088]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/d74aacce6e5f7a52a9579b450ebda2d6f67054706c817a9825b7638f4db9b988.lean
[C250-090]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/060386df73d9b80f1156ddb4a5da8d2d3e286d796b3cdcf029eb7006fd87fca8.lean


#### Exact full-controller laws and what the controls establish

The positive full-controller boundary has two explicit proof stages. `FullControllerReceiptLaw` identifies each finite receipt cylinder with a chronological kernel product. Its recursion multiplies the next row probability at the state and action computed from the acquired history, then extends that history by the actual action/receipt pair. The source-program implementation theorem and the supplied selector certificate connect the generated program to that policy; equality of the configured kernel with the fixed Boolean fixture remains a premise. Cylinder agreement determines the entire finite measure, so the resulting path-law equality is derived rather than assumed as a sampler specification. The same source factors the joint receipt/rejection-count probability into the kernel product and `clockMass 2 3`. That factorization concerns the logical rejection clock, not machine instructions or wall time. Infinitely many reports occur almost surely; no timeout invents a receipt, and forever-rejection tapes are not declared impossible. [N250B-078]

The underlying rejection calculation starts from a deterministic table with D entries and a common L-bit proposal width, where 0<D≤2^L. Read the first acquired bit as most significant, reject codes at least D, and otherwise return the indexed table entry. If w_y entries return y, the event of exactly r rejected proposals followed by y has fair-tape probability (1−D/2^L)^r w_y/2^L. Summing the disjoint first-acceptance events gives w_y/D. The rejection count has geometric mass (1−D/2^L)^r D/2^L and factors from that receipt; its law does not depend on the table's row labels. Eventual acceptance has probability one; when D<2^L, forever-rejecting tapes still exist.

The existing Boolean wrapper realizes D=3 and L=2. Each core acquisition emits the ordered four-bit frame [accepted, observed state, action, accepted-and-receipt]; only the first acquisition of a frame invokes the policy, and the remaining three serialize its fixed payload. Two such frames make one proposal. Its first frame never acknowledges; output coordinates 8k+4 and 8k+7 supply the kth proposal's acknowledgment and receipt. Given the per-call history-policy implementation certificate, this readout equals the literal adaptive sampler on the tape subsequence x₀,x₄,x₈,…. Rejections leave the acquired history unchanged; only accepted action/receipt pairs are appended. The equalities hold on every tape, including the all-one tape that never reports. The corresponding fair-tape cylinder and rejection-clock laws use the separately imported adaptive-cylinder and fair-subsequence results.

The receipt decoder is a noncomputable mathematical readout of the optional proposal sequence. At coordinate n it chooses the unique available accepted prefix of length n+1 and returns its last receipt; if no such prefix exists it uses a fixed default. For the finite receipt alphabet and measurable proposal events, the resulting map is measurable on all tapes. Almost-sure existence of every finite accepted prefix makes the default irrelevant to every decoded cylinder probability. A finite target measure with those same cylinder masses is then the entire decoded law. That target-cylinder hypothesis characterizes the comparison law; it does not assume a sampler-law equality. The totalized readout creates no executed receipt and gives no termination guarantee on the null noncompletion set. [C250-127] [C250-091] [C250-092] [C250-095] [C250-129] [C250-128] [C250-130]

[C250-091]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/a0b92099123636fdc7c42679dce3375c739ea0083cbf5df1ef7a49fb60a72906.lean
[C250-092]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/c8f078876a9ffabfc3201da4ee8b265580798b0ea8456067fb0302626485cf91.lean
[C250-095]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/84b196458bb2ebc6809dc015d130a0b2f15f1c59003fb0229163e67667f1ea5c.lean
[C250-127]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/182a163ebc20bc5ec381eacfcc3b1b460f4cb2efa9f5ccd2e00b9431c4571572.lean
[C250-128]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/233c0a05c5938b4da2f8aadc2c823230702be3597f64413dc0ecfebb061ff65d.lean
[C250-129]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/ebd79d6c905adde49c20b199f8c6045d21a5a3ba8e62021fe2f949c8119ff0a3.lean
[C250-130]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/4b04250322843306880c2e1dfaf67178136b887a19063e80e8f9b3e5ea552856.lean


`FullControllerCanonicalLaw` then proves the exact history-policy identity and transports the runtime law to the canonical Markov history law. Its physical formulation applies one measurable decoder to the actual output stream: that decoder has no hidden-model or original-input-tape argument. The positive computed-tolerance theorem changes **both** the executed program and this decoder to `withComputedTolerance c`, carries the certificate across that change, and retains the fixed kernel, false initial state, winning-region and actual-model-support premises. Parity success is a statement about the decoded history under the physical output law, not parity of the raw Boolean stream. The receipt-law source imports `FullControllerRuntime` and `RuntimeReceiptPath`; the canonical-law source additionally uses `ComputedToleranceSource` and `CanonicalHistoryBinding`. Reading these two proof bodies is not a fresh check of those imported closures. [N250B-077] [N250B-078]

Even two valid separating tolerances need not preserve a literal guard. In the retained 1/3-versus-2/3 fixture, two receipts at one source/action with frequency 1/2 give discrepancy 1/6. For candidate false at phase index zero, tolerance 1/10 rejects and tolerance 1/5 does not, although both are positive and below the inter-model gap 1/3. A sufficiency condition on the tolerance is therefore not an identity theorem for observed-history decisions. [C250-126]

[C250-126]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/75b809af1f8bf8d2791c5df1ddee746f056eb349486f79e300a502ed57d897a9.lean


These dependencies explain the corrected negative control. Keeping the old program while using the computed decoder does not satisfy the matching implementation boundary. In the permissive fixture above, tolerance 2 prevents rejection on every finite acquired history and fixes the actual action at the retained initial model. Its receipt stream has the blind row with true probability 1/3. The corrected argument uses the computed policy's parity result under the opposite model, positive finite-prefix support and agreement of the relevant tail rows to obtain a positive-measure failure of the mixed readout. The retained model is chosen before the tape quantifier. The independent source review checks that the negative argument uses the computed-policy theorem, not the positive full-runtime theorem it is testing. Matching old/old and computed/computed controls remain positive. This establishes the precise mixed statement's failure under its retained hypotheses, not failure of the matching theorem. [N250B-074] [N250B-075] [N250B-086] [N250B-089]

The literal companion has a narrower computational role. It retains the opaque orientation as a two-case disjunction, using cycle codes 44812 and 24332, the common target code 428783445879334172098560 and stage code 64080. The off-path singleton-menu restriction gives complete selector certificates without selecting the opaque orientation by native evaluation. At least one of the two certified records realizes the semantic failure; it is not asserted that both do so for one fixed retained enumeration. The recorded native check parsed four 48,389-byte arity-one programs and compared 340 encoded histories of lengths zero through three. The zero-step run reports resource exhaustion. These finite checks support literal source correspondence on their stated cases; they are neither a direct Lean whole-denotation evaluation nor a proof of all-history Python refinement. The interrupted whole-denotation probe, exit 130, remains inconclusive. [N250B-060] [N250B-061] [N250B-087] [N250B-088]

The codec matters to that interpretation. Its bounded-loop program syntax denotes primitive-recursive functions for each well-formed program; its universal evaluator is not thereby a uniformly primitive-recursive evaluator. It distinguishes malformed syntax, interpreted as zero, from step, bit and recursion resource limits, which raise `ResourceLimit` rather than masquerading as output zero. Inlining renames and reinitializes temporary registers on every invocation, preventing a previous call from becoming hidden state. The rational prefix and bounded counter-machine utilities remain implementation support, not extra runtime-law hypotheses. [N250B-062]

Finally, the replay and identity scripts preserve different evidence. They check exact source manifests and dependency identity, build positive dependencies before interpreting mutation failures, and keep explicit resource limits. The read-only dependency verifier accepts either the pinned clean Git checkout or the specified exact source archive; acceptance of the external object cache is not a claim to have rebuilt it. The portable review wrapper corrects path/working-directory assumptions without changing proof sources, while retaining the original historical records. Historical rebuilding of the 167-module runtime and 146-module cost closures, review controls and literal checks is reported by the reviews. No replay script, compiler, source program or proof checker has been executed in this consolidation. [N250B-063] [N250B-076] [N250B-079] [N250B-080] [N250B-086] [N250B-087]

[N250B-060]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/0ce9886d63c9b890e1b6b2c560646a4f437c11c2cdde31d2a7004f772cc4a6af/README.md
[N250B-061]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/15ad3c3ef916810047f18dad43e465b6194276e0272f98063bfe3d63862a1b95/check_literal_native.py
[N250B-062]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c/prcodec.py
[N250B-063]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/4ea6ca77e7fcbac28051e214173d51b9caf82b2778bd1e8531b2cb064856c3c3/replay.py
[N250B-074]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/160a3b2d5109cfb199a0fc2a8bbfe3db2c68fb159409a14fb6a067b6158ad15e/README.md
[N250B-075]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/8ceccb1dd4ed96945bd27fc190111ae993d2b9fca36d685e337f1b8afd5baf6b/RESULT_INTERPRETATION.md
[N250B-076]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/abef8d7017860e73b131c499357654323f0cf5f43ff0154439427ebb8a4e5dcc/replay.py
[N250B-077]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-continuations/source-store/47df70da9ffde6c5c8f4e7e443e7d4d7389b36001ebd60d15d5c9cb60b2ff1b3.lean
[N250B-078]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-continuations/source-store/c695053bcead7d268b6598b1e7823e1224b2bb28411089b836d517a752036311.lean
[N250B-079]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/7deeab885edfa67829f733766a1d8e9f08439157dec5bd54f05681371ed0e10e/verify_dependency_identity.py
[N250B-080]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/113a31ecdbef8566900fdffd36550b20458315d0508a45880b81f3af1202bb7c/README.md
[N250B-086]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/33aee6f3c86f311ab1e778e4b265a2000a6a732826f8dd18b9ca3f8a31df6592/CORE_REVIEW.md
[N250B-087]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/0898a17498cbe1b488ef2efdd9f256684c13e66c40b758e1333c3cef7b6fdbb7/LITERAL_REVIEW.md
[N250B-088]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/49b2ff378c1bffda370eff5f1af956e30ea2514a43e2b65768dde842eb32cddc/LITERAL_SOURCE_REVIEW.md
[N250B-089]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/0577b8bfcb99a87758160543804959403442591344556a89955a07055898a7cc/SOURCE_REVIEW.md

#### Source review, artifact verification and replay are distinct evidence

The three selector source reviews independently explain the existing A1–A3 derivations: exhaustive raw digits recover the bounded record, actual interpreter calls supply the range restrictions, and supplied certified data fix the recovered model before all tape/fallback quantifiers. They add no arbitrary-input extensionality or closed evaluation of the retained opaque choice. The finite arithmetic control enumerates both literal orientations, tests used-bit mutations and impossible retained payloads, and exhibits the malformed support 4 high-bit difference. It expressly does not evaluate the opaque initial candidate. These are source-specified controls; their asserted outcomes were not regenerated here. [N250C-115] [N250C-116] [N250C-117] [N250C-119]

The public verifier checks more than a top-level digest. Its explicit exception-based guards require exact file census, unique records, unchanged original manifest identities, complete original-to-public maps, null destinations and reasons for omissions, exact required scientific/control preservation, and the full proof-source binding census. Those guards remain active under optimized Python. Its negative tests reseal altered public manifests when testing deeper projection errors, so they distinguish binding failures from a simple stale top-level hash. The test program also checks wrong proof binding, extra Lean source and host-path leakage. This is artifact integrity and projection qualification, not an authorship or mathematical-soundness theorem. [N250C-124] [N250C-122]

The separate Pilot 0 freeze helper has a weaker raw framing contract. It sorts relative paths and hashes, for each file, path bytes, a NUL byte, unrestricted binary content and another NUL, excluding the basename FREEZE-HASH.txt. At this function’s interface, one packet containing exactly file a with content x and file b with content y produces the same prehash bytes as another containing only file a with content x followed by NUL, b, NUL and y: both serialize as a, NUL, x, NUL, b, NUL, y, NUL. The paths contain no NUL and neither is excluded. Thus the raw concatenation is not injective; no cryptographic SHA-256 collision is needed. An independently enforced file census, length framing or content restriction could distinguish or exclude these inputs, but this function supplies none of those checks. This is an analytic example at the displayed binary interface, not an executed packet collision, evidence that either historical pilot contained such bytes, or a diagnosis of the separate public verifier above or current publication tooling. The actual packet contents and surrounding constraints were not inspected. [AFTER2384-EIGHTH25-192](../scripts/freeze_pilot0.py#L21-L35) [AFTER2384-EIGHTH25-192](../scripts/freeze_pilot0.py#L38-L50)

The public replay wrapper treats reuse separately. A qualified core result must report completion, bind exactly 167 source/object pairs and the endpoint readback, have the exact object-file census, and contain no symlinks. Its fixture tests include duplicate module records and missing readback as well as altered/missing objects. Reuse records zero new kernel checks. A fresh path instead invokes the inherited runtime closure and then 15 source/control stages, with 183 requested axiom declarations. File-only intake ends with an explicit no-new-kernel-check status. The original assertion-based A2 census helper and its controls remain historical sources; the public wrapper disables optimization for those historical subprocesses while keeping its own guards active. [N250C-114] [N250C-118] [N250C-120] [N250C-121] [N250C-123]

The selector-continuation validator specifies a narrower route for finishing a missing target audit without relabelling old production as new work. It binds the earlier receipt as FAILED with proof scope NONE and sends only that unchanged receipt through the ordinary validator. Its separate continuation envelope retains one physical selector run, 45 children, 15 selector objects and 167 qualified core objects, while declaring zero new producer runs, child compilations, custom objects and independent-evidence increments. The fresh process is the target audit. Recollected child records must match the retained physical-run, parent-log and output bindings; their new observation times are not substituted for original execution. Before/after source, object, dependency and cache identities are required to agree. The no-follow custody inventory permits exactly its pinned negative-fixture symlink literal and separately hashes its nonexecutable sibling; this exception grants neither proof-import nor execution credit. Qualification additionally requires a completed zero-exit fresh audit and all seven exact target readbacks with their closure, type, axiom and log associations. A completed unsuccessful audit remains FAILED, while timeout or interruption is RESOURCE_INCONCLUSIVE; neither receives partial target or proof credit. These are requirements written in an unexecuted validator, with the producer, audit implementation, imported API and retained receipts still separate dependencies. Reading the envelope cannot itself qualify the suite, restore the old failed receipt or establish faithful execution. [AFTER1384-S13-246](../scripts/v5_selector_continuation.py#L33-L55) [AFTER1384-S13-246](../scripts/v5_selector_continuation.py#L58-L110) [AFTER1384-S13-246](../scripts/v5_selector_continuation.py#L119-L211) [AFTER1384-S13-246](../scripts/v5_selector_continuation.py#L215-L273)

The separate P1 tail recipe continues a retained failed attempt without relabelling its production as new work. It requires the old receipt to remain FAILED with proof scope NONE and exit one, binds its original child ledger and nine retained object/source/capture pairs, and preserves the old never-started inventory. The prescribed new work is four finite Python children followed by one audit of forty-one targets; new Lean producer builds, original-wrapper reruns and independent-evidence increments remain zero. Its finite report distinguishes identity-only source shape, two contract tests, twenty-six edge cases, 266,760 differential cases, 1,593 seeded boundary cases and eighteen internal mutation comparisons. Those internal comparisons are not eighteen rejecting subprocesses. Complete qualification additionally requires ordered successful child captures, report/source/copy/log joins, safe target readbacks and matching dependency checks before and after. A failed or partial continuation retains NONE rather than partial proof credit. The subsequent finite view is a zero-process join of that same qualified continuation, not another run. The body fixes source Python 3.12.3 separately from orchestration Python 3.11.9; these are historical recipe requirements, not evidence of present tool availability. None of its API, metadata, retained receipts, tools or private parameters was requalified by reading this source. [AFTER2134-S7-159](../scripts/v5_p1_tail_assets/p1_tail_recipe.py#L97-L197) [AFTER2134-S7-159](../scripts/v5_p1_tail_assets/p1_tail_recipe.py#L383-L461) [AFTER2134-S7-159](../scripts/v5_p1_tail_assets/p1_tail_recipe.py#L516-L599) [AFTER2134-S7-159](../scripts/v5_p1_tail_assets/p1_tail_recipe.py#L627-L671)

The separate P1 finish recipe starts from a later failed tail whose first three finite children, SourceShape, SourceContract and PythonEdges, already completed; it retains their exact captures and leaves that parent FAILED with proof scope NONE. It prescribes only the remaining IndependentPythonControls child followed by the forty-one-target audit, and forbids recreating the three retained observations as new output captures. Qualification still requires the remaining child’s source, raw/projected log and finite-report associations, successful target readbacks and unchanged dependencies after the audit. Its accounting retains nine builds and three finite observations while assigning zero new builds, original-wrapper runs and independent-evidence increments; its subsequent finite view is a zero-process join of that same qualified completion. These are requirements of this unexecuted successor recipe, not evidence that a continuation succeeded or permission to count the earlier four-child tail and this remaining-child finish as independent replays. [AFTER2884-SECOND25-39](../scripts/v5_p1_tail_finish_assets/p1_tail_finish_recipe.py#L7-L55) [AFTER2884-SECOND25-39](../scripts/v5_p1_tail_finish_assets/p1_tail_finish_recipe.py#L79-L155) [AFTER2884-SECOND25-39](../scripts/v5_p1_tail_finish_assets/p1_tail_finish_recipe.py#L183-L224) [AFTER2884-SECOND25-39](../scripts/v5_p1_tail_finish_assets/p1_tail_finish_recipe.py#L248-L341) [AFTER2884-SECOND25-39](../scripts/v5_p1_tail_finish_assets/p1_tail_finish_recipe.py#L373-L417)

The original-driver tracing body specifies a different association contract. It requires assertions to remain enabled, the exact driver and input-tree inventory, pinned tools and unchanged source arguments, and fresh external output and trace locations; check-only mode cannot qualify the complete recipe. Its direct, controller and nested branches insert capture transport around the original driver. In the nested branch the source-facing command remains distinct from the added transport vector, and both belong in the physical ledger. The wrappers restore the replaced process functions and recheck source inventories. These are requirements of an unexecuted instrumentation layer, whose capture helpers, data tables, drivers and receipts remain separate dependencies. The code alone proves neither that every actual child was captured nor that a physical replay occurred, and it adds no independent-review credit. [AFTER2134-S7-173](../scripts/v5_operational_assets_v1/runtime.py#L60-L94) [AFTER2134-S7-173](../scripts/v5_operational_assets_v1/runtime.py#L97-L158)

The G1 membership view is a different metadata operation, not another producer or audit. Its declared 109-member source map extends the original 107-file projection by the two named path-length and path-edge mutation controls, while retaining the original 127-member archive inventories. The validator requires the exact two-source suffix and associates each source with its existing physical child, expected exit-one mutation rejection, observation, target control, result and shared log. It retains the original executable descriptor separately and marks the enlarged view metadata-only. Its receipt binds the unchanged prior execution, permits only the declared membership-related field changes, and requires zero new processes, builds, audits and independence credit; an unsuccessful original execution cannot be promoted by this correction. Thus source membership, projected files, archive contents and physical runs are different counting units. These are the written requirements of the supplied module, whose adapter, catalogue and retained receipt remain unreceived dependencies here, not a fresh validation of those associations. [AFTER1634-S3-055](../scripts/v5_g1_membership.py#L1-L35) [AFTER1634-S3-055](../scripts/v5_g1_membership.py#L53-L72) [AFTER1634-S3-055](../scripts/v5_g1_membership.py#L82-L189)

The Task 4 domain-C probe gives a concrete reason to distinguish process completion from control success. It specifies thirty malformed or semantically inconsistent cases and ten positive controls, including order permutations, consistent checkpoint renaming and an additional nonselected claimant assessment. Some adverse cases recompute their checkpoint or assessment digests after moving a cutoff before its subject, binding two checkpoints to one target, or hashing unresolved authorities; correct hashing alone is therefore not the intended semantic acceptance condition. The driver classifies zero as acceptance, exit one without its TRACEBACK marker as bounded rejection, and other outcomes as traceback; each case passes only when its expected exit is matched without that traceback class. It prints the detailed summary, including all_expectations_met, but then exits zero unconditionally. A zero outer exit consequently does not establish that those cases met their expectations. The separate Task 14 adapter derives acceptance from a returned issue list or CLI result, raising for CLI codes other than zero or one rather than assigning success from the requested control/mutation role. These are distinct source-level reporting contracts, not observations that either production validator passed, rejected the intended semantics, or was deployed. [AFTER1884-E25-175](../scripts/task14_direct_probes.py#L29-L45) [AFTER1884-E25-184](../tests/task4_parallel_c_regressions.py#L167-L174) [AFTER1884-E25-184](../tests/task4_parallel_c_regressions.py#L244-L269) [AFTER1884-E25-184](../tests/task4_parallel_c_regressions.py#L341-L405) [AFTER1884-E25-184](../tests/task4_parallel_c_regressions.py#L410-L461) [AFTER1884-E25-184](../tests/task4_parallel_c_regressions.py#L176-L339)

A separately retained unittest union consumes those same three historical Task 4 lane definitions under a stricter outcome contract. It requires 13 lane-A cases, 25 lane-B cases and 40 lane-C cases, calls each lane’s production-entry adapter on its supplied baseline or mutation, rejects exit 99 and any output containing TRACEBACK, and asserts the case’s expected exit. Lane A assigns one to invalid cases and zero to controls; the other lanes retain their declared expectations. Consequently this wrapper’s case acceptance is not inferred from the standalone lane-C driver’s unconditional zero outer exit. That distinction does not repair or relabel the historical driver, establish the imported adapters or mutations correct, or turn 78 retained cases into 78 independent reviews. The union source was read without running its tests, so no fresh acceptance, rejection, coverage outcome or independence increment is claimed. [AFTER2134-S6-147](../tests/test_task4_parallel_review_union.py#L1-L66)

The separately retained waking/somnic unittest suite sharpens the distinction between presentation order and operational order. Reversing candidates, event-emission lists or ordinary target lists is expected to pass, as are neutral predecessor prose and a consistently renamed support identifier; reversing actuator stages is expected to fail. Its fifth-review cases also mutate a historical selector version or add a future-dated event, recompute the target-history digest from the altered records, and still expect rejection. These are specific instances of the semantic-boundary requirement above, not a new hash-authentication principle. The adapter calls production main on temporary document copies and maps ordinary exceptions from that call to exit 99; module import and document setup lie outside that handler. The negative-case assertions require exit one without a TRACEBACK marker. These are suite expectations, not observations that the unread production validator or fixtures passed, a complete hostile-input proof, an additional independent review, or evidence of deployed writeback. [AFTER2384-FIFTH25-123](../tests/test_somnic_orthing.py#L50-L135) [AFTER2384-FIFTH25-123](../tests/test_somnic_orthing.py#L1392-L1442) [AFTER2384-FIFTH25-123](../tests/test_somnic_orthing.py#L1508-L1527) [AFTER2384-FIFTH25-123](../tests/test_somnic_orthing.py#L1593-L1678)

The dependency packets, compiler and official cache are explicit prerequisites. Neither the verifier nor the wrapper downloads them, and a source-only read does not supply them. Preservation of the source reviews' historical successes, failures and limitations is compatible with this incorporation performing no replay. These evidence distinctions supplement the mathematical account above without creating another selector result.

## 3. What physical examples establish

### 3.1 Channels and processors have different roles

An air gap excludes the declared direct logical or physical connections; it does not assert universal causal isolation from the surrounding world [NIST]. Thermal, acoustic and electromagnetic research demonstrates particular channels under particular access and equipment conditions. BitWhisper, Fansmitter, AirHopper and GSMem are examples of that limited proposition [CHAN]. They are not evidence that an unmodified system admits every desired channel, that arbitrary initial access is available, or that the surrounding medium can execute the sender's computation. Their relevance here is the separation between a physical influence, a controllable signal and a demonstrated usable channel.

NIST's TEMPEST definition concerns the investigation and control of unintentional compromising emanations [TEMPEST]. Such unintended emissions, deliberately modulated covert transfer and authorised unconventional communication are related but distinct objects. The same physical path can be relevant to more than one, without determining its permission or security-policy status. Host replacement can also be an operator-approved service migration; its authorisation remains separate from its physical feasibility.

Ionospheric conditions affect particular radio paths, as NOAA's technical account explains [NOAA]. Molecular communication models likewise require transport, emission and detection assumptions [ECK]. These are carrier and channel examples. A medium's ability to carry a signal is not a proof that it stores the relevant state, implements a decoder or realises Δ. A propagation model alone also does not provide an autonomous system that can find and maintain the proposed link.

There are genuine processor examples as well. The appropriate inference is bounded by the demonstrated role:

| Research example | Positive contribution | Boundary relevant to continuation |
|---|---|---|
| Prakash and Gershenfeld's microfluidic bubble logic | Logic and a bistable toggle/flip-flop mechanism in a fluidic device | The device still has engineered preparation, flow and interfaces; it does not demonstrate arbitrary processor migration. |
| Benenson and colleagues' biomolecular machine | A programmable finite automaton using molecular representations and transformations | This is a bounded computational construction, not a demonstration of every program or a transferred running large model. |
| Shen and colleagues' nanophotonic network | Physical optical linear transformations in a neural computation | In the inspected early experimental preprint, training is conventional and the nonlinear stage is electronic; the whole system is not all-optical. |
| Wright and colleagues' physical neural networks | Physical computation with a hybrid physical-digital training method across several platforms | A demonstrated trained task is not a proof of a specified large model's complete stateful contract. |
| Wright, Wang, Onodera and McMahon's physical foundation models | A concrete proposal for fixed hardware implementations of large neural networks | The 2026 version inspected is a proposal, with scaling and engineering questions, not a reported large-scale implementation. |

The historical claims in this table are supported by the cited authors' papers or primary abstracts [BUB], [BIO], [SHEN], [WRIGHT], [PFM]. They rule out a blanket claim that nonstandard physical processors are unknown. They do not turn a new implementation or handover into an accomplished experiment.

Learning methods do not erase the interface obligations. Sparse identification of nonlinear dynamics and data-driven PDE discovery use structural assumptions, candidate libraries and measurements; they are not universal discovery oracles [SINDY], [PDE]. Information-processing capacity of a driven dynamical system is a task-and-readout question with explicit conditions [DAMB]. A reservoir's richness is useful only insofar as an accessible encoding, readout and error account make it useful for the declared task.

### 3.2 A substitution profile, not a ladder of intelligence

A substitution statement should identify a source realisation, destination realisation, fixed contract, role-class map, excluded support set and environment. Changes of component, host, carrier, processor, joint organisation and online configuration are different axes. One may occur without the others. A processor can remain in the same host; a channel can change while the processor remains fixed; a recomposition can introduce new shared dependencies.

These axes should also be separated from the kind of evidence available:

1. A mathematical or engineering model specifies a candidate arrangement.
2. A correspondence proof establishes a stated property of that model.
3. A finite computation or simulation checks declared cases or numerics.
4. A physical implementation demonstrates a task in an apparatus.
5. A paired stateful handover demonstrates continuation from the particular source state after the named original support is removed.

The list distinguishes records, not stages guaranteed to follow one another. A correct proof can concern an unrealised model. A physical device can work without a complete model proof. A paired handover needs an export and activation protocol beyond two stand-alone implementations. None of these records by itself measures intelligence, consciousness or moral status.

Ordinary replicated services and familiar hardware redundancy are valuable positive controls. If a proposed vocabulary cannot recognise an already competent implementation with explicit assumptions and guarantees, the vocabulary needs correction. Its comparative value has to be tested against a strong conventional description supplied with the same information.

### 3.3 Exact models, numerical approximations and empirical claims

There are three different verdicts for a bound-based analysis: the bound certifies the chosen tolerance; observed or proved behaviour violates it; or the available bound is inconclusive. A loose upper bound outside tolerance yields the third verdict, not the second.

This distinction is especially important for large models. Parameter count is not, by itself, a lower bound on every implementation of one fixed function. A family of arbitrary programs, an updatable program and one fixed behaviour have different storage requirements. A useful weight quantisation result, such as GPTQ, does not establish bit-exact equivalence of every operation or a uniform output-law bound for all contexts [GPTQ]. Conversely, lack of such a bound is not a proof of physical impossibility.

Storage capacity, precision, bandwidth, execution time, memory traffic and input-output obligations must be assessed jointly. The present theory supplies tests and conditional constructions. It establishes no universal three-barrier impossibility theorem for large-model substitution and no general theorem that any desired substitute can be built.


## 4. From physical influence to a robust message

### 4.1 Conditional noninterference

Fix an experimental specification ℛ: the message distribution, receiver-side prior information S, measurable observations and their precision, accessible interventions and encoders, horizon T and resource budgets. Its operational finite-horizon information budget is

```math
\mathcal I_{\mathcal R}(T)
=\sup_{e\in\mathcal E_{\mathcal R}}
 I_e(M;Y^{0:T}\mid S),
```

where the supremum ranges over the admitted message encoders for that same specification. It is not automatically an asymptotic Shannon capacity or a rate per unit time; a coding theorem needs its own channel assumptions [SHAN]. The proposed reusable communication competence concerns specifying, validating and composing such authorised heterogeneous interfaces, rather than assuming a universal code shared by all matter.

Let M now be a fresh message, and let Y denote the complete receiver observation through the chosen horizon. If, for every admitted encoding procedure, the conditional law of Y given S is independent of M, then

```math
I(M;Y\mid S)=0.
```

Every admitted encoder therefore has zero information and so does the supremum defining the operational budget. Let R be additional decoder randomness independent of the joint pair (M,Y) conditional on S. Then I(M;Y,R given S) is zero: its chain-rule terms I(M;Y given S) and I(M;R given Y,S) both vanish. Any measurable decoder applied to Y, S and R therefore remains uninformative about M beyond S by conditional data processing. Independence from M alone is insufficient. With constant S, independent fair bits M and R, and Y = M xor R, both Y and R separately are independent of M while their pair recovers it exactly. Prior correlation can help predict an already correlated variable, but it is not transmission of a new independent message. Conversely, an observed failure to find a channel is not a proof of noninterference for all admitted controls.

This zero-information result has a useful role: it states what a genuine no-channel premise would mean. It does not substitute intuition about separation for a verified model of all permitted paths.

### 4.2 An exact binary threshold for a linear system

Consider a finite-dimensional linear system on a finite horizon T > 0:

```math
\dot x=Ax+Bu,\qquad x(0)=0,\qquad
z=Cx(T)+n,
\qquad
\int_0^T\|u(t)\|^2\,dt\le E,\quad \|n\|\le\delta.
```

Here E and δ are nonnegative, the entire closed Euclidean noise ball is admissible, and the control is an admitted square-integrable input. Define the input-output operator and its output Gramian by

```math
L_Tu=C\int_0^T e^{A(T-s)}Bu(s)\,ds,
\qquad
W_T=C\left(\int_0^T e^{As}BB^\top e^{A^\top s}\,ds\right)C^\top.
```

**Proposition 1.** Two messages can be distinguished with zero worst-case error under these assumptions if and only if

```math
E\,\lambda_{\max}(W_T)>\delta^2.
```

**Proof.** The operator identity LₜLₜ* = Wₜ gives squared operator norm λ = λmax(Wₜ). Every attainable nominal output has norm at most √(Eλ). Hence the distance between any two nominal outputs is at most 2√(Eλ). If √(Eλ) ≤ δ, their closed radius-δ observation balls intersect; an observation in the intersection cannot be decoded correctly for both messages.

If √(Eλ) > δ, then λ > 0. Choose a unit eigenvector v of Wₜ with eigenvalue λ and use

```math
u_\pm=\pm\sqrt{\frac E\lambda}\,L_T^*v.
```

Each input has squared norm E and produces nominal output ±√(Eλ)v. Their observation balls are disjoint, so nearest-centre decoding is correct for every admitted noise vector. ∎

Strict inequality is essential. At equality the balls touch, and the touching observation is ambiguous. Full-state controllability is unnecessary: one controllable and observable direction can suffice for a bit. Stability of A over infinite time is also unnecessary for this finite-horizon result. Energy, output dimension and the particular readout C remain part of the statement.

For the scalar system with decay rate α > 0, actuation coefficient b and readout coefficient c,

```math
\dot x=-\alpha x+bu,
\qquad
W_T=\frac{(bc)^2(1-e^{-2\alpha T})}{2\alpha}.
```

With α = c = T = 1 and δ = 0.15, b = 0.2 gives Wₜ ≈ 0.017293. An energy budget E = 1 produces radius about 0.131504 and fails the strict threshold; E = 4 produces about 0.263008 and passes. With b = 0 there is no message dependence; with b = 1 and E = 1 the radius is about 0.657520. These are model calculations, not measured channel rates or apparatus results.

### 4.3 Nonlinearity and common calibration

Suppose a finite-horizon input-output map has a controlled local remainder,

```math
F(u)=F(0)+Lu+R(u),
\qquad
\|R(u)\|\le\kappa\|u\|^2
\quad\text{for }\|u\|\le r.
```

Let v be an admissible unit direction with gain σ = ‖Lv‖ > 0. If both ±av are permitted, a ≤ min(r,√E), and additive observation noise has norm at most δ, then

```math
a\sigma-\kappa a^2>\delta
```

is sufficient for a robust binary code. Indeed, the nominal output separation is at least 2aσ − 2κa² by the reverse triangle inequality, so the two radius-δ noise sets are disjoint. This is a sufficient local certificate. A purely nonlinear channel can exist when the chosen derivative gain vanishes, and failure of the bound does not rule out a different code.

Model uncertainty introduces another quantifier. A decoder that works after learning each model's calibration is not necessarily one decoder that works before calibration:

```math
\forall\theta\ \exists d_\theta
\quad\not\Rightarrow\quad
\exists d\ \forall\theta.
```

For example, y = θu with unknown θ in {−1,1} has nonzero gain in either model. Under the sign code u = ±a, the pooled observations for the two message labels coincide. There is no common decoder for that code without further information. This does not exclude a differently designed code, such as one using a separately distinguishable amplitude; it exposes the missing calibration premise.

A uniform positive result uses one reference offset and one reference linear map. Suppose

```math
F_\theta(u)=b_\theta+L_\theta u+R_\theta(u),
\quad
\|b_\theta-\widehat b\|\le\beta,
\quad
\|L_\theta-\widehat L\|_{\mathrm{op}}\le\eta,
\quad
\|R_\theta(u)\|\le\kappa\|u\|^2.
```

For a unit v put σ̂ = ‖L̂v‖. Every observation produced by ±av lies in a ball about b̂ ± aL̂v of radius β + aη + κa² + δ. Consequently, a single decoder works for every admitted θ if

```math
a(\widehat\sigma-\eta)-\kappa a^2>\delta+\beta.
```

The same two reference centres define that decoder. Statistical confidence intervals can be used only with their stated coverage event and error accounting; they are not automatically deterministic bounds for all θ. Units and norms must be consistent across calibration, dynamics and readout.

**Corollary 1: selecting amplitude within the certificate.** Let A₀ = min(r,√E), g = σ̂ − η and d = δ + β. Assume both inputs ±av are admitted for every a in [0,A₀], with the same uniform remainder and uncertainty bounds throughout that interval. For nonnegative κ, d and A₀, the largest certifiable half-separation margin before subtracting d is

```math
\max_{0\le a\le A_0}(ga-\kappa a^2)=
\begin{cases}
0,&g\le0,\\
gA_0,&g>0,\ \kappa=0,\\
ga_*-\kappa a_*^2,&g>0,\ \kappa>0,
\end{cases}
\qquad
a_*=\min\!\left(A_0,\frac{g}{2\kappa}\right).
```

The formula follows by differentiating the concave quadratic, with the zero-amplitude endpoint included. A positive-amplitude certificate exists exactly when this displayed maximum exceeds d. This is an exact optimisation of this sufficient bound on the admitted interval, not a necessary condition for all physical codes. If the actuator admits only a subset of amplitudes, a certificate requires an amplitude in that actual subset; the displayed interval maximum alone is insufficient. For example, g = κ = A₀ = 1 gives its maximum 1/4 at a = 1/2, but an actuator admitting only a = 0 and a = 1 has margin zero at both choices. More available energy can cease to improve this certificate once nonlinear uncertainty dominates; increasing amplitude is not always the right response to a calibration problem.

For σ̂ = 0.8, η = 0.1, κ = 0.1, a = 0.4, β = 0.03 and δ = 0.05, the reference half-separation is 0.32 and the uncertainty radius is 0.136. The remaining half-margin is 0.184. These numerical assumptions exhibit a nonempty robust regime. Their physical truth would have to be measured or otherwise justified.

## 5. Fluid dynamics: a bounded bridge from a model to an output

### 5.1 What the Navier–Stokes context contributes

Existence, regularity, prediction and control are different questions. A theorem about a solution's regularity need not supply accessible inputs, a stable decoder or enough information throughput. A bounded channel can sometimes be certified without solving a global regularity problem. Conversely, a smooth flow can have poor controllability, poor observability or extreme sensitivity for the chosen experiment.

For a smooth incompressible Navier–Stokes flow with suitable boundary or decay conditions,

```math
\partial_tu+(u\cdot\nabla)u
  =\nu\Delta u-\nabla p+f,\qquad \nabla\cdot u=0,
```

the energy identity is

```math
\frac12\frac{d}{dt}\|u\|_2^2+\nu\|\nabla u\|_2^2
   =\langle f,u\rangle.
```

The advection term cancels in this balance; it can redistribute energy without becoming a source of unbounded total energy. A singularity in a continuum model does not itself furnish usable infinite energy, unbounded precision or an accessible communication protocol. The elliptic pressure equation in the incompressible formulation is also not an independently available instantaneous actuator.

The distinctions between equations matter. Fefferman's official statement separates the unforced global-existence alternatives A/B from the breakdown alternatives C/D, which permit a forcing term [FEF]. Tao's averaged equation preserves an energy-cancellation structure while modifying the nonlinear operator; its blowup result shows why that coarse structure alone does not decide the original equation [TAO]. Magnetohydrodynamics introduces a magnetic field and its own assumptions [LEI]. Turing-complete Euler flows on a Riemannian three-sphere, Euclidean Beltrami constructions with non-finite energy, and robust tape-bounded constructions on a torus have distinct geometries and resource conditions [EULER], [BEL]. None is a demonstration that an ordinary atmospheric flow supplies a programmable, robust replacement processor.

The Third Edition's dated discussion of the 2026 Navier–Stokes announcement must be read historically. The released report states a forced finite-time blowup result, including a solution starting from rest, compact spatial support in a fixed compact set, bounded kinetic energy and unbounded velocity supremum as the stated finite time is approached [NSR]. Its theorem and introductory claim are not independently proved here. The manuscript's 10 September reading of Clay's status page preceded Clay's 11 September response. On 26 October 2026 the problem page displays “Active”; the separate 11 September announcement acknowledges the apparent settlement announcement and explains that evaluation and credit proceed deliberately [CLAY], [CLAYNEWS]. Neither record is replaced by an inference of prize award or completed verification.

These developments can motivate new estimates, algorithms or experiments. They do not, by themselves, give a channel, a processor or a migration protocol. To obtain a usable consequence, one needs a bridge to the actual experimental output.

### 5.2 A residual estimate on a fixed finite horizon

A particularly concrete bridge is available for a smooth incompressible solution u and a smooth divergence-free approximation v on a fixed torus over [0,T]. Use the same viscosity ν > 0 and force f in both descriptions, and define the approximation's continuum residual

```math
r=\partial_tv+(v\cdot\nabla)v-\nu\Delta v+\nabla q-f.
```

Assume the required solution and approximation exist on this whole interval, that

```math
L(t)=\|\nabla v(t)\|_{L^\infty,\mathrm{op}}
\quad\text{and}\quad
\|r(t)\|_2
```

are integrable, and that the initial discrepancy is bounded. This is a conditional finite-horizon estimate; it neither establishes global existence nor obtains a continuum residual bound merely from a plotted mesh residual.

**Proposition 2.** With w = u − v,

```math
\|w(T)\|_2\le B(T)
:=
e^{\int_0^T L(t)\,dt}\|w(0)\|_2
+
\int_0^T
 e^{\int_s^T L(t)\,dt}\|r(s)\|_2\,ds.
```

**Proof.** Subtracting the equations gives

```math
\partial_tw+(u\cdot\nabla)w+(w\cdot\nabla)v
  =\nu\Delta w-\nabla(p-q)-r.
```

Take its L² inner product with w. Divergence-free periodic fields cancel the transport and pressure terms. The remaining terms satisfy

```math
\frac12\frac{d}{dt}\|w\|_2^2
+\nu\|\nabla w\|_2^2
\le L(t)\|w\|_2^2+\|r(t)\|_2\|w\|_2.
```

To avoid dividing by a possibly zero norm, apply the inequality to √(‖w‖²₂ + ε²). Its derivative is bounded above by L(t)√(‖w‖²₂ + ε²) + ‖r(t)‖₂. The integrating-factor inequality followed by ε decreasing to zero gives the result. ∎

Let C map L² boundedly into a finite-dimensional Euclidean observation space, with operator norm c. Then the output error is at most cB(T). Point evaluation is not a bounded functional on L² in general; an experimentally meaningful spatial average or a stronger justified norm may be needed.

For two admitted experiments j = 0,1, let their nominal outputs be ŷⱼ = Cvⱼ(T), their residual bounds be Bⱼ and their readout noise radius be δ. If

```math
\|\widehat y_1-\widehat y_0\|
  >c(B_0+B_1)+2\delta,
```

their admissible observation balls are disjoint, giving a robust bit. Each experiment must have its own matched exact and approximate force/initialisation model, and the two experiments must be selectable by the sender. This is the missing connection between an analytic error estimate and a communication claim.

For an illustrative constant envelope T = 1, L = 0.4, initial error 0.02 and residual norm 0.01, the formula gives B ≈ 0.0421321. With c = 1.2, equal bounds for the two experiments, nominal separation 0.4 and δ = 0.04, the separation slack is about 0.218883. This is an evaluation of a supplied error envelope, not a fluid simulation. A larger gradient bound can worsen the exponential factor even when the underlying flow carries more complicated structure.

### 5.3 The useful research question

A new PDE theorem would have an operational consequence here if it provided a demonstrably better bound on an accessible experiment, a more reliable actuator or readout, or a cheaper control computation at fixed assumptions. The comparison should hold the input family, observation, horizon and resources fixed. It should report which uncertainty term improves and how that improvement changes the robust separation or cost.

No such method-specific practical advantage is established by the residual proposition alone. It does, however, turn an open-ended claim about “computation in fluids” into a testable path: certify a finite-time approximation, bound the actual measurement functional, show separated observable sets, and account for the controls that select them.


### 5.4 What an eliminated variable can leave behind

A reduction can change the information needed to continue an experiment even when it preserves the present reported value. The issue is especially visible when an omitted variable influences a retained variable's later evolution. The continuation source gives two elementary calculations: eliminating a variable can leave an exact memory term, while averaging a nonlinear flow can leave a covariance term. They identify additional quantities a reduction must retain or control; they do not establish a physical processor or a new global PDE theorem. [CONT]

Consider the scalar system, with fixed real coefficients and $`\varepsilon>0`$,

```math
\dot x=-ax+bxy,\qquad
\varepsilon\dot y=-y+cx^2.
```

On any interval where its solution exists, multiply the second equation by $`e^{t/\varepsilon}`$ and integrate. The exact result is

```math
y(t)=e^{-t/\varepsilon}y(0)
     +\frac c\varepsilon\int_0^t
              e^{-(t-s)/\varepsilon}x(s)^2\,ds.
```

The initial value and the convolution are still present after substituting this expression into the equation for $`x`$. Thus removing the explicit coordinate $`y`$ can replace a state variable by a dependence on history; it does not remove that variable's effect. The dependency is already visible at the initial time: two states with the same $`x(0)`$ and different $`y(0)`$ have different initial $`x`$ velocities whenever $`bx(0)\ne0`$. A special model or a narrower output contract can remove that dependency, but its removal needs an argument.

The formal algebraic substitution $`\varepsilon=0`$ instead yields $`y=cx^2`$ and

```math
\dot x=-ax+bcx^3.
```

That is a singular-limit proposal, requiring its own approximation hypotheses and error analysis. Neither this formal substitution nor the exact convolution justifies simply deleting the coupling and keeping $`\dot x=-ax`$. Lower state dimension can accompany a higher effective polynomial degree. Those two quantities are also distinct from the tensor degree of an episode record. This calculation illustrates the memory issue studied by reduced-order methods; the elementary identity, rather than an imported approximation theorem, is the argument used here. [CONT, “Why eliminating a component can create a new obligation”][CONT]

A corresponding exact averaging identity holds for a finite family of smooth incompressible Navier–Stokes solutions $`u^s`$ on a common spatial domain and time interval, with the same viscosity $`\nu>0`$. Let $`\pi_s\geq0`$ be fixed weights summing to one, and average the pressures and forces with those same weights. Define

```math
\bar u=\sum_s\pi_su^s,
\qquad
R=\sum_s\pi_s(u^s-\bar u)\otimes(u^s-\bar u).
```

Expanding the products and using $`\sum_s\pi_s(u^s-\bar u)=0`$ gives

```math
\sum_s\pi_su^s\otimes u^s=\bar u\otimes\bar u+R.
```

For a divergence-free vector field $`v`$, componentwise differentiation gives $`\nabla\cdot(v\otimes v)=(v\cdot\nabla)v`$, with $`(\nabla\cdot R)_i=\sum_j\partial_jR_{ij}`$. Taking the fixed weighted average of the equations therefore yields

```math
\partial_t\bar u+(\bar u\cdot\nabla)\bar u
 =\nu\Delta\bar u-\nabla\bar p+\bar f-\nabla\cdot R.
```

The mean record alone need not determine this covariance. At one time, an ensemble concentrated on a single field and an ensemble with compensating fluctuations can have the same mean and different second moments. The displayed evolution therefore retains a term that must be determined, represented or bounded under any proposed mean-only closure. The identity is conditional on the smooth solutions and fixed averaging weights; it neither proves that such solutions exist globally nor supplies a closure approximation. It makes no use of a blowup claim. [CONT]

The methodological consequence is common to both calculations. A learned feature map or numerical discovery procedure may propose a useful reduction, while a separate argument establishes what that reduction preserves and with what error. The source's comparison with its supplied Euler draft separates numerical discovery, spline representation, interval certification and stability analysis; its outstanding certification conditions remain part of that historical comparison. The finite moment-error theorem in [Information and Inquiry, §2.5](information-and-inquiry.md#25-quantifying-the-information-lost-by-a-moment-summary) provides one exact model-bound way to expose or bound a missing observable. It does not turn a finite model into a verified model of a fluid, an agent or a person. The finite-horizon residual estimate in §5.2 addresses a different question and retains its own hypotheses. [CONT]

### 5.5 Coupled estimates and a residual error floor

The finite-horizon estimate in §5.2 controls discrepancy using an accumulated growth bound. A different question is whether damping can keep a discrepancy inside a fixed admissible neighbourhood while the model remains valid. Two estimates may answer that question jointly even when neither controls all its coupling terms alone. The formalisation source isolates this mechanism, a strict residual barrier and the concentration estimate needed to absorb a local loss. The following arguments retain their conditional analytic scope. They require an actual dynamical model and valid estimates for its declared quantities; an order of preferred corrections does not itself supply a vector field or a gradient flow. [FORM, “A dynamical realisation is an extra declaration” and Theorems 10.1–10.2][FORM]

#### Combining two valid estimates

Let $`X(t),Y(t)\geq0`$ be differentiable on a common interval starting at zero. Suppose constants $`a,d>0`$ and $`b,c\geq0`$ give

```math
\frac12\dot X\leq-aX+bY,
\qquad
\frac12\dot Y\leq cX-dY.
```

**Weighted damping criterion.** A positive weight $`\lambda`$ makes both coefficients strictly dissipative in the combined estimate for $`V=X+\lambda Y`$ exactly when $`ad>bc`$. For any such weight,

```math
\gamma=\min\{a-\lambda c,\ d-b/\lambda\}>0,
\qquad
V(t)\leq e^{-2\gamma t}V(0).
```

**Proof.** Adding the first inequality to $`\lambda`$ times the second gives

```math
\frac12\dot V
\leq-(a-\lambda c)X-(\lambda d-b)Y.
```

The two coefficients are positive precisely when $`\lambda>b/d`$ and, if $`c>0`$, $`\lambda\lt{}a/c`$. For $`c>0`$ these conditions define a nonempty open interval exactly when $`ad>bc`$. For $`c=0`$, any $`\lambda>b/d`$ works, and $`ad>bc=0`$ already holds. This includes $`b=c=0`$, when any positive weight works. Dividing the second coefficient by $`\lambda`$ yields the displayed $`\gamma`$ and $`\dot V\leq-2\gamma V`$. Multiplication by $`e^{2\gamma t}`$ and integration proves the bound on the interval where the estimates hold. In particular, $`X\leq V`$ and $`Y\leq V/\lambda`$. ∎

The necessity statement concerns this combination with two positive coefficients. If $`ad\leq bc`$, sharper estimates or an additional relation between $`X`$ and $`Y`$ may still control the actual system. If an application independently requires $`\lambda\leq1`$, the feasible interval must also intersect $`(0,1]`$; $`ad>bc`$ alone does not ensure that additional restriction. [FORM, Theorem 10.1][FORM]

The product of gains matters even when one coupling is small. For the separate linear system

```math
\begin{pmatrix}\dot x\\\dot y\end{pmatrix}
=
\begin{pmatrix}-1&K\\\varepsilon&-1\end{pmatrix}
\begin{pmatrix}x\\y\end{pmatrix},
\qquad K,\varepsilon>0,
```

the characteristic equation is $`(\mu+1)^2-K\varepsilon=0`$. Its eigenvalues are $`-1\pm\sqrt{K\varepsilon}`$, so $`K\varepsilon>1`$ gives an exponentially growing mode. For any positive $`\varepsilon`$, however small, a sufficiently large $`K`$ has this effect. Thus a claim of weak feedback needs a bound on the interacting gains. This example does not identify its signal variables with the energy quantities above, physical frequency scales or stages of inquiry; any such interpretation needs its own model. [FORM, Counterexample 10.6][FORM]

#### A residual gives a range of admissible radii

Suppose $`E(t)\geq0`$ is continuous and $`E(t)^2`$ is differentiable. In a declared regime, including any first contact with the proposed boundary, assume

```math
\frac12\frac{d}{dt}E^2
\leq-aE^2+bE^3+rE,
\qquad a>0,\quad b,r\geq0.
```

Here the constants belong to this estimate; they need not equal the coefficients of the preceding two-level system.

**Strict residual barrier.** If an admissible radius $`\delta>0`$ satisfies

```math
b\delta+\frac r\delta\lt{}a,
\qquad E(0)\lt{}\delta,
```

then $`E(t)\lt{}\delta`$ for as long as the trajectory exists and the boundary-valid estimate applies.

**Proof.** If a first contact $`E(t_*)=\delta`$ occurred, continuity and the strict initial inequality would give $`E(t)\lt{}\delta`$ immediately before $`t_*`$. The left derivative of $`E^2`$ at contact would therefore be nonnegative. Differentiability and the assumed inequality instead give

```math
\frac12(E^2)'(t_*)
\leq-\delta^2\left(a-b\delta-\frac r\delta\right)
\lt{}0,
```

a contradiction. The proof never divides by $`E`$ and therefore also permits zero error away from the boundary. ∎

When $`b,r>0`$ and every positive radius is otherwise admissible, the coefficient inequality admits a radius exactly when $`a>2\sqrt{br}`$. Indeed,

```math
b\delta+\frac r\delta\geq2\sqrt{br},
```

with equality at $`\delta_{\mathrm{opt}}=\sqrt{r/b}`$. Equivalently, multiplying the strict inequality by $`\delta>0`$ gives $`b\delta^2-a\delta+r\lt{}0`$. Under $`a>2\sqrt{br}`$, its two positive roots and the admissible interval are

```math
\delta_\pm=\frac{a\pm\sqrt{a^2-4br}}{2b},
\qquad
\delta_-\lt{}\delta\lt{}\delta_+.
```

The radius $`\delta_{\mathrm{opt}}`$ minimises the left-hand side; it is not the smallest permitted radius. At $`a=2\sqrt{br}`$ the strict margin vanishes, so this argument supplies no strict barrier. That failure is not a proof that an actual trajectory escapes. Any further admissibility restriction must be intersected with the displayed open interval. A usable radius must also satisfy the initial condition $`E(0)\lt{}\delta`$. [FORM, Theorem 10.2 and Corollary 10.3][FORM]

The degenerate cases are also explicit. With $`r=0`$ and $`b>0`$, the allowed radii are $`0\lt{}\delta\lt{}a/b`$. With $`b=0`$ and $`r>0`$, they are $`\delta>r/a`$. With $`b=r=0`$, every positive admissible radius works. A persistent nonzero residual therefore prevents arbitrarily small radii from satisfying this certificate. For the source's abstract example $`a=3,b=r=1`$, the choice $`\delta=1`$ leaves strict margin $`1`$; with $`a=b=r=1`$ no positive radius works. These are illustrative constants, not estimates for a measured device or a fluid solution. [FORM, “Residuals impose a nonzero error scale”][FORM]

#### An exceptional region needs a concentration bound

Suppose a contribution to a low-order estimate obeys

```math
Q(f)\leq-aX+(a+b)M_B,
\qquad a>0,\quad b\geq0,
```

where $`X,Y,M_B\geq0`$ and $`M_B`$ measures the contribution concentrated in an exceptional region. An additional bound with $`m_0,m_1\geq0`$,

```math
M_B\leq m_0X+m_1Y,
```

immediately gives

```math
Q(f)\leq-\alpha X+\beta Y,
\qquad
\alpha=a-(a+b)m_0,
\quad \beta=(a+b)m_1.
```

This follows by substitution and collection of coefficients. The resulting low-order damping is positive only if $`a>(a+b)m_0`$. If $`\tfrac12\dot X\leq Q(f)`$ actually holds and there is also an estimate $`\tfrac12\dot Y\leq cX-dY`$ with $`c\geq0,d>0`$, the preceding weighted argument applies when $`\alpha>0`$ and

```math
\bigl[a-(a+b)m_0\bigr]d
>(a+b)m_1c.
```

This last condition is the direct composition of the source's local-loss substitution and two-level criterion. It exposes the quantitative dependency between concentration control and compensating damping; it does not infer either estimate from the label “exceptional.” [FORM, Theorem 10.1 and Proposition 10.4][FORM]

Region size alone cannot supply the needed bound in an unrestricted $`L^2`$ class. For any measurable region $`B`$ of positive finite Lebesgue measure,

```math
f=\frac{\mathbf1_B}{\sqrt{|B|}}
\quad\Longrightarrow\quad
\|f\|_2^2=\int_B|f|^2=1.
```

All the mass is concentrated in $`B`$, however small its measure. Additional regularity or a justified higher-norm estimate may restrict concentration, but that restriction must be supplied quantitatively. A small count of unresolved issues likewise does not establish a concentration law for an epistemic risk functional. [FORM, Proposition 10.4][FORM]

#### Retaining the trajectory, scale and clock

The strict barrier controls an existing trajectory. It does not itself extend the trajectory or identify the controlled error with the whole state. For a finite-dimensional autonomous equation $`\dot z=F(z)`$ with $`F`$ locally Lipschitz on an open domain $`U`$, remaining in one compact set $`K\subset U`$ supplies a separate continuation argument: if a maximal forward time were finite, boundedness of $`F`$ on $`K`$ would make the trajectory Cauchy as that time approached. Its limit would lie in $`K`$, and local existence there would extend the solution. An error bound around an unbounded reference, a bound near an excluded domain boundary, or an infinite-dimensional estimate need not provide these hypotheses. [FORM, “Continuation is separate from invariance”][FORM]

Even a constant normalised profile can conceal growth in the original state and clock. For

```math
\dot x=x^2,\qquad x(0)=x_0>0,
```

separation of variables gives

```math
x(t)=\frac{x_0}{1-x_0t},
\qquad 0\leq t\lt{}1/x_0.
```

Set $`s=-\log(1-x_0t)`$ and $`\widehat x=e^{-s}x/x_0`$. Direct substitution yields

```math
\widehat x(s)=1\quad(s\geq0),
\qquad
t(s)=\frac{1-e^{-s}}{x_0}\longrightarrow\frac1{x_0}.
```

The rescaled profile remains constant for every rescaled time, while the original variable becomes unbounded at finite original time. This does not contradict compact containment of the original state in its original dynamical domain: that containment is absent. A conclusion about the physical process must retain the reconstruction scale and clock as well as the normalised profile. [FORM, Counterexample 10.8][FORM]

For the communication problem of §5.2, a controlled energy or error radius becomes useful only through a justified bound on the measured output and a separation margin between selectable experiments. For a sequence of operations, invariance also leaves open whether a permitted successor exists and whether the target is eventually reached. These analytic arguments establish no physical implementation, numerical concentration law for inquiry, or permission to offset a violated hard constraint with a better value elsewhere. They provide conditional mechanisms for controlling a declared dynamical discrepancy. [FORM]

### 5.6 Transient amplification and transport of a stability claim

A component can be amplified for a time even when its background influence decays. A bound proved for one model also needs additional uniform premises before it controls a family of models. The formalisation source separates these questions from the strict damping and barrier results of §5.5. [FORM, §10][FORM]

#### An exact transient-amplification calculation

Consider the declared scalar system

```math
\dot b=-\lambda b,
\qquad
\dot f=(-d+\kappa b)f,
\qquad b(0)=B>0,
\quad \lambda,d,\kappa>0.
```

The first equation gives $`b(t)=Be^{-\lambda t}`$. Substitution into the second and integration give

```math
f(t)=f(0)\exp\!\left[-dt+
       \frac{\kappa B}{\lambda}(1-e^{-\lambda t})\right].
```

For $`f(0)\ne0`$, the logarithmic derivative of its magnitude is $`-d+\kappa Be^{-\lambda t}`$. If $`\kappa B>d`$, it is initially positive and changes sign once, at

```math
t_{\mathrm{peak}}=\frac1\lambda\log\frac{\kappa B}{d}.
```

The magnitude grows until that time and then decays to zero, since the positive term in the exponent remains bounded while $`-dt`$ tends to minus infinity. If $`\kappa B\leq d`$, the magnitude is nonincreasing from the start; if $`f(0)=0`$, it stays zero. This is finite transient amplification in an explicitly solved two-component model. It establishes neither an infinite cross-scale cascade nor finite-time blowup. Its variables, gains and timescale interpretation must be identified before it describes a physical or epistemic system; frequency, update time and inquiry level are not interchangeable labels. [FORM, “Fast/slow coupling and amplification”][FORM]

#### A common barrier for a model family

Let $`\theta\in[0,1]`$ index models whose errors satisfy the boundary-valid differential inequality of §5.5 with constants $`a_\theta>0`$ and $`b_\theta,r_\theta\geq0`$. Suppose one radius $`\delta>0`$ is admissible for every member, their initial errors are below that radius, and a common $`\gamma>0`$ satisfies

```math
a_\theta-b_\theta\delta-\frac{r_\theta}{\delta}
 \geq\gamma
\qquad(\theta\in[0,1]).
```

At a first contact with $`E_\theta=\delta`$, the same calculation gives $`\tfrac12(E_\theta^2)'\leq-\delta^2\gamma\lt{}0`$, contradicting first contact. The same radius therefore works for every family member while its trajectory and estimates exist. This is a uniform version of the existing barrier proof; it does not create a common existence time, a continuous branch of profiles, an invertible linearisation or convergence at an endpoint. [FORM, Proposition 10.9][FORM]

The elementary family

```math
\dot x=-(1-2\theta)x,
\qquad
x(t)=e^{(2\theta-1)t}x(0)
```

shows the missing premise. Nonzero solutions decay for $`\theta\lt{}1/2`$, remain constant at $`\theta=1/2`$ and grow for $`\theta>1/2`$. Solving or stabilising the first endpoint supplies no uniform positive damping margin for the family. Removing forcing, adding viscosity or changing an experimental regime likewise needs the relevant model-specific estimates; introducing a parameter alone does not transport the result.

#### The property certified by an approximation

The finite-horizon output bound of §5.2 is one instance of a general property-specific margin calculation. Let $`g:X\to\mathbb R`$ be $`K`$-Lipschitz on a metric space, with $`K\geq0`$. Suppose the actual target $`x`$ and an explicit surrogate $`s`$ satisfy $`d(x,s)\leq\varepsilon`$, and a certified evaluation gives $`g(s)\geq m-\eta`$, with $`\varepsilon,\eta\geq0`$. Then

```math
g(x)\geq g(s)-K\,d(x,s)
      \geq m-\eta-K\varepsilon.
```

In particular, $`g(x)>0`$ follows from $`m>\eta+K\varepsilon`$. The first inequality is the Lipschitz condition and the second substitutes the certified bounds. Small representation error alone does not preserve an arbitrary predicate: even the sign of a real coordinate can change across an arbitrarily small neighbourhood of zero when no positive margin is present. [FORM, Proposition 9.2][FORM]

The claim and its target determine which bridge is needed. As in §5.4, a search procedure may propose a candidate, a spline may become the explicit reference on which residuals and constants are certified, and a separate theorem may establish a true solution near that reference. Certification can bypass the original search object once the reference is fixed. A claim about that original object instead requires its own matched bound. A derivation conditional on hypotheses and certificates establishing those hypotheses for the actual target are both needed for the instantiated conclusion; checked component lemmas do not supply missing application premises. This preserves the source's distinction among numerical discovery, certified reference and target solution, without asserting that its cited Euler or Navier–Stokes programmes have completed their remaining proofs. [FORM, §9][FORM]

Finite flow/reset composition also retains its own scope. The induction in §7.1 applies once each continuous segment preserves its declared safe set and each enabled reset sends its safe guard into the successor safe set; §8.1 gives an explicit nonvacuous example. To cover every finite physical time, an execution must additionally exclude unhandled accumulation of infinitely many events or provide an admissible continuation there. The finite-degree history example in [Tensor Moments, §1.4](tensor-moments-and-corrective-dynamics.md#14-representation-changes-and-future-relevant-reductions) exhibits that boundary. Stability and target correctness remain separate as well: the two attracting signs in §8.1 preserve different logical states, and an application must supply the target and readout that distinguish them. The truth-calibration argument in [Objective Normativity, §7](../foundations/objective-normativity-and-corrective-cognition.md#7-truth-calibrated-revision-on-a-finite-network) makes the corresponding distinction for a correction score. [FORM, Propositions 10.9–10.10 and final stability control][FORM]

## 6. What must cross the boundary

### 6.1 A cut bounds fresh information

Let M be uniform on N ≥ 2 messages and independent of the receiver's prior information S. Let ZΣ be a complete record of all message-dependent influences crossing a declared cut by time T. Assume the conditional Markov relation M → ZΣ → Y given S, where Y includes everything used by the receiver, and suppose

```math
I(M;Z_\Sigma\mid S)\le B(T).
```

If the receiver estimates M with error probability p, then

```math
(1-p)\log_2N-h_2(p)\le B(T),
```

where h₂ is binary entropy.

**Proof.** Let J indicate an estimation error. Conditional on the estimate and J = 0, M is known; conditional on J = 1, at most N − 1 possibilities remain. Thus

```math
H(M\mid Y,S)\le h_2(p)+p\log_2(N-1)
 \le h_2(p)+p\log_2N.
```

Subtract from H(M|S) = log₂N and apply conditional data processing through the complete cut. ∎

If p ≤ ε ≤ 1/2, the weaker but convenient lower bound is obtained by substituting ε. For k fresh independent bits and a cut budget B(T) ≤ CT with C > 0,

```math
T\ge
\max\!\left(0,\frac{k(1-\varepsilon)-h_2(\varepsilon)}{C}\right).
```

For k = 64, ε = 0.01 and C = 2 bits per unit time, this is about 31.6396 time units. It is a necessary information bound, not a protocol or an attainable rate. It is also separate from the scalar control example: that example did not establish a two-bit-per-unit-time stochastic capacity.

Shared code, a retained checkpoint or previously correlated information can reduce the fresh information required. They must be represented in S, with current validity established. Omitting a second physical path from ZΣ invalidates the cut. Adding individual edge capacities without proving joint feasibility can invalidate B(T). A real protocol also needs framing, synchronisation, error handling and an activation procedure.

### 6.2 A one-bit export can lose a two-step state

Consider the delay kernel

```math
Q=\{0,1\}^2,\qquad
\Delta((b,c),a)=(c,a),\qquad
\Lambda(b,c)=b.
```

Suppose the source and destination are each exact realisations, and a perfect channel transmits E(b,c) = b. Both source states (0,0) and (0,1) produce the same export 0. Under the common next input 0, their required next outputs are respectively 0 and 1. A deterministic destination initialiser receiving only that export must start identically in the two cases, so it cannot continue both histories correctly.

The missing item is not channel reliability or the destination's ability to execute Δ. It is sufficient information about the particular current state. Transmitting both b and c removes this obstruction for the stated kernel. It does not, by itself, prove correct ordering, activation, deadlines or support independence.

**Proposition 3: the export obstruction.** Suppose two admitted source states yield the same complete export available to a deterministic initialiser, including its relevant retained side information. If a common admitted future input sequence requires different output traces, that initialiser cannot meet the continuation contract for both states.

**Proof.** The equal complete exports produce the same initial destination state. The same inputs then produce the same destination trace by determinism. This single trace cannot equal both different required traces. ∎

Calling a transfer “state preserving” therefore requires specifying what the export contains, what the receiver already knows and which distinctions affect future behaviour. Copying only current output is generally inadequate.

### 6.3 A minimum for a finite continuation contract

The obstruction has a positive converse at the level of a finite abstract interface. Assume a nonempty finite forward-closed set Qₐ of admitted logical states, a total deterministic kernel, and all finite future input words admitted. Define q ∼ q′ when their output traces agree for every such word, including the current output. Let s(q) be side information known to both the exporter and receiver. For each attained side-information value s, let nₛ be the number of ∼ classes intersecting its state fibre.

Assume the destination has an admissible initialisable representative of every required behavioural class. Ignore physical coding and initialisation costs temporarily, but count the fresh message alphabet.

**Proposition 4: minimum fresh export alphabet.** Exact behavioural continuation is possible with a fresh export alphabet of size

```math
M_*=\max_s n_s,
```

and no smaller alphabet suffices in the worst case. Hence a fixed-length binary export requires exactly ⌈log₂M*⌉ bits at this abstract interface.

**Proof.** If a side-information fibre contains more behavioural classes than available message symbols, two different classes receive the same symbol. With identical s, Proposition 3 excludes exact continuation. This proves the lower bound.

For the upper bound, choose distinct labels for the classes within each fibre using at most M* symbols. The encoder sends the symbol for the actual class. Knowing s, the receiver identifies that class and initialises its stipulated destination representative. By the definition of ∼, every future trace agrees. The symbol can be reused for a different class in a different fibre because s disambiguates it. ∎

This is the deterministic continuation specialisation of the task-relative finite partition principle in [Information and Inquiry](information-and-inquiry.md), section 9.1. It is not a theorem that abstract bits can be transmitted or written for free. The encoders and class initialisers must subsequently satisfy the physical resource, access and deadline contract. Under restricted histories, a horizon or version-dependent admission rule, the state must include the relevant history summary, remaining time or version, or the equivalence must be redefined accordingly.

For the delay kernel, all four states are distinct under ∼. With no retained side information, two bits are necessary and abstractly sufficient. If the receiver already knows the correct current c, each side-information fibre has only two classes, so one fresh bit b suffices. A stale c does not meet that premise. For parity, only the accumulated parity bit, rather than the full input history, distinguishes future behaviour.

When the input alphabet is finite, the transition and output tables are effectively available, and output equality is decidable, the finite equivalence can be computed by partition refinement. Begin by separating states with different current outputs. Repeatedly split a block whenever some input sends two of its states into different current blocks. Finite termination yields a stable partition. Stability proves identical future traces by induction. Conversely, each split is justified by a finite distinguishing word: prepend the splitting input to a word distinguishing the successor blocks. The resulting partition is exactly ∼. This procedure uses common future inputs; it should not be confused with an input-insensitivity test that compares different inputs against one another. A larger input family needs its own effective decision procedure for the refinement conditions. Finite Q alone is insufficient: with natural-number inputs n, a transition can depend on whether a fixed program halts within n simulated steps. Deciding that two finite states agree for every input would then decide nonhalting. This algorithmic limit does not invalidate the abstract minimum-alphabet existence theorem.

### 6.4 Information and precision consequences of the quotient

Choose N behavioural classes within a single side-information fibre and sample one representative of each uniformly. If a transfer must initialise the correct class with error at most ε, and the receiving realisation has the declared class readout, the cut bound applies to that class variable. It gives a lower bound using log₂N, not the size of an unexamined parameter file. This experiment establishes a worst-case task requirement under the chosen challenge distribution. It does not replace an actual nonuniform workload distribution with a uniform one without saying so.

There is a corresponding finite-dimensional precision bound. Suppose N distinct required classes are represented by points in a radius-R ball in Euclidean dimension d ≥ 1. Suppose the same decoder must identify the class after every perturbation in a closed radius-ζ ball, where ζ > 0, with no uncounted side information. Distinct class centres must be more than 2ζ apart. Their radius-ζ balls are disjoint and lie in a radius-(R + ζ) ball. Comparing volumes gives

```math
N\le\left(1+\frac R\zeta\right)^d.
```

This proof also explains its scope. The representation region, norm, perturbation set, time of readout and external memory have been fixed. A sequential encoding, a different geometry, additional state or side information changes the premises. The bound is not a universal limit on matter or on all analogue computation.

Together, the quotient, cut and packing arguments identify three different questions: which distinctions the task actually requires; how much new information must arrive; and whether a specified noisy physical representation can retain those distinctions. A smaller sufficient quotient can improve both communication and storage demands, but it does not establish its own efficient computation or robust implementation.

### 6.5 Continuing source context without confusing source and carrier

A continuation can preserve proposition strings while losing the context that makes a selected occurrence an author's assertion, quotation, reported objection or hypothetical premise. The open-fragment construction addresses one precise decision: whether every selected output occurrence belongs to the original witnessed document's unquoted authorial argumentative voice. It does not decide the truth of those propositions or the present carrier's endorsement. An original authorial assertion can remain a quotation in its new carrier; copying it creates no new assertion or grant. [N250-161] [N250-163]

Let an original-context key include a source snapshot and a particular context occurrence. Equal text does not identify keys, whereas copies of one original context retain that key. A source-justified stack machine has operations enter(o), leave and emit(t), with the current context first and suspended parents afterward. An open fragment may begin or end inside a scope. Give its incoming frames symbolic references I₀,I₁,… and compile its effect into E=(h,P,k,M): the least admitted entry depth h, a finite literal prefix P, consumed incoming-frame count k, and selected emission references M. On an admitted entry stack s, the outgoing stack is P followed by s[k:]. Generated effects satisfy h≥k+1, so the original incoming tail never disappears through an invalid empty configuration. [N250-161] [N250-162]

Initially h=1, P is empty and k=0. Enter prepends its key. Leave removes a literal prefix key when present; otherwise it increments k and raises h to at least k+1. A selected emission records P's first key, or I_k when P is empty. Induction on the operations proves that substituting the actual incoming keys gives exactly the ordinary stack execution. It also proves that h is one minus the minimum prefix net height, counting the empty prefix. Net final height alone is insufficient: leave followed by enter consumes an incoming frame even though the net change is zero. [N250-162] [N250-168]

For f followed by g, put p_f=|P_f| and δ_f=p_f−k_f. Substitute each second-fragment reference I_j by P_f[j] when j<p_f and by I_(k_f+j−p_f) otherwise. The exact entry depth is max(h_f,h_g−δ_f). If k_g<p_f, the outgoing prefix is P_g followed by P_f[k_g:], with consumption k_f; otherwise the prefix is P_g and consumption is k_f+k_g−p_f. Concatenating the first emissions with the substituted second emissions gives the composed effect. These are the exact entry-domain and output formulas, so composition agrees with concatenation and is associative. Output occurrence identifiers must be fresh across fragments. Optional keyed exits add source-key equality constraints: a close marker from a different snapshot is not made valid by having the right depth. [N250-162] [N250-168]

The source-to-boundary identity map is a separate premise. A retained I₂ is not yet evidence identifying its original context. Once justified maps resolve the selected emissions, collapse only shared original keys. After removing roles already witnessed positive, the remaining decision is the conjunction of the unresolved original-role bits on a finite set L; any known negative terminates it immediately. A suspended frame matters only if this continuation actually emits after returning to it. Under independently live role assignments, omitting a key in L changes the decision on an admitted input, while unconsulted frames need not be retained for this particular task. Correlated source evidence or a valid task-specific verdict can reduce the demand. [N250-161] [N250-163]

### 6.6 Exact reacquisition cost depends on the surviving read service

Let W be a finite menu of genuinely permitted, adequate role-witness reads, with positive additive costs c(w) and justified origin coverage C(w). Assume a pinned-snapshot task, an admitted all-positive assignment, and, for every unresolved o∈L, an admitted alternative changing only that relevant bit to zero. Every read not covering o must have the same complete observable response in the two cases, up to permitted renaming of opaque handles. This includes contextual material, outside labels, metadata, status, length and observable timing. The policy’s initial holdings and public metadata must also agree across each star pair, up to that same renaming; no uncounted informative channel is available. Reads claiming to cover a key must actually determine its role. Locality and this sufficiency requirement are distinct: a constant response claiming all keys satisfies the locality condition vacuously but supplies no roles. [N250-161] [N250-163] [N250-170]

Under these premises, the minimum worst-case cost of a deterministic adaptive policy completing the conjunction is exactly the minimum cost of a read family covering L. Follow a correct policy on the all-positive assignment. If it stops before covering o, the corresponding one-negative source gives the same entire transcript but requires the opposite answer. Thus its positive path must be a cover. Conversely, read a minimum cover, returning false at a witnessed negative and true when all demanded roles have been acquired. Negative instances can be cheaper; sound abstention is not completion of the stipulated decision. No-cover means that this interface cannot complete the task, not that every possible source service fails. [N250-161]

The all-positive-star condition is stronger than independence of the target bits alone. An outside observed value equal to their conjunction can decide the task without reading those keys. Public names, a label-dependent retention choice or a content lookup can likewise disclose uncounted information. The synthetic realization uses sibling source contexts with equal-width role tokens, fixed scope shape and assignment-independent metadata; copies share their original roles. Its different assignments are different source bytes, not conflicting contents attributed to one immutable digest. The opaque-handle assumption restricts the mathematical API rather than proving a cryptographic implementation. [N250-163] [N250-165]

If adequate read coverage is convex in the original source order, first sort the distinct demanded positions ℓ₁<⋯<ℓ_m. Reordering or duplicating output occurrences cannot make an original-source interval skip an intermediate demanded position. With F(m+1)=0, the exact weighted recurrence is

```math
F(i)=\min_{w:\,\ell_i\in C(w)}\bigl(c(w)+F(1+r(w))\bigr),
```

where r(w) is the last demanded position covered by w; an empty choice has infinite cost. A window covers the whole demanded suffix segment from i through r(w). Conversely, choose the furthest-reaching window covering i in any optimal cover; the remaining windows cover the suffix after its endpoint. This proves the recurrence by suffix induction. After coverage endpoints are known, its table uses O(m|W|) candidate work and O(m) cost storage. Furthest-right greedy selection applies to unit costs, not arbitrary weights. Raw contiguous text is not automatically an adequate convex role-witness service: an omitted outer quotation opening may leave a gap in justified role coverage. [N250-161] [N250-163]

A genuinely different service offering only whole source-backed cards can realize arbitrary weighted set cover. A card contains adequate context-witness records for its listed origins; the read menu permits only the whole card and no surviving cheaper source route. One origin per universe element and one card per set give exactly the covering instance. The construction charges the source contexts, all transclusion records, identity dictionary and card boundaries. Unit request cost is not constant byte cost; equal-width padding gives a separate polynomial equal-response-length construction. Copying alone does not cause this change in complexity. The change is in the permitted access service, and an actually available whole-source read, singleton access or valid carried verdict must be counted. [N250-161] [N250-165]

The supplied checker implements the effect algebra, an exponential subset-cover solver capped at 20 keys, the interval recurrence, and an independent finite observation-tree optimizer capped at 256 worlds and 24 windows. Its locality and response-fibre sufficiency checks are separate. The source includes conventional-stack comparisons, finite exhaustive cases, explicit wrong-interface controls and source-linked analytical fixtures. Reading those programs is not a new execution of them, and their fixture checks do not establish natural-language interpretation, authentication or permission. The mathematical contribution is the bounded chain from open source context to a task's exact evidence demand and access geometry, using established parsing, query and covering methods. General novelty or superiority over an equally informed conventional implementation is not claimed. [N250-164] [N250-167] [N250-168] [N250-169] [N250-170] [N250-171] [N250-172] [N250-173]

#### Keyed-exit and acquisition contract details

The keyed-exit refinement retains a finite conjunction C of original-key equalities as well as the depth condition. Exiting a literal top a at key o requires a=o; an unequal pair makes the domain empty. Exiting an incoming reference I_j records I_j=o before the ordinary leave operation. Composition retains C_f together with the second constraint list after the same reference substitution used for the emissions. Contradictory literal equalities, or two unequal required keys for one incoming slot, make the composite domain empty. On nonempty domains the depth formula above is unchanged. In the suffix exit(f); exit(p); emit(z), these checks bind I₀=f and I₁=p while z still refers to I₂. They cannot manufacture the missing I₂-to-original-key map. The induction and composition are ordinary symbolic proofs over a source-justified scope skeleton, not an authentication protocol or an algorithm for interpreting arbitrary quotation boundaries. [N250-162]


Two occurrence maps must therefore remain distinct: output occurrence to original source occurrence, context and role; and output occurrence to its present carrier occurrence, context and force. A source author quoted inside an opponent's reported speech does not regain original-document authorial force merely because the local speaker's name matches the author. Conversely, an original authorial assertion may now occur only as a quotation. The source-stack calculation answers the first question; endorsement by the present carrier requires its own justified interpretation. The model recipient's neutral lookup keys also do not erase information that an actual reader already has: recognizable passages, informative locators, available full-source context and valid task-specific verdicts must be credited in that reader's observation contract. [N250-163]


If a fixed boundary-acquisition protocol costs c₀ and also reveals roles on K, a completing plan costs c₀ plus the minimum permitted cover of L minus K, unless a relevant acquired negative already terminates the decision. The cover optimum is exact for the second phase conditional on its actual holdings; their sum is not asserted optimal among all joint identity-and-role acquisition protocols. The source case's first observation supplies both I₂-to-a identity and a's role, so it is a combined observation rather than an instance of the label-only oracle. Constructing and preserving the lookup dictionary, role-bearing metadata and path witnesses remains charged work for both this method and an equally informed conventional comparison. The enter/leave/emit calculus does not reconstruct arbitrary reply-to-objection edges; a separate justified encoding would be needed for that task. [N250-163]


#### A bounded release decision separates care from capacity

For the synthetic original-key demand {a,b,c}, suppose the surviving permitted services reveal {a,b} or {b,c} at unit cost. With complete local observations, total exact decision of their conjunction takes two requests in the worst case. Carrying an independently fixed endpoint a or c reduces that cost to one; carrying the middle b does not. A retained relevant negative, a warranted fixed-query verdict or an agreed label-dependent selector encoding that verdict can reduce further reads to zero. Restoring the whole-source service gives one. This is a comparison of actual holdings and the remaining menu, not a universal transfer lower bound. Identity acquisition, construction, storage and verification costs are outside the displayed role-request count. Correlated outside holdings, rich responses or informative timing/metadata change the problem. [N250-174] [N250-175] [N250-182]

Now independently suppose an organiser owes proportionate care for a legitimate one-request undertaking, knows the exposure, can provide an adequate permitted alternative, and has no undefeated reason excusing omission. Selecting only the inadequate middle-witness arrangement while withholding every fitting precaution then violates that care requirement. The mathematical gap identifies which plans meet the fixed undertaking; it does not generate the duty or require one specific representation. Budget renegotiation, a usable live reader, a suitable verdict, informed refusal or fitting withdrawal may change the conclusion. Lucky success, high prior accuracy and bounded-error policies are not total zero-error completion; a fixed-query verdict also need not answer every individual role or future query. The historical independent review reports 48 explicit finite checks normally and under optimization, not execution of moral inference. Its checker and the separate stack/cover/mutation review sources remain reproducibility dependencies, not redundant prose. No new replay is claimed here. [N250-182] [N250-183] [N250-196] [N250-197] [N250-198] [N250-199]

The actual historical source fixture remains separate from that synthetic comparison. Its source-role annotations and exact original identity do not establish clause-level propositional fidelity or actual service retirement. The later print-collation addendum reports that the English negative reading matches the1920 print while the1888 Latin printing has a positive reading and records a negative variant; this locates the discrepancy before the website without establishing the translators' base or production responsibility. Its independent receipt supports that bounded reported inspection, not a critical edition or new primary-source access in this consolidation. [N250-180] [N250-205]

The public reproducibility route separates finite model replay from historical source replay. The full historical wrapper depends on two excluded primary captures and is not a self-contained public replay. Supplied source annotations and their checks cannot substitute for those missing inputs; no full historical replay is claimed. [N250-146]

## 7. Exact and approximate continuation

### 7.1 The exact induction

Let r and s be realisations of the same kernel. A migration map μᵣₛ from admitted source states into admitted destination states is exact when

```math
\rho_s(\mu_{rs}(x))=\rho_r(x).
```

Continuation-relevant pending inputs, externally visible effects already committed or still pending, membership and replay-prevention metadata must be included in Q or in an explicit separate interface contract with its own preserved state and obligations. Equality of a reduced computational state alone does not establish that an external effect was committed exactly once.

Suppose every execution step satisfies the transition and output equations of section 2, every migration satisfies this equation, and all intermediate states remain admitted. Suppose accepted inputs are neither lost nor duplicated and are processed in the same order as the reference execution. Every step must also preserve any separate effect/interface contract just specified.

**Proposition 5.** Every finite sequence of such execution and migration operations produces the reference logical state and outputs at its declared observation interfaces and retains the stipulated separate effect/interface obligations. Execution steps advance the reference kernel; pure migrations leave its logical state unchanged.

**Proof.** Initially the decoded and reference states agree. An execution step preserves agreement by the transition equation. A migration preserves it by its own equation. Induction over the mixed sequence proves state agreement; the output equation then proves output agreement. Any separate interface obligations are retained by their assumed stepwise preservation, so a replay or lost pending effect is excluded by that contract rather than by the reduced-state equation alone. ∎

The theorem is positive even when the successive physical states use unrelated coordinates. It also isolates the obligations often hidden by the word “migration”: admitted preparation, sufficient export, a correct initialiser, ordered inputs, retained output semantics and a real interface boundary.

Latency is not proved by this induction. A migration can preserve state while taking too long. If service continuity requires a deadline, the complete sequence must meet it. A finite handover log can record the last accepted input index and the active successor, but the log's storage, trust and availability belong in the contract.

A small coordinate example uses Q = ℤ/7ℤ with Δ(q,a) = q + a modulo 7. One implementation stores q; another stores 3q + 1 modulo 7 and decodes with 5(x − 1) modulo 7. Since 3·5 = 1 modulo 7, the conjugated update and migration preserve every state and input exactly. This is an explicit finite witness of coordinate substitution, not a physical implementation of the encoding.

A four-acquisition frame gives a concrete pointwise interface. Suppose every core state q and every four-bit input block w carry a certificate that the machine ends at the represented successor on w₀ and emits the entire prescribed ordered four-output word. Then, on every infinite input tape, its boundary state after 4n acquisitions is the represented core state driven by x₀,x₄,x₈,…, and output 4n+j is the prescribed jth frame output. The three ignored input bits and stalled or null tapes are still covered. Finiteness and fairness are unnecessary for this conditional identity; matching marginal laws or only the final state would not supply its two-part certificate. [C250-086]

[C250-086]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/923326671c48bf359f4285b61010e91a0fbaac7ca90a8e6f7234326ad935d250.lean


### 7.2 Defects accumulate according to the reference dynamics

Let the reference transition at step n be Fₙ, Lipschitz with constant Lₙ in the declared state metric. Let the decoded physical step have defect at most ηₙ from applying Fₙ to its own decoded current state. If eₙ is its discrepancy from the reference state, then

```math
e_{n+1}\le L_ne_n+\eta_n.
```

The triangle inequality gives this one-step bound. Repeated substitution gives

```math
e_N\le
\left(\prod_{i=0}^{N-1}L_i\right)e_0
+
\sum_{j=0}^{N-1}
 \eta_j\prod_{i=j+1}^{N-1}L_i,
```

where an empty product is one. For uniform L and η this becomes

```math
e_N\le L^Ne_0+\eta\sum_{j=0}^{N-1}L^j.
```

If L < 1, the contribution from repeated defects is bounded by η/(1 − L); if L = 1 the upper bound is e₀ + Nη; if L > 1 the bound permits amplification. The last case does not prove that actual errors grow. Exact trajectories can coincide forever under the expansive map q ↦ 2q when e₀ = 0 and the actual defects vanish. A positive upper bound η does not assert a positive realised defect.

For a pure migration, the reference map is the identity, so its relevant Lipschitz constant is one. A contracting execution step cannot be assigned to a migration merely to make the accumulated bound smaller. The actual order of execution and transfer matters.

A state bound implies an output bound only through a justified output relation, such as a Lipschitz output map or a decoding margin. Different state metrics can make different aspects easy to certify; they do not change the declared output obligation. This is one reason exact bit preservation can coexist with continuous physical perturbations in section 8.

### 7.3 Output distributions and common histories

For a stochastic output contract on a finite alphabet, suppose 0 ≤ αₜ ≤ 1 and the two systems' next-output distributions have total variation distance at most αₜ for every common history at time t. Then the laws of their length-H output traces satisfy

```math
\mathrm{TV}(P_{1:H},Q_{1:H})
\le 1-\prod_{t=1}^H(1-\alpha_t)
\le\sum_{t=1}^H\alpha_t.
```

**Proof.** Couple the two processes sequentially. While their histories agree, use a maximal coupling of the conditional next-output laws. Its conditional mismatch probability is at most αₜ. Thus the probability that they remain equal throughout is at least the displayed product. Once histories differ, use any coupling. Total variation is bounded by the disagreement probability of this coupling. The second inequality follows by expanding, or inducting on, the product. ∎

The interval restriction matters: for opposite deterministic length-two traces, actual TV is one, while inserting the loose upper bounds α₁ = α₂ = 2 would give the invalid product bound zero. A valid nonnegative bound above one can first be clipped at one. The common-history premise is stronger than a small average benchmark loss. It must hold on the histories reached while the traces remain coupled, including contexts that may be rare in a test set. Conversely, two independent samples from identical distributions need not match; sample inequality is not a violation of a distributional contract.

The stochastic transfer results in [Collective Inquiry and Strategic Coordination](collective-inquiry-and-strategic-coordination.md), sections 7.5–7.6, additionally track full joint laws, private/public interface modes, admissible controller memory and initial distributions. The finite-horizon trace bound here does not imply the eventual-occupancy or persistence claims developed there. It supplies a different, explicitly finite error account.

A finite cap contract can supply a sharp row-diameter bound. Let C=Σ_i c_i≥1 with c_i≥0, and let P_c={p:0≤p_i≤c_i, Σ_i p_i=1}. For a subset S put a=Σ_{i∈S}c_i and b=C−a. The largest and smallest possible masses of S are min(1,a) and max(0,1−b), attained by allocating proportionally to the caps on S and its complement, with zero-cap blocks handled separately. Since total variation on a finite alphabet is the maximum subset-mass difference, diam_TV(P_c)=max_S min(1,C−1,a,b). In particular it equals one exactly when some split has a≥1 and b≥1. Such a split supplies disjoint capped laws p,q; assigning row p on S and row q on its complement makes both stationary. Total capacity two alone does not force that split: c=(9/10,9/10,1/5) has diameter 9/10, so every pair of rows obeying these caps is strictly closer than one. This finite cap calculation is distinct from a full-history or eventual-restoration guarantee. The source’s dyadic-prefix controls also retain an explicit omitted-tail allowance, but its finite loops do not establish effective maximizing-partition choice for arbitrary countable caps. No checker execution is claimed. [QM-169](../research/t20-v6-20261012/sources/19eb1ee268f5d194f7223828ba9603b5d75208a5ed6239a2080d5670f3366cc6/diameter_checks.py#L6-L39)


<a id="nonuniform-compact-continuation"></a>

### 7.4 Nonuniform compact continuation at a fixed observation time

A continuation can use different state spaces and maps at successive stages. The compact-completion guides explicitly retain that nonuniform interface: they do not add a common state space, stationary transition, common fixed point, time-uniform bound, rate, or inference from an observer's record to an entire hidden state. The elementary compactness argument below states the positive mechanism with its quantifiers. [GUIDE105-G075] [GUIDE105-G091]

Let $X_n$ be nonempty compact Hausdorff spaces and let $f_n:X_{n+1}\to X_n$ be continuous. For $m\ge n$, let $f_{n,m}$ be the finite composite, with $f_{n,n}$ the identity, and define

```math
K_{n,m}=f_{n,m}(X_m),\qquad K_n=\bigcap_{m\ge n}K_{n,m}.
```

The sets $K_{n,m}$ are nonempty compact and nested in $m$, so each $K_n$ is nonempty. Let $L$ be the set of compatible sequences satisfying $f_n(x_{n+1})=x_n$ for every $n$. Then

```math
\pi_n(L)=K_n.
```

**Proof.** Every compatible sequence projects into every finite-horizon image, giving one inclusion. Conversely, fix $x\in K_n$. For any finite horizon $m\ge n$, choose $y\in X_m$ with $f_{n,m}(y)=x$ and propagate it backwards to obtain a compatible prefix. Such prefixes show the finite intersection property for the closed compatibility conditions together with $x_n=x$ in the compact product $\prod_jX_j$. Compactness gives a full compatible sequence. The equality follows. This argument also proves nonemptiness of $L$. ∎

If the $X_n$ are compact metric spaces, then for each fixed $n$,

```math
\lim_{m\to\infty}\operatorname{diam}(K_{n,m})
=\operatorname{diam}(K_n).
```

The left-hand side exists because the diameters decrease. To prove the nontrivial inequality, choose pairs attaining the diameters in a sequence of $K_{n,m}$ and take a convergent subsequence in $X_n\times X_n$. Nestedness puts both limit points in every $K_{n,m}$, hence in $K_n$, and continuity of distance gives the limiting diameter. It follows that a unique compatible full sequence, singleton $K_n$ for every $n$, and diameter decay at every fixed observation time are equivalent. Equivalently, for each fixed $n$ and $\varepsilon>0$, some sufficiently late horizon makes all its projected states within $\varepsilon$ of one another.

The order of those quantifiers matters. Take $X_n=[0,1]$ and $f_n(x)=a_nx$, where $a_n=1/2$ at powers of two and $a_n=1$ otherwise. For each fixed $n$, infinitely many later halvings force $K_n=\{0\}$ and the diameters tend to zero. But there are arbitrarily long identity blocks. For any fixed lookahead length, some starting stage has diameter one throughout that lookahead. Thus pointwise fixed-stage forgetting supplies no uniform lookahead over all starting stages. This elementary illustration does not assert that the guides' formal modules contain this exact example.

The guides assign general algebraic and metric implications, compact-continuous equivalence, and two bounded countercontrols to separate formal components. Another control and the philosophical or source-domain conclusions remain ordinary-only. The full checked source closures are not supplied by these short guides, so their historical validation records are not fresh kernel proofs here. The argument above is the ordinary compact inverse-system argument under explicitly stated hypotheses. It does not establish an actual physical realization, a computational rate, or persistence of a person through replacement. [GUIDE105-G075] [GUIDE105-G091]


### 7.5 Finite survival, exact realization and effective queries

Compactness in §7.4 is a substantive bridge, not a synonym for completeness, boundedness or convergence along each forward orbit. The following controls separate the bridge's conclusions and the information needed to turn them into effective decisions. They also distinguish a sufficient strict-query certificate from a proof of an exact limiting equality.

#### Compatibility cannot be replaced by separately chosen predecessors

Consider the discrete metric space with states e,r and b(n,k) for natural numbers k≤n, distance one between different states. Define f(e)=e, f(r)=e, f(b(n,0))=r and f(b(n,k+1))=b(n,k). This infinite space is complete: a Cauchy sequence is eventually constant. It is bounded by one and every map from it is continuous. Yet its finite-depth survival set is exactly {e,r}. The point e is fixed, and r has a predecessor at every depth t+1, namely b(t,t). No branch point b(n,k) survives all depths: a depth-t predecessor would require k+t≤n. In a compatible infinite backward sequence, every coordinate must survive. The successor coordinate is therefore e or r, and both map to e; consequently every coordinate is e. There is exactly one full backward realization, while there are two finite-depth survivors. Every branch point nevertheless reaches e after k+2 forward steps, so every forward orbit converges to e. The missing premise is compactness, not pointwise attraction. [R250-C037]

Two smaller controls identify distinct mistakes. The map f(n)=n+1 on the natural numbers has no compatible infinite backward sequence: compatibility implies b(n)+n=b(0), contradicted at n=b(0)+1. Thus “at most one” is vacuously true but does not establish the source's uniqueness predicate, which includes existence. On Bool with f constantly false, false survives, true is a predecessor of false, and true does not survive even one positive depth. Choosing an arbitrary predecessor of a survivor therefore need not extend a compatible surviving chain. The reviewer source separately retains an imported complete/bounded counterexample to the claimed implication from singleton survival to uniform attraction; its proof uses failure even of pointwise attraction in that imported example. That distinct control is not supplied by the branch construction, whose forward orbits do converge. [R250-C243]


<a id="final189-b12-complete-bounded-control"></a>

The direct stationary counterexample A is stronger than an unspecified failure of uniform attraction. Use Option ℕ with distance0 on equality and1 otherwise; it is infinite, complete and bounded. Let f(none)=none and f(some k)=some(k+1). Every map is continuous for this discrete metric. The depth-n image is {none} together with some k for k≥n, so only none survives every depth. Every compatible infinite backward sequence is therefore constantly none. Yet each forward orbit beginning at some k stays distance1 from none forever, including the start some1 already in the image. The unique fixed point is consequently not even pointwise attracting. Completeness and boundedness cannot replace compactness in the positive repair; the proof uses a genuinely bounded metric, not a zero-diameter convention for an unbounded set. [F189B-873](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/edf93ff8b4991533032505662ff8347ddc1f0d99be6b0e1e00b56f09d1aba198/LawCompletionCounterexample.lean)

#### The positive indexed theorem retains its quantifier order

For the nonempty compact Hausdorff spaces and continuous bonding maps of §7.4, the compact-product finite-intersection argument realizes each finite-depth survivor at its specified coordinate. It needs neither injectivity nor surjectivity of individual maps, a common state space, stationary dynamics nor contraction. In compact metric spaces, the corresponding fixed-finite-horizon forgetting statement is

```math
\forall H\ \forall\varepsilon>0\ \exists N\ \forall j\ge N,
\quad H\le j\ \Longrightarrow\quad
\forall i\le H\ \forall u,v\in X_j,
\quad d_i(f_{i,j}(u),f_{i,j}(v))<\varepsilon.
```

The finite maximum of the coordinatewise thresholds supplies one N after H and ε have been selected. Conversely, choosing H=i recovers each fixed-coordinate statement. The analogous attraction predicate compares each transported value with the compatible coordinate b_i; these values need not be one common fixed point. Compactness and continuity supply closed, bounded finite images, so ordinary real diameters cannot produce a false zero through a convention for unbounded sets. Padding the extension range by all of X_i when j<i merely makes an everywhere-defined decreasing sequence; those finitely many early indices do not change a limit. [R250-C063]

The dated checked-scope report records a clean sequential replay of four Lean4.19 modules and33 theorem dependency readbacks, with standard `propext`, `Classical.choice` and `Quot.sound` only. This is an inherited source-reported result, not a new execution here or an independent acceptance claim. The separate readback file requests the exact dependent-family definitions, finite-composite and projection laws, compatibility and existence statements, and the coordinate/finite-horizon/diameter equivalences. Its commands are not their outputs. In particular, a separately named scalar supremum-of-finite-maxima identity, an effective rate, all-start-time uniformity, observer-quotient interpretation, quantitative Lipschitz corollaries and metaphysical applicability were not established by that packet's checked statement. [R250-C063; R250-C073]

<a id="next250-finite-warrant-proof"></a>

#### Robust finite answers and exact strict witnesses

The finite-warrant addendum supplies a direct bridge from compact survival to a finite answer. Let K₀ contain a decreasing sequence of nonempty compact subsets K_n of a Hausdorff space, and let their intersection S lie in an ambient open set U. If no K_n were contained in U, the nonempty sets K_n minus U would be closed in compact K₀ and would have the finite-intersection property. Their common point would belong to S outside U, a contradiction. Thus some whole finite stage lies in U. Apply this to a fixed coordinate's finite-extension images, or compact images of a fixed finite observation block. The answer need only be constant on an ambient open neighbourhood of all survivors; full state uniqueness is unnecessary, and continuity solely on the survivors is insufficient. Effective upper-compact range presentations and effectively open answer regions give a terminating containment search on robust instances. Plain compactness does not supply effective names, while an additional numerical convergence rate is not required for that represented-input search. [N250-188]

For the half-affine binary family below, put τ=p/d with integer p and positive integer d. The exact range [V_n/2ⁿ,(V_n+1)/2ⁿ] certifies Below precisely when (V_n+1)d<p2ⁿ, and Above when V_nd>p2ⁿ. Each test is sound because it bounds the entire range. Conversely, if the scalar is strictly on one side, choose n with 2⁻ⁿ smaller than its gap from τ; the corresponding range endpoint is then on that side. Searching depths therefore finds a witness for every true strict comparison without being supplied its gap. At equality neither strict test succeeds, and elapsed time or resource refusal is not an equality answer. The program, threshold, scalar interpretation, model/version, recipient and release rule must remain bound to the independently expected request; equality of those records does not establish their worldly truth or authority. The following series and first-halting arguments retain the addendum's separate uniqueness and exact-zero limits, and the later source comparison retains its P02 ownership rather than introducing a new calculus or checker. [N250-188]

#### A uniquely determined, computably approximable state can have an undecidable exact query

For any binary stream b define half-affine maps f_i(x)=(b(i)+x)/2 on [0,1]. The series

```math
y_i=\sum_{r\ge0}\frac{b(i+r)}{2^{r+1}}
```

lies in [0,1] and satisfies y_i=f_i(y_{i+1}). Unwinding n equations for any compatible z gives the same first n terms and a tail z_{i+n}/2^n. The difference from y_i is at most2^−n; letting n grow proves uniqueness at every coordinate. At coordinate zero the exact finite image is [V_n/2^n,(V_n+1)/2^n], where V_0=0 and V_{n+1}=2V_n+b(n). For bits0,1, f_0(f_1(x))=(1+x)/4; reversing the composition changes it. [R250-C152, §§1–2]

The controls give an effective construction of a total unary bounded-loop programme from a valid finite C2-01 two-counter instruction table M into the actual unary P02-L1 AST syntax, using its `set`, `seq`, `if`, expression and bounded `loop` constructors. Registers retain the input n, output, programme counter and its snapshot, two simulated counters, a latched halt bit, loop index and previous halt bit. Initialize the mutable state to zero and perform n+1 bounded iterations. Each iteration saves the previous halt bit; unless halted, it snapshots the programme counter and dispatches exactly the matching finite instruction case. Increment and conditional-decrement cases update the simulated counters and next programme counter; a halt instruction sets the latch. Dispatch tests the unchanged snapshot, so changing the programme counter cannot run another instruction in the same iteration. The output is the new halt bit minus its saved value. Inductively, before each iteration the registers describe that source stage or retain the already latched halt. The final output is one exactly when the first halt stage is n. An initial halt produces1,0,0,…; one increment followed by halt produces0,1,0,…; a nonhalting self-increment loop produces only zeros. Every target evaluation terminates because its loop is bounded; no promise of totality for an arbitrary source-machine simulation is assumed. [R250-C152, §2]

For this generator, x_M is zero if M never halts and2^−(t+1) if its first halt stage is t. The maps remain1/2-Lipschitz and the scalar is uniformly approximable to error2^−n. Nevertheless, under the inherited non-c.e. premise for nonhalting of these valid two-counter tables, there is no uniformly complete sound c.e. acceptance relation for finite certificates of x_M=0. Otherwise enumerate certificates and dovetail their acceptance computations: a certificate would be accepted exactly for the nonhalting tables, semideciding that set. This argument allows arbitrary effective finite invariants, induction and machine proofs, not only finite prefixes. Individual zero cases can have finite proofs, including the constant-zero programme and the self-loop with no halt instruction. They do not make the whole family effectively enumerable; an asserted law or noncomputable oracle is outside the acceptance premise. [R250-C152, §3]

#### Exact controls for the claim being released

The same enclosure supports strict inequalities without deciding equality. The controls below state ordinary mathematical expected outcomes, not executed checker results. [R250-C152, C01–C12]

- For the zero stream and threshold1/4, depth2 has upper bound1/4 and cannot certify strict Below; depth3 has upper bound1/8 and can. A stream with its only one at index3 has scalar1/16 and the same depth3 enclosure [0,1/8]; that enclosure certifies Below1/4 but not zero. The programmes differ, so this is not a claim of full-source indistinguishability.
- The stream01000… has scalar1/4 and reaches that value as its lower endpoint at depth2; using a nonstrict lower test would falsely certify Above1/4. The stream00111… also has scalar1/4 but reaches it as its upper endpoint at depth2; a nonstrict upper test would falsely certify Below1/4. Both directions are needed. For the first stream at threshold3/8, reversing its two-bit prefix produces the false enclosure [1/2,3/4] and a false Above certificate; the correct depth2 enclosure [1/4,1/2] certifies neither side, while its depth4 enclosure [1/4,5/16] certifies Below.
- A constant-one unary programme has scalar1 and depth3 enclosure [7/8,1]. The controls report that the inspected arity-mismatched `evaluate_index` wrapper returns zero for that unary input; using it would fabricate [0,1/8]. The intended evaluator is `run(P,(i,))` with its explicit resource behavior. This is a source-reported interface finding, not a fresh execution here. Natural outputs must be reduced mod2: constant2 yields zero bits and constant3 yields one bits. Raw2/3 entries and a generic nonzero test are not substitutes.
- At depth0 every enclosure is [0,1]. Above holds for a negative threshold and Below for a threshold greater than1; Below0 and Above1 are impossible. Threshold numerators are integers and a zero denominator is malformed. Constant-one at threshold1 and constant-zero at threshold0 never certify either strict side.
- Equivalent rational thresholds1/4 and2/8 have equivalent arithmetic meaning but may differ as literal records; either use the specified literal binding or a separately declared common normal form. Distinct programme ASTs can likewise have identical output streams while making a certificate bound to one stale for the other. Freshly bound requests can still receive the same correct semantic answer. Reject incorrect prefix lengths, non-bits, false V values, malformed syntax, unsupported formats and stale model/version/recipient/rule/comparison fields even when a fabricated interval happens to support a true conclusion.
- A legal total programme can exceed the host's time or bit budget. Resource refusal is neither a numerical answer nor a proof of syntactic invalidity. The mathematical and operational judgments remain distinct.

The general inverse-system claims need equally concrete controls. With X_i={0,1}×[0,1] and f_i(c,x)=(c,x/2), there are two compatible states but the observable x has depth3 range [0,1/8], sufficient for a robust Below1/4 conclusion. This is a general robust-query control, not an input to the proposed scalar-only certificate syntax. Conversely, a singleton X_0 followed by two-point identity systems has a singleton first coordinate but two full realizations. For K_n=[0,2^−n], the indicator of {0} is continuous on the survivor {0} alone but not constant on any K_n; survivor-only continuity does not give the ambient-open finite-stability argument. This does not rule out a global proof from the entire specified family that its survivor is zero. For noncompact K_n={0}∪[n+1,∞), their intersection lies in(−1,1), yet no K_n does: escaping mass defeats the compactness step. That control makes no effective-search claim. [R250-C152, C13–C16]

Effective input names are a separate requirement. Constant maps to a fixed noncomputable real α form a compact continuous uniquely realized system but do not supply a computable name of α. This differs from the half-affine example, whose inputs and state are uniformly computable. Conversely, if positive nonincreasing computable rational r_n tend to zero, the computable sets [0,r_n] permit a search for r_n<τ for any τ>0 without an explicit modulus as an additional input. The convergence promise guarantees termination but is not thereby decidable for arbitrary purported names. [R250-C152, C17–C18]

Thus a finite prefix000 already warrants x<1/4 for the first-halting family even though later halting may change x from zero to a small positive number. This is sufficient evidence for that unchanged strict rule. A rule demanding exact zero still requires its own equality proof or withholding. The mathematics grants no permission to substitute one release rule for the other and supplies no empirical probability, harm interpretation or authority. [R250-C152, §6]


#### Pointwise attraction, bounded images and the precise published witness

The full ordinary correction supplies a compact counterexample that distinguishes pointwise from uniform attraction. On X={0}∪{±1/n:n≥1}, set f(0)=0, f(1/n)=1/(n+1), f(−1)=1 and f(−1/n)=−1/(n−1) for n≥2. Every nonzero point is isolated and both approaches to zero have images tending to zero, so f is continuous. It is bijective on this compact space and hence a homeomorphism. Every forward orbit tends to zero, but every iterated image is X: all points survive and each starts an infinite backward orbit. The supremum distance of the nth image from zero stays one. Thus pointwise attraction and a unique fixed point do not give backward uniqueness even under compactness. This ordinary control is distinct from the separately checked discrete examples. [N250-184]

Eventual compactness suffices for the positive repair: if some f^m(X) is nonempty compact and f is continuous there, apply the compact theorem to that forward-invariant range. Every coordinate of every full backward path already lies there, and deleting a finite prefix of the nested ranges changes neither their intersection nor eventual uniform attraction. A separate sufficient condition is strict k-contraction on a nonempty complete metric space together with finite diameter D of f(X). The standard Cauchy-orbit estimate supplies the unique fixed point e, and diam(f^n(X))≤k^(n−1)D for n≥1 supplies uniform attraction and singleton survival. Bounded image matters: x↦x/2 on R is a strict contraction with every forward orbit tending to zero, yet it is onto and (2^i a) is a backward realization for every a. Neither condition is claimed to be a logically weakest repair. [N250-184]

The nonuniform implementation's separate independent receipt reports a fresh four-module build, 33 author readbacks and ten reviewer controls under Lean4.19/Mathlib, with the declared standard axioms only. It corroborates the actual dependent-family interface and preserves the ordinary-only status of the scalar supremum/finite-maximum identity, time-uniform separation, effective rates and observable quotients. The two retained validation wrappers refer to different uniform and nonuniform closures; neither was executed in this incorporation. The source-version investigation establishes the bibliographic identity of Billon's article but not finality of the inspected publisher-hosted proof-marked witness. A cached text extraction is not raw PDF acquisition or visual formula verification; absence of a located erratum is not evidence of its absence. The alternative draft cannot silently replace the inspected witness. [N250-159] [N250-160] [N250-186] [N250-187]

The finite-warrant addendum and its independent review preserve the earlier half-affine result rather than adding a new checker. Its exact strict-inequality witnesses are complete at their own queries; exact zero remains outside uniform effective finite certification for the admitted first-halting family. P02's rational-shift arithmetic is an inherited owner, and using its binary observer wrapper for a unary generator would be an arity error, not a new theorem about the stream. A depth can already specify a replay when the complete generator is independently available, so a submitted prefix does not by itself demonstrate reduced checking work. No additional runtime is justified merely by this representation/query application. [N250-188] [N250-189]

#### Direct completion providers and their different scope records

`IndexedCompletionForgetting` directly establishes the dependent-family result already used above: continuous bonding maps on nonempty compact metric fibres equate singleton coordinate survival, a unique compatible realization and fixed-coordinate range forgetting. Taking a finite maximum gives a depth for each fixed finite horizon and tolerance. No one depth uniform over all coordinates, effective modulus or stationary common fixed point is inferred. The companion reviewer controls make two hypotheses concrete: constant bonds can have unique realization without surjectivity, even with changing finite coordinate cardinalities; uniqueness at coordinate0 need not determine later coordinates. Empty fibres can make a range-forgetting assertion vacuous while preventing a realization. [R750A-557] [R750A-544]

The distinct stationary `CHECKED_SCOPE` body reports a dated Lean4.19 replay and51 axiom readbacks, whereas the indexed scope cited earlier reports its own four-module/33-readback packet. Those records must not be merged into one count. Stationary control A gives unique backward realization without forward attraction; control B gives unique backward realization and pointwise attraction while leaving extra finite-depth survivors. Compactness, continuity and nonemptiness supply the positive stationary repair. Control C, eventual compactness, contraction and philosophical interpretation are expressly outside that checked scope. `LawCompletionReadback` lists six exact definitions and51 declaration/axiom requests for that stationary family; no new readback output was produced in this incorporation. [R750A-577] [R750A-582]

[R750A-544]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/91f0b56b890d06a56350a190bdb3ed333c3eb21a56d26242e53aeff1863e467b/ReviewerControls.lean
[R750A-557]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/95f249ed2cbd48515217714a2794d8409ec5032c774dcffff0381909b07d032e/IndexedCompletionForgetting.lean
[R750A-577]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9b3a728681a2a4f46db0bd1a8c9cf9de5f2c885ab4ab8b6eb6b68b4ffb4d5f62/CHECKED_SCOPE.md
[R750A-582]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9bf48905487c241b2188be553a3e5656dc879493e9fcc4e85c53feab1e61e4b3/LawCompletionReadback.lean

## 8. A robust stateful witness

A theory of substitution should exhibit a nonvacuous case in which memory, continuous dynamics and handover actually compose in the model. The parity kernel provides such a case:

```math
Q=A=\{0,1\},\qquad
\Delta(q,a)=q\mathbin{\mathrm{xor}}a,\qquad
\Lambda(q)=q.
```

Both initial states are admitted. Input 0 holds the current parity and input 1 toggles it. The required state cannot be replaced by a memoryless function of the latest input: the same latest input can follow histories with opposite accumulated parity.

### 8.1 Digital and continuous realisations

The digital realisation stores one bit and applies xor. The alternative model has a real physical state z. Decode positive z as 0 and negative z as 1. For each logical bit q define the settled domain

```math
D_q=\left\{z:\frac45\le(-1)^qz\le\frac65\right\}.
```

An input a first applies a bounded-error reset,

```math
z^+=(-1)^az+\xi,\qquad |\xi|\le\frac1{20},
```

and then a dwell of duration τ = 3/10 under

```math
\dot z=z-z^3+w(t),
\qquad |w(t)|\le\frac1{10}.
```

The disturbance is any measurable function satisfying that bound. At the settled interface, the readout is z + n with |n| ≤ 1/10, decoded by sign. The reset is stipulated as an interface operation; a physical implementation would have to supply it with the declared error, duration and resource bounds.

**Proposition 6.** Each completed reset-and-dwell cycle maps Dq into the settled domain for q xor a for every admitted reset error and disturbance. Every admitted readout at that interface gives the correct logical bit.

**Proof.** Put q′ = q xor a. After the reset, let s be z when q′ = 0 and −z when q′ = 1. It initially lies in [3/4,5/4]. During the dwell it obeys

```math
\dot s=s-s^3+\widetilde w(t),
\qquad |\widetilde w(t)|\le\frac1{10}.
```

At the lower outer boundary its worst inward derivative is

```math
\frac34-\left(\frac34\right)^3-\frac1{10}
 =\frac{73}{320}=0.228125>0.
```

At the upper outer boundary its largest derivative is

```math
\frac54-\left(\frac54\right)^3+\frac1{10}
 =-\frac{193}{320}=-0.603125<0.
```

Thus the outer interval is invariant. Local uniqueness for this locally Lipschitz vector field with bounded measurable forcing, together with confinement in a compact interval, supplies the solution throughout the dwell.

On the lower strip [3/4,4/5], the function s − s³ is decreasing, so

```math
\dot s\ge
\frac45-\left(\frac45\right)^3-\frac1{10}
=\frac{47}{250}=0.188.
```

On the upper strip [6/5,5/4],

```math
\dot s\le
\frac65-\left(\frac65\right)^3+\frac1{10}
=-\frac{107}{250}=-0.428.
```

The respective entry times into [4/5,6/5] are therefore bounded by

```math
\frac{1/20}{47/250}=\frac{25}{94},
\qquad
\frac{1/20}{107/250}=\frac{25}{214}.
```

Both are below 3/10. At the inner boundaries the same strict inward inequalities make the settled interval invariant for the remaining dwell. Hence z lies in Dq′ at the observation interface. Its magnitude is at least 4/5, so readout noise of size at most 1/10 leaves a sign margin of at least 7/10. The decoded output is q′. ∎

Induction proves the full parity transition and output contract for every finite input sequence under the admitted disturbances. The result is not a single successful trajectory. It covers a continuous family of initial states and disturbances by the inequalities, while retaining explicit interface and dwell assumptions.

### 8.2 Handover in both directions

For a digital-to-continuous transfer, write

```math
z=(-1)^q+e,\qquad |e|\le\frac1{10}.
```

The signed magnitude then lies in [0.9,1.1], inside Dq. For a continuous-to-digital transfer, read the noisy sign at a settled interface. The margin proved above gives the correct bit.

Pause input acceptance during the transfer, retain the last accepted input index and resume once the new realisation is ready. Under those protocol assumptions, both migration maps preserve q. Proposition 5 therefore applies to every finite mixture of digital steps, continuous cycles and these transfers. It preserves the particular accumulated parity, not merely the ability to compute parity from a fresh start.

A lost or replayed toggle input is a real counterexample to continuation even when both processors and both transfer maps are individually correct. An experiment must therefore check the input protocol as well as the state decoder. A read during an unqualified transient is outside the stated observation contract.

This is a positive model of processor-role substitution. It can exclude the original digital state holder while still relying on engineered timing, actuation, readout and power. It establishes no universal independence from electronics or support. The ideal reset is not a measured instantaneous physical action, and the 0.3 dwell is not automatically the complete operation latency.

### 8.3 Physical interpretation and the next experiment

Microfluidic bubble logic supplies a historical physical precedent for a bistable toggle mechanism [BUB]. That precedent makes a stateful alternative mechanism concrete; it does not establish that a particular bubble device obeys this cubic differential equation or these perturbation bounds. The model must be fitted and checked against an actual apparatus before the analytic certificate applies to it.

A paired physical test would prepare both logical states, exercise both inputs and permitted perturbations, and compare mixed digital/alternative traces. It would transfer at qualified phases, remove the named original state holder, and record the continuing outputs with an independent reference logger that does not supply the controller's state. Preparation failures, calibration drift, missed deadlines, unaccounted support and excursions beyond the assumed noise bounds are separate outcomes. A failure of the proposed certificate is evidence about that model or implementation, not a proof that all physical parity realisations are impossible.

The source reports an exact-rational check of the boundary and entry calculations, together with finite numerical examples. Its reported one-cycle sample comprises 540 trajectories across initial signs, magnitudes, reset errors and disturbance choices; the stated settled range is approximately 0.810979 to 1.136109. A step-halving difference of about 0.00003599 is a numerical comparison, not a rigorous global integration-error bound. Its mixed length-ten exercise reports 2,048 traces, 8,192 alternative steps and 8,192 handovers under the selected schedule. Those finite selections do not enumerate all continuous disturbances or all schedules. The inequalities above carry the universal model claim; the reported computations have their own bounded evidential role.

No new apparatus, hardware dataset or physical replication is supplied by this chapter. The gain is a complete, inspectable conditional construction and a precise account of what must be measured to turn it into a physical continuation result.

## 9. Composition requires compatible mechanisms and compatible evidence

### 9.1 Joint resources and conditional error

A component contract should identify inputs, outputs, retained state, assumptions, guarantees, time, resources and admissible disturbances, together with the actual encoders and decoders. Serial composition requires one component's guaranteed output to meet the next component's assumptions. It also requires units, timing and interpretation to agree.

Suppose a finite sequence of k components has conditional failure probability at most εᵢ at stage i, given successful completion of the earlier stages and all the stated joint conditions. Let Fᵢ be the event that the first failure occurs at i. These events are disjoint, and

```math
\Pr(F_i)
=\Pr(\text{earlier success})\,
  \Pr(\text{failure at }i\mid\text{earlier success})
\le\varepsilon_i.
```

Therefore the probability of any failure is at most Σᵢεᵢ. Independence is unnecessary. But an isolated test error rate is not automatically the needed conditional bound: earlier stages can select a harder input distribution, consume shared resources or alter calibration.

Local feasibility is insufficient even without probability. Two components that each require three quarters of a resource with total budget one are separately feasible and jointly infeasible if they must run simultaneously. Serial scheduling can repair the conflict only if their temporal contract permits it. Similarly,

```math
\forall\text{ required role }j\ \exists\text{ a feasible configuration for }j
```

does not imply that one feasible configuration supplies every role. A storage-only configuration and a stateless execution configuration do not by themselves provide persistent computation. Bootstrap arguments must not borrow a clock, interpreter, power source or state service from the very host whose removal is supposed to have been achieved.

The delay example adds a third obstruction: even compatible roles and a perfect channel can omit a continuation-relevant state variable. A sound joint design must meet all three kinds of requirement—resources, interface assumptions and state sufficiency—at once.

### 9.2 Cases, types and justified placement

The source's proposed representational language distinguishes a concrete case, or **orthemma**, from a repeatable, consequence-bearing type, or **ortheme**. The distinction is indexed to an analysis: a particular versioned device is a case; a repeatable mechanism or failure pattern can be a type relevant to one question. A dated episode can itself become a case under another analysis. An observation of a case, the case itself and a correct type assignment are different objects.

Identifying a case is an operation on it, not the definition of the case itself. In this vocabulary, **orthing** is the rule-governed handling process; an **orthing episode** is a particular dated run and must not be identified with its result alone. A paper title names a record rather than, by itself, a physical channel type. A measured quantity becomes a relevant operational distinction through its scoped question, contrast, tolerance and consequences.

For analysis A, occurrence domain Mₐ and type repertoire Oₐ, the actual instantiation relation determines an actual profile:

```math
\mathrm{Inst}_{\mathsf A}
 \subseteq\mathcal M_{\mathsf A}	imes\mathcal O_{\mathsf A},
\qquad
O^*(m;\mathsf A)
=\{o\in\mathcal O_{\mathsf A}:(m,o)\in\mathrm{Inst}_{\mathsf A}\}.
```

The actual profile is the set of types the case instantiates. It is distinct both from an assessor's inferred partial profile and from the family of complete profiles still compatible with the available evidence. Fixing the analysis selects the question, scope and distinctions; it does not make an assignment true. A stable learned coordinate, a useful inferred category and a true operational distinction remain separate claims.

A **metaortheme** is a repeatable governing configuration of distinctions and relations; a particular configuration token is a metaorthemma. Neither term should stand indiscriminately for a whole episode, a policy act or every item surrounding an inference. Result correctness and pathway adequacy can also differ: a correct answer can arise from an unreliable process, and a reasonable process can encounter an adverse outcome.

The retained configuration-token correction identifies a fourth adequacy question between the governing policy and its execution. A repeatable type, its policy, a case-specific binding token and the execution trace are different objects. The token records or references its type/version, analysis compatibility, occurrence anchor, governed component, binding map, claim scope, instrument/calibration provenance, binding time and validity. Its binder and binding warrant remain distinct from the designated executor. Values uniquely fixed by the declared analysis are referenced rather than overridden without a new analysis version, and the token refers to evidence and trace without absorbing them. Correct type, sound policy and faithful execution can therefore coexist with a wrong reference plane, wrong-role tolerance, stale calibration or wrong success surface. The proposed token-adequacy condition retains each token's failure alongside the episode-level conjunction, so those different remedies remain addressable. Where no material case-specific binding, special scope, instrument/calibration or independent validity condition exists, no explicit token is introduced and that verdict is inapplicable, rather than an extra vacuous success. This is the patch's analytic configuration contract and reported object/terminology distinction, not evidence that the patch was applied, that a real binding was authorized, or that an episode passed it. [AFTER1384-S7-104](../archive/reconciliation/METAORTHEMMA-M1-INCREMENTAL-DIFFS.patch#L9-L17) [AFTER1384-S7-104](../archive/reconciliation/METAORTHEMMA-M1-INCREMENTAL-DIFFS.patch#L24-L80) [AFTER1384-S7-104](../archive/reconciliation/METAORTHEMMA-M1-INCREMENTAL-DIFFS.patch#L109-L125)

These distinctions have a practical use when comparing physical systems. A claim should retain its target and version, regime, procedure, provenance, uncertainty and validity conditions. A crosswalk should preserve inputs, outputs, units, resources and timing. Missing evidence stays missing through translation. Abstraction of a model, combination of evidence and physical composition of mechanisms are three different operations.

### 9.3 Lossless abstraction is target-relative

Let φ map concrete cases X to a representation Z, and let q map X to a target set T. There exists a decoder d on the attained image φ(X) satisfying q = d∘φ if and only if q is constant on every fibre of φ.

**Proof.** If q = d∘φ, equal representations have equal q values. Conversely, if q is constant on fibres, define d(φ(x)) = q(x); the condition makes this well-defined. The definition is unique on the attained image. ∎

Extending d to all of Z requires values on unattained points. A nonempty T permits an arbitrary default there; when X and T are empty but Z is nonempty, such a total extension is impossible. This edge case prevents a valid attained-image result from being silently strengthened to an unrestricted decoder claim.

The theorem is already developed in [Collective Inquiry and Strategic Coordination](collective-inquiry-and-strategic-coordination.md), section 2.1. Here it has two concrete uses. A representation that merges the delay kernel's two different future states loses a relevant distinction. A representation that discards physical coordinates while retaining the parity class can be sufficient for parity continuation. “Lossless” is consequently always relative to the target q and admitted domain.

An exact record of necessary checks need not identify the intended target. Let X={0,1}, let φ be constant, let c(x)=1 be the conjunction of the checks, and let q(x)=x. Then q(x)=1 implies c(x)=1 and c factors through φ, while q does not. [AFTER2884-NINTH25-201](../docs/project-closure/ar8r-v11/fable-research/lean/T299/Basic.lean#L107-L132) The matched-intervention construction realizes this pattern with equal complete profiles and all six conditions satisfied on both backgrounds; its positive sufficiency lemma concerns the label defined by their conjunction, not every label that merely requires them. [AFTER2884-NINTH25-201](../docs/project-closure/ar8r-v11/fable-research/lean/T299/Basic.lean#L183-L255) Definitional equivalence to the intended label, or an independent proof of fibre constancy, supplies the missing step. [AFTER2884-NINTH25-201](../docs/project-closure/ar8r-v11/fable-research/lean/T299/Basic.lean#L62-L89) These formal predicates do not themselves authenticate an actual causal intervention. [AFTER2884-NINTH25-201](../docs/project-closure/ar8r-v11/fable-research/lean/T299/Basic.lean#L134-L210)

### 9.4 Evidence joins, duplication and conflict

Let Θ be a common space of target possibilities, and let each evidence item determine a set Sᵢ of possibilities it leaves admissible. If the actual θ lies in every Sᵢ, it lies in their intersection. Any proposition true throughout that intersection is then true of θ. If instead each exclusion error has probability at most αᵢ, the probability that at least one item wrongly excludes the actual θ is at most Σᵢαᵢ, with no independence assumption.

The operation is idempotent: intersecting the same set twice changes nothing. A copied report is not another acquisition, and sharing one uncertainty source does not make repeated reports statistically independent. This agrees with the acquisition-root and synchronisation analysis in [Collective Inquiry and Strategic Coordination](collective-inquiry-and-strategic-coordination.md), section 1.4: propagation can improve availability without creating an additional evidential origin.

An empty intersection is a conflict requiring diagnosis. It is not permission to certify every proposition by vacuous universal quantification. The items must first be transported to the same target, version and regime; inconsistent units or incompatible operating conditions can produce an apparent contradiction that is really a failed join. Physical mechanisms can also interact while their evidence records are logically consistent, so evidence compatibility cannot replace joint resource analysis.

### 9.5 Representation, interpretation and generalisation

A representational system may aim to describe cases faithfully, support valid composition and generalise to new cases. A further ambition to generate arbitrary desired systems is stronger. Descriptive success does not prove constructive power, and success on a finite set does not prove universal generalisation.

There is an elementary interpretive symmetry. If an encoder e and decoder d realise the same external behaviour through a latent space, any bijection h of that space yields e′ = h∘e and d′ = d∘h⁻¹ with the same external behaviour. Unanchored coordinate names are therefore underdetermined. Interventions, structural constraints or shared anchors can reduce the symmetry; the result is not that interpretation is impossible. Nor does an abstract relabelling guarantee an efficient physical transformation.

The learned communication studied in *Translating Neuralese* is task- and listener-related communication among agents, with translation assessed through its effect on beliefs or performance [NEUR]. It is not evidence for a universal language of all cognition. A model's hidden coordinates need their own grounding and task tests.

For a second negative control, let a finite observed domain D be a proper subset of X, and allow all binary target functions on X. Two target functions can agree on every observed case and disagree at an unobserved x. A deterministic learner must answer x the same way after either identical dataset, and therefore fails for one target. A randomised learner cannot be correct with probability one for both. Generalisation needs restrictions on the hypothesis class, a distributional assumption, additional evidence or interventions.

The proposed representational framework consequently has an empirical question: at fixed target loss and cost, does it reduce risk relative to a competent conventional method on new cases? A meaningful positive claim would require a declared margin γ > 0,

```math
R_{\mathrm{new}}\le R_{\mathrm{baseline}}-\gamma,
```

under a specified test distribution. Acquisition, schema construction, training, human adjudication, abstention and false certification must be included in the account. Splits should separate provenance roots and mechanisms where those are the intended generalisation targets. The name of a type system or an agreement among its own rules supplies none of this comparative evidence.


### 9.6 Joint binding through forks, translations and merges

The preceding resource and evidence conditions become more precise when a handoff branches. The source-sensitive continuation synthesis asks whether a recipient retains the predecessor's reasons and operative organisation for the **declared future tasks**, under the actual source occurrences, meanings, grants, realisers and available interventions. It does not ask only whether the current output agrees. Its additional subject is joint binding: separately available admissibility witnesses need not describe one simultaneously realisable episode. This is not the claim that genuinely factive, jointly applicable warrants in one actual world have a false conjunction. It is the quantifier distinction between a witness for each isolated branch and one witness satisfying their shared conditions together. [Fork, translation and merge][JOIN79]

Represent a local packet over variables $`V_i`$ by a relation $`R_i`$ of alternatives still compatible with its evidence. An alternative is a joint assignment, not a collection of independently selectable column values. The variables can include the operative state, source-assertion occurrence, reading, version, role bearer, issuer, grant allocation, realiser and available future observations. A translation has its own occurrence identity while referring to an earlier source occurrence. A copied report has another recipient without creating another acquisition root. A shared grant-use or resource-reservation key is not reset by reserialisation.

The relational join describes simultaneous assignments satisfying the recorded constraints. Three questions remain distinct:

1. **Compatibility:** Is the join nonempty, and does each retained local alternative extend to a joint one?
2. **Decision adequacy:** Is one proposed action or policy justified across all alternatives still live for the receiver, or is more evidence needed?
3. **Realised continuation:** Is the selected operation currently authorised and causally executable, and does its actual successor retain the support required by the downstream task?

A nonempty join answers a possibility question. It neither selects the true tuple nor authenticates the interpretation, licenses a favourable reading or executes a transition. The task-relative continuation relation may branch or merge where permitted; it is not numerical identity.

#### Correlations can be lost while every local ambiguity survives

Suppose two descendants retain the same local reading set $`\{0,1\}`$. Their source-bound alignment can be parallel, $`\{(0,0),(1,1)\}`$, or crossed, $`\{(0,1),(1,0)\}`$. An operation requiring the correct alignment must distinguish these two relations without necessarily resolving which individual reading is actual. Keeping both unary sets and the source identifier loses the needed bit. For three binary descendants, even all pairwise projections fail to distinguish the even-parity and odd-parity joint relations. Adding pairwise labels is therefore not a general replacement for the higher-order constraint. These are finite separation controls, not a new theorem about contextuality or quantum systems.

Endpoint-exact composition is weaker than preserving the particular middle witnesses. For finite relations L⊆X×M and R⊆M×Y and a summary q on M, the summary relation admits (x,y) when xLm, nRy and q(m)=q(n) for some m,n; genuine composition instead requires one k with xLk and kRy. The genuine relation is always included, and equality holds exactly when every summary-matched pair has such an endpoint lift, which need not identify its original m and n. For example, L={(x,0)}, R={(0,y),(1,y)} and constant q give the correct endpoint relation although the matched witnesses 0 and 1 are distinct. If X is nonempty and exactness is required for every L with R and q fixed, the precise condition is that R(m)={y:mRy} be constant on each q-fibre: this supplies a lift through m, while any differing profiles are detected by a singleton left relation. That uniform condition is unnecessary for one fixed L: with L={(x,0),(x,1)}, R={(0,y)} and constant q, both endpoint relations agree despite different profiles. These finite distinctions do not authenticate causal occurrences or turn a shared provider into a shared intermediate event. [AFTER2884-FOURTH25-078](../research/t20-v6-20261012/sources/f2888ae667722ebc01d2de078c67536002911dc1f005362c170cc2f4bd9081b1/independent_controls.py#L35-L55) [AFTER2884-FOURTH25-079](../research/t20-v6-20261012/sources/f28d552bf7d367ff7731ae8b30d1f4f42a949bc8b477a896a3bdb156d0d0ca49/verify.py#L24-L43) [AFTER2884-FOURTH25-079](../research/t20-v6-20261012/sources/f28d552bf7d367ff7731ae8b30d1f4f42a949bc8b477a896a3bdb156d0d0ca49/verify.py#L127-L141) [AFTER2884-FOURTH25-079](../research/t20-v6-20261012/sources/f28d552bf7d367ff7731ae8b30d1f4f42a949bc8b477a896a3bdb156d0d0ca49/verify.py#L172-L184)

The amount lost depends on the future query family. Fix $`k\ge2`$ descendants and $`d\ge2`$ possible readings, and allow every nonempty relation $`R\subseteq[d]^k`$ with full coordinate projections. If one retained fixed-length annotation must answer **every** membership query $`t\in R`$ exactly with no later source query, then

```math
d^k-d\ \le b_{\min}\ \le d^k.
```

Indeed, include the $`d`$ diagonal tuples, which already make every marginal full, and choose any subset of the remaining $`d^k-d`$ tuples. These yield at least $`2^{d^k-d}`$ distinct admissible relations, and any two differ on a required query. Their annotations must therefore differ. Conversely, the $`d^k`$-bit characteristic table suffices. If $`N_{d,k}`$ is the number of full-marginal relations, unrestricted finite coding gives the exact minimum $`\lceil\log_2N_{d,k}\rceil`$.

For two descendants, inclusion–exclusion gives

```math
N_{d,2}=\sum_{i=0}^{d}(-1)^i\binom di(2^{d-i}-1)^d.
```

First require each row to be nonempty, then exclude empty columns. At $`d=2`$, there are seven relations, requiring three fixed-length bits. Restricting to bijective alignments instead gives $`d!`$ relations and $`\lceil\log_2(d!)\rceil`$ bits. This is elementary counting applied to a specified task family, not a claim that one Boolean question or every continuation requires exponential storage. A restricted generative relation class or genuine later source access can have a different budget.

#### A finite attributed-reading fixture keeps absence distinct from choice

The exact occurrence README and checker give a documentary control for the joint-binding problem. They specify seven manually interpreted claim records, of which six supply all three antecedent coordinates and one supplies (M,M,unspecified). The complete-record projection is the two-row relation

```math
R=\{(M,M,G),(G,G,G)\}.
```

The product of its coordinate projections adds exactly (G,M,G) and (M,G,G). Thus independently preserving the three marginal alternatives loses the first-two-coordinate equality that every supplied complete reading retains. This is a calculation under the fixture's declared interpretation, not a newly authenticated reading of its underlying sources. [Q250B-071] [Q250B-072]

Unspecified content is not a wildcard. The checker excludes the partial record from the complete relation: it licenses neither (M,M,M) nor a newly completed (M,M,G) on that partial record's authority alone. The complete (M,M,G) row has its other complete-record support. Copying a record preserves the same distinct claim identifiers and complete relation, rather than adding an independent acquisition or reading. The source also separates a work's direct exposition from its report of another person's view; occurrence order does not establish exclusive final preference, and a reported group label is not a measured population. [Q250B-071] [Q250B-072]

The seven frozen contract hashes include work, role, antecedents, attributed holder/selector and qualifications. They detect drift in those supplied fields. They do not prove the attribution or interpretation, independently acquire the named earlier authorities, or authenticate primary wording. The checker imports a separate source_rows.json fixture, which has not been opened or reconstructed in this reconciliation. The public description expressly excludes Arabic certification, a religious verdict and a live-application result. These boundaries preserve the positive finite relational example without turning its internal consistency into world-facing warrant. [Q250B-071] [Q250B-072]

The separate occurrence reviewer specifies a stronger future-operation test than equality of the present antecedent row. It generates the monoid of named-work exclusions on seven records plus one absorbing excluded state, then compares each state's observations after every generated operation. When the current row is retained, different future signatures within one row require different sidecar symbols, while symbols may be reused across different rows. The file requires minima 1, 2 and 3, with 4, 6 and 8 observation blocks, as content, voice and work exclusion are successively admitted; these are assertions conditional on the unreceived record fixture, not newly reproduced counts. Its single absorbing excluded state deliberately retains no lost-record identity. A restore-to-original operation cannot recover two distinct originals from that one state without additional retained information. Receipt hashes and a 49-entry register check do not authenticate the record interpretations or establish epistemic warrant. [G23-036](../research/t20-v6-20261012/sources/057f48272aa55a99b3817ad2e05371c17936ee39c1906b36ed57dd6b1e8a2390/independent_check.py#L6-L53)

[Q250B-071]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2ee521ec9c1a5508b4c8f6be80d87265b736a64e3eac6125e77566d7eba8f5c6/README.md
[Q250B-072]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3a34860f74ea5bf75b4ed1cf8322a21abbd65985dabc9a85aa14fc25e44d24b7/check.py

#### Shared authority and future competence are not copied into existence

An authentic grant permitting one of two successor roles to perform one exclusive operation can make each role's solo continuation possible without permitting both uses simultaneously. Copying the grant or translating its wording does not reset its allocation, expiry or use count. A genuinely shareable grant can permit both; branching itself is not the defect.

The same distinction limits source-history transport. If two individually lawful whole-history maps send the same source-command occurrence to different commands, no single-valued map on that shared occurrence has both outputs. Combining their conclusions requires specified duplication, origin and shared-store semantics. Unchanged commitments and cancellation tombstones cannot automatically be applied to transformed keys. Unioning records may change progress; dropping records may change safety. Two comparison isomorphisms do not themselves perform a legal fork–merge. Finite-history reification from authentic complete policy samples can reconstruct the specified source history, but epoch lookup is not source authentication and reconstruction does not prove that the physical history occurred.

Current state and output may also survive while future calibration does not. A successor that loses a source-bound alignment needed for a later task can remain adequate if it retains an actually available, authorised reacquisition interface. If the migration destroys the source or sole credential, a promise to reread it later supplies no capability. The task family, budget and future support must be declared; one successful handoff does not establish unrestricted recursive continuation.

The finite service model separates continued operation from the ability to renew it. Its first migration occurs with all resources present, copies the actual decoded bit into a new direct or inverse encoding, appoints the child and erases the parent's live state. After damage, retain archive, engine, state and grant but not builder or reserve. The child can still read, toggle and reject intruder toggles according to the stated two-request specification: engine and state decode the bit, and the active grant permits each operation. A second migration nevertheless fails its explicit builder requirement. Adding builder restores that particular handoff; retaining reserve supplies the whole required bundle in this model. An independently installed twin can match every declared behavioral word while lacking a migration event from the predecessor, and a fixed twin initialized to one fails to track an intervention changing the predecessor's initial bit to zero. These are direct consequences of the specified transition rules, not an executed enumeration or evidence that an actual archive, constructor or grant has these capabilities. Historical-record reliability and institutional continuity remain separate premises. [AFTER2634-EIGHTH25-187](../research/t20-v6-20261012/sources/e0ef2342554093154991718755afc98787d05f2a35ae6097578a690741665a7c/continuation_model.py#L24-L36) [AFTER2634-EIGHTH25-187](../research/t20-v6-20261012/sources/e0ef2342554093154991718755afc98787d05f2a35ae6097578a690741665a7c/continuation_model.py#L54-L115) [AFTER2634-EIGHTH25-187](../research/t20-v6-20261012/sources/e0ef2342554093154991718755afc98787d05f2a35ae6097578a690741665a7c/continuation_model.py#L135-L168) [AFTER2634-EIGHTH25-187](../research/t20-v6-20261012/sources/e0ef2342554093154991718755afc98787d05f2a35ae6097578a690741665a7c/continuation_model.py#L223-L265)

A causal successor and an independently produced lookalike can share state, outputs, copied proofs and a stated lineage identifier. A snapshot alone does not identify which physical transfer occurred or convey the predecessor's grant. The lookalike may obtain its own warrant or rights; this observation settles neither numerical identity nor ultimate source. Similarly, a faithful translated quotation can preserve the original assertion and ambiguity while performing only a report in its current context. It is not thereby a fresh directive or an independent testimony. Source force and present speech act must be retained separately.

The finite causal discriminator makes this loss stronger than snapshot agreement. Use Boolean roots A,B, route variables HA,HB and effect E. In the left-priority model HA=A and HB=B∧¬HA; in the right-priority model HB=B and HA=A∧¬HB; in the parallel model HA=A and HB=B. In all three, E=HA∨HB, so every intervention limited to A,B,E gives the same coarse root/output response. At A=B=1, however, the fine routes are respectively (1,0), (0,1) and (1,1). Under the source’s modified-HP convention, with candidate causes restricted to actual A/B assignments and other endogenous variables held only at their actual values, the minimal causes are respectively {A}, {B} and {A,B}. For example, changing A to zero while holding the actually inactive HB at zero defeats E in the left model; neither singleton defeats E in the parallel model. Replacing OR by AND gives the separate control in which each singleton is a cause. Moreover, at A=1,B=0, intervening on HA changes the left model’s effect although HA has been forgotten by the coarse representation. The test file requests 108 root/output comparisons, but no test was run here. These are finite model-relative distinctions, not a metaphysical identification of original agents or an enumeration of all causes under every causal convention. [QM-170](../research/t20-v6-20261012/sources/19fc643a6b0ff18ad153ce3dd31ff43b28fc4730121bc1f82ef8610368950381/causal_transfer.py#L9-L50) [QM-170](../research/t20-v6-20261012/sources/19fc643a6b0ff18ad153ce3dd31ff43b28fc4730121bc1f82ef8610368950381/causal_transfer.py#L70-L99) [QM-174](../research/t20-v6-20261012/sources/1aacf61cbd1569f614f5343af533924ecf44264189b342763ed521cfc0408cb5/test_causal_transfer.py#L4-L23)

Identification also depends on which interventions are admitted. For an otherwise arbitrary Boolean law f(A,B), the two concordant observations f(0,0)=0 and f(1,1)=1 leave four laws, distinguished by the two independent values f(0,1) and f(1,0). Querying either off-diagonal point alone leaves two alternatives; querying both identifies the law. Thus the unique inclusion-minimal complete extra-query set in this finite experiment is {(0,1),(1,0)}, entirely outside the original diagonal domain. The enumeration describes the information those queries would provide if separately admitted. It neither grants permission to perform them nor establishes their physical or metaphysical possibility. [QM-170](../research/t20-v6-20261012/sources/19fc643a6b0ff18ad153ce3dd31ff43b28fc4730121bc1f82ef8610368950381/causal_transfer.py#L52-L68) [QM-174](../research/t20-v6-20261012/sources/1aacf61cbd1569f614f5343af533924ecf44264189b342763ed521cfc0408cb5/test_causal_transfer.py#L12-L16)

#### One lawful repair and the observation needed after it

The restricted two-port model makes the lost alignment consequential. An authentic occurrence grants this recipient abstract action 0, which repairs its target; action 1 changes a protected neighbouring register and is not granted. Concrete port i implements i xor θ, for θ∈{0,1}. Both preparation histories retain the same present state, readout, source/version and local ambiguity sets, while the authorized port is i=θ. Before using a port the packet-only recipient receives no distinguishing observation. Choosing either port violates the grant in one history; choosing neither fails to complete the repair. If a randomized policy chooses port 0 with probability p, its two completion probabilities are at most p and 1−p, so its worst case is at most 1/2. Trying both ports is not a lawful diagnostic experiment. [N250C-097]

A task-relevant distinction between the two cases is necessary. An **already authorized**, source-and-realiser-bound calibration observation returning θ supplies it and is sufficient under the given realiser law: execute port θ, whose abstract action is 0. One bit describes the variable task-relevant information, not the full authentication, currentness or trust cost. This observation interprets an existing grant; it does not create one or prove issuer legitimacy. [N250C-097] [N250C-095]

For a second replacement with independent alignment φ, correctly repairing the first target and preserving its state can still destroy the sole service that exposes φ. The successor then faces the same separation at the next handoff. Retaining φ before retirement, or maintaining a genuinely available authorized query service, repairs this fixed two-handoff problem. A transcript adequate for both exact actions over all four (θ,φ) cases needs two bits of distinguishing information before the sole service disappears. It need not retain both permanently: θ may be discarded after its final relevant use. This finite counting argument proves no indefinitely viable strategy. [N250C-097]

Permission to reacquire is bearer-specific. A predecessor's nondelegated query right does not follow its copied evidence or service address to a new bearer. Either the successor already has the relevant right, or the predecessor is allowed to acquire and transmit the binding before retirement, or a new authorization is needed. If every informative probe presupposes a different disputed grant, a decoder does not supply a common lawful first step. The novelty is this occurrence-and-authority application of the existing export and maintained-support principles, not a new general gluing, continuation or identity theorem. [N250C-098] [N250C-095]

The public integrity case gives a concrete documentary analogue. A faithful projection preserves the historical speaker/occurrence/content/stance relation **and** the modern assessor/reconstruction/warrant relation. It cannot attach a modern unresolved burden to the historical speaker, or treat the speaker's affirmation as newly established modern warrant. Related content does not identify those occurrences or speech acts. This is attribution control using the accepted public packet, with no new primary-text précis or quotation. [N250C-096]

#### A bounded positive composition theorem preserves ambiguity

There is a constructive positive result when the independently justified relation model factors over a **finite join tree**. Each bag retains its finite relation, adjacent bags have the same projected relation on their exact shared variables, and the bags containing any one variable form a connected subtree. Starting from any permitted tuple in one bag, choose a matching tuple in each neighbour and recurse. Separator agreement supplies each match. The running-intersection condition ensures agreement on every variable shared by more distant bags, so the assignments combine into one global tuple extending the initial local tuple. No permitted local alternative must be silently discarded.

This is the established acyclic database/CSP local-to-global result. In an application, separators must include the actual shared reading, version, entitlement allocation and future reacquisition dependency whenever these affect the task. Renaming one dependency into two unlinked local variables or omitting a higher-order capacity factor invalidates the premise. After constructing compatible alternatives, the receiver still needs an action adequate across those alternatives and an actual authority/reservation mechanism for executing it. If no such action exists, preserving ambiguity can warrant withholding the operation rather than choosing a convenient tuple.

The synthesis explicitly credits the existing H-MOAT-E3 state-and-output, complete-operative-memory and joint-realiser contracts, its delay-machine export counterexample and augmented repair, shared-resource composition and anti-bootstrap conditions. Its stateful witness also retains the actual input index as a protocol resource alongside transferred state, so an otherwise correct handoff cannot silently lose or replay an accepted input. It does not rediscover those mechanisms. Copied-root minimax non-improvement, common-channel evidence conservation, provenance-span accounting, root-coordinate robustness and inverse-bijection holonomy retain their earlier owners. The relation-counting control and join-tree protocol are an application-level synthesis with established mathematical ancestry, including Beeri–Fagin–Maier–Yannakakis's acyclic database result and the broader global-section and provenance literature. They add no general gluing theorem, source-authentication procedure, theory of consciousness, numerical-identity theorem or unrestricted apoautosis result.

The remaining application burden is concrete: evidence must bind the actual source event and interpretation, the authority of this bearer and action in its current allocation state, the real transfer mechanism, and the availability of future support. Authenticated bytes do not themselves establish a source's competence, normative authority, truth or a hidden causal bridge. Another self-issued certificate cannot settle those facts. [JOIN79]

## 10. Supports, viability and progress

### 10.1 Failure tolerance as a hitting-set problem

Fix a task, horizon, resource and activation model. Let D₁,…,Dₘ be a finite exhaustive family of inclusion-minimal sufficient support sets, each contained in a finite component universe. “Sufficient” must include the interfaces and resources needed to activate and operate the task under this model, not merely the presence of a stored file.

After a set F of components fails, a listed sufficient support remains available exactly when

```math
\exists j\quad D_j\cap F=\varnothing.
```

Hence F eliminates every listed possibility exactly when it intersects every Dⱼ: it is a hitting set of the support family. If all Dⱼ are nonempty, the smallest cardinality of such a failure set is the transversal number

```math
\tau=\min\{|F|:\forall j,\ F\cap D_j\ne\varnothing\}.
```

The proof is the equivalence of the two displayed conditions under negation. Exhaustiveness and the fixed sufficiency model make it useful. With supports {a,b}, {b,c} and {a,c}, every single-component failure leaves one support and a two-component failure can hit them all, so τ = 2.

This is a structural fault-tolerance result. A nonexhaustive catalogue can exhibit redundancy but cannot prove that no unlisted alternative exists. Correlated failures, unequal failure costs or probabilities require the corresponding failure model; τ alone is not a reliability probability. An available sufficient arrangement also does not prove that the present running state can reach it within the required time. That is a campaign and continuation question.

### 10.2 The finite viability kernel

Let X be a finite, perfectly observed state space, Xsafe a safe subset, U(x) a finite set of permitted controls and W(x,u) a nonempty finite set of disturbances. The complete transition F(x,u,w) includes the support configuration and relevant resources. Define

```math
V_0=X_{\mathrm{safe}},
\qquad
V_{n+1}
=\{x\in V_n:
       \exists u\in U(x)\ \forall w\in W(x,u),\
       F(x,u,w)\in V_n\}.
```

The sets decrease and stabilise after finitely many strict removals.

**Proposition 7.** The fixed point V* is the largest subset of Xsafe in which a controller can remain forever against every admitted disturbance. A stationary feedback selecting a witnessing control at each state in V* suffices. Allowing arbitrary history-dependent control does not add states.

**Proof.** At the fixed point, each state has a control whose every successor remains in V*. Selecting such controls gives invariance by induction. Any other controlled invariant safe set S lies in V₀; if S lies in Vₙ, its witnessing controls show that it lies in Vₙ₊₁. Thus S lies in V*.

For the stronger history claim, give each excluded state the first iteration at which it is absent. A state already outside V₀ is unsafe. For a state removed later, every control has a disturbance leading to a state removed at an earlier iteration. An adversary can repeatedly choose such a disturbance, irrespective of the controller's stored history, until safety is lost. Thus no history-dependent policy can keep an excluded state safe against every admitted disturbance. ∎

For a simple finite example, a stable state has a safe hold action, a recoverable state can move to stable, every action at a fragile state admits a failure successor, and a stranded state can only move to fragile. The first pruning removes fragile; the next removes stranded. Stable and recoverable remain. A list of individually safe-looking one-step transitions would miss the stranded state's eventual failure.

The model is doing substantial work. Perfect observation permits the selected feedback to know its current state. Unknown dynamics, partial observations and uncertain transitions require a belief-state or conservative abstraction with justified inclusion of actual possibilities. Restricting permitted controls or enlarging the disturbance set cannot enlarge the viability kernel. These are the same monotonicity principles used for eligible inquiry controllers in [Information and Inquiry](information-and-inquiry.md), section 9.4.

### 10.3 Safety can be idle

An invariant system can remain safe while never producing a requested result. Progress requires a separate condition. Let S be a finite safe set, G a target set and r:S→{0,…,N} an integer rank such that rank zero implies membership in G. Suppose a permitted policy keeps every successor in S and, while outside G, strictly decreases r under every admitted disturbance.

Then every run reaches G in at most r(x₀) steps. Otherwise repeated strict decreases would drive a nonnegative integer below zero. A safe self-loop outside G is a counterexample to any inference from invariance alone.

The stronger temporal analyses in [Information and Inquiry](information-and-inquiry.md), section 9.4, distinguish entry into a controlled invariant target core from eventual persistence in a target set; those objectives need not have the same winning region. The rank condition here is a simple sufficient certificate for a declared finite task. Repeated requests need an arrival model, a reset or renewal condition and enough resources to meet the aggregate load. A one-request rank does not prove arbitrary sustained throughput.

### 10.4 A conditional autonomy theorem

A useful host-relative autonomy result now follows by composition. Fix the excluded support set H₀ and require one joint causal policy, implementable from its admitted information, for the campaign and subsequent operation. Assume:

- This policy carries the current state through a permitted, finite, jointly feasible campaign into an active region V.
- Every execution and transfer in the campaign preserves the full contract, including the effect/interface obligations of section 7.1, input ordering and timing.
- Every active realisation represented in V has its full indispensable support disjoint from H₀. Its computation, memory, input-output, power, timing, maintenance and controller roles are available within the same jointly feasible model.
- Under the same admitted future input and disturbance family, this same policy keeps the operative state in V and meets the declared progress and deadline obligations for as long as operation remains authorised.
- The policy also follows the declared stop and revocation contract; legitimate termination is not treated as a disturbance to resist.

The exact continuation theorem preserves the instance through the campaign. The joint policy's invariance keeps it within V, where support exclusion holds at every active state. That policy's progress and timing conditions supply the task completion that invariance alone lacks. Together they establish autonomy relative to H₀ and the declared model. Exclusion only at entry would be insufficient: an invariant region could subsequently return to a host-dependent realisation. Separate safety and progress policies also do not establish the required joint policy.

This is a substantive positive result. It is also a conjunction of inspectable premises. It is not independence from every physical support, unlimited energy, unlimited future workload or all possible disturbances. A finite campaign with conditional component failure probabilities can use the first-failure sum bound of section 9.1; that finite bound is not an infinite-horizon reliability guarantee.

Delay-tolerant networking's persistent store-and-forward architecture is relevant to intermittent paths and delayed delivery [DTN]. It does not make a dormant copy active or supply a missing processor. Similarly, a checkpoint that can later resume can satisfy a recovery contract while failing an uninterrupted-service contract.

### 10.5 Resources include the controller

A controller is a physical constituent of the claimed solution. Its observation, model identification, planning, updates and stored policy consume resources and can fail. Treating the controller as a free external oracle can make an otherwise impossible architecture appear feasible.

Thermodynamic arguments need equally precise scope. Bennett's account distinguishes logically irreversible operations, reversible computation and their physical implementations [BEN]. A bound associated with erasing information in a specified thermal setting is not a universal fixed energy cost for every logical operation, nor a proof that arbitrarily cheap complete computation is physically available. Preparation, error correction, clocking and maintenance remain part of the chosen model.

The practical objective of orchestration is therefore a contract-level quantity—correct output, latency, cost, robustness or some specified combination—under admissible resources. Increasing the number of components or the number of exchanged signals does not by itself improve it.

<a id="versioned-operational-safety"></a>

### 10.6 Versioned safety, attribution and progress

The operational guides distinguish three interfaces that a real replacement must not conflate: revising a governing criterion, admitting a state transition through an interlock, and identifying the root behind an opaque observed attempt. A certificate valid under a retained criterion is not yet permission to install a different criterion. The earlier criterion version explicitly lacked that installation step; the later version reports installation under a separate permission while retaining source, draft and unrelated state. That is a change in the modeled operation, not merely a stronger description of the earlier certificate. [GUIDE105-G073] [GUIDE105-G082]

The exact compiled-composition v2 review concerns the known-root model with n=4 and B=1 that consumes its imported transition both at proposal and live-root admission. Its successor determines the modeled plant change. V2 corrects a specific information-boundary error: proposal construction reads the actor's stored observed time, not the world's actual clock. An actor observing time 2 while the world is at 100 can still propose locally, while live roots reject an expired landing; an actor observing 100 does not borrow actual time 2 to rescue its proposal. Policy delivery does not silently refresh that observation. The earlier version's live checks already rejected expired landings, so the correction must not be presented as repair of an observed expired-write vulnerability. The review reports detection of a deliberately restored world-clock substitution and 26 kernel-checked composition declarations, 88 native assertions and seven wrapper-boundary tests, all for its exact frozen interface. Those are source-reported executions, not runs performed here. [N250A-002] [N250A-004]

Rule version, draft revision and control epoch remain separate. A successful installation changes normalized-LF to exact at rule version 3→4 while leaving the defective 3,014-byte draft and revision 8 intact. Separately authorized repair restores the 3,013-byte source and advances draft revision 8→9 without changing the installed rule history. Fresh authorized same-rule installation can also advance version/history, so literal full-state idempotence is false. Fixed-action replay exclusion and preservation of the achieved goal are the appropriate claims. Exact-envelope cancellation is likewise not a global blacklist of a nonce across changed commands. Actor authentication, authentic serial certificate delivery, actual service time, stable windows, root independence and non-bypassable execution remain external premises. [N250A-002] [N250A-004]

The original dynamic-history interface has a separate all-finite-history argument for a whole binary table. Its state starts with a genuine serial source descriptor, empty root memories and an arbitrary undamaged table, allowing a defective initial table. Histories include individual preparations, close-before-acknowledge revocations, completed-certificate delivery in delayed or reordered order, selected-root cancellation, same-command live landings, holds and arbitrary local changes at roots in one continuing lifetime-fault superset F. The theorem concerns this original interface; it does not automatically prove the later typed full-record composition or an unknown-label shared-store model. [N250A-026] [N250A-031] [N250A-033]

The induction uses six structural facts: good-root descriptors come from the authentic source history; their epochs do not exceed the effective epoch; every completed old epoch has a retained revocation certificate and good-acknowledger memory; pending good acknowledgers have already revoked the current epoch; cancellation acknowledgers belong to the selected path; and good cancellation acknowledgers retain the exact command's tombstone. No invariant field says that landings are safe or that every good root already knows the latest descriptor. An actual admitted path contains a good root, whose local check excludes future commands. If its command were old, overlap with that epoch's recorded revocation certificate would supply a good live veto. Only then does current full-descriptor authorization follow. Event determinism ensures the trace certificate concerns the actual successor rather than a separately selected safer execution. [N250A-031]

Good-root revocation and cancellation memories are proved monotone through the transition relation. Consequently a completed cancellation excludes the same complete command after every finite allowed continuation; an admitted repair restores the whole table; and a restored goal persists while the effective epoch remains unchanged. These conclusions leave holds and failed service possible indefinitely. Actual external permission additionally consumes the independent **valid-path Reservation** premise. The reviewed v2 correction restricts that premise to actual valid q-root paths, weakening an unnecessarily broad assumption without weakening internal safety. Shared failure correlation alone does not supply coherent root-wide closure across every gate copy, and a lifetime-union budget cannot be reset whenever a root appears recovered. [N250A-031] [N250A-033]

The unknown-root attribution extension fixes a possible alias class and prepared path/quorum families before the map/fault quantifiers. Its root-image criterion, actual-root availability and fixed-family threshold are treated in [Collective inquiry, §7.21](collective-inquiry-and-strategic-coordination.md#721-exact-criteria-opaque-search-and-the-operational-meaning-of-a-repair); they supply no provenance-discovery oracle, redesign after learning the map, cancellation mechanism or service bound. [N250A-000] [N250A-001]

The historical review stages must remain distinct. A preserved first-version receipt does not qualify a corrected second-version root. The earlier dynamic review required repairs to releasing stalled attempts, the adequate remaining horizon and the fixed scope of its restoration claim; the later candidate recorded those repairs while its own review was still pending. Conversely, an old pending-review sentence can remain an accurate historical feature of an unchanged author artifact when a later exact-byte sidecar supplies its disposition. The operational-model acceptance guide explicitly describes a later distribution whose scientific bytes were unchanged but whose state/event wording and manifest were corrected; its full replay concerns that identified distribution. Trusted compiler and dependency caches were not independently bootstrapped by that replay. No new scientific theorem, whole-batch refinement or physical-clock warrant follows from the distribution correction. [GUIDE105-G073] [GUIDE105-G020] [GUIDE105-G043]

A separate program-level exploration distinguishes three finite coverage claims. Its serial oracle tracks rule version/enabled status, requirement version, model version, epoch and issued records; a licence is current only when its stored relevant versions still match. It compares every word of lengths one through four over eight declared operations, recording refusals as outcomes rather than discarding them. This specifies 4,680 histories and 18,056 transitions, not arbitrary histories. Its synchronous-fault experiment injects MemoryError at each traced operational.py line event along fourteen chosen successful call paths and demands unchanged logical state and a cleared active flag. That is not every opcode, input or asynchronous interruption. Its thread experiment forces five chosen orderings plus one provisional-write/fault scenario while dispatch waits; it requests agreement with the corresponding abstract outcomes and expressly withholds fairness and all-schedule claims. These are complementary test designs, not substitutes for one another or for an all-history refinement theorem. AtomicEngine, the logical-state projection and tracing helpers are imported dependencies not examined with this body, and no passing execution or physical atomicity is inferred here. [AFTER1384-S6-082](../research/t20-v6-20261012/sources/2e38443ddbe0482140c7ef1ac3a0cc2b7189d462cdd21cea75a7471f13cf02f2/explore_histories.py#L12-L75) [AFTER1384-S6-082](../research/t20-v6-20261012/sources/2e38443ddbe0482140c7ef1ac3a0cc2b7189d462cdd21cea75a7471f13cf02f2/explore_histories.py#L77-L186)

A separate process-local operational reference binds the absence of a probability obligation as well as its presence. During admission, each relevant operation policy acquires a need-key dependency even when no obligation is installed; the missing key then has default stamp (0,true). Installing an obligation increments that key, and removing it increments the key again rather than restoring the original stamp. Thus a licence issued before installation stays stale after removal, instead of being revived merely because the visible requirement is absent again. Currentness compares the stored relevant dependency stamps, not the global epoch, so an unrelated policy revision need not invalidate that licence. Probability evidence additionally binds the selected observation-model version. A stale handle may nominate its retained source bytes for a new admission check, but does not authorize dispatch or revive its old record. The body places admission, revision and check-use dispatch under one reentrant lock and refuses to overwrite an existing ticket on a random-token collision. These are visible mechanisms of this finite reference, not a remote authentication scheme, proof that imported probability certificates are sound, or an all-fault atomicity theorem. In particular several revision methods perform multiple writes without a displayed rollback; locking alone supplies no guarantee against an exception between them. This original Engine must not be identified with the separately imported AtomicEngine of the finite-history experiments. No source or dependency was executed here. [AFTER1384-S11-205](../experiments/orthemology-v5/source/operational.py#L119-L155) [AFTER1384-S11-205](../experiments/orthemology-v5/source/operational.py#L210-L239) [AFTER1384-S11-205](../experiments/orthemology-v5/source/operational.py#L265-L274)

The separate observation-revision tests make numerical adequacy and licence currentness distinct obligations. In their declared tagged-uniform model, refining view [0,0] to [0,−1] is expected to increase the defect from 0 to 1/2. An old licence with tolerance 1/4 must become unusable; changing the requirement to 3/4 permits a fresh admission but must not revive the old handle. A different test changes only the law-version label while retaining the numerical view and expects the same stale-handle boundary. Conversely, changing an unrelated observation is expected to preserve dispatch. In the finite-program model, refinement from [0,0] to [0,1] is specified to retain zero defect, yet still invalidates the old handle and permits a newly admitted one. These are explicit regression expectations on the unread observation checker and Engine, not observed passes, an arbitrary-measure refinement theorem or evidence that model labels authenticate an actual law. [AFTER2384-SECOND25-32](../experiments/orthemology-v5/source/tests/test_observation_revision.py#L10-L40) [AFTER2384-SECOND25-32](../experiments/orthemology-v5/source/tests/test_observation_revision.py#L50-L92)

The collision regressions separate ticket bytes from issuer authority. One mocked collision asks that a second admission neither replace the first record nor change its dispatch result; another asks that it not revive a revoked licence. The two-engine control then forces equal ticket strings while admitting different primitives under the two engines. It requests each engine's own dispatch result and rejection of either cross-engine handle. Equal token bytes are therefore deliberately insufficient in this test contract: the admitted handle must remain bound to its issuing engine. These are explicit obligations on the unreceived operational import, not obtained outcomes, cryptographic collision resistance, remote authentication or proof that every cross-issuer path is rejected. [AFTER1884-T25-070](../experiments/orthemology-v5/source/tests/test_ticket_collision.py#L6-L29)

The separately retained pre-guard AtomicEngine adapter proposes a more limited transaction mechanism than the original multiwrite Engine. Under one RLock it copies the five mutable registries and epoch into a private Engine, calls the selected method there, and publishes that private reference only after the call returns. Its shallow-copy justification expressly depends on immutable values below those maps; encoding or snapshotting several arguments occurs before entry into the transaction. This shape prevents publication of that private fork on a precommit exception only under its stated host and no-private-mutation premises. It does not itself reject reentrant calls. If an invoked method can synchronously reenter this adapter, an inner call can fork the old published state and publish its result, after which the outer call can overwrite it with its earlier private fork. RLock permits that same-thread nesting. This conditional schedule identifies the missing nonreentrancy or nested-transaction obligation; it is not a demonstration that the unreceived operational methods expose such a callback. The body itself treats cancellation after publication as an indeterminate committed/pending call rather than rollback. It supplies neither crash durability, distributed serializability nor a new passing fault-injection result, and must not be identified with another AtomicEngine by basename. [AFTER1884-N25-207](../research/t20-v6-20261012/sources/7dc42b597a17589d007bad09215fd5d61e4c69684ed78cca80398f83043b42a1/atomic_engine_before_reentrancy_guard.py#L1-L7) [AFTER1884-N25-207](../research/t20-v6-20261012/sources/7dc42b597a17589d007bad09215fd5d61e4c69684ed78cca80398f83043b42a1/atomic_engine_before_reentrancy_guard.py#L15-L46) [AFTER1884-N25-207](../research/t20-v6-20261012/sources/7dc42b597a17589d007bad09215fd5d61e4c69684ed78cca80398f83043b42a1/atomic_engine_before_reentrancy_guard.py#L48-L89)

A separately retained guarded AtomicEngine variant supplies the missing public-entry restriction rather than making RLock itself nonreentrant. Its _call checks _active under the shared lock and refuses a second public transaction before entering the try/finally. That placement matters: a refused nested entry cannot run the finally clause and clear the outer transaction's flag. The accepted outer call sets the flag, forks the five mutable registries and epoch, invokes the selected method on that private Engine, and publishes its reference only after the method returns; finally clears the flag. Nested base-method calls can still share the private Engine and reentrant lock. Thus the displayed public-entry path cannot perform the inner fork of the old committed state described for the pre-guard variant. This is a local source mechanism under the stated immutable-reachable-values, all-or-none-reference-store and no-private-mutation premises, not proof that its unread operational or encoding dependencies meet them. Several argument conversions precede _call. The body still treats response loss after publication as indeterminate commitment rather than rollback, and supplies no crash durability, distributed serializability, CPython verification or newly passing fault-injection experiment. Nor does a shared class name identify it with the AtomicEngine imported by a different explorer. [AFTER2134-E8-184](../research/t20-v6-20261012/sources/9b503111d463be81611d5c5bcdf74921435377bd48bab0f9453e755620176737/atomic_engine.py#L1-L8) [AFTER2134-E8-184](../research/t20-v6-20261012/sources/9b503111d463be81611d5c5bcdf74921435377bd48bab0f9453e755620176737/atomic_engine.py#L15-L56) [AFTER2134-E8-184](../research/t20-v6-20261012/sources/9b503111d463be81611d5c5bcdf74921435377bd48bab0f9453e755620176737/atomic_engine.py#L58-L99)

The admitted dynamic v2 changelog identifies the actual strengthening: independently reachable authenticated control ports, B+1 selected-root cancellation acknowledgments, persistent full-command tombstones and enough remaining authorized preparation/execution/cancellation slots. A withheld tainted path had not been shown to terminate merely because an intact path would finish. The corrected 3N phase count concerns newly initiated final-descriptor macro-attempts after stable delivery; old in-flight work can require prior cleanup. The changelog's pending-review wording is historical, not a substitute for the later finite-history review's precise, independently bounded subject. None of these changes retroactively makes the stronger mechanisms admitted resources of a different restoration model. [N250A-025] [N250A-031] [N250A-033]

The two older semantic controls retain their original inconclusive outcomes: the old-program/new-decoder mutation reached its resource limit, and the initial cost check diagnosed an insufficient scalar premise without rejecting the full mutant module. Neither the baseline reconstruction nor the restart guide converts those runs into successful rejections. [GUIDE105-G068] [GUIDE105-G003] Later, distinct controls supplied stronger evidence. After rebuilding the cost dependency closure, the independent review records a concrete application mismatch: the mutated callee requires η ≤ ε/2 where the unchanged hypothesis supplies only η ≤ ε. That first error precedes the later timeout and unknown-constant cascade. It is rejection of that proof application, not falsity of the unchanged positive theorem. The separate corrected runtime argument proves positive-measure failure of the old-execution/computed-decoder statement, as explained in §2.5; it does not relabel the timed-out source mutation as a kernel rejection. These are historical review results with different targets and dependencies, not fresh executions here. [N250B-074] [N250B-075] [N250B-086] [N250B-089]

The portable-family adapter gives shared production and namespace-specific checking separate evidence identities. Its displayed family entry point calls the physical producer once, then consumes the cost and runtime/literal views without relaunching that producer. Copied objects retain their physical run, source-child, capture-index and digest bindings and receive zero new compilation credit. A view is eligible for its own target audit only after the physical collection satisfies the full original contract and that view has all required semantic outcomes; an eligible copy alone is not qualification. The audit must additionally bind its generated source and object-provenance map, finish without a resource diagnostic, cover the exact targets and retain the permitted axiom closure. In the cost-rejection path, the adapter requires the specified mutant, positive prerequisites, a concrete application mismatch, no source-log augmentation and the displayed mismatch_precedes_resource flag to be false. That last field is an exact local receipt condition, not permission to relabel the historically earlier mismatch-before-timeout review. The producer, collector and auditing dependencies were not executed or independently qualified here. These are contracts visible in one adapter body, not an observed physical run, two independent replications or a new kernel result. [AFTER2634-FIFTH25-100](../scripts/portable_family.py#L42-L79) [AFTER2634-FIFTH25-100](../scripts/portable_family.py#L81-L127) [AFTER2634-FIFTH25-100](../scripts/portable_family.py#L129-L175) [AFTER2634-FIFTH25-100](../scripts/portable_family.py#L258-L285)

[N250B-074]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/160a3b2d5109cfb199a0fc2a8bbfe3db2c68fb159409a14fb6a067b6158ad15e/README.md
[N250B-075]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/8ceccb1dd4ed96945bd27fc190111ae993d2b9fca36d685e337f1b8afd5baf6b/RESULT_INTERPRETATION.md
[N250B-086]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/33aee6f3c86f311ab1e778e4b265a2000a6a732826f8dd18b9ca3f8a31df6592/CORE_REVIEW.md
[N250B-089]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/0577b8bfcb99a87758160543804959403442591344556a89955a07055898a7cc/SOURCE_REVIEW.md




### 10.7 Durable cancellation and conditional progress

The versioned results above become more informative when the command identity, cancellation state and progress argument are stated together. The relevant sources describe two related models: a shared-root interpreter, in which several interface labels can address one actual store, and a separate four-path withholding batch in the `OperationalJoin.Offset.Batch` namespace. Each uses the specified local admission operation. Their conclusions retain their own state relations and premises; in particular, the four-path uniqueness theorem is not assumed for an arbitrary shared-root execution. The following arguments extend the exposition of §10.6 without changing the scope or historical verdict of any receipt cited there.

#### Complete commands and live authorization

In the common interface, a command has a selected path, epoch and recipient, while admission depends on the current plant, service time and local policy. A root stores its descriptor, revoked epochs, commitments and cancelled commands. Landing requires the path's declared cardinality and permission at every good selected root. The global damage predicate classifies an admitted effect against the current source policy; the local landing gate does not consult that predicate. Similarly, the consistency record contains authenticity and durable-memory conditions rather than assuming the desired safety or goal as a field. [R250-124]

In the typed specialization, write a complete envelope as

```math
e=(a,p',\nu,P),
```

where $a$ is the action, $p'$ its complete proposed successor, $\nu$ the nonce and $P$ the ordered path. These coordinates all belong to command identity. Altering only the successor's rule version yields a distinct envelope with the same nonce, action and path. Reversing a path can preserve its underlying label set while changing the envelope. A tombstone for the original therefore need not be a tombstone for either altered command. Whether the altered command is admissible remains a separate question. The source's snapshot representation also does not by itself constrain the effective global policy; that conclusion needs the stronger alignment invariant. [R250-216]

There are legitimate changes of path representation, but they transport more than the displayed list. The order-transport interface transforms the command, root memory, receipt function and event sequence together and preserves the corresponding trace and admission result. It does not justify reordering a command while leaving its identity-sensitive memory unchanged. Separate finite diagnostics show an empty receipt list and eligibility for a nonce-changed envelope and for a particular permitted action change. These are statements about the displayed fixtures, not operations that erase an old receipt or authorize every proposed change. [R250-228] [R250-136] [R250-194]

Even unchanged epoch and plant do not fix authorization. In the shared-root relation, a request followed by a genuine good-root acknowledgment creates a pending veto before the epoch advances. The revoked epoch belongs to the actual store, so it can block a selected alias that did not issue that acknowledgment. Keeping the epoch constant is therefore weaker than keeping the selected command unrevoked. [R250-206]

#### A false reply can leave durable evidence

Cancellation has both a state effect and a reply. In the explicit budget-one control, one bad-root reply is insufficient to close an otherwise live command; one bad and one good selected reply suffice. More subtly, two separate subthreshold calls can both return false while leaving tombstones at different good roots. Their represented cumulative acknowledgment sets are $\{1\}$ and then $\{1,2\}$, while repeating label 1 leaves only $\{1\}$. The second distinct call can therefore leave a cumulative cancellation certificate despite its own false reply. The source constructs aligned, reachable histories for these cumulative states. [R250-019]

This does not make every rejected call state-changing. Duplicate or unselected acknowledgment lists in that interface fail their outer guard before any partial mutation and are exact identity operations. Nor does cancellation undo a lawful landing: the plant remains at the achieved successor. A delayed preparation cannot reopen the same closed envelope. The distinction between the reply and the state must be made operation by operation. [R250-019]

The enlarged runtime language makes the durability result precise. It retains the predecessor's ordinary operations and adds cancellation. A valid cancellation step refines a finite abstract history even when its reply is false. A true reply additionally supplies a certificate for an abstract close event. Induction concatenates these local histories to refine every finite trace in the enlarged language. Given an initially reachable aligned state and a true `cancelWith` reply, any later successful attempt of that same complete envelope would refine to a landing forbidden by the retained cancellation certificate. Thus no such attempt succeeds after any finite continuation in this language. [R250-205]

The quantification is over that event language. It contains no clock-update event: every step, and hence every finite trace, preserves the runtime clock. Arbitrary real-time progress and refreshed actor observations require additional operations and arguments. A rejected landing is also not a rollback of earlier preparation. The separate runtime control preserves the entire partially prepared world, including honest commitments left by the preceding false prepare reply. Full policy alignment excludes replacing the effective policy, even by an unequal policy carrying the same epoch. [R250-128] [R250-205]

#### Exact freshness is weaker than a nonce high-water bound

The four-path withholding batch has a useful sufficient condition. Define `FreshAbove(w, ν)` to mean that every envelope stored in every good root's cancellation memory has nonce at most $\nu$. Every subsequently issued envelope with nonce greater than $\nu$ is then absent from that memory. `ReadyFor` adds requester identity, actual local admission to the same successor, matching good-root policies and absence of epoch revocation. The actor's own successful proposal remains a separate premise. Merely incrementing an actor counter does not establish a bound on hidden root memories. [R250-084]

The high-water invariant is preserved by preparation and attempts. Cancellation preserves an increased bound covering the cancelled command, a complete four-path batch advances a supplied bound by four, and certification and delivery preserve it. These are conditional invariant-preservation results. They neither discover the initial bound nor return a new actor record from `runBatch`. [R250-213]

For a particular trial, the source exposes the smaller relevant fact. `IntactUncancelled(w,e)` requires every selected root of $e$ to be intact and to lack that exact envelope in cancellation memory. Successful withholding proves this condition without a numerical fault-budget premise. Conversely, it suffices for that trial to land when the path, action, successor and live-admission conditions are supplied. An unselected root's tombstone is irrelevant to this predicate. That last coordinate test does not assert that every arbitrarily edited initial store is lifecycle-reachable. Cancellation is monotone for old tombstones and preserves absence or presence of a different complete envelope. [R250-113]

The sharpened batch theorem uses `ExactReady`, retaining the live-admission obligations while requiring the four predicted envelopes, rather than all high-nonce commands, to be absent from good-root cancellation memory. For actor nonce $\nu$, these envelopes have the fixed action and successor and the following nonce/path pairs:

```math
(\nu+1,[0,1,2]),\quad
(\nu+2,[0,1,3]),\quad
(\nu+3,[0,2,3]),\quad
(\nu+4,[1,2,3]).
```

**Conditional four-path completion.** In the literal withholding batch, suppose the actor's observed local proposal returns $p'$, the world has four roots and quorum three, at most one root is tainted, and `ExactReady` holds for these four envelopes. Then the batch has exactly one recorded landing and its final plant is $p'$. [R250-181]

**Proof.** At most one tainted root leaves an all-good path among the four. Induct over the scheduled paths. If a trial lands, the landing count is already positive. If it fails, the exact readiness conditions persist for the remaining distinct envelopes. The all-good witness cannot have been the failed head, since its eligibility would force that trial to land. It therefore remains in the tail, where induction gives a landing. The separate withholding invariant supplies the upper bound of one, and the successful proposal binds the resulting plant to $p'$. $\square$

The upper bound has its own smaller premise set. For this withholding controller, zero landings leave the plant unchanged, while one landing makes the fixed action unable to succeed again at any later policy or time. Induction preserves this invariant over the batch. No fault-cardinality, effective-policy alignment, actor-authenticity or synchronized-clock premise is needed for that at-most-one argument; these facts must not be confused with the premises needed to obtain a landing. It is an at-most-one result for the specified action and controller, not full-state idempotence of every future operation. [R250-229]

An explicit control separates exact readiness from high-water freshness. Put an unrelated complete-envelope tombstone with nonce 99 in the initial good-root stores, and start the specified actor at nonce zero. The four issued envelopes remain absent, so `ExactReady` holds and the batch completes once. `FreshAbove(w,0)` fails, since it would require $99\leq0$. Thus the high-water condition is strictly more restrictive. Neither the theorem nor the counterexample gives the actor an observation of those memories or an implementation of nonce allocation. [R250-182]

#### Delivery does not revive a cancelled retry

The retry fixture places an authentic new certificate at the actor before it reaches the honest roots. The first repair batch has zero landings and leaves durable cancellation records. Delivering the certificate afterward preserves those records. Repeating the same actor input still gives zero landings: `runBatch` has not returned an automatically advanced actor, and the same complete envelopes remain cancelled. [R250-248]

The source exhibits two different successful changes. Raising the actor nonce to eight avoids the old envelopes. Alternatively, changing the admitted repair command's lease end to 91 creates different envelopes and succeeds with the old actor nonce. That second run satisfies exact readiness but violates the high-water condition. The changed command is checked by the actual local admission operation; its success is not inferred solely from inequality of envelope names. The source describes this as a mathematical command-renewal control, not a renewal service already implemented by `runBatch`. The old command stays cancelled in both cases. [R250-248]

#### A public schedule can progress without recognizing success

The shared-root controller supplies a complementary constructive argument. A trial prepares a valid $q$-label path, attempts its complete command and cancels it. For the stated authenticated schedule it has a shared-root trace of exactly $2q+2$ events, including the terminal close. Its plant either remains unchanged or becomes the command's declared successor. On an all-good path with the required live eligibility, it reaches that successor regardless of the faulty-gate Boolean, since no faulty gate lies on that path. [R250-204]

The controller's `Clear` predicate requires every good actual store to have the selected policy descriptor, no revocation of the command's exact epoch and no tombstone for that full command. Preparation preserves clearance. Cancelling one command preserves clearance of another when their complete identities differ. These are protected service-state conditions; the actor is not assumed to observe them. [R250-249]

**Conditional run-all progress.** Fix a shared environment and a finite schedule of pairwise distinct complete commands. Suppose every command has a valid path, the correct requester and the same declared successor $p'$. Suppose all commands are initially clear, local admission from the initial plant under the selected policy returns each declared successor at its annotated service time, and one scheduled path is all-good. Then executing the whole schedule leaves the plant at $p'$. [R250-249]

**Proof.** Induct over the schedule. If the first trial reaches $p'$, every later trial either leaves that plant unchanged or writes the same successor. Otherwise the first trial leaves the original plant unchanged. It cannot be the all-good witness, because clearance and local admission would have forced success. That witness remains in the tail. Distinctness preserves its cancellation clearance, and the unchanged plant preserves the local-work premises. Induction applies to the tail. The proof never requires the controller to recognize a successful reply. $\square$

The actor-facing program binds this argument to a public instruction list. It computes its proposal from the observed plant, policy, observed time and action, then issues the chosen ordered paths with increasing nonces. Service times and faulty replies decorate the already fixed list; they do not choose command content or order. Hidden fault sets, actual root maps, actual plant state and acknowledgments are not inputs to that program. With the successful source proposal, uniform path size, actor identity, initial clearance, local admission from the initial plant at each annotated service time, and an all-good scheduled path supplied, `source_controller_progress` produces the final successor and a shared-root trace of length $N(2q+2)$ for $N$ paths. The source definition is noncomputable; this mathematical public-program interface is not by itself an executable extraction or a wall-clock bound. [R250-237]

The surrounding transition relation still permits arbitrary finite hold prefixes and a constant infinite hold run outside the goal. Even adding a specified eventual successful continuation does not bound the length of the prefix. The run-all theorem obtains progress from its particular schedule and service premises, while the unchanged relation alone supplies neither universal eventual progress nor a uniform delay. This is the operational counterpart of §10.3's safety/progress distinction. [R250-206]

These arguments preserve the source division of labor: current local admission determines permission, complete-envelope memory determines what cancellation blocks, a declared schedule preserves an eligible all-good witness, and the particular action semantics determine whether a landing can repeat. All proof credit remains with the exact cited modules and their inherited dependencies. Their source bodies were inspected for this incorporation; no Lean build, native guard evaluation, axiom readback, physical experiment or new acceptance review is claimed. The imported definitions and verification artifacts remain independently necessary.

The exact preparation provider distinguishes refusal from rollback. An invalid path leaves the world unchanged and returns false. On a valid path, a false all-signed reply may nevertheless retain the successful partial commitments and the corresponding trace/alignment. Its single shared `badSign` parameter is the declared behavior, not arbitrary independent Byzantine replies at each bad root. [R750A-553]

The batch-freshness controls then distinguish complete-envelope freshness from current local admission. Closing a failed batch cancels its old envelopes; later policy delivery can restore eligibility without reopening those cancellations. A fresh nonce batch can land, and a cancelled faulty first trial need not prevent an intact fourth trial. These are native-alignment/refinement-based source controls, not an unperformed empirical run. [R750A-507]

`EpochOffset` preserves the raw commands, actions and envelopes while changing the proof-side epoch index. Its root-gate equivalence and honest-path argument reject raw epochs below the base instead of deleting those commands. For a reachable shifted history, the current-source conclusion refers to raw epoch base+epoch. This proves neither the authenticity of an arbitrary snapshot nor the safety of a history before the selected base. [R750A-562]

[R750A-507]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/87397524cd22b46b1b8a68b83ff3bb2c11b7d036e30a7578c767d853980e54bc/BatchFreshnessV2SourceChallenges.lean
[R750A-553]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/942d32ffc7e2c0e045721b26b60eb9113e394ec8d7efd2befe318ecb089d3a0c/LifecyclePreparation.lean
[R750A-562]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/96d07179161099d80800ac4ed0e2a73a3a9aaf0d3ddfbbb452ed1a8e84711324/EpochOffset.lean

### 10.8 A known-arena game result is not a hidden-model controller

The family-104 transfer assessment makes the controller's information and objective part of the proposed reduction. The Ninth source already owns checker soundness for the actual submitted body and same structured input, common-policy/certificate equivalence and literal branch/node bindings. Proof-side choices in the existence argument are not computation performed inside the checker. Its stated verification cost is polynomial in materialized input, certificate size and rational bit lengths, not a polynomial bound on witness size or an implemented runtime theorem. The Sixteenth source adds structurally terminating signed search, exact negative checking and a controller compiled from the literal accepted body under the original history laws, with invalid inputs and empty support separately treated. These are inherited ownership claims; no fresh target replay is asserted. [R250-148]

The inspected ordinary mean-payoff endpoints solve a different problem: a total, finite, fully observed, two-player game with integer rewards, returning its zero-threshold winning set. The source contains the deterministic endpoint as well as the randomized endpoint listed by the family metadata. That corrects an incomplete endpoint census, not a missing target completeness proof. The randomized manuscript gives at least $`7/8`$ probability of the entire winning set being correct and quasipolynomial cost on every random tape. Its separate potential-certificate construction checks an exact clipped fixed point; uniqueness identifies the top-box solution and threshold regions. Repeated validated trials have almost-sure termination and expected-cost scope, not termination on every tape. The deterministic manuscript's additional value, strategy and fixed-credit energy services must not be attributed automatically to a formal endpoint that returns only a winning set. The inspected `low_payoff` helper states $`\liminf\leq-1/(n+1)`$, sufficient for its encoded losing-region separation, rather than the paper's stronger $`\limsup\leq-1/n`$ conclusion. No stochastic or mean-payoff/parity formal endpoint was established by that inspection.

The target chooses one policy before the fixed hidden model is known, supplies only observed action/state history and asks for model-relative parity almost surely under each actual model law. Stochastic mean payoff takes an expectation after the pathwise liminf; that objective is not almost-sure parity. Five analytical controls prevent replacing this contract with a game-winning bit. A half-chance choice of absorbing rewards $`+1`$ and $`-1`$ has expected limiting payoff zero while its nonnegative objective fails with probability one half. Repeated half-chance escape from an odd-priority state to an even absorbing state succeeds almost surely, although an adversary choosing the stay edge could prevent escape forever. Two hidden models can each have a winning first action while requiring opposite actions, so their modelwise winners do not give one almost-sure policy for both. Bad visits at times $`2^j`$ can be infinite while their negative penalties have limiting mean zero, which yields neither finite bad count, coBüchi nor exponential count moments. Finally, progressively longer waits at a priority-1/reward-0 vertex with repeated excursions to a priority-0/reward-$`-1`$ vertex can meet mean-payoff/parity together; an eventually periodic deterministic finite-memory policy either has negative mean or fails parity. These are written mathematical controls, not newly executed countermodels or experiments.

A known, fully observed finite adversarial quantitative arena remains a conditional application opportunity for the ordinary complexity theorem, potential check or one-resource fixed-credit service. A genuine application needs a total effective finite encoding, information-preserving strategy correspondence, equivalence of both objectives, faithful integer/rational and bit-cost compilation, literal checker/runtime linkage and a size/cost comparison with the existing service. None is supplied merely by finite state labels or rational transition rows. Even an accepted potential certifies only its encoded game fact, not model truth, source authority, safe physical actuation or normative jurisdiction. The assessment's disposition is therefore no new completeness transfer, with existing target ownership and model mismatch retained. Its four manuscript readings and bounded source inspection do not constitute fresh Lean, Comparator, empirical or adoption evidence. [R250-148]

### 10.9 From typed histories to a finite ordered controller

Section 10.7 separates durable command memory from progress. The adjacent formal sources also explain what the command changes, how a concrete service represents the abstract history, and which order changes preserve the result. These are different obligations. A representation of one state is not a simulation of every operation, and a source-level executable definition is not a record of a new execution.

#### Installing a criterion is a separately authorized effect

The criterion-installation interface uses two defined rules: exact byte equality and equality after removing trailing line-feed bytes. These are constructors for specified functions, not labels that authorize arbitrary supplied code. Appending one line-feed changes every finite byte sequence while leaving its trailing-line-feed normalization unchanged. Thus the normalized rule accepts a concrete wrong answer under the exact-source standard. Installing the exact rule changes this decision behavior: the altered sequence rejects and the source itself accepts. [R250-230]

The installation guard checks the standard, source target, destination, expected rule and version, authorization epoch, requested exact rule, installation operation and absence of revocation. Its grant must bind actor, destination, target and epoch to the installation operation; grant and command observation/lease intervals must contain the service time, with the command lease ending no later than the grant. Successful installation changes only the rule, its version and its appended history. Source, draft, draft revision, standard, destination, authorization data, clock and unrelated state are retained; rejection leaves the entire state unchanged. A data-repair grant cannot authorize criterion installation. Separate typed controls hold the numerical epoch and ordinary policy scope fixed while changing only the grant operation: installation and repair both reject their respective wrong-operation grants. Permission is therefore not reduced to epoch equality or broad scope. [R250-230] [R250-133]

The ordinary source-bound criterion argument clarifies what is being corrected. Its normalized-LF checker C0 was deliberately constructed for the experiment, not attributed to the historical programme or to the initial file-writing process. The observed extra-LF defect supplies a concrete wrong candidate under a retained exact-recovery standard. The supplied source identity and exact comparison warrant C1 independently of C0's own verdict; deleting the standard removes the claim that the difference is a defect of this task, while deleting source identification leaves equality to an unidentified array. The local criterion is extensionally unique for that target, not a universally obligatory norm or a proof of a particular theory of proper function. [N250A-011] [N250A-012] [N250A-015] [N250A-016]

The installation specification and Python interpreter give the two rules explicit meanings and change only rule, rule version and prior-rule history on success. Their exact-rule constructor cannot authorize arbitrary code carrying the same label. An extra-LF draft remains physically unchanged and now fails the repaired criterion; document restoration requires the separate replace-derived grant. Another recipient can reuse the adequacy proof but needs its own current actor/destination/target-bound grant. Revocation or a version change can defeat present permission while leaving criterion adequacy true. The 19 installation tests exercise these separations alongside the 25 draft tests, including fresh-recipient success and stale/revoked/expired/replayed commands rejecting without change. The admitted review reports 44 passing tests and a finite 4,096-row installation comparison, including four normalized-to-exact repairs and four authorized same-rule reinstalls. Those counts describe that review's recorded experiment, not additional executions or distinct universal theorems. [N250A-003] [N250A-012] [N250A-013] [N250A-014] [N250A-018] [N250A-020] [N250A-022] [N250A-023]

The transport argument separately warrants the current contextual inputs: copying a valid proof does not cover a recipient history in which permission was revoked after observation. Its coverage theorem remains sufficient for the chosen judgment and necessary only for uniform transport over its explicitly rich predicate class, as developed in [Collective inquiry, §7.21](collective-inquiry-and-strategic-coordination.md#721-exact-criteria-opaque-search-and-the-operational-meaning-of-a-repair). The argument's access-control comparison does not import clock freshness from Abadi and colleagues' calculus: timestamps and lifetimes lie outside that calculus's stated formal scope. [N250A-012] [N250A-016]

#### A local gate supports a current-policy conclusion

The abstract safety argument obtains a good selected root from the path/quorum and fault bounds. Its overlap inequality ensures that an old command's path intersects the old epoch's retained revocation certificate at a good root. That root cannot permit the command, excluding stale landings. For a command that does land, local admission fixes its epoch to the good root's descriptor; the invariant excludes a future descriptor, and the stale-command argument excludes an older epoch. Authenticity then identifies the **full** descriptor with the current authority-stream policy. Admission at the actual plant and annotated time follows without supplying that global policy to the live gate. Equal epochs identify full descriptors only under the stated authenticity and consistency hypotheses. [R250-043]

Cancellation uses a related but distinct argument. More than the fault budget of distinct acknowledgments yields a good acknowledging root, and consistency places it on the command's path with a durable tombstone. A landing would contradict its local gate. Each abstract step preserves good-root revocation and cancellation memories, acknowledgment sets grow, and epochs do not decrease. Induction therefore carries the cancellation obstruction through any finite trace from a reachable consistent state. The typed challenge closes a prepared but unlanded command while its expected version, permissions and other landing conditions still hold. This isolates the cancellation guard from replay rejection. Its exclusion theorem even permits later events with decreasing time annotations: it is a memory theorem, not a physical-clock theorem. [R250-043] [R250-133]

The typed command keeps the original ordered path inside its complete identity and separately proves that the path has no duplicates and every index is in range. Only then does its finite-set view have the same cardinality as the original list. Duplicate `[1,1,2]` and out-of-range `[1,2,4]` paths cannot inhabit the four-root command subtype. Root representation forgets repetition and ordering of *memory lists* because the gates use membership; it does not identify distinct complete commands. [R250-190] [R250-133]

At represented snapshots, a successful compiled attempt entails the abstract landing predicate with the same actual plant, time and single faulty-gate Boolean. The converse is established when that Boolean opens faulty gates; withholding can add rejection, so no unrestricted equivalence is asserted. At a reachable safe represented state, a successful attempt has the exact declared full successor. The snapshot relation alone does not establish macro-operation trace refinement or constrain every omitted world coordinate. [R250-190]

The typed history results expose the effect rather than merely a success flag. An installation sets the rule to exact, increments the rule version and appends the old rule. A repair copies source content into the draft, increments the draft revision and appends the previous draft. Other primitive events leave the plant unchanged. Along an initially consistent safe finite history, rule version and rule-history length increase by the number of installation landings; draft revision and draft-history length increase by the number of repair landings. Source, destination, standard and unrelated custody remain fixed. Goals, once achieved in the stated reachable safe setting, persist. [R250-190] [R250-120]

These nondecreasing counters give a stronger replay boundary than immediate duplicate rejection. Once a particular expected-version action has succeeded, it cannot succeed again after any lawful finite continuation from its reachable successor, at any later policy or annotated time. A hypothetical second success would require the old expected version or revision to equal a counter already increased by the first success and never decreased. Fresh valid actions can still change their respective counters and histories. This is not literal full-state idempotence. [R250-120] [R250-190]

The direct data-repair guard binds the command's target and payload to the stored source record, and checks destination, criterion, actor, operation, expected revision, authorization epoch and the current unrevoked grant with its time bounds. It does not independently authenticate that source record or its root labels. Its successful execution appends the previous draft and advances revision; rejection is identity. Already repaired content remains repaired through the specified mediated command lists. `Composition` then combines this repair with separately authorized criterion installation in the full plant and ordered envelope. Its good-root argument reaches the actual current full policy only through the fault-budget and sufficiently large selected-path premises, authentic same-epoch policy equality, absence of future descriptors and durable stale-epoch vetoes; the live landing gate is not given a global effective-policy oracle. The exact local no-repeat result starts from a successful step and rejects the fixed action at its successor plant, for any later policy and time. Its landing version also retains the fault-budget and sufficiently large selected-path premises. These conclusions do not extend to arbitrary state replacement or reset. [T750-C701] [T750-C745]

The local frame witnesses are correspondingly specific: preparation preserves plant, epoch, damage and envelopes; delivery preserves plant, epoch and damage; landing preserves epoch and pending. The finite-native preparation diagnostic preserves certificate history at the abstract view through its exact service refinement; its displayed theorem is not a separate equality of the underlying certificate-row lists. Extra malformed/duplicate fixture values declared alongside that diagnostic are not additional universally checked claims. These frame equalities support the composed history proof without independently supplying authorization or progress. [T750-C733] [T750-C722]

[T750-C701]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/be6587a55db1d3b3ac587282f78b9dd82e7575d634e9c3c4398f18ab555b5187/TypedCriterionGuard.lean
[T750-C745]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ca93c5a62515718c2de475e6102cff67b902f3021d297b68ce17e03694d2bee0/Composition.lean
[T750-C733]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c6f7d4890dbcfd30489f1f4ad322d24393d90dc9b067063dd5a9bfd8d9174901/JoinOperations.lean
[T750-C722]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c34696bf1c48fd3195755c534d94bbf1b80b517d03f080cdfeee8b981dd516cc/Diagnostic_prepare_preserves_certificates.lean

The direct lifecycle providers bind these conclusions to the native branches. From an aligned state, `LifecycleCertification` uses the full authentic **next** source policy, a raw previous epoch equal to base plus the abstract epoch, duplicate-free acknowledgers, exact quorum and bounded indices. Its actual aggregate transition expands into request, the supplied acknowledgments and completion, preserving older certificate correspondence, uniqueness and root alignment. A numerical next-epoch match alone does not supply that full policy. [F939A-763]

`LifecycleAttempt` maps a successful attempt to one primitive landing and the exact complete successor plant; all other world fields are retained. Rejection is full-world identity and an empty abstract trace, unlike earlier partial preparation. `RuntimeTrace` composes the actual prepare/attempt/certify/deliver branches from an aligned reachable start; invalid preparation and unrecorded delivery have explicit identity/empty witnesses. Its reached-success current-policy consequence does not itself establish aggregate `runBatch` refinement, aggregate cancellation or liveness. Those require the separate providers already distinguished in this chapter. [F939A-800] [F939A-784]

[F939A-763]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cfd9be46f852b6c01d13e78101b40c83246c0f1d4e7fba03a9ced16cb8ba0ac5/LifecycleCertification.lean
[F939A-784]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d52b337029651d38ddbad5a63023c7542b5d71f1a7fbadfb50480e09b213ac23/RuntimeTrace.lean
[F939A-800]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d9d4319ba644f1120aa30e6d04f0fd8f5b588328bc9053be535c7d94278d2f43/LifecycleAttempt.lean

The lifecycle reviews distinguish exact specialization from an unrestricted representation theorem. The original finite binary-table machine and the generic common machine have inverse state translations and corresponding events, including damaged states; the original admission predicate permits the stated time erasure. The later typed plant has unbounded versions and histories, so it cannot be injected into the four-value binary table merely by reusing that specialization. Its representation supplies the ordered-path and complete-successor facts above, while the stronger `Aligned` relation additionally binds the full effective policy, lifetime fault classification, roots and recorded authentic certificates. Snapshot existence is not this provenance invariant. [N250B-065] [N250B-066] [N250B-070] [N250B-073]

The reviewed raw-epoch offset preserves raw fields while relating a post-boundary source starting at epoch 2 to the abstract index. It does not authorize arbitrary pre-base histories: exact raw-epoch checks exclude a low value merely collapsed by subtraction, and the initial certificate list is empty. Certification needs the full authentic next record, not a same-epoch record of different contents. Invalid raw paths cannot enter the typed command interface, and direct plant mutation lies outside its admitted trace language. These are positive source-binding conditions rather than a global safety oracle inserted into admission. [N250B-066] [N250B-072]

The later cancellation and reference-clock acceptances extend that language in different ways. A true current-call cancellation threshold yields its durable certificate; a false reply can still leave partial tombstones, and requester-field equality is not a physical authentication protocol. The reference-time extension adds explicit clock changes, while the earlier trace theorem leaves time unchanged. The reviewed monotone-expiry result concerns one fixed envelope, not renewal or automatic observation refresh. The earlier runtime-lifecycle v4 review corrected its theorem-declaration count to 244 from the comment-derived 245. [N250B-072] The independent review records support these bounded extensions; they are not new execution here or permission to replace the retained good-root gate by a cached commitment check. [N250B-064] [N250B-069] [N250B-067] [N250B-068] [N250B-071]

[N250B-064]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/485083cfa8c0510ca3af177abd23d6e51835bf0c91074797c9d9fc4a0920fc69/CANCELLATION_ARGUMENT.md
[N250B-065]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/aee02b93ba8dcc1ac27bd6219f3d989ce17051ba8d6c039daa9b3062588fe4dc/CURRENT_CLAIM_MAP.md
[N250B-066]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/50367da2d04f4e85b5c38f41d20db6e8f9ecb8a0bb245cf50365464e4b062e90/LIFECYCLE_ARGUMENT.md
[N250B-067]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/26ec16efd3983558c87eeeda3029b65f653879600a9cb2bc2022243b77587966/REFERENCE_CLOCK_ARGUMENT.md
[N250B-068]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/bce6d90d2b4801643dfceb8846c2084c1acdedbaf9ec971e1f72b480f625c647/REFERENCE_CLOCK_CLAIM_MAP.md
[N250B-069]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/724ecc632703905871bfd0810d45897ee08b6e4ecda9fac59a9814f5ae1bd720/CANCELLATION_V5_REVIEW.md
[N250B-070]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/a27cb1d8dd4ca6e8f2f5da7e93ba88ef7a5f62c0f1b9ef84a9758262dbfdae15/CORE_V1_REVIEW.md
[N250B-071]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/17187ce22497bf218d70e47f8d98a156a45746b72eeb2635155cce38ca370151/REFERENCE_CLOCK_V6_REVIEW.md
[N250B-072]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/6de1ccd720711735bb998dbd26262d2a13533a65696295ea2ac2b08799939052/RUNTIME_V4_REVIEW_CORRECTED_V1.md
[N250B-073]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/e799f81c3d3a8f2adf7bb89d1390f67c9ad127ddc1bea53e2663af3a03fa4469/TYPED_V2_REVIEW.md

#### What the four-path log and lifecycle actually record

The batch-source module names the literal fold body of the imported `runBatch` and gives definitional equality, rather than introducing a replacement service. Each scheduled path appends one record with nonce equal to the actor's input nonce plus the previous record count plus one. Consequently its four records have exactly the four fixed paths and successive nonces. When proposal fails, the body leaves the world unchanged and appends a **synthetic** closed record with false preparation and landing flags. When proposal succeeds, it calls preparation, conditionally attempts, and calls cancellation on the full path. [R250-099]

For the correctly named owner, four roots, quorum three and budget one, every log record is closed. On a proposed well-formed three-label path, full-path cancellation obtains a true current-call reply; the proposal-none branch instead uses the synthetic record just described. An induction preserves the closure statement through the literal fold. This distinction prevents a closed log flag from being mistaken for evidence that every scheduled proposal executed a cancellation call. [R250-039]

Frame lemmas establish that preparation and cancellation preserve root policies and revoked epochs, while attempts preserve the whole roots function. The complete batch therefore preserves those root fields as well as root count, quorum, budget, runtime clock, effective policy and taint classification. Commitments and cancellation memory are deliberately not included in this frame. A false response may have changed them, as §10.7 explains. [R250-080]

A zero-fault control sharpens that warning: four preliminary cancellations, each receiving only one selected owner's reply, all return false. Their four distinct-envelope tombstones nevertheless block preparation and landing on all four scheduled trials, leaving the plant unchanged. The source supplies a genuine cancellation trace and an aligned reachable abstract history for this fixture; the obstruction is not merely an arbitrary edited store. Thus absence of a successful cancellation reply does not establish trial availability. [R250-072]

Completed-certificate delivery is also bound to the actual operation. Given alignment, reachability and membership of the certificate in the world's completed list, the compiled delivery refines a finite sequence of primitive deliveries to good roots. It updates a root's policy only when the certificate is newer, preserves its revoked epochs, commitments and cancelled commands, and preserves the plant, effective policy and completed-certificate alignment. Delayed or repeated older certificates are included; the aligned post-boundary stream admits no pre-base certificate. The proof's enumeration of good recipients is not information supplied to the actor. [R250-160]

The retained batch test function exercises installation followed by separately granted repair for each of the five listed fault patterns: no fault or one of four faulty roots. It specifies exact full successors, four closed records, one version/history-changing landing per batch and retained source/custody. It explicitly advances the actor's observed plant and nonce before the next phase rather than inferring that `runBatch` returns a refreshed actor. These are the source's executable assertions, not fresh test results. [R250-068]

The fixture-to-source link can itself be exact. `BatchControllerProjection` removes only IO assertions and the outer test loop from the let-bound installation/certification/delivery/repair sequence, retaining the original service calls and the explicit actor nonce update to 4. For the pinned bytes and bad-root-0 fixture, definitional equality identifies that pure sequence with the native aggregate witness; its completion follows from that witness. This is neither an executed IO test nor a theorem for arbitrary fault lists. `TypedFixtureHelpers` separately expands preparation at labels `[1,2,3]` into its three literal events and a landing condition, with four-root typing, quorum three and each selected envelope's readiness supplied. It is not an arbitrary-path controller or unconditional progress result. [F939A-755] [F939A-750]

[F939A-750]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cc715c3ff6ea0af4c0e0cb112d5051c2c1381b80e8bb93a113051b5a36d14278/TypedFixtureHelpers.lean
[F939A-755]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cd50511e1625838e74c095e60ddffcb22808742876cc1b93abb2f0d28bf9cab8/BatchControllerProjection.lean

#### Transporting command order is not merely reordering service

An admitted involutive command symmetry transports commitment and cancellation sets by its command image, the receipt function by the corresponding key substitution, and command-bearing events and corruption payloads consistently. Descriptors, revoked epochs and the plant remain unchanged. The source proves involution, membership and receipt correspondence, preservation of permission and landing, and commutation with preparation, cancellation, landing, requests, completion, acknowledgment and delivery. The concrete attempt bridge preserves valid-path checks, each gate and the attempt result with the **same** faulty-gate Boolean, including withholding. One cannot obtain these conclusions by changing a path while keeping its command-keyed memories fixed. [R250-070] [R250-018]

The trace-level extension retains the same environment while transporting the full state and each command-bearing event. A case analysis covers requests, acknowledgments, completion, delivery, preparation, cancellation acknowledgments, closure, landing, hold and corrupt-root replacement. The symmetry’s involution gives a two-way step equivalence; induction on event lists then gives a two-way trace equivalence with exactly the same list length. Since the initial-state transformation retains its plant, reachability is preserved in both directions as well. These are structural consequences of the supplied state-operation and gate correspondences, not merely permission for one landing or an executable procedure that migrates a physical state. [A750-S50-074](../research/t20-v6-20261012/sources/bbdf7ff794e5a3054c83d09530a3a61e0b727fc24767a827e1e3f7c565fdb096/SharedTraceTransport.lean#L9-L58) [A750-S50-074](../research/t20-v6-20261012/sources/bbdf7ff794e5a3054c83d09530a3a61e0b727fc24767a827e1e3f7c565fdb096/SharedTraceTransport.lean#L60-L87)

There is a smaller service-order freedom for one unchanged complete command. Preparing two addressed stores commutes even when the labels alias the same store: equal addresses apply the same transformation twice, and unequal addresses use commuting independent updates. The preparation eligibility test is unchanged by another preparation. Cancellation slots likewise commute, including the represented acknowledgment set. Therefore permutations of a fixed preparation or cancellation service list have the same represented set-valued final state. Raw native list insertion order need not be identical, and the complete command itself has not been reordered. [R250-052]

#### A public finite portfolio and its native interpreter

The public portfolio of all size-$q$ subsets of $m$ labels has $\binom{m}{q}$ entries. The environment's fault bound and repair-availability inequality guarantee at least $q$ good labels, hence an all-good member of that portfolio. Combining this existence fact with §10.7's clearance, authentic proposal and initial-plant admission premises gives conditional completion after servicing the entire public schedule, with $\binom{m}{q}(2q+2)$ abstract events. The concrete seven-label, five-label portfolio has 21 paths and 252 events. These counts belong to the shared-store reference program; they do not change the four-path implementation. The portfolio theorem is noncomputable and does not grant the actor a hidden-root query. [R250-030]

The separate native program supplies explicit ordered paths. It computes commands from the actor's observed plant, policy, observed time and action, assigning successive nonces. It accepts no actual-world state, routing map or service response as a command-selection input. Service annotations supply time, prepare bits, one gate Boolean and cancellation bits. Their number must equal the command count, and each bit array must have exactly $m$ entries. Missing, excess or malformed annotations reject. Successful annotation erases back to the exact command list and the exact supplied annotations, preserves pairwise command distinctness, and exists for matching lengths with valid arrays. Two successful decorations therefore expose identical complete commands, without implying that their visible replies or outcomes are identical. [R250-156]

The native interpreter services labels in the order actually stored in each command. A trial emits its preparation events, one attempt event, cancellation events and a terminal close event or the corresponding admitted primitive hold. Under `RoutingMatches`, its represented final state equals the shared reference run and its *actual emitted* events form a valid trace; these are separate conclusions. Slot-level correspondence and the service-permutation results above support induction over each service list, then over the trials. Each trial has exactly $2|P|+2$ events and a uniform $N$-trial run has $N(2q+2)$. Valid paths and authentic requester imply actual closure. Conditional native progress still requires common successors, distinct complete commands, initial clearance, admission at each annotated time from the initial plant, and an all-good scheduled path. Representation has not removed these premises. Independent contract wrappers retain the routing-match premise, actual emitted trace and exact annotation-erasure signatures. [R250-166] [R250-144]

The native execution-data source fixes 21 service annotations, a first-twenty prefix, repeated and expired runs, two routing fixtures and a malformed annotation. Its checks require 259 events for the full fixture and 247 for the first-twenty projection, which explicitly prepends seven holds to its twenty-trial trace. Those fixture totals must not be substituted for the 252 trial events of the 21-path reference schedule. They require no effect during that prefix, a single installation on the full run, retained state changes in the failed prefix, no reinstallation on replay and no effect under expired service. They also check rejection of wrong annotation lengths, malformed arrays and nonadmitting proposals, plus withholding and good-alias cases. These are precisely stated fixture expectations in the retained source, not general worst-case completeness and not observations from a run performed for this chapter. [R250-097] [R250-031]

This supplement incorporates the operational argument and its boundaries, while the exact cited formal modules retain every declaration, proof term, fixture, import and executable check. Prose is not their executable successor. No imported dependency body was inspected for this supplement, and no Lean compilation, native evaluation, axiom readback, CI, physical experiment or new assurance acceptance is asserted. Source preservation, consumer migration and any later active-path retirement remain separate obligations.

The direct portfolio and entry witnesses retain the public order and the service assumptions of this finite construction. `NativePortfolio` literally lists all21 five-label subsets of seven, assigns distinct nonces to ordered commands, and covers every path. Equality of path support preserves the relevant predecessor trial index but does not identify two different full command orders. Its all-good-path conclusion retains q=5 and the environment premises; the section's noncomputable declarations do not amount to a new implemented optimizer. [R750A-522]

`NativeInitialWitness` specializes this fixed public list at epoch zero. With matching hidden routing/source and21 supplied valid monotone service annotations in [2,22], it proves the exact execute result, a259-event shared trace and the installed final plant. No command is selected by consulting the hidden world. The service decorations, source matching and authority remain assumptions. In particular this bounded positive endpoint does not implement nonzero-epoch policy delivery or turn the existence of a trace into an unconditional scheduling guarantee. [R750A-583]

[R750A-522]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8a7593a91eaf694abf686e188416ceba65a5db75f35f93e1fdb4d3e14ddfd08a/NativePortfolio.lean
[R750A-583]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9bfcab94a182a89beb52438d82defc136b168da017f2c551281a16dc8a16925b/NativeInitialWitness.lean

#### Reference time and persistent rejection

`ReferenceClock` updates the world's clock without changing structural alignment, even if the clock moves backward. Nevertheless, the actual local install and repair predicates imply `now < leaseEnd`, so expiry rejects a local step and an aligned reachable attempt. `MonotoneReferenceTrace` supplies the stronger temporal contract: its explicit advance step is nondecreasing, and its service steps are the real retained operations. An expired **fixed envelope** stays rejected along that trace class, while durable cancellation remains effective through its continuations. Structural alignment alone establishes neither monotone time nor freshness. [T750-C706] [T750-C679]

The theorem guide distinguishes weak snapshot representation from alignment, and numerical epoch shape from authentic full-policy provenance. Its earlier trace class omits the later reference-time updates; those updates also do not refresh the actor's observations. Accordingly the monotone theorem is a specified extension, not a retroactive claim about every runtime trace. Neither equal-time stalling nor unbounded forward advances has a physical latency bound here; a fresh longer-lived envelope is a different command from the expired one. [T750-C727]

[T750-C679]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b78337de857142de64045121783d306d379ca436fdc863c193de83557e611d05/MonotoneReferenceTrace.lean
[T750-C706]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bf32299fcceb48426fd7b88a8bfca4461390e1c85260fb6cc2d7157003cd592f/ReferenceClock.lean
[T750-C727]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c443ac6238304a5d11e751e8ffc22fad80905e16b1459f8695bcaf0fdfc091ea/THEOREM_GUIDE.md

The clock controls give exact separating cases. Installation and repair can occur in one monotone history at reference times 3 and 4, with a common abstract-history witness. The fixed command succeeds at time 89 and rejects at 90 even though the grant expires at 100 and cached root commitments are unchanged. An uncancelled envelope rejected at 100 can instead succeed after a structural rollback to 2; no monotone trace realizes that rollback. A cancellation tombstone survives both changes. Thus monotonicity is a substantive premise for persistent **expiry**, while cancellation has its own durable-memory argument. [F939A-798]

The actor's observed time is separate again: a stale observation may permit a proposal that the current root clock rejects, while a nonadmitting actor observation cannot borrow a valid live clock to create that proposal. `ClockTests` states the corresponding IO checks. These source controls do not report a fresh test run or an automatic refresh of actor observations. [F939A-770] [F939A-798]

[F939A-770]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d2cac04c13db2780e3a56eb5ded174f0c032d1e040e65a47401efb6bbf8dbd69/ClockTests.lean
[F939A-798]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d971a5e4b1862dfa650266aba88c430ceac1d39189ba829976850cd759b389cc/ReferenceClockControls.lean


<a id="final189-b10-window-clock-and-native-effects"></a>

The end-to-end shared-window theorem starts from a reachable idle state and a correctly observed plant, authentic current actor policy and matching requester. It requires all scheduled service times to be nondecreasing, after observation and inside the declared window, and the very same action/successor to remain locally admitted throughout that window. Uniform q-label paths, tombstone freshness and a wholly good path then give a compiled shared trace of exactly m+|paths|·(2q+2) events, including the m-label synchronization prelude. For seven labels and all twenty-one five-label paths this is259. The hidden root map is not a controller input; bounded slot completion and full-window applicability are genuine conditions, not measured latency guarantees. [F189B-850](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e77ba7d705231040c4abf8f3f4776e9bf09ae9d502502720fd272cb338675e2e/WindowProgress.lean)

The clock challenges preserve that qualification concretely. Arbitrarily many equal-time advances can leave the world unchanged, and an arbitrary forward jump is permitted. Structural alignment can hold at both time100 and time2 while the same prepared envelope changes from rejected to accepted. Expiry rejection is identity of the whole World, including commitments and certificates, for either badOpen flag. A fresh longer-lease command may still land, and expired preparation may retain a dishonest commitment even though honest live gates block landing. No theorem identifies monotone reference time with physical progress. [F189B-855](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e8dba20d27d40b85e5943b11aa83e3959e58091dae8575d013cebce5b69ffb48/ReferenceClockV6Challenges.lean)

The selected native execution controls go beyond a fixture's requested test output: applying the universal refinement to the actual Executed.withholding, specs and full values proves a21-trial compile/execute result, a259-event shared trace, the complete installed plant, exactly one installation and zero repair events. Option extraction is justified by successful compilation, not an arbitrary fallback. The final source, destination, standard, unrelated state, draft, draft revision and draft history equal their initial coordinates. These are source-bound mathematical assertions, not a newly run executable or deployment receipt. [F189B-875](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ee0016084088a44b87287b179219a10474c74cab337e4058d4c0e8bff2e9d90f/NativeExecutionControls.lean)

### 10.10 Exact primitive contracts and remaining runtime boundaries

The arguments in §§10.7 and 10.9 rely on a particular transition language and on separately stated applicability conditions. The following details complete its scientific contract rather than enlarging its assurance or physical scope.

#### The primitive kernel's premises and effects

For $n$ labels, fault budget $B$, landing quorum $q$ and revocation quorum $r$, the configuration requires at most $B$ faulty labels, $B<n$, strict overlap $n+B<q+r$, and both availability inequalities $q+B\leq n$ and $r+B\leq n$. Its policy source assigns epoch $e$ a descriptor whose epoch is exactly $e$. The local interface requires admission to expose the already checked command epoch and requester; neither desired safety nor a goal is an interface law. A root carries its descriptor, revoked epochs, commitments and cancelled complete commands. The global proof-side state additionally records epoch, pending status, current acknowledgments, past certificates, per-command cancellation acknowledgments, plant and damage flag. Initialization sets epoch zero and source-zero descriptors, with empty memories/certificates, no pending transition and no damage. A root permits a command only when it is committed, locally admitted, unrevoked at its epoch and uncancelled. Landing requires exactly $q$ selected labels and permission at every good selected root. [R250-124]

The legal events have distinct guards and effects. A request requires no pending transition and opens one with empty acknowledgments. Acknowledgment requires a pending transition, adds a label, and records the current epoch as revoked at a good root. Completion requires a pending transition and exactly $r$ acknowledgments; it stores that certificate, advances the epoch, clears pending state and resets the acknowledgment set to empty. Delivery requires $0<e\leq$ the current epoch and replaces a descriptor only when newer. Preparation requires a selected label and valid $q$-path; a good root must pass live admission, unrevoked-epoch and uncancelled-command checks, while a faulty label may supply its own response. It adds a commitment. Cancellation acknowledgment requires a selected label and either a faulty label or the intended requester; it adds the acknowledgment and, at a good root, the exact tombstone. A close event requires more than $B$ distinct cancellation acknowledgments and changes no state. Landing requires the local landing predicate; hold is identity, and arbitrary root replacement is allowed only at a faulty label. [R250-124]

The landing update classifies damage after admission: existing damage is absorbing; a failure of current-source admission marks damage instead of changing the plant; otherwise it applies the declared effect. This classifier is not read by the local landing gate. Consistency records full descriptor authenticity, no future good-root descriptor, exact-size past certificates with good signers' retained revocations, revocation at every good label in the current acknowledgment set, without a separate pending-state hypothesis, selected cancellation acknowledgers and durable good-root tombstones. It does not assume that damage is false. A finite trace is a chain of these guarded steps; reachability means such a chain from some initialized plant. These definitions specify the hypotheses used in §10.9's safety argument, not a universal model of any interlock. [R250-124]

The external reservation premise can be narrowed without being eliminated. `ReservationDomain` includes `ValidPath` among its antecedents, so permission restricted exactly to that licensed domain satisfies the revised predicate. The copied older predicate omitted that antecedent: at an explicitly invalid empty path it would demand the same permission and thereby fails. This is a genuine removal of an unused **out-of-domain** obligation, not a derivation of institutional consent from the internal gate and not a weakening of permission for an admitted command. [F939A-761]

The independent-root review also earns a positive boundary case: its configuration inequalities imply positive landing and revocation quorums even when the fault budget is zero, and a one-root, zero-budget configuration has an explicit prepare/land repair trace. That does not remove the positive-budget premise from the different hidden-alias robustness equivalence. In the ordinary model, merely requesting revocation still permits a live current landing until a good-root acknowledgment closes its gate; arbitrary finite holds remain safe without furnishing progress. [F939A-757]

[F939A-761]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cef9aeb5ac9e49fc718399c78a35ac641ecf1db4548fd9dfdc480a08102b13f6/ReservationDomain.lean
[F939A-757]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ce31bbe84122f46fdd84c22ee0c8d5f93bead73107eb16e0fafb44502a2a0c38/ReviewChallenges.lean

#### What readiness preservation does and does not supply

`AdmissionReady` is `ReadyFor` without its high-water cancellation condition: it retains requester identity, actual current-plant admission to the declared successor, and matching unrevoked good-root policies. `HasSurvivingTrial` says that at least one predicted envelope is intact and uncancelled at every selected root. It is a proof-side existential definition, not an actor observation or a batch-completion theorem by itself. [R250-113]

Preparation leaves cancellation memory and eligibility unchanged and creates each eligible good selected commitment; with a valid all-good path this makes the subsequent withholding attempt succeed. Preparation preserves readiness. Cleanup preserves readiness at any new nonce bound covering both the old bound and the cancelled envelope. Cancellation alone preserves admission readiness without a freshness premise. A rejected complete trial also preserves admission readiness, and preserves high-water readiness under that same bound condition. At the more exact level, a whole trial preserves every prior tombstone, leaves a *different* complete envelope's cancellation membership unchanged, and therefore preserves its intact-and-uncancelled condition. Conversely, if that condition holds after a trial, it held before it. These statements explain why a failed trial cannot silently consume a different eligible witness. [R250-084] [R250-113] [R250-213]

The exact-progress induction applies to an arbitrary supplied finite path list and accumulator, not only the four-path corollary: well-formed paths, a successful actor proposal, exact readiness for the remaining predicted envelopes at the accumulator-adjusted nonce, and an all-good remaining path imply a strict increase in recorded landings over that accumulator. Its induction either keeps an already obtained increase or preserves the tail's eligible witness. The four-path theorem then supplies the witness from its fault bound and combines this increase with the separate at-most-one invariant. Neither this general induction nor the existence predicate supplies a hidden-memory query or a nonce allocator. [R250-181]

#### Further cancellation, offset and representation controls

Three concrete cancellation controls separate authorization and identity. A wrong requester fails to close the prepared command, which can still land for its proper requester. Cleanup after the authority advances from epoch two to three can still record an old command's tombstone and return true. Finally, a reversed-path envelope with the original nonce is a different complete command and, in the displayed fixture, actually prepares and lands after the original was cancelled. That last control deliberately violates a correct actor's fresh-nonce discipline. It establishes command-specific cancellation, not an authorized general strategy for escaping it. [R250-019]

Offsetting epochs can map a pre-base raw command and a boundary command to the same abstract epoch. The retained control has unequal raw action epochs, and the actual prepared attempt of the low raw command still rejects. Arithmetic coincidence in the projection therefore does not establish source admission. In this offset interface, goals persist along reachable finite histories because the unchanged local source effect preserves them; no extra goal-preservation premise is needed. The enlarged cancellation-runtime refinement also yields a current-policy conclusion: any later successful attempt has its raw action epoch equal to the actual effective-policy epoch and the actual local step returns its declared successor. Initial alignment and reachability, and continuation in that event language, remain required. Ordinary runtime traces embed through the ordinary-event wrapper; an invalid cancellation outer guard is identity and refines an empty abstract history, while a true reply additionally justifies a close event. [R250-128] [R250-205]

Delivery has two exact full-world boundaries in addition to its alignment theorem. An unrecorded certificate causes identity. Delivering the same certificate twice equals delivering it once, including faulty-root state and unrelated fields: either membership fails both times, or the first update makes each updated descriptor no older than that certificate. This is idempotence of delivery, not the full-state idempotence of installation or repair rejected in §10.9. [R250-128]

Two representation checks prevent vacuous or overly strong transfer claims. Every concrete runtime root has a representing typed root, constructed by `rootView`; the snapshot correspondence is therefore not justified merely by quantifying over an empty relation. Conversely, the binary source specialization maps landing events with any two time annotations to the same lowered event. That projection erases time and cannot on its own establish preservation of timing obligations. [R250-216]

The selected-order controls preserve action, complete successor and nonce and give an involution. If the old and proposed label lists are literally identical, the transformed command is itself unchanged. General trace transport requires transforming initial/final state, every command-bearing event and corruption payload together, as well as receipt keys; concrete application equality retains either value of the same faulty-gate Boolean. A set-level path equality alone still does not identify commands. [R250-228]

The shared trial takes its Boolean from the unchanged compiled attempt and lifts success into a shared-state landing; a rejected attempt slot instead has a hold-event witness. Finally, trace existence and progress have different premise sets even in the shared controller. Valid paths and authentic requester suffice for a reference run trace of $N(2q+2)$ events, without clearance or an all-good witness. Keeping an already achieved common successor needs only that every later command declares that same successor, by the trial's unchanged-or-declared-successor dichotomy. Obtaining that successor initially needs the stronger progress premises in §10.7. The public source schedule preserves every supplied path, fixes its command list under service decoration and gives distinct complete commands through increasing indices/nonces, even if a path is repeated. These structural facts are not fresh execution evidence. [R250-204] [R250-249] [R250-237]

The generic `JoinTrace` provider lifts consistency to authorization at each actual landing's **pre-state**, damage safety, determinism and epoch monotonicity. Preservation of an additional plant invariant requires a separately supplied `effect_preserves` proof. The institutional `Reservation` condition remains external; a gate equation is not a derivation of real consent. [R750A-570]

`SimulationControls` also makes the direction of refinement observable. Extra concrete vetoes can close a gate that is open in the abstract state, so a safety-preserving `RootRefines` relation has no automatic converse admission theorem. Its wrong-veto-direction and missing-selected-commitment targets preserve the rejected strengthenings. Preparation and delivery expansions leave receipt and certificate sets unchanged; the abstract witness cannot manufacture either. These are exact source assertions and controls, not newly executed tests. [R750A-578]

[R750A-570]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/98b03f1f0f75c2b0fbefb2c96f2e1c00fc7b2778ac12c36e0976a03d5678748b/JoinTrace.lean
[R750A-578]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9b4df2b46e0ff573cf82942195ccbda592407a2b47ade216b9768805e7d72e9f/SimulationControls.lean

### 10.11 Exact criteria, opaque search and the limits of replay

#### What criterion transport preserves

The conditional transport result separates several claims that a single word such as “equivalent” would conceal. Defeating every eligible authority witness is not the same proposition as rejecting the whole object. Exactness relative to a witness is not global injectivity. Transporting a judgment robustly over the represented worlds gives truth at an actual world only when that world is included and the evidence-soundness premises hold. Likewise, one repair available separately in each world need not determine one action selectable from the actor's observations. Infinite recurrence of successor states does not itself fix the truth value. These distinctions are part of [CriterionTransport](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/08d5efa5dc92642e6aec422389928314a0cd39c5a64f6f63032a369825905edc/CriterionTransport.lean), not new warrants for authenticity, adequacy or legitimacy.

#### Why opaque failure creates the cap

The earlier [OpaqueSearch](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2db9c51cecebf0f4d680c1b4fe82d9c3bbc8cfcf63920aa7f01ed1cc4e6ce3bf/OpaqueSearch.lean) argument allows the failure reply to depend on the trial ordinal and selected path, but not on the hidden bad set. Before its first success, an adaptive policy therefore follows the same all-failure history. Its first N trials form a portfolio of at most N paths. Guaranteeing success against every allowed bad set requires their complements to cover all those sets. Conversely, enumerating a minimum prepared cover attains the mathematical bound. That enumeration is noncomputable in the source: attaining the bound does not establish an efficient executable cover-construction algorithm. Informative failure replies can invalidate this reduction. This earlier deterministic argument does not inherit the separate later randomized theorem in the T07 covering treatment merely because both concern opacity.

[ExactCap](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2cf94c485255f644b3d369b0e247d1c1d6d3bd228753e9fb12f40750b47d220a/ExactCap.lean) specializes the cap to C(m,m−q,k), under q≤m and k≤m−q. At m=3k+1 and q=2k+1, each complement has k members, so every k-element bad set must itself occur as a complement and the exact count is binomial(3k+1,k). The canonical observations include a truthful effect receipt; the arithmetic does not prove that receipt truthful. [FullCommandInterface](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4404a9dde8c580e01e1b752769e2a5a04a3af71e9b42b21a0d42b77b1fd2c746/FullCommandInterface.lean) retains the fixed body and fresh nonce while accommodating arbitrary reply payloads under its world-cardinality assumptions. Neither a cap nor its attainment authenticates the body or supplies permission to execute it.

The [negative controls](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0f076b4569ee9ff41c0490f99ad08f6031e5221494d898e3f349accb0f9363bb/NegativeControls.lean) make the missing hypotheses concrete. On four labels, P={0,1,2} and T={0} satisfy T⊆P, not T⊆Pᶜ, and P does not avoid T. The three singleton blocks {0},{1},{2} fail to cover the missing world {3}. A reply that reveals the hidden bad set distinguishes {0} from {1} on the same failed path, contradicting a common opaque failure reply. Finally, the larger block {0,1} covers two different singleton worlds: the equal-cardinality premise is essential to the exact binomial argument. The source's axiom-print commands are not new observed audit outputs.

#### Exact replay and evidence roles

Every successful local installation or repair leaves both rule version and draft revision nondecreasing. After an installation succeeds, its exact old command cannot execute at any later plant whose rule version is at least the post-success version, even with an arbitrary later policy and time. Repair has the corresponding result for draft revision. These are the [reviewer-monotonicity source's](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1a309a2ea8ca97510f94160db9ccbd5cea346e04f4e12403eabbb589bd91701a/ReviewerMonotonicity.lean) conditional results, not an assumption that every uncontrolled environmental transition is monotone. Separately, the [old-action fixture](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/06be349c33d5277aeceb05d8de8c9292f9f2d80320118fab64581ee475560510/old_action_still_authorized.lean) deliberately asserts authorization against the revoked epoch; it is a negative current-authority control, not evidence that such authorization holds. No new compiler rejection or axiom-audit output is reported here.

The [rule-installation replay program](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/13bd258591c255005e0661291643b34364c98607c388b2a09961936beee39adc/ReplayRuleInstallation.lean) decodes CSV, executes the modeled transition and projects output; its presence is not an additional execution receipt. Audit inventories and serialization programs must retain those operational roles rather than being counted as new proofs.

The exact `ReplayCriterionFixtures` interface is a separate17-numeric-field CSV harness for typed criterion state and commands. It emits application, revision, draft-tag, history-length and source-preservation coordinates to `lean_actual.csv` when its main routine runs. It trusts its generated fixture rows; neither its permissive decoding nor its output filename authenticates an external parser or a security endpoint. Its referenced input was not opened and its IO was not invoked here. This preserves the reproduction role without confusing it with the earlier12-field criterion-installation harness or with newly observed replay evidence. [R750A-530]

The corresponding Python fixture bodies make the two finite domains auditable without conflating them. `shared_fixture_check.py` generates the 17-coordinate draft-repair product and projects index, acceptance, revision, draft tag, history length and source preservation; its comparison detects both missing rows and unexpected trailing output. `rule_install_audit.py` generates all 2^12 installation combinations and compares eleven output coordinates, with a separate equal-length check. These are generated trusted fixtures, not hostile-input protocols, and agreement of those projections is weaker than equality of every state field for every Python value. The report's 393,216 draft rows and 4,096 installation rows remain historical results. `bounded_audit.py` separately specifies the execution conjunction, finite representation-fibre examples, unmatched revoked-recipient model, witness-relative defeat control and corrupt-gate deletion. Its 40-string illustration finds 36 ordered normalization collisions and 468 one-byte-prefix collisions; it supplies no hash-injectivity or general Python refinement theorem. [N250A-017] [N250A-019] [N250A-021]

The original dynamic source and its checkers expose additional execution obligations. The ordinary `World.attempt` consults the global descriptor only to classify an already permitted effect; it does not use that descriptor as a protective veto. The controller uses actor-held certificates, and its run-all batch does not stop on an untrusted success receipt. Controls preserve the alternatives: stale cached votes, post-check payload substitution, target-only permission checks, too-small cancellation certificates, an already-budgeted downstream bypass, an omitted common selector, instantaneous rather than lifetime faults and immediate external revocation. The seven-scenario source-replay driver imports the accepted dynamic module and exercises reordered delivery and those specified controls; the false-claim driver requires kernel reduction of seven concrete false propositions, rather than treating any compiler error as success. These import, fixture, compiler and artifact-writing roles remain executable dependencies. Their source understanding here is static: no driver, test, imported module, Lean build or referenced primary source was executed or opened to validate those historical results. Assertions in the Python model/check suites and their expected typed inputs are not a hardened parser or an all-input validation guarantee. [N250A-026] [N250A-028] [N250A-032] [N250A-034]

[R750A-530]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8d48109d936200fae905eb981f7ebc9c1005de5b0f7caf1d4d08e8d0f7412dbe/ReplayCriterionFixtures.lean

### 10.12 Shared roots, explicit mutation controls and exact embedded inputs

A shared store is not a collection of independent attestations merely because several labels address it. The mathematical environment fixes one nonempty alias class A, actual-root faults F of cardinality at most b, b≥1, and b<m−|A|+1. Its induced label fault bound is B=b+|A|−1<m. Repair and revocation thresholds obey m+B<q+r, q+B≤m and r+B≤m. The source policy at index e has epoch e. Actual roots, the alias class and lifetime faults are environment parameters, not observations supplied to the controller. Label i is good precisely when its actual root is not faulty; equal roots therefore have equal goodness. Unused ambient root names are not extra roots available to events. [R250-X014] [R250-X161]

The state contains epoch, actual-root stores, pending status, acknowledgment labels, epoch certificates, command-specific cancellation acknowledgments and plant. Initially epoch is zero, every store has source policy zero with empty recorded sets, and the plant is supplied. A request sets pending and clears acknowledgments. An acknowledgment records a label and, if good, revokes the current epoch in its actual-root store. Completion requires pending and exactly r acknowledgment labels, saves their certificate, advances epoch and clears pending and acknowledgments. Delivery accepts certified positive epochs no later than current epoch, but updates the stored descriptor only when the delivered epoch is newer. Preparation inserts the complete command into the addressed store, requiring path membership, a valid path and either a faulty label or the stated envelope. Cancellation records the addressed label and, when good, updates the shared cancelled set, requiring path membership and either faulty status or the command's recipient. Closing requires more than B cancellation acknowledgments and leaves the state unchanged. Landing changes only the plant and requires a valid path plus permission at every selected good root. Hold changes nothing; corruption may arbitrarily rewrite one lifetime-bad actual root. Finite traces compose these steps, and reachability starts from an initial plant. Preparing or cancelling through one label consequently affects the same actual store seen by its aliases. These definitions do not establish a scheduler, transcript equivalence or physical implementation. [R250-X014] [R250-X161]

The two retained AliasModel variants deliberately expose distinct failures; they must not be promoted together as a positive implementation. Source14 replaces the single-label acknowledgment insertion with the union of **all labels sharing that root**, while retaining the assertion that the result equals insertion of just i by reflexivity. For a distinct alias j not previously acknowledged, the new definition adds j and the displayed claimed equation does not. Shared storage does not license manufactured label receipts. Source161 keeps single-label receipts but substitutes b for the inflated B in the label configuration, while still supplying proofs and thresholds stated at B. With a two-label alias class and one faulty shared root, one actual fault taints two labels, so the actual-root budget alone cannot bound faulty labels. The unaffected structure and store-sharing definitions above explain what each mutation changes; neither mutated proof text is counted as freshly compiled or validated. [R250-X014] [R250-X161]

The corruption controls retain the complementary positive boundary. SameGoodState cannot hide a changed store at a good actual root: its good-root equality immediately contradicts that change. Nor can it hide a fresh acknowledgment, because acknowledgment sets are shared observable coordinates of that relation. An arbitrary rewrite of a bad root, however, leaves the exact gate Boolean `applied E C k who time badOpen` unchanged for either value of badOpen. This is equality for the same envelope, requester and time, not immunity to altering good stores or receipts. [R250-X002]

Erasure of bad writes does not erase their time cost. If a woven service has core length259 and added corruption count a>0, the actual trace is longer than259. In the seven-label fixture, conditional on q=5 and the stated source-at-zero equality, every supplied badSync and bad-reply function has compiled specifications and a service with21 specifications and259 core events. **Every** realized finite trace woven from that service ends at the installed plant, has length259+a, exactly one installation and zero repairs. The proof derives the counters from the realized endpoint and trace invariants; it does not assume a successful trace as an extra caller premise. The universal conditional on a realized trace is not a claim that every external scheduler supplies one. The source's axiom-print commands are inspection requests, not fresh output here. [R250-X002]

A different exact-input fixture embeds3013 bytes as a literal list of natural numbers and states its length by reflexivity. Its namespace is OperationalJoin.Offset.NativeFixture; its external authenticity is explicitly separate. The embedded text concerns Candidate E, whose historical five-way partition distinguishes retained meta-standard, trans-state standard, holistic fixed point, primitive normative fact and relativization/error theory. It records no counted cold audit and retains DEFERRED_INSUFFICIENT_AUDIT. Cross-lane proper-function, defeater, warrant, recursive partition and distributed-unification work must not be backfilled as Candidate E's recovered historical theorem. [R250-X225]

The embedded substantive constraints distinguish result correctness from pathway adequacy, same output from same proper function or warrant, and integration of reasons, defeaters, provenance and authority from consensus or state similarity. Reliable correction or query optimality does not select a function-fixing account or establish Wisdom. The ten alternatives are frequency, causal role, organization, selected effect, design, learned objective, success surface, teleological, Plantingian and fitrah accounts; each needs its corresponding evidence. Open burdens remain a genuine independent audit, noncircular bearer and norm-source identification, distinctions among teleology/design/selection history/role/policy/source order, proof or refutation of partition-synthesis, and distributed evidence without laundering common roots. Connections to Candidate N, R5, TAC/SAC, PRH, daee restoration and transcendental ascent require typed reductions. Consensus does not create independent evidence, epistemic unification does not establish metaphysical unity, and engineering validation does not establish theology. Retaining the exact byte fixture therefore preserves an input and its deferred-status warning, not scientific adoption. [R250-X225]

[R250-X002]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/002d91939fdf407dc76cdf097a13428a6b4e927cc18a668f4030aea1bfc2439a/ReviewerCorruptionControls.lean
[R250-X014]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/038f725316aea02a3330401ac33208b3a72bb7df32a2d955668b27b4d70a6e8f/AliasModel.lean
[R250-X161]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/310d07172eb6c03277408763316c8d5cbaa1b9b0904785a0ca6cad9c23b0d85e/AliasModel.lean
[R250-X225]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4158d835b3720ab328c839529d0d390b0773128dd1f8a91e36528583db5dbdb2/PinnedSource.lean

<a id="third-cohort-b-cancellation-address"></a>

**A third exact variant has an address mismatch, not a new shared-cancellation proof.** The selected `AliasModel.lean` with native blob `0487ae8ac2fb669148faaf244a0612ff1598ebe8` differs from the two mutations described above. Its `cancelAck` inserts just the responding label into the command's acknowledgment set, but writes the updated root at `some i`; the old root is read at `E.rootOf i`. Its `shared_cancel` conclusion instead concerns the store at `E.rootOf j` when `E.rootOf j = E.rootOf i`. [T750B596]

These coordinates cannot be exchanged without an argument. If a good selected label satisfies `E.rootOf i ≠ some i`, updating the function at `some i` leaves its value at the actual shared root unchanged. If that shared store did not already contain the command's tombstone, the displayed update therefore does not install the tombstone there. The same file's acknowledgment, preparation and corruption operations address `E.rootOf i`, making the exceptional cancellation address consequential rather than a uniform change of representation.

This is a local source-level inconsistency in that exact object. Its imported root-map body and compiler outcome were not newly checked, so it is not a reported build failure, a demonstrated deployed vulnerability, or a judgment on another same-basename edition. The affected shared-cancellation claim must not be credited from this variant without resolving its intended role and supplying the relevant source/build evidence. The positive shared-root arguments above retain their own separately identified witnesses; neither receipt preservation nor their cancellation results are obtained by silently correcting this archived body.

[T750B596]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a004284259ab3df2625ee260cded7d9d2cd592fd122d90bec1c31b2bf0fe5a2f/AliasModel.lean


<a id="final189-b15-positive-shared-root-provider"></a>

A distinct positive AliasModel body retains both the inflated label budget B=b+c−1 and single-label receipts. For a good addressed label i, its cancellation update writes the actual address E.rootOf(i); for a faulty label the root store is unchanged, although the addressed receipt is still added. Under that good-label premise, the shared-cancellation theorem places the tombstone in that same store for every alias j with E.rootOf(j)=E.rootOf(i). This is a different exact source object from the three altered variants above, not a repair silently made to any archived mutation. Its transition language still assumes the fixed hidden root map, fault set, thresholds and authentic source; it supplies no physical scheduler. [F189B-843](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e443dadbbea18b0badf3cb788741bbc25c33e7ba63b81c7b642e265ef6d977b8/AliasModel.lean)

The accompanying preservation source realizes the one-way relation used in §10.13. A concrete preparation expands into abstract preparations only for selected labels in the same alias class. Acknowledgment and cancellation add only the addressed receipt, although shared storage may add vetoes visible through other aliases. Delivery expands over aliases, and corruption of a bad actual root preserves every good-root relation. Observable acknowledgment/certificate coordinates remain exact, while concrete revocation/cancellation may be stronger and commitments are filtered by selected-path membership. These are local preservation lemmas under the supplied Refines relation, not literal equality of shared and independent states or invented receipt events. [F189B-834](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e211d17a45518fc8b2878ffa62838ea894d65af64c5c365496d0898fbc3ba236/AliasPreservation.lean)

### 10.13 Refinement preserves effects, not merely successful replies

The shared-root results above have a positive implementation route and two exact source variants that do not support the same conclusion. These must remain distinguishable in a consolidated account. A successful Boolean is evidence of a physical successor only when the implementation actually performs that successor update and the refinement theorem binds that very definition.

#### Source variants and the meaning of success

The three retained `Composition.lean` bodies share names and substantial surrounding definitions, but are not interchangeable. All distinguish rule installation from draft repair through the actual `localStep`, including contextual permission and the rule's exact-byte acceptance. In the source at [R500-327](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/56b4f1c0e119e8d63521020354efe0362171333acfe675651a960e6c2863d8e3/Composition.lean), however, `attempt` returns `(w,true)` when the gate opens: its world is unchanged. Its `runBatch` calls that definition. Thus that body's success flag alone cannot establish installation of the proposed successor, even though the adjacent comment describes the only mutation event. This is a literal definition-level observation, not a fresh compiler failure or a refutation of a separately bound implementation.

The source at [R500-413](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6c1b3027df89d67ca999a45fc3236e5718af26fbc304ef047907213277a84e10/Composition.lean) presents a different boundary. Its cancellation operation records complete envelopes, but its `rootPermits` combines commitment and `Eligible` without checking that the envelope is absent from `cancelled`; `Eligible` itself checks requester, revocation and `localStep`, not that missing tombstone predicate. Its storage of a cancellation record therefore does not establish the live exclusion theorem of §10.7. Positive `HistorySafety` and lifecycle-cancellation results belong to the definitions they actually import. They cannot be transferred by a matching filename or a similar record layout. The unchanged earlier composition source and its fixtures retain their own binding; none of these three textual variants is silently repaired or declared equivalent by this exposition. [R500-298](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4fe230ad25655c303ab64970b526bbc7d724fc619758541b697afcfc9c989e88/Composition.lean) [R500-440](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/75a06e846cdb5d43c29ede7ee914347ab3abbb705b568b1933d0a90ea1de7621/HistorySafety.lean) [R500-422](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/716502096735929bc1dad61f21898fd1ee74d50176f60b71738c7b1f59537a23/LifecycleCancellation.lean)

This distinction also prevents two mistakes about local tests. A target-only check is not a permission check; omitting durable revocation is not harmless; and permitting unmediated damage changes the transition system. The negative files that ask Lean to establish those stronger claims are rejection probes, not additional positive results. Installation/replay/expiry tests and fixture constructors remain executable evidence interfaces, not newly observed executions here. [R500-344](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5bbc30b7ab29459105fcd3eb89bbbbfb7f74972a2c6c20767b5e84dfeb9e12a2/target_only_checks_preserve_permission.lean) [R500-392](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/65540e49510fca4291e83089de5e149a81c4e9a96d44889753d8c37397459aae/revocation_omission_is_safe.lean) [R500-431](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/74154ee80afd1637ed231536c5cbfadc20fd30bf5f282ce77485e0e68ab17ca8/mediation_is_redundant.lean) [R500-410](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6b616bdb2b9da070daba086f92128e0e4d325dfe0bfac6d61489a0f79e6eda3f/LocalTests.lean) [R500-258](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/486836776e562f1cd15c919d68c25f6851b97c4e64b88cd7282b700d3c9d700d/Fixtures.lean)

Three separately retained RED stages have still different limits. Composition.local-red defines localStep to return none for every input, so it supplies no successful local adapter. Composition.batch-red contains the contextual local adapter, live envelope checks, successor installation, cancellation and revocation arguments, but defines runBatch(w,actor,a)=(w,[]); it supplies no scheduled portfolio. Composition.clock-red replaces that stub with the four-path proposal/prepare/attempt/cancel fold and retains conditional local and effective-policy refinements. Its added actor.observedTime field is unused: proposals receive current.now, and the service phases do not advance that clock. Thus this body does not establish an independently timed actor observation or elapsed-time guarantee. These are exact stage-specific definitions, not failures of the separately bound positive implementations or newly obtained compiler results. [NEXT-R18-088](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2de18bdb414fdf658126a8add89ed1018eca2155a61422ff409f6605d60f132e/Composition.local-red.lean) [NEXT-R18-223](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/44e0af0aff22b70c66bdb23b1990cd8d0fffac98a1f87cd5c6123809cb2589df/Composition.batch-red.lean#L424-L452) [NEXT-R18-083](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2d0c844f1184f415a41a7b2cb57c7632f43b60a27fa667a53055c241603bf7bb/Composition.clock-red.lean#L268-L285) [NEXT-R18-083](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2d0c844f1184f415a41a7b2cb57c7632f43b60a27fa667a53055c241603bf7bb/Composition.clock-red.lean#L424-L453)

Composition.dynamic-red retains the contextual local adapter: its written refinement arguments distinguish criterion installation from draft repair, retain the source/custody frame, update the corresponding version and history, and exclude replay of the same fixed action after success. Proposal can package an accepted local successor. Its dynamic entries are nevertheless explicit stubs: both prepare and attempt return the unchanged world together with false for every input. This stage therefore supplies no active preparation or landing through those entries, regardless of the local adapter's conditional results. It is distinct from a localStep that always refuses, a batch that schedules nothing, and a clock field that is unused. These are source definitions and dependency-relative local arguments, not a failure of a separately bound positive dynamic implementation or received compilation evidence. [NEXT250-Q25-091](../research/t20-v6-20261012/sources/8fa56b73e351e4d20e9340e44c6bee754489a0b8dae01e59952fa284d596b448/Composition.dynamic-red.lean#L48-L86) [NEXT250-Q25-091](../research/t20-v6-20261012/sources/8fa56b73e351e4d20e9340e44c6bee754489a0b8dae01e59952fa284d596b448/Composition.dynamic-red.lean#L88-L210) [NEXT250-Q25-091](../research/t20-v6-20261012/sources/8fa56b73e351e4d20e9340e44c6bee754489a0b8dae01e59952fa284d596b448/Composition.dynamic-red.lean#L243-L252)

The separate lifecycle-red composition has progressed beyond the dynamic-red stubs: propose computes a successor through localStep, prepare records commitments on a distinct in-range path of the required size, and attempt installs the proposed plant only when the selected gates open. Honest gates check requester identity, epoch revocation, envelope cancellation, commitment membership and a fresh localStep against the same actual plant. The charged-path argument, with tainted cardinality at most the budget and path cardinality strictly greater than it, yields one honest local-policy step and hence preservation of the source. The earlier local refinement, frame, version/history, non-replay and goal-persistence arguments retain their stated premises. This does not authenticate an effective global policy: cancellation still returns failure, transition certification returns none, delivery leaves the world unchanged and actor receipt leaves the actor unchanged. Those four lifecycle operations remain explicit RED placeholders despite the functioning prepare/attempt layer. [NEXT250-Z50-202](../research/t20-v6-20261012/sources/a571376a3c5a0d433a946b71d63f076d49da9a2a1acdfc071262caf549cb2304/Composition.lifecycle-red.lean#L48-L86) [NEXT250-Z50-202](../research/t20-v6-20261012/sources/a571376a3c5a0d433a946b71d63f076d49da9a2a1acdfc071262caf549cb2304/Composition.lifecycle-red.lean#L88-L210) [NEXT250-Z50-202](../research/t20-v6-20261012/sources/a571376a3c5a0d433a946b71d63f076d49da9a2a1acdfc071262caf549cb2304/Composition.lifecycle-red.lean#L253-L321) [NEXT250-Z50-202](../research/t20-v6-20261012/sources/a571376a3c5a0d433a946b71d63f076d49da9a2a1acdfc071262caf549cb2304/Composition.lifecycle-red.lean#L324-L328)


The race harness enumerates 80 revocation, 60 cancellation and 20 open/withheld cases per supplied byte payload, plus stale-source, expiry, wrong-requester and full-successor controls. Its unseen external-consent-loss and insufficient-tainted-acknowledgment examples deliberately violate positive premises; they delimit the model rather than justify unmediated consent inference. These are assertions in the exact IO program, not reported test passes. [R500-301](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4ffbae78d25ded6d7bc3d33b018fdf4299076b1727eb6431ccd2b84136f2e72b/RaceTests.lean)

A fourth exact `Composition.lean` body has a stronger cached-permission change than the missing-cancellation variant above. At lines147–148, `rootPermits` ignores its plant, time and requester arguments and returns only membership of the envelope in `root.commitments`. `gateOpen` uses that result, and an open `attempt` installs the stored successor. Cancellation and certificate revocation append tombstones but do not remove the old commitment. Thus recording those tombstones does not close that cached gate in this object; the adjacent comment claiming live rechecking is inconsistent with the definition. This is an exact source-level finding, not a new compiler run, an assertion of canonical deployment, or a repair to this archived variant. [R750A-524]

The separate `DynamicTests` program expects replay rejection, late-cancellation rejection, fresh-nonce success, actor ownership, stale-epoch revocation, delivered descriptors, duplicate-ack rejection and cleanup after revocation. Its replay, cancellation and revocation expectations would conflict with the cached definition **if** its unresolved `Fixtures` import selected this exact Composition object. The program is not test output, and that imported binding has not been established by these source reads. The correctly bound positive lifecycle results above remain unaffected; no same-basename substitution is permitted. [R750A-545]

[R750A-524]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8a998e2027a8cf0634db468d5c6850354e4fba99760bafc5f33e22d6c10e364e/Composition.lean
[R750A-545]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/924d37068f63b2c0d0448f6563f7f23b628a819876b4b5261fd0a2334a8752e3/DynamicTests.lean

A further exact `Composition.lean` variant preserves the full-envelope mechanism but replaces the repair branch's additional installed-rule test by the literal condition `if true`. Its preceding comment still advertises rule-constructor and interpreter checks. The branch continues to call `TypedCriterionGuard.execute`, so this is not a claim that every repair guard disappears; it is the precise omission of the advertised additional condition. Neither the comment nor a theorem or test imported through an unresolved same-name dependency repairs that omission. The soundness of the separately bound positive implementations is unaffected. [F939A-808]

The independent IO-test source specifies 140 fixture/path/taint cases, tampering with twelve successor fields, time boundaries, delayed certificates, complete-envelope cancellation, stale observations and an all-tainted out-of-scope case. It provides reproducible test obligations, not their outcomes or an established import binding to the variant just described. `TestRunner` would read source bytes, invoke five imported test groups and then write artifacts before its terminal PASS string. Neither that runner nor these tests was executed for this incorporation. [F939A-809] [F939A-771]

[F939A-808]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/db77fe866b6352db7225535729ed71dc7d9b185b3b215c12752278d1876dbdd4/Composition.lean
[F939A-809]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/db9041027ecf36b058a6c9f62f2dec495882066f6a3b09f0f4eeb4f79801a26e/IndependentTests.lean
[F939A-771]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d31ae8c4304b978bbd71521f84b723329635c9997c222e965362cddffbfc198c/TestRunner.lean


<a id="final189-b06-inductive-state-and-time-translation"></a>

The direct common-machine invariant is established by induction over the explicit operations and finite traces. It retains authentic, nonfuture good-root descriptors, past and pending revocations, selected-label cancellation receipts and the good-root veto behind each closed command. Preservation of a helper root update is proved from its local conditions; it is not an extra transition rule granted a global landing guarantee. This supplies an earned invariant for the common model without moving source authentication into a Boolean reply. [F189B-829](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e1424f4f1e33c07044bf97650630ef881d57670f0195236223da2cf5a981672e/JoinInvariant.lean)

The original-history specialization then proves a bidirectional translation of every event, including corruption, and of complete traces. Its state maps are inverse even on damaged or unreachable states, and its attempt correspondence is not restricted to successful safe executions. Prepare and land timestamps can be erased, or arbitrary timestamps supplied in the converse translation, only because this exact original admission predicate ignores time. This is a structural equivalence for that specialization, not permission to erase time from the later lease-sensitive runtime. [F189B-847](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e6c0c3e0b8b1091747fe346005bd150d568bf9a3cee344fc435f52f3192fe678/OriginalTranslation.lean)

A further exact `Composition.lean` variant, SHA-256 `ffc641d1fefe312d12afed12fe94f6f91035507b0215a85c4cc18aecab98abe0`, retains complete successor binding and cancellation but omits the revoked-epoch guard from `Eligible`. Its literal eligibility condition is requester equality, absence from `root.cancelled`, and the full `localStep` equation. The earlier exact source at index745 additionally requires `e.action.epoch ∉ root.revoked`. The weakened body still writes revocation memory, but that storage cannot supply the omitted eligibility test. Revocation conclusions of the guarded edition therefore cannot be transplanted by basename. This source-level distinction is not an assertion of deployed behavior, canonical adoption, intent or a freshly observed runtime failure. [F939-C937]

[F939-C937]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ffc641d1fefe312d12afed12fe94f6f91035507b0215a85c4cc18aecab98abe0/Composition.lean

#### Shared memory requires a relation rather than a literal snapshot

A reachable literal independent-label machine records good-root commitments and cancellations only at selected command-path labels. In the shared-root machine, preparing selected label i also changes its actual store as seen through an unselected alias j. When j is good, a literal per-label identification would require the corresponding independent machine to contain an out-of-path commitment. Its invariant forbids that. The obstruction is to this literal identification, not to every simulation or implementation. The concrete controls demonstrate both the single operation and a nonvacuous typed installation history. [R500-300](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4ff96a4895ba0ddb480b2dd269a53787556612bb3e7c01e362b05f5bfcfcc501/ModelControls.lean) [R500-468](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7d08dec17db87752eab153a28fbc9f75933a44b0cb57669ed823113f6ca78778/AliasObstruction.lean) [R500-289](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4e9307cc7d3e955373bfef62e8f4f132702619d63d61d28c9c4b785de1edc3bd/ReviewerTypedControls.lean) [R500-320](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/551eca9b5201b8facfc8d46cdcd9f6d28f77fbad7710761bf9ce6f316b0f0da1/AliasTypedWitness.lean)

The positive relation instead permits extra concrete vetoes and masks commitments not justified at an abstract label, while preserving the shared observable coordinates. A selected concrete preparation may expand to several abstract preparations, one for each selected alias needing that commitment. This is a weak forward safety simulation: one concrete event may have a finite abstract event-list witness. Induction yields a reachable abstract witness for every reachable shared state, and admitted current-action and durable-cancellation consequences transfer along it. It is neither a literal independent snapshot nor a claim that the auxiliary abstract events physically occurred. The reviewer example explicitly preserves the empty receipt sets and introduces no abstract landing during its preparation simulation. [R500-481](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7fe24919a26cb40031de165cc295bc335de338942b1e69100b312a6b71aa30df/AliasRelation.lean) [R500-368](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/612541253cdbb0e12394aa435fed271435751210936abdc34cf149284360d348/AliasSimulation.lean) [R500-347](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5c58385bf38d938211b1ea0a40fc99b0c5af282c622ef323fa7569a15205617e/ReviewerSimulationControls.lean)

The separate `AliasRuntime` construction is narrower. It duplicates one shared store into a literal snapshot to characterize an immediate attempt. The snapshot need not be reachable as an independent-label lifecycle. The snapshot bridge does not compile certification, preparation and cancellation histories or manufacture certificate rows; its converse admission direction retains its specified faulty-gate permissiveness. These two representations solve different problems and must not be substituted for one another. [R500-310](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/52088475e303e247a73746ee1d9936c373010bd973b31378c977dfe19dc1fa74/AliasRuntime.lean)

The native finite-state route goes further at a different, explicit boundary. With `RoutingMatches`, native preparation and cancellation updates and their emitted events refine the corresponding shared-store steps. Native success both establishes shared landing and writes the exact successor plant; failure retains the modeled state according to its branch. Closing uses the count of cancellation labels, not the number of distinct actual stores. For a reachable viewed state, `native_success_full_effect` also recovers the actual current-source `localStep` and the resulting plant. Reachability/authentic history, routing agreement, full command and query time are genuine premises. [R500-257](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4830ec8996c4c474f33ed7a8314e07ac369966ada1fab497aa2367d3514afad0/NativeRefinement.lean) [R500-321](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/55346fee044a71705b829399d5ff02e904c01312323a5e750d9052f653022c28/NativePrimitives.lean)

A raw snapshot does not supply those premises. The diagnostic snapshot with claimed epoch 99 can return `applied=true` while the actual source policy at 99 rejects the action. The other diagnostic establishes one exact source-step equation, not validation of every auxiliary altered envelope defined beside it. A complete implementation statement must bind the successful gate, source policy and actual history, rather than laundering a snapshot's fields as an authority receipt. [R500-455](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7a23da5d8cb3357168886b2ea8307d3ecc9306b963743b7345776c62f466a0af/Diagnostic_snapshot_does_not_authenticate_epoch.lean) [R500-336](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/58ff61080f8beb02191d16c22451fb0048b605684c41db092309ed67d8afd04d/Diagnostic_fixture_direct_source_step.lean)

The selected `AliasRelation` gives the precise one-way relation used above: abstract commitments are exactly concrete commitments **filtered by membership of the addressed label in the command's selected path**; abstract revoked and cancelled sets are subsets of their concrete counterparts; descriptors agree. Additional concrete vetoes are allowed, so concrete permission transports to abstract permission on a selected good label without a general converse. This exact body contains the selected-path conjunct used by its permission proof. It must not be conflated with a different historical same-named object whose commitment field omitted that conjunct. [T750-C709]

The native controls separately test requester, successor, lease, policy, epoch, commitment, tombstone and path shape. Shared root storage can hold a veto for an alias without providing that unaddressed label's cancellation receipt; first-match receipt lookup and distinct-label counting remain explicit. Ordered-identity controls exhibit complete commands with paths `[0,1]` and `[1,0]`: their supports agree, their identities and commitment keys do not, and sorting maps both to one command. Repetition of an identical memory entry can be removed under membership semantics, but permutation of distinct labels inside a command cannot be treated as an injective transport. [T750-C708] [T750-C714] [T750-C737]

[T750-C709]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bf5a0dfba95799400911b35eb86e0058689261252abf9ffc0e27ab2e58eaa128/AliasRelation.lean
[T750-C708]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bf437d2c57bd052bbd241148e5376fd8851f5649dd1b8057b31265dac7d04d39/NativeControls.lean
[T750-C714]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c127a7496f67428cc7114fdb0df0224410850b68297183123672ff246f769a7c/IndependentSortingWitness.lean
[T750-C737]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c86686b73f0a9d2d4692957cf6349cc1ca25f6334bb6c930a0816eb8166ea66a/OrderedIdentityControls.lean

The direct finite-data and reification providers distinguish a stronger Boolean statement from a stronger safety statement. `NativeData` uses finite first-match tables and one effective shared store per routed root. `setRoot` prepends a new row, so older rows for that root may remain shadowed; malformed historical envelopes remain stored and are ignored only by the typed proof projection. Native operations do not invoke that projection. `NativeReference` proves equality of the application Boolean with the shared reference for **either** value of the same faulty-gate Boolean, under `RoutingMatches`, even at arbitrary raw finite states, for the same bounded, duplicate-free complete command. It also proves equality of the projected attempt result. Reachability and policy authentication are not premises of this representation equality; they remain separate premises for the current-source effect conclusion. The ordered complete command is identical on both sides. [F939A-764] [F939A-787]

The separate executable-kernel bridge preserves more than this set-valued projection. Its stateView copies every raw field, including defaults, root-row and receipt order, duplicate rows and malformed historical memories. Slot-by-slot and list induction identify its entire outcome with the imported Native implementation, including the mapped event list; distinct-label counting is equated with Finset cardinality for closure. This implementation correspondence has no RoutingMatches or reachable-state premise because the routing fields and raw state are carried unchanged into the comparison. It does not itself authenticate a policy, prove current-source safety, or replace the epoch-zero entry restriction and exact annotation checks. [SUB250-U25-029](../research/t20-v6-20261012/sources/539a03f6fa831bc63a8a0332f18471b4d814c49cc650bd12f281308b2eb0bf65/ExecutableBridge.lean#L7-L234) [SUB250-U25-031](../research/t20-v6-20261012/sources/53acb41526795c9266a44eda687ee2633281b7a0eece436e280c4bb41877ba68/ExecutableKernel.lean#L9-L273)

The separate executable-program bridge extends the representation comparison from kernel operations to ordered command issuance, ordered programmes, annotation validation and compilation. Its annotate and compileOrdered equations map the complete successful specification list and preserve none on rejection. A further prefixed-run equation explicitly maps the event list, including the displayed m hold events, rather than inferring trace equality from the final state. The final runInitial equation includes the epoch-zero entry branch and the positive-epoch refusal branch as well as the compiled outcome. These are source-relative equalities against the imported Native and executable definitions, not independent inspection of those definitions, policy authentication, reachable-history safety or an observed executable run. [T33-087](../research/t20-v6-20261012/sources/f40103ef349e7a79f1a979da79458dcde98fd262911b98ca5cb2b12121c0eb5d/ExecutableProgramBridge.lean#L6-L62) [T33-087](../research/t20-v6-20261012/sources/f40103ef349e7a79f1a979da79458dcde98fd262911b98ca5cb2b12121c0eb5d/ExecutableProgramBridge.lean#L64-L101)

The shared-alias review also restricts legal addresses to actual image roots; unused Option padding remains untouched. Preparation and delivery preserve receipts, and a stale delivery is identity. Exact revocation quorum is not a lower threshold: in the specified r=5 fixture, six receipts do not satisfy it. One reply does not close the command, and literal cancellation pullback remains obstructed. These controls preserve the relational refinement rather than manufacture independent-label acknowledgments. [F939A-810]

The storage boundary is concrete. Servicing two cancellation labels in opposite orders yields receipt lists `[2,0]` and `[0,2]`. The native states are unequal, while their projected cancellation Finsets agree. This is a valid set-valued abstraction, not equality of raw states, permission to reorder the complete command, or proof that an observer cannot see the difference. [F939A-777]

[F939A-764]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d0c2e785b48bb870a4cb990a3794c164e508948a1ecde00ac07b14e7363069cc/NativeData.lean
[F939A-777]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d40af4e098a319b49c27168ac93b5a63fc4eb180989f6a43f4eedfe10c9fc686/ServiceOrderControls.lean
[F939A-787]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d7a28aa7f9c23602b45501c47787e54cbc95bdcc08d935b44895e4f940dbdc12/NativeReference.lean
[F939A-810]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/db9737455bc7109fd40e7ff10812604000d18d650bb4868f1007790db1c9ebe8/ReviewerControls.lean

The contrasting `AliasRelation` source with SHA-256 `f3edd8c4ea46f3932a688b22db5c2f3e433a3954dd02c54fcf7edc55e0d2c6fb` is not the filtered relation cited above. Its `RootRefines.commitments` states only abstract membership iff concrete membership, but `concrete_permits_abstract` passes the pair of concrete membership **and selected-path membership** to that equivalence. The selected-path conjunct is absent from the receiving field's displayed type. This is an apparent local interface mismatch in this exact body, not an alternative proof of the filtered safety simulation. Its imported definitions and compiler outcome were not resolved here. The archived object is neither silently repaired nor credited with a newly checked refinement theorem. [F939-C890]

[F939-C890]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f3edd8c4ea46f3932a688b22db5c2f3e433a3954dd02c54fcf7edc55e0d2c6fb/AliasRelation.lean

The direct frame and receipt controls strengthen the operation-by-operation reading. One cancellation in the seeded finite diagnostic preserves epoch 11, pending status, the exact acknowledgment list [6,2,6], all epoch-certificate rows, an unrelated command's receipts, root 6's revocation list and the entire plant. This is a stated frame theorem for that fixture, not evidence that an authorization guard can be dropped. The shared-controller control separately proves that an eligible cancellation installs the actual shared-root veto while leaving an unresponding alias absent from the receipt set. With seven labels, one actual fault, two aliases and q=5, the retained threshold premises force label budget 2 and r=5. Its service annotations cannot change the actor's complete command list. [F939-C876] [F939-C877]

The same controller source retains a positive all-world endpoint. For every admitted seven-label environment with q=5 and the specified source-at-zero equality, and arbitrary supplied faulty synchronization and reply functions, it produces 21 compiled specifications and an accepted 259-event trace with exactly one installation and zero repairs. The counts follow from the accepted trace's full-plant counter laws even though the controller does not stop at its first success. The statement does not promise that an external scheduler will perform the service, and its axiom-print request is not a new execution receipt. [F939-C877]

The finite-history witness applies the same distinction to certification: the accepted acknowledgment/delivery history updates both aliases' stored descriptor and records the shared revocation, but the five actual acknowledgment labels do not gain the unresponding label 1. Corruption propagates only within its actual-root class. Missing samples, wrong-epoch samples and a wrong first same-key sample are refused; a key-consistent sample with a false actor nevertheless looks up successfully. Thus exact sample lookup is not external policy authentication. The specified constructor evaluations and trace-counter conclusions remain source evidence, not new native runs. [F939-C914]

[F939-C876]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ee8a60d289f180af0abb9ed4a7d77bad435c8b027c736b6f57439b93bfa60992/Diagnostic_cancel_frames_nonroot_controls.lean
[F939-C877]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/eeea7c2a163227418adaf0362e93a4e51bb09eda6b11ef274eebc98b229d9be1/ReviewerControllerControls.lean
[F939-C914]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fb8524832cfae8ede5d1090c2080d54ba96cb718eb35e85f7b43b8917807bff6/NativeHistoryControls.lean

#### Finite inputs and accepted history do not authenticate themselves

The native constructor has a finite public input interface. Policy samples are key/value pairs; lookup returns the first matching key. A sample is accepted for epoch e only if its stored policy's epoch is e. Missing initial policy, wrong initial epoch and unresolved delivery requests return `none`; resolving a whole history fails if a required delivery sample is missing. Successful reconstruction is exactly an initial sample, a completely resolved finite request list and replay of those inputs. No environment or infinite source function is an input to this constructor. [R500-483](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/80140a9767e9ff67492ce62f6e6a4dfba650a47514e4af9b9da063cb6a31856a/NativePolicyInputs.lean)

That executable consistency check is not external authentication. The positive correspondence theorem separately assumes that the initial sample and every supplied delivery policy are authentic for the environment. Conversely, an accepted finite shared history supplies finite authentic samples and request skeletons reconstructing a corresponding native state. The collector's same-key consistency comes from authenticity, not from the mere presence of a dictionary. The concrete owner-history fixture supplies a real accepted trace and an independently specified endpoint for this boundary. [R500-483](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/80140a9767e9ff67492ce62f6e6a4dfba650a47514e4af9b9da063cb6a31856a/NativePolicyInputs.lean) [R500-379](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/62a04befdbf1c55debb6cf61aea90011dee645c564648696799bb2c20b5f5be9/OwnerHistoryTrace.lean)

Synchronization has its own preservation theorem. In a reachable idle shared state, good stores do not revoke the current epoch. Delivering the current authentic descriptor to each label makes every good actual store current, while retaining cancellation and revocation memories and leaving epoch and plant unchanged. The finite public prelude lists labels; it does not discover a hidden root map. An authentic actor policy identifies its actor-facing synchronization with the mathematical one. Therefore a fresh current command becomes clear under the explicit idle, authentic-history and freshness conditions. Delivery alone does not erase an old cancellation. [R500-488](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/81bd547413824ba537f64dbb56996dce923d64f3e648561aa98813f15386179c/SharedAuthority.lean)

`NativeHistory` reconstructs a finite representation of an **accepted reachable** shared history using finite policy inputs and guard-free replay updates. The guards are discharged by the accepted `Step` evidence; a successful replay by itself does not establish them. Delivery still needs an authentic full policy sample and routing consistent with the environment. Its finite-table result applies to reachable states, not arbitrary function-valued certificate stores. [T750-C691]

The native-entry certificate source supplies a positive completeness direction under explicit representation premises. Environment overlap and repair availability force the revocation quorum r to be positive; reachable shared-state simulation preserves each past accepted certificate’s exact cardinality r. Since tableRead equals tableFind with its fallback, a positive-epoch represented reachable state cannot disguise a missing certificate row by the empty default. A returned row therefore has exactly r distinct labels even if its raw list has duplicates or its table contains shadowed rows. With routing matched to the environment, reachability, idle state, an actor observing the actual plant, authentic current actor policy, an explicitly present current policy sample and a bit list of length m, the wrapper returns that policy. None of these authenticity or reachability premises is inferred from successful table lookup or cardinality alone. [NEXT250-Z50-233](../research/t20-v6-20261012/sources/a9e3c27879b8cd3162982cb2af410f5155c1a293c3ad0c1f9201ff1887f77742/NativeEntryCertificates.lean#L9-L33) [NEXT250-Z50-233](../research/t20-v6-20261012/sources/a9e3c27879b8cd3162982cb2af410f5155c1a293c3ad0c1f9201ff1887f77742/NativeEntryCertificates.lean#L35-L59) [NEXT250-Z50-233](../research/t20-v6-20261012/sources/a9e3c27879b8cd3162982cb2af410f5155c1a293c3ad0c1f9201ff1887f77742/NativeEntryCertificates.lean#L61-L77)

`BatchExtraction` supplies another positive result at a deliberately weaker interface: for arbitrary actor observations it extracts genuine runtime calls from each literal batch branch and concatenates them through the fold, with the clock unchanged. A rejected proposal contributes an empty call trace even when its synthetic log entry says closed; preparation failure contributes preparation and cancellation; readiness adds the attempt. This structural extraction requires neither alignment nor honesty and does not establish their conclusions. The all-faulty countercontrol demonstrates why the trial semantics must stay fixed: a permissive open-gate execution can land the same action again after a true cancellation reply, while the retained `runBatch` forces faulty attempts to withhold and records four failures. No budget-free uniqueness statement is transferred between those semantics. [T750-C728] [T750-C699]

[T750-C691]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bb9bfdee643330fcea93d58eab688a8ffa219227bb62286ce95f7e532587ce01/NativeHistory.lean
[T750-C699]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/be465ed8ae81a7a0f8f44c02950efbdc738e67c42f24735fd1c52f0c38b04e43/BatchFaultSemanticsChallenges.lean
[T750-C728]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c520ac3048ec8ebb701401b5ecbca24b6f68b7cf0d996e1a61028ac0f303cca8/BatchExtraction.lean


<a id="final189-b11-finite-tables-and-authentication"></a>

A finite empty-default certificate table cannot represent every opaque epoch function. For any finite list of natural-key rows, choose epoch=1+the sum of its keys. Every listed key is at most that sum, so first-match lookup returns the empty default at the chosen epoch. It therefore disagrees with the function returning singleton{0} at every epoch. This is a constructive obstruction with an explicit key, not an appeal to oracle choice; it limits arbitrary-function reification without refuting the finite representation theorem for accepted histories. [F189B-856](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e8ef76829420d9565984b5de124e59e74b25071556a59090bd172c573a72cb43/OpaqueCertificateObstruction.lean)

The history-sample controls also show why reconstruction is not authentication. A forged first row shadows an authentic later row with the same key; delivery events carrying different policy contents may have identical projected event syntax while the forged content fails Authentic. A missing sample at the tail makes the whole reconstruction fail. Conversely, an empty-request reconstruction can retain a forged initial actor field. These cases preserve the positive authentic-history correspondence while preventing successful construction, event equality or a duplicate key from supplying its missing authenticity premise. [F189B-862](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ea5436e722bc37e8aa5d3bfb20b0c5a5d5773b9cda3a083dc21f5baf3dac913b/HistorySampleControls.lean)

#### Shared-store refinement and the scope of its reviewed controller

The shared-root reviews qualify the positive refinement already developed above. A literal label-store pullback fails because preparation or cancellation at one alias can alter an unselected alias's physical store, contradicting the selected-memory invariant of the label-local machine. The accepted `RootRefines` relation is deliberately weaker: represented commitments are the concrete commitments restricted to selected labels, while abstract vetoes are included in concrete vetoes. Extra concrete vetoes can withhold an opening. Thus concrete permission implies abstract permission, not the converse; simulation preserves exact ordered landing events and common plant/control fields without claiming equality of every actor transcript or charging the internal expansion as physical service cost. The reviews do not prove that every alternative architecture lacks a stronger encoding. [N250B-082] [N250B-083] [N250B-084]

The typed shared-gate acceptance is also narrower than the later lifecycle controller. Its snapshot need not be commonly reachable, its completed-certificate collection is empty, and a single shared bad-opening choice remains in the actual attempt semantics. The seven-label/six-root witness retains three genuine addressed acknowledgments; an alias acquires a tombstone, not a fabricated receipt. These facts explain why the selected-memory mask, veto direction, root address and alias-adjusted budget are substantive premises of that gate result. The review's mutant failures test those particular proof interfaces, not the impossibility of all implementations. [N250B-085]

The subsequent protected 21-command schedule is a mathematical source model at that historical release, not a native executable deployment. Its 259-event bound counts completion of each designated service slot under the protected policy/time and freshness premises. Silence is not itself a completed hold, and the theorem does not obtain fairness or elapsed-time bounds for free. The first 20 commands' 247-event failure witness establishes sharpness for that fixed order and world. The finite-corruption extension transports every realized finite bad-store rewrite weave while retaining the fixed fault set, common state, good stores and exact events; its length is 259 plus the inserted corruption events. Infinite interference, mobile faults and arbitrary extra owner operations are outside this result. Later native results below have their own premises and should not be backdated into this release. [N250B-090] [N250B-091] [N250B-092] [N250B-093]

The safety wrapper's acceptance history is correspondingly limited. The earlier false lint rejection and working-directory failure were packaging problems; the corrected wrapper's reported checks do not change the proof bodies. Its public correction also withdraws an unsupported Python 3.11 attribution. A later observed interpreter version cannot establish the version of an earlier unrecorded run. These historical review records add reproducibility qualifications, not a fresh replay here. [N250B-081]

[N250B-081]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/8d0d5c3934128136fbd69b70b8a0669fe055e5eb005797e25269a69157361657/PUBLIC_ACCEPTANCE.md
[N250B-082]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/0ca71bec66a49f143354ad9107b31068766ff4bdfaaffd5f2143b347048dca44/RESULTS.md
[N250B-083]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/b80ee984272f34b9956797f5418242f434aa0d286d13ba075a9924400c97e5a5/MODEL_V1_REVIEW.md
[N250B-084]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/4d05b715f32722fe75cf0479ff8b77dab048fe2d3818291e706e0c6e5e29bb4a/SIMULATION_V1_REVIEW.md
[N250B-085]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/a59f02cfc93afbf8655b4345a72d0d2102f3be6f013b8ffbe9a44421ad68f1c4/TYPED_V1_REVIEW.md
[N250B-090]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/38372d1f743fe0c4fa3ef4d214ee776e828b62aeea9b13d6d6769fe0b9f9a1bf/CORE_V1_REVIEW.md
[N250B-091]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/dc86cb946b650981969da124d5b7b5e902da39c924b174cb4da843d309922e7e/CORRUPTION_V1_REVIEW.md
[N250B-092]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/35c2fd015a6b1bd5dd4e886f628be990b934151683074f2c19c66077d7072d1d/SHARPNESS_V1_REVIEW.md
[N250B-093]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/ac522e04a17cd99459c265883df2253716cf0ccd0779b1bd748fd0c0a2783f14/EXECUTION_CLARIFICATION.md

<a id="next250-shared-execution-clarification"></a>

The execution clarification identifies why that distinction matters. These shared-progress and fixed-controller sharpness definitions occur in classical/noncomputable Lean sections, including decisions over service-guard propositions and Finset.toList choices. Their historical kernel-checked mathematical status does not mean that the whole 21-path interpreter was extracted, code-generated or natively evaluated. The unchanged executable localStep/attempt definitions occur inside the proofs, and local source-window checks reduce those definitions; neither fact turns the larger classical interpreter into the native four-path runBatch. Its concrete source fixture is [65,66,67], the three bytes ABC, with SHA-256 b5d4045c3f466fa91fe2cc6abe79232a1a57cdf104f7a26e716e0a1e2789df78. The starting draft [65,66,67,10] retains its extra line feed: installation changes ruleVersion from 3 to 4 without repairing the draft. The result is one installation and zero repairs, distinct from the separately verified 3013-byte label-local batch witness. The generic theorem still has its explicit applicability premises. These are the clarification's historical mathematical and fixture claims, not new executions. [N250B-093]


#### Whole batches, surviving trials and a sharp schedule

The aggregate batch has a full refinement theorem from an aligned reachable state for arbitrary actor observations and identity. Failed proposals and partial service effects remain in the extracted trace. After the batch, a successful actual attempt still entails its current epoch and full effective-policy `localStep` at the actual query time. A genuine earlier cancellation certificate continues to block its complete command after arbitrary such batches; a synthetic `closed` bit in a log is not used as a substitute certificate. A batch following a monotone reference-clock prefix can be concatenated into the primitive history, but the batch itself does not introduce a physical clock. [R500-364](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5fbdb63a111d1902a1d9a9688f724bb9a8e4b53e75f09352d81610f6791f528c/BatchSafety.lean)

`BatchAdmission` strengthens the **interpretation of an actual success**, not the promise of a future success. From an aligned reachable source boundary and positive `landedCount`, its aggregate theorem derives that the action uses the effective policy's epoch and that some successor is both admitted by the original plant/full policy/time and equal to the final batch plant. Preparation and fold frames carry those actual coordinates through failed trials. Positive landing count remains a premise; current admission is a conclusion of accepted history, not an extra assumed progress oracle. [F939-C926]

The complementary availability witness stops a genuine accepted runtime prefix after installation and certification but before policy delivery. Its effective policy admits the fresh repair and every good cancellation list is empty; nevertheless the roots still hold the earlier authentic policy. All four preparation and landing flags are false and the installed plant stays unchanged. Thus aligned reachability, current admission and freshness together still do not replace delivery. This is a defined finite counterexample to the stronger liveness implication, not evidence that the accepted safety theorem failed. [F939-C928]

[F939-C926]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fd8d317b6f49f564625bad68d7a23d35408c1b4ab8a88b6bf4b7bdc24ed29277/BatchAdmission.lean
[F939-C928]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fe17943e50db0ace4dd04197851d1b1a3b71f6bf225895bb6c9e595bea85f353/BatchAvailabilityChallenges.lean

Even the four-command `ExactReady` condition of §10.7 is only sufficient. The final survival theorem is an exact characterization for the literal four-trial withholding batch. Fix the actor's admitted proposal with its complete predicted successor, the four prescribed nonce/path pairs, n=4 and q=3. Require `AdmissionReady` in the starting world: actual admission of that action to the same successor at the world's time under its full effective-policy record, correct requester, and good-root policy agreement without the relevant revocation. Then the batch lands if and only if at least one predicted envelope selects only intact roots and is absent from every selected root's cancellation memory. The positive case has exactly one landing and that complete final successor; the negative case has zero landings. No numerical fault bound, cancellation budget, high-water bound or freshness of all four commands is needed for this equivalence. The predicate is a proof-side property of the actual world, not an actor-visible oracle. [N250B-052] [N250B-055]

The two directions use different facts. An actual successful withholding attempt implies intact selected roots, and durable cancellation memory shows that its envelope could not already have been vetoed. Conversely, choose a surviving trial. If an earlier trial landed, the required positive count is already obtained. Otherwise the plant is unchanged and the admission premises persist; earlier cleanup cannot cancel this future complete envelope because the four nonces differ. The surviving trial therefore lands. The fixed version-changing action and intact landing gate prevent a second landing. This argument concerns `badOpen=false`; it does not silently generalize to an arbitrary Byzantine opening behavior. [N250B-053] [N250B-054] [N250B-055]

The equivalence itself quantifies over raw `World` records and does not require `Authority`, `Aligned` or reachability. Its `effectivePolicy` field is therefore a semantic coordinate, not proof of authentic current authority. The separately proved aggregate refinement and admission theorem supplies that interpretation from an authenticated aligned history. Confusing these theorem layers would either strengthen the raw equivalence without warrant or treat a fabricated policy record as authenticated. Before delivery, survival can hold while policy agreement fails. In the budget-one fixture, cancelling the first path still leaves the fourth all-intact path and permits one landing, while cancelling the fourth destroys the sole survivor. The unselected-root memory example tests only its stated world, not lifecycle reachability. [N250B-051] [N250B-052] [N250B-055] [R500-350](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5d0039addced8f23d7048d412894896235c435a56194eaa147fc2eec4a870a5b/BatchSurvivalControls.lean) [R500-452](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/78c59bb688bfdce25f4a1af458a69618851420e5356ba246fe87b671e32b335d/BatchV2ContractChallenges.lean) [R500-464](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7c2df5b46bbd1bec33408aa402ac5c26d4478315dac5bdcfc5ce1a7675e90dee/BatchHistoryPremiseChallenges.lean)

Delivery also does not erase the effects of a failed batch. In the corrected two-stage witness, the actor has received the new repair certificate while the roots still store the old policy. The failed repair batch's cleanup tombstones its exact nonce-5-through-8 envelopes. Authentic delivery subsequently synchronizes the roots but preserves those tombstones, so retrying the unchanged actor and action still produces zero landings. Advancing the actor nonce to 8 produces fresh envelopes 9 through 12 and a successful retry. Alternatively, changing the admissible lease end from 90 to 91 changes the complete envelope even with the same nonce; it can succeed while the high-water test is false. Neither example is a general permission to extend a lease or a service that automatically renews it. `runBatch` does not return a refreshed actor, and source grant limits still govern the changed command. [N250B-056]

[N250B-051]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/3671d870e7ee39d73563891c584d5bb3346edb32329b7f1647629c98405aa234/ACTUAL_BATCH_V3_REVIEW.md
[N250B-052]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/75545ad5a0a409bf607ef418138dc8355c3a9ea53f186feff80e823ceb704bd4/ACTUAL_BATCH_V4_REVIEW.md
[N250B-053]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/18c76e8f23d2e55bf1ac6911920b865cb17641141d83b4f408c88083ca111793/BATCH_ARGUMENT.md
[N250B-054]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/94cee25cff035891f95993a78ed56cdac6ec9dfc8353acfa2e0145dfa899d696/BATCH_SUCCESSOR_ARGUMENT.md
[N250B-055]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/58765f52aba9d4493550d2df6b7cffdfbab1ec82146b4f2a60a8f403bb379bee/BATCH_SURVIVAL_ARGUMENT.md
[N250B-056]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/a093c7ade358a41e7cec9f08053e81f30d6b35c3236d15f9c4da401b7c0e2a84/BATCH_RETRY_ARGUMENT_CORRECTED.md

In the changed-command control the old actor nonce is 4, the actual annotation is 2, and both lease ends 90 and 91 lie within the same source grant ending at 100. It is an admitted alternate command, not an implemented renewal operation. The corrected note also binds the complete witness to the [retained four-path source projection](#what-the-four-path-log-and-lifecycle-actually-record): its installation, predicted installed actor observation, authentic repair transition, certificate getD fallback, actor receipt, delivery and repair sequence are preserved. Only the IO assertions and outer loop over fault sets are removed. Definitional equality for the pinned complete source and bad-root-0 fixture then transports the one-landing/repaired-plant result. It does not interpret the whole IO runner, authenticate physical delivery, allocate future nonces or grant actor knowledge. [N250B-056]




The direct four-root controls enumerate all sixteen fault patterns: the fixed three-of-four portfolio contains an intact path exactly up to one fault, and removing any one of its four paths loses that guarantee for one single-fault world. Those combinatorial facts do not supply service admission. Failed proposals can create synthetic closed log entries without cancellation; a wrong requester or stale observation can retain partial faulty-root preparation effects. A batch does not automatically refresh its actor or stop after success. The service-trial decomposition records the prepare/attempt/cancel sequence and keeps its endpoint and no-relanding claims tied to that source. [R500-316](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/54a1144d5d0727a771ef7cdd1088bab614d4afd3da87632635fdb0342f24496b/BatchSourceChallenges.lean) [R500-418](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6dfbf97ab4ede0aed173f424b5066b4f48934e6b9151f785a79c3a22f5fbe010/BatchTrial.lean)

One intact cancellation reply can already veto an exact command even when the threshold Boolean is false; the greater-than-budget certificate is sufficient to establish an intact reply without identifying it, not necessary for every veto. Repeated cancellation can append duplicate list tombstones while distinct-label certification remains idempotent. Cancellation preserves commitments and the whole plant; wrong-requester cancellation is world identity. Reordering a path can preserve nonce and support while changing the complete command and its tombstone key. Shared aliases do not turn the three-label receipt requirement in the seven-label fixture into three independent physical stores. [R500-446](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/776055108a112624bdf1dc1f0b42eddc647c19369040db0848cef64c41fd1aa4/CancellationV5Challenges.lean) [R500-338](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/59e5dc63b11db9b702b37aaa45e89f5b39d4e6e920196f8b3636c7ba4878ae5c/AliasTypedControls.lean)

The typed accounting theorem retains source, destination, standard and unrelated state through lawful histories, and counts installation and repair increments from the actual landing events. A fixed successful command cannot replay through a lawful reachable continuation because its expected versions cannot rewind; a newly versioned installation may still change the plant. A late time may invalidate an otherwise matched command, and internal admission does not create an externally reserved permission. The full successor binding prevents a stale cached observation from overwriting an intervening audit. These are distinct controls, not a universal idempotence theorem. [R500-377](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/61df10a0ad98bd550237dcaee33e2918c8f1415b9e2296d824fa9e26d124c6d5/AliasTyped.lean) [R500-383](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/636cd9b75c1de286a15b48aa77804f686a10a76ffddeccddf949db278edcf946/TypedControls.lean) [R500-465](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7c7d2f85bb0e5b8dfcd78f587c8861ed077f5bf7f050cc397a0e67735b503fa1/OffsetHistoryProperties.lean)

The finite two-stage witness installs an exact-byte rule, crosses an acknowledged policy transition, delivers the current repair grant and then repairs under that rule. Its preparation lemmas expand repeated selected-root operations into explicit traces. The runtime counterpart binds six aggregate operations to a primitive common history and preserves the complete final plant, source and audit fields. Alignment retains the full stored policy and ordered acknowledger list; a base-offset certificate cannot be treated as a pre-base message. These are constructive nonvacuity witnesses for their actual imported definitions, not for the defective variants above. The earlier invariant establishes consistency by induction over the admitted operations; its separately stated public targets retain reachable-history premises and same-epoch restoration stability. [R500-285](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4df579e1f7c9afa47dab091682d1bc37d964feb40ae8f6bf57d8010307fe8ee7/TypedExamples.lean) [R500-264](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/49d5511c7409d783a162e68968b5fc7805b4ebd48a17309cdcb8c6544cb52e55/JoinPreparation.lean) [R500-356](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5ea1d3694f380d473f1aed46213b3248faf7d9b97fdac0408d6b9d5bca917a7e/RuntimeFixture.lean) [R500-417](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6ce4dfaf0f6ddce419adccddf8bc3147def71d8a9128bd8e6d30accff4bc7e6c/LifecycleModel.lean) [R500-329](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5772d191b00386413efa3dc0d753c59c17635baecb93d6aee876dec967a13e78/HistoryInvariant.lean) [R500-282](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4cf34b90a48a8a12d877e48c665ca7fb3801fdc8393777fd3a8155365ce91166/Targets.lean)

The seven-label witness makes the schedule bound concrete. Its 21 commands produce 259 core events and an installed final plant under the stated authentic policy and service-window conditions. A fixed admissible shared world with withholding faulty replies meets the first 20 paths; that prefix has no successful effect and keeps the original plant. The last path is at its proved position in the actual delivered order and attains the installation. The additional review checks zero installation and repair counters in the first 20-command schedule prefix (247 primitive events) and a genuine trace, not merely an endpoint Boolean. This is sharpness for that public order and fixed world, not an optimum over every possible scheduler or a physical elapsed-time bound. [R500-302](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/50098a95fd5af226f7855dd84ccb2cc5a9bb07dfc57c93e877f07316e4ecf645/ProgressWitness.lean) [R500-397](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6772e1b6852b62b28179e276cd0ab779b810fff0e013d58307b446623c776847/ControllerWorstCase.lean) [R500-381](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/62b8b0483f5375ef257f3c669cd246bfd19342147290a70e823324561881fc57/ReviewerSharpnessControls.lean)

The uniform native-effect theorem puts the quantifiers in the operational order: **one public list of 21 complete commands is fixed first**, then every admitted hidden world, matching finite routing and valid 21-entry schedule are considered. With q=5, the specified source policy at epoch zero and `AnnotationClock 2 2 22`, execution yields an accepted 259-event trace, the exact installed plant, one installation and zero repairs. The counts follow from the actual emitted trace and full-plant counters, not from synthetic trial-success flags. No hidden root map or fault set is returned through the command-selection API. [T750-C736]

This implementation uses separately defined shared-store service handlers. Each selected-label preparation or cancellation is represented by one legal event, including `hold` when its gate rejects; preparation preserves envelope eligibility, existing commitments and plant. For a valid quorum path and the command's authorized recipient, cancellation gathers more than the label fault budget of distinct replies, using `q > 2*labelBudget` derived from the environment's contract. Shared memory never manufactures sibling receipts. Source-defined execution controls reject short cancellation-reply lists, excess preparation/cancellation-reply lists and a nonzero initial-run entry even when a later repair proposal is present. These list-length controls concern replies within annotations, not the outer 21-entry schedule. Withholding and open-gate decorations can land different nonces, 1021 and 1001, while retaining the same public commands, 259 events and installed plant. These are exact theorem and fixture scopes, not newly observed native executions. [T750-C730] [T750-C738]

[T750-C736]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c81047778b2ce6e696a3617c91b5bcf1355c8fbe4834942fdb46021a5b471d50/NativeUniformEffect.lean
[T750-C738]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c866a0dbe33b1b866d7faae97b315434fdff3d65dde1f4fd73520f2551544246/OrderedExecutionControls.lean
[T750-C730]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c6158e932d787a7a381c71ea9e567677a174aa007630f70dea18b68cb1faf0b7/SharedService.lean

#### Finite corruption between completed service events

The fixed service core also admits a positive robustness extension. `SameGoodState` in `BadStoreErasure` relates two shared states when their epoch, pending flag, acknowledgments, certificates, cancellation acknowledgments and plant agree, and every good actual store agrees. Among actual stores, only bad-store contents may differ; unused carrier coordinates are not constrained by this relation. This is a proof-side relation, not an actor observation. A permitted rewrite at a lifetime-bad root preserves it because any label sharing a good root is itself good. The preparation guards, source application Boolean with the same `badOpen`, and each genuine service operation respect this relation. Transport therefore does not silently change the service branch, invent acknowledgments or weaken a grant. [F939A-767]

A finite weave inserts a finite block of such rewrites before each prescribed service event and after the last one. Induction transports the reference trace through every block, preserving the related endpoint. Determinism of the event transition then gives the stronger conclusion for **every actual trace realizing that weave**, not merely one chosen successful execution. Combining this with the fixed seven-label installation witness, with quorum five and the specified authentic source-zero policy, supplies the successful 259-event core without assuming its desired endpoint as a caller premise. Every finite weave has the same installed plant and exactly 259 plus the number of inserted rewrites events. When a lifetime-bad root is available, arbitrarily long finite rewrite blocks preclude a uniform raw-event delay bound; the theorem does not cover infinite service starvation or establish transcript opacity. [F939A-767]

[F939A-767]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d24e15ad5a890aca297fd3ef7b8ea6246c97241d9797714720d51bfd0eb44fdd/BadStoreErasure.lean

#### Changing an ordered command changes every complete-keyed store

A selected-order profile gives one coherent new order for each selected support. The induced map swaps the old and selected orders as a bijection of complete commands, fixing other cases; it does not sort all commands into an equivalence class. The symmetry preserves action, successor and support, but must also transport commitments, tombstones, cancellation acknowledgments and corruption payloads. Events stay in their original temporal positions. Exact trace length and both opening/withholding gate cases are preserved when this whole transformation is applied. [R500-394](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/659e5f14e2ec2dcc52b66a8e3e94f7f95a8cf938feb1282bbcf3121afe8caafe/SelectedOrderTransport.lean) [R500-349](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5ccb05b0389b38070bc331b2d59aeb9894ece419a8d31d2cfae3f5bf735b8917/SharedTraceTransport.lean) [R500-493](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/83ec766ad7ea8789005cfb51934177e9026c3774c1142a61cac14b68984e38fb/IndependentTransportControls.lean)

The negative controls show why a smaller operation fails. A commitment for k does not admit a distinct transformed command in the unchanged store; a tombstone for k does not veto the other command merely because their supports agree. The old receipt key may meet the close quorum while the new key has none. A corruption event retaining its old payload may cease to be a valid transformed event because the payload itself should have been renamed. Sorting also collapses a nonfixed pair and so cannot be substituted for the required complete-key bijection. These failures are compatible with the positive full-state transport theorem. [R500-276](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4c1f196fa16f0a2699272240d7f915462384167355c74234bbb754c176631606/TransportNegativeControls.lean) [R500-493](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/83ec766ad7ea8789005cfb51934177e9026c3774c1142a61cac14b68984e38fb/IndependentTransportControls.lean)

The nonidentity transport control removes a possible vacuity in this comparison. For the selected support {0,1,2,3,4}, it chooses ascending order unless that is already the source's abstract finite ordering, and descending order otherwise. Therefore the selected new order differs without guessing which order classical `Finset.toList` chose. The support stays fixed while the complete issued command changes. This directly tests a nontrivial order profile, rather than an identity renaming, under the full-key transport contract above. [F939-C908]

[F939-C908]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f970e3fc55af8e71b99e6288187a498129cc3e041b37b2bae46665f1a54dff04/NontrivialProfileControl.lean

All of these are source-bound mathematical or source-inspection conclusions. This consolidation does not claim a new Lean/kernel run, observed IO-test outcome, physical execution, arbitrary dependency equivalence or authenticated real-world source. The finite programs, negative probes and imported dependencies retain their distinct reproducibility roles.

#### What the controller and transport acceptances actually certify

The controller review reports a source-bound positive epoch-zero execution and independent controls, rather than just the fixture expectations quoted above. Its reported tuple is (21,247,0,259,1,0,4,8): 21 trials, a 247-event no-effect prefix, 259 total events, one installation, zero repairs, and installed rule/draft versions 4/8. The full Plant still contains its source and draft, not only those two numbers. Moving the successful landing from nonce 1021 to 1001 leaves the complete public command list unchanged; that program independence does not hide the reply transcript. The review expressly rejects using this entry point as a nonzero-epoch synchronization result. These are historical observations of the bound packet, not newly run native tests. [N250C-099]

The separate ordered-command acceptance reports cold source checks of its 72 named declarations, nine contract examples and 20 independent declarations. It accepts whole-history conjugacy with the same badOpen Boolean, not executable state conversion. In particular, its reference trial/run and pointwise public-program composition remain separate work, requiring support/index/nonce correspondence and service ordering. This is compatible with the controller's represented comparison on the **same** new commands; the two results cannot silently be combined into old-to-new in-place command migration. [N250C-125] [N250C-126]

Public-projection review has a third role. It can establish faithful custody of accepted bytes and explicit omissions without giving an unfinished extension scientific acceptance. Its paused archive remains custody-only: locally compiled kernel/bridge pieces do not certify uncompiled program/fixture drafts; an unchecked later semantics edit does not inherit a prior check of different bytes; and failed nonzero-entry certificates supply no accepted progress theorem. The scope record itself is usable evidence for these limits, not permission to recover or promote excluded paused bodies. Selected historical TeX custody likewise has an explicitly incomplete include closure. Neither projection fidelity nor path-only cache-metadata comparison is a proof replay or compiler bootstrap. [N250C-113]

## 11. Coordination, discoverability and agency

### 11.1 Recognition, coordinated updates and adaptation

Recognition, determination and execution change different things. Recognition proposes a connection or a realisation. Determination supplies evidence and a contract for a restricted operating domain. Execution builds or maintains the corresponding physical process. Learning can change an estimated feasible set without changing the physically feasible set. Building a transducer or storing a usable checkpoint can change what is reachable from the present state. A theory becomes causally effective through an implemented intervention; recognising a possibility is not itself that intervention.

An organised research collective can distribute modelling, estimation, proof checking, resource accounting and integration. The September 2026 OpenAI announcement reports coordinated mathematical agents operating with monitoring and isolation [NSA]. That is a reported workflow, not evidence of independence from its infrastructure.

Let a finite dependency graph be acyclic. Associate each vertex i with an update Fᵢ:D→D, so all admitted updates preserve the common state domain. Suppose updates at incomparable vertices commute:

```math
F_i\circ F_j=F_j\circ F_i.
```

Then every topological order gives the same final state. Any two linear extensions of a finite partial order can be connected by swapping adjacent incomparable elements: move the next required element left across only elements with which it has no ordering relation, and continue inductively. Each swap preserves the composed map by commutation, proving the result.

This theorem gives a genuine form of schedule freedom. It does not make noncommuting updates safe to reorder. Their dependency must be preserved, or a separately justified reconciliation rule must be supplied. If elapsed time, resource state or deadlines affect behaviour, they belong in the state and contract; equality of a simplified final value does not certify timed equivalence.

State-machine replication is an established way to organise replicated services under explicit assumptions [SCH]. The impossibility result of Fischer, Lynch and Paterson concerns guaranteed termination of deterministic consensus in its asynchronous model with even one possible crash [FLP]. It does not prohibit all distributed coordination. It shows why failure, timing and termination assumptions cannot be dropped from an orchestration argument.

An adaptive system can change both a policy π and an architecture description g,

```math
(\pi_{t+1},g_{t+1})
=\Psi(\pi_t,g_t,\text{observations},\text{verified results}).
```

Changes to encoders, decoders, membership or transfer policy can invalidate previous certificates. A sufficiently broad invariant may cover a family of adaptations; otherwise the new arrangement needs a new justification. Incremental bootstrap is a positive possibility: improved shared models can support better coordination, which can support further bounded discoveries. Drawing this feedback loop supplies no convergence theorem and does not require an already completed higher-level agent to create itself in one step.

### 11.2 There is no universal unbounded-horizon discovery algorithm

A general search procedure cannot always decide whether a usable distinction will ever appear in every effectively presented, unbounded-memory computational system. The following reduction makes the scope exact.

Given a program P and input w, construct a system that stores one binary input b, simulates P(w), and outputs zero while the simulation has not halted. If it halts, the system thereafter outputs b. There is a finite observation horizon distinguishing b = 0 from b = 1 exactly when P(w) halts. A procedure deciding the existence of such a horizon for every such system would decide the halting problem [TUR].

The reduction assumes a computational class with unbounded working memory. It is not a proof that every physically finite channel is undecidable. For a fixed finite horizon with an effective finite-step model, finite input choices and computable observations, the prescribed cases can be simulated. For a known finite-state machine with a finite effectively given input/output interface and decidable output comparisons, state-pair exploration or partition refinement can decide the relevant distinguishability question. Nor does the reduction say that all finite-horizon inverse problems over real-valued models are decidable; effectiveness and representation assumptions matter.

[Measure, Computability and Finite Warrant](measure-computability-and-finite-warrant.md), section 4, illustrates a different finite-state calculation: a paired-state algorithm identifies input-insensitive behaviour and the measure of eventual entry into it. Its finite graph and computable transition assumptions are essential. The present unbounded-horizon reduction does not negate such bounded positive procedures.

The research consequence is a disciplined combination of methods: prove results for specified model classes, search within finite admitted horizons and resources, and report the residual uncertainty. Failure of a universal discovery promise does not make all engineering discovery futile.

### 11.3 Authorship and architecture are latent hypotheses

Communication through an interface does not uniquely reveal the architecture producing it. A response may have been authored, selected, relayed or transformed by different arrangements. These hypotheses should be distinguished from one another and from the separate question of a continuing person's identity.

Let P₀ and P₁ be the laws of all admitted evidence under two hypotheses. With equal priors, the best possible probability of correct binary classification is

```math
\frac{1+\mathrm{TV}(P_0,P_1)}2.
```

**Proof.** For a deterministic test that selects hypothesis 1 on event A, success is

```math
\frac12P_1(A)+\frac12P_0(A^c)
=\frac12\bigl(1+P_1(A)-P_0(A)\bigr).
```

Maximising over A gives total variation. Randomised tests are mixtures of deterministic decisions and cannot improve the supremum. ∎

When the evidence laws are equal, no such evidence can distinguish the hypotheses or change their prior odds. A system's statement about its own architecture is one observation inside the evidence law, not an independent authentication of that architecture. Additional technical records, controlled interventions or appropriately consented observations can change the evidence experiment; they cannot be assumed to exist.

This does not deny the possibility of attribution. It specifies what would make attribution informative. Ordinary human interfaces likewise concern measured outputs and declared interventions. Rao and colleagues' brain-to-brain experiment used a specific EEG, network and stimulation apparatus for a restricted task [RAO]; it is not evidence of unmediated access to private thought. Personal experience is not used here as an empirical premise for covert communication, hidden authorship or an unseen distributed agent.

### 11.4 Continuation is not a complete theory of persons

The mathematical results preserve an explicitly selected organisation and trace. They can establish causal dependence on a previous state and distinguish a continuation from a fresh restart. They do not decide whether two identical copies are one person, whether every information-processing system is conscious, or what obligations are owed to it.

This limit is also a positive philosophical clarification. A claim of continuity can be meaningful and testable without carrying every possible metaphysical conclusion. A causal handover, a role-equivalent implementation, an authorised successor and a numerically identical subject are distinct claims with different grounds. One should neither dismiss the operational claim because it leaves personal identity unresolved nor promote it into a solution of that unresolved problem.


## 12. Tests that can change the claims

### 12.1 Distinct experimental targets

The analytical results suggest several different experiments. Combining them into one claim about the eventual emergence of a planetary intelligence would make failure difficult to interpret. The following targets can succeed or fail independently.

| Target | Evidence that would support it | A relevant adverse result |
|---|---|---|
| A specified usable channel | Predeclared actuation, blinded fresh messages, calibrated readout, held-out decoding and a valid resource account | No signal beyond controls, unknown polarity, inadequate separation, inaccessible actuation or an omitted causal path |
| A physical stateful implementation | Correct transitions from all admitted preparations within declared disturbance and timing regimes | Reliance on an uncounted state store, incorrect outputs, drift outside the domain or a missed deadline |
| Paired continuation | Transfer of the actual current state, correct input ordering and later behaviour after removing the named original support | A stale checkpoint, missing export variable, replayed effect, hidden original-host dependency or unmodelled interruption |
| Resilient maintained operation | An explicit support family, reachable operating region, admissible feedback and progress evidence | A shared failure domain, an unreachable replacement, unsafe continuation or safe indefinite idling |
| An orchestration advantage | Matched resources and information, separated task dependencies, useful joined results and a declared objective | Improvement explained by extra budget, incompatible joins or coordination overhead exceeding the benefit |
| A PDE-derived operational advantage | A named estimate improving the same fixed input/readout problem within its validity domain | No bound improvement, inaccessible measurement or use outside the approximation regime |
| Better representation and composition assessment | Support-disjoint held-out cases, a strong conventional schema, explicit uncertainty and separate error categories | No predeclared improvement, dependence on extra information, missed conflicts or unjustified confidence from duplicate reports |

For a channel test, no-actuation and message-blind controls matter. For a processor test, freezing or removing the alleged memory-bearing component can expose a hidden external memory. For continuation, paired before-and-after state tests matter more than separate task scores on two devices. For representational comparisons, a vocabulary ablation can retain the same mathematics and evidence in both arms.

The errors should not all be pooled into one undifferentiated score. A false physical assertion, an incorrectly transferred certificate, a missed shared-resource conflict, an unwarranted confidence increase and an unauthorised application are different failures. Abstention, conflict and “not established” are legitimate results when the evidence does not determine the target.

### 12.2 A simultaneous bound for held-out assessment

Let M ≥ 1 fixed candidate assessors be evaluated on n ≥ 1 independent identically distributed held-out cases. Each loss lies in [0,1]. Candidate j has population loss Rⱼ and sample mean R̂ⱼ. The candidates must be fixed independently of this test data, although their losses on the same case can be correlated.

For 0 < α < 1, with probability at least 1 − α,

```math
R_j\le \widehat R_j+
\sqrt{\frac{\log(M/\alpha)}{2n}}
\quad\text{for every }j.
```

The logarithm is natural, and the bound can be clipped at one.

**Proof.** For a centred random variable supported on an interval of length one, let ψ(s) be its log moment-generating function. Then ψ(0) = ψ′(0) = 0. Its second derivative is variance under an exponential tilt; any variable in an interval of length one has variance at most 1/4. Integrating twice gives ψ(s) ≤ s²/8. Apply this to the centred negative loss, use independence across cases and Markov's inequality, and optimise over s > 0:

```math
\Pr(R_j-\widehat R_j>t)
\le\inf_{s>0}\exp(-snt+ns^2/8)
=e^{-2nt^2}.
```

Substitute the stated threshold and union-bound over M candidates. ∎

This is the standard bounded-loss concentration argument associated with Hoeffding [HOEF], not a new inequality. Selecting among the already fixed M candidates after testing retains the simultaneous guarantee. Creating uncounted new candidates in response to the same test answers does not. Distribution shift, correlated acquisitions, inaccurate labels and changes to the target are separate problems.

### 12.3 What zero observed transition failures means

Suppose there are k ≥ 1 fixed test cells. In each cell, n fixed independent identically distributed trials have a fixed failure probability pᵢ. Cross-cell independence is unnecessary. Put

```math
p_* = 1-(\alpha/k)^{1/n},
\qquad 0<\alpha<1.
```

The probability that some cell with pᵢ > p* nevertheless records zero failures is at most α. For each such cell, the chance of zero failures is (1 − pᵢ)ⁿ < α/k; a union bound proves the result.

This can support simultaneous frequentist upper assertions for cells with zero observed failures under the declared test design. It is not a posterior probability that a physical theorem is true, a worst-case guarantee over every disturbance or a guarantee for an adaptively stopped experiment with a different sampling rule.

For four fixed cells, one thousand trials per cell and α = 0.05, p* is about 0.004372. This is an illustrative design calculation. No corresponding four-thousand-trial hardware dataset is reported here. A universal analytic perturbation proof and a sampled transition test answer different questions and can usefully coexist.

### 12.4 Strong comparisons and historical computation

A conventional assessment supplied with full contracts, provenance and the same admissibility rule should agree with an annotated assessment supplied with the same information. The source's seven matched synthetic composition fixtures report such agreement by construction. That establishes compatibility of the formal encodings in those fixtures, not superiority of a new vocabulary.

To test an advantage, assessors must encounter consequential distinctions not already encoded as the answer: sufficient versus insufficient margin, known versus unknown polarity, independent versus shared power, stored versus executable state, current versus stale calibration, inadequate export and incompatible regimes. Hold-outs should match the intended claim, including acquisition roots or mechanism families rather than paraphrases of the same experiment. Equal costs and retained adverse examples make a negative result interpretable.

The Third Edition also reports an executable finite test suite, extending the previous edition's 27 top-level checks to 42, with ordinary and optimised executions stated to agree. The earlier report gives 341 finite fibre cases, including the empty-domain case and a separate empty-target extension guard; all 5,040 permutations of a seven-symbol alphabet for latent relabelling; and 1,944 finite-automaton initial-pair cases. The later report gives 29,366 coordinate-correspondence equalities, rejection of all four memoryless parity candidates and all 16 one-bit delay initialisers, alongside the selected parity computations discussed above. These are historical source-reported model checks, not newly executed confirmations. This chapter does not claim to have replayed that historical execution or to have converted it into a formal proof-assistant certificate. Documentary claims about such runs remain separate from the explicit mathematical proofs.

Independent mathematical review, source inspection and computer checks can each find errors. Agreement among AI-generated assessments is not an independent physical measurement, and it does not create empirical replication. A model theorem is defeated by an error in its statement or proof; a physical application can fail because its premises do not hold. Those are different findings and should be recorded as such.

### 12.5 Open questions that follow from the results

The immediate experimental questions are a calibrated physical stateful implementation, a genuine paired handover and a fair comparison of assessment procedures. The mathematical framework also leaves substantial work.

First, behavioural quotienting can reduce export size, but computing a quotient under realistic input restrictions, large state spaces and partial observations can be difficult. A useful implementation needs a tractable sufficient representation and an accessible initialiser, not only the abstract minimum in Proposition 4. Approximate quotients need an error account that survives both changing dynamics and repeated transfers.

Second, a robust channel certificate needs physically justified uncertainty sets. Learning a model and then acting outside the data's regime can invalidate its gain, residual or noise bounds. A more informative uncertainty geometry or a calibration phase may improve the certificate, but its cost and acquired information must be counted.

Third, real apparatuses replace ideal resets and clean interface times with finite-duration preparation and measurement. The parity proof points to the exact obligations: a post-reset domain, an inward-flow estimate, a dwell bound and a readout margin. Establishing those for a measured device would add evidence that the abstract model alone lacks.

Fourth, support adaptation must join reachability, invariant operation and sustained progress under shared resources. Possibility of some suitable configuration, reachability from the current configuration and maintained operation are three different modal claims. The finite viability and rank constructions give positive algorithms under strong observation and model assumptions; richer partially observed or continuously varying systems require additional work.

Fifth, semantic comparison must keep target-relative equivalence separate from evidence about actual instantiation. A shared representation can make contradictions and missing assumptions easier to find. Whether it improves accuracy or cost beyond strong contract and provenance methods remains an empirical question.

The results identify a claim-specific gap between a coherent description and a physically adequate, reachable and maintained realisation. They also identify ways to narrow it: certify a signal, preserve the future-relevant state, exhibit a compatible joint implementation, prove progress and test the physical premises. None of these steps depends on treating matter, evidence or permission as interchangeable.

## 13. Sources and attribution

### Source manuscript

[LM] *The Last Moat, Third Edition: Physical Realisability, Cross-Substrate Communication, and Holarchic Agency*, dated 10 September 2026, is the source manuscript family consolidated here. Its main TeX body has Git blob `6d5153cc4944f8bd74465cafed4de505d21298f9` and SHA-256 `06256dd01149f7351d4c5fdcd876cc8d8ae0f264c0636b23e699b242165bc8da`. The family comprises that body and 22 dependent components, including substantive sections, worked examples, an edition-change account, claim index and bibliography. It is one manuscript, not 23 independent papers. Its user-originated, AI-assisted authorship and research-stage status do not imply peer review, new physical experiments or proof-assistant verification.

The channel, residual, continuation, export, packing, parity, evidence, support, viability, progress, scheduling, undecidability, attribution and evaluation arguments above retain the manuscript's declared assumptions and negative controls. Proposition 4 and its information consequences compose its export obstruction with the existing finite task-partition result; Corollary 1 explicitly optimises its uniform channel certificate. Neither addition asserts an otherwise unproved physical implementation.

External references below support particular definitions, reported experiments, methodological connections and historical attributions. The use of an abstract or a theorem statement does not imply a complete independent verification of its paper. The Navier–Stokes report's full 166-page proof and Lean development, and the cited physical experiments, are not independently verified or reproduced here.

[CONT] Orthemology, *Continuation-Complete Orthings: Sharp information loss, minimal predictive memory, and safe strategic composition*, 8 September 2026, “From fluid reduction to an Orthemological obligation.” [Exact public source][CONT]. Section 5.4 derives its elementary elimination and averaging identities and preserves the source-relative status of its discovery/certification comparison. The other continuation results are treated in Information and Inquiry and Collective Inquiry.

[FORM] Orthemology, *Graded Representations, Witnessed Revision, and Inquiry Landscapes: A conditional mathematical extension of Orthemology*, version 1 research draft, 8 September 2026. [Exact public source][FORM]. Section 5.5 develops the source's Theorems 10.1–10.2, Corollary 10.3, Proposition 10.4 and Counterexamples 10.6 and 10.8, including their strict hypotheses, degenerate cases and continuation limits. The displayed concentration-and-damping condition is an explicit algebraic composition of its two estimates. The source relates these abstract mechanisms to an uploaded Euler manuscript; no PDE-specific constants, full proof, formal development or physical application of that manuscript is independently verified here. The source's broader representation, witnessed-history and inquiry-landscape arguments remain distinct from this bounded treatment.

Section 5.6 also develops [FORM]'s exact transient-amplification model, uniform-parameter barrier and general surrogate-margin calculation. Its discussion of search, certified reference and target solution retains the source-relative reading limits of that research draft. The finite flow/reset and stability-versus-target arguments are connected to the existing proofs in §§7–8; the infinite-event degree example is stated in Tensor Moments. No new fluid proof, numerical certification or execution of the source's historical checks is claimed.

### Physical channels, processors and representation

The proposed case/type terminology is attributed by the Third Edition to the Orthemology project’s research-stage *Orthemic Core Formalization—Orthing, Episodes, Metaorthemes, Pathway Adequacy*, at historical Git commit `f50dc1aee52356cc6adbef342387576b02afc124`. Section 9 states the relevant definitions and their limits; this historical attribution supplies no independent empirical validation [LM].

- **NIST.** *Air gap* and *TEMPEST*, Computer Security Resource Center glossary. [Air-gap definition][NIST]; [TEMPEST definition][TEMPEST].
- **Thermal, acoustic and electromagnetic channels.** Guri, Monitz, Mirski and Elovici, *BitWhisper* (2015); Guri, Solewicz, Daidakulov and Elovici, *Fansmitter* (2016); Guri, Kedma, Kachlon and Elovici, *AirHopper* (2014); Guri and colleagues, *GSMem*, USENIX Security (2015), pp. 849–864. [BitWhisper][CHAN]; [Fansmitter][FAN]; [AirHopper][AIR]; [GSMem][GSM].
- **NOAA Space Weather Prediction Center.** *HF Radio Communications*. [Technical account][NOAA].
- **Eckford, A. W.** *Molecular Communication: Physically Realistic Models and Achievable Information Rates* (2008). [Author preprint][ECK].
- **Prakash, M., and Gershenfeld, N.** *Microfluidic Bubble Logic*, Science 315 (2007), 832–835. [Author-hosted paper][BUB].
- **Benenson, Y., Paz-Elizur, T., Adar, R., Keinan, E., Livneh, Z., and Shapiro, E.** *Programmable and Autonomous Computing Machine Made of Biomolecules*, Nature 414 (2001), 430–434. [Primary author abstract][BIO]; DOI `10.1038/35106533`.
- **Shen, Y., and colleagues.** *Deep Learning with Coherent Nanophotonic Circuits*, Nature Photonics 11 (2017), 441–446. The experimental qualification used here is from the [2016 first preprint][SHEN].
- **Wright, L. G., and colleagues.** *Deep Physical Neural Networks Trained with Backpropagation*, Nature 601 (2022), 549–555. [Author preprint][WRIGHT].
- **Wright, L. G., Wang, T., Onodera, T., and McMahon, P. L.** *Physical Foundation Models: Fixed Hardware Implementations of Large-Scale Neural Networks* (2026), version 1. [Research proposal][PFM].
- **Frantar, E., Ashkboos, S., Hoefler, T., and Alistarh, D.** *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*, ICLR (2023). [Version 2 preprint][GPTQ].
- **Dambre, J., Verstraeten, D., Schrauwen, B., and Massar, S.** *Information Processing Capacity of Dynamical Systems*, Scientific Reports 2 (2012), 514. [Author-institution record][DAMB].
- **Andreas, J., Dragan, A., and Klein, D.** *Translating Neuralese*, ACL (2017), 232–242. [Primary proceedings record][NEUR].
- **Rao, R. P. N., and colleagues.** *A Direct Brain-to-Brain Interface in Humans*, PLOS ONE 9 (2014), e111332. [Primary article][RAO].

### Dynamics, information and system design

- **Fefferman, C. L.** *Existence and Smoothness of the Navier–Stokes Equation*, official six-page Clay problem statement with errata. [Problem statement][FEF].
- **OpenAI.** *Finite Time Blowup for Navier–Stokes*, September 2026, 166 pages. [Research report][NSR]. *On the Navier–Stokes Millennium Prize Problem*, 8 September 2026, [announcement][NSA].
- **Clay Mathematics Institute.** *Navier–Stokes Equation*, status page read 26 October 2026; *Navier–Stokes Announcement*, 11 September 2026. [Status page][CLAY]; [dated response][CLAYNEWS].
- **Tao, T.** *Finite Time Blowup for an Averaged Three-Dimensional Navier–Stokes Equation*, Journal of the American Mathematical Society 29 (2016), 601–674. [Author preprint][TAO].
- **Cardona, R., Miranda, E., Peralta-Salas, D., and Presas, F.** *Constructing Turing Complete Euler Flows in Dimension 3*, PNAS 118 (2021), e2026818118. [Author preprint][EULER].
- **Cardona, R., Miranda, E., and Peralta-Salas, D.** *Computability and Beltrami Fields in Euclidean Space*, Journal de Mathématiques Pures et Appliquées 169 (2023), 50–81. [Author preprint][BEL].
- **Lei, Z.** *On Axially Symmetric Incompressible Magnetohydrodynamics in Three Dimensions*, first posted 2012. [Author preprint][LEI].
- **Bousquet, G. D., and Slotine, J.-J. E.** *A Contraction Based, Singular Perturbation Approach to Near-Decomposability in Complex Systems* (2015). [Author preprint][BS].
- **Brunton, S. L., Proctor, J. L., and Kutz, J. N.** *Discovering Governing Equations from Data by Sparse Identification of Nonlinear Dynamical Systems*, PNAS 113 (2016), 3932–3937. [Author preprint][SINDY].
- **Rudy, S. H., Brunton, S. L., Proctor, J. L., and Kutz, J. N.** *Data-Driven Discovery of Partial Differential Equations*, Science Advances 3 (2017), e1602614. [Author preprint][PDE].
- **Shannon, C. E.** *A Mathematical Theory of Communication*, Bell System Technical Journal 27 (1948), 379–423 and 623–656. [Corrected reprint][SHAN].
- **Bennett, C. H.** *Notes on Landauer's Principle, Reversible Computation, and Maxwell's Demon*, Studies in History and Philosophy of Modern Physics 34 (2003), 501–510. [Author preprint][BEN].
- **Abadi, M., and Lamport, L.** *The Existence of Refinement Mappings*, Theoretical Computer Science 82 (1991), 253–284; earlier LICS version (1988). [Author-hosted earlier paper][AL].
- **Girard, A., Julius, A. A., and Pappas, G. J.** *Approximate Simulation Relations for Hybrid Systems*, IFAC Proceedings Volumes 39(5) (2006), 106–111; extended journal treatment, Discrete Event Dynamic Systems 18 (2008), 163–179. [Author-hosted journal paper][GJP]; [coauthor's publication list][GJPB]. The source manuscript's two-author 2006 entry omitted Julius; this attribution includes him.
- **Benveniste, A., and colleagues.** *Contracts for System Design*, Foundations and Trends in Electronic Design Automation 12 (2018), 124–400. [Author-institution record][BC].
- **Schneider, F. B.** *Implementing Fault-Tolerant Services Using the State Machine Approach: A Tutorial*, ACM Computing Surveys 22 (1990), 299–319. [Author-hosted paper][SCH].
- **Cerf, V., and colleagues.** *Delay-Tolerant Networking Architecture*, RFC 4838, IRTF (2007), informational architecture. [RFC][DTN].
- **Fischer, M. J., Lynch, N. A., and Paterson, M. S.** *Impossibility of Distributed Consensus with One Faulty Process*, Journal of the ACM 32 (1985), 374–382. [Author-hosted paper][FLP].
- **Turing, A. M.** *On Computable Numbers, with an Application to the Entscheidungsproblem*, Proceedings of the London Mathematical Society 42 (1936–1937), 230–265. [Paper][TUR].
- **Hoeffding, W.** *Probability Inequalities for Sums of Bounded Random Variables*, Journal of the American Statistical Association 58 (1963), 13–30. [Publication identity][HOEF].

[LM]: #source-manuscript
[NIST]: https://csrc.nist.gov/glossary/term/air_gap
[TEMPEST]: https://csrc.nist.gov/glossary/term/tempest
[CHAN]: https://arxiv.org/abs/1503.07919
[FAN]: https://arxiv.org/abs/1606.05915
[AIR]: https://arxiv.org/abs/1411.0237
[GSM]: https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/guri
[NOAA]: https://www.spaceweather.gov/impacts/hf-radio-communications
[ECK]: https://arxiv.org/abs/0812.1554
[BUB]: https://cba.mit.edu/docs/papers/07.02.bubble.pdf
[BIO]: https://www.wisdom.weizmann.ac.il/~lbn/new_pages/Abstract.html
[SHEN]: https://arxiv.org/html/1610.02365v1
[WRIGHT]: https://arxiv.org/abs/2104.13386
[PFM]: https://arxiv.org/abs/2604.27911
[GPTQ]: https://arxiv.org/abs/2210.17323v2
[DAMB]: https://biblio.ugent.be/publication/2972574
[NEUR]: https://aclanthology.org/P17-1022/
[RAO]: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0111332
[FEF]: https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf
[NSR]: https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf
[NSA]: https://openai.com/index/navier-stokes-solution/
[CLAY]: https://www.claymath.org/millennium/navier-stokes-equation/
[CLAYNEWS]: https://www.claymath.org/news/navier-stokes-announcement/
[TAO]: https://arxiv.org/abs/1402.0290
[EULER]: https://arxiv.org/abs/2012.12828
[BEL]: https://arxiv.org/abs/2111.03559
[LEI]: https://arxiv.org/abs/1212.5968
[BS]: https://arxiv.org/abs/1512.08464
[SINDY]: https://arxiv.org/abs/1509.03580
[PDE]: https://arxiv.org/abs/1609.06401
[SHAN]: https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
[BEN]: https://arxiv.org/abs/physics/0210005
[AL]: https://lamport.azurewebsites.net/pubs/abadi-existence.pdf
[GJP]: https://sites.ecse.rpi.edu/~agung/Research/DEDS.pdf
[GJPB]: https://sites.ecse.rpi.edu/~agung/pubs.html
[BC]: https://research-explorer.ista.ac.at/record/5677
[SCH]: https://www.cs.cornell.edu/fbs/publications/SMSurvey.pdf
[DTN]: https://datatracker.ietf.org/doc/html/rfc4838
[FLP]: https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf
[TUR]: https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf
[HOEF]: https://doi.org/10.1080/01621459.1963.10500830

[CONT]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/theory/lineages/h-continuation/continuation_complete_orthing.md

[FORM]: https://github.com/theislampill/orthemology/blob/28679eaed33ee48cf0c5d15ba6dc3b27aac9067b/theory/lineages/h-formalisation/orthing_formalisation_v1.md


## Source guides for the additional arguments and qualifications

These exact public guides identify the reported results, historical review scopes and dependencies used in the additional discussion. A guide citation does not claim receipt or renewed verification of every linked proof, primary source or execution record.

- [GUIDE105-G003] Orthemology Seventh research restart checkpoint 1.
- [GUIDE105-G020] Reviewed dynamic V2 finite-history safety kernel.
- [GUIDE105-G026] Seventh research checkpoint 5 General proof coverage and source continuation.
- [GUIDE105-G043] External acceptance of the operational-model checkpoint.
- [GUIDE105-G068] Seventh research checkpoint 4 Compiled composition and baseline checks.
- [GUIDE105-G073] Seventh research checkpoint 3.
- [GUIDE105-G075] Nonuniform compact completion: isolated Lean extension.
- [GUIDE105-G082] Seventh research checkpoint 3 Current operational collection.
- [GUIDE105-G091] Law-completion correction: isolated Lean packet.

[GUIDE105-G003]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/051d8f8ebc0b27421fef9812de14b59ec9ccb55c46d00685faf75b2fee671698/README.md
[GUIDE105-G020]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/2bf4aa20d6c009bee1e1a5161163fa1686f48809cc9a37a01d6dc800e5e8e20a/README.md
[GUIDE105-G026]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/50a0407740b183f6ec3c7505584088d148fce3acde4108f3384f0dddd920daa6/README.md
[GUIDE105-G043]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/76507e2b3b55b455d380530dd9a152004a79f4a43001e1839b687131b268ffcf/README.md
[GUIDE105-G068]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/aa25f70324cba0ee0b90ed368549a2344b66c4470b5a7d5da3ec56a2c45c3e6c/README.md
[GUIDE105-G073]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/b3cdfd7d4208143c2f37da8f9ae2d220622a6af37f9acd6c633a61d657f13d9e/README.md
[GUIDE105-G075]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/bc1f50cf87277c4f726da9089d1ffded10bec3c149db94bc6d86a6c15a3e8be5/README.md
[GUIDE105-G082]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/d5287737a29ebdc21d94ada81bd78e77bcc6d7b904d101e541d536852a7b3329/README.md
[GUIDE105-G091]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/e0b751137b92a04177bcf5b2ca4452306cf082bc503cc794062310f6cfc9e8a6/README.md


## Exact formal sources for durable cancellation and conditional progress

These immutable source editions support §10.7. They remain distinct formal artifacts; their inclusion here does not replace imported source dependencies or renew historical execution claims.

- **R250-019 — RuntimeCancellationControls.lean.** Native Git blob `468d8c18ed20a05f58c075482920966d9a0a6df2`; SHA-256 `050d8724874a2f1c472ea60ac25ce1519cde3a0b2758352d5573b519b0c5e887`. [RuntimeCancellationControls.lean][R250-019]

- **R250-084 — BatchReadiness.lean.** Native Git blob `ce014f6154b7976ccecb1e881f4dcd584a17ff5e`; SHA-256 `1a3afb0987c9132f807f0579d1e120819a5741ca301c4ea0f00d978c88dc1ea5`. [BatchReadiness.lean][R250-084]

- **R250-113 — BatchSurvivalModel.lean.** Native Git blob `696dd2d6f77a7a3c5d4b270a97c21f9bb62b758f`; SHA-256 `21caabe1a994a1f137a91f5c15123a32e61ecc0c9c37ba98b9a7be7c918c8a65`. [BatchSurvivalModel.lean][R250-113]

- **R250-124 — JoinModel.lean.** Native Git blob `d713592505711077cdc84fda9a7c4a8e8302c963`; SHA-256 `25c695850ade6c70755dfe4cd87cb252079f0d9b219ed23945bba4d77dcfeac7`. [JoinModel.lean][R250-124]

- **R250-128 — RuntimeV4Challenges.lean.** Native Git blob `b715c006856f734c048ee72b033303976ca2610a`; SHA-256 `2660006e89558df2b8e21f19fc8e5d8d8ecadbafeb2aa00a7a35ce7860fba3ee`. [RuntimeV4Challenges.lean][R250-128]

- **R250-136 — Diagnostic_changed_action_has_no_receipt.lean.** Native Git blob `566ce9109eac6e6fba7f7a9f4bff3df64fa58da7`; SHA-256 `29ea2310e781b1854a06965507c04f4eab3833c1152d1b7d79795abd31571563`. [Diagnostic_changed_action_has_no_receipt.lean][R250-136]

- **R250-181 — BatchExactProgress.lean.** Native Git blob `2bb4e79e7c47b201f69649107ca06515b6aca83e`; SHA-256 `35e98610c0aefb3305142db213b83934f790ce7fee78f599e93ef344d7e19bce`. [BatchExactProgress.lean][R250-181]

- **R250-182 — BatchExactControls.lean.** Native Git blob `a25dfdbf3bb354944c24905cb92a01879681baae`; SHA-256 `36420f1e75f388c264ce66945c8106de0c1eb5df6c4898a4d9af8be981e20419`. [BatchExactControls.lean][R250-182]

- **R250-194 — Diagnostic_fresh_nonce_has_no_receipt.lean.** Native Git blob `d4e78ebb9e524bca8b44ab248b44638ed4d5912d`; SHA-256 `3993e78269f82b3bdf9df60e456ca5cec31bb9589a4ecb57d6341ceb2a9a46fa`. [Diagnostic_fresh_nonce_has_no_receipt.lean][R250-194]

- **R250-204 — SharedTrial.lean.** Native Git blob `729b02fb800042a63c2093c805b209fe7d4183c7`; SHA-256 `3c664ba712bd1edcd2547f280b6e51e56a7088662b746a4c3837dca21209a4f8`. [SharedTrial.lean][R250-204]

- **R250-205 — RuntimeCancellationTrace.lean.** Native Git blob `5672a0fbe9f977378815c5fca76b16622cb63f74`; SHA-256 `3cf48bc4bcd643d8731360235688fb214b48c664f95d77d851c2a9ceec0d52ba`. [RuntimeCancellationTrace.lean][R250-205]

- **R250-206 — ContractControls.lean.** Native Git blob `186d9423522ba9e38e879ead8ae28b551cfc7ad1`; SHA-256 `3d00e3902bcae260c5da8f97e1c09584095081c7fc094df8e5f8e3e800043f7c`. [ContractControls.lean][R250-206]

- **R250-213 — BatchMemory.lean.** Native Git blob `76c40853ba5789854b28b962f8171e1e41cadf58`; SHA-256 `3f1f515f339a1ee07b2c148e4e143c286833b63a9b8feed12f818235efdfc1f6`. [BatchMemory.lean][R250-213]

- **R250-216 — CoreChallenges.lean.** Native Git blob `bd710a24a09e28e1f6caac045cf99d3f9240271d`; SHA-256 `3fd4d907b3c6b3b41cc608767cd3f48e603303cff76842aa5c62db20f42de94a`. [CoreChallenges.lean][R250-216]

- **R250-228 — CoreContractControls.lean.** Native Git blob `28bfeffaaf1ec2e62164779b38908942b53af08f`; SHA-256 `41e847dd182ef3bedae7fb6c3461cca2382904119cfc04fbef56c7146a84218e`. [CoreContractControls.lean][R250-228]

- **R250-229 — BatchUniqueness.lean.** Native Git blob `e5c66e80d40720abbd2c607127766f3e49571f6e`; SHA-256 `41e94ef85091bee475d23e9c7e8d3126db7ad45f665034bdd84059ec4842fd3a`. [BatchUniqueness.lean][R250-229]

- **R250-237 — SourceController.lean.** Native Git blob `35dc874632ef05bb764a4c04df90e71d80fb3d53`; SHA-256 `43fcfb07d40fddb7a0a5bf980255aa24df81426f157d8f70d5c4a01f95b1d07c`. [SourceController.lean][R250-237]

- **R250-248 — BatchRetryControls.lean.** Native Git blob `09760d029d05f1cb179a176f24c9587b46cf1ee7`; SHA-256 `4565c5e0f9b2aa7748588a56cc923ae1ca6f15fbd34f5da18b197a43388fcd24`. [BatchRetryControls.lean][R250-248]

- **R250-249 — SharedController.lean.** Native Git blob `7228ae4a77246d2cfbe4cac46a348050397a5527`; SHA-256 `4583107aeea76ec0de8470f890406ba7e1c31fb9aa1b8918fc252e02c5d796f0`. [SharedController.lean][R250-249]

[R250-019]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/050d8724874a2f1c472ea60ac25ce1519cde3a0b2758352d5573b519b0c5e887/RuntimeCancellationControls.lean

[R250-084]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1a3afb0987c9132f807f0579d1e120819a5741ca301c4ea0f00d978c88dc1ea5/BatchReadiness.lean

[R250-113]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/21caabe1a994a1f137a91f5c15123a32e61ecc0c9c37ba98b9a7be7c918c8a65/BatchSurvivalModel.lean

[R250-124]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/25c695850ade6c70755dfe4cd87cb252079f0d9b219ed23945bba4d77dcfeac7/JoinModel.lean

[R250-128]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2660006e89558df2b8e21f19fc8e5d8d8ecadbafeb2aa00a7a35ce7860fba3ee/RuntimeV4Challenges.lean

[R250-136]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/29ea2310e781b1854a06965507c04f4eab3833c1152d1b7d79795abd31571563/Diagnostic_changed_action_has_no_receipt.lean

[R250-181]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/35e98610c0aefb3305142db213b83934f790ce7fee78f599e93ef344d7e19bce/BatchExactProgress.lean

[R250-182]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/36420f1e75f388c264ce66945c8106de0c1eb5df6c4898a4d9af8be981e20419/BatchExactControls.lean

[R250-194]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3993e78269f82b3bdf9df60e456ca5cec31bb9589a4ecb57d6341ceb2a9a46fa/Diagnostic_fresh_nonce_has_no_receipt.lean

[R250-204]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3c664ba712bd1edcd2547f280b6e51e56a7088662b746a4c3837dca21209a4f8/SharedTrial.lean

[R250-205]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3cf48bc4bcd643d8731360235688fb214b48c664f95d77d851c2a9ceec0d52ba/RuntimeCancellationTrace.lean

[R250-206]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3d00e3902bcae260c5da8f97e1c09584095081c7fc094df8e5f8e3e800043f7c/ContractControls.lean

[R250-213]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3f1f515f339a1ee07b2c148e4e143c286833b63a9b8feed12f818235efdfc1f6/BatchMemory.lean

[R250-216]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3fd4d907b3c6b3b41cc608767cd3f48e603303cff76842aa5c62db20f42de94a/CoreChallenges.lean

[R250-228]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/41e847dd182ef3bedae7fb6c3461cca2382904119cfc04fbef56c7146a84218e/CoreContractControls.lean

[R250-229]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/41e94ef85091bee475d23e9c7e8d3126db7ad45f665034bdd84059ec4842fd3a/BatchUniqueness.lean

[R250-237]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/43fcfb07d40fddb7a0a5bf980255aa24df81426f157d8f70d5c4a01f95b1d07c/SourceController.lean

[R250-248]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4565c5e0f9b2aa7748588a56cc923ae1ca6f15fbd34f5da18b197a43388fcd24/BatchRetryControls.lean

[R250-249]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4583107aeea76ec0de8470f890406ba7e1c31fb9aa1b8918fc252e02c5d796f0/SharedController.lean
[R250-148]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2dcdece2b95688d09b736bc46fe1258a05ecf93a2dfd05f322637511a3e3edbb/FAMILY104_CURRENT_SCOPE.md "Retained public DERIVED assessment projection; Git 597c89055e2e95edb6f5c3f8f255a1ec2c72379b; SHA-256 2dcdece2b95688d09b736bc46fe1258a05ecf93a2dfd05f322637511a3e3edbb"


## Exact formal sources for typed histories and the ordered controller

[R250-018] SourceAttemptTransport.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/04c3c9bf44070ad2a03a714a224d0b75602ad9e96a16f94552fa44c26b3112e9/SourceAttemptTransport.lean); native Git blob `57b1aa63fdd0ced3072105d1c4082b4823bfb11d`, 3,987 bytes, SHA-256 `04c3c9bf44070ad2a03a714a224d0b75602ad9e96a16f94552fa44c26b3112e9`.

[R250-030] FinitePortfolio.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/078300119e296335d1a3d2fa02eefb62419f51fc0a8685c72238d1d3f964957c/FinitePortfolio.lean); native Git blob `18c3ec8f34c75e8b231774a05711b25645ece269`, 5,983 bytes, SHA-256 `078300119e296335d1a3d2fa02eefb62419f51fc0a8685c72238d1d3f964957c`.

[R250-031] NativeExecutionChecks.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/07c02ba31fa6a551b4d5dc93364a6e794d5f8f458cb3e7699c66e84c4beaf7ca/NativeExecutionChecks.lean); native Git blob `927f931b72557657feddda3fb0c9b8dd4ff08547`, 3,237 bytes, SHA-256 `07c02ba31fa6a551b4d5dc93364a6e794d5f8f458cb3e7699c66e84c4beaf7ca`.

[R250-039] BatchCleanup.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/09a245aa1374d14a4d6ab0e793a61f40ef488a7f3df7fda5c30c6453ac9bd6ea/BatchCleanup.lean); native Git blob `519730d55b69348de7c1da7ed23cfb8c5fac67e3`, 5,404 bytes, SHA-256 `09a245aa1374d14a4d6ab0e793a61f40ef488a7f3df7fda5c30c6453ac9bd6ea`.

[R250-043] JoinSafety.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/09f8fe24a6cbed4f48b14116cedd44a4f6371e37145655e88483bd9e04f5899e/JoinSafety.lean); native Git blob `4098470c5b0a95ec973fa297fb1d696ee86f8b9b`, 6,657 bytes, SHA-256 `09f8fe24a6cbed4f48b14116cedd44a4f6371e37145655e88483bd9e04f5899e`.

[R250-052] NativeServiceOrder.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0e6f7c025bb96f6935e91b669f166c49a2025bd07553c1e2421b217fd2bea739/NativeServiceOrder.lean); native Git blob `4b93cb681c5ca41e52c4bd5851b3212fb66cfa2a`, 7,156 bytes, SHA-256 `0e6f7c025bb96f6935e91b669f166c49a2025bd07553c1e2421b217fd2bea739`.

[R250-068] BatchTests.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/12b365143d21b350d99048b06225bb64bc527990e302854dc3c901d224a89bcd/BatchTests.lean); native Git blob `2492913c9d4b0dec9f5a61850cb6417fac7f2669`, 2,344 bytes, SHA-256 `12b365143d21b350d99048b06225bb64bc527990e302854dc3c901d224a89bcd`.

[R250-070] SharedStateTransport.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/13730c2c61b4003f7a93ed434b19cba9db7865954bbd8032246303080d994a3b/SharedStateTransport.lean); native Git blob `6394cb304109b436f172ff40e67109faf602450f`, 8,529 bytes, SHA-256 `13730c2c61b4003f7a93ed434b19cba9db7865954bbd8032246303080d994a3b`.

[R250-072] BatchAvailabilityIffSourceChallenges.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/140b6548e7440f6ade39fee2b161044ffa62b580538ad2b080afd9cb2619bb78/BatchAvailabilityIffSourceChallenges.lean); native Git blob `669b65d2a5dda896bcf6cb833cb970c8c1c7e539`, 3,334 bytes, SHA-256 `140b6548e7440f6ade39fee2b161044ffa62b580538ad2b080afd9cb2619bb78`.

[R250-080] BatchFrames.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/189400bb156da6be2aa53fa422acd6e6277d373e5aab5b683616318378712148/BatchFrames.lean); native Git blob `09492d06b7c8ec8d6849bf8ddf6bd102871b5e4a`, 5,280 bytes, SHA-256 `189400bb156da6be2aa53fa422acd6e6277d373e5aab5b683616318378712148`.

[R250-097] NativeExecutionData.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1ecb4c51487ba020a0df9779ab206af74eb67b85bbaedcaa86ff2214ef2eab24/NativeExecutionData.lean); native Git blob `768406453677646100f3347b2df73a50b778550e`, 1,668 bytes, SHA-256 `1ecb4c51487ba020a0df9779ab206af74eb67b85bbaedcaa86ff2214ef2eab24`.

[R250-099] BatchSource.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1ef04bf3dbc517ee9427bca459b428b29ce04bd89ba1cd73716b3eec262f7871/BatchSource.lean); native Git blob `10f321240909c348e5686252ae6be65a8bc3d144`, 5,964 bytes, SHA-256 `1ef04bf3dbc517ee9427bca459b428b29ce04bd89ba1cd73716b3eec262f7871`.

[R250-120] TypedHistoryProperties.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/246e8b03c7505328d9363b6a7a2b24af1cfe1ef77f3380bbcd9e033b96b4b138/TypedHistoryProperties.lean); native Git blob `2f681d573618c679979117d0d12b42cb93dcff95`, 7,018 bytes, SHA-256 `246e8b03c7505328d9363b6a7a2b24af1cfe1ef77f3380bbcd9e033b96b4b138`.

[R250-133] TypedV2Challenges.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2937ef95cc90678547409a1850e0883da48c400b2bcd106586853155eac22e28/TypedV2Challenges.lean); native Git blob `edc07c50444e46e7cd14d3fcfe27a8de36554263`, 4,894 bytes, SHA-256 `2937ef95cc90678547409a1850e0883da48c400b2bcd106586853155eac22e28`.

[R250-144] OrderedContractControls.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2cc7c155bb04a2180ed1294dc12c9551bcf4400745b097b66d6bb9d0914f4307/OrderedContractControls.lean); native Git blob `ec647f4be158efce142be7250f51e068a68e44b3`, 1,826 bytes, SHA-256 `2cc7c155bb04a2180ed1294dc12c9551bcf4400745b097b66d6bb9d0914f4307`.

[R250-156] NativeOrderedProgram.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/300e7a9b8a3dc02d576cc45860a16dc90c40185466d718cda4f513b04f7108f4/NativeOrderedProgram.lean); native Git blob `7ba6db5844274abec7f559cb4a03364c73f5eb05`, 10,067 bytes, SHA-256 `300e7a9b8a3dc02d576cc45860a16dc90c40185466d718cda4f513b04f7108f4`.

[R250-160] LifecycleDelivery.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/30f617de7a5186a16dcca0050bd0ea159223d21ae1a1ffd95825c0ae9c59ba5d/LifecycleDelivery.lean); native Git blob `ec466f21810e522a844ec417725df892a08fce97`, 5,395 bytes, SHA-256 `30f617de7a5186a16dcca0050bd0ea159223d21ae1a1ffd95825c0ae9c59ba5d`.

[R250-166] NativeController.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/32d0d50457bc604dd040b06e74b28e4e10cb2870e05206b0380b19f03648f2fb/NativeController.lean); native Git blob `636aade8d9033b8f1308d59214754f13e7726e80`, 14,486 bytes, SHA-256 `32d0d50457bc604dd040b06e74b28e4e10cb2870e05206b0380b19f03648f2fb`.

[R250-190] TypedInstantiation.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/38d79954d4934e6d5c627efea77aa672a5dc944fa26e6c101715448b496389e1/TypedInstantiation.lean); native Git blob `b324e8d30e9f2287361dca60a8fa35d9c8863514`, 13,866 bytes, SHA-256 `38d79954d4934e6d5c627efea77aa672a5dc944fa26e6c101715448b496389e1`.

[R250-230] CriterionInstallation.lean. Exact source at [a7ff0e33](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/421084add94732b1b81154923efe38c30ae8df75825b94f2595ec6e7bc2f51c9/CriterionInstallation.lean); native Git blob `5b2115f24e26269163ef5a3633ab432b757a08ef`, 8,513 bytes, SHA-256 `421084add94732b1b81154923efe38c30ae8df75825b94f2595ec6e7bc2f51c9`.


### Exact sources for finite survival and effective queries

[R250-C037] LawCompletionBranches.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/096e4c454af036875c6b9f95a2a1a37724708b7ebab741044f38335de3d67e7d/LawCompletionBranches.lean.

[R250-C063] CHECKED_SCOPE.md. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/10e2a4de40dd7a6a2c3fe1e7bc86683fc85f10d0ac236520ce37b7441fbedee0/CHECKED_SCOPE.md.

[R250-C073] IndexedCompletionReadback.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/145d232cd81c75ab228bc3f791b4dcee91b0a52def7ebafaac4035666cc0c76e/IndexedCompletionReadback.lean.

[R250-C152] MATHEMATICAL_CONTROLS.md. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2f9f3b008b1afeac4ef9e3786835e811c95a9ad84d96c30c90dcda93f7b50b53/MATHEMATICAL_CONTROLS.md.

[R250-C243] ReviewerControls.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/44c033325bf422ab2b15a6cd58753fa4b6ab8f7dac04eb004bf9062bc6060f11/ReviewerControls.lean.



## Exact sources for selector representation and joint continuation

[SEL8]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0292fcacef3e13fa618c20bc5eea58ed617d85cc43e7624f60f549a3d803c5cb/SCIENTIFIC_SCOPE.md
[SEL42]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/09ecb596817c6df3371f4570ddd7855c863e34863e07aab2ad130d4178cf38f9/CertifiedSelectorFamily.lean
[JOIN79]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1847d9defcef9bf83a4aa5caf8f7658d468ef497d45548514c5a66dcc99cd247/CANDIDATE_RELATION_AND_SCOPE.md
[SEL91]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1d6960b44f149cafab4de9b53c35155fe4f29cad6b9f82137b60d011e2ebf11a/ReviewerTransportBoundaries.lean
[SEL197]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3a43274f399b332eca32613feee11257364b862bda96c8c73f303490184e0bbc/SelectorCallDomains.lean
[SEL217]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3ff2d9315ca3c70a9d3007a985b7d91c8cd2ed61dfd42b04bca0eb9df14b9c10/ReviewerSuppliedConsumer.lean



## Exact sources for source-warrant and interlock qualifications

These exact-public bodies were read as scientific prose or source code. Review replay statements are attributed historical evidence; no new execution or inspection of their referenced originals is claimed. Batch indices identify the present250-file cohort; manifest indices preserve its admission-source identities.

- **N250A-000**, cohort row0, manifest28395: [REVIEW.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ff64060c0e14ba67437f92f5b714aa7018941c26b9afdf2aa86aba9cbe8bad69/REVIEW.md). Exact repository path `experiments/orthemology-v5-successors/source-store/ff64060c0e14ba67437f92f5b714aa7018941c26b9afdf2aa86aba9cbe8bad69/REVIEW.md`; SHA-256 `ff64060c0e14ba67437f92f5b714aa7018941c26b9afdf2aa86aba9cbe8bad69`; 12,511 bytes. Role: authored_argument.

[N250A-000]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ff64060c0e14ba67437f92f5b714aa7018941c26b9afdf2aa86aba9cbe8bad69/REVIEW.md

- **N250A-001**, cohort row1, manifest25383: [SPEC.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e39f418d04d5bb4e5e7a8866150a0aca063a79da707d450f48afbf43623785b1/SPEC.md). Exact repository path `experiments/orthemology-v5-successors/source-store/e39f418d04d5bb4e5e7a8866150a0aca063a79da707d450f48afbf43623785b1/SPEC.md`; SHA-256 `e39f418d04d5bb4e5e7a8866150a0aca063a79da707d450f48afbf43623785b1`; 2,340 bytes. Role: authored_argument.

[N250A-001]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e39f418d04d5bb4e5e7a8866150a0aca063a79da707d450f48afbf43623785b1/SPEC.md

- **N250A-002**, cohort row2, manifest2967: [PUBLIC_VERIFICATION.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1b8136e143af5a48f0c92191e8722e82ec939f441a1b5793514e842a72bfb54f/PUBLIC_VERIFICATION.md). Exact repository path `experiments/orthemology-v5-successors/source-store/1b8136e143af5a48f0c92191e8722e82ec939f441a1b5793514e842a72bfb54f/PUBLIC_VERIFICATION.md`; SHA-256 `1b8136e143af5a48f0c92191e8722e82ec939f441a1b5793514e842a72bfb54f`; 1,987 bytes. Role: authored_argument.

[N250A-002]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1b8136e143af5a48f0c92191e8722e82ec939f441a1b5793514e842a72bfb54f/PUBLIC_VERIFICATION.md

- **N250A-003**, cohort row3, manifest13143: [CRITERION_REVIEW_V3.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7657c1ef78490a622fd17d88a7737e716da7ee6a5325248bf2a7cefc985b0e6c/CRITERION_REVIEW_V3.md). Exact repository path `experiments/orthemology-v5-successors/source-store/7657c1ef78490a622fd17d88a7737e716da7ee6a5325248bf2a7cefc985b0e6c/CRITERION_REVIEW_V3.md`; SHA-256 `7657c1ef78490a622fd17d88a7737e716da7ee6a5325248bf2a7cefc985b0e6c`; 8,087 bytes. Role: authored_argument.

[N250A-003]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7657c1ef78490a622fd17d88a7737e716da7ee6a5325248bf2a7cefc985b0e6c/CRITERION_REVIEW_V3.md

- **N250A-004**, cohort row4, manifest12773: [REVIEW_V2.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/73691b50b7a287522d03076011756b9e7c57dd3214935a10062f565c4a889f3f/REVIEW_V2.md). Exact repository path `experiments/orthemology-v5-successors/source-store/73691b50b7a287522d03076011756b9e7c57dd3214935a10062f565c4a889f3f/REVIEW_V2.md`; SHA-256 `73691b50b7a287522d03076011756b9e7c57dd3214935a10062f565c4a889f3f`; 9,923 bytes. Role: authored_argument.

[N250A-004]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/73691b50b7a287522d03076011756b9e7c57dd3214935a10062f565c4a889f3f/REVIEW_V2.md

- **N250A-011**, cohort row11, manifest9875: [CANDIDATE_E_COLD_ASSESSMENT.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/59ac68fa9278932de6f35d30ef219bc7af9eca63e84f843e4b256103c2afb16e/CANDIDATE_E_COLD_ASSESSMENT.md). Exact repository path `experiments/orthemology-v5-successors/source-store/59ac68fa9278932de6f35d30ef219bc7af9eca63e84f843e4b256103c2afb16e/CANDIDATE_E_COLD_ASSESSMENT.md`; SHA-256 `59ac68fa9278932de6f35d30ef219bc7af9eca63e84f843e4b256103c2afb16e`; 11,404 bytes. Role: authored_argument.

[N250A-011]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/59ac68fa9278932de6f35d30ef219bc7af9eca63e84f843e4b256103c2afb16e/CANDIDATE_E_COLD_ASSESSMENT.md

- **N250A-012**, cohort row12, manifest8478: [CRITERION_INSTALLATION_ARGUMENT.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4df16d4432931594e928292b9b1535f195588d8ac5bd6af4ab5cd7aa1b0cf7c2/CRITERION_INSTALLATION_ARGUMENT.md). Exact repository path `experiments/orthemology-v5-successors/source-store/4df16d4432931594e928292b9b1535f195588d8ac5bd6af4ab5cd7aa1b0cf7c2/CRITERION_INSTALLATION_ARGUMENT.md`; SHA-256 `4df16d4432931594e928292b9b1535f195588d8ac5bd6af4ab5cd7aa1b0cf7c2`; 8,924 bytes. Role: authored_argument.

[N250A-012]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4df16d4432931594e928292b9b1535f195588d8ac5bd6af4ab5cd7aa1b0cf7c2/CRITERION_INSTALLATION_ARGUMENT.md

- **N250A-013**, cohort row13, manifest19653: [CRITERION_INSTALLATION_SPEC.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b0782e11f4873366bcc603a687553e717d0ee20e37e66e71cc75970a7f38d9a2/CRITERION_INSTALLATION_SPEC.md). Exact repository path `experiments/orthemology-v5-successors/source-store/b0782e11f4873366bcc603a687553e717d0ee20e37e66e71cc75970a7f38d9a2/CRITERION_INSTALLATION_SPEC.md`; SHA-256 `b0782e11f4873366bcc603a687553e717d0ee20e37e66e71cc75970a7f38d9a2`; 3,969 bytes. Role: authored_argument.

[N250A-013]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b0782e11f4873366bcc603a687553e717d0ee20e37e66e71cc75970a7f38d9a2/CRITERION_INSTALLATION_SPEC.md

- **N250A-014**, cohort row14, manifest4378: [REVIEW_SUMMARY.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/289830061d35809c9ab1d3103b04898ba066a2d4bfd7519ffbcec79c1367cf2b/REVIEW_SUMMARY.md). Exact repository path `experiments/orthemology-v5-successors/source-store/289830061d35809c9ab1d3103b04898ba066a2d4bfd7519ffbcec79c1367cf2b/REVIEW_SUMMARY.md`; SHA-256 `289830061d35809c9ab1d3103b04898ba066a2d4bfd7519ffbcec79c1367cf2b`; 2,214 bytes. Role: authored_argument.

[N250A-014]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/289830061d35809c9ab1d3103b04898ba066a2d4bfd7519ffbcec79c1367cf2b/REVIEW_SUMMARY.md

- **N250A-015**, cohort row15, manifest457: [SPECIFICATION.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0455329eb125848dbdb0601e5e75221804355094382cdf20cd004e59dded8603/SPECIFICATION.md). Exact repository path `experiments/orthemology-v5-successors/source-store/0455329eb125848dbdb0601e5e75221804355094382cdf20cd004e59dded8603/SPECIFICATION.md`; SHA-256 `0455329eb125848dbdb0601e5e75221804355094382cdf20cd004e59dded8603`; 6,894 bytes. Role: authored_argument.

[N250A-015]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0455329eb125848dbdb0601e5e75221804355094382cdf20cd004e59dded8603/SPECIFICATION.md

- **N250A-016**, cohort row16, manifest14893: [TRANSPORT_ARGUMENT.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/855b8f438e5d5f05b53e2d6ee151375a1601d3e568f53b31316b336f07f3def1/TRANSPORT_ARGUMENT.md). Exact repository path `experiments/orthemology-v5-successors/source-store/855b8f438e5d5f05b53e2d6ee151375a1601d3e568f53b31316b336f07f3def1/TRANSPORT_ARGUMENT.md`; SHA-256 `855b8f438e5d5f05b53e2d6ee151375a1601d3e568f53b31316b336f07f3def1`; 21,081 bytes. Role: authored_argument.

[N250A-016]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/855b8f438e5d5f05b53e2d6ee151375a1601d3e568f53b31316b336f07f3def1/TRANSPORT_ARGUMENT.md

- **N250A-017**, cohort row17, manifest10012: [bounded_audit.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5af09df76949eac6fc6d179b3be863f77bb7c0fcf1bdfe09fcd2d7b67f38d8ef/bounded_audit.py). Exact repository path `experiments/orthemology-v5-successors/source-store/5af09df76949eac6fc6d179b3be863f77bb7c0fcf1bdfe09fcd2d7b67f38d8ef/bounded_audit.py`; SHA-256 `5af09df76949eac6fc6d179b3be863f77bb7c0fcf1bdfe09fcd2d7b67f38d8ef`; 9,338 bytes. Role: authored_code.

[N250A-017]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5af09df76949eac6fc6d179b3be863f77bb7c0fcf1bdfe09fcd2d7b67f38d8ef/bounded_audit.py

- **N250A-018**, cohort row18, manifest24542: [criterion_model.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dbe3d8618c340acea59a052b4a8ccef2526b93b2f50b3f9db334101fe327aa11/criterion_model.py). Exact repository path `experiments/orthemology-v5-successors/source-store/dbe3d8618c340acea59a052b4a8ccef2526b93b2f50b3f9db334101fe327aa11/criterion_model.py`; SHA-256 `dbe3d8618c340acea59a052b4a8ccef2526b93b2f50b3f9db334101fe327aa11`; 3,328 bytes. Role: authored_code.

[N250A-018]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dbe3d8618c340acea59a052b4a8ccef2526b93b2f50b3f9db334101fe327aa11/criterion_model.py

- **N250A-019**, cohort row19, manifest10572: [rule_install_audit.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5fdc620bae68555e3f99e1626887553f90038505059cb2f1dc5b75efd03ad94a/rule_install_audit.py). Exact repository path `experiments/orthemology-v5-successors/source-store/5fdc620bae68555e3f99e1626887553f90038505059cb2f1dc5b75efd03ad94a/rule_install_audit.py`; SHA-256 `5fdc620bae68555e3f99e1626887553f90038505059cb2f1dc5b75efd03ad94a`; 5,993 bytes. Role: authored_code.

[N250A-019]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5fdc620bae68555e3f99e1626887553f90038505059cb2f1dc5b75efd03ad94a/rule_install_audit.py

- **N250A-020**, cohort row20, manifest18881: [rule_install_model.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a9a7c5efa87b3e714799a501834bd1fa0cdf2c251693d34a8a79da1f08b9b9f7/rule_install_model.py). Exact repository path `experiments/orthemology-v5-successors/source-store/a9a7c5efa87b3e714799a501834bd1fa0cdf2c251693d34a8a79da1f08b9b9f7/rule_install_model.py`; SHA-256 `a9a7c5efa87b3e714799a501834bd1fa0cdf2c251693d34a8a79da1f08b9b9f7`; 3,245 bytes. Role: authored_code.

[N250A-020]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a9a7c5efa87b3e714799a501834bd1fa0cdf2c251693d34a8a79da1f08b9b9f7/rule_install_model.py

- **N250A-021**, cohort row21, manifest6687: [shared_fixture_check.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3d3ba9169f19449c44428ce8b873a585bb527750a4c68633fca95e0d060a681d/shared_fixture_check.py). Exact repository path `experiments/orthemology-v5-successors/source-store/3d3ba9169f19449c44428ce8b873a585bb527750a4c68633fca95e0d060a681d/shared_fixture_check.py`; SHA-256 `3d3ba9169f19449c44428ce8b873a585bb527750a4c68633fca95e0d060a681d`; 5,117 bytes. Role: authored_code.

[N250A-021]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3d3ba9169f19449c44428ce8b873a585bb527750a4c68633fca95e0d060a681d/shared_fixture_check.py

- **N250A-022**, cohort row22, manifest10695: [test_criterion_model.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6109638cb1ea2d2d427e37867974e2670751b60caf71514078bc01df3e1b0807/test_criterion_model.py). Exact repository path `experiments/orthemology-v5-successors/source-store/6109638cb1ea2d2d427e37867974e2670751b60caf71514078bc01df3e1b0807/test_criterion_model.py`; SHA-256 `6109638cb1ea2d2d427e37867974e2670751b60caf71514078bc01df3e1b0807`; 6,702 bytes. Role: authored_code.

[N250A-022]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6109638cb1ea2d2d427e37867974e2670751b60caf71514078bc01df3e1b0807/test_criterion_model.py

- **N250A-023**, cohort row23, manifest4160: [test_rule_installation.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/267fffa1ff0237bb291dd28e07a59519c83514bcde1dc0b87de77ab3639cc1ce/test_rule_installation.py). Exact repository path `experiments/orthemology-v5-successors/source-store/267fffa1ff0237bb291dd28e07a59519c83514bcde1dc0b87de77ab3639cc1ce/test_rule_installation.py`; SHA-256 `267fffa1ff0237bb291dd28e07a59519c83514bcde1dc0b87de77ab3639cc1ce`; 6,980 bytes. Role: authored_code.

[N250A-023]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/267fffa1ff0237bb291dd28e07a59519c83514bcde1dc0b87de77ab3639cc1ce/test_rule_installation.py

- **N250A-025**, cohort row25, manifest26982: [REVIEW_CHANGELOG.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f2707b7041e595ac32c378e871abef835b2b3e9e0cb7c15a2e0c8c13b3852466/REVIEW_CHANGELOG.md). Exact repository path `experiments/orthemology-v5-successors/source-store/f2707b7041e595ac32c378e871abef835b2b3e9e0cb7c15a2e0c8c13b3852466/REVIEW_CHANGELOG.md`; SHA-256 `f2707b7041e595ac32c378e871abef835b2b3e9e0cb7c15a2e0c8c13b3852466`; 2,294 bytes. Role: authored_argument.

[N250A-025]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f2707b7041e595ac32c378e871abef835b2b3e9e0cb7c15a2e0c8c13b3852466/REVIEW_CHANGELOG.md

- **N250A-026**, cohort row26, manifest23957: [dynamic_interlock.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d67b95645512d78c51cab469cc71fc4fc5fd622a7c379481f1ee178e1031052a/dynamic_interlock.py). Exact repository path `experiments/orthemology-v5-successors/source-store/d67b95645512d78c51cab469cc71fc4fc5fd622a7c379481f1ee178e1031052a/dynamic_interlock.py`; SHA-256 `d67b95645512d78c51cab469cc71fc4fc5fd622a7c379481f1ee178e1031052a`; 13,538 bytes. Role: authored_code.

[N250A-026]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d67b95645512d78c51cab469cc71fc4fc5fd622a7c379481f1ee178e1031052a/dynamic_interlock.py

- **N250A-028**, cohort row28, manifest19149: [verify_dynamic.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ac4170a11a1487f4a4ae8079c7d8cc5d2971434968c92bec970922b0a2f80230/verify_dynamic.py). Exact repository path `experiments/orthemology-v5-successors/source-store/ac4170a11a1487f4a4ae8079c7d8cc5d2971434968c92bec970922b0a2f80230/verify_dynamic.py`; SHA-256 `ac4170a11a1487f4a4ae8079c7d8cc5d2971434968c92bec970922b0a2f80230`; 19,352 bytes. Role: authored_code.

[N250A-028]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ac4170a11a1487f4a4ae8079c7d8cc5d2971434968c92bec970922b0a2f80230/verify_dynamic.py

- **N250A-031**, cohort row31, manifest13654: [STATEMENT_AND_SOURCE.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7ae9af2dec2088c39766758f5565f2c2bd6536fbb7a9bd80f140087d3fb17a62/STATEMENT_AND_SOURCE.md). Exact repository path `experiments/orthemology-v5-successors/source-store/7ae9af2dec2088c39766758f5565f2c2bd6536fbb7a9bd80f140087d3fb17a62/STATEMENT_AND_SOURCE.md`; SHA-256 `7ae9af2dec2088c39766758f5565f2c2bd6536fbb7a9bd80f140087d3fb17a62`; 14,660 bytes. Role: authored_argument.

[N250A-031]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7ae9af2dec2088c39766758f5565f2c2bd6536fbb7a9bd80f140087d3fb17a62/STATEMENT_AND_SOURCE.md

- **N250A-032**, cohort row32, manifest16099: [check_controls.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/90162a106383eedfb2f7be6a31236c42a81c78d563500d21090b1fb4e2fd3745/check_controls.py). Exact repository path `experiments/orthemology-v5-successors/source-store/90162a106383eedfb2f7be6a31236c42a81c78d563500d21090b1fb4e2fd3745/check_controls.py`; SHA-256 `90162a106383eedfb2f7be6a31236c42a81c78d563500d21090b1fb4e2fd3745`; 2,070 bytes. Role: authored_code.

[N250A-032]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/90162a106383eedfb2f7be6a31236c42a81c78d563500d21090b1fb4e2fd3745/check_controls.py

- **N250A-033**, cohort row33, manifest20397: [REVIEW.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b72e810387325bbde14d9a565b03501b2b1326e26cd63df85069ce1a2789dfa2/REVIEW.md). Exact repository path `experiments/orthemology-v5-successors/source-store/b72e810387325bbde14d9a565b03501b2b1326e26cd63df85069ce1a2789dfa2/REVIEW.md`; SHA-256 `b72e810387325bbde14d9a565b03501b2b1326e26cd63df85069ce1a2789dfa2`; 5,713 bytes. Role: authored_argument.

[N250A-033]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b72e810387325bbde14d9a565b03501b2b1326e26cd63df85069ce1a2789dfa2/REVIEW.md

- **N250A-034**, cohort row34, manifest22613: [source_replay.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cada8edbe323dcb7d3ca352103afc0e3e8a30622b0ed08687643672e4e13c6ba/source_replay.py). Exact repository path `experiments/orthemology-v5-successors/source-store/cada8edbe323dcb7d3ca352103afc0e3e8a30622b0ed08687643672e4e13c6ba/source_replay.py`; SHA-256 `cada8edbe323dcb7d3ca352103afc0e3e8a30622b0ed08687643672e4e13c6ba`; 3,862 bytes. Role: authored_code.

[N250A-034]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cada8edbe323dcb7d3ca352103afc0e3e8a30622b0ed08687643672e4e13c6ba/source_replay.py

## Exact public sources for the Ninth argument and evidence reconciliation

[N250C-095]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/ec1c011309d1d4c35fb867cd18366f3a02c52f0217c282c0189d9c8c2cce7c55/PUBLIC_ACCEPTANCE.md "Next-250 cohort index 95; SHA-256 ec1c011309d1d4c35fb867cd18366f3a02c52f0217c282c0189d9c8c2cce7c55"
[N250C-096]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/aed43e209215077ef16e9855537f2a895dcbd9e82af5c00626a17c74f08e650b/PUBLIC_OCCURRENCE_ATTRIBUTION_CASE.md "Next-250 cohort index 96; SHA-256 aed43e209215077ef16e9855537f2a895dcbd9e82af5c00626a17c74f08e650b"
[N250C-097]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/edb51175abfa5a10afea085802e37f95cfc4840d68f9ecd0c7d860b9e94fa83b/RESTRICTED_REPAIR_AND_NEXT_HANDOFF_MODEL.md "Next-250 cohort index 97; SHA-256 edb51175abfa5a10afea085802e37f95cfc4840d68f9ecd0c7d860b9e94fa83b"
[N250C-098]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/79291b4294872f89ea37dc834dd4fb38b49acb5777c0b106007dbb2a1091e21c/SYNTHESIS_RESULT.md "Next-250 cohort index 98; SHA-256 79291b4294872f89ea37dc834dd4fb38b49acb5777c0b106007dbb2a1091e21c"
[N250C-099]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/c040382cd3b5d7be31e243f837edbaf335d5f265c4e4e5e8ee38bd5d6c42ffcb/PUBLIC_ACCEPTANCE.md "Next-250 cohort index 99; SHA-256 c040382cd3b5d7be31e243f837edbaf335d5f265c4e4e5e8ee38bd5d6c42ffcb"
[N250C-113]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/f6d0b984c520cb95073765bae052c13990cc9bd85fda622f2cc750cfd58dc82c/REVIEW.md "Next-250 cohort index 113; SHA-256 f6d0b984c520cb95073765bae052c13990cc9bd85fda622f2cc750cfd58dc82c"
[N250C-114]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/e2fe376205e5690cd7928f19650e8ff02d96b661385a2f4100d38e10505a2c0d/README.md "Next-250 cohort index 114; SHA-256 e2fe376205e5690cd7928f19650e8ff02d96b661385a2f4100d38e10505a2c0d"
[N250C-115]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/7962950f50dcaedd6df77814cd65376783e7473e05e305472b98e5037d1c076e/A1_SOURCE_REVIEW.md "Next-250 cohort index 115; SHA-256 7962950f50dcaedd6df77814cd65376783e7473e05e305472b98e5037d1c076e"
[N250C-116]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/7faba8ad9cb427ecaf7ee478ad7fb70836896f22ae5bd34e15853181197e040a/A2_SOURCE_REVIEW.md "Next-250 cohort index 116; SHA-256 7faba8ad9cb427ecaf7ee478ad7fb70836896f22ae5bd34e15853181197e040a"
[N250C-117]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/dc7966ef933a7327571d50034f9db6c948fbe11cdf3edd321da900913294b271/A3_SOURCE_REVIEW.md "Next-250 cohort index 117; SHA-256 dc7966ef933a7327571d50034f9db6c948fbe11cdf3edd321da900913294b271"
[N250C-118]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/70f00b8ea97851e72057b89da66b6e1dea7f30c774ea75e5dabc4ebc3c89de0b/check_original_replay_guards.py "Next-250 cohort index 118; SHA-256 70f00b8ea97851e72057b89da66b6e1dea7f30c774ea75e5dabc4ebc3c89de0b"
[N250C-119]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/1ef7df66227a399d74d48aea827605846cd753f12c45cf3493c85b0c2a89b787/finite_controls.py "Next-250 cohort index 119; SHA-256 1ef7df66227a399d74d48aea827605846cd753f12c45cf3493c85b0c2a89b787"
[N250C-120]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/314fb0521f809e3c5ca471363341546f9bcb88737109f861dff14b78414f0dc1/A2_replay.py "Next-250 cohort index 120; SHA-256 314fb0521f809e3c5ca471363341546f9bcb88737109f861dff14b78414f0dc1"
[N250C-121]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/a02ac9ee8c6108bd247c64c8a5fdfd66741dfdc24370600b90fe1ae15c2c6946/replay.py "Next-250 cohort index 121; SHA-256 a02ac9ee8c6108bd247c64c8a5fdfd66741dfdc24370600b90fe1ae15c2c6946"
[N250C-122]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/6867f7a07652ed5f5f7982007ebe478e69e6b5502b4f7c41343be180a76ebc01/test_artifact.py "Next-250 cohort index 122; SHA-256 6867f7a07652ed5f5f7982007ebe478e69e6b5502b4f7c41343be180a76ebc01"
[N250C-123]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/4876c53cfb35f3b4df7f4a34c1d932107cede8b1d3a9682598d91d3dee36b74a/test_replay_guards.py "Next-250 cohort index 123; SHA-256 4876c53cfb35f3b4df7f4a34c1d932107cede8b1d3a9682598d91d3dee36b74a"
[N250C-124]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/667c870e8b04f8486008ee43bb4cf6a6486d88160941c667443c2d702f0a2fe4/verify_artifact.py "Next-250 cohort index 124; SHA-256 667c870e8b04f8486008ee43bb4cf6a6486d88160941c667443c2d702f0a2fe4"
[N250C-125]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/bcd09b50664b6041e13399040878262b6f1e34c54fce46564f91e3a6dfc5adb2/README.md "Next-250 cohort index 125; SHA-256 bcd09b50664b6041e13399040878262b6f1e34c54fce46564f91e3a6dfc5adb2"
[N250C-126]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/ad8dd5d7ad058a5931c19d6b84da0164b29be577eefe541fa2c004b453387b88/ORDERED_COMMAND_TRANSPORT_ACCEPTANCE.md "Next-250 cohort index 126; SHA-256 ad8dd5d7ad058a5931c19d6b84da0164b29be577eefe541fa2c004b453387b88"



[N250-146]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e203c1b497da4db352d8d26fb17d835d7c89104ca8b5382da7c2c70ade9053e4/REPRODUCIBILITY.md
[N250-159]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/10d15cd1df71ca909c3598e98d090df25cdcd745861d8bbc9cea9ea9d513be13/validate.sh
[N250-160]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a67f3ae196aa45d895f881b02787ec04db4a97c344b73a7aa7e126a0d6ded5c7/validate.sh
[N250-161]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/221a50045570edb56a62012eff862df258f9af0ae51d74d116ff224e5c5498e7/ARTICLE.md
[N250-162]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b824c43b4f4fad672bb96e930241787b8d07d36a69d49f20ea9d85d2d51b43d2/EXACT_EFFECT_ALGEBRA.md
[N250-163]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a282ebf891d26ca2e55fc93bdb73fa3159f60a6388545b930076c17fd73c7571/ORACLE_AND_FORCE_PRECISIONS.md
[N250-164]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/66e0a9c2856b28ea2c701dba5c88350b4de6c513ff0922232863b17e2744f69d/PRIOR_ART_DISPOSITION.md
[N250-165]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6e3c5aee5d3c339d8a58a4087ea78ded5b75c616dc18ffa697732d44c16ccae6/REALISABILITY_AND_RESOURCE_ACCOUNT.md
[N250-166]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e25a4892f50eabf427b9eafce002744aeed9e5ffecc2b5f8896a8992ed7f28f1/SOURCE_CAPSULE.md
[N250-167]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/08d2b29597f4ee32240d7c54ed0fa70b1aa6d1e35d6d16253fd3fde078ddb04d/README.md
[N250-168]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0f65f172926e61ff7280ec2e13fd36b4ff287ea530ebbfa00c9dce831f3355fa/context_effects.py
[N250-169]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7614ed0a2d9eca6c2e07c74ee0e02c902cff4956b07347ee9b1b47e70edd8ee2/exhaustive_validation.py
[N250-170]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/808a9297d27b903722b4fc04ad9a526d3cfc3e371b14e5047e1d33d1c6e3e79f/read_cover.py
[N250-171]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/090c48a908c2780f5eccce07c7b211e3970f0f24ea1188d3528a5195fafe8130/semantic_mutations.py
[N250-172]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d286e1099431a64390a14c9533d96cdd7aebc673f68ea74953c9c4852e5e24db/source_and_release_validation.py
[N250-173]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/af8ae17bd3881ab703fc773bf91bffad9859a4fa8f9cb3559d39ed43b4696bf8/test_contract.py
[N250-174]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a25c4464f85c4b9a8f920b2e208e35164cf821ef69f352d341b4c86046b434a4/BOUNDED_RELEASE_DECISION.md
[N250-175]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/68d885c2cec1f9551dc9899bac224c17ddb3ebd0f9e2858b7989fea19c12c9dc/PREMISE_AND_ALTERNATIVE_LEDGER.md
[N250-180]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cb9aa16dc764ad0aa193ca464e2335a8474b782084a573ab1ede1420eda228ff/COLLATION_ADDENDUM.md
[N250-182]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/61deeb33635687c7206fe0b70bf0160d4ed42ad72200f42ef7214bcc2ecb839c/INDEPENDENT_REVIEW_v1.md
[N250-183]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ba4f0fa9ed04750b629b5a504c976de589c3899c9c753742dd34cbb0cdcd644c/check_observations.py
[N250-184]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9ef042d82a12e7aadb8219e41741a21297172dcef72bea3102916eef84f960ad/INVERSE_LIMIT_AND_CONVERGENCE_CORRECTION.md
[N250-186]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4c9e8a08260d26b8b1821c190c715518d0b763ee1327d396aefd2bbe903dc87a/INDEPENDENT_NONUNIFORM_ACCEPTANCE.md
[N250-187]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cdff07e133a38347c1a0f5b31787af914c50f3023e6690a42a356ec97ab4e74e/VERIFICATION_NOTE.md
[N250-188]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/94a47f2ed5926fcef2e178544640eb7f713af3d33b49dd55d0a45445c8769320/MINIMAL_ADDENDUM.md
[N250-189]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/efb057ac25c9abdb28da8208830f102f18fe225146325a507231605345515747/REVIEW.md
[N250-196]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1dff5f73b342b3685837468887215898a1754786cf22127497587c99c3622fb5/INDEPENDENT_REVIEW_v1.md
[N250-197]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cf9ac967668e35fc47c89214efbd9f84aa97a820ec255ffff4d48b41b1af1d3a/independent_models.py
[N250-198]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b94b8df9b31c8b635743440afc3525fb6abff282336ef1ba9e2dd9a316f6fee4/run_independent_mutations.py
[N250-199]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e1303f10bbe5da403553c2be7f2b7ff468f0567b501f63d854cfb3f908cabcf2/run_independent_review.py
[N250-205]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/05f00f5678a39cc0e608b3ded1184321a2a42112150b7c1841a9a345ad701fbf/REVIEW_RECEIPT.md
