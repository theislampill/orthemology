# U10 — logical relations, identity extension and finite effects

**Disposition: PARTIAL.** Two unrestricted extensions are refuted at precise scope. A finite-outcome relational theorem and its finite rational diagonal-coupling corollary are proved as ordinary mathematics; a new contextual relation-environment proposal is specified. Four-way conflation of unary membership, derivational relationality, identity extension and full Reynolds semantics is explicitly refused.

## 1. Exact inherited scope

The unchanged obligation binds `RelationalFragment.lean`, `PRIOR_ART_COMPARISON.md`, `InternalPolymorphism.lean` and `ABSTRACT_OWOU.md`; its predecessors are V4::T15, T16, T17 and V4::V4-R1, with concepts A4C-C041/C042. Exact hashes and source rows are retained in the obligation files.

The phrase “its source is uncompiled” is historical. Included accepted A8F evidence checks the mapped finite fragment at 4.19.0. It is not permission to edit the historical sentence or to infer the stronger theorem. The canonical finite result is

```
FiniteDerives t A → ∀rho, (relInterpret A rho).relates t t.
```

`rho` ranges over all step-stable raw binary `RelationCode`s. This theorem has a finite pure derivation hypothesis. It is not an assertion that every member of every unary code is relationally uniform. The identity/Boolean/numeral representation theorems retain their exact membership, marker-freshness and conversion hypotheses.

## 2. P01-U10-01 — identity extension fails for the raw-conversion diagonal

Define `Δ_A(t,u) :⇔ A.accepts t ∧ Conv t u`. Stability of A supplies endpoint membership for u. This is a step-stable relation. At `A=top`, Δ_A is just raw conversion.

For the type `α→α` at the unary environment α↦top, ordinary arrow interpretation is top. Relation interpretation at α↦Δ_top relates f,g exactly when they take related inputs to related outputs.

Put E=S K K. For any x,y with x≈y,

```
I x → x ≈ y ← K y (K y) ← E y.
```

Hence `(I,E)∈(Δ_top⇒Δ_top)`. But `(I,E)∉Δ_(top⇒top)`: I and E are distinct normal forms and are not convertible, by the explicit ordinary confluence proof in U09 §5.

Therefore the identity-extension equation

`R_(α→α)[Δ_top] = Δ_([[α→α]]_(α↦top))`

is false for the canonical raw-conversion equality. Endpoint restrictions do not rescue it because every endpoint here is in top. Replacing the diagonal by literal term identity fails even sooner and is not a stable `RelationCode`.

This does **not** refute finite_fundamental, or the fact that both I and E behave as identities. It refutes identifying behavioural arrow relatedness with equality of their raw program representations. The normal-form separation depends on the ordinary confluence proof, not on bounded failure to discover a path.

**Review boundary.** An extensional equality, a PER interpretation, or an alternative relational decoding would be a new definition. No such definition is patched into `Conv`, `Code`, `El`, `RelationCode` or the accepted internal All by this packet. Fixing this one arrow witness would not, by itself, establish identity extension at universal or dependent types.

## 3. P01-U10-02 — a fixed-environment unary-to-relational implication is false

The statement `t∈[[A]]_rho ⇒ (t,t)∈R_A` for an arbitrary compatible chosen relation environment fails even at a simple arrow in one fixed unary environment.

Take rho(α)=top and t=K. Unary membership at α→α is vacuous on the codomain and holds. Let `R(x,y)` mean `Conv x I ∧ Conv y I`. This relation is stable and is a subrelation of top×top. R(I,I) holds, but R(K I,K I) does not: K I and I are distinct normal forms. Therefore `(K,K)∉(R⇒R)`.

This witness is deliberately scoped. It does **not** establish that a closed term belonging to a closed polymorphic type under every unary interpretation fails every stronger invariance theorem. K at this fixed arrow is not claimed to inhabit `∀α.α→α`. The quantifier difference is preserved, so the witness neither misstates Pistone 5.21 nor weakens accepted free theorems.

## 4. P01-U10-03 — an endpoint-aware contextual relation proposal

This is a separate candidate definition, not a source-status promotion. A relation environment is a triple

`(rhoL,rhoR,R)`

where each rho is a Nat→Code assignment and every R(n) is stable in both term coordinates with `R(n)⊆El(rhoL(n))×El(rhoR(n))`.

Define the proposed interpretation `Rel_A(rhoL,rhoR,R)` as follows. Variables use R(n); bottom is empty. An arrow relates f,g only if they have their respective unary arrow memberships and they map related arguments to related results. A universal type relates t,u only if each has its respective unary All membership and, for **every** pair of codes X,Y and every stable endpoint-respecting relation Q⊆X×Y, the body relation holds under the extended triple `(X::rhoL,Y::rhoR,Q::R)`.

Stability and endpoint inclusion follow by induction on the type. The simultaneous-substitution lemma has three components: the two accepted unary interpretation squares and the new relation square. At a binder, lift all three environments together. A type instantiation may then use the triple formed by the two interpretations of the actual type and its relation interpretation; the required endpoint condition follows from the preceding inclusion lemma.

For open source syntax, add finitely many term variables and a finite type context Γ. Add its variable rule; retain the I/K/S schemes, application, instantiation and compatible forward reduction. The correct generalisation rule is

```
renameTypes succ Γ ⊢ t : B
-------------------------
       Γ ⊢ t : all B.
```

For empty Γ this recovers the accepted one-premise shape. Dropping context weakening for a nonempty Γ is not allowed.

**Proposed contextual fundamental theorem.** For a finite derivation `Γ⊢t:A` and two closing substitutions θL,θR that are pointwise related at the corresponding Γ entries, the outputs `t[θL]` and `t[θR]` lie in the proposed Rel_A.

**Ordinary proof.** Induct over that explicit derivation. Variables use the hypothesis on substitutions. For I/K/S, their fixed positive root computations and relation stability establish the relational arrow clauses; ordinary unary soundness establishes endpoints. Application uses the relational arrow clause and its argument induction hypothesis. For generalisation, quantify over arbitrary X,Y,Q; the renamed context is interpreted by the same old environment, so the same pair of closing substitutions remains related. For instantiation, apply the induction hypothesis to the interpretation triple of the actual type and use the simultaneous-substitution lemma. For forward reduction, the open SKI rewrite is preserved by closing substitution, and stability transports both endpoints and the relation. These exhaust the constructors.

This is a fundamental induction for a **new finite contextual derivation system**, not semantic completeness and not the missing full Reynolds model. No universal identity-extension lemma is used; §2 would make that premise false for the raw diagonal. The proposal needs a formal context datatype, weakening/substitution proofs and the exact inclusion lemma before any implementation acceptance. It does not introduce lambda abstraction and so does not evade U11's separate abstraction-congruence defect.

## 5. P01-U10-04 — every typed finite outcome has a pure finite derivation

For the **unchanged** accepted `EffectDerives` and `Outcome`:

```
EffectDerives e A → ∀t, Outcome e t → FiniteDerives t A.
```

**Proof.** Induct on the effect derivation and invert the outcome witness. A pure expression yields its original finite derivation. A positive-weight left or right outcome of a mixture comes from the corresponding branch, so use that branch's induction hypothesis. An application outcome is an application of a function outcome and an argument outcome; combine their finite derivations with `FiniteDerives.app`. Generalisation and instantiation wrap the resulting finite derivation with the same source constructor. Zero-weight branches cannot appear in the positive-support premise. No other effect constructor exists.

Compose this result with accepted finite_fundamental:

```
EffectDerives e A →
  ∀t, Outcome e t → ∀rho, (relInterpret A rho).relates t t.
```

The order says that each outcome works at **all** relation environments. `P01FiniteEffects.lean` contains complete-looking, but locally unverified, candidates for these statements and for their common diagonal-support consequence. It contains no definition of probability mass and makes no kernel claim about mass.

## 6. P01-U10-05 — one uniform coupling for the exact finite rational effects

Use only finite rational probability. For p=num/den with positive den and 0≤num≤den, define

```
μ_pure(t) = δ_t
μ_mix(p,l,r) = p μ_l + (1-p) μ_r
μ_app(f,x)  = app_*(μ_f × μ_x).
```

The last product is justified by the included source's once-per-subtree independent sampling semantics. Each expression has finite support and total mass one, by structural induction. Positive mass is equivalent to `Outcome`: for mixtures, a nonnegative finite sum is positive exactly when some positively weighted summand is positive; for application, some positive product in the finite preimage witnesses the outcome rule.

**Theorem.** If `EffectDerives e A`, define π_e(t,u)=μ_e(t) when t=u and zero otherwise. Then π_e is a coupling of μ_e with itself, and for every rho its positive support is contained in `relInterpret A rho`.

Both marginals equal μ_e because a fixed row or column contains its sole possible nonzero entry at the diagonal. If π_e(t,u)>0, then t=u and Outcome e t. Apply §5 for every rho. Thus **the same coupling** works for all rho: no choice of relation-dependent couplings is hidden in the quantifier order. This is a finite-effect theorem, not a full Reynolds identity-extension result, not an atomless measure theorem and not a theorem about divergent stochastic evaluation.

For comparing two different finite expressions, the usual sufficient constructions can be stated without enlarging this result. Related pure outcomes have a Dirac coupling. Mixtures with the **same weight** combine already-supplied branch couplings. For independently sampled application nodes, take the product of a function coupling and an argument coupling and push it forward along paired application; the arrow-relation clause proves the support property. Unequal weights, shared random state, continuous laws or probabilistic term reduction require additional hypotheses and are not supplied by these constructions.

## 7. P01-U10-06 — couplings do not commute with arbitrary relation intersections

Let both marginals be the fair law on {0,1}. For

`R_eq={(0,0),(1,1)}` and `R_flip={(0,1),(1,0)}`,

the diagonal fair coupling is supported by R_eq; the anti-diagonal fair coupling is supported by R_flip. Their intersection is empty. No mass-one coupling can have empty support. Hence

`(∀R in {R_eq,R_flip}, ∃π supported by R)`

does not imply

`∃π, ∀R in {R_eq,R_flip}, π supported by R`.

This exact two-element countermodel refutes an unrestricted effectful universal-quantifier interchange. It does not refute canonical `support_all_iff`: that theorem fixes one support predicate before moving universal quantifiers and introduces no existential coupling. Section 6 succeeds precisely because it constructs a common diagonal coupling first.

Nor should a self-coupling be replaced by every possible cross-pair of outcomes. A mixture of two different typed Boolean projections may have a diagonal coupling while its cross-pairs are not all Boolean-related. The packet claims the supported-coupling property, not universal cross-outcome equality.

## 8. Dependent relations: exact conditional boundary

For a related pair of domains `(A_L,A_R,R_A)`, a dependent relation requires fibres B_L(x),B_R(y), plus a relation between those fibres for each related input pair. It must specify transport/coherence in x and y, and either proof-irrelevance for the witness of R_A(x,y) or explicit witness-indexed transport. A Pi relation quantifies over such related argument pairs; a Sigma relation relates their first projections and then their second projections in the displayed fibre relation.

A J rule additionally needs the relational motive to respect all endpoint and equality-proof transports. Unary code coherence is not that theorem. The proof-coordinate countermodel and a restricted unary based-J lemma are given in U11. No dependent Reynolds fundamental theorem follows here from the finite effect theorem. These are **conditional design obligations**, not passed inputs from another packet.

## 9. Completion and source comparison

`LITERATURE_COMPARISON.md` gives the exact 5.21/7.1 hypotheses and distinctions. A raw-SKI-to-lambda reduction simulation is not enough to identify the two semantic models: U09 §7 explicitly refutes conversion reflection. The new finite-effect argument is a consequence of finite outcome retyping and the accepted R1, with an independently constructed finite rational coupling. No historical novelty or outside review is claimed.

The obligation remains PARTIAL: preserved R1 stays accepted at its pin; the stronger raw identity-extension claim is falsified; finite effects are resolved at ordinary proof scope with an unverified candidate; a full semantic/dependent model is not established. No source record is relabelled, and no P02/P03 result has been presumed.
