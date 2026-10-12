# Root-aware likelihood transport and continuation memory

9 October 2026 UTC. Bounded constructive T20 interface test. Scratch-only, with no protected edits, integration, adoption, empirical validation, or programme closure. General mathematical novelty is not claimed.

## Result and prior ownership

The useful increment is narrow: a source-root-aware likelihood store has a simple lawful implementation, but its posterior readout need not implement named-root acquisition, withdrawal, or overlap-aware merge. Under the stated positive finite model, its exact continuation quotient retains the membership of every informative root. This can require 2^k distinguishable states even when all k likelihood vectors are identical. The result concerns operational state for a stipulated evidence calculus, not knowledge or warrant.

The following are already in the pinned repository and are **not new results** here:

- S1, Deep AX V2 §§2–4: joint Bayesian source updating, factorization only under conditional independence, and exact copies preserving rather than multiplying the one-root likelihood factor.
- S2, Deep AR V2 §§4–6: provenance-adjusted log evidence over authenticated conditionally independent acquisition roots, alias contraction, and distinct-root conflation as the opposite error. S2 expressly separates machine provenance from warrant and authority.
- S3, Deep AU V2: scoped linear root-span rank, same output versus distinct lineage, and no identification of rank with probabilistic independence or general nonlinear operational capacity.
- S4, typed-core candidates: root-labelled idempotent evidence contexts and a calibration-root transport example. Its own status qualification marks the Core B claims DERIVED_BUT_UNVERIFIED. This report does not upgrade them.
- S5, the MOAT Orthemic crosswalk: idempotent intersection of sound model constraints, with an ordinary union-bound coverage result, not Bayesian likelihood multiplication.
- S6–S7, the CP04/CP12 basing analyses: endpoint/pathway distinctions and the prohibition on inferring rational basing from arbitrary gateable bits or numerical labels.

All S1–S7 were read at Orthemology commit 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c. Exact paths, URLs and Git blob identities are in SOURCE_BINDINGS.json. The daee MEMETIC-ECOLOGY and TAWATUR-WARRANT examples and the T08 history/cancellation guide were also inspected from the concurrent source packets; they motivate the same separations but are not premises of the proof.

The sibling reset/withdrawal investigation supplies the general essential-coordinate continuation theorem. The proof below is its finite-likelihood specialization, with the additional observation that this particular readout already has the same quotient under either all named activations alone or all named deactivations alone. No new general automata theorem is claimed. The narrow source check did not locate this exact likelihood-store continuation statement; it is not an exhaustive priority search.

## 1. Declared model and semantic boundary

Fix a nonempty finite hypothesis set Θ, a strictly positive prior p on Θ, and k authenticated, immutable root records. Each root i has a fixed strictly positive likelihood vector L_i: Θ → (0,∞). Distinct roots may have identical likelihood vectors; root identity is not vector identity. Copies of the same acquisition retain the same root identifier.

For E ⊆ {1,…,k}, define

    W(E) = [∏_{i∈E} L_i],
    q_E(θ) = p(θ)∏_{i∈E}L_i(θ) / Σ_φ p(φ)∏_{i∈E}L_i(φ).

Square brackets quotient positive vectors by a common positive scalar. Define the root operations

    A_i(E) = E ∪ {i},       D_i(E) = E \ {i},       M(E,F) = E ∪ F.

This is a **retractable accepted-evidence store**. D_i changes which fixed evidence factors the stipulated calculation accepts. It does not by itself mean that an observation became false, that a subject forgot evidence, that a source lost authority, that access was lost, that a belief lost warrant, or that rational Bayesian agents should decondition historical facts. Permissions, validity, factual evidence, memories, and operative grounds require separate semantics. A surviving independent ground can continue supporting the same content.

The formulas have a genuine conditional probabilistic realization: choose c_i > 0 small enough that 0 < c_i L_i(θ) < 1 for every θ; independently conditional on θ, let Y_i be Bernoulli with P(Y_i=1|θ)=c_i L_i(θ). For each fixed E, conditioning on Y_i=1 for i∈E gives q_E. The root observations need not be identically distributed. This establishes consistency of the stipulated model, not its truth of actual sources.

The selection of E must be fixed, exogenous, or have an explicitly justified ignorable selection mechanism for this formula to be the complete posterior given the available observations. An informative selection/withdrawal history can itself be evidence. Likewise, conditioning a subject's complete history on fewer events is not automatically a justified revision of that subject's posterior. Without conditional independence, use the joint likelihood or valid sequential conditionals, not the product of marginal root factors. A changed root observation or model/version needs a declared update contract, not silent reuse of an old identifier.

## 2. Idempotent merge does not transport to likelihood multiplication

Let G be the abelian group of strictly positive Θ-vectors modulo common scale, with pointwise multiplication. Its identity is the class of constant positive vectors.

**Proposition 1.** Every semigroup homomorphism from the union semilattice of root sets into G is trivial.

**Proof.** For every E, E∪E=E. Thus f(E)=f(E∪E)=f(E)f(E). Cancellation in G gives f(E)=1. No preservation-of-unit assumption is needed. ∎

Consequently W cannot be a union-to-multiplication homomorphism if any L_i is nonconstant. In particular, for a full-support prior, an ordinary likelihood update U_L(q)=N(qL) is idempotent only when L is constant: U_L(U_L(q))=U_L(q) implies [L]^2=[L], hence [L]=1. This is an elementary algebraic restatement of the already-owned duplicate-evidence warning, not a new Bayesian discovery.

Strict positivity matters. Hard constraints represented by nonnegative indicator vectors are idempotent under multiplication on their surviving support, and all-zero products may make normalization undefined. They do not form the positive group used above. This is one reason S5's model-set intersection should not be identified with positive probabilistic updating.

**Correct overlap law.** In the declared model,

    W(E∪F) = W(E) W(F) / W(E∩F),
    q_{E∪F} = N(q_E q_F / q_{E∩F}).

The second equality follows by cancelling one copy of the common prior and one copy of each common evidence factor. If E and F are disjoint, q_{E∪F}=N(q_E q_F / p). Multiplying posteriors directly double-counts the prior even before considering shared roots. The overlap term must be supplied or reconstructible; posterior equality does not identify overlap.

## 3. Constructive implementation

Retain the immutable root catalogue, the active set E, and optionally cache q_E or log odds. An activation checks root membership; if i is absent, multiply by L_i and mark i active, otherwise leave the state unchanged. A deactivation checks membership; if i is active, divide by L_i and remove i, otherwise leave the state unchanged. Merge takes union of compatible root identities and recomputes, or applies only the incoming roots absent locally.

These operations realize A_i, D_i and M exactly. Repeated activation and repeated deactivation are idempotent. Arbitrary finite operation words preserve the displayed posterior invariant by induction. Fixed-root division is safe algebraically because each L_i is positive; this grants no epistemic permission to perform the retraction. Concurrent add/remove conflict resolution, root discovery, identity authentication, and distributed tombstones are outside this sequential fixed-store model.

This positive construction is not a universal no-go for posterior-only state: if q_E uniquely determines all informative root memberships, a posterior can encode them and support their recovery. The exact criterion follows next.

## 4. Exact continuation quotient

Let I = {i : L_i is nonconstant on Θ}. Define E ≈ F when the posterior outputs agree after every common finite word of the admitted named-root operations, including the empty word. The comparison covers the full store domain 2^{1,…,k}. Reachability restrictions can change a minimal-state claim; all states are reachable from the empty store under activation or from the full store under deactivation.

**Theorem 2.** With all named activations and deactivations, E≈F if and only if E∩I=F∩I. The same statement holds with all named deactivations alone, and separately with all named activations alone. Hence the exact quotient has 2^{|I|} classes.

**Proof, sufficiency.** Factors for roots outside I are common scalars and do not affect a posterior. Equal informative memberships remain equal under each common named activation/deactivation. Induction gives equal outputs after every word.

**Proof, deactivation necessity.** Suppose i∈(E△F)∩I. Apply D_j for every j≠i. The resulting stores differ only between {i} and ∅. Their posteriors are N(pL_i) and p. Equality, using p(θ)>0 for every θ, would force L_i to be constant. This contradicts i∈I.

**Proof, activation necessity.** For the same differing i, apply A_j for every j≠i. The resulting informative stores are I and I\{i}. If their posteriors were equal, cancelling their common strictly positive prior and factors would again force L_i constant. Thus they are distinguished. Either restricted alphabet already proves necessity for the larger alphabet. ∎

This is a behavioral information lower bound, not a claim about literal bit-array layout or RAM cost. Any exact deterministic representation for these observations and actions must distinguish the 2^{|I|} classes; it can encode them in any form. In particular, the posterior readout itself is continuation-sufficient exactly when q_E=q_F implies E∩I=F∩I. Log-likelihood span dimension alone cannot decide that injectivity.

For a general target readout h on Boolean stores, the sibling essential-coordinate theorem with independently named set/clear operations gives the coarsest state h needs. It can forget coordinates semantically irrelevant to h. Here each nonconstant L_i affects the posterior in every context, so its essential-coordinate set is exactly I. This specialization must not be transported to a thresholded decision or to actual warrant without rechecking its target and operation semantics.

## 5. Exact same-posterior counterexample

Take Θ={0,1}, p=(1/2,1/2), and two distinct conditionally independent acquisition roots a,b with L_a=L_b=(2,1). A genuine observation model is P(Y_i=1|0)=2/3 and P(Y_i=1|1)=1/3.

    q_∅ = (1/2,1/2)
    q_{a} = q_{b} = (2/3,1/3)
    q_{a,b} = (4/5,1/5).

The common command D_a sends {a} to ∅ and leaves {b} unchanged. The same current posterior therefore requires two different next posteriors. The common command A_a leaves {a} unchanged and sends {b} to {a,b}, giving another contradiction for a posterior-only transition.

For merge, the input posterior pair is (2/3,1/3) twice both for ({a},{a}) and for ({a},{b}); the correct merged posteriors are respectively (2/3,1/3) and (4/5,1/5). Thus no merge function of those posterior values alone works over all these stores. A provenance-aware store handles all three cases directly.

For k distinct roots with the same L=(2,1), q_E depends only on |E|, so there are k+1 current posterior values but 2^k continuation classes. The aggregate log-likelihood vectors span one direction. This concerns **log-likelihood-vector span**, not Deep AU's distinct root-signature space: identifying those two ranks would repeat precisely the type error AU excludes. Conversely, distinct weights along one direction can give all 2^k subset sums different, making the posterior injective despite rank one. Low dimension alone is not a memory lower bound; named operations and actual collisions do the work.

## 6. Ancestry and scope of credit

The algebraic ingredients are classical idempotent-semigroup/group cancellation, normalized Bayes multiplication, and common-information correction in probabilistic data fusion. The continuation argument belongs to ordinary observational equivalence and finite-state/Moore-machine minimization. The general reset theorem is owned by the concurrent reset/withdrawal investigation; Deep AR/AX already own the source-specific likelihood nonduplication and conditional-independence interface.

This packet supplies a useful cross-programme contract and exact counterexample, not field novelty or a new warrant theory. It gives no actual root authentication, calibrated source model, authority licence, knowledge-loss criterion, mental basing discriminator, or automatic bridge from geometric learning to proper function. Its positive payoff is modest and executable: keep precisely the informative root-membership information needed for the admitted operations, preserve the shared-root correction, and refuse to treat authority revocation as evidence deconditioning.

## 7. Verification record

`python3 verify_models.py` passed with exact rational arithmetic. It checked 5,460 overlap-merge pairs, 21 complete finite-state partition refinements (0–6 informative roots plus one constant root, across three action alphabets), the two-root collisions for activation/withdrawal/merge, a rank-one injective control, and the nonpositive hard-constraint exception. Partition refinement was computed directly from the posterior outputs and action transitions, independently of the claimed essential-coordinate formula. These finite controls corroborate the written proofs and do not replace them. No Lean run or external human review is claimed.

All seven downloaded source files were rehashed as Git blobs and exactly matched their pinned connector blob identities. The manifest separately binds the local artifact bytes. The result has author self-checking and sibling coordination, not an independent review receipt.
