# A bounded information consequence for coordination explanations

4 October 2026 UTC. Separate ordinary-mathematics result. This answers only whether the Gaussian-history obstruction constrains a proposed finite-capacity coordination record. It is not a general information programme, an implementation, a finitely additive entropy theory, or a claim about actual physical resources.

## Verdict and useful increment

The information inequality is valid and supplies a quantitative requirement stronger than merely naming dependence. Positive capture in a fixed bounded interval forces state–future-sum mutual information to grow at least logarithmically with the horizon. Consequently, a record of uniformly bounded entropy cannot mediate all of that dependence. For an at-most-N-valued complete record there is a sharper exact capture bound, with a matching one-horizon construction.

These are standard information and concentration methods applied to this particular history question. H-MOAT already owns the substantive requirement that a purported information cut include every relevant route, common preparation, and prior resource. No source-existence conclusion, physical capacity bound, or general causal principle follows here.

## 1. Countably additive setting and conventions

For each positive integer n let P_n be an ordinary countably additive Borel law of real variables (Y_n,S_n), with S_n distributed as N(0,n). Suppose X_0=Y_n+S_n and the terminal law of X_0 is the same at every horizon under consideration. Let Q_n be the usual countably additive product of P_n's two marginals.

For a bounded interval I of positive length L put

p=P(X_0∈I),
q_n=Q_n({(y,s):y+s∈I}).

The independent Gaussian concentration bound gives

q_n ≤ a_n(L):=2Φ(L/(2sqrt(n)))−1 ≤ L/sqrt(2πn).

For L>0, Q_n gives the sum event probability strictly between zero and one: every real translate of I has positive Gaussian probability and a complement of positive Gaussian probability, and the outer marginal is an ordinary probability. Singleton intervals are treated separately below.

All logarithms in this note are natural. Information and entropy are in nats; division by log 2 converts them to bits. Define

I(Y_n;S_n)=D(P_n || Q_n)∈[0,+∞].

If P_n is not absolutely continuous with respect to Q_n, relative entropy is +∞. Otherwise use the usual integral of f log f against Q_n, where f=dP_n/dQ_n and 0 log 0=0. The negative part is integrable, so this is a defined extended nonnegative number, not an infinity-minus-infinity expression. No joint Lebesgue density or finite differential entropy is assumed.

## 2. Binary-event lower bound and its proof

Let E_I={(y,s):y+s∈I}. Binary data processing gives

I(Y_n;S_n) ≥ d(p || q_n)
= p log(p/q_n)+(1−p)log((1−p)/(1−q_n)).

For completeness, if P_n is absolutely continuous, apply convexity of f log f separately on E_I and its complement under Q_n, producing the two displayed terms. If absolute continuity fails, the left side is +∞ and the inequality remains valid. Boundary probabilities use the usual conventions: positive mass compared with zero mass yields +∞; a term with zero numerator mass is zero.

Writing h(p)=−p log p−(1−p)log(1−p), with h(0)=h(1)=0, gives

d(p || q_n)
= p log(1/q_n)+(1−p)log(1/(1−q_n))−h(p)
≥ p log(1/q_n)−h(p).

Hence

I(Y_n;S_n) ≥ (p/2)log n − p log(L/sqrt(2π)) − h(p).       (1)

The sharper form keeps a_n(L) in place of L/sqrt(2πn). The coarse form is valid even when its right side is negative; nonnegativity of information supplies the additional lower bound zero.

For fixed p>0 and fixed L this grows as at least (p/2)log n−O(1). If a singleton terminal event has positive probability, its independent benchmark probability is zero, so I(Y_n;S_n)=+∞ at each such horizon. The main finite-width formula does not divide by L=0.

Because an ordinary countably additive probability on R is tight, a fixed terminal Borel law always admits bounded intervals of probability arbitrarily close to one. Choose an interval after ε and before n, apply (1), and then let ε decrease. This yields

liminf_(n→∞) I(Y_n;S_n)/log n ≥ 1/2.                    (2)

No uniform additive constant or convergence rate follows from tightness alone. A particular warranted capture interval provides the explicit finite-horizon constant in (1).

If B_n is the entire future innovation block and S_n is its measurable sum, ordinary data processing also gives I(Y_n;B_n)≥I(Y_n;S_n). Thus (1) is a lower bound on information about the whole block as well. No finite-additive entropy or data-processing claim is being made.

## 3. The coefficient is attained by a consistent Gaussian anchor

Let X_0=A∼N(0,τ²), where 0<τ²<∞, independently of a two-sided ordinary iid N(0,1) noise sequence. Define every position by finite forward/backward sums from A. Then S_n has variance n, Y_n=A−S_n, and the whole recurrence is consistent across horizons.

The joint pair (Y_n,S_n) is nonsingular Gaussian, with

Var(Y_n)=τ²+n,  Var(S_n)=n,  Cov(Y_n,S_n)=−n,
Var(Y_n | S_n)=τ².

The Gaussian entropy calculation therefore gives

I(Y_n;S_n)=1/2 log((τ²+n)/τ²)=1/2 log(1+n/τ²).

This has asymptotic coefficient 1/2 in (2). At τ=0 the pair is supported on the line y=−s while its product marginal law gives that line probability zero, so information is +∞ instead; substituting τ=0 in a finite formula is not allowed.

The example is a globally anchored, state–future-dependent recurrence, not a fresh forward innovation law. The anchor A alone does not mediate that dependence: conditional on A, Y_n=A−S_n remains dependent on S_n. A finite description of this formula is not a finite information record through which the dependence passes.

## 4. What a finite-capacity explanation must actually assert

Suppose a discrete record R_n is proposed to mediate all the state–future dependence at horizon n. The exact requirement is

Y_n is conditionally independent of S_n given R_n.

For standard Borel variables the ordinary conditional distributions and information identities are available. The chain rule and conditional independence imply

I(Y_n;S_n) ≤ I(R_n;S_n) ≤ H(R_n).

If H(R_n)≤C for all n, equation (1) contradicts arbitrarily remote horizons as soon as a fixed bounded capture has p>0. At a particular horizon, a necessary condition is

C ≥ p log(sqrt(2πn)/L)−h(p).

Equivalently, for that fixed capture contract,

n ≤ (L²/(2π)) exp(2(C+h(p))/p).                         (3)

This is a necessary model constraint, not a sufficient construction. It applies also to countably infinite records whose Shannon entropy is bounded by C. More generally, a certified bound I(R_n;S_n)≤C suffices even when the record is not discrete; differential entropy is not used as a capacity bound.

For a record with at most N possible values, H(R_n)≤log N. The elementary entropy consequence is therefore a required growth of the record alphabet; Section 5 provides the sharper exact finite-alphabet constraint.

If there is side information U_n, the relevant complete-mediation condition is Y_n independent of S_n conditional on (R_n,U_n). Then

I(Y_n;S_n) ≤ I(U_n;S_n)+H(R_n|U_n).

A bound on the record alone is insufficient when the side information carries uncontrolled state–future dependence. If U_n is independent of S_n, its first term is zero; that independence must be warranted rather than presumed.

The inequality H(Y_n)≤log N applies directly only when the actual state variable Y_n itself has at most N values. A quantized readout of a real state does not automatically qualify: lower information about Y_n does not pass backward through a lossy readout. Likewise, finite program length, a finite law-description, a fixed number of controller states, finite differential entropy, and a complete finite-alphabet coordination record are different assertions. A controller can accumulate a long transcript or use an external correlated resource while its instantaneous internal state stays finite. Those paths must be included before (3) is applied.

## 5. Exact finite-alphabet capture capacity

Fix one horizon n, one interval I of length L≥0, and an integer N≥1. Among ordinary joint laws satisfying S∼N(0,n) and admitting a mediator M with at most N values such that Y and S are conditionally independent given M,

P(Y+S∈I) ≤ a_n(NL)=2Φ(NL/(2sqrt(n)))−1.                (4)

For L>0 this bound is attained when optimizing over the state marginal and encoder at that one horizon. It does not assert attainability while preserving any independently prescribed state marginal, terminal law, or one common history at every horizon.

### Upper bound

Discard labels of M of probability zero. For each remaining label m let ν_m be the conditional law of Y, and define the finite noise submeasure

λ_m(B)=P(M=m,S∈B).

Then Σ_m λ_m=γ_n and every λ_m is dominated by γ_n. In particular λ_m has no atoms. Conditional independence gives

P(Y+S∈I)=Σ_m ∫ λ_m(I−y) dν_m(y)
≤ Σ_m sup_y λ_m(I−y).

For any ε>0 choose, for each of the finitely many labels, a translated interval J_m=I−y_m within ε/N of its supremum. Then

Σ_m λ_m(J_m) ≤ Σ_m λ_m(∪_j J_j)
= γ_n(∪_j J_j).

The union has Lebesgue measure at most NL. Among Borel sets of a fixed finite Lebesgue measure, the centered interval maximizes centered Gaussian mass. An elementary proof compares the set with the centered interval: density outside the interval is at most its boundary density, and density on any missing interior portion is at least that value. The outside portion has no more length than the missing portion. Hence γ_n(∪J_m)≤a_n(NL).

Let ε decrease to zero to obtain (4). No supremum-attaining translation was assumed. Open, closed, and half-open endpoint conventions do not affect the value, since every λ_m is nonatomic. If L=0, every translated singleton is λ_m-null and the conclusion is zero; the empty interval is immediate.

### Matching fixed-horizon construction

For L>0 partition a centered interval of length NL into N consecutive cells J_1,…,J_N of length L. Draw S from the ordinary Gaussian law. When S lies in J_m, let M=m. Assign every exterior value of S to label 1. Choose a constant y_m translating J_m onto I, and set Y=y_M.

Because Y is constant conditional on M, conditional independence of Y and S given M is automatic. The capture event is precisely the centered length-NL interval up to endpoint null sets: exterior points assigned label 1 do not create additional capture. Thus its probability is a_n(NL). This also works for N=1. At L=0, zero capture is trivially attainable.

This is a retrospective encoder and matching state assignment. It does not furnish a forward-causal realisation, a sampler for a finitely additive law, or a physical coordinator.

### Reading the bound

For 0<p<1 and L>0, capture probability at least p requires

N ≥ (2sqrt(n)/L) Φ^−1((1+p)/2),

with rounding up to an integer when necessary. Probability-one bounded capture is impossible with any finite N and finite L because a_n(NL)<1. A fixed positive capture therefore requires alphabet size of order at least sqrt(n), not merely the weaker n^(p/2) lower bound obtained from (1) and log N.

The useful additional burden is exact: a finite set of complete coordination modes cannot supply arbitrary remote-horizon capture under these assumptions. Merely calling a proposed global explanation finite-state does not establish that its modes form the complete mediator used in this theorem.

## 6. Inherited ownership and scope decision

Read directly before attributing new credit:

- The retained H-MOAT E3 source, “Cross-substrate communication and airgap-ese,” defines information budgets relative to specified interventions, observations, precision, and prior information. Its noninterference proposition separates a shared model from a fresh information channel.
- The retained H-MOAT E3 source, “Information cuts, fresh state, and physical budgets,” already requires a complete conditional Markov cut, applies conditional data processing and finite-message entropy bounds, and warns that omitted common sources or prior resources defeat a nominal cut. This is retained historical work, not new Twelfth credit.
- P02 attempt-0002, U05 Measure Core M2-01/M2-02/M2-05/M2-06, supplies the probability-domain, countable-event, total-variation, and existence-versus-effective-acquisition guards already used in the Gaussian review. The inspected P02 proof prose did not provide an exact Gaussian coordination information-growth owner.
- Sixth's action-sufficient disclosure supplement already proves a contract-specific finite message-alphabet bound, distinguishes useful action disclosure from full world diagnosis, and counts timing, silence, and side channels as part of the operative message. No general message-capacity principle is new here.

The checked H-MOAT text is the selected historical source at `tranche9/final-evidence-work/projections/H_MOAT_E3_Selected_Historical_Source_v1/the_last_moat_e3.tex`, sections labelled `sec:channels` and `sec:cuts`. The selected historical component identity is recorded by `tranche9/final-evidence-work/work/HMOAT_COMPONENT.json`. No frozen file was changed and no historical acceptance status was reopened.

**Decision:** retain this as one bounded analytic consequence because it answers the stated coordination question: a complete finite-entropy or finite-alphabet record is quantitatively insufficient under the same Gaussian capture contract. The techniques and complete-cut condition are inherited standard material. This is a specific application, not a new general information theorem. Do not extend it to finitely additive information, infer an actual physical capacity bound, identify a necessary or original source, or claim that short descriptions of globally coordinated laws are excluded.
