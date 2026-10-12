# U11 — contextual dependence, J and the abstraction-congruence obstruction

**Disposition: PARTIAL, with an ordinary counterexample to the proposed direct full-calculus bridge.** The packet supplies a tracked contextual substitution core, a coherent based-J lemma, Sigma eta at its actual encoded scope, and a precise universe boundary. It does **not** call these a complete dependent calculus. The ordinary beta-under-abstraction congruence requirement fails for the two bracket compilers examined, even though their application-level beta law holds.

## 1. Exact inherited boundary

The obligation's predecessors are **V4::T23**, **ARGUMENT::INTERNAL-ALL** and **ARGUMENT::SCUU-AT**, with concepts A4C-C041–C044. Exact source records and hashes are preserved separately. The active mapped 4.19.0 source includes coherent Pi/Sigma/equality constructions and the exact operational `SCUUAt` extraction. These accepted results are not weakened or reclassified by their older embedded “uncompiled” comments.

Canonical types are step-invariant predicates on finite SKI programs, with `El A` retaining the raw program. `dependentPi A B` admits f when every accepted x is sent to an accepted result in B(x). `dependentSigma A B` admits z when it is convertible to the encoded pair of some accepted x and y. `equalityCode A x y` admits p exactly when x,y∈A, x≈y and p≈I. The source's `equality_transport` has a coherent **one-coordinate family**; that is not a full proof-dependent J theorem.

The accepted internal All remains in the same semantic Code universe, retains one common underlying program, and allows self-instantiation. No proposal here replaces it with only an external metalinguistic quantifier. Conversely, none of these constructions admits arbitrary ambient sections or supplies an object universe `U` with unrestricted `El U = Code`.

## 2. P01-U11-01 — a contextual tracked core, stated without a full-calculus claim

A context is a finite telescope. Its valuations are tuples γ=(t₁,…,tₙ), with each tᵢ accepted by its type evaluated on the preceding tuple. Valuations are equivalent when corresponding components are related by canonical Conv. Each type family is coherent: equivalent admissible valuations give the same acceptance predicate. This coherence makes telescope membership independent of the chosen equivalent representatives, by induction on the telescope length.

For a context Γ, define a contextual type A to be a Code-valued family A(γ) coherent in this sense. A represented term is **one finite open SKI polynomial** e with a proof

`∀γ∈Val(Γ), e[γ] ∈ A(γ)`.

It is not an arbitrary function γ↦Term, and it cannot branch on a hidden code argument. Constants, variables and application form the auxiliary grammar. Equality of represented terms is pointwise Conv at all admissible valuations. This is a semantic equality relation, not a decision procedure or a replacement definition for canonical Conv.

A substitution σ:Δ→Γ is a finite tuple of represented terms satisfying the telescope's successive typing obligations. At a valuation δ it produces the admissible tuple σδ. Put

`A[σ](δ)=A(σδ)`, and `e[σ]` equal to simultaneous polynomial substitution.

**Substitution theorem.** Evaluation satisfies

`eval_δ(e[σ]) = eval_(σδ)(e)`

as literal raw terms. Variable and constant cases are immediate; application uses the two induction hypotheses. Consequently typing reindexes along σ. Identity and composite substitutions satisfy

```
e[id] = e,
(e[σ])[τ] = e[σ∘τ],
A[id] = A,
(A[σ])[τ] = A[σ∘τ]
```

pointwise, with `(σ∘τ)(i)=σ(i)[τ]`. The type equations follow from the displayed evaluation equality, not from assuming an unproved substitution principle for dependent syntax. The candidate `P01OpenSubstitution.lean` isolates the finite polynomial equations.

Application is congruent under pointwise Conv because canonical Conv is an application congruence. Equivalent substitutions therefore give equivalent evaluations of a fixed polynomial and equivalent reindexed type predicates. Context extension has the projection deleting the final component and the new-variable term selecting it. Pairing a substitution with a term gives a substitution into an extension; the projection/new-variable equations follow componentwise. These establish a semantic tracked context/substitution core.

**Limit.** This construction has not specified a finite syntax for all coherent Code-valued families. Membership in such a semantic family is not automatically decidable. The core is not advertised as a full CwF with Pi abstraction, a syntactic dependent type theory, or an executable checker.

## 3. P01-U11-02 — application-level bracket beta is valid

For a distinguished variable x, use this explicitly specified non-eta bracket compiler:

```
[x]x       = I
[x]e       = K e                       if x is not free in e
[x](u v)   = S ([x]u) ([x]v)           otherwise.
```

The variable-free optimisation is part of the proposal, not a change to any accepted source definition. It makes the compiler natural under substitutions for other variables whose values do not contain x: a variable-free subtree remains variable-free and stays inside its K wrapper. Substitution for x itself is handled by the beta statement instead.

**Tracked beta lemma.** For every finite body e and every argument a,

`([x]e) a →* e[a/x]`.

For e=x use I. For an x-free e use K. For a remaining application, first contract S, giving `([x]u)a (([x]v)a)`, then lift the two inductively constructed sequences into its left and right contexts. This is a concrete sequence proof and allows repeated occurrences of x. Closing any other free variables preserves all its source steps.

If the body is accepted by the dependent fibre at every accepted x, the compiled function lies in the existing dependentPi code, by the beta lemma and code stability. This supplies a tracked representative for that particular body. It does not yet show that choosing another equal body gives an equal function representative.

## 4. P01-U11-03 — beta congruence under abstraction fails

A conventional judgemental equality with beta and lambda congruence must infer

`λx.(I x) ≡ λx.x`

from the body step `I x → x`. This is a beta-plus-congruence obligation, **not merely Pi eta**.

The bracket compiler in §3 sends the two sides to

```
[x](I x) = S (K I) I,
[x]x     = I.
```

Both are distinct normal forms for the exact compatible SKI relation. By U09's ordinary confluence proof they are not convertible. Nevertheless applying either to any a reduces to a. Thus the beta lemma in §3 is true while the body-congruence implication

`e≈e′ ⇒ [x]e≈[x]e′`

is false. In the contextual core, e=I x and e′=x represent the same body class, but abstraction sends them to different result classes. **Abstraction therefore does not descend to the proposed quotient of represented terms.** A complete contextual Pi model cannot be claimed from this construction.

The witness is not an artefact of untyped or empty-domain examples. In context x:α, I has type α→α and both bodies have type α; interpreting α by an inhabited code gives the same failure. The two closed compiled functions have the corresponding simple arrow type.

### An eta shortcut does not discharge the gate

Consider the separately specified usual shortcut `[x](f x)=f` for x-free f, in addition to the variable-free K case. It fixes the first witness but not the general obligation. The body equation `K x I → x` yields

```
[x](K x I) = S K (K I),
[x]x       = I.
```

These too are distinct SKI normal forms. This is an independent counterexample to abstraction congruence for the eta-optimised variant. The executable test retains both witnesses.

These counterexamples refute the **two stated translation proposals**, not every possible dependent calculus or every possible abstraction representation. A new lambda-algebraic model, an extensional quotient, a conversion-respecting elaboration, or another representation might supply the missing law. Each requires its own theorem and source/interface comparison. Fixing a finite witness, or merely changing the reduction strategy, is not that theorem.

No accepted gate is weakened by omitting congruence, restricting equality without review, or renaming the resulting fragment a full calculus. The full U11 target remains open. This is the main negative result of this round.

## 5. P01-U11-04 — dependent application and Sigma rules at exact scope

The contextual core reindexes existing coherent families pointwise. For A over Γ and B over Γ.A, Pi and Sigma membership are the pointwise canonical predicates. Their coherence follows from coherence of A,B and code stability; no arbitrary untracked section is introduced. To match the total `CoherentFamily` API, extend B(γ,x) by bottom outside the accepted domain A(γ). Equivalent raw x values cannot cross this boundary because A is invariant. On accepted inputs use the given contextual fibre. This is a metatheoretic totalisation of a coherent family, not a program that inspects its input code.

Dependent application uses the existing `dependent_application_conversion`: when f≈g and x≈y, `f x≈g y`; acceptance transports inside B(x), then coherence transports it to B(y). This is valid independently of the failed abstraction-congruence law.

For Sigma, retain canonical `pairTerm`, `firstTerm` and `secondTerm`. The existing pair computation/projection lemmas give the beta equations. There is also an ordinary **Sigma eta on actual encoded inhabitants**:

`z∈Sigma(A,B) ⇒ pairTerm(firstTerm z)(secondTerm z)≈z`.

Choose the witness x,y with z≈pair(x,y). Projection congruence and pair beta give `first z≈x` and `second z≈y`. Congruence of the fixed pair polynomial gives `pair(first z,second z)≈pair(x,y)≈z`. This does not use function extensionality or Pi eta. `P01CoherentJ.sigma_eta` is an unverified candidate for this exact statement.

A dependent Sigma eliminator may therefore evaluate its branch at the two projections and transport the motive along the displayed pair eta conversion, **provided the motive is coherent**. This is a semantic admissibility argument; a finite syntactic eliminator and its substitution theorem are still later work.

## 6. P01-U11-05 — coherent, proof-dependent based J

Fix a code A and x∈A. A proposed based motive consists of a Code `C(y,p)` for y∈A and p∈Id_A(x,y), with the explicit condition:

Whenever both (y,p) and (z,q) are admissible and y≈z, p≈q, membership in C(y,p) and C(z,q) agrees for every result term.

This is **a new, separately stated two-coordinate coherence hypothesis**. It is not silently attributed to the source's one-coordinate `CoherentFamily`.

**Based-J theorem.** If `p∈equalityCode A x y` and `d∈C(x,I)`, then `d∈C(y,p)`.

From equalityCode's exact definition we obtain x≈y and p≈I. Reflexivity gives the admissible base (x,I). Hence (x,I) and (y,p) are equivalent in both coordinates; motive coherence transfers membership of d. There is no induction over a fictional syntactic proof object and no use of `Conv` as Lean's equality.

A tracking term is

`J_rep(d,y,p) = K (K d) y p`.

It reduces in two K steps to d. Stability of C(y,p) therefore gives `J_rep(d,y,p)∈C(y,p)`. At y=x,p=I, the same finite reduction gives the based computation equation. The four candidates `based_J`, `j_reduces`, `tracked_based_J` and `j_beta` specify this precisely in `P01CoherentJ.lean`.

For an unfixed x, use a branch d(x) and require the motive to be coherent in the surrounding valuation and x as well. Reindexing then follows from the polynomial substitution theorem and motive coherence. This is a conditional extension of the semantic construction, not an implemented general dependent syntax.

### P01-U11-06 — arbitrary proof-inspecting motives are refuted

Take A=top, x=y=I, and p=I I. Then p≈I, so p is accepted by equalityCode. Let C(y,q) be top when q is **syntactically** I and bottom otherwise. The base fibre C(I,I) is inhabited, but C(I,I I) is empty. No J operation can send every base inhabitant to that empty fibre.

This motive is not coherent in the proof coordinate. The witness shows that dropping the new hypothesis makes the proposed based-J extension false. It generalises the preserved warning about incoherent endpoint families without reclassifying the accepted `equality_transport` theorem.

Nothing here asserts a full identity-type eliminator with arbitrary motives, a decidable conversion procedure, equality reflection in the object syntax, or a new UIP axiom. The concrete semantic identity code has its own collapsed proof representations, and the rule is restricted exactly as stated.

## 7. P01-U11-07 — code formation, internal All and the exact excluded universe closure

A proposed syntax must distinguish a **code judgement** from a **program judgement**. A type parameter ranges over the accepted Code universe C; a program term has a finite common tracker. Formation may include type variables, primitive bottom, coherent Pi/Sigma/Id constructors and `All α.B`. These are grammar/formation proposals, not claims that all coherent semantic families have finite syntax.

For All, the unchanged semantics is

`All(B).accepts t ⇔ ∀X∈C, B(X).accepts t`.

It is a code in the same C. A finite type-generalisation rule must keep the term tracker unchanged and use type weakening for every open term assumption. Instantiation uses an actual code, including All(B) itself when appropriate. This preserves legal internal self-instantiation; it does not weaken All to a finite family or to an external-only object.

The following additional capability is **not supplied**:

* an object universe whose decoded elements are every ambient Code or every ambient type at the same level;
* a packing of every unrestricted dependent ambient section into one small decoded carrier, with total unpacking and the specified beta law.

The exact source `HurkensBoundary.no_self_product` assumes a family `decode:C→Type`, a code c, and

```
GirardFamily(decode,x)
  = (DPred(decode x) → decode x) → DPred(decode x),
DPred X = (X → Prop) → Prop,

pack   : ((x:C) → GirardFamily(decode,x)) → decode c,
unpack : decode c → ((x:C) → GirardFamily(decode,x)),
beta   : ∀f x, unpack(pack f) x = f x.
```

It concludes False. The operational `SCUUAt` uses `C=Type r` and identity decoding, with its explicit lifts: at a fixed operational state there are exported pack/unpack handles, packTotal for **every FullSections value**, unpackTotal for every small value, and returnedBeta preserving the actual returned values. The accepted proof extracts the retraction by Classical.choice and invokes the exact no-self-product theorem.

A finite represented term is not a packer for every FullSections function. A common-program All section is not such a packer either. Therefore internal All and the tracked contextual core do not supply the antecedent. This preserves the accepted positive/negative conjunction; it does not change the SCUU hypotheses to make an easier theorem.

A separate predicative Tarski hierarchy, a PER universe, or a two-decoder model could be proposed later, but none is adopted here. Its level constraints, decoding, closure and exact relation to existing C would require review. The programme's owner-policy and publication/licensing boundaries are not mathematical variables to choose for convenience.

## 8. What a later implementation must actually decide and prove

A finite syntax proposal needs explicit context and type-parameter telescopes, lifting substitutions in both sorts, formation derivations for dependent families, Pi/Sigma/Id introduction and elimination, and a judgemental equality definition. Its equality must include the intended congruence rules. The chosen compiler/interpretation must then prove those rules sound; the two counterexamples must remain negative tests for unsuitable bracket backends.

One route is a new conversion-respecting representation with a checked translation back to the accepted interface where valid. Another is a deliberately weaker, separately named tracked certificate language with explicit computational witnesses. The latter may be useful, but cannot close the full-calculus gate by changing its name or requirements.

A sound terminating verifier for a finite supplied derivation would not imply complete type inference or decidable semantic conversion. No such verifier is implemented in this packet. Source typing under Pi binders and relation transport under dependent J also cannot be inferred from the closed finite System F normalisation argument.

The positive local substitution/J/Sigma results and the failed abstraction bridge are separated in the handoff. Formal candidates remain unverified. U11 therefore receives a precise PARTIAL result, not a full-calculus PASS and not a claim that the target is impossible.
