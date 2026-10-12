# A sharp error budget for finite coordination modes

## Scope and inherited source

This is a v6 ordinary-mathematics corollary, not a new formalisation or physical memory theorem. The source is the fully read T12 BOUNDED_COORDINATION_INFORMATION_v1.md, SHA256 c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7, especially lines 110–154. It proves the exact fixed-horizon capacity below by finite noise submeasures and Gaussian rearrangement. The only additional step is transport through event total variation, with a matching error-budget construction.

Fix n>0, finite L≥0 and an interval I of length L. On a common measurable space let E={Y+S∈I}. Let Q be a countably additive probability law with S∼N(0,n), admitting a complete mediator M with at most N≥1 values such that Y and S are conditionally independent given M. Write

    a = 2 Φ(NL/(2√n)) − 1.

Let P be any probability law on the same event algebra (finite additivity is enough for this transport step), and suppose the event-total-variation convention is

    sup_A |P(A)−Q(A)| ≤ η,       0≤η≤1.

Then

    P(E) ≤ min(1, a+η).

It is enough to assume the one-event error |P(E)−Q(E)|≤η. The total-variation hypothesis is a sufficient uniform contract, not a necessary premise for this single event.

**Proof.** The source's exact finite-mediator theorem gives Q(E)≤a. Consequently P(E)≤Q(E)+η≤a+η, and P(E)≤1. No conditional probability or entropy under P is used. The Gaussian marginal and conditional-independence hypotheses belong to Q and cannot be discarded because the numerical bound resembles a generic finite-message bound. ∎

## Consequences

If P(E)≥p and 0<p−η<1 with L>0, every such approximating N-mode reference must satisfy

    N ≥ ceil[(2√n/L) Φ⁻¹((1+p−η)/2)].

For p≤η the bound gives no positive alphabet-size information. For L=0 it says p≤η. If p−η=1, no finite N and finite L can meet the contract. In particular, with a fixed positive gap p−η and fixed L, the necessary alphabet size grows at least proportionally to √n. For a fixed N, any approximation of a capture-p law has event-TV at least max(0,p−a). This quantifies the error a finite sidecar must tolerate under this exact complete-mediation contract.

## Sharpness at one horizon, even with the same Gaussian noise marginal

Assume L>0. Take the source's extremising countably additive Q: partition the centred interval J of length NL into N adjacent length-L cells J_m, set M=m on J_m and M=1 outside J, and choose constants y_m so that I−y_m=J_m. Put Y=y_M. Then Q(E)=γ_n(J)=a<1.

For any δ=min(η,1−a), choose a Borel subset C of R\J with Gaussian mass δ; nonatomicity supplies it. Keep the same Gaussian S. On C replace the state value by Y'=c−S for a fixed c∈I; elsewhere keep Y'=Y. Let P be the resulting pair law of (Y',S). Then P(E)=a+δ. The coupling changes its pair only on C, so its event-TV from Q is at most δ. Conversely the capture event changes probability by δ, proving event-TV exactly δ. Hence the upper bound min(1,a+η) is attained. In this construction P generally does not possess Q's finite complete mediator; that is exactly the information carried by the allowed approximation error.

This is retrospective fixed-horizon law construction. It does not preserve a separately prescribed Y marginal, a terminal law, one coherent history across all horizons, a forward-causal implementation, or physical resource constraints. For L=0, a parallel change Y'=c−S on a Gaussian set of mass η makes singleton capture η, while any finite-mediator Q has zero capture; the transport inequality remains sharp for a nonempty singleton target.

## Use with the later continuation results

A finite alphabet is a complete mediator only if it includes every operative route and prior resource relevant to Y and S. A finite program description, finite plant or finite currently visible state is insufficient. The controller source's history-conditioned seed posterior and the renewal source's retained service/authorization conditions are examples of information that must be kept when establishing a proposed mediation or approximation contract. This corollary does not assert that those distinct models automatically satisfy the Gaussian contract. It provides a test only after that bridge is independently warranted.
