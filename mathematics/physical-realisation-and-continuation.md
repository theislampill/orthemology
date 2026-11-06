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

These distinctions have a practical use when comparing physical systems. A claim should retain its target and version, regime, procedure, provenance, uncertainty and validity conditions. A crosswalk should preserve inputs, outputs, units, resources and timing. Missing evidence stays missing through translation. Abstraction of a model, combination of evidence and physical composition of mechanisms are three different operations.

### 9.3 Lossless abstraction is target-relative

Let φ map concrete cases X to a representation Z, and let q map X to a target set T. There exists a decoder d on the attained image φ(X) satisfying q = d∘φ if and only if q is constant on every fibre of φ.

**Proof.** If q = d∘φ, equal representations have equal q values. Conversely, if q is constant on fibres, define d(φ(x)) = q(x); the condition makes this well-defined. The definition is unique on the attained image. ∎

Extending d to all of Z requires values on unattained points. A nonempty T permits an arbitrary default there; when X and T are empty but Z is nonempty, such a total extension is impossible. This edge case prevents a valid attained-image result from being silently strengthened to an unrestricted decoder claim.

The theorem is already developed in [Collective Inquiry and Strategic Coordination](collective-inquiry-and-strategic-coordination.md), section 2.1. Here it has two concrete uses. A representation that merges the delay kernel's two different future states loses a relevant distinction. A representation that discards physical coordinates while retaining the parity class can be sufficient for parity continuation. “Lossless” is consequently always relative to the target q and admitted domain.

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

#### Shared authority and future competence are not copied into existence

An authentic grant permitting one of two successor roles to perform one exclusive operation can make each role's solo continuation possible without permitting both uses simultaneously. Copying the grant or translating its wording does not reset its allocation, expiry or use count. A genuinely shareable grant can permit both; branching itself is not the defect.

The same distinction limits source-history transport. If two individually lawful whole-history maps send the same source-command occurrence to different commands, no single-valued map on that shared occurrence has both outputs. Combining their conclusions requires specified duplication, origin and shared-store semantics. Unchanged commitments and cancellation tombstones cannot automatically be applied to transformed keys. Unioning records may change progress; dropping records may change safety. Two comparison isomorphisms do not themselves perform a legal fork–merge. Finite-history reification from authentic complete policy samples can reconstruct the specified source history, but epoch lookup is not source authentication and reconstruction does not prove that the physical history occurred.

Current state and output may also survive while future calibration does not. A successor that loses a source-bound alignment needed for a later task can remain adequate if it retains an actually available, authorised reacquisition interface. If the migration destroys the source or sole credential, a promise to reread it later supplies no capability. The task family, budget and future support must be declared; one successful handoff does not establish unrestricted recursive continuation.

A causal successor and an independently produced lookalike can share state, outputs, copied proofs and a stated lineage identifier. A snapshot alone does not identify which physical transfer occurred or convey the predecessor's grant. The lookalike may obtain its own warrant or rights; this observation settles neither numerical identity nor ultimate source. Similarly, a faithful translated quotation can preserve the original assertion and ambiguity while performing only a report in its current context. It is not thereby a fresh directive or an independent testimony. Source force and present speech act must be retained separately.

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

The compiled-composition checkpoint then reports a known-root model with $n=4$ and fault budget $B=1$ that consumes the actual imported transition both at proposal and at live-root admission. Its returned successor determines the modeled plant change. Actor-observed time, root landing time, rule and draft versions, and operation-specific permissions remain separate. A fixed expected-version command changes the full record at most once; a later duplicate rejects without undoing the achieved goal. This is a statement about that exact modeled interface, not a proof that an arbitrary physical controller realizes it. [GUIDE105-G068]

The dynamic-history guide reports finite multi-epoch safety, durable cancellation exclusion and stable whole-table goal preservation for its corrected dynamic interface. It does not prove complete liveness, a covering or randomized search theorem, physical realization or automatic transfer to another root/table interface. This agrees with §10.3: a safety invariant can hold while useful progress fails. The unknown-root attribution extension additionally fixes prepared path/quorum families, a specified alias class and opaque macro-attempt observations. Its obstruction does not exclude arbitrary adaptive provenance discovery or redesign of the family. The general root-image criterion, actual-root availability, arbitrary fixed-family feasibility, root-name/fault transport, original-definition correspondence and root-cost corollaries retain their interface premises even where more of their algebra was later mechanized. [GUIDE105-G020] [GUIDE105-G082] [GUIDE105-G026]

The historical review stages must remain distinct. A preserved first-version receipt does not qualify a corrected second-version root. The earlier dynamic review required repairs to releasing stalled attempts, the adequate remaining horizon and the fixed scope of its restoration claim; the later candidate recorded those repairs while its own review was still pending. Conversely, an old pending-review sentence can remain an accurate historical feature of an unchanged author artifact when a later exact-byte sidecar supplies its disposition. The operational-model acceptance guide explicitly describes a later distribution whose scientific bytes were unchanged but whose state/event wording and manifest were corrected; its full replay concerns that identified distribution. Trusted compiler and dependency caches were not independently bootstrapped by that replay. No new scientific theorem, whole-batch refinement or physical-clock warrant follows from the distribution correction. [GUIDE105-G073] [GUIDE105-G020] [GUIDE105-G043]

Two older semantic controls remain expressly inconclusive: the old-program/new-decoder mutation reached only its declared resource failure, and the cost check diagnosed an insufficient scalar premise without rejecting the full mutant module. A later baseline reconstruction did not convert either outcome into a successful rejection. The restart guide likewise awards no rejection credit to those resource-limited controls. These are retained limits on historical evidence, not refutations of an unrelated accepted theorem and not new executions in this chapter. [GUIDE105-G068] [GUIDE105-G003]


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

#### A local gate supports a current-policy conclusion

The abstract safety argument obtains a good selected root from the path/quorum and fault bounds. Its overlap inequality ensures that an old command's path intersects the old epoch's retained revocation certificate at a good root. That root cannot permit the command, excluding stale landings. For a command that does land, local admission fixes its epoch to the good root's descriptor; the invariant excludes a future descriptor, and the stale-command argument excludes an older epoch. Authenticity then identifies the **full** descriptor with the current authority-stream policy. Admission at the actual plant and annotated time follows without supplying that global policy to the live gate. Equal epochs identify full descriptors only under the stated authenticity and consistency hypotheses. [R250-043]

Cancellation uses a related but distinct argument. More than the fault budget of distinct acknowledgments yields a good acknowledging root, and consistency places it on the command's path with a durable tombstone. A landing would contradict its local gate. Each abstract step preserves good-root revocation and cancellation memories, acknowledgment sets grow, and epochs do not decrease. Induction therefore carries the cancellation obstruction through any finite trace from a reachable consistent state. The typed challenge closes a prepared but unlanded command while its expected version, permissions and other landing conditions still hold. This isolates the cancellation guard from replay rejection. Its exclusion theorem even permits later events with decreasing time annotations: it is a memory theorem, not a physical-clock theorem. [R250-043] [R250-133]

The typed command keeps the original ordered path inside its complete identity and separately proves that the path has no duplicates and every index is in range. Only then does its finite-set view have the same cardinality as the original list. Duplicate `[1,1,2]` and out-of-range `[1,2,4]` paths cannot inhabit the four-root command subtype. Root representation forgets repetition and ordering of *memory lists* because the gates use membership; it does not identify distinct complete commands. [R250-190] [R250-133]

At represented snapshots, a successful compiled attempt entails the abstract landing predicate with the same actual plant, time and single faulty-gate Boolean. The converse is established when that Boolean opens faulty gates; withholding can add rejection, so no unrestricted equivalence is asserted. At a reachable safe represented state, a successful attempt has the exact declared full successor. The snapshot relation alone does not establish macro-operation trace refinement or constrain every omitted world coordinate. [R250-190]

The typed history results expose the effect rather than merely a success flag. An installation sets the rule to exact, increments the rule version and appends the old rule. A repair copies source content into the draft, increments the draft revision and appends the previous draft. Other primitive events leave the plant unchanged. Along an initially consistent safe finite history, rule version and rule-history length increase by the number of installation landings; draft revision and draft-history length increase by the number of repair landings. Source, destination, standard and unrelated custody remain fixed. Goals, once achieved in the stated reachable safe setting, persist. [R250-190] [R250-120]

These nondecreasing counters give a stronger replay boundary than immediate duplicate rejection. Once a particular expected-version action has succeeded, it cannot succeed again after any lawful finite continuation from its reachable successor, at any later policy or annotated time. A hypothetical second success would require the old expected version or revision to equal a counter already increased by the first success and never decreased. Fresh valid actions can still change their respective counters and histories. This is not literal full-state idempotence. [R250-120] [R250-190]

#### What the four-path log and lifecycle actually record

The batch-source module names the literal fold body of the imported `runBatch` and gives definitional equality, rather than introducing a replacement service. Each scheduled path appends one record with nonce equal to the actor's input nonce plus the previous record count plus one. Consequently its four records have exactly the four fixed paths and successive nonces. When proposal fails, the body leaves the world unchanged and appends a **synthetic** closed record with false preparation and landing flags. When proposal succeeds, it calls preparation, conditionally attempts, and calls cancellation on the full path. [R250-099]

For the correctly named owner, four roots, quorum three and budget one, every log record is closed. On a proposed well-formed three-label path, full-path cancellation obtains a true current-call reply; the proposal-none branch instead uses the synthetic record just described. An induction preserves the closure statement through the literal fold. This distinction prevents a closed log flag from being mistaken for evidence that every scheduled proposal executed a cancellation call. [R250-039]

Frame lemmas establish that preparation and cancellation preserve root policies and revoked epochs, while attempts preserve the whole roots function. The complete batch therefore preserves those root fields as well as root count, quorum, budget, runtime clock, effective policy and taint classification. Commitments and cancellation memory are deliberately not included in this frame. A false response may have changed them, as §10.7 explains. [R250-080]

A zero-fault control sharpens that warning: four preliminary cancellations, each receiving only one selected owner's reply, all return false. Their four distinct-envelope tombstones nevertheless block preparation and landing on all four scheduled trials, leaving the plant unchanged. The source supplies a genuine cancellation trace and an aligned reachable abstract history for this fixture; the obstruction is not merely an arbitrary edited store. Thus absence of a successful cancellation reply does not establish trial availability. [R250-072]

Completed-certificate delivery is also bound to the actual operation. Given alignment, reachability and membership of the certificate in the world's completed list, the compiled delivery refines a finite sequence of primitive deliveries to good roots. It updates a root's policy only when the certificate is newer, preserves its revoked epochs, commitments and cancelled commands, and preserves the plant, effective policy and completed-certificate alignment. Delayed or repeated older certificates are included; the aligned post-boundary stream admits no pre-base certificate. The proof's enumeration of good recipients is not information supplied to the actor. [R250-160]

The retained batch test function exercises installation followed by separately granted repair for each of the five listed fault patterns: no fault or one of four faulty roots. It specifies exact full successors, four closed records, one version/history-changing landing per batch and retained source/custody. It explicitly advances the actor's observed plant and nonce before the next phase rather than inferring that `runBatch` returns a refreshed actor. These are the source's executable assertions, not fresh test results. [R250-068]

#### Transporting command order is not merely reordering service

An admitted involutive command symmetry transports commitment and cancellation sets by its command image, the receipt function by the corresponding key substitution, and command-bearing events and corruption payloads consistently. Descriptors, revoked epochs and the plant remain unchanged. The source proves involution, membership and receipt correspondence, preservation of permission and landing, and commutation with preparation, cancellation, landing, requests, completion, acknowledgment and delivery. The concrete attempt bridge preserves valid-path checks, each gate and the attempt result with the **same** faulty-gate Boolean, including withholding. One cannot obtain these conclusions by changing a path while keeping its command-keyed memories fixed. [R250-070] [R250-018]

There is a smaller service-order freedom for one unchanged complete command. Preparing two addressed stores commutes even when the labels alias the same store: equal addresses apply the same transformation twice, and unequal addresses use commuting independent updates. The preparation eligibility test is unchanged by another preparation. Cancellation slots likewise commute, including the represented acknowledgment set. Therefore permutations of a fixed preparation or cancellation service list have the same represented set-valued final state. Raw native list insertion order need not be identical, and the complete command itself has not been reordered. [R250-052]

#### A public finite portfolio and its native interpreter

The public portfolio of all size-$q$ subsets of $m$ labels has $\binom{m}{q}$ entries. The environment's fault bound and repair-availability inequality guarantee at least $q$ good labels, hence an all-good member of that portfolio. Combining this existence fact with §10.7's clearance, authentic proposal and initial-plant admission premises gives conditional completion after servicing the entire public schedule, with $\binom{m}{q}(2q+2)$ abstract events. The concrete seven-label, five-label portfolio has 21 paths and 252 events. These counts belong to the shared-store reference program; they do not change the four-path implementation. The portfolio theorem is noncomputable and does not grant the actor a hidden-root query. [R250-030]

The separate native program supplies explicit ordered paths. It computes commands from the actor's observed plant, policy, observed time and action, assigning successive nonces. It accepts no actual-world state, routing map or service response as a command-selection input. Service annotations supply time, prepare bits, one gate Boolean and cancellation bits. Their number must equal the command count, and each bit array must have exactly $m$ entries. Missing, excess or malformed annotations reject. Successful annotation erases back to the exact command list and the exact supplied annotations, preserves pairwise command distinctness, and exists for matching lengths with valid arrays. Two successful decorations therefore expose identical complete commands, without implying that their visible replies or outcomes are identical. [R250-156]

The native interpreter services labels in the order actually stored in each command. A trial emits its preparation events, one attempt event, cancellation events and a terminal close event or the corresponding admitted primitive hold. Under `RoutingMatches`, its represented final state equals the shared reference run and its *actual emitted* events form a valid trace; these are separate conclusions. Slot-level correspondence and the service-permutation results above support induction over each service list, then over the trials. Each trial has exactly $2|P|+2$ events and a uniform $N$-trial run has $N(2q+2)$. Valid paths and authentic requester imply actual closure. Conditional native progress still requires common successors, distinct complete commands, initial clearance, admission at each annotated time from the initial plant, and an all-good scheduled path. Representation has not removed these premises. Independent contract wrappers retain the routing-match premise, actual emitted trace and exact annotation-erasure signatures. [R250-166] [R250-144]

The native execution-data source fixes 21 service annotations, a first-twenty prefix, repeated and expired runs, two routing fixtures and a malformed annotation. Its checks require 259 events for the full fixture and 247 for the first-twenty projection, which explicitly prepends seven holds to its twenty-trial trace. Those fixture totals must not be substituted for the 252 trial events of the 21-path reference schedule. They require no effect during that prefix, a single installation on the full run, retained state changes in the failed prefix, no reinstallation on replay and no effect under expired service. They also check rejection of wrong annotation lengths, malformed arrays and nonadmitting proposals, plus withholding and good-alias cases. These are precisely stated fixture expectations in the retained source, not general worst-case completeness and not observations from a run performed for this chapter. [R250-097] [R250-031]

This supplement incorporates the operational argument and its boundaries, while the exact cited formal modules retain every declaration, proof term, fixture, import and executable check. Prose is not their executable successor. No imported dependency body was inspected for this supplement, and no Lean compilation, native evaluation, axiom readback, CI, physical experiment or new assurance acceptance is asserted. Source preservation, consumer migration and any later active-path retirement remain separate obligations.

### 10.10 Exact primitive contracts and remaining runtime boundaries

The arguments in §§10.7 and 10.9 rely on a particular transition language and on separately stated applicability conditions. The following details complete its scientific contract rather than enlarging its assurance or physical scope.

#### The primitive kernel's premises and effects

For $n$ labels, fault budget $B$, landing quorum $q$ and revocation quorum $r$, the configuration requires at most $B$ faulty labels, $B<n$, strict overlap $n+B<q+r$, and both availability inequalities $q+B\leq n$ and $r+B\leq n$. Its policy source assigns epoch $e$ a descriptor whose epoch is exactly $e$. The local interface requires admission to expose the already checked command epoch and requester; neither desired safety nor a goal is an interface law. A root carries its descriptor, revoked epochs, commitments and cancelled complete commands. The global proof-side state additionally records epoch, pending status, current acknowledgments, past certificates, per-command cancellation acknowledgments, plant and damage flag. Initialization sets epoch zero and source-zero descriptors, with empty memories/certificates, no pending transition and no damage. A root permits a command only when it is committed, locally admitted, unrevoked at its epoch and uncancelled. Landing requires exactly $q$ selected labels and permission at every good selected root. [R250-124]

The legal events have distinct guards and effects. A request requires no pending transition and opens one with empty acknowledgments. Acknowledgment requires a pending transition, adds a label, and records the current epoch as revoked at a good root. Completion requires a pending transition and exactly $r$ acknowledgments; it stores that certificate, advances the epoch, clears pending state and resets the acknowledgment set to empty. Delivery requires $0<e\leq$ the current epoch and replaces a descriptor only when newer. Preparation requires a selected label and valid $q$-path; a good root must pass live admission, unrevoked-epoch and uncancelled-command checks, while a faulty label may supply its own response. It adds a commitment. Cancellation acknowledgment requires a selected label and either a faulty label or the intended requester; it adds the acknowledgment and, at a good root, the exact tombstone. A close event requires more than $B$ distinct cancellation acknowledgments and changes no state. Landing requires the local landing predicate; hold is identity, and arbitrary root replacement is allowed only at a faulty label. [R250-124]

The landing update classifies damage after admission: existing damage is absorbing; a failure of current-source admission marks damage instead of changing the plant; otherwise it applies the declared effect. This classifier is not read by the local landing gate. Consistency records full descriptor authenticity, no future good-root descriptor, exact-size past certificates with good signers' retained revocations, revocation at every good label in the current acknowledgment set, without a separate pending-state hypothesis, selected cancellation acknowledgers and durable good-root tombstones. It does not assume that damage is false. A finite trace is a chain of these guarded steps; reachability means such a chain from some initialized plant. These definitions specify the hypotheses used in §10.9's safety argument, not a universal model of any interlock. [R250-124]

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
