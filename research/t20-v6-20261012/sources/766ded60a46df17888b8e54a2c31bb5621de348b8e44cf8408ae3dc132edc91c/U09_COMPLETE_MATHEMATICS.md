# U09 — exact finite-source normalisation and conversion

## Status and scope

This is a new ordinary proof supplement to attempt-0001, not a replacement of its files. The direct reducibility argument below removes its mathematical dependence on an unprovided Curry-System-F normalisation bridge. It proves strong normalisation for **every constructor of the actual `FiniteDerives` relation**, including impredicative generalisation/instantiation and forward reduction. It does not prove that arbitrary canonical semantic realisers normalise. Formal-source and execution statuses are recorded separately in `formal/FORMAL_STATUS.json`.

Predecessors: V4::T13, V4::T14 and attempt-0001 P01-U09-01 through -06. Exact original wording, hypotheses and source hashes are in `boundary/ORIGINAL_OBLIGATIONS.json`. Throughout, no inference uses reflection of lambda conversion into raw source conversion.

## N01. Exact source and target

The source is exactly `OrthemologyV2.Term`: five constants `I,K,S,zero,one` and binary application. Its compatible reduction `Step` has three root rules

    I x → x
    K x y → x
    S f g x → (f x)(g x)

and reduction in either child of application. `Red` is its finite reflexive/transitive closure. `Conv` is reflexivity, one source step, symmetry and transitivity; application congruence is derived. Inert `zero,one` have no reduction rules. Strong normalisation means accessibility for the reverse step relation, not termination of a selected head strategy.

Source types are exactly `var n`, primitive `bottom`, `arrow A B`, and `all B`. Simultaneous substitution uses de Bruijn lifting: `up σ(0)=var 0`, `up σ(n+1)=rename succ (σ n)`. The actual typing relation has I/K/S schemes, application, **one-premise** `allI`, `allE` by this type substitution, and **forward** `reduce : FiniteDerives t A → Red t u → FiniteDerives u A`. There are no open term assumptions in this accepted relation. The proof therefore does not overlook generalisation of an assumption.

For translation only, the auxiliary target is Curry-style System F with a rigid atomic type κ, de Bruijn type variables, arrow and universal types. Runtime target terms are variables, inert constants and lambda/application. The standard typing rules are variable, arrow introduction/elimination, universal introduction with the free-type-variable condition on the term context, and universal elimination. The target computational relation is compatible **beta only**, including under lambda; no eta or normalization is built into the translation. Primitive source bottom maps to rigid κ, not an instantiable type variable. The closed source constants have lambda translations

    τI = λx.x
    τK = λx.λy.x
    τS = λf.λg.λx.(f x)(g x)
    τ(t u) = τt τu.

Markers translate to inert constants. An auxiliary open source variable translates to the corresponding target variable. Type translation is structural and carries bottom to κ. Auxiliary open syntax is not a new constructor added to canonical `Term`.

## N02. Translation, substitution and typing preservation

Attempt-0001's explicit term/type substitution and positive paths are retained, not re-counted. Here is their role in the completed theorem.

For a simultaneous source term substitution σ, `τ(t[σ]) =α τ(t)[τ∘σ]`. The variable case is the defining lookup, every combinator macro is closed, markers are unchanged, and application follows its two induction hypotheses. Using separately tagged free variables and de Bruijn bound variables makes this literal equality. Type substitution commutes with translation by structural induction; under `all` the newly bound zero remains zero on both sides and old variables are shifted once. The rigid κ case is fixed.

The target term-substitution lemma states: if `Γ,x:A,Δ ⊢ M:B` and `Γ⊢N:A`, then `Γ,Δ[N/x]⊢M[N/x]:B`. In this nondependent target Δ and B have no term indices, so the bracket notation only reindexes term variables. Induct on the typing derivation. Variable lookup either supplies N or the corresponding surviving lookup. Lambda raises the substitution under its new variable and uses the induction hypothesis; application uses both hypotheses. Universal introduction retains its side condition because N is typed in Γ and the generalised type variable is absent from Γ; universal elimination commutes with term substitution because term and type variables are disjoint. The companion type-substitution lemma substitutes simultaneously in Γ, its annotations and the result type; its universal case uses the same lifted environment square. These are separate lemmas, not an appeal to an untyped evaluation strategy.

Subject reduction follows by induction on a compatible beta contraction, using the term-substitution lemma at its root and the typing derivation under the corresponding context. In Curry presentations, universal introduction/elimination may surround the last arrow rule. Commute those outer universal rules along the contraction using the type-substitution lemma; their term-context side conditions are unchanged. Equivalently one may annotate the finite typing derivation with explicit type abstractions/applications, commute a selected erased term contraction through the finite type-redex spine, perform the typed term beta contraction, and erase again. The annotations and commute are proof artefacts, not new runtime source reductions. This gives finite subject reduction as well.

Now induct on `FiniteDerives`. I/K/S macros have precisely their arrow schemes by lambda introduction and application. Application is immediate. Source `allI` becomes target generalisation with empty term context, so its side condition is discharged. `allE` uses the type-substitution square. In the forward `reduce` case, the already supplied nonempty simulation lifts each source step to a finite target beta path; subject reduction retains the target type along that path. Thus

**N02-TYPING:** `FiniteDerives t A → ⊢F τt:T(A)`.

This ordinary typing result is not a claim that a missing System F Lean library was executed. The source SN proof below has no F-SR/F-SN hypothesis.

## N03. Positive simulation, finite and infinite paths

For an actual source step `t→u`, root I/K/S use respectively one, two and three target beta contractions. Left/right source contexts lift **all** contractions into the same target application context. In particular a step inside the second argument of `K t q` is simulated there before any K contraction; discarded arguments are not dropped from the simulation. This is a nonempty path, not a reflexive conversion.

Concatenating the selected paths gives `t→*u ⇒ τt→β*τu`, and a source path of length n produces at least n target steps. For an infinite source sequence choose the explicit path specified by each step witness. Its cumulative lengths are strictly increasing and unbounded, so their concatenation is an infinite target sequence. Alternatively accessibility reflection proves the same exclusion constructively without choosing infinite sequences: accessibility for the target relation pulls back along a map that sends every source edge to a nonempty target path. The strengthened induction predicate allows a finite target prefix before the mapped source state, exactly as in the preserved helper.

Source conversion consequently implies target beta conversion. The reverse implication remains false: `I` and `S K K` are distinct source normal forms, while their lambda translations beta-convert. None of the arguments below uses the reverse implication.

## N04. Direct source reducibility candidates — definitions

Write `SN(t)` for accessibility and `P t` for candidate membership. A source term is **neutral** when it is not one of the underapplied heads

    I, K, S, K x, S f, S f g.

Thus markers, marker-headed applications and every saturated I/K/S redex are neutral. A neutral f cannot acquire a new root redex merely by applying one more argument: every step from `f x` then comes from a step in f or x. Application of a neutral term remains neutral. These are finite syntactic case analyses of the exact grammar, not normalisation assumptions.

A reducibility candidate P satisfies:

1. `P t ⇒ SN(t)`;
2. `P t ∧ t→u ⇒ P u`;
3. for neutral t, `(∀u, t→u ⇒ P u) ⇒ P t`.

These are **not `Code` axioms**. In particular candidate membership is not closed under arbitrary backward conversion. The canonical semantic counterexample `K t Ω` is therefore not smuggled into a candidate by its reduct t. Both inert markers are in every candidate by rule 3 with no successors.

SN itself is a candidate: successor accessibility gives condition 2, and the accessibility constructor gives condition 3 even without neutrality. Nonempty intersections of candidates are candidates, taking SN from any one component; all other conditions are pointwise. The impredicative intersection used below is indexed by all candidates, which is nonempty because SN is one. No set contains itself as a runtime decoded type.

## N05. Arrow candidate, with the missing neutral-expansion obligation discharged

For candidates P,Q put `(P⇒Q)(f) := ∀x, P x ⇒ Q(f x)`.

**SN:** zero belongs to P. Therefore Q(f zero), hence SN(f zero). Any reduction of f lifts to its application with zero, so accessibility of the application implies accessibility of f. This is the elementary one-edge special case of positive simulation reflection; it can also be proved directly by accessibility induction.

**Reduction closure:** if f→g and f∈P⇒Q, then Q(f x) reduces to Q(g x) for each x∈P.

**Neutral expansion:** suppose f is neutral and all its immediate reducts belong to P⇒Q. Fix x∈P. Induct on SN(x). To prove Q(f x), use Q's neutral expansion. A reduct from f comes from some f→g, and the hypothesis gives Q(g x). A reduct from x comes from x→y; downward closure gives y∈P, and the accessibility induction hypothesis gives Q(f y). There is no new root contraction because f is neutral. This exhausts the successors, proving the arrow is a candidate. Crucially, it does not assume that every application of two SN terms is SN; that false shortcut is unnecessary.

## N06. Head expansion for each source combinator

The following lemmas are stronger and more precise than weak-head expansion.

**I:** `P x ⇒ P(I x)`. Induct on SN(x). `I x` is neutral. Its root successor x lies in P; each other successor is I x′ with x→x′, where P x′ follows by closure and the induction hypothesis applies.

**K:** `P x ∧ SN(y) ⇒ P(K x y)`. Use nested accessibility induction on x and y. At the root the successor is x. A reduction inside x gives the corresponding smaller first induction argument and P x′. A reduction inside y gives the smaller second argument. The proper K prefix has no other root rule. Neutral expansion covers every successor. SN(y) is essential: it is exactly what fails in `K t Ω`.

**S:** `SN(f)∧SN(g)∧SN(x)∧P((f x)(g x)) ⇒ P(S f g x)`. Use nested accessibility induction on f,g,x. The saturated S term is neutral. Its root successor is the assumed member. If f or g reduces, the contractum reduces in that corresponding position, so P's downward closure supplies the smaller instance. If x→x′, the original contractum reduces in **both** occurrences of x, in two compatible steps, to `(f x′)(g x′)`. This supplies the smaller-x instance. The underapplied prefixes S and S f and S f g have no additional root contractions, so the listed cases exhaust all successors.

These arguments justify recursion on the nested accessibility proofs: when an outer argument decreases the inner universally quantified arguments are reintroduced; when only the innermost decreases its accessibility induction is used. There is no circular appeal to SN of the saturated redex.

It follows that I∈P⇒P; K∈P⇒Q⇒P; and S∈(P⇒Q⇒R)⇒(P⇒Q)⇒P⇒R. For S, candidate membership supplies SN for f,g,x and supplies the contractum's R-membership by two arrow applications.

## N07. Exact impredicative finite-source theorem

Interpret type variables by candidates, primitive bottom by SN (a **normalisation-only interpretation of an inert atom**), arrows by N05 and universal types by intersection over **all candidates**. Denote this interpretation `RC(A,ρ)`. N04–N05 establish by structural recursion that it is a candidate for every type.

Renaming and simultaneous substitution commute with this interpretation. At a type variable this is lookup; at bottom the predicate SN is fixed; at arrow use the two component equalities; at `all`, quantify over the same arbitrary candidate and use the lifted-substitution equation. In particular

    RC(B[A],ρ) = RC(B, RC(A,ρ)::ρ).

Induction on the actual finite derivation proves `∀ρ, RC(A,ρ)(t)`. The I/K/S cases are N06; application is the arrow clause. Generalisation quantifies the induction hypothesis over the new arbitrary candidate. Instantiation chooses the candidate `RC(A,ρ)` and uses the substitution equation. Forward `reduce` applies downward closure along its finite path. This covers **all seven** source constructors and also accommodates inert markers in the ambient reduction grammar without giving them a typing rule.

Taking the candidate's SN component yields the unconditional ordinary theorem

**N07-SN:** `∀t A, FiniteDerives t A → StronglyNormalising t`.

The theorem is about the accepted finite derivation, not arbitrary `Derives` at a semantic Code, arbitrary membership, complete type inference or all terms in a Code. The original non-SN semantic realiser theorem remains true.

## N08. Confluence, normal forms and a complete source conversion procedure

The predecessor's complete-development proof is reused with its exact atom, congruence, I/K/S-root and duplicated-argument cases. The proof is independent of typing and of N07. Briefly, parallel reduction contracts any selected compatible redexes and reduces their arguments in parallel. Every parallel successor u of t has a parallel edge to t's complete development t★. The application case at an already saturated root must allow both contraction and congruence; the I/K/S skeleton remains visible when congruence was chosen because its partial prefixes cannot contract. At S a shared developed argument is used in both copies. The resulting diamond tiles finite paths. Ordinary one-steps embed into parallel steps, and each parallel step sequentialises into finitely many ordinary steps. Therefore the exact source `Red` is confluent.

For completeness, define `Join(t,u) := ∃v, Red t v ∧ Red u v`. It is reflexive and symmetric. Confluence proves its transitivity: join the two reducts of the shared middle term, then concatenate the outer paths. It contains each source step. Induction on `Conv` therefore gives `Conv t u ⇒ Join(t,u)`. The converse follows by converting each reduction path and reversing one. This proof does not use a nonfaithful target translation.

For a term equipped with SN, choose a root step when present, otherwise the first step in its left subtree, otherwise in its right subtree. If none exists the term is normal; this follows by inversion of the five source step constructors. Recurse on the smaller accessibility proof after every chosen step. The procedure terminates, returning a normal form n and an actual source path t→*n. If n and m are normal and convertible, joinability forces their common reduct to be n and m, hence literal equality.

Thus, given finite derivations for both inputs,

**N08-CONVERSION:** `Conv t u ↔ nf(t)=nf(u)`.

Their source types need not be the same to ask this raw-conversion question. A complete checker for the finite-source relation can verify the input certificates, normalise both terms, and compare their literal syntax. This is not a decision procedure for arbitrary raw SKI conversion or for inference of a missing impredicative typing derivation. The Python normaliser has an explicit resource bound; exhaustion returns refusal and **no** inequality verdict. Its mathematically unbounded version terminates on these certified inputs by N07.

## N09. Exact representability and conversion dispositions

The preserved Ω invariant is now combined with unconditional N07. Write D=S I I, T₀=D, Tₙ₊₁=I Tₙ and Oₘₙ=Tₘ Tₙ. Every reduct of Ω=O₀₀ has that form. A tower contraction decrements its positive index; when m=0 the outer S rule produces Oₙ₊₁,ₙ₊₁. D's proper prefixes have no redex. Every such shape has a successor, hence no reduct of Ω is normal. This exact invariant is inherited, not regenerated as a bounded experiment.

If Ω were convertible to a finitely typed u, N07 would give u a normal form n. N08's source joinability would give Ω→*n, contradicting the invariant. Therefore

**N09-NONREP:** `¬∃u A, FiniteDerives u A ∧ Conv Ω u`.

Nevertheless Ω is a canonical semantic member of bottom→bottom, because the domain is empty. Universal semantic representability modulo source conversion is conclusively false. In contrast `K t Ω≈t` when t is finitely typed, so non-SN alone does not prove nonrepresentability.

The five meanings of “conversion completeness” now have exact dispositions:

| Statement | Disposition |
|---|---|
| Source Conv implies target beta conversion | PROVED, N02–N03 |
| Target beta conversion reflects source Conv | REFUTED: I versus S K K |
| Source Conv for two finitely typed inputs is decided by their source normal forms | PROVED, N07–N08 |
| The full-compatible normaliser/checker is sound and complete on certified finite-source terms, with unbounded mathematical recursion | PROVED; bounded executable refusal is not a negative answer |
| Every canonical semantic realiser has some finitely typed representative modulo source Conv | REFUTED: Ω at primitive bottom→bottom; N09 |

The original U09 contract explicitly allows a precisely scoped conversion countermodel. Its mathematical question is therefore resolved by the positive normalisation/conversion theorems and the negative semantic-completeness theorem, not left as a vague failed reflection target. Any remaining **formal-execution** credit is recorded independently.
