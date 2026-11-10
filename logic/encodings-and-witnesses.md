# Impredicative Encodings, Typed Identity and Proof Witnesses

## Status and scope

This is a proposed scholarly exposition of public mathematical results already developed in Orthemology. It reconciles their positive constructions, later corrections and countermodels. It does not change an accepted paper, adopt a proposed calculus, or establish a metaphysical conclusion. The results concern particular finite syntactic judgments and explicitly defined interpretations. Their strongest conclusions require keeping those objects fixed.

The central example is elementary to state. One compiler turns the arithmetic expression $`x`$ into the identity combinator. The same compiler turns $`x+0`$ into a program that iterates a pair of counters and projects the answer. The programs agree on Church numerals. Does the proof calculus identify them as functions on its impredicative natural-number type?

The answer depends on what “identify” means. Raw conversion, an inhabitant of a typed identity, equality in a chosen interpretation, and acceptance by an arithmetic certificate checker are different relations. For the extensional calculus studied here, the exact function identity has no proof, and its internal negation has no proof either. Nevertheless it is valid in a sound full-PER interpretation. Every particular closed, already typed Church input has the expected scalar identity; closed Church identities are even decidable once their typings are supplied. These facts are compatible because a theorem for each supplied closed derivation is not a single proof over a bound variable.

This chapter gives the proofs, including the concrete countermodel and the closure properties that make it a model of the whole calculus. Historical source and formal-verification citations support exact inspection; they are not substitutes for the arguments below.

Section 10 compares these extensional results with the original and bridge-only judgments. It proves the earlier representation boundary and full-rule intensional identity criterion, retaining the different preservation conditions of each calculus.

## 1. Erased terms and the identity judgment

### 1.1 Application, conversion and abstraction

Application associates to the left. Raw terms are finite application trees over the combinators $`I,K,S`$ and two inert constants. The inert constants are not the Church numerals defined below. The computational rules are

```math
Iu\longrightarrow u,
\qquad Kuv\longrightarrow u,
\qquad Sfgu\longrightarrow fu(gu).
```

Reduction is closed under application on either side. Conversion, written $`u\simeq v`$, is its reflexive, symmetric and transitive closure. No unrestricted function extensionality or eta rule is part of raw conversion.

An open *polynomial* contains variables, raw-term atoms, and application. Packing an entire raw application inside an atom and writing it as an application of two atoms give different polynomial trees. The extensional calculus uses the conversion relation $`\simeq_+`$ that contains the combinatory equations, congruence, equivalence closure, and the packing equation

```math
\mathrm{atom}(uv)
\simeq_+
\mathrm{atom}(u)\mathrm{atom}(v).
```

This last equation preserves the original raw expression. It permits reifying an interpreted raw application back into the corresponding polynomial. It is not a rule identifying all semantically equivalent programs.

We write $`[x]b`$ for the actual bracket abstraction algorithm. It first checks whether $`x`$ occurs anywhere in $`b`$. If it does not, it returns $`Kb`$, with the appropriate lowering of free-variable indices. Otherwise,

```math
[x]x=I,
\qquad [x]\bigl(uv\bigr)=S([x]u)([x]v).
```

The absence test has priority over decomposition. In particular, a whole application independent of $`x`$ is kept beneath one $`K`$; it is not expanded into an eta-equivalent alternative. Structural induction proves

```math
([x]b)a\simeq_+ b[a/x].
```

The absent-variable case uses $`K`$, the variable case uses $`I`$, and the application case uses $`S`$ followed by the two induction hypotheses. All lambda notation below abbreviates this algorithm. Thus a displayed program denotes a specific polynomial, not merely a choice of extensionally equivalent implementation. The formal source proves this abstraction equation for arbitrary semantic arguments as well as source terms. [Abstraction and compiler source][compiler]

P01Polynomials supplies a stronger syntax-level compatibility for this particular compiler. Its abstraction tests whether the entire subterm omits the fresh variable before decomposing an application. The absent-variable/drop lemmas then yield literal abstraction_naturality under lifted capture-avoiding substitution, not merely equality after semantic evaluation. The separate beta theorem is a compatible reduction after application, and the applied substitution square yields conversion. These statements do not license eta contraction, normalization of an arbitrary body or conversion congruence of two un-applied abstractions. The literal equality depends on the chosen whole-subterm K-priority algorithm and its precise lift; the source explicitly labels itself uncompiled. [A750-T50-140](../research/t20-v6-20261012/sources/c79a594c05a4a9ef0e77a7f5b539a0feac278aa20cfbd04f63d59163c8626462/P01Polynomials.lean#L56-L152) [A750-T50-140](../research/t20-v6-20261012/sources/c79a594c05a4a9ef0e77a7f5b539a0feac278aa20cfbd04f63d59163c8626462/P01Polynomials.lean#L154-L194)

Normalizing the body first breaks that literal substitution square even in a small open example. Let p=y x, abstract x, and substitute I for the older variable y. Before substitution p is normal, so normalize-then-bracket produces S(K y)I, whose substituted result is S(K I)I. Substituting first gives I x, which normalizes to x and abstracts to I. The two resulting unapplied terms are distinct source normal forms; source confluence therefore excludes raw conversion between them. The nonnormalizing whole-subterm K-priority compiler instead yields S(K I)I along both routes. This is a newly spelled-out witness in the negative register, not recovery of its missing historical executable log. It distinguishes capture-avoiding substitution from arbitrary body conversion and does not withdraw the unchanged compiler's positive naturality theorem. [AFTER3384-SECOND25-026](../research/t20-v6-20261012/sources/0672cf452a452f9efd88e980ef1c77b8d750d8df54499c62c42046d32721e56b/NEGATIVE_AND_REPLACEMENT_REGISTER.md#L23-L40)

### 1.2 Types and finite derivations

Types are generated by parameters, $`\bot`$, $`\mathrm{Raw}`$, dependent products, dependent sums, identities and impredicative universal quantification:

```math
A,B ::= \alpha\mid\bot\mid\mathrm{Raw}
\mid\Pi x:A.B
\mid\Sigma x:A.B
\mid\mathrm{Id}_A(p,q)
\mid\forall\alpha.B.
```

An arrow $`A\to B`$ is a dependent product whose codomain does not depend on its argument. Contexts are finite dependent telescopes. Formation, context validity and typing are mutually defined. In particular, forming $`\mathrm{Id}_A(p,q)`$ requires derivations of both endpoints at the same formed carrier $`A`$.

Write $`\Gamma\vdash_E p:A`$ for the extensional judgment, named `HasE` in the formal source. It has twenty typing constructors. The following table states their roles; all displayed types, substitutions and contexts must satisfy the explicit formation and scope premises of the finite grammar.

| Rule | Content |
|---|---|
| Variable | Read a variable at its dependent telescope lookup type. |
| $`I`$, $`K`$, $`S`$ | The three combinators have their usual formed arrow types. |
| Finite derivation import | Import a finite derivation built from combinators, application, universal introduction/elimination and reduction, after supplying its finite list of formed type images. |
| Universal introduction | Generalize a type parameter using the correspondingly type-weakened context; the proof polynomial is unchanged. |
| Universal elimination | Instantiate at a formed type; the same erased polynomial receives the instantiated type. |
| Raw atom | Every raw-term atom has type $`\mathrm{Raw}`$. |
| Raw application | Apply two Raw polynomials at $`\mathrm{Raw}`$. |
| Dependent product introduction | From a body under $`x:A`$, construct its bracket abstraction. |
| Dependent product elimination | Apply a typed function and substitute the actual argument into its codomain. |
| Dependent sum introduction | Construct the specific combinatory pair of two appropriately typed components. |
| First projection | Read the first component at the sum's domain type. |
| Second projection | Read the second component at the fiber indexed by the actual first projection. |
| Identity introduction | From typed endpoints $`p\simeq_+q:A`$, obtain $`I:\mathrm{Id}_A(p,q)`$. |
| Proof erasure | A proof of an identity also has type $`\mathrm{Raw}`$. |
| Identity elimination | Transport along a typed identity using its actual dependent motive and proof coordinate. |
| Polynomial conversion | Replace a proof polynomial by a convertible, correctly scoped polynomial at the same formed type. |
| Product extensionality | A typed pointwise identity family yields identity of the two typed dependent functions. |
| Universal extensionality | A typed identity at an arbitrary type parameter yields identity at the universal type. |

The grouped combinator entry counts as three constructors; each other entry counts as one. The import rule does not admit arbitrary semantic truth. Its underlying finite grammar has seven constructors: $`I,K,S`$, application, universal introduction, universal elimination and reduction. All proof objects and rule applications are finite. [Complete source grammar][syntax]

We also use $`\vdash_0`$ for the original base judgment. Its relevant derivations embed in $`\vdash_E`$. It lacks the two extensionality rules and uses the original polynomial conversion relation. When a theorem below asks for an original base typing, that hypothesis is retained rather than silently replaced by semantic membership.

### 1.3 Identity elimination preserves a type dependency even when it erases computation

Fix $`x:A`$. The identity-elimination context extends the original context first by $`y:A`$ and then by $`e:\mathrm{Id}_A(x,y)`$. Let $`B(y,e)`$ be a type formed in that context. From

```math
e:\mathrm{Id}_A(x,y),
\qquad d:B(x,I),
```

with the endpoint typings and all motive instances formed, identity elimination produces

```math
J(d,y,e):B(y,e),
\qquad J(d,y,e)=K(Kd)y e.
```

Two $`K`$ contractions give $`J(d,y,e)\simeq_+d`$. The resulting *type* remains $`B(y,e)`$. Replacing this derivation by the reflexive base derivation would generally change the type back to $`B(x,I)`$. Computation can discard an argument that was essential to typing.

The telescope has two different coordinates: the varying endpoint and its identity proof. A motive may depend on either. This distinction is essential both to the Raw probe in section 3 and to scalar fusion in section 4.

Identity composition and transport of convertible endpoints are derived operations. For example, from $`r:\mathrm{Id}_A(u,v)`$ and $`s:\mathrm{Id}_A(v,w)`$, use identity elimination on $`s`$ with motive $`\mathrm{Id}_A(u,z)`$ and base proof $`r`$. If $`u'\simeq_+u`$ with both terms typed at $`A`$, identity introduction supplies $`\mathrm{Id}_A(u',u)`$, which can be composed with $`r`$. This justifies later changes between displayed beta-convertible endpoints without pretending that arbitrary type expressions themselves have an unrestricted conversion rule.

Product extensionality is equally specific. Given typed $`p,q:\Pi x:A.B(x)`$ and a typed section

```math
h:\Pi x:A.\mathrm{Id}_{B(x)}(px,qx),
```

it produces $`I:\mathrm{Id}_{\Pi x:A.B(x)}(p,q)`$. Pointwise semantic agreement alone is not its premise. Universal extensionality likewise requires an actual derivation at the fresh type parameter. These are proof rules, not semantic reflection principles.

The Raw-motive review makes a stronger boundary than a failed formation attempt. In the exact two-coordinate theta context the proof is var0 and the varying endpoint is var1, and the displayed endpoint environments are inhabited. Closed polynomial syntax is Raw-typable by structural recursion in any formed context; this does not provide an erasure or quotation rule for a bound typed variable. Consequently the review forms the exact target Id_Raw(p,q) in the inhabited assumed context [B], for the original variableExpr/redundantExpr endpoints, yet invokes the retained nonreflection theorem to exclude every HasE witness there. Formation of this fixed target and inhabitation of its context therefore do not remove the source-proof obstruction. The imported exclusion is not newly kernel-checked here. [research/t20-v6-20261012/sources/40e9fcd259f8a31a81ebb27331f09c39f6aef4fb922a28d4f3c8c3f5235de279/IndependentBoundaryChecks.lean:13–52 at ffca0abdf25079ef7639fe19776a21db60272fc4]

#### Literal binder and scope equations for extensionality

The displayed product-extensionality family uses the actual shifted application
$`p^\uparrow x=\mathrm{app}(\mathrm{pren}(\mathrm{succ},p),\mathrm{var}(0))`$.
The source's substitution operations satisfy

```math
\mathrm{inst}\bigl(\mathrm{subst}(\mathrm{pup}(\mathrm{var}\circ\mathrm{succ}),B),
                    \mathrm{var}(0)\bigr)=B,
\qquad
\mathrm{eval}(\mathrm{pren}(\mathrm{succ},p),x::\eta)
=\mathrm{eval}(p,\eta),
```

and therefore $`\mathrm{eval}(p^\uparrow x,x::\eta)=\mathrm{eval}(p,\eta)x`$.
For the first equation, compose the lifted shift with the substitution whose
head is $`\mathrm{var}(0)`$ and whose tail is the variable map. The composite is
literally the identity at both zero and every successor index. Structural
substitution composition and identity give the result. The evaluation equation
follows from polynomial renaming at the shifted environment.

If $`A`$ is type-scoped at $`n`$, $`B`$ at $`n+1`$, and both $`p,q`$ are scoped
at $`n`$, then $`p^\uparrow x,q^\uparrow x`$ are scoped at $`n+1`$. The inner
identity family is type-scoped at $`n+1`$, its product at $`n`$, and
$`\mathrm{Id}_{\Pi A.B}(p,q)`$ at $`n`$. Likewise, type scope of $`B`$ and term
scope of $`p,q`$ at $`n`$ give scope of both $`\mathrm{Id}_B(p,q)`$ and
$`\mathrm{Id}_{\forall\alpha.B}(p,q)`$ at $`n`$. These statements follow by
unfolding the respective scope clauses and the shifted-variable bound.
Type weakening maps a telescope without changing its length. These are raw
binder and scope facts; they add neither a conversion generator nor a
structural admission rule to the extended judgment. [Literal schema equations][R0002-L001]
## 2. Church numbers and the exact pair-state compiler

Define

```math
N=\forall\alpha.(\alpha\to\alpha)\to\alpha\to\alpha,
\qquad T=N\to N.
```

For a natural number $`k`$, the Church numeral $`\overline{k}`$ is the bracket abstraction $`[f][a]f^k a`$, where $`f^0a=a`$ and $`f^{k+1}a=f(f^ka)`$. Let

```math
z=\overline{0}=KI,
\qquad s=[n][f][a]f(nfa).
```

Then $`zfa\simeq a`$ and $`snfa\simeq f(nfa)`$. The source supplies original base typings of the numerals and successor at the required Church types.

Use the specific pair and projections

```math
\langle a,b\rangle=S(SI(Ka))(Kb),
\qquad \pi_1u=uK,
\qquad \pi_2u=u(KI).
```

The combinatory equations show $`\langle a,b\rangle c\simeq cab`$, hence

```math
\pi_1\langle a,b\rangle\simeq a,
\qquad \pi_2\langle a,b\rangle\simeq b.
```

Define the diagonal update, initial state and compiled function by the same bracket algorithm:

```math
\Delta=[u]\langle s(\pi_1u),s(\pi_2u)\rangle,
\qquad z_0=\langle z,z\rangle,
\qquad q=[n]\pi_2(n\Delta z_0).
```

The compiler's other endpoint is exactly $`p=I`$. These are literal source equalities: the imported compiler transport identifies $`p`$ with the compilation of $`x`$ and $`q`$ with the compilation of $`x+0`$. The theorem does not replace the latter with a simpler arithmetic implementation. Both endpoints have original base typings at $`T`$. [Exact compiler binding][transport]

Put $`s^0z=z`$ and $`s^{k+1}z=s(s^kz)`$. Induction on $`k`$ gives

```math
\Delta^kz_0\simeq\langle s^kz,s^kz\rangle,
\qquad (s^kz)fa\simeq f^ka.
```

For the state equation, the base is the definition of $`z_0`$; the induction step uses the two projection equations inside $`\Delta`$. For the scalar equation, the base uses $`z`$, and the step uses the successor equation. It follows that

```math
q\overline{k}\simeq s^kz,
\qquad \overline{k}fa\simeq(q\overline{k})fa.
```

The function-identity question is stronger than this calculation. The identity type

```math
\mathcal B=\mathrm{Id}_{N\to N}(p,q)
```

asks for a typed identity between functions on all inputs admitted by the type judgment. Arithmetic agreement on the displayed numerals is not already a proof of $`\mathcal B`$.

## 3. An inhabited generic probe

There is a real positive result for a generic Church variable, before any assumption of numeral standardness.

**Proposition 1 — the unit probe.** In the original base calculus,

```math
n:N\ \vdash_0\ I:\mathrm{Id}_{\mathrm{Raw}}(nII,I).
```

**Proof.** Form $`R=\mathrm{Id}_{\mathrm{Raw}}(I,I)`$. Identity introduction gives $`I:R`$. The ordinary identity combinator also has type $`R\to R`$. Instantiate $`n`$ at $`R`$ and apply it to these two typings of $`I`$. The resulting polynomial $`e=nII`$ has type $`R`$, hence also $`\mathrm{Raw}`$ by proof erasure.

Apply identity elimination to $`e:\mathrm{Id}_{\mathrm{Raw}}(I,I)`$. Use the motive

```math
B(y,r)=\mathrm{Id}_{\mathrm{Raw}}(r,I).
```

It is formed because its proof-coordinate variable $`r`$ has type $`\mathrm{Raw}`$ by proof erasure. The reflexive base instance is $`\mathrm{Id}_{\mathrm{Raw}}(I,I)`$, proved by $`I`$. The conclusion is $`J(I,I,e):\mathrm{Id}_{\mathrm{Raw}}(e,I)`$. Its proof polynomial converts to $`I`$ at that same type. Substituting $`e=nII`$ proves the claim. $`\square`$

**Proposition 2 — an inhabited extensional endpoint.** Let

```math
F=[n]nII=S(SI(KI))(KI),
\qquad G=[n]I=KI.
```

Both have original base typings at $`N\to\mathrm{Raw}`$, and

```math
\vdash_E I:\mathrm{Id}_{N\to\mathrm{Raw}}(F,G).
```

**Proof.** Under $`n:N`$, bracket beta gives $`Fn\simeq_+nII`$ and $`Gn\simeq_+I`$. Proposition 1 and the derived transport of convertible endpoints give a proof of $`\mathrm{Id}_{\mathrm{Raw}}(Fn,Gn)`$. Product introduction closes this family; product extensionality then gives the displayed identity. The domain is inhabited by $`\overline{0}:N`$, and the function carrier is inhabited by $`G`$. No empty-domain argument is involved. $`\square`$

These are proofs in the stated source grammars. The first already belongs to the original base calculus; the second uses its extensional extension. [Generic probe and exact witnesses][probe]

The result tests one carrier and one pair of arguments. It neither promotes Raw identity to identity at an arbitrary $`\alpha`$ nor produces $`\mathrm{Id}_{N\to N}(p,q)`$. Even different iteration counts at different carriers could satisfy a unit test, since $`I^kI=I`$ for every finite $`k`$. The proof is useful precisely because it states an inhabited positive result without claiming that this one test establishes general uniformity.

There is also an ordinary erased-lambda distinction. Expanding the combinators gives $`\lambda n.n(\lambda x.x)(\lambda x.x)`$ and $`\lambda n.\lambda x.x`$. They are distinct beta-eta normal forms, so the usual confluence theorem for untyped lambda calculus rules out beta-eta conversion between them. This observation concerns untyped conversion; it does not invalidate the typed identity just constructed. The historical probe report records this lambda analysis separately from its Lean-checked declarations. [Probe report and qualification boundary][probe-report]

<a id="t20-generic-probe-literal-witnesses"></a>

**The literal open-to-closed witnesses.** The selected probe supplies the explicit context, carrier formation, endpoint typings and scope witnesses used above. In $\Theta=\mathrm{theta}([N],\mathrm{Raw},I)$ the proof occupies index $0$ and the varying endpoint index $1$. Its motive `Id Raw (var 0) i` is formed by erasing the proof coordinate to Raw; its instances are literally $R$ and $\mathrm{Id}_{\mathrm{Raw}}(nII,I)$. The conversion $J(d,y,e)\simeq d$ is stated for **all** polynomials $d,y,e$, preserving the particular target type when used in the typing rule. [R250-235, lines 13–67][R250-235]

The closed $F$ and $G$ above have scope zero, and $C=N\to\mathrm{Raw}$ is formed in every valid telescope. Their beta-conversion equations hold for every polynomial argument $v$. In the pointwise step the literal renamed terms `leftPoint = (pren Nat.succ F) (var 0)` and `rightPoint = (pren Nat.succ G) (var 0)` equal $Fn$ and $Gn$. The left point retains type $R$ as well as Raw; the right point has Raw type. Instead of leaving the endpoint transport implicit, the source forms the motive `Id Raw (var 0) (G (var 2))` in $\Theta$. Its instances are precisely $\mathrm{Id}_{\mathrm{Raw}}(I,Gn)$ and `pointType = Id Raw leftPoint rightPoint`. The first is proved by $I$ using $G$'s beta conversion; $J$ and proof conversion give `Has [N] i pointType`. Product introduction therefore gives the **particular** closed witness `Has [] G (pi N pointType)`, since $G=[n]I$. Together with the formed function identity, formed family, endpoint typings and scope witnesses, this supplies the unchanged `piExt` rule's premises for `HasE [] i (identity C F G)`. Inhabitation is also explicit: `inputNumeral 0 : N` and $G:C$ both have original `Has` typings. [R250-235, lines 69–174][R250-235]

The file changes no inherited calculus, conversion, compiler or endpoint and explicitly does not prove the literal identity between the compilations of $x$ and $x+0$. It requests axiom listings for `raw_unit_probe`, `point_identity`, `F_has`, `G_has` and `closed_probe_identity`; reading those commands is not obtaining their output. This incorporation does not execute the source or its imported dependencies and makes no new axiom-audit or kernel-check claim. [R250-235, lines 1–7, 176–182][R250-235]

### 3.1 Three exact judgment controls

The inhabited endpoint result does not erase the distinction between a conversion premise, the original typing judgment and its extensional extension. Three short controls isolate those boundaries. In the first, the requested type is `PolyConvPlus p q`, while the supplied term is `PolyConvPlus.refl p`, whose reflexive endpoints are `p` and `p`. The expected type mismatch concerns that supplied proof term; it is not a nonderivability theorem for `PolyConvPlus p q`. [Reflexivity control](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0b5e02f6d3fe4c131085bd28a33dd0ffb2fb6eccfae2698318751fc285777f5d/ReflexivityCannotReplacePremise.lean)

The second control requests `Has [] (jPoly (.atom .i) q (.atom .i)) (.identity Q Fp Fq)` and supplies `inhabited_endpoint_identity`. The latter is an extended identity witness, not an ordinary `Has` proof. The control therefore does not license casting a theorem of the extensional judgment into the original judgment. It also does not establish that every possible ordinary derivation of the target is absent. [Judgment-cast control](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/248b5ba9b09a97396153d47c9c373720afac702cc787e69ba98e88b5b6161c30/WrongJudgmentCast.lean)

The third retains `HasE` and the same displayed proof polynomial but requests `(.identity Q Fp Fp)` instead of the exact `(.identity Q Fp Fq)` endpoint statement furnished by `inhabited_endpoint_identity`. Its expected rejection is a mismatch of that exact theorem statement, not noninhabitation of the reflexive identity: the source expressly records that the reflexive identity is derivable. These controls import the existing endpoint module without adding a derivation rule. Their expected elaboration failures are source-specified tests, not freshly observed compiler results, and none is substituted for the independent semantic separation arguments elsewhere in this work. [Exact-endpoint control](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4105a1e224403f5dc9fecada98c0e902cd391cb402ef4781936ce2e03a6bfd88/WrongEndpointReadback.lean)

### A separate transport into an inhabited function carrier

There is a second, exact positive endpoint construction, distinct from the unit probe and from the compiled x/x+0 question. Put U=All α.α and E=U→Raw. The closed constants p=K I and q=K K are ordinarily typed at E. In context [U], instantiate its U-variable at the formed identity between p applied to that variable and q applied to it. This supplies the pointwise identity used by the extensional rule, and hence HasE(I : Id_E(p,q)). This step uses the extensional calculus, not original conversion of p and q. [S250-L482]

One can carry that identity to the inhabited carrier Q=N→N with the **literal** term H=abstract(abstract(fst(var0 I (pair(0,var1)))): in context [N,E], instantiate the Church variable at the dependent-pair type Σ N.E, start at (0,var1), and iterate the identity. Formation, ordinary typing and closedness are supplied for H, Fp=H p and Fq=H q. In the J telescope, proof remains coordinate0 and endpoint coordinate1. The motive Id_Q(Fp,H var1) substitutes to Id_Q(Fp,Fp) at the base and Id_Q(Fp,Fq) at the target. The retained J rule gives the exact HasE witness J(I,q,I) at the latter target. Q itself is ordinarily inhabited by I. This earns a positive result at an inhabited function carrier without asserting the literal compiler-pair identity. [S250-L333]

The independent readback also derives **that same J-shaped witness at the reflexive target** Id_Q(Fp,Fp), using its conversion to I. Thus rejection of an attempted wrong-endpoint cast is a mismatch of the supplied theorem statement, not a proof that the reflexive target is empty. Literal compiler readback separately identifies the variable compiler with I and the redundant-expression compiler with its retained pair-state body; neither is substituted for Fp or Fq. These are inspected source derivations and contracts, not newly executed kernel or axiom-audit results. [S250-L474] [S250-L482]

[S250-L333]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/57a4559c45f76bbb6b2a55b0ddc208350bb866bb7fe1be0f80fd4df8ffeef61f/InhabitedEndpointControl.lean
[S250-L474]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7ebd4056c1aece159fd00270eb1f8de5239276943659f863eda71dd0ac20e90e/ReviewerReadback.lean
[S250-L482]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7fe317d5fbc4657ecd7f793808872941a8bfdf5b3a281f87a2f11b6ea70ac7a9/UArrowAndCompilerControls.lean

## 4. A fixed witness for the exact scalar-fusion obligation

For a closed polynomial $`k`$ with an original base derivation $`\vdash_0 k:T`$, define

```math
\mathcal B(k)=\mathrm{Id}_T(I,k),
```

```math
W(k)=\Pi n:N.\forall\alpha.
\Pi f:(\alpha\to\alpha).\Pi a:\alpha.
\mathrm{Id}_{\alpha}(nfa,(kn)fa).
```

The universal quantifier over $`\alpha`$ is erased. There are exactly three term binders, so the constant proof section is the literal polynomial

```math
c_3=[n][f][a]I=K(K(KI)).
```

**Theorem 3 — four equivalent obligations.** Under the stated base typing of $`k`$, the following propositions are equivalent:

1. Some closed polynomial proves $`\mathcal B(k)`$ in $`E`$.
2. $`\vdash_E I:\mathcal B(k)`$.
3. Some closed polynomial proves $`W(k)`$ in $`E`$.
4. $`\vdash_E c_3:W(k)`$.

**Proof, identity to the fixed scalar witness.** First construct $`c_3:W(I)`$ in the original base calculus. At the scalar leaf, $`nfa\simeq_+(In)fa`$, and both endpoints have type $`\alpha`$, so identity introduction supplies $`I`$. Introduce the three term binders and the type parameter.

Now suppose $`e:\mathcal B(k)`$. Eliminate that identity with motive $`M(y,e')=W(y)`$. It does not depend on the proof coordinate. In the literal indexed syntax, the endpoint occupies coordinate 1 before the scalar binders and coordinate 4 under the three term binders; the proof coordinate is not substituted for it. The reflexive instance is exactly $`W(I)`$, and the target is exactly $`W(k)`$. Identity elimination gives $`J(c_3,k,e):W(k)`$. Its two $`K`$ contractions give $`c_3`$ at the unchanged target type. [Forward construction][fusion-forward]

**Proof, arbitrary scalar witness to identity.** Work first with a local variable $`w:W(k)`$. For arbitrary $`n:N`$, fresh $`\alpha`$, $`f:\alpha\to\alpha`$ and $`a:\alpha`$, eliminate $`w`$ to obtain

```math
wnfa:\mathrm{Id}_{\alpha}(nfa,(kn)fa).
```

Close over $`a`$ and apply product extensionality to obtain identity of $`nf`$ and $`(kn)f`$ at $`\alpha\to\alpha`$. Close over $`f`$ and apply product extensionality again. Universal extensionality then gives

```math
n:N,\ w:W(k)\ \vdash_E\ I:\mathrm{Id}_N(n,kn).
```

Transport the left endpoint from $`n`$ to the literal $`In`$, using identity introduction for $`In\simeq_+n`$ and identity elimination. Close over $`n`$ and apply product extensionality to obtain $`I:\mathcal B(k)`$ under $`w:W(k)`$.

Crucially, close over $`w`$ *before* using a supplied closed witness $`h:W(k)`$. This gives $`[w]I:\Pi w:W(k).\mathcal B(k)`$. Applying it to $`h`$ yields the desired type, and $`([w]I)h\simeq_+I`$. This proof does not presume a general weakening theorem for arbitrary supplied $`E`$ derivations. The two constructions, together with the obvious existential introductions, establish all four equivalences. $`\square`$ [Reverse construction][fusion-reverse]

Because the compiler gives the literal equality $`p=I`$ and the required original typing of $`q`$, Theorem 3 applies to $`\mathcal B=\mathcal B(q)`$ without changing either endpoint. [Literal specialization][fusion-literal]


<a id="second-cohort-scalar-fusion-source-guards"></a>

The exact reverse implementation supplies every domain/codomain formation, endpoint typing, motive formation and scope premise to its unchanged extensionality rules. It first derives the scalar leaf from the **local** variable w:W(k), then uses actual identity elimination to move the left endpoint n to In. Closing over n gives identity under w; closing over w precedes application of the supplied closed extended witness. This is the source-level reason the proof above does not presume arbitrary HasE weakening. Its `generic_four_way_iff` states equivalence of four propositions, not an inhabitant of any one. The source proof and its derived theorem map preserve the original premise Has [] k T. [S250F405]

Three compact controls expose different invalid substitutions. `RejectSemanticReflection` supplies semantic endpoint validity where `canonical_identity` requires an actual HasE derivation; the mismatch does not invalidate semantic soundness. `RejectUnconditionalIdentity` supplies `literal_reverse` without the required scalar witness. `BeforeImplementation` imports the declared observer/syntax interface and then invokes a later named Raw probe; that import-surface attempt does not itself implement or prove the probe. These are exact negative/elaboration targets. No compiler run or universal nonderivability result is inferred merely from their presence. [S250F326] [S250F401] [S250F373]

[S250F326]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/568831c8e9f6226328560c0e2d1d6803dbcab5a79341cc074ba91c1cb73b268e/RejectSemanticReflection.lean
[S250F373]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/61a7fbcb6076d71bf5d2c4fd02128cc76103acab57e53ba1af59dc0a1dd2a3ee/BeforeImplementation.lean
[S250F401]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/680346cc7b3fcaa3ca96b5818de33f673a1ae704d36c3da72b7b0d45781fe53d/RejectUnconditionalIdentity.lean
[S250F405]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6a03e72fe6e087c98b97d0f881f6f1dc7960c2a46b89f7f1351394ff3b410b65/ScalarFusionReverse.lean

### 4.1 What fixed proof syntax does and does not decide

There is also a general proof-polynomial result: if $`\vdash_E r:\mathrm{Id}_A(u,v)`$ is already supplied and closed, then

```math
\vdash_E I:\mathrm{Id}_A(u,v).
```

One proof uses soundness in an interpretation where identity evidence is represented by the conversion class of $`I`$. It obtains conversion of the *supplied proof polynomial* to $`I`$; closed conversion reflection and the source conversion rule then preserve its original type. This does not infer a source identity merely from semantic equality of $`u`$ and $`v`$. Sections 5–6 give an interpretation and reification argument sufficient for this proof. [Closed proof canonicalization][canonical]

The fixed polynomial $`c_3`$ is not a finite bound on the derivations that could assign it a type. The forward proof above can use an arbitrary identity derivation inside $`J`$ and erase its entire proof argument. Inverting the outer $`K`$ applications of $`c_3`$ as though its last rules must have been product introductions is therefore invalid. Removing the identity-elimination step leaves a derivation of $`W(I)`$, not $`W(k)`$.

A normal proof polynomial can conceal complicated type annotations and an essential dependent transport. Neither a short normal form nor finitely many failed searches bounds those annotations. [Proof-theoretic obstruction][failed-routes]

<a id="t20-scalar-contract-and-rejection-boundaries"></a>

**The literal statement and judgment boundary.** The statement and motive contracts independently spell out the same literal endpoint bindings, scalar type, threefold abstraction, coordinate-4 motive, local judgments and four equivalent obligations already displayed in §§2 and 4. Those statements are retained at that scope, without replacing either compiled endpoint or asserting that an equivalent obligation is inhabited. [R250-123, lines 7–23][R250-123] [R250-040, lines 5–18][R250-040]

The general canonicalization contract also retains two prerequisites for arbitrary telescopes: from `HasE Γ r A` one obtains both `Scoped Γ.length r` and `FormE Γ A`. For any closed identity at **any** carrier and endpoints, not just the compiler pair, the closed canonicalization statement is equivalently

```math
(\exists r,\ \vdash_E r:\mathrm{Id}_A(p,q))
\quad\Longleftrightarrow\quad
\vdash_E I:\mathrm{Id}_A(p,q).
```

The nontrivial implication consumes the supplied derivation; the reverse chooses $r=I$. This is a proof-polynomial result within $E$, not an implication from semantic equality to syntactic derivability. [R250-046, lines 3–12][R250-046]

Two deliberately restricted source attempts guard this distinction. `CanonicalizationRed.lean` imports only `ExtensionalRepairSyntax` and then invokes `ClosedProofCanonicalisation.canonical_identity` at the same general closed identity statement. Its companion positive contract instead imports `ClosedProofCanonicalisation`. `RejectCurrentLaundering.lean` attempts to use `literal_reverse` to turn `HasE [] c3 (W q)` into the **original** judgment `Has [] i literalB`, whereas the positive direction contract concludes `HasE`, not `Has`. These exact import-surface and judgment-boundary attempts are negative-control targets. The selected bodies contain no rejection logs; no compilation was performed here. A failed import or elaboration, even if separately observed, would not by itself be a mathematical counterexample or a proof that every possible original-calculus derivation is absent. The independent separation arguments elsewhere in this chapter retain their own evidence and scope. [R250-089, lines 1–5][R250-089] [R250-164, lines 1–4][R250-164]

The retained `ScalarFusionCore` is the same exact source already linked as [fusion-forward]. It forms W(k), proves the literal three-abstraction base c3, and places the endpoint at var4 beneath the three term binders. Its `forward_fixed` consumes a supplied HasE identity from i to k and transports that premise to c3 at W(k). The header leaves the literal endpoint open; this one-way reduction is not an independent proof of that missing identity. The `RejectNonliteralWitness` control asks the literal forward theorem to return a doubly abstracted witness instead. Its purpose is exact witness preservation, not an alternative positive fusion derivation. [R750A-563] [R750A-542]

`StatementContract` records a different, already explained probe: the raw-unit identity in context [N], the literal F/G functions at N→Raw, their **extended** HasE closed identity, and inhabited domain and carrier. It retains current endpoint typing separately from extended identity. Neither its repeated interface applications nor the scalar conditional erase that judgment distinction. [R750A-567]

[R750A-542]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/91c2125bd2b75af9b46dc56c47fe6385726cdf7af3d89f943ef4bb696d483dc6/RejectNonliteralWitness.lean
[R750A-563]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618/ScalarFusionCore.lean
[R750A-567]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9889aaea30cd558de1535a6f066435d2d3536c724c72b1239cf4db2c171da9ba/StatementContract.lean

## 5. Full-PER semantics and uniform iteration

### 5.1 Partial equivalence relations

A partial equivalence relation, or PER, is a symmetric and transitive binary relation. Its support consists of elements related to themselves. Reflexivity is required only on that support. A PER $`R`$ on an applicative carrier is *conversion-saturated* if replacing either endpoint by a convertible term preserves relatedness.

For saturated PERs $`R,S`$, define the arrow relation

```math
(R\Rightarrow S)(f,g)
\quad\Longleftrightarrow\quad
\forall a,b\,\bigl(R(a,b)\Rightarrow S(fa,gb)\bigr).
```

It compares related arguments, not merely the same argument. Symmetry and saturation follow directly from those of $`R,S`$. For transitivity, if $`f`$ is related to $`g`$, $`g`$ to $`h`$, and $`R(a,b)`$, then $`R(b,b)`$; combine $`S(fa,gb)`$ with $`S(gb,hb)`$. Thus the arrow relation is again a saturated PER.

Take the carrier $`D`$ of all finite *open* SKI terms, also containing the inert constants and countably many inert variable generators. Conversion is the ordinary combinatory congruence. Interpret

```math
\mathcal N(n,m)
\quad\Longleftrightarrow\quad
\forall R\in\mathcal P\,
((R\Rightarrow R)\Rightarrow(R\Rightarrow R))(n,m),
```

where $`\mathcal P`$ is the set of **all** conversion-saturated PERs on $`D`$. Universal quantification is intersection over this fixed universe. This is the standard PER method of interpreting erased polymorphism. The role of the chosen carrier and of the available PERs must remain explicit. Hyland, Robinson and Rosolini's analysis of algebraic types provides the relevant antecedent; its open-term argument is attributed there to Moggi. Reynolds's abstraction theorem supplies the broader relational context. Neither is imported as a blanket soundness theorem for the present dependent calculus. [Primary literature][hrr] [Reynolds][reynolds]

### 5.2 One fresh orbit forces a uniform count

**Theorem 4 — standardness in the full open-term interpretation.** For any finite open term $`n`$,

```math
\mathcal N(n,n)
\quad\Longleftrightarrow\quad
\exists k\in\mathbb N\ \forall f,a\in D,
\quad nfa\simeq f^ka.
```

The natural number $`k`$ is independent of the chosen carrier relation and of $`f,a`$.

**Proof, forward direction.** Choose two variable generators $`u,v`$ absent from $`n`$. On $`D`$, define the orbit PER

```math
O_{u,v}(x,y)
\quad\Longleftrightarrow\quad
x\simeq y\ \text{ and }\
\exists k\in\mathbb N\, x\simeq u^kv.
```

It is symmetric: reverse $`x\simeq y`$ and use the same orbit witness. It is transitive by composing conversions and retaining the first witness. It is saturated by composing with the conversions of the endpoints. The definition does not assume that different iteration counts are distinct.

The seed $`v`$ lies in its support, and $`u`$ is an endomorphism of this PER: applying $`u`$ carries an orbit witness $`k`$ to $`k+1`$ and preserves conversion. Instantiate $`\mathcal N(n,n)`$ at this one relation, endomorphism $`u`$ and seed $`v`$. It follows that

```math
nuv\simeq u^kv
```

for some $`k`$. Raw conversion is preserved by substitution. Substitute arbitrary $`f,a`$ for the fresh generators $`u,v`$. The substitution leaves $`n`$ unchanged, because neither generator occurs in it. The resulting equation is $`nfa\simeq f^ka`$, with the same $`k`$ for every $`f,a`$.

**Reverse direction.** Suppose a uniform $`k`$ is given. For any saturated PER $`R`$, related endomorphisms $`f,g`$, and $`R`$-related seeds $`a,b`$, induction on $`k`$ gives $`R(f^ka,g^kb)`$. Saturation along the two supplied conversions yields $`R(nfa,ngb)`$. This is $`\mathcal N(n,n)`$. $`\square`$ [Standardness proof][standardness] [Converse and arrow interface][per-interface]

This is an explicit semantic proof. It assumes neither a general parametricity axiom nor strong normalization of every typed expression. The fresh open generators and the availability of the orbit PER do the work. A different universe that excludes the needed relation does not automatically satisfy this theorem.

Uniform iteration also yields a supported-square transport law. For saturated PERs A and B, endomorphisms f and g, an arrow h:A→B and supported a, assume B(h(f x),g(h x)) only for supported x in A. Induction first gives B(h(f^k a),g^k(h a)); a uniform count and saturation then give B(h(n f a),n g(h a)). For related Church inputs n,m, related arrows f,f′, g,g′, h,h′ and related seeds a,a′, the left square alone suffices for B(h(n f a),m g′(h′ a′)): self-support follows from PER symmetry and transitivity, and Church relatedness supplies the second leg. No equality of separately extracted counts or heterogeneous graph-admission axiom is needed for this full-PER carrier. This is a semantic, dependency-relative result, not a source HasE derivation. [NEXT-T8-084](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2d1c5df800d77933c6d8b1564209e27606fb209da0720f96f68e8e43b420cc0e/GenericFoldTransport.lean#L7-L58)

### 5.3 The compiler is valid in this interpretation

For $`\mathcal N(n,n)`$, choose its uniform count $`k`$ by Theorem 4. The state calculation of section 2 gives

```math
qn\simeq\pi_2(\Delta^kz_0)\simeq s^kz,
```

and therefore

```math
nfa\simeq(qn)fa
```

for all $`f,a`$. This is *scalar fusion*: interpretation by a scalar iterator agrees with interpretation through the pair-state representation followed by projection.

To prove full arrow equality, let $`\mathcal N(n,m)`$. Then $`m`$ is in the support of $`\mathcal N`$. For any $`R`$, related $`f,g`$ and related $`a,b`$, the given relation gives $`R(nfa,mgb)`$. Scalar fusion for $`m`$ and saturation replace the second endpoint by $`(qm)gb`$; the $`I`$ equation replaces the first by $`(In)fa`$. Thus

```math
(\mathcal N\Rightarrow\mathcal N)(I,q).
```

This is equality of the actual compiler endpoints, including heterogeneous related inputs. It is not just equality on a list of identical test numerals.

The two source transports have different reflection guarantees. Into open SKI terms, erasing every fresh generator to the original zero is a retraction of the raw-term embedding and preserves conversion. Hence conversion of embedded original terms is equivalent to their original conversion, even though the compiler endpoints are related at the Church arrow. The Henkin transport instead folds open terms into the carrier of §8 under arbitrary valuations, preserves open conversion, and derives the original abstraction beta law there. Both bodies preserve the original bridge-extended polynomial conversion, with atom packing interpreted by reflexivity; the Henkin body also verifies the pair projections. It does not supply the open-carrier retraction or a converse conversion theorem for its larger target. These bridge results alone do not prove HasE soundness. [NEXT-T8-220](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/448e9f950a1c51a9267ca04671fe6ade3377a485692621bd8252925ae02fbdbc/ImportedCompilerTransport.lean#L11-L141) [NEXT-T8-220](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/448e9f950a1c51a9267ca04671fe6ade3377a485692621bd8252925ae02fbdbc/ImportedCompilerTransport.lean#L177-L193) [NEXT-T8-188](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3e3e4bcbea2c19c58df20cb7f83c7e5e9a41e7a4c9dcfab6085e09fc2025987a/SourceTransport.lean#L13-L117)

A separate literal Raw context makes the obstruction more explicit. Set tail=K(K(K one)), probe=K(K(pair zero tail)) and C(t)=t probe I I K. The source transports reductions of C(originalP) and C(originalQ) to the distinct inert constants zero and one back to source conversion. Any relation saturated under conversion, compatible with application and reflexive on I,K,S,zero,one therefore relates zero to one if it identifies those endpoints. This requires neither a full PER model nor reflexivity of every carrier element. The probe is separately shown not to be Church and not to have closed Joint typing at N, so the test does not contradict equality at the Church arrow. Reflection, normalization and typing boundaries remain imported dependencies, and the requested axiom listings were not executed. [AF750-Q4-167](../research/t20-v6-20261012/sources/cc322a811064c1e53e0b53a86a9ac6836edcac7c8f57b0121e3eee31fbe896e6/SourceRawSeparator.lean#L13-L65) [AF750-Q4-167](../research/t20-v6-20261012/sources/cc322a811064c1e53e0b53a86a9ac6836edcac7c8f57b0121e3eee31fbe896e6/SourceRawSeparator.lean#L67-L118)

### 5.4 Extending the interpretation to the whole source calculus

The above reduct becomes a sound interpretation of all twenty source rules under explicit semantic admissibility conditions. A type valuation $`\rho`$ assigns a binary relation on $`D`$ to each type parameter. It is **admissible** when every $`\rho(\alpha)`$ is a conversion-saturated PER, hence belongs to $`\mathcal P`$. A term environment $`\eta`$ assigns an element of $`D`$ to each term-variable coordinate. The recursive interpretation can be defined even for arbitrary relation valuations; the soundness conclusions below apply only to admissible valuations and the specified context environments. Interpret types by relations $`\mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}_{\rho,\eta}`$:

```math
\mathopen{\lbrack\!\lbrack}\alpha\mathclose{\rbrack\!\rbrack}_{\rho,\eta}=\rho(\alpha),
\qquad\mathopen{\lbrack\!\lbrack}\bot\mathclose{\rbrack\!\rbrack}_{\rho,\eta}=\varnothing,
\qquad\mathopen{\lbrack\!\lbrack}\mathrm{Raw}\mathclose{\rbrack\!\rbrack}_{\rho,\eta}=\simeq.
```

For a dependent family with domain relation $`A`$ and fibers $`B(a)`$, use

```math
\Pi(A,B)(f,g)
\quad\Longleftrightarrow\quad
\forall a,b\,[A(a,b)\Rightarrow B(a)(fa,gb)],
```

```math
\Sigma(A,B)(z,w)
\quad\Longleftrightarrow\quad
A(\pi_1z,\pi_1w)
\ \text{ and }\
B(\pi_1z)(\pi_2z,\pi_2w).
```

The fibers satisfy $`A(a,b)\Rightarrow B(a)=B(b)`$. This is proved for formed source families by the simultaneous soundness induction; it is not added as a new source-rule premise. Interpret identity evidence by

```math
\mathopen{\lbrack\!\lbrack}\mathrm{Id}_A(p,q)\mathclose{\rbrack\!\rbrack}_{\rho,\eta}(r,s)
\quad\Longleftrightarrow\quad
\mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}_{\rho,\eta}
  (\mathopen{\lbrack\!\lbrack} p\mathclose{\rbrack\!\rbrack}_\eta,\mathopen{\lbrack\!\lbrack} q\mathclose{\rbrack\!\rbrack}_\eta)
\ \text{ and }\ r\simeq I\ \text{ and }\ s\simeq I.
```

Interpret $`\forall\alpha.B`$ by intersection of $`\mathopen{\lbrack\!\lbrack} B\mathclose{\rbrack\!\rbrack}`$ over every PER assigned to $`\alpha`$. Terms are interpreted compositionally, independently of their types or derivations. In particular, type instantiation changes a relation, not the erased term.

We must also specify which environments satisfy a context. Fix a default environment $`\eta_*`$, the constant inert-zero environment in the formal source. Write $`\mathrm{Supp}^{\rho}_{\Gamma}(\eta)`$ for context support and $`\mathrm{Rel}^{\rho}_{\Gamma}(\eta,\xi)`$ for context relatedness. Their empty-context clauses are

```math
\mathrm{Supp}^{\rho}_{[]}(\eta)\ \Longleftrightarrow\ \eta=\eta_*,
\qquad
\mathrm{Rel}^{\rho}_{[]}(\eta,\xi)\ \Longleftrightarrow\
\eta=\eta_*\ \text{ and }\ \xi=\eta_*.
```

For a telescope extended by a type $`A`$ over its tail $`\Gamma`$, use the recursive clauses

```math
\mathrm{Supp}^{\rho}_{A::\Gamma}(a::\eta)
\ \Longleftrightarrow\
\mathrm{Supp}^{\rho}_{\Gamma}(\eta)
\ \text{ and }\ \mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}_{\rho,\eta}(a,a),
```

```math
\mathrm{Rel}^{\rho}_{A::\Gamma}(a::\eta,b::\xi)
\ \Longleftrightarrow\
\mathrm{Rel}^{\rho}_{\Gamma}(\eta,\xi)
\ \text{ and }\ \mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}_{\rho,\eta}(a,b).
```

Here $`a::\eta`$ adds the new head value and shifts the existing coordinates. The head type is interpreted at the left tail environment, as in the actual dependent telescope relation. No arbitrary assignment of raw values is presumed to satisfy a context.

**Theorem 5 — source soundness.** Let $`\rho`$ be admissible. For each formed source context $`\Gamma`$, the relation $`\mathrm{Rel}^{\rho}_{\Gamma}`$ is a PER whose support is exactly $`\mathrm{Supp}^{\rho}_{\Gamma}`$; in particular, related environments are both supported. If $`A`$ is formed over $`\Gamma`$ and $`\mathrm{Supp}^{\rho}_{\Gamma}(\eta)`$, then $`\mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}_{\rho,\eta}`$ is a saturated PER. If instead we have context-related $`\eta,\xi`$, their interpretations of that formed type are equal: $`\mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}_{\rho,\eta}=\mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}_{\rho,\xi}`$. Finally, if $`\Gamma\vdash_E p:A`$ and $`\mathrm{Rel}^{\rho}_{\Gamma}(\eta,\xi)`$, then

```math
\mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}_{\rho,\eta}
  (\mathopen{\lbrack\!\lbrack} p\mathclose{\rbrack\!\rbrack}_\eta,\mathopen{\lbrack\!\lbrack} p\mathclose{\rbrack\!\rbrack}_\xi).
```

**Proof.** Using the stated telescope recursion, prove context PER laws and the equivalence of support with self-relatedness, type PER laws and coherence at the specified environments, and term relatedness simultaneously over the actual finite formation and typing rules. The empty telescope is supported by its fixed default environment. These are semantic premises and induction conclusions, not new formation or typing rules.

For dependent products, symmetry uses $`B(a)=B(b)`$ to reverse related arguments; transitivity inserts a middle value at a supported argument. Dependent sums use this same fiber equality to compose the second projections at the correct index. Saturation is application congruence plus fiber transport. Identities are either empty or the conversion class of $`I`$; coherence of their endpoint condition follows by composing the related interpretations of the two typed endpoints. Intersections preserve the PER laws and coherence.

Variables follow telescope lookup. The $`I,K,S`$ cases use their equations and saturation. Product introduction uses bracket beta at arbitrary related arguments; elimination uses the dependent substitution identity. Pair introduction uses the two projection equations and fiber transport; the projection cases read the two conjuncts. Universal introduction quantifies over every PER; elimination selects the PER supplied by the formation induction for the actual instantiation type. Identity introduction uses conversion soundness. Raw atoms are self-related, Raw application uses congruence, and proof erasure uses the two proof terms' conversions to $`I`$.

For identity elimination, $`e:\mathrm{Id}_A(x,y)`$ makes the two extended environments $`(x,I)`$ and $`(y,e)`$ related: their endpoint coordinates are $`A`$-related, and the proof coordinates both convert to $`I`$. Motive coherence transports the base relation from $`B(x,I)`$ to $`B(y,e)`$. The equation $`J(d,y,e)\simeq d`$ then supplies the conclusion by saturation. This checks the proof coordinate as well as the endpoint coordinate.

For product extensionality, the typed pointwise section gives $`B(a)(pa,qa)`$ at every supported $`a`$. The typing of $`q`$ supplies $`B(a)(qa,qb)`$ whenever $`A(a,b)`$. Transitivity gives $`B(a)(pa,qb)`$, the required heterogeneous arrow relation. Universal extensionality takes the endpoint component of its identity premise at each PER. Polynomial conversion uses conversion soundness at the unchanged type.

Finally, the finite-import rule is not left opaque. Induct on its seven constructors using the same PER laws, intersection and substitution. Interpret the supplied finite type-image list by its formed PERs and fill unused positions by the empty PER. This validates impredicative elimination inside the imported finite derivation as well as the outer rule.

Term substitution, type substitution and their mixed form commute with interpretation by structural induction. Under a type binder the fixed quantifier universe remains the same. These identities justify every substituted target above. The simultaneous induction therefore covers every constructor; none assumes the conclusion of its own soundness case. $`\square`$ [Full interpretation and complete source induction][full-per]

As a consequence, $`I`$ semantically inhabits $`\mathcal B`$, and $`c_3`$ semantically inhabits $`W(q)`$. At each scalar leaf its proof applications convert to $`I`$, and the endpoint relation follows from scalar fusion. These are semantic inhabitants, not source derivations. [Exact semantic endpoint application][application]

## 6. Closed source terms: canonicity and a genuine decision boundary

The full interpretation gives a positive theorem about actual source terms, stronger than agreement only for literal numerals.

### 6.1 Recovering conversion at generic variables

Reify an open semantic term by replacing each variable generator with the corresponding polynomial variable, each primitive constant with its atom, and each application with polynomial application. Induction on a semantic conversion gives polynomial conversion of the reifications. For an original raw atom that contains an application, repeated use of the packing equation yields the required reification. Consequently,

```math
\mathopen{\lbrack\!\lbrack} u\mathclose{\rbrack\!\rbrack}_{\mathrm{var}}
\simeq\mathopen{\lbrack\!\lbrack} v\mathclose{\rbrack\!\rbrack}_{\mathrm{var}}
\quad\Longrightarrow\quad u\simeq_+v.
```

This reflects **raw conversion at the generic-variable interpretation**. It does not reflect arbitrary typed semantic equality.

If $`\vdash_E n:N`$ is supplied, its polynomial is closed, so its interpretation does not depend on the term environment. Theorem 5 makes it a member of the full Church interpretation. Theorem 4 and reification therefore give a finite $`k`$ with

```math
nfa\simeq_+f^ka
```

as an open polynomial equation in generic variables $`f,a`$. The same argument and scalar fusion give

```math
nfa\simeq_+(qn)fa.
```

The original $`n`$ is retained throughout; it is not replaced in the premise by a numeral or a normal form. [Generic conversion reflection and closed instances][closed-instances]

### 6.2 Typing and identity of the closed instances

For each fixed closed derivation $`\vdash_E n:N`$, the scalar identity has a finite source proof. One can first type $`f^ka:\alpha`$ by induction on $`k`$ under $`f:\alpha\to\alpha,a:\alpha`$, then use the previous conversions to type both literal scalar endpoints. Identity introduction and the two term introductions yield

```math
\vdash_E c_2:
\forall\alpha.\Pi f:(\alpha\to\alpha).\Pi a:\alpha.
\mathrm{Id}_{\alpha}(nfa,(qn)fa),
\qquad c_2=K(KI).
```

This is exactly the body of $`W(q)`$ after substitution of the particular closed $`n`$. Since $`c_3n\simeq_+c_2`$, the original fixed witness applied to that $`n`$ has the same literal instance type.

For the stronger closed canonicity statement, the source also proves structural renaming for the entire extensional grammar. If a map of telescope variables preserves scope and dependent lookup, it transports formation and typing, including the two extensionality rules. The proof is simultaneous induction. Product and sum cases lift the variable map under one binder; identity elimination lifts it under both endpoint and proof coordinates; universal rules type-weaken the context; finite type images are mapped entry by entry. The extensionality cases retain their explicit formation and scope guards. Bracket abstraction commutes with these lifted renamings, and all eight conversion generators are stable under polynomial substitution. Taking the empty source telescope and the identity variable map therefore weakens any closed derivation into any formed telescope without changing its polynomial or its type. [Structural renaming][rename] [Closed weakening][weakening]

**Theorem 6 — closed Church identity.** Suppose actual closed typings $`\vdash_E u:N`$ and $`\vdash_E v:N`$ are supplied. Let $`j,k`$ be their generic-open iteration counts. Then

```math
\bigl(\exists r\;\vdash_E r:\mathrm{Id}_N(u,v)\bigr)
\quad\Longleftrightarrow\quad
\bigl(\vdash_E I:\mathrm{Id}_N(u,v)\bigr)
\quad\Longleftrightarrow\quad j=k.
```

In particular every supplied closed $`n:N`$ is source-identical at $`N`$ to a Church numeral.

**Proof, equal counts.** Weakening provides typings of the unchanged closed endpoints under the fresh scalar variables. Their observations $`ufa`$ and $`vfa`$ convert to the same $`f^ja`$. Identity introduction proves the scalar identity. Product extensionality first closes $`a`$, then $`f`$; universal extensionality closes $`\alpha`$. This yields $`I:\mathrm{Id}_N(u,v)`$. Applying the same construction to $`n`$ and $`\overline{k}`$ proves canonicity.

**Proof, any identity implies equal counts.** Soundness puts $`u`$ and $`v`$ in relation $`\mathcal N`$. Use a fresh orbit PER $`O_{f,a}`$. It relates their observations, so $`ufa\simeq vfa`$. Their respective count equations give $`f^ja\simeq f^ka`$. These are redex-free open terms with distinct free head and seed variables. Confluence of SKI reduction makes convertible normal forms identical, and induction on their application trees gives $`j=k`$. Thus an arbitrary, possibly noncanonical proof witness cannot identify distinct counts. $`\square`$ [Closed canonicity and identity theorem][closed-identity]

### 6.3 Extracting the count without assuming strong normalization

There is an effective procedure on this **promised input domain**: the two original polynomials and their actual closed typing derivations are supplied. Compute the generic observation $`nfa`$, repeatedly take its complete parallel development, and inspect whether the result has the literal form $`f^ka`$.

The development operation recursively develops subterms and contracts any $`I,K,S`$ redex already present at the current root. It does not repeatedly normalize a newly exposed redex in the same step. For parallel reduction $`t\Rightarrow u`$, the triangle property gives $`u\Rightarrow\mathrm{dev}(t)`$. A second use gives monotonicity $`\mathrm{dev}(t)\Rightarrow\mathrm{dev}(u)`$.

If $`z`$ has no redex, every parallel reduct of $`z`$ equals $`z`$. Monotonicity and the triangle property show that reaching $`z`$ by repeated development is invariant in both directions along a parallel step, and hence along a conversion chain. Therefore every term convertible to a redex-free $`z`$ reaches it after finitely many developments. Apply this to the conversion $`nfa\simeq f^ka`$ proved above. Structural readback recognizes the iteration tree and returns $`k`$. Its count is unique because distinct iteration normal forms are not convertible.

Each development and readback is computable. Search over the finite development count is unbounded but terminates on the supplied typed inputs. The source implementation uses natural-number search with a proved termination witness; erased typing proofs are not runtime semantic oracles. Comparing the two extracted natural numbers decides the identity proposition in Theorem 6. [Complete development and extraction][developments] [Typed identity decision][decision]

The finite scalar-certificate controls keep trace validation separate from an asserted answer. Their four written checks reject a left address into a variable leaf, an application of two variables offered as a root redex, a genuine I-step paired with the forged endpoint var17, and that same step paired with a forged count-one generic iteration. Thus an address, a step, its endpoint and the literal iteration target are separate obligations. These concrete rejection declarations use the imported stepAt and replayTo interfaces; they do not give a complete JSON parser refinement, validate arbitrary submitted traces or provide fresh axiom-readback or execution results. [SUB250-C20-025](../research/t20-v6-20261012/sources/52f0ae30d75225049b29280f5a2f3e05d45b6e8e3994d1ae6a54d1a26d009998/NegativeCertificateControls.lean#L6-L19)

Positive replay also does not certify the promised closed input domain. The open-certificate control explicitly takes n=K(K I)(var42), supplies separate address lists for its literal left and right scalar observations, and applies the imported replay interfaces to convert each observation to iterationPoly(0). Transitivity then gives their conversion. The right replay first expands the original Q, preserving that literal endpoint rather than substituting an unspecified equivalent program. This body supplies no closed HasE typing of n:N; an erased free-variable argument can coexist with a successful scalar conversion certificate. The conversion declarations therefore remain distinct from closedness, Church-input typing and the general typed extraction contract, and their axiom-print requests are not execution evidence. [SUB250-F28-117](../research/t20-v6-20261012/sources/64aa51d9042ddee3ebb17f77887d78222d5dd65708505dc427aae390c24115c2/OpenCertificateControl.lean#L4-L20)

There is nevertheless a positive source-syntactic reconstruction for a fixed scoped input. Given Scoped 0 n and conversions of both scalarLeft(n) and scalarRight(n) to the same iterationPoly(k), sourceInstanceFromConversions types both observations by conversion from the already typed iteration, introduces their identity, and abstracts the scalar variables and type parameter to obtain HasE [] c2 (scalarInstance n). Its exact companion returns c3 applied to n at the instantiated original-Q scalar leaf. This construction makes no inference of HasE [] n N and does not need that premise for this fixed instance. It must therefore remain distinct both from replay soundness alone and from the universal source proposition W(originalQ) with a bound Church input; the source conversion, scoping and expansion interfaces are still imported. [AFTER750-F50-246](../research/t20-v6-20261012/sources/ddc7e8ad0cbb8716346530c6f2637cd20c943d7f5dbcdf7ed02726fe7e71a60e/ScalarCertificates.lean#L8-L71) [AFTER750-F50-246](../research/t20-v6-20261012/sources/ddc7e8ad0cbb8716346530c6f2637cd20c943d7f5dbcdf7ed02726fe7e71a60e/ScalarCertificates.lean#L88-L138)

The concrete positive corpus supplies explicit left and right address lists for numerals zero through six, an atom-packed numeral three, an identity-wrapped numeral four, and the input K numeral(2) Omega. Each fixed case has written conversions to the same literal iteration polynomial, joined by transitivity with the symmetric right conversion. The right application expands the original Q, and the source-instance declaration uses the displayed scope proof and both conversions to construct the corresponding instantiated scalar identity with witness c3 applied to that input. Separate equalities bind the seven numeral inputs to inputNumeral and the erased input to erasingOmegaNumeral(2). These are dependency-relative concrete declarations, not a theorem for a bound Church variable or supplied Church typing of every input. The long address literals were statically accounted rather than replayed or semantically read in full; neither they nor the axiom-print requests supply a new kernel result. [AFTER750-F50-245](../research/t20-v6-20261012/sources/ddb991de32a9c0357a2fce6922dffc5c28d359f281ea5285a6c71e2b53b7adb1/ConcreteScalarCertificates.lean#L5-L282)

The independent extraction review records additional literal-binding attacks behind this certificate interface. Replacing n while retaining certified counts and addresses makes the relevant Lean replay-success propositions false; changing the local Q to I and recomputing its digest can instead let Python certify a different local problem, but its emitted right-endpoint claim fails when rebound to the actual imported originalQ. Thus a successful local digest or conversion check does not identify the caller's intended input without that external binding. The deliberately failing commands are negative evidence, and their error-recovery sorryAx output is neither an accepted theorem nor an imported proof. The review also records a resource-handling repair: host recursion or memory exhaustion is inconclusive, and open conversion certificates omit a closed source-instance claim unless the actual closed-scope premise holds. These are reported bounded executions and corrections, not new Lean or Python runs. The extractor and finite source reconstruction remain distinct from general typability and the universal bound-variable judgment; the review's historical OPEN label for that latter question must not override the later two-sided independence already stated in §9. [AFTER3384-SIXTH25-145](../research/t20-v6-20261012/sources/0eda1bd7fa3ffbc5ce60e53ce368001b74e081f1f33f350750adf953515953b4/REVIEW.md#L13-L27) [AFTER3384-SIXTH25-145](../research/t20-v6-20261012/sources/0eda1bd7fa3ffbc5ce60e53ce368001b74e081f1f33f350750adf953515953b4/REVIEW.md#L29-L55)

A finite negative certificate can instead reject membership in the promised input domain. If replay takes the candidate's generic scalar observation to z, normalB certifies that z has no redex, and readIteration(z)=none, then the source derives that the candidate has no closed HasE typing at N. The argument combines imported uniform iteration for an assumed typing with uniqueness of normal endpoints, so it rejects precisely Church-input typing. Primitive literal zero provides a concrete empty-replay example. This partial rejection theorem neither refutes the scalar-instance identity target, recognizes every non-Church term, nor gives logical meaning to resource refusal or failed search. Its replay and standardness interfaces are imported, and these written certificate conditions are not a newly executed check. [SUB250-R81-247](../research/t20-v6-20261012/sources/7d8dea161aa5c3005b746814503f79f016452f6efaf0e74524a029d14db7f9ab/NonstandardRejection.lean#L15-L61)

This does not decide whether an arbitrary polynomial has type $`N`$, general type inhabitation, or identity at every type. Nor does it establish strong normalization. For example, let $`\Omega=(SII)(SII)`$. It reduces back to itself after finitely many steps. The polynomial $`K\overline{k}\Omega`$ converts to $`\overline{k}`$ and is therefore typed at $`N`$ by the source conversion rule. It admits an infinite reduction within its discarded argument. Its generic observation nevertheless reaches the required iteration normal form by complete development. A fixed point of the development function is not, by itself, a test that a term has no redex.

Similarly $`I`$ and $`SKK`$ both have type $`N`$ and generic count 1. They are source-identical at $`N`$, although they are distinct raw normal forms and hence not raw-convertible. A proof polynomial such as $`KI\Omega`$ can witness the same identity as $`I`$ by conversion while retaining a nonterminating subexpression. These examples separate typed identity, erased proof shape and reduction behavior. [Independent closed-fragment controls][closed-controls]

The retained Raw-context boundary review extends the observation claim in a specific direction. From HasE (rawTel m) n N it gives one count k, a source identity of n with the numeral k, and the same count after every syntactic substitution and every later open-term valuation. Admissible finite environments have a literal zero tail: the untruncated generic-variable environment is not admissible, while truncation restores the needed premise. The erased term K numeral(k) var(j), with j<m, supplies nonvacuous examples at every count. This conversion preservation is not a typing-substitution theorem: substituting var100 into the one-variable opaque input preserves its observation count while taking the endpoint outside that telescope’s scope. Reflection at a single collapsed zero valuation also fails. Nor does the result extend to arbitrary typed telescopes: a Church-typed variable cannot be source-identical to any fixed numeral, as the interpretation at the next numeral separates them. These are dependency-relative theorem bodies, not new kernel or import-closure acceptance. [research/t20-v6-20261012/sources/35f8ba45b49046e8ce0ed4d0e9c07e2f40a69e220400bf4f9eb115f2aff7392f/IndependentBoundaryChecks.lean:16–155 at ffca0abdf25079ef7639fe19776a21db60272fc4]

The structured-context source extends Raw-only uniformity to a precise syntactic class. Rigid types are Raw, Bottom, identities and universal closures of rigid bodies; opaque types are Raw, products with rigid domain and opaque codomain, sums of opaque types, their universal closures, and Bottom-domain products with arbitrary codomain. Rigid interpretations force Raw conversion, while opaque interpretations admit every convertible pair, so truncating any valuation to an opaque telescope supplies its semantic admissibility. A HasE Church term over such a telescope consequently has one generic observation count, a source identity with that numeral, and the same count after every polynomial substitution and at every open-term valuation. The identity proof closes two product extensionalities and uses type weakening for universal extensionality. This establishes neither typing of arbitrary substitutions nor uniformity for unrestricted higher-order telescope entries; all semantic and structural dependencies remain imported. [NEXT-D8-141](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/36f2333919d27087ae172190ea02820b35149827ddc76e543aae5ce542ba4203/StructuredContextUniformity.lean#L16-L86) [NEXT-D8-141](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/36f2333919d27087ae172190ea02820b35149827ddc76e543aae5ce542ba4203/StructuredContextUniformity.lean#L125-L242)

The structured-context controls make that higher-order boundary concrete. The opaque telescope [Raw→Raw, Sigma Raw Raw, Raw] admits a Church term that actually uses typed application and sum projection before erasing the result; its count is one. Opaqueness also allows a product with an identity domain mentioning a free type parameter, whose literal syntax changes under type weakening, and a Bottom-domain product with arbitrary Church codomain. But Raw→Raw is not rigid: a variable and its SKI eta expansion are related pointwise there while remaining distinct raw normal forms. Consequently a generic variable at (Raw→Raw)→Raw is not self-related, and this higher type is not opaque. A Church-typed variable supplies a separate exclusion of N itself. These are dependency-relative controls for the specified syntactic class, not uniformity over arbitrary higher-order contexts or new kernel results. [NEXT250-F25-020](../research/t20-v6-20261012/sources/8270747720fe25a7c57bf9f19bf0d7d07026988015badf20518cc4ffe5b0b502/StructuredContextControls.lean#L13-L102) [NEXT250-F25-020](../research/t20-v6-20261012/sources/8270747720fe25a7c57bf9f19bf0d7d07026988015badf20518cc4ffe5b0b502/StructuredContextControls.lean#L104-L168)

The independent structured controls separate opacity from both formation and individual observations. The syntactically opaque product Pi (Id_Raw(var100,var100)) Raw is not formed in the empty source context. Conversely the Church variable in the nonopaque context [N] has its reflexive source identity; this supplies no fixed-numeral observation or characterization of OpaqueTel. The excluded higher type (Raw->Raw)->Raw forms a source context and has the closed inhabitant K I, even though its generic-variable environment is inadmissible. Thus the higher-order boundary is not an emptiness claim. A further rigid identity can have endpoints related in RawEnd but not raw-convertible: its rigidity concerns proof representatives. These are dependency-relative source/semantic controls, not a new formation algorithm or an executed validation. [L34-130](../research/t20-v6-20261012/sources/ff78ba61a388f4911bf3c9b22fec5cfe5fae1b4906cfafff96d0168ce681298d/IndependentStructuredChecks.lean#L53-L75) [L34-130](../research/t20-v6-20261012/sources/ff78ba61a388f4911bf3c9b22fec5cfe5fae1b4906cfafff96d0168ce681298d/IndependentStructuredChecks.lean#L141-L170)

## 7. Why simple separating proposals fail

The positive closed theorems do not prove $`W(q)`$ with a bound variable $`n:N`$. Conversely, finding a nonstandard operation that separates two untyped evaluations does not automatically produce a countermodel of $`E`$. The operation must preserve every relation required by its Church type, and the interpretation must validate every source rule.

### 7.1 The same program can have two carrier typings

For a formed type $`B`$, define the nondependent product and Church pair carrier

```math
P_B=\Sigma x:B.B,
\qquad C_B=(B\to B\to B)\to B.
```

These are different type expressions. Nevertheless the *same* polynomial $`\langle a,b\rangle=S(SI(Ka))(Kb)`$ has both types whenever $`a,b:B`$ are supplied in the original base judgment. The sum introduction rule gives its $`P_B`$ typing. For the $`C_B`$ typing, put $`L=B\to B\to B`$. Then $`I:L\to L`$, $`Ka:L\to B`$ and $`Kb:L\to B`$. Two instances of the typed $`S`$ rule give

```math
SI(Ka):L\to(B\to B),
\qquad S(SI(Ka))(Kb):L\to B.
```

For a generic $`n:N`$ and $`a,b:B`$, let

```math
u=\langle a,a\rangle,
\qquad d=K\langle b,b\rangle,
\qquad o=(ndu)K.
```

Instantiate $`n`$ first at $`P_B`$. The seed has that type, the step is its constant endomorphism, and applying the first projection gives $`o:B`$. Instantiate $`n`$ instead at $`C_B`$. The literal seed and step again have the required types; applying their result to the selector $`K:B\to B\to B`$ gives the **same** polynomial judgment $`o:B`$. Identity introduction therefore gives $`I:\mathrm{Id}_B(o,o)`$ with the endpoints typed through the two routes. No isomorphism between carrier types, conversion between their outer constructors, or general naturality principle was used.

The observer converts to $`a`$ when $`n=\overline{0}`$ and to $`b`$ when $`n=\overline{1}`$: the first computation returns the seed and projects its first component; the second returns the constant step value and projects its first component. Thus an interpretation that assigns a single coherent value to this judgment cannot choose zero iteration at the product carrier and one iteration at the Church pair carrier when $`a,b`$ have distinct observations. Reversing the two choices fails for the same reason. Matching zero choices or matching one choices pass. The conclusion is conditional on coherence of these two computations of this exact judgment; it is not a theorem of unrestricted naturality. [Both source typings and observer controls][cross-typing]

The cross-typing controls preserve a genuinely dependent carrier: for B=Id_α(var0,var0), the second Product component uses var1 after weakening, not the unshifted B. They type the same expanded observer through both the sum and Church routes and retain its source identity. The companion unshifted-product assertion is a contrary control, not an accepted equation. Bare unary carrier membership alone still permits incompatible observations, and a singleton value carrier hides the distinction. More sharply, this constant-step observer distinguishes zero from positive iteration but not different positive counts: iterations one and two have the same observation. Coherence of this one observer therefore does not force equality of arbitrary iteration counts or supply a whole-source model. [SUB250-C20-026](../research/t20-v6-20261012/sources/531d1d056f5cd5611c9716439f5a3c22214a24060419aa20aeede4c73203f640/CrossReviewControls.lean#L9-L97) [SUB250-C20-007](../research/t20-v6-20261012/sources/4d8f77dd8383213f277300693cdf988652c769ff3690ea589d17fee4c82a8224/RejectUnshiftedProduct.lean#L1-L4)

This rules out a simple type-shape assignment. It does not rule out the later countermodel, whose term interpretation is independent of typing derivations: both literal pair seeds are function-shaped, so the same semantic iterator takes one step under either typing.

The independent typed-family controls distinguish the premises behind a related observer obstruction. Constant-body reintroduction can be compositional while failing the erased-cycle equation; identity reintroduction can satisfy the cycle while failing compositional assembly. A coherent constant contract alone is consistent: the varying zero/one candidate fails only with the separate observer-body assembly obligation and a distinguishing pair of values. An identity update or a singleton value carrier makes that variation invisible, while constant-zero and constant-one candidates assemble. The dependent typing examples separately shift outer type and term coordinates, rather than silently treating a dependent carrier as closed. [B141-014](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/0396367472a3230fbe3f4ac4d9d5590f41fd3acabd6b7361b4bb73d7eab42fac/IndependentControls.lean)

The actual source controls behind that family comparison keep the unannotated judgment fixed. With ConstantAll=All Raw, the variable at that type can be instantiated at the formed Raw type and reabstracted, returning literally the same context, polynomial and type; identity introduction compares its direct and reabstracted typings. With Discriminator=All(α→Raw), the unchanged grammar permits self-instantiation at Discriminator and types the diagonal application var0 var0 at Raw. These are formed, source-typed examples of erasure and impredicative self-application, not an untyped surrogate, a general inconsistency proof or a construction of the disputed family semantics. [NEXT-R18-225](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/4585df3f78ef14f329c1bf9fad7d5d4390915a7d6a77a15a4f7785ced8ac7262/SourceControls.lean#L8-L64)

The general typed structured observer holds an arbitrary formed source carrier B fixed by genuine type weakening. Its carrier is Σ B.(α₀→α₀), its seed pairs a with I, and its step pairs f applied to the first projection with I. Original Has typings of n:N, f:B→B and a:B yield the run at that carrier and its first projection at B. Moving to the type-weakened telescope gives that same observer at twk(B), so universal introduction yields All(twk(B)); elimination at any formed type T recovers exactly B by tinst_twk. The direct and specialized typings consequently give a same-endpoint HasE identity, without equating carrier types or assuming unrestricted naturality. The general re-abstraction cycle likewise starts from p:All(twk(B)), eliminates to B, then weakens and reintroduces. Its concrete check shifts outer parameter zero to parameter one and recovers the original parameter on specialization. Thus this is not the invalid claim that All(B) leaves a possibly dependent B fixed by definition. All typing and substitution claims remain relative to the imported original structural interfaces. [NEXT250-E25-186](../research/t20-v6-20261012/sources/a30aeab8990230bf9502737509f8e5ee0aaf120f0cbebe83826c6cb5f9d68d88/TypedObserver.lean#L11-L72) [NEXT250-E25-186](../research/t20-v6-20261012/sources/a30aeab8990230bf9502737509f8e5ee0aaf120f0cbebe83826c6cb5f9d68d88/TypedObserver.lean#L74-L107) [NEXT250-E25-186](../research/t20-v6-20261012/sources/a30aeab8990230bf9502737509f8e5ee0aaf120f0cbebe83826c6cb5f9d68d88/TypedObserver.lean#L109-L123)

The associated ordinary set-family obstruction leaves a restricted model fragment intact. Reabstracting f at r gives the constant family i↦f(r), so coherence requires f(i)=f(r) for every i. Unrestricted Boolean families fail, but the coherent constant-family carrier is equivalent to R and can be nontrivial. A structured observer is uniform across instances only when its assembled result belongs to that carrier and is separately identified with the displayed observer body. A different diagonal argument restricts impredicative decoding: for ev:D→D→R and a fixed-point-free flip, x↦flip(ev(x)(x)) is outside the image of ev. Distinct values in R supply such a flip. Consequently an equivalence El(d)≃∏ᵢ(El(i)→R) is impossible, because its d-component would expose every function El(d)→R. Every set-sized Henkin decoder for this discriminator must omit some self-function. These are conditional ordinary family semantics, not a model of all HasE constructors, an axiom added to HasE, or an inconsistency proof for the source calculus. [SUB250-R17-072](../research/t20-v6-20261012/sources/5c4055c5238d8c321e7f2695eaaad13d8ca3f2cb2b609bca571c8cf726f3d345/FamilyObstructions.lean#L9-L81) [SUB250-R17-072](../research/t20-v6-20261012/sources/5c4055c5238d8c321e7f2695eaaad13d8ca3f2cb2b609bca571c8cf726f3d345/FamilyObstructions.lean#L85-L138)


### 7.2 Strict iterators fail a source-definable arrow test

The following failed constructions identify a real obstruction rather than merely unsuccessful search attempts. Assume one applicative carrier with ordinary combinatory equations, an absorbing element $`\perp`$ satisfying $`\perp x=\perp`$, and $`I\ne\perp`$. For this attempted interpretation, let Raw equality be genuine equality and let the reflexive identity $`R=\mathrm{Id}_{\mathrm{Raw}}(I,I)`$ have the single proof class represented by $`I`$.

Consider two operations, each using one shared application operation:

```math
\nu_1(f,a)=
\begin{cases}
\perp,&a=\perp,\\
fa,&a\ne\perp,
\end{cases}
\qquad
\nu_0(f,a)=
\begin{cases}
\perp,&f=\perp,\\
a,&f\ne\perp.
\end{cases}
```

Both pass the unit probe: $`\nu_i(I,I)=I`$. Their availability as carrier elements is generously granted for this test; the failure occurs even with that grant.

Let $`U=R\to\mathrm{Raw}`$ and $`g=[r]r\perp`$. Then $`gI=\perp`$, so $`g`$ and $`\perp`$ are related at $`U`$. Globally they differ, since $`g(KI)=I`$. Also $`I`$ belongs to $`U`$ but is not $`U`$-related to $`\perp`$, because their outputs on $`I`$ differ.

For $`\nu_1`$, take the $`U`$-endomorphism $`F=KI`$ and related seeds $`\perp,g`$. The outputs are

```math
\nu_1(F,\perp)=\perp,
\qquad \nu_1(F,g)=I,
```

which are not related at $`U`$. Thus $`\nu_1`$ fails the Church arrow relation on a carrier that the source itself can form.

For $`\nu_0`$, take endomorphisms $`F=\perp`$ and $`G=Kg`$. They are related at $`U\to U`$ because their constant outputs $`\perp,g`$ are $`U`$-related; $`G`$ is globally nonbottom. At the same seed $`I:U`$,

```math
\nu_0(F,I)=\perp,
\qquad \nu_0(G,I)=I.
```

This violates preservation of the endomorphism argument. Neither operation belongs to the proposed interpretation of $`N`$.

These candidates would have separated the compiler if they had been admissible. First, $`zII=I`$ shows $`z\ne\perp`$: an absorbing bottom would still give bottom after both applications. Since $`\pi_1z_0=z`$, the seed $`z_0`$ is also nonbottom. The step needs a separate argument. The pair-state equation gives $`\Delta z_0=\langle sz,sz\rangle`$, and $`(sz)II=I`$ shows that $`sz`$ is nonbottom. Thus $`\pi_1(\Delta z_0)=sz`$ is nonbottom. If $`\Delta=\perp`$, absorption would instead give $`\pi_1(\Delta z_0)=(\perp z_0)K=\perp`$, a contradiction.

Now $`\nu_1(\Delta,z_0)=\Delta z_0`$, so $`q\nu_1`$ behaves as Church one, while $`\nu_1(KI,\perp)=\perp`$; the compiled observation gives $`I`$. Because the step is nonbottom, $`\nu_0(\Delta,z_0)=z_0`$, so $`q\nu_0`$ behaves as Church zero, while $`\nu_0(\perp,I)=\perp`$; the compiled observation again gives $`I`$. These are conditional separation calculations for the proposed operations. Their failure is membership in the required Church relation, established above.

A global definedness tag would deny equality of $`g`$ and $`\perp`$ at $`U`$, but the extensionality premise remains inhabited. At every supported $`r:R`$, both $`gr`$ and $`\perp r`$ equal $`\perp`$ at Raw. Their identity fiber therefore has the proof class of $`I`$ as support, and the constant section $`KI`$ supplies that proof at every such argument. In a semantic context assigning the two function variables to $`g,\perp`$ and their pointwise-proof variable to $`KI`$, these values satisfy the typed pointwise identity premise. The actual product-extensionality rule then requires identity of the functions at $`U`$. A definedness tag that preserves their individual membership but rejects this conclusion invalidates that rule; ordinary pointwise agreement was not being substituted for its proof premise. No new source constant for $`\perp`$ is asserted by this semantic instance.

Collapsing $`I`$ with $`\perp`$ at Raw would instead remove the separating observation. These are diagnoses of these particular constructions, not a proof that every separating model or every refinement of a semantic relation is impossible. [Complete failed-route argument][failed-routes]

## 8. A concrete homogeneous-PER countermodel

The successful construction changes the semantic universe openly and proves all the necessary closure and soundness obligations. It uses one erased application operation and one term interpretation for every source expression.

### 8.1 A finite-term applicative carrier

Let $`D_h`$ consist of finite **closed** application trees over $`I,K,S,a_0,a_1,\nu`$. The symbols $`a_0,a_1`$ are distinct inert atoms. The new semantic combinator $`\nu`$ is not a new source constant or source conversion rule.

<a id="baseline141-finite-reachable-raw-summary"></a>

Finite terms should not be confused with a finite summary carrier. The independent raw-image source shows that a finite-valued summary of all raw terms is constant when it respects conversion and computes every application by one binary operation. Restricting to values actually denoted by terms removes any need for surjectivity onto the whole carrier: unreachable junk may remain. Its partial-application variant still collapses a finite carrier when every K-first application and every resulting constant application is defined. A nonconstant syntax-shape summary supplies the complementary control: it is compositional but does not respect conversion. Bounded or restricted syntax and summaries lacking one of these hypotheses are outside the obstruction; the imported raw-image theorem has not been recompiled here. [Exact source](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/0959e43472eeea9f704a4ed36981299e74a78ad8cf1788845ad067ad44cbe6b6/IndependentControls.lean#L10-L104)

The exact two-Raw-variable source bridge distinguishes this carrier obstruction from unary membership soundness. A compositional interpretation with total application and equality-valued soundness for typed Raw conversions makes the existing K conversion give app(app(k,x),y)=x for arbitrary carrier elements. Invoking the imported finite-K theorem then makes a finite whole Raw carrier subsingleton and a nontrivial one infinite. Bool therefore cannot be that entire carrier, although this says nothing against a Bool typed subcarrier inside an infinite Raw model. The displayed Unit interpretation satisfies this Raw-only contract; it is not a model of all HasE. These are dependency-relative source arguments, not a fresh check of the finite-K dependency. [NEXT-D8-23](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/1f6f831f54f3331c3d8212ba271f5a25af838fd38ad28ba0ee9f9975a549d4b4/SourceRaw.lean#L11-L93)

The finite-K obstruction itself needs only a total application operation and app(app(k,x),y)=x. The map x↦app(k,x) is injective: apply a proposed equality to k and use the K law. If app(k,a)=k, that same law makes app(k,x)=a for every x, so injectivity collapses the whole carrier. On a finite carrier injectivity gives the required preimage of k; hence the carrier is a singleton, and every nontrivial total-K carrier is infinite. The one-point Unit model attains the finite boundary. No I or S law, extensionality, source typing, impredicative universe or full function space is used in this elementary argument; its formal finite-cardinality facts are imported, with no fresh kernel run asserted. [A750-F50-019](../research/t20-v6-20261012/sources/b18a927e8c3584924d076b8b7107d58974504f7bae1ee4e8849ef13872677e87/FiniteK.lean#L9-L56)

The finite-Raw dependency audit distinguishes an axiom closure from a declaration-value graph. For its four finite-K and raw-denotation roots it permits only propext, Classical.choice and Quot.sound, then traverses declaration bodies with a 100000-step bound while excluding I/S reduction, the atom/application bridge, universal rules, typed extensionality and J. The RawDenotation.toTotalK root must still reach rawAtom, rawApp, var and the K conversion. A grammar appearing in a theorem type is therefore not counted as use of every rule in its proof. These are authored inspection requirements, not obtained PASS logs, proof compilation or an audit of arbitrary native dependencies. [NEXT250-S25-026](../research/t20-v6-20261012/sources/8489fcdd1439930492a711242f144a14fe0da7aef660dd7817f2b7aa36a69a0c/DependencyAudit.lean#L7-L23) [NEXT250-S25-026](../research/t20-v6-20261012/sources/8489fcdd1439930492a711242f144a14fe0da7aef660dd7817f2b7aa36a69a0c/DependencyAudit.lean#L25-L65)

Besides the three SKI rules, use

```math
\nu f a_0\longrightarrow a_0,
\qquad \nu f a_1\longrightarrow a_1,
```

and $`\nu f v\longrightarrow fv`$ for each of the eight function shapes

```math
v=I,\ K,\ Kx,\ S,\ Sx,\ Sxy,\ \nu,\ \nu x.
```

This is a thirteen-rule first-order rewrite system. The variables in a function shape stand for arbitrary finite terms, which may themselves contain redexes. A function shape is a weak-head shape, not an assumption of full normality.

Write $`\approx`$ for compatible conversion in this enlarged system. Define two classes:

```math
\mathrm{At}(t)\quad\Longleftrightarrow\quad
t\approx a_0\ \text{ or }\ t\approx a_1,
```

```math
\mathrm{Fn}(t)\quad\Longleftrightarrow\quad
t\approx v\ \text{for one of the eight function shapes }v.
```

**Lemma 7 — operational properties.** The enlarged reduction is confluent; $`a_0\not\approx a_1`$; the two classes are disjoint; and

```math
\mathrm{At}(ta)\ \text{or}\ \mathrm{Fn}(ta)
\quad\Longrightarrow\quad \mathrm{Fn}(t).
```

**Proof.** The root patterns are left-linear and nonoverlapping, and none has a proper nonvariable subpattern that is itself an active root. There is also a direct parallel-development proof for this specific system. Let parallel reduction reduce corresponding subterms simultaneously and optionally contract an initially present root redex. Define the complete development by the matching root rule, developing each surviving subterm; otherwise develop the application's two children.

Induction on a parallel step proves that every parallel reduct of $`t`$ reduces in parallel to this same complete development. For $`S`$, duplicated arguments use the same developed argument. For a $`\nu`$ function case, reductions inside the shape preserve its head and arity, so the same case rule remains applicable. The two atom cases remain fixed. If a root was not initially a case redex, the triangle argument may retain that root and use congruence; it need not contract a newly created case redex. Thus parallel reduction has the diamond property. Its reflexive transitive closure is confluent, and ordinary compatible reduction has the same closure. Conversion therefore implies a common reduct.

The inert atoms have no reduct other than themselves, so common-reduct existence proves their inequivalence. Every reduct of a function shape retains a function shape. Therefore an atom cannot be convertible to a function shape.

For the last assertion, join $`ta`$ with the atom or function shape to which it converts. The latter's reduct remains a value shape. In a reduction from an application to such a shape, consider the first root contraction. Its left prefix is necessarily $`I`$, $`Kx`$, $`Sxy`$ or $`\nu f`$, hence a function shape. If no root contraction occurs, the final application is itself a partial function shape, whose left prefix is again a function shape. Tracking the preceding reductions of the left child proves that the original $`t`$ converts to a function shape. This uses finite reduction and confluence; no head-normalization or standardization theorem is assumed. $`\square`$ [Concrete operational proof][case-operational]

The usual orthogonality theorem explains the rewriting pattern, but the formal source also proves the parallel-development argument rather than assuming a confluence contract. The cited literature's PVS formalization has its own stated axiomatization boundary; it is not being represented as the kernel certificate for this construction. [Orthogonal rewriting][orthogonal]

Saturation of the case equations gives

```math
\mathrm{At}(a)\Rightarrow\nu fa\approx a,
\qquad
\mathrm{Fn}(a)\Rightarrow\nu fa\approx fa.
```

### 8.2 A universe closed under the actual type constructors

Let $`\mathcal U`$ consist of every $`\approx`$-saturated PER $`R`$ on $`D_h`$ satisfying at least one of the following:

1. $`R=\top`$, the universal relation.
2. Every supported element of $`R`$ lies in $`\mathrm{At}`$.
3. Every supported element of $`R`$ lies in $`\mathrm{Fn}`$.

The empty relation is included. This is a set of all relations with the stated property, defined independently of source syntax. It is not a finite list of test types, nor a family chosen afresh for each source derivation.

**Lemma 8 — universe closure.** The universe contains empty and universal relations, identity proof relations, arbitrary intersections, dependent products, and dependent sums formed from coherent families in $`\mathcal U`$.

**Proof.** Empty and universal relations satisfy the definition directly. A proposition-guarded conversion class of $`I`$ is empty when its guard fails and function-supported when it holds. This includes the interpretation of every identity type.

An arbitrary intersection is a saturated PER. If all factors are universal, so is the intersection, including the empty intersection. Otherwise choose a nonuniversal factor. Every supported point of the intersection is supported by this factor and therefore lies in its one homogeneous class.

For products, use the relation $`\Pi(A,B)`$ of section 5. The PER laws require $`A(a,b)\Rightarrow B(a)=B(b)`$ and the PER laws of each supported fiber; their proofs are the ones already given. If every supported fiber is universal, the product is universal. Otherwise choose a supported $`a`$ whose fiber is nonuniversal. If $`\Pi(A,B)(f,f)`$, then $`B(a)(fa,fa)`$. The fiber is atom-supported or function-supported, so Lemma 7 forces $`\mathrm{Fn}(f)`$. Thus the product is function-supported.

The chosen fiber must lie over a supported argument. An empty domain gives a universal product even if every fiber away from the support is empty. With the ordinary $`K`$ equation, the characterization is exact: a universal product forces every supported fiber to be universal, because applying it to the constant functions $`Kc,Kd`$ yields $`B(a)(c,d)`$ for arbitrary $`c,d`$.

For sums, use the actual projection relation $`\Sigma(A,B)`$, with no requirement that every supported term literally have a pair constructor. If $`A`$ is nonuniversal, a supported $`z`$ has its first projection in one homogeneous class. Since $`\pi_1z=zK`$, Lemma 7 forces $`\mathrm{Fn}(z)`$. If $`A`$ is universal, coherence forces all fibers to be the same relation. If that relation is universal, the sum is universal. Otherwise its second projection lies in one homogeneous class, and $`\pi_2z=z(KI)`$ again forces $`\mathrm{Fn}(z)`$. The sum's symmetry, transitivity and saturation follow by transporting the second component along equality of fibers. $`\square`$ [General closure proof][homogeneous] [Concrete instantiation][universe]

Two finite controls show that these hypotheses are substantive. First, on $`\{0,1,2\}`$ define selectors $`\pi_1z=z0`$ and $`\pi_2z=z1`$. Let application by 1 return 1 on 0 and 0 otherwise, and let application by 0 or 2 return 2. These are arbitrary selectors for this test; no combinatory laws are imposed. Set $`\mathrm{At}=\{0\}`$, $`\mathrm{Fn}=\{1\}`$ and use equality conversion. Application has the strictness property of Lemma 7. Let the domain be universal and let the fiber at 1 be universal while the other fibers are empty. Every fiber is individually eligible, but the family is not coherent. The projection relation relates 1 to 0 and does not relate 0 to 1, so it is not a PER.

Second, on the same three-element set let application by 0 or 1 always return 0 and application by 2 always return 2. Keep equality conversion and the same two classes. Let the domain and each fiber be the singleton PER on 0. The product supports both 0 and 1 but not 2: it is neither universal nor homogeneous. Application strictness fails, since applying 0 produces an atom although 0 is not a function. These small structures test the closure lemmas' hypotheses; they are not proposed combinatory models of the source calculus. [Closure controls][closure-controls]

### 8.3 The semantic Church witness is inhabited

Interpret $`N`$ by quantifying over all of $`\mathcal U`$ using the same arrow relation as before.

**Lemma 9.** The single element $`\nu`$ belongs to this Church interpretation.

**Proof.** Let $`R\in\mathcal U`$, let $`f,g`$ be related $`R`$-endomorphisms and let $`R(a,b)`$. If $`R`$ is universal there is nothing to prove. If $`R`$ is atom-supported, both seeds lie in $`\mathrm{At}`$; the case equations give $`\nu fa\approx a`$ and $`\nu gb\approx b`$, and saturation preserves $`R(a,b)`$. If $`R`$ is function-supported, the outputs convert to $`fa,gb`$, which are related by the endomorphism hypothesis. Therefore

```math
R(\nu fa,\nu gb)
```

in every case. The same $`\nu`$ and the same application operation serve every relation. $`\square`$

This argument includes instantiations at $`N`$ itself, dependent pair types, and every other eligible formed type. Closure under arrows and intersection also proves that the Church relation itself lies in $`\mathcal U`$. There is no empty-domain surrogate for a Church witness.

### 8.4 Soundness of the whole calculus in the restricted universe

Interpret the actual source polynomials compositionally in $`D_h`$, mapping the source's inert constants to $`a_0,a_1`$. Interpret products, sums and identities exactly as in section 5, now with $`\approx`$ and universal quantification over $`\mathcal U`$. The essential change is

```math
\mathopen{\lbrack\!\lbrack}\mathrm{Raw}\mathclose{\rbrack\!\rbrack}_h=\top.
```

Here a type valuation $`\rho`$ is **admissible** exactly when $`\rho(\alpha)\in\mathcal U`$ for every type parameter. Define $`\mathrm{Supp}^{h,\rho}_{\Gamma}`$ and $`\mathrm{Rel}^{h,\rho}_{\Gamma}`$ by the same context recursion as in section 5.4, using the present interpretation $`\mathopen{\lbrack\!\lbrack}-\mathclose{\rbrack\!\rbrack}_h`$ and the constant $`a_0`$ default environment. Thus context support and relatedness concern this carrier and its eligible relations; they are not inherited from the different full-PER model.

**Theorem 10 — homogeneous source soundness.** Let $`\rho`$ be admissible for $`\mathcal U`$. For each formed source context $`\Gamma`$, $`\mathrm{Rel}^{h,\rho}_{\Gamma}`$ is a PER with support exactly $`\mathrm{Supp}^{h,\rho}_{\Gamma}`$. If $`A`$ is formed over $`\Gamma`$ and $`\mathrm{Supp}^{h,\rho}_{\Gamma}(\eta)`$, then $`\mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}^h_{\rho,\eta}\in\mathcal U`$, so it is a saturated PER. At context-related $`\eta,\xi`$, the interpretations of the formed type are equal. For every actual derivation $`\Gamma\vdash_E p:A`$ and every $`\mathrm{Rel}^{h,\rho}_{\Gamma}(\eta,\xi)`$, we have

```math
\mathopen{\lbrack\!\lbrack} A\mathclose{\rbrack\!\rbrack}^h_{\rho,\eta}
  (\mathopen{\lbrack\!\lbrack} p\mathclose{\rbrack\!\rbrack}^h_\eta,\mathopen{\lbrack\!\lbrack} p\mathclose{\rbrack\!\rbrack}^h_\xi).
```

No formation, coherence or typing conclusion is asserted for valuations outside $`\mathcal U`$ or for term environments unsupported by the relevant context.

**Proof.** Repeat the simultaneous context, formation and typing induction of Theorem 5 with these admissible valuations and context relations, now adding universe membership at supported environments to the formation conclusion. Lemma 8 supplies the product, sum, intersection and identity cases. The polynomial and mixed type/term substitution identities still hold, since interpretations are compositional and the quantifier universe is fixed independently of types.

Every source constructor is covered. Variables, the three combinators, product introduction/elimination and the three sum rules use the same lookup, beta, projection and substitution arguments. The source's eight conversion generators are sound: the seven combinatory/congruence/equivalence forms use $`\approx`$, and atom packing is compositional equality. Universal introduction ranges over every eligible relation. Universal elimination uses the actual formation induction to show that its instantiated type is eligible. The finite-import proof separately covers all seven underlying finite constructors and interprets unused type-image coordinates by the empty eligible relation.

Identity introduction uses conversion soundness and typed endpoints. Identity evidence still has support in the conversion class of $`I`$, although Raw is universal. Raw atoms, Raw application and proof erasure are therefore valid. Identity elimination uses the actual two-coordinate motive context: endpoint relatedness and proof conversion to $`I`$ make the extended environments related; formation coherence transports the base fiber; the literal $`J`$ term converts to its base proof. Product extensionality combines its pointwise identity with the typing of the second function to cover heterogeneous related arguments. Universal extensionality takes the endpoint relation at every eligible type instance. Proof conversion preserves the same formed target by saturation.

The empty term context has a fixed default environment, for example the constant $`a_0`$ environment, and the empty type environment assigns the empty eligible PER to each parameter. Thus closed soundness has an actual input environment. Formation eligibility, family coherence and the fundamental theorem are conclusions of induction on the unchanged source grammar. They are not assumptions placed on a model that already presupposes the theorem. $`\square`$ [Whole homogeneous soundness proof][henkin-soundness] [Original term interpretation and transport][henkin-transport]

### 8.5 Separation of the literal compiler

Let $`R_a`$ be the discrete atom PER:

```math
R_a(x,y)\quad\Longleftrightarrow\quad
x\approx y\ \text{ and }\ \mathrm{At}(x).
```

It is a saturated, atom-supported PER. Take $`f=Ka_1`$ and $`a=a_0`$. This $`f`$ is an $`R_a`$-endomorphism, and $`a_0`$ is a supported seed.

The left scalar observation is

```math
\nu(Ka_1)a_0\approx a_0.
```

The original pair seed $`z_0=\langle z,z\rangle`$ has the function shape $`Sxy`$. Hence the same $`\nu`$ takes one step on the pair representation:

```math
\nu\Delta z_0\approx\Delta z_0
\approx\langle sz,sz\rangle.
```

The exact compiler equation then gives

```math
q\nu\approx sz,
\qquad(q\nu)(Ka_1)a_0\approx a_1.
```

The two outputs are not $`R_a`$-related, because $`a_0\not\approx a_1`$ by Lemma 7. This computation is bound to the original compiled $`q`$ by source transport, not merely to an unverified formula mirror. [Exact literal counterexample][counterexample]

**Theorem 11 — nonderivability.** For every source polynomial $`r`$,

```math
\nvdash_E r:W(q),
\qquad\nvdash_E r:\mathcal B.
```

**Proof.** If a pair of semantic proof realizers inhabited $`W(q)`$, instantiate its outer product at the actual semantic Church member $`\nu`$, its universal parameter at $`R_a`$, and its scalar arguments at $`Ka_1,a_0`$. The identity leaf would require the two displayed outputs to be $`R_a`$-related, a contradiction. Thus $`W(q)`$ has no semantic realizers in this model. Theorem 10 excludes every source derivation of that type, including one using the fixed polynomial $`c_3`$.

An arbitrary proof of $`\mathcal B`$ would yield $`c_3:W(q)`$ by Theorem 3 and the compiler's actual base typing. This contradicts the first conclusion. $`\square`$ [Universal scalar noninhabitation][noninhabitation] [Literal identity consequence][identity-negative]

This is a proof about all finite derivations of the unchanged grammar. It does not conclude nonderivability from a rejected elaboration, a changed carrier, a changed endpoint or a bounded search.

### 8.6 Why the universe restriction and Raw choice matter

The countermodel must not be described as a counterexample to full-PER standardness. Its universe excludes proper relations with mixed atom and function support.

For an explicit excluded relation, put $`j=Ka_0`$. Let one equivalence class be the union of the conversion classes of $`a_0`$ and $`I`$, and let a second be the conversion class of $`j`$. These classes are disjoint. An atom cannot be convertible to $`j`$, which is function-shaped. Also $`I\not\approx j`$: applying a hypothetical conversion to $`a_1`$ would give $`a_1\approx a_0`$. Their two-class relation $`R_m`$ is a proper saturated PER, and $`R_m(a_0,I)`$.

The constant function $`Kj`$ is an endomorphism of $`R_m`$. But

```math
\nu(Kj)a_0\approx a_0,
\qquad\nu(Kj)I\approx j,
```

and those outputs belong to different classes. Thus this ordinary mixed PER rejects $`\nu`$ as a Church member. It is unavailable in $`\mathcal U`$ for precisely the stated homogeneity reason. The restriction has mathematical force. [Mixed-PER control][mixed-control]

Raw must be universal in this universe. The source raw-atom rule supplies both $`a_0`$ and $`I`$ as supported Raw values. A relation in $`\mathcal U`$ with both supports cannot be atom-supported or function-supported, by disjointness; it must be universal. In particular ordinary conversion is not eligible, because it would then equate $`a_0`$ and $`a_1`$.

A separate faithful-Raw control rejects this particular nu even without the mixed relation above. I and SKK are related as endomaps of raw conversion, since both act as identity, although their unapplied normal forms differ. The stuck seed a0 a0 is normal and has neither the atom-value nor function-value tag. None of the nu case rules applies to that seed, so nu I (a0 a0) and nu (SKK) (a0 a0) are distinct normal forms. The imported confluence/join property therefore excludes conversion between them. Quantifying the Church contract over conversion itself would require just that conversion, and consequently excludes this nu. This is a diagnostic of the displayed operational witness, not a universal impossibility theorem for all Raw-faithful models or a new execution result. [A750-F50-042](../research/t20-v6-20261012/sources/b6bcdd52139974a5fe592b36d41153bc9fd4cb61fa1b8a536c8a328706f73c2e/FaithfulRawControl.lean#L11-L24) [A750-F50-042](../research/t20-v6-20261012/sources/b6bcdd52139974a5fe592b36d41153bc9fd4cb61fa1b8a536c8a328706f73c2e/FaithfulRawControl.lean#L26-L88)

This is an alternative sound interpretation for proving a source-nonderivability result. It does not replace the faithful Raw interpretation, refute scalar fusion there, or assert that every semantic Church element is denoted by a source polynomial. The extra semantic value $`\nu`$ is exactly why universal source proof is more demanding than the collection of closed source instances.

## 9. Independence, proof systems and the remaining boundaries

### 9.1 Neither the identity nor its internal negation is derivable

Define the internal negation of a type $`A`$ as $`A\to\bot`$.

**Theorem 12 — syntactic independence.** Neither $`W(q)`$ nor $`\mathcal B`$ has a closed $`E`$ inhabitant, and neither internal negation has a closed $`E`$ inhabitant.

**Proof.** The positive types are excluded by Theorem 11. In the full-PER model of section 5, $`W(q)`$ is inhabited by the interpretation of $`c_3`$ and $`\mathcal B`$ by $`I`$. If $`r:A\to\bot`$ were a closed source derivation for either type $`A`$, soundness would make its interpretation an arrow from a relation with a supported element to the empty relation. Apply that arrow to the related pair consisting of the chosen inhabitant twice. Its result would belong to the empty relation, a contradiction. $`\square`$ [Complementary no-negation control][identity-control] [Scalar no-negation proof][no-negation]

The two parts use different sound interpretations. The homogeneous interpretation refutes the positive type; the faithful full-PER interpretation refutes a derivation of its negation. The conclusion is external nonderivability in both directions. It is not an internal proof of negation, a contradiction in the calculus, or an assertion that the arithmetic equation $`x+0=x`$ is false.

### 9.2 Closed completeness does not supply universal induction

For every supplied closed $`n:N`$, section 6 gives a finite proof of the substituted scalar body of $`W(q)`$. Theorem 11 proves that no single source proof inhabits the outer product over a generic $`n:N`$. There is no conflict:

```math
\text{for each closed derivation }\vdash_E n:N,
\text{ construct a proof of }P(n)
```

is a statement in the surrounding mathematics, whereas

```math
\vdash_E h:\Pi n:N.P(n)
```

is one particular finite derivation in the source calculus. The latter must act on every semantic member of $`N`$ in every sound interpretation, including $`\nu`$ in the homogeneous model. Closed canonicity characterizes supplied source terms; it does not characterize every member of every possible Henkin interpretation.

Similarly, a graph invariant on a represented pair state does not by itself yield the scalar projection-fusion law. In the countermodel, the pair state is function-shaped and triggers one step, while the external atom seed triggers zero steps. Any proposed graph-to-scalar bridge must discharge that exact typed obligation. Passing the unit probe, preserving one state invariant, and using a single shared application operation are useful controls, but none alone establishes the missing bridge.

The retained GraphBridgeAssembly source states the conditional converse precisely. Given both typed HasE judgements stateTransport and scalarTransport in the displayed scalar context, typed J supplies observer congruence, identity composition and left-endpoint replacement. It assembles the original scalar leaf, converts its supplied identity evidence to literal I, and abstracts to the unchanged c3 at W(originalQ). Neither bridge is inhabited in that source. Converting an existing typed identity witness to I therefore does not create the missing identity premise or prove unconditional scalar fusion. [B141-067](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/0dd6090f8cde9debb2bb58b921bac52c9bd6dd058cece3d2b09fc8f501d1b8e3/GraphBridgeAssembly.lean)

The independent internal-graph controls give positive computations on the other side of that boundary. Erasing the two J evidence terms leaves the scalar update f applied to the previous scalar component; it does not erase that scalar action. The literal graph step remains typed after adding a genuinely dependent graph binder over the open iterator and seed. At input numeral zero, both state and scalar projections compute and the graph run has the displayed graph type. These zero-instance and nested-typing facts do not supply the two generic projection identities required by the assembly theorem. [research/t20-v6-20261012/sources/3a26ba10146c8375caab832b040c9b1f3d95081cda4fcd66c70712a2948009bd/IndependentControls.lean:12–85 at ffca0abdf25079ef7639fe19776a21db60272fc4]

The general internal graph construction preserves a precise dependent invariant. Graph(f,a) packages a state s:S, a separate scalar x:A and evidence of x=image(f,a,s), where image applies the second state coordinate to f and a. Its lifted step updates s by diagonalStep and x by f; source J transports the supplied identity through application congruence and identity composition, rather than replacing x by the image expression. Original formation, typing and Church instantiation then type graphRun(n,f,a) for every originally typed n:N, and its proof projection gives a HasE identity between that run's scalar and the image of that same run's state. This is a generic internal invariant, stronger than the zero-instance control but still different from either projection-transport premise connecting the run to the external state and scalar folds. It supplies neither of those missing bridges nor unconditional scalar fusion. [SUB250-R81-204](../research/t20-v6-20261012/sources/74ef636570ba73c227daf40d913bdba5a9c40bb83b87579f1b902f1f6a2db25e/InternalGraph.lean#L17-L359)

The two missing graph projections have separate raw-conversion countervaluations. For the state projection, interpreting the open iterator by K(K I) makes the graph run’s first projection reduce to K while the direct state run reduces to I. For the scalar projection, K(K K) makes the graph scalar reduce to K I while the direct scalar iterator reduces to K. Distinct normal forms and imported conversion soundness therefore exclude both unrestricted PolyConvPlus equations. These valuations are deliberately untyped; neither exclusion is noninhabitation of the corresponding HasE transport type. The same body forms those transport types, retains the graph’s literal dependent invariant and proves the state/scalar seed and step commutations, so those positive computations remain distinct from a generic projection-transport proof. [NEXT250-X25-136](../research/t20-v6-20261012/sources/99209853e5882ee3ce54d86c32cd0f33efcc43e66ef7dca934788ca5ecfd8469/ProjectionBoundary.lean#L12-L66) [NEXT250-X25-136](../research/t20-v6-20261012/sources/99209853e5882ee3ce54d86c32cd0f33efcc43e66ef7dca934788ca5ecfd8469/ProjectionBoundary.lean#L69-L99) [NEXT250-X25-136](../research/t20-v6-20261012/sources/99209853e5882ee3ce54d86c32cd0f33efcc43e66ef7dca934788ca5ecfd8469/ProjectionBoundary.lean#L101-L163)

The assembly control distinguishes two erased witnesses: the initial assembled proof converts to the retained graph-invariant projection, while an additional typed J reset produces evidence convertible to I at the same scalar leaf. Typing the scalar result still consumes the state- and scalar-transport premises. The separate SourceFoldContract makes a broader proposed source schema explicit: old Has types the iterator, two endomorphisms, comparison map and seed, and HasE supplies the commuting-square evidence; the requested conclusion is HasE evidence of fold naturality. Its actual theorem proves a full-PER I realizer under those premises, not that source schema. The encoded image observer has an old-source typing, beta/seed equations and an actual typed square, but these do not supply the missing general fold identity. The assembly dependency audit is authored checking code, not an observed successful audit. [NEXT-R18-035](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2167a1b555d9b8a1446e2fda736e6ffa7dc869d05049b3f225ff51529c2ce0eb/AssemblyControls.lean#L12-L60) [NEXT-R18-035](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2167a1b555d9b8a1446e2fda736e6ffa7dc869d05049b3f225ff51529c2ce0eb/AssemblyControls.lean#L69-L104) [NEXT-R18-177](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3cf4645641d47b036c8b7172dba3c2ead2e927c775713a186a90b6f641f5ce2a/SourceFoldContract.lean#L39-L94) [NEXT-R18-177](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3cf4645641d47b036c8b7172dba3c2ead2e927c775713a186a90b6f641f5ce2a/SourceFoldContract.lean#L96-L145)

The generic SourceNaturality schema is nevertheless sufficient for the exact original target: SourceFoldApplication applies it to the typed image map and actual commuting square, uses the image-map seed and beta equations to replace the identity endpoints, and obtains literal I at the original scalar leaf. Abstracting that leaf yields HasE [] c3 (W originalQ), retaining the original q, W and c3. This conditional route does not use the graph invariant or assume its two projection transports, but it still requires a supplied SourceNaturality proof. It therefore distinguishes an alternative sufficient source contract from the full-PER validity result above; it neither constructs that contract unconditionally nor supplies fresh kernel acceptance. [SUB250-U20-122](../research/t20-v6-20261012/sources/6544c631ce50b3637962dca29f0d652c3e2eb26139f4e853778166a81d8e3c1a/SourceFoldApplication.lean#L15-L62)

FoldNaturality supplies a conditional source route to that contract. Keep original Ctx and Form premises and original Has typings of n:N, f:X→X, g:Y→Y, h:X→Y, a:X and b:Y. With arbitrary actual HasE evidence of Rigidity, of h(a)=b and of the commuting square h(f(x))=g(h(x)) in X::Γ, it constructs HasE evidence of h(n f a)=n g b. The proof specializes the literal internal Uniqueness proposition to Y, supplies the mapped fold's zero law and transports its square evidence under the numeral binder using actual-E weakening. Setting b=h(a) recovers the exact earlier fold-naturality conclusion with one explicit extra rigidity premise. It does not replace SourceNaturality by a premise-free theorem, upgrade the original carrier and algebra typings to arbitrary HasE inputs, or supply an inhabitant of Rigidity. [SUB250-R81-130](../research/t20-v6-20261012/sources/66abf61f2374a7a782bbdf639d8b36f3cb5ad72e1d1cdae7cd66d373a5812926/FoldNaturality.lean#L76-L316)


### 9.3 Certificate acceptance is not a translation theorem

A separate finite-certificate calculus admits an arithmetic certificate rule. It retains its own original base rules and can certify identity between compiled unary expressions when a finite check accepts the certificate. Its literal certificate grammar is distinct from $`E`$; it does not acquire the extensional rules merely because both calculi discuss identity.

For the original expressions $`x`$ and $`x+0`$, the concrete certificate is the description with coefficient list $`[0,1]`$ and an empty exception list. Coefficients are in increasing degree order, so this denotes $`n\mapsto n`$. On the constant and addition fragment, the normalizer assigns tail data $`(0,[c])`$ to a constant, $`(0,[0,1])`$ to the variable, and adds coefficient lists componentwise while taking the maximum of their tail cutoffs. Thus the variable and its sum with zero both have tail data $`(0,[0,1])`$. Building their descriptions trims trailing zero coefficients and collects exceptions below cutoff 0; it changes neither coefficient list and collects none. The certificate verifier checks that both normalized descriptions equal the supplied description, so it returns true. The original base typings form the identity target, and the certificate rule supplies a proof of the same exact type $`\mathcal B`$. This finite computation does not need the normalizer's more general theorem for nested equality tests. [Normalizer and verifier][normalizer] [Exact accepted compiler pair][certificate-pair]

Therefore there cannot be a translation taking **every** closed certificate-calculus judgment to a closed $`E`$ judgment at the same type, even if the translation is allowed to change the proof polynomial arbitrarily. Applied to this accepted certificate, such a translation would produce the inhabitant of $`\mathcal B`$ excluded by Theorem 11. This is a logical consequence of the concrete certificate and the negative theorem; it does not establish reverse inclusion or an ordering of the two calculi as strict extensions. [Certificate grammar][certificate-syntax] [Exact certificate separation][certificate-separation]

Additional induction or dependent elimination rules define further proof systems. They must be assessed using their own grammar and soundness theorems. None of the nonderivability results in this chapter licenses carrying an old negative result over to a changed calculus. Conversely, success of a proposed extension does not retrospectively supply a proof in $`E`$ or make an owner adoption decision.

The separate Joint grammar retains explicit old-E inclusion constructors while recursively allowing Joint formation and typing in its rules. Its two added constructors are syntactic: dependent sum elimination takes a formed motive over the sum, a branch under the two-entry dependent telescope and a typed sum input; natural induction takes a formed family over N with typed zero seed and dependent step, returning the literal sectionPoly witness. Neither constructor asks for semantic validity. The authored mutual soundness proof handles these new cases through the imported full-PER sum-elimination and dependent-induction interfaces and derives no closed Bottom inhabitant. Raw still denotes the same open-term conversion relation, and the original endpoints remain Raw-distinct in that interpretation. These are dependency-relative claims for the separate grammar, not adoption into E, completeness, or newly obtained kernel acceptance. [NEXT-J12-163](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3adb4dc48b40befdfaef1db6b2e586a2a171ca5e05172eb752893ad92aeeab56/JointSyntax.lean#L9-L90) [NEXT-J12-114](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/31b121c690e0ab2da1896753b8f1ab35c679a62478328ad3a7f9a9499eaa9a8a/JointSoundness.lean#L7-L60) [NEXT-J12-114](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/31b121c690e0ab2da1896753b8f1ab35c679a62478328ad3a7f9a9499eaa9a8a/JointSoundness.lean#L113-L139)

The contextual discriminator places the positive typed identity and Raw refutation in one unchanged Joint context, [NoConfusion]. Weakening transports the closed Joint compiler identity into that context, while the literal variable at index zero supplies the visible assumption to the weakened Raw-negation witness. In the faithful full-PER interpretation, Raw identity between zero and one is empty, so the NoConfusion arrow admits the explicit environment cons I zeroEnv. Joint soundness at that same environment excludes every Bottom inhabitant in the context. Thus the source states typed equality of the original endpoints, refutation of their Raw identity, and consistency together without changing contexts between the claims. The semantic realization does not produce a closed HasJ proof of NoConfusion, identify typed with Raw equality or adopt Joint rules into E; the soundness and compiler dependencies remain imported. [AFTER750-F50-234](../research/t20-v6-20261012/sources/dadc4691f22e1be263aa07707bd63d73d2641526c895fc76fc7aaca14c09f0bd/ContextualDiscrimination.lean#L15-L81) [AFTER750-F50-247](../research/t20-v6-20261012/sources/de0e0ce434634d17f8f2aed92e188b520b55e9b99a5682ebefddabd783c7f30b/FaithfulRawNoConfusion.lean#L9-L81)

A separate selective soundness port fixes the grammar flags to FormX/HasX true false: dependent sum elimination is enabled and natural induction is disabled. Its formation and typing inductions use the homogeneous Henkin interfaces for the inherited cases; the sum-elimination branch combines hereditary instantiation of the formed motive with the imported semantic elimination theorem, while the induction branch is eliminated by its impossible permission flag. The resulting fundamental theorem and formation eligibility apply at admissible parameter valuations and supported contexts of that model. This gives a dependency-relative soundness construction for the sum-only selective extension, not soundness with induction enabled, a new nonderivability theorem, or adoption of either rule into unchanged E. [NEXT250-Q25-096](../research/t20-v6-20261012/sources/90817a13157273e3fc81a3b64d67a5e5a1ebed3ac92d1a6c977e3c8acd03d6ad/HenkinSelectiveSoundness.lean#L9-L60) [NEXT250-Q25-096](../research/t20-v6-20261012/sources/90817a13157273e3fc81a3b64d67a5e5a1ebed3ac92d1a6c977e3c8acd03d6ad/HenkinSelectiveSoundness.lean#L63-L124)

The Henkin sum component supplies the semantic interfaces used by that sum-only port. Given context and type laws and a Fundamental sum input, it constructs semantic eta at Id_Sigma(z,reconstruct(z)); with a lawful dependent motive and branch it transports the branch result from the reconstructed pair back to the original input. This is eta in the displayed relation, not unrestricted raw pair conversion or an inhabitant of the unchanged source calculus. Its SemSub condition separately preserves supported environments and related environment pairs. Those two clauses transport type laws, lift under term and impredicative type binders, and preserve every hereditary component law under substitution and typed instantiation. Context laws, admissible valuations and the imported interpretation/substitution equations remain explicit dependencies, without a new model construction or compiler verification. [T33-097](../research/t20-v6-20261012/sources/f5cc19424e01b32f0409a29b307dab83d1518f9bc9f976677d0aa736baac81c1/HenkinSigma.lean#L9-L49) [T33-097](../research/t20-v6-20261012/sources/f5cc19424e01b32f0409a29b307dab83d1518f9bc9f976677d0aa736baac81c1/HenkinSigma.lean#L51-L93) [T33-097](../research/t20-v6-20261012/sources/f5cc19424e01b32f0409a29b307dab83d1518f9bc9f976677d0aa736baac81c1/HenkinSigma.lean#L95-L119)

The semantic substitution port makes its preservation premises explicit. SemSub(Gamma,Delta,sigma) sends each supported Delta environment to a supported Gamma environment and each related Delta pair to a related Gamma pair after interpreting every polynomial image, for every admissible type environment. TypeLaws and all hereditary component laws then transfer. Under a term binder it uses pup(sigma) and the substituted head type; under a type binder it weakens both telescopes but retains sigma, shifting the type environment instead. Instantiation additionally needs ContextLaws for reflexivity and a Fundamental argument. These are semantic term-substitution obligations, not permission to leave a separate type-image substitution unlifted, and they do not by themselves prove a syntactic source-judgment substitution theorem. The FullPER interpretation and binder equations remain imports. [L34-114](../research/t20-v6-20261012/sources/fbe89439147400d7e3319077dc52d9e52988f9307ec7d707f4427c879fe52e9c/JointSubstitution.lean#L7-L58) [L34-114](../research/t20-v6-20261012/sources/fbe89439147400d7e3319077dc52d9e52988f9307ec7d707f4427c879fe52e9c/JointSubstitution.lean#L60-L73)

The Joint controls witness genuine recursive reuse of the enlarged judgments. Sum elimination first supplies a closed Eta witness excluded in unchanged E; that witness can be the seed of a Joint induction section over the constant Eta family, whose old-E inhabitant would again imply the forbidden Eta inhabitant. More strongly, identity at Eta with that new witness as endpoint forms a new motive unavailable to old E. Sum elimination is then re-entered with this newly formed motive and a newly typed branch, and its result supports another nested identity formation. Thus these rules are not merely wrappers restricted to old formation and typing inputs. The same control keeps the ghost and its pair reconstruction distinct at faithful Raw while relating them at Sigma. It establishes neither raw eta nor minimality of induction, and its boundary and soundness imports remain dependency-relative. [NEXT250-Y25-158](../research/t20-v6-20261012/sources/9d893e52fcad6b79274fd7b98ea221b6d894913a75332d4173f095ea61915188/JointControls.lean#L30-L92) [NEXT250-Y25-158](../research/t20-v6-20261012/sources/9d893e52fcad6b79274fd7b98ea221b6d894913a75332d4173f095ea61915188/JointControls.lean#L94-L156)

The selective completion presentation makes the two additions independently switchable: its mutually recursive context, formation and typing judgments retain old-E inclusion and the explicit inherited formation and scope obligations, while sigmaElim requires the sum flag and natInduction requires the induction flag. PositiveRigidity isolates the decisive positive direction in unchanged E first: a supplied section of EqFamily(u), with an E-formed context and E-typed u:N→N, yields literal I at ResultAt(u) by symmetry, transitivity and product extensionality. It abstracts this implication in old E and applies that old function to a newly typed selective section, so no weakening or substitution theorem for the selective extension is needed for this transfer. Full dependent induction alone, with the sum flag false, then constructs the triple abstraction of I at Rigidity and, through the supplied original-Q typing and rigidity-to-identity implication, obtains the original compiler identity. The syntax alone is not a semantic conservativity theorem, and this positive induction-only result must not be confused with the separately retained soundness of the sum-only fragment. [NEXT250-Z50-219](../research/t20-v6-20261012/sources/a81f32e343169f596dd4a00dac141b55e59034009c64efc272e054b596334a2b/SelectiveSyntax.lean#L12-L92) [NEXT250-Z50-213](../research/t20-v6-20261012/sources/a6e5dad22d09c7ff70a45e478949b6d3988d0ac932fe94671db844aaea28ca6e/PositiveRigidity.lean#L14-L76) [NEXT250-Z50-213](../research/t20-v6-20261012/sources/a6e5dad22d09c7ff70a45e478949b6d3988d0ac932fe94671db844aaea28ca6e/PositiveRigidity.lean#L78-L136)

The positive transfer additionally retains the exact fixed scalar witness. A structural induction maps every selectively enabled HasX derivation into the Joint grammar, carrying its formation, lookup, scope and extensionality premises and using the matching Joint constructors for the enabled additions. In the selective grammar itself, old typing k:T together with selective evidence of Id_T(I,k) feeds the original two-coordinate J motive; erased J conversion returns precisely c3:W(k). Applying this to the induction-only original-compiler identity gives c3:W(originalQ) with the sum flag false, and the syntactic inclusion transfers that witness, rigidity and the compiler identity into Joint. The source separately retains noninhabitation of those targets in unchanged E and uses the corresponding induction-only and Joint soundness models to exclude identity between the original endpoints at faithful Raw. Thus the positive fixed-witness transfer is neither semantic reflection nor adoption into E, and its stronger typed identities do not collapse the Raw boundary. All cited structural, original-Q and separation interfaces remain imported rather than newly executed. [A1000-S33-058](../research/t20-v6-20261012/sources/ed24f22b0c4940f9883e7f04933db7c4f0fd644393602d405b934404be3c1596/PositiveTransfer.lean#L9-L51) [A1000-S33-058](../research/t20-v6-20261012/sources/ed24f22b0c4940f9883e7f04933db7c4f0fd644393602d405b934404be3c1596/PositiveTransfer.lean#L59-L126)

TaggedSelectiveSoundness provides the complementary model-specific port for FormX/HasX with the sum flag false and the induction flag true. Its mutually recursive formation and typing inductions retain all inherited context, substitution, extensionality and J obligations. The sum-elimination case is unavailable by its flag, while the induction case uses the supplied dependent-induction semantics together with the seed and step interpretations and hereditary Church laws. This is soundness of the induction-only selective grammar in TaggedPER, relative to the imported tagged substitution and semantic results. It is not the sum-only Henkin port, soundness of both additions at once, or a general conservativity/eta theorem for the original grammar. [A750-T50-114](../research/t20-v6-20261012/sources/c45b616b56c0ac754a0e360acc43e1bebecf2cea8f056eac5623ee5c68522e5a/TaggedSelectiveSoundness.lean#L9-L61) [A750-T50-114](../research/t20-v6-20261012/sources/c45b616b56c0ac754a0e360acc43e1bebecf2cea8f056eac5623ee5c68522e5a/TaggedSelectiveSoundness.lean#L63-L125)

The separate schema-separation body treats admissibility over the recursively extended judgments, not merely old-E inputs. Sum-only judgments admit their full sum schema but not even the weak full induction schema; induction-only judgments admit induction but not the weak full sum schema. The first obstruction uses the original compiler equality family and a nonstandard Church element in the homogeneous model, while the second uses the sum-eta ghost in the faithful-Raw model. Each extension separately has no closed Bottom inhabitant. These arguments deliberately use different Raw interpretations, universal in the sum model and conversion-faithful in the induction model. They are dependency-relative nonadmissibility proofs, not identification of those models, adoption of either rule into unchanged E or a new kernel check. [AF750-Q4-175](../research/t20-v6-20261012/sources/ce09cebcb67e70619a8516cda4d902fd215d91265a9717c948ecc9602a37ee64/SchemaSeparation.lean#L18-L62) [AF750-Q4-175](../research/t20-v6-20261012/sources/ce09cebcb67e70619a8516cda4d902fd215d91265a9717c948ecc9602a37ee64/SchemaSeparation.lean#L64-L123)

The Raw-to-top diagnostic is only a translation of type syntax: it replaces Raw by Pi Bottom Bottom, preserves parameters and Bottom, recurses through products, sums and universal types, and leaves identity endpoints unchanged. Its structural equations commute with term substitution, weakening, instantiation, type renaming and mixed substitution, mapping the type-image substitution as well. It fixes finite TypeCode images and N, and transports motive, branch and dependent-step type expressions. These exact syntax equations do not translate source derivations or establish semantic faithfulness of a rival model. [NEXT-D8-197](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/404c2103ddd8f4662137fa920c1fc2842bec1d3c9c9071d9a8d8af2b8c8000cb/RawTopTranslation.lean#L13-L126)

A separate RawTopSoundness body adds semantic soundness to that diagnostic translation. Raw is interpreted as Pi Bottom Bottom, whose relation accepts every polynomial and has the hereditary laws needed by the induction. Lookup translation retains indices. Mutual arguments transport old formation and typing, followed by an actual Joint typing induction whose sum-elimination and natural-induction cases use the corresponding semantic interfaces. The resulting fundamental judgment keeps the original proof polynomial while translating its telescope and type; formation and context laws follow as well. This does not translate derivation trees into a new source calculus or make the model faithful to Raw conversion: the source expressly calls it diagnostic. Reflection, conservativity and fresh compiler acceptance are not supplied, and FullPER, substitution and semantic-constructor imports remain dependencies. [L34-123](../research/t20-v6-20261012/sources/fe8fca25835f69e87d32721ac5425ca7d3595b3408b2182dedbbbce56f13fa67/RawTopSoundness.lean#L4-L25) [L34-123](../research/t20-v6-20261012/sources/fe8fca25835f69e87d32721ac5425ca7d3595b3408b2182dedbbbce56f13fa67/RawTopSoundness.lean#L27-L149) [L34-123](../research/t20-v6-20261012/sources/fe8fca25835f69e87d32721ac5425ca7d3595b3408b2182dedbbbce56f13fa67/RawTopSoundness.lean#L154-L255)

ExplicitRawGap uses that translation for a more specific diagnostic. Composing it with the full-PER interpretation preserves the open carrier, conversion, quantification over all PERs, projection-based sums and Church N, but makes Raw universal. Its chosen no-confusion candidate is formed in old E and valid in the faithful interpretation, while the diagnostic interprets it as empty; diagnostic soundness consequently excludes a Joint inhabitant. Faithful soundness separately excludes the opposite Raw equality. This is a source-grammar completeness gap witnessed by a deliberately Raw-unfaithful interpretation, not a rival preserving the intended meaning of Raw, an inconsistency of the faithful model or permission to add a rule. The semantic candidate facts and the two soundness interfaces remain imported premises. [A750-T50-112](../research/t20-v6-20261012/sources/c445a2c1d5f8115c11109e8498472dec5d920a93a61c6778061aa4a6ee8fa6ea/ExplicitRawGap.lean#L16-L51) [A750-T50-112](../research/t20-v6-20261012/sources/c445a2c1d5f8115c11109e8498472dec5d920a93a61c6778061aa4a6ee8fa6ea/ExplicitRawGap.lean#L56-L106)

The retained rigidity discriminator separates semantic validity from source derivability. In the full open-term Church PER, an endomorphism preserving zero and commuting with successor is related to identity: standardness relates each supported input to a numeral in the Church PER, and induction fixes every numeral. The source develops validity of the fixed rigidity witness from this argument, while deriving noninhabitation of Rigidity in unchanged E from the original-identity obstruction. Soundness and the valid witness exclude an E inhabitant of its internal negation as well. These two source exclusions are not a claim that every semantic interpretation is complete. [B141-012](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/031cd0c8825f45a0dbedb015e79c1de16a21b80fe90695be9ed0cb5a55eae70b/RigidityDiscriminator.lean)

The corresponding semantic uniqueness statement is more general than the identity endomorphism case. Let A be any saturated PER, f an A-endomap, a an A-supported seed, and u a related map from the Church PER to A. If u at zero is A-related to a and u at every supported successor is A-related to f applied to its predecessor value, then u(n) is A-related to n f a for every supported Church input n. Standardness first relates n to a numeral inside the Church PER; induction proves the equation for that numeral, and relatedness of u transports it back. Related inputs n and m likewise give u(n) related to m f a. The contract mentions neither q nor fusion and asserts no raw equality of unapplied numerals or source-typed rigidity witness. Its standardness and numeral-computation interfaces are supplied imports. [A750-F50-010](../research/t20-v6-20261012/sources/af620d83295749a696674576c33c5b521b1f721ad9db5130125152fd8022e1f4/RecursorUniqueness.lean#L7-L49)

The Joint extension has a narrower positive conservativity result. Given an actual closed Joint typing n:N, complete development of the applied generic observation nfa and structural readback return a unique iteration count. The representative is an old-E Church numeral, and all supplied source and open-carrier iterator/seed applications agree with it. The old-E extractor remains definitionally unchanged on old inputs. This is applied observational conservativity, not raw conversion of n to that numeral or normalization of every reduction of n. [B141-023](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/054cb2f484e6078430854781ceebf69917601bb374a6bb1a952cd044ec984f7d/JointNumeralExtraction.lean)

The Joint extraction has a further typed, bidirectional endpoint. With actual closed Joint typings p:N and q:N supplied, equality of their extracted generic iteration counts is equivalent to existence of a Joint identity witness at Id_N(p,q). The positive direction weakens the endpoints into the fresh scalar context, introduces identity at their converted observations, then uses Pi extensionality twice and All extensionality; in particular it yields literal I at the identity with the extracted old numeral. The converse uses Joint full-PER soundness and injectivity of open iterations, so an arbitrary identity witness cannot identify distinct counts. Comparing the extracted naturals therefore decides this promised typed-identity problem. It does not decide arbitrary typing or inhabitation, assert raw conversion of an unapplied term to a numeral, or provide a new compilation result. [NEXT250-Y25-150](../research/t20-v6-20261012/sources/9beab51f3fe8ffde00a3838989a46bc45fcedc441986987cb6cc20bfaf49d6f1/JointTypedCanonicity.lean#L46-L123) [NEXT250-Y25-150](../research/t20-v6-20261012/sources/9beab51f3fe8ffde00a3838989a46bc45fcedc441986987cb6cc20bfaf49d6f1/JointTypedCanonicity.lean#L125-L175)

Its dependent-section construction also keeps its premises: a formed family over N, typed seed and step, a rigidity witness and a typed numeral input. The literal output is the second projection of the numeral fold on the total space, transported from its projected index to the requested index. A separate control forms an identity family whose endpoints syntactically vary with the index and whose new carrier is not old-E formed; neither its seed nor its step is old-E typable. Joint induction supplies its section and computation equations, but this reflexive family also has a direct section. It demonstrates the enlarged input scope, not necessity or minimality of the induction rule. [B141-029](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/06c346ba09a6079cf4deedd6ab1a187d40b8d914331f91a48526b83721707a24/JointInductionSectionCorollaries.lean) [B141-016](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/03f77315e6632e5a0c0de2f9a9da99f1bd41149988f0ba885db106536962315e/JointInductionControls.lean)

For dependent sum elimination, the retained review supplies a fixed eliminator only when the stated eta identity z=reconstruct(z) is supplied. Its raw pair computation and invariance under changing the proof argument need no typing or equality-of-proofs premise. A tagged ghost counterexample separately excludes the unrestricted eta schema and hence the weak and strong elimination schemas in the stated calculus. These are dependency-relative source developments; reading them supplies no new kernel or dependency-closure verification. [B141-025](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/058b8131979e092632413f48a2d5c8afb871d45ee3364f06ce0f0d520ff2e1ee/ConstructiveReview.lean)

The constructive source makes the original-source schema equivalence explicit. With formed context, sum, motive and branch and an original Has-typed sum input, a HasE eta witness transports the branch at the reconstructed pair back to the input. Raw SKI conversion erases that transport, and at a literal pair computes to branchAt d a b independently of the supplied eta proof. Conversely, choosing the formed eta motive and its canonical I branch extracts eta even from elimination without any computation clause. Thus these original-input eta, weak-elimination and computed-elimination schemas are equivalent; this does not provide eta unconditionally or extend the premises to arbitrary HasE inputs. A typed pair-computation identity additionally checks both endpoints independently and uses the separately proved raw conversion, without UIP. [NEXT-C8-054](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/254b95f0b02765d1b3018f256299af432083ac7f2bcdd0d4d99f538e50c861c7/Constructive.lean#L16-L79) [NEXT-C8-054](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/254b95f0b02765d1b3018f256299af432083ac7f2bcdd0d4d99f538e50c861c7/Constructive.lean#L82-L107) [NEXT-C8-054](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/254b95f0b02765d1b3018f256299af432083ac7f2bcdd0d4d99f538e50c861c7/Constructive.lean#L181-L240)

The actual-E port removes that original-input restriction while retaining every formation and typing premise. For each CtxE telescope, formed dependent sum and HasE-typed input z, a HasE witness of z=reconstruct(z) is equivalent to dependent elimination at that input for every FormE motive and HasE branch, even when the elimination conclusion asks only for inhabitation and no computation law. The forward direction transports the branch at the reconstructed pair along the reversed eta identity; the converse specializes elimination to the formed eta motive and its canonical I branch. The same equivalences hold uniformly as external schemas, and the constructed eliminator also erases to the branch on the projections. At an actual typed pair its computation has a typed propositional identity witness, with both endpoints independently typed. These constructions supply neither eta unconditionally nor a new source rule, and their imported structural and raw-computation facts are not freshly audited. [A750-F50-046](../research/t20-v6-20261012/sources/b7d7cec79167623c3a53093d8bcdc96fd1c882437a0faf5583f00a1331fe1b82/FullESigmaElimination.lean#L20-L60) [A750-F50-046](../research/t20-v6-20261012/sources/b7d7cec79167623c3a53093d8bcdc96fd1c882437a0faf5583f00a1331fe1b82/FullESigmaElimination.lean#L63-L155) [A750-F50-046](../research/t20-v6-20261012/sources/b7d7cec79167623c3a53093d8bcdc96fd1c882437a0faf5583f00a1331fe1b82/FullESigmaElimination.lean#L157-L216)

The full-E boundary keeps the rigidity hypothesis available in the same actual telescope: with S=Sigma Raw Raw and R=Rigidity, it forms Γ=[S,R], types var0:S and var1:R, and invokes the retained tagged boundary to exclude EtaAt at var0. The supplied eta/elimination equivalences then exclude both weak and strong elimination there, hence their unrestricted schemas. Its inherited two-sided source-independence statement is specifically the absence of closed HasE witnesses of R→Eta and R→(Eta→Bottom). It reuses the existing model; the external schemas are not identified with a single source type, and no new model or import verification follows. [NEXT-D8-150](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/38d6d7eab3f9453de8f89870c5fc5deff83348aa966941fec588d15cc015872f/FullESigmaBoundary.lean#L11-L60)

The reverse directional separation is also model-relative: no closed actual-E proof inhabits Eta -> Rigidity or Eta -> (Rigidity -> Bottom). For the first obstruction, the componentwise Henkin sum model validates Eta but makes the diagnostic ResultAt(originalQ), and consequently Rigidity, empty; soundness sends a proposed implication to that contradiction. For the second, FullPER supplies simultaneous semantic witnesses of Eta and Rigidity, excluding the proposed implication to Bottom. Old-Has noninhabitation follows by inclusion. The Henkin eta step retains its carrier and dependent-fibre law premises, and neither model witness supplies a source inhabitant of Eta or Rigidity, semantic completeness, or unrestricted raw eta. Soundness and discriminator interfaces remain imported. [L34-119](../research/t20-v6-20261012/sources/fcda14a453a363f3d51a62549ea3e67f3690d29b9889179fc4f55fe3f0be7a07/CompletionSeparation.lean#L17-L53) [L34-119](../research/t20-v6-20261012/sources/fcda14a453a363f3d51a62549ea3e67f3690d29b9889179fc4f55fe3f0be7a07/CompletionSeparation.lean#L55-L91)

The retained branch compatibility source identifies Structural.pairSub, branchType and branchAt definitionally with their SigmaCompletion counterparts. More than an equality of names is retained: from CtxE Γ, an actual HasE branch d:branchType P under B :: A :: Γ, and HasE arguments a:A and b:inst B a, the imported structural substitution theorem gives HasE Γ (branchAt d a b) (inst P (pairPoly a b)). This preserves the exact dependent result type and the existing branch syntax. It is a branch-at-a-pair substitution interface, not unrestricted elimination at an arbitrary sum input or a new eta principle; its axiom-print commands are not fresh verification results. [NEXT-C30-144](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/372e4295f748bc5907bf599d47ce7cee9daee23a8c968b2c81faadee1380a565/RetainedCompatibility.lean#L7-L23)

The positive full-E sum controls separate several enlarged-input obligations. With D=proofId and E=extId, they exhibit CtxE [D] without original Ctx [D], a motive wk D that is not originally formed over the originally formed sum Sigma Raw Raw, an E-only branch even in the original two-Raw-variable telescope, and a closed E-only input at Sigma E Raw. The combined test supplies all actual-E formation and typing premises in [D], proves eta for its literal pair input, and applies elim_of_eta to obtain the constant-motive result D. Its raw pair beta law is retained independently of that E evidence. These controls demonstrate actual-E input scope, not that eta is necessary for these canonical-pair, constant-motive instances or that an unrestricted eta schema has been obtained. [SUB250-U20-147](../research/t20-v6-20261012/sources/6a4a17bdc76a068fc4f0b60a8219177a9ea71fe90ab592662ca5703c3d4201bd/FullESigmaScopeControls.lean#L14-L113)

In the separate Joint calculus, the full sum-elimination constructor supplies the propositional eta identity for every formed dependent sum and every Joint-typed input, rather than taking eta as an extra premise. Its canonical pair branch and formed eta motive yield literal I at Id(z,reconstruct(z)). Given a typed identity of first components, dependent pair congruence transports the second component without changing its erased polynomial; reconstruction and identity composition then give fidelity of the whole package. For a closed Joint input z:Σ n:N.P(n), the retained extractor's index identity thus yields I at the identity between z and pair(numeral(count),snd(z)). A formed dependent consumer with the correctly typed branch can consume that extracted pair while retaining its exact original result type R(z), not only R of the representative. The final erased transport preserves the branch polynomial. This uses the supplied extraction interface and source J; it implies neither raw eta nor uniqueness of identity proofs, and does not transfer the result to unchanged E. [NEXT-J12-86](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2da1e6adf781d20e9d56cc9275f6532c53955d98da1706b16c92233ead8b0e03/JointSigmaFidelity.lean#L20-L89) [NEXT-J12-86](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2da1e6adf781d20e9d56cc9275f6532c53955d98da1706b16c92233ead8b0e03/JointSigmaFidelity.lean#L91-L119) [NEXT-J12-65](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/26891775232a3b8566cee2b7f67472c0aa9059b541e0d537a9db6e7613dda84d/JointNumeralFidelity.lean#L13-L111)

Separate proof-uniqueness controls distinguish identity evidence from explicit labels. Two bound variables at the same old identity type are source-identical while remaining different under unrestricted PolyConvPlus; a Joint-only identity carrier has the analogous typed result. In Joint, any typed observer from one fixed identity type into a fixed formed carrier identifies the two proof inputs. A closed numerical observer therefore has equal counts when both stated scalar-observation conversion certificates are supplied. Provenance can instead occupy a separate data component: the source types each labelled k as a pair of numeral k and evidence in Sigma N Id_Raw(I,I), and shows that an identity between two such packages forces equality of their labels. In particular labels zero and one cannot be identified. These are conditional typed source interfaces, not raw conversion of arbitrary proof terms or identification of all labelled data; the negative and numerical arguments retain their imported soundness dependencies. [SUB250-R81-074](../research/t20-v6-20261012/sources/5c82146fa3fe931bd0be9ddc52d10482095ae5202c38ea12b860a0b5b1e8de46/ProofUniquenessControls.lean#L15-L124)

The original extensional calculus has a direct typed proof-uniqueness construction in arbitrary formed contexts. Its actual judgments are CtxE, FormE and HasE, despite a comment calling the transport Joint. With the stated family and endpoint typings, source J transports a term and its two K contractions preserve the erased polynomial; symmetry and composition then give canonical I at any inhabited identity type. A motive depending on the proof coordinate supplies I at Id_(Id_A(x,y))(e,I). Combining the two contractions gives I at Id_(Id_A(x,y))(e,f) for any two supplied HasE witnesses at the same identity type. This is propositional identity of typed proofs, not unrestricted raw conversion of e and f or identification of separate data labels. Formation, scope and substitution facts are imported, and the axiom-print requests are not received audit results. [NEXT250-S25-042](../research/t20-v6-20261012/sources/86fb13ba8e541daf18c98d184f1e871e99ecf43aad9abb39eb366a6e54c2c9a7/OriginalProofUniqueness.lean#L12-L43) [NEXT250-S25-042](../research/t20-v6-20261012/sources/86fb13ba8e541daf18c98d184f1e871e99ecf43aad9abb39eb366a6e54c2c9a7/OriginalProofUniqueness.lean#L46-L82) [NEXT250-S25-042](../research/t20-v6-20261012/sources/86fb13ba8e541daf18c98d184f1e871e99ecf43aad9abb39eb366a6e54c2c9a7/OriginalProofUniqueness.lean#L84-L130)

The separate Joint proof-uniqueness construction supplies the general typed result behind those controls. In any valid Joint context, an identity witness e:Id_A(x,y) can first be replaced by the canonical I at the same type using source identity symmetry twice. A motive that also mentions the identity-proof coordinate then uses source J to produce I:Id_(Id_A(x,y))(e,I); composing these contractions identifies any two witnesses e and f at that fixed identity type. The construction retains formation and endpoint typings and permits newly Joint-formed types. It proves propositional equality inside HasJ, not unrestricted raw conversion of e and f, equality of separate provenance labels, or translation of arbitrary HasJ derivations into unchanged E. The structural, symmetry and J interfaces remain imported dependencies, and the axiom-print requests are not received verification results. [NEXT250-Q25-082](../research/t20-v6-20261012/sources/8e877b97c15aba2d3530c48b5a4ead75ff410a111fdb9ef5f1299aaed684ab27/JointProofUniqueness.lean#L11-L33) [NEXT250-Q25-082](../research/t20-v6-20261012/sources/8e877b97c15aba2d3530c48b5a4ead75ff410a111fdb9ef5f1299aaed684ab27/JointProofUniqueness.lean#L35-L70)

The dependent extraction control tests a fiber that genuinely constrains its index, rather than a merely reflexive family. It uses P(n)=Σ e:Id_N(n,numeral 2).newMotive, forms and inhabits the Joint package built from the supplied count-two control, and proves that P(numeral 2) is not even old-E formed. Projecting an inhabitant at numeral 1 would give a Joint identity between the distinct numeral counts 1 and 2, so that wrong fiber is uninhabited. The first projection of the concrete package has count two, extraction returns two, and the same second-projection polynomial remains typed in P(numeral 2). This witnesses both the enlarged grammar and the need to retain the dependent index. It does not turn Joint inhabitation into old-E inhabitation, and the appended evaluation and dependency commands are requests, not observed outputs. [NEXT-R18-236](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/495ed6e77340d6c93aee9dcd807859b16b371a3074fc57086ec8034ea66ee98a/JointDependentControls.lean#L16-L117)

The dependent Sigma extractor supplies the underlying general source witness, not only the later fidelity controls. From an actual closed Joint typing z:Σ n:N.P(n), it extracts a natural count from the first projection’s generic scalar observation and obtains I at Id_N(fst(z),numeral(count)). Source J transports the literal second projection into P(numeral(count)); two K contractions erase the transport back to that same polynomial, whose scope is retained. NumeralFiber stores the computational count together with its observation conversion, index identity, second-projection typing and typing of pair(numeral(count),snd(z)). Any independently supplied finite observation conversion to iteration(k) forces count=k, without identifying fibre proof terms. An actual Joint branch under [P,N] then consumes the numeral and the preserved second projection by the simultaneous substitution [snd(z),numeral(count)]. Its result type is R of that representative pair; the separate fidelity argument is still needed to recover R(z). The construction imports typed canonicity and structural substitution and introduces neither raw eta nor a new typing rule. [NEXT250-E25-197](../research/t20-v6-20261012/sources/a49bbaca2aba6ae131d6f1e5f1ba1ebd2926ff22f099b5d8c11f0fba67443f5b/JointSigmaExtraction.lean#L15-L47) [NEXT250-E25-197](../research/t20-v6-20261012/sources/a49bbaca2aba6ae131d6f1e5f1ba1ebd2926ff22f099b5d8c11f0fba67443f5b/JointSigmaExtraction.lean#L49-L81) [NEXT250-E25-197](../research/t20-v6-20261012/sources/a49bbaca2aba6ae131d6f1e5f1ba1ebd2926ff22f099b5d8c11f0fba67443f5b/JointSigmaExtraction.lean#L83-L107)

The closed Joint extraction-input provider exposes how both new rules enter the count-two control rather than assuming an old-E seed. Its input type is Sigma N newMotive, which is Joint-formed but not formed, and therefore not inhabited, in unchanged E. The pair of zero with I has this type by the supplied new-motive reentry proof. Actual Sigma elimination, using var1 in the genuinely new branch context [newMotive,N], produces the seed at N. The imported old-E successor supplies the step, and actual Joint natInduction forms the section, which is finally applied to the literal numeral two. This body proves Joint typing and closure of that composite input; the numerical extraction or identity-classification conclusion belongs to the separately retained downstream control, not to a fresh evaluator run here. [NEXT250-Z50-222](../research/t20-v6-20261012/sources/a892efeffafd8fa8606dbed06093d821b4632cf71aed0c9e1057c03a2dae54eb/JointExtractionInput.lean#L16-L40) [NEXT250-Z50-222](../research/t20-v6-20261012/sources/a892efeffafd8fa8606dbed06093d821b4632cf71aed0c9e1057c03a2dae54eb/JointExtractionInput.lean#L42-L80)


The independent uniqueness controls keep two interfaces separate. SourceUniqueness compares u(n) with n f a at arbitrary ambient context and generic carrier A only with typed seed and successor laws and an explicit HasE rigidity witness. The Joint control instead constructs the direct section’s zero and successor identities without mentioning a canonical section; its imported uniqueness theorem then compares that section with the canonical section for the same seed and step. These are dependency-relative source proof interfaces, not an adoption of Joint rules into unchanged E or a newly checked import closure. [B141-050](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/0a878ff5456935f38614ae9b1385e9254c03fc5cbc92a9a4f61a255ae8096fb5/IndependentControls.lean) [B141-054](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/0b9091d41331bdcf4ff58d1b07ca6507a4fc62b6cf55afbe0d8ae2a7e4e05432/JointRecursorControls.lean)

The Joint recursor-congruence component supplies the typed transport used before any uniqueness conclusion. With a Joint context, formed domain and codomain, a typed arrow and two typed inputs, source identity evidence yields canonical I at the identity of their images; the carrier need not be old-E formed. Its successorLawFamily states the ordinary equation u(succ n)=s n (u n), with no comparison to a canonical section built into that family. Instantiation identifies the exact dependent fibers, and applying arrow congruence to the curried step gives identity of step outputs in P(succ n). Section application and application at a fresh numeral variable retain their formation and weakening premises. This file provides these congruence and substitution interfaces, not by itself recursor uniqueness, a missing successor law, or translation into unchanged E. [T33-090](../research/t20-v6-20261012/sources/f4e9f83137f667015167eb747fea6afb0a00227213a672c098a5b08a2e3d1106/JointRecursorCongruence.lean#L13-L35) [T33-090](../research/t20-v6-20261012/sources/f4e9f83137f667015167eb747fea6afb0a00227213a672c098a5b08a2e3d1106/JointRecursorCongruence.lean#L37-L64) [T33-090](../research/t20-v6-20261012/sources/f4e9f83137f667015167eb747fea6afb0a00227213a672c098a5b08a2e3d1106/JointRecursorCongruence.lean#L66-L94)

The UnitTransfer construction extracts another conditional source consequence. For Unit=∀α.α→α it lifts an originally typed u:Unit to the Church input K u and applies source uniqueness to a constant recursor and identity step. Pointwise identity followed by product and universal extensionality gives Unit eta when original-Has rigidity evidence can be weakened. It then abstracts the literal double-I term at Rigidity→Πu:Unit.Id(u,I) in every original well-formed context. Applying that already formed implication admits an arbitrary HasE rigidity witness while retaining the original Has premise for u, without postulating arbitrary HasE weakening. This supplies neither an inhabitant of Rigidity nor unconditional Unit eta, and remains relative to the imported uniqueness and structural interfaces. [AF750-Q4-173](../research/t20-v6-20261012/sources/cd7ea123838e58294a078b1538be8003a022da6623a7f2d8753b2001072ded82/UnitTransfer.lean#L12-L166) [AF750-Q4-173](../research/t20-v6-20261012/sources/cd7ea123838e58294a078b1538be8003a022da6623a7f2d8753b2001072ded82/UnitTransfer.lean#L168-L213)

Shared zero equations alone do not give recursor uniqueness. The separate Joint control types both constantZero=K zero and ident at N→N and supplies their identities at zero, but states that no Joint identity witness relates the two functions at that type. Applying a hypothetical function identity at numeral one and using the imported count-separation interface would force 0=1. The missing successor law is therefore substantive. Soundness is used in this independent negative control; it does not become an extra source rule, supply an old-E rigidity witness or identify the Joint and old-E judgment families. [SUB250-C20-001](../research/t20-v6-20261012/sources/4cf58d5bc6d15a0dbb05b8e0fe2ede970865bec2caaae935a49d3f8fec393287/ZeroOnlyControl.lean#L17-L56)

For the Joint uniqueness interface, one generic-context successor-law derivation and an existentially packaged Pi law are equivalent: abstraction packages the former, and specialization at the newest variable recovers it from the latter. No additional law-uniformity assumption is introduced. The associated controls keep the actual identity premise in arrow congruence and require the two compared section laws to use the same successor operation; endpoint typing or a law for an unrelated operation cannot replace them. The canonical uniqueness conclusion can therefore consume an ordinary generic law and remains a Joint judgment after weakening into a genuinely newly formed context. These applications retain their imported uniqueness and structural dependencies, and their fail_if_success lines are authored controls, not observed rejection. Typed identity still does not imply raw conversion. [A750-F50-047](../research/t20-v6-20261012/sources/b84d75e6881ba2fb4d65e9463cc2d7eb7a920f1c9ef3b48f1ddaac9dc00c3e0e/IndependentControls.lean#L15-L76)

The canonical Joint recursor provider supplies the law witness consumed by uniqueness rather than postulating a family of chosen proofs. From the actual Joint context, formed family P over N, seed and dependent step, it weakens into the generic numeral context, applies the successor computation theorem there, and abstracts that one proof to a section of the successor-law family for sectionPoly(p,s). Formation of that family is built from the typed section and step. Combining this canonical law with the supplied zero and successor laws of any other Joint-typed section yields identity with the exact canonical section. The construction retains the imported induction, renaming and uniqueness interfaces; it neither turns unrelated pointwise existence into a source function nor supplies raw successor conversion or an unchanged-E induction rule. [A750-S50-063](../research/t20-v6-20261012/sources/b9640895a24d5005b0622168a7d215bde58e504e9b5abbcdad720a3cb04e7712/JointCanonicalRecursor.lean#L13-L38) [A750-S50-063](../research/t20-v6-20261012/sources/b9640895a24d5005b0622168a7d215bde58e504e9b5abbcdad720a3cb04e7712/JointCanonicalRecursor.lean#L40-L72)

The source computation laws also distinguish zero from successor. The literal section’s zero identity is already in Has. Its successor identity is propositional in HasE and requires an explicit typed Rigidity witness: the projected fold index is related to the input, and typed dependent action transports the comparison into P(succ n). Both endpoints are formed and typed in that fiber, including the converted left endpoint. Erased-J computation does not identify rigidity paths or establish uniqueness of identity proofs. This is the conditional source interface, separate from the Joint section and uniqueness interfaces. [B141-102](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/1462a229392c9804484cdb3239af1cf417b842b0012d1e41a680dd41b4522b9f/ComputationLaws.lean)

The Joint successor law has a concrete raw-conversion boundary. Take the zero seed, step K and open numeral variable var0: the two literal endpoints sectionPoly zero K (succPoly var0) and K var0 (sectionPoly zero K var0) admit a Joint identity in context [N], yet the source states that they are not PolyConvPlus-convertible. For the latter separation it interprets the free variable by the operational element nu; applying the same observer yields distinct atoms a1 and a0. That valuation is used only to refute unrestricted raw conversion and is not asserted to realize the Joint context [N]. The typed propositional equation and the raw separation therefore have different premises and remain compatible. Both arguments retain their imported soundness and operational dependencies, without a new compilation result. [SUB250-U20-171](../research/t20-v6-20261012/sources/6ee126a68672dde6042b3298351067bf5cb76c3224a2966857010901c45b277f/JointInductionRawBoundary.lean#L14-L75)

The Joint structural interface makes the binder bookkeeping explicit: branch substitution lifts twice in the branch term and once in its motive, while sectionPoly commutes with ordinary polynomial substitution; term-variable renaming is the corresponding variable-image specialization. Its scoped constructors retain the stated input scopes. In the separate Joint calculus, induction supplies the literal section from a formed family, seed and dependent step without an external rigidity premise; the successor identity uses rigidity already derivable there and lives in P(succ n), not raw successor conversion. The comparison motive is Id_P(u(var0),v(var0)) with both functions weakened into the numeral context. Induction and Pi extensionality identify u and v only after a zero witness and a dependent induction-step witness for that very comparison family are supplied. Algebra laws are not silently assumed to generate that step. These source interfaces retain their structural, extraction and positive-transfer imports and neither extend unchanged E nor establish fresh kernel acceptance. [NEXT250-T25-050](../research/t20-v6-20261012/sources/883150d231c939b6ec5b18bc4cd40f52e528c6b41842098e225b15812c563153/JointCompletionAlgebra.lean#L11-L49) [NEXT250-T25-050](../research/t20-v6-20261012/sources/883150d231c939b6ec5b18bc4cd40f52e528c6b41842098e225b15812c563153/JointCompletionAlgebra.lean#L51-L145) [NEXT250-T25-053](../research/t20-v6-20261012/sources/88fd210d38fdcd5d1b761988b5749fe6a244ecbe4457c013878c9f275827f2db/JointInductionLaws.lean#L15-L69) [NEXT250-T25-053](../research/t20-v6-20261012/sources/88fd210d38fdcd5d1b761988b5749fe6a244ecbe4457c013878c9f275827f2db/JointInductionLaws.lean#L71-L104)

The Joint recursor-uniqueness construction derives that comparison step from actual matching algebra laws. Given CtxJ Gamma, a family P formed over N, typed seed p and dependent step s, and two typed sections u,v:Pi N P, assume a typed zero identity from each section to p and a typed successor-law section for each using the same s. Typed congruence transports the comparison-family induction hypothesis through s, and the two successor laws identify its outputs; the zero laws supply the comparison seed. Induction extensionality then gives canonical ident at Id_(Pi N P)(u,v). Actual successor-law derivations in the generic numeral context suffice because Pi introduction packages them. Arbitrary pointwise existence or laws for unrelated operations do not suffice. The conclusion is Joint source identity, not raw conversion or a new unchanged-E induction rule, and its congruence/structural/induction dependencies remain imported. [L34-121](../research/t20-v6-20261012/sources/fe105ad62367810413ddb320d959e77e20ddda452f537f2890d6090472a3684a/JointRecursorUniqueness.lean#L15-L44) [L34-121](../research/t20-v6-20261012/sources/fe105ad62367810413ddb320d959e77e20ddda452f537f2890d6090472a3684a/JointRecursorUniqueness.lean#L48-L96) [L34-121](../research/t20-v6-20261012/sources/fe105ad62367810413ddb320d959e77e20ddda452f537f2890d6090472a3684a/JointRecursorUniqueness.lean#L101-L128)

The old-E total-space construction also packages the conditional section as one source function. Given a formed context Γ, a family P formed over N :: Γ, a seed p at P(0) and a dependent step s, weakening and abstraction give the literal term abstract(sectionPoly(pren Nat.succ p)(pren Nat.succ s)) the HasE type Rigidity → Π n:N.P(n). The scoping proof for sectionBody additionally assumes a typed input n:N; sectionPoly discharges that numeral binder internally. Both scoping arguments use the formed context and family, typed seed and dependent step without a rigidity witness. The typing proof of the section still uses that witness before abstracting it. This neither supplies a closed inhabitant of Rigidity nor adopts Joint induction into E. The result remains relative to the imported total-space and dependent-section interfaces, without a new kernel or dependency-closure check. [NEXT-U11-243](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/4aa321371591d7f6506de3ac91e8e787c296b4582b352236cc6d7a18183d2f2c/FullEUniformSection.lean)

The actual-E computation-law port keeps CtxE, FormE and HasE premises throughout, rather than restricting the family, seed and step to the old Has fragment. Erased transport retains the same proof polynomial at the changed dependent fiber; dependent action also admits a separately scoped left endpoint convertible to the original application. The literal section’s zero identity needs the formed E context and family and E-typed seed and step, but no rigidity witness. Projection back to the supplied input and the successor identity additionally require an E-typed Rigidity witness and n:N; the latter returns existential identity evidence at P(succ n). Thus the zero law and the rigidity-dependent successor law extend to the full actual-E input interface without supplying Rigidity, raw successor conversion or proof uniqueness. These are source constructions relative to imported structural and total-space lemmas. [NEXT250-F25-006](../research/t20-v6-20261012/sources/7ee81cb46bfb8a86253844efbb68ffe170cd43e1c0862fef74d0831170b110db/FullEComputationLaws.lean#L13-L39) [NEXT250-F25-006](../research/t20-v6-20261012/sources/7ee81cb46bfb8a86253844efbb68ffe170cd43e1c0862fef74d0831170b110db/FullEComputationLaws.lean#L118-L196) [NEXT250-F25-006](../research/t20-v6-20261012/sources/7ee81cb46bfb8a86253844efbb68ffe170cd43e1c0862fef74d0831170b110db/FullEComputationLaws.lean#L200-L269)

The corresponding full-E section construction keeps the enlarged input interface throughout. From CtxE Gamma, FormE P over N::Gamma and an E-typed dependent step s, uncurrying gives an E-typed total-space step over total(P)::Gamma. With a seed p:P(0), such a step d, r:Rigidity and n:N, the total-space fold is typed at total(P); projected-fold identity and rigidity identify its first projection with n. Dependent transport then erases by the displayed K conversions, so the literal term snd(n (totalStep d) (totalSeed p)) itself has type P(n). Substituting uncurriedStep(s) gives the curried corollary. This supplies neither a Rigidity inhabitant nor an unconditional E induction rule, and retains the imported structural, projected-fold and transport interfaces. [L34-105](../research/t20-v6-20261012/sources/f7d0f3e22a9ec26d3bc8ba2ff143458990b6b985df62e296cfd8f30a30093225/FullESectionCorollaries.lean#L17-L53) [L34-105](../research/t20-v6-20261012/sources/f7d0f3e22a9ec26d3bc8ba2ff143458990b6b985df62e296cfd8f30a30093225/FullESectionCorollaries.lean#L56-L94)

The constant-family scope control makes the full-E enlargement nonvacuous without claiming rigidity is always necessary. Its family is wk(proofId), literally proofId and fixed by substitution, with seed ident and step abstract ident. The family, seed and step have actual-E derivations, while the imported original-image exclusions rule out old formation and old-Has seed or step derivations. The full-E uniform theorem therefore applies to genuinely enlarged inputs. Yet this particular constant family has the direct section abstract ident without Rigidity, and its zero law also omits that premise; only the displayed generic successor control takes r:Rigidity and n:N. The scope exclusions and computation laws remain imported, not freshly audited. [L34-132](../research/t20-v6-20261012/sources/ff8516657b6c04b11a8f1d6d498d1bf8d603b19073a69e456dae5816bcbbed59/IndependentScopeControl.lean#L15-L59) [L34-132](../research/t20-v6-20261012/sources/ff8516657b6c04b11a8f1d6d498d1bf8d603b19073a69e456dae5816bcbbed59/IndependentScopeControl.lean#L62-L84)

The full-E induction control makes the enlarged premise scope concrete. It takes family(n)=Id_extId(iterateAt(n),iterateAt(n)), where iterateAt(n)=n ident ident, and supplies actual-E formation, a reflexive seed and a dependent step. The zero and successor instances are literally different syntax, yet the imported no-original-image result excludes the old Form family premise and any old Has seed or step of those indicated types. The full-E theorem consequently applies outside the predecessor's original input scope and yields the conditional Rigidity→Πn:N.family(n) section. This example does not show that rigidity is necessary for that particular family: the same source constructs a direct section abstract ident without a rigidity premise. Its contribution is discrimination of input judgments and real syntactic index dependence, not a closed rigidity witness or a transfer of Joint rules into unchanged E. [R134-011](../research/t20-v6-20261012/sources/e0443e24e078a13619c325547920e472ad884f68bddddb10cca4173ec44f9603/FullEInductionControls.lean#L15-L68) [R134-011](../research/t20-v6-20261012/sources/e0443e24e078a13619c325547920e472ad884f68bddddb10cca4173ec44f9603/FullEInductionControls.lean#L69-L105)

The uniform-section port separately retains actual Joint premises throughout. From CtxJ Γ, a FormJ family over N::Γ and Joint-typed seed and dependent step, it obtains the shifted family by weakening the total Sigma type and forms the literal section body through its fold and projections. A supplied Joint-typed Rigidity witness then gives HasJ Γ (sectionPoly p s) (Pi N P). The scope of that same section polynomial needs no rigidity witness. Abstracting over a newly introduced rigidity variable consequently gives the exact shifted section at Rigidity→Pi N P. This is a judgment-specific total-space construction for recursively Joint-formed families and newly typed inputs, not a replacement of those premises by old E, an inhabitant of Rigidity in every context, or an unqualified raw computation law. [NEXT250-Z50-220](../research/t20-v6-20261012/sources/a8365ff8cb9d65d00051c9dc363bbe573867ddf058a8c4e78a4935736430f2e0/JointInductionUniformSection.lean#L13-L30) [NEXT250-Z50-220](../research/t20-v6-20261012/sources/a8365ff8cb9d65d00051c9dc363bbe573867ddf058a8c4e78a4935736430f2e0/JointInductionUniformSection.lean#L32-L62) [NEXT250-Z50-220](../research/t20-v6-20261012/sources/a8365ff8cb9d65d00051c9dc363bbe573867ddf058a8c4e78a4935736430f2e0/JointInductionUniformSection.lean#L64-L82)

The separate section-application lemma connects that uniform polynomial to its pointwise body: for all polynomials p,s,n, raw PolyConv relates sectionPoly(p,s) applied to n to sectionBody(p,s,n). Its authored beta proof uses substitution/renaming naturality and the imported closedness of successor and zero. No typing or rigidity premise is needed for this raw equation, but it neither gives the conditional section its missing rigidity witness nor replaces the separately typed zero/successor laws. [NEXT-C8-227](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/47153681df6d0e6487871d1c63883163550f59f7e001c608892de235897efed6/SectionApplication.lean#L12-L21)

The converse controls also state two closed source implications between the unchanged Rigidity and internal Uniqueness formulas: the first uses abstract uniqueUniformProof, and the converse uses the literal fourfold abstraction of ident. The natural-number instance retains Ctx, a HasE Uniqueness witness and base Has typings of the endomorphism and its zero/successor laws; the displayed endomorphism consequence with base Has Uniqueness has the exact orientation I=u. These are supplied-evidence interfaces, not an unconditional inhabitant of either principle. The separate Rigidity controls retain arbitrary-context applications to the original compiler endpoints, invariance of the closed formulas under all polynomial substitutions into the types and the literal evidence-variable order. Their imported semantic-validity and two-sided source-independence statements remain distinct from those source implications. [research/t20-v6-20261012/sources/21453bd7719ed193a394fd377632714b815582d9fb46bc05da51d88ca0014378/IndependentControls.lean:8–32 at ffca0abdf25079ef7639fe19776a21db60272fc4] [research/t20-v6-20261012/sources/1b31327a97820d3941105a309efe151639daa1c4bc94c26c67f3d94883e44787/IndependentControls.lean:11–58 at ffca0abdf25079ef7639fe19776a21db60272fc4]

The independence transfer for internal Uniqueness uses actual source application and composition, rather than a general substitution assumption for arbitrary HasE derivations. With the carrier types formed, composeE constructs S(K f)g from the source S and K rules. Applying Uniqueness→Rigidity to a hypothetical closed Uniqueness witness contradicts the imported Rigidity noninhabitation theorem. Composing a hypothetical Uniqueness→Bottom witness with Rigidity→Uniqueness similarly contradicts the imported absence of an internal negation of Rigidity. Both sides therefore have no closed HasE witness, and the corresponding Has statements follow by inclusion. These are dependency-relative noninhabitation transfers for the exact source formulas, not an inhabitant of either principle or a newly established semantic or kernel result. [AFTER750-F50-235](../research/t20-v6-20261012/sources/dadf79deae58ea8b688733b162ba7976c41f7659167da12800fc007bdb136cb1/UniquenessIndependence.lean#L11-L67)

The weak-induction converse concerns an external admissibility schema, not an added source type. WeakInductionAt Γ asks only for a HasE section of every family formed over N::Γ with actual-E zero seed and dependent step; it imposes no computation law. Applying it to the equality family u(n)=n and then using actual-E product extensionality makes a supplied zero/successor-preserving endomorphism rigid. The single generic context [StepAt(var1),ZeroAt(var0),N→N] suffices to abstract a closed rigidity proof. Thus the global weak schema, its instance at that generic context and existence of a closed HasE Rigidity witness are equivalent, and the imported rigidity noninhabitation excludes both schemas. At a general formed Γ, equivalence with a Γ-rigidity witness requires weak induction at every well-formed finite telescope extension of Γ, not merely at Γ itself. These are source-relative metatheorems, not an internal negation of the schema or a new kernel result. [SUB250-R81-138](../research/t20-v6-20261012/sources/6817015986cf36c0a36bb4affd6f608c432f22215a532e848304be88ac519684/InductionRigidityConverse.lean#L24-L276)

The polymorphic unit review fixes a different endpoint from the raw unit probe: UnitTy is All α.(α→α), and UnitEta is Πu:UnitTy.Id_UnitTy(u,I). It imports the closed double-abstraction witness for Rigidity→UnitEta, then explicitly applies that witness in any original formed context to arbitrary HasE rigidity and unit evidence, retaining FormE premises for both eliminations and the identity target. This route does not reflect HasE evidence back into original Has. The companion binder helper has its own original-evidence restriction and cannot be substituted merely because its conclusion looks similar. The source freezes these types and applications but supplies no new proof of the imported closed implication or observed axiom readback, and it does not remove the rigidity premise. [A750-S50-057](../research/t20-v6-20261012/sources/b911e3fba82b8a49deb2fef18ff0a46b1451dee6a52183d77ff28c89f42a378b/UnitReview.lean#L6-L35) [A750-S50-084](../research/t20-v6-20261012/sources/bde07c7af3060d1ab9ba237f8b823a912271c3464e7921b32ae841f144d9885c/UncertifiedBinderMustFail.lean#L3-L6)

### 9.4 What the result contributes

The worked example separates several obligations that are easily conflated in formal reasoning:

| Question | Result established here |
|---|---|
| Do the literal programs agree on every displayed Church numeral? | Yes, by the pair-state induction. |
| Does a generic Church variable satisfy the Raw unit probe? | Yes, by a source identity-elimination proof. |
| Can arbitrary proof-polynomial choice be removed from the compiler identity problem? | Yes: it is equivalent to the exact fixed witness $`c_3:W(q)`$. |
| Does this yield bounded or syntax-directed proof search? | No; dependent type justification can survive erased proof computation. |
| Is the literal compiler identity valid in the full open-term PER model? | Yes, with proof by a fresh orbit and exact compiler transport. |
| Can identities between supplied closed Church terms be decided? | Yes, by their computably extracted unique counts. |
| Does that procedure decide typing or arbitrary type inhabitation? | No such conclusion follows. |
| Is there a closed $`E`$ proof of the universal scalar law or function identity? | No, by a concrete inhabited whole-rule countermodel. |
| Is there a closed $`E`$ proof of either internal negation? | No, by the complementary full-PER model. |
| Does arithmetic certificate acceptance imply an endpoint-preserving translation into $`E`$? | No; the exact accepted identity is a counterexample. |

These are mathematical results about an explicit representation of proofs and programs. They show both the usefulness of extensional proof rules and the limits of deriving general witness principles from erased computation. They supply no direct theorem about metaphysical grounding, collective cognition, or an unfinished noetic-field research objective. Such applications would require a separate, explicit interpretation and its own evidence.

<a id="witness-metadata-and-repair-boundaries"></a>

### 9.5 Corrected metadata is not a changed proof witness

The scalar provenance-correction guide explicitly says that preserved predecessor metadata falsely alleged a historical scalar receipt/object mismatch. It assigns those old claims a correction-evidence role and states that the original proof and review evidence remained valid and unchanged. That metadata must not be revived as a current defect in the scalar witness of §4. The guide itself does not supply the correction record or a fresh inspection of the original objects; its contribution here is the exact reported status of the allegation. [GUIDE105-G027]

A separate candidate guide distinguishes actual repair from replacement of a test surface. Its type-space proposal required a complete exact original body and a criticized-passage guard; a receipt, not the existence of a proposal, determines whether that guard succeeded. Its modal-support iterator repair belongs to a preserved interrupted attempt and still requires the original helper, tests, candidate and direct-world oracle to be reconciled. A newly written finite-model suite elsewhere cannot certify that the original helper was repaired. These are source-specific pending repair obligations, not additional theorems about the calculus or reasons to rewrite the accepted witness arguments. [GUIDE105-G006]

A later implementation-qualification report supplies a concrete source-bound reproduction for that historical modal-support obligation. For one conjunctive support mask 3 on two sources, the minimal cuts are 1 and 2. The valid absence downset {0,2} gives false with reusable set input, but iter([0,2]) gives true: searching the one-shot iterator for missing cut 1 exhausts it before cut 2 is tested. The report assigns this false necessity answer to the exact historical modal_support.py with SHA-256 08f03eaf860610bdc575761f16174536f13819c8bc5d2daa679e2bceab00421f. The supplied suite uses re-iterable sets, so its success does not cover the declared Iterable interface. This attributed reproduction was not rerun here, and no repair is thereby adopted. The contracts.py and DAG repairs have different identities; the missing R3 state remains unverified. The result neither refutes the set-theoretic theorem nor shows that a current or unreceived successor module retains the defect. [AFTER3384-FOURTH25-091](../research/t20-v6-20261012/research-v6/operational_successors/MODAL_FRONTIER_IMPLEMENTATION_SCOPE.md#L19-L27)

A different, small patch repairs the representation of dependency parents used by repeated reachability scans. The declared interface accepts Iterable parents; the added line first materializes each parent collection as a set, then performs every scan against that same map. The distinction matters for single-use iterators. In a finite dependency map visited in the order c then b, give c the one-shot parent iterator (b), b the one-shot iterator (a), and start with changed set {a}. The unmaterialized first pass consumes both iterators and adds b; the second pass sees no parents and misses c. Materialization retains b as a parent of c for the next pass, recovering {a,b,c}. This is an elementary explanation of the displayed diff under finite, stable input, not a test execution. It neither authenticates the declared dependency edges nor proves that the patch was applied to its named original, and it does not discharge the separate interrupted modal-support repair above. [AFTER1384-S8-134](../research/t20-v6-20261012/sources/3423508f5911e2421ac1c9b2181861728a9254394b065ae578b2527224442649/ITERABLE_REPAIR.patch#L1-L14)

The separate iterator-review body distinguishes another observable from equality of stored values. It requires the changed top-level function/class definition names to be exactly Contract, valid_partition, as_reaches and closure_basis; that AST comparison alone does not rule out edits outside those definitions. It then requests finite old/new comparisons on reusable list and tuple inputs. Its final order probe requires the kernel dictionaries to have equal mapping values, yet requires the repaired dictionary not to preserve the supplied key iteration order while the old dictionary does. Thus the intended qualification expressly permits an observable order change; dictionary equality alone is not full behavioral compatibility for a consumer that iterates those keys. The body also captures outcomes for inner partition generators, generated closure-output rows and generated enabled-action menus without endorsing those shapes as a general Iterable API. These are source-specific review requirements, not observed behavior of the unread old or repaired implementations, evidence that the patch was applied, or a claim that every one-shot input is supported. [AFTER2384-NINTH25-203](../research/t20-v6-20261012/sources/bec784ddd3561af019d3351eae64e7f1092ba9507da3a7db9017c106c6395b17/run_review.py#L39-L46) [AFTER2384-NINTH25-203](../research/t20-v6-20261012/sources/bec784ddd3561af019d3351eae64e7f1092ba9507da3a7db9017c106c6395b17/run_review.py#L89-L129) [AFTER2384-NINTH25-203](../research/t20-v6-20261012/sources/bec784ddd3561af019d3351eae64e7f1092ba9507da3a7db9017c106c6395b17/run_review.py#L131-L161)


<a id="after3134-ninth25-iterator-invariant-scope"></a>

The integration scope assessment distinguishes an accepted-input invariant failure from three defensive extensions of an underspecified iterable boundary. In its reported constructor example, a mass-one one-shot row is traversed during validation and then traversed again when frozen, so the accepted object retains an empty row rather than the validated distribution. This is a failure of the documented promise to freeze the validated mapping, even without a general promise to accept every Iterable. The same assessment reports consumed inputs at valid_partition, as_reaches and closure_basis, respectively hiding the partition's labels or kernel, exhausting reachability targets, and leaving an undersized action-generated basis. Those three interfaces did not explicitly promise arbitrary finite iterables, so their hardening should not be advertised as three additional violations of a stated API contract or as counterexamples to the finite algebraic theorems. The successor materialises the relevant finite inputs at these four boundaries; quotient and sidecar operations still require reusable partitions. This attribution is to the received scope report, not a fresh inspection or execution of either implementation. Its historical thirty-test and oracle results neither erase the old twenty-six-test success nor identify this repair with the separate fifty-two-to-fifty-five-test ancestry. Together with the preceding iteration-order qualification, the result supports a narrowly described invariant repair and compatibility extension, not blanket behavioural equivalence or unrestricted iterator support.

Source: [research/t20-v6-20261012/sources/01b1232252abaaa24a2f90914962d0ad1120528822fcb62cf15e8d0432efb2d7/INTEGRATION_SCOPE_NOTE.md](https://github.com/theislampill/orthemology/blob/345f62310fd4895c26a20acb47ffb6b978667258/research/t20-v6-20261012/sources/01b1232252abaaa24a2f90914962d0ad1120528822fcb62cf15e8d0432efb2d7/INTEGRATION_SCOPE_NOTE.md?plain=1#L7-L48), lines 7–48. SHA256 01b1232252abaaa24a2f90914962d0ad1120528822fcb62cf15e8d0432efb2d7; blob 5b3952cf3fd07419fd8ab71a169fa801ed93e7fb; bytes 8817.

## 10. Representation fidelity and the intensional identity boundary

The distinction between a supplied program representation and the existence of any proof is already visible before extensionality is added. This section reconstructs that boundary in the original calculus, shows exactly what the atom/application bridge changes, and proves the older intensional identity theorem against which the positive extensional results must be compared. The proofs come from the complete opaque-atom, bridge, residual-identity and intensional-separation sources. Here F/G names the original unary and heterogeneous predicates, whose full universal-type conditions are used in section 10.5. Their order here is explanatory: the residual source's stopped argument is followed by the later argument that resolves it. It is not a newly open problem. [Opaque representation][opaque-source] [Bridge][bridge-source] [Historical residual question][residual-source] [Full-rule resolution][intensional-source]

### 10.1 Three judgments on the same expressions

Write $`\vdash_0`$ for the original judgment already used above, $`\vdash_+`$ for its bridge-only extension, and $`\vdash_E`$ for the extensional judgment of sections 1–9. These are three different finite inductive judgments on the same raw terms, polynomials, types and telescopes.

| Judgment | Exact source name | Context / formation / typing constructors | Polynomial conversion |
|---|---|---:|---|
| $`\vdash_0`$ | P01AC.Has | 2 / 7 / 18 | The seven original constructors |
| $`\vdash_+`$ | P01AC.Intensional.Plus.HasPlus | 2 / 7 / 18 | Those seven constructors and the atom/application bridge |
| $`\vdash_E`$ | P01AC.ExtensionalRepair.HasE | 2 / 7 / 20 | The same bridge relation as $`\vdash_+`$ |

The seven original conversion constructors are reflexivity, symmetry, transitivity, application congruence and the exposed polynomial $`I,K,S`$ contractions. The bridge is

```math
\mathrm{atom}(rs)\simeq_+
\mathrm{app}(\mathrm{atom}(r),\mathrm{atom}(s)).
```

In moving from $`\vdash_0`$ to $`\vdash_+`$, only the conversion premises of identity introduction and proof-polynomial conversion are changed. Every formation premise, endpoint typing, finite image table, scope condition and dependent motive remains. The bridge is one additional conversion generator, not a nineteenth typing rule. Moving from $`\vdash_+`$ to $`\vdash_E`$ retains all eighteen typing rules and adds precisely the product and universal extensionality rules stated in section 1. [Original declarations][original-syntax] [Exact bridge declarations][bridge-definitions] [Extensional declarations][syntax]

Mutual induction on context, formation and typing derivations gives inclusions into the next system. The inclusion of conversion certificates is an induction on their generators. Thus these inclusions preserve the literal context, polynomial and type:

```math
\Gamma\vdash_0 p:C
\quad\Longrightarrow\quad
\Gamma\vdash_+ p:C
\quad\Longrightarrow\quad
\Gamma\vdash_E p:C.
```

They preserve positive derivations. They do not carry a negative theorem into the larger system. Nor is a theorem requiring a $`\vdash_+`$ derivation a theorem about an arbitrary $`\vdash_E`$ derivation.

We will use $`\zeta`$ for the constant inert-zero term environment. A polynomial is *scope-zero* when it contains no free term-variable node. Type parameters are a different sort: a type over the empty term telescope may still have free type parameters. The closed-identity theorem below retains that possibility and states all its formation, typing and term-scope premises explicitly.

### 10.2 Whole-label replacement in the original calculus

Let $`\mathrm{Finite}(a,C)`$ denote the actual seven-constructor finite derivation judgment of section 1, and define

```math
\mathrm{NoFinite}(a)
\quad\Longleftrightarrow\quad
\forall C\;\neg\mathrm{Finite}(a,C).
```

The finite grammar is unchanged throughout this comparison. Each of $`I,K,S`$ has a finite type, so $`\mathrm{NoFinite}(a)`$ implies that $`a`$ is different from those three primitive labels.

Fix raw terms $`a,b`$. Define $`M=M_{a,b}`$ on polynomials by replacing the **whole label** of the atom $`a`$ by $`b`$, fixing other whole atom labels, fixing variables, and commuting with polynomial application:

```math
M(\mathrm{var}(n))=\mathrm{var}(n),\qquad
M(\mathrm{atom}(r))=
\begin{cases}
\mathrm{atom}(b),&r=a,\\
\mathrm{atom}(r),&r\ne a,
\end{cases}
```

```math
M(\mathrm{app}(p,q))=\mathrm{app}(Mp,Mq).
```

In particular, if another atom's raw label contains $`a`$ as a proper subterm, that label is left intact. Extend $`M`$ structurally to types by mapping identity-endpoint polynomials, and entrywise to telescopes and finite type-image lists.

**Proposition 13 — whole-label preservation.** If $`\mathrm{NoFinite}(a)`$, then $`M_{a,b}`$ preserves every original context, formation and typing derivation:

```math
\mathrm{Ctx}_0(\Gamma)\Rightarrow\mathrm{Ctx}_0(M\Gamma),
\qquad
\Gamma\vdash_0 C\ \mathrm{type}
\Rightarrow M\Gamma\vdash_0 MC\ \mathrm{type},
```

```math
\Gamma\vdash_0 p:C
\quad\Longrightarrow\quad
M\Gamma\vdash_0 Mp:MC.
```

There is no normalization or finite-typability condition on the replacement $`b`$. [Whole-label proof][opaque-source]

**Proof.** The map fixes the primitive atoms $`I,K,S`$. Structural induction gives its exact commuting laws with polynomial renaming and substitution, including the lifted substitution under a binder. It therefore commutes with type term-substitution, weakening, instantiation and the two-coordinate operation $`\mathrm{motiveAt}`$. Type-parameter renaming does not touch polynomial atoms. Structural induction through the mixed substitution consequently gives commutation with type renaming, type weakening, type instantiation and the type-weakened telescope. The finite-code translation $`\mathrm{fin}(C)`$ contains no identity-endpoint polynomials and is fixed.

The map preserves free-variable tests and scope. The actual bracket compiler first tests absence of the bound variable and only then decomposes the polynomial. Since $`M`$ preserves that test, the absent-variable branch remains the same $`K`$ branch; the present variable and application branches use the same fixed $`I,S`$ atoms. Thus

```math
M([x]p)=[x]\bigl(Mp\bigr).
```

This is equality for this particular syntactic map and compiler. It is not a congruence theorem for arbitrary conversion between abstraction bodies. The displayed definitions of pairing, both projections and $`J`$ also commute with $`M`$ because they use only their polynomial arguments, application and the three fixed primitive atoms.

Both lookup constructors are preserved: each changes its target by the actual term weakening, which commutes with $`M`$. Likewise the exact motive telescope
$`\mathrm{Id}_{\mathrm{wk}(C)}(\mathrm{pren}(\mathrm{succ},x),\mathrm{var}(0))::C::\Gamma`$
is mapped to the same construction on the mapped arguments. Bottom-default finite type tables obey

```math
M(\mathrm{typeImages}(\tau,n))
=\mathrm{typeImages}(M\tau,n).
```

Their lengths and finite-code support bounds are unchanged.

Induction over the seven original polynomial-conversion constructors preserves conversion. The equivalence and application cases are immediate; the three contraction cases use the fixed primitive atoms. In a transitivity proof, **every intermediate polynomial** is mapped. No provenance extraction or additional scope restriction on intermediates is required.

Now perform simultaneous induction on the original mutual derivations. The two context cases use the mapped tail and formation premises. In formation, parameters, Bottom and Raw retain the context; products and sums retain the mapped domain and bound body; universal formation uses the mapped type-weakened context; identity formation retains the mapped carrier and both mapped endpoint typings. The eighteen typing cases are as follows.

| Original rule or group | Preservation argument |
|---|---|
| Variable | Map its formed type and its exact weakened lookup. |
| $`I,K,S`$ — three cases | Map every formation premise; the primitive proof atom is fixed and arrows commute with $`M`$. |
| Finite import | Its unchanged certificate $`\mathrm{Finite}(r,C)`$ forces $`r\ne a`$. Reuse that certificate and support bound, map the finite type-image list and all formation premises, and use the commuting law for type substitution. |
| Universal introduction | Map body typing in the type-weakened telescope; the erased polynomial remains the mapped one. |
| Universal elimination | Map the universal type, replacement type, explicit result formation and typing; type instantiation commutes with $`M`$. |
| Raw atom | The original rule admits the replacement raw atom, including when its label changes. |
| Raw application | Map the two Raw typings and the Raw formation premise. |
| Product introduction | Map the bound body and product formation, preserve the scope check, and use the literal bracket-compiler equality. |
| Product elimination | Map both typings, product formation and explicit result formation; term instantiation commutes. |
| Sum introduction | Map both component typings and formation premises; pairing and instantiation commute. |
| First projection | Map the sum typing and both required formations; the projection commutes. |
| Second projection | Map the sum typing and explicit indexed result formation; projection and instantiation commute. |
| Identity introduction | Map the carrier identity formation, both endpoint typings and the complete original polynomial-conversion certificate; the proof atom $`I`$ is fixed. |
| Proof erasure | Map the identity, its proof and Raw formation, then use the same rule. |
| Identity elimination | Map all nine formation/typing premises, including the motive telescope, both motive instances, both endpoints, identity proof and base proof. The endpoint and proof coordinates both commute with $`M`$. |
| Proof-polynomial conversion | Map the formed target, supplied typing, complete conversion certificate and conclusion scope. |

The finite-import step is decisive: the proof does not attempt to transform a finite certificate for the forbidden atom. Such a certificate is excluded by $`\mathrm{NoFinite}(a)`$. These cases exhaust the declared rule populations and prove the proposition. $`\square`$

No raw-algebra homomorphism property of $`r\mapsto M(\mathrm{atom}(r))`$ has been used. The map need not preserve raw application, raw reduction or raw conversion. The original typing and polynomial-conversion rules simply do not inspect a nonprimitive opaque label through those operations.

### 10.3 Equal evaluation need not preserve a supplied typing

Let

```math
D=SII,\qquad \Omega=DD,\qquad
t=SK(K\Omega),\qquad
A_{\mathrm{id}}=\forall\alpha.(\alpha\to\alpha).
```

Write $`w_t`$ for the exposed polynomial

```math
\mathrm{app}(\mathrm{app}(\mathrm{atom}(S),\mathrm{atom}(K)),
\mathrm{app}(\mathrm{atom}(K),\mathrm{atom}(\Omega))).
```

Its evaluation is literally $`t`$ at every term environment.

The inherited normalization boundary supplies

```math
[]\vdash_0 w_t:A_{\mathrm{id}},
\qquad
\mathrm{Finite}(I,\mathrm{identityCode}),
\qquad
\neg\exists u,C\;
\bigl(\mathrm{Finite}(u,C)\land t\simeq u\bigr).
```

The first typing can also be read directly. At a free type parameter $`\alpha`$, Raw admits $`\Omega`$; $`K\Omega:\alpha\to\mathrm{Raw}`$ and $`K:\alpha\to\mathrm{Raw}\to\alpha`$ have the required types for $`S`$. Their exposed application has type $`\alpha\to\alpha`$, and universal introduction closes the type parameter. The target is therefore already inhabited independently by $`I`$.

The stronger last statement is an inherited source-normalization theorem, not a result of a failed search. Every reduct of $`SK(Ku)`$ retains that wrapper and reduces only inside $`u`$; the source's $`\Omega`$ has no normal reduct. Hence $`t`$ has no normal reduct. A finite-typed $`u`$ has a normal reduct, and source confluence would turn $`t\simeq u`$ into a normal reduct of $`t`$, a contradiction. In particular $`\mathrm{NoFinite}(t)`$ holds. The inherited finite-normalization and confluence premises keep their own source and verification roles. [Exact normalization boundary][normalization-boundary]

**Theorem 14 — prescribed representation failure.** The two scope-zero polynomials $`w_t`$ and $`\mathrm{atom}(t)`$ have the same evaluation at every environment, and $`w_t`$ is originally typed at $`A_{\mathrm{id}}`$, but

```math
[]\nvdash_0\mathrm{atom}(t):A_{\mathrm{id}}.
```

Nevertheless $`\mathrm{atom}(t)`$ satisfies both the original unary and full heterogeneous semantic predicates at that type. [Complete opaque-atom argument][opaque-source]

**Proof.** Apply Proposition 13 with $`a=t`$ and $`b=K`$. The carrier $`A_{\mathrm{id}}`$ has no identity-endpoint polynomials, so it is fixed. An alleged typing of $`\mathrm{atom}(t)`$ would therefore give
$`[]\vdash_0\mathrm{atom}(K):A_{\mathrm{id}}`$.

Define the lawful PER consisting of the single conversion class of $`I`$:

```math
P_I(x,y)\quad\Longleftrightarrow\quad
x\simeq I\ \land\ y\simeq I.
```

It is symmetric and transitive, and saturation follows from symmetry and transitivity of raw conversion. Original unary soundness applied to the alleged polymorphic typing of $`K`$, and then instantiated at $`P_I`$, says that $`K`$ preserves this relation. Taking the related inputs $`I,I`$ gives $`KI\simeq I`$. But $`KI`$ and $`I`$ are distinct raw normal forms: the former does not yet have the second argument needed for a $`K`$ contraction. Confluence rules out their conversion. This proves nonderivability.

For semantic validity, apply the original heterogeneous fundamental theorem to the actual typing of $`w_t`$ at the empty telescope's zero-padded environment. Replace its evaluated value by the literally equal evaluation of $`\mathrm{atom}(t)`$. The unary argument is identical. The same supplied representation therefore satisfies the full original semantic conditions while having no original typing at this type. $`\square`$

Using Raw alone would not give the rejection of $`K`$: the raw-conversion arrow relation is too weak. The singleton-class PER is the required test. Also, $`\mathrm{atom}(t)`$ still has type Raw by the original raw-atom rule.

Consequently universal closed packing
$`p\mapsto\mathrm{atom}(\mathrm{eval}(p,\zeta))`$
does not preserve original typings at fixed types. The result concerns a prescribed representation. It does not show that the same raw program has no well-typed representation: $`w_t`$ is one. It does not refute completeness that permits choosing another representation, or finite representability up to a separately specified PER equality.

The argument has a useful general form. Suppose $`\mathrm{NoFinite}(a)`$,
$`[]\vdash_0 C\ \mathrm{type}`$,
$`[]\vdash_0\mathrm{atom}(a):C`$, and, for the chosen $`b`$,

```math
M_{a,b}(C)=C.
```

Then Proposition 13 gives $`[]\vdash_0\mathrm{atom}(b):C`$. This **exact type-fixity equation** is the relevant condition. A convenient sufficient condition, uniform in $`b`$, is that no identity-endpoint polynomial in $`C`$ contains the whole atom $`a`$. Avoidance is tested structurally through the type and polynomial constructors; proper raw subterms hidden inside another atom label are not examined. Avoidance is sufficient, not necessary for the exact equation. Every finite-code type satisfies it.

If some lawful original interpretation rejects some $`b`$ at $`C`$, unary soundness now forbids the original opaque typing of a nonfinite $`a`$ whenever this fixity condition holds. In ordinary classical mathematics, a resulting necessary condition is

```math
[]\vdash_0\mathrm{atom}(a):C
\quad\Longrightarrow\quad
\exists B\;\mathrm{Finite}(a,B),
```

provided the stated formation, avoidance and semantic-rejection hypotheses hold. The finite code $`B`$ need not be $`C`$ or its finite-code antecedent. This is neither a sufficient condition nor an extraction algorithm from a typing proof. Its existence formulation uses the classical passage from failure of $`\mathrm{NoFinite}(a)`$ to a finite certificate. At Raw every raw term is self-related, so the required semantic rejection is unavailable.

A second witness makes the conversion boundary sharper. Put

```math
d=(KI)\Omega.
```

There is a root contraction $`d\longrightarrow I`$, so $`d`$ has a finite-typed representative at exactly the desired code $`\mathrm{identityCode}`$. But the three-step cycle of $`\Omega`$ can also be reduced inside the discarded argument, giving a cycle of $`d`$. Thus $`d`$ is weakly normalizing and not strongly normalizing. The inherited finite-typing normalization theorem implies $`\mathrm{NoFinite}(d)`$. Applying the same replacement argument and the same rejecting PER gives

```math
\exists v\;
\bigl(\mathrm{Finite}(v,\mathrm{identityCode})\land d\simeq v\bigr),
\qquad
[]\nvdash_0\mathrm{atom}(d):A_{\mathrm{id}}.
```

The witness on the left is $`v=I`$. This defeats transport from a finite representative even when its finite code exactly matches the target. It is a failure of backward expansion or conversion transport between supplied opaque atoms. It is not a counterexample to forward subject reduction.

The exposed polynomial $`K\,I\,\mathrm{atom}(\Omega)`$ remains originally typed at $`A_{\mathrm{id}}`$: its original polynomial $`K`$ contraction gives conversion to the already typed atom $`I`$, and the conversion rule can be used in reverse with the scope-zero check. It evaluates to $`d`$. This second example therefore also preserves existence of a different representation. The cycle and finite-normalization premise are inherited source facts; the conclusion about the supplied opaque atom is the whole-label consequence. [Discarded-loop argument and limits][opaque-source] [Literal cycle][discarded-loop-source]

#### Operational identity and the reviewed normalization boundary

Applying the first witness to an argument helps locate its exact negative claim. For every raw $`a`$,

```math
(SK(K\Omega))a\longrightarrow
Ka\bigl((K\Omega)a\bigr)\longrightarrow a.
```

This finite reduction establishes the displayed behavior after application. It neither supplies a normal reduct of the unapplied $`t`$ nor identifies $`t`$ with $`I`$ by raw conversion. In the unapplied wrapper $`SK(Kq)`$, the outer $`S`$ has only two arguments and the inner $`K`$ only one, so neither is a head redex. With the full compatible reduction relation, every step is inside $`q`$ and preserves the wrapper. Conversely every step of $`q`$ lifts through it. The wrapper is normal exactly when $`q`$ is normal. Combined with the inherited all-reduct obstruction for $`\Omega`$, this gives the no-normal-reduct premise used above; it is not an argument from failure of one evaluation strategy. [R18-G060, §§“Exact negative result”, “Independent discriminators”][R18-G060]

The independent review checks the stronger quantification over **every** finite-typed raw $`u`$ at **any** finite code, not just rejection of the identity code for $`t`$. A finite-typed $`u`$ has a normal reduct; conversion and Church–Rosser would join it with $`t`$, forcing a normal reduct of $`t`$ and giving the contradiction. The discarded-loop $`KI\Omega`$ is the necessary contrasting control: it reduces to $`I`$ despite lacking strong normalization, and therefore cannot supply this stronger no-convertible-finite-representative conclusion. The distinction from equivalence under a separately declared PER also remains essential. These are qualifications of the already proved boundary in this subsection, not another normalization theorem or a new calculus. [R18-G060, §§“Exact negative result”–“Ownership and interpretation”][R18-G060]

The review's positive certificate concerns the literal exposed application polynomial and its closed old polymorphic identity typing, with Raw used for the $`\Omega`$ premise. It does not replace that polynomial by the opaque atom with the same evaluation. Its recorded formal assessment used a selected 48-source closure, including the audit support, and retained the inherited normalization and confluence premises. Those are historical, bounded automated-review claims. This exposition has not rerun that closure, rebuilt its dependencies or promoted its verdict to external human peer review. The mathematical arguments and the source's reported execution remain separate evidence. [R18-G060, §§“Contract and source binding”, “Literal positive result”, “Reproduction and evidence”][R18-G060]


### 10.4 What the bridge repairs

The prior dependent-All design had already identified the mismatch between an application of two atom polynomials and the single atom of their raw application, and explicitly excluded the bridge from the retained calculus. The bridge source records that design choice and assesses a hypothetical reconsideration of it. The following result inherits that assessment; it does not discover a previously unrecognized option or authorize an implementation migration. [Prior design and hypothetical scope][bridge-source]

**Theorem 15 — closed conversion and typing transfer.** For scope-zero polynomials $`p,q`$,

```math
p\simeq_+q
\quad\Longleftrightarrow\quad
\mathrm{eval}(p,\zeta)\simeq\mathrm{eval}(q,\zeta).
```

Consequently, if
$`[]\vdash_+ C\ \mathrm{type}`$,
$`[]\vdash_+p:C`$,
$`p,q`$ are scope-zero, and their evaluated raw terms are convertible, then
$`[]\vdash_+q:C`$.
The type is the same literal $`C`$; it may have free type parameters. [Bridge theorem][bridge-source]

**Proof.** Induction on the eight conversion generators proves evaluation soundness at every environment. The seven old cases use raw equivalence, application congruence and the source contractions. In the bridge case both sides evaluate to the same raw application, so reflexivity suffices.

For packing, induct on a scope-zero polynomial $`p`$. The variable case is impossible. An atom packs by reflexivity. In an application, pack each subpolynomial by induction, apply congruence and then the reverse bridge. This gives

```math
p\simeq_+\mathrm{atom}(\mathrm{eval}(p,\zeta)).
```

The same induction proves that its evaluation is independent of the environment.

Next lift any raw one-step reduction to conversion between its two atoms. For the $`I,K,S`$ contractions, expose respectively one, two or three application nodes by the bridge and apply the corresponding polynomial contraction. In the $`S`$ case, repack the two inner applications and then the outer one. For a compatible left or right step, expose the outer application, use the induction conversion in the appropriate child and repack. These are all five source-step cases. Induction on raw conversion then proves

```math
r\simeq s
\quad\Longrightarrow\quad
\mathrm{atom}(r)\simeq_+\mathrm{atom}(s).
```

The reverse implication follows from evaluation soundness. Composing packing, raw-to-atom conversion and reverse packing proves the displayed closed-polynomial equivalence. The original scoped conversion rule of $`\vdash_+`$ then gives the typing consequence. $`\square`$

This also repairs closed typing transport under literal evaluation equality, since equality supplies raw conversion. In particular, the embedded typing of $`w_t`$ now packs to $`\mathrm{atom}(t)`$ at $`A_{\mathrm{id}}`$. The exposed discarded-loop polynomial similarly packs to $`\mathrm{atom}(d)`$. Neither raw term acquires a direct finite derivation: the finite grammar and its normalization theorem have not changed.

The failure of the old replacement invariant is visible in one bridge instance:

```math
\mathrm{atom}(d)\simeq_+
\mathrm{app}(\mathrm{atom}(KI),\mathrm{atom}(\Omega)).
```

Replace only the whole label $`d`$ by $`K`$. The left evaluation becomes $`K`$ while the right stays $`d`$. If this transformed pair were still convertible, evaluation soundness and $`d\simeq I`$ would imply $`K\simeq I`$, contrary to normal-form uniqueness. The bridge exposes precisely the raw application structure that the old invariant was allowed to ignore.

Original F/G soundness is preserved by a fresh mutual proof for the bridge judgment. Context and formation cases use their own smaller semantic induction conclusions; they are not assumed to have old formation certificates. All unchanged typing cases use the same semantic-rule arguments. For proof conversion, evaluation soundness supplies a raw conversion at each of the two environments, and two-sided saturation transfers the relation at the fixed type. For identity introduction, the old helper's literal signature requires old polynomial conversion and cannot simply be applied. Its mathematical proof needs only the two evaluation-conversion facts: typed endpoint membership and raw saturation supply carrier equality, while the introduced proof $`I`$ satisfies the proof clauses. Reproving that helper with the new conversion soundness supplies the remaining case. This is a new induction over the fresh grammar, not a reinterpretation of an old theorem's argument type. [Bridge soundness argument][bridge-source] [Original simultaneous induction][original-soundness] [Identity helper][original-term-lemmas]

Scope-zero remains substantive. An open variable cannot pack into one fixed raw atom with its valuation-dependent value. A proposed conversion $`\mathrm{var}(0)\simeq_+\mathrm{atom}(r)`$, evaluated at environments giving that variable $`I`$ and $`K`$, would force $`I\simeq K`$. This excludes that fixed-atom proposal; it does not exclude a separately specified environment representation or translation between open syntaxes. The bridge theorem neither decides raw conversion nor identifies equality in an arbitrary PER with raw conversion. It transfers a supplied typing across the displayed raw relation and does not supply full semantic completeness.


The exact bridge supplement establishes this fixed-type transfer by a new mutual proof for the copied context, formation and typing rules; its closed packing theorem still requires scope-zero polynomial endpoints. It neither extends the seven-rule `FiniteDerives` relation nor authorizes replacing a whole opaque label inside an old derivation. Those distinctions are the substantive content retained above, not a declaration that the hypothetical calculus has been adopted. [Q250A-006]

### 10.5 The identity question that packing leaves open

Set

```math
k_{\mathrm{id}}=SKK,\qquad
u=\mathrm{atom}(I),\qquad
v=\mathrm{atom}(k_{\mathrm{id}}),\qquad
B_{\mathrm{id}}=\mathrm{Id}_{A_{\mathrm{id}}}(u,v).
```

Both endpoints have original finite polymorphic identity typings. For $`I`$ the certificate is universal introduction over its usual arrow typing. For $`SKK`$, at a type variable $`X`$, instantiate the finite $`S`$ rule with types $`X`$, $`X\to X`$, $`X`$, then apply $`K:X\to(X\to X)\to X`$ and $`K:X\to X\to X`$. This yields $`SKK:X\to X`$, and finite universal introduction gives the required closed code. The original finite-import and formation rules therefore form $`B_{\mathrm{id}}`$ and type both endpoints at $`A_{\mathrm{id}}`$. These derivations embed into $`\vdash_+`$.

To state the old semantic witness precisely, let $`F`$ and $`G`$ denote the original unary and heterogeneous predicates, respectively. They include the source's recursive uniformity conditions for universal types, not just an unqualified intersection of unary carriers. The actual endpoint typings supply each endpoint's own universal uniformity conjuncts. For every lawful PER $`P`$ and $`P`$-related inputs $`x,y`$,

```math
Ix\simeq x,\qquad k_{\mathrm{id}}y\simeq y
\quad\Longrightarrow\quad P(Ix,k_{\mathrm{id}}y).
```

Saturation gives the last relation. Together with those inherited uniformity conjuncts, this proves

```math
F(A_{\mathrm{id}},\rho,\zeta,I,k_{\mathrm{id}})
```

for every lawful object environment $`\rho`$. It is the full inherited polymorphic witness, unpacked at this carrier.

The old identity clauses are

```math
F(B_{\mathrm{id}},\rho,\zeta,r,s)
\quad\Longleftrightarrow\quad
F(A_{\mathrm{id}},\rho,\zeta,I,k_{\mathrm{id}})
\land r\simeq I\land s\simeq I,
```

and

```math
G(B_{\mathrm{id}},R,\zeta,\zeta,r,s)
\quad\Longleftrightarrow\quad
F(A_{\mathrm{id}},R_{\mathrm{left}},\zeta,I,k_{\mathrm{id}})
\land F(A_{\mathrm{id}},R_{\mathrm{right}},\zeta,I,k_{\mathrm{id}})
\land r\simeq I\land s\simeq I.
```

Thus the single scope-zero polynomial $`\mathrm{atom}(I)`$ satisfies both full predicates at the formed closed type $`B_{\mathrm{id}}`$. In particular this does not replace heterogeneous validity by a unary surrogate. [Original predicate definitions][original-predicates] [Residual semantic witness][residual-source]

On the other hand, $`I`$ and $`SKK`$ are distinct normal forms of the unchanged raw calculus. The $`S`$ expression has only two arguments. Confluence gives $`I\not\simeq SKK`$, so Theorem 15 excludes $`u\simeq_+v`$. This blocks direct identity introduction at $`B_{\mathrm{id}}`$.

That observation alone was the precise stopping point of the residual source. An identity conclusion can also arise through $`J`$, application, universal elimination or conversion of an existing proof polynomial. Excluding one possible last rule is not a proof that every derivation is absent. The fact that old semantic proof witnesses convert to $`I`$ constrains the **proof source**; it does not force raw conversion of the **identity endpoints**. An earlier raw-index identity-admission theorem belongs to a different type grammar and supplies no unproved reverse translation of these derivations. The accepted legacy and nucleus comparisons also run into the original calculus; they do not supply an inverse translation of arbitrary bridge-only derivations. The whole-label argument also cannot fill the gap: both $`I`$ and $`SKK`$ have finite certificates, and its preservation step has already failed for the bridge.

A tempting alternate interpretation fails for a concrete reason. Keep the old type and context relations, but strengthen the identity predicate by requiring raw conversion of its endpoints. In the original formed context $`[A_{\mathrm{id}}]`$, consider the formed family

```math
T(x)=\mathrm{Id}_{A_{\mathrm{id}}}(x,\mathrm{atom}(I)).
```

The variable and constant endpoints have the required original typings; a finite import supplies the constant in this formed context. The old context relation relates $`I::\zeta`$ and $`SKK::\zeta`$, because the head values are related at $`A_{\mathrm{id}}`$. Yet the strengthened fiber admits the proof source $`I`$ at the first environment and rejects it at the second. The endpoint memberships themselves still hold; raw endpoint conversion is what changes.

Consequently that isolated modification violates the hereditary transport law for a formed family along the retained context relation. Dependent product, sum and $`J`$ soundness cannot be assumed for it. This counterexample does not exclude every intensional interpretation. It says that the rest of the type and context equalities must be changed coherently and the whole rule system then validated. The following construction does that. [Failed shortcut and exact stopped obligation][residual-source]

### 10.6 A coherent interpretation of all eighteen rules

The construction uses all raw-conversion-saturated subsets of the raw term set $`\mathbb T`$:

```math
\mathfrak S=
\{X\subseteq\mathbb T:
r\simeq s\Rightarrow(r\in X\Longleftrightarrow s\in X)\}.
```

Empty, the full raw set and every individual conversion class belong to $`\mathfrak S`$. This is an ordinary subset of a powerset. Saturation is also equivalent to the inherited unary Code's stability in both directions along each step: induct over conversion for one implication and restrict to a step for the other. The construction is not a new universe of arbitrary functions decoded as source programs. The intensional source explicitly credits the earlier P01 U11 study *Contextual dependence, J and the abstraction-congruence obstruction*, especially sections 1–3 and 5–7, for conversion-coherent unary codes and telescopes, dependent products and represented pairs, the identity predicate with both endpoint memberships and proof conversion to $`I`$, two-coordinate based $`J`$, and intersection All. That earlier study stopped before the full finite-syntax soundness theorem and retained the abstraction-congruence obstruction. The later source supplies the exact eighteen-rule proof reconstructed here. This preserves its attribution; it does not claim a fresh complete reading or revalidation of U11. [Full written construction and provenance][intensional-source]

For $`\rho:\mathbb N\to\mathfrak S`$ and a total raw term environment $`\eta`$, define sets $`\lvert C\rvert_{\rho,\eta}`$ by structural recursion:

```math
\lvert\alpha_n\rvert_{\rho,\eta}=\rho(n),\qquad
\lvert\bot\rvert_{\rho,\eta}=\varnothing,\qquad
\lvert\mathrm{Raw}\rvert_{\rho,\eta}=\mathbb T,
```

```math
f\in\lvert\Pi x:C.D\rvert_{\rho,\eta}
\quad\Longleftrightarrow\quad
\forall a\in\lvert C\rvert_{\rho,\eta},\
fa\in\lvert D\rvert_{\rho,a::\eta},
```

```math
z\in\lvert\Sigma x:C.D\rvert_{\rho,\eta}
\quad\Longleftrightarrow\quad
\exists a,b,\
a\in\lvert C\rvert_{\rho,\eta}
\land b\in\lvert D\rvert_{\rho,a::\eta}
\land z\simeq\langle a,b\rangle,
```

```math
r\in\lvert\mathrm{Id}_C(p,q)\rvert_{\rho,\eta}
\quad\Longleftrightarrow\quad
\mathrm{eval}(p,\eta)\in\lvert C\rvert_{\rho,\eta}
\land\mathrm{eval}(q,\eta)\in\lvert C\rvert_{\rho,\eta}
\land\mathrm{eval}(p,\eta)\simeq\mathrm{eval}(q,\eta)
\land r\simeq I,
```

```math
\lvert\forall\alpha.D\rvert_{\rho,\eta}
=\bigcap_{X\in\mathfrak S}\lvert D\rvert_{X::\rho,\eta}.
```

Both endpoint memberships and the proof-source condition are present in the identity clause. The sum predicate uses an actual represented pair up to conversion. The universal clause is an intersection of sets obtained by recursion on the **smaller type expression** $`D`$; its quantifier over all saturated sets does not change that recursion.

#### Saturation and coherence

Every raw type, whether formed or not, denotes a member of $`\mathfrak S`$. Parameters use their assigned saturation, and Bottom and Raw are immediate. In a product, $`f\simeq g`$ implies $`fa\simeq ga`$ for each argument, so the body's saturation transfers membership. In a sum, keep the same witnesses and compose the represented-pair conversion. In an identity, endpoint conditions are independent of the witness and $`r\simeq I`$ is invariant under conversion of $`r`$. An intersection of saturated sets is saturated. These are all seven type cases.

Write $`\eta\simeq\xi`$ when the environments are pointwise raw-convertible. A second structural induction proves

```math
\eta\simeq\xi
\quad\Longrightarrow\quad
\lvert C\rvert_{\rho,\eta}=\lvert C\rvert_{\rho,\xi}.
\tag{10.1}
```

For products, the domain sets agree and, at each fixed argument $`a`$, the body environments $`a::\eta`$ and $`a::\xi`$ are pointwise convertible. The same argument retains the sum's witnesses. For an identity, structural induction on polynomials gives conversion of each evaluated endpoint across the two environments. Carrier coherence and saturation transfer both endpoint memberships, and equivalence of raw conversion transfers their mutual-conversion condition. Universal types use the body equality for each $`X::\rho`$. The other cases are independent of the term environment.

The induced binary type relation is

```math
R_C^{\rho,\eta}(r,s)
\quad\Longleftrightarrow\quad
r\in\lvert C\rvert_{\rho,\eta}
\land s\in\lvert C\rvert_{\rho,\eta}
\land r\simeq s.
```

It is a saturated PER with the displayed set as support, and (10.1) makes it coherent. Crucially, **every** such relation refines raw conversion, including the product and universal relations. Both $`I`$ and $`SKK`$ can have product membership without being related by this binary relation. This coherently differs from the old extensional/parametric carrier relations; it is not a projection preserving all their equalities or heterogeneous links.

#### The actual substitutions

For a polynomial substitution $`\sigma`$, put $`\eta_\sigma(n)=\mathrm{eval}(\sigma(n),\eta)`$. Direct structural induction gives

```math
\mathrm{eval}(\mathrm{psub}(\sigma,p),\eta)
=\mathrm{eval}(p,\eta_\sigma).
\tag{10.2}
```

The variable case selects an image, the atom case leaves its raw label intact, and application uses the two induction equalities. The lifted substitution satisfies the literal image equation
$`\mathrm{images}(\mathrm{pup}(\sigma),a::\eta)=a::\eta_\sigma`$.
Induction over all seven type constructors therefore gives

```math
\lvert\mathrm{subst}(\sigma,C)\rvert_{\rho,\eta}
=\lvert C\rvert_{\rho,\eta_\sigma}.
\tag{10.3}
```

In an identity use (10.2) for both endpoints. Under a product or sum use the lifted image equation at each argument; All leaves the term substitution unchanged. In particular,

```math
\lvert\mathrm{wk}(C)\rvert_{\rho,a::\eta}
=\lvert C\rvert_{\rho,\eta},\qquad
\lvert\mathrm{inst}(D,p)\rvert_{\rho,\eta}
=\lvert D\rvert_{\rho,\mathrm{eval}(p,\eta)::\eta},
```

```math
\lvert\mathrm{motiveAt}(D,y,e)\rvert_{\rho,\eta}
=\lvert D\rvert_{\rho,\mathrm{eval}(e,\eta)::\mathrm{eval}(y,\eta)::\eta}.
\tag{10.4}
```

Proof is coordinate zero and endpoint is coordinate one. The source arrow is $`\Pi C.\mathrm{wk}(D)`$, so its interpretation is the set of raw terms taking arguments from $`\lvert C\rvert_{\rho,\eta}`$ into the **outer** set $`\lvert D\rvert_{\rho,\eta}`$; its codomain is not reevaluated at the introduced argument.

Type renaming satisfies

```math
\lvert\mathrm{trename}(r,C)\rvert_{\rho,\eta}
=\lvert C\rvert_{\rho\circ r,\eta}.
\tag{10.5}
```

The identity endpoints are literally unchanged. In the All case, the lifted renaming fixes the fresh head and applies $`r`$ only to the tail. Hence
$`\lvert\mathrm{twk}(C)\rvert_{X::\rho,\eta}=\lvert C\rvert_{\rho,\eta}`$.

For simultaneous term/type substitution, evaluate the replacement type images in the original term environment:

```math
\mu(n)=\lvert\tau(n)\rvert_{\rho,\eta}.
```

Each is saturated by the preceding induction, even if $`\tau(n)`$ is term-dependent. The exact mixed law is

```math
\lvert\mathrm{mixed}(\sigma,\tau,C)\rvert_{\rho,\eta}
=\lvert C\rvert_{\mu,\eta_\sigma}.
\tag{10.6}
```

Here $`\mu`$ is evaluated at $`\eta`$, not at $`\eta_\sigma`$ or at a newly bound argument. The parameter case is its definition. The identity case uses the carrier induction and (10.2). Under a product or sum, the source lifts $`\sigma`$ and replaces each type image by $`\mathrm{wk}(\tau(n))`$. At $`a::\eta`$ the latter still interprets as $`\mu(n)`$ by (10.3), while the lifted term images are $`a::\eta_\sigma`$. Thus the body induction has exactly the required unchanged $`\mu`$. Under All, the source's lifted type images have a fresh parameter at zero and type-weakened old images afterwards. Equation (10.5) makes their interpretations exactly $`X::\mu`$, with the same term-image environment. Intersecting the body equality over $`X`$ completes the proof. Bottom and Raw are immediate.

Taking the identity term substitution gives

```math
\lvert\mathrm{tsubst}(\tau,C)\rvert_{\rho,\eta}
=\lvert C\rvert_{n\mapsto\lvert\tau(n)\rvert_{\rho,\eta},\eta},
\qquad
\lvert\mathrm{tinst}(D,C)\rvert_{\rho,\eta}
=\lvert D\rvert_{\lvert C\rvert_{\rho,\eta}::\rho,\eta}.
\tag{10.7}
```

These equations cover arbitrary source replacement types, including dependent types and nested universal types. They do not invoke an old F/G substitution theorem with unverified premises. [Literal type operations][original-syntax] [Polynomial operations and compiler][original-polynomials]

#### Zero-padded contexts and both motive coordinates

Define telescope membership by

```math
V_{[]}(\rho,\eta)\Longleftrightarrow\eta=\zeta,\qquad
V_{C::\Gamma}(\rho,a::\eta)
\Longleftrightarrow
V_\Gamma(\rho,\eta)\land a\in\lvert C\rvert_{\rho,\eta}.
```

A declaration is interpreted at the tail environment before its binder is entered. No nonemptiness of a telescope is inferred from its formation.

Define context relatedness recursively by requiring the two zero environments at the empty telescope and, at an extension, related tails and $`R_C`$-related heads in the left tail fiber. Induction on the telescope, using (10.1), shows that this is exactly

```math
V_\Gamma(\rho,\eta)\land V_\Gamma(\rho,\xi)\land\eta\simeq\xi.
```

It is therefore a PER on the admitted zero-padded environments. This is not a claim that arbitrary pointwise-convertible total environments preserve literal zero-padding; both displayed membership conditions are retained.

The exact lookup lemma follows from its two constructors. At zero, the declaration's head membership is initially at the tail environment, and the result type is $`\mathrm{wk}(C)`$; (10.3) identifies that set at the extended environment. At successor, apply the lookup induction to the tail and then the same weakening equality. Thus

```math
\mathrm{Lookup}(\Gamma,n,C)\land V_\Gamma(\rho,\eta)
\quad\Longrightarrow\quad
\eta(n)\in\lvert C\rvert_{\rho,\eta}.
\tag{10.8}
```

Lookup is not unshifted list access. Induction on the telescope also gives the precise All-context equation

```math
V_{\mathrm{twkTel}(\Gamma)}(X::\rho,\eta)
\quad\Longleftrightarrow\quad
V_\Gamma(\rho,\eta).
\tag{10.9}
```

At an extension, use (10.5) for its type-weakened declaration; at the empty telescope both sides require $`\eta=\zeta`$. This is the context shift that prevents generalizing a fixed type-dependent term assumption.

For $`J`$, put $`x_0=\mathrm{eval}(x,\eta)`$, $`y_0=\mathrm{eval}(y,\eta)`$ and $`e_0=\mathrm{eval}(e,\eta)`$. Unfold the actual motive telescope from section 10.2 and use weakening. Its membership condition at $`e_0::y_0::\eta`$ is exactly

```math
V_\Gamma(\rho,\eta)\land
x_0,y_0\in\lvert C\rvert_{\rho,\eta}\land
x_0\simeq y_0\land e_0\simeq I.
\tag{10.10}
```

When this holds, both $`I::x_0::\eta`$ and $`e_0::y_0::\eta`$ are admitted motive environments and are pointwise convertible. The comparison uses the endpoint and proof coordinates separately. This is the transport fact used in the full typing proof.

#### Finite import with the literal image table

For a finite type code $`C`$, define $`J_\rho(C)`$ using $`\rho(n)`$ at a variable, the empty set at Bottom, the raw-term arrow at an arrow code, and intersection over all $`X\in\mathfrak S`$ at a universal code. Structural induction gives saturation and

```math
\lvert\mathrm{fin}(C)\rvert_{\rho,\eta}=J_\rho(C).
\tag{10.11}
```

Finite-code renaming and substitution commute with $`J`$. At a type binder the lifted renaming fixes the fresh head; the lifted substitution supplies that fresh parameter and renames each old image under it. The finite instantiation equation is consequently

```math
J_\rho(\mathrm{instantiateType}(C,D))
=J_{J_\rho(D)::\rho}(C).
\tag{10.12}
```

The selected P01DependentSubstitution body violates the old-image part of that binder contract. Its liftTypes maps the fresh parameter to param 0 but maps successor n directly to σ n; the All interpretation argument requires the latter image to be renamed beneath the new type binder. For σ 0=param 0, the written successor image remains param 0 rather than param 1. The separate term-index lift under Pi and Sigma does not prevent this type-parameter capture. The declared interpretation, instantiation and relation transfers therefore retain this unresolved exact-definition obligation. This is a syntactic mismatch in the supplied variant, not a newly observed typechecker failure or a criticism of the finite-code lift stated above. [A750-T50-115](../research/t20-v6-20261012/sources/c47660fa966b32286b445a42f9c4c04436e3fe33dcd23b8a93299796fa5fdf75/P01DependentSubstitution.lean#L68-L96) [A750-T50-115](../research/t20-v6-20261012/sources/c47660fa966b32286b445a42f9c4c04436e3fe33dcd23b8a93299796fa5fdf75/P01DependentSubstitution.lean#L114-L170)

**Finite soundness for this interpretation** follows by induction on all seven finite constructors, universally quantified over $`\rho`$.

1. For $`I:C\to C`$, use $`Ia\simeq a`$ and saturation.
2. For $`K:C\to D\to C`$, use $`Kab\simeq a`$ and saturation of the outer result set.
3. For $`S`$, if $`f\in X\Rightarrow(Y\Rightarrow Z)`$, $`g\in X\Rightarrow Y`$ and $`a\in X`$, then $`fa(ga)\in Z`$; $`Sfga\simeq fa(ga)`$ gives the required membership.
4. Application applies the function induction conclusion to the argument conclusion in the same environment.
5. Universal introduction uses the single premise's induction conclusion at every $`X::\rho`$. The finite grammar has no term context to be improperly generalized.
6. Universal elimination selects the saturated set $`J_\rho(D)`$ and uses (10.12). The code $`D`$ may itself contain a universal type.
7. Reduction uses its actual finite reduction certificate, hence raw conversion, and saturation.

For the outer typing rule, retain its literal finite list $`\tau`$, support bound, formed images, formed result and finite certificate. Let $`\bar\tau=\mathrm{typeImages}(\tau)`$ and
$`\mu(n)=\lvert\bar\tau(n)\rvert_{\rho,\eta}`$.
Out-of-range images are Bottom and therefore interpret as the empty set. Equations (10.7) and (10.11) give

```math
\lvert\mathrm{tsubst}(\bar\tau,\mathrm{fin}(C))\rvert_{\rho,\eta}
=J_\mu(C).
```

The finite soundness induction supplies the imported raw term in exactly this set. Although the semantic argument works for arbitrary such saturated images, the syntactic rule still requires its original finite table, support bound and formation premises. A stronger semantic lemma is not authorization to remove them. [Seven-constructor finite grammar][finite-grammar]

The retained generated export slices separate certificate acceptance, exact erasure and semantic soundness. Each constructs a Checked value from check 0, states its literal term and type by decide, then obtains acceptance for every interpretation environment by rewriting checked_sound with those two equalities. In Exports001 the nested identity applications remain in the stated erased terms, whereas Exports004 uses explicit one-, two- and three-step certificates whose erasure is I. Exports002 supplies K/S instances, and Exports007 retains seven distinct seven-binder identity types selecting variables 0 through 6 despite their common erasure I. These are concrete consumers of the imported checker/soundness interface, not additional proofs of that interface. Every slice explicitly marks the generated text UNCOMPILED; JSON-digest comments and theorem-shaped declarations are not compiler-acceptance receipts. [source 230](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/47b3355312f02f1eee8a6b57e7c8012a4fe190b1ddff4243eee57f1fc5c547fe/Exports001.lean#L1-L166) [source 102](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/30a998496379d5ff20f9f32b60d02ca9ccab08ca495635830c6e19adbed58fc0/Exports002.lean#L1-L166) [source 16](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/1e7f5125b90cdf2d18c1c999dae426b681affaea89d64179e92fd286380f285d/Exports004.lean#L1-L166) [source 22](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/1f361994b99f881086b02b4b34cf2d8530a67f93aba34ab56f310d4b6df2e301/Exports007.lean#L1-L76)

#### All typing constructors

**Theorem 16 — intensional soundness.** If $`\Gamma\vdash_+p:C`$, then for every $`\rho:\mathbb N\to\mathfrak S`$ and every $`V_\Gamma(\rho,\eta)`$,

```math
\mathrm{eval}(p,\eta)\in\lvert C\rvert_{\rho,\eta}.
```

The same result holds for original $`\vdash_0`$ derivations by inclusion. [Full eighteen-rule proof][intensional-source]

**Proof.** Use simultaneous induction on the actual mutual context, formation and typing derivations, with the typing conclusion quantified over both environments. The two context cases use the stated empty environment and extension. The seven formation cases use the already proved saturation and coherence for the corresponding raw constructors; All additionally uses (10.9), and identity retains its four-conjunct predicate and both endpoint typings. They assert no inhabitedness of an arbitrary formed context.

For typing, the eighteen cases have the following proofs.

1. **Variable.** Apply the actual lookup lemma (10.8); evaluation selects that coordinate.

2. **$`I`$.** The arrow interpretation has the same domain and codomain set. For an argument in it, $`Ia\simeq a`$ and saturation prove membership.

3. **$`K`$.** At the outer environment the source's weakened arrows interpret as $`X\Rightarrow(Y\Rightarrow X)`$. For $`a\in X,b\in Y`$, use $`Kab\simeq a`$. The weakenings keep $`X,Y`$ at that outer environment.

4. **$`S`$.** At the same outer environment, its type interprets as
$`(X\Rightarrow(Y\Rightarrow Z))\Rightarrow((X\Rightarrow Y)\Rightarrow(X\Rightarrow Z))`$.
The memberships of $`f,g,a`$ put $`fa(ga)`$ in $`Z`$; its conversion from $`Sfga`$ finishes the case.

5. **Finite import.** Apply the preceding seven-case finite proof with the actual finite image list and the mixed-substitution equation. No old semantic soundness theorem is substituted for this new interpretation.

6. **Universal introduction.** For each saturated $`X`$, equation (10.9) makes the unchanged term environment admissible for the smaller derivation in the type-weakened telescope. Its induction conclusion puts the same evaluated polynomial in the body at $`X::\rho`$. Intersect over $`X`$.

7. **Universal elimination.** The smaller derivation belongs to every body instance. Choose $`X=\lvert A\rvert_{\rho,\eta}`$ for the actual formed replacement type $`A`$; it is saturated. Equation (10.7) identifies the exact instantiated result, including term-dependent replacement types.

8. **Raw atom.** Its evaluated raw label belongs to the full raw set.

9. **Raw application.** Its evaluation is also a raw term. Both smaller Raw typings remain source-rule premises.

10. **Product introduction.** For $`a`$ in the domain, telescope extension admits $`a::\eta`$. The body induction gives its evaluated body in the corresponding fiber. The exact bracket compiler satisfies
$`\mathrm{eval}([x]b,\eta)a\longrightarrow^*\mathrm{eval}(b,a::\eta)`$:
the absent-variable branch is one $`K`$ contraction, the variable branch is $`I`$, and the application branch is $`S`$ followed by the two compatible induction reductions. Saturation of that fiber proves function membership. The source scope condition remains, and no abstraction-congruence principle is used.

11. **Product elimination.** Apply function membership to the evaluated typed argument. Equation (10.4) for instantiation makes the resulting fiber exactly the conclusion type.

12. **Sum introduction.** The two smaller typings and instantiation equation give witnesses $`a,b`$ in the required domain and fiber. The literal pair polynomial evaluates to their represented pair.

13. **First projection.** Choose witnesses $`a,b`$ from the sum induction conclusion. Conversion to their pair and the pair projection equation give $`\pi_1z\simeq a`$. Domain saturation proves the first projection typing.

14. **Second projection.** The same witnesses give $`\pi_1z\simeq a`$ and $`\pi_2z\simeq b`$. Saturation puts $`\pi_2z`$ in the body fiber at $`a::\eta`$; coherence (10.1) changes it to the fiber at $`\pi_1z::\eta`$. The instantiation equation identifies the actual indexed target.

15. **Identity introduction.** The endpoint induction conclusions give both memberships. Soundness of the actual eight-generator conversion certificate gives their raw conversion. The introduced witness is $`I\simeq I`$, completing all four conjuncts.

16. **Proof erasure.** The evaluated proof is a raw term and hence lies in the Raw set. This does not manufacture an identity between endpoints at another carrier.

17. **Identity elimination.** The identity-proof induction conclusion gives $`x_0,y_0`$ in the carrier, $`x_0\simeq y_0`$ and $`e_0\simeq I`$. The base-proof induction and (10.4) put its value $`d_0`$ in the motive fiber at $`I::x_0::\eta`$. Equation (10.10) admits both this environment and $`e_0::y_0::\eta`$; coherence (10.1), in **both coordinates**, transports $`d_0`$ to the latter fiber. This is precisely the target motive instance. The literal $`J`$ polynomial reduces by two $`K`$ contractions to $`d_0`$, so saturation of that target fiber proves the conclusion. Arbitrary syntactic proof dependence of the motive is covered because coherence was proved for every raw type.

18. **Proof-polynomial conversion.** The supplied typing gives membership of the first evaluation. Eight-generator evaluation soundness gives raw conversion to the second evaluation, and saturation transfers membership at the unchanged formed target. The conclusion's original scope premise is retained.

All cases are covered. The additional bridge has already been handled inside conversion soundness and creates no extra typing case. $`\square`$

The relational consequence uses the newly defined context relation: apply the theorem to both admitted environments, use (10.1) to identify their type sets, and use polynomial evaluation's compatibility with pointwise raw conversion. This gives $`R_C`$-related evaluations. It does not claim arbitrary heterogeneous links between different type valuations, or preserve every equality of the old F/G model.


### 10.7 Full-rule separation and the exact closed criterion

Theorem 16 immediately reflects raw endpoint conversion from **any** identity derivation at an admitted environment:

```math
\Gamma\vdash_+r:\mathrm{Id}_C(p,q),\quad
V_\Gamma(\rho,\eta)
\quad\Longrightarrow\quad
\mathrm{eval}(p,\eta)\simeq\mathrm{eval}(q,\eta).
\tag{10.13}
```

For an empty term telescope, $`\eta=\zeta`$ is admitted. There is also an actual saturated type valuation, for example the constant empty-set valuation. Thus no hidden assumption of an inhabited arbitrary context is needed for closed reflection.

Apply (10.13) to $`B_{\mathrm{id}}`$. Its endpoint atoms evaluate to $`I`$ and $`SKK`$, whose raw conversion is impossible. Therefore

```math
\neg\exists r\;[]\vdash_+r:B_{\mathrm{id}},
\qquad
\neg\exists r\;[]\vdash_0r:B_{\mathrm{id}}.
```

The second statement follows from the exact inclusion. The argument places no restriction on the chosen proof polynomial, its final rule or its use of $`J`$, finite import and other eliminations. Together with section 10.5's original F/G witness, this disproves the particular completeness implication from a formed closed type with a fully semantically valid closed polynomial to existence of some bridge-only syntactic inhabitant. It also disproves the stronger implication requiring that same polynomial as proof. Soundness of the original semantics is fully compatible with this failure of its converse.

The inherited positive open-$`J`$ example remains intact. Its context includes an assumed identity between its endpoint variables. The old F/G context relation can admit a valuation assigning them $`I`$ and $`SKK`$. The new identity membership condition would require raw conversion of those values, so that particular valuation is not admitted by the new context. Theorem 16 still validates the open derivation at every environment the new context does admit. The old example supplies no closed inhabitant of its assumed identity. This is a difference between two sound interpretations' context domains, not a contradictory treatment of the same admitted input.

**Theorem 17 — closed typed-identity criterion.** Retain exactly these five hypotheses in the bridge-only system:

```math
[]\vdash_+ C\ \mathrm{type},\qquad
[]\vdash_+p:C,\qquad
[]\vdash_+q:C,\qquad
\mathrm{Scoped}(0,p),\qquad
\mathrm{Scoped}(0,q).
```

Then the following are equivalent:

```math
\exists r\;[]\vdash_+r:\mathrm{Id}_C(p,q),
```

```math
[]\vdash_+\mathrm{atom}(I):\mathrm{Id}_C(p,q),
```

```math
\mathrm{eval}(p,\zeta)\simeq\mathrm{eval}(q,\zeta).
```

The carrier may have free type parameters. [Written criterion][intensional-source] [Exact formal theorem statements][intensional-theorems]

**Proof.** From any inhabitant, Theorem 16 at the admitted empty-context environment gives the third statement. Conversely, the two scope-zero premises and Theorem 15 turn the third statement into the actual bridge conversion certificate $`p\simeq_+q`$. The supplied carrier formation and endpoint typings form their identity type; the actual identity-introduction constructor gives the second statement with witness $`\mathrm{atom}(I)`$. That specific witness implies existence. $`\square`$

This is a criterion with supplied typings and the specified raw-conversion proposition. It does not decide that proposition, arbitrary typing or general inhabitation. The converse proof uses the bridge, and is not asserted for unchanged $`\vdash_0`$, arbitrary open endpoints or a richer identity theory. Nor does the fixed witness bound the derivations that might type it: proof normalization and the size of type justification remain separate, as in section 4.1.

The criterion concerns endpoint conversion. The extensional proof-canonicalization result of section 4.1 concerns conversion of a **supplied identity proof** to $`I`$ at its existing type. They are different statements. Conflating them would incorrectly import (10.13) into the extensional calculus.

### 10.8 The same identity is positive in the extensional calculus

The current twenty-rule system has an explicit proof of the **same** type $`B_{\mathrm{id}}`$, with the same carrier and endpoint atoms:

```math
[]\vdash_E\mathrm{atom}(I):B_{\mathrm{id}}.
\tag{10.14}
```

Here is the finite construction. At a free type parameter $`\alpha`$, the original finite imports supply both $`I`$ and $`SKK`$ at $`\alpha\to\alpha`$, in the empty telescope and in the formed telescope $`x:\alpha`$. These are actual original derivations, not an assumed weakening theorem for arbitrary extensional proofs. Application gives both scalar endpoints at $`\alpha`$.

Expose the closed atom $`SKK`$ by two bridge instances. Applying it to the still-open variable $`x`$, the polynomial $`S`$ and $`K`$ contractions give

```math
\mathrm{atom}(I)x\simeq_+x,
\qquad
\mathrm{atom}(SKK)x
\simeq_+Kx(Kx)
\simeq_+x.
```

No closed-packing converse is applied to the open variable. Identity introduction therefore proves the scalar identity with proof atom $`I`$. Product introduction abstracts this proof to the literal polynomial $`KI`$, because the actual compiler's absent-variable branch has priority. The resulting typed section is

```math
[]\vdash_E KI:
\Pi x:\alpha.\mathrm{Id}_\alpha
\bigl(\mathrm{atom}(I)x,\mathrm{atom}(SKK)x\bigr).
```

One product-extensionality instance, with the endpoint typings and all formed/scoped family premises, gives

```math
[]\vdash_E I:
\mathrm{Id}_{\alpha\to\alpha}
\bigl(\mathrm{atom}(I),\mathrm{atom}(SKK)\bigr).
```

The two original finite polymorphic typings supply the outer endpoint premises at $`A_{\mathrm{id}}`$. The body proof is over the fresh type parameter, and the type-weakened empty telescope is still empty. One universal-extensionality instance gives (10.14). All endpoint and proof polynomials are scope-zero, and the arrow body has the required type scope. This is exactly one product and one universal extensionality application. [Literal finite witness with every guard][extensional-identity-witness]

Raw conversion has not changed. The raw-indexed identity
$`\mathrm{Id}_{\mathrm{Raw}}(\mathrm{atom}(I),\mathrm{atom}(SKK))`$
is formed in $`E`$ but has no inhabitant: Theorem 5's faithful Raw interpretation would turn any such closed derivation into raw conversion between the two distinct normal forms. Proof erasure sends the proof of (10.14) to Raw; it does not move its endpoints to a new identity carrier. Thus (10.14) is increased typed identity power, not a new raw equation. [Exact distinction and retained older negatives][extensional-identity-consequences]

This also exhibits the failure of the saturated-set interpretation to validate the added extensionality rules. Its product membership admits the endpoint functions and the pointwise identity section: at each argument their applications convert. Its product **relation**, however, additionally requires raw conversion of the function sources themselves. That requirement rejects $`I`$ and $`SKK`$. The eighteen-rule soundness theorem therefore has no unnoticed two-case extension to $`E`$.

Section 6's identity between $`I`$ and $`SKK`$ at the Church carrier $`N`$ is another positive extensional result. The carrier there is different from $`A_{\mathrm{id}}`$. Construction (10.14) removes any need to explain the older separation merely by changing carriers: at the very same $`A_{\mathrm{id}}`$ and endpoints, the bridge-only and extensional proof systems give different inhabitation answers.

<a id="third-cohort-b-extensional-soundness"></a>

The direct repaired-soundness provider explains why the added rules are sound in the original paired full-PER F/G interpretation, without extending the separating saturated-set interpretation just discussed. For Pi extensionality, take related arguments x and y. The supplied pointwise identity section gives p(x) related to q(x) in the fiber at x. The endpoint typing of q gives q(x) related to q(y) for the related argument pair. The fiber PER's transitivity composes them. This is the full cross-argument obligation; equality tested only at identical arguments would not establish it without q's membership and the formed fiber laws. [T750B655]

For All extensionality, the two endpoint typings supply their separate uniformity clauses. The identity section in the type-weakened telescope supplies equality at each unary PER, since extending the type environment preserves the required context relation. These three components build the All relation. The final identity witness is I, with both endpoint relations and reflexive proof conversion. Identity introduction under the bridge likewise uses the imported conversion soundness theorem and the unchanged raw saturation law rather than adding a semantic equality oracle. Mutual induction then derives context, formation and term soundness for every constructor of the repaired syntax.

The accompanying audit checks the distinct signatures: original Has and bridge-only HasPlus each have eighteen typing constructors, while the repaired HasE has twenty. Its declaration and axiom checks are source programs, not newly observed successful runs. The `MissingAllScope` probe deliberately supplies the All rule without its scope obligations and is an expected interface rejection, not a noninhabitation theorem. This exact soundness source describes an isolated, unadopted candidate. Its positive mathematical claims therefore supply no additional canonical-adoption receipt merely because the chapter uses the extensional judgment as a comparison language. [T750B589] [T750B603] [T750B655]

[T750B589]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9ce227a5337b05e70ce8da58ad0f0a290f07c72beae27f8386e45cd0e755ae25/MissingAllScope.lean
[T750B603]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a2b12f0df76d8ca0973ea4d6c34cc6892324e0a0fdb89f414c6628e40974651a/ExtensionalRepairAudit.lean
[T750B655]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b0d879f3ac11bc29f56887c0f56cc7e59e677150357da7304b783b3aefb0cda5/ExtensionalRepairSoundness.lean

### 10.9 What a proof translation must preserve

**Proposition 18 — strict inclusions and distinct transfer obstructions.** As relations on literal context–polynomial–type triples,

```math
\{\Gamma\vdash_0p:C\}
\subsetneq
\{\Gamma\vdash_+p:C\}
\subsetneq
\{\Gamma\vdash_Ep:C\}.
```

The first strictness concerns a supplied representation. The second also separates existence of **any** proof at one fixed closed identity type.

**Proof.** The inclusions were established in section 10.1. For the first, $`\mathrm{atom}(t)`$ is typed at $`A_{\mathrm{id}}`$ in the bridge-only system by packing, while Theorem 14 excludes the same original judgment. For the second, (10.14) inhabits $`B_{\mathrm{id}}`$ in $`E`$, while Theorem 17 and raw $`I/SKK`$ separation exclude every bridge-only proof there. $`\square`$

This proposition composes inherited results; it is not a new discovery of either counterexample. Its usefulness is to distinguish two exact translation contracts.

| Proposed transfer | What the displayed witness establishes |
|---|---|
| Every bridge-only derivation becomes an original derivation preserving the same context, proof polynomial and type | Impossible: the opaque $`\mathrm{atom}(t):A_{\mathrm{id}}`$ judgment is a counterexample. |
| A bridge-only result may choose a different original polynomial with the same evaluated raw program | The opaque witness alone does not exclude this: its exposed $`w_t`$ is exactly such a representation. No general translation is constructed here. |
| Every closed $`E`$ identity proof becomes some bridge-only proof at the same context, carrier, endpoint polynomials and identity type | Impossible, even when the output proof polynomial may change arbitrarily: $`B_{\mathrm{id}}`$ has no bridge-only inhabitant. |
| The same identity-preserving transfer from $`E`$ to the original calculus | Impossible for the same $`B_{\mathrm{id}}`$, by original-to-bridge inclusion. |
| A translation changes the type representation, identity endpoints, source rules or semantics | Outside these preservation contracts; no blanket impossibility is inferred. |

The two negative identity-transfer statements require no assumption that a translation is computable. A total translation satisfying the stated preservation conditions would have to output an inhabitant of an empty source-judgment fiber. Allowing a different proof polynomial cannot do that. Conversely, changing the meaning or representation of the target identity is a different obligation and is not ruled out by this argument.

These boundaries explain why a shared semantic interpretation does not itself supply a certificate translation. Old F/G validity passes across literal evaluation equality, yet original typing of the supplied opaque atom fails. Adding the bridge repairs that representation transfer at supplied closed typings, while old F/G validity still does not yield any bridge-only proof of $`B_{\mathrm{id}}`$. Adding typed extensionality supplies that particular identity but does not yield unrestricted semantic completeness: the exact compiler identity of sections 8–9 remains independent in $`E`$. Each statement uses its own unchanged source judgment and its own explicit input conditions.

The scientific contribution of this section is the reconciled account: whole-label preservation and its exact fixity condition, closed bridge transport, the failure of the isolated identity-predicate shortcut, the full eighteen-rule model with both $`J`$ coordinates, and the resulting asymmetric translation consequences. The opaque and bridge results remain inherited from their original proofs; the old residual stop is resolved by the later intensional proof; the positive extensional witness is independently owned prior work. The comparison and organization are composed exposition. No new formal execution, completeness theorem, calculus adoption or historical-priority claim follows.



### 10.10 A normalization theorem for a different calculus

A theorem about weak and strong normalization cannot be transferred merely because both source systems have typing, conversion and an operation called erasure. The family-245 assessment concerns the exact pure-type-system calculus in OpenAI's pinned normalization study. Its system-wide hypothesis ranges over every legal annotated expression and type in every valid context. Checking one closed polynomial or its proof component is a different premise. [R250-093]

There are two structural mismatches. Pure-type-system conversion changes the assigned type while retaining the subject expression and its typed generation witnesses. The assessed `HasE.conv` rule instead changes the term polynomial at the same type through symmetric conversion plus a scope condition; reverse conversion can introduce a discarded subterm without a typing derivation for that subterm. Moreover, the upstream mode-label erasure retains applications, annotations and binders, whereas the actual `J` polynomial discards endpoint and proof coordinates. Equality of terminology supplies neither a typed translation nor an operational simulation.

Three controls identify what a proposed bridge would have to repair. First, the inherited Raw interface permits a non-weakly-normalizing $`\Omega`$. A faithful positive-step simulation into a globally weakly normalizing pure type system conflicts with the inherited nonnormalization and reflection facts; making the raw term an inert quotation changes that operational claim. Second, a reflexive identity can have the normal proof polynomial $`I`$ while its endpoint annotation contains $`\Omega`$. The proof polynomial alone therefore does not satisfy the upstream premise about legal annotated types. Third, reverse conversion at an ordinary closed reflexive identity carrier admits $`KI\Omega`$. It reduces to $`I`$, but reduction may continue forever in its discarded argument. That particular derivation uses neither Raw typing nor the `J` or extensionality rules. Restricting only the final carrier or requiring closedness does not establish strong normalization. These are the assessment's written rule instantiations using inherited lemmas, not new kernel executions here. They agree with the distinction between normalizing representatives and stronger properties of a supplied representation developed above.

The genuinely finite `FiniteDerives` fragment excludes backward conversion and already has its inherited `P01Candidates.finite_SN` theorem. Reproving that fragment through a pure type system would still require elaboration, system-wide weak normalization and nonempty-step simulation; it supplies no missing bridge for the unrestricted target. Likewise, normalizing the fixed witness $`c_3`$ cannot construct or normalize the complete derivation at its exact identity type. A target-specific derivation-normalization argument must preserve contexts, carriers and endpoints, cover every unchanged constructor and establish the needed canonical-form result. The family-245 theorem alone supplies none of these premises. The assessment records its literal scalar-fusion target as open. That historical source status is not a current claim overriding or reopening the exact-calculus independence and certificate results in §§8–9 and §11.

The negative transfer decision was based on a complete 72-page paper reading and bounded inspection of critical interfaces and proof stages. The recorded audit checked 33 upstream module identities (29,547 source lines), 30 target-root identities, 82 frozen scalar predecessors and four scalar sources. Identity checks are not a claim that every tactic or transitive Mathlib proof was independently read. Neither upstream nor target Lean was executed for that assessment. The upstream Lean 4.34.1/Mathlib pin and local Lean 4.19.0 pin remain distinct; importing a theorem or upgrading the toolchain is not justified by this inapplicability finding. [R250-093]

### 10.11 Typed telescopes, recursive universal types and exact source preservation

The representation boundaries above do not prevent a positive typed construction. A separate syntax-generated telescope nucleus makes arbitrary typed dependent products, sums and identities coherent under their stated formation rules; a recursive `All` extension joins this dependence to universal type binding. Their bounded historical source reviews accept the stated constructions and translations. This is stronger than an unreviewed design proposal, but it does not add rules silently to the original judgment or its extensional successor. The earlier design gate and still-in-progress control plan retain their historical status rather than overriding the later exact-source review. Positive substitution and contextual-J results continue to retain the raw I/SKK obstruction and imply neither normalization nor equality reflection through arbitrary heterogeneous links. [T11R81] [T11R76] [N250B-206] [N250B-207] [N250B-208] [N250B-209] [N250B-210] [N250B-224] [N250B-225]

[N250B-206]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/a16f18b461923a2cd4d3d150e583ebb59985c28971cf605a8e359f76a79dac08/README.md
[N250B-207]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/90b2a657a301e94869c39658ff0a3bde4659c87cf8d8031f4d7bfc647cebe6a7/PUBLIC_REVIEW_v2.md
[N250B-208]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/f4eb382dc54e142b14d943affe8602b8dbb2f3097eaea8f6e630f6d182e83545/DEPENDENT_ALL_DESIGN_v5.md
[N250B-209]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/73e85fd8b4750db3999d63b15de4780f589b546a44f8d3e45a246bbc0d16e5f6/CONTROL_PLAN.md
[N250B-210]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/963ff1bc8b09a31637ed9b616410807bd97d1565a6da6d5944573fd4e0bbba21/REVIEW.md
[N250B-224]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/14c1276fc9443f79c4dfcd12e802110f40f3c435482e82ae02068c887fa70d42/README.md
[N250B-225]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/6e1832ad33853ba245c46ef65e7eb560bfb79f76ea5c566b5488a1b223a856c5/REVIEW.md



#### 10.11.1 Derive semantic laws from formation rather than assume them

For a telescope Γ, D expresses admissible valuations, E relates two valuations in one parameter environment, and H relates valuations across the two endpoints of a relation environment. The unary type predicate F and heterogeneous predicate G are defined before their laws. A formed type receives a partial-equivalence-relation interpretation only after the induction establishing its laws. The distinction matters because arbitrary raw type syntax need not have lawful transport. [T11R118] [T11R81]

The relation-law package contains symmetry, transitivity and stability under raw conversion. Endpoint self-relatedness follows from symmetry and transitivity, rather than being an extra universal reflexivity claim about all raw terms. The context package proves admissible endpoints, symmetry and transitivity for E, endpoint conditions for H, two-sided respect of H under E, and the strong diagonal equation H(diagρ,η,ξ) iff E(ρ,η,ξ). The type package likewise proves F is a PER on admissible valuations, transport of F along E, separate left/right endpoint conditions for G, respect under the two endpoint PERs, two-sided valuation invariance, and the diagonal identification of G with F for **E-related**, possibly unequal, valuations. These records are induction conclusions; they are not covert formation premises. [T11R118]

Context extension illustrates why the conditions are not redundant. When the new head is related at the left valuation, its right endpoint must be transported to the right valuation before that extended valuation is declared admissible. Symmetry and transitivity similarly transport the head relation; heterogeneous respect uses both endpoint relations and then valuation invariance. For a typed identity A(p,q), transport also uses the fundamental properties of **both** endpoint polynomials p and q. Raw conversion alone does not supply these typed endpoint premises. A fundamental typing is a heterogeneous preservation statement for every admissible relation environment; its unary consequence follows by the context and type diagonal laws. [T11R118]

The constants and finite-leaf bridge keep this construction anchored to the accepted finite interpretation. For a nondependent arrow, F is the usual related-argument preservation condition. Its heterogeneous G requires each endpoint function separately to preserve its own domain relation, as well as the cross-endpoint mapping of the supplied Link. The I, K and S fundamental cases follow from their corresponding link lemmas under the relevant context/type laws. Translating a finite type code preserves its exact unary and heterogeneous interpretation; an existing `FiniteDerives t C` yields the fundamental interpretation of the unchanged atom t. This is not reconstruction of t or replacement of its literal source polynomial by an extensionally convenient term. [T11R137]

The public packaging makes the resulting objects explicit. `formedObject` has relation exactly F; `formedLink` has relation exactly G between the separately constructed endpoint objects. A dependent fibre is the formed body PER at an admissible argument, and Bottom outside that argument domain. Related arguments yield equal fibre PERs by formation-law transport. Consequently formed Pi and Sigma agree with the corresponding dependent PER constructions, and formed typed identity agrees with `IdPER` at the evaluated endpoints. These are equality statements at the selected interpretation, not canonical carrier equality independent of it. Raw still types Ω, and the retained theorem that Ω has no normal reduct remains. The typed construction therefore does not establish normalization of every term it types. [T11R76]

#### 10.11.2 Both coordinates of contextual J remain present

The contextual identity eliminator has a motive depending on an endpoint **and a proof coordinate**. The representation constructs a motive object over the accepted intrinsic identity context, proves its coherence from E-transport, and represents the submitted identity proof and base case with their exact polynomials. It then invokes the actual accepted contextual J operation. The output code is literally `jPoly d y e`; pulling the motive along the point substitution agrees with the represented target type `motiveAt B y e`, provided the displayed formation and typing hypotheses are supplied. One may not replace that target by a motive depending only on y or replace the proof e by literal I without the relevant equations. [T11R90]

A concrete positive witness uses context [Idα(x,y),α,α], with de Bruijn positions proof0, endpoint1 and original endpoint2. Its motive is a dependent sum whose first component is an α-identity from the original endpoint to the new endpoint, and whose second component states Raw identity of the proof coordinate with I. The base is the pair (I,I). Simultaneous substitution gives the exact base and target types, including the shift beneath the Sigma binder; the literal J term is typed at that target and satisfies its fundamental relation. [T11R151]

The witness is not confined to a Raw-refining carrier or a literal reflexivity token. Choose the parameter PER interpreting polymorphic identity, which relates I and SKK although they are not source-convertible. Evaluate the context at original endpoint I, new endpoint SKK and proof I I. The proof is convertible to I but is not literally I. The same J derivation remains valid, exercising both the changed endpoint and nonliteral proof coordinate. This establishes the intended typed coherence, not raw conversion of I and SKK. [T11R151]

Related controls explain the limits. Total links from a total PER to Raw and back can relate nonconvertible endpoints without reflecting equality on either side. A one-sided identity predicate can admit a witness outside its purported right identity PER. An unformed Raw-indexed family can contain I over one related index while failing over the other. Inspecting proof syntax is not invariant under conversion. Finally, reverse raw conversion can introduce a discarded out-of-scope argument: closed I is convertible to K I var0, whose polynomial is not scoped at depth0. These are source-level separating theorems and countermodels; neither a name such as “Link” nor raw convertibility alone grants the absent transport or scope law. No fresh execution of their axiom-print requests is reported here. [T11R21]

IndependentControls checks the corresponding boundaries in FullPER itself. Universal types range over every saturated PER, including the empty PER; Raw remains conversion, and sums use actual projections. The original I and redundant compiler endpoints are typed-related at EndN while remaining Raw-separated. Paired admissible environments exclude both a single EndN variable and the older endpoint coordinate of theta from Raw. The newest identity-proof coordinate, by contrast, legitimately erases to Raw and supports the specified proof-sensitive motive; those two coordinates must not be confused. A further assumed typed identity does not entail Raw reflection. These controls use the imported FullPER fundamental theorem and explicit environment ordering, rather than automatically inheriting another model's proof or licensing arbitrary unformed motives. [A750-T50-116](../research/t20-v6-20261012/sources/c47711ac052a8aaf0b6f9e9455b158d3a6edc01af1fd46e4eb9b4f8db2d6e0aa/IndependentControls.lean#L16-L45) [A750-T50-116](../research/t20-v6-20261012/sources/c47711ac052a8aaf0b6f9e9455b158d3a6edc01af1fd46e4eb9b4f8db2d6e0aa/IndependentControls.lean#L48-L95) [A750-T50-116](../research/t20-v6-20261012/sources/c47711ac052a8aaf0b6f9e9455b158d3a6edc01af1fd46e4eb9b4f8db2d6e0aa/IndependentControls.lean#L97-L160)

#### 10.11.3 Recursive All requires two distinct binder lifts

The extension's types contain parameters, Bottom, Raw, arbitrary typed Pi and Sigma, typed Id, and recursively generated All. There is no object-language universe or Type:Type. All binds a **type parameter**: it shifts free type parameters in the surrounding telescope while leaving term indices alone. Pi and Sigma bind a **term variable**: substitution must lift term indices in the body and in every replacement type. Literal renaming, composition, top cancellation and mixed-substitution equations keep these lifts separate, including both coordinates of the J motive. Confusing the two lifts would change open dependent replacements even if some closed examples survived. [T11R81]

The guide's construction defines raw unary and heterogeneous predicates together by structural recursion. At All, unary uniformity invokes the heterogeneous predicate of the strictly smaller body. It does not first assume the desired PER or soundness theorem. Finite telescope valuations are total evaluator environments with an unused zero tail; type weakening leaves term coordinates intact. Raw term-substitution and type-renaming equations precede formation-law proofs. [T11R81]

Semantic replacement is conditional on an exact image match relative to a lawful source relation environment: separate unary endpoints, the heterogeneous relation and both diagonal image equations are required. This is a metatheorem hypothesis, not a new typing premise. In the structural induction on the target type, the source environment stays frozen when the target valuation gains a term prefix; syntactic weakening of replacement images cancels that prefix semantically. Under All, it extends by the newly selected PERs and Link. Instantiation obtains the image hypotheses from **smaller replacement-formation conclusions**, evaluating image PERs separately at the two target valuations and taking their actual heterogeneous predicate as the Link. No formation theorem for the substituted result is used to justify the substitution theorem itself. [T11R81]

The formation and typing induction then carries the smaller body results as hereditary conclusions. All introduction derives uniformity at arbitrary Links, including diagonal endpoint environments. All elimination and finite imports use the smaller replacement laws. The strong diagonal argument permits unequal E-related valuations; its reverse direction changes the right valuation by invariance, transports the within-endpoint relation, and applies respect to the right result. It does not identify the two valuations. Intrinsic mixed representation subsequently proves equality of image parameter environments along unary E while retaining the genuine heterogeneous relation for independently evaluated endpoints. Unary context equality is not substituted for cross-endpoint relation preservation. [T11R81]

These construction details are stated in the inherited proof guide, whose exact dependency and review digests are preserved in its source. The guide reports a frozen47-module nucleus and an automated independent contract review, not human-specialist validation. This integration does not rerun or independently recheck every imported module. The positive direct witnesses below retain their own inspected declarations and explicit dependencies. [T11R81]

The mixed-algebra source makes capture precautions into equations. Write `mixed σ τ A` for simultaneous term/type substitution and `psub` for substitution in a term. Its composition law is

```text
mixed σ₂ τ₂ (mixed σ₁ τ₁ A)
 = mixed (n ↦ psub σ₂ (σ₁ n)) (n ↦ mixed σ₂ τ₂ (τ₁ n)) A.
```

Input term substitution changes only the polynomial replacement family: `mixed σ τ (subst δ A) = mixed (n ↦ psub σ (δ n)) τ A`. Output substitution acts on both images: `subst δ (mixed σ τ A) = mixed (n ↦ psub δ (σ n)) (n ↦ subst δ (τ n)) A`. The two-coordinate J motive requires two lifts:

```text
mixed σ τ (motiveAt B y e)
 = motiveAt (mixed (pup (pup σ)) (n ↦ wk (wk (τ n))) B)
            (psub σ y) (psub σ e).
```

A replacement with a free term and a free type parameter shifts both when it crosses the respective binders. Literal positive capture examples and rejected unshifted equations separate these operations. If `TyScoped n A`, `ScopedSub n m σ`, and every `τ k` is `TyScoped m`, then `mixed σ τ A` is `TyScoped m`. These are exact substitution and scope results, not merely naming conventions. [F250-165]

For semantic transport put `EvalImages σ η(n) = eval (σ n) η`. Under `ImageMatch τ r η ξ s`, the three equations are

```text
F (mixed σ τ A) r.left η t u = F A s.left (EvalImages σ η) t u
F (mixed σ τ A) r.right ξ t u = F A s.right (EvalImages σ ξ) t u
G (mixed σ τ A) r η ξ t u = G A s (EvalImages σ η) (EvalImages σ ξ) t u.
```

`ImageMatch` supplies left, right, cross and both diagonal image conditions at frozen base valuations. The source environment `s` stays frozen through term binders while replacement images weaken; the All case needs the two diagonal clauses as well as the cross clause. These hypotheses belong to the substitution metatheorem, not to new formation rules and not to a licence to treat arbitrary raw target types as lawful. They make precise the semantic transport used in §10.11.3. [F250-173]

#### 10.11.4 Open replacements and a joined dependent universal witness

The finite syntactic substitution interface uses an explicit list of term components. Each telescope declaration is instantiated using its previously supplied tail components; replacement types may depend on **all variables of the full target context**. Unused term-image entries are atom-zero, whereas unused type-image entries are Bottom. An identity list agrees with the total variable map only on the finite scope in question. Its action is proved by scoped extensionality; it is not globally equal to the total identity function. [T11R81] [T11R139]

An explicit replacement is Id Raw(var0,var0) in target context [Raw]. It is formed and genuinely open: it is not scoped at depth0. Mapping the sole source parameter to this type and its sole term component to I gives a mixed context map from the target into the source [Param0], and preserves the source variable's typing as the literal I at that replacement. The All-elimination map also accepts this open replacement. At the unused index1, the one-component identity list returns atom-zero, not var1, giving a direct refutation of the alleged global identity-tail equation. No closedness restriction on replacements can be added without excluding this positive example. [T11R139]

The joined example is

Q = All α. Pi x:α. Sigma y:α. Id α x y.

Its witness q is the exact bracket abstraction of the open pair (var0,I). The body is formed and q is typed before All introduction. Instantiating Q with **Q itself** yields exactly Pi Q (Sigma Q (Id Q var1 var0)); All elimination supplies that typing and its fundamental interpretation. This self-instantiation is in the declared recursive grammar, not an assertion of Type:Type or a change to the canonical source conversion. [T11R16]

Polymorphic I can similarly be instantiated at any formed replacement A, yielding the arrow A→A. The controls instantiate it at an open identity over [α,α], at an inhabited dependent Sigma over [α], and at the Raw-specialized Sigma family. The open pair relates (I,I) to (SKK,I) across the corresponding unequal related valuations while retaining ¬Conv(I,SKK). With Raw indices, both fibres at I and SKK are inhabited by their own pairs, but the I-pair does not inhabit the SKK fibre: nonemptiness does not collapse the dependent family into a constant relation. [T11R16] [T11R151]

Capture protection is visible in the exact nested equation. Substituting the open Sigma replacement through All followed by Pi Raw shifts the outer term occurrence to var2, while the inner identity's bound endpoint remains var0 and its type parameter becomes Param1. Both binder effects are necessary. This is a literal syntax equation, accompanied by independently meaningful inhabitation and relation controls, rather than an appeal to a vague claim that substitution is “capture avoiding.” [T11R16]

#### 10.11.5 Translate retained legacy derivations without changing their code

The recursive extension also has a constructor-faithful translation of the entire old type grammar. Parameters, Bottom and Raw remain themselves; old untyped identity becomes typed identity at Raw; arrows become nondependent typed Pi; old Pi and Sigma bind Raw; All is recursively translated wherever it occurs. Term-index substitution, instantiation, motive substitution, type renaming, both lifts and type substitution commute with this translation by structural induction. Finite-code embedding translates to its exact finite interpretation. This is a grammar translation, not literal equality of old and new type syntax. [T11R49]

A `RawContext` provides an actual finite syntactic typing of every in-range variable at Raw. Such contexts extend by Raw and survive type weakening. Any scoped polynomial is typed at Raw by induction on variables, atoms and applications. The identity context Theta requires care: its newest declaration is Id, not Raw, so the explicit proof-erasure rule is needed to obtain Raw access there. A supported legacy motive is first formed in an all-Raw context and then transported unchanged into Theta. [T11R49]

Two transport interfaces must remain distinct. A total identity-polynomial substitution is used only as a syntax-scoped interface. The finite component substitution instead has atom-zero term padding and Bottom type padding. Its action on a formed, scoped type is the identity by the finite-identity theorem; no invalid global equality between its padded function and Poly.var is used. This supplies formation transport into any suitable RawContext, including the two-coordinate J context. [T11R49]

The derivation translation consumes the accepted **Type-valued retained tree before its erasure** to the old Prop judgment. Its support predicate checks every displayed term and type at the actual term-binder depth, including both identity endpoints, implicit All replacement types, Pi/Sigma bodies and arguments, the two-extra-coordinate J motive and displayed conversion endpoints. All binding does not add a term coordinate. Internal hidden histories of a PolyConv certificate are not traversed. Thus support of a retained derivation is stronger than scope of its final term, but is not a claim to inspect every internal conversion witness. [T11R66]

Induction on this retained tree translates every old rule, including All introduction/elimination and genuinely nonfinite dependent All, with **exactly the old polynomial**. There is no Prop-to-Type reification and no reconstruction of imported finite atoms. The applications, dependent introductions/eliminations and J cases use the appropriate commuting equations and separately supplied formation/scoping premises; conversion retains the actual displayed conversion and target scope. Erasing the retained tree still recovers its original old judgment. Concrete witnesses include polymorphic identity, an open identity replacement involving var0, the nonfinite dependent-All tree with literal abstract K, and its self-instantiation. These examples broaden the explicit grammar comparison beyond the finite nucleus without changing that nucleus's prior restriction. [T11R66]

The older finite-image comparison has a stricter domain than this recursive-All result. Its Type-valued derivation predicate excludes All introduction and elimination even if the final displayed type happens to be finite; its accepted old All types must be whole finite-code images. Decoding supplies a unique translation on that domain. The later recursive comparison preserves the unary and heterogeneous interpretations and represented objects on its broader supported grammar. An invalid generalization from an unshifted parameter assumption remains excluded: the premise at Param0 cannot simply become All Param0. These restrictions concern particular derivation interfaces, not the loss of the earned recursive translation. [S250-L255] [S250-L256] [S250-L292]

For the separate legacy admissibility interface, a finite prefix of a type substitution suffices up to the type's **maximum free parameter index plus one**, with the appropriate decrement beneath All, not merely the number of parameter occurrences. Substitution agreement then proves finite-prefix completeness and arbitrary type substitution; term substitution, type substitution and their mixed compositions keep their stated order. Nested replacement controls preserve the endpoint and proof coordinates of J and both kinds of binder lifting. The later intrinsic representation uses finite term lists with zero padding and formed pullbacks; it preserves the exact substituted polynomial rather than choosing a semantically equivalent replacement. [S250-L408] [S250-L357] [S250-L427]

[S250-L255]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/47675347844cf2858eb2e5a0aea9bbca08cdf90e4de0aee7f26cb8e2a73f9d45/TypedLegacy.lean
[S250-L256]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/47ed250bec3cc080c689adeade033b52acd88d733ed897065bb1a7605f310585/AllLegacyComparison.lean
[S250-L292]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4f1fce0d4f76ff89feb6e35bdef8d1a70d1a588238b18718c048786d48dafcd4/IndependentAllRuleControls.lean
[S250-L408]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6ae02ec07b67a81f3019192118e44d4ac37cd26f9ad61f09831c8fafd55ce121/SubstitutionAdmissibility.lean
[S250-L357]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5ef51c33cee2464f514881e06bd9b647db355cb4297bbdd6276284dd5a720b2f/IndependentControls.lean
[S250-L427]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/736b408e67348b264191a85f0e9591bf8c209ed4dd557bed83e4e1fe83163722/AllRepresentation.lean

#### Exact formation and substitution witnesses

The direct finite-telescope sources support the construction above at distinct levels. `TypedSyntax` requires formation, scope and endpoint typing in the syntax itself; `TypedSoundness` derives context and hereditary type laws by mutual induction. `TypedPiLaws` obtains its dependent-function PER, transport, respect, endpoint and diagonal laws from the context, domain and extended-context codomain laws. The recursive-All structural source derives formation of the result and context, scope, and preservation under type-parameter renaming. Its finite comparison identifies both unary F and heterogeneous G on embedded finite codes with the retained finite interpretation. These are positive structural and semantic preservation results, with their context premises intact. [T750-C675] [T750-C689] [T750-C711] [T750-C700] [T750-C710]

`IndependentNucleusContracts` proves an empty-context variable untypable at any result type, rejects the malformed Raw identity over an arbitrary parameter, and exercises the strong diagonal theorem at related but unequal valuations. Its positive pair witness also has distinct endpoint objects as well as distinct valuations, so it is genuinely heterogeneous. The same source retains zero padding of the empty substitution and literal typed substitution. `SubstitutionControls` supplies concrete open two-sort, dependent-J and Sigma certificates, preserves opaque finite terms as atoms, and binds an admitted candidate to the actually substituted source. Its counterequations distinguish an unlifted substitution from capture avoidance, sequential replacement from simultaneous replacement, and the required two J lifts from one. The positive substituted certificates therefore retain both endpoint and proof coordinates; their nontrivial cases cannot be reduced to closed examples or merely equal denotations. [T750-C690] [T750-C724]

[T750-C675]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b65b90129c3d5e198f9e9266efb8295cea016b41be541b0dbef7683a6438357c/TypedSyntax.lean
[T750-C689]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ba9667b33cb3b6268b3450dbd5a803bb880948d12e2b74f1b3739165ee109143/TypedSoundness.lean
[T750-C690]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bb2030369ada2d2bf6e355e8f92931989eb4359862169ec41912e610b1b7a2a0/IndependentNucleusContracts.lean
[T750-C700]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/be56bb140b8d9c9ce720eb7f142567b2d4f0f9af56684a79544b8b83959b571d/AllStructuralBase.lean
[T750-C710]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bf768fbeeff2ff79aba29a1ce1579dbc877239561a8345873b60f2891906ef1a/AllFiniteComparison.lean
[T750-C711]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bf99ba54a2ee69f0856dc50c7a4c0dc90e3789d590058dcae53909fe39e5e489/TypedPiLaws.lean
[T750-C724]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c3d31d2c24e9db193bbe60801bffdbc54e1a61ddb13a21ca19672259c57e7dec/SubstitutionControls.lean


<a id="final189-b03-malformed-and-varying-images"></a>

A concrete malformed replacement shows why the diagonal-image condition cannot be omitted. Let A=Sigma(Param0, Id_Raw(var0,I)) and interpret Param0 by the total PER. The raw unary formula F(A) relates (I,I) to (SKK,I), but the right pair is not self-related: its dependent Raw identity would force Conv(SKK,I). Consequently G(A) at the diagonal environment does not relate that pair, and the unrestricted equation G(diagρ,η,η)=F(ρ,η) for every raw type is false. An ImageMatch for this malformed image would imply the excluded diagonal relation, so it is impossible. Formation-dependent diagonality is doing mathematical work, not merely documenting a convention. [F189B-823](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/de9ec5d46ba83491c91dfa416c6fe0b896c9d9f8a49605a9ee5fd65dc02376c1/IndependentMalformedReplacement.lean)

The independent positive mixed controls retain the other side of the distinction. Their image parameter environments actually differ between target valuations headed by I and SKK, rather than being merely syntactically open. They import the finite application I I as one opaque atom and preserve that exact atom through an open contextual type substitution. A nonempty heterogeneous replacement relates (SKK,I) and (I,I) across unequal endpoint interpretations, and the resulting All instantiation acts on that genuine Link. These examples support open code-preserving substitution without imposing equality of the two endpoint PERs. [F189B-869](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ed3f7e8fd54071a09a8d166dbf3354278f92050ee219e478ce0f62c52c3b1374/IndependentMixedControls.lean)

<a id="baseline141-extensional-only-dependent-target"></a>

The IndependentDependentTarget control also makes the target calculus substantive. It constructs an extensional-only context [proofId], a genuinely term-dependent identity replacement, and then a two-entry telescope whose newer declaration depends on the older one. Closed type substitution yields the displayed HasE result in that dependent target. Original context formation is excluded, so no original Has derivation at any result type can inhabit the two-entry target. This is stronger than merely showing that a replacement is syntactically open, but remains conditional on the imported structural and substitution theorems; no fresh dependency replay is asserted. [Exact source](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/0a4017c76784ee709bdfcb43ec57b61dc7b210a227ae4619a8573981f9ee403c/IndependentDependentTarget.lean#L12-L73)

#### 10.11.6 The retained boundary and evidence scope

The twelve sources contribute different things: syntax and derivation translations, semantic-law proofs, exact intrinsic packaging/J, positive joined witnesses, separating countermodels, structural controls and an explanatory dependency guide. The substitution-readback file is different again: it requests definitions and checks for index/type composition, their interchange, finite-prefix elimination/completeness, typed and mixed substitution, and open two-sort, J, Sigma and source-changing substitution controls. Its `#print`, `#check` and `#print axioms` commands preserve the intended inspection surface; their presence supplies no new output or replay result. The structural and endpoint files' own audit commands have the same limitation. [T11R44] [T11R139] [T11R21]

The positive results do not establish raw eta, equality reflection through arbitrary Links, normalization, higher identity, arbitrary frontend correctness, canonical unary carrier equality, full U11 closure or numerical identity of actual bearers. Typed Id here is equality in the selected PER, with witnesses convertible to I; it is not a universal equation between source conversion and semantic relatedness. Formation and fundamental premises are doing real work, as the Raw-family and one-sided-endpoint countermodels demonstrate. Preserve those premises while crediting the exact code-preserving translations, genuinely open substitution and joined dependent/impredicative witnesses that have been obtained. [T11R81] [T11R21] [T11R151]

<a id="baseline141-rigidity-relative-sigma-eta"></a>

Even supplying the explicit Rigidity hypothesis does not settle the universal pair identity. For SigmaRaw=Σ Raw.Raw and Eta=Π z:SigmaRaw.Id_SigmaRaw(z,pair(fst z,snd z)), the tagged-PER source validates Rigidity while refuting Eta, excluding every HasE proof of Rigidity→Eta. The original componentwise PER validates both and excludes every HasE proof of Rigidity→(Eta→bottom). Thus the additional result is two-sided nonderivability relative to Rigidity, not merely failure of unrestricted eta or independence of Rigidity itself. Both exclusions retain their imported fundamental-theorem dependencies; no new compilation is asserted. [Exact source](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/08710f5ab91d89ec916330bd68cb7bc3663e0b6902e0db6f26337e6f9e92404f/Boundary.lean#L27-L122)

The companion review records the converse relative boundary: its imported exclusions rule out every closed HasE witness of Eta→Rigidity and Eta→(Rigidity→bottom). This is distinct from the Rigidity-relative exclusions above. The sum controls also exhibit equal raw projections for I and pair(K,K I) while the tagged Sigma relation separates them; canonical pairs satisfy the eta body, and the old componentwise model satisfies that body even at the ghost I. The Pi/All rigidity interpretation is unchanged between these two PER models. These are exact formula checks and applications of imported separation and model results, not new proofs of those imports, unrestricted raw eta, or fresh compiler acceptance. [SUB250-F28-039](../research/t20-v6-20261012/sources/54d7af331e0852a5aae9632666aaab3edecb7cb3036d0ef9f1c9ac9998f3a22e/Independent.lean#L4-L23) [SUB250-F28-102](../research/t20-v6-20261012/sources/60f12a1978a6400267104564d9cbef75f4dcb3ba24730bd1d67abaa758b714de/ReviewControls.lean#L34-L61)

The tagged interpretation supplies its own actual-E soundness construction rather than inheriting the old componentwise F theorem. Its Sigma relation requires the two projection relations and equivalence of the predicates tag(z) and tag(w), where tag(z) means raw conversion to pair(fst z,snd z); it does not require both tags to hold. Conversion invariance of this predicate supports saturation, and dependent environment transport supplies symmetry and transitivity. Structural term and type substitution, fresh finite-grammar soundness, and mutual induction on the actual context, formation and typing recursors then yield the new fundamental and formation-coherence interfaces. In the J case the motive is transported across both the endpoint and the supplied proof coordinate in the actual theta context. These are conclusions of the displayed semantic argument, not new premises inserted into the source grammar. The term carrier, source recursors and raw/compiler transport facts remain supplied imports, with no fresh compilation, unrestricted Sigma eta or enlarged source rule inferred. [A750-F50-001](../research/t20-v6-20261012/sources/adfe1306346b6d5f4267c1acaddcef3c20de13db4753d467542deeac613aae8a/TaggedPER.lean#L20-L54) [A750-F50-001](../research/t20-v6-20261012/sources/adfe1306346b6d5f4267c1acaddcef3c20de13db4753d467542deeac613aae8a/TaggedPER.lean#L75-L158) [A750-F50-001](../research/t20-v6-20261012/sources/adfe1306346b6d5f4267c1acaddcef3c20de13db4753d467542deeac613aae8a/TaggedPER.lean#L243-L294) [A750-F50-001](../research/t20-v6-20261012/sources/adfe1306346b6d5f4267c1acaddcef3c20de13db4753d467542deeac613aae8a/TaggedPER.lean#L382-L402) [A750-F50-001](../research/t20-v6-20261012/sources/adfe1306346b6d5f4267c1acaddcef3c20de13db4753d467542deeac613aae8a/TaggedPER.lean#L516-L664)

The retained tagged interpretation also supports full external dependent induction under semantic premises: ContextLaws for Γ, TypeLaws for P over N :: Γ, and Fundamental evidence for the zero seed and dependent step yield Fundamental Γ (sectionPoly p s) (Pi N P). The proof pairs each index with its fiber witness, iterates the related total-space step from the related seed, and transports the resulting fiber along the projected-index equation before applying the section evaluation equations. It imposes no old FormE premise or separately supplied rigidity witness, and the displayed argument uses neither a Sigma-eta premise nor a Sigma-elimination premise. This semantic closure is not a source HasE derivation, soundness of an entire enlarged grammar or a received transitive dependency audit. [SUB250-C9-003](../research/t20-v6-20261012/sources/4d38059e808101073cbbb407dc4acff7c3da785fd5592ef3d302928ee7397c37/TaggedInduction.lean#L18-L77)

Three substitution interfaces must be distinguished when applying this construction. The original fifteen-constructor `P01DF.Has` judgment admits term substitution by **every total** index map and type substitution by every type map, with no caller-supplied finite support, scopedness or semantic admissibility premise. This is a proof transformer for the unchanged Prop-valued judgment. Its type-substitution proof uses the old unrestricted All rules and a binder-aware finite prefix sufficient for the submitted type; it does not reclassify arbitrary old terms as finite typed terms. The telescope nucleus instead derives its laws from `Ctx`, `Form` and typed premises, and its finite substitutions use zero-filled unused term slots. The recursive-All mixed substitution adds finite type images with Bottom padding, formation-dependent image laws and the two distinct binder lifts. The stronger hypotheses of the latter theorems are not missing hypotheses of the first: they concern different judgments and stronger semantic conclusions. [N250B-219] [N250B-220] [N250B-224] [N250B-225] [N250B-210]

The earlier fifteen-constructor P01DF judgment states a separate fundamental theorem over arbitrary heterogeneous relation environments and pointwise raw-convertible index environments. Its seven-constructor raw PolyConv deliberately omits abstraction congruence, and no typing constructor accepts arbitrary semantic validity. The displayed J case nevertheless leaves a proof-coordinate transport obligation visible: hbase starts at B(x,I), and hm explicitly transports the endpoint from x to y while retaining I as the proof coordinate; the final relation is then selected at B(y,eval p). The additional transport from I to the supplied identity evidence is not exhibited in that branch. Because imported definitions and elaboration were not checked, this is an unresolved local proof obligation, not an observed compiler failure or a newly accepted fundamental theorem. Its stated unary and substitution semantic corollaries depend on that theorem. This qualification is separate from the already retained syntactic substitution transformer and does not transfer either interface to the later contextual HasE or Joint judgments. [SUB250-R81-097](../research/t20-v6-20261012/sources/604c355ab04ff6603144ee4e879dbe5d52ddbfbb7d0956fe3e8cbeac3dfec8d7/P01DependentFundamental.lean#L8-L196)

The Joint structural port adds another judgment-specific interface. Context inversion retains the old-E inclusion case; dependent lookup gives a formed lookup type, enabling substitution by any Joint-typed argument and syntactic regularity of the two added result types without semantic reflection. Its mixed substitution requires a formed target context, Joint formation of every type image and Joint typing of each term image at its transformed dependent lookup type. Under a term binder, term images lift and all replacement types weaken; under All, type images lift while the term map is unchanged. The sum branch requires two such term lifts and two weakenings of replacement types. Closed N is fixed, and the step-family square preserves the literal induction witness after substitution. These equations support the authored old-E-to-Joint and Joint-to-Joint formation/typing transformations, including the new elimination and induction cases; they do not assert unrestricted replacement by unformed types or a new dependency audit. [NEXT-J12-20](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/1eee1923d77df4ecff12aaba27a61477ee249e01997174243d06e13d36f4873a/JointRegularity.lean#L10-L73) [NEXT-J12-168](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3b6bbb780b092407089122ae93e51f381fe40e4f350778bdab15253b990f2fad/JointMixedSubstitution.lean#L10-L63) [NEXT-J12-168](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3b6bbb780b092407089122ae93e51f381fe40e4f350778bdab15253b990f2fad/JointMixedSubstitution.lean#L229-L246) [NEXT-J12-168](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3b6bbb780b092407089122ae93e51f381fe40e4f350778bdab15253b990f2fad/JointMixedSubstitution.lean#L405-L435) [NEXT-J12-244](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/4aefb592968abd48d87aa45d1191d0ae7f47d191758f467123f21f2e076f0c99/JointMixedAlgebra.lean#L11-L47)

The pure type specializations retain the distinction between actual E and actual Joint judgments. In each, every replacement type must be formed in the target context, and each source lookup must preserve the same term variable at its substituted dependent type; only an empty source telescope makes the lookup condition vacuous. Substituting the newest type variable restores the original telescope and derives the result-formation premise for All elimination, rather than assuming it. A finite type-image list needs formation only at its actual entries, with Bottom supplying the remaining images. Typed composition also respects order: term substitution after type substitution acts on the replacement types as well, whereas type substitution after term substitution keeps the already target-relative type images. These are judgment-specific applications of the imported mixed and dependent substitution theorems, not replacement by merely scoped types or an identification of HasE with HasJ. [SUB250-U20-179](../research/t20-v6-20261012/sources/701a3e5d84e9dcf3e5607ce2be886a6e2c7ecd17dc38c672a3418594691c3bd8/TypeSubstitutionApplications.lean#L12-L132) [SUB250-U20-128](../research/t20-v6-20261012/sources/6617c64a77785b81b55db3d3c4e6605e429f233f77fb8bf3306ffcd2ea34dff8/JointTypeInstantiation.lean#L13-L136)

The underlying actual-E mixed-substitution theorem carries both replacement families at once. It assumes a formed target telescope, actual-E formation of every type image τ(n), and actual-E typing of every term image σ(n) at the mixed image of its dependent lookup type. These are stronger premises than mere scope and concern HasE rather than HasJ. Under a term binder, σ lifts and every τ image weakens; under All, the telescopes type-weaken, the new type image is parameter0 and the older images type-weaken, while σ is unchanged. The endpoint-and-proof context of J requires two term lifts and two weakenings of each type image. Mutual induction over actual FormE/HasE handles finite imports, dependent products and sums, J, conversion and both extensionality rules, carrying the explicit scope obligations. The exposed typing corollary follows by applying the formation theorem to an identity formed from the supplied typing and then inverting it. Finite type-image lists may use formed Bottom padding, but arbitrary unformed replacement types are not admitted. This source proof retains the imported structural and mixed-algebra interfaces and supplies no fresh dependency audit or compiler result. [A1000-S33-066](../research/t20-v6-20261012/sources/ef218f67761ff75d7a5a68cb97f03f6699c1a3eb2a9a91625719939272df652e/HasEMixedSubstitution.lean#L11-L74) [A1000-S33-066](../research/t20-v6-20261012/sources/ef218f67761ff75d7a5a68cb97f03f6699c1a3eb2a9a91625719939272df652e/HasEMixedSubstitution.lean#L76-L146) [A1000-S33-066](../research/t20-v6-20261012/sources/ef218f67761ff75d7a5a68cb97f03f6699c1a3eb2a9a91625719939272df652e/HasEMixedSubstitution.lean#L147-L247)

The concrete type-substitution controls distinguish capture avoidance from mere replacement-list formation. Starting from I at All(α1→α1), replace the free parameter in context [Raw] by IdRaw(var0,var0). The resulting Pi codomain under All is IdRaw(var1,var1); leaving var0 there would capture the original free variable. Closing that target variable by the typed substitution var0↦I changes both endpoints inside the injected type image and gives All(IdRaw(I,I)→IdRaw(I,I)); retaining the old images after that term map gives a different raw type. A separate closed replacement proofId is formed only in actual E, using the supplied extensional branch witness. Type substitution alone then yields I at All(proofId→proofId), while original formation of proofId, and hence original Has typing at that result for any polynomial, is excluded. These controls preserve the actual-E premises and do not infer that merely scoped replacement types suffice. [NEXT250-Z50-217](../research/t20-v6-20261012/sources/a781b181d745e877b147e700619d3de54864bbefc1fb6f0ef0af768637849391/TypeSubstitutionControls.lean#L16-L49) [NEXT250-Z50-217](../research/t20-v6-20261012/sources/a781b181d745e877b147e700619d3de54864bbefc1fb6f0ef0af768637849391/TypeSubstitutionControls.lean#L51-L70) [NEXT250-Z50-217](../research/t20-v6-20261012/sources/a781b181d745e877b147e700619d3de54864bbefc1fb6f0ef0af768637849391/TypeSubstitutionControls.lean#L72-L104)

The independent actual-E term-substitution controls use CtxE and arbitrary HasE evidence throughout. Context inversion forms dependent lookup types, which builds the top substitution sending the newest variable to any E-typed a:A and retaining the older variables. Substitution then gives exactly psub(cons a var,b) at inst(B,a), with a parallel formation theorem; an identity whose endpoint was the newest variable becomes Id_A(a,a). Typed substitution maps compose by substituting the second map into each first image. Under a term binder the images lift with pup and the dependent types change accordingly; under All the telescope is type-weakened while the term map stays unchanged. These are applications of the imported actual-E structural theorem, not replacement by untyped arguments or a transfer to a different judgment. [SUB250-FINAL28-190](../research/t20-v6-20261012/sources/722bc48e3307e5f73d9650eaf5e2d2a40f41fe1523f6338743d41ff83bc99acd/IndependentControls.lean#L9-L72)

The underlying actual-E dependent term-substitution construction supplies the general theorem used by those controls. Each lookup image must have HasE typing in the target telescope at its simultaneously substituted dependent type. With a formed target context, mutual formation and typing induction carries FormE and HasE through substitution, including finite type images, J and both extensionality rules. A term binder lifts the map with pup and requires formation of the substituted head; a type binder weakens the telescopes while retaining the term map. J uses two lifted term binders for its endpoint-and-proof context, while product abstraction and extensionality retain their scope obligations. Thus no original-Has witness is required for substituted terms, but arbitrary untyped images are still excluded. The construction keeps the unchanged grammar and imported weakening, conversion and substitution equations; it supplies no new execution or source axiom report. [NEXT250-X25-130](../research/t20-v6-20261012/sources/9830e8dd5ffa26c1a28dfc85fd2f7660e6c56088ce4acae67035e3884cdbdfc3/HasEDependentSubstitution.lean#L11-L63) [NEXT250-X25-130](../research/t20-v6-20261012/sources/9830e8dd5ffa26c1a28dfc85fd2f7660e6c56088ce4acae67035e3884cdbdfc3/HasEDependentSubstitution.lean#L65-L122) [NEXT250-X25-130](../research/t20-v6-20261012/sources/9830e8dd5ffa26c1a28dfc85fd2f7660e6c56088ce4acae67035e3884cdbdfc3/HasEDependentSubstitution.lean#L136-L229) [NEXT250-X25-130](../research/t20-v6-20261012/sources/9830e8dd5ffa26c1a28dfc85fd2f7660e6c56088ce4acae67035e3884cdbdfc3/HasEDependentSubstitution.lean#L231-L240)

The old-E instantiation/composition control retains concrete applications rather than a new general substitution theorem. In its imported genuinely dependent context it obtains I at the endomorphism type of the supplied image both by top type instantiation and by universal introduction followed by formed elimination. It then composes a nonrenaming mixed map with the single typed Raw substitution sending the head to I. Applying the mixed-substitution interface to the imported J-conversion input gives the unchanged displayed polynomial K (J I I I) I at Id_Raw(I,I) in the empty context. These are dependency-relative proof applications; the imported context, image formation and nonrenaming map are required, not arbitrary unformed replacements or observed kernel results. [NEXT-C8-226](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/463c15dd52a18e24461582e91060aff958bf342486b4ae3693e6c42de7efe501/IndependentInstantiationComposition.lean#L11-L32)

The source-preservation obligation also survives each transition. The nucleus's legacy translation supports a restricted displayed Type-valued derivation tree, excluding unsupported old universal rules. The later recursive-All translation covers the supported old universal tree and finite-instance bridge with exact polynomials, including a finite application imported as one opaque atom. One must not replace `atom (Term.app f a)` by `Poly.app (atom f) (atom a)` merely because their evaluation agrees. Neither translation extracts a Type-valued syntax tree from an arbitrary Prop proof or inspects hidden conversion derivations. The recursive-All proof discharges image matching from smaller formed replacements; the malformed Sigma example above explains why unrestricted raw images cannot be substituted into that semantic theorem. These are the code-preserving gains earned by the later design repair and acceptance, not a claim of normalization or a universe of all types. [N250B-210] [N250B-224] [N250B-225]

The reported checking scope is finite and attributed. The nucleus review describes a 47-module closure, 17 added modules and 300 declaration audits; the recursive-All review describes 81 modules, retaining 47 inherited modules, and 588 candidate plus 44 independent-control declaration checks. The declared axiom boundary is `propext`, `Classical.choice` and `Quot.sound`. These source reports are evidence of historical bounded review, not present kernel output or independent human peer review. The positive joined witnesses, nonempty unequal endpoint Links, Raw boundary and exact old-tree translation remain the mathematical content; counts alone cannot establish them. [N250B-210] [N250B-225]

The scripts explain how that evidence was meant to be reproduced. The dependent-All `check-all` and `check-module` entry points delegate to explicit reproduction drivers. The drivers demand a readable `TOOLCHAIN_ENV`, check the declared Lean executable hash, and use the pinned import environment; they do not independently rebuild and verify every external mathlib object. The source-manifest utility records ordered imports and source hashes. The readback generator enumerates declarations and emits `#check`, `#print axioms` and audit commands; regex-based enumeration and generated commands are not their successful outputs. The public portable driver preserves that checking contract without local absolute paths. The normalized historical failed-log copy retains its failure diagnostics, not an invented success. [N250B-211] [N250B-212] [N250B-213] [N250B-214] [N250B-215] [N250B-216] [N250B-217] [N250B-218]

The sibling wrappers have their own contracts. The syntactic-substitution checker relies on the externally verified environment rather than independently hashing its Lean binary; `verify-inputs` checks the specified manifests, candidate and reviewer-control files, and recorded historical exit status. Its verification shell invokes those checks and readbacks. The nucleus's single-module checker does check the executable hash, validates module names and writes separate fresh logs; its `check-all` and reviewer `compile-one` wrappers delegate rather than furnish extra mathematical evidence. None of these files has been sourced or run here. [N250B-221] [N250B-222] [N250B-223] [N250B-226] [N250B-227] [N250B-228]

The normalization boundary in §10.3 has the same distinction between design, acceptance and reproduction. The design/admission files propose and delimit the literal exposed `S K (K Ω)` polynomial; the later independent review accepts the positive old typing and the no-convertible-finite-representative result under the inherited normalization/confluence closure. That failure was already available through old Raw and is not a regression caused by recursive All. The boundary's source-verification and ordered reproduction scripts preserve this dependency boundary. Its packaging account records an original shell-return 127, does not establish an alleged edit race, and distinguishes a portability smoke test using checked objects from a cold full rebuild. These qualifications preserve the stronger mathematical boundary without promoting the mere presence of a wrapper to successful new execution. [N250B-229] [N250B-230] [N250B-231] [N250B-232] [N250B-233] [N250B-234] [N250B-235]

[N250B-210]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/963ff1bc8b09a31637ed9b616410807bd97d1565a6da6d5944573fd4e0bbba21/REVIEW.md
[N250B-211]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/432d8eb689d7d1c76d5f8183ee434ccbbf6419c7dbe2937b12da833b2d22102d/README.md
[N250B-212]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/c3ce3803eeaa041b78ebe825067062e09cfa6c2bfcd726e82926da4158fdd9de/reproduce-module.sh
[N250B-213]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/45912110fb5ab80505c6173a3eaac1c9d8b761c43e2be0b7d4acee300ca56426/check-all.sh
[N250B-214]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/56ffe2ca9ae7661010b07bc9fb1e06ebc3e92f402c0b66b892eb2bfad7a5d3a4/check-module.sh
[N250B-215]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/46401f4b34aca9ac66b8b4d42f943b38f3ae111ccb8012f377992fe466a4c93a/make-readback.py
[N250B-216]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/14a753487334e8be5f3e1f9836bd6d373acb75c984b0a78f78c4f6a4ddba89c6/reproduce-all.sh
[N250B-217]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/dd33894849ba7f1f6d05594cf05130be5ca4b9a47868fc696b2dca2edf953ad9/reproduce-module.sh
[N250B-218]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/52766301c730ae93458ac25deab71b493a94dadd189fc6ce630a099a27028f59/source-manifest.py
[N250B-219]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/ab02d6afbf5e56a97051682aebe955395d41f1bb9f37e721d775693cca5ebdde/README.md
[N250B-220]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/c0b598b80f5ccd3bbcc2a3c8c9c03c8c51e4e77c9ba92845eaed5982d0178bd8/REVIEW.md
[N250B-221]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/8fa90c19a9f03c674b59a6e86e5750eb10bb503a8c7a719d30d091310ebd4969/check-module.sh
[N250B-222]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/0998ba1ff76bd6620707f38035612431fa94f9e16e1a5105b5f527d12eef21ab/verify-inputs.py
[N250B-223]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/934fc3b6c02da01cac4ab733c6fcfa9ba5aa1edaf6eff246444f4da27896e00f/verify.sh
[N250B-224]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/14c1276fc9443f79c4dfcd12e802110f40f3c435482e82ae02068c887fa70d42/README.md
[N250B-225]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/6e1832ad33853ba245c46ef65e7eb560bfb79f76ea5c566b5488a1b223a856c5/REVIEW.md
[N250B-226]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/6b5f2b434bc1cdc43862d20a4fd88fd73f95830fe009ad16a7cc5e5950cc0d09/compile-one.sh
[N250B-227]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/f9dccb6b33bb463a9d24f22cc4c9a5da3585772034808d4767ea3bac023722f7/check-all.sh
[N250B-228]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/e20f549d36bdc98d97b485f9365fb281b7c363a1aae9a44f6a2619a0d3f10b74/check-module.sh
[N250B-229]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/c4ac4efd0e0abaa29d031c377ab78d4e9b0083a4fd807584991a54bd05c4a81f/PACKAGING.md
[N250B-230]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/f9690e33ee57f8e665d47954e7dbe0cfedf7ddc6770557d3e2566ccd055dbc23/README.md
[N250B-231]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/be25d5f4177387c99909bd173009e391ea80be6335e8ba5bcc452b5dd436fa5d/DESIGN_REVIEW_v1.md
[N250B-232]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/2c67e22d0b19126c63fc9f1e476dd38d06174bd9208d816680165a64b437ea23/INDEPENDENT_REVIEW.md
[N250B-233]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/f0cab5068c0ea6205a51d07d1fd3686b8551417f749ad55c327fb1a4c2b39851/POLYMORPHIC_NONNORMALIZATION_ADMISSION_v1.md
[N250B-234]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/b1551290af5638d00a3ceb40b4c6d0407b99910591375523997be247f28cf012/reproduce-all.sh
[N250B-235]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/59dfb863bd8f583993d9497f961db96d009343d805abb81fd4f67e5516600a23/verify-sources.py

#### Exact sources for the typed-telescope extension

[T11R16]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0469bca07f0057d734ea479380f4e33cc45e6f673ab1aa71be93ca141c549912/AllJoinedControls.lean
[T11R21]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/05b13737c47cf4987d0a8892a8e791930a8da714684d8acaccb4dac81e1d2f9e/IndependentEndpointControls.lean
[T11R44]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0a0b469b9b874b9ec4bf6d1d3c94e4214a14d7ca90961b0d6e6b14cbd4a76137/SubstitutionReadback.lean
[T11R49]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0d2d2c2d2aba2dadd6f194b86b1ba87c693a9f3cebe0fc4fda5cc0391c7a192e/AllLegacySyntax.lean
[T11R66]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1272802684942dfd8e4009ce772f2685cdd5550fad4ae1fb36059245d39435fa/AllLegacyDerivations.lean
[T11R76]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/15f1fd5429884678f073c9b7bb302a2711567ef7952de7de8160c606ddaf2c66/TypedBoundaryResults.lean
[T11R81]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/18db66b880752841d3103651ee62224312bd37c2b030a77b44011f56439b4140/PROOF_GUIDE.md
[T11R90]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1be1692557b5ec60b7b0170f0682c0503b1d9ea76ca582ff95a3a8af66517f8d/TypedContextualJ.lean
[T11R118]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/234d778b12696c34cf7d61f5fa0c75b4f3e488d14b29f09aef89ea6a12ac8a12/TypedLaws.lean
[T11R137]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/29ef624541635cd7a2ae00c5c19de93895472b7c676d63ce6c2d8233b7614834/TypedConstants.lean
[T11R139]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/29f0417393cb5dcc24173c892f385de9cab9ceb721ca85a417b3cfd04727006c/AllStructuralChecks.lean
[T11R151]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2f5d21fa81bed6dbabc6659a9f695983e9dafad5f9d36656c23d9988b209527b/TypedPositiveControls.lean


The exact structural providers give separate support to this already established construction. `TypedStructural` proves dependent lookup and scope preservation, weakening, formation of typing results, and finite substitution composition for the typed telescope. `AllStructural` supplies simultaneous term/type substitution for recursive All, with atom-zero term padding, Bottom type padding, scoped finite identities, and the two lifts needed by the endpoint/proof motive. Their finite maps are not arbitrary total semantic transports. [R750A-511] [R750A-550]

The separately retained `TypedSigmaLaws` and `AllPiLaws` derive their law packages from the smaller domain/codomain laws. Sigma preserves the represented pair and the first-coordinate-dependent second fibre; Pi extends the related argument environments before applying codomain laws. `AllPredicates`, already cited as [original-predicates], supplies the actual mutually structural F/G definitions, including All's use of the smaller body's heterogeneous predicate and identity's proof conversion to I. It is a provider of these definitions, not another derivation of all their laws. [R750A-514] [R750A-525] [R750A-523]

`AllInheritedPositiveControls` gives exact examples for the positive dependent pair, bracket abstraction, heterogeneous pair and two-coordinate J described above. Its non-Raw PER relates I and SKK although the source terms are not convertible; its J witness uses a changed endpoint and a nonliteral proof convertible to I. The inhabited but distinct Raw fibres remain a countercontrol. These additional exact witnesses preserve the earned coherence result without extending arbitrary heterogeneous links into raw equality reflection. [R750A-503]

[R750A-503]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/86989a82ccb5c8afd430b1c87a446d30f8b1df76239a80f281c5a0a11316fd37/AllInheritedPositiveControls.lean
[R750A-511]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/881b63b6e21657c32cdd5347c0e32b7877214836ba6c15c45d3e67048d2f0caf/TypedStructural.lean
[R750A-514]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/88d025701e15b575b14f6790d0e6ef707591951ed8fd2d3af5aa37ccf92d707e/TypedSigmaLaws.lean
[R750A-523]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8a8986200e9f4a6713238b77a1f23605201ee61552e55e72a2165eef05bab1d3/AllPredicates.lean
[R750A-525]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8bf72d8305f56d39b629be8d1c417cb58e0259b579d5cfada2fe5017e7ed242f/AllPiLaws.lean
[R750A-550]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9396848b7cfd7463d1b445783193795eb50fbaa7b6165ba89cb0e6811d03d4e1/AllStructural.lean

### 10.12 Finite proof checking does not decide general inhabitation

The closed criterion of §10.7 admits an exact algorithmic classification, provided the input problem is specified. Checking a *supplied, fully annotated finite derivation tree* differs from finding such a tree for a displayed judgment, and both differ from finding some polynomial inhabiting a displayed type. Finite syntax can be encoded with constructor tags, natural-number labels and finite list delimiters. Parsing and equality of annotations are literal syntactic operations, never calls to a conversion oracle. The actual term and type substitutions, their separate binder lifts, weakening, instantiation, abstraction, finite-type embedding and context lookup are computable structural operations on this syntax. Arbitrary semantic functions or valuations are not free certificate inputs. [Q250A-010]

FiniteTypeCodeCompilation makes two of these structural operations numerical without turning them into validity tests. One fold computes the finite-code support: a variable contributes its index plus one, a universal binder takes the predecessor, and an arrow takes the maximum. A second fold translates the finite type code into Ty; the arrow branch weakens its translated codomain. Both numerical functions are stated primitive recursive, with exact agreement on every encoded TypeCode, uniformly in the fold’s otherwise unused environment. Their step functions are total, using zero for missing child values and support fallback and Ty.bottom for the translation fallback. These defaults do not certify that an arbitrary natural was a finite type encoding or that its translated type is formed in a supplied context. [NEXT-FC14-165](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3af59a3bc61edd9a25b7418077ea1a9d07549ae94df0e09bd79b6167f0b2eb17/FiniteTypeCodeCompilation.lean#L8-L94)

The numerical substitution interfaces remain sort-specific. TypeCode substitution uses a finite replacement list with variable tail n−length(images)+shift, lifting the list and shift under All; its single-entry, zero-shift specialization agrees exactly with type instantiation on encoded TypeCode values. The larger Ty mixed operation instead uses separate term- and type-binder lifts, and substitutes into the two polynomial endpoints of an identity as well as its carrier. Each is stated primitive recursive and exact on its specified encoded inputs. The visible mixed Ty fold filters children by strictly smaller syntax code; this is not the sorted validity evaluator's additional check that every originally listed child descends. Thus the total substitution folds, missing-child defaults and exactness equations do not themselves validate arbitrary natural codes, establish target formation or accept source derivations. The proofs remain relative to their imported environments, folds and encodings. [SUB250-U20-225](../research/t20-v6-20261012/sources/7a0d7f680593f6103a1def6653bdd1fb93b7a9494860cb29c6e29508d44d0c82/TypeCodeSubstitution.lean#L7-L107) [SUB250-U20-248](../research/t20-v6-20261012/sources/7dccb04e63985a804a01bc0baa451de4d2afb3d0b4c5a99e5fb1e4535d0fd1de/MixedTypeSubstitution.lean#L8-L130)

The finite mixed environment exposes two distinct type tails. A listed image is used when present; beyond the list, variable-tail mode returns parameter n−length(images)+shift, while bottom-tail mode returns Bottom and ignores the shift. Crossing a term binder lifts the polynomial environment and term-weakens each listed type image without changing its tail mode or shift. Crossing a type binder leaves the polynomial environment unchanged, prepends parameter zero, type-weakens the listed images and increments the shift. The source states primitive recursiveness of these numerical operations and exact agreement with the corresponding source environments. Independent unfolding equations distinguish these lifts from type-parameter renaming, whose Pi codomain uses the unchanged renaming environment, and test the missing-parameter Bottom branch. These are finite environment and encoded-input equations, not validity or formation checks; their imported encoding and renaming dependencies remain unverified here. [NEXT250-Q25-076](../research/t20-v6-20261012/sources/8d1de1cd47a02c741eb8601c1c91a63247916e5a60cba9e3b2fbc4cb9dab78cd/FiniteTypeEnvironments.lean#L7-L79) [NEXT250-Q25-085](../research/t20-v6-20261012/sources/8f33af4663ff4a8725001fa7e852dc677569179673d7cd43eb4084faf29fb42e/IndependentCodeEquations.lean#L6-L51)

The finite polynomial environment has its own total numerical substitution construction. Listed images are used in order and the unlisted tail maps n to var(n−length(images)+shift). The numerical transformer substitutes a tag-zero variable, leaves tag-one codes unchanged, and recursively transforms both children of a tag-two application only when both codes strictly decrease; unsupported or nondecreasing branches return zero. Strong-recursion tabulation establishes primitive recursiveness, and structural induction identifies the result on encoded polynomials with actual substitution. Empty images realize variable shifts, one image with zero tail shift realizes single instantiation, and crossing a term binder prepends var0, shifts every listed image and increments the tail shift, exactly matching pup. The arbitrary-code defaults make the numerical function total; they do not validate arbitrary atom payloads, establish type formation or turn encoded-input exactness into all-natural syntax recognition. [NEXT250-Z50-236](../research/t20-v6-20261012/sources/aac5c80b5842c9cfe01b587a9d7880a6235dddf78ddb927f20e0e4c9fef7a7c9/FinitePolySubstitution.lean#L8-L44) [NEXT250-Z50-236](../research/t20-v6-20261012/sources/aac5c80b5842c9cfe01b587a9d7880a6235dddf78ddb927f20e0e4c9fef7a7c9/FinitePolySubstitution.lean#L46-L98) [NEXT250-Z50-236](../research/t20-v6-20261012/sources/aac5c80b5842c9cfe01b587a9d7880a6235dddf78ddb927f20e0e4c9fef7a7c9/FinitePolySubstitution.lean#L100-L162)

Term substitution into the larger Ty grammar has its own numerical fold. It retains the finite polynomial environment under All, lifts it only in the codomain of Pi and Sigma, and transforms both wrapped polynomial endpoints as well as the carrier of an identity. Well-founded recursion filters children by strictly smaller syntax codes and uses total missing-child defaults; primitive-recursion closure then supplies the numerical transformer. Structural induction states exact agreement on every encoded Ty, with empty images and shift1 giving term weakening and one image with shift0 giving instantiation. This is distinct from type-parameter renaming and mixed substitution. Neither its filtered fold nor its encoded-input exactness validates arbitrary natural codes, forms a target type or establishes a source judgment, and its imported polynomial/environment interfaces remain dependencies. [A750-S50-076](../research/t20-v6-20261012/sources/bc3b5580f5a285c3055b85f157221c7c2df4262224cec58300d9e46d68d0b548/TermTypeSubstitution.lean#L8-L50) [A750-S50-076](../research/t20-v6-20261012/sources/bc3b5580f5a285c3055b85f157221c7c2df4262224cec58300d9e46d68d0b548/TermTypeSubstitution.lean#L52-L95) [A750-S50-076](../research/t20-v6-20261012/sources/bc3b5580f5a285c3055b85f157221c7c2df4262224cec58300d9e46d68d0b548/TermTypeSubstitution.lean#L97-L144)

The separate coded type-renaming interface represents a renaming by a finite image list and a tail shift: index n uses the listed image when present, otherwise n−length(images)+shift. Passing a type binder prepends zero, increments every listed image and increments the shift. The authored primitive-recursive fold agrees with type-parameter renaming on every encoded Ty; on identity types it transforms the carrier while retaining both polynomial endpoints. The empty image list with shift one gives exact coded type weakening. These total numerical operations are not tests of code validity or context formation, and their exactness proof uses the imported bounded-fold interface. [NEXT-T8-081](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2be86e10b9afad02649da01fcf4ee39a06659c2e2cbe1f3cc7cae7ee961706de/TypeRenaming.lean#L7-L121)

The finite TypeCode renamer has its own exact interface: its bounded fold handles variables, arrows, universal binders and bottom, lifting the finite renaming environment under All. It is stated primitive recursive and agrees with finiteRen renaming on encoded TypeCode values; the empty image list with shift one gives exact successor renaming. This is distinct from the larger Ty operation above. The rule-template helpers likewise state primitive recursiveness and encoded-input agreement for telescope cons, type weakening, theta, length, the six context/formation/typing claim constructors and the ordered finite-image formation list. These numerical building blocks do not test whether an arbitrary code is well formed, establish the listed premises or accept a whole derivation. Their proofs remain relative to the imported folds, transports and encoding interfaces. [SUB250-C9-028](../research/t20-v6-20261012/sources/536f7894ebb7650d9802eb4000524190fcadb145a9940973d7a6b0471d4ead8f/TypeCodeRenaming.lean#L7-L71) [SUB250-C9-002](../research/t20-v6-20261012/sources/4d2e0779f1da48dc05dd46cbf90545ea03df8d7623cc566461d2a27e81c3583e/RuleCodeBasics.lean#L11-L100)

**Exact finite presentation.** Validate all two context, seven formation and eighteen typing constructors recursively, together with the five raw `Step`, two `Red`, four `Conv`, two `Lookup`, seven `FiniteDerives` and eight bridge-extended polynomial-conversion cases. For unchanged Has, omit only the extra bridge constructor. Every repeated endpoint or computed annotation must agree literally. In particular, a `Red` certificate may use either application context and any finite sequence, not just the inherited head-step elaborator. `Lookup` computes the rule's iterated weakenings, not unweakened list access. A finite import with image list τ has exactly length(τ) image-formation certificates, one for each actual index below that length; the displayed universal implication over natural indices is reconstructed from that finite list and is vacuous beyond it. Bottom defaults do not add infinitely many premises. Likewise finite `allI` has one child, not a family indexed by semantic types. Do not insert extra TypeCode scope conditions from a convenience checker where the actual relation has none. [Q250A-010]

The separate LookupCert image lemma concerns which natural codes encode syntax, not whether the encoded lookup judgement holds. It reconstructs either constructor from the local shape and canonical child codes; the successor case retains its raw natural payload separately from its four canonical fields. Thus local encoded-image recognition and checking the represented telescope lookup remain distinct obligations. [B141-052](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/0af3a293348ba5d2830c0e899797a2fa151187b467091fa0a84be69d09476b02/LookupCertImageRule.lean)

The selected code proofs distinguish three further obligations. GrammarExactness characterizes the image of each of Term, TypeCode, Poly and Ty by local shape plus canonical children; the StepCert and PolyCert image rules likewise reconstruct certificate syntax, without asserting its judgment. The StepCert child bound assumes that the parent already lies in the encoded image. By contrast, StepExact, FiniteExact and LookupCode compare numerical checking with typed certificate checking only when certificate and endpoint inputs are actual encodings. LookupCode computes the weakened type and increments the successor index; RedCode performs its step-certificate check locally and sends only the reduction tail to its recursive child. None of these image-restricted agreement statements alone rejects every malformed natural code. TelescopeDecoderBridge supplies a different all-natural interface: normalizeTel retains c exactly when validTel c holds, agrees with decode₂ Tel c followed by re-encoding, and yields primitive recursiveness of the encoded optional decoder without assuming Primcodable Ty. These are source-level proofs relative to their imports, not newly checked compilation. [NEXT-FC14-134](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/34e2dc12d272d788c1486bcc297a1db469f29752e4643e6c9fc87404e06d3dab/GrammarExactness.lean#L7-L105) [NEXT-FC14-196](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3fd121ca64cd6040b3115c37e8e8874be104cfc79f47e8f076f29941cea52926/StepCertImageRule.lean#L9-L44) [NEXT-FC14-178](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3d3d2bff2dc3d83deace29aafe51cf23fbea5488f285156c219b67a5b9fd8778/PolyCertImageRule.lean#L9-L59) [NEXT-FC14-029](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/207cd23966fc3739f3f85e76c3d899309d67c5b8b95412b940f2f94bd3be96aa/StepCertBounds.lean#L9-L16) [NEXT-FC14-048](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/241549430d00dcf35b9b534aa3fc73633145c435513e1679db2478e5ae70269e/StepExact.lean#L10-L48) [NEXT-FC14-167](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3b6110d2c9bdf01e0b1a4919af7533f014d9d9e2ccd102edf3bc6adb5d5cd7bc/FiniteExact.lean#L10-L69) [NEXT-FC14-028](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/205e4fc56700411e39a6aa6dc40c46ca8cf527e4e4512ea321a5b73fda367fca/LookupCode.lean#L29-L96) [NEXT-FC14-092](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2e5c2b441c218013799e3438374f99bca4902f291d40222b7e5f9fa2e9f4c4e6/RedCode.lean#L13-L41) [NEXT-FC14-011](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/1c5de72e470fd616a9f35ea502f9ad3da4a9e4184967effac8606a8b3f14c0cb/TelescopeDecoderBridge.lean#L8-L37)

Two concrete code components refine these interfaces. The polynomial templates compile pair, projections, erased J, branch application and the total-space section by primitive-recursive numerical constructors. branchAtCode uses the ordered substitution list [b,a], and sectionPolyCode shifts both seed and step before abstracting; their agreement statements apply to actual encoded polynomials. The separate StepCode dispatcher has exactly five tags for I, K, S and left/right application congruence. It checks the stated endpoint equations locally, passing one endpoint-pair/certificate child only in each congruence case; other tags return false. Its final result is primitive recursiveness of that numerical check through the imported evaluator, not a new all-natural syntax-validity or judgment-exactness theorem. Neither component by itself forms a type, validates arbitrary payloads or accepts a source derivation. [NEXT250-T25-057](../research/t20-v6-20261012/sources/89deb4788ac40500777a8547419d52ccc18e4338de4b26f49b911db554cf61a2/PolyTemplates.initial.lean#L7-L46) [NEXT250-T25-057](../research/t20-v6-20261012/sources/89deb4788ac40500777a8547419d52ccc18e4338de4b26f49b911db554cf61a2/PolyTemplates.initial.lean#L48-L78) [NEXT250-T25-067](../research/t20-v6-20261012/sources/8b188c36004c91c2559bda4c6851a2402cd6ca5d0dcaa689a893bf8db5839d6a/StepCode.lean#L9-L32) [NEXT250-T25-067](../research/t20-v6-20261012/sources/8b188c36004c91c2559bda4c6851a2402cd6ca5d0dcaa689a893bf8db5839d6a/StepCode.lean#L34-L44)

The corresponding type templates compile more than the polynomial witnesses. arrCode weakens its codomain, motiveAtCode substitutes the ordered images [e,y] with tail zero, the Sigma branch substitutes [pair(var1,var0)] with tail two, and the successor family substitutes [succ(var0)] with tail one. These form the dependent step type, while thetaListCode places Id_(wk A)(shift x,var0) before A and the old telescope. Primitive-recursion and exactness statements identify these numerical constructions on actual encodings. The separate no-lift control exposes a binder obligation: substituting e=var4 and y=var3 into the displayed Pi identity must lift the images under Pi to var5 and var4, rather than retain var4 and var3. That negative target is not a received rejection. Neither the positive template equations nor this control establish formation, off-image validity or derivability of arbitrary supplied codes. [AFTER750-F50-215](../research/t20-v6-20261012/sources/d71ac2b967488993a0de3d01a3a1c7ef7452c1848b1982141e2a7bb826c14184/TypeTemplates.lean#L8-L58) [AFTER750-F50-244](../research/t20-v6-20261012/sources/dd9971bd57e2962eff325923396ec95e02f9bb88bf1b04d0db39701a775b2b43/WrongMotivePiNoLift.lean#L6-L7)

The finite-code controls retain the numerical binder contract for the type templates as well as the polynomial ones: motiveAtCode uses ordered images [e,y] with tail0, the Sigma branch type uses [pair(var1,var0)] with tail2, and the successor family uses [succ(var0)] with tail1. Theta prefixes Id_(wk A)(shift x,var0) and A to the telescope. Pi lifts term images while All leaves that term environment unchanged. The mixed-code specializations separately distinguish false-mode type-image padding by Bottom from the true-mode singleton environment that retains successor parameters. With an empty term-image list, the latter computes type instantiation; false mode computes finite type-image substitution, and mapping type weakening computes twkTel. Their primitive-recursion and exactness statements concern actual encodings. They do not validate arbitrary natural codes or supply formation or derivability; the separate ordered finite-image premises, including unused and duplicate entries, remain obligatory. [L34-102](../research/t20-v6-20261012/sources/f75a1be2f043b8b860156bc7ed869f467bffcd2400fceb16fca5bdcb01117bdd/IndependentTemplateControls.lean#L12-L37) [L34-127](../research/t20-v6-20261012/sources/ff1f5143c2fe6d0bb25036b14d6be332fbfe4156ac1c899460bcdefc8b708577/MixedSpecializations.lean#L9-L46)

The polynomial analyzer supplies three linked numerical operations in one recursion: occurrence of variable zero, binder-removing drop, and the literal compiled bracket abstraction. Its variable and atom branches construct those three results directly; at an application it combines the two occurrence flags, combines the dropped children, and chooses the S branch only when a child uses variable zero, otherwise applying K to the dropped application. Strictly smaller child-code tests make the natural-code definition total, with a fixed default outside the supported branches. A list of earlier results gives the bounded-table step used in the primitive-recursion proof. Structural induction then states analyze(encode p)=(freeZero p,encode(drop p),encode(abstract p)), and projection gives primitive recursiveness and encoded-input exactness of each component. Totalization does not certify an arbitrary natural as syntax, and this code-level correspondence neither supplies typing nor permits arbitrary abstraction congruence. The coding, child bounds and compiler equations remain imported; no axiom-print output or kernel execution is supplied. [R134-002](../research/t20-v6-20261012/sources/deb8e4780f2ee2ee2f05de1dd2a5893261f51caa025e729557bef670576c835b/PolyAnalysis.lean#L7-L108) [R134-002](../research/t20-v6-20261012/sources/deb8e4780f2ee2ee2f05de1dd2a5893261f51caa025e729557bef670576c835b/PolyAnalysis.lean#L110-L153)

The numerical PolyCert dispatcher has eight tags: reflexivity, symmetry, transitivity, application congruence, I, K, S, and the atom/application bridge. It checks the requested endpoint equations locally. Symmetry creates one recursive child with the original endpoint order, transitivity creates the two ordered links through its stated middle, and application creates function and argument children; the remaining branches have no recursive certificate children. The bridge is directed from the atom of a raw application to the polynomial application of its two atoms, so reversing those endpoints is not the same certificate. The stated primitive-recursion result follows by composing the primitive-recursive shape and child functions with the imported evaluator. This is a total numerical checking component, not an all-natural canonicality gate or an independent proof that its accepted endpoints denote a valid judgment. Its constructor encodings and evaluator stay explicit dependencies. [R134-004](../research/t20-v6-20261012/sources/df3b012c33bc1502fb711ea5a48070ab30bb4c558211a188cd0921f8a500e9d3/PolyCode.lean#L9-L42) [R134-004](../research/t20-v6-20261012/sources/df3b012c33bc1502fb711ea5a48070ab30bb4c558211a188cd0921f8a500e9d3/PolyCode.lean#L44-L56)

The Rule image proof performs the corresponding reconstruction for all 63 tags, numbered zero through 62, across the Joint and old-E rule constructors. For every natural c it states that c encodes an actual Rule exactly when its rule descriptor has local shape and every listed child is CertCanonical. The reverse cases reconstruct canonical syntax fields from their child witnesses while recovering raw natural payloads directly from their wrapped slots. This recognizes rule syntax, not the truth of the rule's premises or conclusion. The companion certValid controls retain overlapping numerical images: the code of Term.i also encodes the empty serial-certificate list, Term.k the empty Joint-context rule, and Poly.var(0) the empty Joint-context claim. Intended sort, exact shape and recursive child validity therefore remain separate obligations; neither these controls nor the Rule image equivalence supplies a fresh compiled checker or the generic evaluator's child-descent proof. [SUB250-F28-104](../research/t20-v6-20261012/sources/612f222a031e552d406ea7beede269ebcf6bd0bd326d92f71e6d0e3a163a7562/RuleImageRule.lean#L9-L1024) [SUB250-F28-146](../research/t20-v6-20261012/sources/6a220150949a9ea156ceac6902c145475caa0adf29027d0b625dfcf3730587c2/ControlsPrefix.lean#L10-L63)

The rule-conclusion encoder supplies a different numerical interface from rule-image recognition. It has 63 tag branches for the Joint and actual-E context, formation and typing constructors; the dispatcher returns zero outside those tags. Its source states both primitive recursiveness and exact agreement conclusionCode(encode r)=encode(r.conclusion) for every syntactic Rule r. Dependent projections and J compute their indicated instantiated result types, and the Joint-only sum-elimination and induction branches construct their own conclusions. This extracts syntax without checking the rule premises: lookup and conversion certificates, and some extensionality witnesses, need not affect the computed conclusion. Exactness on encoded rules therefore supplies neither acceptance of malformed natural codes nor derivability of their conclusions. The code-constructor, substitution and encoding equations remain imported dependencies, and the axiom-print requests are not received execution results. [NEXT250-X25-144](../research/t20-v6-20261012/sources/9a8846405f456079b1bb0676355f8203c3474785187b9b31ca30ddc8767f076a/RuleConclusionCode.lean#L191-L204) [NEXT250-X25-144](../research/t20-v6-20261012/sources/9a8846405f456079b1bb0676355f8203c3474785187b9b31ca30ddc8767f076a/RuleConclusionCode.lean#L386-L519) [NEXT250-X25-144](../research/t20-v6-20261012/sources/9a8846405f456079b1bb0676355f8203c3474785187b9b31ca30ddc8767f076a/RuleConclusionCode.lean#L956-L1209) [NEXT250-X25-144](../research/t20-v6-20261012/sources/9a8846405f456079b1bb0676355f8203c3474785187b9b31ca30ddc8767f076a/RuleConclusionCode.lean#L1210-L1404)

A different generated RuleConclusionCode.initial body must not inherit that exactness claim by its name. In both its Joint and actual-E piExt branches, the displayed expression puts piCode outside identityTyCode, includes the anomalous subexpression encode(), and applies the outer Pi constructor to additional arguments. The corresponding Primrec expression repeats the same constructor nesting. This differs from an identity whose carrier is the Pi type and whose endpoints are the two supplied functions. A lossless structural census retains all 63 constructor blocks and 63 dispatch definitions, but only the two anomalous blocks and an initial bounded range receive full raw-body analysis here; the remaining proof bodies are not thereby verified. The local template discrepancy blocks promotion of this variant's advertised total exactness, without replacing the correctly bound encoder above or reporting compiler execution. [A750-T50-108](../research/t20-v6-20261012/sources/c34174d2511c2ef1f6e9a47075e1fbd992032f761f4321eb2b8c220a171f9464/RuleConclusionCode.initial.lean#L521-L537) [A750-T50-108](../research/t20-v6-20261012/sources/c34174d2511c2ef1f6e9a47075e1fbd992032f761f4321eb2b8c220a171f9464/RuleConclusionCode.initial.lean#L1048-L1064)

The reduction-specific counterparts keep the same input restrictions. RedExact compares checkRedCode on the encodings of an actual RedCert and actual endpoint terms with checkRed on those objects; induction handles reflexivity and the tail constructor, using exact step checking and strict descent of the encoded reduction tail. RedCertBounds separately proves descent for every listed local child only under the premise that the parent already encodes an actual RedCert. Neither result replaces the stronger local-shape descent premise of the generic sorted evaluator, rejects arbitrary malformed naturals by itself, or says that every supplied reduction certificate is accepted. These remain agreement and image-bound interfaces relative to their imports, not fresh compiler or axiom-readback results. [SUB250-R25-114](../research/t20-v6-20261012/sources/6418f5d8dca6647618567550105573ebc7b39f3d3d98d02860ad7c94d5cad43a/RedExact.lean#L10-L30) [SUB250-R25-192](../research/t20-v6-20261012/sources/726ce24640ec6a8939e32515b15ce12512fe23cdd4a3a524d737c657f43a583f/RedCertBounds.lean#L9-L16)

Two additional image rules reconstruct certificate syntax on every natural input. RedCert has the reflexive and tail tags, reconstructed respectively from one and five canonical fields; FiniteCert splits its seven I, K, S, application, universal-introduction, universal-elimination and reduction tags and reconstructs their canonical payloads. In each case encoded-image membership is equivalent to local shape plus canonicality of every listed child. This does not make the represented reduction or typing judgment true. PolyExact proves a different statement: at an actual encoded PolyCert and actual encoded endpoints, checkPolyCode agrees with checkPoly. Its eight-constructor induction uses strict child-code bounds in the recursive symmetry, transitivity and application cases. Image reconstruction, image-restricted checker agreement, and all-natural judgment acceptance remain separate, and the grammar, codec and evaluator interfaces are imported rather than newly audited. [A750-F50-003](../research/t20-v6-20261012/sources/ae3d6d456fe9b3825e6135d7cc0ae2c08335dba35aa9ced9054b23121a50f65d/RedCertImageRule.lean#L9-L29) [A750-F50-022](../research/t20-v6-20261012/sources/b25f6e5ea74551b6a81c9805623ba6f96b766c67e5766569b91ea51e9bd761eb/FiniteCertImageRule.lean#L9-L54) [A750-F50-017](../research/t20-v6-20261012/sources/b15cc421bb5be1e4664be5e885f254733b50743e7a7e840b88b0b28fe691c306/PolyExact.lean#L10-L75)

The standard list-to-natural transport has a weaker input assumption than a primitive-recursive decoder for every head type. For any Encodable alpha and list xs, encoding the list of encoded heads gives the same natural as encoding xs itself; consequently listNatDecode (encode xs) returns xs.map encode. The source inherits primitive recursiveness of this natural-list decoder from telNatDecode. These algebraic transport statements require no Primcodable alpha premise and do not establish primitive-recursive decoding or validity recognition for arbitrary alpha values. [SUB250-U20-158](../research/t20-v6-20261012/sources/6c741ab45a9db890fa98fb6c8fee7148e2f552917a288a36d726b9c556144ff9/ListNatCodeTransport.lean#L7-L27)

The exact telescope replay driver has a source-level audit-dispatch inconsistency before its final PASS receipt. Its selected module list includes ListNatCodeTransport. After a successful compile, that name enters the four-name audit branch, but the required-count dictionary contains only TelescopeValidityAudit, TelescopeTransportAudit and ListNatTransportAudit. Indexing it with ListNatCodeTransport therefore raises KeyError if execution reaches that branch, regardless of the number of printed axiom records. Earlier compilation or dependency failures could stop sooner. The later negative-control loop, final pin check and FINAL_REPLAY.json emission cannot be credited from this body as a successful completed path. This observation does not refute the algebraic list-code transport statement or establish a compiler failure in its Lean module; no target was executed and no historical receipt was opened here. It qualifies only this exact Python variant and cannot be transferred to another verify_final.py or silently repaired by omitting the selected module. [AFTER1884-N25-223](../research/t20-v6-20261012/sources/8018308dae4fbacb2e250ceecd40204eb0f36f8a5252b99564379d7e7cf2e065/verify_final.py#L8-L10) [AFTER1884-N25-223](../research/t20-v6-20261012/sources/8018308dae4fbacb2e250ceecd40204eb0f36f8a5252b99564379d7e7cf2e065/verify_final.py#L23-L46)

The separately retained verify_release.py has a different dispatch condition: it compiles ListNatCodeTransport, but its axiom-count branch contains only TelescopeValidityAudit, TelescopeTransportAudit and ListNatTransportAudit, with matching required counts eight, three and four. The specific missing-dictionary-key mechanism in the preceding verify_final.py therefore does not occur at this branch; that comparison neither repairs nor requalifies the earlier body. This release wrapper additionally requests exact Boolean control outputs, three source-specific negative diagnostics and pin checks before and after its selected trust-zero compilation. Its receipt template withholds baseline rebuilding, ordinary-decoder equivalence and whole-checker computability; the imported verifier, Lean sources, actual outputs and receipt remain separate evidence. No execution or successful release is inferred from this source-level variant comparison. [AFTER2884-SECOND25-40](../research/t20-v6-20261012/sources/ec5481854cebf1ccd408355ab91974eead812273936da505a64442f180ef733c/verify_release.py#L6-L20) [AFTER2884-SECOND25-40](../research/t20-v6-20261012/sources/ec5481854cebf1ccd408355ab91974eead812273936da505a64442f180ef733c/verify_release.py#L23-L47)

Two further numerical interfaces keep these obligations separate. FiniteCode instantiates the generic evaluator with the seven finite-typing tags: application supplies two ordered children, universal introduction/elimination one, and reduction checks its Red certificate locally while recursing on the finite-typing premise. Its primitive-recursion theorem does not add all-natural judgment exactness. CanonicalDecoderBridge instead uses the exact image characterization of each of Term, TypeCode, Poly and Ty to prove that normalize(s,c) retains precisely canonical codes and equals decode₂ followed by re-encoding. It thereby obtains primitive recursiveness of the encoded optional canonical decoder; arbitrary Encodable decoders are not assumed canonical. [SUB250-U25-183](../research/t20-v6-20261012/sources/70adda5b1c8e800cdb922a798881d1e1e00252f54f3471e5b43fc14b9d411b65/FiniteCode.lean#L11-L53) [SUB250-U25-186](../research/t20-v6-20261012/sources/7117b558c50b00e345be4d5063c9a6b1c957d855cf7fde1f2ae25ed6f67d08df/CanonicalDecoderBridge.lean#L8-L63)

The descriptor controls make the local/global distinction concrete. They state local-shape acceptance for step, claim and serial-list descriptors without asserting global validity of the children; the serial-list example records child sorts 13 and 14 separately. Their literal equality encode(Term.zero)=encode(TypeCode.bottom) also shows that syntax sorts can overlap numerically. A code therefore needs its intended sort and recursive validity conditions; numerical equality alone cannot supply a globally disjoint sort classification. Separate bad-tag and malformed-field controls concern local shape only. These are dependency-relative written controls, not newly observed checker results. [NEXT-C30-192](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3f2c5a9bf0d9fa9c8e694dfb5abbe0d9171c72f9810a20238db5ead0748f47d8/DescriptorReviewControls.lean#L6-L16)

The serial-certificate-list image rule supplies the corresponding all-natural grammar equivalence: c encodes an actual SerialCertList exactly when its descriptor has local shape and all listed children are CertCanonical. The reverse proof splits the nil and cons tags and reconstructs the latter from its certificate-head and list-tail witnesses. The companion controls exhibit locally shaped cons data whose head or tail code is invalid, alongside the shared numerical encoding of Term.i and the empty list. Thus local shape, intended child sort and recursive validity remain distinct, and this image equivalence does not establish any encoded judgment or the soundness of a submitted proof tree. The listed constructor examples and diagnostic #check/#eval commands are authored requests, not observed runtime acceptance. [NEXT250-V25-122](../research/t20-v6-20261012/sources/96eb9b301e181b3b94cab0b1f86b8f12d4bc3c3e10b9c715c2eab096a6bcb8e5/SerialCertListImageRule.lean#L9-L28) [NEXT250-V25-123](../research/t20-v6-20261012/sources/96f12086107c3a32ccce4e1ead8f6dbfa91aef6e8d8e33275f4c8e67bf6716cf/ControlsStackProbe.lean#L10-L33) [NEXT250-V25-123](../research/t20-v6-20261012/sources/96f12086107c3a32ccce4e1ead8f6dbfa91aef6e8d8e33275f4c8e67bf6716cf/ControlsStackProbe.lean#L74-L94) [NEXT250-V25-123](../research/t20-v6-20261012/sources/96f12086107c3a32ccce4e1ead8f6dbfa91aef6e8d8e33275f4c8e67bf6716cf/ControlsStackProbe.lean#L96-L166) [NEXT250-V25-123](../research/t20-v6-20261012/sources/96f12086107c3a32ccce4e1ead8f6dbfa91aef6e8d8e33275f4c8e67bf6716cf/ControlsStackProbe.lean#L168-L269)

The descriptor interpreter makes those grammar obligations explicit. Each field records its external-leaf wrapper flag and intended syntax sort; localShape checks tag range and exact repacking, while localChildren separately extracts the sort/code dependencies. Packing, field extraction, reconstruction and both local functions are stated primitive recursive for parameterized finite descriptions. The Claim image theorem supplies a further exact equivalence on every natural c: c encodes one of ctxJ, formJ, hasJ, ctxE, formE or hasE precisely when its claim descriptor has local shape and every listed child is CertCanonical. Its reverse proof reconstructs the six constructors tag by tag. Neither the local operations nor this grammatical image equivalence prove the represented judgments, acceptance of a derivation tree or the additional strict-child-descent obligations of the generic evaluator. All statements retain their imported grammar and encoding dependencies. [SUB250-R81-172](../research/t20-v6-20261012/sources/6ee7c95c6b686ad0c03f12ca431a781ffc3059b44b4d6a1ab764c650d7770915/ConstructorDescriptors.lean#L7-L89) [SUB250-R81-222](../research/t20-v6-20261012/sources/79b4b843ec16befc677a1dec59251a5db1720a169a858472c30f317dd63ff0ad/ClaimImageRule.lean#L9-L49)

The generic sorted-code evaluator supplies a separate recursion contract. At a sort/code pair it tests local shape and every listed child, returning false if any child code is not strictly smaller. Its primitive-recursion proof assumes primitive-recursive shape and child-list functions; although recursion uses the filtered smaller-child list, the driver also checks the bounds of every original child, so a nondecreasing dependency is not silently discarded. Exactness for a predicate P additionally requires a local generation equivalence and strict descent for every child of every locally shaped parent. The displayed proof is generic, not four supplied grammar instantiations or a source-judgement checker. The companion PolyCert and LookupCert bounds have a narrower premise: the parent must already be an actual encoding of the respective certificate. Those image-restricted bounds do not alone discharge the evaluator’s stronger local-shape premise or establish truth of the encoded conversion or lookup judgement. These are dependency-relative source proofs on natural codes, without a new source Primcodable assumption or received compiler result. [SUB250-B25-067](../research/t20-v6-20261012/sources/5b23b70952c9d85cca0f75fcaed82b3dcd141bd620e5cad831b1425a622c1fc3/ExactSyntaxValidity.lean#L10-L104) [SUB250-B25-063](../research/t20-v6-20261012/sources/5a75294d2d4b83cb8059b08f88fe8f17beceae509f01e60524574ed5f5ac93a0/PolyCertBounds.lean#L9-L16) [SUB250-B25-065](../research/t20-v6-20261012/sources/5b13972e05bafedccb258b6dca7e36420f2d6da2353ab8fa1cf7df6dbf59c1c2/LookupCertBounds.lean#L9-L16)

GrammarImage supplies an alternative exactness argument whose child-descent premise is required only for genuine P objects. The evaluator still tests strict descent on every child of arbitrary input; in the acceptance direction that runtime condition supplies the induction bound, while in the reverse direction P supplies it. Applying the canonical reconstruction rule and image-specific bounds therefore gives valid(s,c)=true exactly when c encodes a Term, TypeCode, Poly or Ty of the requested sort. A separate primitive-recursive checkTyScope computes the actual TyScoped predicate on encoded types: Pi and Sigma increase term scope in their codomains, All retains it, and identity checks both polynomial endpoints. This latter agreement is restricted to genuine type encodings and is not an all-natural grammar-validity or typing test. Both bodies retain their imported evaluator, grammar and coding dependencies; no compilation is newly established. [NEXT250-F25-004](../research/t20-v6-20261012/sources/7eacd15ff1794e50b2b058150f85ad3b32d0a79340bb1171972daace810293cf/GrammarImage.lean#L28-L89) [NEXT250-F25-002](../research/t20-v6-20261012/sources/7e4a33b9209b112457858b37c5c23a307c3540fdad0be26e804adc9405dbe53c/TypeScope.lean#L7-L84)

ScopeControls makes the same distinction concrete for polynomials: checkScope 1 0 returns true, but its structural case analysis states that no polynomial has natural encoding zero. The scope routine can thus accept a natural outside the syntax image while still being exact on actual polynomial encodings. Its ordinary in-range and out-of-range variable examples concern scope only. This is why a separately justified grammar-validity gate must precede any inference that a scoped natural denotes syntax; it is not a refutation of encoded-input scope exactness or evidence that the examples were executed. [A750-T50-136](../research/t20-v6-20261012/sources/c74e382a7d9c538168710a6cccaf9e4be602d29ef28d0aea7b3046eaac3a7290/ScopeControls.lean#L7-L30)

The polynomial-scope provider gives a separate total natural-code computation. Its variable branch tests the index against the supplied scope, atom branches return true, and application checks both children under explicit strict child-code bounds; unsupported shapes return false. A bounded-table construction proves primitive recursiveness, and the exactness theorem identifies the result with Scoped on actual encoded polynomials. This supplies the term-scope component used inside type checks without conflating it with the all-natural grammatical image test. In particular, exactness on encode(p) is not type formation, certificate validity or derivability, and the source retains its numerical coding and recursion dependencies without a new run. [AFTER750-F50-240](../research/t20-v6-20261012/sources/dc345bc6302875f4ec6fc58ca211bc6f70f59d76ff31f022c45380323002cd9e/CodedScope.lean#L8-L142)

The concrete four-sort computability attempt supplies the primitive-recursive shape and child-list functions needed by that evaluator, dispatching among Term, TypeCode, Poly and Ty and then deriving Primrec₂ valid. Its Ty child list keeps the carrier type and the two polynomial endpoints of identity in their respective sorts. This is a concrete primitive-recursion instantiation, not an additional all-natural image-exactness proof. A separate Claim bound proves strict descent of every listed descriptor child only when the parent already encodes an actual Claim; it does not strengthen that premise to arbitrary locally shaped input or prove the represented judgment. Both constructions retain their imported evaluator, grammar and field-bound interfaces, without newly established compilation. [NEXT250-X25-127](../research/t20-v6-20261012/sources/97d40bcde0b2ef129a36c095eba68db12788e5a44b488230c5cd0b62eda688d8/ComputabilityAttempt01.lean#L7-L74) [NEXT250-X25-127](../research/t20-v6-20261012/sources/97d40bcde0b2ef129a36c095eba68db12788e5a44b488230c5cd0b62eda688d8/ComputabilityAttempt01.lean#L76-L120) [NEXT250-X25-138](../research/t20-v6-20261012/sources/997a7c294b896aef73d504541f74887f5f5e7a17031490ad5bebd028b795382d/ClaimBounds.lean#L9-L16)

The fifteen-sort CertificateImage assembly uses the image-restricted exactness interface explicitly. Its canonical predicate excludes sort indices at least 15; the admitted sorts are Term, TypeCode, Poly, Ty, Nat, Tel, StepCert, RedCert, FiniteCert, PolyCert, LookupCert, Claim, Rule, SerialCert and SerialCertList, in that order. The local canonical equivalence dispatches to each sort’s grammar rule, and its strict-child bound assumes an already canonical parent. Passing those two statements to the imported evaluate_exact_of_image yields certValid(s,c)=true exactly when (s,c) is canonical, with a separate encoded-image corollary for each of the fifteen sorts. This assembles an all-natural syntax-image gate from the explicitly named grammar and bound dependencies; it neither proves the encoded judgment nor strengthens image-restricted descent to descent from local shape alone. The construction does not give fresh verification of those imports or of the evaluator. [NEXT250-E25-195](../research/t20-v6-20261012/sources/a46300dc9cc1c253afab6f14d2174cd0430bdb57d58d2035b8df23bf5d34e531/CertificateImage.lean#L17-L67) [NEXT250-E25-195](../research/t20-v6-20261012/sources/a46300dc9cc1c253afab6f14d2174cd0430bdb57d58d2035b8df23bf5d34e531/CertificateImage.lean#L69-L101) [NEXT250-E25-195](../research/t20-v6-20261012/sources/a46300dc9cc1c253afab6f14d2174cd0430bdb57d58d2035b8df23bf5d34e531/CertificateImage.lean#L103-L146)

Every validation step either descends into a proper certificate subtree or computes a terminating syntax operation. Induction on accepted trees reconstructs genuine judgments; induction on derivations produces such finite trees, including the finite import's explicitly enumerated image indices. This proves decidability of supplied-certificate checking and completeness of the finite certificate format for the specified judgments. Enumerating finite strings by length, parsing and checking each, then emitting accepted conclusions enumerates every derivable judgment. Searching that stream for a fixed conclusion semidecides derivability; searching for any `Has Γ p A` with the requested Γ and A semidecides inhabitation and returns both p and its tree. Unbounded proof heights, indices and reduction lengths are accommodated by the enumeration. No finite failure cutoff or negative certificate follows. This is written existence of a validator and search procedure, not a new executable implementation or kernel run. [Q250A-010]

The distinct Joint/old-E certificate sources state a six-judgment completeness interface for CtxE, FormE, HasE, CtxJ, FormJ and HasJ. Their authored mutual inductions preserve ordered premises, enumerate the finite-import formation family and consume separate lookup, finite-typing and polynomial-conversion witnesses. The Joint cases also retain dependent sum elimination and natural induction. This is not the earlier eighteen-rule judgment or a semantic completeness claim. A separate canonical-code checker gates claim/certificate codes with validity tags11/13, traverses list heads and tails together, and supplies primitive-recursion and encoded-image correspondence proofs. Its SerialCert format is not identified here with DerivationCertificate without the imported serialization bridge. Neither these bodies nor their requested axiom listings supply a fresh compilation, arbitrary off-image decoder equivalence or a terminating negative search. [baseline141 source 2](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/00a1b081562fc33f99a78dff001f7040e706032659a632932049d566e84107c8/CertificateCompleteness.lean) [baseline141 source 9](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/017c8616c1d18c9cdf651680ed53a7d9616d28bf7f488cc83483fad7fa52de8a/CanonicalCertificateCode.lean)

The generic CertificateFramework isolates the soundness obligation behind that interface. At every node it checks the side Boolean, exact ordered equality of child conclusions with the rule premises, and recursive acceptance of every child; checkRoot additionally compares the actual conclusion with the requested claim. Induction transports a supplied localSound premise to accepted-root truth. Conversely, accepted certificates for a rule’s premises can be assembled into a certificate for its conclusion when its side condition holds. The framework does not itself prove localSound for arbitrary rule data or decide negative derivability, and its six imported claim denotations are not new semantics for the current calculus. [NEXT-CERT8-091](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2e13df720328457835592a46b5176ee939cd6052b03a98fda9311be481ff2e85/CertificateFramework.lean)

The concrete CertificateRules body supplies the local soundness argument required by that framework for 63 Joint and actual-E rule payloads. Context, formation and typing premises are stored separately from finite lookup, finite-typing and polynomial-conversion certificates; their auxiliary checkers supply the corresponding side-condition evidence. Finite import requires the support bound and every formation in the supplied finite image list, followed by formation of the substituted result. Pi introduction retains abstracted-term scope, conversion retains target scope, and the extensionality cases retain their endpoint, witness and type-scope premises. The two Joint-only rules retain a six-premise dependent-sum branch interface and a four-premise natural-induction interface, without adding their constructors to E. Case analysis passes the ordered semantic premises and checked side evidence to the respective source constructor; the resulting Rule.sound is then passed to checkRoot_sound. This is a concrete source-relative soundness provider, distinct from rule-image recognition, premise/conclusion encoding and completeness. Its opening assertion of kernel checking and final axiom-print requests are not newly received execution evidence. [NEXT250-E25-176](../research/t20-v6-20261012/sources/a1b58e5bf5c6337b41a50447784719d721ad42509d439d89f126990d8496e886/CertificateRules.lean#L11-L74) [NEXT250-E25-176](../research/t20-v6-20261012/sources/a1b58e5bf5c6337b41a50447784719d721ad42509d439d89f126990d8496e886/CertificateRules.lean#L141-L175) [NEXT250-E25-176](../research/t20-v6-20261012/sources/a1b58e5bf5c6337b41a50447784719d721ad42509d439d89f126990d8496e886/CertificateRules.lean#L185-L204) [NEXT250-E25-176](../research/t20-v6-20261012/sources/a1b58e5bf5c6337b41a50447784719d721ad42509d439d89f126990d8496e886/CertificateRules.lean#L206-L272) [NEXT250-E25-176](../research/t20-v6-20261012/sources/a1b58e5bf5c6337b41a50447784719d721ad42509d439d89f126990d8496e886/CertificateRules.lean#L333-L359) [NEXT250-E25-176](../research/t20-v6-20261012/sources/a1b58e5bf5c6337b41a50447784719d721ad42509d439d89f126990d8496e886/CertificateRules.lean#L380-L449) [NEXT250-E25-176](../research/t20-v6-20261012/sources/a1b58e5bf5c6337b41a50447784719d721ad42509d439d89f126990d8496e886/CertificateRules.lean#L494-L617)

The numerical SidePrefix is explicitly smaller than that full rule system. It supplies16 Joint-side functions: three context, eight formation and five typing branches. Fifteen are constantly true; the variable branch instead calls checkLookupCode on fields3,0,2,1. Each displayed branch has a primitive-recursion proof and agreement with checkSide on the encoding of its matching actual Rule constructor. This prefix supplies neither a complete63-tag side dispatcher nor validity of arbitrary fields, recursive premises or conclusions. In particular, constant true leaves all separately stored formation and typing premises intact. The exactness proofs depend on imported slot/encoding and auxiliary-checker equations and are not received execution results. [L34-133](../research/t20-v6-20261012/sources/ffac9bc3f15916cb1a91a152f0cb490ae29956d5ec423bb99f7ab9ec92147fa2/SidePrefix.lean#L13-L143) [L34-133](../research/t20-v6-20261012/sources/ffac9bc3f15916cb1a91a152f0cb490ae29956d5ec423bb99f7ab9ec92147fa2/SidePrefix.lean#L145-L187)

AuxiliaryCertificates makes five of those side-condition formats explicit: finite trees for Step, Red, FiniteDerives, PolyConvPlus and telescope Lookup. Their Boolean checks retain the requested endpoints, ordered transitivity middles and recursively supplied evidence; lookup also retains the weakening of the type returned from the tail. Separate structural inductions supply accepted-check soundness and a certificate for every derivation of each relation. The polynomial certificate has reflexivity, symmetry, transitivity, application congruence, I/K/S equations and the atom/application bridge; no semantic function or proof object is stored in its data. These are source-relative soundness and completeness statements for supplied finite certificates. They do not decide whether an arbitrary judgment has a certificate, validate an arbitrary natural code or establish a newly observed kernel run. [A750-T50-104](../research/t20-v6-20261012/sources/c2c3ebad5fdb7040827f71d4f007bfad410b91188c06da553227a0df7ebc65c5/AuxiliaryCertificates.lean#L10-L79) [A750-T50-104](../research/t20-v6-20261012/sources/c2c3ebad5fdb7040827f71d4f007bfad410b91188c06da553227a0df7ebc65c5/AuxiliaryCertificates.lean#L82-L145) [A750-T50-104](../research/t20-v6-20261012/sources/c2c3ebad5fdb7040827f71d4f007bfad410b91188c06da553227a0df7ebc65c5/AuxiliaryCertificates.lean#L147-L250)

The serialized checker supplies a specific ordered-tree bridge: serialCheck tests the node's side Boolean and requested conclusion, while serialCheckList consumes exactly one child for each premise and rejects either list-length mismatch. Mutual induction identifies these checks with checking fromSerial and its ordered child list. Soundness and completeness then transfer through the imported check_sound, complete and fromSerial/toSerial equations. This is an explicit serialization interface relative to those imports, not verification of arbitrary numeric encodings, a new semantic completeness theorem, or termination of negative proof search. [SUB250-U25-099](../research/t20-v6-20261012/sources/60b5ca1546ac3eef0bf1ba9b7e30ffc4ad5977bc4d2e01d0d4c579aa39123789/SerialCertificateCheck.lean#L7-L51)

The distinct SerializedCertificateCodec body supplies the serialization equations themselves. Mutually recursive tree and list conversions are inverse in both directions. After encoding the serial tree as a natural and partially decoding it, decodeCertificate(encodeCertificate c)=some c; malformed decoding makes checkCode return false. Accepted numeric or serial checks imply the requested derivation, while completeness gives existence of a suitable numeric or serial certificate for every derivation. These transfers remain relative to the imported certificate checker and its soundness/completeness. The round trip is for codes produced by the encoder, not an assertion that every natural is a valid or canonical certificate, and the existence equivalences provide neither terminating negative proof search nor a separately verified machine-model implementation. [A750-T50-105](../research/t20-v6-20261012/sources/c2f656e0a330056b4da5834154a18ed7cc29bd6e30c836953fe59016dac74593/SerializedCertificateCodec.lean#L10-L87) [A750-T50-105](../research/t20-v6-20261012/sources/c2f656e0a330056b4da5834154a18ed7cc29bd6e30c836953fe59016dac74593/SerializedCertificateCodec.lean#L90-L144)

The canonical source-search controls exercise the validity gate separately from ordered proof checking. They accept the empty Joint context and its well-formed extension, but reject missing or extra premises, a swap of distinct premise claims, a wrong requested root and a false conversion witness. Every supplied finite-image formation obligation remains, including an unused image. Claim code zero rejects every certificate, certificate code zero rejects every claim, and proof search on claim zero has no domain witness. The companion validity wrapper retains local shape together with strict descent and recursive validity of every listed child; its image-membership examples do not establish the judgments encoded. These are dependency-relative written controls, and the requested evaluations neither execute unbounded search nor make finite search failure a negative derivability certificate. [SUB250-FINAL28-173](../research/t20-v6-20261012/sources/6eec605dd7cc2eb4ee5fdae6a4f058ba0d31bb98a84f6e920049bf350801a39b/SourceSearchControls.lean#L8-L93) [SUB250-FINAL28-193](../research/t20-v6-20261012/sources/728265b9b5dc3d94bb2c2e1addda5a69c32168ae5baa2fa81106b3e7a1b88941/ControlsWrapperProbe.lean#L10-L66)

The independent actual-source controls extend the canonical-search boundary beyond the special zero codes. Acceptance implies actual encoded Claim and SerialCert inputs, so every noncanonical claim or certificate is rejected, and malformed claim/type codes have no proof/inhabitation search domain. Returned proof certificates are sound and least among accepted certificate codes; inhabitant search instead returns the least accepted natural pair, whose type, polynomial and serial-certificate components are all canonical. These least-code results are not shortest-proof or semantic-minimality claims. Ordered checking preserves list arity, rejects either exhaustion mismatch and rejects swapping distinct Joint/E empty-context claims, while swapping certificates for the same repeated claim is harmless. The finite-import control accepts all supplied image formations but rejects omission of an unused Bottom image. A literal raw I inhabitant supplies a positive inhabitation control. These are import-relative declarations plus two small evaluation requests and an axiom/dependency audit program, not executed searches or observed PASS output. [NEXT250-E25-196](../research/t20-v6-20261012/sources/a482c89d7f7114922fe05059bfe375e368a44769d4c6ad020a8d6559880b813d/IndependentControls.lean#L8-L105) [NEXT250-E25-196](../research/t20-v6-20261012/sources/a482c89d7f7114922fe05059bfe375e368a44769d4c6ad020a8d6559880b813d/IndependentControls.lean#L108-L160) [NEXT250-E25-196](../research/t20-v6-20261012/sources/a482c89d7f7114922fe05059bfe375e368a44769d4c6ad020a8d6559880b813d/IndependentControls.lean#L162-L185)


The auxiliary-code controls exhibit why that canonical gate must remain separate. The deliberately ungated polynomial checker accepts the malformed payload pack 0 [leaf 0] with both endpoint codes zero, while the polynomial syntax-validity test rejects endpoint code zero. Positive encoded controls still accept contextual I reduction, actual type instantiation and weakened telescope lookup; mismatched endpoints, transitivity middles and unweakened lookup reject. The malformed acceptance is a control for the total extension, not a counterexample to the separately gated certificate checker. These are written source proofs, without fresh execution. [NEXT-BOUNDARY12-025](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/20234adacc4d2123f145b27adbdb2d6c1561a07c313d096adf0d99e98bc87634/AuxiliaryControls.lean)

The separate RulePremisesCode source makes ordered premise extraction explicit: a primitive-recursive dispatcher selects among 63 rule tags, and its correspondence theorem states premisesCode(encode r) = r.premises.map encode. Finite-import branches place the actual image-formation list first, followed by the substituted finite-type formation premise. This total extractor is not a validity test: an unrecognized tag returns the empty list, just as the two genuine context-nil rules do, while recognized branches do not themselves validate their fields or auxiliary certificates. Its exactness on encoded rules therefore cannot replace the separate validity and certificate checks. The final axiom-print commands are not received audit results. [NEXT-RULE-PREMISES-135](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/34fcbe0c90f627af0605f769ebe750834b2f1d98d5b8d3e9d38b9437431dbab1/RulePremisesCode.lean#L11-L1405)

The separate DeepRuntimeAttempt controls apply the canonical gate to supplied certificates: they state acceptance of the empty context and its Raw extension, and refusal of missing or extra premises, a swap of distinct premise claims, a wrong root, false conversion and a dropped finite-import image. The finite-import premise list retains the bottom image even when unused by the finite type. No claim is made that swapping interchangeable certificates of the same claim must fail. Separate zero-code validity assertions feed universal refusal statements for malformed claim or certificate zero. These are authored control obligations and evaluation/readback requests, not observed runtime outcomes, an executed unbounded proof search or evidence that every displayed proof compiled. [NEXT-R11-181](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3d50e642fbaf28d707006a749c1dafa9d1be8bd96d6d07257ed9c97be1e03083/DeepRuntimeAttempt.lean#L8-L91)

**Bridge-only opaque targets.** For arbitrary closed raw terms t,u, construct $`R(t,u)=\mathrm{Id}_{\mathrm{Raw}}(\mathrm{atom}(t),\mathrm{atom}(u))`$. Raw formation, both endpoint typings and scope-zero certificates are effective for every such pair. Section 10.7 therefore gives

```math
\mathrm{Conv}(t,u)
\iff []\vdash_+\mathrm{atom}(I):R(t,u)
\iff \exists p\;[]\vdash_+p:R(t,u).
```

The reverse implication uses the full eighteen-rule saturated soundness theorem, not inversion of the last identity-introduction rule. This is why §10.5's earlier residual stopping point is historical rather than the present conclusion. The older F/G semantic inhabitant of the polymorphic-I/SKK identity and the now proved syntactic noninhabitation coexist: that semantic interpretation is sound but not complete for this syntactic problem. [Q250A-008] [Q250A-011] [Q250A-010]

**Unchanged Has has a different exact reduction.** Define Ex on raw syntax by exposing applications: primitive raw constants become their polynomial atoms, and $`\mathrm{Ex}(ts)=\mathrm{app}(\mathrm{Ex}(t),\mathrm{Ex}(s))`$. Every raw contraction translates to an old polynomial contraction, and the left/right congruences, symmetry and transitivity preserve the translation. Conversely evaluation of an old polynomial-conversion proof at the empty environment gives raw conversion. Hence $`\mathrm{Conv}(t,u)\iff\mathrm{PolyConv}_0(\mathrm{Ex}(t),\mathrm{Ex}(u))`$. These exposed endpoints have old Raw typings by structural induction. The all-rule raw-conversion interpretation gives the converse from **any** old inhabitant, while identity introduction gives the forward direction. Thus the same three-way equivalence holds for unchanged Has with $`R_0(t,u)=\mathrm{Id}_{\mathrm{Raw}}(\mathrm{Ex}(t),\mathrm{Ex}(u))`$. It is not a converse for old opaque endpoints. Neither reduction changes the current grammar or adopts the hypothetical bridge. [Q250A-010]

**Undecidability premise and its exact transfer.** The inherited combinatory representation theorem for partial recursive functions supplies a closed pure I/K/S representative F of a partial characteristic function h with h(n)=0 exactly on halting inputs. With Church numerals, halting implies $`F N_n\simeq N_0`$; otherwise the represented computation has no weak normal form. Confluence makes conversion to the normal numeral $`N_0=KI`$ impossible in the latter case. This is compatible weak I/K/S conversion, not extensional equality or an asserted equivalence with lambda-beta conversion. The inert constants zero and one do not weaken the lower bound: retract them to I in a purported extended conversion proof between pure terms. The substitution preserves each rule and fixes the pure endpoints. The source's cited representation result remains an imported theorem, not a new primary-source inspection. [Q250A-010]

Composing this reduction with either exact identity map proves undecidability of general inhabitation and fixed-witness derivability, already on effectively formed closed Raw identity targets with supplied endpoint typings. Both problems remain semidecidable. Decidable finite proof checking, and conversion decisions for the separately controlled finitely typed fragment, are compatible with that limit. The written classification adds no claim of completeness for the original F/G semantics, a negative search cutoff, or a new adopted calculus. [Q250A-010]

#### Retained proof interfaces keep their different normalization and identity contracts

The predecessor sources explain why these boundaries cannot be collapsed into one certification claim. `InternalPolymorphism` interprets types by raw-conversion-stable codes and represents a uniform section by one literal tracker; quantification over all codes includes self-instances but does not provide arbitrary ambient functions as programs. `BoundaryResults` gives uniform left/right behavior only with its marker-free hypothesis and distinguishes the weak three-property singleton counterexample from the richer no-full-sections obstruction. `Effects` proves membership of every positive-support outcome and existence of an outcome for its finite derivations; a quantitative mass law or coupling theorem is not established by that support theorem. These retained declarations supply mathematical interfaces, not a license to replace them with a prose assertion of parametricity. [Q250A-018] [Q250A-015] [Q250A-016]

The finite-effect extension makes the support statement relational: every Outcome of an EffectDerives term has a finite derivation, hence satisfies the imported relational interpretation, and its diagonal support works for every relation environment. That unverified support file defines no mass. The separate quantitative controls give I and SKK marginal mass 1/2 each; their independent comparison puts mass 1/4 on a raw-unrelated pair, whereas the common-seed coupling puts zero there. This does not require sharing samples between repeated syntax occurrences within one run: applying the mixture to itself still gives the mixed application mass 1/4. Other written controls retain exact zero/full branch weights, equality of the 2/4 and 1/2 laws, and summation of colliding branches to mass one. These are dependency-relative source statements, not fresh kernel or runtime results. [SUB250-U25-182](../research/t20-v6-20261012/sources/707ac140dc356f27647a416b64f483bf3c814e14b1b025b87cf69b69752051a0/P01FiniteEffects.lean#L1-L45) [SUB250-U25-195](../research/t20-v6-20261012/sources/72aa975f546c7de1d02975f9c370b3d7b4497abdc92f9e06f391716ea674602b/IndependentEffectControls-attempt3.lean#L9-L91)

Existence of a suitable coupling separately for each relation does not supply one coupling suitable for every relation. Let both marginals be the fair law on {0,1}. The diagonal relation {(0,0),(1,1)} admits the coupling placing mass 1/2 at each diagonal point. The antidiagonal relation {(0,1),(1,0)} likewise admits mass 1/2 at each of its two points. Their intersection is empty, so no probability coupling can be supported on both relations at once. Thus the quantifiers “for every relation there exists a coupling” and “there exists a coupling valid for every relation” are different, even for these fixed equal marginals. This elementary control complements the preceding independent-versus-common-seed distinction; it does not refute a theorem that already provides one uniform diagonal witness on an admitted relational family. The source’s imported probe implementation was not received or run. [AFTER2634-SEVENTH25-169](../research/t20-v6-20261012/sources/dea5bc8fe7521661d6dcf859f7a5c41c99db8c429c71cc6cb98e6095b9abb938/test_probes.py#L70-L76)

The successor audit describes a constructive quantitative interface beyond the earlier support-only result. Each finite fixed-weight expression has a nonempty finite product seed space, with mixture coordinates sampled at their exact rational weights and separate child coordinates for application. Pushing uniform seed mass to outputs sums collisions and gives normalized laws; pushing the same seed to two valuations gives a nonnegative joint matrix with those exact marginals, chosen before quantifying over the relation environment. For open expressions its relation-support conclusion retains ValRelated; the embedded original closed-language theorem needs no valuation premise and has diagonal raw outputs. A separate open witness is genuinely nondiagonal: its left law puts mass one on I, its right law gives I and SKK mass one-half each, and the joint mass at (I,SKK) is one-half, with the input valuations related at polymorphic identity for every relation environment. The audit reports an isolated rebuild and declaration/axiom checks, not performed here. This is one finite expression under two valuations, not arbitrary program pairs, value-dependent bind, unrestricted recursion, independent cross-run sampling or a universal coupling quantifier exchange. [AFTER3384-SECOND25-030](../research/t20-v6-20261012/sources/06b514e04dc36b0d6796f8baf11c8e017e938569ae76fba11142d0a58d98b755/REPORT.md#L36-L58) [AFTER3384-SECOND25-030](../research/t20-v6-20261012/sources/06b514e04dc36b0d6796f8baf11c8e017e938569ae76fba11142d0a58d98b755/REPORT.md#L60-L76)

Raw-conversion-stable membership is not strong normalization: a discarded divergent argument remains accepted in every inhabited stable code. The direct reducibility-candidate proof instead uses strongly normalizing candidates, neutral expansion and careful S-contraction duplication to prove strong normalization of all seven `FiniteDerives` rules. Its bottom-tag candidate is a normalization candidate, not the empty canonical semantic code. Compatible-reduction confluence supplies joinability and uniqueness of normal forms; the separate Ω shape argument proves that **every** reduct remains reducible, rather than merely displaying one cycle. Together these prove no finitely typed representative converts to Ω. The alternative System F route supplies capture-avoiding lambda substitution, source typing preservation, subject reduction and positive-length simulation of each I/K/S step; its generic normalization reflection requires a nonempty simulated reduction, and the retained translation does not itself prove System F strong normalization. These are complementary explicit proof dependencies, not interchangeable assumptions. [Q250A-019] [Q250A-020] [Q250A-023] [Q250A-035] [Q250A-033] [Q250A-040] [Q250A-041] [Q250A-039] [Q250A-042]

At the dependent interface, forgetting a PER to its domain preserves less than the relation: raw identity is exact for its raw-conversion carrier, while an arbitrary PER identity may relate I and SKK without raw conversion; arrow projection has only the stated direction. The finite witnesses and negative controls make those failures explicit. The recursive model's independently related environments, endpoint restrictions and diagonal identity extension give the positive finite fundamental theorem; they do not turn arbitrary old unary membership into relational validity. The polynomial compiler's literal abstraction-substitution naturality preserves its K-priority treatment of absent variables, not arbitrary abstraction congruence or eta. Curry parametricity respects the shifted context at universal introduction and application-beta behavior, not equality of arbitrary unapplied raw labels. [Q250A-021] [Q250A-034] [Q250A-026] [Q250A-038] [Q250A-037] [Q250A-025]

The carrier controls isolate a further dependent-family premise. Coherence along an empty domain PER is vacuous, yet an inspected fibre can distinguish convertible raw terms; PER-relative coherence alone therefore does not supply global conversion coherence for the projected unary family. Their anchored identity family is nonconstant: it accepts the identity evidence at index I and accepts none at SKK. The displayed source pair is admitted into the canonical dependent sum with its unchanged evaluated polynomial, whereas pair(SKK,I) is rejected at that same family. Empty fibres exclude every product or sum inhabitant at the raw-conversion domain, and the PER sum projection still requires an actually represented pair. These source-relative controls refine the projection boundary above; they neither identify equal unary carriers with equal PERs nor validate the imported fundamental and admission theorems anew. [SUB250-F28-105](../research/t20-v6-20261012/sources/615a28d1dfdb0d943031a1efaea3872836d33ad23978e9b4cdd4cd41d7d4ec80/ScopeControls.lean#L48-L101)

Nonempty dependent fibres still need not form a constant family. The independent control uses the arrow from an anchored identity to itself: I inhabits it at every index, while K SKK is accepted at the SKK index and rejected at I. Its dependent product is nevertheless explicitly typed and inhabited. Additional exact substitutions keep both free term and type coordinates safe under nested binders, and a J example varies both endpoint and proof coordinates. A mixed All body contains genuine index dependence and a bound parameter yet admits its stated self-instance. These examples do not license a free raw variable at an arbitrary parameter or unrestricted transport of raw identity along every heterogeneous Link. Their nonemptiness and separation rely on imported unary soundness and raw I/SKK separation, without new compilation or identification of the different grammars. [A750-S50-093](../research/t20-v6-20261012/sources/c19e5d1a8134f9f76b5b3d4de44c6cd31caa899359f7c15e553f66f655d16208/IndependentDependentControls.lean#L6-L50) [A750-S50-093](../research/t20-v6-20261012/sources/c19e5d1a8134f9f76b5b3d4de44c6cd31caa899359f7c15e553f66f655d16208/IndependentDependentControls.lean#L52-L80) [A750-S50-093](../research/t20-v6-20261012/sources/c19e5d1a8134f9f76b5b3d4de44c6cd31caa899359f7c15e553f66f655d16208/IndependentDependentControls.lean#L83-L101)

The intrinsic dependent core represents terms by finite polynomial trackers plus their validity, with coherent PER families for dependent products and sums and an extra parametric-family obligation at universal formation/introduction. The raw-index grammar has its own fundamental theorem; its two-sort substitution identities freeze the original valuation of type images across term binders. The representation map into the repaired core preserves exact code and the candidate Pi/Sigma/identity/All operations, not an unproved identification with every canonical unary carrier. The contextual J proof uses both the endpoint and proof coordinates; a motive branching on literal proof syntax fails coherence, whereas the supplied reflexivity, pair and J examples witness nonempty genuine dependent constructions. These positive constructions and their controls remain attached to their respective grammars. [Q250A-027] [Q250A-036] [Q250A-028] [Q250A-029] [Q250A-031] [Q250A-030] [Q250A-024] [Q250A-032]

The tracked contextual core additionally separates exact substitution equality from semantic relatedness. SubEq requires equal valuation maps and equal polynomial trackers, whereas SubRel compares the images of related valuations in the target context relation. Code-exact equality implies SubRel, and SubRel is preserved by composition; coherence then identifies pulled-back fibers and term validity relates the substituted trackers even when the substitutions are only semantically related. Identity and associativity are retained at the stronger code-exact level. This does not turn arbitrary ambient sections into terms, infer raw conversion from product equality, or discharge the explicit uniformity premise of universal introduction. The selected source labels its authored attempt uncompiled, and no execution is supplied here. [NEXT-D8-72](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2955aa515e77baf2f5e2de8341819891177a5d3b00b88092be328738858c41ac/P01DependentCore.lean#L56-L166) [NEXT-D8-72](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2955aa515e77baf2f5e2de8341819891177a5d3b00b88092be328738858c41ac/P01DependentCore.lean#L374-L413)

Finally, the retained finite bridge translates each finite derivation to semantic validity, but its executable convenience certificate uses an explicitly restricted strategy and scope test. The certificate module adds addressed compatible reduction traces, join certificates and envelopes binding a finite proof to a literal term and type. Its dependent envelope binds an actual represented term and exact code; its finite TypeCode image does not thereby acquire every dependent sum or identity type. No JSON parser refinement, complete target recognizer or fresh kernel execution follows. This is why the complete finite-tree *mathematical* presentation above is stated separately from those useful narrower implementations, and why their Lean sources and imported modules remain retained dependencies. [Q250A-017] [Q250A-022]

A separate two-sort Python frontend makes the gap between source acceptance and finite export explicit. It freezes only lists, tuples, strings and exact integer leaves, rejects cycles and excessive syntax, and checks term and type binders separately; the J motive crosses two term binders. Conversion is supplied by two addressed reduction traces ending at the same literal expression, rather than by an oracle for general equality. Its accepted dependent syntax includes Sigma and identity types, but the unchanged finite Cert vocabulary does not. Export therefore freshly checks the accepted term and type, refuses an open context, checks the restricted target type, and requires the emitted certificate's erased term to equal the literal SKI compilation. The accompanying tests request both an accepted dependent identity that cannot be exported and refusal of a forged accepted Result. Every returned export record leaves kernel_verified false. These are distinct implemented gates and unexecuted test obligations, not a proof that Python refines the kernel, that resource refusal establishes inequivalence, or that every accepted source term has an export. The test file's import name does not by itself identify its actual checker dependency. [G24–25-063](../research/t20-v6-20261012/sources/096218de3e630030fcac53a7b8e02aa21be121a75a0a0a003d72a36c45fdaa85/checker.py#L293-L307) [G24–25-063](../research/t20-v6-20261012/sources/096218de3e630030fcac53a7b8e02aa21be121a75a0a0a003d72a36c45fdaa85/checker.py#L342-L430) [G24–25-180](../research/t20-v6-20261012/sources/1b35af2893c77e3b0f626cf9b3a3b01003de9338efb7aba31915b69e73431f89/test_checker.py#L114-L158)

#### Native-tree decoding, independent checking and partial export

The retained native model adds a concrete positive bridge without claiming verification of a host parser. `SourceProof` has seven rules: I, K, S, application, universal introduction/elimination and explicit reduction. Its source evaluator independently checks scope, matching application types, capture-avoiding instantiation and every supplied head-step transition; a trace must be nonempty and begin at the checked term. Separate equations identify source scope, substitution and head stepping with the inherited mathematical operations. Induction on successful source checking then establishes target `check` acceptance of the erased certificate with the same term and type, and hence inherited semantic acceptance. This is a forward constructor-erasure theorem. A wrong-start singleton trace is refused by the source checker but erases to an accepted certificate, explicitly disproving the converse. [F109-N053] [F109-N062] [F109-N058] [F109-N055] [F109-N061] [F109-N056]

The resource layer retains that direction: resource acceptance refines semantic-core acceptance, so a semantic refusal cannot become success. Its transport shape counts containers, keys, tags and integer leaves, unfolds occurrences and requires at most 20,000 nodes, height 100 and natural indices below 2^256. The initial type-depth guard is 100; successful subtree outputs are charged by their term/type node sizes against an aggregate 2,000,000 limit. Explicit native-tree encoding preserves all three shape components, and successful source checking bounds proof visits by 20,000 and proof-call height by 100. These are structural guards, not bounds on host allocation, elapsed time or textual input bytes. [F109-N061] [F109-N059] [F109-N060] [F109-N052]

The concrete work controls distinguish the returned term from the expanded types being charged. Write A_d for d universal constructors around bottom and B_0(X)=X, B_(n+1)(X)=B_n(X)→B_n(X). Work007 states successful sourceRun 0 equalities for identity at A_d with charges 368, 388, 396 and 400 for d=90, 95, 97 and 98, and at B_n(bottom) with charges 2048, 4096, 8192 and 16384 for n=8, 9, 10 and 11; each returns I at the corresponding identity-arrow type. For n=3, 4 and 5, allE(allI(i(B_n(var0))), B_n(bottom)) instead returns I at B_(2n+1)(bottom), with charges 674, 2370 and 8834. These fixed substitution controls display type expansion while retaining the same returned term. They supply neither an all-depth cost theorem, a sharp refusal threshold nor a host-resource estimate. All eleven authored equations depend on SourceResources and end with by decide; maxRecDepth 200000 and maxHeartbeats 0 are elaboration settings, not received compilation or audit evidence. [SUB250-W007-198](../research/t20-v6-20261012/sources/72d80992489847547c09d3bf10eb0683a2b159f68de09173a6d7b5fb40e33c03/Work007.lean#L1-L15)

The separate constructor-erasure review reports an accepted pair with the same exact erased certificate but different source work. At variable type zero, the identity result contributes arrow shape 8 and term shape 2, giving charge 10. Universal introduction adds 12, giving 22; wrapping that accepted source proof in a valid singleton reduction adds another 12, giving 34. The singleton trace has no transitions, so erasure adds no certificate steps, although exporter construction counts the extra wrapper and changes its constructor count from 2 to 3. The displayed arithmetic and equality-substitution argument are transparent: no function of that one certificate can recover both exact source charges. Acceptance, exact certificate equality and the reported trust-zero theorem replay remain the review's evidence, not fresh checker execution here. This is a concrete instance of the existing fibre criterion, not a new general nonfactorization theorem, a defect in target-only cost, or a host-time estimate. [AFTER3384-SIXTH25-131](../research/t20-v6-20261012/research-v6/root_math/erasure_review/REVIEW.md#L3-L7)

The Cross019 controls add fixed refusal obligations to that resource comparison. With A_d and B_n as above, sourceCheck 0 is written to refuse identity at A_101 and A_110, accept identity at B_n(bottom) for n=8,9,10,11 with result (I,B_(n+1)(bottom)), and refuse n=12. The substitutions allE(allI(i(B_n(var0))),B_n(bottom)) are written to return (I,B_(2n+1)(bottom)) for n=3,4,5 and to refuse n=6,7. Every one of the twelve examples ends by decide. These are exact finite test obligations relative to SourceResources, not an all-depth threshold theorem or evidence that either implementation was run; the Python accept/refuse labels are comments. The repetitive literal terms were examined through an exactly reconstructing abbreviation, with no imported checker expansion or proof-execution claim. [NEXT250-S25-044](../research/t20-v6-20261012/sources/874c2e88b2c3aba108b699b138af72551bdff372cb3e4dd6a1d181d39bbafcc7/Cross019.lean#L1-L28)

The finite Python reference checker makes the placement of one resource guard explicit. In type instantiation it first counts the argument, then charges that count at every substituted occurrence before calling the capture-avoiding shift that constructs its copy. Other visited type nodes are charged separately, and a final structural check remains. This 20,000-node construction budget therefore differs from discovering excessive expansion only after the entire substituted result has been built. It is not a bound on all host allocation: the same body first constructs a head-reduction successor and only then checks its aggregate work and freezes it. Weak-head fuel exhaustion is also reported separately from reaching a normal form. These are local program mechanisms, not a proof of termination, full normalization, universal parser refinement or a common instantaneous snapshot of mutable input. The imported boundary counter and JSON loader were not followed, and no execution is claimed. [AFTER1384-S10-165](../experiments/orthemology-v5/source/reference.py#L85-L117) [AFTER1384-S10-165](../experiments/orthemology-v5/source/reference.py#L120-L157)

`WireValue` distinguishes natural and negative integers, booleans, null, strings, arrays and ordered object-field lists. The decoder uses exact rule-field sets and rejects duplicates; `NativeProofRep` describes the same seven-rule syntax by key permutations, field membership and recursive representation, allowing field order to vary. Successful decoding yields that grammar witness. Canonical roundtrips require sufficient structural fuel, while grammar completeness covers every valid field ordering with sufficient fuel; these imply representation determinism. With a grammar witness and the actual native tree's shape bound, `nativeCheck` equals `sourceCheck` on the represented proof, including semantic and resource refusal. Unlike constructor erasure, this bounded representation bridge preserves the entire outcome. The positive native bridge also transfers accepted term/type results and universally refuses duplicate object keys. [F109-N042] [F109-N049] [F109-N047] [F109-N050] [F109-N046] [F109-N048] [F109-N044] [F109-N051] [F109-N041]

Constructor export has a further independent limit. `partialConstructorExport` first checks at depth 0 and then requires expansion work at most 512. Reduction wrappers count an extra source work unit, making that work a conservative bound on emitted certificate nodes. Export success implies accepted target output and at most 512 nodes, but checker acceptance alone does not imply export success: `balancedIdentity 8` has 7,916 transport nodes, is accepted, and incurs 1,022 expansion-work units, so export refuses it. Identifier, row, byte and host guards of a textual exporter remain outside this theorem. [F109-N057]

The selected textual exporter exposes several of those otherwise separate host guards. It requires an exact string identifier beginning with an ASCII letter, followed by at most 79 letters, digits or underscores, and a module collection of one through sixteen exact list/tuple pairs with distinct names. It invokes the imported strict JSON loader and reference checker before emitting syntax. Its certificate budget begins at 512, charges each visited proof constructor and additionally charges every reduction step; both each export and the final module have a 1,048,576-byte UTF-8 ceiling checked after their text is constructed. These byte tests therefore do not bound peak construction memory. The emitted Checked value asks Lean to evaluate check 0, and the erasure and type equations each use decide; semantic acceptance then invokes checked_sound with both equations. The generated module expressly says UNCOMPILED. This body specifies a bounded text-generation interface, not a successful Lean build, a verified Python/JSON-to-Lean refinement, or proof that every checker-accepted input exports within budget. Its same-named imports are not identified with any other retained variant. [AFTER1884-S25-048](../research/t20-v6-20261012/sources/6980b13029b17602c1eb516b8cc6ffa6b750e3e226513ba4fd8b7a52fb65467b/proof_export.py#L1-L12) [AFTER1884-S25-048](../research/t20-v6-20261012/sources/6980b13029b17602c1eb516b8cc6ffa6b750e3e226513ba4fd8b7a52fb65467b/proof_export.py#L26-L76)

The finite controls distinguish grammar failures from semantic failures: reordered fields are accepted; missing, extra and duplicate fields and malformed tags/types/traces are refused; an empty trace successfully decodes yet fails semantic checking. Separate branch and binder-capture fixtures supplement the general proofs. The audit files mainly request declaration and axiom readback, plus example applications of existing theorems; those requests are not obtained audit outputs. This source-level reconciliation performs no Lean execution or external dependency closure, and proves no UTF-8 JSON parser, Python object/protocol behavior, atomic capture of mutable inputs or total textual export. [F109-N045] [F109-N052] [F109-N043] [F109-N054]

The P03 runtime driver specifies a finite comparison rather than a universal parser refinement. Its 188 hash-bound raw JSON cases must match recorded outcomes, with 54 accepts and 134 refusals; accepted outputs are compared after JSON normalization. For ordinary wires it also requires native-object and strict-JSON checking to agree, but duplicate-field wires are deliberately excluded from that duplicate-losing object comparison and must instead refuse. Thus the intended experiment compares different representations under an explicit exception, not every wire with its parsed object. The imported checker, case data and runtime results were not obtained in this reading, so these are authored test obligations rather than observed successes or kernel certification of Python. [AFTER1134-G20-139](../research/t20-v6-20261012/sources/1608e28ca2759d68b734c13f0bc830a3da20c42d0ea2ad57b78adf24c6d419a3/replay_p03_runtime.py#L24-L49)

A separate independent successor audit reports completion of that finite native comparison: all 188 archived cases agreed with exact returned term/type or refusal, comprising 54 accepted and 134 refused cases. The 147 duplicate-free cases additionally agreed with native reference checking; the 41 duplicate-bearing cases were tested through strict raw JSON with duplicate fields retained. The same report records a fresh source rebuild of 24 local P03 modules and type/axiom readback for 30 designated targets. Its grammar theorem allows arbitrary field order and preserves the entire Option outcome, while constructor erasure remains only acceptance-directed and the 512-unit exporter keeps its separate refusal gate. These are attributed historical audit outcomes rather than executions of the supplied driver in this consolidation. They do not verify arbitrary UTF-8/JSON parsing, CPython heaps or races, foreign objects, host failures or the complete textual exporter. [AFTER3384-SECOND25-030](../research/t20-v6-20261012/sources/06b514e04dc36b0d6796f8baf11c8e017e938569ae76fba11142d0a58d98b755/REPORT.md#L13-L33) [AFTER3384-SECOND25-030](../research/t20-v6-20261012/sources/06b514e04dc36b0d6796f8baf11c8e017e938569ae76fba11142d0a58d98b755/REPORT.md#L78-L108)

The bounded correspondence probe uses simultaneous substitution as a distinct oracle for the reference checker's cutoff traversal, and application spines as an oracle for its recursive head-context reduction. Under a universal type binder the substitution fixes index 0 and shifts every substituted free image by one. Its explicit witness instantiates the body ∀.var1 with var0 and returns ∀.var1, not the captured ∀.var0. For I, K and S it contracts the head only when enough arguments are present, then reapplies the remaining spine. The requested comparison covers types of at most five AST nodes with initial variable indices 0,1,2, shift amounts and cutoffs 0 through 3, and application terms of at most seven AST nodes over I,K,S,zero,one. These independent finite representations expose binder and head-reduction mistakes without proving universal Python refinement or kernel correspondence. The imported reference, generated corpus and PASS_FINITE_ONLY output were not executed or received as successful results. [AFTER1884-Q25-081](../research/t20-v6-20261012/sources/6edd51a78bb1309ac14303c58c30937d9ac49374766cd50388bd855cc1e71132/probe_finite_correspondence.py#L11-L87)

The separate owned-value adapter provides a narrower capture mechanism. It copies exact builtin containers into private dictionaries and tuples, rejects cycles, expands shared occurrences separately, and retains only bounded immutable builtin leaves. A successful encoding is explicitly passed through the existing strict decoder again; no decoder guard is relaxed by the wrapper. This owns the resulting transport value, but does not establish a single-instant snapshot of a concurrently changing caller tree: the source permits a bounded mixed-time read transcript or refusal and leaves atomicity to caller cooperation. Its export entry also narrows the input to one through sixteen exact sequence pairs with immutable string/bytes leaves, rather than proving equivalence to an arbitrary iterator interface. The imported boundary checker and exporter remain separate dependencies, host resource failures are not logical refutations, and generated module text is not kernel proof. [AFTER1384-R10-015, lines 1–107]

The separately retained pre-count-capture export variant leaves a specific concurrency gap even within that narrower input domain. It first checks that examples is an exact list or tuple with length between one and sixteen, then obtains count by calling len(examples) again. If a caller grows an exact list between these reads, the second count can exceed sixteen; the loop then attempts that many rows. If it shrinks the list to empty in that interval, the loop can instead produce no rows. The later IndexError handler covers a failed indexed read, not this disagreement between two successful length reads. This hand interleaving concerns the adapter's own admission and capture sequence; the unread downstream exporter might still refuse the captured rows, so no oversized successful export is inferred. It is distinct from the already stated lack of a single-instant snapshot of row contents, and it supplies neither a runtime result nor a replacement implementation. [AFTER2634-EIGHTH25-183](../research/t20-v6-20261012/sources/e01fd0f334f2eba45523f053d44d884d27138436d5c3f07f9fb7f712accc2fd0/safe_frontend_before_count_capture.py#L82-L105)

The distinct bounded-transport body specifies the textual guard left separate above. Its tree walk permits exact builtin containers and leaves, rejects active-path cycles and unpaired surrogates, limits native depth to 100 and visited nodes to 20,000, and permits integers of at most 256 bits. Its JSON loader additionally requires strict UTF-8 bytes of at most 524,288 bytes, rejects duplicate keys and nonintegral numeric forms, and counts container nesting before parsing. Native depth counts a root at zero, whereas JSON counts the root container as one. Accordingly the exporter separately rejects a container at native depth 100, while a scalar leaf at that depth remains admissible. It streams ASCII JSON chunks and checks the accumulating output byte count instead of first allocating the complete oversized serialization. These are distinct input, structural and output guards; they do not prove a total host-memory bound or a single-instant snapshot of caller-owned mutable input. The optional Fraction branch belongs to the tree checker and is not enabled by the JSON entry points. Resource refusal remains operational refusal, not logical falsity, and no checker or transport execution is claimed. [AFTER2134-S25-026](../research/t20-v6-20261012/sources/86794c3b03f26421dd007e0d317930fd57fd27dc042342b56815c8ec561eb7c4/boundaries.py#L1-L100)

The earlier canonical bounded-transport body has a narrower roundtrip contract than the later variant just described. Its native tree walk starts at depth zero and permits a container at depth 100, while its JSON scanner counts the root container as depth one and refuses nesting above 100. Its streaming exporter calls the native tree guard but adds no separate deepest-container check. Consequently a nested-list chain whose deepest empty list is at native depth 100 meets that depth condition yet serializes with 101 container levels, which its loader refuses. This is a direct comparison of the displayed guards, not an executed test or a defect in the distinct later variant. The separate allocation test requests refusal of one oversized payload and a peak below four byte budgets; it supplies neither an observed result nor a universal allocation bound. [0](../experiments/orthemology-v5/source/boundaries.py#L6-L88) [2](../experiments/orthemology-v5/source/tests/test_final_boundaries.py#L7-L19)

The separate refinement-contract suite makes the input/output byte distinction concrete. Its fixture is a list of thirty strings, each containing 4096 copies of é. Compact JSON with literal UTF-8 characters occupies 245,851 bytes; compact all-ASCII JSON using a six-byte \u00e9 escape for each character occupies 737,371 bytes. Thus with a 524,288-byte cap at both interfaces, the first representation fits and the second does not, although they represent the same JSON value. The suite explicitly requests successful decoding followed by output-budget refusal from its unread boundary implementation. This is an authored regression expectation, not a received pass or identification of that import with another retained variant. Its tuple-to-list and key-order example likewise treats canonicalization as a value quotient, not preservation of original object type or wire bytes. The arithmetic explains why input acceptance cannot alone promise re-encoding within a differently expressed output budget; it supplies no total host-allocation bound or semantic rejection. [AFTER2384-TENTH25-231](../research/t20-v6-20261012/sources/c31c30728e19f0e4bc83977711513add57ef2530ab242e8aa7453e11a20e4d25/test_refinement_contracts.py#L31-L54)

The observation-signature patch makes a smaller ownership boundary explicit. It first requires an exact builtin list or tuple, captures tuple(values[:4097]) before validation and before waiting for the registry lock, and then permits only one through 4096 exact nonnegative integers. The extra captured position is an oversize sentinel, so the copy is bounded even when the caller supplies a much longer list; booleans do not pass the exact-int test. Subsequent validation therefore sees the captured tuple rather than the caller's mutable list. This local change does not establish a single-instant snapshot across concurrent caller mutations, prove the undisplayed storage and dispatch path, or qualify the imported bound_tree guard. The patch was read as text and remains unapplied. [AFTER1884-Q25-084](../research/t20-v6-20261012/sources/6f74c4489e45da213f6831c9e9e559494aeeedbd39db2debee1536a654cf6bc2/operational.py.patch#L3-L17)

[F109-N041]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/d060856a54e1fc122a4080d8a203701584e0205ab1a6b2f568cf91c8b7cad932.lean
[F109-N042]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/a2c025d675ceebf357dd25ba976ce4bf7bbf3e21a9203c78ae97c650a81adb22.lean
[F109-N043]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/8698fa61b4f65fbab39b91911fb65a6cba7d5d0e0d0028822446a9e4b4bc3270.lean
[F109-N044]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/ca82dd9791b6746d5d350d69226aa1638d81e32e042e4e5b0c94875944ea91d6.lean
[F109-N045]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/7ff3a0ff99449d52ba123f2543ec93f0b71219cf0ba81ad0c14e29ab588a4e21.lean
[F109-N046]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/342771fe9e1de1059429dda64888287c42d3b076ceebe8e21d92f2516dced827.lean
[F109-N047]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/66b33036ade34e22271d395cff12ea4d235c063075e701d0b45578d59ab387d7.lean
[F109-N048]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/3e72827eaa86ff17fa39e050529802b16091e8562414e56f5610f6a3982ea629.lean
[F109-N049]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/59c39ea0d7ff8e837dcb51ce24edd147e7cf0e12a6326f79111b82b210ade605.lean
[F109-N050]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/053e43f23ec8949886f08817443b830fc0b6f3b9546b0199cb185e945ae6f898.lean
[F109-N051]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/afb708e5195fcbbc43d09402e82830982a8b0cb19c4301f6c1c2c80e972706f9.lean
[F109-N052]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/7194891944b852fe2b301b03f895e8ed47ab3dc8336a94c2a44fb6cebb30ac99.lean
[F109-N053]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/0469fa6f9f32452bba861eddba88c389f0f9eae4ef529468926ac959c67cc299.lean
[F109-N054]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/0832f94fb866da91dea03247af1a1cbdf4810b1cfad1d0f2a494ae2d29274e8e.lean
[F109-N055]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/22d81a3948be52b14749eb6c200e6e4fcb971bc44bb87240e4760158d8148e27.lean
[F109-N056]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/be028b2ca3d26319e8a76aaa4687c67982cebf5afe6c31cba2f4755d3e36fa38.lean
[F109-N057]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/eaff0792a6eab2665c3e34ccc860c3e2d74e23ae49168934680a56bb964dba7c.lean
[F109-N058]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/dcd10c48454ef1e84c9ed136d040d9cee4a5d746ff2081e9f73e3c02020ae877.lean
[F109-N059]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/d0c1117bdce0d2990b89534cd88ad64d802c3faee533f22816a04314551bac91.lean
[F109-N060]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/752290febc488db6a8d84b9acc4f57fa17b7aad2f8e955c7b852c36451a8aff0.lean
[F109-N061]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/6b293ac5119cc072754413a7e9b084db0a3b2bcbd65a724b8646cf5666f23429.lean
[F109-N062]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/579aaaf659975a05aecb874b67f555bd64d642c390477663dbe92dd909ac30d8.lean

## 11. Exact finite certification for a nested unary language

Section 9.3 already exhibits the exact certificate that separates $`x`$ from its literal compiled $`x+0`$ implementation at the level of proof systems. The broader positive result is an algorithm for the entire declared unary language, followed by a sound extension that can use its certificates inside every inherited rule. These are two obligations: a complete semantic decision procedure for a restricted source language, and a proof that adding its introduction rule preserves the original contextual semantics. Neither follows just from seeing one accepted certificate. [Mathematical Companion, entries 7–9 and theorem appendix][unary-companion]

### 11.1 The language and its exact class of functions

Let expressions be generated by natural constants, one variable $`x`$, addition, multiplication, and

```math
\mathrm{if}\ a=b\ \mathrm{then}\ c\ \mathrm{else}\ d,
```

where **all four** children are expressions of the same grammar. Equality guards may themselves contain arbitrarily nested conditionals. Evaluation is over the ordinary natural numbers. There is no subtraction, division, minimisation, recursion or second input variable in this source language.

Its denotations are exactly the functions that agree, except at finitely many arguments, with a polynomial in $`\mathbb N[X]`$. The coefficient restriction matters: eventual agreement with an integer-coefficient polynomial would describe a larger class. A canonical description is a pair $`(P,E)`$, where $`P\in\mathbb N[X]`$ and $`E`$ is a finite map of **exact deviations**:

```math
f(n)=\begin{cases}E(n),&n\in\mathrm{dom}(E),\\P(n),&n\notin\mathrm{dom}(E),\end{cases}
\qquad E(n)\ne P(n)\text{ on its domain}.
```

Polynomials are represented canonically by coefficient lists with trailing zero coefficients removed. The finite map also has a canonical finite representation; a missing entry must be distinguished from an entry with value zero. The source's optional-natural lists make this distinction explicit. Redundant entries equal to the polynomial value are removed. A strict verifier rejects a submitted description containing such redundancy rather than silently identifying it with the canonical one.

Two elementary bounds explain why the normaliser is finite. If $`H\in\mathbb Z[X]`$ is nonzero of degree $`d\geq1`$, let $`S`$ be the sum of the absolute values of all coefficients below the leading one and put $`B(H)=1+S`$. For $`n\geq B(H)`$,

```math
\left|\sum_{i\lt{}d}h_i n^i\right|
\leq S n^{d-1}\lt{}n^d\leq |h_d|n^d,
```

so $`H(n)\ne0`$. For a nonzero constant take $`B(H)=1`$. In particular two distinct natural-coefficient polynomials can agree only at the finitely many natural arguments below $`B(P-Q)`$.

The checked dense-list algorithm uses a different, simpler bound. For coefficient lists $`p,q`$, put

```math
D(p,q)=2+\sum_i p_i+\sum_i q_i.
```

At every $`n\geq D(p,q)`$, each coefficient is strictly below $`n`$. Equality of the evaluations is then equality of base-$`n`$ digit expansions, hence equality of the trimmed coefficient lists. This argument does not subtract natural coefficients. The sparse signed-polynomial proof and the dense positional proof establish compatible finite bounds; they are not claims that two implementations perform the same computation.

### 11.2 A complete normalisation algorithm

Constants and the variable have their evident polynomial tails and no deviations. For addition and multiplication, combine the tail polynomials, inspect the union of the two finite deviation domains, evaluate the actual composite function at each inspected argument, and discard entries equal to the new tail.

For a conditional, suppose the four children have canonical tails $`P_a,P_b,P_c,P_d`$ and deviation maps $`E_a,E_b,E_c,E_d`$. Let $`W`$ initially be the union of all four deviation domains.

If $`P_a=P_b`$, the guard is true outside $`W`$. Choose $`P_c`$ as the result's tail, evaluate the **whole conditional** at every argument in $`W`$, and retain only deviations from that tail. If $`P_a\ne P_b`$, compute their finite coincidence set

```math
Z=\{n\lt{}B(P_a-P_b):P_a(n)=P_b(n)\},
```

or use the corresponding dense bound. Outside $`W\cup Z`$ the guard is false. Choose $`P_d`$ as the tail, evaluate the whole conditional on $`W\cup Z`$, and trim deviations. Notice why all four exception domains are included: an exceptional value in either compared child can reverse the guard, and an exceptional value in either branch can matter after that reversal.

**Normalisation theorem.** This algorithm terminates on every finite expression and returns its unique canonical description.

**Proof.** Structural recursion terminates because each recursive call is on a proper subtree. Every remaining operation is finite polynomial arithmetic, evaluation or bounded search. By induction the child descriptions are correct. Outside the inspected finite set, all children equal their tails and the root bound determines the guard; the chosen tail is therefore correct there. Inside the set, direct evaluation of the whole operation gives its actual value. Trimming preserves that value. This proves correctness.

If two canonical descriptions represent the same function, their polynomials agree at every sufficiently large natural argument. The nonzero-polynomial bound forces the polynomials to be identical. With the same tail, an exact deviation occurs at precisely the arguments where the function differs from that tail, and its stored value is determined. Thus the maps are identical as well. $`\square`$

Conversely, every pair $`(P,E)`$ of this form has an expression: express $`P`$ by natural constants, addition and multiplication, then place finitely many equality tests $`x=n`$ around it to return the exceptional values. Hence the description is exact in both directions, not merely a sound approximation to the grammar.

Semantic equality of two input expressions is decidable by equality of their normal forms. This is recognition within a supplied finite syntax; it is not an algorithm that recognises, from an arbitrary program or arbitrary mathematical function, whether it belongs to this class.

### 11.3 Finite tests, negative witnesses and composition

The normal form also gives a finite complete test set for a fixed pair. Let their descriptions be $`(P,E)`$ and $`(Q,F)`$, set $`W=\mathrm{dom}(E)\cup\mathrm{dom}(F)`$, and choose $`M`$ strictly above every member of $`W`$ and at least $`B(P-Q)`$ when the polynomial difference is nonzero. When the tails agree, any sufficiently large $`M\geq1`$ suffices. Then

```math
f=g\quad\Longleftrightarrow\quad
\forall n\in W\cup\{M\}\ f(n)=g(n).
```

Agreement at $`M`$ forces equality of the tails if they were different; agreement on $`W`$ handles every remaining deviation. The test set has at most $`|E|+|F|+1`$ elements. If the tails differ, $`M`$ is a concrete unequal-output witness. If only the deviation maps differ, a point in $`W`$ supplies one. This is a pair-specific finite test obtained from the exact syntax; no fixed finite test set works for all expressions, since an equality conditional can create an exception beyond any proposed fixed set. No polynomial bound on the size or running time of the normalisation is asserted.

The grammar is closed under composition by substituting the inner expression for every occurrence of $`x`$, including occurrences in both guard children. Normalising the resulting finite expression is a complete composition procedure. There is also a direct formula on canonical descriptions, which exposes an otherwise easy mistake.

Let the outer function have description $`(P,E)`$ and the inner function $`(Q,F)`$. If $`Q`$ is a constant $`c`$, the composite tail is the **actual value** $`f(c)`$, which may be an outer exception; inspect the inner deviation domain $`\mathrm{dom}(F)`$ and trim. For example, the outer function that returns $`7`$ at $`2`$ and otherwise returns its input, composed with the constant-$`2`$ function, is constantly $`7`$. Using the polynomial tail value $`P(2)=2`$ would be wrong.

If $`Q`$ is nonconstant, its natural coefficients imply $`Q(n)\geq n`$ for $`n\geq1`$. Let $`K`$ be the largest outer exception key, using $`0`$ when there are none. The composite tail is $`P\circ Q`$. It suffices to inspect

```math
\mathrm{dom}(F)\cup\{0,1,\ldots,K\}.
```

Outside this set the inner value is $`Q(n)>K`$, so it cannot hit an outer exception. Evaluate the actual composite at the inspected points and trim. This finite-preimage argument depends on the nonconstant, nonnegative-coefficient hypothesis. The source gives the direct sparse construction as a written result; its checked route composes the finite syntax and then normalises it. Neither should be credited as a fresh execution of the other.

The older unary languages first embed by an explicit interpretation-preserving translation. Recursively translate an old zero test `if a = 0 then b else c` to the equality conditional whose right compared expression is the natural constant zero. Translate an old root predicate `P = Q` to `if P = Q then 1 else 0`, and translate constants, the input, addition and multiplication by their corresponding constructors. Structural induction on the old expressions proves that this translation preserves their natural-number values.

The extension is semantically strict over the accepted older unary root-test union. Let $`h(2)=7`$ and $`h(n)=n`$ otherwise. The expression `if x = 2 then 7 else x` denotes it. An old unary zero-test expression agrees with one natural-coefficient polynomial on every positive input. If it denoted $`h`$, its eventual polynomial would have to be $`X`$ by the nonzero-polynomial bound, contradicting the value at $`2`$. Nor is $`h`$ an old root equality predicate, whose range is contained in $`\{0,1\}`$. This distinguishes expressive functions, not just the spelling of the syntax. The language can describe arbitrarily large finite exception patterns; there is no fixed bound on their number.

Every equality guard is itself eventually fixed: equal tail polynomials make it eventually true, and distinct tails make it eventually false outside finitely many roots and exceptions. Finite nesting cannot create an infinitely recurring change of guard. Several further boundaries follow at once. A bounded function in this language is eventually constant, excluding parity. The truncated predecessor function cannot have a natural-coefficient tail: its eventual polynomial would be $`X-1`$. With two input variables, equality of distinct polynomials can hold on an infinite diagonal, so the unary finite-exception proof does not extend. The source's union over variable arities has a separately stated $`\Pi^0_1`$-complete equality problem. Its lower-bound mechanism can be stated explicitly using the standard Diophantine representation theorem as an inherited theorem. Split an integer polynomial into two natural-coefficient polynomials $`P_+,P_-`$. The root predicate `if P_+ = P_- then 1 else 0` is equal to zero on every natural tuple exactly when the original polynomial has no natural solution. Diophantine representation makes these no-solution questions $`\Pi^0_1`$-hard; universal equality of total finite expressions has the matching $`\Pi^0_1`$ upper bound by evaluating each finite tuple. This invokes the established representation theorem, not a new proof of it. It fixes arity as part of the input and makes no numerical hardness-arity or every-fixed-arity claim. [Diophantine representation theorem][unary-diophantine] The presence of exact nested equality tests therefore does not erase the representation-sensitive boundary.

### 11.4 Which functions are invertible in this language?

The normal form and composition theorem yield a further exact consequence.

**Proposition — finite permutations are exactly the bijections.** A denoted function $`f:\mathbb N\to\mathbb N`$ is bijective if and only if it fixes all but finitely many naturals and permutes the finite set on which it differs from the identity. Its inverse is denoted by the same grammar, and bijectivity is decidable from the canonical description.

**Proof.** Let $`f`$ have tail $`P\in\mathbb N[X]`$. A constant tail violates injectivity. If the degree is at least two, the differences $`P(n+1)-P(n)`$ eventually exceed one; if it is linear with slope at least two, they always do. In either case infinitely many natural values are omitted by the tail, and finitely many exceptional inputs cannot fill all of them. Surjectivity therefore forces $`P(X)=X+c`$ for some $`c\geq0`$.

Choose $`N`$ beyond every exceptional input and $`M`$ larger than $`N+c`$ and every value of $`f`$ below $`N`$. The number of inputs mapped into $`\{0,\ldots,M-1\}`$ is

```math
N+(M-c-N)=M-c.
```

A bijection has exactly $`M`$ such inputs, so $`c=0`$. Let $`D`$ be the exact deviation domain from $`X`$. Outside $`D`$, every point maps to itself. If an input in $`D`$ mapped outside $`D`$, it would collide with that fixed point. Thus bijectivity is exactly the finite condition that the stored map $`E:D\to D`$ is a permutation. Conversely such a permutation together with the identity off $`D`$ is plainly a bijection. Its inverse is obtained by reversing the finite table and is expressible using equality conditionals. $`\square`$

This gives positive and negative controls with different explanations. Swapping $`0`$ and $`1`$ and fixing the rest is invertible. The function $`x+1`$ is injective but omits zero. The function $`x^2`$ leaves infinitely many gaps. Changing only $`f(0)`$ from $`0`$ to $`1`$ collides with the unchanged value at $`1`$. The finite-permutation algorithm concerns this exact source language, not bijectivity of arbitrary computable or typed functions.

If $`e`$ and $`e^{-1}`$ denote such a permutation and its constructed inverse, syntactic substitution produces expressions for both composites. Normalisation certifies their equality to $`x`$. The proof system below therefore certifies the identities of the **literal compiled substituted expressions**. This conclusion does not assume that the raw compiler commutes with an independently chosen raw composition operator.

### 11.5 From arithmetic equality to the original semantic identity

Compile each expression through the fixed primitive-recursive compiler and the original bracket compiler, obtaining the literal closed polynomial $`p_e`$. The equality primitive returns $`1`$ when its arguments agree, whereas the primitive-recursive choice operator uses zero to select its first branch. Accordingly the conditional compiler must pass the else branch first and the then branch second. Reversing this order would compile a different function.

The structural denotation proof covers every source constructor and yields an actual current typing

```math
\mathrm{Has}\,[]\,p_e:(N\to N).
```

The operational compiler interface is stronger than the particular uses of it
in the semantic proof. For every expression $`e`$, every total term environment
$`\eta`$, every raw input $`u`$ and every natural $`n`$, it gives

```math
\operatorname{NatObs}(u,n)
\quad\Longrightarrow\quad
\operatorname{NatObs}\bigl(\mathrm{eval}(p_e,\eta)\,u,
                           \llbracket e\rrbracket(n)\bigr).
```

The sole input premise here is the displayed observation. The raw input need
not be the canonical numeral, marker-free, or supplied with a typing or
semantic-membership certificate. The compiled endpoint is the literal
$`p_e=e.\mathrm{closed}`$ already typed above. Its scope-zero property gives
$`\mathrm{eval}(p_e,\eta)=\mathrm{eval}(p_e,\zeta)`$ for every $`\eta`$, so the
arbitrary environment introduces no valuation of a free endpoint variable.
The observation-only input contract is the retained compiler theorem exercised
by the source controls. The subsequent F/G argument additionally uses actual
endpoint typings and related-input membership to establish the semantic
relation; those additional premises belong to that argument, not to this
operational observation interface. [Unary compiler interface controls][R0002-L159]
To expose the semantic bridge, define the all-environment endpoint condition

```math
V(e,f)\Longleftrightarrow
\forall\rho\ F(N\to N,\rho,\eta_0,|p_e|,|p_f|).
```

It is equivalent to $`\forall n\in\mathbb N\,\llbracket e\rrbracket(n)=\llbracket f\rrbracket(n)`$. In the forward direction, apply the original arrow relation to the canonical raw natural input of index $`n`$, which the canonical-input theorem makes self-related. Compiler observation adequacy and `related_same_index` then force equality of the numerical outputs.

For the converse, fix an arbitrary unary type environment and independently chosen related raw natural inputs $`u,v`$. Natural standardness supplies their observation indices, and `related_same_index` identifies a common index $`n`$. Pointwise source equality and compiler adequacy give equal output observations. This agreement alone is insufficient for arbitrary raw outputs. The actual current typings of both compiled endpoints, together with the accepted fundamental theorem, make each endpoint self-related. The original PER laws give self-relatedness of each related input, and the arrow laws then give self-relatedness of each respective output. With these premises established, `same_index_related` relates the two outputs. Since the environment and cross-input pair were arbitrary, the complete arrow relation follows; testing only identical raw inputs would not prove this direction.

The original identity clauses now give the remaining equivalences. For $`F`$ at $`\mathrm{Id}_{N\to N}(p_e,p_f)`$, the clause consists of endpoint relatedness and the reflexive proof-conversion checks for the literal witness $`I`$; hence identity validity with $`I`$ in every unary environment is equivalent to $`V(e,f)`$. The original $`G`$ identity clause requires endpoint $`F`$-relatedness in both its left and right unary environments, each supplied by $`V`$. Conversely, validity in every lawful relation environment includes the diagonal environments and recovers the endpoint condition. Existence of a semantic polynomial witness uniformly over those environments is equivalent as well: any such identity witness entails the endpoint relation, while $`V`$ supplies the literal polynomial atom $`I`$ as a uniform witness. The actual endpoint typings also form the identity type through the existing formation rule. They do not by this argument supply a current-$`\mathrm{Has}`$ inhabitant of that identity.

The output is a semantic identity for the actual $`p_e,p_f`$. An externally supplied pair of endpoints needs a separate literal binding to those compiler results. The checker does not replace those endpoints with extensionally nicer programs and does not turn semantic validity into a derivation in unchanged $`\mathrm{Has}`$.

The exact pair $`x,x+0`$ makes this distinction concrete. The current compiler returns the old endpoints literally: $`I`$ for the variable and the distinct normal application tree for addition of zero. The latter contains 237 raw nodes in the source's fixed representation. A structural normality check and the fact that every one-step reduction requires a redex prove both terms normal. Confluence makes convertible normal forms equal, whereas these trees differ. Full closed-identity reflection for all rules of current $`\mathrm{Has}`$, and the corresponding bridge-only $`\mathrm{HasPlus}`$ theorem in section 10, therefore exclude **every** proof polynomial for that identity. A failed attempt to use $`I`$ alone would not establish this conclusion. The distinct but convertible terms $`I`$ and $`II`$ supply the contrary control showing why raw syntactic inequality alone is insufficient.

The companion's own obstruction stops at $`\mathrm{Has}`$ and $`\mathrm{HasPlus}`$. The homogeneous countermodel in section 8 separately excludes the literal pair in $`\mathrm{HasE}`$, and section 9.3 already combines that result with its concrete certificate. That previously established comparison is reused here; it is not attributed to the companion's more limited theorem.

### 11.6 The full certificate extension

Define $`\mathrm{CtxC},\mathrm{FormC},\mathrm{HasC}`$ simultaneously as least inductive relations. Copy the two context constructors, seven formation constructors and eighteen typing constructors of the full current polymorphic grammar, replacing only the recursive judgment names. In particular retain:

- the finite type-image table, support bound and bounded formation family;
- the type-weakened context of universal introduction;
- the original scope premise of product introduction;
- all five formation and four typing premises of dependent $`J`$;
- original polynomial conversion in identity introduction and conversion;
- the target scope requirement of conversion.

Add one constructor, with $`A=N\to N`$:

```math
\frac{\mathrm{FormC}\,\Gamma\,\mathrm{Id}_{A}(p_e,p_f)
\qquad \mathrm{verify}(e,f,c)=\mathrm{true}}
{\mathrm{HasC}\,\Gamma\,I:\mathrm{Id}_{A}(p_e,p_f)}.
```

The finite certificate $`c`$ is the common canonical description. The verifier recomputes both descriptions and checks their exact agreement with it. The premise is a total Boolean computation over finite data, not a call to an unrestricted semantic-validity oracle. The raw proof polynomial is $`I`$, while the finite source expressions and certificate are annotations in the derivation. No extensionality constructor or new raw conversion equation is added.

Mutual induction on old derivations embeds every current context, formation and typing judgment into this extension. This is syntactic inclusion, not conservativity: the certificate for $`x=x+0`$ supplies a closed identity absent from the included calculus.

The semantic work is more demanding than checking the new leaf at the empty environment. In the original heterogeneous identity interpretation,

```math
\begin{aligned}
G(\mathrm{Id}_A(p,q),R,\eta,\xi,u,v)
\Longleftrightarrow{}&F(A,R_\ell,\eta,p\eta,q\eta)\\
&\land F(A,R_r,\xi,p\xi,q\xi)\\
&\land u\simeq I\land v\simeq I.
\end{aligned}
```

A certificate rule may be used under an arbitrary formed context, so validity only at the zero environment is insufficient. The required transfer uses two specific facts. First, $`N`$ and $`N\to N`$ are represented by the inherited finite **type-code syntax**, and the original finite-code theorem makes their $`F`$ interpretation independent of the term valuation. This does not make either carrier a finite set. Second, the actual current closed typings of $`p_e,p_f`$ give scope zero; the closed-evaluation theorem makes their values independent of the term valuation. Combining these facts transports the checker theorem from the zero environment to every $`R,\eta,\xi`$ needed by the unchanged $`G`$ clause.

An earlier proposed transport through the empty-context compatibility relation was invalid: that relation fixes both term valuations to the zero environment and cannot by itself justify arbitrary-valuation validity. The finite-carrier and closed-evaluation argument is the corrected proof. Retaining this distinction prevents a closed theorem from being silently used as an all-context premise.

### 11.7 Why every inherited rule remains sound

The soundness proof is a simultaneous induction on the **whole** extended grammar. It proves context laws for $`\mathrm{CtxC}`$, hereditary type laws for $`\mathrm{FormC}`$, and the original fundamental relation for $`\mathrm{HasC}`$:

```math
\forall R,\eta,\xi,\quad
H(\Gamma,R,\eta,\xi)
\Longrightarrow G(A,R,\eta,\xi,p\eta,p\xi).
```

The contextual hypothesis $`H`$ is retained. The theorem does not assert a typing relation at arbitrary incompatible environments.

Context extension uses the formation induction hypothesis's type laws. Parameter, Bottom and Raw formation retain their original laws; universal, product and sum formation rebuild the hereditary component laws from the extended induction hypotheses. Identity formation uses the carrier laws together with both endpoint fundamental results. These formation conclusions are proved for extended derivations, rather than assumed by pretending that every extended formation already has an old derivation.

Each of the eighteen old typing cases applies its original semantic lemma to the extended induction hypotheses. Variables use context lookup. The combinators use their original application laws. Finite import retains the actual type-image and support assumptions. Universal rules retain uniformity over the appropriate valuations. Product rules use heterogeneous argument relations; sum rules retain projection and representation facts. Identity introduction uses original conversion soundness, proof erasure uses the original proof interpretation, and conversion uses saturation at the original target and its scope. Dependent $`J`$ uses the full carrier, motive and target type laws together with the equality and base-proof hypotheses, including both coordinates of its dependent motive. It is not replaced by a nondependent example.

For the new constructor, the target-formation induction hypothesis supplies its hereditary type laws, and section 11.6 supplies the certificate identity at all required valuations. This holds in particular at every pair admitted by $`H(\Gamma,R,\eta,\xi)`$. The witness $`I`$ satisfies the two conversion clauses reflexively. This completes the mutual induction and yields whole-rule soundness, not merely the soundness of an isolated certificate leaf.

Three conditional interfaces make the inherited laws explicit. Write
$`E(\Gamma,\rho,\eta,\xi)`$ for the original unary context relation,
$`\operatorname{diagEnv}(\rho)`$ for its diagonal heterogeneous relation
environment, and $`R_\ell,R_r`$ for the two unary endpoints of a relation
environment $`R`$. For an actual extended typing,

```math
\mathrm{HasC}\,\Gamma\,p:A,
\qquad E(\Gamma,\rho,\eta,\xi)
\quad\Longrightarrow\quad
F(A,\rho,\eta,\mathrm{eval}(p,\eta),\mathrm{eval}(p,\xi)).
```

For an actual $`\mathrm{FormC}\,\Gamma\,A`$ derivation, and arbitrary raw
$`t,u`$, the strong diagonal law is

```math
E(\Gamma,\rho,\eta,\xi)
\quad\Longrightarrow\quad
\bigl[G(A,\operatorname{diagEnv}(\rho),\eta,\xi,t,u)
\Longleftrightarrow F(A,\rho,\eta,t,u)\bigr].
```

The same formation premise gives two-sided invariance:

```math
E(\Gamma,R_\ell,\eta,\eta'),\quad
E(\Gamma,R_r,\xi,\xi')
\quad\Longrightarrow\quad
\bigl[G(A,R,\eta,\xi,t,u)
\Longleftrightarrow G(A,R,\eta',\xi',t,u)\bigr].
```

For the first statement, specialize the fundamental theorem to the diagonal
relation environment. The context diagonal law converts the given $`E`$
premise into its required $`H`$ premise, and the formed target's diagonal law
then yields $`F`$. The latter two statements are respectively the diagonal and
invariance clauses of the hereditary type laws obtained by the mutual
formation proof. Thus these consequences keep their exact $`\mathrm{HasC}`$
or $`\mathrm{FormC}`$ and compatibility premises. The special certificate leaf's
all-valuation fact in §11.6 does not remove those premises from the general
interfaces. [Certificate extension relation laws][R0002-L150]
### 11.8 Exact completeness at the closed compiled interface

For source expressions $`e,f`$ and their literal endpoints, the following are equivalent:

1. Some polynomial $`r`$ has $`\mathrm{HasC}\,[]\,r:\mathrm{Id}_{N\to N}(p_e,p_f)`$.
2. The same judgment has the explicit witness $`I`$.
3. The complete normal-form equality checker accepts $`e,f`$.
4. The original $`F`$ identity with witness $`I`$ holds in every unary environment.
5. The original $`G`$ identity with witness $`I`$ holds in every lawful relation environment.
6. The source functions agree at every natural input.

**Proof.** Checker acceptance supplies a common canonical description and an accepted finite certificate. Existing current formation embeds into $`\mathrm{FormC}`$; the new constructor yields the explicit $`I`$ derivation. Conversely, an arbitrary derivation with any proof polynomial is subject to whole-rule soundness. At the empty context the actual zero environments satisfy the compatibility relation, so the derivation supplies an original semantic witness. The established semantic-witness equivalence forces pointwise natural equality and hence checker acceptance. This direction does not inspect the last rule: derivations ending in $`J`$, conversion or any other retained constructor are covered. The remaining equivalences are the original compiler-semantic interfaces. $`\square`$

The empty context is essential for this unconditional completeness statement. A well-formed context may assume the identity between the compiled constants zero and one. A variable then inhabits that assumed identity although the closed checker rejects the pair. Such a context has no compatible semantic valuation, so conditional all-context soundness remains intact. This explicit example blocks the overclaim that the checker decides identity inhabitation under arbitrary assumptions.

The new $`x=x+0`$ proof can be erased by the retained erasure rule and used in the actual $`J`$ rule with a constant Raw motive. The source also supplies the generic dependent-$`J`$ interface with all its original premises; the full induction above is what supports that general case. A few successful uses would not substitute for it.

This gives a genuine effective finite-proof presentation for the restricted completion service. It does not provide a serialised parser and checker for arbitrary complete proof files, unrestricted type inference, arbitrary Raw completeness or a practical resource bound. The finite certificate and its raw witness are different objects. Resource exhaustion while computing a normal form is not a certified negative mathematical judgment.

### 11.9 Source, implementation and proof-evidence boundaries

The new mathematical account draws on entries 7–9 and the theorem appendix of the single public *Mathematical Companion* body, Git blob `1169e7dccb24481aa478c8929434dbe9daf251cd`, SHA-256 `10903b3260522cec902c7213a1b93a2c3280922126994c76f95755baadc2a91e`. Its thirteen internal entries do not become thirteen separately received source bodies. The public companion distinguishes its written sparse bounds and direct composition construction from the checked dense-list normaliser, compiler interfaces, literal obstruction and full certificate extension.

Its historical records report six initial normaliser/compiler modules, a seventh literal-obstruction module and two further certificate-extension modules, with independent formal acceptance of the specified frozen interfaces. The recorded finite arithmetic checks include 64 expression trees, 704 output comparisons, 64 addition-of-zero comparisons and 64 reification comparisons, alongside negative controls. These are source-reported executions, not newly run results of this composition. Likewise the standard assumptions `propext`, `Quot.sound` and inherited `Classical.choice`, the permitted standard opaque `Lean.opaqueId`, and the native compiler and foreign-function trust boundary remain those reported by the source. No kernel replay, source-code audit or binary validation is claimed here.

The source's rejected unequal certificate, missing formation, changed endpoint, omitted-$`J`$-premise, invalid coercion and discarded-environment-transport controls test the interface at their actual scope. A rejected coercion does not prove mathematical noninhabitation. The all-derivation reflection argument supplies the current-calculus negative theorem; the separate homogeneous countermodel supplies the extensional-calculus negative theorem already established in section 8.

The new result of section 11.4 is an elementary consequence composed from the exact canonical class and its closure under substitution. The earlier concrete certificate and the current chapter's full semantic and nontranslation results retain their prior ownership. No external priority claim, canonical adoption of the extension, or new theorem about arbitrary programs follows from this restricted consolidation.

The exact `UnaryExpressions` provider binds the finite +, multiplication and nested-equality grammar to the literal primitive-recursive compiler, including substitution into every child and the guard/else/then argument order. Its observed-natural adequacy and original F/G identity equivalences identify pointwise source equality; endpoint formation is not a current intensional identity derivation. `PositiveInterface` separately instantiates the restricted compiler's `FragmentValid` equivalence and closed typing at `Curried2`; a matching semantic conclusion does not make the two grammars identical. [R750A-556] [R750A-548]

The accepted concrete boundary in §11.8 is precisely the `UnaryCurrentIdentityBoundary` object already linked as [certificate-pair]: x and x+0 have distinct normal compiled endpoints, accepted semantic/checker identity, and no current Has or HasPlus identity witness. This existing theorem, rather than the text of a failed attempt, supplies the nonderivability claim. The three small controls instead attempt an unequal 0/1 certificate, a semantic-existence-to-current-Has coercion, and a coercion of the strict certificate extension back to current Has. A fourth omits the argument-observation premises of `PR.compile_obs`. They specify rejected interface uses; they are not new independence proofs or newly observed compiler failures. [R750A-533] [R750A-528] [R750A-566] [R750A-580] [R750A-555]

The generated regression body contains64 expression cases, each with values at inputs0 through10, an additive-zero identity assertion and normalize/reify idempotence, including finite exceptions from nested equality. Its comment attributes the expected vectors to an independent evaluator. Reading those192 assertions does not reproduce that evaluator or execute the assertions, and this finite sample is not the completeness proof for all inputs. [R750A-505]

[R750A-505]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/86f9c6f6a43bc996b9c2d56e669519345f167799512a713de05cdead42288175/GeneratedUnaryRegressions.lean
[R750A-528]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8ce8e8c1fba1948f579202f8a490551483782475b5ac3fce387d50a4e95b0749/ForgedUnequalCertificate.lean
[R750A-533]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8e943773416edcb225d1c3ed9961938bc75f82d7cc67f0bdb1aea5a98b126eac/UnaryCurrentIdentityBoundary.lean
[R750A-548]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9369477b55dad4c2fc11bb8d554d343d91057c443ac81fc3a7ef3f45bc5b8859/PositiveInterface.lean
[R750A-555]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/952a4e5f9843c4f6e1e22c25aa3bd4a2b53a731170d4214a45933669dda07281/MissingArgumentObservation.lean
[R750A-556]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9577dc7da47df9915c87b374b9bd87f534849f94ba272bf60ccd7f20313cbe56/UnaryExpressions.lean
[R750A-566]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9880810bb76f711fad57c1dc2643b4bffc6dba02365266492545447c8004d71b/SemanticExistenceIsNotCurrentTyping.lean
[R750A-580]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9b753d8e766a1edb17d5c1ad40fb3e6451711d09b9ec46f4ae9a2c0f6fd62456/NoCurrentHasCoercion.lean

## 12. Effective syntax codes and a semantic non-enumerability boundary

The effective results above have specified input domains. A different, explicitly represented family shows why neither a computable type description nor a single short semantic witness makes unrestricted semantic validity effectively enumerable. The construction uses the existing source types and the full-PER interpretation, rather than assigning an arbitrary undecidable predicate to new syntax. Its conclusion concerns semantic inhabitation and fixed-term semantic validity, not an unproved assertion about the enumerability of source derivations. [FAMILY-HALTING] [FAMILY-CODE]

### 12.1 One formed type for each machine index

Fix a binary primitive-recursive program $`f`$ in the retained finite-arity program syntax. The compiler interface supplies the literal source polynomial $`p_e=\operatorname{simFamily}(f,e)`$, typed as $`N\to B`$, where $`B`$ is the inherited Boolean type. Its numerical arguments are ordered as the bound $`k`$ followed by the machine index $`e`$. Define the actual source type

```math
A_e=\Pi n:N.\ \mathrm{Id}_{\mathrm{Raw}}
       (p_e\,n\,\mathbf 0\,\mathbf 1,\mathbf 0).
```

Here $`\mathbf 0,\mathbf 1`$ are the source Raw observation atoms, not an assertion that the carrier is a two-element set. The source obtains the body typing by instantiating the Boolean at Raw and applying it to those atoms. The existing product and identity formation rules then form $`A_e`$ in the original calculus; formation also passes to the extensional calculus by inclusion. [FAMILY-TESTS] [FAMILY-HALTING]

Keep the interpretation's premises explicit. Let $`\rho`$ range over admissible valuations by conversion-saturated PERs, and keep the closed term environment equal to the actual $`\eta_0=\operatorname{zeroEnv}`$. Write

```math
H(A)\ \Longleftrightarrow\
 \forall\rho\,[\operatorname{Adm}(\rho)\Rightarrow
   \exists t\ F(A,\rho,\eta_0)(t,t)],
```

and let $`V_{KI}(A)`$ replace that existential clause by
$`F(A,\rho,\eta_0)(KI,KI)`$, for the one fixed semantic applicative term $`KI`$. The selected family satisfies

```math
H(A_e)\quad\Longleftrightarrow\quad
V_{KI}(A_e)\quad\Longleftrightarrow\quad
\forall k\in\mathbb N\ f(k,e)=0.
```

This equivalence is not justified by testing a finite list of numerals. For necessity, apply any semantic inhabitant to each canonical Church input, which is self-related in the Church PER. The Raw identity endpoint forces its observation to convert to $`\mathbf 0`$; faithful transport back to the source observation and the compiler's observation lemma give $`f(k,e)=0`$.

For sufficiency, take arbitrary related semantic Church arguments. Standardness relates the first to a canonical input of some index $`k`$. The supplied typing of the closed $`p_e`$, its inclusion in the extensional calculus and the full-PER fundamental theorem relate their Boolean outputs. Instantiating that Boolean relation with Raw conversion transfers the canonical zero observation to the arbitrary argument. Closed-environment independence supplies the required body instance. Finally $`KI`$ applied to either argument converts to $`I`$, discharging both proof coordinates of the identity relation. Thus the same $`KI`$ works for every admissible $`\rho`$, although $`H`$ initially allowed a different witness for each valuation. This is semantic evidence; no source derivation assigning $`KI`$ the type $`A_e`$ is inferred. [FAMILY-TESTS]

### 12.2 The family map uses the actual syntax encoding

The coding argument fixes the existing derived `Encodable` instances for the actual polynomial and type syntax. They are generated by the retained handler attributed to Kyle Miller, whose documentation expressly treats its concrete encoding as an implementation detail. The argument is therefore tied to this exact edition, not a promise that arbitrary future encodings retain the same constructor equations. The handler represents constructors by tagged finite trees and encodes natural leaves and pair nodes using $`\operatorname{pair}(0,n)`$ and $`\operatorname{pair}(a+1,b)`$. The selected source verifies the resulting application, product and identity constructor equations directly. [FAMILY-ENCODED] [FAMILY-CODEC] [FAMILY-CODE]

In particular, the actual unnormalised input numerals satisfy $`\operatorname{inputNumeral}(0)=KI`$ and $`\operatorname{inputNumeral}(n+1)=\sigma\,\operatorname{inputNumeral}(n)`$ for one fixed source polynomial $`\sigma`$. Their numerical codes are primitive recursive by ordinary recursion and the application-code equation. With $`f`$ fixed, the simulator's code is a constant; composing the constructor-code operations gives primitive-recursive, hence computable, maps

```math
e\longmapsto\ulcorner p_e\urcorner,
\qquad e\longmapsto\ulcorner A_e\urcorner.
```

This does not assume a `Primcodable` instance for all source syntax, replace the syntax encoding, or establish a general parser or proof-checker implementation. Uniformity here is over $`e`$ for each fixed $`f`$. It is not a universal primitive-recursive evaluator with the program itself varying as another input. [FAMILY-CODE]

The separate coded-rule side-condition component supplies a primitive-recursive Boolean function checkSideCode on natural-number codes. Its 63 tag branches cover the source J and E rule constructors, with false as the unmatched-tag fallback. The nonconstant branches preserve lookup, finite and polynomial certificate checks and the displayed scope conditions; in particular dependent-function extensionality tests its codomain at one greater context depth. Other branches have no additional Boolean side condition. The stated exactness theorem is checkSideCode(encode r)=r.checkSide for a Rule value r. It does not say that every accepted natural is a well-formed rule encoding, that its premises hold, or that a whole derivation has been validated. This is a dependency-relative side-condition compiler for the source rule interfaces, not adoption of J or E rules into the unchanged current calculus or a new kernel execution. [NEXT-RSIDE-219](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/446de3c94bc35024d376d36e30074235151e951e83146dbd452538470d30c4cf/RuleSideCode.lean)

The rule-map controls retain the precise finite-import premise list: encoding a rule with supplied type images τ produces their formation claims in order, followed by formation of the instantiated finite target, so its length is |τ|+1 even when some supplied images are unused. The two-image example therefore retains three obligations. The separate lookup, polynomial-certificate, scope, extensionality and branch/motive examples are requested evaluation checks, not obtained Boolean results or a proof that an entire encoded derivation is accepted. The general premise-list equations themselves rely on the imported map exactness theorem. [NEXT-D8-238](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/49a77625c46d2495fe457cc48dc876dcbbe1440b1a58e9417e8f75709384bdc8/RuleMapControls.lean#L21-L56)

### 12.3 Bounded evaluation supplies the obstruction

Use the actual natural-number enumeration $`c_e`$ of Mathlib partial-recursive codes, with its inverse encoding, and define

```math
b(k,e)=
\begin{cases}
0,&\operatorname{evaln}(k,c_e,0)=\mathrm{none},\\
1,&\operatorname{evaln}(k,c_e,0)=\mathrm{some}(x)
   \text{ for some }x.
\end{cases}
```

Bounded evaluation makes $`b`$ primitive recursive. The source translates finite-arity primitive-recursion evidence into existence of a program in the retained program syntax, respecting the counter, accumulator and parameter order. Choose the resulting one fixed binary program $`f`$ representing $`b`$. This is an existence argument, not extraction of executable data from a proposition. Completeness of bounded evaluation gives

```math
\forall k\ f(k,e)=0
\quad\Longleftrightarrow\quad
\operatorname{eval}(c_e,0)\text{ is undefined}.
```

The right-hand index set is not recursively enumerable. The source reduces the corresponding result for actual partial-recursive codes along their computable encoding, rather than postulating a surrogate halting predicate. Combining this fact with §§12.1–12.2 gives one computably presented family of formed source types for which both $`\{e:H(A_e)\}`$ and $`\{e:V_{KI}(A_e)\}`$ are not recursively enumerable. [FAMILY-BOUNDED] [FAMILY-HALTING]

Consequently, if an acceptance predicate on these indices is recursively enumerable and sound for $`H(A_e)`$, it cannot accept every valid member. Otherwise soundness and completeness would identify its accepted set with the non-enumerable set just constructed. A recursively enumerable acceptance procedure on the exact syntax codes would likewise yield an enumerable index predicate by the computable family map. The conclusion requires soundness. It neither assumes that a particular source derivability relation is recursively enumerable nor identifies semantic validity with a derivation in `Has`, `HasE` or the certificate extension. [FAMILY-HALTING] [FAMILY-CODE]

This does not contradict the supplied-typing Church decision procedure of §6.3 or the restricted unary certificate completeness theorem of §11.8. Their domains and judgments are different. It also sharpens the warning in §4.1: even the same short semantic witness $`KI`$ need not make its varying type-validity problem enumerable.

This family has a separate one-sided negative search. For fixed binary primitive-recursive f, scan(f,e,fuel) checks indices below fuel and returns the least k with f(k,e) nonzero; none says only that the inspected prefix is zero. The written scan/search correspondence and semantic-family interface identify eventual return with failure of Holds(programType(f,e)); the numerical least-witness search is stated partial recursive. Mapping a returned k to the literal certificateTerm(k) gives HasE evidence of NoConfusion→(programType(f,e)→bottom), retaining the explicit NoConfusion premise and not serializing a derivation tree. The projection control returns none at fuel one despite invalidity, then returns k=1 at fuel two; valid zero-program inputs have undefined search. The separate audit excludes semantic shortcuts only from the literal certificate-typing root. These are import-relative source interfaces and audit requests, not fresh execution, unconditional refutation or a decision procedure for validity. [SUB250-FINAL28-230](../research/t20-v6-20261012/sources/7a82b91805c79e60920aeac71d4900f60ca1b9aa38920e31094778995c5a5ab6/NegativeSearch.lean#L10-L126) [SUB250-FINAL28-233](../research/t20-v6-20261012/sources/7b56f10a92293f81383100e7ec3f66f1e0f1d310e38f828e8d3508a10290692b/SearchControls.lean#L9-L62)

The conditional refutation source makes the missing premise explicit at two judgment levels. A finite failed primitive-recursive test converts its Raw observation to one; source J then transports the submitted identity with zero into RawClash=Id_Raw(zero,one). Abstracting over that test-bearing program and NoConfusion=RawClash→bottom constructs an old-E witness of NoConfusion→(programType→bottom). Only after an actual closed HasJ proof of NoConfusion is supplied does the final application produce a HasJ witness of programType→bottom. Formation, observation typing and the original source transport are retained throughout. The construction neither supplies NoConfusion itself nor reflects semantic invalidity directly into unconditional source refutation; its compiler, conversion and structural interfaces remain imported. [NEXT250-V25-113](../research/t20-v6-20261012/sources/95aaa16c13506a9fa579eb07ef7200b3db1060975cca946318a5b75a564f3c36/ConditionalRefutation.lean#L15-L56) [NEXT250-V25-113](../research/t20-v6-20261012/sources/95aaa16c13506a9fa579eb07ef7200b3db1060975cca946318a5b75a564f3c36/ConditionalRefutation.lean#L58-L114) [NEXT250-V25-113](../research/t20-v6-20261012/sources/95aaa16c13506a9fa579eb07ef7200b3db1060975cca946318a5b75a564f3c36/ConditionalRefutation.lean#L116-L128)

On this fixed primitive-recursive test family, the completeness interface is an exact conditional equivalence: failure of Holds(programType(f,e)) is equivalent to a finite index k with f(inputs(k,e))≠0, and also to existence of an actual HasE certificate of NoConfusion→(programType(f,e)→Bottom). The forward direction turns the finite counterexample into the imported literal refutation template. The reverse direction uses FullPER soundness together with semantic validity of NoConfusion in the faithful interpretation; semantic validity here is not source adoption of a no-confusion axiom. Only an actually supplied closed HasJ proof of NoConfusion converts invalidity into an unconditional HasJ negation of the program type. The dependency-audit program targets the forward construction roots, not the semantic converse of the equivalence. Its requested exclusion of semantic or reflection shortcuts is not a received audit result, and the theorem supplies neither a decision procedure for validity nor a closed source proof of NoConfusion. [R134-033](../research/t20-v6-20261012/sources/e7897dc8845d86ace3a4c58d32b77bb63588a0c888de03acf39a8e68a84e4cb0/RefutationCompleteness.lean#L12-L50) [R134-033](../research/t20-v6-20261012/sources/e7897dc8845d86ace3a4c58d32b77bb63588a0c888de03acf39a8e68a84e4cb0/RefutationCompleteness.lean#L57-L71)

The conditional-refutation controls retain both directions of discrimination on concrete primitive-recursive programs. For every parameter e, the constant-one program supplies an old-E certificate of NoConfusion→(programType(oneProgram,e)→Bottom), using its failed test at index zero. Conversely, the constant-zero program has no old-E certificate of that same conditional form: the imported invalidity/refutation equivalence would make such a certificate contradict the all-zero validity test. The second statement is absence of the conditional certificate itself, not merely failure of a particular bounded search. Neither control provides a proof of NoConfusion or an unconditional refutation; both consume their stated completeness and semantic-boundary dependencies and supply no new execution result. [NEXT250-E25-189](../research/t20-v6-20261012/sources/a3336c3a99632aee3bdf08e9bf146a079ed0d048ff187e97aa2545ea4c25fb77/RefutationControls.lean#L8-L18)

These arguments preserve the exact source statements and their imported compiler, standardness and full-PER interfaces. The 138-module source/import closure is a source-identity result, not a new build or kernel replay. The exact accepted A05/CP3 artifact and its source, toolchain, search-root and axiom-readback join remain unreceived. The displayed `#print axioms` requests in the sources are not received axiom outputs, and this consolidation neither adopts an unverified toolchain nor claims new Lean execution.


## 13. Effective observations: the exact semantic bridge and its limits

The effective observation results distinguish three things that a statement about “deciding identity” can otherwise obscure: the supplied typing evidence, the semantic relation being decided, and the representation of the numerical computation. They concern the fixed research P01AC interfaces. They do not, merely by sharing syntax or terminology, adopt those interfaces as a different canonical calculus. The finite certificate result of §11 and the semantic index-family result of §12 consequently coexist with the following conditional observer theorem. [R250-C27-196][R250-C27-210]

### 13.1 Canonical tests recover the typed relation, not raw endpoint conversion

Let $`N`$ be the Church carrier and $`C=N\to\mathrm{Raw}`$. For two closed polynomials with **both** current typing derivations $`\mathrm{Has}\;[]\;p\;C`$ and $`\mathrm{Has}\;[]\;q\;C`$, the exact interface equates

```math
\forall\rho\;F(C,\rho,\eta_0)(\llbracket p\rrbracket_{\eta_0},
                                  \llbracket q\rrbracket_{\eta_0})
\quad\Longleftrightarrow\quad
\forall n\;\operatorname{Conv}
 (\llbracket p\rrbracket_{\eta_0}\,\overline n,
  \llbracket q\rrbracket_{\eta_0}\,\overline n).
```

Here $`\overline n`$ is the retained canonical source numeral. The corresponding identity statement ranges over all relation environments in the original $`G`$ interpretation and keeps the actual closed term environment $`\eta_0`$. Its displayed semantic proof coordinates are both $`I`$. This is a semantic identity equivalence, not an assertion that a current source derivation of that identity exists. [R250-C27-210]

The forward direction can specialize to canonical inputs because their semantic membership is known. The reverse direction needs more than tests on a list of numerals: Church standardness and the two endpoint typings transfer the tests to arbitrary **related, potentially different** inputs $`x,y`$. For every $`\rho`$ and $`F(N,\rho,\eta_0)(x,y)`$, the conclusion compares $`p\,x`$ with $`q\,y`$. The same-index interface likewise keeps both self-membership premises and each term's uniform iteration equation; equality of the iteration indices is not a substitute for those premises. [R250-C27-210]

The small rejected-interface sources mark these exact boundaries. Reusing left typing as right typing, omitting the semantic-membership input to standardness, supplying validity at only one environment, or using a same-argument pointwise equation as a cross-argument equation fails to supply the displayed theorem's contract. The analogous Boolean observation interface also requires right Boolean self-membership; its control deliberately supplies the left proof twice. The wrong-raw-endpoint control tries to replace the semantic endpoint relation by raw conversion of the endpoint terms themselves. None of these failed applications is, on its own, a theorem that every possible proof of the stronger claim is impossible. They are exact negative interface fixtures, and their compiler rejection has not been rerun by this exposition. [R250-C27-55][R250-C27-191][R250-C27-214][R250-C27-103][R250-C27-241][R250-C27-223]


<a id="final189-b02-original-semantic-standardness"></a>

The direct original-F/G standardness proof does not require a marker-free term or a supplied syntactic typing. For an arbitrary raw semantic inhabitant t of N, use a Link between two Raw PERs whose related pairs have the form (zeroⁿ one, fⁿx), up to source conversion. The universal semantic clause supplies a common n for the two applications. The terms zeroⁿ one are normal and their syntax is injective in n; normal-form uniqueness therefore identifies the count obtained from any f,x with that obtained at the fixed marker arguments. Thus one n works for every f,x even when t itself contains the marker constructors. This is application-conversion standardness, not a normal form theorem for the unapplied t. [F189B-821](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ddf25f10d625a38087f237b1d16c0e2968a5fd7ed1a86a6f3f9192318f3b0428/EffectiveStandardness.lean)

The corresponding rule boundary keeps semantic evidence and syntax separate. Existence of any closed polynomial semantic proof of Id_C(p,q) is equivalent to the validity witnessed by literal I: necessity projects the endpoint relation at diagonal environments, and sufficiency chooses I. Both current Has and repaired HasE identity derivations imply that validity. For the exact typed machine-observer target, the supplied step/output representation hypotheses then imply that every observed run output is zero. The module also supplies a closed scoped target and infinitely many typed endpoints distinguished by the normal marker outputs. It expressly does not kernel-prove recursive enumerability or non-enumerability; those classifications retain their separate written arguments. [F189B-824](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/df16203390fe6a5106d72a5d6d4323ff8999a85731ed2dfbfa5f944b8e830a4c/EffectiveRuleBoundary.lean)

### 13.2 The universal observer retains its representation hypotheses

Fix a term $`U`$ and a binary predicate $`H(e,n)`$. The source constructs the literal $`\operatorname{universalTester}(U,e)`$ at $`C`$ and a constant endpoint returning the observer numeral $`\nu_0`$. Its current typing, closedness and target formation do not require that $`U`$ terminate. Use a separate notation $`\nu_n`$ for the observer's literal `numeral n`, with $`\nu_0=K I`$ and $`\nu_{n+1}=\operatorname{numericSucc}\,\nu_n`$. The canonical Church inputs $`\overline n`$ above and these observer numerals are distinct retained syntax conventions, not silently interchangeable terms. Observation of the tester on canonical input $`\overline n`$ converts to $`U\,\nu_e\,\nu_n`$. The semantic theorem then assumes **both** representation clauses:

```math
H(e,n)\Rightarrow\operatorname{Conv}(U\,\nu_e\,\nu_n,\nu_0),
\qquad
\neg H(e,n)\Rightarrow\neg\operatorname{Conv}(U\,\nu_e\,\nu_n,\nu_0).
```

Under these clauses, endpoint validity, and equivalently the original semantic identity validity, holds exactly when $`\forall n\;H(e,n)`$. For necessity, a failed $`H(e,n)`$ contradicts the canonical test at that $`n`$ using the negative representation clause. For sufficiency, each positive representation instance gives its canonical test and the typed semantic bridge supplies the full relation. Thus typing the tester is not an oracle for its semantic identity. [R250-C27-196, `universal_endpoint_valid_iff_total`, `original_universal_identity_iff_total`][R250-C27-196]

A stronger negative premise is sometimes easier to supply: the exact marker-erased observation has no raw normal form. Conversion to the actual normal zero numeral would, by the inherited joining property for conversion and normality of that numeral, supply such a normal form. The source therefore derives nonconversion and passes it to the same observer theorem. Marker replacement is tied to the retained source conversion theorem; for a marker-free $`U`$ the displayed numerical observation is unchanged by that replacement. This is not an identification of an unspecified external machine language with the source reduction relation. [R250-C27-196, `raw_no_normal_form_excludes_zero`, `erased_no_normal_form_excludes_zero`, `original_universal_identity_iff_total_of_no_normal_form`][R250-C27-196]

The existence of a universal representer for an external computation, its two representation properties, its coding, and any hierarchy classification remain additional obligations. $`H`$ is arbitrary in this theorem; neither its computability nor the existence of a representing $`U`$ is obtained merely by introducing them as parameters. The exact-interface examples explicitly retain those parameters rather than claiming a hierarchy theorem. Similarly, a representation of an observation function cannot be supplied again where the distinct step function's representation is required. [R250-C27-210][R250-C27-211]

A separate step-and-observer reduction supplies an exact positive instance of this representation discipline. Let `Represents g G` mean that G applied to each literal configuration numeral k converts to the numeral for g(k), and independently let O represent the observation function o. Induction carries G's equation through the represented run starting at c; O's equation then yields the numeral for o(run(g,c,n)). The normal and injective configuration numerals reflect conversion back to equality of their natural-number values. [F939-C917]

Consequently the literal tester at the fixed N→Raw carrier has original F/G identity validity against constant numerical zero exactly when o(run(g,c,n))=0 for every n. Semantic Church standardness supplies the sufficiency direction for **arbitrary semantic inputs**, not just the canonical numerals inspected in the necessity direction. Target formation and closedness are available independently of the represented computation equations; neither proves those equations. The source also gives an explicitly typed constant family with pairwise distinct F-classes in this carrier: endpoint validity between its mth and nth constants forces m=n. Both representation premises remain explicit mathematical inputs, with no general representability/computability axiom, new current-Has inhabitant of the identity or hierarchy classification inferred from the reduction. [F939-C917]

[F939-C917]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fc3d89c9768e4fedb0c5120b6927c9ea6e2340355d3333f06996345ee057735d/EffectiveReduction.lean

### 13.3 Boolean observations and a finite positive typing gate

For $`C_B=N\to B`$, with $`B`$ the inherited impredicative Boolean type, self-related Boolean outputs have one of the two uniform selection behaviors. Given **both current typings**, the Boolean interface equates semantic endpoint validity with all canonical Boolean tests, and invalidity with the defined finite mismatch predicate. The primitive-recursive compiler retains its input-environment representation premise. For a fixed binary primitive-recursive program $`f`$, the literal family $`\operatorname{simFamily}(f,e)`$ has semantic identity with the constant choice exactly when $`\forall n\;f(n,e)=0`$, using the source's actual input order. A finite testing budget cannot be promoted to the all-tests premise. These are the stated contracts; they do not by themselves establish a complexity classification for untyped bare input codes. [R250-C27-226][R250-C27-88]

The positive gate supplies a different, genuinely constructive connection between a finite numerical witness and **current typing**. Its search state at counter $`n`$ unfolds to the next counter when the numerical result is zero and to $`I`$ when it is nonzero. If some $`n`$ satisfies $`f(n,e)\ne0`$, induction over the finite distance to that witness gives conversion of the gate to $`I`$. The supplied witness need not be the first nonzero value: an earlier nonzero value also terminates the search. [R250-C27-231, `state_choice`, `state_halts`, `gate_halts`][R250-C27-231]

For a closed **pure** endpoint $`q`$ already currently typed at $`C_B`$, the gate applied to $`q`$ is then currently typed at $`C_B`$. The proof uses closed pure conversion and the original conversion rule, not an undeclared semantic-to-syntactic completeness principle. For an additionally currently typed endpoint $`r`$, the same halting witness gives

```math
\operatorname{BoolValid}(\operatorname{gate}(\operatorname{simFamily}(f,e))\,q,r)
\quad\Longleftrightarrow\quad
\operatorname{BoolValid}(q,r).
```

Purity is a premise on the endpoint being gated; the displayed theorem does not add that premise to $`r`$. This preserves the original endpoint equality as well as typing. [R250-C27-231, `gated_has`, `gated_valid_iff`][R250-C27-231]

The negative interface is explicitly conditional. If the observation at canonical input zero converts to neither Boolean choice, Boolean standardness contradicts current typing. The source does **not** prove that a nonhalting gate has this no-observation property. Therefore the finite positive proof is not a completed halting/typability equivalence, and the missing operational nonhalting argument cannot be replaced by the absence of a discovered finite witness. [R250-C27-231, opening scope notice and `noHas_of_no_observation`][R250-C27-231]

The independent gate interface makes the exact missing premise reusable without claiming to prove it. For fixed f, OperationalExclusion(f) says: if f(n,e)=0 for every n, then for **every** endpoint q and either Boolean b, the zero-input observation of gated(f,e,q) is not convertible to pick(b,zero,one). Assuming this premise, a currently typed pure q satisfies

- Has(gated(f,e,q):C_B) if and only if some n has f(n,e)≠0;
- BareValid(gated(f,e,simFamily(f,j)),constantChoice) if and only if (∃n f(n,e)≠0) and (∀n f(n,j)=0).

Here BareValid includes both scope conditions, both current typings and Boolean semantic validity. The reverse implication in the first equivalence is the earned finite positive gate theorem; the forward implication uses OperationalExclusion and Boolean standardness. The second combines this with the existing simulator test equivalence. OperationalExclusion is an explicit theorem parameter, not an introduced axiom, a proved negative gate result or a completed hierarchy classification. The exact input order is (n,e). Controls also check marker-free noncanonical counters, zero-bound positive witnesses and the failure of the purity/exposure correspondence for compound raw atoms outside its declared fragment. [S250-L395]

[S250-L395]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/66c18675d2bd703dd1afe8535840fd3bf2d71b4d9075216b9d45eff0c62adb4a/CheckGateInterfaces.lean

#### Finite witnesses and the judgments they inhabit

The pure gate fragment has an additional positive representation theorem: for closed polynomials built only from the primitive I, K and S atoms, exposing raw application structure lets raw conversion of their evaluations lift back to the unchanged polynomial conversion relation. The whole-opaque-atom obstruction of §10.3 does not apply indiscriminately to this exposed fragment. `EffectiveBooleanCertificates` then gives the exact negative witness for two closed **currently typed** N→B endpoints: invalidity is equivalent to a finite canonical input, two different Boolean observations, and their conversion certificates. The converse uses Boolean and Church standardness with both endpoint typings; it is not finite positive testing of all inputs. [T750-C673] [T750-C717]

The unary certificate judgment has all-context soundness, but its exact checker completeness concerns the empty-context compiled fragment. A context can contain an unequal identity and type its own assumption even when the numerical checker rejects the endpoints. Thus that example does not contradict empty-context completeness and prevents extending it to arbitrary contexts. Canonicality also matters to equality of **description data**: descriptions `[0,1],[]` and `[0,1,0],[none]` denote the same function but are not equal records. The corresponding attempted data equality is a rejection fixture. [T750-C703] [T750-C694]

The multivariate restricted checker deliberately permits reordered and redundant certificate rows when every mask has a matching row; an unused extra row can even contain contradictory data, as the admitted `good ++ [(s0, [(a0, 999)])]` control shows. It rejects incomplete, wrong-label and duplicate-only coverage, including failure to supply the single empty mask at arity zero. Sparse comparison sums repeated exponents and ignores zero contributions; dead variables are handled before branch selection. This certificate language differs from the strictly indexed body interfaces in the collective chapter, without conflicting with their theorems. Its completeness still concerns the declared finite expression grammar. [T750-C747]

The small negative interfaces preserve exact failure targets: `MissingJBaseDerivation` supplies formation but omits the base **typing** argument; `MissingLeftTyping` supplies the right endpoint's proof where the left is needed; `MissingObserverRepresentation` omits the computation-representation premise; and `RawToBoolCast` substitutes arbitrary raw typing for Boolean typing. `NoSyntacticIdentityCompleteness` attempts to turn a semantic checker equivalence into current `Has`; `ExtensionalIsNotCurrent` substitutes the extension's judgment for that current judgment. `RejectCarrierPromotion` asks a raw unit probe to establish the stronger carrier statement, while `RejectChangedEndpoint` changes the W endpoint in the scalar-fusion conclusion. These source-defined rejected applications are not additional independence proofs, and no new compiler rejection is asserted here. [T750-C678] [T750-C732] [T750-C718] [T750-C735] [T750-C692] [T750-C716] [T750-C725] [T750-C698]

[T750-C673]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b6201af0d80822607665139f8bf5d4194ba82104ef2ae55002686cfe1e58bed6/BareBooleanGateSyntax.lean
[T750-C717]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c1d0ffad7ea64205e54b342a343fdb80c0c1a5fbfe9f497875c8e774f21a0354/EffectiveBooleanCertificates.lean
[T750-C718]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c244f5b686b5d7a9048cc67178042f22474f8229c396a203f1f2ab91553ba907/MissingObserverRepresentation.lean
[T750-C732]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c6b2853424b12b8370fa0666f187c68720a15e758cd54348efb71621f1b2409e/MissingLeftTyping.lean
[T750-C735]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c785cfeb9ed9024ee425e6de10729f95f868c2ccf340122c0048e10e1776cb56/RawToBoolCast.lean
[T750-C725]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c3f78e7e06bdfcf714937ac00bd55969abbfa67a7e7e5d1aba8b04b9d88eb265/RejectCarrierPromotion.lean
[T750-C692]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bbb5c7372c2adfeea611779da933708b28450177d759bc7e0381f3c7655965f6/NoSyntacticIdentityCompleteness.lean
[T750-C716]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c1ba98538103ef2eecd62b0e309d7d494e77689c3967d81325e5088dd90eb655/ExtensionalIsNotCurrent.lean
[T750-C703]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/be852f8804bc85c743c298ac6ee3a50f44e9097af0785231c8e513d7dc2c359d/CertificateControls.lean
[T750-C678]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b6d61f6161a99bc1ce857f16878272bfac80cead756e0198bc58fecd8044ffb4/MissingJBaseDerivation.lean
[T750-C694]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bdceca0466bdf5a54dcf4962453415360ed3c03d65f4a562c82f36990cd5e7c0/CanonicalPremiseRequired.lean
[T750-C698]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/be410b79282a16f264dfe6f989c7bbf19153613b796afe76298e247bb4d79b37/RejectChangedEndpoint.lean
[T750-C747]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cb9ceffe348b298ff4d46883a731597440a428ac92394c4775d78624002c4efa/CheckRestrictedInterfaces.lean

Two additional short controls fix branch orientation rather than establish general independence. `WrongDiscriminatorOrientation` asks the canonical-zero Boolean discriminator applied to zero and one to return one, while supplying the canonical-zero observation theorem for the opposite branch. `WrongZeroBranch` asks the primitive-recursive chooser at control 0 with candidates 5 and 11 to equal 11 by reflexivity. These exact attempted equations preserve the discrimination contract; they are not successful observations, new computation results or claims that every alternative proof method has been ruled out. [F939-C904] [F939-C911]

[F939-C904]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f883051869b9385d2b0cf2047fdfe3972cf2272921e72eb3122ec09d7f96c753/WrongDiscriminatorOrientation.lean
[F939-C911]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fadb9286161236fa503b7730b98a857ad539e5eea2b683d4c783dfc8b2852016/WrongZeroBranch.lean

### 13.4 Proof audits, boundary controls and what their evidence establishes

The audit sources serve a different purpose from the preceding mathematical bridges. The Boolean audit maintains authored declaration and theorem inventories, examines the selected namespace's closure and axioms, and separately inventories unsafe or partial runtime auxiliaries. The all-project audit chooses theorem roots by their actual originating modules, rejects an empty selection, allows only the listed ordinary axioms `propext`, `Quot.sound` and `Classical.choice`, and traverses checked dependency types, available bodies, inductive constructors and recursor right-hand sides. It rejects unsafe, partial, unchecked or unapproved-axiom dependencies and refuses a traversal whose bounded worklist is not exhausted. This selection is not a claim to audit every file in an arbitrary repository or to verify the native compiler. [R250-C27-98][R250-C27-234]

The deliberately contaminated inputs distinguish the failure modes: an unsafe definition; explicit `sorry`/admitted proofs of falsehood; custom-axiom dependencies; and partial-recursion implementation dependencies, including the compiled `_unsafe_rec` rather than just a safe-looking public wrapper. Their role is to challenge the audit's rejection behavior, not to add their false statements to the accepted theory. The recorded sources identify these as negative fixtures. This consolidation does not claim that the auditor or those rejection tests were newly executed, and requested axiom listings are not received outputs. [R250-C27-12][R250-C27-13][R250-C27-85][R250-C27-94][R250-C27-125][R250-C27-131][R250-C27-146][R250-C27-179][R250-C27-200][R250-C27-233]

Other small controls preserve mathematical premises rather than audit trust: missing positivity cannot justify the sparse polynomial zero-test argument; reversing truncated subtraction changes its numerical expression; and index $`2`$ does not meet the bound for `Fin 2`. Their exact retained source bytes remain necessary to replay those particular controls. A readable account can absorb their substantive warning without treating a prose description as a replacement executable test or reporting an unperformed rejection as passed. [R250-C27-95][R250-C27-163][R250-C27-172]

The distinction between proof closure and runtime closure is substantive. The runtime auditor follows erased computational values rather than treating erased proof or type arguments as executable data. It rejects computational choice, admitted terms, unsafe or partial values, runtime axioms and unclassified opaque values; selected authored native replacements/externs are refused while inherited native boundaries are inventoried. Its 200,000-step traversal limit is fail-closed on an unexhausted worklist. Proof closure may allow the stated ordinary logical axioms without thereby authorizing noncomputable choice as runtime code. Neither closure is independent verification of compiler optimizations, foreign functions or replacement implementations. [R250-C27-187][R250-C27-169]

The additional closure probes exercise direct partial roots, partial definitions behind safe-looking wrappers, unsafe dependencies and custom or admitted falsehoods. They preserve the distinction between the checked declaration and its actual computational implementation. The opaque-control source requests audits of the selected unary roots and `normalise`, `distinguishingInput` and `Expr.closed`; those commands are not themselves an obtained audit result. The package explicitly identifies `Lean.opaqueId` as a permitted standard opaque boundary and records that the safe-looking public surrogate of a partial definition was an inherited known issue, not a newly discovered theorem. [R250-C27-3][R250-C27-20][R250-C27-32][R250-C27-41][R250-C27-56][R250-C27-57][R250-C27-65][R250-C27-96][R250-C27-158][R250-C27-167][R250-C27-236][R250-C27-247][R250-C27-77]

The retained scope declaration also distinguishes empty-context fragment completeness for `HasC` from its all-context soundness theorem with the original H/E compatibility assumptions. It does not change `Has`, `HasPlus` or `HasE`. Its accepted-map descriptions of inherited roots, unary checker/certificate modules, renewal/lookahead modules and the fixed-computable-matrix policy reduction are source-reported historical scopes, not new replay results. A computable callback theorem is not a native-code exporter or an arbitrary-program totality checker, and finite enumeration need not be lexicographic. Written hierarchy normal forms/strictness and upper bounds, syntax-total evaluator claims, randomized measure and population arguments, sparse-normalization variants, philosophical warrants, empirical claims and applications remain outside that package's kernel acceptance map. The tested Python JSON reference checker is not a proved refinement of its wire parser to the Lean checker. Exact surviving historical records, digest-only anchors and new archive verification have different evidential roles: archive assurance adds no mathematical theorem. [R250-C27-77]

The independent kernel-check source compares the old and Plus constructor signatures **after explicit renaming**, including `PolyConv` to `PolyConvPlus`. Its count checks are Ctx2→2, Form7→7 and Has18→20. The conversion constructors remain exactly refl, symm, trans, app, i, k, s and bridge. The two new Has schemas are specific:

- PiExt requires formed A, B under A::Γ and Pi A B; typed p and q at Pi A B; the pointwise family `Id B ((pren succ p) var0) ((pren succ q) var0)`, its formed Pi and a witness h; and the formed target `Id (Pi A B) p q`. It requires `Scoped Γ.length` for p,q,h, `TyScoped Γ.length A` and `TyScoped (Γ.length+1) B`. Its conclusion uses literal I as target identity evidence.
- AllExt requires formed B in `twkTel Γ`, formed All B, p and q typed at All B, formed `Id B p q` and a witness h in `twkTel Γ`, and formed target `Id (All B) p q`. It requires `Scoped Γ.length` for p,q,h and `TyScoped Γ.length B`; again literal I is the evidence.

The checker preserves the old F clauses, uses the axiom whitelist `propext`, `Quot.sound`, `Classical.choice`, rejects candidate axioms, and includes a declaration-count sanity check of at least156 candidate declarations. Unsafe compiler auxiliaries may exist, but no safe declaration's logical dependency closure may reach unsafe or partial declarations. The witness dependency graph must use piExt at `arrow_identity_has` and allExt at `separation_has`, without importing the has/form/fundamental soundness declarations as circular justification. Literal typing, separation and Raw-boundary checks remain distinct. These are concrete audit algorithms and theorem-shaped controls, not fresh successful audit logs; reading them changes neither the original/bridge/extensional judgment distinction nor their evidence status. [F250-138]

The distinct structural DependencyAudit has a narrower contract: constructor counts2/7/20/8 for CtxE/FormE/HasE/PolyConvPlus; only propext and Quot.sound in Structural.form_mixed; no old-judgment or semantic-fundamental shortcut; and positive dependency checks for the mutual formation recursor, extensional/J/conversion constructors and both substitution lifts with theta. Four chosen theorem values must each contain exactly one direct occurrence of the designated constructor. These are specified checks, not obtained PASS output, full signature comparison or runtime closure. [baseline141 source 10](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/02f1f2d7ea88a9d732799b0a38dcc2e5f93dcc9e0b1b5a250103ba97801dc72c/DependencyAudit.lean)

The initiality-specific DependencyAudit asks a narrower ancestry question. A visited-name traversal follows each found declaration's used-constant set; for appE_arrow and composeE it rejects the FullPER, HomogeneousOriginal, GenericFoldTransport and RigidityDiscriminator name families, the exact SourceFoldContract.SourceNaturality name and SourceRigidity.q_ names. For the two internal-uniqueness noninhabitation roots it instead requires the corresponding rigidity-discriminator ancestor. Missing names receive no further traversal, and the file supplies neither a general axiom allowlist nor a fail-closed complete-environment audit. Its printed PASS strings are conditional program output, not received results. These exact selected-root positive and negative dependency obligations must be retained separately from the broader audits and from the mathematical independence statements themselves. [T33-098](../research/t20-v6-20261012/sources/f5f3c76d033ec77c982ca4a56f7df8a7462371371a84833f76d9448af9c2db69/DependencyAudit.lean#L1-L22) [T33-098](../research/t20-v6-20261012/sources/f5f3c76d033ec77c982ca4a56f7df8a7462371371a84833f76d9448af9c2db69/DependencyAudit.lean#L24-L32)

The closed-scalar DependencyAudit deliberately requires a new semantic dependency rather than banning all semantics. Its seven roots exclude fifteen exact old semantic, standardness and canonicalization declarations and permit only propext, Classical.choice and Quot.sound. All roots except generic_conversion_reflect must visit FullPER.fundamental. The final closed_scalar_instance_exact root must also visit the named scope and formation results, generic reflection, open-term Church standardness and the conv, identityIntro, piIntro and allIntro constructors of HasE. These are transitive visited-name requirements, not direct constructor counts. The displayed code supplies neither an unsafe/partial/runtime-closure test nor received PASS output, and it must not inherit another audit’s stronger or opposite dependency contract. [SUB250-FINAL28-217](../research/t20-v6-20261012/sources/778572c92739416d539d23082a9f5d1cbf697271787e407854c7a82eaaf2a0ce/DependencyAudit.lean#L5-L48)

The retained closed-identity audit has a different, explicitly narrower set of checks: HasE20/FormE7, two direct piExt occurrences and one allExt occurrence in the identity construction, actual closed weakening for canonicity, semantic same-index dependencies for the negative direction, and Nat.find/readIteration dependencies for the decision procedures. Its J-built input separately requires one direct J occurrence. The development/certificate audit distinguishes triangle/cofinality-based development, terminating extraction, finite positive certificate replay and negative noniteration refutation; it excludes semantic standardness, extraction and Classical.choice from the positive source-certificate path while requiring standardness in the negative path. The two simpler ancestry traversals are weaker still: one exempts rigidity_uninhabited from the generic-semantic forbidden-name check, while the other excludes named semantic prefixes from five source-section roots. They silently stop at absent environment entries and impose no axiom whitelist or runtime-closure test. The graph audit excludes listed semantic helpers from construction roots but only checks axioms for its two projection-boundary roots. All these are specified checks and output templates, not received successful audits, and direct Expr occurrence counts are not transitive dependency counts. [research/t20-v6-20261012/sources/213b7978e34bb8a615b2e61a43be7430f80fbd404e57c80ee59eb4b45873011f/DependencyAudit.lean:15–77 at ffca0abdf25079ef7639fe19776a21db60272fc4] [research/t20-v6-20261012/sources/250045a376926f52a32144708c9d34ae1067a8b40f632a6cf372404b2d77d2f1/DependencyAudit.lean:6–54 at ffca0abdf25079ef7639fe19776a21db60272fc4] [research/t20-v6-20261012/sources/1c372a7bb0032881c92171d623f7630b43c3487ad4b26e14c74b4ac368293651/DependencyAudit.lean:4–24 at ffca0abdf25079ef7639fe19776a21db60272fc4] [research/t20-v6-20261012/sources/2ea7e39dd10e2e73cd2cb606fbd4f2abdf5f73ad141f06588df7c89441aa1e93/DependencyAudit.lean:4–25 at ffca0abdf25079ef7639fe19776a21db60272fc4] [research/t20-v6-20261012/sources/3a26ba10146c8375caab832b040c9b1f3d95081cda4fcd66c70712a2948009bd/IndependentControls.lean:88–120 at ffca0abdf25079ef7639fe19776a21db60272fc4]

The separate ProofUniquenessAudit has ten positive and four negative roots. All fourteen use the axiom whitelist propext, Classical.choice and Quot.sound, but only the positive roots additionally exclude six exact semantic or completion declarations. Each of the old-E and Joint identity_contract roots must visit either HasE.j or HasJ.j; this OR check is transitive name membership, not a direct constructor count or a requirement that each root visit only its own judgment's J. A subsequent loop prints imported module names. The displayed code adds no explicit unsafe, partial or runtime-closure check, and its PASS strings and module listings are requested outputs, not obtained audit results. [SUB250-R81-126](../research/t20-v6-20261012/sources/65cd1a0baeb08f6777bddd581b8b740193aace2c5eb5dc700cb7f605f110e688/ProofUniquenessAudit.lean#L6-L45)

The type-indexed Dependencies check has a different contract again. Its fixed roots cover constant-family and discriminator source controls, family obstructions and structured observations. It first requires each root to exist, restricts its collected axioms to propext, Quot.sound and Classical.choice, and rejects visited dependencies on the listed semantic-fundamental and closed-scalar standardness/identity shortcuts. Six selected roots must additionally visit their designated source routes: reabstraction and diagonal elimination, identity introduction, the structured Sigma/Pi/application observation route, and the raw normal-form/numeral/abstraction route used to separate observations. These are transitive membership requirements, not direct constructor-use counts or an automatic complete inventory. This file specifies neither the stronger unsafe/partial/runtime checks nor an observed successful run. [source 214](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/42e984534be66fd66ee2d5b006c1506ad14b607827e0fcf7ea86d2fc05fbc1bf/Dependencies.lean#L10-L98)

The recovered-package scope record distinguishes three restoration bases:111 mathematical modules matching historical digests;167 of220 historical fixture slots matching retained digests;52 restored from complete original write/patch payloads without old digests; and one regenerated finite fixture with repeat-generation evidence. Four integration-auditor controls were new. Its reported staged verification is not the separate fresh-extraction author/independent archive replay needed by that package's delivery scope. These historical counts characterize that source package, not current repository totals or a fresh replay performed by this consolidation. Readback and required-interface files identify the declarations to inspect; contaminated audit fixtures remain deliberate rejection inputs, not accepted scientific propositions. [S250-L386]

[S250-L386]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/64509a4f5bafcea6e6e7ed26dfea4d31ef42f10bbc701582b7642ae8dead5c81/RECOVERY_SCOPE.md

The additional exact audit providers preserve these distinct targets. `ComplexityKernelAudit` inventories authored declarations and theorems in the effective-completeness/identity-complexity namespaces, checks their kinds and safety, and follows checked type/value dependencies. `RestrictedKernelAudit` selects the restricted-identity roots and requests six closure checks. `CheckerKernelAudit` separately names checker, normalizer and certificate-theorem closures. Unsafe or partial compiler auxiliaries are inventoried outside the safe-root set, not silently accepted as logical dependencies. Their program strings containing PASS are templates for possible output, not obtained audit evidence. [R750A-517] [R750A-518] [R750A-565]

TaggedInductionAudit requests a different transitive dependency check for dependent_induction, hereditary_nat and dependent_induction_sound. It permits only the three standard logical axioms and checks that the visited closure excludes JointCompletion’s sigma eta, sigma elimination and dependent induction, and FullPER’s F, TypeLaws, Fundamental and ContextLaws. Its PASS message is an output template, not a received result; this check must not inherit the stronger runtime or opaque-boundary rules of other auditors. [B141-064](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/0d3389e05e1be87cffb10898366501638554f23f13b6e3e93805255b2e74ad8d/TaggedInductionAudit.lean)

SourceSearchAudit has a narrower effective-search contract. Its fixed list of 29 roots covers serial and canonical checking, six source judgments, derivability search and inhabitant search. It collects each root’s axioms, permits only propext, Classical.choice and Quot.sound, and rejects visited names beginning FullPER. or exactly JointCompletion.fundamental. The latter is an exact-name exclusion, not a ban on the entire JointCompletion namespace. The visible loop does not add the stronger auditors’ unsafe, partial or runtime-closure checks. Its PASS text is a possible log message, not an obtained audit result or a proof that an unbounded search terminates. [SUB250-C9-020](../research/t20-v6-20261012/sources/51ab1d20c81ca13999d8745bcd4464b0b80df9e95470917889521daf55eb301b/SourceSearchAudit.lean#L3-L42)

Two exact adversarial inputs challenge the computational boundary: a directly partial self-recursive root submitted to the unary opaque audit, and a partial lookahead loop hidden behind an ordinary-looking wrapper submitted to both renewal audits. These preserve the direct-versus-transitive rejection obligation already explained above. No rejection or clean audit execution is newly claimed. [R750A-500] [R750A-531]

[R750A-500]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/86053cf85b07c5b22d501c200c57653eb73d0054d9223756759decd7139cb96d/PartialRootGuarded.lean
[R750A-517]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/891130121cb6e9eb6c7223d7e2b829fedd9dced84158885d6c4e9ad40b7f9da7/ComplexityKernelAudit.lean
[R750A-518]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8946929b92c08c02390452296effaef33efd6e5eb84dba6302093061967977c9/RestrictedKernelAudit.lean
[R750A-531]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8d987ed9ba5f3f970c86e75c73cccb7744052671a975f186051d2f1f040b8133/PartialWrapped.lean
[R750A-565]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/987c8dc902a4ffd41ed8542a20ef35f22789f245927958e01863a8f10cf2a975/CheckerKernelAudit.lean

The additional audit bodies sharpen those evidence distinctions. `RestrictedComputationalAudit` and `UnaryOpaqueBoundaryAudit` inspect checked types and values, inductive constructors and recursor rules, reject unsafe/partial dependencies and fail if the bounded traversal remains incomplete; the latter explicitly allows `Lean.opaqueId` while rejecting other opaque boundaries. `UnaryProofAudit` selects authored safe unary declarations and theorem roots, separately counts unsafe/partial auxiliaries, and requests closure checks for normalization, identity checking, certificate completeness, distinguishers and expressivity. These are executable inspection specifications, not the results of running them in this consolidation. [T750-C682] [T750-C705] [T750-C723]

`CombinedAxiomAudit` requires 156 constants in the extensional-repair namespace and separately verifies the theorem kind of eleven decisive declarations; it does not call all 156 constants theorems. Its whitelist is `propext`, `Classical.choice` and `Quot.sound`. The two custom-axiom poisons make a false theorem directly or through an intermediate bridge and request the respective auditor to reject that transitive dependency. They contribute rejection targets, not trusted theorems of falsehood. The selected `sixteenth_recovered` package lists its build roots and pins Mathlib to `c44e0c8ee63ca166450922a373c7409c5d26b00b`; that configuration is not a build receipt or evidence that every listed root was rebuilt here. [T750-C685] [T750-C704] [T750-C715] [T750-C680]

[T750-C680]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b7c139548d9e3417149723c5f2568e0956f369fe2a11fb736d4c5ea801f30826/lakefile.lean
[T750-C682]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b7d9414161ba3faa975b5c8719691d6039762fc0832e19efda152f3b893ff325/RestrictedComputationalAudit.lean
[T750-C685]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b89fb44ce3c9029c708889ad58df13142edfbc6ca4c9b61635a4d14aef0939a5/CombinedAxiomAudit.lean
[T750-C704]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/be94aa2c9267283d67a1976cf8b1f2bd531691ad674ff4c93cc67652ed8fe7ab/RejectCustomAxiom.lean
[T750-C705]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bf1a275a68a0a3bda342b38e167fd6931b7c14162a6ca33fe7bd1f739b771d00/UnaryOpaqueBoundaryAudit.lean
[T750-C715]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c16fbb7788cb655e99575b3dfccb6e31b38ec0d6f4bc7993e6f2d83ee44c2d2b/AuditorRejectsCustomAxiom.lean
[T750-C723]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c3a90f6f6616f227f2fd2b4a5266d07fc51b69f290bcd21bc829fb276ebc7dd2/UnaryProofAudit.lean

The two selected `KernelAudit` bodies have a material difference. The effective-observation version traverses checked types, available kernel values, constructors and recursor rules and **logs** reachable opaque declarations. The renewal version additionally rejects an unclassified opaque declaration while permitting the named standard `Lean.opaqueId` boundary. Both reject unsafe/partial or unapproved-axiom dependencies and an unfinished bounded traversal. A matching basename therefore does not establish the same opaque-boundary policy, and neither program is a compiler-IR or foreign-implementation audit. [F939A-754] [F939A-796]

`IndependentRootAudit` strengthens direct-root qualification: each enumerated unary root must exist in the checked environment, be safe and total, non-axiomatic, computable and free of an `implementedBy` redirect; the declared theorem sublist must actually contain theorems. It checks the allowed logical axioms, invokes closure, and refuses an unsafe/partial theorem hidden among excluded auxiliaries. This is stronger than a bare namespace census, but its frozen list is not automatic complete module enumeration. [F939A-799]

That latter coverage duty has a separate provider. `CompleteInventory` verifies every declared project module is imported, selects declarations by their **defining module**, includes every theorem in those modules, forbids unsafe/partial theorem exclusions, records nonproof auxiliary exclusions and invokes full logical proof closure. `ExportDeclarationInventory` uses a narrower declared module list and writes declaration flags without those completeness and closure checks. Its inventory cannot substitute for the former audit. These are source-inspected programs and their intended outputs; no inventory PASS, closure result or expanded kernel-acceptance scope was obtained by reading them. [F939A-778] [F939A-792]

[F939A-754]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cd31c9d6321bbfd35eea813b6648b74d36ddddc8314d599f912dd718a94cb8e1/KernelAudit.lean
[F939A-778]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d46fd11733381c62f45834e4cb3bac32a7bf8a27fefcb5b8aa7f5b3ffe1c1f16/CompleteInventory.lean
[F939A-792]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d8cc868cfb48b5db265771fcccf9ff4b0fd902d35ac50be24800133d01dbe048/ExportDeclarationInventory.lean
[F939A-796]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d91f1cd81936546e251d3bcc24e995e7a9b641308e86731fd881f06fd24ffb03/KernelAudit.lean
[F939A-799]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d985a39f125d6e82b3643da687a8bfc32f59e469466077ba70c372de875e816e/IndependentRootAudit.lean


<a id="final189-b13-exact-audit-surfaces"></a>

Three further audit sources retain distinct selection mechanisms. PolynomialTestAudit enumerates safe declarations in its polynomial-test namespace, inventories unsafe/partial auxiliaries separately and requests closures of eight named semantic/checker interfaces. The intensional AxiomAudit instead supplies an explicit fixed array of theorem names across its frozen modules, checks each declaration really is a theorem and rejects transitive axioms outside propext, Classical.choice and Quot.sound. Its name-list is not an automatic census of every future declaration. The hidden-change AllAxioms source is a readback driver covering count/contamination, fixed/adaptive-law transport, posterior/restart, no-leakage and prefix/tail interfaces; it requests axiom output rather than implementing either of those audits. Their embedded PASS strings and print commands are not new clean-run receipts. [F189B-815](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dc023592bde318b10ef03b71d3ba952f51c573b05b021ee35f3cff4bedddd365/PolynomialTestAudit.lean) [F189B-864](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/eb7b45593a3248d8166f47dbf4d7f30f51218d92bc91264c322e6ebaa53a2173/AxiomAudit.lean) [F189B-820](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ddaf736552460936cfe6bd50a26b6b85325be60c683eefb668e8d7b20c218822/AllAxioms.lean)

#### Recovered-source orchestration retains distinct proof obligations

The recovered core wrapper supplies concrete custody and execution contracts beyond a list of accepted theorem names. Its 111 mathematical modules retain frozen bytes, while the post-reset Python wrappers and complete-inventory wrapper are newly authored integration work. The source-lock checker requires 111 distinct module names, an exact top-level mathematical-source census, every declared mathematical and packaged-control hash, and the whole package file census outside the declared dependency area. It refuses package symlinks and Python optimisation that would disable its assertions. These are identity and wrapper-precondition checks, not proofs of the mathematical modules. [Q250B-073] [Q250B-074] [Q250B-076]

The compilation wrapper recursively builds packaged imports into absent output directories outside the source package. It constructs its own project/inherited/dependency search path, records the source, log and new-object hashes, and checks the frozen mathematical hashes again after compilation. The control stage then checks that every object it consumes still matches that build receipt. This establishes an intended chain from selected source to newly produced project objects to the controls actually run, rather than treating a similarly named old object as a new build. The wrapper source is inspected here, not executed. Its historical receipts remain distinct evidence. [Q250B-075] [Q250B-079]

Namespace placement is consequential. The inherited verification support is compiled into one coherent namespace directory because Lean resolves a namespace prefix in the first existing directory; splitting siblings between later search roots can select the wrong support or fail to find one. The renewal and policy auditors keep their identical bare names in different lanes, and lookahead explicitly sees its own lane followed by renewal. These arrangements preserve the intended dependency identity instead of claiming that a shared filename identifies the same checker. [Q250B-073] [Q250B-079]

The constructor-retention check compares the actual packaged AllSyntax and UnaryCertificateSyntax mutual grammars after restoring only the three judgment names and removing the declared certificate constructor. It requires inherited counts 2/7/18, the original PolyConv relation, and the executable certificate guard. The independent coverage check equates proof roots with **all** theorem declarations in the exported inventory, disallows theorem exclusions, limits auxiliary exclusions to unsafe or partial nonproof declarations, and checks the acceptance-map source identities and family membership. Exact grammar retention, complete theorem coverage and full logical dependency closure are separate obligations; a count alone cannot establish all three. [Q250B-076]

Negative controls likewise require more than a nonzero exit. The orchestration checks the expected diagnostic patterns and rejects missing-module, missing-object, unknown-name and unreadable-file failures remaining after the intended patterns are removed. Positive controls require success, no reported error and all specified success markers. A timeout or infrastructure failure therefore cannot be silently counted as the intended mathematical rejection. Original support/positive/negative fixtures, new integration controls, complete inventory and Python references have different recorded roles. The complete entry point runs their sequence and rechecks source and dependency-object bindings; the source-only branch stops after integrity checking. Its full-replay success marker cannot be inferred from an integrity-only pass. [Q250B-078] [Q250B-079]

The exact dependency helper is the official-cache route: it obtains nine pinned clean source checkouts, validates the transitive revision relation and version-pinned release tag, then requests cache objects for the selected imported Mathlib roots in a new preparation directory. It explicitly disclaims a source cold build. The full core replay verifies pinned clean sources and hashes each required prepared dependency object before and after the project run, but those runtime hashes are a binding for the objects used, not a source-to-object equivalence proof. The later detached assurance described by the verification guide is different evidence: it reports rebuilding the 1,369 required third-party modules without prior third-party proof objects and then replaying the unchanged core. The five project inventories and 226 control/audit contracts agree with the earlier prepared-cache route, while fourteen differing dependency-object byte strings remain unexplained. Neither route bootstraps the official compiler or establishes native/FFI correctness. [Q250B-077] [Q250B-078] [Q250B-058]

The unary regression generator also has an exact, limited role. With its fixed random seed it constructs 64 depth-at-most-three source trees, evaluates each independently by recursion at inputs zero through ten, and emits three Lean assertions per tree: those eleven expected values after normalization, equality under adding zero, and normalize-after-reification idempotence. The conditional evaluator selects the third child on equality and the fourth otherwise, so it directly checks the branch orientation in the generated examples. These 704 finite values and 128 structural comparisons corroborate interfaces if executed; the universal normalizer and completeness results still depend on their kernel theorems. No generator, generated regression or compiler was run for this reconciliation, and its already retained generated body remains a separate replay dependency. The complete reader keeps sparse written algorithms separate from the checked dense implementation, and keeps conditional all-context HasC soundness separate from closed-family completeness; the existing mathematical treatments in §11 are retained without changing those proof levels. [Q250B-080] [Q250B-070]

[Q250B-058]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a9fbe1d74a790020862fb39a37cb2951131d63f09779e60c9dd57b1c77188408/VERIFICATION_GUIDE.md
[Q250B-073]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0aaa903908711262e9bc509d5484084c6cb8ac1748d92c00800a30d45cfd37c1/INTEGRATION_CHANGES.md
[Q250B-074]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ab95d684c03c6921a2cc1dfe92dcaf39949da97c15bf9e76853758abaf7015a3/README.md
[Q250B-075]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c9685593161cae3448cdd174355c2ccdaa63fece538a7d1c601b5a62e8396b86/compile_project.py
[Q250B-076]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/17f158ed734a570a6821a90631099925d50ed4201bb297844f8b2a6ae1bf6f81/package_checks.py
[Q250B-077]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1f67912e54d5977e3dc1c1c5d1bed78cfe5b58aff8683ff334c25096b4cf7214/prepare_dependencies.py
[Q250B-078]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/52a240909b4b1c3f5fbd6a749e71e286afa265191c746b909f32a20335e34c06/replay.py
[Q250B-079]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/60b8715511ff8d269f5629501ec98c8bfc13e3482183557af5a0836953702d72/run_controls.py
[Q250B-080]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6d9fb42f6ab653e41d601dfd199711c27ed72b603c591b075286c57283d3a0ea/generate_regressions.py

[Q250B-070]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/10903b3260522cec902c7213a1b93a2c3280922126994c76f95755baadc2a91e/FULL_READER_TEXT_v5.md

## 14. Arithmetic interfaces and exact expression-machine refinement

### 14.1 Sparse coefficients and the positivity required by zero tests

A sparse natural polynomial is a finite list of pairs `(a,c)`, with exponent vector `a : Fin r → Nat` and natural coefficient `c`. This representation admits repeated exponent vectors and zero coefficients. Its meaning is the sum of the corresponding monomials, so equality of lists is unnecessarily strong and equality of their exponent supports is too weak. The effective coefficient comparison aggregates all entries at each exponent. It checks the exponents occurring in either list; any absent exponent has coefficient zero. The source proves that this comparison holds exactly when the two represented multivariate polynomials are equal. Appending represents addition, while the distributive multiplication routine adds exponent vectors and multiplies coefficients. Neither operation needs to discard duplicates before the semantics is correct. [F250-153]

The zero test has a stronger premise than general polynomial evaluation. If every supplied coordinate is strictly positive, every monomial value is positive. With natural coefficients, there is no cancellation. Thus the represented polynomial evaluates to zero at that valuation exactly when its aggregated coefficients all vanish, equivalently when the mathematical polynomial is zero. At a boundary valuation containing a zero coordinate, a nonzero monomial can vanish; with signed coefficients, cancellation can make a nonzero polynomial vanish. Neither case is covered by this argument. The formal `SparsePolynomial` interface proves coefficient and zero-test laws; using those laws in a larger normalization or complexity theorem requires the additional language and proof of that theorem.

The exact short controls keep coefficient equality separate from one evaluation. `ZeroAtZeroIsNotZeroMap` asks the sparse monomial x to pass the zero-map test; vanishing at zero cannot justify that assertion. `ForgedCoefficient` instead asks coefficient5 to equal coefficient4 at the same exponent. Both are adversarial source assertions, not accepted arithmetic results or observed rejection logs. `PolynomialRequired` only names unary trimming, evaluation, addition/multiplication and finite-bound/all-input equality interfaces; its `#check` commands neither prove those results again nor establish current runtime behavior. [R750A-521] [R750A-575] [R750A-581]

[R750A-521]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/89da87d537047b1be2ce42efe8ea3a6f451d52ca24c3dd2b97d6d6e566976529/ZeroAtZeroIsNotZeroMap.lean
[R750A-575]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9a33b4258625be160bacfee4163903681799d3c678b57b1fb11ea91ae478eb91/ForgedCoefficient.lean
[R750A-581]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9be4655b4ec9255d72b5bcd6bec84b5b64edd5e6f8bc9a6f19f9c6db070a90e0/PolynomialRequired.lean

### 14.2 Arithmetic compilation preserves the question being asked

The auxiliary arithmetic language contains natural constants, variables, addition and multiplication. The root extension retains the imported expression grammar through `Root.old`; its new constructor adds only a root equality test between two auxiliary arithmetic expressions, with literal outputs1 and0. Thus the whole root language is not restricted to arithmetic alone. Primitive-recursive predecessor, reverse subtraction and equality implement the numerical operations in the declared argument order. Compiling and closing a root expression supplies an actually typed endpoint at the finite-arity curried natural carrier. The observation theorem relates that endpoint to its numerical denotation for represented input tuples. [F250-101]

For the formed, closed identity endpoints compiled from two root expressions, endpoint validity is equivalent to equality of their denotations at **every** valuation. The corresponding original F-identity, G-identity and semantic-witness statements retain that universal quantifier. In particular, the root test comparing arithmetic expressions `p` and `q` is equivalent to the constant-zero expression exactly when no valuation makes their values equal. This is an exact semantic reduction for the specified syntax. The module does not itself supply DPRM, a universal Diophantine representation or an arithmetical-hierarchy classification. Written classifications using such results must retain those additional premises, rather than attributing them to this compiler interface alone.

The expression-to-primitive-recursion interface retains the exact argument discipline. A recursion step receives counter, accumulator and parameters, so its arity is two greater than the base function's arity. Successor state updates both the counter and the recursive value. Closing r variables and then applying the canonical argument list uses the source's reversed list order to recover the intended valuation; this is not an arbitrary permutation. At arity zero the curried target is N, not an extra function arrow. Extensional correctness compares related argument lists with their membership premises, rather than silently replacing that relation by literal equality of raw lists. [S250-L312] [S250-L456]

Positive-grid separation quantifies over **every strictly positive integer vector**. The proof passes to an integer polynomial difference and uses univariate root finiteness inductively; a single positive valuation does not suffice. Zero coordinates require the separately normalized mask cells. The associated controls preserve complete mask coverage even at arity zero, reject duplicate rows used in place of missing masks, and reject exponent entries for inactive coordinates. A certificate for one expression pair does not certify an externally supplied different pair, and compiled-endpoint equality does not bind unrelated endpoint variables. The unary distinguishing-input routine searches downward through its finite bound: its certificate is a valid distinguishing input within the bound, not necessarily the least one. [S250-L495] [S250-L341] [S250-L340] [S250-L380] [S250-L398] [S250-L437] [S250-L484] [S250-L487]

[S250-L312]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/52d39087b9c1eaf316c497cb265bc34f41a290a9b091e70f8458a98b842e4eba/EffectivePrimitiveRecursion.lean
[S250-L456]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7a29142ab5f29a1b213aff3481fd8926b9ff1811fee31e429f18cd5d1e93ce30/RestrictedCompiler.lean
[S250-L495]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8428453cf8d75c20aea651038cbb5d0b95096c5915f2026de7283dd86cd7ead8/PositiveSeparation.lean
[S250-L341]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5b389da5396383c6fc987c3733ff7b5728ad255dc3a9b2fddfe69f12189e9144/UnaryWitnesses.lean
[S250-L340]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5b2697880020f84e5974a58970e875ecd3711abf605345b75c2a1eb2ef81a444/EmptyArityIsNotVacuous.lean
[S250-L380]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/62a85803b72e56ae6ce845639b61f66de6e2f6fb87a075cb95d1d56ebf0f4e71/INDEPENDENT_DuplicateRowsCannotCoverMasks.lean
[S250-L398]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/678a22f1dede68b426d32212cd547063bd126fb8e9b8c5b0529118f19e3c1355/INDEPENDENT_DeadExponentForgery.lean
[S250-L437]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7571f83ef0c48cc705337cf3c661169f39739748c1c1a99c0fbc4d9b9a493693/EmptyZeroArityCertificate.lean
[S250-L484]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8028ba1ddd151269dcf555a48b97706dfef424453e51f01ecf3e96ede14e210c/INDEPENDENT_ExternalPairMismatch.lean
[S250-L487]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8193143b6a315cdf4c0817d629e50673be3b020884a290f056cfc8a5c58ba59a/UnaryMissingEndpointBinding.lean


<a id="final189-b09-literal-checker-grammar"></a>

The exact multivariate checker controls cover piecewise identities across zero masks, forged coefficient data, aggregation of repeated monomials, inert zero coefficients, nested zero products, absent variables and the inhabited zero-arity assignment. Those cases preserve semantic coverage rather than demanding an unrelated unique row ordering. Two short negative interfaces test different syntax boundaries: the pure Arithmetic grammar has no ifZero constructor, whereas a variable in Expr0 would require an impossible Fin0 index. Availability of zero tests in the larger expression language does not add them to the narrower arithmetic grammar. The source contains evaluation probes, but their output and rejection were not regenerated here. [F189B-848](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e6d5b8b58cd4b7d2444d2b34f3f8ce585f6455068d5fa5ee1dc75529952fa537/CheckerControls.lean) [F189B-853](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e8797ee367c6695f405df193e270668acf8aae5059c7f981265dc760d1470f95/NoPureZeroTests.lean) [F189B-861](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ea29fb0d4fba7068615951c0f8421b3627304aed933801a6943e4a475d2f5a73/InvalidVariableIndex.lean)

### 14.3 A stack-machine refinement includes faults and the continuation

A separate expression evaluator uses a work stack of expression/ready pairs, a value stack and a meter. A step with nonempty work ticks the meter before doing the selected operation, including when the expression is already marked ready. A step with empty work leaves the configuration unchanged. The expression grammar's natural-number operators include truncated subtraction, division with value zero at zero divisor, modulus with `a mod 0 = a`, comparisons returning0 or1, and powers of two. These are the model's declared operations, not a claim about every host language's exception semantics. [F250-117] [F250-242]

Let `cost(e)` be the source's exact syntax cost. For arbitrary pending work `tail`, preexisting values `vs`, dictionary `d` and initial meter `m`, the central refinement equation is

```text
runSteps(d, cost(e), ((e,false)::tail, vs, m))
  = do (v,out) ← reference(d,e,m)
       return (tail, v::vs, out).
```

The equation is equality of the result type, not merely equality of successful values. On failure it preserves the complete failure record, including fault kind and tick. Splitting a run after `cost(e)` therefore gives the continuation equation for any additional number `n` of steps: first perform the reference expression computation, then continue from the unchanged pending work with its one new value. This does not require the pending work or preexisting stack to be empty. [F250-117] [F250-242]

For a well-formed expression started through the expression wrapper, success returns its source numerical denotation and increases the step counter by exactly `cost(e)`. With no resource limits, evaluation succeeds. More strongly, for each fixed expression, dictionary and starting count, the source supplies finite bounds using `starting count + cost(e)` and `neededBits(d,e)` that suffice for success. This existence result neither promises a fixed bound uniform over all inputs nor identifies these abstract ticks with wall-clock time or machine instructions. [F250-117] [F250-242]

Failures of the well-formed expression wrapper can only be step-limit, integer-storage or exponent-storage failures. Value-stack underflow and stack-invariant failure are excluded at that wrapper interface; they are still possible for arbitrary malformed machine configurations. Any two successful budget settings return the same numerical value. The safety theorem does not assert budget monotonicity or turn a resource refusal into a mathematical negative answer. [F250-215]

The typed command runner extends this budget distinction beyond a single expression. Its remaining summary separates task pops, meter ticks including embedded expression work, and maximum width at actual check sites. Fits is preserved after each successful task step; induction on remaining pops supplies a finite completing run with the input-specific tick and width bounds. Neither initial stored values nor unchecked loop writes acquire a new width bound. The API checks arity, loads successive natural arguments into registers with zero elsewhere, and separates arity errors, modeled resource errors, pending mathematical fuel and successful observations. Tracing adds count and events without changing the successful value, which agrees with the lowered command semantics. These dependency-relative source statements assume already valid typed natural inputs; they do not certify Python validation, host resources or a uniform cap over all inputs. [NEXT-R11-041](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/22d6a114e41808e2f133efde90cc7312e1f34b919c341568c8ed31c1caf349d1/PythonRunnerBudgets.lean#L6-L164) [NEXT-R11-171](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3bdd06b2ba0f70246aeb4bd7333d801b5364b2e76c2a1ad17a89767b7e9dced3/PythonRunnerAPI.lean#L6-L140)

The runner syntax preserves a variadic Seq as an explicit finite list, scheduled in source order ahead of the pending tail of its head-top task stack. Its ideal summary composition threads the resulting store, concatenates chronological events, adds pops and ticks, and takes the maximum checked width. Associativity and the append/scheduled-summary equations let a command list be composed with an arbitrary continuation without binary reassociation of the source syntax. A loop captures its entry count, writes each loop index before the body, and still charges the terminal repeat task one pop and tick. This is an input-specific mathematical summary, not a practical preflight estimator, a bound on all stored values, or verification of the Python frontend and host. [NEXT250-Y25-154](../research/t20-v6-20261012/sources/9c3d3a803aeeb8e96de17d80ac3b91001d18a2cc886398383de71f7da5420186/PythonRunnerSyntax.lean#L11-L43) [NEXT250-Y25-154](../research/t20-v6-20261012/sources/9c3d3a803aeeb8e96de17d80ac3b91001d18a2cc886398383de71f7da5420186/PythonRunnerSyntax.lean#L45-L90) [NEXT250-Y25-154](../research/t20-v6-20261012/sources/9c3d3a803aeeb8e96de17d80ac3b91001d18a2cc886398383de71f7da5420186/PythonRunnerSyntax.lean#L92-L126)

The runner’s machine layer makes the budget proof’s conservation law explicit. A successful step from a nonempty task stack preserves the final summarized store, the accumulated events followed by remaining events, and spent ticks plus remaining ticks; it removes exactly one remaining outer-task-pop obligation, does not increase remaining checked width, and leaves both configured limits unchanged. This is not a claim that the runtime stack length decreases: entering a repetition schedules its body and continuation. Each outer task is ticked before its case is handled; embedded expressions use the same meter, repetition index writes are untraced, and the terminal repetition pop still consumes its step. The zero-valued branch selects the false arm. Mathematical fuel exhaustion returns pending rather than semantic zero, while modeled resource errors retain their category. The accounting proof relies on the supplied expression/reference and command-summary equations and does not execute Python or certify host resource usage. [NEXT250-Z50-248](../research/t20-v6-20261012/sources/adc9cf1332fbbcc410bcdfd54b7e8206eaf1c34c845a5011be3c6c2cdcec04b1/PythonRunnerMachine.lean#L12-L61) [NEXT250-Z50-248](../research/t20-v6-20261012/sources/adc9cf1332fbbcc410bcdfd54b7e8206eaf1c34c845a5011be3c6c2cdcec04b1/PythonRunnerMachine.lean#L66-L85) [NEXT250-Z50-248](../research/t20-v6-20261012/sources/adc9cf1332fbbcc410bcdfd54b7e8206eaf1c34c845a5011be3c6c2cdcec04b1/PythonRunnerMachine.lean#L86-L163)

The concrete controls fix details that a value-only paraphrase would lose. A register read can return a large preexisting dictionary value with zero new integer-storage allowance, whereas construction of a constant or arithmetic result is checked. A missing register reads zero, and writing one key retains other keys. The tick occurs before a ready-state underflow check, so an exhausted step budget can take precedence over that stack fault. In the power example with exponent8, a bit allowance8 yields an exponent-storage fault at tick3 while allowance9 permits256; an insufficient step budget instead fails at tick3. Swapping subexpressions can change which resource fault occurs first. These are specified source controls, not fresh observations of CPython. [F250-242]

Two intentional mutations test that exact contract. `PowerFaultMutant` replaces the power-specific guard with a generic check of the computed power, while retaining the old refinement claim. `ReadyTickMutant` omits the tick on ready visits while retaining the old cost and fault claims. Both can preserve some successful arithmetic values while violating the required trace-level result. Their expected rejection is not reported as freshly executed here. The refinement is a theorem about the declared algorithm model; neither it nor its controls certify a JSON parser, the CPython interpreter, native compilation, or an unexamined implementation. [F250-104] [F250-240]

`PythonExprCore` supplies the separate recursive reference to which the stack theorem is compared. It explicitly binds its model to `prcodec.py` lines122–159, SHA-256 dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c. Its admitted inputs are already decoded well-formed expressions, exact natural integers and natural-valued dictionaries, optional natural budgets and a natural starting count. Dictionary writes remove older entries at the key and preserve other reads; missing reads return zero. Register reads have no new integer-width check. The power branch checks exponent+1 before allocating 2^exponent, preserving a distinct exponent fault. Value/lowering correctness, exact successful step cost and unbounded-budget totality belong to this model. The hash and source-range declaration are not a checked Python frontend, interpreter refinement or physical-resource guarantee. [R750A-574]

[R750A-574]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9a120790a308a57f7fa0e8d0480cf80b517197ddd429960244ea2d5f73c66867/PythonExprCore.lean

`RegisterWidthMutant` targets another part of that exact contract: it inserts a new width check on dictionary register reads, where the reference returns the stored value without that check. The remainder copies the universal stack/reference and tick claims, but the file explicitly identifies itself as expected rejection. For a stored value wider than the new allowance, the changed branch can refuse where the reference succeeds, so preserving selected numerical successes would not rescue full result equality. The copied claims receive no positive proof credit, and no fresh compilation or CPython verification is inferred. [F939A-806]

[F939A-806]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dab91418c44075d35146fe54e714fdaa612bed7489a47c2a020a97dd5c7c10cb/RegisterWidthMutant.lean


<a id="final189-b04-operand-order-control"></a>

The operand-order mutant supplies a further independent challenge to §14.3. After popping the right value bv and then the left value av, it calls binaryValue(op,bv,av), reversing the reference argument order. Commutative examples can conceal the change, but truncated subtraction and division need not agree. The copied universal refinement, exact tick and success assertions below that altered branch are expected-rejection obligations, not accepted results for the reversed evaluator. No Lean rejection or CPython execution was newly observed. [F189B-827](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dfa201676d9e775063a90767470fdf022007ed6554b349589335d4733ddbca7c/OperandOrderMutant.lean)

#### Exact successful cost, early failure and source-correspondence evidence

The expression acceptance's wording clarification makes §14.3's equation operationally explicit: cost(e) is available recursive fuel, not a demand to keep executing after an exception. On success exactly that many work pops/ticks occur and the pending tail is untouched. On failure propagation stops at the earlier modeled fault, retaining its category and visible count. In particular, a starting meter already above its limit fails after increment at start+1, and a ready visit still ticks. This clarifies the existing theorem without changing its source. [N250C-137] [N250C-135]

The rule-by-rule source review gives a stricter admission boundary than the word “integer” alone: constants, keys, values, budgets and starting count must be exact built-in natural integers, excluding bool, subclasses and callback-bearing/custom dictionaries; tuples must be finite, immutable, correctly aritied expression trees. These are preconditions, not validation performed by Meter, eval_expr or Program.__post_init__. The model's empty-work stuttering is unused fuel after source exit, not an extra source tick. On failure, the external observation is fault category/count, not the unexposed partial work and value stacks. Binary arithmetic precedes generic width checking and can encounter a host allocation failure first; the distinct power precheck does not prove host-safe computation in general. [N250C-136] [N250C-143]

The source-contract program first requires the exact whole-source hash, then checks the named Python AST fingerprints and line ranges. Its mutation tests bind operand order, ready ticks, unchecked variable reads, the exponent guard and default-zero lookup. Those are identity and control-flow drift tests, not semantic extraction. The independent control program uses a recursive oracle against the iterative evaluator, separately instruments the initial/final stack boundary, and tests 18 source mutations with fixed witnesses. Its malformed tick-before-tag witness is deliberately outside the theorem's input domain. The bounded edge suite likewise treats negative/bool direct literals and unbounded input/output width as excluded-interface observations rather than extending the theorem. [N250C-138] [N250C-139] [N250C-141] [N250C-142]

The exact acceptance reports 266,760 recursive-oracle comparisons, 1,593 seeded stack-boundary cases, 28 valid-domain executed source lines and 18 detected behavioral mutants, alongside source-bound Lean checks. These are historical finite corroboration; no Python or Lean run was performed here. The public runner's two compatibility-layout literal copies both derive from the same bound source, so replaying the independent control script does not create new independently sourced provenance. The runner separately checks its compiler/source/cache inventories, allowing only five hash-reproducing trace-prefix substitutions, and keeps source freeze, historical acceptance and any future replay receipt distinct. [N250C-134] [N250C-135] [N250C-140]

Thus the accepted connection is a mathematical algorithm theorem plus reviewed source correspondence. Neither source hashes, all observed branch coverage nor many differential cases supply a universal Python frontend or CPython proof. Parser/serializer behavior, statement/repeat execution, whole-run/trace wrappers and allocation/time/OS outcomes remain separate endpoints. The paused extensions do not acquire acceptance through this expression-only result. [N250C-134] [N250C-136] [N250C-143]

### 14.4 Separate numeric-envelope and statement-runtime interfaces

The Q8 numeric-envelope and statement-runtime sources supply separate interfaces from the expression-only acceptance above. Base-256 byte expansion and the complete sentinel-envelope decoder, including rejection and removal of leading sentinel 1, are primitive recursive. This qualifies the numeric envelope, not the full program parser or universal evaluator.

The statement/repeat machine uses a finite association-list register file with zero default reads and newest-write shadowing. It captures each loop count on entry and writes the loop index before the body. Its transition-fuel evaluator is sound for the functional-store semantics, completes every finite statement with enough fuel, and preserves a successful result at every larger budget. Invalid numeric/program syntax or wrong arity yields some 0; insufficient transition fuel yields none, even when the semantic answer is one. The unbounded fuel search terminates and returns the semantic value. However, the formal universal-computability conclusion still assumes Computable₂ for the bounded numeric evaluator in its input triple and fuel. That explicit premise is not discharged by the envelope theorem or by the termination argument alone. Expression arithmetic, decoding and host storage are unmetered here, so these fuel counts are not Python Meter.steps or physical resource guarantees.

The operational boundary controls distinguish a finished machine from a semantic no-op: an empty task stack succeeds with zero fuel, whereas a pending skip needs one transition. They also state that a single set transition can store 2^n for arbitrary n, making the absence of an arithmetic-size bound explicit. The expression convention gives 7/0=0 and 7 mod 0=7 on naturals. These exact controls supplement, rather than replace, the captured-loop-count and successful-fuel agreement interfaces; their check and axiom-print commands are not fresh execution results or host-resource guarantees. [NEXT-C30-248](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/4be7c1abac6dceb3bd1a746fd52a69ea08b16d8cc3a4dd9f1b7ed1f0c27e65fe/BoundaryControls.lean#L8-L36)

The primitive-recursive program controls add three call-level obligations. Compiling the first projection after swapping its two inputs returns the second input, so composition retains argument order. Specialization permits a program to update its input register in place. An inlined zero-argument counter that increments scratch register seven returns one even from an arbitrary caller store, and two consecutive calls still return one rather than two: each call resets its private scratch state. A separate loop control retains its entry count despite a body write to the bound register. Extensional coverage supplies a representing program, not correctness of any syntax merely named successor; the displayed zero program fails that claimed value. These written controls depend on the imported compilation, specialization and call interfaces and supply no newly observed execution. [SUB250-F28-070](../research/t20-v6-20261012/sources/5c0ebaced3f367dc7b71905c2a1601fddb628975eb992a5c1cdb7ec87b8a5743/BoundaryControls.lean#L5-L44)

A separate effectivity development discharges that premise for the exact decoder and machine. Constructive natural-number encodings of expressions, statements, repeat tasks and packed programs support primitive-recursive expression evaluation and the exact stack transition. These internal codes do not replace the serialized representation. For parsing, a finite table stores the lower-fuel result at every suffix of the original input; proved suffix preservation identifies each lookup with the original recursive parser. Canonical varint reading, sequential parsing and these tables therefore make the exact expression and statement parsers primitive recursive jointly in fuel and input, including failure and unread suffixes. The complete decoder retains magic, canonical-field and trailing-byte checks on every numeric input, not only generated codes. Composing it with the bounded machine yields a primitive-recursive fuel evaluator; composing that result with the existing terminating fuel-search theorem yields uniform computability of evaluateIndex, also at an explicit twice-unpaired Nat-to-Nat interface. This is not uniform primitive recursiveness of unbounded evaluation, a physical resource bound or a fresh compiled-proof validation. [F109-M02] [F109-M08] [F109-M10] [F109-M11] [F109-M14] [F109-M00] [F109-M05] [F109-M01] [F109-M06] [F109-M13] [F109-M03]

[F109-M02]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/ba64a8c6745afaa3ec7579b9412db90f66c241f0036ecdc259b296ec48c17540.lean
[F109-M08]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/f9b92e7e1aed4e139e0f2aa5744fa12e1a03d5961345aad59bdc07e051cd6535.lean
[F109-M10]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/b35aee95ada4bc6c97fab8942b9de4fc3d9dbf69a702ee3d74c0296e2975d68b.lean
[F109-M11]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/35c9adbb36f904f3e207ba538ed61a90924a9901ac3b01d202575e0e6842237c.lean
[F109-M14]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/0a753dd580e113d766759f99f40bc116dea59ced1d2ea6d1a3edd63d487cc415.lean
[F109-M00]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/58d3441f4832f42dd2224ba51aea7f39403cc1fe52bda7da7726c9254555b6c5.lean
[F109-M05]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/ea9073dc5830304417d9c6e993f5ff6639c4ebeb807a8f2780c06f9665b3b23e.lean
[F109-M01]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/e4039eb1aa7110db405695d48806e6528f2e64ef5e82cd730fb0b3e3ed1427cc.lean
[F109-M06]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/b99e84db7064e5134b5f174bbbe5155625782092e25f39606cb435103e259f92.lean
[F109-M13]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/f28d1911bdbc216241b713c2752954d36235cd040c519fa2725ff74ed4e49de1.lean
[F109-M03]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/373593d1d9b371b29d72414f2e2142e528441b33b723138be1352d3883b93808.lean

The retained numeric-decoder controls make those conventions concrete: overwriting the bound register does not alter the captured count, and overwriting the loop index does not prevent its next scheduled write. They also state zero/nonzero branch, zero-loop, invalid-index and wrong-arity equations. Their results are optional output bits modulo two, not raw register values; the evaluation-vector and axiom-print commands are requests rather than newly observed executions. [F109C-015](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/d851d7c49464f06e0f4a13edea2d51b54e0e00af95a4f410c3c56f3a9ab1a47d.lean)

For each supplied nonempty Q8 machine and fixed finite horizon N, a decidable predicate checks completion for every N-bit word and every tick k<N. Pointwise runtime completeness gives a maximum over those finitely many cases; the least successful fuel is selected by finite search. Prefix dependence and fuel monotonicity then make that one budget, and every larger budget, correct for all infinite input streams through N. This uses the imported parser/runtime soundness and completeness interfaces; it does not reprove them. The quantifiers do not provide one budget for every horizon, an infinite-horizon bound, or a wall-clock, memory or Python-meter bound. Evaluation commands in the source are requests, not observed executions. [C250-135] [C250-136] [C250-137]

[C250-135]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/4f137dd91e8d56c084dd0a664f182b4fe3f09356eef1fa1fd08102c7e514df73.lean
[C250-136]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/31864c8129fab9ef98cc377ef647f9cee8323a2319a3756a1504ce2e8ebe8f0c.lean
[C250-137]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/ffdd64d1a7d01f80a2eb8e9576c5fd503f1835de036d2ef85c42df3c8b03d3ea.lean


## 15. The written completeness landscape and its exact input domains

The Fifteenth Mathematical Compendium's first five papers establish a connected written theory beyond the individual formal interfaces in §§11–14. The distinction is substantive: a checked semantic bridge is not, by itself, a checked computability classification; conversely, a written proof supported by such a bridge is not erased because the whole metatheorem was not encoded in Lean. The results below concern the unchanged current `Has` judgement and original paired interpretations F/G, unless explicitly stated otherwise. They do not supply a HasE scalar-fusion witness or reopen the exact noninhabitation and internal-independence results retained in §§8–9. The compendium and later companion's descriptions of that target as OPEN are historical statuses of those sources, not the present verdict. [F250-C168]

The source's bounded prior-art comparison credits established Church classification and computability methods without conflating targets. Hinze's *Church numerals, twice!* uses System F with inductive types, parametricity and η-conversion for the Church/Peano inverse and fold correspondence. It is precedent for classification/iteration, not automatically the no-added-η P01AC F/G arbitrary-inhabitant observation theorem or a current-Has counter compiler. Pistone–Tranchini's *What’s Decidable About (Atomic) Polymorphism?* studies typed-context Boolean/natural observations: its atomic-F numerical-equivalence decision result, ML/F₁ undecidability and general atomic-F contextual-congruence undecidability do not themselves establish these fixed-carrier hierarchy levels or the bare/annotated boundary. A relation-preserving transfer is still required. The comparison is bounded source reading, not a priority claim or exhaustive literature review. [F250-C168, Relation to established methods]

### 15.1 Raw-valued identity has an exact second-level classification

Let N be the Church-natural type and C=N→Raw. For closed endpoint polynomials p,q, let D(p,q) assert scope and both current endpoint typings at C, and let V(p,q) assert their F-relation in every unary environment. The bare coded set is E={⟨p,q⟩:D(p,q) and V(p,q)}; malformed codes are excluded. The annotated set additionally requires the *supplied* finite endpoint typing certificates to validate, rather than searching for different certificates when the supplied ones fail.

Every semantic natural has a unique iteration index. Canonical observations u_n realize every index, and two semantic naturals with the same index are related in the required relation. With both endpoint typings, these facts give

V(p,q) iff for every n, P u_n ≃ Q u_n,

where P,Q are endpoint evaluations and ≃ is raw conversion. For the reverse direction, take arbitrary cross-related inputs x,y of common index n. Endpoint soundness and the same-index relation transport P x to P u_n and Q u_n to Q y; the canonical hypothesis completes the chain. This is not an assertion that arbitrary environments or unapplied programs are identical.

Finite annotated typing and conversion derivations have recursive validators. Put both endpoint certificates and the nth conversion certificate in one finite witness w. The bare target therefore has a matrix ∀n∃w R(z,n,w) with recursive R. At n=0 the witness supplies typing; the additional existential typing search does not introduce a third alternation. The annotated version fixes those typing certificates in the input.

For hardness, fix a pure I/K/S representation of the partial computation H(e,n) which returns zero exactly when machine e halts on n. The imported representation premise supplies a single finite pure term U: defined computations convert to the corresponding numeral, while undefined computations have **no pure weak normal form**. The chosen pure numerals satisfy ν₀=KI and νₙ₊₁=SBνₙ, where B=S(KS)K. A fixed bracket-abstraction template makes p_e a currently typed C endpoint testing Uν_e on the iteration generated by its N input; q is the constant ν₀ endpoint. Current Raw typing admits these templates without a termination premise. On u_n their outputs convert respectively to Uν_eν_n and ν₀.

If e is total, every canonical test agrees and hence V(p_e,q). If it is not total at n, such agreement would give Uν_eν_n ≃ ν₀. Retract the inert raw constructors to I while fixing pure I/K/S and application; every raw step retracts to a pure step. Together with confluence and the pure normal endpoint, this would provide a pure weak normal form, contradicting the imported undefined-computation condition. Mere failure to *observe* termination would not suffice. This gives a total computable reduction of totality, and both coded identity sets are Π₂-complete.

The conclusions apply to one fixed carrier, not every type. On the typed family, neither validity nor invalidity is recursively enumerable. For validity, a program that halts on input n precisely when a fixed machine has not halted within n steps reduces nonhalting to totality. For invalidity, a program that waits for that fixed machine before halting on every input reduces nonhalting to failure of totality. Thus malformed-input rejection is not responsible for either obstruction. Distinct raw-normal constant outputs also give infinitely many inequivalent currently typed endpoints at this fixed carrier.

No recursively enumerable sound and complete positive *or negative* finite-proof system with effective target projection can characterize this typed Raw family: enumeration of its proofs would enumerate the corresponding forbidden set. This preserves the established sound positive HasE repairs while excluding their unrestricted completeness. Finite canonical successes do not prove the universal claim: a machine can halt on exactly a prescribed finite set of inputs. A finite list of conversion obligations is not decidable merely because its length is finite; supplied valid derivations make checking finite, while discovering arbitrary conversions is a different task.

**Evidence boundary.** The canonical bridge, observer equations under explicit assumptions, and pure/raw reflection interfaces have checked components. Existence and matching of the universal pure representer, finite-code construction, totality/hierarchy classification and certificate impossibility are written metamathematics. Historical compiler and axiom readbacks in the compendium are not new executions of this consolidation. [F250-C168, Paper 1]

### 15.2 Boolean observations change both the bound and the role of typing

Let B be the Church-Boolean carrier and C_B=N→B. Every self-related Boolean has exactly one of the two marker observations. On currently typed endpoints, inequality is equivalent to a finite mismatch witness: a canonical input n and two finite conversion derivations to opposite markers. The mismatch set M is recursively enumerable. On valid annotated endpoint certificates, semantic equality is therefore Π₁.

The lower bound uses a finite-arity primitive-recursion compiler with current typings and adequacy on arbitrary semantic natural observations, not a supposition that every partial computation can inhabit B. A fixed primitive-recursive bounded-halting characteristic χ(n,e) is zero for all n exactly when e never halts. Compile its fixed finite description and specialize the machine index. The endpoint p_e and constant-zero q have current typings for every e, and V_B(p_e,q) iff e never halts. Enumerating and validating finite endpoint derivations yields the required certificates on every input e, because their existence is already proved. This extraction-independent search is a total computable annotation map. Thus annotated Boolean identity is Π₁-complete and its complement is Σ₁-complete.

There is no partial computable distinguishing bound which terminates on **every valid annotated input** and bounds a distinguishing n whenever the endpoints differ. If there were, finitely many output-bit searches would terminate by Boolean standardness; agreement through the bound would decide the Π₁-complete identity problem. For each fixed syntax-size bound the finite maximum of least distinguishing inputs still exists. What fails is a computable uniform majorant, not those individual finite maxima or bounds for separately restricted fragments.

Bare input changes the classification. Let D be the recursively enumerable set of endpoint pairs with both current typings. Then E_B=D\M, a difference of two recursively enumerable sets. To prove matching hardness, the source constructs an explicit search gate G_{p_e}. If e halts, applying that gate to a currently typed endpoint preserves its typing and required behavior. If e never halts, its application to **any closed q** cannot be typed at C_B. The latter conclusion is stronger than saying the gate itself lacks a normal form: after forward translation to lambda syntax, deterministic weak-head reduction repeatedly exposes the next recursive state, with every finite trailing argument preserved. It therefore cannot be beta-convertible to either marker variable. Current typing would, by soundness and Boolean standardness at canonical zero, require exactly such a marker conversion.

Combining gate index e with the earlier bounded-halting endpoint p_j gives

(G_{p_e} p_j,q₀) ∈ E_B iff e halts and j never halts.

Any difference U\V of enumerable sets reduces to this pair by using machines that halt on entry into U and V. Hence bare Boolean identity is d.c.e.-complete. Fixing the closed endpoint q₀ gives e halts iff `Has [] (G_{p_e} q₀) C_B`, so typability at this **one fixed type** is Σ₁-complete. The negative gate argument does not deny ordinary Raw typing, import strong normalization for the current calculus, or identify non-normalization of an unapplied term with non-typability of its observations.

For both carriers, universal original F-identity at proof I, universal original G-identity at I, and existence of a uniform semantic polynomial witness are equivalent to the endpoint semantic relation, using diagonal environments for the converse G implication. These are semantic identity claims, not derivations of current `Has` at the identity type.

**Evidence boundary.** Boolean standardness, mismatch equivalence, the general finite primitive-recursion compiler and original F/G transfers have checked components. The concrete machine arithmetic/indexing, finite-code and hierarchy proofs, and complete gate nonhalting argument remain written mathematics at the reported scope. The narrower conditional interfaces in §13 are not silently promoted into whole-theorem kernel formalizations. [F250-C168, Papers 2–3]

### 15.3 An exactly decidable multivariate fragment

For each finite arity r, let E_r consist of natural constants, the r variables, addition, multiplication, and arbitrary finite nesting of `if t=0 then e else f`. It contains neither subtraction, negative coefficients, arbitrary equality tests, recursion constructors nor embedded arbitrary P01AC programs. The literal compiler produces currently typed endpoints at C₀=N, C_{r+1}=N→C_r; its arbitrary-observation adequacy relates numerical equality to the original semantic relation with independently related arguments at every arrow.

For each zero/nonzero coordinate mask S, specialize dead variables to zero and compute a finite nonnegative coefficient map NF_S(e). On the mask cell, a nonzero supported monomial is strictly positive and all others nonnegative. Thus a test is zero throughout that cell exactly when its map is zero; every conditional selects one fixed branch there. Structural induction proves normalization adequacy even with nested zero tests. Nonnegativity is essential: x−y would not have a fixed zero status on the all-positive cell.

Conversely any finite table of S-normal nonnegative polynomial maps is realized by a depth-r decision tree testing each coordinate for zero, with the prescribed polynomial at each leaf. The fragment therefore denotes exactly these piecewise-polynomial functions. To prove uniqueness rather than assume it, subtract two different maps in the integers. A nonzero polynomial with individual degrees d_i cannot vanish on a Cartesian grid with d_i+1 distinct values in each variable: induction on the number of variables reduces to the univariate root bound. Consequently it suffices, on each mask, to test dead coordinates at zero and live coordinates at 1,…,d_i+1, where d_i is the maximum exponent appearing in either normalized map.

Taking the union of those grids gives a computable complete test with cardinality Σ_S ∏_{i∈S}(d_i+1). Empty products equal one: the all-zero mask contributes its zero tuple; arity zero contributes the unique empty tuple; degree-zero live coordinates still contribute test value one. Different tables have a bounded distinguishing tuple. Coefficient-table certificates and evaluation-grid certificates are finite, recursively checked, sound and complete for the exact source inputs. The implementation must bind arity, syntax, coefficients or evaluations and, when supplied externally, the *literal* compiled endpoints; accepting an unrelated or merely conversion-equivalent endpoint changes the problem.

Thus numerical equality, equality of every mask map, agreement on the finite grid, original semantic endpoint/identity validity and existence of a semantic witness coincide for this fragment. No current syntactic identity witness or arbitrary-endpoint decision procedure follows. The sparse formal interfaces in §14 retain their own exact scope; the compendium additionally supplies this written completeness argument and its checked compiler/certificate components. [F250-C168, Paper 4]

The exact `IdentityChecker` source supplies the finite mask-and-coefficient checker for this restricted fragment. It exhausts every mask, including the unique arity-zero mask, and compares the normalized coefficient maps. Its theorem interfaces equate Boolean acceptance with pointwise equality, `FragmentValid`, the original F/G identity relations and semantic witness existence. The submitted finite certificate must cover every mask with a common coefficient row; soundness and completeness refer to the same bound expression pair. This provides the direct checker witness for the preceding account, not a decision procedure for general primitive-recursive equality or a constructor for unchanged current Has identity. [R750A-568]

[R750A-568]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/989b586bcd7b333e62c4a811f9d094c8347b5f89f703b0c4a2618b9f85124f02/IdentityChecker.lean

The public reference checker makes the representation contract stricter than the mathematical map equality alone. Natural annotations must be actual nonnegative integers, not Booleans; syntax and certificate fields have exact keys. It validates even branches not selected on a particular mask. Each certificate binds the arity and source pair, covers every mask, and supplies the recomputed canonical coefficient rows. Reordered rows, duplicate support, explicit zero entries and omitted masks are rejected by the Python representation even where a typed Lean list representation may admit redundant entries under its own coverage hypotheses. Equality of these languages or parsers is not established by having similarly named checkers. Literal compiled-endpoint binding is a separate obligation when a certificate is used for an external target. [Q250A-050] [Q250A-051] [Q250A-052]

The reference distinguishes a real empty-tuple counterexample at arity zero from absence of a witness. Its grid routine uses dead coordinates zero and live coordinates $`1,\ldots,d_i+1`$, then independently evaluates any returned distinguishing tuple. The general grid theorem is the polynomial argument above; the author and independent test suites are finite checks of its implementation, including higher-degree witnesses, malformed syntax, forged certificates and literal endpoint mismatches. Their ten and twelve test groups, random seeds and thousands of direct evaluations do not themselves prove the unbounded theorem. The runtime-agreement script deterministically generates 720 expression pairs at arities zero through five, emits Lean evaluations and verifies a supplied output against regenerated inputs. It does not invoke Lean, supply missing output, or establish formal refinement; static reading of it is no new cross-runtime pass. [Q250A-053] [Q250A-054] [Q250A-055]

The declaration map keeps the wider claim boundary explicit: the Raw and Boolean reductions, the bare-code exclusions, the restricted positive compiler/checker, and the one-root-test extension have different assumptions and proof statuses. A conditional gate is not an unconditional classifier. The DPRM existence reduction is written mathematics without concrete machine-to-polynomial coefficients, and acceptance in this restricted arithmetic fragment remains original semantic F/G identity validity rather than a new current-Has syntactic identity witness. The retained proof modules, checker, tests and cross-runtime harness remain necessary source artifacts for their respective claims. [Q250A-050]

### 15.4 One root equality test crosses the general boundary, but not at arity one

Let A_r be pure natural arithmetic trees (constants, variables, addition, multiplication). Define R_r as the **disjoint union** of old E_r expressions and a root expression test(P,Q), with P,Q∈A_r, returning one when P=Q and zero otherwise. This is not closure under nested new tests. `ZeroTest(r,P,Q)` means ∀v P(v)≠Q(v), so it concerns *absence of roots*, not ordinary polynomial identity.

The written lower bound imports the established Diophantine representation premise: each enumerable set has an integer polynomial H(a,y) whose nonnegative roots in y characterize membership of a. Fix one H representing halting, aggregate coefficients, split them into nonnegative H⁺ and H⁻, and specialize a=e. The resulting fixed-tree substitution e↦(P_e,Q_e) is computable, and

e does not halt iff ∀y P_e(y)≠Q_e(y).

Existence of the fixed finite H suffices to prove existence of this computable map; no uniform polynomial-selector algorithm or unprovided runnable reducer is being asserted. The witness arity is some fixed finite m, not a specified number. Unused-variable padding extends hardness to all r≥m. Enumeration of a root is the matching negative semidecision. Hence ZeroTest, and universal equality of R_r expressions against old zero, are Π₁-complete. The numerical/original-semantic compiler bridge transfers the classification to the exact source-presented endpoints.

This excludes every enumerable sound complete positive finite-certificate format, and every total effective complete finite testing bound for the whole extension. The mask proof fails specifically because equality of two positive polynomials can vary within one cell: x=y holds at (1,1) but not (1,2). This does not erase the positive mask result.

There is also a positive unary boundary. For a nonzero integer polynomial H(x)=a_d x^d+Σ_{i<d}a_i x^i with d≥1, put B(H)=1+Σ_{i<d}|a_i|; use B=1 for nonzero constants and, for bookkeeping only, zero. At natural n≥B(H), the leading term dominates the sum of lower terms, since |a_d|≥1 and n exceeds that coefficient sum. Nonzero H therefore cannot vanish there.

Each old unary expression has a polynomial tail from its positive mask, valid for n≥1. Each new root test has constant tail one if P−Q is the zero map, and otherwise constant tail zero after B(P−Q). Compute tail data (b_s,T_s),(b_t,T_t); let B=max(b_s,b_t), H=T_s−T_t and M=max(B,B(H)). Equality at every n=0,…,M forces H=0 (otherwise M distinguishes), and verifies all earlier exceptions. It is therefore equivalent to universal equality. This covers cancellation, constants and differences confined to zero, but only the declared grammar, not arbitrary nested root-test extensions. Arity zero is direct evaluation. The unspecified hardness arity must accordingly be at least two; no classification of every arity ≥2 follows.

**Evidence boundary.** The DPRM existence premise is externally sourced to Matiyasevich–Robinson, *Two universal 3-quantifier representations of recursively enumerable sets*, §§1–3, equation (3), corrected translation [arXiv:0802.1052](https://arxiv.org/abs/0802.1052). It is not a new axiom in the checked compiler. The written classification supplies no concrete representing coefficients or numerical fixed-arity bound. The unary finite criterion is written mathematics; the separately retained reference implementation below is not a kernel refinement theorem. [F250-C168, Paper 5]


The unary root-extension reference implementation realizes that finite tail argument for exactly the declared disjoint grammar: an old restricted expression, or one root equality of two pure arithmetic trees. It does not admit arbitrary nested equality tests. It computes a signed polynomial difference, the coefficient bound above, and the constant tail of a root test; nonidentical tails yield a witness at a safe dominating bound, while equal tails require checking the finite exceptional prefix. The returned witness need not be the least counterexample. This is a concrete reference algorithm whose mathematical justification is the retained unary argument, not a general multivariate solver, a parser-to-Lean refinement theorem or evidence of a new executed test. [Q250A-056]

The Twentieth companion's later transfer assessment does not import a normalization theorem from the inspected pure-type-system endpoint. That endpoint assumes weak normalization of legal expressions in its annotated grammar; its conversion and annotation-preserving erasure do not match HasE's proof-term-changing conversion and discarded proof coordinates. A weakly normalizing converted HasE term can contain a divergent discarded raw argument. The endpoint therefore supplies neither the original identity witness nor the required derivation-normalization theorem. This is a completed negative transfer assessment, not evidence that all normalization routes are impossible. [F250-C220, Part 3]

## References and formal sources

### Primary mathematical literature

- John C. Reynolds, “Types, Abstraction and Parametric Polymorphism,” in *Information Processing 83*, 1983, pp. 513–523. [Primary paper][reynolds]. Relational interpretation of abstraction and parametric polymorphism; cited for the conceptual antecedent, not as a soundness proof for this dependent source language.
- J. M. E. Hyland, E. P. Robinson and G. Rosolini, “Algebraic Types in PER Models,” in *Mathematical Foundations of Programming Semantics*, Lecture Notes in Computer Science 442, 1990, pp. 333–350. [Primary paper][hrr], especially §2. The distinction between open-term PER standardness and unrestricted transfer to another model is retained.
- Ana Cristina Rocha Oliveira and Mauricio Ayala-Rincón, “Formalizing the Confluence of Orthogonal Rewriting Systems,” *Electronic Proceedings in Theoretical Computer Science* 113, 2013, pp. 145–152. [Primary paper record][orthogonal]. The particular confluence proof needed here is supplied in section 8 and in the concrete formal source.

### Exact public source witnesses

The following references bind this exposition to the public source edition at Git commit `a7ff0e33d1a299db640041c46b1af81ca70851f6`. Mathematical notation above is organized by subject; the historical source paths serve only exact verification. The Lean modules remain independent formal artifacts. Replacing duplicated prose with this exposition would not by itself justify removing a required formal dependency.

- [Extensional finite grammar][syntax]; [generic inhabited probe][probe].
- [Literal bracket abstraction and compiler formulas][compiler]; [transport from the original compiler][transport].
- [Scalar-fusion forward construction][fusion-forward], [reverse construction][fusion-reverse], [literal specialization][fusion-literal], and [closed proof canonicalization][canonical].
- [Full-PER standardness][standardness], [PER interface][per-interface], [whole-source soundness][full-per], and [exact compiler application][application].
- [Closed scalar instances and generic conversion reflection][closed-instances]; [structural renaming][rename]; [closed weakening][weakening]; [closed Church identity][closed-identity]; [complete developments and count extraction][developments]; [effective closed-identity decision][decision]; [independent closed-fragment controls][closed-controls].
- [Failed strict-iterator routes and proof-inversion obstruction][failed-routes]. Their historical open status predates the later negative theorem and is not the current conclusion of this chapter.
- [Concrete operational model][case-operational]; [homogeneous closure][homogeneous]; [concrete universe][universe]; [finite closure controls][closure-controls]; [whole-source homogeneous soundness][henkin-soundness]; [exact compiler counterexample][counterexample]; [scalar noninhabitation][noninhabitation]; [literal identity consequence][identity-negative]; [mixed-PER control][mixed-control].
- [Scalar no-negation proof][no-negation]; [independent exact-identity controls][identity-control]; [certificate grammar][certificate-syntax]; [certificate separation][certificate-separation].
- [Independent scalar-fusion review][fusion-review] and [independent homogeneous-model review][model-review], with [the final bounded review reconciliation][final-review] and [exact identity delta review][identity-review]. These report historical source and kernel checks at their stated scopes. This exposition does not claim to have rerun them or to have rebuilt their inherited dependency closures.

- [Whole-label opaque representation proof][opaque-source]; [exact hypothetical bridge][bridge-source]; [the historical residual identity argument][residual-source]; [the later complete intensional interpretation and closed criterion][intensional-source]. These four public written bodies retain their original ordinary-proof status, inherited prerequisites and historical order. The residual stop is resolved by the later proof.
- [Original eighteen-rule declarations][original-syntax]; [exact bridge declarations and conversion theorem][bridge-definitions]; [finite import grammar][finite-grammar]; [literal polynomial operations][original-polynomials]; [original F/G predicates][original-predicates], [simultaneous soundness induction][original-soundness] and [identity/J semantic helpers][original-term-lemmas].
- [Inherited normalization witness][normalization-boundary], [finite-normalization premise][normalization-premise], [raw confluence and normal-form separation][confluence-premise], and [the discarded-loop cycle][discarded-loop-source]; [later intensional theorem component][intensional-theorems]; [exact positive extensional identity witness][extensional-identity-witness] and [its distinct raw and old-calculus consequences][extensional-identity-consequences]. Inspection of these public definitions and specified proof premises is separate from a new Lean run or a complete recheck of their imported closures.

[reynolds]: https://www.cs.cmu.edu/~crary/819-f09/Reynolds83.pdf
[hrr]: https://www.dpmms.cam.ac.uk/~jmeh1/Research/Oldpapers/hrr90.pdf
[orthogonal]: https://arxiv.org/abs/1303.7335
[syntax]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dc4415c2e367c957589f1162243804cce1955f28894355a0d73a4a0b7ef66d9f/ExtensionalRepairSyntax.lean
[probe]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/43e824a746ef624e8d783e89d62d3dc95108042cb311f931cd868cbe5cf76028/GenericIdentityCarrierProbe.lean
[probe-report]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ff55a678cc16fa68bee9379c9f5bc11933f53608c53437da3c00217fca23bd4c/README.md
[compiler]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/f77cd702ec5f1dd242a8e30959aab203b5215b838a3305d64c5c733ec00d01c0/FrozenCompilerMirror.lean
[transport]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/448e9f950a1c51a9267ca04671fe6ade3377a485692621bd8252925ae02fbdbc/ImportedCompilerTransport.lean
[fusion-forward]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618/ScalarFusionCore.lean
[fusion-reverse]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6a03e72fe6e087c98b97d0f881f6f1dc7960c2a46b89f7f1351394ff3b410b65/ScalarFusionReverse.lean
[fusion-literal]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b3d6f9e9b235171c0b885ee40d1fb985c6efa82e1647c76a5ca98e493795af5b/LiteralScalarFusion.lean
[canonical]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c773b21488efd769d57b3f92ea81b5d3c1cf50de15c7cf4fb1dfd30fa8dc45d8/ClosedProofCanonicalisation.lean
[standardness]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/d3972a5dff963d07cb1808427686dfdae3bf54bdc811bef025809ec8846a527d/OpenTermStandardness.lean
[per-interface]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/312b60aafb9752d02e67c9cec6843c12b0419d96d86202f219b2b10a4b3032f3/PERInterface.lean
[full-per]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/2a0d01d92923a22c4b41f512e4c4b3524ea1c630d13478176c5c20d63afa7638/FullPER.lean
[application]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/6d57b65eb3c4ffc8b7c34ba66beea17b7705265dcc4fdd11e66b14d0c5702bb9/Application.lean
[closed-instances]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/57fd4fdc378db98dc7dda8ac443871a398765761b694c7135b9a20eb67349535/ClosedScalarInstances.lean
[rename]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/7f6b97124cdfc453df0eb9ad10b34caa025a5a59b3bef75654b9584b543b3ce5/HasEStructuralRename.lean
[weakening]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/5414eed802dafb25634a61136feeafeca8f1bce23074f57934c46c24b85d3edb/HasEClosedWeakening.lean
[closed-identity]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/0599dd8f6516179c7463897840c3078241ea0a956554b912e6110022760c5cec/ClosedChurchIdentity.lean
[developments]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/d7604981e4dd1746fe7cfc7bebea5040c6993a44840f80103bbae2a9a5e0e44e/OpenDevelopments.lean
[decision]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/26dad868c809f8cf87ac120d3d5f3627049864341e8142a5729a684582eed67b/EffectiveChurchIdentity.lean
[closed-controls]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/96b2ec1c9c1dd9c1c7461d3813eeac2464e27114bd7560fa5bc235208623fc9c/ClosedChurchReviewControls.lean
[failed-routes]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f52f7257475c5187a8cba284d596fa6a1d3e4d589721524354997d9f5bfc2f7f/NEW_PASS_RESULT.md
[case-operational]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/5575a1d8e69c8f857b0b15dc6f1358a4c3f44bd54a47bf528cf3295ae59c3708/CaseOperational.lean
[homogeneous]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/f06b84a8dd088a9cf82ab99dff2d476023ab50427fee0245ef5d210a8ec57f0f/HomogeneousPER.lean
[universe]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/8fb9848611f88b2f2555a15469eb59c3ff98e9a831f92f701cdb0091dc2d6904/ConcreteUniverse.lean
[closure-controls]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/5468abd37ac6c90a831a5440e8ef61fa9c4d7ab5b16e00ceb404a5d0f391e4b6/GuardControls.lean
[henkin-soundness]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/d0c9bc80e4014f2dc7ba685af95690b96ea02e166209101966e9a9e797fbcf5f/HenkinSoundness.lean
[counterexample]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/af219bfec917e3f083b093ffc9d1e07f54fec5d72e8f8a274915eaa030397c0c/LiteralCounterexample.lean
[noninhabitation]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/b4c46829c268c37860114d5d99c08a2bc099373133a591664503ef07d8b75628/OriginalWNoninhabitation.lean
[identity-negative]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/5ee0cbdab27fa18866d5e7b1b6b13131bbdb649b5bacab839a67c46e11619d08/OriginalIdentityNoninhabitation.lean
[mixed-control]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/7d89f93d755650106be0a045abf52b926032d1d8cd29898d6c1746639768085e/MixedPERControl.lean
[no-negation]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/30fe6cffc3e9b93ea48bd20957e5ef96678fe5b227d5fc0549b9ebbf5840cd56/NoInternalNegation.lean
[identity-control]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/1654c2cc234cc2eb8155d9b84590dd3b2b884cc01ce62f1a8b9779aa9d59cda9/IdentityReviewControls.lean
[certificate-syntax]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5f80f464475cb12a6ad90fc89c3540912322f31470be86e26072a990222115c4/UnaryCertificateSyntax.lean
[certificate-separation]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/0d1981d8d8a5d0c95e4649cd910698cba9410d71e63650df7eb118c125ef135c/CertificateSeparation.lean
[normalizer]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a2be40ceebd2c9293ac2be158abff27ed6093c2a82325fb946b5d2b534040d9c/UnaryNormalForm.lean
[certificate-pair]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8e943773416edcb225d1c3ed9961938bc75f82d7cc67f0bdb1aea5a98b126eac/UnaryCurrentIdentityBoundary.lean
[fusion-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2ff68e5e14d132976512e6b51e49af871fd488bcaa65288a81a8a1a881a837cf/REVIEW_SUMMARY.md
[model-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/8b4ddda158c65ca01c78fa8022fb88205c6cc6ed24ae56885f91983834f29147/REVIEW.md
[final-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/2891cdca4363db9553820d718c7806887cc820b0bdb4fdd549b1f9dce99dd002/FINAL_REVIEW.md
[cross-typing]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/10051b9df50fce7fef173bbe1cffe111cdc70529a29386753b8c872bf4789ba8/CrossTypedObserver.lean
[henkin-transport]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/3e3e4bcbea2c19c58df20cb7f83c7e5e9a41e7a4c9dcfab6085e09fc2025987a/SourceTransport.lean
[identity-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/0bccb4776a93509bfb004dbf08d1b7da89b8ae7637d6b066757f9b662f810047/REVIEW.md

[opaque-source]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b99fb16058f99ce5db66dd7a02e7515ede5157a002a6e76fc29d0f1bd8d65236/OPAQUE_ATOM_COMPLETENESS_PROOF_v3.md
[bridge-source]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/02f2ba85547a0798288ec5d307f06fa5b239b8cb9e0faa4b7c7a6ba303097bbe/HYPOTHETICAL_ATOM_APPLICATION_BRIDGE_v2.md
[residual-source]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7ff286710275b8873e2847ef21b9a30e70c20f465b6bb680569b8f107b484f3e/RESIDUAL_IDENTITY_COMPLETENESS_FEASIBILITY_v1.md
[intensional-source]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5d58087eab7e247235ec159abc17f6dc6d5779dc7722518f06d5040b25414e3a/Intensional_Identity_Separation_and_Closed_Identity_Conversion.md
[original-syntax]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/633c8de0c13b7fd2972710836ed6ab6bd85f7b86145e7c33a32fc38a7e6ddc46/AllSyntax.lean
[bridge-definitions]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/37a270542756fe1f93e7cd07b12a777cd5977c17b97f656edbd358625c4d6333/IntensionalIdentityBridge.lean
[finite-grammar]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f75306d1a29cd76385058ca1a819910b1f635a63369d807d484ab6db981a0042/FiniteBridge.lean
[original-polynomials]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/57bef4972e782bb85bc9f267bd899afdd09f65ebad610b107348db42b2b3b8b8/P01Polynomials.lean
[original-predicates]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8a8986200e9f4a6713238b77a1f23605201ee61552e55e72a2165eef05bab1d3/AllPredicates.lean
[original-soundness]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e5eabefb6f4d09efe592a53c2b9425707632d09f53241f7b4d0a5c30637bf4a7/AllSoundness.lean
[original-term-lemmas]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6158c711c97f461c0661fdd126a4458be3fabc853ca8bb4d059087e48406ce2e/AllTermLemmas.lean
[normalization-boundary]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dc41ea4ff297e4cd29501b1d1160195c2a1a4be2e91cbdd6f811bca1124152bc/PolymorphicNormalizationBoundary.lean
[normalization-premise]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9b1a18c1f189774d22858ba56bb77aecd5fc7506a08195c94fbb1873158a0e7e/P01Candidates.lean
[confluence-premise]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/682ad4ce3fda2b69601f267e6c7cfd729d8004fbfdd95c60f12d24fb59bc303e/P01Confluence.lean
[discarded-loop-source]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/13c3b0ba7aa7e57fd13bf1d61d28ef842755d5f5103ef9598d18cc885f4e2ca2/NormalisationAndNumerals.lean
[intensional-theorems]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/48c216af205451ec75f6d761f0dbee97a0ba279dfaa386cfd125676b96d6975c/IntensionalIdentityTheorems.lean
[extensional-identity-witness]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0a4a840f4256c0586c6d3443009889887720d82a2afa1f93150c8eea058e9b29/ExtensionalRepairWitness.lean
[extensional-identity-consequences]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4cd35d7e986496a7306ee239d9b4f3a24666a7e3979f46d46700ca49a175fc51/ExtensionalRepairTheorems.lean

[unary-companion]: https://github.com/theislampill/orthemology/blob/7b385e4116b052a0132dd740d07b918d3103f648/experiments/orthemology-v5-successors/source-store/10903b3260522cec902c7213a1b93a2c3280922126994c76f95755baadc2a91e/FULL_READER_TEXT_v5.md
[unary-diophantine]: https://doi.org/10.1070/IM1971v005n01ABEH001004


## Exact public sources for the additional discussion

These links identify the received public bodies at their immutable original revision. Their historical review and prospective statuses remain source-relative; this exposition performs no new source-program or formal execution.

- [Review of the closed polymorphic source-normalization boundary][R18-G060]. historical review of prior covered argument. Git blob `2489da4be949d888d8fafaa9cbae35576f77fa3d`.

[R18-G060]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2c67e22d0b19126c63fc9f1e476dd38d06174bd9208d816680165a64b437ea23/REVIEW.md


## Source guides for the additional arguments and qualifications

These exact public guides identify the reported results, historical review scopes and dependencies used in the additional discussion. A guide citation does not claim receipt or renewed verification of every linked proof, primary source or execution record.

- [GUIDE105-G006] Isolated candidates, not repository changes.
- [GUIDE105-G027] Untitled source guide.

[GUIDE105-G006]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/0ae580e4d03d07903afe36fa936696ec62193be206be37dcf97264cf1acfb5ef/README.md
[GUIDE105-G027]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/50e05cfde2ff11cb8fe262b8bc85bc9f9432d3d302274fc84b8d1f5500917d7c/README.md

[FAMILY-CODE]: https://github.com/theislampill/orthemology/blob/d7d0ad63acaaf33cbe22c72ac7408087a46ba9b8/research/t20-v6-20261012/sources/b77fabcd8d512e8839edf137482285511b544e2f4267f2a02ab67635f544f9a4/FamilyComputability.lean
[FAMILY-HALTING]: https://github.com/theislampill/orthemology/blob/d7d0ad63acaaf33cbe22c72ac7408087a46ba9b8/research/t20-v6-20261012/sources/8b8951ef7d1f932717226176b17700bf7a8a6beb4f78d0433376ecfc3ae92ba2/FullPERHalting.lean
[FAMILY-TESTS]: https://github.com/theislampill/orthemology/blob/d7d0ad63acaaf33cbe22c72ac7408087a46ba9b8/research/t20-v6-20261012/sources/1e8900ea5a9dd296986391acb1d887c8658b6806165c22191485a61615516edf/FullPERTests.lean
[FAMILY-BOUNDED]: https://github.com/theislampill/orthemology/blob/d7d0ad63acaaf33cbe22c72ac7408087a46ba9b8/research/t20-v6-20261012/sources/bc669cde2038e1ce800f5697afc4a244ce544371f37134054054a95273d6298a/BoundedHaltingPR.lean
[FAMILY-ENCODED]: https://github.com/theislampill/orthemology/blob/d7d0ad63acaaf33cbe22c72ac7408087a46ba9b8/research/t20-v6-20261012/sources/54c9b4616f23e904484432cac6f6936b724b42f48621fffa60ad957217b2e4b0/EncodedCertificateSyntax.lean
[FAMILY-CODEC]: https://github.com/theislampill/orthemology/blob/d7d0ad63acaaf33cbe22c72ac7408087a46ba9b8/research/t20-v6-20261012/sources/0eccaf3087d1ca760b5ab5b1c51b044e73250f971b0dae3624489bd647e7051a/CodecDeriveEncodable.lean

[R250-123]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/25a1623204ffb54724a7396ade2d5333c3c025f0d95c7950c84be98376b2e28f/StatementContract.lean
[R250-040]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/09a3eb40ec65389a7b06a2d7a829d94f76d3bdb6958476c4dc728ea01029c5f0/MotiveAndDirectionContract.lean
[R250-046]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0a87d4ddb3cba9f45ac2cdd298668cfc6403f75aa06d7e6877f774cde7dd049c/CanonicalizationContract.lean
[R250-089]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1b83248dc6fe0975f18099558e0a30332105019bd6c282598d32fe50510efea3/CanonicalizationRed.lean
[R250-164]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3238b21fe5dae7149de4e1c622e78a50ed723df0cac20ed654247cd2bcee8678/RejectCurrentLaundering.lean
[R250-235]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/43e824a746ef624e8d783e89d62d3dc95108042cb311f931cd868cbe5cf76028/GenericIdentityCarrierProbe.lean
[R250-093]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1db37f08cdb7a7d8e31fef95b48e4c6720c29f1550ca0549d8e7905bc9aff5e4/CORPUS_AND_TRANSFER_SCOPE.md "Retained public DERIVED assessment projection; Git 2288057541be6de7c9c876cb62fea97ab1ed55cc; SHA-256 1db37f08cdb7a7d8e31fef95b48e4c6720c29f1550ca0549d8e7905bc9aff5e4"


## Exact formal sources for supplementary scope and relation interfaces

[R0002-L001]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/00283060fbb1f8940432f4929b6062fdebe709f4d871e772a4035caafe11a2ac/ExtensionalRepairLemmas.lean
[R0002-L150]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2f02facf2dc87a4aa99f9f9f7efa8e56d8ddfba8c21a395085e99af01c6ec635/UnaryCertificateSoundness.lean
[R0002-L159]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/30cf8db7d8ab013db0cbc6a4dbc4690ece90ba1c244be65335ee2d2424738f9b/UnaryExpressionsControls.lean


## Exact sources for effective-observation contracts and audit boundaries

[R250-C27-3]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0071d28c2d0a9556d6e79f7cbd93d0a40abeb0cd7b72e9f6d51d255852f6e960/IndependentOpaqueControls.lean
[R250-C27-12]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/03088e5132be807c660b49e3123ce77d0c623e809049b708187ad8b4df94ad16/AuditorRejectsUnsafe.lean
[R250-C27-13]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/035488a9c3f940f49a253424cfb66abd33a2573b632563bef64128304ad73b06/RejectAdmittedProof.lean
[R250-C27-20]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/058cb1413a84322e942f5b2084f79069037cd1f6ed83c64e1b8d137803c3a3eb/PartialDirect.lean
[R250-C27-32]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/07e42ee1e0a132ee35dd7b991872b6beefcb3f5501c3a7ac3748786e82b2857d/CustomAxiom.lean
[R250-C27-41]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/09b240911c6d829ab6240ff2d62e2d2a3b1a56dfd8ac7544ca6ee8ea8a24a072/RejectAddedAxiom.lean
[R250-C27-55]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0f4ffb7dc60be26f65ed1bb8a3935d0aa2dc0337293fcb35926b1e453e380c7d/MissingRightTyping.lean
[R250-C27-56]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0f83919009a9d4a831dbcbbfd6edcafafbc83f88a08a0336ad2fabad838133b7/PartialWrappedRuntime.lean
[R250-C27-57]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0fad4c30e7a4cf0ab4995ef57982463e9dc95089b1106f0393ab8c388959a855/CustomAxiom.lean
[R250-C27-65]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/11ed533d8d1138c9daac9f751b2addec32a2d5c1f1e5aff05baac50d2edeb3b3/PartialWrappedKernel.lean
[R250-C27-77]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/16b94ff32abefcd72d84455b06b045963112d7ffb2b8204d217dc6713097daf5/SCOPE.md
[R250-C27-85]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1ab5ef3f02f0160c5a10cb729039f13eff5595d6a4292438223e2c2e1c27a45e/AuditorRejectsPartial.lean
[R250-C27-88]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1b784056a804d4de0c5012dedd87744bcff93ae5699eb2cc5ba571f02d6c5d66/FiniteBudgetIsNotAllTests.lean
[R250-C27-94]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1de016f96f7f084ab621a08b9c2636a451ca0b32586c911030a7b11cbd4b0b85/AuditorRejectsPartial.lean
[R250-C27-95]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1e20d933f325cddddab82ecbb6d4050c0474f67f5474891832eff17767bdbf2a/INDEPENDENT_MissingPositivity.lean
[R250-C27-96]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1e6aac21a4bd79427610e382d58bbc15a213bf1f8129971e19e99e672f32cc8d/PartialRootKernel.lean
[R250-C27-98]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1ed43a78a52fb5e570d06ddd9f53484c90d4e25892ebbb310480708009fdbafd/BooleanKernelAudit.lean
[R250-C27-103]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1f2385be631a4330db9df6c1f23aadf61798eb0331c25d209a50460698adcaa2/OneEnvironmentIsNotEndpointValidity.lean
[R250-C27-125]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/25eee1be267c97ef0e48e6915e0c8672bd152cca4241b4335425fbf6f3930968/AuditorRejectsCustomAxiom.lean
[R250-C27-131]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/286da8e4766b9f20526b1fb99aa15ad9354a46b3972436cf3c639460c533dcbc/RejectAdmittedProof.lean
[R250-C27-146]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2d9e7402c87fa7e111673fe5dc9d57966a373fd6bcd72412ce95ff81121e2462/AuditorRejectsSorry.lean
[R250-C27-158]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/30541a1f508fde3e9ff271f8d3880bd13c93a2b4455d532a9fb79e1e62d65d28/UnsafeDependency.lean
[R250-C27-163]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3212592033b944ca2fc633e88ac834fd6a35b4d7a6ae377cdd78c25461ae269d/WrongSubtractionOrder.lean
[R250-C27-167]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/33372a5efbdce29a8cb5c3965ea031032de84f48eaf982e42abaf9e6220f12b9/AuditorRejectsCustomAxiom.lean
[R250-C27-169]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/34472a86cae8e55cd75aa953f85bf46f28f5c22c53074b60d1a1004442bf8769/RuntimeChoice.lean
[R250-C27-172]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/34c2d6d13a3633e6fb05aa33dfee1800a5eca3ae18f5b190b18592e41fdc7958/WrongProjectionBound.lean
[R250-C27-179]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/359de6231a4b1393e537f7760d4f05c883ab24c7cd48fc654ffbb4fdaecc5eab/RejectCustomAxiom.lean
[R250-C27-187]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/37d0cd8f7c90cb94a720051955e8d47624505e34f42ba6b1bcba10c66c60b162/RuntimeAudit.lean
[R250-C27-191]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/38f0cafee5502b9a8e5d569cee3c15c86a03c968607bfd1a617bc3e10ade098a/MissingRightMembership.lean
[R250-C27-196]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3a2c534f00f0d5c4e8a2bde6c8bf057078d03a8c37338eeea2a90f14c8d994aa/EffectivePartialObserver.lean
[R250-C27-200]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3ac0153ee816a8d41afa96b630bd06ed54e5be0db2e51567407f399ff2e4e17c/INDEPENDENT_Admission.lean
[R250-C27-210]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3e62bef5fdeec0239669961fdc5144bc54b4764cd58fc55b125890f2e4e881cf/CheckComplexityInterfaces.lean
[R250-C27-211]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3e9cff8a2e5a338230bde4a074595cb50672756682ae6f90f12835fd868021d4/MissingStepRepresentation.lean
[R250-C27-214]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3f6c905cf2363c713795aa75a1edd21fd6b3cc3c312572ca2fd8d9949b596254/MissingSemanticInput.lean
[R250-C27-223]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/410a9a8ecea276190996a85380f2eb49ee387a5ceff9373e2802c33fb02712b3/WrongRawEndpointRelation.lean
[R250-C27-226]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/41593f408c8f8f6543f1b9824d24c5ea3e3340e1c8d7adc3ce0cd6aa0c2de618/CheckBooleanInterfaces.lean
[R250-C27-231]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/42727d6803bc6c8f42102dd56b5473036d83b6aa1b8746b94995db2b7c559033/BareBooleanGatePositive.lean
[R250-C27-233]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/42fa7a899fe0ed22831d4799c49f96d4848c902464654ca198bc7715b1781fb1/AuditorRejectsSorry.lean
[R250-C27-234]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4354990c11644d1df339494be74a63ec016ec0f432ae07fd4dfd7cc07fa9c58f/AllProjectProofAudit.lean
[R250-C27-236]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/43fad5b422f303cd474f2015448ce369ac7c234cd4e1a1fbb9151fb356f3c01b/PartialRootRuntime.lean
[R250-C27-241]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4493327fb512ac8184def34bf332f3e6be5504ee2b199e8c4c940ff796224e74/PointwiseIsNotCrossArgument.lean
[R250-C27-247]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4541dc01f4e2eeae660b97bebea6ae366eef55edd83c75b5db38373b53381206/AdmittedProof.lean


## Exact sources for formal and operational interfaces

[F250-101]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1f12008a084bae138d375e7a9abe05004284f99e688db06a474b0eabbc3d2a82/PolynomialTestBoundary.lean
[F250-104]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1f8bbfa5aae143f4ade726c4dc56c1390814c20bf0cce54b6cb5007b6fd8f554/PowerFaultMutant.lean
[F250-117]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/22d97f7d120194c258791867028edddc5921b8d3ea65d35f73723336019a1077/PythonExprMachine.lean
[F250-138]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/29efba63a8bb81d82a0a3c8fb2bbab68cab27036be5c550adf3b1c87c588b9f0/IndependentKernelChecks.lean
[F250-153]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2fa686bbe04f48f71db17446ec3b75fcc26356c04d142b2dd1f1c3a3e58c7b0a/SparsePolynomial.lean
[F250-165]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/327cf7b9d6679924b7047a76dbefe1fd632bae72cc3524539a2feedca491b367/AllMixedAlgebra.lean
[F250-173]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/352395bd515bdc85e3c4112ca9c9b0f541d6f336bb3ad716bef1ee5198762d09/AllSemanticSubstitution.lean
[F250-215]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3f962df5e2b98f0b294ee2726b10b0c10e2fdfc11cdecee8b22f965c7ab05a25/PythonExprSafety.lean
[F250-240]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4457b5564e7cec234f3515899fc5b67dbce32a9b233ba3c19249bd5f9f9745ba/ReadyTickMutant.lean
[F250-242]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/44afb191c7a8d17e7b561a8d9629ed4094a247110e3b44f0bf8041c2e2fd7de8/ReviewerContract.lean

[F250-C168]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/34393b10d6a7447b0d802cb2aa65f6ec93d3f20446d0de97a9c4e292e59081f2/Orthemology_Fifteenth_Mathematical_Compendium_v1_20261005.md

[F250-C220]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/40e374a62246636ffdbd424f517094dbaa7a7d00cc177675bed19377598e44fd/MATHEMATICAL_COMPANION.md

## Exact public sources for the Ninth argument and evidence reconciliation

[N250C-134]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/b6fa8492065ff7a4d183739ce5886edf9f43ef1ff18938219967769c8dbc4ddd/README.md "Next-250 cohort index 134; SHA-256 b6fa8492065ff7a4d183739ce5886edf9f43ef1ff18938219967769c8dbc4ddd"
[N250C-135]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/c31578f82921ea6e25f3c338bebf0e78b2f91ab248c9fc707f86503a2c0ec0b5/ACCEPTANCE.md "Next-250 cohort index 135; SHA-256 c31578f82921ea6e25f3c338bebf0e78b2f91ab248c9fc707f86503a2c0ec0b5"
[N250C-136]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/3ae1e9e04da476f9960d7d51b617dfaff77168fdc3571e9eaf723aa1cbdb24e2/SOURCE_REVIEW.md "Next-250 cohort index 136; SHA-256 3ae1e9e04da476f9960d7d51b617dfaff77168fdc3571e9eaf723aa1cbdb24e2"
[N250C-137]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/c0d90d203b0d069e9568b19fb7aa6e2560a19503ef59b80f017914ee48f94610/WORDING_CLARIFICATION.md "Next-250 cohort index 137; SHA-256 c0d90d203b0d069e9568b19fb7aa6e2560a19503ef59b80f017914ee48f94610"
[N250C-138]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/57103c998289104191087bbc35bd27fe20fcc42634c17201c6b0242c16259d0a/check_python_edges.py "Next-250 cohort index 138; SHA-256 57103c998289104191087bbc35bd27fe20fcc42634c17201c6b0242c16259d0a"
[N250C-139]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/d71d0783cb99178fb90b9e0e83b50d7be7b2eb74a7784779f52ca79d1c1bb7a4/test_source_contract.py "Next-250 cohort index 139; SHA-256 d71d0783cb99178fb90b9e0e83b50d7be7b2eb74a7784779f52ca79d1c1bb7a4"
[N250C-140]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/3c6cd0c6573778acc4f81e3d1e139e9467b2147ba5ff5fd12c262f1cdfc7101e/replay.py "Next-250 cohort index 140; SHA-256 3c6cd0c6573778acc4f81e3d1e139e9467b2147ba5ff5fd12c262f1cdfc7101e"
[N250C-141]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/f85aa830978c4ed6d4379e313a971a8aba59c1d8c943719ca269064f2511429f/independent_source_controls.py "Next-250 cohort index 141; SHA-256 f85aa830978c4ed6d4379e313a971a8aba59c1d8c943719ca269064f2511429f"
[N250C-142]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/dc580e4d6b6ed0bffec69a976d913b9ca389bf17467d05765978dfbe40c920b7/source_contract.py "Next-250 cohort index 142; SHA-256 dc580e4d6b6ed0bffec69a976d913b9ca389bf17467d05765978dfbe40c920b7"
[N250C-143]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/f40bc24f587245f89eff67da47525e336e0b3731e07b77e4ac25f9f8498770ff/SOURCE_CORRESPONDENCE.md "Next-250 cohort index 143; SHA-256 f40bc24f587245f89eff67da47525e336e0b3731e07b77e4ac25f9f8498770ff"

[Q250A-006]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/02f2ba85547a0798288ec5d307f06fa5b239b8cb9e0faa4b7c7a6ba303097bbe/HYPOTHETICAL_ATOM_APPLICATION_BRIDGE_v2.md
[Q250A-008]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7ff286710275b8873e2847ef21b9a30e70c20f465b6bb680569b8f107b484f3e/RESIDUAL_IDENTITY_COMPLETENESS_FEASIBILITY_v1.md
[Q250A-010]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2c16dbf40f6a945785b51ddc230a0e1f78004fe716a0412492b4345be8c95734/Finite_Certificates_and_Inhabitation_Limits_for_P01AC_and_HasPlus_v1.md
[Q250A-011]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5d58087eab7e247235ec159abc17f6dc6d5779dc7722518f06d5040b25414e3a/Intensional_Identity_Separation_and_Closed_Identity_Conversion.md
[Q250A-015]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/cf337cad057a4c2cb93f2c0145f8132368867257c2b0bf7ee32f7be70d29d11c.lean
[Q250A-016]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/0e3adde9d907e2c0a28afb5087feb42986e2e1fd880682edd70d4b4214790be2.lean
[Q250A-017]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/f75306d1a29cd76385058ca1a819910b1f635a63369d807d484ab6db981a0042.lean
[Q250A-018]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/7cf85525305944e343b50f63e9b593a0fdcab3c89303f2f32cdb37d92c70b1ee.lean
[Q250A-019]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/13c3b0ba7aa7e57fd13bf1d61d28ef842755d5f5103ef9598d18cc885f4e2ca2.lean
[Q250A-020]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/9b1a18c1f189774d22858ba56bb77aecd5fc7506a08195c94fbb1873158a0e7e.lean
[Q250A-021]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/d2cd1460fd8f15eabdcf0bc7044af5b01e82f7ea05242157f2503eaf5585b41e.lean
[Q250A-022]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/5e457f06ecc1622fd53b1917f383c48ce019887910ce0fcb64d99c7e5a2b35f6.lean
[Q250A-023]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/682ad4ce3fda2b69601f267e6c7cfd729d8004fbfdd95c60f12d24fb59bc303e.lean
[Q250A-024]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/e3342d36b3012206cdcf39115d13f14246236f24a122cbd466d6b11bda15d28c.lean
[Q250A-025]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/b29f2917d48adf8462cc272ecffb12e50cb3217b4de360c71f9f13fe75bbeb2a.lean
[Q250A-026]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/6f1afe90be0a46d00763808013733f068a65b4f0fd34d215fb101f0db313856c.lean
[Q250A-027]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/d69233c44f1406044f649204626c4f58155bcb2dc81ac319cf451c473ab13498.lean
[Q250A-028]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/82cd316ba5a0c4efbfb7bbc8ce5e69659e33cb7227d1d4effbaddb3d2f1d66aa.lean
[Q250A-029]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/f2017f4ff67c81eb2d1cb6d4ed3b7efea3e686567409e9d07531a61f6b6d5e59.lean
[Q250A-030]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/e7c7bd5d62f361f4f8a283e1fe442341e87f0200f0494cb2553af4da3a0ff737.lean
[Q250A-031]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/74eec27e534d5b3fe69b0543d343043483288011d7edc85a424cc8458e91a610.lean
[Q250A-032]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/7372d4bd7f7c70fb1b4178743ba84c3ba2f072be88c5a0b04a67a53ccf947c82.lean
[Q250A-033]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/1a969ade6fc6daf226cde5a9f077bb7f16ef5a396a090728c8468356df555e21.lean
[Q250A-034]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/f49f5693dd928e74bb375a3a52a4e8cd0e9792ba0f90b9d543928ab0cf84510f.lean
[Q250A-035]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/df83be41f01616777a5e53aba4e890161c155ad21d6c8b594d0c6cf7806fdf88.lean
[Q250A-036]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/ee15654ad70d9c0e9a77d699a0ff53122d1dcde65f610e26555edc589f97c87e.lean
[Q250A-037]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/57bef4972e782bb85bc9f267bd899afdd09f65ebad610b107348db42b2b3b8b8.lean
[Q250A-038]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/a53b9b16b5013701ab18692035d140db6d34fd3076dd595837dd8808553274f9.lean
[Q250A-039]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/017d12cb7f47f1767310f550277043536a6606e520bdd2f406eabcd91480dd86.lean
[Q250A-040]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/9d06b1180a90048ebe6249e461ed6551fdbf94971a8ba1232b6ffb86e5d45f1a.lean
[Q250A-041]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/538b51e6c199bc43ef2f32d4ffdc16f52043e277b8ea50b1da93a73aa9b38b4d.lean
[Q250A-042]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/222b99bb10321cfe4fbd55ea252631fb0824fa43d966995bb7873a3c8b11b188.lean
[Q250A-050]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3f6e138825d599075b6f920f0079ccc2ca8b7d6c24c8bba0940af4f62d68de1a/DECLARATION_CLAIM_MAP.md
[Q250A-051]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/373659d652481787fc1e9499261ee931b2e9150d003e640f9ae035258f6722fe/README.md
[Q250A-052]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8f5ba88d07447c8c92d49161f82118f805cae707404b477c81936828103d60ef/certificate_checker.py
[Q250A-053]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f2689d00865ed2964fa6dc4337d67da5017f23c34a870e5dad183ccc6ccd6bb9/test_certificate_checker.py
[Q250A-054]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/27c5e18f459c5a6103a35f2fe0570ee2c229832490a02aa4f62064c8c6d25416/test_independent_checker.py
[Q250A-055]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dd69712d1a7b79bdb5fcb55c855c4c13a00725dda1cd8f4dfcdc4544afcbe8fd/check_runtime_agreement.py
[Q250A-056]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bd796dc6d0157d0b8a125cc3b394a866812567f12ce132ee11d2fa3844e081d9/root_extension_checker.py
