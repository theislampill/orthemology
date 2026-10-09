# Graph-constrained continuation: an exact transfer from parity synthesis

9 October 2026. Bounded T20 mathematical research. No integration or final T20 closure.

## Result first

The inherited continuation theory can be made exact for an interaction graph, rather than merely for an all-to-all menu of pairwise updates. Its sufficient-information space is indexed by **Steiner accessibility**, not by tensor order alone.

For a nonempty set of slots S, the first horizon at which its parity can become a unary terminal observable is

\[
 d_G(S)=2\tau_G(S)-|S|-1,
\]

where τ_G(S) is the smallest number of vertices in a connected subgraph containing S. It is infinite when S crosses connected components. This gate-cost formula is already known in CNOT parity synthesis. The contribution here is its exact transport into the inherited continuation and information-preservation contract, with a general kernel-checked optimality proof and a kernel-checked observable pullback.

Three consequences matter:

1. **The sufficient moment family need not be downward-closed.** On a four-slot path, the four-way parity is accessible after three gates, but the endpoint pair is inaccessible until five. “Keep everything through order k” is therefore not the exact finite-horizon compression criterion.
2. **The global tree boundary is sharp.** For a tree with n≥2 vertices and L leaves, every parity becomes accessible by horizon 2n−L−1, and the leaf parity first appears at exactly that horizon.
3. **Disconnected dynamics preserve a genuine compression opportunity.** All component marginal laws suffice indefinitely for individually evaluated unary expectations after fixed, silent gate words. Joint readout on the same realization or observation-driven feedback is outside this contract and can reveal cross-component dependence. No independence assumption on the initial law is needed.

Constants, horizon semantics, and proof status are essential. The raw span of unary continuation observables excludes the constant. We explicitly augment it by 1. Finite-horizon sufficiency does not mean that the same summary is closed under arbitrary further updates. The dimension and tree results below are written, independently reviewed mathematics; they are not claimed as Lean theorems.

## 1. Inherited work and the genuinely unperformed operation

The graded representation manuscript distinguishes tensor degree from information content, gives the exact fibre criterion, and leaves future stochastic preservation to an additional declaration. The later manuscript *Continuation-Complete Orthing*, at repository commit 3a0bdeaa1394c656245cae9599adcb143e885059, already resolves much more:

- Theorem 1: the full-simplex moment defect, including nonlinear decoders.
- Theorem 2: action–observation continuation spans and minimum continuous exact summary dimension.
- Theorem 3: the complete-graph pairwise-update horizon law, with Walsh degree at most h+1.
- The later augmentation and approximation results.

These are reused, not rediscovered. The local range 108–292 and the actual pinned source range 293–700 were read. The latter contains the already-completed all-to-all calculation; a partial reading would have mistakenly credited it as new work.

The selected extension supplies an explicit graph of permitted interactions and computes the resulting continuation space. It does not add a sampling problem, a theological interpretation, or a new definition-only factorisation theorem.

## 2. Exact model and cross-domain map

Let G=(V,E) be a finite simple undirected graph with named vertices. Its vertices are retained slot/occurrence identities, not interchangeable labels. Put X={−1,+1}^V. For every edge {i,j}, both ordered updates are available:

\[
 F_{ij}(x)_i=x_i x_j,\qquad F_{ij}(x)_k=x_k\quad(k\ne i).
\]

Each update is deterministic, reversible, and touches two slots. There is no informative intermediate observation. The terminal contract is the family of **individual unary expectations** E[x_i]. A horizon counts at most h sequential elementary updates. It does not count parallel layers, and it does not request the simultaneous joint law of all terminal coordinates.

For S⊆V, write χ_S(x)=∏_{i∈S}x_i, with χ_∅=1. Direct multiplication yields

\[
 \chi_S\circ F_{ij}=
 \begin{cases}
 \chi_{S\triangle\{j\}},&i\in S,\\
 \chi_S,&i\notin S.
 \end{cases}
\]

`GraphContinuation.character_gate` proves this identity over a commutative monoid with the required coordinate square equal to one. Thus the mask rule is derived from the observable operation, rather than supplied as an assumed semantic correspondence.

Set x_i=(−1)^{b_i}. Then F_ij is exactly the binary CNOT operation b_i←b_i XOR b_j: its control is j and its target is i. χ_S is (−1) raised to the binary parity of S. Every gate corresponds bijectively, preserves adjacency, and costs one in both declarations. Products of pullbacks reverse chronological state-update order; reversing the sequence preserves the gate menu and length. The terminal output bit is (1−x_i)/2, so parity expectations and terminal bit probabilities determine each other.

This is a classical reversible-circuit correspondence. It assumes no quantum phase, superposition, entanglement, measurement collapse, physical gate reliability, or actual access to an occurrence. Other output coordinates may change. Requiring their restoration, a fixed output slot, one-way gates, or auxiliary clean bits changes the contract.

### Prior art, stated narrowly

Vandaele, Martiel, and Goubault de Brugière, *Phase polynomials synthesis algorithms for NISQ architectures and beyond*, [arXiv:2104.00934, §4.1, p.10](https://arxiv.org/pdf/2104.00934#page=10), already derive the identical cost by filling Steiner vertices and eliminating along a tree. Sections 2 and 4.1 were inspected for the gate and cost correspondence; the displayed formula was visually checked. Their practical method uses an approximate Steiner tree. Here τ denotes an actual optimum. No claim is made that their heuristic computes it, that their entire synthesis algorithm was replayed, or that this cost formula is a new theorem. The continuation application below is separately derived.

## 3. Exact graph cost

For S≠∅, define τ_G(S) as the minimum |U| over connected induced vertex sets U⊇S. Connected subgraphs and connected induced supersets have the same minimum vertex count. Define d_G(S) as the fewest updates needed to make some unary terminal character pull back to χ_S.

### Lower bound

Follow a mask execution A_0={r},…,A_m=S, and let U be the union of all masks visited. Every first appearance attaches one new vertex to a currently active neighbor, so G[U] is connected.

If r∈S, every vertex in S\{r} must be toggled at least once and every transient vertex in U\S at least twice. If r∉S, r must be removed once, each final vertex must be introduced once, and every other transient vertex must be toggled at least twice. In either case,

\[
 m\ge2|U|-|S|-1\ge2\tau_G(S)-|S|-1.
\]

No-ops and repeated revisits cannot improve this bound. Lean proves the stronger invariant 2|U|≤m+|S|+1 for every execution, together with connectedness of the visited set.

### Upper bound

Take a minimum connected U⊇S and a spanning tree rooted at any r∈S. Activate every vertex in parent-before-child order, using |U|−1 gates. Then remove each vertex of U\S in deepest-first order, using its still-active parent. This uses |U|−|S| more gates and ends at S. The two bounds coincide.

The Lean upper proof uses an equivalent induction on connected-set generation. Together with the lower bound it proves `exact_steiner_cost`: for any minimum connected witness of size t, an optimal run exists with m+|S|+1=2t. Its minimality comparison quantifies over every run, not only an enumerated gate bound. The ambient slot type need not even be finite when a finite minimum witness is supplied.

When S spans components, no connected witness exists and no run reaches it. Conversely every nonempty subset of one component is reachable. The empty mask is excluded: invertible gates cannot turn a nonzero character into the constant.

## 4. Continuation space and exact information dimension

Let

\[
 \mathcal R_h(G)=\{\varnothing\ne S\subseteq V:d_G(S)\le h\}.
\]

The raw unary continuation span and its explicitly augmented counterpart are

\[
 W_h=\operatorname{span}\{\chi_S:S\in\mathcal R_h(G)\},\qquad
 C_h=\operatorname{span}(\{1\}\cup W_h).
\]

The mask theorem and exact pullback imply that these are precisely the spaces in the inherited continuation construction for the present silent-update model. Walsh orthogonality gives

\[
 \dim W_h=|\mathcal R_h(G)|,\quad
 \dim C_h=1+|\mathcal R_h(G)|.
\]

Over the **full probability simplex** on X, the inherited continuous-encoder theorem therefore gives

\[
 d_{\min}(G,h)=|\mathcal R_h(G)|.
\]

The retained moments attain this dimension. The lower bound permits arbitrary nonlinear decoders but requires a continuous encoder. It counts exact real coordinates, not memory bits or samples. A known restricted family of laws may require less.

For an independent view of the lower bound, let q=|R_h| and consider positive laws p_a(x)=2^{−|V|}(1+Σ_{S∈R_h}a_Sχ_S(x)) for Σ|a_S|<1. Their required moments are exactly the q independent coordinates a_S. Any continuous sufficient encoder is injective on this open q-dimensional family, so invariance of domain excludes fewer than q real coordinates. This is the inherited topological argument specialized to the exact graph span.

Only C_∞ is necessarily invariant. Before saturation, F* C_(h−1)⊆C_h supports a remaining-horizon hierarchy, while F* C_h⊆C_h can fail. A summary certified for three future updates cannot silently be reused for an unlimited sequence.

### A sharp non-downward-closed example

On the path 1–2–3–4, d({1,2,3,4})=3 but d({1,4})=5. Thus C_3 contains the full four-factor character while excluding an ordinary pair character. Its augmented dimensions at h=0,…,5 are 5,8,10,13,15,16.

This is an information-preservation distinction, not merely a gate-count curiosity. Define

\[
 \lambda_\pm(x)=2^{-4}(1\pm\chi_{\{1,4\}}(x)).
\]

Both are nonnegative normalized laws. They agree on **every** C_3 moment by Walsh orthogonality, including the four-way moment. Yet after the five-gate endpoint circuit, the terminal negative-sign event has probability zero under λ_+ and one under λ_−. Every decoder of the three-horizon summary has worst-case error at least 1/2 for that later event; the constant estimate 1/2 attains the bound. This uses the inherited defect principle with a newly identified missing graph-constrained direction.

Actual chronological circuits were checked on all 16 states: F_34,F_23,F_12 exposes the four-way parity at slot 1; F_12,F_23,F_34,F_23,F_12 exposes the endpoint pair. No restoration of other slots is claimed.

## 5. Global completion boundaries

### Trees

Let T have n≥2 vertices and L leaves. For nonempty S let H be its unique minimal connecting subtree, with m vertices. Then

\[
 d_T(S)=2m-|S|-1.
\]

Every original leaf of T that belongs to H must belong to S; otherwise it could be removed from the minimal hull. Hence L≤|S|+(n−m), giving

\[
 d_T(S)\le n+m-L-1\le2n-L-1.
\]

If S is all leaves, its hull is the whole tree and equality holds. Therefore the least horizon at which the whole joint law is needed for universal exact continuation is

\[
 \boxed{h_{\mathrm{sat}}(T)=2n-L-1.}
\]

The terminal readout coordinate is freely chosen from the declared unary family for each question. A fixed output-coordinate requirement is a different theorem. For n=1 the saturation horizon is zero and is handled separately. Paths give 2n−3; the inherited complete graph gives n−1. This theorem measures the exact point at which all 2^n−1 nonconstant law coordinates enter this continuation contract. It is not a physical time or sampling guarantee.

### Disconnected graphs

For connected components B,

\[
 \dim C_\infty=1+\sum_B(2^{|B|}-1),\qquad
 d_{\min}(G,\infty)=\sum_B(2^{|B|}-1).
\]

The saturated observable functions are sums of functions depending on one component at a time. Two laws have identical required predictions exactly when their component marginal laws agree. Initial cross-component dependence can be arbitrary; this contract never asks for it. For two disjoint edges the augmented rank is seven and six continuous coordinates suffice, rather than fifteen for the full four-slot joint law.

This conclusion can fail if a simultaneous joint terminal observation, recorded multi-component observation history, or observation-driven adaptive control is added. Such a change inserts products of component observables into the required space. Graph disconnection alone is not a universal independence or unobservability claim.

## 6. Verification and residuals

`GraphContinuation.lean` kernel-checks:

- active masks lie in their visited set;
- the visited set has finite connected growth;
- the universal visit-count lower bound;
- constructive upper synthesis from a connected witness;
- the exact minimum formula and reachability equivalence;
- the actual character/gate pullback identity.

Fresh replay uses Lean 4.19.0 with trust level zero and warnings as errors. Principal axiom readbacks are propext, Classical.choice, and Quot.sound. There are no admitted proofs or new axioms. Cached mathlib dependencies are used and are not rebuilt; this is not a clean-room proof of Lean or mathlib.

The author’s independent checker works on full state truth tables rather than mask pseudocode: all 75 labelled graphs through four vertices and 1,023 nonempty graph–mask pairs agree with separately computed connected-superset minima. It also checks the exact circuits, 248 gate/character identities, normalized separating laws, and disconnected rank. A separate reviewer’s mask-BFS implementation checked all 33,867 graphs through six vertices, 2,097,151 pairs, and all 1,441 labelled trees through six vertices. These are distinct implementations and scopes; finite checks do not replace the proofs.

The real-span rank, continuous-encoder lower bound, tree saturation, and disconnected-law characterization are written and independently reviewed; their full formalization is not claimed. The Lean connected-set presentation is `Grown`, not a theorem stated using mathlib’s `SimpleGraph.Connected`; their elementary equivalence is explained above. General proof trust and finite implementation testing remain separate.

Remaining application obligations are explicit: justify the actual slot extraction, graph, gate availability and semantics, allowed output contract, law class, horizon and reacquisition rules. No empirical implementation, multi-parity joint circuit optimum, approximate nonlinear compression theorem, directed/weighted/noisy analogue, or global Orthemology completeness follows. No connection to metaphysical source uniqueness is proposed. This bounded branch stops with the exact transfer, sharp counterexample, and global completion boundary.
