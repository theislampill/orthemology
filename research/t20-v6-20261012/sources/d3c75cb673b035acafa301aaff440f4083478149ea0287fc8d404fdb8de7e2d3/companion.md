# Mathematical diagnostics: explicit assumptions, proofs and counterinterpretations

**Evidence status.** This file contains written general arguments and explicitly bounded finite interpretations. The accompanying Python checks use exact integers and `fractions.Fraction`; they are not probabilistic simulations. They do not certify the intended metaphysical interpretation. No new Lean compilation occurred in this session. Optional Lean source is separately labelled uncompiled and is not part of the successful verification claim.

**Intellectual ancestry.** Bayes's theorem, Bernoulli-mixture calculations, graph-component propagation, modal witness distinctions and the elementary order arguments below are standard mathematics. The explanatory-fact statements and Boolean model are inherited from the supplied checkpoints, with an independent implementation and an additional source-padding consequence. The proposed applications and critiques are new analysis within this delivery; no claim of first discovery in the wider literature is made.

## D1. A common requisite of exhaustive alternatives must be necessary

### Statement

Let W be a nonempty set of admissible worlds and P,N,R predicates on W. Assume:

\[
\forall w\in W\;[P(w)\lor N(w)],\qquad
\forall w\;[P(w)\to R(w)],\qquad
\forall w\;[N(w)\to R(w)].
\]

Then `∀w R(w)`.

### Proof

Fix any w. Exhaustivity gives P(w) or N(w). In the first case the second assumption gives R(w); in the second the third gives R(w). Since w was arbitrary, R holds throughout W. No transitivity, symmetry, S5 axiom, probability, efficient-cause interpretation or grounding principle is used.

### Consequences

A world in the same scope where R is absent cannot be added while preserving all three assumptions. This is true even if a description of such a world is syntactically well formed. If R is independently assumed contingent, the conjunction of that assumption and the displayed three premises is inconsistent. The contradiction identifies a compatibility failure; it does not by itself identify which premise should be rejected.

### Application boundary

Harrop's definition makes a requisite a necessary condition. Sections 4–5 use an exhaustive positive/negative pair and a common requisite, then a recombination move deleting that requisite. [M02] The formal observation explains why the deletion is not free. A defence of the full argument would need to derive its world-selection/recombination premises independently and show precisely how they follow under the reductio assumption. This note does not declare every approach in the paper refuted.

**Executable control:** `common_requisite_check`. The tests enumerate all 512 lists of three Boolean worlds and check the implication. They additionally show that the tempting removed-R case makes an assumption false, rather than falsifying the theorem.

## D2. Worldwise negative witnesses cannot be silently made uniform

### Weaker schema

Let `N(i,w)` mean that witness i obtains at w. Consider:

\[
\forall w\;\bigl(P(w)\lor\exists i\,N(i,w)\bigr),
\qquad
\forall i,w\;[N(i,w)\to\neg P(w)].
\]

This is not the stronger schema `∃i ∀w [P(w) ∨ N(i,w)]`.

### Exact three-world control

| World | P | R | N0 | N1 |
|---|---:|---:|---:|---:|
| w0 | 1 | 1 | 0 | 0 |
| w1 | 0 | 1 | 1 | 0 |
| w2 | 0 | 0 | 0 | 1 |

The weak schema holds. Every negative witness implies ¬P. P implies R, and N0 implies R. R is contingent. At w2, removing R also removes P and N0, but N1 remains. There is no contradiction with the existence of some negative witness.

### Sufficient repairs

Either of the following restores the common-requisite conclusion:

1. A uniform selected witness i0 with `∀w(P(w)∨N(i0,w))`, together with `N(i0,w)→R(w)`.
2. Retain world-dependent witnesses but require `∀i,w(N(i,w)→R(w))`.

Each repair is sufficient. Neither is claimed uniquely necessary or weakest among all possible premise sets.

### Application boundary

The later negative-fact-free route in Harrop's section 6 changes to an existentially supplied fact implying nonexistence. [M02] The table tests the local step from absence of a chosen witness to absence of any such witness. It is not a model of every premise, explanatory requirement or truthmaker commitment in that paper.

The same error can arise in the Necessary Being programme when a worldwise original witness is mistaken for one and the same necessary original. Conversely, the table does not show the worldwise witnesses are metaphysically possible beings.

**Executable control:** `rotating_witness_model` and the corresponding tests.

## D3. Cross-membership can force explanatory-fact identity

### Inherited formal setting

Let F be a fact domain with a reflexive antisymmetric relation `Part`. Let `E(x,S)` mean full explanation of a nonempty plurality S, and `PE(x,S)` partial explanation. Assume:

- full explanation supplies partial explanation;
- explaining a plurality permits the relevant singleton/member projection;
- **NEC:** if `PE(x,S)`, `y∈S`, `y≠x`, and `¬Part(y,x)`, then `¬PE(y,{x})`.

These express an explanatory theory; they are not consequences of naming E “explanation.”

### Mutual singleton lemma

If `PE(q,{r})` and `PE(r,{q})`, then q=r.

**Proof.** Suppose q≠r. If r were not part of q, NEC applied to the first partial explanation would exclude the second. Hence Part(r,q). Reversing the roles gives Part(q,r). Antisymmetry yields q=r, contradicting the supposition.

### Cross-membership theorem

If `E(q,S)`, `E(r,T)`, `r∈S` and `q∈T`, the member projections give the two singleton partial explanations, so q=r.

This is a useful weaker sufficient condition than requiring both targets to be the universal fact-domain. But **the target membership conditions cannot be dropped**. A theory about all created effects may exclude the candidate original explainers from its domain, exactly where the proof needs them.

### Inheritance and verification

The theorem and its Lean development are inherited from checkpoint 18. This report supplies an explicit proof explanation and a fresh independent finite-model implementation, not a new claim of kernel verification. Exact inherited source hashes appear in `verification/INHERITED_PROOF_IDENTITIES.json`.

## D4. A total explaining fact is atomic—and source padding is incompatible with it

### Inherited atomhood consequence

The checkpoint-15 proof shows that any part p of a total explaining fact q must equal q, given its partial-source closure, target projection and NEC assumptions. Here is the same proof in expanded language.

1. Since q explains all facts, it explains p.
2. Because p is a part of q, partial-source closure gives p as a partial explainer of p and, in particular, of q through q's total explanation and the appropriate target projection.
3. More directly, total explanation gives `PE(q,{p})`, while source-part closure applied to q's explanation of q gives `PE(p,{q})`.
4. D3's mutual singleton lemma gives p=q.

The precise source-closure formulation matters. The claim is not a theorem of mereology alone.

### Additional no-padding corollary

Assume a unique total explainer q and a full-explanation weakening rule:

\[
E(q,S)\land Part(q,r)\Longrightarrow E(r,S).
\]

For any r containing q, apply weakening to the universal target. Then r is another total explainer; uniqueness forces r=q. Consequently, q has no proper superfact in that domain under these combined assumptions.

If the domain additionally provides a fusion q∨a strictly larger than q, the package is inconsistent. It must reject unrestricted explanatory weakening, the larger-fusion claim, or one of the premises supplying uniqueness.

This corollary concerns **source-side explanatory padding**. It is not the familiar target-side projection from a plural explanation to a member. Confusing these operations would hide the result.

### Exact Boolean interpretation

Facts are the 15 nonempty subsets of four atoms, encoded as integers 1–15. Part is subset inclusion and fusion is set union. Let q={0}, a={1}, b={2}, e={3}. Full explanation holds as follows:

- q explains every nonempty plurality of facts;
- a explains exactly the singleton target {e};
- b explains exactly the singleton target {e};
- no other full explanations hold.

Partial explanation is induced by source parthood: x partially explains S exactly when x is part of some z which fully explains S.

All 32,767 nonempty pluralities are examined. The implementation checks reflexivity, antisymmetry, transitivity of parthood, strong supplementation, all nonempty fusions, overlap/least-upper-bound conditions, unrestricted plural PSR, full and partial transitivity, target distribution, partial-source closure and NEC. The unique total explainer is q, while {e} has three full explainers q,a,b.

The transitivity check quantifies over every target using exact integer bit-set inclusion, not a sample. For each relevant x,S,y, it compares the entire set of targets explained by y with those explained by x (or partially by x). This avoids billions of repeated loops without weakening the condition.

### Deliberate negative control

Add q∨a as an all-target explainer. NEC and total-explainer uniqueness fail. The recorded witness is part of `DIAGNOSTIC_RESULTS.json`. This corroborates the no-padding corollary and makes the excluded operation concrete.

**Limits:** set union in this interpretation is mereological fusion, not a claim that facts are logically conjoined propositions; atom complements are not logical negations; no actual-world metaphysical realisation is established.

## D5. The exact Bayesian likelihood dependency

Let C and U be complementary events, K a target event, and define:

`e=P(C∧K)`, `d=P(U)`, `α=P(K|U)`.

Assume all quantities are well defined, `0≤e≤1-d`, and `e+αd>0`. Then:

\[
P(U\mid K)=\frac{\alpha d}{e+\alpha d}.
\]

**Proof.** Partition K into C∧K and U∧K. The latter has mass αd. Divide that mass by the sum.

For fixed e,d with e>0,d>0, the derivative with respect to α is `de/(e+αd)^2>0`; alternatively cross-multiplication proves monotonicity without calculus. Thus α=1 is the worst-case upper endpoint, not a uniquely warranted value.

The exact contrasting examples are:

| e | d | α | P(U given K) |
|---|---|---|---|
| 1/1000 | 1/100 | 1 | 10/11 |
| 1/1000 | 1/100 | 1/1000 | 1/101 |
| 1/1000 | 1/100 | 0 | 0 |

Koons–Pruss explicitly choose the worst-case treatment; the mathematical criticism is not that their algebra accidentally omitted a term. [M01] The local issue is what justifies the likelihood treatment and how its robustness requirement bears on knowledge. No numerical likelihood for real uncaused observations is established here.

### Interval update theorem

Let p=P(H), l=P(E|H), and `a=P(E|¬H)∈[u,v]`. Provided both endpoint denominators are positive:

\[
P(H\mid E)\in\left[
\frac{pl}{pl+(1-p)v},
\frac{pl}{pl+(1-p)u}\right].
\]

Both bounds are attainable when the endpoints are allowed. The proof is monotonicity in a. The interval is a mathematically informative object even when it is not a point. The epistemic legitimacy of the prior and interval is a distinct assumption.

## D6. Finite exchangeability is insufficient for a Bernoulli-mixture interpretation

### General covariance obstruction

Suppose `(X1,X2)` is a mixture of iid Bernoulli variables, with latent success parameter Θ. Conditional independence gives:

`E[X1X2|Θ]=Θ²`, and `E[Xi|Θ]=Θ`.

Therefore:

\[
\operatorname{Cov}(X_1,X_2)
=\mathbb E[\Theta^2]-\mathbb E[\Theta]^2
=\operatorname{Var}(\Theta)\ge0.
\]

Now take P(01)=P(10)=1/2. This law is exchangeable. It has E[X1]=E[X2]=1/2 and E[X1X2]=0, so covariance is -1/4. It cannot be a mixture of iid Bernoulli laws.

This argument handles all such mixtures, not merely the finite parameter grid checked by Python. It supplies a compact general proof of the finite extendibility obstruction relevant to the de Finetti appeal. The associated literature has long studied finite exchangeability. [M09]

### Coherence is even weaker

The law `(P00,P01,P10,P11)=(1/8,1/8,3/8,3/8)` is a valid probability distribution, but P01≠P10. It is not exchangeable. Probability coherence therefore does not imply the symmetry assumption of the representation theorem.

### Positive control and consistency

For Θ uniformly distributed on [0,1], the probability of **one specified word** of length n with k ones is:

\[
p_{n,k}=\int_0^1\theta^k(1-\theta)^{n-k}d\theta
=\frac{k!(n-k)!}{(n+1)!}.
\]

Integration by parts, or the elementary beta-integral identity, proves the formula. It obeys the consistency recursion `p(n,k)=p(n+1,k)+p(n+1,k+1)`. Multiplying by `binomial(n,k)` gives the head-count probability, a different quantity. The tests check exact values and the recursion through n=8.

The law can have a probabilistic representation without the representation itself identifying an efficient cause. An ontic interpretation of Θ and any causal claim require independent premises. The test does not prove that uncaused events have meaningful chances, nor that they cannot.

## D7. Two source-local complete determinations constrain the compatibility graph

### Statement

Let X and Y be nonempty sets and R a relation on X×Y. Let f:X→Z and g:Y→Z satisfy:

\[
R(x,y)\Longrightarrow f(x)=g(y).
\]

Label X-vertices by f and Y-vertices by g. Along each R-edge the labels agree. By induction on path length, labels agree throughout every connected component of the bipartite graph.

If the graph is connected, all labels have one common value. If Z has m elements and a finite graph has k connected components, there are exactly `m^k` admissible assignments: independently choose one label for each component.

### Proof

For a path of length zero, the start and end vertex coincide. Appending an edge preserves equality by the edge constraint and transitivity. Conversely, a component-constant labelling satisfies every edge constraint. The assignment/component correspondence is bijective, giving the count.

### Explicit cases

For X=Y={0,1}, full Cartesian R is connected and permits only constant common outputs. Three edges already connect the graph. The diagonal relation has two components and permits the shared output to vary with the component. A graph with one edge has three components when both unused declared vertices are retained.

The tests exhaust all sixteen Boolean bipartite graphs and enumerate all binary and ternary vertex assignments. Isolates are deliberately not dropped.

### Philosophical application and limit

The potential interpretation is that each agent's own complete determination fixes the same entire output, and R describes joint admissibility. Then a nonconstant common effect requires disconnected admissibility components, or failure of a complete-determination condition. But original metaphysical independence does not automatically imply full Cartesian recombination or connectedness. Nor does a single actual agreement imply agreement at every permitted pair.

This is the exact bridge the application must defend. The result is closely related to known common-information/support-component mathematics and to Orthemology's earlier identity propagation; it is not a standalone divine uniqueness proof. [M12; inherited context]

## D8. First-order knowledge does not automatically imply reflective knowledge

Let W={0,1,2}, with accessibility edges `(0,0),(0,1),(1,1),(1,2),(2,2)`. Let p be true at 0 and 1. Define Kp at w as p being true at every world accessible from w.

At 0, Kp holds, since 0 and 1 satisfy p. At 1, Kp fails because 2 is accessible and p is false there. Therefore KKp fails at 0. The relation is reflexive but not transitive.

This shows that factivity/reflexivity alone does not establish positive introspection. An S4/S5 epistemic theory adds stronger structure and can behave differently. The control distinguishes two conclusion types in the PSR discussion; it does not certify that a real person occupies any of these states.

## D9. Fact atomicity does not imply attribute identity without a map

Take a fact sort with one member q and reflexive parthood only. Take a bearer sort with one member g and an attribute-token sort with distinct members k and p. Both qualify g. No relation maps k or p to proper parts of q.

The fact-atomicity antecedent is true. The conclusion k=p is false. The model therefore disproves the unqualified cross-sort inference. It does not disprove any stronger theorem with an explicitly supplied, faithfully interpreted map.

To obtain an attribute consequence one would need, for example, an injective attribute-to-fact map, a theorem assigning each relevant image as a part of q, and source justification of both conditions. If the map sends an attribute to a proposition about its bearer rather than an actual component, that semantic shift must be retained rather than hidden by the word “part.”

## D10. Positive necessity and voluntary action do not entail modal collapse without necessary determination

Let `□` mean truth throughout a declared W. From `□(D→E)` and D at the actual world, one obtains E at that world. To conclude `□E`, one additionally needs `□D` or another premise sufficient to spread D/E throughout W.

For an explicit interpretation, take two worlds with a bearer g present at both, D and E true at the first and false at the second. The implication holds everywhere and g exists necessarily, yet E is not necessary. This is standard propositional/modal reasoning and is not an independent model of divine willing.

The semantic gain is to keep standing necessary power, particular complete determination and product distinct. A proof treating all determinations as necessary seeds must take responsibility for that assumption; it cannot attribute the resulting modal collapse merely to the necessary existence of the bearer.

## Verification scope

D1–D9 have corresponding exact finite/rational controls in `engineering/diagnostics.py`; some controls are inherited-model reimplementations. D10 is written reasoning only. None of the probability examples is an experiment on actual cognition, and none of the modal/causal interpretations certifies metaphysical possibility.

Use `python3 engineering/replay.py --output /absolute/path/to/new-output` from the extracted archive. The replay verifies the sealed input inventory, runs the tests, recomputes a canonical diagnostic result, and checks that the research tree is unchanged. It uses no network and modifies no repository. See `engineering/README.md` for the trust boundary.
