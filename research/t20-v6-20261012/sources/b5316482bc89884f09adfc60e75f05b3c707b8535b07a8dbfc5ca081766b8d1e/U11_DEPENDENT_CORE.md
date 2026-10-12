# U11 — a contextual dependent core with a sound PER interpretation

## D00. Equality diagnosis and selected architecture

The two failed bracket compilers remain raw-conversion counterexamples. They do not refute contextual dependency. This proposal keeps the canonical SKI substrate and its exact `Conv`, but interprets a **new typed calculus** in the type-relative PERs of U10. Thus abstraction is compared pointwise in a Pi PER; no global extensionality axiom is added to raw SKI.

The alternatives have distinct dispositions. An eta shortcut on the old compiler already failed. Normalising a body before compiling it fixes a fixed-body equation but breaks substitution naturality: for body y x, substitute y=I after compilation to obtain S(KI)I, whereas first substitute and normalise I x to x and then compile gives I. These are distinct raw normal forms. A raw quotient by lambda beta/eta would strictly enlarge accepted equality and require separate preservation/quotient proofs; it is not silently chosen. A direct binder-bearing syntax is useful as the **front end** used here, while its back end remains actual SKI. A PER/setoid interpretation gives the required well-definedness: equality of typed functions is defined by related applications and proved to be a PER. It is not a quotient asserted without a congruence theorem.

The new `Id_PER` likewise is not the old raw `equalityCode`: its endpoints may be equal in their type PER without being raw-convertible. At a raw diagonal PER the two definitions agree; at an extensional function PER they need not. This is an explicit new semantic layer for later review, not an amendment to an accepted definition.

## D01. Semantic contexts and types

For each fixed type environment, a context Γ of length n has a PER E_Γ on length-n tuples of raw terms. Empty context has the unique empty tuple. A type over Γ is a family A(γ) of PC objects, defined on Γ's domain, with

    E_Γ(γ,δ) ⇒ E_A(γ)=E_A(δ)  (pointwise as binary relations).

Form the extension Γ.A with elements (γ,x) and equality

    E_(Γ.A)((γ,x),(δ,y)) iff E_Γ(γ,δ) and E_A(γ)(x,y).

Symmetry/transitivity follow from context PER laws and A's displayed coherence. This also proves that the second coordinate is accepted at the corresponding endpoint type; no arbitrary invalid tuple is treated as an environment. Where a total raw-indexed family is convenient, assign bottom outside the domain. PER equivalence cannot cross the domain boundary, so this totalisation preserves coherence. It is metatheory, not executable inspection of a semantic code.

A term of A is an open SKI polynomial p in the n context variables with

    E_Γ(γ,δ) ⇒ E_A(γ)(eval(p,γ),eval(p,δ)).

This supplies a **single actual program tracker**. It is not the full ambient set of functions γ↦values. Substitution from Δ to Γ is a tuple of such represented terms, typed successively in the telescope. Two substitutions are equal when their tuple evaluations are E_Γ-related at every E_Δ-related pair of environments.

## D02. Syntax of the smallest specified core

Raw runtime terms are de Bruijn variables; I/K/S and the two inert markers; lambda/application; pair/first/second; `refl`; based `j(d,y,p)`; and `eta(z)`, the encoded-Sigma-eta proof. Markers have no typing introduction rule. There are no runtime type abstractions or type applications: All introduction/elimination are erased certificate rules as in the accepted finite fragment.

Types are

    α_n | bottom | Pi(A,B) | Sigma(A,B) | Id(A,t,u) | All(B).

Pi/Sigma bind one **term** variable in B; All binds one **type** variable. Terms contain no type variables or annotations at runtime. The interface distinguishes a type-parameter depth from a term-context telescope. There is no object term `Universe`, no `Type:Type`, no type-family branch on proof representations and no external semantic membership oracle.

A context is well formed by empty context and extension by a formed type. Type formation is variable scope, bottom, Pi/Sigma with formed domain and codomain in Γ.A, Id with two checked endpoints of its formed base, and All with one added type parameter and the old context's type variables shifted. User-supplied Id indices are themselves term certificates, not arbitrary unchecked raw expressions.

Typing rules are variable; nondependent I/K/S schemes; lambda, application; annotated dependent pair and its projections; reflexivity; encoded Sigma eta; based J; All introduction/elimination; forward finite reduction; and computational type conversion. The relevant rules are stated below. `executable/checker.py` reconstructs their conclusions rather than trusting a supplied conclusion.

## D03. Structural substitution — exact two-sort operations

For raw term substitution θ, variables map by θ and every nonbinding constructor maps componentwise. Under lambda, lift θ by `θ↑(0)=v₀` and `θ↑(n+1)=shift(θn)`. The variable cases prove identity and composition; the constructor cases use the component induction hypotheses; the lambda case uses the displayed lift and its composition equation. This proves capture-avoiding substitution for every raw constructor, including J, pair/projections and eta.

Term substitution in a type acts on all its term indices. It lifts once in the codomain of Pi/Sigma and does not lift at an All type binder. Type substitution changes type variables, leaves raw term indices untouched, lifts type variables under All, and **weakens substituted dependent types under each Pi/Sigma term binder**. The last clause is essential when instantiating a polymorphic identity at a type such as Id_α(x,x): the codomain under its new function argument refers to shifted x, not to that argument. A dedicated fixture checks this exact case.

Induction on types proves the two identity/composition laws and commutation of term substitution with type substitution, using the corresponding lifted maps at the two different binders. For Id, use raw term substitution identity/composition for both indices and the base-type induction hypothesis. For Pi/Sigma, use the type hypothesis in the extended context and the lifted-map equation. For All, use type lifting and the fact that runtime term indices are type-erased. These are the operations `tm_sub_ty`, `ty_sub`, `ty_rename`, `tm_inst`, and `tm_inst2` in the implementation.

Polynomial evaluation commutes literally with polynomial substitution: variable lookup gives the assigned value; constant cases are fixed; application combines its two hypotheses. Consequently identity substitutions act as identity and composing substitution tuples is associative. The projection Γ.A→Γ drops the newest coordinate; the newest variable is its second coordinate; pairing a substitution with a term gives a substitution into Γ.A. Their projection and pairing equations are literal tuple equations.

## D04. Bracket abstraction, naturality and typed congruence

The compiler first eliminates inner binders. To bracket the newest remaining variable x, use I for x, **K applied to the whole variable-free subterm** when x is absent, and S applied to the recursively bracketed children otherwise. Older variables are lowered after x is removed. No beta-normalisation or eta shortcut is applied during compilation.

For every closing environment γ and argument a,

    app(eval([x]p,γ),a) →* eval(p,(γ,a)).

Proof is structural. For x use I beta. In the variable-free case use K beta. For application use S beta followed by the two child reductions in their respective application positions. Thus even a complex variable-free argument is retained in the same polynomial shape, without a normalisation assumption.

Capture-free substitution for older variables preserves whether x occurs. The variable-free case therefore remains a single K case on both sides; the bound-variable case remains I; and application uses the two induction hypotheses. This proves the literal compiler/substitution square for the selected backend. The initial new implementation omitted the whole-subterm K priority; a new test found its strict square failed, and the repaired implementation and its exact preimage/red log are retained. This is a proposal implementation repair, not a change to old evidence.

For typed abstraction, if p is a term of B over Γ.A, then for E_Γ-related γ,δ and E_A-related a,b, the body gives related results at B(γ,a). The two application-beta reductions and raw saturation transfer that relation to the compiled function applications. Hence the abstractions are related by the dependent Pi PER. If two bodies are equal at every related extended valuation, the same proof gives equal abstractions in that Pi PER. This is the required abstraction congruence theorem. It does **not** give raw Conv of their un-applied compiler outputs.

## D05. Pi formation, application and substitution

For coherent A over Γ and B over Γ.A define

    E_Piγ(f,g) iff ∀x y, E_Aγ(x,y) → E_B(γ,x)(f x,g y).

Fibre coherence identifies B(γ,x) and B(γ,y) when x~y. Symmetry swaps x,y and uses that identification. Transitivity uses the intermediate argument y, which is self-related whenever x~y, then transitivity in its fibre. Raw saturation is application congruence. Context coherence follows by transporting A and B along E_Γ. This proves Pi is a formed PC-valued family.

Application of related functions to related arguments is its defining clause. A checked lambda is interpreted by D04. Reindexing by a substitution σ replaces γ by σγ in this formula; extension of σ with the newest variable supplies the codomain substitution. Thus Pi formation, lambda and application commute with substitution, with beta witnessed by the actual tracker reduction. Function eta is a semantic Pi-PER theorem by applying both sides to related arguments; it is not added as raw SKI equality or required as a new computational rewrite.

## D06. Sigma formation, introduction, projections and eta

Use the unchanged `pairTerm`, `firstTerm`, `secondTerm` polynomials. Define E_Sigmaγ(z,w) by witnesses x,u,y,v with

    z≈pair(x,u), w≈pair(y,v), E_Aγ(x,y), E_B(γ,x)(u,v).

The last condition includes domain membership for u and v. Symmetry uses A/B symmetry and fibre coherence. For transitivity, projections of two witnesses for the middle w are raw-convertible, by the accepted pair projection beta laws; saturation relates their first and second components. Transitivity of A, coherence of B and transitivity in the second-component fibre then give the composite witness. This proves well-definedness, not just a constructor signature.

Projection beta also proves that first(z) has A's domain and second(z) has B(first(z))'s domain, and that related z,w have related projections. Pairing related components supplies the introduction rule. For an actual inhabitant z, choose a pair witness x,u; first(z)≈x and second(z)≈u. Congruence of the pair polynomial gives

    pair(first(z),second(z)) ≈ pair(x,u) ≈ z.

Thus the predecessor's **encoded Sigma eta is retained at raw Conv on actual represented Sigma inhabitants**. The frontend constructor `eta(z)` represents a proof of this equation at Id_PER; it is not identified syntactically with `refl` and does not add a new raw equation for arbitrary non-Sigma programs. A Sigma eliminator is definable using the projections, with its motive transported along this typed/encoded eta equation. No additional primitive recursor is needed for this specified core.

All Sigma formulas reindex by substituting the outer tuple and extending that substitution with its first component. The pair/projection polynomials commute with substitution. The displayed eta proof then supplies the same transport in each reindexed fibre.

## D07. Identity, coherent based J and computation

For endpoints x,y in a PER P define the new proof PER

    E_Id(P,x,y)(p,q) iff E_P(x,y) and p≈I and q≈I.

It is symmetric/transitive in proof values and saturated under raw conversion. Replacing x,y by their P-equivalents leaves E_P(x,y) unchanged, by symmetry/transitivity. Therefore the identity family is coherent. At P=ΔA it agrees with the old equalityCode domain; in general it need not, and no old definition is overwritten.

Reflexivity is represented by I. For based J, let C be a formed type over Γ.y:A.p:Id_A(x,y). Its formation guarantees coherence in **the outer environment, y, and p**, not merely in y. If p belongs to Id_A(x,y), then y is A-related to x and p is raw-convertible to I, hence related to I in the proof PER. The base valuation (γ,x,I) and (γ,y,p) are therefore related in the extended context. Coherence identifies their C fibres. A base branch d:C(γ,x,I) is consequently accepted in C(γ,y,p).

The actual tracker `K(K d)y p` reduces to d in two K steps. Saturation gives the J membership and the based beta equation at y=x,p=I. For two related outer valuations, the branch terms are related by their typing, and the same two-coordinate transport followed by the two beta reductions proves **relational J**, not only unary transport.

The motive which chooses top for literal proof I and bottom for I I is not coherent in p, even though I I≈I. It is therefore excluded by type formation; the old counterexample is retained. This is not a promise to support arbitrary proof-inspecting motives. The input language has no constructor to supply such a semantic branch.

## D08. All and the exact universe boundary

The type-parameter context ranges over PC objects, separately from runtime terms. The All family, its Par restriction and its endpoint-indexed relation are exactly U10 R03, including proof of identity extension. Introduction checks the body under a shifted old type environment with one new type parameter; its single tracker is independent of that parameter. Elimination substitutes an actual formed type, with its complete endpoint relation. The type-substitution square includes the term-index shifts of D03. The accepted closed finite allI/allE erasure is retained by the embedding described below.

The new All code belongs to PC and can be its own type argument. The canonical `Code.all` and `selfInstantiate` continue to quantify over their original universe and remain unchanged. The two facts coexist; no equality between those universes or their All operations is asserted.

There is no runtime code whose decoding is every ambient type, and no packer for **all** ambient dependent sections. Sections here require one finite program tracker and parametric All additionally requires its displayed relational laws. Thus the hypotheses of the accepted `no_self_product` / SCUUAt theorem are not supplied. In particular, internal self-instantiation is not the retraction

    FullSections → decode(c) → FullSections

with totality and returned beta for every arbitrary ambient section. The exact SCUU hypotheses and negative theorem remain untouched. No Type:Type or universe-level collapse occurs in the proposed grammar.

## D09. Formation and typing soundness — complete rule induction

Interpret a well-formed context by D01. Interpret each formed type as a coherent PER family and its R06 relation family. Interpret a checked raw term by its compiled SKI polynomial. Prove formation/coherence, endpoint typing and relational typing simultaneously by induction on the finite derivations.

Variable formation/typing is environment lookup. Bottom is the empty PER. I/K/S schemes use their raw computational laws and the arrow/Pi PER clauses. Pi formation and lambda/application use D05/D04. Sigma formation and pair/projections use D06. Id formation uses the two endpoint typing hypotheses: their preservation under related contexts makes the endpoint equality condition coherent. Reflexivity uses self-relatedness. Sigma eta uses D06's actual pair witness. J uses D07's full extended-context coherence. All uses D08/R03, with type-variable weakening of every old context entry. Conversion uses equality of the interpreted coherent type families; forward computational reduction uses the typed equality lemma below. These are all constructors, not selected examples.

Substitution soundness is proved simultaneously: variables use the corresponding substitution component; each constant is fixed; application/pair/projections/J commute with polynomial substitution; lambda uses D04's binder-lift naturality and Pi beta; All uses the two-sort lift and R04's environment square; Id and conversion use the type-family substitution equation. It follows that a well-typed term substituted by a well-typed context substitution has the substituted type and the expected interpreted value. This also supplies weakening as substitution by shifted variables, and substitution associativity as D03's componentwise composition theorem.

For computational equality, take compatible closure of frontend I/K/S beta, lambda beta, pair projection beta and `j(d,y,refl)→d`. Lambda beta is D04 plus substitution soundness, including dependent codomain substitution. Pair beta is D06. J beta is D07; the frontend `eta(z)` is a different constructor and cannot trigger this rule. Reduction inside any typed constructor is sound by its relational congruence lemma, with the appropriate dependent fibre transport. Repeated forward reductions and reversal therefore preserve the typed PER equality. Equality inside type indices preserves the family's PER by formation coherence.

The computational syntax is also confluent. Extend the source parallel-development relation with lambda/application and its substitution lemma, pair/projection, j/refl, and inert eta with congruence in its index. Substitution preserves a parallel step by induction on that step; lambda lifts the substitution and beta uses its composition equation. In the complete-development triangle, lambda beta's application/contraction overlap uses this substitution lemma; pair and J root/congruence overlaps preserve their constructor skeleton until the next parallel contraction; I/K/S are the already established cases. The different root heads are disjoint, and the J root is linear in d,y. Thus the diamond-grid proof applies. Types have only independent reductions in their finite term-index positions, so type conversion likewise has finite common-reduct witnesses. This proves completeness of the **finite equality-evidence presentation**, not an oracle for semantic PER equality.

## D10. Executable certificate kernel and its completeness boundary

`checker.py` implements the finite rules above, with exact field whitelists and scopes. It returns reconstructed term/type/context, compiled tracker and conversion evidence. It never trusts a caller-provided conclusion, semantic predicate, family function or purported universe.

In `certificate_only=True` mode, nonliteral type equality requires a supplied finite **common-reduct witness**. Both endpoints must exactly match types already checked or produced by the rules. Each addressed reduction is recomputed by `type_step`/`at_step`; the two final type expressions must be literally equal. The common reduct need not be a normal form. Thus checking a supplied finite certificate terminates without a normalisation or semantic-decision assumption. Reflexivity is accepted without a redundant path. A finite typing/equality derivation can be encoded with its rule tree and, by D09 confluence, its finite common-reduct paths; induction on the tree shows the certificate verifier reconstructs that derivation, subject only to explicitly selected resource limits.

An optional convenience mode searches for equality by bounded full normalisation of type indices. A completed unequal-normal-form comparison is a computational inequality at that syntax; fuel exhaustion is **RESOURCE_REFUSAL**, not inequality. The existence of this convenience mode is not a proof that every dependent term normalises or that all PER equality is decidable. The definitive terminating kernel surface is the finite-evidence mode.

Malformed indices, unknown constructors/fields, invalid traces, non-Pi application, non-Sigma projections, wrong J proofs and unscoped type variables fail closed. Python bools are not accepted as integer indices or fuel. No type inference for unannotated impredicative programs and no arbitrary semantic Code membership decision is claimed. This is a full specified calculus with a finite proof verifier, not a weak collection of semantic constructors relabelled as a calculus. Universal correctness of these Python bytes is supported by the rule/operation correspondence argument above; **it has not been kernel-refined or independently externally reviewed**. Tests are finite implementation evidence only.

## D11. Relation to U09 and original accepted source

Embed a TypeCode arrow A→B as Pi(A,term-weakening(B)); bottom, variables and All retain their constructors. Embed exact raw I/K/S/application programs unchanged. The source finite derivation rules map to the corresponding certificate rules, including allI/E erasure and forward source steps. The old and new semantic interpretations are then separately sound for the same finite derivation.

U09 decides **raw source conversion on finitely typed source inputs**. The full new frontend computational syntax includes binders and proof constructors; U09's positive simulation/SN theorem is not automatically a theorem about that entire syntax. In particular eta's index may reduce while its compiled proof is I, an empty backend change; this must not be counted as a nonempty U09 simulation. The checker uses its own finite equality witnesses and its typed PER soundness, not an illicit global source-normal-form equality test for the PER.

U09 confluence certifies the preserved raw counterexamples. U10's new equality makes the selected compiler sound at Pi and makes identity extension meaningful. U11's tracked contexts and coherent motives supply the dependent clauses used by U10. This mutual specification is not a cyclic proof: basic PER laws → contextual constructors and their typed induction → the relational dependent induction. No P02/P03 result is consumed.

## D12. Research disposition

The previously missing architecture is supplied: a defined contextual syntax, a tracked coherent interpretation, structural/substitution proofs, Pi/Sigma/Id/J/All rules with their actual equality theories, and a finite proof-carrying executable checker. Adoption of this **new PER layer** and canonical implementation changes remain separate. Full semantic PER equality and arbitrary ambient sections are not checker goals; their absence is not a missing implementation trick. Exact Lean qualification and any stronger Python-to-kernel refinement remain separately labelled in the formal ledger and Codex handoff, with no current credit.
