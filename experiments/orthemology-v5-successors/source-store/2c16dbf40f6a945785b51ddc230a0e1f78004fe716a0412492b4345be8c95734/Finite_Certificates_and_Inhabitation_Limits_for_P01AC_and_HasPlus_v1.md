# Finite certificates and inhabitation limits for exact P01AC and Has⁺

## Results and scope

This is ordinary written mathematics about the delivered P01AC grammar and the precisely specified hypothetical Has⁺ system. It gives no executable implementation or new kernel-verification claim, and does not adopt or change any rule of the delivered calculus.

The conclusions are deliberately separated:

1. **Supplied finite certificates can be checked decidably.** A total syntactic validator exists for all current context, formation and typing rules, including the finite-import family, arbitrary finite `Red` certificates and all eight `PolyConv⁺` cases.
2. **Existence of certificates and inhabitants is semidecidable.** For finite Γ,p,A, the judgments Ctx⁺ Γ, Form⁺ Γ A and Has⁺ Γ p A are recursively enumerable. So is the relation “some p has Has⁺ Γ p A.” This is a search theorem, without a termination guarantee on negative instances.
3. **General Has⁺ inhabitation is undecidable even on an effectively presented family of formed, closed Raw identity types.** The exact many-one map is

       (t,u) ↦ identity(raw,atom(t),atom(u)).

   Its correctness is the accepted closed typed-identity characterization. The required raw-conversion undecidability premise is separately matched below to compatible weak I/K/S conversion, with closed inputs and the inert zero/one extension. Nothing here identifies weak equality with extensional or λβ equality.

4. **The unchanged P01AC already has the same solver limit on exposed endpoints.** Define Ex recursively by turning each raw primitive into its atom and each raw application into polynomial application. Section 10 proves old PolyConv(Ex(t),Ex(u)) iff raw Conv(t,u), old Raw endpoint typing, and old inhabitation of identity(raw,Ex(t),Ex(u)) iff raw Conv(t,u). Thus old Has inhabitation and fixed-witness derivability are also semidecidable and undecidable. The opaque-label converse is not transferred to old Has.

The enumeration proof applies to the unchanged P01AC by removing the bridge certificate constructor. Section 7's opaque-target reduction is for Has⁺; Section 10's separate exposed-target reduction is for unchanged Has and is valid also in Has⁺.

Earlier supplied-certificate checking for a predecessor grammar and conversion decidability on finitely typed inputs are inherited results. The contribution here is their precise current-rule boundary: complete finite encoding and enumeration, together with the two identity-target reductions. Standard computability and combinatory-logic undecidability are not discoveries claimed here.

## 1. Exact inputs and decision problems

The fixed source component is **Dependent_All_Public_Source_v2_20261003.zip**, SHA-256 `a58e2f510e08d2e2447b15b617cdb85dd1c36a3f04441a75897781c2c8f544db`. The decisive modules are AllSyntax, P01Polynomials, InternalPolymorphism, BoundaryResults, FiniteBridge, P01DependentFundamental, P01Confluence, AllPredicates, AllSoundness and P01PER. Has⁺ is defined below as a fresh mutually inductive copy with exactly one additional polynomial conversion generator.

The raw source syntax is

    t ::= I | K | S | zero | one | app(t,t).

It has no variables: every raw term is closed. `Step` has exactly I, K and S contractions and compatible left/right application contexts. `Red` has reflexivity and `tail(Step,Red)`. `Conv` has reflexivity, injection of Step, symmetry and transitivity. The constants zero and one have no reduction rules.

The polynomial syntax is `var(n)`, `atom(t)`, and application. TypeCode has `var(n)`, bottom, arrow and all. Current Ty has param(n), bottom, raw, pi, sigma, identity(A,p,q), and all. A telescope is a finite list of Ty. Natural indices are unbounded but each occurrence is a finite natural number.

Has⁺/Form⁺/Ctx⁺ copy the current 18/7/2 mutual rules. The only changes are replacing the conversion premise of identityIntro and conv by PolyConv⁺. PolyConv⁺ has the seven existing constructors plus

    bridge(r,s): atom(app(r,s)) ≈ₚ app(atom(r),atom(s)).

No extra equality of types, abstraction congruence, eta rule, semantic admission, or universal family of syntactic derivations is added.

“Checking a supplied certificate” takes a finite, fully annotated rule tree as input and asks whether it is a correct derivation of its displayed conclusion. “Derivability” takes only a finite conclusion and asks whether some certificate exists. “Inhabitation” takes Γ,A and asks whether some polynomial p and some certificate for Has⁺ Γ p A exist. Supplying Γ,p,A without a rule tree is not the first problem.

The hard inhabitation instances below all have effectively supplied formation and endpoint-typing certificates, so the lower bound is not caused by uncertainty about whether the target is formed.

## 2. Finite syntax and computable binder operations

Use a finite alphabet of constructor tags, separators and unary natural numerals. Prefix trees with tagged list delimiters give an injective, decidable encoding of every raw term, polynomial, TypeCode, Ty, telescope and finite annotated rule tree. Binary numerals would work equally well. Parsing and equality of parsed syntax are total: recursively compare tags, natural labels and corresponding subtrees. No quotient by conversion is used for these comparisons.

Every operation needed to validate a rule is computable on this syntax:

- `psub σ` replaces variable leaves and recursively traverses application; atoms are fixed. `pren r` is its renaming instance. `pup σ(0)=var(0)` and `pup σ(n+1)=pren successor(σ(n))` are computable when σ is one of the explicit substitutions needed here.
- `subst σ` fixes params, bottom and raw, substitutes both identity endpoints, uses `pup σ` in a Pi/Sigma body, and leaves σ unchanged under All. Its recursion is on the input type tree.
- `wk A`, `inst B a`, and `motiveAt B y e` use, respectively, successor variables, `a::var`, and `e::y::var`. The motive order is proof in coordinate 0 and endpoint in coordinate 1. These maps have finite descriptions, not oracle inputs.
- `arr A B=pi(A,wk B)` and the recursive finite-type embedding `fin` are computable.
- `trename` renames type parameters, lifts the renaming under All, and leaves polynomials unchanged. Thus `twk` and `twkTel` are computable.
- `mixed σ τ` uses `pup σ` and the images `wk(τ(n))` under Pi/Sigma; under All it uses σ and `tup τ=param(0)::(twk∘τ)`. Consequently `tsubst` and `tinst` are computable for the substitutions used by the rules. An evaluation of a finite type encounters only finitely many indices. The lifts have explicit index-zero/successor cases and therefore terminate.
- `typeImages τ n` is finite list lookup with bottom as default. It is not a freely supplied infinite function. `finSupport` has clauses n+1, zero, maximum and truncated subtraction by one for TypeCode variable, bottom, arrow and All. The inequality `finSupport C≤length τ` is decidable.
- `Scoped m` checks each polynomial variable index against m. `TyScoped` similarly traverses type trees, increasing term scope only under Pi/Sigma and leaving it unchanged under All. No type-parameter scope bound is added to the actual rules: `Form.param` permits every natural n.
- `freeZero`, `drop=pren predecessor`, and `abstract` are computable structural traversals. If freeZero is false, abstract returns K applied to drop; a present variable returns I; a present application returns S applied to the recursively abstracted children. No source reduction or conversion decision is used to run this compiler.
- `pairPoly`, `fstPoly`, `sndPoly` and `jPoly` are fixed finite polynomial templates. In particular `jPoly d y e` is `K(K d)y e`. `theta Γ A x` is the finite list `identity(wk A,pren successor x,var(0))::A::Γ`.

These observations do not claim arbitrary functions Nat→Poly or Nat→Ty are effectively encodable. Such arbitrary functions occur in metatheorems and semantic interpretations; they are not freely quantified data accepted by these typing constructors. Every substitution that the checker must evaluate is generated by a finite annotation, a fixed index map, and finitely many lifts.

Lookup can be checked from its two constructor tags. Zero checks precisely `Lookup (A::Γ) 0 (wk A)`; successor checks a child `Lookup Γ n A` and concludes `Lookup (B::Γ) (n+1) (wk A)`. In particular the validator does not replace Lookup with unweakened list access. Alternatively, a total recursive list lookup can compute the appropriately iterated weakened answer for n and compare it syntactically with the requested type.

## 3. Explicit reduction and conversion certificates

Every certificate node carries its constructor tag, all finite parameters needed to specify that instance, and its child certificates. It can also carry its displayed conclusion; the validator recomputes and compares it. Redundant annotations are harmless and avoid any implicit type inference.

### 3.1 Raw relations

A Step certificate has one of five tags:

1. I, with x, concludes `Step (I x) x`.
2. K, with x,y, concludes `Step (K x y) x`.
3. S, with f,g,x, concludes `Step (S f g x) (f x (g x))`.
4. Left, with child `Step f g` and x, concludes `Step (f x) (g x)`.
5. Right, with f and child `Step x y`, concludes `Step (f x) (f y)`.

Each clause consists of recursive child validation and literal syntax comparison. A Red certificate is either reflexivity at t or a Step certificate from t to u followed by a Red certificate from u to v; compare the middle endpoints. This accepts all finite compatible reductions, including right-context steps and arbitrary sequences. It is not restricted to the head-step strategy of the pre-existing example `Cert` elaborator in FiniteBridge.

Raw Conv certificates can likewise be checked under their four tags. Symmetry reverses the endpoints, and transitivity checks the middle term. There is no call to an oracle deciding whether those endpoints are convertible.

### 3.2 All eight polynomial conversion cases

The validator checks:

1. Reflexivity at p.
2. Symmetry of a checked p≈ₚq child.
3. Transitivity of checked p≈ₚq and q≈ₚr children, with literal middle equality.
4. Application congruence of checked f≈ₚg and p≈ₚq children.
5. Exposed I contraction `app(atom(I),p)≈ₚp`.
6. Exposed K contraction `app(app(atom(K),p),q)≈ₚp`.
7. Exposed S contraction `app(app(app(atom(S),p),q),r)≈ₚapp(app(p,r),app(q,r))`.
8. Bridge(r,s), with exactly the endpoints displayed in §1.

All raw and polynomial labels are finite. There is no abstraction congruence case and no semantic equality case.

## 4. All seven FiniteDerives cases

The finite-import sublanguage needs its whole derivation relation, not just a convenient subset recognized by a particular inherited executable elaborator. Its validator uses these seven cases:

1. **i(A).** Check conclusion `FiniteDerives I (A→A)`.
2. **k(A,B).** Check `FiniteDerives K (A→B→A)`.
3. **s(A,B,C).** Check `FiniteDerives S ((A→B→C)→(A→B)→A→C)`.
4. **app.** Children have conclusions `FiniteDerives f (A→B)` and `FiniteDerives x A`; compare the repeated A and conclude `FiniteDerives (f x) B`.
5. **allI.** A single child `FiniteDerives t B` concludes `FiniteDerives t (all B)`.
6. **allE.** A child `FiniteDerives t (all B)` and a finite TypeCode A conclude `FiniteDerives t (instantiateType B A)`. TypeCode substitution and its binder lift are total structural operations.
7. **reduce.** A child `FiniteDerives t A` and an arbitrary checked Red certificate from t to u conclude `FiniteDerives u A`.

The allI case has one child, even though the semantic soundness theorem later quantifies over every interpretation of its new parameter. The certificate relation adds no independent TypeCode well-scopedness restriction absent from FiniteDerives. This matters because an inherited depth-indexed convenience checker can reject some annotated raw TypeCodes without disproving that the underlying relation has a finite derivation.

## 5. Complete mutual-rule validation

Below, F(Γ,A), H(Γ,p,A) and C(Γ) denote the conclusions of recursively checked Form⁺, Has⁺ and Ctx⁺ children. All parameters are explicit finite annotations. Repeated objects and computed expressions must agree literally.

### 5.1 Two context cases

- **nil:** conclude C([]).
- **ext:** children C(Γ), F(Γ,A); conclude C(A::Γ).

### 5.2 Seven formation cases

- **param:** child C(Γ); conclude F(Γ,param(n)).
- **bottom:** child C(Γ); conclude F(Γ,bottom).
- **raw:** child C(Γ); conclude F(Γ,raw).
- **all:** children C(Γ), F(twkTel Γ,B); conclude F(Γ,all B).
- **pi:** children F(Γ,A), F(A::Γ,B); conclude F(Γ,pi(A,B)).
- **sigma:** children F(Γ,A), F(A::Γ,B); conclude F(Γ,sigma(A,B)).
- **identity:** children F(Γ,A), H(Γ,p,A), H(Γ,q,A); conclude F(Γ,identity(A,p,q)).

### 5.3 Eighteen typing cases

1. **var:** F(Γ,A) and checked Lookup Γ n A; conclude H(Γ,var(n),A).
2. **i:** F(Γ,A), F(Γ,arr A A); conclude H(Γ,atom(I),arr A A).
3. **k:** F(Γ,A), F(Γ,B), F(Γ,arr A (arr B A)); conclude the specified K typing.
4. **s:** F(Γ,A), F(Γ,B), F(Γ,C), and formation of `arr (arr A (arr B C)) (arr (arr A B) (arr A C))`; conclude atom(S) at that exact type.
5. **finite:** finite parameters τ,C,t; the decidable support inequality; exactly length τ children F(Γ,typeImages τ n), in index order n=0,…,length τ−1; one child F(Γ,tsubst (typeImages τ) (fin C)); one checked FiniteDerives t C certificate. Conclude H(Γ,atom(t),tsubst (typeImages τ) (fin C)).
6. **allIntro:** F(Γ,all B), H(twkTel Γ,p,B); conclude H(Γ,p,all B).
7. **allElim:** F(Γ,all B), F(Γ,A), F(Γ,tinst B A), H(Γ,p,all B); conclude H(Γ,p,tinst B A).
8. **rawAtom:** F(Γ,raw); conclude H(Γ,atom(t),raw) for the supplied finite raw t.
9. **rawApp:** F(Γ,raw), H(Γ,f,raw), H(Γ,a,raw); conclude H(Γ,app(f,a),raw).
10. **piIntro:** F(Γ,pi(A,B)), H(A::Γ,b,B), and the decidable check Scoped(length Γ,abstract b); conclude H(Γ,abstract b,pi(A,B)).
11. **piElim:** F(Γ,pi(A,B)), F(Γ,inst B a), H(Γ,f,pi(A,B)), H(Γ,a,A); conclude H(Γ,app(f,a),inst B a).
12. **sigmaIntro:** F(Γ,sigma(A,B)), F(Γ,inst B a), H(Γ,a,A), H(Γ,b,inst B a); conclude H(Γ,pairPoly a b,sigma(A,B)).
13. **sigmaFst:** F(Γ,A), F(Γ,sigma(A,B)), H(Γ,z,sigma(A,B)); conclude H(Γ,fstPoly z,A).
14. **sigmaSnd:** F(Γ,sigma(A,B)), F(Γ,inst B (fstPoly z)), H(Γ,z,sigma(A,B)); conclude H(Γ,sndPoly z,inst B (fstPoly z)).
15. **identityIntro:** F(Γ,identity(A,p,q)), H(Γ,p,A), H(Γ,q,A), and a checked PolyConv⁺ p q certificate; conclude H(Γ,atom(I),identity(A,p,q)).
16. **proofErase:** F(Γ,raw), F(Γ,identity(A,x,y)), H(Γ,p,identity(A,x,y)); conclude H(Γ,p,raw).
17. **j:** F(Γ,A), F(theta Γ A x,B), F(Γ,identity(A,x,y)), F(Γ,motiveAt B x atom(I)), F(Γ,motiveAt B y e), H(Γ,x,A), H(Γ,y,A), H(Γ,e,identity(A,x,y)), H(Γ,d,motiveAt B x atom(I)); conclude H(Γ,jPoly d y e,motiveAt B y e).
18. **conv:** F(Γ,A), H(Γ,p,A), checked PolyConv⁺ p q, and Scoped(length Γ,q); conclude H(Γ,q,A).

This is an exhaustive case list, not an appeal to an unspecified syntax-directed elaborator. The validator descends only into proper certificate subtrees. Computing annotations can increase syntax size, but every such computation is a terminating operation from §2. Thus validation terminates on every finite input, malformed or well-formed.

### 5.4 Why the finite-import family has a finite certificate

The source writes its third finite-import premise as

    ∀ n, n<length τ → Form⁺ Γ (typeImages τ n).

For a fixed finite τ of length k, this is equivalent to the k propositions indexed by 0,…,k−1. From the source premise, apply it to those k natural numbers and their true inequalities. From a checked list of those k derivations, any n with n<k selects the nth derivation. No derivation is needed when n≥k, since the inequality premise is then false. When k=0 the list is empty and the family is vacuous. Duplicated entries in τ still occupy distinct positions; no equality or deduplication assumption is used.

Hence this constructor has finite arity depending effectively on its finite annotation τ. It does not take a semantic family indexed by arbitrary Codes, saturated sets, functions, or valuations.

## 6. Correctness and exhaustiveness of the certificate presentation

**Soundness of validation.** Simultaneous induction on an accepted finite tree reconstructs the corresponding current derivation. Every nonrecursive side condition was directly checked. The only superficially higher-order syntactic premise is reconstructed from its finite indexed list as in §5.4. The reduction, conversion, Lookup and FiniteDerives subvalidators have the same inductive reconstruction property. Therefore acceptance certifies exactly the displayed conclusion.

**Completeness for derivability.** Simultaneous induction on Ctx⁺/Form⁺/Has⁺ derivations supplies a finite annotated tree. For finite import, its finite list of image indices yields finitely many smaller Form⁺ derivations; apply the induction conclusions at those indices and list the resulting finite certificates. Separate inductions encode the five Step, two Red, four Conv, two Lookup, seven FiniteDerives and eight PolyConv⁺ constructors. This is a statement that every derivable judgment has some finite code, not that every possible ambient proof object or higher-order presentation must have a chosen syntactic code.

The two directions establish an exact, effective finite certificate presentation of the current mutually inductive judgments. Neither direction decides an unprovided conversion premise. Conversion proofs are part of certificates.

**Enumeration.** Enumerate all strings over the finite encoding alphabet by increasing length, and lexicographically within each length. Parse and validate each; output the conclusions of accepted trees. Each length contains only finitely many strings, every check terminates, and every finite certificate is eventually visited. Thus every derivable conclusion is eventually output and no false conclusion is output. Unbounded natural indices, raw labels, substitutions generated from lists, proof height and reduction length are all accommodated by the unbounded string enumeration.

For a fixed finite judgment, halt when its identical conclusion is output. For inhabitation at Γ,A, halt when an accepted conclusion has form H(Γ,p,A) for any p, returning that p and its certificate. One need not first enumerate p separately. This gives semidecision procedures both for fixed-term derivability and for existence of an inhabitant. It does not provide negative certificates or a computable cutoff after which an unsuccessful search may safely answer “no.”

Semantic All interpretation has an unrestricted universal quantifier. None of the algorithms enumerates semantic interpretations or decides membership in them. All formation and both typing introductions remain the finite cases listed above. The semantic universal quantifier in soundness does not turn their syntax into an infinitary rule.

## 7. The exact Raw-identity many-one reduction

Write Inh⁺(A) for `∃p, Has⁺ [] p A`. For every pair of finite raw terms t,u, define

    R(t,u) = identity(raw,atom(t),atom(u)).

This finite output is effectively constructed. More importantly, it comes with effective current derivations:

- Ctx⁺ [] by nil;
- Form⁺ [] raw by raw;
- Has⁺ [] atom(t) raw and Has⁺ [] atom(u) raw by rawAtom;
- Form⁺ [] R(t,u) by identity formation with those two endpoints.

The atoms are Scoped 0, and literal evaluation at zeroEnv gives t and u. The closed typed-identity characterization in the companion proof *Intensional Identity Separation and Closed Identity Conversion*, applied with A=raw, therefore gives

    Conv(t,u)
      ⇔ Has⁺ [] atom(I) R(t,u)
      ⇔ Inh⁺(R(t,u)).

The forward implication uses the closed PolyConv⁺ characterization followed by identityIntro. The converse holds for every possible typing derivation of every possible inhabitant, by the companion proof's all-rule saturated interpretation. It is not merely inversion of the final identityIntro constructor.

Consequently any total algorithm deciding Inh⁺ on these formed closed targets would decide raw Conv on arbitrary finite raw input pairs. The same reduction proves undecidability of the fixed-witness derivability problem `Has⁺ [] atom(I) R(t,u)`. This does not contradict decidable checking when its entire derivation is supplied.

## 8. Separately warranted raw-conversion premise

### 8.1 The imported representation premise

Hindley and Seldin's representation theorem supplies, for every partial recursive h, a closed pure I/K/S term F with F N(n)=w N(h(n)) when h(n) is defined and with no weak normal form otherwise. Here B=S(KS)K, N(0)=KI and N(n+1)=SB N(n); =w is finite conversion generated by I x→x, K x y→x and S f g x→f x(g x) in arbitrary application contexts. This is weak conversion, without eta or abstraction congruence. See [M1], Definitions 2.9, 2.29, 4.2 and 4.5; Notation 4.1; Theorem 4.23.

### 8.2 Closed inputs, without a false translation-reflection claim

Here is the short computability deduction that makes closedness explicit. Let H be an ordinary undecidable recursively enumerable set of natural numbers, for example the set of coded machines that halt on their coded input. Its partial characteristic function h is zero when the coded finite computation eventually halts and undefined otherwise. It is partial recursive: check bounded computation histories and perform unbounded search for a halting history. Equivalently, h is the composition of the constant-zero function with minimization of the primitive-recursive bounded-halting test.

Apply §8.1 to this h and fix the resulting F. The displayed recursion for N is effective, and its base KI is visibly a weak normal form. Then:

- If n∈H, F N(n) is weakly convertible to N(0).
- If n∉H, F N(n) has no weak normal form. If it were weakly convertible to N(0), Church–Rosser for precisely this compatible I/K/S relation would give a reduction to the normal form N(0), a contradiction. Here confluence is also the inherited P01Confluence result restricted to pure inputs.

Thus n↦(F N(n),N(0)) is an effective map from H to conversion of **closed pure I/K/S terms**. The finite term F is fixed; constructing N(n) and the application is effective. No term is asked to inspect unencoded syntax, no unproved internal quote/evaluator is postulated, and no λ-to-SKI equivalence-reflection theorem is used. The representation premise is imported explicitly; this deduction does not infer it from a bracket beta lemma.

### 8.3 Inert zero and one do not change pure I/K/S conversion

Let E send the raw constants zero and one to I, fix I,K,S, and commute with application. This is a computable retraction from the exact five-constant raw syntax to pure I/K/S syntax.

Induction on the five Step cases shows that `Step t u` implies a pure I/K/S step `E(t)→E(u)`: root I/K/S rules remain those same rules, and compatible contexts remain compatible contexts. No case contracts zero or one, because the source has no such case. Induction on Conv then gives

    Conv_raw(t,u) ⇒ Conv_pure(E(t),E(u)).

For pure inputs E fixes both terms; the other implication is the inclusion of pure certificates into the larger grammar. Therefore raw conversion on pure inputs is exactly pure weak conversion, even though a conversion chain may introduce extra constants through reversed discarded-argument contractions.

If the cited pure CL presentation allows variables in intermediate conversions, that also does not alter the closed subproblem: replace every such variable by I throughout its finite chain. Substitution preserves I/K/S contractions and contexts, and fixes closed endpoints. Conversely, closed chains are already permitted in the presentation with variables.

Hence the undecidable closed pure subproblem remains undecidable in this exact raw syntax. This is a genuine conservativity argument for added inert constants, not an assumption that a larger relation automatically preserves a lower bound.

### 8.4 Scope of the resulting limit

Combining §§6–8 proves that Has⁺ inhabitation is semidecidable and undecidable, already on the formed closed Raw identity targets R(t,u). No complexity-completeness label is needed or claimed. In particular, mere recursive enumerability plus undecidability would not alone justify such a label.

Nonnormalization by itself, the presence of Ω, and the non-reflecting SKI-to-λ macro translation would not establish this result. The inherited typed-input normalization and decidability results do not decide arbitrary raw endpoints admitted by rawAtom. Neither All nor dependent function inhabitation is needed to manufacture these target types, although the noninhabitation direction applies to all rules an attempted proof might use.

## 9. Mathematical dependencies and limits

The argument is relative to the exact delivered source component, the stated Has⁺ definition, and the companion closed identity characterization. Section 10 additionally uses the delivered AllPredicates and AllSoundness directly. The complete case inspection proves that a mathematical validator exists; no parser, implementation, extraction theorem, runtime complexity bound or verified executable is supplied. No source or model was executed for this result.

Without §8.1's imported premise, §§1–7 still establish exact finite checking, enumeration and a conditional many-one reduction. With that premise and the explicit relation matching in §8, the undecidability conclusion follows. No theorem about arbitrary extensions, arbitrary semantic validity or the old F/G equality relation is inferred. The unchanged Has inhabitation consequence receives its own exposed-endpoint proof below.

## 10. Unchanged P01AC and exposed Raw identities

The unchanged current P01AC already has undecidable inhabitation and undecidable fixed-witness derivability on effectively formed closed Raw identity targets whose endpoints are fully exposed polynomials. The hypothetical atom/application bridge is unnecessary for this family. It remains necessary for the previously stated proof of the corresponding characterization with arbitrary whole raw terms used as opaque atom labels.

### 10.1 An effective exposure map

For each raw source term t define a polynomial Ex(t) by structural recursion:

    Ex(I) = atom(I),  Ex(K) = atom(K),  Ex(S) = atom(S),
    Ex(zero) = atom(zero),  Ex(one) = atom(one),
    Ex(app(f,a)) = app(Ex(f),Ex(a)).

There are no raw variables. Thus Ex is a total computable operation on finite syntax. Structural induction proves, for every valuation η,

    eval(Ex(t),η) = t,
    Scoped 0 Ex(t).

For a primitive constant the evaluation equality is the atom clause and scope is True. For application use the two induction equalities and the two scope conjuncts.

The unchanged nil and raw formation rules give Ctx [] and Form [] raw. Structural induction on t then constructs **old** Has [] Ex(t) raw: primitive constants use rawAtom; application uses rawApp with the two induction derivations and Form [] raw. In particular this proof never asks for FiniteDerives t C, and works for arbitrary raw t.

### 10.2 Exact old conversion on exposed polynomials

**Lemma.** For all raw t,u,

    Conv(t,u) ⇔ PolyConv(Ex(t),Ex(u)),

where PolyConv is the unchanged seven-constructor relation.

For the forward direction first induct on the exact five Step cases:

- **I:** Ex(I x)=app(atom(I),Ex(x)); the existing polynomial I constructor concludes its conversion to Ex(x).
- **K:** Ex(K x y)=app(app(atom(K),Ex(x)),Ex(y)); the existing K constructor concludes its conversion to Ex(x).
- **S:** Ex(S f g x)=app(app(app(atom(S),Ex(f)),Ex(g)),Ex(x)). The existing S constructor gives app(app(Ex(f),Ex(x)),app(Ex(g),Ex(x))), which is literally Ex(f x (g x)).
- **Left context:** from the induction certificate Ex(f)≈ₚEx(g), use application congruence with reflexivity at Ex(x). Its endpoints are literally Ex(f x), Ex(g x).
- **Right context:** use reflexivity at Ex(f) and the induction certificate Ex(x)≈ₚEx(y), again under application congruence.

Next induct on the four raw Conv constructors: reflexivity, Step injection using the preceding lemma, symmetry and transitivity use the corresponding old PolyConv constructors. This covers every compatible reduction and every finite conversion chain; it assumes no normalization.

For the reverse direction apply the unchanged `polyConv_sound` theorem at any η. The evaluation equalities from §10.1 change its endpoints to t and u. This proof is equality reflection for the **specific exposure map Ex into old polynomial conversion**, not for the non-reflecting SKI-to-lambda map. No abstraction is involved.

### 10.3 Formed old identity targets and exact inhabitation

Define the effective target

    T(t,u) = identity(raw,Ex(t),Ex(u)).

Old identity formation, with the Raw derivations from §10.1, gives Form [] T(t,u). The target has no free term or type variables. Its formation certificate is effectively constructed from t,u.

Then the following propositions are equivalent:

1. Conv(t,u).
2. Has [] atom(I) T(t,u), in the **unchanged** current calculus.
3. There exists p such that Has [] p T(t,u), again in the unchanged calculus.

**1⇒2.** The conversion lemma gives old PolyConv Ex(t) Ex(u). Apply old identityIntro with this certificate, the old identity formation, and the two old Raw endpoint typings.

**2⇒3.** Choose p=atom(I).

**3⇒1, directly in the old delivered interpretation.** Let ζ be zeroEnv and choose any lawful old type environment ρ, for example the constant Raw PER environment. The empty-context relation E([],ρ,ζ,ζ) is the pair of literal equalities ζ=zeroEnv, so it holds by reflexivity. Given Has [] p T(t,u), `AllSoundness.unary_fundamental` gives

    F(T(t,u),ρ,ζ,eval(p,ζ),eval(p,ζ)).

The exact `AllPredicates.F_identity` equation makes its first conjunct

    F(raw,ρ,ζ,eval(Ex(t),ζ),eval(Ex(u),ζ)).

The exact `F_raw` equation identifies this with raw Conv(eval(Ex(t),ζ),eval(Ex(u),ζ)). The structural evaluation equalities of §10.1 conclude Conv(t,u).

This proof depends on the delivered all-rule soundness theorem for old Has and its existing F clauses at Raw and identity. It uses neither the hypothetical bridge nor the new saturated interpretation. It does not generalize F(A) to raw Conv for arbitrary carriers A: it unfolds only F(raw), where the source explicitly defines that relation to be raw Conv. Nor does it invert the final typing rule; all typing constructors are already covered by the inherited soundness theorem.

For comparison, a second valid route embeds the old derivation into Has⁺ and applies the companion closed typed-identity characterization to Ex(t),Ex(u). The direct route above avoids this additional dependency.

### 10.4 Decision consequence and separation of endpoint representations

The exact many-one reduction for **old Has** is (t,u)↦T(t,u). A total inhabitation decider restricted to these supplied formed closed targets, or a total derivability decider for the fixed witness atom(I) at these targets, would decide unrestricted raw Conv. Section 8 therefore implies undecidability of both problems. Sections 2–6 apply unchanged, so old Has inhabitation remains semidecidable.

For Has⁺ there are two valid hard families: these exposed endpoints and §7's opaque endpoints identity(raw,atom(t),atom(u)). For unchanged Has, this section proves the exposed family only. It does not assert that old PolyConv identifies Ex(t) with atom(t), nor that an arbitrary old inhabitant transports to the opaque target. The absence of that bridge is fully respected.

The distinction is operationally important: general solver limits already occur in the unchanged delivered calculus; the hypothetical bridge additionally lets the same raw-conversion problem be carried by opaque labels. This is a source-specific mathematical consequence, not a new implementation or a general theorem about every extension of the calculus.

## References and source access

**[M1]** J. Roger Hindley and Jonathan P. Seldin, *Lambda-Calculus and Combinators: An Introduction*, Cambridge University Press, 2008. Relevant locators: Definitions 2.9 and 2.29, pp. 24 and 29; Notation 4.1 and Definitions 4.2 and 4.5, pp. 47–49; Theorem 4.23, pp. 58–59. [Publisher chapter record](https://www.cambridge.org/core/books/abs/lambdacalculus-and-combinators/representing-the-computable-functions/CCD505D1E0E0EA4D93412C26CED28B56), DOI 10.1017/CBO9780511809835.005.

The numbered text was read in a [359-page mirror copy](https://anggtwu.net/tmp/hindley_seldin__lambda-calculus_and_combinators_an_introduction.pdf), retrieved 4 October 2026, SHA-256 `a36207146f72eeca9088bd389c5df44b6379ec3facdf32b620fd47e9fe80d7e8`. The publisher record corroborates bibliographic identity; publisher-hosted full-text byte equality was not verified. The mirror PDF is not included with this proof.

**Companion result.** [Intensional Identity Separation and Closed Identity Conversion](Intensional_Identity_Separation_and_Closed_Identity_Conversion.md), especially the all-current-rule saturated soundness theorem and the closed typed-identity characterization. The opaque-target argument uses those results; the unchanged exposed-target necessity proof instead uses the delivered AllSoundness and AllPredicates directly.
