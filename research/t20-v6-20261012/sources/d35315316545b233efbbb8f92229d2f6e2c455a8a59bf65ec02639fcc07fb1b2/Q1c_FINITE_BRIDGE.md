# Q1c — general finite-probability bridge and T300 constructions

Ordinary proofs below cover arbitrary finite dimension, not just the three-bit candidate. All constructions are new scoped research; the original seven three-bit candidates, source statements, Q0 scope and historical non-recovery boundary remain unchanged. No absent numerical payload is claimed to have been recovered.

## Q2-01. Minimal finite law interface and genuine measure bridge

Let X be finite and nonempty. A finite rational probability law is a function `w:X→ℚ` with w_x≥0 and `Σ_x w_x=1`. For an event A⊂X define `P_w(A)=Σ_(x∈A)w_x`. Nonnegativity, normalization and finite disjoint additivity follow from finite sum partitioning.

On a finite discrete measurable space, define the actual probability measure `μ_w=Σ_x (w_x:ℝ≥0∞) • δ_x`, where the coefficient is the nonnegative real embedding (not a cast of a negative rational). Dirac evaluation and the finite sum definition give `μ_w(A)=P_w(A)` after conversion to reals. Countable additivity also follows directly: a disjoint sequence of subsets of finite X can contain any point at most once, so summing pointwise indicators and interchanging a finite sum proves the measure axiom. Thus this is an actual finite-distribution-to-measure bridge, not merely a list of weights or a logical Full predicate. By M2-01 it has d=0; none of the parity claims requires that defect fact.

For a deterministic f:X→Y with finite Y, set `(f_*w)_y=Σ_(x:f(x)=y)w_x`. Fibres partition X, so weights remain nonnegative and sum to one, and `P_(f_*w)(B)=P_w(f⁻¹B)`. For a stochastic kernel K(x,y) with nonnegative rational entries and each row sum 1, set `(wK)_y=Σ_x w_x K(x,y)`. Nonnegative finite interchange proves normalization and event evaluation. Deterministic maps are the special rows `K(x,y)=1[f(x)=y]`.

For `0≤α≤1` rational, `(1-α)w+αv` is another law and every event probability is the corresponding affine combination. The same statements hold for nonnegative real weights; rationality is needed only for exact executable arithmetic, not the probability identities. Composition of deterministic maps and kernels agrees with ordinary finite fibre/matrix composition by finite-sum interchange.

## Q2-02. Parity normalization in arbitrary dimension

For integer n≥1 let `X_n={0,1}^n`. Define `π(x)=Σ_(i<n)x_i mod 2`, and `E_b={x:π(x)=b}` for b∈{0,1}. Flipping any fixed coordinate is an involutive bijection E_0↔E_1. These disjoint classes partition the 2^n words, so each has 2^(n-1) words. Define

`P_b(x)=2^-(n-1)` if π(x)=b, and 0 otherwise.

This is an exact dyadic rational finite law. The positivity and normalization proofs follow from the cardinality, not from a finite table. At n=0 there is only the empty word with even parity; an odd uniform parity law does not exist. The n≥1 hypothesis is therefore substantive.

An equivalent constructive presentation selects all but one pivot coordinate uniformly and independently, then sets the pivot to the unique bit giving parity b. There are exactly 2^(n-1) free assignments and each parity word has one preimage, proving equivalence with P_b. This supplies the reusable finite law constructor and a direct normalization witness.

## Q2-03. Every proper-subset marginal and deterministic transport

Take J⊊{0,…,n-1}, with k=|J|, and a pattern u on J. Choose a pivot j outside J. Once u and the bits at all other omitted coordinates are assigned, there is a unique pivot bit giving parity b. Hence exactly 2^(n-k-1) words of E_b restrict to u. Dividing by 2^(n-1),

`P_b[x↾J=u]=2^-k`.

This includes J empty (probability 1) and fails for J the whole coordinate set. It proves equality of **all proper-subset marginals** of P_0 and P_1. For n≥3 every singleton and every two-coordinate set is proper, so their complete pairwise profiles agree.

Let `flip_j(x)` toggle coordinate j. It is a bijection, is its own inverse and satisfies π(flip_jx)=1-π(x). All nonzero point weights are equal, so `(flip_j)_*P_1=P_0`. For the explicit target `Q(P):=P(E_0)=1`, Q(P_1) is false and Q(P_0) true. Thus this declared deterministic intervention restores Q while preserving the entire proper-subset marginal profile. It is not only a comparison of unrelated laws, and it is not an assertion about an unspecified real-world intervention.

At n=2 the pair is the full coordinate set and detects parity. At every n, observing all n coordinates distinguishes P_0 from P_1. These are exact hypothesis-boundary countermodels, preserved rather than hidden by the n=3 fixture.

## Q2-04. General finite mixture and observables changed/preserved

Let n≥3 and α be rational with 0<α≤1. Put `P^(α)=(1-α)P_0+αδ_(0^n)`. Both components have even parity, so `P^(α)(E_0)=1`; Q is already true before and after. For every proper J of size k and pattern u,

`P^(α)[x↾J=u]=(1-α)2^-k+α·1[u=0^J]`.

For k=0 both laws give 1. For any nonempty proper J, the all-zero pattern gains mass α(1-2^-k)>0 and every other pattern loses α2^-k>0. Thus all these nonempty marginals change, while parity remains exactly even. This identifies which observables change, not merely that “something changes”.

At α=1/2 every pair has the predecessor's exact profile `(5/8,1/8,1/8,1/8)` in the order 00,01,10,11, instead of `(1/4,1/4,1/4,1/4)`. This witnesses the public T300 converse existence claim with explicitly new scoped weights. The intervention is the finite stochastic kernel `K_α(x,·)=(1-α)δ_x+αδ_0`: keep the word or overwrite it with zero. For α=0 no marginal changes, so the strict α>0 premise cannot be dropped.

Together Q2-03 and Q2-04 show pairwise-profile movement is neither necessary nor sufficient for a **false-to-true change of this declared target**. They do not prove stochastic independence of arbitrary phenomena named “profile” and “restoration”, and do not turn target preservation into target restoration.

## Q2-05. Equivalent test-function description

For J⊂{0,…,n-1}, let `χ_J(x)=(-1)^(Σ_(j∈J)x_j)`. Under P_b, its expectation is 1 if J is empty, 0 if J is nonempty proper (uniform marginal with cancelling even/odd assignments), and (-1)^b if J is the full set. Under P^(α) with b=0, the corresponding expectations are 1, α, and 1. These follow from Q2-03 and affine mixture evaluation, not from an additional approximation assumption. They make the preserved full-parity observable and changed lower-order observables explicit.

## Exact proof interfaces for consumers

- Finite law requires finite nonempty carrier, nonnegative weights and a normalization proof.
- Pushforward requires the declared total function; stochastic transport requires normalized nonnegative rows.
- Proper marginal theorem requires n≥1 and J genuinely proper.
- Pairwise blindness and both T300 constructions require n≥3.
- Mixture movement requires α>0, with α≤1 for nonnegative weights; real α is mathematically allowed, rational α supports exact arithmetic.
- The target Q, flip coordinate and overwrite kernel are explicit and may not be replaced by an unnamed metric/causal operation.
- General parity proofs use counting and finite probability alone. U05 is needed only for an optional actual-measure/defect interpretation, not as an artificial prerequisite to the pure finite theorem.

## Formal scope

The supplied Lean sources separate finite-law/measure definitions, algebraic transport and parity completion from the exact all-n target contracts. Every proof-candidate versus unproved contract is enumerated in the formal coverage file. The seven unchanged predecessor three-bit theorems remain unexecuted unless the exact-pin external runner succeeds. Their existence is not presented as evidence that the general counting theorem has compiled.
