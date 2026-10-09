# A meaningful isolated kernel target

This is an exact specification for optional Lean 4.19 work, not a claim that a Lean file has compiled. Installing the official toolchain and ordinary dependencies is authorised. The local absence of a toolchain is a cost consideration, not a permission blocker.

## Main mathematical statement

Let E be a finite type with decidable equality. A histogram H consists of five functions a,b,c,d,e from finite subsets of E to natural numbers. All five functions vanish at the empty subset. They count the five declared root/guard types, indexed by a nonempty output bundle. No route ID or ordering is part of this histogram.

For one such function f define its hit transform

hit_f(U) = sum over T subset of E, with T intersecting U, of f(T).

Define the exact rational panel:

Q_A(H,U) = (1/2)^(hit_a(U)+hit_d(U)),
Q_B(H,U) = (2/3)^(hit_b(U)+hit_e(U)),
Q_AB(H,U) = (1/2)^hit_a(U) × (2/3)^hit_b(U) × (5/6)^hit_c(U).

**Kernel target:** for all such H and H', if the three rational panels agree for every nonempty U, then each of the five functions agrees at every finite T. This verifies identification up to anonymous histogram, not numerical route identity.

The panel must be defined from those rational products. Assuming an unspecified decoder or left-inverse hypothesis and then concluding injectivity would not verify the load-bearing step.

## Useful proof decomposition

1. Prove the concrete arithmetic code is injective on natural triples:
   (1/2)^a (2/3)^b (5/6)^c = (1/2)^a' (2/3)^b' (5/6)^c'
   implies a=a', b=b', c=c'.
   Prime valuations at 5,3,2 supply the written proof. A kernel proof may use rational valuation lemmas or clear positive denominators and use natural factorisation. The exact available Mathlib lemma names should be checked by the implementer rather than guessed.
2. Prove the corresponding powers of 1/2 and 2/3 are injective on natural exponents. Combined with equal a and b hit counts, this identifies d and e hit counts by natural addition cancellation.
3. Prove the finite hit transform is injective on functions vanishing at the empty set. One route uses a Boolean-lattice inversion theorem. A potentially simpler kernel route proves the partition identity
   sum(T subset of V) f(T) + hit_f(E minus V) = hit_f(E),
   then uses induction on |V| to recover each f(V) from its subset sums. This avoids importing a large general incidence-algebra development while still proving the actual inverse step for arbitrary finite E.
4. Combine the arithmetic identification and transform identification to obtain the main theorem.

## Required boundaries

- Use exact rationals and unbounded finite natural multiplicities.
- Prove the finite-set transform and concrete rational coding; do not add their injectivity as axioms.
- A file should compile without `sorry`, `admit` or extra axioms; report kernel declarations and exact source/toolchain versions.
- This does not formalise a probability space or prove the independent-route response law from physical assumptions. The rational product is the formal model definition. The model-to-stochastic-process factorisation remains a separately stated premise.
- It does not formalise the source's true productive ground, admissible original-agent interventions, finite sampling, general-root design rank, or metaphysical uniqueness.

This target adds assurance because it checks two coupled, load-bearing inversions for arbitrary finite catalogues. A generic statement that an existing left inverse implies injectivity would not provide comparable assurance.

## Higher-priority general guarded criterion

The generated general-root result offers a broader load-bearing target. Let R be a finite root type. Let Pos be its nonempty finite subsets. Let Guard be pairs (P,N) with P in Pos and N disjoint from P. Let I be a finite measurement-coordinate type and let M : I × Pos → integers be any fixed matrix. A hidden histogram is n : Guard → naturals.

Define the integer-valued panel at each nonempty issued S by

Obs_M(n)(i,S) = sum over nonempty P subset of S of
  M(i,P) × sum over N subset of R minus S of n(P,N).

**Target iff:** this panel map is injective on all natural-valued guarded histograms if and only if M has trivial integer kernel on Pos.

For integer M with finite columns, trivial integer kernel is equivalent to full column rank over the rationals: a rational kernel vector can have denominators cleared. That equivalence can be proved separately if kernel-based formulation materially simplifies the library interface.

The forward construction is substantive. Given a nonzero integer kernel vector z, form delta(P,N)=(-1)^|N| z(P); split delta into pointwise positive and negative natural parts. The alternating sum vanishes at every proper issued profile, and the full-profile measurement vanishes by the kernel condition. Equality of the resulting natural histograms would force delta(P,empty)=z(P)=0, a contradiction. No negative counts appear in either hidden model.

The reverse construction uses matrix-kernel triviality to recover, for each S, all enabled aggregate support counts (extend by zero for P not subset of S). A finite guard-zeta inversion then recovers every n(P,N). The proof must establish this inversion and the alternating-sum cancellation, rather than assume either as an oracle.

This is an exact formal theorem about the valuation-channel model. To connect it to rational response probabilities, additionally prove that taking the recorded prime valuations is injective on the subgroup generated by the known positive rational failure factors, and that valuations turn finite products into these integer sums. The particular physical or stochastic origin of the factorisation is still an external premise. A kernel certificate confined to Obs_M should be labelled as that component, not as a full verified probabilistic or metaphysical theorem.

This general iff is the preferred target if its finite-sum, sign-splitting and matrix interfaces fit the available Mathlib version at reasonable cost. The earlier concrete rational-panel theorem remains a useful independently bounded alternative. Neither target justifies inventing a toolchain limitation or installing a toolchain only to certify a generic injective-map tautology.
