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
