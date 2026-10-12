# U10 — endpoint-indexed parametric PER replacement

## R00. What is replaced, and what is not

The two predecessor equations about arbitrary canonical unary membership and raw-conversion identity extension remain false. They are not repaired by changing `Conv`. This file constructs a **separate, type-relative partial-equivalence-relation model over the same raw SKI programs**, proves its identity-extension/abstraction theorems, and specifies its dependent and finite-effect scope. A PER is a symmetric, transitive relation; its domain consists of its self-related elements. Equality in a function PER is behavioural at that type, not equality of source normal forms.

No semantic Code, accepted theorem, source status or canonical universe is replaced. In particular, a finite source derivation has both the original accepted interpretation and the new interpretation by separate induction; we do not assert that their type objects are identical. Higher-type variance makes a blanket inclusion between recursively interpreted old/new types unjustified. These distinctions are necessary parts of the theorem, not qualifications to be removed on adoption.

The original predecessors V4::T15/T16/T17/V4-R1 and the exact raw countermodels remain inside the unchanged attempt-0001 ZIP. The exact source record's historical “uncompiled” clause is not revived: mapped finite R1 is already accepted at 4.19.0. The new results below have ordinary mathematical proof status; kernel credit is separately recorded.

## R01. Objects, endpoints and relations

Let V be the exact raw `Term` set, with canonical source conversion ≈ and application. A **code P** in the new universe `PC` is a PER `E_P⊆V²` saturated under ≈ in both coordinates. Thus if t≈t′ and u≈u′, `E_P(t,u)↔E_P(t′,u′)`. Write `|P|={t:E_P(t,t)}`. A relation between P and Q is a predicate R(t,u) with:

* endpoint restriction `R(t,u)⇒t∈|P|∧u∈|Q|`;
* respectfulness `E_P(t,t′)∧R(t,u)∧E_Q(u,u′)⇒R(t′,u′)`.

By symmetry, respectfulness also gives equivalences for replacing either endpoint. All relation quantifiers below range over **these explicitly indexed relations**, not over unindexed binary predicates.

Every canonical Code A gives a PC object `ΔA(t,u):=A.accepts(t)∧Conv(t,u)`. Its PER and saturation laws follow from Code invariance and Conv equivalence. Conversely every P has a canonical shadow Code with accepts `E_P(t,t)`. This shadow is conversion-invariant. These two operations on individual objects do not imply that every new type constructor equals its old counterpart.

An environment is `ρ:Nat→PC`. A relational environment is the triple `r=(ρ₀,ρ₁,(R_n:Rel(ρ₀n,ρ₁n))_n)`. Its diagonal `Δρ` has the same endpoints and uses `E_(ρn)` as each relation. Extending r by a type argument means extending **both** endpoint environments and their displayed relation simultaneously. This explicitly records the endpoint dependence missing from the failed fixed-environment implication.

## R02. Arrow and bottom constructors

Bottom is the empty PER. For P,Q define

    E_(P⇒Q)(f,g) iff ∀x y, E_P(x,y) → E_Q(f x,g y).

Symmetry follows by swapping related inputs. For transitivity of f~g and g~h, use f~g at x,y, and g~h at y,y; `E_P(x,y)` implies `E_P(y,y)`. Transitivity in Q yields the result. Raw saturation follows by application congruence. Thus this really is a PC object, including when P has empty domain.

Given domain relation R_A and codomain relation R_B at four endpoint codes, the arrow relation is

    Rel_arrow(f,g) iff
      f∈|P_A⇒P_B| and g∈|Q_A⇒Q_B| and
      ∀x y, R_A(x,y) → R_B(f x,g y).

The endpoint clauses are not omitted. To replace f by f′ under the left arrow PER, use the self-relatedness of x supplied by R_A, obtaining E_(P_B)(f x,f′x); then apply respectfulness of R_B. The right side is identical. This proves respectfulness of the arrow relation.

At a diagonal environment, this relation is **exactly** the arrow PER. One direction discards redundant endpoint clauses; conversely PER symmetry/transitivity imply the two endpoint memberships. This proves arrow identity extension for the new equality. It does not prove the false identity-extension equation for the canonical raw diagonal. In particular I and S K K may be equal at an arrow PER while their raw normal forms remain distinct.

## R03. Parametric impredicative All — explicit unary restriction

It is not enough to use an ordinary intersection of unary domains and hope that identity extension will follow at All. The missing parametricity restriction must be part of the **new** object definition.

Assume a body type B already has object interpretation `B₀(ρ)∈PC` and relation interpretation `B₁(r):Rel(B₀ρ₀,B₀ρ₁)`, with respectfulness and identity extension. For a fixed outer object environment ρ define

    Par_(B,ρ)(t) iff
      ∀P Q∈PC, ∀R:Rel(P,Q),
      B₁(Δρ extended by (P,Q,R))(t,t).

The All object is the PER

    E_Allρ(t,u) iff
      Par_(B,ρ)(t) and Par_(B,ρ)(u) and
      ∀P∈PC, E_(B₀(P::ρ))(t,u).

The heterogeneous All relation at r is

    All₁(r)(t,u) iff
      t∈|All₀(ρ₀)| and u∈|All₀(ρ₁)| and
      ∀P Q∈PC, ∀R:Rel(P,Q),
      B₁(r extended by (P,Q,R))(t,u).

All quantifiers and their endpoints are displayed. `Par` does not follow from arbitrary old unary membership; it is a new domain restriction, exactly where the predecessor countermodel says a restriction is required.

**PER and raw invariance.** Symmetry/transitivity of E_All follow pointwise from those of each body PER, retaining the two Par clauses. Body relations are raw-invariant, so Par and E_All are raw-invariant. A Par value has every required body self-membership by choosing P=Q and R=E_P and using body identity extension. Consequently the All domain is precisely the stated parametric uniform programs, not an empty formal placeholder.

**Respectfulness.** Suppose t E_All₀ t′, u E_All₁ u′ and All₁(r)(t,u). For any P,Q,R, endpoint All equality gives body equality at P on the left and Q on the right. Body relation respectfulness transports the displayed body relation to (t′,u′). Endpoint memberships are preserved by PER laws. This proves All relation respectfulness.

**Identity extension.** At r=Δρ, All₁(r)(t,u) supplies endpoint Par membership. Taking P=Q,R=E_P and applying the body's identity extension yields `E_B(P::ρ)(t,u)` for every P, hence E_Allρ(t,u). Conversely suppose E_Allρ(t,u). For arbitrary P,Q,R, Par(t) gives the body relation of (t,t). The homogeneous component of E_All at Q gives body right-endpoint equality of t and u. Body respectfulness transports (t,t) to (t,u). Therefore All₁(Δρ)=E_Allρ. **No existential coupling or other existential witness is exchanged with these universal quantifiers.**

Because E_All is a PER on the same fixed set V, it belongs to PC. Its own code is therefore a permitted type argument in this new model. This is an independently proved legal self-instantiation statement; it does not redefine the old `Code.all` or add a decoder for PC as an object-level type.

## R04. Interpretation, transport and substitution

Interpret the exact finite source type grammar by variable lookup, empty PER, R02 arrow and R03 All. Simultaneously interpret its binary relations by lookup, empty relation, arrow relation and All relation. Structural induction, with the explicit proofs R02/R03, gives endpoint inclusion, respectfulness, raw-conversion compatibility and

**R04-IE:** `Rel_A(Δρ)(t,u) ↔ E_(Obj_Aρ)(t,u)`.

Renaming maps all three components of an environment. Under a binder, zero is the new code/relation and successor variables use the renamed old components. The ordinary structural renaming proof therefore commutes with object and relation interpretation.

For a simultaneous type substitution σ, define the substituted object environments by `ρ′_i(n)=Obj_(σn)(ρ_i)` and the relation environment by `R′_n=Rel_(σn)(r)`. Its endpoint/respectfulness laws are R04. Then

    Obj_(A[σ])(ρ) = Obj_A(n↦Obj_(σn)ρ),
    Rel_(A[σ])(r) = Rel_A(r′).

Proof is simultaneous structural induction on A. Variable and bottom are immediate, arrows use component equalities. Under All, lift σ and the three environments together. In the **object** All's Par clause the induced relation environment of a diagonal is diagonal because R04-IE has already been proved for each substituted type σn. That is the nontrivial square which an endpoint-only informal notation would hide. Applying the body induction hypothesis then identifies every quantified P,Q,R clause and each homogeneous component. Relations use the same lifted substitution and endpoint object equalities. Thus instantiation chooses an actual interpreted code/relation triple and is well typed at both endpoints.

Equal PER relations determine the same object up to extensional equality of predicates; proof fields are irrelevant. A mechanisation may use setoid equality rather than Lean structure equality, but must preserve the displayed pointwise equations. No raw-program equality is inferred from equality of semantic predicates.

## R05. Contextual finite-source abstraction theorem

Extend source syntax by finitely many inert term variables solely for the new contextual calculus. A context Γ is a finite list of source types. The rules are variable, exact I/K/S schemes, application, forward compatible reduction and the following type rules:

    renameTypes succ Γ ⊢ t:B        Γ⊢t:All B
    ------------------------       -----------------
          Γ ⊢ t:All B               Γ⊢t:B[A].

Generalisation does **not** hold a type-dependent term assumption fixed. For the accepted closed calculus Γ is empty, so this reduces to its exact one-premise `allI` rule.

Fix a relational environment r and closing valuations θ₀,θ₁. They are related at Γ when every corresponding entry is related by Rel at the appropriately interpreted context type. Then

**R05-FT:** `Γ⊢t:A ⇒ Rel_A(r)(t[θ₀],t[θ₁])`.

Prove this by induction simultaneously with endpoint self-membership. Variables use the valuation relation. For I/K/S, their raw root computations transport along respectful relations; endpoint PER membership is proved with the same computation and the PER arrow clauses. Application uses the arrow relation and the argument induction hypothesis. For All introduction, arbitrary P,Q,R extension leaves the lifted context relation unchanged by renaming. Thus the same fixed valuations satisfy the body hypothesis. Endpoint Par clauses follow by applying the induction hypothesis to each endpoint valuation with itself, at diagonal outer environment and arbitrary P,Q,R; context self-relatedness follows from endpoint membership and R04-IE. This supplies the extra unary Par restriction rather than assuming it. All elimination selects `(Obj_Aρ₀,Obj_Aρ₁,Rel_A r)` and applies R04's substitution square. Forward reduction is preserved by closing substitution and by raw-invariance of every relation.

Consequently every actual `FiniteDerives t A` is in the new model at all environments, with θ empty. This gives a genuine abstraction theorem for **the complete actual finite calculus**, not merely some enumerated I/K/S terms. It is stronger than a claim that its printed normal form looks parametric, and different from the false statement about all canonical unary realisers.

## R06. Dependent relation families and structural constructors

The dependent extension uses the PER contextual model detailed in U11. For clarity its relation indices are stated here. At related context valuations γ₀,γ₁, a type A supplies endpoint PERs A₀(γ₀),A₁(γ₁) and a respectful relation `R_A(γ₀,γ₁)`. A family B over Γ.A supplies, **for each pair x₀,x₁ related by that particular R_A**, endpoint fibres B₀(γ₀,x₀),B₁(γ₁,x₁) and a respectful relation `R_B(γ₀,γ₁,x₀,x₁)`. Relations depend on these indices, not on an unrecorded proof witness. Coherence transports them when any endpoint is replaced by its context/domain PER equality. Formation derivations, not arbitrary user functions, establish these laws.

The Pi relation requires endpoint membership in the corresponding dependent Pi PERs and relates f,g exactly when every R_A-related x,y gives R_B-related applications f x,g y. Respectfulness uses the Pi PER at self-related arguments, then fibre relation respectfulness, exactly as R02 with its indices retained.

The Sigma relation uses representatives z≈pair(x,u), w≈pair(y,v), requiring R_A(x,y) and R_B(x,y)(u,v), together with their endpoint memberships. Projection beta, raw saturation and indexed coherence prove independence from representatives and respectfulness. Its diagonal is exactly the dependent Sigma PER.

The new identity PER has domain p with `E_A(x,y)` and `p≈I`. At related endpoint pairs, the identity relation also requires the cross relations of the two displayed endpoints and p≈I,q≈I. The motive of J must respect the context, **both identity endpoints and the equality-proof coordinate**. A base pair of related branches then remains related at arbitrary admissible y,p by these transports, and each J tracker raw-reduces to its branch. This proves relational J, not just unary endpoint transport. The predecessor proof-inspecting motive violates precisely this formation law.

Identity extension for these constructors follows from their displayed definitions: Pi uses the pointwise PER; Sigma uses its representative condition; Id uses the singleton proof PER and endpoint identity extension. Type substitution transports context/endpoints and then these formulas. At All use R03 once more. Types may therefore be formed from variables, bottom, Pi, Sigma, Id and All. Nondependent products are a Sigma instance; no sum constructor or effectful dependent bind is required by the actual source contract or introduced here.

## R07. Dependent fundamental theorem and equality

A term is interpreted by an **actual open SKI tracker**, not by an arbitrary ambient section. For abstraction, standard bracket compilation supplies `([x]p) a →* p[a/x]` under any closing context valuation. If two extended valuations are related, the body's induction hypothesis relates the two results. Two beta transports then prove the dependent Pi relation of the compiled abstractions. This proves abstraction congruence **in the Pi PER**, without claiming raw conversion of the two un-applied compilers.

Every other typing constructor has a matching relation lemma: application is the Pi clause; pairing/projections use R06; reflexivity is the identity singleton; Sigma eta uses actual encoded representatives and projections; J uses the two-coordinate motive transport; polymorphic rules use the lifted relational environments of R05; conversion/reduction uses saturation and contextual type coherence. Variables and substitution tuples use their displayed context components. These are the complete rules of the proposed checker language. Induction on its well-formedness/typing derivations yields the dependent abstraction theorem. The underlying unary soundness into the shadow Code follows by taking the diagonal and using identity extension.

Typed PER equality is permitted to be coarser than the checker's computational conversion. The checker decides no arbitrary semantic PER assertion. In particular neither a successful typed relation test nor its compiled program grants `Conv I (S K K)`.

## R08. Exact effect and observational scope

For the **unchanged** accepted finite `EffectDerives` and `Outcome`, the predecessor outcome-transfer theorem supplies FiniteDerives for every positive outcome. Apply R05, or its dependent extension where a new typed finite effect context is explicitly supplied. Finite rational probability and common couplings are fully specified in `U10_COUPLING_THEOREMS.md`.

The completed statement is not merely per-outcome inheritance: a type-independent finite random seed, synchronised between two related runs and independent between distinct application subtrees within each run, constructs a **single common output coupling** supported in every required relation environment. For a closed original effect expression its diagonal is the special case already established in attempt-0001. Compatible finite contexts and relation-respecting observations preserve the coupling and therefore give equal observed distributions. No theorem covers arbitrary representation-inspecting observations, general recursion, value-dependent probabilistic bind, continuous distributions or code-dependent sampling weights. Those are absent from the actual grammar, not hidden P02 dependencies.

## R09. Terminal mathematical disposition

**False target retained:** canonical raw-conversion identity extension and arbitrary fixed-environment unary-to-relational membership.

**Replacement proved:** the endpoint-indexed, respectful, parametric PER interpretation above satisfies identity extension, renaming/substitution, a fundamental theorem for the actual finite source calculus, its stated contextual Pi/Sigma/Id/All extension, and the finite-effect common-coupling/observation theorem at exactly the stated hypotheses.

This is a new research interpretation. Adoption of type-relative PER equality or the parametric All domain is an explicit later choice. It does not retroactively turn the false old equation into a theorem or replace the accepted raw Code universe. No global claim of a uniquely strongest semantics, novelty, independent expert review or kernel verification is made.
