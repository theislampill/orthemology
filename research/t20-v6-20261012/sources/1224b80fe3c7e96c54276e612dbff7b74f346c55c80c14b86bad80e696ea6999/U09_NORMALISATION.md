# U09 — finite-source normalisation and conversion completeness

**Disposition: PARTIAL at the obligation's requested mechanisation scope.** The preserved ordinary result is made explicit, with independently executed finite falsification probes and unverified Lean helper candidates. The full System F bridge and the SKI confluence proof have not been kernel-checked in this run. No accepted theorem or historical status is replaced.

## 1. Exact subject and preserved negatives

The verbatim obligation, source bindings, predecessor records and hashes are in `../obligations/EXACT_INPUT_OBLIGATIONS.json` and `../obligations/CONFIRMATIONS.json`. The predecessors are **V4::T13** and **V4::T14**. The governing source is the supplied main/tree, not an embedded historical instruction. The relevant source statements are `NormalisationAndNumerals.lean` and the historical mathematical proof, §5. The latter is preserved as ordinary relative mathematics, not promoted to a Lean theorem by accepted checks of nearby declarations.

Write `t → u` for the exact compatible I/K/S reduction in `OrthemologyV2.Step`; `→*` for its finite reflexive-transitive closure; and `≈` for `Conv`. Inert `zero` and `one` are atoms, not reduction rules. Source typing is exactly `FiniteDerives`, including its one-premise `allI` and forward `reduce` constructor. There are no term-context assumptions in that accepted certificate language.

The accepted negative has priority over any proposed semantic normalisation assertion. Put `D = S I I` and `Ω = D D`. The compatible cycle is

```
D D → (I D)(I D) → D(I D) → D D.
```

For every invariant code A and t∈A, `K t Ω → t`, so `K t Ω∈A`. The same term admits the cycle inside its discarded argument. It is not strongly normalising. This is not a new diagnosis and receives no new historical theorem credit here.

Three claims must remain distinct:

* finite-source typability implies strong normalisation;
* arbitrary semantic membership does not imply strong normalisation;
* absence of strong normalisation alone does not rule out a typable representative modulo conversion.

The last distinction matters because `K I Ω≈I`, whereas Ω itself has no normal form. We retain both examples rather than replacing one gate with the other.

## 2. P01-U09-01 — explicit translation and substitution squares

For proof organisation only, adjoin free term variables to the source grammar. They are inert atoms; this is a **new auxiliary syntax**, not a change to canonical closed `Term` or to `FiniteDerives`. Define the lambda translation τ by

```
τ(I) = λx.x
τ(K) = λx.λy.x
τ(S) = λf.λg.λx.(f x)(g x)
τ(M N) = τ(M) τ(N)
τ(v_i) = v_i
τ(zero), τ(one) = corresponding inert constants.
```

Names above are exposition; the executed probe uses de Bruijn bound variables and separately tagged free variables. Its beta contraction is capture-avoiding substitution with shift-in/substitute/shift-out. No beta normalisation is built into τ.

For every finite open source term t and simultaneous term substitution σ,

`τ(t[σ]) =α τ(t)[i ↦ τ(σ(i))]`.

**Proof.** For a variable both sides are the assigned translation. For an inert atom or combinator both sides are the same closed macro; inserted binders cannot capture free variables. For application use the two induction hypotheses. This exhausts the grammar. The equality is literal on the separate-free/de-Bruijn representation used by the probe. The Lean helper `P01OpenSubstitution.eval_subst` supplies an unverified candidate for the corresponding polynomial substitution/evaluation square, not the entire lambda theorem.

Type translation T preserves variables, arrow and universal binding, but maps the **primitive bottom** to a rigid fresh type atom κ. In particular κ is not a variable eligible for generalisation or type substitution. For a simultaneous type substitution σ, lift under a binder by

```
σ↑(0)   = var 0
σ↑(n+1) = rename succ (σ(n)).
```

Then `T(A[σ]) = T(A)[T∘σ]`. The induction is componentwise for arrow; under `all`, the displayed lift gives exactly the same new zero and shifted old variables on both sides. Bottom is unchanged on both sides. The existing accepted `substitute_sem` and `relSubstitute` establish interpretation squares for their stated source semantics; they are not this new System F syntactic bridge.

## 3. P01-U09-02 — positive compatible simulation

**Statement.** For every source one-step derivation `h : t → u`, there is an explicitly nonempty compatible beta reduction `τ(t) →β+ τ(u)`. A root I, K or S step uses respectively 1, 2 or 3 beta contractions. A source context step lifts that same positive sequence under the translated application context.

At the roots the actual sequences are

```
(λx.x) X → X
((λx.λy.x) X) Y → (λy.X) Y → X
(((λf.λg.λx.f x(g x)) F) G) X
  → ((λg.λx.F x(g x)) G) X
  → (λx.F x(G x)) X
  → F X(G X).
```

Capture avoidance in the display is supplied by the substitution convention above. Under a left or right context, apply the induction hypothesis inside that context. Compatibility retains every contraction: it does not replace the sequence with a reflexive conversion certificate. Induction over the `Step` derivation now covers every constructor.

This gives two additional implementation requirements. First, retain reduction witnesses, rather than comparing only normalised endpoints. Second, a source step under a K-discarded argument must still be simulated; evaluating only at weak head silently loses it.

The probe constructs paths from the source redex address. I uses address `p`, K uses `p.left,p`, and S uses `p.left.left,p.left,p`. It independently checks each adjacent pair using the lambda one-step relation. This is stronger evidence than merely observing equal end normal forms, but remains finite testing.

## 4. P01-U09-03 — relative finite-source normalisation

Here are the exact external metatheoretic inputs, stated separately rather than silently added to canonical source:

**F-SR:** subject reduction for the chosen Curry-style System F typing judgement, with a rigid type atom κ.

**F-SN:** every term typable in that Curry judgement is strongly beta-normalising.

The primary comparison is in `LITERATURE_COMPARISON.md`. The standard explicit System F normalisation proof is not, by itself, a checked Curry-erasure bridge. A later formal implementation must use a library whose judgement is exactly the target judgement, or supply the annotation/erasure lifting and subject-reduction bridge explicitly. This is the principal remaining kernel dependency, not an extra accepted axiom.

**Typing translation.** From `FiniteDerives t A`, derive `⊢F τ(t):T(A)`. Induct on the finite derivation. The I/K/S lambda macros have exactly the corresponding arrow schemes. Application uses the target application rule. `allI` uses target generalisation; the term context is empty, so no missing term-context side condition arises. `allE` uses the type-substitution square. The forward `reduce` case uses the positive simulation, its finite extension, and F-SR. Thus the exact accepted source constructors are all accounted for.

**SN reflection lemma.** For any relations r,s and map f, if

`r(a,b) ⇒ s⁺(f(a),f(b))`,

then `SN_s(f(a)) ⇒ SN_r(a)`.

A constructive proof uses accessibility induction on a target state y with the strengthened induction predicate

`∀a, s*(y,f(a)) ⇒ SN_r(a)`.

For a nonempty prefix, use the induction hypothesis at its first successor. For the empty prefix, introduce source accessibility: each source successor has a positive simulated path, whose first target step allows the induction hypothesis and whose remaining prefix is the strengthened premise. There is no conversion-to-equality reflection assumption, and no need to choose an infinite path. `P01SNReflection.lean` is an unverified candidate for exactly this generic lemma, with the simulation as an explicit parameter and no global axiom.

Combining typing translation, F-SN and positive reflection proves the **same relative ordinary T13 statement**. This packet does not turn the inherited ordinary conclusion into a fresh kernel result.

## 5. P01-U09-04 — compatible SKI confluence, including the actual overlaps

Define parallel reduction `⇒` by atom reflexivity, componentwise application, and I/K/S root contraction while all retained arguments reduce in parallel. In a K contraction the discarded argument may be reduced arbitrarily, but its choice cannot affect the result. This is a relation, not deterministic evaluation.

Define complete development t★ recursively on the strict subterms of t. If t has an I root, return the developed argument. At a K root, return the developed retained argument. At an S root with arguments f,g,x, return `(f★ x★)(g★ x★)`. At a non-redex application return the application of the developed components. Atoms are fixed.

**Triangle lemma:** `t⇒u ⇒ u⇒t★`.

A structural induction on t, with a case split on the parallel derivation, suffices. At a non-redex application only congruence is available; the two component hypotheses produce the desired parallel application. At an I root, a contracting derivation gives x′ and induction gives x′⇒x★; a congruence derivation gives I x′ and can contract with that same hypothesis. At a K root, a contracting derivation gives the developed-in-part retained argument, and a congruence derivation can contract its still-visible K root. At an S root, a contracting derivation gives `(f′ x′)(g′ x′)`; apply the three induction hypotheses, using the same `x′⇒x★` twice. A congruence derivation preserves the outer S skeleton and can contract next. Partial K and S prefixes cannot perform a root contraction of their own: this is why no additional overlap case has been suppressed.

Any two parallel successors of t therefore have the common parallel successor t★. The finite diamond-grid induction proves confluence of `⇒*`. Each ordinary source step is parallel, while every parallel step can be sequentialised: reduce the selected argument subterms first, then contract the root if that rule was used. Hence `→* = ⇒*`, and the exact compatible source relation is confluent. The inert markers add only atom cases.

Consequently convertible terms have a common reduct, and distinct normal forms cannot be convertible. These conclusions are ordinary proofs here; the bounded triangle census is not their logical justification and there is no new Lean confluence declaration.

## 6. P01-U09-05 — exact modulo-conversion countermodel

Let `T_0=D`, `T_(n+1)=I T_n`, and `O_(m,n)=T_m T_n`. D is a normal form. Every one-step successor of O_(m,n) is one of:

```
O_(m-1,n)         when m>0,
O_(m,n-1)         when n>0,
O_(n+1,n+1)       when m=0 (the outer S contraction).
```

An I contraction anywhere within a given tower produces the same decremented tower. The partial application prefixes of D have no hidden redex. These facts classify all source-step positions. Induction on a reduction sequence from Ω=O_(0,0) proves the displayed shape invariant. Every shape has a successor: decrease m when positive, otherwise contract S. Thus Ω has **no normal form**, not merely an infinite path.

The exact semantic primitive-bottom arrow is top:

`(Code.arrow Code.bottom Code.bottom).accepts t`

holds for every raw t, because there is no accepted input. In particular it holds for Ω.

Suppose Ω≈u and `FiniteDerives u A`, for any A. By the relative T13 result, u is SN and hence has a normal form n. Confluence and Ω≈u imply Ω≈n; joinability and normality of n give Ω→*n, contradicting the shape invariant. Therefore

`¬∃u A, FiniteDerives u A ∧ Conv Ω u`.

In particular there is no finite-source representative at primitive `bottom→bottom`. The statement is relative to F-SR/F-SN through T13. It does not concern another bottom encoding, an extensional quotient, or a completeness theorem restricted to a different type grammar and closure model.

## 7. P01-U09-06 — translation preserves but does not reflect conversion

Let E=S K K. Both E and I are distinct SKI normal forms, so E≉I by §5. Nevertheless τ(E) beta-reduces to λx.x=τ(I). Thus the lambda macro translation is **not conversion-reflecting**. This is an additional exact guard for future imports of lambda-calculus parametricity or completeness: a reduction simulation cannot justify replacing raw SKI equality by target beta equality.

The same pair supports the U10 identity-extension countermodel. This is an explicitly recorded local proof dependency, not an invented serial dependency on another packet.

## 8. Evidence and remaining work

`evidence/probes/census_final.stdout` records 15,764 source terms, 15,108 one-step witnesses, 21,908 checked target beta steps, 33,388 parallel pairs, 22,848 term-substitution squares and 62,208 type-substitution composition squares. Exact populations and generators are retained. No finite bound is silently extended to all terms.

Remaining work: choose and verify the exact System F formal target; formalise its typing/term/type substitution bridges and positive simulation; compile generic SN reflection; mechanise parallel confluence and the Ω shape invariant; combine them into T13/T14 at Lean 4.19.0. Definitions and theorem names must be additions on an authorised proposal branch, with all original records and negatives preserved. This research checkpoint supplies no canonical closure credit.
