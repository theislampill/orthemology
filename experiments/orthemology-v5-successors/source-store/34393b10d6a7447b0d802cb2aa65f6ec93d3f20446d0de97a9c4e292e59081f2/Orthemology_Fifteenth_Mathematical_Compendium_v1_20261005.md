> **DERIVED public reading projection.** Source input T15-COMPENDIUM; original DOCX SHA-256 `06622a9ab290a76993e0864b96b39a78bec725b5a3e59d226d5a8902e552eaca`. Original paragraph and table order, source notices, scope limitations, and native equations are retained. This conversion preserves supplied evidence and research-candidate scope; it is not new scientific acceptance or fresh proof verification.

# Orthemology Fifteenth<br>Mathematical Compendium

Six mathematical research companions<br>5 October 2026

This compendium collects the mathematical papers accompanying the Fifteenth research report. Each paper states its assumptions, argument and limits in full.

### Contents

**Relation to established methods**

**1  Exact Complexity of Original Semantic Identity**

**2  Boolean Identity Completeness**

**3  Bare Boolean Identity and Fixed Type Typability**

**4  Restricted Semantic Identity Completeness for Natural Number Expressions in P01AC**

**5  Polynomial Equality Tests and the Boundary of Effective Semantic Identity Completeness**

**6  What final answers can identify about collective evidence use**

### Scope of the first five papers

The first five papers concern the fixed P01AC research calculus specified in their statements. “Original semantics” refers to that research calculus. Its telescope-indexed typing and paired F/G interpretations have not been adopted as the canonical public P01DF interface; these classifications do not assert a transfer to that distinct interface.

### Reproducibility note

The source package preserves historical receipts for the 71-module Raw replay, the 76-module Raw and Boolean replay, and the 86-module unified replay under lean/verification/historical/ as raw-v2-receipt.json, unified-v3-receipt.json and unified-v4-receipt.json respectively. The current 88-module project-source replay is recorded separately at lean/verification/receipt.json. The representation premise, complexity classifications and univariate polynomial-boundary corollary remain written mathematics.

### Reading and navigation

The contents entries link to each contribution. The heading hierarchy also supports Word’s Navigation pane. Each paper retains its own equation, theorem and section numbering; unqualified references are local to that paper.

The accompanying main report contains the broader research discussion and empirical context. Mathematical notation is editable throughout.

Context for the P01AC papers

## Relation to established methods

The results in the first five papers concern the fixed research P01AC syntax, current typing rules and paired F/G interpretations. Their exact target-specific bridges are distinguished from established classification, iteration and computability methods.

#### Hinze: Church classification

Ralf Hinze, [“Church numerals, twice!”](<https://www.cs.ox.ac.uk/ralf.hinze/publications/Church.pdf>), linked by his publication list to JFP 15(1), 2005, DOI [10.1017/S0956796804005313](<https://doi.org/10.1017/S0956796804005313>). The inspected author manuscript is marked under consideration, not publisher-version verified.

Section 2, pp.2–4, works in System F with inductive types. It gives inverse Church/Peano maps, proves the difficult inverse using parametricity and η-conversion, and transfers folding operations to Church numerals. This is direct precedent for the classification/iteration idea. It is not the P01AC arbitrary-inhabitant theorem: the latter retains original F/G uniformities and proves applied raw-conversion observations without adding η. Nor does the displayed fold correspondence itself certify the current-Has counter/accumulator compiler. No complexity classification is asserted in these inspected passages.

Read: abstract, §§1–2, pp.1–4; page images 3–4. The remaining manuscript was not substantively reviewed.

#### Pistone–Tranchini: contextual equivalence

Paolo Pistone and Luca Tranchini, [“What’s Decidable About (Atomic) Polymorphism?”](<https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSCD.2021.27>), FSCD 2021, DOI 10.4230/LIPIcs.FSCD.2021.27. The official 23-page paper was inspected.

Definition 11 quantifies over typed contexts with Boolean or natural observations. Lemma 17 connects pointwise numeral agreement to natural-contextual equivalence. Proposition 19 makes numerical equivalence decidable in atomic F, but undecidable in ML/F₁; Theorem 23 makes both general atomic-F contextual congruences undecidable. Lemma 7’s simply-typable erasure and the paper’s decidable βη contrast show why termination does not settle contextual equality. Remark 18 invokes primitive-recursive expressivity for System-F undecidability. None establishes the P01AC fixed-carrier hierarchy levels, annotation boundary, or direct current-Has compiler. A relation-preserving transfer is still required.

Read: §§1–2; Lemma 7; §§5–6, especially pp.27:10,12–15. Images 27:12,13,15 checked. Appendices were not reviewed.

No claim of historical priority accompanies these results. Conversion, contextual equivalence and model equality are different targets until a correspondence is proved. A bounded literature comparison does not supply that correspondence or an exhaustive priority search.

Paper 1

## Exact Complexity of Original Semantic Identity

Version 4 · 5 October 2026. Research companion.

### Main result

At the single closed carrier



$$
N=\forall{}X.\,{}(X\to{}X)\to{}X\to{}X,\quad{}\quad{}C=N\to{}\mathsf{R}\mathsf{a}\mathsf{w},
$$



the set of closed, currently typed polynomial pairs whose endpoints are equal in the original P01AC $F/G$ interpretation is ${\Pi{}}_{2}^{0}$-complete under computable many-one reductions. This classification holds both for plain pair codes and for codes carrying checked current endpoint-typing certificates. Malformed and untypable pair codes are excluded by an actual ${\Pi{}}_{2}^{0}$ definition; the upper bound is not merely a promise-problem statement.

The lower bound has one fixed constant endpoint and effectively supplies every required current typing and formation certificate. Consequently neither validity nor invalidity within this correctly typed slice has a sound and complete recursively enumerable certification system. In particular, every sound effective proof system, including the existing extensional repair $\mathsf{H}\mathsf{a}\mathsf{s}\mathsf{E}$, misses some original semantic identities at this one infinite carrier.

The proof identifies the semantic classes of Church inputs with their finite iteration indices, characterises equality of typed endpoints by all canonical raw-conversion tests, and reduces machine totality to those tests. One identified imported representation premise is used. The generic totality and arithmetic-hierarchy methods are inherited; no claim of literature priority is made. The final section distinguishes the written theorem from its kernel-checked semantic bridges.

### 1 Raw syntax and the original semantic target

#### 1.1 Raw computation and polynomial abstraction

Raw terms are finite trees generated by $I,K,S,\mathbf{z},\mathbf{w}$ and binary application, written left-associatively. Here $\mathbf{z}$ and $\mathbf{w}$ are the original inert constructors zero and one. The one-step relation has exactly the rules



$$
Ix\to{}x,\quad{}\quad{}Kxy\to{}x,\quad{}\quad{}Sfgx\to{}fx(gx),
$$



and closure under application in either argument. Let $\simeq{}$ denote its finite reflexive, symmetric, transitive closure, the original Conv. In particular, application respects $\simeq{}$. The inherited confluence theorem gives uniqueness of raw normal forms: convertible normal terms are literally the same finite tree. There are no reduction rules for $\mathbf{z}$ or $\mathbf{w}$.

A polynomial is a finite tree built from $\mathrm{v}\mathrm{a}\mathrm{r}(i)$, $\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(a)$ for a raw term $a$, and application. Its evaluation in $\eta{}:\mathbb{N}\to{}\mathsf{T}\mathsf{e}\mathsf{r}\mathsf{m}$ sends variables to their values, atoms to their labels, and polynomial application to raw application. Put ${\eta{}}_{0}(i)=\mathbf{z}$, the original zeroEnv. A polynomial is closed when it has no variable occurrences.

Write $\mathcal{A}(b)$ for the existing abstract compiler. It binds variable 0 and decrements the indices of older variables. It first tests the whole subterm: if variable 0 is absent, the result is $K$ applied to the index-decremented subterm; otherwise variable 0 compiles to $I$, and an application compiles by the $S$-rule on its two children. This is the existing whole-subterm $K$-priority convention. Its applied computation theorem is



$$
\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(\mathcal{A}(b),\eta{})\,{}a\simeq{}\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(b,a::\eta{}).
$$



(1)

No use below lifts conversion of bodies to conversion of unapplied compiled abstractions.

#### 1.2 The relevant original clauses

A conversion-saturated partial equivalence relation, or PER, is a symmetric, transitive relation on raw terms preserved when either endpoint is replaced by a convertible term. Its domain consists of its self-related terms. The PER $\mathsf{r}\mathsf{a}\mathsf{w}\mathsf{P}\mathsf{E}\mathsf{R}$ is $\simeq{}$; its domain is every raw term. A Link $R:P\rightsquigarrow{}Q$ is a relation whose related endpoints belong to the respective domains and which is stable under replacing the endpoints by $P$- and $Q$-related terms. A Link is not required to be a PER.

A unary type environment $\rho{}$ assigns PERs to type parameters. A relational environment $r$ has unary endpoints ${r}_{L},{r}_{R}$ and a Link at each parameter. Its diagonal $\mathrm{d}\mathrm{i}\mathrm{a}\mathrm{g}(\rho{})$ uses each PER as its own Link. Prefixing a PER or Link extends the corresponding environment at parameter 0.

The following are the original clauses, restricted to the type constructors needed here. We suppress unchanged arguments only where displayed. At a parameter, $F$ is its assigned PER and $G$ its assigned Link. At $\mathsf{R}\mathsf{a}\mathsf{w}$, both are $\simeq{}$. At an arrow,



$$
\begin{gathered}F(A\to{}B,\rho{},\eta{},f,g)\Leftrightarrow{}\forall{}x,y\,{}[F(A,\rho{},\eta{},x,y)\Rightarrow{}F(B,\rho{},\eta{},fx,gy)], \\ G(A\to{}B,r,\eta{},\xi{},f,g)\Leftrightarrow{}F(A\to{}B,{r}_{L},\eta{},f,f)\:{}\wedge{}\:{}F(A\to{}B,{r}_{R},\xi{},g,g) \\ \quad{}\wedge{}\:{}\forall{}x,y\,{}[G(A,r,\eta{},\xi{},x,y)\Rightarrow{}G(B,r,\eta{},\xi{},fx,gy)].\end{gathered}
$$



(2)

Thus the unary arrow clause quantifies over related pairs of arguments. It is not a pointwise equality clause. For universal types, define



$$
{U}_{B}(\rho{},\eta{},t)\Leftrightarrow{}\forall{}P,Q\:{}\forall{}R:P\rightsquigarrow{}Q,\:{}G(B,R::\mathrm{d}\mathrm{i}\mathrm{a}\mathrm{g}(\rho{}),\eta{},\eta{},t,t).
$$



Then the original clauses are



$$
\begin{gathered}F(\forall{}X.B,\rho{},\eta{},t,u)\Leftrightarrow{}{U}_{B}(\rho{},\eta{},t)\wedge{}{U}_{B}(\rho{},\eta{},u)\wedge{}\forall{}P\:{}F(B,P::\rho{},\eta{},t,u), \\ G(\forall{}X.B,r,\eta{},\xi{},t,u)\Leftrightarrow{}F(\forall{}X.B,{r}_{L},\eta{},t,t)\wedge{}F(\forall{}X.B,{r}_{R},\xi{},u,u) \\ \quad{}\wedge{}\forall{}P,Q\:{}\forall{}R:P\rightsquigarrow{}Q,\:{}G(B,R::r,\eta{},\xi{},t,u).\end{gathered}
$$



(3)

Both endpoint-uniformity conjuncts are retained. The original type laws make $F$ a PER at every formed type in an admitted environment. In particular, $F(A,\rho{},\eta{},x,y)$ implies self-relatedness of each endpoint. Current typing is sound for these same $F/G$ clauses.

Let ${p}_{\eta{}}=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,\eta{})$ and ${q}_{\eta{}}=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(q,\eta{})$. For an identity type, the clauses are



$$
\begin{array}{rl}F({\mathrm{I}\mathrm{d}}_{A}(p,q),\rho{},\eta{},u,v) & \Leftrightarrow{}F(A,\rho{},\eta{},{p}_{\eta{}},{q}_{\eta{}})\wedge{}u\simeq{}I\wedge{}v\simeq{}I, \\ G({\mathrm{I}\mathrm{d}}_{A}(p,q),r,\eta{},\xi{},u,v) & \Leftrightarrow{}F(A,{r}_{L},\eta{},{p}_{\eta{}},{q}_{\eta{}})\wedge{}F(A,{r}_{R},\xi{},{p}_{\xi{}},{q}_{\xi{}})\wedge{}u\simeq{}I\wedge{}v\simeq{}I.\end{array}
$$



(4)

These identity clauses do not assert a heterogeneous endpoint relation $G(A,\ldots{},p,q)$. Their two substantive heterogeneous requirements are the two displayed unary equalities.

#### 1.3 Two exact finite-code targets

In the actual syntax, let



$$
\begin{array}{rl}NBody & =\mathrm{a}\mathrm{r}\mathrm{r}(\mathrm{a}\mathrm{r}\mathrm{r}(\mathrm{p}\mathrm{a}\mathrm{r}\mathrm{a}\mathrm{m}0,\mathrm{p}\mathrm{a}\mathrm{r}\mathrm{a}\mathrm{m}0),\mathrm{a}\mathrm{r}\mathrm{r}(\mathrm{p}\mathrm{a}\mathrm{r}\mathrm{a}\mathrm{m}0,\mathrm{p}\mathrm{a}\mathrm{r}\mathrm{a}\mathrm{m}0)), \\ N & =\mathrm{a}\mathrm{l}\mathrm{l}(NBody),\quad{}\quad{}C=\mathrm{a}\mathrm{r}\mathrm{r}(N,\mathsf{R}\mathsf{a}\mathsf{w}).\end{array}
$$



Here $\mathrm{a}\mathrm{r}\mathrm{r}(A,B)=\mathrm{p}\mathrm{i}(A,\mathrm{w}\mathrm{k}(B))$. Both types are formed in the empty context and have no free type parameters or term variables. Write ${D}_{C}(p,q)$ for the syntactic domain condition



$$
\mathrm{S}\mathrm{c}\mathrm{o}\mathrm{p}\mathrm{e}\mathrm{d}(0,p)\wedge{}\mathrm{S}\mathrm{c}\mathrm{o}\mathrm{p}\mathrm{e}\mathrm{d}(0,q)\wedge{}\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}p\:{}C\wedge{}\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}q\:{}C.
$$



(5)

For any two finite polynomials put $P={p}_{{\eta{}}_{0}}$, $Q={q}_{{\eta{}}_{0}}$, and



$$
{V}_{C}(p,q)\Leftrightarrow{}\forall{}\rho{}\:{}F(C,\rho{},{\eta{}}_{0},P,Q).
$$



(6)

Use a standard effective coding of the exact finite syntax: parsing and literal equality are decidable, and encoding and decoding finite trees are effective. Define



$$
{E}_{C}=\{\langle{}p,q\rangle{}:{D}_{C}(p,q)\wedge{}{V}_{C}(p,q)\}.
$$



(7)

All malformed codes are outside ${E}_{C}$. Define ${E}_{C}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$ similarly on quadruple codes $\langle{}p,q,a,b\rangle{}$, requiring closed, well-formed endpoints, a checked finite current derivation $a$ of $\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}p\:{}C$, a checked derivation $b$ of $\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}q\:{}C$, and (6). An invalid supplied certificate is rejected even if another correct certificate exists.

For every pair in the domain (5), current identity formation gives ${\mathrm{I}\mathrm{d}}_{C}(p,q)$. By (4), (6) is equivalent to original unary identity validity at $\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(I)$, and to original relational identity validity at that same polynomial. For relational validity, use (6) separately at ${r}_{L}$ and ${r}_{R}$; conversely take $r=\mathrm{d}\mathrm{i}\mathrm{a}\mathrm{g}(\rho{})$. Empty-context valuations are ${\eta{}}_{0}$, and closed endpoints are valuation-independent. A semantic polynomial witness at this identity necessarily gives the endpoint equality in (4); when that equality holds, $\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(I)$ is a witness. Thus existential semantic identity witnessing gives the same two code sets. None of this asserts that current $\mathsf{H}\mathsf{a}\mathsf{s}$ derives every such identity.

### 2 Every semantic natural has a unique iteration index

For raw $f,x$, set ${f}^{0}x=x$ and ${f}^{n+1}x=f({f}^{n}x)$. Let



$$
{h}_{n}={\mathbf{z}}^{n}\mathbf{w}.
$$



The ${h}_{n}$ are distinct normal finite trees because their heads are inert. Inherited raw confluence therefore gives



$$
{h}_{m}\simeq{}{h}_{n}\quad{}\Rightarrow{}\quad{}m=n.
$$



(8)

**Lemma 1.** For arbitrary $\rho{},\eta{},t$,



$$
F(N,\rho{},\eta{},t,t)\quad{}\Rightarrow{}\quad{}\exists{}!n\:{}\forall{}f,x\quad{}tfx\simeq{}{f}^{n}x.
$$



(9)

All term quantifiers here range over raw terms, including semantic inputs with no assumed syntactic typing.

**Proof.** For fixed raw $f,x$, define



$$
{R}_{f,x}(a,b)\Leftrightarrow{}\exists{}n\,{}[a\simeq{}{h}_{n}\wedge{}b\simeq{}{f}^{n}x].
$$



(10)

This is a Link from $\mathsf{r}\mathsf{a}\mathsf{w}\mathsf{P}\mathsf{E}\mathsf{R}$ to itself. Both endpoints belong to its PER domains by reflexivity. If either endpoint is replaced by a convertible term, transitivity transports the displayed conversions using the same $n$, proving the Link’s respect condition.

Both $\mathbf{z}$ and $f$ preserve raw conversion by application congruence. Moreover ${R}_{f,x}(\mathbf{w},x)$ holds, and ${R}_{f,x}(a,b)$ implies ${R}_{f,x}(\mathbf{z}a,fb)$, using respectively the indices 0 and $n+1$. These facts supply the two endpoint-function conditions and the cross-argument condition of the original $G$-arrow clause. Instantiate the first uniformity conjunct of the hypothesis in (9) with the two raw PERs and this Link, then apply the nested arrow clauses to $(\mathbf{z},f)$ and $(\mathbf{w},x)$. The result is



$$
{R}_{f,x}(t\mathbf{z}\mathbf{w},tfx).
$$



(11)

The choice $f=\mathbf{z},x=\mathbf{w}$ yields one index $n$. Every other choice yields some $m$ with the same first component $t\mathbf{z}\mathbf{w}$, so (8) forces $m=n$. The second component of (11) proves (9). Applying any two candidate observational equations to $\mathbf{z},\mathbf{w}$ and using (8) proves uniqueness. ∎

The lemma assumes neither MarkerFree, definability, nor normalisation of $t$. The graph is a genuine Link, not an assumed PER. A result about a marker-free syntax or a separate unary code type would not by itself prove this all-input statement.

#### 2.1 Canonical inputs at every index

Define exact polynomials and raw evaluations by



$$
{v}_{0}=\mathrm{v}\mathrm{a}\mathrm{r}(0),\quad{}{v}_{n+1}=\mathrm{v}\mathrm{a}\mathrm{r}(1){v}_{n},\quad{}{w}_{n}=\mathcal{A}(\mathcal{A}({v}_{n})),\quad{}{u}_{n}=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}({w}_{n},{\eta{}}_{0}).
$$



(12)

**Lemma 2.** These polynomials are closed and satisfy, for every $n,\rho{},f,x$,



$$
\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}{w}_{n}\:{}N,\quad{}\quad{}F(N,\rho{},{\eta{}}_{0},{u}_{n},{u}_{n}),\quad{}\quad{}{u}_{n}fx\simeq{}{f}^{n}x.
$$



(13)

**Proof.** In context $[X,X\to{}X]$, induction on $n$ with the variable and arrow-elimination rules types ${v}_{n}:X$. Twice arrow introduction and once universal introduction give the first assertion, with scope supplied by the compiler’s scope theorem. Current soundness supplies the middle assertion. Apply (1) twice and evaluate the iteration body by induction to obtain the last assertion. Every finite tree and derivation in this construction is computable from $n$. ∎

#### 2.2 The same-index converse

**Lemma 3.** Fix $\rho{},\eta{}$. Two self-related inhabitants $s,t$ of $N$ are $F(N,\rho{},\eta{})$-related if and only if their indices from (9) agree.

**Proof of necessity.** Instantiate the final universal conjunct of their $F$-relation with $\mathsf{r}\mathsf{a}\mathsf{w}\mathsf{P}\mathsf{E}\mathsf{R}$, and the two arrow clauses with $(\mathbf{z},\mathbf{z})$ and $(\mathbf{w},\mathbf{w})$. Conversion congruence supplies the required function relation. This gives $s\mathbf{z}\mathbf{w}\simeq{}t\mathbf{z}\mathbf{w}$. Their index equations and (8) force equal indices.

**Proof of sufficiency.** Suppose the shared index is $n$. The two self-relatedness assumptions supply the two distinct endpoint-uniformity conjuncts of (3). For the remaining conjunct fix an arbitrary PER $A$, any related functions $f,g$ at $A\to{}A$, and any $A$-related inputs $x,y$. Induction proves



$$
A({f}^{k}x,{g}^{k}y)\quad{}\quad{}(k\in{}\mathbb{N}).
$$



The base is the input relation; the successor is exactly the full cross-argument arrow relation for $f,g$. Conversion saturation of $A$, applied to the two index equations at $k=n$, transports this relation to $A(sfx,tgy)$. These are precisely the nested arrow clauses required for the final universal conjunct. ∎

Uniformity is retained from the hypotheses, not inferred from observational equations alone. At ${\eta{}}_{0}$, Lemmas 1–3 and (13) show that every semantic class has exactly the canonical representative index $n$. No equality between the unapplied ${u}_{n}$ and a separately chosen numeric encoding is needed.

### 3 Typed validity is exactly the set of all canonical tests

For finite polynomials define



$$
{T}_{C}(p,q)\Leftrightarrow{}\forall{}n\quad{}P{u}_{n}\simeq{}Q{u}_{n}.
$$



(14)

**Theorem 4.** If $\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}p\:{}C$ and $\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}q\:{}C$, then



$$
{V}_{C}(p,q)\quad{}\Leftrightarrow{}\quad{}{T}_{C}(p,q).
$$



(15)

**Proof.** Forward, specialise (6) to the explicit environment constantly equal to $\mathsf{r}\mathsf{a}\mathsf{w}\mathsf{P}\mathsf{E}\mathsf{R}$. Apply the arrow relation to the self-related canonical input in (13). The raw output clause yields each test in (14).

Conversely, assume (14) and fix any $\rho{}$. Given any $F(N,\rho{},{\eta{}}_{0},x,y)$, the PER endpoint law makes $x$ self-related. Lemma 1 supplies its index $n$, and Lemma 3 relates $x$ to ${u}_{n}$ in this same environment. Symmetry and transitivity then relate ${u}_{n}$ to $y$. Current soundness of the two endpoint typings gives the self-relations for $P$ and $Q$ at $C$, again in this arbitrary $\rho{}$. Their arrow clauses and the $n$th test give



$$
Px\simeq{}P{u}_{n}\simeq{}Q{u}_{n}\simeq{}Qy.
$$



(16)

This is the raw conclusion for every related input pair, so the original cross-argument arrow clause gives $F(C,\rho{},{\eta{}}_{0},P,Q)$. Since $\rho{}$ was arbitrary, (6) follows. ∎

Both endpoint typings are essential to this proof. The theorem is not asserted for untyped endpoint pairs, does not enumerate PERs, and does not replace the universal environment quantifier by a claimed environment-independence principle.

### 4 A genuine arithmetical upper bound

A set is ${\Pi{}}_{2}^{0}$ if it has a presentation $\{k:\forall{}n\exists{}w\:{}R(k,n,w)\}$ with recursive $R$. A many-one reduction is a total computable function preserving membership in both directions.

Raw terms, polynomials, types, contexts and rule annotations are finite trees. The exact compatible raw Step and Conv constructors admit a recursive finite-certificate validator. Current $\mathsf{H}\mathsf{a}\mathsf{s}$ does too, using fully annotated finite derivation trees for its mutually defined context, formation and typing rules and their finite-conversion premises. In particular, its finite-import rule’s apparent family of premises is bounded by the supplied finite list: its certificate contains one formation subcertificate for each list entry. Lookup, scope, weakening and substitution are effective syntactic checks. No semantic oracle is part of this validator.

Parsing, closure, bracket compilation, evaluation at ${\eta{}}_{0}$, and the construction of ${u}_{n}$ are computable. Let $R(z,n,w)$ reject unless $z$ parses as a closed pair $(p,q)$ and $w$ parses as two checked current endpoint-typing certificates and one checked raw-conversion certificate for the $n$th test. Every part of $R$ is recursive. Then



$$
z\in{}{E}_{C}\quad{}\Leftrightarrow{}\quad{}\forall{}n\exists{}w\:{}R(z,n,w).
$$



(17)

If $z\in{}{E}_{C}$, fixed endpoint derivations can be reused in every witness, and (15) supplies each conversion certificate. Conversely, the instance $n=0$ supplies both endpoint typings, all instances supply their raw tests, and (15) proves validity. Malformed, open or untypable pairs fail the recursive matrix for every possible witness. Witnesses need not be selected uniformly or coherently from semantic truth.

For ${E}_{C}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$, the recursive matrix checks the supplied certificates in $z$ and asks only for the conversion certificate in the existential witness. Thus both actual sets are ${\Pi{}}_{2}^{0}$. Existential endpoint derivations have not introduced an extra alternation: they are included in the witnesses already present in (17).

### 5 The pure computation interface

The sublanguage $\mathsf{C}\mathsf{l}\mathsf{o}\mathsf{s}\mathsf{e}\mathsf{d}\mathsf{I}\mathsf{K}\mathsf{S}$ consists of finite raw trees generated by $I,K,S$ and application alone. Its pure weak reduction has the same three contraction rules and the same application compatibility as §1.1. Write ${\simeq{}}_{\kern0pt{}p}$ for finite pure weak conversion and $\mathsf{W}\mathsf{N}\mathsf{F}(a)$ when $a$ reduces by finitely many such steps to a term with no pure weak step. “Weak” here names this combinatory relation; it does not limit compatibility to head reduction. If free variables are admitted in a presentation of the pure calculus, closed endpoints still have the meaning just specified.

**Lemma 5.** For pure closed endpoints, raw conversion and pure weak conversion coincide. Moreover, if a pure term is raw-convertible to a pure raw normal form, it has a pure weak normal form.

**Proof.** Pure certificates embed in raw syntax. In the other direction, define a retraction sending both inert raw constructors to $I$, fixing $I,K,S$, and commuting with application. Each raw Step constructor maps to a pure weak step: the three contractions remain the corresponding contractions, and the two compatibility cases follow inductively. Induction on a finite Conv certificate then gives pure conversion. The retraction fixes pure endpoints, even when reversed steps introduced markers into intermediate raw terms. Free variables in intermediate pure conversion chains can likewise all be substituted by $I$, preserving the contraction and compatibility rules and fixing closed endpoints.

For the final assertion, raw confluence joins the given pure term and its convertible raw normal form. Normality makes the latter reduction stationary, yielding a raw reduction from the former to that normal form. Retract this finite reduction to a pure reduction. A pure raw normal form has no pure step, so this gives a pure weak normal form. ∎

The following is the single imported premise block. Downward and upward arrows mean defined and undefined values of a partial function.



$$
\begin{array}{c}\nu{}(0)=KI;\quad{}\nu{}(n+1)=SB\nu{}(n);\quad{}B=S(KS)K. \\ \mathrm{P}\mathrm{a}\mathrm{r}\mathrm{t}\mathrm{i}\mathrm{a}\mathrm{l}-\mathrm{r}\mathrm{e}\mathrm{c}\mathrm{u}\mathrm{r}\mathrm{s}\mathrm{i}\mathrm{v}\mathrm{e}\ h:\quad{}\exists{}R\in{}\mathsf{C}\mathsf{l}\mathsf{o}\mathsf{s}\mathsf{e}\mathsf{d}\mathsf{I}\mathsf{K}\mathsf{S},\quad{}\forall{}m,n: \\ h(m,n)\downarrow{}\Rightarrow{}R\nu{}(m)\nu{}(n){\simeq{}}_{\kern0pt{}p}\nu{}(h(m,n)); \\ h(m,n)\uparrow{}\Rightarrow{}\neg{}\mathsf{W}\mathsf{N}\mathsf{F}(R\nu{}(m)\nu{}(n)).\end{array}
$$



(R)

Hindley–Seldin \[1\].

Fix a conventional effective enumeration of machines on natural-number inputs with a decidable bounded simulation relation. Define $H(e,n)$ by simulating machine $e$ on input $n$ and returning 0 if it halts, with no value otherwise. Bounded simulation is recursive; searching for a successful time and then returning 0 makes $H$ partial recursive. Apply (R) once to this binary $H$, and call the chosen finite term $U$. Put $s=SB$, using the symbols fixed in (R).

The choice of $U$ is made once for the whole reduction. A reduction program can contain this fixed finite string, compute the finite code $\nu{}(e)$, and build the templates below. An existence proof of this computable map needs neither an executable listing of $U$ nor an algorithm selecting representers for arbitrary functions. No term is asked to inspect unencoded raw syntax.

### 6 A totality reduction with current typed endpoints

For arbitrary finite raw labels $g,o,c$, define



$$
\begin{array}{rl}{a}_{g} & =\mathcal{A}(\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(g)\mathrm{v}\mathrm{a}\mathrm{r}(0)), \\ {b}_{g,o,c} & =\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(o)((\mathrm{v}\mathrm{a}\mathrm{r}(0)\,{}{a}_{g})\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(c)), \\ \mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}\mathrm{e}\mathrm{r}(g,o,c) & =\mathcal{A}({b}_{g,o,c}),\quad{}\quad{}\mathrm{c}\mathrm{o}\mathrm{n}\mathrm{s}\mathrm{t}\mathrm{a}\mathrm{n}\mathrm{t}(c)=\mathcal{A}(\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(c)), \\ {p}_{e} & =\mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}\mathrm{e}\mathrm{r}(s,U\nu{}(e),\nu{}(0)),\quad{}\quad{}q=\mathrm{c}\mathrm{o}\mathrm{n}\mathrm{s}\mathrm{t}\mathrm{a}\mathrm{n}\mathrm{t}(\nu{}(0)).\end{array}
$$



(18)

Here $U\nu{}(e)$ is one composite raw atom label. It is finite regardless of the behaviour of the computations in which it later participates.

**Lemma 6.** The map $e\mapsto{}({p}_{e},q)$ is total computable, and effectively supplies closed endpoints, current derivations



$$
\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}{p}_{e}\:{}C,\quad{}\quad{}\mathsf{H}\mathsf{a}\mathsf{s}\:{}[]\:{}q\:{}C,
$$



and formation of ${\mathrm{I}\mathrm{d}}_{C}({p}_{e},q)$.

**Proof.** Current rawAtom admits every raw label, and rawApp types raw application. In any formed context, extend by a raw variable, type the body of ${a}_{g}$ using those rules and the variable rule, and apply piIntro. This gives the closed polynomial ${a}_{g}:\mathsf{R}\mathsf{a}\mathsf{w}\to{}\mathsf{R}\mathsf{a}\mathsf{w}$.

In context $[N]$, the variable rule gives variable 0 type $N$, since $\mathrm{w}\mathrm{k}(N)=N$. Universal elimination at $\mathsf{R}\mathsf{a}\mathsf{w}$ uses the literal syntactic identity



$$
\mathrm{t}\mathrm{i}\mathrm{n}\mathrm{s}\mathrm{t}(NBody,\mathsf{R}\mathsf{a}\mathsf{w})=(\mathsf{R}\mathsf{a}\mathsf{w}\to{}\mathsf{R}\mathsf{a}\mathsf{w})\to{}\mathsf{R}\mathsf{a}\mathsf{w}\to{}\mathsf{R}\mathsf{a}\mathsf{w}.
$$



Two arrow eliminations with ${a}_{g}$ and $\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(c)$, followed by rawApp with $\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(o)$, type ${b}_{g,o,c}:\mathsf{R}\mathsf{a}\mathsf{w}$. Arrow introduction types the tester at $C$. A raw constant body and arrow introduction type $\mathrm{c}\mathrm{o}\mathrm{n}\mathrm{s}\mathrm{t}\mathrm{a}\mathrm{n}\mathrm{t}(c):C$. All scope premises follow from the displayed finite trees and the compiler’s scope theorem. Type formation uses the current parameter, raw, arrow and universal rules; identity formation uses the endpoint typings.

These are fixed finite annotated derivation templates. Substitute the finite labels in (18) and compute their certificates. Raw typing requires no termination test and uses no new identity rule, atom/application bridge or calculus extension. ∎

Set $d=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}({a}_{s},{\eta{}}_{0})$, ${P}_{e}=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}({p}_{e},{\eta{}}_{0})$ and $Q=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(q,{\eta{}}_{0})$. Applied bracket computation gives, for all raw $z,t$,



$$
dz\simeq{}sz,\quad{}\quad{}{P}_{e}t\simeq{}(U\nu{}(e))(t\,{}d\,{}\nu{}(0)),\quad{}\quad{}Qt\simeq{}\nu{}(0).
$$



(19)

Closedness of ${a}_{s}$ justifies using the same $d$ under the extended body environment. None of these equalities is an abstraction-congruence principle.

Induction on $n$, using application congruence, the first equation in (19), and the defining recursion in (R), gives



$$
{d}^{n}\nu{}(0)\simeq{}\nu{}(n).
$$



(20)

Indeed the base is reflexivity; the successor converts $d({d}^{n}\nu{}(0))$ first to $d\nu{}(n)$, then to $s\nu{}(n)$, the next finite code. If a semantic natural $t$ has index $n$, its equation from (9), followed by (20) and (19), therefore gives



$$
{P}_{e}t\simeq{}U\nu{}(e)\nu{}(n).
$$



(21)

In particular this holds for $t={u}_{n}$ by (13). Equation (21) is the compiled observer’s computation bridge. It does not identify unapplied canonical inputs with the numeric codes.

Let $\mathsf{T}\mathsf{O}\mathsf{T}=\{e:\mathrm{m}\mathrm{a}\mathrm{c}\mathrm{h}\mathrm{i}\mathrm{n}\mathrm{e}\ e\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s}\ \mathrm{o}\mathrm{n}\ \mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\mathrm{y}\ \mathrm{i}\mathrm{n}\mathrm{p}\mathrm{u}\mathrm{t}\}$.

**Theorem 7.** The effective construction (18) satisfies



$$
e\in{}\mathsf{T}\mathsf{O}\mathsf{T}\quad{}\Leftrightarrow{}\quad{}({p}_{e},q)\in{}{E}_{C}.
$$



(22)

**Proof of the forward implication.** If $e$ is total, $H(e,n)$ is defined with value 0 for every $n$. Use the defined case of (R), pure inclusion from Lemma 5, (21) at ${u}_{n}$, and the constant equation in (19). This proves ${P}_{e}{u}_{n}\simeq{}Q{u}_{n}$ for every $n$. Theorem 4 gives validity, and Lemma 6 gives the full domain condition.

**Proof of the reverse implication.** If $e$ is not total, choose an input $n$ on which it does not halt. Validity would imply the $n$th test by Theorem 4. Combining that test with (21) and (19) would make the pure term on the right of (21) raw-convertible to $\nu{}(0)$. The latter is a raw normal form by direct inspection of its definition in (R): no head has enough arguments for a contraction. Lemma 5 would therefore give a pure weak normal form for that term, contradicting the undefined case of (R). Thus validity fails. ∎

The negative argument requires the no-normal-form part of (R); defined-input computation alone would not justify it. Lemma 5 supplies the exact pure/raw bridge even if a raw conversion proof passes through inert markers. The reduction keeps $U$, $q$, $C$, and the template fixed. By Lemma 6 it also yields a total computable reduction to ${E}_{C}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$, including its two endpoint certificates.

### 7 Exact completeness and both enumeration obstructions

**Lemma 8.** $\mathsf{T}\mathsf{O}\mathsf{T}$ is ${\Pi{}}_{2}^{0}$-complete.

**Proof.** Bounded halting is decidable, and



$$
e\in{}\mathsf{T}\mathsf{O}\mathsf{T}\Leftrightarrow{}\forall{}n\exists{}t\,{}[\mathrm{m}\mathrm{a}\mathrm{c}\mathrm{h}\mathrm{i}\mathrm{n}\mathrm{e}\ e\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s}\ \mathrm{o}\mathrm{n}\ \mathrm{i}\mathrm{n}\mathrm{p}\mathrm{u}\mathrm{t}\ n\ \mathrm{w}\mathrm{i}\mathrm{t}\mathrm{h}\mathrm{i}\mathrm{n}\ t\ \mathrm{s}\mathrm{t}\mathrm{e}\mathrm{p}\mathrm{s}].
$$



For any ${\Pi{}}_{2}^{0}$ set $A$, fix a recursive matrix with $k\in{}A\Leftrightarrow{}\forall{}n\exists{}m\,{}R(k,n,m)$. A machine with $k$ embedded in its finite program, on input $n$, tests $m=0,1,\ldots{}$ until $R(k,n,m)$ holds and then halts. Each test terminates because $R$ is recursive. In the chosen effective machine indexing, the finite program and its index are computable from $k$. It is total exactly when $k\in{}A$. ∎

**Theorem 9.** Both ${E}_{C}$ and ${E}_{C}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$ are ${\Pi{}}_{2}^{0}$-complete under computable many-one reductions.

**Proof.** Section 4 supplies their upper bounds. Lemma 8 and the two effective versions of (22) supply their lower bounds. ∎

The classification fixes the actual syntax and carrier. It gives no upper bound for original semantic identity at arbitrary carriers.

#### 7.1 Validity is not recursively enumerable

For completeness, the obstruction can be obtained without invoking a hierarchy-separation theorem. Let $K$ be an ordinary machine/input halting set. Finite simulation enumerates $K$. Its complement is not recursively enumerable: enumerations of both sets would decide halting by dovetailing, whereas a putative halting decider yields the usual machine that halts precisely when the decider says it will not.

Given a halting instance $k$, construct a program ${A}_{k}$ which, on input $n$, simulates that fixed instance for $n$ steps. It halts if the simulation has not halted, and otherwise loops. Thus ${A}_{k}$ is total exactly when $k\notin{}K$. Its index is computable from $k$. Compose with (18) to reduce $\overline{K}$ to valid identities. Every output is already in ${D}_{C}$, with computably supplied certificates. Neither ${E}_{C}$ nor ${E}_{C}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$ can be recursively enumerable.

#### 7.2 Invalidity within the correctly typed slice is not recursively enumerable

Define the typed invalidity set



$$
{I}_{C}=\{\langle{}p,q\rangle{}:{D}_{C}(p,q)\wedge{}\neg{}{V}_{C}(p,q)\}.
$$



(23)

Construct a program ${B}_{k}$ which, on every input, waits for the fixed halting instance $k$ to halt, and halts if it does. This program is total exactly when $k\in{}K$. Its computable endpoint image under (18) belongs to ${I}_{C}$ exactly when $k\notin{}K$. Hence ${I}_{C}$ is not recursively enumerable. The same proof works when the correct endpoint certificates are included.

Since these reductions always produce correctly typed closed pairs, they also show that the complements of ${E}_{C}$ and ${E}_{C}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$ are not recursively enumerable. The conclusion does not arise from placing malformed inputs in a complement. Thus both validity sets are neither r.e. nor co-r.e., and typed invalidity itself is not r.e.

### 8 The fixed carrier is infinite

For each $k$, set



$$
{r}_{k}=\mathrm{c}\mathrm{o}\mathrm{n}\mathrm{s}\mathrm{t}\mathrm{a}\mathrm{n}\mathrm{t}({h}_{k}),\quad{}\quad{}{R}_{k}=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}({r}_{k},{\eta{}}_{0}).
$$



Lemma 6’s constant template types ${r}_{k}:C$, and applied bracket computation gives ${R}_{k}t\simeq{}{h}_{k}$ for every raw $t$. Current soundness makes each ${R}_{k}$ a semantic inhabitant of $C$. In any environment $\rho{}$, if $F(C,\rho{},{\eta{}}_{0},{R}_{k},{R}_{\ell{}})$ held, apply its arrow clause to the self-related input ${u}_{0}$. The raw output relation would force ${h}_{k}\simeq{}{h}_{\ell{}}$, and (8) gives $k=\ell{}$. Hence every such environment has infinitely many semantic classes represented by explicitly current-typed closed polynomials at this one carrier.

### 9 Positive and negative certification limits

**Theorem 10.** No recursively enumerable finite-proof presentation with an effective target projection can be both sound and complete for validity on the typed family (18). Nor can one be both sound and complete for invalidity on that family.

**Proof.** For a positive presentation, enumerate its finite proofs and inspect the projected context and conclusion. On an effectively constructed target ${\mathrm{I}\mathrm{d}}_{C}({p}_{e},q)$, accept as soon as a proof has empty context and that exact finite conclusion type. Any proof polynomial is allowed. Original identity soundness and (4) force validity; existential completeness would eventually accept every valid target. Apply this procedure to the family constructed from ${A}_{k}$ in §7.1. It would semidecide $\overline{K}$, a contradiction.

For a negative presentation, enumerate certificates and compare their effective targets with the pairs constructed from ${B}_{k}$ in §7.2. Soundness excludes valid targets, and completeness would accept every invalid target, again semideciding $\overline{K}$. The argument applies equally if certificates are only recursively enumerable rather than given by a decidable verifier. ∎

A sound recursively enumerable extension of current $\mathsf{H}\mathsf{a}\mathsf{s}$ is a special case of the positive statement. Extending $\mathsf{H}\mathsf{a}\mathsf{s}$ is not necessary: soundness and completeness on this certified family already conflict. Conversely, no assumption is needed that every other endpoint pair admitted by an extension has a current typing derivation.

Finite rule schemas with effectively checkable finite evidence have recursively enumerable proofs. A finite printed rule with an oracle or non-r.e. semantic side condition need not. These conclusions allow proofs of particular positive or negative instances, complete effective restricted fragments, a non-effective complete presentation, or a different semantic target.

#### 9.1 The consequence for HasE

The existing $\mathsf{H}\mathsf{a}\mathsf{s}\mathsf{E}$ includes current $\mathsf{H}\mathsf{a}\mathsf{s}$ through $\mathsf{H}\mathsf{a}\mathsf{s}\mathsf{P}\mathsf{l}\mathsf{u}\mathsf{s}$. Its syntax imports $\mathsf{P}\mathsf{o}\mathsf{l}\mathsf{y}\mathsf{C}\mathsf{o}\mathsf{n}\mathsf{v}\mathsf{P}\mathsf{l}\mathsf{u}\mathsf{s}$ and adds the extensional rules piExt and allExt; omitting the imported conversion relation would misdescribe the system. Its established fundamental theorem is sound for the same original $F/G$ interpretation.

Its finite annotated grammar is recursively enumerable. Substitution and scope are effective; conversion premises carry finite certificates; and the family of premises of the finite-import rule ranges over a supplied finite list. Enumerating and checking finite annotated proof trees therefore enumerates its conclusions. This is a mathematical consequence of the grammar, not a claim that a new executable $\mathsf{H}\mathsf{a}\mathsf{s}\mathsf{E}$ checker has been written here.

Theorem 10 consequently applies to $\mathsf{H}\mathsf{a}\mathsf{s}\mathsf{E}$: some valid original identities in the fixed typed family lack any $\mathsf{H}\mathsf{a}\mathsf{s}\mathsf{E}$ proof. Its previously established positive witness and raw-conversion obstruction retain their exact meanings. Effective sound repairs may settle particular missed identities while still failing full semantic completeness.

### 10 The finite-fragment boundary

The result concerns the unbounded semantic claim (6), equivalently the infinite test family (14). It does not invalidate the inherited finite-evidence results.

A supplied finite conversion or typing derivation is decidably checked. A finite list of arbitrary raw-conversion obligations, without supplied certificates, is only guaranteed to be semidecidable: dovetail certificate searches and accept when each succeeds. The list’s finiteness alone does not make this a decision procedure; even one arbitrary raw-conversion question can be undecidable. A bounded search can safely report that it has not yet found a certificate, but that outcome need not certify nonconversion. A genuinely restricted, normalising finite-source class can retain its separate inherited conversion decision theorem.

Successful canonical tests at finitely many indices do not establish (14). For any prescribed finite set of indices $S$, there is a finite machine that halts with no further work on inputs in $S$ and loops elsewhere. The proof of Theorem 7 gives a typed endpoint pair passing every test in $S$ but failing validity, since $\mathbb{N}\setminus{}S$ is nonempty. This uses no change to the carrier or endpoint typing. Extra hypotheses may make a particular finite criterion sufficient, but the finite successes alone do not supply them.

These distinctions preserve finite certificate completeness, restricted conversion decision procedures, and bounded procedures with explicit inconclusive outcomes. They do not turn finite evidence into a uniform complete positive or negative certification of the unbounded semantic identity relation.

### 11 Inherited methods and verification boundary

The generic totality reduction, the arithmetic-hierarchy classification method, and the use of nonhalting to exclude complete r.e. certification are inherited mathematics. The earlier programme already uses related computability obstructions for other targets. No novelty claim is made for those methods or for the imported premise (R).

The target-specific argument combines arbitrary-semantic-input graph standardness, the same-index converse retaining both uniformity conjuncts, the canonical-test characterisation with actual current endpoint typings, and the directly typed totality family. The result concerns one fixed original $F/G$ carrier. It neither supplies an upper bound at arbitrary carriers nor closes another programme target or adopts a replacement calculus.

#### 11.1 Mathematical dependencies

The proof uses the unchanged finite P01AC syntax, current formation and typing rules, original $F/G$ clauses, their soundness and PER/diagonal laws, raw confluence, and applied bracket computation. Section 5 proves the local pure/raw correspondence; (R) is the identified imported input. Finite effective syntax coding, the two recursive matrices, the effective machine-index constructions, and the hierarchy and enumeration arguments are written mathematical components.

#### 11.2 Kernel checks and reproducibility

The separate Lean 4.19.0 semantic-kernel successor preserves all 65 frozen project modules and the four predecessor additions byte-for-byte. Its two further modules, EffectiveCanonicalTests and EffectivePartialObserver, have received independent source, interface and compiled-proof-dependency review. The six additions leave the original syntax, current typing rules, raw conversion, bracket compiler and $F/G$ clauses unchanged.

In the namespace P01AC.IdentityComplexity, endpoint\_valid\_iff\_canonical\_tests proves Theorem 4’s semantic equivalence with both current endpoint typings explicit. Its reverse direction retains arbitrary cross-related arguments and every unary environment. The same-index results preserve the two endpoint-uniformity hypotheses. The fixed observer’s current typing, formation, closure, scope and fully applied computation are also checked. The unchanged predecessor modules provide graph standardness, canonical inputs, the original unary/relational identity and semantic-witness bridges, the infinite typed family, and current/$\mathsf{H}\mathsf{a}\mathsf{s}\mathsf{E}$ soundness interfaces.

The principal original\_universal\_identity\_iff\_total proves the original all-relation-environment identity equivalence for an arbitrary binary predicate, under explicit defined-conversion and undefined-nonconversion hypotheses. The variant original\_universal\_identity\_iff\_total\_of\_no\_normal\_form takes explicit negative evidence after raw marker erasure. The raw normal-form obstruction and the marker-erasure consequences are kernel-checked; matching those statements to the external pure calculus remains the written argument of §5. These hypotheses are theorem parameters, not new axioms or typing rules.

The final package build freshly compiled all 71 project modules into fresh project outputs, reusing the pinned dependency checkouts and compiled caches. It retained 22 inherited linter warnings and emitted no warning in the six additions. The complete verification/run\_checks.sh exited 0, covering source and dependency locks, exact interfaces, inherited regressions, compiled proof-dependency checks, and deliberate interface, auditor and source-validator rejection controls. The independent successor replay separately compiled the two new modules from fresh copies while reusing predecessor and dependency objects. Neither replay is claimed as a clean dependency or network bootstrap.

Across both added namespaces, the compiled audit checked 98 safe roots and 2,180 reachable declarations. Their only transitive axioms are propext, Quot.sound and Classical.choice; no custom axiom, sorryAx, unsafe declaration or partial declaration occurs in that logical closure. Compiler runtime auxiliaries were reported separately and were not reachable from the safe roots. Expected rejections check the specified interfaces and auditors; they are not logical-independence proofs.

The package’s DECLARATION\_CLAIM\_MAP.md and AXIOM\_REPORT.md give the detailed bindings and controls. Its final verification/receipt.json has SHA256 24db3eb238d712fa242cb5c71a5c074d70a4a52434d34b41ada2f3d731327082 and records the actual build and complete-check results, exact source hashes and dependency pins.

No whole-classification Lean formalisation is claimed. Representing-program existence, external source-language matching, effective finite-certificate coding and recursive matrices, concrete machines and computable index/target maps, totality’s arithmetical completeness, and the positive/negative certification metatheorems remain written mathematical components. The semantic theorems do not themselves construct the representing program or instantiate their explicit assumptions. Kernel verification of these links and the complete written proof of the classification are distinct claims.

#### References

- \[1\] J. Roger Hindley and Jonathan P. Seldin, *Lambda-Calculus and Combinators: An Introduction*, Cambridge University Press, 2008. Notation 4.1 and Definitions 4.2, 4.5, pp. 47–49; Theorem 4.23, pp. 58–59. [Publisher chapter record](<https://www.cambridge.org/core/books/abs/lambdacalculus-and-combinators/representing-the-computable-functions/CCD505D1E0E0EA4D93412C26CED28B56>); DOI: 10.1017/CBO9780511809835.005.

- For relation matching: *Finite Certificates and Inhabitation Limits for P01AC and HasPlus*, Fourteenth companion, section 8.1.

- Original P01AC declarations AllSyntax, AllPredicates, AllConstants, AllBaseLaws, AllSoundness, P01PER, P01Polynomials and P01Confluence.

- Existing extensional repair declarations ExtensionalRepairSyntax and ExtensionalRepairSoundness.

- Tenth *Minimal Addendum*, section 3, and *Defect Computability*, section 6, for earlier generic computability obstructions.

Paper 2

## Boolean Identity Completeness

### Abstract

For the fixed P01AC polynomial calculus, with its current syntactic typing judgement and original relational interpretations F and G, equality of closed functions from Church naturals to Church Booleans is Π₁-complete when finite endpoint-typing certificates are included in the input. Invalid syntax or invalid supplied certificates are rejected. Its complement is Σ₁-complete. On the correctly typed domain, every semantic inequality has a finite certificate consisting of a canonical natural input and two raw conversion derivations with opposite inert-marker outputs. There is no computable uniform bound on a distinguishing input.

The lower bound is obtained by compiling finite primitive-recursive descriptions directly into the current typing system. The compiler handles every finite arity, checks the term and type context shifts, and is adequate for arbitrary raw Church-numeral observations. An explicit arithmetic encoding of binary machines supplies the one primitive-recursive bounded-halting function needed by the reduction. Finite enumeration of current typing certificates makes the annotated reduction effective without proof extraction.

Erasing the typing certificates changes the effective presentation. For bare endpoint-pair codes, this paper proves a d.c.e. upper bound and a Π₁ lower bound. The separate companion *Bare Boolean Identity and Fixed Type Typability* proves d.c.e.-completeness for exactly that bare domain. The identity conclusions concern the original F/G semantic clauses and existence of a semantic polynomial witness, not syntactic identity completeness.

### 1 The fixed problem

#### 1.1 Raw terms and polynomials

We use the fixed P01AC raw applicative calculus, polynomial syntax, current judgement Has, and original interpretations F and G. No typing rule or semantic clause is changed. A raw term is a finite applicative term. Application associates to the left. Write



$$
s\simeq{}t
$$



for its raw conversion relation, the equivalence congruence generated by the fixed reduction rules. Conversion proofs are finite trees. The raw calculus is confluent. Its two inert constants, written $\mathbf{0}$ and $\mathbf{1}$, are distinct normal forms, so



$$
\mathbf{0}\not\simeq{}\mathbf{1}.
$$



(1)

These constants are observation markers. They are not Church numerals or Church Boolean terms.

A polynomial is a finite tree built from raw-term atoms, de Bruijn variables, and application. Its evaluation in a raw-term environment $\eta{}$ is written $\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,\eta{})$. The fixed bracket-abstraction operation is written $\lambda{}x.p$ when named-variable notation makes the binding clearer. This is an abbreviation for that operation, not an additional term constructor. Its computational law is



$$
\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(\lambda{}x.p,\eta{})\,{}a\simeq{}\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,a::\eta{}).
$$



(2)

Polynomial substitution has the literal evaluation law



$$
\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p[\sigma{}],\eta{})=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,i\mapsto{}\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(\sigma{}(i),\eta{})).
$$



(3)

A polynomial is closed when it has no free term variables. Let ${\eta{}}_{0}$, also called zeroEnv, be the environment constantly equal to the inert marker $\mathbf{0}$. Evaluation of a closed polynomial is independent of the environment; ${\eta{}}_{0}$ fixes one canonical convention.

The judgement



$$
\mathrm{H}\mathrm{a}\mathrm{s}\;{}\Gamma{}\;{}p\;{}A
$$



means derivability in the current P01AC syntactic typing rules, with finite telescope $\Gamma{}$. It does not mean semantic membership. We use its established formation, scope, weakening, mixed-substitution and soundness theorems. In particular, a closed current typing supplies self-relatedness under F at every unary type environment.

Put



$$
N=\forall{}X.(X\to{}X)\to{}X\to{}X,\quad{}\quad{}B=\forall{}X.X\to{}X\to{}X,\quad{}\quad{}{C}_{B}=N\to{}B.
$$



(4)

All three are formed types. The arrow is the current nondependent arrow, and later $\Sigma{}N\,{}N$ denotes the current nondependent product. Type abstraction and type instantiation in displayed programs denote current allIntro and allElim derivation steps; they add no runtime polynomial syntax.

#### 1.2 The relevant original semantic clauses

A partial equivalence relation, or PER, is a symmetric and transitive relation on raw terms, saturated under raw conversion in both coordinates. Its members are its self-related terms. The PER rawPER is raw conversion itself, so every raw term is a member of rawPER.

A Link between PERs $A$ and $A\prime{}$ is a relation with endpoint-membership conditions and respect for the two endpoint equivalences. A unary type environment $\rho{}$ assigns PERs to type parameters. A relational environment $\mathcal{R}$ assigns Links and has unary endpoint environments ${\rho{}}_{L},{\rho{}}_{R}$. The diagonal relational environment of $\rho{}$ uses its PER relations as Links.

We write ${F}_{A}^{\rho{},\eta{}}(s,t)$ for the original unary relation and ${G}_{A}^{\mathcal{R},{\eta{}}_{L},{\eta{}}_{R}}(s,t)$ for the original relational interpretation. Subscripts and environments are suppressed only when fixed. On a nondependent arrow the original unary clause is



$$
{F}_{A\to{}D}(s,t)\Leftrightarrow{}\forall{}x,y\;{}({F}_{A}(x,y)\Rightarrow{}{F}_{D}(sx,ty)).
$$



(5)

The original G-arrow clause retains three requirements: the left endpoint is self-related at the left unary arrow interpretation, the right endpoint is self-related at the right unary arrow interpretation, and G-related arguments have G-related outputs. In particular, the last requirement uses independently supplied related arguments, not merely identical inputs.

For a universal type $\forall{}X.A$, define the membership-uniformity condition



$$
{U}_{A}^{\rho{},\eta{}}(t)\Leftrightarrow{}\forall{}P,Q\;{}\forall{}R:\mathrm{L}\mathrm{i}\mathrm{n}\mathrm{k}(P,Q),\;{}{G}_{A}^{R::\mathrm{d}\mathrm{i}\mathrm{a}\mathrm{g}(\rho{}),\eta{},\eta{}}(t,t).
$$



The original F clause is



$$
{F}_{\forall{}X.A}^{\rho{},\eta{}}(s,t)\Leftrightarrow{}{U}_{A}^{\rho{},\eta{}}(s)\:{}\wedge{}\:{}{U}_{A}^{\rho{},\eta{}}(t)\:{}\wedge{}\:{}\forall{}P\;{}{F}_{A}^{P::\rho{},\eta{}}(s,t).
$$



(6)

The two uniformity conjuncts are essential. An equation between applied observations does not by itself manufacture them. Below they are either obtained from a given semantic self-relation or supplied by current typing soundness. At a formed type, F has the PER laws and conversion saturation.

#### 1.3 Codes and annotations

Fix effective encodings of finite raw terms, polynomials, types, telescopes and derivation trees. Current Has certificates are full finite trees of the actual rules. Their validation is recursive: syntax, lookup, scope, arithmetic side conditions, substitution and syntactic equality are effective. A formation family indexed by a finite list is encoded as a finite table of the stated length. Any finite-derivation premise contains its own finite rule tree, including its raw reduction evidence; polynomial and raw conversion premises likewise have finite derivation trees. No infinitary family is inserted into the coding. The validator covers the whole current judgement rather than only a restricted convenient proof format.

An annotated input is a code



$$
a=\langle{}p,q,{d}_{p},{d}_{q}\rangle{}
$$



where $p,q$ are closed polynomials and ${d}_{p},{d}_{q}$ validate as proofs of



$$
\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}p\;{}{C}_{B},\quad{}\quad{}\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}q\;{}{C}_{B}.
$$



(7)

Let ACert be the decidable set of such valid annotations. For closed endpoints put



$$
P=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,{\eta{}}_{0}),\quad{}Q=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(q,{\eta{}}_{0}),\quad{}{V}_{B}(p,q)\Leftrightarrow{}\forall{}\rho{}\;{}{F}_{{C}_{B}}^{\rho{},{\eta{}}_{0}}(P,Q).
$$



(8)

The certificate-carrying positive set is



$$
{E}_{B}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}=\{\langle{}p,q,{d}_{p},{d}_{q}\rangle{}\in{}\mathrm{A}\mathrm{C}\mathrm{e}\mathrm{r}\mathrm{t}:{V}_{B}(p,q)\}.
$$



(9)

All malformed codes and invalid supplied certificates lie outside this set. This is a set of all finite strings, not a promise problem with an unspecified treatment of invalid inputs.

A set is Π₁ if it has the form $\{a:\forall{}n\,{}R(a,n)\}$ for a total recursive predicate R. It is Σ₁, or recursively enumerable, if membership has finite recursively checkable witnesses. Completeness below is with respect to total computable many-one maps.

**Theorem 1.** The set ${E}_{B}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$ is Π₁-complete. Its complement is Σ₁-complete. On valid annotations, failure of ${V}_{B}$ is equivalent to a finite opposite-marker certificate. The same exact complexity holds for the corresponding original closed F/G identity-validity problems at proof I and for existence of a semantic polynomial identity witness. No computable function, even one required to terminate only on ACert, uniformly bounds a distinguishing canonical input for every unequal annotated pair.

For bare endpoint-pair codes let D be the set of closed pairs admitting the two typings in (7), and set ${E}_{B}=\{(p,q)\in{}D:{V}_{B}(p,q)\}$. We shall prove



$$
{E}_{B}=D\setminus{}M
$$



(10)

for an explicit recursively enumerable mismatch set M. Thus ${E}_{B}$ is d.c.e. (also called 2-c.e.) and lies in Δ₂. The lower-bound family also makes it Π₁-hard. The matching d.c.e.-hardness proof is given in *Bare Boolean Identity and Fixed Type Typability*, using an independent current-typing gate.

### 2 Semantic Boolean standardness

For $b\in{}\{0,1\}$, put



$$
{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{0}(x,y)=x,\quad{}\quad{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{1}(x,y)=y,\quad{}\quad{}\mathrm{o}\mathrm{b}\mathrm{s}(t)=t\,{}\mathbf{0}\,{}\mathbf{1}.
$$



The numbers indexing pick denote the first and second choices only.

**Lemma 2.** For every environment $\rho{},\eta{}$, if ${F}_{B}^{\rho{},\eta{}}(t,t)$, then there is exactly one $b\in{}\{0,1\}$ such that



$$
\forall{}x,y\ \mathrm{r}\mathrm{a}\mathrm{w},\quad{}\quad{}txy\simeq{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(x,y).
$$



(11)

**Proof.** Fix arbitrary raw x and y. Define a Link from rawPER to rawPER by



$$
{R}_{x,y}(a,c)\Leftrightarrow{}\exists{}b\in{}\{0,1\},\quad{}a\simeq{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(\mathbf{0},\mathbf{1})\:{}\wedge{}\:{}c\simeq{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(x,y).
$$



(12)

Its endpoints are members of rawPER by reflexivity. Its respect condition follows by composing the conversions in (12). It contains $(\mathbf{0},x)$ and $(\mathbf{1},y)$.

Apply the membership-uniformity conjunct of ${F}_{B}(t,t)$ to this Link. The two successive G-arrow cross-argument clauses, applied to these two related pairs, yield a bit b with



$$
\mathrm{o}\mathrm{b}\mathrm{s}(t)\simeq{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(\mathbf{0},\mathbf{1}),\quad{}\quad{}txy\simeq{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(x,y).
$$



(13)

First take $x=\mathbf{0},y=\mathbf{1}$ to select one bit ${b}_{0}$. For any other x,y, the first equation in (13) forces $b={b}_{0}$, by (1). This proves existence of a uniform bit. Applying any two proposed instances of (11) to the markers and using (1) proves uniqueness. ∎

This is a graph argument about arbitrary semantic inhabitants. It has no syntactic-definability, current-typing, marker-freeness or strong-normalisation premise for t.

**Lemma 3.** If s and t are self-related at B in the same environment, then



$$
{F}_{B}(s,t)\Leftrightarrow{}\mathrm{o}\mathrm{b}\mathrm{s}(s)\simeq{}\mathrm{o}\mathrm{b}\mathrm{s}(t).
$$



(14)

**Proof.** Forward, instantiate the universal PER component of (6) with rawPER and apply the two F arrows to the self-related markers.

Conversely, Lemma 2 gives bits b and c for s and t. Conversion of the marker observations implies $b=c$. The two uniformity conjuncts required by (6) come from the assumed self-relations of s and t. For its remaining conjunct, take any PER A and independently related inputs $A(x,x\prime{})$, $A(y,y\prime{})$. The common chosen branch gives



$$
A({\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(x,y),{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(x\prime{},y\prime{})).
$$



Conversion saturation and (11) then yield $A(sxy,tx\prime{}y\prime{})$. This is the required pair of cross-argument arrow clauses. ∎

### 3 Natural observations and canonical tests

Write ${f}^{0}x=x$ and ${f}^{n+1}x=f({f}^{n}x)$. Define



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(t,n)\Leftrightarrow{}\forall{}f,x\ \mathrm{r}\mathrm{a}\mathrm{w},\quad{}tfx\simeq{}{f}^{n}x.
$$



(15)

Let $\overline{n}$ be the polynomial obtained by the fixed bracket abstraction of $\lambda{}f.\lambda{}x.{f}^{n}x$, and let



$$
{u}_{n}=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(\overline{n},{\eta{}}_{0}).
$$



The current variable, application, abstraction and universal-introduction rules give



$$
\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}\overline{n}\;{}N,\quad{}\quad{}\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}({u}_{n},n).
$$



(16)

In de Bruijn coordinates the numeral body has context $[x:X,f:X\to{}X]$, starts at var 0, and applies var 1 n times. Two instances of (2) prove its applied equation. Current typing soundness therefore gives ${F}_{N}^{\rho{},{\eta{}}_{0}}({u}_{n},{u}_{n})$ for every $\rho{}$.

For completeness we record the natural standardness facts used here and their graph proof.

**Lemma 4.** Every self-related semantic natural t has a unique index n satisfying NatObs(t,n). If two self-related naturals have the same index, they are F-related in their common environment. F-related naturals have the same index.

**Proof.** The raw terms ${\mathbf{0}}^{n}\mathbf{1}$ are distinct normal forms. Confluence consequently implies



$$
{\mathbf{0}}^{m}\mathbf{1}\simeq{}{\mathbf{0}}^{n}\mathbf{1}\Rightarrow{}m=n.
$$



(17)

For fixed raw f,x define the orbit Link



$$
{R}_{f,x}(a,c)\Leftrightarrow{}\exists{}n,\quad{}a\simeq{}{\mathbf{0}}^{n}\mathbf{1}\:{}\wedge{}\:{}c\simeq{}{f}^{n}x.
$$



As in (12), it is an admissible Link between rawPERs. The pair $(\mathbf{1},x)$ belongs to it. The pair of raw functions $(\mathbf{0},f)$ preserves it, because it takes the orbit witness n to n+1. The two unary endpoint-arrow conditions also hold, by congruence of raw conversion under application by any fixed raw term.

Apply the universal membership-uniformity of t first to this related function pair and then to $(\mathbf{1},x)$. One obtains an n simultaneously satisfying



$$
t\mathbf{0}\mathbf{1}\simeq{}{\mathbf{0}}^{n}\mathbf{1},\quad{}\quad{}tfx\simeq{}{f}^{n}x.
$$



The witness selected at $f=\mathbf{0},x=\mathbf{1}$ agrees with every other witness by (17). This proves standardness and uniqueness.

For the same-index converse, let s and t be self-related with index n. Retain their two membership-uniformity conjuncts in (6). Given a PER A, an A-arrow relation between f and g, and $A(x,y)$, induction gives $A({f}^{n}x,{g}^{n}y)$. Saturation and the two NatObs equations give $A(sfx,tgy)$, which supplies the universal PER component. Finally, if s and t are F-related, instantiate that component at rawPER, use $\mathbf{0}$ as the related function pair and $\mathbf{1}$ as the related argument pair, and apply (17). ∎

**Proposition 5.** On D,



$$
{V}_{B}(p,q)\Leftrightarrow{}\forall{}n\in{}\mathbb{N},\quad{}\mathrm{o}\mathrm{b}\mathrm{s}(P{u}_{n})\simeq{}\mathrm{o}\mathrm{b}\mathrm{s}(Q{u}_{n}).
$$



(18)

**Proof.** Forward, use any unary environment, for example the one constantly rawPER. Apply the relation at $N\to{}B$ to the self-related ${u}_{n}$, then use Lemma 3.

For the converse fix an arbitrary $\rho{}$ and arbitrary x,y with ${F}_{N}^{\rho{},{\eta{}}_{0}}(x,y)$. The PER laws give self-relatedness of x. By Lemma 4 it has an index n and is related to ${u}_{n}$; symmetry and transitivity then give ${F}_{N}({u}_{n},y)$. Current soundness of p and q supplies their arrow self-relations, hence



$$
{F}_{B}(Px,P{u}_{n}),\quad{}\quad{}{F}_{B}(Q{u}_{n},Qy).
$$



Both canonical outputs are self-related. The nth test in (18), followed by Lemma 3, supplies ${F}_{B}(P{u}_{n},Q{u}_{n})$. Transitivity yields ${F}_{B}(Px,Qy)$, exactly the original arrow condition in the arbitrary environment. ∎

Thus canonical testing is complete for all semantic natural inputs and all unary environments. It is not a restriction of arrow equality to identical or syntactically definable arguments.

### 4 Finite negative certificates and the upper bounds

Define M on bare pair codes, rejecting malformed polynomial syntax, by



$$
\begin{gathered}M(p,q)\Leftrightarrow{}\exists{}n,b,c,\;{}b\ne{}c\:{}\wedge{}\:{}\mathrm{o}\mathrm{b}\mathrm{s}(P{u}_{n})\simeq{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(\mathbf{0},\mathbf{1}) \\ \wedge{}\:{}\mathrm{o}\mathrm{b}\mathrm{s}(Q{u}_{n})\simeq{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{c}(\mathbf{0},\mathbf{1}).\end{gathered}
$$



(19)

A finite witness specifies n, the opposite bits b and c, and the two conversion trees with the displayed endpoints. All components have recursive validation, so M is recursively enumerable without any typing premise.

**Proposition 6.** For every $(p,q)\in{}D$,



$$
\neg{}{V}_{B}(p,q)\Leftrightarrow{}M(p,q).
$$



(20)

**Proof.** If validity fails, Proposition 5 gives an input n whose observations are not convertible. Soundness and Lemma 2 give a bit for each of the two outputs. If the bits agreed, the two conversions to their common marker would make the observations convertible. Thus they differ and give (19).

Conversely, validity supplies conversion between the two observations in (19). Composing the witness conversions would convert the two distinct markers, contrary to (1). ∎

Including the two current typing certificates with (19) gives a sound and complete finite verifier of semantic inequality on the closed typed domain. This statement does not certify every untypable pair.

For a valid annotation a and a fixed n, enumerate all finite conversion trees from each observed output to either marker. By Lemma 2, each search terminates at a marker; by (1), its answer is unique. Hence the two bits at n can be computed effectively. The method enumerates conversion derivations. It makes no assertion that an arbitrary reduction strategy terminates.

Define a total recursive predicate R(a,n) as follows. If a fails the decidable ACert check, return false. Otherwise run the two terminating searches and return whether the bits agree. Proposition 5 gives



$$
a\in{}{E}_{B}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}\Leftrightarrow{}\forall{}n\,{}R(a,n).
$$



(21)

This proves the Π₁ upper bound. Equivalently, the complement is enumerated by rejecting invalid annotations and searching for (19) on valid ones. Invalid annotations themselves have finite rejection evidence from the recursive validator.

For bare codes, D is recursively enumerable by enumeration of full current typing certificates. Equation (20) proves (10). Explicitly, an approximation to ${E}_{B}$ starts at zero; it becomes one when typing evidence is found, provided no mismatch has appeared, and becomes zero permanently if a mismatch appears. If a mismatch precedes typing evidence it stays zero. There are at most two changes per code. This is the d.c.e. presentation, and hence a Δ₂ upper bound.

The existential projection that forgets typing certificates need not preserve Π₁. Moreover, the full bare complement contains untypable strings as well as typed inequalities. No complete finite untypability-certificate system is supplied here. The exact bare-code classification is established by the separate gate argument in *Bare Boolean Identity and Fixed Type Typability*; it does not follow from the annotated upper bound or from generic results about a different typing judgement.

### 5 The finite primitive-recursion language

To establish the lower bound we construct a simulator through the current Has rules themselves.

For every finite arity r, let ${\mathrm{P}\mathrm{R}}_{r}$ be the following finite syntax of natural-number functions:

- ${\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{r}$, the r-ary constant zero, including r=0;

- $\mathrm{s}\mathrm{u}\mathrm{c}\mathrm{c}\in{}{\mathrm{P}\mathrm{R}}_{1}$;

- ${\mathrm{p}\mathrm{r}\mathrm{o}\mathrm{j}}_{i}\in{}{\mathrm{P}\mathrm{R}}_{r}$ for $i<r$;

- $\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(f;{g}_{0},\ldots{},{g}_{k-1})\in{}{\mathrm{P}\mathrm{R}}_{r}$, where $f\in{}{\mathrm{P}\mathrm{R}}_{k}$ and each ${g}_{i}\in{}{\mathrm{P}\mathrm{R}}_{r}$;

- $\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}(g,h)\in{}{\mathrm{P}\mathrm{R}}_{r+1}$, where $g\in{}{\mathrm{P}\mathrm{R}}_{r}$ and $h\in{}{\mathrm{P}\mathrm{R}}_{r+2}$.

Denote the numerical interpretation by $[\![f]\!]$. Coordinates start at zero. For primitive recursion the order is exactly



$$
\begin{array}{rl}[\![\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}(g,h)]\!](n,\vec{x}) & =v(n), \\ v(0) & =[\![g]\!](\vec{x}), \\ v(k+1) & =[\![h]\!](k,v(k),\vec{x}).\end{array}
$$



(22)

Thus h receives counter, current value, then original parameters. The recursion argument of the resulting function is first. A convention that puts it elsewhere is translated by projections and composition.

The k children of a composition are a finite k-entry table. An implementation may express this table as a function on the finite set $\mathrm{F}\mathrm{i}\mathrm{n}(k)$; the external description still consists of k finite subtrees. The k=0 case has no argument subtrees or argument premises. Parsing, table access and recursive traversal are effective.

### 6 Direct compilation and current typing

Let



$$
{\Gamma{}}_{r}=[N,\ldots{},N]\quad{}\mathrm{w}\mathrm{i}\mathrm{t}\mathrm{h}\ \mathrm{r}\ \mathrm{e}\mathrm{n}\mathrm{t}\mathrm{r}\mathrm{i}\mathrm{e}\mathrm{s}.
$$



We construct a polynomial $\mathcal{C}(f)$ for each $f\in{}{\mathrm{P}\mathrm{R}}_{r}$.

**Theorem 7.** For every finite r and $f\in{}{\mathrm{P}\mathrm{R}}_{r}$,



$$
\mathrm{H}\mathrm{a}\mathrm{s}\;{}{\Gamma{}}_{r}\;{}\mathcal{C}(f)\;{}N.
$$



(23)

Consequently $\mathcal{C}(f)$ is scoped to those r variables, and abstracting those variables yields a closed current-typed function. The compiler is an effective transformation of finite descriptions into the original polynomial syntax.

#### 6.1 Base operations and context shifts

Set $\mathcal{C}({\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{r})=\overline{0}$ and $\mathcal{C}({\mathrm{p}\mathrm{r}\mathrm{o}\mathrm{j}}_{i})=\mathrm{v}\mathrm{a}\mathrm{r}i$. The closed numeral can be weakened into any formed telescope. Every actual lookup in ${\Gamma{}}_{r}$ has type N and index less than r. This includes the weakening present in de Bruijn lookup: N is independent of term variables, so weakening and term substitution leave it unchanged.

Let Succ be the literal threefold bracket abstraction of the body



$$
f(n[X]fx),
$$



with displayed order $\lambda{}n.\Lambda{}X.\lambda{}f:X\to{}X.\lambda{}x:X$. Its innermost context is



$$
[x:X,f:X\to{}X,n:N],
$$



and its body is precisely



$$
\mathrm{a}\mathrm{p}\mathrm{p}(\mathrm{v}\mathrm{a}\mathrm{r}1,\mathrm{a}\mathrm{p}\mathrm{p}(\mathrm{a}\mathrm{p}\mathrm{p}(\mathrm{v}\mathrm{a}\mathrm{r}2,\mathrm{v}\mathrm{a}\mathrm{r}1),\mathrm{v}\mathrm{a}\mathrm{r}0)).
$$



Instantiate n at X using the current allElim rule; the two applications produce a term of X, and applying f preserves that type. The two inner current arrow introductions produce the Church numeral body in context \[N\]. Universal introduction then gives N in that context. This type-coordinate shift is legitimate because N is closed in type parameters: the current type weakening fixes \[N\]. The final arrow introduction gives



$$
\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}\;{}(N\to{}N).
$$



Every abstraction’s scope premise follows from the actual scope theorem for its already typed body and the bracket-abstraction scope rule. Define



$$
\mathcal{C}(\mathrm{s}\mathrm{u}\mathrm{c}\mathrm{c})=\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}\,{}(\mathrm{v}\mathrm{a}\mathrm{r}0).
$$



It has type N in ${\Gamma{}}_{1}$ by weakening the closed Succ and applying the current arrow elimination.

#### 6.2 Composition by the current substitution theorem

For $f\in{}{\mathrm{P}\mathrm{R}}_{k}$ and ${g}_{i}\in{}{\mathrm{P}\mathrm{R}}_{r}$, set



$$
\mathcal{C}(\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(f;\vec{g}))=\mathcal{C}(f)[\sigma{}],\quad{}\quad{}\sigma{}(i)=\{\begin{array}{ll}\mathcal{C}({g}_{i}) & i<k, \\ \mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(\mathbf{0}) & i\ge{}k.\end{array}
$$



(24)

Use the existing current mixed-substitution theorem with identity type substitution. Each source lookup in ${\Gamma{}}_{k}$ has index below k and type N, so the corresponding induction hypothesis supplies its required image typing in ${\Gamma{}}_{r}$. The unused padding is never a typing premise. Because N is invariant under term substitution, the resulting type is again N.

This mixed-substitution theorem is a structural theorem about finite current derivations, including their term- and type-binder lifts. It introduces neither a new rule nor a semantic-completeness principle. In particular, k=0 uses an empty source telescope and requires no typed padding atom.

#### 6.3 Primitive recursion with the exact parameter map

Put $S=\Sigma{}N\,{}N$. The second component N is term-independent, so this is a nondependent product. Write pair, fst and snd for the literal current polynomial pair and projections. Their evaluations satisfy



$$
\mathrm{f}\mathrm{s}\mathrm{t}(\mathrm{p}\mathrm{a}\mathrm{i}\mathrm{r}(a,b))\simeq{}a,\quad{}\quad{}\mathrm{s}\mathrm{n}\mathrm{d}(\mathrm{p}\mathrm{a}\mathrm{i}\mathrm{r}(a,b))\simeq{}b.
$$



(25)

For $g\in{}{\mathrm{P}\mathrm{R}}_{r}$, $h\in{}{\mathrm{P}\mathrm{R}}_{r+2}$, the recursion polynomial in context $[n:N,{x}_{0}:N,\ldots{},{x}_{r-1}:N]$ is



$$
\mathrm{s}\mathrm{n}\mathrm{d}(n[S]\;{}\mathrm{s}\mathrm{t}\mathrm{e}\mathrm{p}\;{}\mathrm{p}\mathrm{a}\mathrm{i}\mathrm{r}(\overline{0},\mathcal{C}(g)(\vec{x}))),
$$



(26)

where



$$
\mathrm{s}\mathrm{t}\mathrm{e}\mathrm{p}(z)=\mathrm{p}\mathrm{a}\mathrm{i}\mathrm{r}(\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}(\mathrm{f}\mathrm{s}\mathrm{t}z),\mathcal{C}(h)(\mathrm{f}\mathrm{s}\mathrm{t}z,\mathrm{s}\mathrm{n}\mathrm{d}z,\vec{x})).
$$



(27)

Equations (26)–(27) specify original polynomial operations. More explicitly, the target telescope for the step body is



$$
\Delta{}=[z:S,n:N,{x}_{0}:N,\ldots{},{x}_{r-1}:N].
$$



The source telescope for $\mathcal{C}(h)$ has coordinates $[k:N,a:N,{x}_{0}:N,\ldots{}]$. The literal polynomial substitution is



$$
0\mapsto{}\mathrm{f}\mathrm{s}\mathrm{t}(\mathrm{v}\mathrm{a}\mathrm{r}0),\quad{}\quad{}1\mapsto{}\mathrm{s}\mathrm{n}\mathrm{d}(\mathrm{v}\mathrm{a}\mathrm{r}0),\quad{}\quad{}j+2\mapsto{}\mathrm{v}\mathrm{a}\mathrm{r}(j+2).
$$



(28)

The original recursion argument n, now at target index one, is therefore not confused with the accumulator a. The first two images have type N by current Sigma elimination. Every remaining source index is an original parameter, with the same target index after insertion of z; its lookup is obtained by the current weakening rule and the source index bound. The current mixed-substitution theorem makes the substituted h body type N in $\Delta{}$. Closed Succ is available there, and current Sigma introduction gives the whole body type S. Current arrow introduction gives step type $S\to{}S$.

The base program $\mathcal{C}(g)$ is weakened once under n, by mapping its variables i to i+1. Together with $\overline{0}$, it forms the S-valued initial pair. Current allElim instantiates n at S; two current arrow eliminations apply its iterator to step and the initial pair. The final Sigma projection has type N. All required formation judgements follow from formation of N and the current Sigma and arrow formation rules. Term-independence of N also verifies the substitutions required by the dependent Sigma rule forms.

This proves the recursion case of (23). Induction on the finite PR description proves Theorem 7. The construction has not used an arbitrary raw atom at N, an inverse translation from another typing calculus, or semantic membership as a substitute for Has. ∎

### 7 Adequacy for arbitrary raw numeral observations

**Theorem 8.** Let $f\in{}{\mathrm{P}\mathrm{R}}_{r}$. If the first r entries of a raw environment $\eta{}$ satisfy



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(\eta{}(i),{v}_{i})\quad{}(i<r),
$$



then



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(\mathcal{C}(f),\eta{}),[\![f]\!]({v}_{0},\ldots{},{v}_{r-1})).
$$



(29)

The hypothesis concerns arbitrary raw terms with the displayed observational equations. It assumes no current typing, semantic membership, marker-freeness or canonical syntactic representation of the inputs. Environment entries beyond r are irrelevant.

**Proof.** NatObs is preserved backwards along conversion, by raw congruence. The zero and projection cases follow from (16) and the environment hypothesis. Three instances of (2) give the successor equation



$$
\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}\,{}t\,{}f\,{}x\simeq{}f(tfx).
$$



Thus NatObs(t,m) implies NatObs(Succ t,m+1). For composition, apply (3), the induction hypotheses for all k argument descriptions, and then the induction hypothesis for f. This also treats the empty argument table.

For recursion, let ${\eta{}}_{p}(i)=\eta{}(i+1)$, let ${v}_{p}(i)={v}_{i+1}$, and define the numerical recurrence v(k) by (22) with parameters ${\vec{v}}_{p}$. Let d be the raw evaluation of the step in (27) in the environment $\eta{}$, and put



$$
{z}_{0}=\mathrm{p}\mathrm{a}\mathrm{i}\mathrm{r}\mathrm{T}\mathrm{e}\mathrm{r}\mathrm{m}({u}_{0},\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(\mathcal{C}(g),{\eta{}}_{p})).
$$



Applied abstraction and the exact substitution (28) give, for every raw z,



$$
\begin{gathered}dz\simeq{}\mathrm{p}\mathrm{a}\mathrm{i}\mathrm{r}\mathrm{T}\mathrm{e}\mathrm{r}\mathrm{m}(\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}(\mathrm{f}\mathrm{i}\mathrm{r}\mathrm{s}\mathrm{t}\mathrm{T}\mathrm{e}\mathrm{r}\mathrm{m}z), \\ \mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(\mathcal{C}(h),\mathrm{f}\mathrm{i}\mathrm{r}\mathrm{s}\mathrm{t}\mathrm{T}\mathrm{e}\mathrm{r}\mathrm{m}z::\mathrm{s}\mathrm{e}\mathrm{c}\mathrm{o}\mathrm{n}\mathrm{d}\mathrm{T}\mathrm{e}\mathrm{r}\mathrm{m}z::{\eta{}}_{p})).\end{gathered}
$$



(30)

We prove by induction on k the two-component invariant



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(\mathrm{f}\mathrm{i}\mathrm{r}\mathrm{s}\mathrm{t}\mathrm{T}\mathrm{e}\mathrm{r}\mathrm{m}({d}^{k}{z}_{0}),k),\quad{}\quad{}\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(\mathrm{s}\mathrm{e}\mathrm{c}\mathrm{o}\mathrm{n}\mathrm{d}\mathrm{T}\mathrm{e}\mathrm{r}\mathrm{m}({d}^{k}{z}_{0}),v(k)).
$$



(31)

At k=0, the pair projection equations (25), canonical zero, and the adequacy hypothesis for g give both components. For the successor case apply (30) to $z={d}^{k}{z}_{0}$, then apply the two projections. The first component has index k+1 by successor adequacy. For the second component, h receives at coordinate zero a natural of index k, at coordinate one a natural of index v(k), and then the original parameter observations. Its induction hypothesis gives index $[\![h]\!](k,v(k),{\vec{v}}_{p})=v(k+1)$. This proves (31).

Finally NatObs($\eta{}(0),{v}_{0}$) can be instantiated at the arbitrary raw d and ${z}_{0}$. It gives



$$
\eta{}(0)\,{}d\,{}{z}_{0}\simeq{}{d}^{{v}_{0}}{z}_{0}.
$$



Congruence under the second projection and (31) yield exactly the NatObs equation for (26). ∎

The computational states in this argument are literal pair terms, so no product representation theorem or product eta principle is required. The independent current typing proof supplies their semantic well-typedness by soundness. No equation between unapplied compiled functions has been inferred from their applied behaviour.

### 8 A typed Boolean discriminator and the fixed family

Let ${\mathsf{c}}_{0}$ and ${\mathsf{c}}_{1}$ be the literal bracket abstractions



$$
{\mathsf{c}}_{0}=\lambda{}x.\lambda{}y.x,\quad{}\quad{}{\mathsf{c}}_{1}=\lambda{}x.\lambda{}y.y.
$$



The current variable and arrow-introduction rules, followed by universal introduction, give both closed typings at B. Two applications of (2) give



$$
{\mathsf{c}}_{b}xy\simeq{}{\mathrm{p}\mathrm{i}\mathrm{c}\mathrm{k}}_{b}(x,y).
$$



(32)

Define the closed zero/nonzero discriminator Z by



$$
Z=\lambda{}n:N.\:{}n[B]\;{}(K{\mathsf{c}}_{1})\;{}{\mathsf{c}}_{0}.
$$



(33)

The original K combinator makes $K{\mathsf{c}}_{1}$ a constant step at type $B\to{}B$. Instantiate n at B and apply it to that step and ${\mathsf{c}}_{0}$. The current rules give



$$
\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}Z\;{}(N\to{}B).
$$



For every arbitrary raw t with NatObs(t,m),



$$
Ztxy\simeq{}\{\begin{array}{ll}x & m=0, \\ y & m>0.\end{array}
$$



(34)

Indeed, its natural observation reduces the iteration in (33) to m applications of $K{\mathsf{c}}_{1}$ starting from ${\mathsf{c}}_{0}$. At zero this is the initial choice; at any positive m the outermost K application returns ${\mathsf{c}}_{1}$. Equation (32) finishes the proof.

For any fixed $f\in{}{\mathrm{P}\mathrm{R}}_{2}$, with coordinate order (bound n, program e), define



$$
{\mathrm{s}\mathrm{i}\mathrm{m}}_{f}=\lambda{}e:N.\lambda{}n:N.\:{}Z(\mathcal{C}(f)),\quad{}\quad{}{p}_{e}={\mathrm{s}\mathrm{i}\mathrm{m}}_{f}\;{}\overline{e},\quad{}\quad{}q=\lambda{}n:N.{\mathsf{c}}_{0}.
$$



(35)

The context of the simulator body is exactly \[n:N,e:N\], so it agrees with the compiler’s two coordinates. Theorem 7, current application, and the two abstractions give



$$
\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}{\mathrm{s}\mathrm{i}\mathrm{m}}_{f}\;{}(N\to{}N\to{}B),\quad{}\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}{p}_{e}\;{}{C}_{B},\quad{}\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}q\;{}{C}_{B}.
$$



(36)

The typing scope theorem makes these endpoints closed. The polynomial q is fixed independently of e.

Let ${P}_{e}=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}({p}_{e},{\eta{}}_{0})$ and $Q=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(q,{\eta{}}_{0})$. Applied abstraction, Theorem 8 and (34) imply



$$
\mathrm{o}\mathrm{b}\mathrm{s}({P}_{e}{u}_{n})\simeq{}\{\begin{array}{ll}\mathbf{0} & [\![f]\!](n,e)=0, \\ \mathbf{1} & [\![f]\!](n,e)>0,\end{array}\quad{}\quad{}\mathrm{o}\mathrm{b}\mathrm{s}(Q{u}_{n})\simeq{}\mathbf{0}.
$$



(37)

By Proposition 5 and marker separation,



$$
{V}_{B}({p}_{e},q)\Leftrightarrow{}\forall{}n\;{}[\![f]\!](n,e)=0.
$$



(38)

This equivalence has an actual finite PR description as its parameter. Its premise is not an assumed current-Has representer. We now construct the single description needed for the lower bound.

### 9 Arithmetic in the exact primitive-recursion basis

Write ${P}_{i}^{r}$ for projection i of arity r and ${C}_{r}(c)$ for an r-ary constant. Constants are obtained from ${\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{r}$ and repeated composition with successor. Composition permits any fixed argument reordering, duplication, omission, or insertion of a constant. Therefore every finite expression in functions already constructed below is translated to a literal finite composition tree with its stated arity.

#### 9.1 Elementary arithmetic and bounded sums

The following descriptions have the argument convention (22):



$$
\begin{array}{rl}\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{d} & =\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{0},{P}_{0}^{2}), \\ \mathrm{a}\mathrm{d}\mathrm{d} & =\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({P}_{0}^{1},\mathrm{s}\mathrm{u}\mathrm{c}\mathrm{c}\circ{}{P}_{1}^{3}), \\ \mathrm{m}\mathrm{u}\mathrm{l} & =\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{1},\mathrm{a}\mathrm{d}\mathrm{d}({P}_{2}^{3},{P}_{1}^{3})), \\ \mathrm{p}\mathrm{o}\mathrm{w} & =\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({C}_{1}(1),\mathrm{m}\mathrm{u}\mathrm{l}({P}_{2}^{3},{P}_{1}^{3})).\end{array}
$$



(39)

They compute predecessor with pred(0)=0, addition, multiplication, and $\mathrm{p}\mathrm{o}\mathrm{w}(n,a)={a}^{n}$, respectively. For instance the multiplication step receives (k,current value,a) and adds a to the current value.

Define



$$
T=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({P}_{0}^{1},\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{d}\circ{}{P}_{1}^{3}),\quad{}\quad{}a\dot{-}b=T(b,a).
$$



This is truncated subtraction. The zero indicator is



$$
{\delta{}}_{0}=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({C}_{0}(1),{\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{2}),
$$



so ${\delta{}}_{0}(0)=1$ and ${\delta{}}_{0}(n+1)=0$. Consequently



$$
\begin{array}{rl}\mathrm{l}\mathrm{e}(a,b) & ={\delta{}}_{0}(a\dot{-}b), \\ \mathrm{e}\mathrm{q}(a,b) & =\mathrm{l}\mathrm{e}(a,b)\mathrm{l}\mathrm{e}(b,a), \\ \mathrm{s}\mathrm{i}\mathrm{g}\mathrm{n}(a) & =1\dot{-}{\delta{}}_{0}(a), \\ \mathrm{i}\mathrm{f}(c,u,v) & =\mathrm{s}\mathrm{i}\mathrm{g}\mathrm{n}(c)u+{\delta{}}_{0}(c)v.\end{array}
$$



(40)

The last function returns u when c is positive and v otherwise. All branches are total, so evaluating the unselected arithmetic expression causes no partiality.

For an $(r+1)$-ary PR function $R(j,\vec{x})$, construct



$$
\begin{array}{rl}{\mathrm{S}\mathrm{u}\mathrm{m}}_{R}(0,\vec{x}) & =0, \\ {\mathrm{S}\mathrm{u}\mathrm{m}}_{R}(k+1,\vec{x}) & ={\mathrm{S}\mathrm{u}\mathrm{m}}_{R}(k,\vec{x})+R(k+1,\vec{x}).\end{array}
$$



(41)

This is one prec node with base ${\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{r}$ and step of arity r+2,



$$
H(k,a,\vec{x})=\mathrm{a}\mathrm{d}\mathrm{d}(a,R(k+1,\vec{x})).
$$



Its literal coordinate map uses counter 0, accumulator 1 and parameters beginning at 2. It computes the sum over j=1 through k. The upper bound may also be supplied as a parameter by composition.

#### 9.2 Division and the exponent of two

For d\>0 put



$$
\mathrm{d}\mathrm{i}\mathrm{v}(x,d)=\sum\limits_{j=1}^{x} [dj\le{}x],\quad{}\quad{}\mathrm{d}\mathrm{i}\mathrm{v}(x,0)=0,
$$



(42)

where brackets denote the indicator from (40). The arity-three summand is $R(j,x,d)=\mathrm{l}\mathrm{e}(dj,x)$. Its bounded sum has coordinates (bound,x,d); substituting (x,x,d) gives the arity-two formula. When d\>0 the successful positive j are exactly $1,\ldots{},\lfloor{}x/d\rfloor{}$, all within the bound x. Thus (42) is ordinary integer division for positive d, expressed in the exact PR basis. Define



$$
\mathrm{r}\mathrm{e}\mathrm{m}(x,d)=x\dot{-}d\mathrm{d}\mathrm{i}\mathrm{v}(x,d).
$$



(43)

For m\>0 define



$$
{\nu{}}_{2}(m)=\sum\limits_{j=1}^{m} [\mathrm{r}\mathrm{e}\mathrm{m}(m,{2}^{j})=0],\quad{}\quad{}{\nu{}}_{2}(0)=0.
$$



(44)

The arity-two summand uses $\mathrm{p}\mathrm{o}\mathrm{w}(j,2)$, and the upper bound and parameter are both supplied by m. For positive m, the dividing powers are precisely ${2}^{1},\ldots{},{2}^{{\nu{}}_{2}(m)}$. Every such exponent lies within the bound m, because ${2}^{j}\le{}m$ and $j\le{}{2}^{j}$. Equation (44) therefore computes the exponent of two in m. Neither division nor this valuation is an oracle or an additional PR constructor.

#### 9.3 Pairing and finite lists

Use the numerical pairing function



$$
\langle{}a,b\rangle{}={2}^{a}(2b+1)\dot{-}1.
$$



(45)

The product is positive, so the subtraction is exact. Its inverse coordinates are



$$
\begin{array}{rl}\mathrm{l}\mathrm{e}\mathrm{f}\mathrm{t}(t) & ={\nu{}}_{2}(t+1), \\ \mathrm{r}\mathrm{i}\mathrm{g}\mathrm{h}\mathrm{t}(t) & =\mathrm{d}\mathrm{i}\mathrm{v}(\mathrm{d}\mathrm{i}\mathrm{v}(t+1,{2}^{\mathrm{l}\mathrm{e}\mathrm{f}\mathrm{t}(t)})\dot{-}1,2).\end{array}
$$



(46)

The unique decomposition of a positive integer as a power of two times an odd positive integer proves both projection identities and reconstruction. All functions in (45)–(46) are PR by the preceding constructions.

Encode a list by



$$
\mathrm{n}\mathrm{i}\mathrm{l}=0,\quad{}\quad{}\mathrm{c}\mathrm{o}\mathrm{n}\mathrm{s}(a,l)=1+\langle{}a,l\rangle{}={2}^{a}(2l+1).
$$



For c\>0 define



$$
\mathrm{h}\mathrm{e}\mathrm{a}\mathrm{d}(c)={\nu{}}_{2}(c),\quad{}\quad{}\mathrm{t}\mathrm{a}\mathrm{i}\mathrm{l}(c)=\mathrm{d}\mathrm{i}\mathrm{v}(\mathrm{d}\mathrm{i}\mathrm{v}(c,{2}^{\mathrm{h}\mathrm{e}\mathrm{a}\mathrm{d}(c)})\dot{-}1,2),
$$



and set both functions to zero at c=0. For a positive c written as ${2}^{a}(2l+1)$, these formulas return a and l, and $l<c$. Iterating tail therefore reaches zero, so every natural code denotes a finite list.

The bounded iteration



$$
\mathrm{d}\mathrm{r}\mathrm{o}\mathrm{p}(0,c)=c,\quad{}\quad{}\mathrm{d}\mathrm{r}\mathrm{o}\mathrm{p}(i+1,c)=\mathrm{t}\mathrm{a}\mathrm{i}\mathrm{l}(\mathrm{d}\mathrm{r}\mathrm{o}\mathrm{p}(i,c))
$$



is a PR₂ description with base ${P}_{0}^{1}$ and step $\mathrm{t}\mathrm{a}\mathrm{i}\mathrm{l}\circ{}{P}_{1}^{3}$. Hence



$$
\mathrm{n}\mathrm{t}\mathrm{h}(c,i)=\mathrm{h}\mathrm{e}\mathrm{a}\mathrm{d}(\mathrm{d}\mathrm{r}\mathrm{o}\mathrm{p}(i,c))
$$



(47)

is PR₂ and returns zero beyond the end of the decoded finite list. Termination of list decoding is used to interpret the table as finite; PR membership of drop already follows from its explicitly bounded recursion.

### 10 A concrete binary-machine characteristic

#### 10.1 Programs and tape representations

Consider deterministic machines with one two-sided binary tape, blank symbol 0, start state 1 and halt state 0. A program e is a finite transition list encoded as above. At a positive state q reading $s\in{}\{0,1\}$, fetch the instruction



$$
i=\mathrm{n}\mathrm{t}\mathrm{h}(e,2(q\dot{-}1)+s).
$$



(48)

Instruction zero means halt. For i\>0 decode



$$
\begin{array}{rl}q\prime{} & =\mathrm{l}\mathrm{e}\mathrm{f}\mathrm{t}(i-1), \\ a & =\mathrm{r}\mathrm{e}\mathrm{m}(\mathrm{l}\mathrm{e}\mathrm{f}\mathrm{t}(\mathrm{r}\mathrm{i}\mathrm{g}\mathrm{h}\mathrm{t}(i-1)),2), \\ d & =\mathrm{r}\mathrm{e}\mathrm{m}(\mathrm{r}\mathrm{i}\mathrm{g}\mathrm{h}\mathrm{t}(\mathrm{r}\mathrm{i}\mathrm{g}\mathrm{h}\mathrm{t}(i-1)),2).\end{array}
$$



(49)

The machine writes a, moves right if d=1 and left if d=0, and enters q’. Any desired transition to q’ with bits a,d is encoded by



$$
1+\langle{}q\prime{},\langle{}a,d\rangle{}\rangle{}.
$$



Thus every finite binary transition table has an effective code, with omitted slots filled by zero. Conversely every natural e denotes a finite table with total decoding; arbitrary positive instructions still give bit-valued a,d by the remainders in (49).

Represent the tape by two binary stacks L,R. The low bit of R is the current cell, and its higher bits are successive cells to the right. The low bit of L is the nearest cell to the left. All cells beyond the finite binary encodings are zero. Put



$$
\mathrm{b}\mathrm{i}\mathrm{t}(x)=\mathrm{r}\mathrm{e}\mathrm{m}(x,2),\quad{}{\mathrm{t}\mathrm{a}\mathrm{i}\mathrm{l}}_{2}(x)=\mathrm{d}\mathrm{i}\mathrm{v}(x,2),\quad{}\mathrm{p}\mathrm{u}\mathrm{s}\mathrm{h}(a,x)=2x+a.
$$



A configuration is the number $\langle{}q,\langle{}L,R\rangle{}\rangle{}$. Numerical pairing here is distinct from the raw pair terms used by the PR compiler.

#### 10.2 The primitive-recursive step

Define Step(e,c) by decoding q,L,R from c. If q=0, return c. Otherwise fetch i by (48). If i=0, return $\langle{}0,\langle{}L,R\rangle{}\rangle{}$. For i\>0 decode (49) and let $T={\mathrm{t}\mathrm{a}\mathrm{i}\mathrm{l}}_{2}(R)$. The two movement cases are



$$
\begin{array}{lll}\mathrm{r}\mathrm{i}\mathrm{g}\mathrm{h}\mathrm{t}: & L\prime{}=\mathrm{p}\mathrm{u}\mathrm{s}\mathrm{h}(a,L), & R\prime{}=T, \\ \mathrm{l}\mathrm{e}\mathrm{f}\mathrm{t}: & L\prime{}={\mathrm{t}\mathrm{a}\mathrm{i}\mathrm{l}}_{2}(L), & R\prime{}=\mathrm{p}\mathrm{u}\mathrm{s}\mathrm{h}(\mathrm{b}\mathrm{i}\mathrm{t}(L),\mathrm{p}\mathrm{u}\mathrm{s}\mathrm{h}(a,T)).\end{array}
$$



(50)

Return $\langle{}q\prime{},\langle{}L\prime{},R\prime{}\rangle{}\rangle{}$.

The right case makes the newly written a the nearest cell to the left and exposes the old right tail. In the left case,



$$
R\prime{}=\mathrm{b}\mathrm{i}\mathrm{t}(L)+2a+4T,
$$



so the old nearest-left cell becomes current, followed to its right by the newly written a and then the old right tail. These are precisely the intended tape updates. Removing any unrecorded all-zero suffix loses no information about the infinite blank tape.

Every component decoder, address calculation, test, instruction field and tape update is a composition of the functions constructed in Section 9. The nested choices are the total arithmetic conditional in (40). Hence Step is one fixed PR₂ description with coordinates (e,c). Its first branch makes halting configurations absorbing.

The blank initial configuration is



$$
{c}_{0}=\langle{}1,\langle{}0,0\rangle{}\rangle{}=1.
$$



Define



$$
\mathrm{R}\mathrm{u}\mathrm{n}(0,e)=1,\quad{}\quad{}\mathrm{R}\mathrm{u}\mathrm{n}(n+1,e)=\mathrm{S}\mathrm{t}\mathrm{e}\mathrm{p}(e,\mathrm{R}\mathrm{u}\mathrm{n}(n,e)).
$$



(51)

This is exactly one prec node with base ${C}_{1}(1)$ and step



$$
H(k,c,e)=\mathrm{S}\mathrm{t}\mathrm{e}\mathrm{p}({P}_{2}^{3},{P}_{1}^{3}).
$$



It gives Run in PR₂ with coordinates (n,e). Finally put



$$
\chi{}(n,e)={\delta{}}_{0}(\mathrm{l}\mathrm{e}\mathrm{f}\mathrm{t}(\mathrm{R}\mathrm{u}\mathrm{n}(n,e))).
$$



(52)

Induction on n and the verified step equations show that Run encodes the machine after n steps. Since state zero is absorbing,



$$
\chi{}(n,e)\in{}\{0,1\},\quad{}\quad{}\chi{}(n,e)=1\Leftrightarrow{}e\ \mathrm{h}\mathrm{a}\mathrm{s}\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{e}\mathrm{d}\ \mathrm{b}\mathrm{y}\ \mathrm{s}\mathrm{t}\mathrm{e}\mathrm{p}\ n.
$$



(53)

Equations (39)–(52), read in dependency order, are a finite algorithm producing one description ${f}_{\chi{}}\in{}{\mathrm{P}\mathrm{R}}_{2}$. All bounded sums, conditionals and coordinate substitutions have been reduced to the five constructors of Section 5. No minimisation, partial-function representation or unspecified universal interpreter is used. Printing the fully expanded composition tree is unnecessary to its finite effective construction.

#### 10.3 Completeness of this machine indexing

This particular blank-input nonhalting set is Π₁-complete. Here is the effective source argument.

A deterministic machine over any finite alphabet can be translated into the binary-tape model just defined. Choose a fixed block width large enough for the symbols and assign the blank symbol the all-zero block. Finitely many additional states record the original state, the phase in a block, and the finite block information already read. A finite routine reads a complete block, determines the source transition, rewrites the replacement block, and moves to the start of the adjacent block. The controller keeps the block phase, so alignment is preserved from the designated initial origin. Invalid block patterns may have fixed default transitions; they are not reached from correctly encoded data. A source stationary move can be replaced by a right/left pair through an intermediate state that preserves the temporarily visited cell. Rename start and halt to 1 and 0 and encode the resulting finite table by (48)–(49). Every step of this compilation is effective.

Now let A be any Π₁ set, with



$$
k\in{}A\Leftrightarrow{}\forall{}n\,{}R(k,n)
$$



for a total recursive predicate R. Construct a machine that, from blank input, tests $R(k,0),R(k,1),\ldots{}$ and halts at the first false result. Each individual test terminates. The finite parameter k can be written by a finite initialisation routine generated effectively from k. Translate this finite-alphabet machine to binary by the preceding construction. Its resulting code e(k) is computable and satisfies



$$
k\in{}A\Leftrightarrow{}e(k)\ \mathrm{n}\mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s}.
$$



(54)

Conversely, (53) expresses nonhalting as $\forall{}n\,{}\chi{}(n,e)=0$, with a total recursive matrix. This proves Π₁-completeness of exactly the machine source used here.

### 11 The effective annotated reduction

Fix the one description ${f}_{\chi{}}$, its simulator (35), and the constant endpoint q. For each e, compute the finite polynomial



$$
{p}_{e}={\mathrm{s}\mathrm{i}\mathrm{m}}_{{f}_{\chi{}}}\;{}\overline{e}.
$$



Only the canonical numeral and a fixed application template vary. Theorems 7 and 8 and the current rules give the two endpoint typings for every e. Equations (38) and (53) give



$$
e\ \mathrm{n}\mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s}\Leftrightarrow{}\forall{}n\,{}\chi{}(n,e)=0\Leftrightarrow{}{V}_{B}({p}_{e},q).
$$



(55)

To produce an annotated output effectively, use the following extraction-independent algorithm. Compute ${p}_{e}$ and q. Enumerate all finite strings coding current Has derivations, and recursively validate them against the respective targets



$$
\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}{p}_{e}\;{}{C}_{B},\quad{}\quad{}\mathrm{H}\mathrm{a}\mathrm{s}\;{}[]\;{}q\;{}{C}_{B}.
$$



Dovetail the two searches, or enumerate candidate pairs of certificates. Their existence has been proved for every e, so the search terminates for every e. Output the computed polynomials with the first two valid certificates. This is a total computable map into ACert. It does not require extracting program data from classical semantic proofs or from arbitrary proof-assistant propositions. Equivalently, one may implement the finite syntactic proof transformations in the compiler, but the enumeration argument already establishes effectiveness.

Combining this map with (54) proves Π₁-hardness of ${E}_{B}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$. Equation (21) proves its Π₁ upper bound. The same map reduces halting to its complement, which is recursively enumerable by Section 4, so that complement is Σ₁-complete. Erasing the output certificates gives the stated Π₁ lower bound for ${E}_{B}$, alongside the d.c.e./Δ₂ upper bound proved here. The independent gate in *Bare Boolean Identity and Fixed Type Typability* supplies the matching d.c.e. lower bound.

There can be no sound and complete recursively enumerable positive-certificate system for ${E}_{B}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$. Such a system would make the positive set recursively enumerable as well as co-recursively enumerable, and therefore decidable, contradicting (55). The reduction lands wholly inside ACert, so the impossibility remains if positive certificates are requested only for valid annotated inputs.

The lower bound requires only the primitive-recursive bounded-halting characteristic. It does not claim that all total computable functions have current-Has representations or that an unbounded partial computation can be placed at B.

### 12 Transfer to the original identity clauses

Let ${\mathrm{I}\mathrm{d}}_{{C}_{B}}(p,q)$ be the current identity type. Formation of ${C}_{B}$ and the two endpoint typings in (7) give its current formation.

The original F identity clause has the form



$$
\begin{gathered}{F}_{{\mathrm{I}\mathrm{d}}_{{C}_{B}}(p,q)}^{\rho{},\eta{}}(r,s)\Leftrightarrow{}\kern0pt{}{F}_{{C}_{B}}^{\rho{},\eta{}}(\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,\eta{}),\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(q,\eta{})) \\ \wedge{}\:{}r\simeq{}I\:{}\wedge{}\:{}s\simeq{}I.\end{gathered}
$$



(56)

At proof I the two conversion requirements are reflexivity. Hence



$$
\forall{}\rho{}\;{}{F}_{{\mathrm{I}\mathrm{d}}_{{C}_{B}}(p,q)}^{\rho{},{\eta{}}_{0}}(I,I)\Leftrightarrow{}{V}_{B}(p,q).
$$



(57)

The original G identity clause requires endpoint F equality at the left unary environment and endpoint F equality at the right unary environment, together with the two proof conversions to I. It does not add an extra cross-relation between p and q. At the empty telescope both term environments are ${\eta{}}_{0}$, so (56) gives



$$
\begin{gathered}{G}_{{\mathrm{I}\mathrm{d}}_{{C}_{B}}(p,q)}^{\mathcal{R},{\eta{}}_{0},{\eta{}}_{0}}(I,I) \\ \quad{}\Leftrightarrow{}{F}_{{C}_{B}}^{{\rho{}}_{L},{\eta{}}_{0}}(P,Q)\:{}\wedge{}\:{}{F}_{{C}_{B}}^{{\rho{}}_{R},{\eta{}}_{0}}(P,Q).\end{gathered}
$$



(58)

Universal unary validity implies (58) for every relational environment. Conversely diagonal relational environments recover every unary validity instance. Thus universal original G identity validity at I is equivalent to ${V}_{B}$ as well.

Finally, if a polynomial w is a semantic identity witness uniformly in the environments, projecting its identity clause yields the endpoint equality. Conversely the closed polynomial atom I supplies one uniform witness whenever ${V}_{B}$ holds. Therefore existence of a semantic polynomial identity witness is equivalent to ${V}_{B}$. The same implication holds whether the witness is required in the unary interpretation or in the full relational interpretation, by (57)–(58).

These equivalences transfer the annotated completeness theorem and the finite negative-certificate result without changing the endpoint coding. A semantic witness is not a derivation of Has at the identity type. In particular, these results do not say that every semantically valid identity has a current syntactic proof.

### 13 No computable uniform distinguishing-input bound

**Corollary 9.** There is no partial computable function b that terminates on every a in ACert and has the following guarantee: whenever the endpoints of a are semantically unequal, some



$$
n\le{}b(a)
$$



has opposite Boolean observations. In particular no total computable function has this guarantee.

**Proof.** On an arbitrary input a, first perform the decidable ACert check and reject invalid annotations. On a valid annotation compute b(a), which terminates by hypothesis. For each $0\le{}n\le{}b(a)$, compute the two observation bits by the terminating conversion searches of Section 4. If one pair differs, reject by Proposition 6. If every pair agrees, accept: the proposed guarantee excludes semantic inequality. This would decide ${E}_{B}^{\mathrm{c}\mathrm{e}\mathrm{r}\mathrm{t}}$, contrary to Theorem 1. ∎

A computable bound depending only on an effective length measure of the endpoint syntax, or of the endpoints together with their certificates, would compose with the computable length function and give such a b. It is therefore impossible as well.

For each fixed size bound, only finitely many annotated strings occur. Every unequal valid one has a least distinguishing input. Their finite maximum therefore exists, with value zero if there are no such strings. The corollary excludes a computable uniform majorant of these maxima; it does not deny their existence. Nor does it exclude a bound proved for a separately restricted family or a particular pair. It asserts no complexity bound for discovering one output’s bit. An arbitrary fixed testing budget has no uniform completeness guarantee on this whole certified domain.

### 14 Formalisation boundary and interpretation

The mathematical conclusion above is a written completeness theorem with substantial kernel-checked components. The formalised components include:

- semantic natural standardness, canonical numeral typings and applied equations, and the same-index relation;

- arbitrary semantic Boolean standardness, equality by observation, and canonical-test completeness;

- the sound and complete mismatch characterization on current-typed endpoints;

- finite-arity primitive-recursion compilation into the actual current Has judgement, including successor, composition, recursion and their context shifts;

- adequacy for arbitrary raw NatObs inputs;

- literal Boolean choices, the zero/nonzero discriminator and their current typings and equations;

- the closed simulator family and equivalence (38) for every finite PR₂ description;

- the original F/G identity transfers, semantic witness equivalence and current identity formation.

The public Boolean development uses the modules EffectiveBooleanStandardness, EffectiveBooleanCertificates, EffectivePrimitiveRecursion and EffectiveBooleanInterfaces. The semantic Boolean declarations are in P01AC.BooleanIdentity, and the compiler declarations are in P01AC.BooleanPrimitive. The natural foundations are reused from P01AC.EffectiveCompleteness and P01AC.IdentityComplexity. In particular, the compiler’s central results are PR.compile\_has and PR.compile\_obs; the discriminator is zeroDiscriminator, with discriminator\_has and discriminator\_obs.

The following remain written mathematics rather than a whole-theorem kernel formalisation: the effective finite certificate coding and validator argument; the arithmetic constructions, numerical pairing and lists; the concrete binary-machine Step, Run and χ and construction of the particular description fχ; the complete machine-indexing argument; the external computability classification and extraction-independent reduction algorithm; and the uniform-bound contradiction. The general current-Has compiler and its adequacy are proved, so this distinction leaves no assumed current-typing representation bridge in the lower bound.

The checked core compiler and discriminator declarations use propositional extensionality and quotient soundness. The semantic declarations also use classical choice. The decisive checked declarations contain no admitted-proof axiom or newly postulated representation axiom. The result is not presented as a kernel formalisation of the full external machine and hierarchy argument.

The mechanism separating this theorem from Raw-valued identity is the codomain’s observational totality. Every self-related Boolean output makes one of two effectively discoverable choices, while the canonical natural input domain remains unbounded. This gives complete finite negative witnesses and an exact Π₁ annotated classification. It neither changes the original semantics nor turns universal identity checking into a finite test.

Paper 3

## Bare Boolean Identity and Fixed Type Typability

### Abstract

For the fixed P01AC polynomial calculus, semantic equality of closed current-typed functions from Church naturals to Church Booleans is d.c.e.-complete when the input contains only the endpoint syntax. Closed typability at this single function type is ${\Sigma{}}_{1}^{0}$-complete. The equality problem is therefore neither recursively enumerable nor co-recursively enumerable. These results concern the actual current typing judgement and the original relational interpretations; they do not identify semantic membership with syntactic typability.

The proof separates two independent computations. An explicit search gate permits a current typing exactly when one machine halts. Once the gate returns, the established Boolean simulator makes equality hold exactly when a second machine does not halt. The positive gate argument respects the restricted polynomial conversion rules by exposing the actual combinator syntax. The negative argument proves that the search remains active at the head under every finite list of arguments. This rules out the possibility that application erases an otherwise divergent subterm.

The supporting Lean development checks the syntax, the positive typing and equality transport, and the semantic non-typability interface. The head-reduction argument and computability classifications are written mathematics. The certificate-carrying equality problem retains its previously established ${\Pi{}}_{1}^{0}$-complete classification.

### 1 The fixed problem

#### 1.1 Syntax and semantics

Raw terms are finite trees generated by the combinators $I,K,S$, two inert markers $\mathbf{0},\mathbf{1}$, and application. Application associates to the left. Compatible reduction has the three computational rules



$$
Ia\to{}a,\quad{}\quad{}Kab\to{}a,\quad{}\quad{}Sfgx\to{}fx(gx).
$$



(1)

Write $t\simeq{}u$ for the equivalence relation generated by these rules in application contexts. This is the unchanged raw conversion relation. The markers have no computational rules and are distinct normal forms.

A polynomial is a finite tree built from variables, arbitrary raw-term atoms, and application. Its evaluation at an environment $\eta{}$ is $\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,\eta{})$. A closed polynomial has no free variables; its evaluation is independent of the environment. Fix ${\eta{}}_{0}$ to be the environment constantly equal to $\mathbf{0}$, and abbreviate



$$
|p|=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,{\eta{}}_{0})\quad{}\mathrm{f}\mathrm{o}\mathrm{r}\ \mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}\mathrm{d}\ p.
$$



(2)

The existing bracket abstraction is denoted $[x]p$. It is an operation on polynomials, with its established applied computation law



$$
\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}([x]p,\eta{})\,{}a\simeq{}\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,a::\eta{}).
$$



(3)

This notation introduces no new object-language constructor.

We use the actual judgement $\mathrm{H}\mathrm{a}\mathrm{s}\,{}\Gamma{}\,{}p\,{}A$, the original unary interpretation $F$, and the original relational interpretation $G$. In particular, $\mathrm{H}\mathrm{a}\mathrm{s}$ means a finite derivation in the current rules, not merely semantic membership. Put



$$
N=\forall{}X.(X\to{}X)\to{}X\to{}X,\quad{}\quad{}B=\forall{}X.X\to{}X\to{}X,\quad{}\quad{}{C}_{B}=N\to{}B.
$$



(4)

For closed endpoints define



$$
{V}_{B}(p,q)\Leftrightarrow{}\forall{}\rho{}\;{}{F}_{{C}_{B}}^{\rho{},{\eta{}}_{0}}(|p|,|q|).
$$



(5)

Thus equality ranges over all unary type environments and the full original arrow clause, including independently related arguments. The universal-type membership conditions of the original semantics are retained.

#### 1.2 Bare and annotated codes

Fix effective codes for raw terms, polynomials, types, contexts and finite current derivation trees. Let



$$
\begin{array}{rl}{T}_{{C}_{B}} & =\{p:p\ \mathrm{i}\mathrm{s}\ \mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}\mathrm{d}\ \mathrm{a}\mathrm{n}\mathrm{d}\ \mathrm{H}\mathrm{a}\mathrm{s}\,{}[]\,{}p\,{}{C}_{B}\}, \\ D & ={T}_{{C}_{B}}\times{}{T}_{{C}_{B}}, \\ {E}_{B} & =\{(p,q)\in{}D:{V}_{B}(p,q)\}.\end{array}
$$



(6)

Malformed codes lie outside these sets. In particular, an untypable pair is a negative instance of ${E}_{B}$. This is a total decision problem on codes, not a promise problem restricted to an externally supplied typed domain.

A set is d.c.e. when it is the difference of two recursively enumerable sets. Completeness throughout means completeness under total computable many-one reductions. The class d.c.e. is also called 2-c.e. and is contained in ${\Delta{}}_{2}^{0}$.

**Theorem 1.** The bare equality set ${E}_{B}$ is d.c.e.-complete. The fixed-type typability set ${T}_{{C}_{B}}$ is ${\Sigma{}}_{1}^{0}$-complete. Consequently ${E}_{B}$ is neither recursively enumerable nor co-recursively enumerable. The same d.c.e.-complete classification holds for the original closed $F$- and $G$-identity-validity problems at proof $I$, and for existence of a semantic polynomial identity witness, when they use the same bare current-typed endpoint domain.

The companion *Boolean Identity Completeness* proves that equality with supplied finite endpoint-typing certificates is ${\Pi{}}_{1}^{0}$-complete. Theorem 1 resolves the different presentation obtained by erasing those certificates.

### 2 The established Boolean family

We recall precisely the results from *Boolean Identity Completeness* needed here. Their compiler, arithmetic construction and binary-machine indexing are unchanged.

Let ${u}_{n}$ be the evaluated canonical Church numeral. For an arbitrary raw term $t$, define



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(t,n)\Leftrightarrow{}\forall{}f,x\;{}tfx\simeq{}{f}^{n}x.
$$



(7)

The current-typed successor polynomial $\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}$ satisfies



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(t,n)\Rightarrow{}\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(|\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}|t,n+1).
$$



(8)

Fix the finite primitive-recursive description ${f}_{\chi{}}$ from that companion. Its numerical function $\chi{}(n,e)$ tests whether the blank-input binary machine with code $e$ has halted within $n$ steps. Thus



$$
\begin{array}{rl}e\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s} & \Leftrightarrow{}\exists{}n\;{}\chi{}(n,e)\ne{}0, \\ e\ \mathrm{n}\mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s} & \Leftrightarrow{}\forall{}n\;{}\chi{}(n,e)=0.\end{array}
$$



(9)

The accepted indexing represents every recursively enumerable predicate by a total computable map to such machine codes. The construction of this specific ${f}_{\chi{}}$ is finite and uses only the stated primitive-recursion basis.

Let ${p}_{e}$ be the associated closed Boolean simulator polynomial and let ${q}_{0}$ be the fixed constant first-choice function. The current typing and equality results are



$$
\mathrm{H}\mathrm{a}\mathrm{s}\,{}[]\,{}{p}_{e}\,{}{C}_{B},\quad{}\quad{}\mathrm{H}\mathrm{a}\mathrm{s}\,{}[]\,{}{q}_{0}\,{}{C}_{B},
$$



(10)



$$
{V}_{B}({p}_{e},{q}_{0})\Leftrightarrow{}\forall{}n\;{}\chi{}(n,e)=0.
$$



(11)

More importantly for the gate, the compiler is adequate on every raw $\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}$ input. Applied abstraction, compiler adequacy and the zero discriminator give



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(t,n)\Rightarrow{}|{p}_{e}|txy\simeq{}\{\begin{array}{ll}x, & \chi{}(n,e)=0, \\ y, & \chi{}(n,e)\ne{}0.\end{array}
$$



(12)

The premise in (12) is observational. It does not require that $t$ be a canonical numeral, currently typed, or a semantic member. The supporting development checks this version explicitly.

We also use two semantic consequences from the same companion. First, current typing at $B$, or arbitrary semantic self-relatedness at $B$, forces one uniform Boolean choice. In particular,



$$
{F}_{B}^{\rho{},\eta{}}(b,b)\Rightarrow{}\exists{}i\in{}\{0,1\}\;{}b\mathbf{0}\mathbf{1}\simeq{}\mathbf{i}.
$$



(13)

Second, on $D$, equality is characterised by all canonical observations. Writing



$$
{\mathrm{o}\mathrm{b}\mathrm{s}}_{n}(p)=|p|{u}_{n}\mathbf{0}\mathbf{1},
$$



(14)

we have



$$
{V}_{B}(p,q)\Leftrightarrow{}\forall{}n\;{}{\mathrm{o}\mathrm{b}\mathrm{s}}_{n}(p)\simeq{}{\mathrm{o}\mathrm{b}\mathrm{s}}_{n}(q).
$$



(15)

The converse in (15) restores the original relation on independently related semantic naturals, in every environment. It is not a redefinition of arrow equality.

### 3 Polynomial conversion and exposed syntax

#### 3.1 Why raw conversion alone is insufficient

The current polynomial conversion relation, written $\mathrm{P}\mathrm{o}\mathrm{l}\mathrm{y}\mathrm{C}\mathrm{o}\mathrm{n}\mathrm{v}$, has reflexivity, symmetry, transitivity, application congruence and the exposed $I/K/S$ contractions. It has no rule that unfolds an arbitrary raw atom. For example, the polynomial atom containing the raw application $II$ is not literally the polynomial application of the two atoms $I$ and $I$.

This distinction matters because the current typing conversion rule has the form



$$
\frac{\mathrm{F}\mathrm{o}\mathrm{r}\mathrm{m}\,{}\Gamma{}\,{}A\quad{}\mathrm{H}\mathrm{a}\mathrm{s}\,{}\Gamma{}\,{}p\,{}A\quad{}\mathrm{P}\mathrm{o}\mathrm{l}\mathrm{y}\mathrm{C}\mathrm{o}\mathrm{n}\mathrm{v}(p,q)\quad{}\mathrm{S}\mathrm{c}\mathrm{o}\mathrm{p}\mathrm{e}\mathrm{d}(|\Gamma{}|,q)}{\mathrm{H}\mathrm{a}\mathrm{s}\,{}\Gamma{}\,{}q\,{}A}.
$$



(16)

A conversion between raw evaluations cannot simply be inserted into (16).

#### 3.2 Purity and reification

Call a polynomial *pure* if every atom is one of the primitive raw terms $I,K,S$. Variables and polynomial application are allowed. In particular, neither an inert marker nor a compound raw application is a permitted atom of a pure polynomial.

**Lemma 2.** Every output of the current finite primitive-recursion compiler is pure. The canonical numeral polynomials, $\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}$, ${p}_{e}$, and ${q}_{0}$ are pure. A closed pure polynomial evaluates to a marker-free raw term.

**Proof.** Variables and the primitive combinator atoms are pure. Renaming preserves purity, and substitution preserves it whenever the images of the variables actually occurring are pure. The fixed bracket abstraction preserves purity: its bound-variable case uses $I$, its absent-variable case uses $K$, and its application case uses $S$ and the recursively abstracted subterms. The represented pair and projections are also explicit polynomial expressions in these three combinators.

Induct on the finite primitive-recursion description. Zero, successor and projection follow from these observations. The recursion case uses only the represented pair, projections, successor, substitution and abstraction. In a composition with source arity $k$, the compiler substitutes the recursively compiled arguments for indices below $k$, and uses a marker-valued default for the other indices. The already proved current compiler typing implies scope below $k$, so that default is never inserted. This proves purity even at arity zero. The simulator and constant function then use only pure subterms and abstraction.

For a closed pure polynomial, evaluation never consults ${\eta{}}_{0}$, because no free variable occurs. Its only raw leaves are therefore $I,K,S$, proving marker-freeness. ∎

Define structural exposure $\mathcal{E}$ on raw terms by



$$
\begin{array}{rl}\mathcal{E}(fa) & =\mathrm{a}\mathrm{p}\mathrm{p}(\mathcal{E}(f),\mathcal{E}(a)), \\ \mathcal{E}(c) & =\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{m}(c)\quad{}(c\in{}\{I,K,S,\mathbf{0},\mathbf{1}\}).\end{array}
$$



(17)

**Lemma 3.** If $t\simeq{}u$, then $\mathrm{P}\mathrm{o}\mathrm{l}\mathrm{y}\mathrm{C}\mathrm{o}\mathrm{n}\mathrm{v}(\mathcal{E}(t),\mathcal{E}(u))$. If $p,q$ are closed and pure, then



$$
|p|\simeq{}|q|\Rightarrow{}\mathrm{P}\mathrm{o}\mathrm{l}\mathrm{y}\mathrm{C}\mathrm{o}\mathrm{n}\mathrm{v}(p,q).
$$



(18)

**Proof.** Each root step in (1) becomes exactly the corresponding polynomial contraction after exposure. Each raw application-context step becomes polynomial application congruence. Induction on the finite raw conversion tree gives the first assertion.

Structural induction on a closed pure polynomial gives



$$
\mathcal{E}(|p|)=p.
$$



(19)

There is no variable case at scope zero, and every atom is already one primitive combinator. Apply the first assertion and substitute (19) at both endpoints. ∎

Lemma 3 is restricted to the stated fragment. It introduces no atom-unfolding or abstraction-congruence rule into the calculus.

### 4 The explicit search gate

Define raw counter terms by



$$
{A}_{0}={u}_{0},\quad{}\quad{}{A}_{n+1}=|\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}|{A}_{n}.
$$



(20)

Induction using (8) gives $\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}({A}_{n},n)$. These terms are closed and marker-free.

For a closed polynomial $p$, define



$$
\begin{array}{rl}{L}_{p} & =[r][n].\;{}p\,{}n\,{}(r\,{}r\,{}(\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}\,{}n))\,{}I, \\ {G}_{p} & ={L}_{p}\,{}{L}_{p}\,{}\overline{0}.\end{array}
$$



(21)

Here $\overline{0}$ is the canonical zero polynomial. In the body of (21), de Bruijn index zero is $n$ and index one is $r$. The embedded $p$ and $\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}$ are closed, so their indices require no adjustment. The inner abstraction binds $n$; the outer abstraction binds $r$. If $p$ is pure, both polynomials in (21) are closed and pure.

Put



$$
{\ell{}}_{p}=|{L}_{p}|,\quad{}\quad{}{S}_{p}(n)={\ell{}}_{p}{\ell{}}_{p}{A}_{n}.
$$



(22)

Two uses of (3) give



$$
{S}_{p}(n)\simeq{}|p|{A}_{n}{S}_{p}(n+1)I.
$$



(23)

Taking $p={p}_{e}$, equation (12) gives



$$
{S}_{{p}_{e}}(n)\simeq{}\{\begin{array}{ll}{S}_{{p}_{e}}(n+1), & \chi{}(n,e)=0, \\ I, & \chi{}(n,e)\ne{}0.\end{array}
$$



(24)

These conversion equations prove the finite successful computations. By themselves, they do not prove nontermination or non-typability in the unsuccessful case.

### 5 Halting gives actual current typing

**Lemma 4.** If $e$ halts, then $|{G}_{{p}_{e}}|\simeq{}I$. For every closed pure $q$ with $\mathrm{H}\mathrm{a}\mathrm{s}\,{}[]\,{}q\,{}{C}_{B}$,



$$
\mathrm{H}\mathrm{a}\mathrm{s}\,{}[]\,{}({G}_{{p}_{e}}q)\,{}{C}_{B}.
$$



(25)

For every current-typed right endpoint $r$, under the same assumptions,



$$
{V}_{B}({G}_{{p}_{e}}q,r)\Leftrightarrow{}{V}_{B}(q,r).
$$



(26)

**Proof.** By (9), some $t$ satisfies $\chi{}(t,e)\ne{}0$. At a successful bound, (24) gives conversion to $I$. At a preceding bound, either that bound is already successful or (24) passes to the next state. Finite backward induction therefore gives ${S}_{{p}_{e}}(0)\simeq{}I$, which is the first assertion. A least successful bound need not be computed.

Application congruence and the $I$ rule yield



$$
|{G}_{{p}_{e}}q|=|{G}_{{p}_{e}}||q|\simeq{}I|q|\simeq{}|q|.
$$



(27)

Both polynomials in the outer conversion are closed and pure. Lemma 3 gives $\mathrm{P}\mathrm{o}\mathrm{l}\mathrm{y}\mathrm{C}\mathrm{o}\mathrm{n}\mathrm{v}({G}_{{p}_{e}}q,q)$. Symmetry supplies its direction from the already typed $q$ to ${G}_{{p}_{e}}q$; (16), current formation of ${C}_{B}$, and the established closure prove (25).

For (26), both left endpoints are now actually current-typed. Equation (27) transports every canonical observation by raw congruence. Apply (15) to the two pairs with common endpoint $r$. ∎

This argument constructs a current typing through the actual conversion rule. It does not infer typing from semantic equality or from a bare raw equation.

### 6 A beta operational lemma

We use ordinary untyped lambda calculus only as a sound computational target. Write ${=}_{\beta{}}$ for beta conversion, ${\to{}}_{\beta{}}^{*}$ for finite beta reduction, and ${\to{}}_{h}$ for deterministic weak-head reduction. All substitutions avoid capture, and terms are considered up to alpha-renaming. A weak-head normal term is either an abstraction or a variable followed by zero or more arguments.

**External result K.** Kashima’s leftmost reduction theorem states that, for ordinary untyped lambda terms, if $M$ reduces by beta reduction to a beta-normal term $N$, then a finite leftmost reduction reaches $N$. We use the beta-only theorem, with capture-avoiding substitution, from Theorem 2.6 and Definitions 2.1–2.2 \[Kashima 2000, pp. 2–3\].

**Lemma 5.** For a free variable $z$,



$$
M{=}_{\beta{}}z\Rightarrow{}M{\to{}}_{h}^{*}z.
$$



(28)

**Proof.** First justify the conversion-to-reduction step separately. Define parallel beta reduction $\Rightarrow{}$ by variable reflexivity, lambda and application compatibility, and



$$
\frac{P\Rightarrow{}P\prime{}\quad{}\quad{}Q\Rightarrow{}Q\prime{}}{(\lambda{}x.P)Q\Rightarrow{}P\prime{}[Q\prime{}/x]}.
$$



(29)

Induction on the parallel derivation proves stability under simultaneous substitution of parallel-related terms. Define complete development ${M}^{*}$ recursively: develop variables and abstraction bodies; at an application, develop both subterms and contract the root precisely when the original left subterm is syntactically an abstraction. Induction on $M\Rightarrow{}N$, using substitution stability in the root-redex case, proves



$$
M\Rightarrow{}N\Rightarrow{}N\Rightarrow{}{M}^{*}.
$$



(30)

Hence parallel reduction has the diamond property. The finite grid argument gives confluence of its reflexive-transitive closure. That closure equals finite beta reduction: each beta step is parallel, and each parallel derivation serialises to finitely many beta steps. Beta-convertible terms therefore have a common reduct. Since $z$ is irreducible, the hypothesis of (28) gives $M{\to{}}_{\beta{}}^{*}z$.

Apply K. No intermediate term of the resulting trace can be an abstraction or a variable-headed application with a nonempty list of arguments. Those outer shapes are preserved by beta reduction and cannot become the bare variable $z$. Before its endpoint, the trace is therefore never weak-head normal. At every such term, the leftmost redex is exactly its unique weak-head redex. Thus the trace proves (28). ∎

Lemma 5 is a specialisation to a variable target. No general identification of full leftmost normalisation with weak-head normalisation is needed.

### 7 Forward translation and branch traces

#### 7.1 Exact computational translation

Choose distinct fresh free lambda variables ${z}_{0},{z}_{1}$. Define $\mathcal{T}$ on raw terms by preserving application and setting



$$
\begin{array}{rl}\mathcal{T}(I) & =\lambda{}x.x, \\ \mathcal{T}(K) & =\lambda{}xy.x, \\ \mathcal{T}(S) & =\lambda{}fgx.fx(gx), \\ \mathcal{T}(\mathbf{0}) & ={z}_{0},\quad{}\quad{}\mathcal{T}(\mathbf{1})={z}_{1}.\end{array}
$$



(31)

Bound names are chosen to avoid capture. The source markers thus become variables of ordinary lambda calculus; no additional constant syntax or extension of K is required.

**Lemma 6.** Raw conversion is preserved:



$$
t\simeq{}u\Rightarrow{}\mathcal{T}(t){=}_{\beta{}}\mathcal{T}(u).
$$



(32)

Extending $\mathcal{T}$ to polynomials by translating variables and atoms and preserving application, the actual bracket abstraction satisfies



$$
\mathcal{T}([x]b){=}_{\beta{}}\lambda{}x.\mathcal{T}(b).
$$



(33)

**Proof.** The three source root rules in (1) translate into one, two and three beta contractions, respectively. Application contexts preserve those reductions. Induct on the finite raw conversion proof to obtain (32).

For (33), induct on the exact bracket-abstraction definition. Its bound-variable case is the translation of $I$. In the absent-variable case, $K$ discards the new argument, and the index-drop operation removes the unused binder. In the present application case, the translation of $S$ applies both recursively abstracted subterms to the bound variable. Beta congruence under abstraction completes the induction. Every step uses beta conversion only. ∎

Only the forward implication in (32) is used. Equation (33) does not assert abstraction congruence for source $\mathrm{P}\mathrm{o}\mathrm{l}\mathrm{y}\mathrm{C}\mathrm{o}\mathrm{n}\mathrm{v}$.

#### 7.2 Uniform finite branch traces

Put



$$
{D}_{e}=\mathcal{T}(|{p}_{e}|),\quad{}\quad{}{s}_{+}=\mathcal{T}(|\mathrm{S}\mathrm{u}\mathrm{c}\mathrm{c}|),\quad{}\quad{}\iota{}=\lambda{}x.x,\quad{}\quad{}{a}_{n}=\mathcal{T}({A}_{n}).
$$



(34)

These are closed lambda terms. In particular, ${z}_{0},{z}_{1}$ do not occur in ${D}_{e}$ or ${a}_{n}$. Also ${a}_{n+1}={s}_{+}{a}_{n}$ literally, because translation preserves application.

**Lemma 7.** If $\chi{}(n,e)=0$, then for arbitrary lambda terms $U,V$,



$$
{D}_{e}{a}_{n}UV{\to{}}_{h}^{*}U.
$$



(35)

The displayed trace can be retained when any fixed finite list of trailing arguments is appended.

**Proof.** Apply (12) to ${A}_{n}$ and the source markers, then use (32). This gives



$$
{D}_{e}{a}_{n}{z}_{0}{z}_{1}{=}_{\beta{}}{z}_{0}.
$$



(36)

Lemma 5 supplies its finite deterministic weak-head trace. Since ${D}_{e},{a}_{n}$ are closed, the only free occurrences of the two placeholders come from the two supplied arguments.

Before the last state, neither placeholder can be the head of the whole term. A variable-headed term is already weak-head normal, and the deterministic trace could not continue to its prescribed endpoint. Therefore every preceding contraction is a lambda redex already on the head spine. Capture-avoiding simultaneous substitution of $U,V$ for the placeholders preserves that redex and its position. It may introduce redexes inside arguments, but the weak-head strategy does not select them while the old head redex is present. Induction over this finite trace gives (35), stopping at $U$ without reducing it.

Every contraction just described occurs on the existing head spine. Appending a fixed list of arguments preserves each contraction up to the final displayed state. The added arguments are not needed to create any of those redexes. ∎

This proof uses the finite trace on fresh placeholders. Extensional equality on arbitrary supplied branches alone would not justify a head-strategy claim.

### 8 Nonhalting excludes current typing

Define lambda terms



$$
\begin{array}{rl}{\mathcal{L}}_{e} & =\lambda{}rn.\;{}{D}_{e}n\,{}(rr({s}_{+}n))\,{}\iota{}, \\ {R}_{e}(n) & ={\mathcal{L}}_{e}{\mathcal{L}}_{e}{a}_{n}.\end{array}
$$



(37)

By (33),



$$
\mathcal{T}(|{G}_{{p}_{e}}|){=}_{\beta{}}{R}_{e}(0).
$$



(38)

**Lemma 8.** If $e$ never halts, then for every finite list ${Z}_{1},\ldots{},{Z}_{m}$, the term ${R}_{e}(0){Z}_{1}\cdots{}{Z}_{m}$ has an infinite deterministic weak-head reduction and is not beta-convertible to a variable.

**Proof.** Every $\chi{}(n,e)$ is zero. For each $n$, two head contractions followed by Lemma 7 give



$$
\begin{gathered}{R}_{e}(n){Z}_{1}\cdots{}{Z}_{m}{\to{}}_{h}^{2}{D}_{e}{a}_{n}{R}_{e}(n+1)\iota{}{Z}_{1}\cdots{}{Z}_{m} \\ {\to{}}_{h}^{*}{R}_{e}(n+1){Z}_{1}\cdots{}{Z}_{m}.\end{gathered}
$$



(39)

The second phase substitutes the next recursive state for the first placeholder and $\iota{}$ for the second. Each complete phase is finite and contains at least the first two contractions. Repetition therefore gives the actual infinite deterministic trace, not just an infinite sequence of convertible terms. Every trailing argument survives unchanged to the next phase.

If the starting term were beta-convertible to a variable, Lemma 5 would give a finite terminating trace for that same deterministic strategy, a contradiction. ∎

**Lemma 9.** If $e$ never halts, then for every closed polynomial $q$,



$$
\neg{}\mathrm{H}\mathrm{a}\mathrm{s}\,{}[]\,{}({G}_{{p}_{e}}q)\,{}{C}_{B}.
$$



(40)

**Proof.** First, its zero-input marker observation cannot convert to either marker. Otherwise, (32) and (38) would make



$$
{R}_{e}(0)\,{}\mathcal{T}(|q|)\,{}\mathcal{T}({u}_{0})\,{}{z}_{0}{z}_{1}
$$



(41)

beta-convertible to ${z}_{0}$ or ${z}_{1}$, contrary to Lemma 8. The terms in this finite trailing list may themselves contain placeholders; they are appended after the branch substitution in Lemma 7 and are unaffected by it.

Now suppose the typing in (40) existed. Current soundness makes the endpoint self-related at $N\to{}B$ in every unary environment. The canonical zero is self-related at $N$, so applying that arrow relation makes the resulting Boolean output self-related at $B$. Equation (13) then supplies exactly one of the marker conversions just excluded. Contradiction. ∎

The conclusion is non-typability at the fixed type ${C}_{B}$. It does not deny ordinary Raw typing. Nor does it depend on strong normalisation of the current calculus.

The application-sensitive argument is essential. For a divergent raw $\Omega{}$, the term $S(K(KI))(K\Omega{})$ can fail to have a full normal form while every application of it reduces to $I$. Mere absence of a normal form of an unapplied term would therefore be insufficient. In (39), the recursive call is instead the next head, with the entire trailing list preserved.

### 9 The exact classifications

#### 9.1 The upper bounds

The companion *Boolean Identity Completeness* establishes an explicit recursively enumerable mismatch set $M$: a witness consists of a canonical input and two finite raw conversion proofs to opposite markers. On currently typed endpoints, the witness is equivalent to semantic inequality. Consequently



$$
{E}_{B}=D\setminus{}M.
$$



(42)

The set $D$ is recursively enumerable by enumeration and recursive checking of the two finite current typing derivations. Therefore (42) is a d.c.e. presentation on all bare codes. The same certificate enumeration makes ${T}_{{C}_{B}}$ recursively enumerable.

#### 9.2 Difference hardness

Define the total computable map



$$
\Phi{}(e,j)=({G}_{{p}_{e}}{p}_{j},{q}_{0}).
$$



(43)

Its output is built from the fixed finite compiler and gate template. It neither decides halting nor searches for a typing certificate.

If $e$ never halts, Lemma 9 puts the first endpoint outside ${T}_{{C}_{B}}$, so the pair is outside ${E}_{B}$. If $e$ halts, Lemma 4 and (10) provide the two actual current typings. Equations (26) and (11) then identify its equality. Thus



$$
\Phi{}(e,j)\in{}{E}_{B}\Leftrightarrow{}e\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s}\:{}\wedge{}\:{}j\ \mathrm{n}\mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s}.
$$



(44)

Let $A=U\setminus{}V$ be any d.c.e. set, with $U,V$ recursively enumerable. From an input $x$, generate a finite blank-input program that halts exactly when $x$ enters $U$, and independently one that halts exactly when $x$ enters $V$. Compile both into the same binary-machine indexing used for $\chi{}$. This gives total computable code maps $e(x),j(x)$, including on negative instances. Equation (44) yields



$$
x\in{}A\Leftrightarrow{}\Phi{}(e(x),j(x))\in{}{E}_{B}.
$$



(45)

Hence ${E}_{B}$ is d.c.e.-hard; (42) gives its matching upper bound.

#### 9.3 Typability at one fixed type

The polynomial ${q}_{0}$ is closed, pure and currently typed. Lemmas 4 and 9 therefore give



$$
e\ \mathrm{h}\mathrm{a}\mathrm{l}\mathrm{t}\mathrm{s}\Leftrightarrow{}\mathrm{H}\mathrm{a}\mathrm{s}\,{}[]\,{}({G}_{{p}_{e}}{q}_{0})\,{}{C}_{B}.
$$



(46)

This is a total computable reduction of halting to ${T}_{{C}_{B}}$. Together with its enumeration above, it proves ${\Sigma{}}_{1}^{0}$-completeness. The target type is fixed throughout; it is not part of the varying input.

For completeness, fix a halting index in (44). This reduces nonhalting to ${E}_{B}$, excluding recursive enumerability. Fixing a nonhalting second index instead reduces halting to ${E}_{B}$, excluding co-recursive enumerability. These consequences follow from the same reduction, without a separate typing-inference theorem.

### 10 Original identity interpretations

For the current identity type with closed endpoints, the original unary clause is



$$
{F}_{{\mathrm{I}\mathrm{d}}_{{C}_{B}}(p,q)}^{\rho{},{\eta{}}_{0}}(a,b)\Leftrightarrow{}{F}_{{C}_{B}}^{\rho{},{\eta{}}_{0}}(|p|,|q|)\wedge{}a\simeq{}I\wedge{}b\simeq{}I.
$$



(47)

At proof $I$, the last two conjuncts are reflexive conversions. The original $G$-identity clause asks for that endpoint equality in its left and right unary environments, together with the proof conversions. Diagonal relational environments recover each unary instance. Thus universal original $F$- and $G$-identity validity at $I$ are both equivalent to (5).

A semantic polynomial identity witness implies endpoint equality by projecting its identity clause. Conversely, the constant polynomial $I$ supplies a semantic witness whenever (5) holds. Imposing exactly the endpoint domain $D$ therefore transfers the d.c.e.-complete classification to all these bare-code formulations.

Existence of such a semantic witness does not assert a current derivation of the identity type. No syntactic identity-completeness claim is made.

### 11 Formalisation boundary

The supporting Lean development contains two modules, BareBooleanGateSyntax and BareBooleanGatePositive. They use the unchanged current syntax and semantics. Their checked declarations establish:

- purity of the actual primitive-recursion compiler and simulator, including the scoped treatment of the marker-valued composition default;

- marker-freeness of closed pure evaluations, raw-conversion exposure, and exact lifting to polynomial conversion in that fragment;

- the concrete gate syntax, closure, purity, counter observations, and one-state computation equation;

- the Boolean branch equation for arbitrary raw natural observations;

- finite halting conversion, the current typing in Lemma 4, and its original-semantic equality transport;

- the implication from absent marker observations to current non-typability used in Lemma 9.

The checked positive and semantic declarations use only propositional extensionality, classical choice and quotient soundness as applicable. The pure closed conversion-lifting theorem is axiom-free. There is no admitted proof or newly postulated representation axiom.

The complete head argument in Sections 6–8 is written mathematics: ordinary lambda confluence, the specialisation in Lemma 5, fresh-placeholder trace transport and infinite head activity are not kernel-checked in these modules. The source-to-lambda forward simulation already has checked foundational components, but the full ordinary-lambda argument presented here is not thereby a kernel theorem. The specific arithmetic description ${f}_{\chi{}}$, external certificate and machine coding, and arithmetic-hierarchy classifications retain the written/formal boundary stated in *Boolean Identity Completeness*.

Thus the result is a complete mathematical classification with checked supporting components. It is not presented as a whole-theorem Lean formalisation. Certificate-carrying equality remains ${\Pi{}}_{1}^{0}$-complete, while erasing the certificates yields the d.c.e.-complete set in Theorem 1.

### References

*Boolean Identity Completeness*. Companion development for the same P01AC syntax and original semantics. Sections 2–4 establish standardness, canonical testing and finite mismatch certificates; Sections 5–11 give the primitive-recursive compiler and concrete bounded-halting family; Section 12 gives the original identity transfers.

Ryo Kashima. *A Proof of the Standardization Theorem in Lambda-Calculus*. Tokyo Institute of Technology, August 2000. Theorem 2.6 and Definitions 2.1–2.2. [Author-hosted paper](<https://www.is.c.titech.ac.jp/users/kashima/pub/C-145.pdf>).

Paper 4

## Restricted Semantic Identity Completeness for Natural Number Expressions in P01AC

This chapter proves a sound and complete finite certificate theorem for a declared first-order expression fragment of P01AC. Expressions are built from natural constants, finitely many natural-number variables, addition, multiplication, and zero tests. Their semantic equality is characterised by a finite table of nonnegative polynomial coefficient maps, or equivalently by agreement on an explicitly computable finite set of inputs. The result concerns the original P01AC interpretations and the endpoints produced by a fixed compiler.

The source-specific compilation, current typing, and bridge to the original semantic relations are kernel-checked. A separate executable Lean coefficient checker and typed finite-certificate verifier now also have kernel-checked soundness and completeness for this fragment. The complete written argument below additionally gives an explicit finite separating grid and a strict Python reference interface. The degree-bounded grid proof remains written mathematics, and the Python implementation is not formally refined against the Lean program. The theorem does not assert syntactic identity inhabitation in the current typing judgement.

### 1 Result and exact scope

Fix the P01AC raw applicative calculus, polynomial syntax, current telescope-indexed judgement $\mathrm{H}\mathrm{a}\mathrm{s}$, raw conversion $\mathrm{C}\mathrm{o}\mathrm{n}\mathrm{v}$, and original paired interpretations $F$ and $G$ used in the Boolean semantic-identity result. Define the natural-number type and its curried finite-arity input types by



$$
N=\forall{}X.\,{}(X\to{}X)\to{}X\to{}X,\quad{}\quad{}{C}_{0}=N,\quad{}\quad{}{C}_{r+1}=N\to{}{C}_{r}.
$$



Equation (R1).

For every finite arity $r$, consider the expression grammar



$$
{E}_{r}\;{}:\mathop{:=}\;{}c\mid{}{x}_{i}\mid{}{E}_{r}+{E}_{r}\mid{}{E}_{r}\cdot{}{E}_{r}\mid{}\mathrm{i}\mathrm{f}\:{}{E}_{r}=0\:{}\mathrm{t}\mathrm{h}\mathrm{e}\mathrm{n}\:{}{E}_{r}\:{}\mathrm{e}\mathrm{l}\mathrm{s}\mathrm{e}\:{}{E}_{r},
$$



Equation (R2).

where $c\in{}\mathbb{N}$ and $0\le{}i<r$. Expressions are finite trees. Their direct natural-number semantics is written $[\![e]\!](v)$ for $v\in{}{\mathbb{N}}^{r}$. A conditional evaluates its zero branch exactly when its test has natural value zero. The grammar has no subtraction, negative coefficient, arbitrary equality test, user-defined recursion, higher-order input, or embedded arbitrary P01AC term. Addition and multiplication are unbounded natural operations, but the expression grammar has no recursion constructor.

Section 2 defines a total, syntax-directed compilation $e\mapsto{}{p}_{e}$ into the existing P01AC syntax. It satisfies



$$
\mathrm{H}\mathrm{a}\mathrm{s}\:{}[]\:{}{p}_{e}\:{}{C}_{r}.
$$



Equation (R3).

Put ${P}_{e}=\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}({p}_{e},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v})$. The exact semantic target is



$$
{V}_{r}(e,f)\:{}\Leftrightarrow{}\:{}\forall{}\ \mathrm{u}\mathrm{n}\mathrm{a}\mathrm{r}\mathrm{y}\ \mathrm{e}\mathrm{n}\mathrm{v}\mathrm{i}\mathrm{r}\mathrm{o}\mathrm{n}\mathrm{m}\mathrm{e}\mathrm{n}\mathrm{t}\mathrm{s}\ \rho{},\quad{}F({C}_{r},\rho{},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},{P}_{e},{P}_{f}).
$$



Equation (R4).

This definition uses the original $F$ relation, with independently related arguments at every arrow. It is not defined by testing only syntax-definable arguments, by contextual equivalence, by raw conversion of unapplied programs, or by a replacement equality relation.

**Theorem A (restricted completeness).** For every finite $r$ and every $e,f\in{}{E}_{r}$, the following conditions are equivalent.

1. ${V}_{r}(e,f)$.

2. $[\![e]\!](v)=[\![f]\!](v)$ for every $v\in{}{\mathbb{N}}^{r}$.

3. For every zero/nonzero input mask $S\subseteq{}\{0,\ldots{},r-1\}$, the coefficient maps ${\mathrm{N}\mathrm{F}}_{S}(e)$ and ${\mathrm{N}\mathrm{F}}_{S}(f)$ defined in Section 3 are identical.

4. The two expressions agree on the explicitly computable finite union of grids $\mathcal{G}(e,f)$ defined in Section 4.

5. There exists a finite positive certificate accepted by the verifier in Section 5 for this exact instance $(r,e,f)$.

These conditions are also equivalent to universal original $F$-identity validity at proof $I$, universal original $G$-identity validity at proof $I$, and existence of a uniform semantic polynomial witness for $\mathrm{I}\mathrm{d}({C}_{r},{p}_{e},{p}_{f})$.

Consequently, equality of expression-presented instances is decidable. Its positive instances have a sound and complete finite, recursively checked certificate system, and its unequal instances have a computably bounded distinguishing canonical tuple. Both the arity and the expressions may vary in the input.

Theorem A does not establish current-$\mathrm{H}\mathrm{a}\mathrm{s}$ syntactic identity completeness. In particular, it does not derive



$$
\mathrm{H}\mathrm{a}\mathrm{s}\:{}[]\:{}w\:{}\mathrm{I}\mathrm{d}({C}_{r},{p}_{e},{p}_{f}).
$$



Equation (R5), an excluded conclusion.

Nor does the theorem decide equality of arbitrary polynomials already typed at ${C}_{r}$. Its decidable input domain is the declared expression syntax, with endpoints obtained by the fixed compiler. If externally supplied P01AC endpoints are included in a claim, their literal equality to the compiled endpoints must be checked separately. A conversion-equivalent representation is not silently admitted into the fragment.

The methods are elementary polynomial and finite-case arguments. The contribution is the scoped completeness statement and its exact connection to this fixed calculus. No claim of worldwide priority or exhaustive literature coverage is made.

### 2 Compilation and the original semantics

#### 2.1 Literal primitive recursive descriptions

Use the finite-arity primitive-recursive description language and its fixed recursion convention:



$$
\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}(g,h)(0,\vec{x})=g(\vec{x}),
$$



Equation (R6).



$$
\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}(g,h)(n+1,\vec{x})=h(n,\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}(g,h)(n,\vec{x}),\vec{x}).
$$



Equation (R7).

Write ${P}_{i}^{k}$ for projection $i$ of arity $k$, and $\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(f;{g}_{0},\ldots{},{g}_{k-1})$ for finite composition. The following are actual finite descriptions in that language:



$$
{K}_{r}(0)={\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{r},\quad{}\quad{}{K}_{r}(c+1)=\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(\mathrm{s}\mathrm{u}\mathrm{c}\mathrm{c};{K}_{r}(c)),
$$



Equation (R8).



$$
A=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({P}_{0}^{1},\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(\mathrm{s}\mathrm{u}\mathrm{c}\mathrm{c};{P}_{1}^{3})),
$$



Equation (R9).



$$
M=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{1},\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(A;{P}_{2}^{3},{P}_{1}^{3})),\quad{}\quad{}Z=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({P}_{0}^{2},{P}_{3}^{4}).
$$



Equation (R10).

The descriptions $A$ and $M$ have arity two, while $Z$ has arity three. Induction on the recursion coordinate proves



$$
A(a,b)=a+b,\quad{}\quad{}M(a,b)=a\cdot{}b,
$$



Equation (R11).



$$
Z(t,a,b)=\{\begin{array}{ll}a & \mathrm{i}\mathrm{f}\ t=0, \\ b & \mathrm{i}\mathrm{f}\ t>0.\end{array}
$$



Equation (R12).

For $Z$, the step context is exactly $(\mathrm{c}\mathrm{o}\mathrm{u}\mathrm{n}\mathrm{t}\mathrm{e}\mathrm{r},\mathrm{a}\mathrm{c}\mathrm{c}\mathrm{u}\mathrm{m}\mathrm{u}\mathrm{l}\mathrm{a}\mathrm{t}\mathrm{o}\mathrm{r},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{B}\mathrm{r}\mathrm{a}\mathrm{n}\mathrm{c}\mathrm{h},\mathrm{p}\mathrm{o}\mathrm{s}\mathrm{i}\mathrm{t}\mathrm{i}\mathrm{v}\mathrm{e}\mathrm{B}\mathrm{r}\mathrm{a}\mathrm{n}\mathrm{c}\mathrm{h})$. Index three selects the positive branch. At zero, the base selects the first parameter. Neither the counter nor the accumulator is inadvertently selected.

Compile $e$ to a primitive-recursive description $T(e)$ by



$$
T(c)={K}_{r}(c),\quad{}\quad{}T({x}_{i})={P}_{i}^{r},
$$



Equation (R13).



$$
T(e+f)=\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(A;T(e),T(f)),\quad{}\quad{}T(e\cdot{}f)=\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(M;T(e),T(f)),
$$



Equation (R14).



$$
T(\mathrm{i}\mathrm{f}\:{}t=0\:{}\mathrm{t}\mathrm{h}\mathrm{e}\mathrm{n}\:{}e\:{}\mathrm{e}\mathrm{l}\mathrm{s}\mathrm{e}\:{}f)=\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(Z;T(t),T(e),T(f)).
$$



Equation (R15).

Every composition table has the finite length explicitly displayed here. Structural induction proves



$$
\mathrm{d}\mathrm{e}\mathrm{n}\mathrm{o}\mathrm{t}\mathrm{e}(T(e),v)=[\![e]\!](v),
$$



Equation (R16).

including $r=0$. This constructs a finite primitive-recursive description; it does not assume a representability theorem.

The source grammar remains restricted even though the fixed implementations of $A$, $M$, and $Z$ use the primitive-recursion constructor. An arbitrary primitive-recursive description is not an input expression. In particular, the bounded-machine simulator used in the global impossibility theorem is not admitted merely because its implementation is primitive recursive.

#### 2.2 Current typing and argument order

Let ${b}_{e}=\mathrm{P}\mathrm{R}.\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}\mathrm{i}\mathrm{l}\mathrm{e}(T(e))$, using the unchanged compiler. Its theorem PR.compile\_has gives



$$
\mathrm{H}\mathrm{a}\mathrm{s}\:{}(\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{C}\mathrm{t}\mathrm{x}\:{}r)\:{}{b}_{e}\:{}N,
$$



Equation (R17).

where $\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{C}\mathrm{t}\mathrm{x}\:{}r$ is the list of $r$ copies of $N$. The variable ${x}_{i}$ is exactly the existing de Bruijn coordinate $i$, rather than an unspecified named-variable convention.

Using the existing bracket abstraction, define



$$
{\mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}}_{0}(p)=p,\quad{}\quad{}{\mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}}_{r+1}(p)=\mathrm{a}\mathrm{b}\mathrm{s}\mathrm{t}\mathrm{r}\mathrm{a}\mathrm{c}\mathrm{t}({\mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}}_{r}(p)),\quad{}\quad{}{p}_{e}={\mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}}_{r}({b}_{e}).
$$



Equation (R18).

Repeated current arrow introduction proves Equation (R3). The subsidiary types ${C}_{k}$ are unchanged by term substitution, so each rule uses the actual dependent-rule body type. No informal arrow approximation is substituted for it. Scoping follows from has\_scoped.

The resulting application order is ${x}_{r-1},\ldots{},{x}_{0}$. Given $v=({v}_{0},\ldots{},{v}_{r-1})$, the canonical tuple is applied as



$$
{P}_{e}\,{}u({v}_{r-1})\cdots{}u({v}_{0}),
$$



Equation (R19).

where $u(n)$ is the canonical raw Church numeral. A consumer who wants ${x}_{0}$ first can explicitly reverse the input convention; no such renaming is hidden in the theorem or implementation.

For a raw list $xs$ in application order, define application and environment extension by



$$
\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}(t,[])=t,\quad{}\quad{}\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}(t,x::xs)=\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}(t\,{}x,xs),
$$



Equation (R20).



$$
\mathrm{E}\mathrm{x}\mathrm{t}\mathrm{e}\mathrm{n}\mathrm{d}(\eta{},[])=\eta{},\quad{}\quad{}\mathrm{E}\mathrm{x}\mathrm{t}\mathrm{e}\mathrm{n}\mathrm{d}(\eta{},x::xs)=\mathrm{E}\mathrm{x}\mathrm{t}\mathrm{e}\mathrm{n}\mathrm{d}(x::\eta{},xs).
$$



Equation (R21).

Induction using only applied bracket-abstraction beta proves



$$
\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}(\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}({\mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}}_{\mathrm{l}\mathrm{e}\mathrm{n}\mathrm{g}\mathrm{t}\mathrm{h}(xs)}(p),\eta{}),xs)\simeq{}\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(p,\mathrm{E}\mathrm{x}\mathrm{t}\mathrm{e}\mathrm{n}\mathrm{d}(\eta{},xs)).
$$



Equation (R22).

Thus $\mathrm{E}\mathrm{x}\mathrm{t}\mathrm{e}\mathrm{n}\mathrm{d}$ reverses the list into the de Bruijn coordinates. At arity zero, Equation (R22) is reflexive and has no application. Throughout this chapter, $\simeq{}$ denotes the fixed raw conversion relation.

#### 2.3 Adequacy for arbitrary observations

Retain the natural observation predicate



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(t,n)\:{}\Leftrightarrow{}\:{}\forall{}\ \mathrm{r}\mathrm{a}\mathrm{w}\ a,b,\quad{}t\,{}a\,{}b\simeq{}\mathrm{i}\mathrm{t}\mathrm{e}\mathrm{r}\mathrm{a}\mathrm{t}\mathrm{e}(a,n,b).
$$



Equation (R23).

The theorem PR.compile\_obs applies to arbitrary raw inputs satisfying $\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}$, not only canonical inputs. Combining it with Equation (R16) and the applied closure equation yields the following statement. If $\mathrm{l}\mathrm{e}\mathrm{n}\mathrm{g}\mathrm{t}\mathrm{h}(xs)=r$ and



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(\mathrm{E}\mathrm{x}\mathrm{t}\mathrm{e}\mathrm{n}\mathrm{d}(\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},xs)(i),{v}_{i})\quad{}\mathrm{f}\mathrm{o}\mathrm{r}\ \mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\mathrm{y}\ i<r,
$$



Equation (R24),

then



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}({P}_{e},xs),[\![e]\!](v)).
$$



Equation (R25).

No raw eta equality between unapplied terms is asserted.

#### 2.4 The exact bridge for all semantic arguments

Natural standardness and the same-index results for the original semantics have three consequences. Every self-related inhabitant of $N$ has a unique $\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}$ index. Related inhabitants of $N$ have the same index. Finally, two inhabitants of $N$ that are separately self-related and have the same $\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}$ index are $F$-related.

The last consequence retains the two endpoint-uniformity requirements of the original universal $F$ clause. An observation alone is not semantic membership.

For raw lists $xs,ys$, write $xs{\sim{}}_{\rho{}}ys$ when both lists have length $r$ and $F(N,\rho{},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},{xs}_{j},{ys}_{j})$ holds for every $j<r$. This notation includes two independently chosen lists. For arbitrary raw $t,u$, iteration of the original arrow clause gives



$$
\begin{gathered}F({C}_{r},\rho{},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},t,u)\Leftrightarrow{} \\ {\forall{}}_{xs{\sim{}}_{\rho{}}ys}\:{}F(N,\rho{},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}(t,xs),\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}(u,ys)).\end{gathered}
$$



Equation (R26).

Here the indices $j$ refer to list positions in application order. At $r=0$, the only lists are empty, and Equation (R26) is the original $N$ relation itself.

We now prove that ${V}_{r}(e,f)$ is equivalent to numerical equality everywhere. For the forward direction, choose any unary environment, for example the environment constantly equal to $\mathrm{r}\mathrm{a}\mathrm{w}\mathrm{P}\mathrm{E}\mathrm{R}$. Apply Equation (R26) to the same canonical reversed tuple on both sides. Canonical numeral typing gives each input self-relation. Equation (R25) gives output indices $[\![e]\!](v)$ and $[\![f]\!](v)$. Related outputs have equal indices, proving numerical equality.

For the converse, fix an arbitrary $\rho{}$ and independently related input lists $xs,ys$. The natural partial-equivalence-relation laws give self-relatedness of each input. Standardness and the related-same-index theorem give one common natural index at each paired coordinate. Reversing these coordinate indices produces one $v$ satisfying the hypotheses of Equation (R25) for both lists. Current soundness of the two closed endpoint typings supplies output self-relatedness after application to the corresponding self-related lists. Numerical equality and Equation (R25) give the same output index. The same-index converse therefore gives the cross-related output relation required by Equation (R26). Since $\rho{}$ and both input lists were arbitrary, ${V}_{r}(e,f)$ follows.

This proves the equivalence of Conditions 1 and 2 in Theorem A using the original semantics on all semantic inputs. The source-specific bridge is kernel-checked, including current typing, reverse-coordinate closure, arbitrary-observation adequacy, Equation (R26), both directions of the equivalence, identity formation, and the identity transfers that follow.

#### 2.5 Original identity clauses

The original unary identity clause at $I$ is exactly endpoint $F$ equality together with two occurrences of the reflexive conversion $I\simeq{}I$. Therefore universal $F$-identity validity is equivalent to ${V}_{r}(e,f)$. The original relational identity clause at $I$ requires endpoint $F$ equality in both the left and right unary environments, together with the same reflexive proof conversions. Universal ${V}_{r}(e,f)$ supplies this for every relational environment; diagonal environments give the converse.

If a uniform semantic polynomial witness exists, projecting its identity clause recovers endpoint equality. Conversely, the closed polynomial atom $I$ supplies a witness whenever endpoint equality holds. These are semantic assertions only. Current endpoint typings also give current formation of the identity type, but formation does not give inhabitation.

### 3 A finite table of nonnegative polynomial normal forms

#### 3.1 Coefficient maps and mask cells

For $S\subseteq{}\{0,\ldots{},r-1\}$, define the mask cell



$$
{D}_{S}=\{v\in{}{\mathbb{N}}^{r}:\:{}{v}_{i}>0\ \mathrm{f}\mathrm{o}\mathrm{r}\ i\in{}S,\quad{}{v}_{i}=0\ \mathrm{f}\mathrm{o}\mathrm{r}\ i\notin{}S\}.
$$



Equation (R27).

These ${2}^{r}$ cells are disjoint, cover ${\mathbb{N}}^{r}$, and are all nonempty. At arity zero there is one mask, one empty tuple, and one cell containing that tuple.

A coefficient map is a finitely supported function $p:{\mathbb{N}}^{r}\to{}\mathbb{N}$, represented by a finite sorted list of distinct exponent vectors with strictly positive coefficients. An omitted exponent has coefficient zero. The map evaluates as



$$
p(v)=\sum\limits_{\alpha{}\in{}\mathrm{s}\mathrm{u}\mathrm{p}\mathrm{p}(p)} p(\alpha{})\prod\limits_{i=0}^{r-1} {v}_{i}^{{\alpha{}}_{i}},
$$



Equation (R28),

where an empty product is one and ${0}^{0}=1$. The zero map has empty support. A map is $S$-normal when every supported exponent satisfies ${\alpha{}}_{i}=0$ for every $i\notin{}S$. Thus zero coordinates have already been substituted, and dead-variable exponents cannot create false differences between maps.

Addition is pointwise coefficient addition. Multiplication is finite convolution:



$$
(pq)(\gamma{})=\sum\limits_{\alpha{}+\beta{}=\gamma{}} p(\alpha{})q(\beta{}).
$$



Equation (R29).

The zero map is $\varnothing{}$; a positive constant $c$ is represented by $\{\vec{0}\mapsto{}c\}$, and a live variable ${x}_{i}$ by $\{{\mathrm{u}\mathrm{n}\mathrm{i}\mathrm{t}}_{i}\mapsto{}1\}$. These operations preserve finite support, nonnegative coefficients, and the $S$-normal support condition. Rearranging finite sums shows that they compute the usual sum and product evaluations. No cancellation is used.

#### 3.2 Positivity on a mask cell

**Lemma 1.** If $p$ is $S$-normal and $v\in{}{D}_{S}$, then $p(v)=0$ if and only if $p$ is the zero map.

**Proof.** The zero map evaluates to zero. If $p$ is nonzero, choose a supported exponent $\alpha{}$ with coefficient $c>0$. Every factor for a live coordinate is a positive natural number and remains positive after exponentiation. For every other coordinate, ${\alpha{}}_{i}=0$, so the factor is ${0}^{0}=1$. The chosen supported monomial therefore has strictly positive value. Every other summand is nonnegative, so the finite sum is positive. This also proves the empty-coordinate case: a nonzero constant is positive because the empty product is one. $\square{}$

#### 3.3 Syntax directed normalisation

Define ${\mathrm{N}\mathrm{F}}_{S}(e)$ recursively. The normal form of zero is the zero map; the normal form of $c>0$ is its constant map. The normal form of ${x}_{i}$ is its variable map when $i\in{}S$ and the zero map otherwise. For the arithmetic constructors, set



$$
{\mathrm{N}\mathrm{F}}_{S}(e+f)={\mathrm{N}\mathrm{F}}_{S}(e)+{\mathrm{N}\mathrm{F}}_{S}(f),\quad{}\quad{}{\mathrm{N}\mathrm{F}}_{S}(e\cdot{}f)={\mathrm{N}\mathrm{F}}_{S}(e){\mathrm{N}\mathrm{F}}_{S}(f).
$$



Equation (R30).

To normalise a conditional, first compute the test map. The rule is



$$
{\mathrm{N}\mathrm{F}}_{S}(\mathrm{i}\mathrm{f}\:{}t=0\:{}\mathrm{t}\mathrm{h}\mathrm{e}\mathrm{n}\:{}e\:{}\mathrm{e}\mathrm{l}\mathrm{s}\mathrm{e}\:{}f)=\{\begin{array}{ll}{\mathrm{N}\mathrm{F}}_{S}(e) & \mathrm{i}\mathrm{f}\ {\mathrm{N}\mathrm{F}}_{S}(t)=0, \\ {\mathrm{N}\mathrm{F}}_{S}(f) & \mathrm{o}\mathrm{t}\mathrm{h}\mathrm{e}\mathrm{r}\mathrm{w}\mathrm{i}\mathrm{s}\mathrm{e}.\end{array}
$$



Equation (R31).

Here zero means the empty coefficient map. The branch decision is a finite map-emptiness check. Computing the unchosen branch is unnecessary; computing it as well does not change the result. Recursion is on strict subexpressions and each map operation is finite, so normalisation terminates. Tests may themselves contain arbitrarily nested conditionals within this finite grammar.

**Lemma 2 (mask adequacy).** For every $e$ and $S$, the map ${\mathrm{N}\mathrm{F}}_{S}(e)$ is $S$-normal, and



$$
\forall{}v\in{}{D}_{S},\quad{}\quad{}{\mathrm{N}\mathrm{F}}_{S}(e)(v)=[\![e]\!](v).
$$



Equation (R32).

**Proof.** Induct on $e$. The cases for constants, variables, addition, and multiplication follow from the map definitions and finite sum and product evaluation. For a conditional, the induction hypothesis identifies the test value with ${\mathrm{N}\mathrm{F}}_{S}(t)(v)$. By Lemma 1, this value is zero throughout ${D}_{S}$ exactly when the test map is empty; otherwise it is positive throughout ${D}_{S}$. The normaliser therefore selects the same fixed branch as expression evaluation at every point of the cell. Apply the corresponding branch induction hypothesis. The support condition is inherited from that branch as well. $\square{}$

Nonnegativity is essential. If integer subtraction were allowed, $x-y$ would vanish at some positive tuples and not at others in the all-positive mask. The proof does not cover that larger grammar.

Identical normal-form tables therefore imply numerical equality on each cell and hence globally. The converse requires a separation theorem, rather than an unsupported assertion that different coefficient maps define different functions. Section 4 supplies the full argument.

#### 3.4 Exact semantic representation

Every finite table of $S$-normal nonnegative coefficient maps is realised by an expression in the grammar. At a leaf, express each monomial as its natural coefficient multiplied by the finite product of repeated variable factors, then sum the monomials. Empty support is represented by the constant zero. Construct a depth-$r$ decision tree testing ${x}_{0}=0$, then ${x}_{1}=0$, and so on. Put the corresponding map expression at each mask leaf. A zero branch marks its coordinate dead and the other branch marks it live.

On ${D}_{S}$, this tree reaches exactly the leaf for $S$, where the constructed arithmetic expression evaluates to the supplied map. Its normalised leaf map is exactly that $S$-normal map, because coefficient addition and convolution reconstruct the displayed finite sum of distinct monomials.

Thus the fragment denotes exactly the functions given by nonnegative polynomial pieces on the zero/nonzero input cells. Section 4 proves uniqueness of their table representation: unequal tables cannot denote the same function. The tables are a canonical complete invariant for the whole declared grammar, including arbitrary finite nested zero tests. At $r=0$, the decision tree has no tests and reifies its single constant map.

### 4 Finite grid separation and degenerate cases

#### 4.1 Univariate roots over the integers

**Lemma 3.** A nonzero integer polynomial of degree at most $d$ has at most $d$ distinct integer roots.

**Proof.** Induct on $d$. At $d=0$, a nonzero constant has no root. For $d>0$, there is nothing to prove if the polynomial has no root. Otherwise choose a root $a$. Write $P(T)=\sum\limits_{k=0}^{d} {c}_{k}{T}^{k}$ and use the finite identity



$$
{T}^{k}-{a}^{k}=(T-a)\sum\limits_{j=0}^{k-1} {T}^{k-1-j}{a}^{j}\quad{}\quad{}(k\ge{}1).
$$



Equation (R33).

Since $P(a)=0$, summing Equation (R33) gives $P(T)=(T-a)Q(T)$, where



$$
Q(T)=\sum\limits_{k=1}^{d} {c}_{k}\sum\limits_{j=0}^{k-1} {T}^{k-1-j}{a}^{j}.
$$



Equation (R34).

The degree of $Q$ is at most $d-1$. Moreover, $Q$ is nonzero: if the leading nonzero coefficient of $P$ is ${c}_{m}$, with $m\ge{}1$, then the coefficient of ${T}^{m-1}$ in $Q$ is ${c}_{m}$. For any other root $b\ne{}a$,



$$
0=P(b)=(b-a)Q(b).
$$



Equation (R35).

The integers have no zero divisors, and $b-a\ne{}0$, so $Q(b)=0$. By induction, there are at most $d-1$ such other roots. Including $a$ gives at most $d$ roots. $\square{}$

The proof explicitly supplies the needed linear factorisation; no external root-count theorem is assumed.

#### 4.2 Multivariate rectangular grids

**Lemma 4.** Let $R$ be an integer polynomial in $s$ variables with individual degree bounds ${d}_{1},\ldots{},{d}_{s}$. Let ${A}_{i}$ be a set of ${d}_{i}+1$ distinct integers. If $R$ vanishes at every point of ${A}_{1}\times{}\cdots{}\times{}{A}_{s}$, then its coefficient map is zero.

**Proof.** Induct on $s$. For $s=0$, the polynomial is a constant and the empty Cartesian product contains exactly one empty tuple. Vanishing at that tuple says the constant is zero.

For $s>0$, group the coefficients according to the last exponent:



$$
R(Y,T)=\sum\limits_{k=0}^{{d}_{s}} {Q}_{k}(Y){T}^{k}.
$$



Equation (R36).

Fix $Y$ in the product of the first $s-1$ grid factors. The resulting univariate polynomial vanishes at the ${d}_{s}+1$ distinct members of ${A}_{s}$. Lemma 3 implies that it is the zero polynomial, so ${Q}_{k}(Y)=0$ for every $k$. Each coefficient polynomial ${Q}_{k}$ inherits the individual degree bounds in the first $s-1$ coordinates. The induction hypothesis makes its coefficient map zero. Every grouped coefficient of $R$ is therefore zero. $\square{}$

This lemma does not require positive coefficients. It will be applied to an integer difference of two nonnegative coefficient maps. That difference is formed in the metatheoretic proof and does not add a constructor to the expression language.

#### 4.3 Explicit finite grids

For $p={\mathrm{N}\mathrm{F}}_{S}(e)$, $q={\mathrm{N}\mathrm{F}}_{S}(f)$, and each live coordinate $i\in{}S$, define



$$
{d}_{i}(S)=\mathrm{m}\mathrm{a}\mathrm{x}(\{{\alpha{}}_{i}:\alpha{}\in{}\mathrm{s}\mathrm{u}\mathrm{p}\mathrm{p}(p)\cup{}\mathrm{s}\mathrm{u}\mathrm{p}\mathrm{p}(q)\}\cup{}\{0\}).
$$



Equation (R37).

Set



$$
{\mathcal{G}}_{S}(e,f)=\{v\in{}{\mathbb{N}}^{r}:\:{}{v}_{i}=0\ \mathrm{f}\mathrm{o}\mathrm{r}\ i\notin{}S,\quad{}1\le{}{v}_{i}\le{}{d}_{i}(S)+1\ \mathrm{f}\mathrm{o}\mathrm{r}\ i\in{}S\},
$$



Equation (R38),

and take the union over all masks:



$$
\mathcal{G}(e,f)=\underset{S\subseteq{}\{0,\ldots{},r-1\}}{\bigcup{}}{\mathcal{G}}_{S}(e,f).
$$



Equation (R39).

This union is computable and finite. Every factor contains at least one element. Since different masks give disjoint tuples, its cardinality is exactly



$$
|\mathcal{G}(e,f)|=\sum\limits_{S\subseteq{}\{0,\ldots{},r-1\}} \prod\limits_{i\in{}S} ({d}_{i}(S)+1).
$$



Equation (R40).

An empty product is one. The all-zero mask always contributes the zero tuple. At arity zero, the whole union is the singleton containing the empty tuple. The zero polynomial has degree bound zero by Equation (R37); a live coordinate of degree zero still receives the one test value $1$.

**Lemma 5 (effective separation).** If $p\ne{}q$ for some mask $S$, then some $v\in{}{\mathcal{G}}_{S}(e,f)$ satisfies $[\![e]\!](v)\ne{}[\![f]\!](v)$.

**Proof.** Delete the dead exponent coordinates from $p$ and $q$. Because both maps are $S$-normal, deletion is injective on their supports and on coefficient maps. Embed the natural coefficients in $\mathbb{Z}$ and subtract. Since $p\ne{}q$, the resulting integer polynomial $R$ is nonzero. Its individual degrees are bounded by the values ${d}_{i}(S)$.

If the two map evaluations agreed on the whole grid, $R$ would vanish on a product of ${d}_{i}(S)+1$ distinct positive integers in each live coordinate. Lemma 4 would make its coefficient map zero, a contradiction. Some grid tuple therefore separates the map evaluations. Lemma 2 identifies those evaluations with the two expression values. $\square{}$

The lemma is algorithmic: enumerate the finite grid lexicographically and directly evaluate both expressions until a mismatch appears. The proof guarantees success when the maps differ. It does not invoke unbounded search.

Condition 2 implies Condition 3 of Theorem A by contraposition using Lemma 5. Condition 3 implies equality at every tuple by Lemma 2. Conditions 3 and 4 are equivalent by Lemmas 2 and 5. This establishes all the algebraic equivalences in the theorem.

An explicit uniform coordinate bound for the fragment is



$$
B(e,f)=\mathrm{m}\mathrm{a}\mathrm{x}(\{{d}_{i}(S)+1:\:{}S\ \mathrm{i}\mathrm{s}\ \mathrm{a}\ \mathrm{m}\mathrm{a}\mathrm{s}\mathrm{k},\:{}i\in{}S\}\cup{}\{0\}).
$$



Equation (R41).

If the pair is unequal, a distinguishing tuple exists with every coordinate between $0$ and $B(e,f)$. At $r=0$, the coordinate assertion is vacuous and the unique empty tuple distinguishes unequal constants. This is a computable bound relative to the fragment and is consistent with the impossibility of such a bound on the entire Boolean and primitive-recursive domain.

### 5 Exact finite certificate algorithms

#### 5.1 Input and endpoint binding

An instance is a finite encoding of $(r,e,f)$. Validate that $r$ is a natural number and that every expression node has an allowed tag, the required child count, a natural constant where required, and a variable index strictly less than $r$ where required. Reject malformed or out-of-fragment inputs. Both expressions use the same arity. The compiled endpoints are defined by these descriptions and the compiler in Section 2.

For a claim about separately supplied raw polynomial codes $p,q$, first compute ${p}_{e},{p}_{f}$ and require literal code equality:



$$
p={p}_{e},\quad{}\quad{}q={p}_{f}.
$$



Equation (R42).

One may additionally supply current typing derivation trees and validate them against $\mathrm{H}\mathrm{a}\mathrm{s}\:{}[]\:{}p\:{}{C}_{r}$ and $\mathrm{H}\mathrm{a}\mathrm{s}\:{}[]\:{}q\:{}{C}_{r}$. Such trees exist by Section 2. They neither enlarge the fragment nor establish identity inhabitation. The Python checker uses only the expression-presented interface; it does not implement a serialised P01AC endpoint parser or a parser for $\mathrm{H}\mathrm{a}\mathrm{s}$ derivation trees.

A consumer must bind the certificate’s stored instance $(r,e,f)$ to the actual claim being checked. A valid certificate about different expressions proves nothing about an external pair.

#### 5.2 Positive coefficient certificates

A positive certificate stores $(r,e,f)$ and a table with exactly one row for each of the ${2}^{r}$ Boolean masks, in lexicographic order. Each row contains the mask and two proposed sorted coefficient lists.

The verifier performs these finite checks:

1. Validate the instance and the exact certificate schema.

2. Enumerate all masks itself, so that no omitted zero case or duplicate row can conceal an inequality.

3. Compute ${\mathrm{N}\mathrm{F}}_{S}(e)$ and ${\mathrm{N}\mathrm{F}}_{S}(f)$ for every mask by Section 3.

4. Require each claimed list to equal the recomputed canonical list exactly, including positive coefficients, distinct sorted exponents, and the full arity of every exponent vector.

5. Require the two maps to coincide in every row.

6. Accept exactly when all checks pass.

This is a total finite algorithm in the standard unbounded-memory model of computation. Expression recursion, finite map operations, and enumeration of all ${2}^{r}$ masks terminate. This is not an efficiency claim: coefficient growth, expansion, and the number of masks may be large. All stored arithmetic data are finite natural integers.

**Soundness.** Acceptance implies genuine equality of both normal forms for every mask. Lemma 2 gives numerical equality everywhere. The kernel-checked source bridge then gives ${V}_{r}(e,f)$ and the original semantic identity conditions.

**Completeness.** If ${V}_{r}(e,f)$ holds, the bridge gives numerical equality everywhere. Lemma 5 rules out unequal coefficient maps on any mask. The finite table of actual normal forms therefore passes every verifier check. An accepted positive certificate exists exactly for the valid fragment identities.

The certificate table is redundant in the precise sense that the verifier can recompute it. This provides an explicit finite, independently replayable certificate without an oracle or an unchecked normal-form claim. Both the certificate producer and the abstract checker terminate on the declared syntax. A decision procedure can omit the table and compare the computed maps directly.

#### 5.3 Finite evaluation certificates and negative evidence

An alternative positive verifier recomputes the maps only to obtain degree bounds, enumerates the complete union $\mathcal{G}(e,f)$, and directly evaluates $e$ and $f$ at every tuple, requiring equality everywhere. A finite grid table with expression-evaluation traces may record the computation. All values and traces can be checked by syntax-directed arithmetic. Lemma 5 proves completeness of this finite testing scheme. The Python reference producer and positive checker use the coefficient-table scheme; its grid and distinguish procedures implement finite separation search.

For an unequal well-formed pair, return a finite tuple $v$ and its two different computed natural outputs. A negative verifier checks $v\in{}{\mathbb{N}}^{r}$ and recomputes the outputs. This is sound by the semantic bridge and complete because Lemma 5 supplies a grid witness. The positive-grid bound is unnecessary for validating a supplied negative witness; its purpose is effective discovery.

For an additional layer of raw-conversion evidence, fully apply the two compiled endpoints to the canonical tuple and observe both outputs at the fixed inert iterator markers. Adequacy yields finite conversion trees to



$$
\mathrm{i}\mathrm{t}\mathrm{e}\mathrm{r}\mathrm{a}\mathrm{t}\mathrm{e}(\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o},[\![e]\!](v),\mathrm{o}\mathrm{n}\mathrm{e})\quad{}\mathrm{a}\mathrm{n}\mathrm{d}\quad{}\mathrm{i}\mathrm{t}\mathrm{e}\mathrm{r}\mathrm{a}\mathrm{t}\mathrm{e}(\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o},[\![f]\!](v),\mathrm{o}\mathrm{n}\mathrm{e}).
$$



Equation (R43).

Unequal indices give distinct normal forms by the marker-injectivity theorem. This optional conversion-tree encoding is not implemented by the Python checker and is unnecessary for the fragment theorem. No termination claim for arbitrary reduction strategies is needed.

Negative-witness generation is implemented. The negative verifier just specified is an abstract algorithm, rather than a separate command of the reference interface. That interface provides decide, certify, and verify; verify checks positive certificates. Independent tests validate generated negative tuples using an independent direct evaluator.

#### 5.4 Reference implementation and trust boundary

The standard-library-only Python reference implementation uses array encodings with the tags c, v, add, mul, and if0. The respective node layouts are \["c", n\], \["v", i\], \["add", e, f\], \["mul", e, f\], and \["if0", t, e, f\].

A coefficient entry stores an exponent vector followed by a positive coefficient. Lists are sorted lexicographically by exponent vector; zero is the empty list. The implementation rejects Boolean values where natural integers are required and compares certificate structures with type-sensitive equality. Its arity-zero decision procedure distinguishes an actual empty-tuple counterexample from the absence of a counterexample.

All branches must be validated as grammar, including an unselected branch of a conditional. Internal helpers such as grid and eval\_poly assume canonical well-formed maps produced by the validated pipeline; they are not separately hardened parsers for arbitrary external map objects.

Tests cover distributivity, genuinely mask-dependent conditionals, nested tests, zero factors, positive-orthant zero tests, degree-bound regressions, all-zero masks, empty polynomial maps, arity zero, malformed and out-of-fragment input, tampered coefficients, missing and duplicate masks, modified endpoints, unsorted coefficients, and randomised comparisons with direct evaluation. These tests are evidence about the implementation and do not replace the general proof.

The Python normaliser and its strict JSON interface remain a reference implementation, not Lean-extracted or formally refined code. A separate Lean implementation proves coefficient-decision and typed-certificate soundness and completeness, as described in Section 7. Its certificate representation differs from the strict canonical tables specified here. The explicit finite-grid theorem and grid-search implementation remain at their written-proof and reference-code boundary. Practical integer, stack, parser, and memory limits may prevent completion; such failures are not mathematical inequality verdicts. No efficiency or adversarial-service availability guarantee is claimed.

### 6 Examples and boundaries

#### 6.1 A genuinely piecewise identity

At arity two, let



$$
e=\mathrm{i}\mathrm{f}\:{}{x}_{0}+{x}_{1}=0\:{}\mathrm{t}\mathrm{h}\mathrm{e}\mathrm{n}\:{}7\:{}\mathrm{e}\mathrm{l}\mathrm{s}\mathrm{e}\:{}({x}_{0}+1)({x}_{1}+1),
$$



Equation (R44),

and



$$
\begin{gathered}f=\kern0pt{}\mathrm{i}\mathrm{f}\:{}{x}_{0}=0 \\ \mathrm{t}\mathrm{h}\mathrm{e}\mathrm{n}\:{}(\mathrm{i}\mathrm{f}\:{}{x}_{1}=0\:{}\mathrm{t}\mathrm{h}\mathrm{e}\mathrm{n}\:{}7\:{}\mathrm{e}\mathrm{l}\mathrm{s}\mathrm{e}\:{}{x}_{1}+1) \\ \mathrm{e}\mathrm{l}\mathrm{s}\mathrm{e}\:{}{x}_{0}{x}_{1}+{x}_{0}+{x}_{1}+1.\end{gathered}
$$



Equation (R45).

Their common normal-form table has four rows:

- Neither coordinate positive: the constant $7$.

- Only ${x}_{1}$ positive: ${x}_{1}+1$.

- Only ${x}_{0}$ positive: ${x}_{0}+1$.

- Both coordinates positive: ${x}_{0}{x}_{1}+{x}_{0}+{x}_{1}+1$.

This is a finite fragment certificate for actual current-typed P01AC endpoints, rather than merely an example of raw syntax equality. Its all-zero branch also shows why zero masks cannot be discarded and why a single global polynomial normal form is insufficient.

#### 6.2 A distinguishing input regression

The one-variable expressions $x$ and ${x}^{2}$ agree at zero and one but are unequal. Here $x$ denotes ${x}_{0}$, and the square abbreviates multiplication in the expression grammar. The positive mask has degree bound two, so its prescribed grid is $\{1,2,3\}$. The procedure finds the witness $2$. A fixed testing budget or an erroneous $d$-point grid would not have the theorem’s guarantee.

#### 6.3 Scope exclusions

No result is asserted for arbitrary current-$\mathrm{H}\mathrm{a}\mathrm{s}$ endpoints, arbitrary primitive-recursive descriptions, nonnegative functions presented with subtraction, arbitrary equality tests between positive expressions, or higher-order input types. There is no procedure here for deciding whether an arbitrary endpoint happens extensionally to coincide with a fragment expression. Raw conversion completeness, current syntactic identity completeness, and contextual-equivalence correspondence do not follow.

The global Boolean theorem rules out a sound and complete recursively enumerable positive certificate system on its whole annotated domain, while allowing separately declared restricted families. The present language has only finitely many zero/nonzero branch cells and a computable polynomial degree bound on each cell. These structural facts make positive completeness possible.

### 7 Kernel checked decision and certificate procedures

#### 7.1 Exact semantic completeness

The additional Lean development supplies an executable Boolean function identityCheck on the same typed expression grammar. For every finite arity and every pair of expressions, it proves



$$
\mathrm{i}\mathrm{d}\mathrm{e}\mathrm{n}\mathrm{t}\mathrm{i}\mathrm{t}\mathrm{y}\mathrm{C}\mathrm{h}\mathrm{e}\mathrm{c}\mathrm{k}(e,f)=\mathsf{t}\mathsf{r}\mathsf{u}\mathsf{e}\quad{}\Leftrightarrow{}\quad{}{V}_{r}(e,f).
$$



Equation (R46).

The declaration P01AC.RestrictedIdentityV2.identityCheck\_iff\_fragmentValid has no extra polynomial-injectivity, completeness, separation, or endpoint-membership premise. It composes the coefficient procedure with the unchanged source-specific compiler bridge from Section 2. The corresponding original unary identity, relational identity, and semantic polynomial-witness equivalences are checked as well. All semantic arrows still quantify over independently related arguments, and the canonical application order remains the explicitly stated reversed coordinate order.

The same development defines a typed finite-certificate verifier and proves



$$
(\exists{}c:\mathrm{C}\mathrm{e}\mathrm{r}\mathrm{t}\mathrm{i}\mathrm{f}\mathrm{i}\mathrm{c}\mathrm{a}\mathrm{t}\mathrm{e}(r),\quad{}\mathrm{v}\mathrm{e}\mathrm{r}\mathrm{i}\mathrm{f}\mathrm{y}\mathrm{C}\mathrm{e}\mathrm{r}\mathrm{t}\mathrm{i}\mathrm{f}\mathrm{i}\mathrm{c}\mathrm{a}\mathrm{t}\mathrm{e}(e,f,c)=\mathsf{t}\mathsf{r}\mathsf{u}\mathsf{e})\quad{}\Leftrightarrow{}\quad{}{V}_{r}(e,f).
$$



Equation (R47).

Here the expressions are explicit verifier arguments. The computable producer makeCertificate e supplies an accepted certificate whenever the expressions are semantically equal. The definition fragmentIdentityDecidable e f selects its proof-carrying result by running the Boolean checker, rather than using a classical decision procedure for the semantic proposition.

Equations (R46) and (R47) are full kernel-checked semantic completeness results for these Lean definitions. They do not assert a current typing derivation of the identity type, recognise arbitrary P01AC endpoints as fragment expressions, or verify a wire-format parser. They also do not formalise every equivalence in Theorem A: its explicit degree-bounded grid and its strict reference-packet presentation keep their separately stated boundaries.

#### 7.2 Executable sparse representation and masks

The executable implementation represents an exponent by a finite coordinate function and a polynomial by a finite list of exponent/coefficient pairs. Explicit recursion over the coordinate count decides equality of exponent tuples and masks, including the empty tuple. No classical function-equality oracle is used in the computation.

The sparse lists are representatives of coefficient maps, rather than the sorted canonical lists required by the Python format. Duplicate monomials are permitted and their natural coefficients are added. Zero-coefficient entries are permitted. coeffEqual compares aggregate coefficients at every exponent occurring in either input list. The proof that every other coefficient is zero makes this finite comparison sound and complete for polynomial equality.

Concatenation represents addition, and finite convolution represents multiplication. The executable zero test checks that every stored coefficient is zero; it does not test list emptiness. This distinction matters because a zero constant can be represented by a nonempty list containing a zero entry. Nonnegative coefficients and strictly positive variable values ensure that zero evaluation is equivalent to this zero test, without any cancellation assumption.

The normaliser substitutes zero for dead variables. Its proved adequacy evaluates the resulting polynomial on an arbitrary all-positive auxiliary tuple and evaluates the original expression on the corresponding masked tuple. A separate support theorem shows that dead-coordinate exponents are zero. Every natural input is represented by its exact zero/nonzero mask and an auxiliary tuple obtained by replacing only zero entries with one. Thus all cells, missing variables and arity zero are covered.

The completeness direction uses a proved positive-evaluation injectivity lemma. It embeds natural coefficients in the integers, establishes infinitely many distinct positive-natural roots for each required univariate polynomial, and inducts over the finite variable count. Evaluation of polynomial coefficients reduces the inductive step to the univariate infinite-root theorem. Injectivity of the coefficient embedding returns equality over the naturals. All ring, domain, map and positivity hypotheses are discharged. In particular, ordinary polynomial function extensionality over an infinite ring is not incorrectly applied directly to natural coefficients or to a single positive point.

The polynomial interpretation used in these correctness proofs is noncomputable library mathematics. It is absent from the executable checker, certificate producer and verifier. The runtime procedures operate on finite lists and explicit finite coordinate comparisons.

#### 7.3 Typed certificates and the reference interface

A Lean certificate is a finite list of mask labels and proposed common sparse maps. The verifier enumerates every mask itself and requires a correctly labelled row whose aggregate coefficient map equals both recomputed forms. A missing required mask cannot be hidden by duplicating another row. Extra rows, repeated rows, reordered rows, split coefficients and zero entries are harmless when every required matching row exists.

This is a different typed certificate representation from the strict canonical JSON table of Section 5. The two implementations express sound and complete methods for the same declared semantic problem, but no formal parser or implementation-refinement theorem connects their serialised inputs. Natural constants and valid variable indices in the Lean interface are enforced by its types. External P01AC claims still require the literal endpoint binding in Equation (R42).

The implementation does not rely on the finite degree-plus-one grid to decide equality. Its kernel-checked completeness uses positive-tuple polynomial injectivity. Consequently the explicit grid bound and bounded negative-witness generator remain written mathematics and reference code; the stronger coefficient-checker theorem does not silently upgrade them.

#### 7.4 Independent verification of the Lean checker

The independent final replay freshly compiled the exact restricted compiler bridge, the unchanged primitive-recursion compiler module, and all seven new mathematical, control and audit modules under Lean 4.19.0. The type-and-value dependency audit checked 140 safe roots, 93 namespace theorems including generated declarations, and 9,175 reachable checked declarations. Its only axioms were propext, Quot.sound and Classical.choice; no admitted theorem, custom axiom, unsafe proof dependency or partial proof dependency was accepted. The 105 reported nonproof runtime auxiliaries were kept separate from proof roots.

A separate computational-root audit checked 460 declarations reachable from identityCheck, verifyCertificate and makeCertificate. It found no classical-choice dependency, classical proposition or equality decider, noncomputable polynomial interpretation, unsafe dependency or partial dependency. Correctness proofs may use classical mathematics, but that mathematics does not select the runtime result.

All 36 independent examples and interfaces passed, including 33 kernel-reduced concrete cases and three generic interfaces. Executed controls exercised equal and unequal pairs, certificate production, acceptable redundant representations, forged certificates and the false branch of the proof-carrying decision wrapper. Nine supplied and seven independent negative controls were rejected with their intended diagnostics. These included insufficient single-point equality, omitted positivity, duplicate-mask noncoverage, changed external endpoints, forged dead-variable exponents, a custom axiom and an admitted proof.

The replay used the pinned Mathlib revision c44e0c8ee63ca166450922a373c7409c5d26b00b and its exact subsidiary revisions. Selective official compiled caches were acquired; the work does not claim a fresh build of every external dependency. The inherited source, earlier compiler bridge and Python reference artifacts were preserved. These checks establish the stated Lean procedure and proof boundary, not canonical adoption or historical priority.

### 8 Earlier compiler and reference implementation checks

The following checks concern the earlier compiler bridge and strict Python reference implementation. They remain valid historical evidence; the later Lean checker above has its own representation and verification record.

The source-specific Lean verification checks compilation, current typing, arbitrary-observation adequacy, currying, the exact original $F$ and $G$ semantic equivalences, semantic-witness equivalence, and identity formation. The numerical Lean statement uses assignments $\mathbb{N}\to{}\mathbb{N}$; bounded variables and the dependence-only-on-used-coordinates theorem ensure that only the first $r$ coordinates matter, matching the finite-tuple formulation here.

An independent replay used Lean 4.19.0, commit 6caaee842e94. It freshly compiled the primitive-recursive compiler module, the restricted compiler bridge, and the restricted kernel audit. It also freshly compiled the inherited kernel auditor and reran the restricted audit against it. Independent interface checks covered arbitrary independently related lists, current endpoint typing, original $F$ and $G$ identity statements, branch coordinates, reversal, unused coordinates, and arity zero.

The type-and-value dependency-closure audit checked 138 safe roots, 79 namespace theorems including generated declarations, and 2,337 reachable declarations. The only axioms were propositional extensionality (propext), quotient soundness (Quot.sound), and classical choice (Classical.choice). No admitted proof, new mathematical axiom, unsafe proof dependency, or partial proof dependency was found. The audit separately excluded 71 compiler-generated unsafe or partial runtime auxiliaries from proof roots; it does not assert that such runtime auxiliaries do not exist. The replay recorded inherited compiled dependencies without claiming that every inherited module was rebuilt.

All seven supplied negative Lean controls were rejected with the expected diagnostic. Five additional independent negative controls rejected reversed coordinate order, omitted natural endpoint uniformity, a swapped zero branch, a custom axiom, and an admitted proof. Positive controls passed.

All ten reference test methods and all twelve independent test methods passed. Independent tests included 5,100 normalisation comparisons with an independently written direct evaluator over arities zero through three; 40 coefficient-list forgeries; 33 schema and mask mutations; malformed unselected branches; and arbitrary admissible mask-table reification. The forgeries included zero and negative coefficients, duplicate or reordered monomials, Boolean, floating-point, and string scalar confusion, incorrect exponent lengths, negative exponents, and dead-variable support. Schema tests included missing or extra fields, incorrect version and arity types, missing, duplicate, or reordered mask rows, non-Boolean or wrong-length masks, and malformed row data.

The separation tests included sharp univariate regressions for $d=1,\ldots{},7$. Splitting the signed coefficients of $\prod\limits_{j=1}^{d} (X-j)$ into two nonnegative source expressions gives equality at the first $d$ positive points and a first positive witness at $d+1$. A sharp three-coordinate case used degree bounds $(2,0,3)$: the absent middle variable still required a singleton live-coordinate factor, giving a $3\times{}1\times{}4$ all-live grid that separated only at $(3,1,4)$. Global mask enumeration found $(3,0,4)$ earlier. Additional tests covered empty maps, absent variables, all-zero inputs, degree-zero live coordinates, and the distinction between an empty-tuple counterexample and no counterexample.

These earlier checks support the strict reference implementation and source-specific semantic bridge at their stated scopes; they are not the evidence for the later kernel-checked Lean checker. Sections 3 and 4 give the complete elementary written algebraic arguments independently of tests. Section 7 states the additional checked procedure and its actual library dependencies. No exhaustive novelty claim, extension to arbitrary typed endpoints, or formal refinement of the Python implementation follows.

Paper 5

## Polynomial Equality Tests and the Boundary of Effective Semantic Identity Completeness

Adding a single root equality test between two pure natural-number polynomials suffices to make equality with zero Π₁-complete. The test has literal branches 1 and 0. Its arguments contain only natural constants, variables, addition, and multiplication. No nested equality test or user-defined recursion is needed. The result also applies to equality of pairs in the disjoint union of these new root expressions and the existing decidable zero-test fragment.

This chapter gives the complete written complexity argument and its connection to the original P01AC semantic identity relations. It distinguishes the existence proof of a computable reduction from an extracted executable reducer. The finite primitive-recursive comparison descriptions, current endpoint typing, arbitrary-observation adequacy, and original-semantic bridge are kernel-checked. The representation premise, hierarchy argument, coefficient transformations, and impossibility consequences remain written mathematics.

### 1 The source languages and decision problems

Write ℕ₀ for the nonnegative integers. For each finite arity r, retain the expression language Eᵣ of the restricted semantic-identity completeness theorem:



$$
{E}_{r}:\mathop{:=}c\mid{}{x}_{i}\mid{}{E}_{r}+{E}_{r}\mid{}{E}_{r}\cdot{}{E}_{r}\mid{}\mathrm{i}\mathrm{f}\:{}{E}_{r}=0\:{}\mathrm{t}\mathrm{h}\mathrm{e}\mathrm{n}\:{}{E}_{r}\:{}\mathrm{e}\mathrm{l}\mathrm{s}\mathrm{e}\:{}{E}_{r},\quad{}\quad{}c\in{}{\mathbb{N}}_{0},\quad{}0\le{}i<r.
$$



Expressions are finite trees, with the usual total natural-number interpretation. The existing restricted theorem decides equality in this language by a finite table of zero/nonzero input masks and polynomial coefficient maps; its executable coefficient checker is also kernel-checked. Arbitrary polynomial equality tests are absent from Eᵣ.

Define the separate pure arithmetic grammar Aᵣ by



$$
P:\mathop{:=}c\mid{}{x}_{i}\mid{}P+P\mid{}P\cdot{}P,\quad{}\quad{}c\in{}{\mathbb{N}}_{0},\quad{}0\le{}i<r.
$$



Every expression in Aᵣ denotes a polynomial with nonnegative integer coefficients on ℕ₀ʳ. Conversely, every finite coefficient map of this kind has a computably produced Aᵣ expression: expand each monomial into repeated multiplication, multiply by its natural coefficient, and sum the resulting terms. Empty sums denote zero and empty products denote one. Exponents are finite notation for repeated multiplication, rather than a further source constructor.

The extension Rᵣ has exactly two alternatives:



$$
s:\mathop{:=}\mathrm{o}\mathrm{l}\mathrm{d}(e)\quad{}(e\in{}{E}_{r})\quad{}\mid{}\quad{}\mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}(P,Q)\quad{}(P,Q\in{}{A}_{r}).
$$



Its direct interpretation is the old interpretation on old(e), and



$$
[\![\mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}(P,Q)]\!](v)=\{\begin{array}{ll}1 & \mathrm{i}\mathrm{f}\ P(v)=Q(v), \\ 0 & \mathrm{i}\mathrm{f}\ P(v)\ne{}Q(v).\end{array}
$$



There is exactly one new equality test in a test expression, at its root. Its two arguments are pure arithmetic, and its branches are literally 1 and 0. In particular, Rᵣ is a disjoint union, not the closure of Eᵣ under nested equality conditionals. A lower bound for this small union also applies to any effective extension containing it with the same meanings.

An instance of the first problem is a finite code (r,P,Q). A total recursive parser checks its natural constants, finite trees, and variable ranges. Invalid codes are rejected. On valid codes define



$$
\begin{gathered}\mathrm{Z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{T}\mathrm{e}\mathrm{s}\mathrm{t}(r,P,Q)\Leftrightarrow{}\forall{}v\in{}{\mathbb{N}}_{0}^{r},\quad{}[\![\mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}(P,Q)]\!](v)=0 \\ \Leftrightarrow{}\forall{}v\in{}{\mathbb{N}}_{0}^{r},\quad{}P(v)\ne{}Q(v).\end{gathered}
$$



Thus a positive ZeroTest instance says that the equality test never succeeds. Equivalently, the integer polynomial P−Q has no nonnegative zero. This is different from universal polynomial identity, which asks whether P(v)=Q(v) for every v. Universal identity for pure arithmetic expressions is decidable by the existing coefficient-comparison theorem, since Aᵣ is contained in Eᵣ. Neither that decision procedure nor polynomial identity testing decides whether P and Q coincide at some input.

The second problem has valid inputs (r,s,t), where s,t∈Rᵣ, and asks whether their direct values agree at every input. When P01AC endpoints are included, they are the literal results of the compiler defined below; an externally supplied endpoint must be checked for literal equality to that compilation. The problems are source-presented, rather than problems of recognizing arbitrary typed P01AC endpoints.

**Theorem 1.** With arity included in the input, ZeroTest is Π₁-complete under total computable many-one reductions. Its complement is Σ₁-complete.

**Theorem 2.** With arity included in the input, universal equality of pairs of Rᵣ expressions is Π₁-complete. The same classifications hold for the corresponding original P01AC semantic equality and identity interfaces in Section 7.

Some fixed finite arity already supports the hardness reduction, and every greater arity does so by unused-variable padding. The proof does not specify that arity or show hardness at every positive arity. At arity zero both decision problems are decidable by evaluation at the unique empty tuple.

### 2 Imported premise

For every recursively enumerable set A ⊆ ℕ₀, there are a finite m and an integer-coefficient polynomial H(a,y₁,…,yₘ) such that a ∈ A exactly when H(a,y)=0 for some y ∈ ℕ₀ᵐ. Matiyasevich–Robinson’s §§1–3, equation (3), state this established representation premise; their variable convention includes zero. This citation supplies existence, not an extracted uniform procedure transforming machine codes into polynomials. Their later paper witnesses the premise; the original DPRM proof is not reverified here. No numerical witness bound or three-quantifier theorem is imported.

Reference: Yuri Matiyasevich and Julia Robinson, *Two universal 3-quantifier representations of recursively enumerable sets*, original article (1974), author-submitted corrected English translation, arXiv:0802.1052v1 (2008), PDF pages 1–2, Sections 1–3, equation (3). [Article record](<https://arxiv.org/abs/0802.1052>). [Primary text](<https://arxiv.org/pdf/0802.1052>).

### 3 The upper bounds

For valid (r,P,Q), evaluation at any supplied finite natural tuple terminates by recursion on the expression trees. For b∈ℕ₀, let T(r,P,Q,b) assert that the syntax is valid and that P(v)≠Q(v) at every tuple in the finite box {0,…,b}ʳ. This predicate is total recursive: validation is decidable, the box is finite, and every evaluation terminates.

Every tuple belongs to some finite box. Consequently,



$$
\mathrm{Z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{T}\mathrm{e}\mathrm{s}\mathrm{t}(r,P,Q)\Leftrightarrow{}\forall{}b\in{}{\mathbb{N}}_{0},\quad{}T(r,P,Q,b).
$$



Invalid syntax makes T false for every b, so this is a Π₁ definition over all code strings. At r=0 the box consists of the single empty tuple. It is not empty, and the constant comparison is actually performed.

A valid negative instance has a finite certificate: one tuple v such that P(v)=Q(v). Its validity can be checked recursively. Invalid syntax instead has a finite parser rejection. Enumerating boxes therefore semidecides every negative instance. This establishes the Σ₁ upper bound for the complement.

For universal equality of two Rᵣ expressions, validate the common arity and compare their direct values on each finite box. Both alternatives in the grammar have terminating evaluation. The same universal-bound argument gives a Π₁ upper bound, and a differing tuple is a recursively checkable negative certificate. No general type inference or recognition of a compiler image is used.

### 4 The lower bound

#### 4.1 The fixed halting source

Use the effective binary-machine indexing of the Boolean semantic-identity theorem. Let K⊆ℕ₀ be its blank-input halting set. Simulation enumerates K. The completeness argument for this particular indexing can be recalled explicitly.

A finite-alphabet deterministic machine is translated effectively to binary tape by encoding symbols in fixed-width blocks, with the blank symbol encoded by the all-zero block. Finitely many control states record the source state, block phase, and finite information already read. Finite routines read a block, implement its transition, rewrite it, and move to the next block origin. Invalid block patterns can receive fixed default transitions, since correctly encoded computations never reach them. A stationary move can be replaced by a right/left pair through an intermediate state that preserves the visited cell. Renaming the start and halt states and encoding the resulting finite transition table are effective operations in the fixed indexing.

Now let B be any Π₁ set. Choose a total recursive predicate R with



$$
k\in{}B\Leftrightarrow{}\forall{}n\in{}{\mathbb{N}}_{0},\quad{}R(k,n).
$$



Construct a machine which tests R(k,0), R(k,1), and so on, halting at the first false value. Each test terminates. A finite initialisation routine generated from k writes that parameter, and the preceding compilation translates the machine into the fixed binary model. Its index e(k) is computable and satisfies



$$
k\in{}B\Leftrightarrow{}e(k)\notin{}K.
$$



Conversely, nonhalting is the assertion that no finite simulation stage halts, a universal statement with a total recursive matrix. Thus ℕ₀∖K is Π₁-complete.

Apply Section 2 once to this fixed set K. Fix a representing polynomial H and its finite number m of witness coordinates. H is fixed before the machine index e varies. Its coefficients and exponent vectors are fixed finite integers.

#### 4.2 Splitting the coefficients

Write the finite expansion of H as



$$
H(a,y)=\sum\limits_{(j,\alpha{})} {c}_{j,\alpha{}}\,{}{a}^{j}{y}^{\alpha{}},\quad{}\quad{}{c}_{j,\alpha{}}\in{}\mathbb{Z},\quad{}j\in{}{\mathbb{N}}_{0},\quad{}\alpha{}\in{}{\mathbb{N}}_{0}^{m}.
$$



Duplicate monomials are first aggregated by finite integer arithmetic if necessary. For every coefficient put



$$
{c}^{+}=\mathrm{m}\mathrm{a}\mathrm{x}(c,0),\quad{}\quad{}{c}^{-}=\mathrm{m}\mathrm{a}\mathrm{x}(-c,0),
$$



and define



$$
{H}^{+}(a,y)=\sum\limits_{(j,\alpha{})} {c}_{j,\alpha{}}^{+}\,{}{a}^{j}{y}^{\alpha{}},\quad{}\quad{}{H}^{-}(a,y)=\sum\limits_{(j,\alpha{})} {c}_{j,\alpha{}}^{-}\,{}{a}^{j}{y}^{\alpha{}}.
$$



Both coefficient maps are nonnegative, and H=H⁺−H⁻ as integer polynomials. Hence, at every nonnegative tuple,



$$
H(a,y)=0\Leftrightarrow{}{H}^{+}(a,y)={H}^{-}(a,y).
$$



The equivalence uses ordinary integer equality and the injective embedding ℕ₀→ℤ. It does not identify integer subtraction with truncated natural subtraction. Zero coefficients may be omitted; a side with no remaining monomials is represented by the legal constant zero.

Construct fixed pure-arithmetic trees for H⁺ and H⁻. For each machine index e, substitute its natural numeral for the parameter a, obtaining Pₑ,Qₑ∈Aₘ. The substitution can retain repeated multiplications instead of computing large coefficient values. The map



$$
e\mapsto{}(m,{P}_{e},{Q}_{e})
$$



is total computable: generate a finite numeral and insert it at the parameter occurrences of two fixed trees. Binary natural constants and successor numerals both give effective encodings; in the latter case the algorithm simply emits e successors.

By the fixed representation and coefficient splitting,



$$
\begin{gathered}e\in{}K\Leftrightarrow{}\exists{}y\in{}{\mathbb{N}}_{0}^{m},\quad{}{P}_{e}(y)={Q}_{e}(y) \\ \Leftrightarrow{}[\![\mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}({P}_{e},{Q}_{e})]\!]\ \mathrm{i}\mathrm{s}\ \mathrm{n}\mathrm{o}\mathrm{t}\ \mathrm{i}\mathrm{d}\mathrm{e}\mathrm{n}\mathrm{t}\mathrm{i}\mathrm{c}\mathrm{a}\mathrm{l}\mathrm{l}\mathrm{y}\ \mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}.\end{gathered}
$$



Negation gives the exact reduction polarity:



$$
e\notin{}K\Leftrightarrow{}\mathrm{Z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{T}\mathrm{e}\mathrm{s}\mathrm{t}(m,{P}_{e},{Q}_{e}).
$$



Thus ZeroTest is Π₁-hard. Section 3 proves its Π₁ upper bound, completing Theorem 1; complementing the same reductions gives Σ₁-completeness of the complement. For Theorem 2 take the exact pair



$$
(\mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}({P}_{e},{Q}_{e}),\mathrm{o}\mathrm{l}\mathrm{d}(0)).
$$



The larger pair problem has the upper bound already proved, so it too is Π₁-complete.

#### 4.3 The effectivity of a fixed finite constant

For every finite integer-polynomial code h, splitting and specialisation are total computable uniformly in h and e. Existence of a suitable fixed h therefore entails existence of a total computable many-one reduction in which h is a literal constant. This is an existence proof of a computable map even though the polynomial coefficients are not displayed and no executable halting-to-polynomial generator is supplied.

The proof does not require an algorithm selecting polynomial codes from arbitrary descriptions of enumerable sets. Nor does it propose searching for H by a decidable universal correctness test. Producing a runnable reducer would require supplying and verifying the actual finite polynomial data. The kernel-checked bridge below does not assume a representing polynomial or add a representation axiom.

#### 4.4 What the arity statement says

Since H was fixed before e varied, its witness arity m is fixed. The reduction consequently establishes Π₁-completeness for some one finite arity. If necessary an unused variable may be adjoined so that m≥1; the existence and universal assertions are preserved because ℕ₀ is nonempty. A zero-witness representation for K would in fact decide membership by evaluating H(e), which is impossible, but the padding argument does not depend on that observation.

For any r≥m, pad Pₑ and Qₑ with unused variables. A tuple of length m extends to length r, and the polynomial values ignore the added coordinates. Therefore the same hardness result holds at every r≥m, while the upper bound continues to apply.

No numerical m, minimum arity, or hardness result at every r≥1 follows from this proof. Arity zero has just the empty tuple and is decidable. “One root test” counts the number and placement of new source operations, not the number of input variables.

### 5 Domain normalisation

The main reduction already uses nonnegative variables. The following finite transformations explain separately how positive and integer domains would be handled, without introducing subtraction into Aᵣ.

If witnesses are strictly positive, substitute zᵢ=yᵢ+1. This is a bijection from ℕ₀ᵐ to ℕ₊ᵐ. Substitute into the integer polynomial, expand finitely, and split coefficients as above. This preserves the existence condition over nonnegative witnesses. For a strictly positive parameter, represent the shifted set {e+1:e∈K} and specialize at a=e+1. These are effective finite substitutions.

Conversely, to express nonnegative-witness existence by a test whose inputs are positive, substitute yᵢ=zᵢ−1 into H before expansion and coefficient splitting. The substitution is an integer-polynomial operation performed in the construction. After splitting, both generated arguments contain only natural constants, addition, and multiplication. No subtraction is a source constructor.

For integer witnesses, replace each zᵢ by uᵢ−vᵢ with uᵢ,vᵢ∈ℕ₀. Every integer has such a representation, and every pair gives an integer, so existential satisfiability is preserved in both directions. Finite expansion and coefficient splitting again eliminate subtraction before generating the source expressions. This conversion doubles the witness coordinates of the particular polynomial; it establishes no numerical bound for the polynomial selected in Section 4.

Finally, replacing P,Q by P+1,Q+1 preserves equality and makes both values strictly positive at every input. The hardness result therefore persists under this positivity-of-values requirement. It is not a requirement that every possible monomial have a strictly positive coefficient. Testing only against literal zero remains the original restricted operation and is different from comparing two arbitrary polynomial values.

### 6 Finite compilation and current typing

#### 6.1 The arithmetic descriptions

Use the unchanged finite primitive-recursive description language, with the exact convention



$$
\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}(g,h)(0,\vec{x})=g(\vec{x}),
$$





$$
\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}(g,h)(n+1,\vec{x})=h(n,\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}(g,h)(n,\vec{x}),\vec{x}).
$$



Let Pᵏᵢ be projection i at arity k, with indices starting at zero. Write comp for finite composition and Kᵣ(c) for the natural constant description. The existing descriptions are



$$
{K}_{r}(0)={\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{r},\quad{}\quad{}{K}_{r}(c+1)=\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(\mathrm{s}\mathrm{u}\mathrm{c}\mathrm{c};{K}_{r}(c)),
$$





$$
A=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({P}_{0}^{1},\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(\mathrm{s}\mathrm{u}\mathrm{c}\mathrm{c};{P}_{1}^{3})),
$$





$$
M=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{1},\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(A;{P}_{2}^{3},{P}_{1}^{3})),\quad{}\quad{}Z=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({P}_{0}^{2},{P}_{3}^{4}).
$$



Induction on the recursion coordinate gives A(a,b)=a+b and M(a,b)=a·b. Z(t,a,b) returns a at t=0 and b at t\>0. For Z the step context is exactly (counter, accumulator, zeroBranch, positiveBranch), so projection P⁴₃ selects the positive branch.

Define two further literal descriptions:



$$
D=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{0},{P}_{0}^{2}),\quad{}\quad{}U=\mathrm{p}\mathrm{r}\mathrm{e}\mathrm{c}({P}_{0}^{1},\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(D;{P}_{1}^{3})).
$$



D has arity one. At zero it gives zero; at n+1 its step returns the counter n. Thus D(n)=n−1 for truncated natural subtraction. U has arity two: its base is its second argument b, and each recursion step decrements the accumulator. Induction, including the zero case, gives U(a,b)=b−a, again with truncated subtraction. The order is second argument minus first argument.

Set



$$
\begin{gathered}\mathrm{E}\mathrm{Q}=\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(Z;\;{}\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(A;\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(U;{P}_{0}^{2},{P}_{1}^{2}),\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(U;{P}_{1}^{2},{P}_{0}^{2})), \\ {K}_{2}(1),{\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}}_{2}).\end{gathered}
$$



On (a,b), the first argument to Z is (b−a)+(a−b). It is zero precisely when both truncated differences vanish. That implies a≤b and b≤a, and hence a=b. Conversely, a=b makes both differences zero. Therefore EQ(a,b) is 1 exactly when a=b, and is 0 otherwise, including cases with a zero argument. These are finite descriptions, not an appeal to an unspecified primitive-recursive representability theorem.

Compile constants, variables, sums, and products by their corresponding descriptions K, projection, A, and M. Compile the old zero conditional by composition with Z. For the new root put



$$
T(\mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}(P,Q))=\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}(\mathrm{E}\mathrm{Q};T(P),T(Q)),\quad{}\quad{}T(\mathrm{o}\mathrm{l}\mathrm{d}(e))=T(e).
$$



Structural induction using the EQ computation proves, for every s∈Rᵣ,



$$
\mathrm{d}\mathrm{e}\mathrm{n}\mathrm{o}\mathrm{t}\mathrm{e}(T(s),v)=[\![s]\!](v).
$$



Using primitive recursion to implement these fixed arithmetic operations does not add arbitrary primitive-recursive descriptions or user-defined recursion to the source grammar.

#### 6.2 Closing the compiled body

Retain the P01AC raw applicative calculus, polynomial syntax, current judgement Has, raw conversion relation ≃, and original interpretations F and G of the preceding semantic-identity results. Define



$$
N=\forall{}X.\,{}(X\to{}X)\to{}X\to{}X,\quad{}\quad{}{C}_{0}=N,\quad{}\quad{}{C}_{r+1}=N\to{}{C}_{r}.
$$



Let NatCtx(r) be the context of r copies of N. For s∈Rᵣ set



$$
{b}_{s}=\mathrm{P}\mathrm{R}.\mathrm{c}\mathrm{o}\mathrm{m}\mathrm{p}\mathrm{i}\mathrm{l}\mathrm{e}(T(s)),\quad{}\quad{}{p}_{s}=\mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}\mathrm{M}\mathrm{a}\mathrm{n}\mathrm{y}(r,{b}_{s}).
$$



The unchanged primitive-recursive compiler gives Has(NatCtx(r),bₛ,N). Repeated current bracket-abstraction introductions give



$$
\mathrm{H}\mathrm{a}\mathrm{s}([],{p}_{s},{C}_{r}).
$$



The branch values 0 and 1 are represented at the Church-natural codomain N. They are not cast to the distinct Church-Boolean type. The derivations use the current P01AC rules and actual terms, with no inverse System F translation or arbitrary raw-term cast.

Closing reverses the de Bruijn coordinates. An assignment (v₀,…,vᵣ₋₁) is applied in the order of canonical raw Church numerals u(vᵣ₋₁),…,u(v₀). For a list xs in application order, let Apply(t,xs) successively apply its elements, and let Extend(η,xs) successively prepend them to the environment. Then the applied-closure equation is



$$
\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}(\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(\mathrm{c}\mathrm{l}\mathrm{o}\mathrm{s}\mathrm{e}\mathrm{M}\mathrm{a}\mathrm{n}\mathrm{y}(|xs|,b),\eta{}),xs)\simeq{}\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(b,\mathrm{E}\mathrm{x}\mathrm{t}\mathrm{e}\mathrm{n}\mathrm{d}(\eta{},xs)).
$$



It follows by induction from applied bracket-abstraction beta. Extend reverses the application list into the environment coordinates. For an empty list the equation is reflexive.

#### 6.3 Adequacy for arbitrary raw observations

The natural observation predicate is



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(t,n)\Leftrightarrow{}\forall{}\ \mathrm{r}\mathrm{a}\mathrm{w}\ a,b,\quad{}t\,{}a\,{}b\simeq{}\mathrm{i}\mathrm{t}\mathrm{e}\mathrm{r}\mathrm{a}\mathrm{t}\mathrm{e}(a,n,b).
$$



Put Sₛ=eval(pₛ,zeroEnv). The existing compiler adequacy theorem applies to arbitrary raw inputs carrying NatObs indices. Combining it with the denotation and closure equations gives: if \|xs\|=r and



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(\mathrm{E}\mathrm{x}\mathrm{t}\mathrm{e}\mathrm{n}\mathrm{d}(\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},xs)(i),{v}_{i})\quad{}\mathrm{f}\mathrm{o}\mathrm{r}\ \mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\mathrm{y}\ i<r,
$$



then



$$
\mathrm{N}\mathrm{a}\mathrm{t}\mathrm{O}\mathrm{b}\mathrm{s}(\mathrm{A}\mathrm{p}\mathrm{p}\mathrm{l}\mathrm{y}({S}_{s},xs),[\![s]\!](v)).
$$



This retains arbitrary raw representatives of the input observations. At r=0 the input list is empty, the input-observation premise is vacuous, and the output observation is still a substantive statement. No eta conversion of unapplied programs is inferred.

### 7 The original semantic identity interfaces

#### 7.1 Numerical equality and the original relation

A unary type environment ρ assigns partial equivalence relations to type parameters. The original nondependent arrow clause quantifies over independently related arguments. Iterating it gives a curried-list characterization: F(Cᵣ,ρ,zeroEnv,t,u) holds precisely when every pair of length-r lists xs,ys, related coordinatewise at N, produces outputs Apply(t,xs), Apply(u,ys) related at N. At r=0 both lists are empty, so the characterization is the original relation at N itself.

Define



$$
{V}_{r}(s,t)\Leftrightarrow{}\forall{}\ \mathrm{u}\mathrm{n}\mathrm{a}\mathrm{r}\mathrm{y}\ \rho{},\quad{}F({C}_{r},\rho{},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},{S}_{s},{S}_{t}).
$$



The natural standardness theorems supply three facts for the original semantics. Every self-related inhabitant of N has a unique NatObs index. Related inhabitants have the same index. Two separately self-related inhabitants with the same index are related. The self-relatedness hypotheses in the third fact are essential: an observation by itself does not supply the endpoint uniformity conditions of the original universal-type interpretation.

Suppose Vᵣ(s,t). Fix a numerical tuple v and apply the curried-list characterization to the same reversed canonical tuple on each side. Canonical numeral membership makes the input lists related. The adequacy theorem provides output indices ⟦s⟧(v) and ⟦t⟧(v). Related natural outputs have equal indices, so the direct values agree.

Conversely, suppose the direct values agree at every numerical tuple. Fix any unary environment and any independently related input lists xs,ys of length r. Standardness gives a common natural index for each related pair. Reverse these indices to obtain a numerical assignment v satisfying the adequacy premises for both lists. Current soundness of the two closed endpoint typings supplies each output’s separate self-relatedness after application to its respective self-related input list. Adequacy and numerical equality give the outputs the same index. The same-index converse, with both self-relatedness hypotheses retained, gives their cross-relation at N. The curried-list characterization now yields the original relation at Cᵣ. Thus



$$
{V}_{r}(s,t)\Leftrightarrow{}\forall{}v\in{}{\mathbb{N}}_{0}^{r},\quad{}[\![s]\!](v)=[\![t]\!](v).
$$



The formal denotations are written on total assignments ℕ₀→ℕ₀. Their checked congruence theorems show that they depend only on coordinates below r, so restriction and extension identify this statement exactly with the finite-tuple version. This is a theorem proved for the new grammar; it does not apply the restricted Eᵣ theorem to an expression outside that grammar.

#### 7.2 Unary and relational identity

Let I be the raw identity combinator and let the identity type be Id(Cᵣ,pₛ,pₜ). Its original unary clause at proof I consists of endpoint F equality and two reflexive conversions of I. Consequently Vᵣ(s,t) is equivalent to



$$
\forall{}\rho{},\quad{}F(\mathrm{I}\mathrm{d}({C}_{r},{p}_{s},{p}_{t}),\rho{},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},I,I).
$$



A relational environment ℛ has induced left and right unary environments. The original G identity clause requires the endpoint F equality in both of them, together with the reflexive proof conversions. Universal Vᵣ supplies both endpoint equalities for every ℛ. Conversely, a diagonal relational environment constructed from an arbitrary unary environment recovers Vᵣ. Therefore it is also equivalent to



$$
\forall{}\mathcal{R},\quad{}G(\mathrm{I}\mathrm{d}({C}_{r},{p}_{s},{p}_{t}),\mathcal{R},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},I,I).
$$



If a uniform semantic polynomial identity witness exists, projecting its identity clause in diagonal environments recovers endpoint equality. If endpoint equality holds universally, the polynomial atom I is a uniform witness. Thus the same conditions are equivalent to



$$
\exists{}w\in{}\mathrm{P}\mathrm{o}\mathrm{l}\mathrm{y},\quad{}\forall{}\mathcal{R},\quad{}G(\mathrm{I}\mathrm{d}({C}_{r},{p}_{s},{p}_{t}),\mathcal{R},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v},\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(w,\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v}),\mathrm{e}\mathrm{v}\mathrm{a}\mathrm{l}(w,\mathrm{z}\mathrm{e}\mathrm{r}\mathrm{o}\mathrm{E}\mathrm{n}\mathrm{v})).
$$



The current endpoint typings also give current formation of Id(Cᵣ,pₛ,pₜ). Formation and a semantic witness do not establish current-Has identity inhabitation.

#### 7.3 Complexity transfer and its domain

The root comparison with old(0) gives



$$
{V}_{r}(\mathrm{t}\mathrm{e}\mathrm{s}\mathrm{t}(P,Q),\mathrm{o}\mathrm{l}\mathrm{d}(0))\Leftrightarrow{}\forall{}v\in{}{\mathbb{N}}_{0}^{r},\quad{}P(v)\ne{}Q(v).
$$



Theorems 1 and 2 therefore transfer to the original endpoint relation, universal F identity validity at I, universal G identity validity at I, and existence of a uniform semantic polynomial identity witness. These are the exact compiled endpoints; compilation is total and effective.

The input still contains the source presentation, or an exact check that any supplied endpoints equal its compilation. No Π₁ upper bound is asserted for general bare endpoint codes. Nor is the result a characterization of arbitrary currently typed endpoints, current-Has identity inhabitation, raw conversion completeness, or contextual equivalence.

### 8 Consequences for certificates and finite testing

#### 8.1 No enumerable complete positive certificate system

Suppose finite certificates c were accepted by a recursive checker C(instance,c), sound and complete for ZeroTest. Dovetailing over instances and certificates would enumerate exactly the positive instances. Taking the computable preimage under the reduction of Section 4 would enumerate nonhalting. Halting is already enumerable; dovetailing the two enumerations would decide whether any machine halts, a contradiction.

The argument also applies when certificate acceptance is only recursively enumerable: dovetail the acceptance computations as well. Hence there is no recursively enumerable sound and complete positive certificate system of any finite-certificate format for this problem. The same conclusion transfers to the larger source equality problem and all the original semantic identity interfaces in Section 7. It does not depend on choosing a particular algebraic proof format.

#### 8.2 No total effective complete finite test procedure

Suppose a total algorithm assigned to each valid instance a finite list of tuples whose agreement with zero guaranteed universal agreement with zero. Evaluate the test at those tuples. If all results are zero, the guarantee proves the instance positive; if some result is nonzero, that tuple refutes it. The algorithm would decide ZeroTest, contradicting Theorem 1.

Likewise, suppose a total computable bound B(r,P,Q) guaranteed that whenever P and Q coincide at any input, they coincide somewhere in {0,…,B(r,P,Q)}ʳ. Finite evaluation of that box would decide whether such an input exists and hence would decide ZeroTest. No such total bound exists.

These conclusions leave intact the partial negative search of Section 3: enumerate larger boxes until a successful equality test is found. It terminates on each valid negative instance and need not terminate on a positive one.

#### 8.3 Why the previous mask argument stops

Within a zero/nonzero mask, specialize the coordinates fixed at zero. A remaining nonnegative-coefficient polynomial is either identically zero or strictly positive on the positive coordinates. This determines its branch when tested against literal zero. Comparing two positive polynomial values is different: x=y succeeds at (1,1) and fails at (1,2), although both inputs lie in the all-positive mask.

This example shows why the previous fixed-branch argument does not extend. The many-one reduction proves the stronger result that no effective sound and complete positive certificate method exists for the displayed extension. The boundary concerns this particular source operation: Eᵣ has its finite decision and certificate theorem, while adjoining the stated root expressions already produces the obstruction. No classification of all small extensions, numerical minimal-arity theorem, or claim of worldwide novelty is made.

### 9 Verification scope

The kernel-checked development includes the actual finite predecessor, reverse-subtraction, and equality descriptions; the syntactically distinct pure arithmetic and root grammars; correct compilation and coordinate dependence; current body and closed endpoint typings; adequacy for arbitrary raw natural observations; both directions of the numerical/original-F equivalence; the original F and G identity transfers; uniform semantic witnesses; and identity formation. The finite-tuple formulation, nonvacuous arity-zero behaviour, and arbitrary-observation interfaces have also been checked independently.

Fresh project-source replay succeeded for the 72 prerequisite P01AC modules and the two new support modules using Lean 4.19.0 and pinned external dependencies. The proof-dependency audit found only propext, Quot.sound, and Classical.choice. It found no admitted proof, unsafe or partial proof dependency, native-decision axiom, or extra representation axiom. This was a fresh replay of the project sources, not a fresh rebuild of Lean or its external library dependencies.

The full Π₁-completeness result is not a Lean theorem here. The imported existence premise, arbitrary coefficient-map splitting and domain shifts, finite parser and enumeration coding, fixed-polynomial specialisation, machine and hierarchy reduction, and certificate and finite-bound impossibility arguments are written mathematics. No concrete representing coefficients, runnable halting-to-polynomial reducer, or numerical fixed-arity bound are supplied. The result is a reviewed written complexity proof with a kernel-checked current-typing and original-semantics bridge.

### 10 A complete finite criterion in one variable

The root-equality extension remains decidable when it has just one input variable. This section adds a written corollary to the preceding result. It uses the same source language, compiler, and original semantic bridge. Its elementary polynomial argument imports no additional external premise, and it is not a new kernel formalisation or executable implementation.

**Theorem 3.** For any two expressions s,t∈R₁, a natural number M can be computed from their finite descriptions such that they are equal at every natural input if and only if they agree at 0,1,…,M. Equality of their literal compiled endpoints is therefore decidable under every original semantic identity interface in Section 7. At arity zero, evaluation at the empty tuple remains the decision procedure.

The bound need not be minimal. Its computation uses finite coefficient lists with unbounded integers. Resource exhaustion in a concrete implementation would not constitute a negative identity verdict.

#### 10.1 An explicit integer polynomial root bound

Given a finite integer-coefficient univariate polynomial H, aggregate equal exponents and remove zero coefficients. If H is zero or a nonzero constant, define B(H)=1. Otherwise write



$$
H(x)={a}_{d}{x}^{d}+\sum\limits_{i<d} {a}_{i}{x}^{i},\quad{}\quad{}d\ge{}1,\quad{}\quad{}{a}_{d}\ne{}0,
$$



and set



$$
S(H)=\sum\limits_{i<d} |{a}_{i}|,\quad{}\quad{}B(H)=S(H)+1.
$$



These data are computable from the finite coefficient representation.

**Lemma.** For every nonzero H and every natural n≥B(H), H(n)≠0.

For a nonzero constant the assertion is immediate. Otherwise n≥1 and n\>S(H). For i\<d, the inequality nⁱ≤nᵈ⁻¹ holds, while the nonzero integer coefficient ${a}_{d}$ has magnitude at least one. Therefore



$$
\begin{gathered}|\sum\limits_{i<d} {a}_{i}{n}^{i}|\le{}S(H){n}^{d-1} \\ <n\,{}{n}^{d-1} \\ ={n}^{d} \\ \le{}|{a}_{d}{n}^{d}|.\end{gathered}
$$



The lower terms cannot cancel the leading term. This includes S(H)=0, d=1, and a zero constant coefficient. The argument uses no division by a coefficient, rational-root theorem, analytic estimate, or external root-count theorem. Defining B(0) is convenient bookkeeping; the zero polynomial remains excluded from the nonvanishing assertion.

#### 10.2 Effective polynomial tails

For an old expression e∈E₁, use the accepted normal form for the unique positive mask. Identifying its variable with x yields a finite natural-coefficient polynomial Rₑ such that e(n)=Rₑ(n) for every n≥1. Choose bₑ=1 and Tₑ=Rₑ, regarded as an integer polynomial. This does not assert that the same polynomial gives e(0); that value will be checked separately.

For s=test(P,Q), expand the two pure arithmetic trees into finite natural coefficient maps. Embed the coefficients into the integers and compute



$$
D=P-Q.
$$



This is subtraction of coefficient maps in the construction, not a source-language constructor. If D is the zero polynomial, P and Q agree at every input and the test is constantly one. Set bₛ=1 and Tₛ=1. If D is nonzero, set bₛ=B(D) and Tₛ=0. The root-bound lemma implies P(n)≠Q(n), hence s(n)=0, for every n≥bₛ. This comparison uses the injective ordinary embedding of natural values into the integers.

Every expression s∈R₁ therefore has computably obtained data (bₛ,Tₛ), where bₛ≥1 and Tₛ is an integer polynomial, satisfying



$$
\forall{}n\in{}{\mathbb{N}}_{0},\quad{}n\ge{}{b}_{s}\Rightarrow{}[\![s]\!](n)={T}_{s}(n).
$$



The natural value on the left is embedded in the integers for this equality. Old expressions have polynomial tails; the new root expressions have constant tails. This statement concerns exactly the declared disjoint-union grammar, not arbitrary currently typed endpoints or a larger grammar of nested new tests.

#### 10.3 A finite bound for every pair

Compute the tail data for s and t, then put



$$
B=\mathrm{m}\mathrm{a}\mathrm{x}({b}_{s},{b}_{t}),\quad{}\quad{}H={T}_{s}-{T}_{t},\quad{}\quad{}M=\mathrm{m}\mathrm{a}\mathrm{x}(B,B(H)).
$$



For n≥B, the integer difference of the source values equals H(n). In particular, this is true at M, and M≥B(H).

Universal equality plainly implies agreement throughout 0,…,M. Conversely, suppose the source values agree at every input in that finite range. If H were nonzero, the root-bound lemma would give H(M)≠0. The tail equations would then give different source values at M, contradicting the tested equality. Thus H is the zero polynomial. The tail equations now give equality for every n≥B. Every input n\<B was also tested, because B≤M. This proves universal equality and Theorem 3.

Equivalently, one may compare the values below B and compare the two tail coefficient maps. The bound M additionally gives a finite collection of evaluations of the original source expressions, so the final test need not be a separate coefficient comparison.

If the tail maps differ, M itself distinguishes the functions. If the maps agree but the functions differ, a distinguishing input lies below B. The algorithm covers zero polynomials, nonzero constants, vanished leading coefficients after subtraction, and differences confined to n=0. Aggregation and removal of zero coefficients occur before choosing any leading exponent.

#### 10.4 Semantic transfer and the fixed arity boundary

The compiler and bridge of Sections 6 and 7 apply to every Rᵣ expression, hence to R₁. The exact endpoints retain current typing at N→N and Church-natural outputs. Their numerical equality is equivalent to the original endpoint F relation, the original F and G identity assertions, and the uniform semantic witness condition. Combining those equivalences with the finite criterion proves the decision result for the exact source-presented compiled endpoints. It does not prove that the current Has judgement derives every semantically valid identity.

The global lower bound fixes an unspecified finite number of witness coordinates; it does not fix one coordinate. The present corollary rules out one as a hardness arity. Together with the arity-zero decision procedure, it shows that every fixed arity supporting the previously proved hardness is at least two. It neither identifies such an arity nor classifies any particular arity greater than one.

The resulting boundary has three parts. The old zero-test language is decidable at every finite arity. Its root-equality extension remains decidable at arities zero and one. With arity as part of the input, that extension is Π₁-complete, already at some unspecified larger fixed arity. The finite method in this section depends on univariate integer polynomials and the exact tail structure proved above; it is not a finite bound for unrestricted Boolean or raw identity families.

Paper 6

## What final answers can identify about collective evidence use

### The result and its scope

The identity of the person announcing a joint answer need not reveal whose evidence influenced that answer. A precise version of this limitation can be proved without fitting any observations: two Gaussian decision mechanisms can have identical complete final-answer distributions while differing in whether both members’ evidence affects the decision. The equivalence below requires no noise specific to integration, allows different output reliability for the two announcers, and holds even when output noise vanishes.

This is a bounded nonidentification result. It establishes that the specified final-answer observations do not uniquely identify the mechanism within any model class containing this pair. It does not identify the mechanism in an actual group, establish that either model fits an empirical study, or exclude support supplied by other observations or justified restrictions. The associated empirical discussion appears in the main report’s collective competence section.

### Design and structural assumptions

Fix a finite number of trials $n$, the entire real-valued stimulus sequence ${x}_{1},\ldots{},{x}_{n}$, and the entire predetermined announcer schedule ${a}_{1},\ldots{},{a}_{n}$, where ${a}_{t}\in{}\{B,W\}$. Write this complete design as $D$. Alternation is allowed but is not required. Neither stimuli nor announcer assignments are selected in response to the models’ noises or answers in this fixed-design construction.

Choose finite parameters



$$
v>0,\quad{}\quad{}k>1,\quad{}\quad{}{r}_{B},{r}_{W}\ge{}0.
$$



For every trial, let ${Z}_{Bt},{Z}_{Wt},{Z}_{At}$ be mutually independent standard normal variables, independent also across trials. In both models define the same latent sensory summaries



$$
{X}_{Bt}={x}_{t}+\sqrt{v}\,{}{Z}_{Bt},\quad{}\quad{}{X}_{Wt}={x}_{t}+\sqrt{kv}\,{}{Z}_{Wt}.
$$



Thus $B$ has the smaller sensory variance. Hypothetical unaided threshold readouts of these summaries would give maximum response-curve slopes $1/\sqrt{2\pi{}v}$ and $1/\sqrt{2\pi{}kv}$. These are model quantities, not an assertion that people formed or reported private decisions. Their distributions are identical across the rival models. That model-to-model equality makes no claim about stability of human capacities across experimental conditions.

Suppress the trial index and put



$$
\alpha{}=\frac{k-1}{k+1},\quad{}\quad{}\beta{}=\frac{2}{k+1}.
$$



The rival structural equations are



$$
\begin{array}{rlrl}L:\quad{} & {T}_{L}={X}_{B}+\sqrt{{r}_{a}}\,{}{Z}_{A}, & {Y}_{L} & =\mathbf{1}\{{T}_{L}>0\}, \\ P:\quad{} & {T}_{P}=\alpha{}{X}_{B}+\beta{}{X}_{W}+\sqrt{{r}_{a}}\,{}{Z}_{A}, & {Y}_{P} & =\mathbf{1}\{{T}_{P}>0\}.\end{array}
$$



Model $L$ uses only $B$’s summary. Model $P$ uses both summaries with strictly positive weights. The same output-noise law is used in both, and there is no additional integration-noise term. The notation does not assert that the two models produce the same answer for every coupled realisation of the noises. The claim concerns equality of their probability laws.

### Exact equality of the observed output laws

The weights satisfy



$$
\alpha{}+\beta{}=1,\quad{}\quad{}{\alpha{}}^{2}+k{\beta{}}^{2}=\frac{{(k-1)}^{2}+4k}{{(k+1)}^{2}}=1.
$$



Consequently both scores have the conditional Gaussian law



$$
{T}_{L}\mid{}x,a\:{}\sim{}\:{}N(x,v+{r}_{a}),\quad{}\quad{}{T}_{P}\mid{}x,a\:{}\sim{}\:{}N(x,v+{r}_{a}).
$$



The construction can also be derived directly. If positive weights sum to one, matching the sensory variance of ${X}_{B}$ requires



$$
{(1-\beta{})}^{2}+k{\beta{}}^{2}=1\quad{}\Leftrightarrow{}\quad{}\beta{}((k+1)\beta{}-2)=0.
$$



The zero root gives the single-input mechanism; the nonzero root gives the two-input mechanism above. For $k=3$, $\alpha{}=\beta{}=1/2$: the ordinary average of the two summaries has sensory variance $(v+3v)/4=v$. The weights demonstrate equivalence; they are neither asserted to be optimal nor estimated from behaviour. The strict condition $k>1$ matters: at $k=1$, this nonzero solution has $\alpha{}=0$ and no longer uses both inputs.

Let $\Phi{}$ and $\phi{}$ be the standard normal distribution and density, and set ${\sigma{}}_{a}=\sqrt{v+{r}_{a}}$. The full response curve and its maximum slope are identical:



$$
p(x,a)=\mathrm{P}\mathrm{r}(Y=1\mid{}x,a)=\Phi{}(x/{\sigma{}}_{a}),\quad{}\quad{}{s}_{a}=\underset{x}{\mathrm{m}\mathrm{a}\mathrm{x}}\frac{\partial{}p(x,a)}{\partial{}x}=\frac{1}{\sqrt{2\pi{}}\,{}{\sigma{}}_{a}}.
$$



If the correct answer is 1 for $x>0$ and 0 for $x<0$, accuracy is $\Phi{}(|x|/{\sigma{}}_{a})$ in both models. Accuracy at $x=0$ requires a separate truth-label convention. Equality holds whether or not ${r}_{B}={r}_{W}$; equal announcer-specific slopes are unnecessary. Any pooled curve formed using the same design mixture is also identical.

The equality extends beyond single-trial marginals. Put ${p}_{t}=\Phi{}({x}_{t}/{\sigma{}}_{{a}_{t}})$. Under the stipulated independence across trials, for every $y\in{}\{0,1{\}}^{n}$,



$$
\underset{L}{\mathrm{P}\mathrm{r}}({Y}_{1:n}=y\mid{}D)=\underset{P}{\mathrm{P}\mathrm{r}}({Y}_{1:n}=y\mid{}D)=\prod\limits_{t=1}^{n} {p}_{t}^{{y}_{t}}{(1-{p}_{t})}^{1-{y}_{t}}.
$$



(1)

Thus the complete conditional output-sequence law agrees. Every statistic calculated only from these outputs and this design has the same sampling law under the pair. This statement concerns the constructed experiment, not sampling distributions fitted to an unexamined dataset.

For a random stimulus sequence, retain the predetermined announcer schedule and give both models the same joint exogenous law of the entire stimulus sequence, independent of every model noise. Integrating (1) against that common joint law gives equality of the unconditional output-sequence laws. The stimulus values need not be independent of one another. More generally, the same integration argument works for a common joint exogenous law of the complete design that is independent of the noises. These are sufficient conditions for the extension, not asserted necessary conditions for every conceivable observational equality. Adaptive or endogenous designs are outside this proof unless their full joint laws are separately established.

Matching only the one-trial stimulus marginals is insufficient. For example, take two trials with common $\sigma{}$ and let each stimulus be equally likely to be $+c$ or $-c$, where $c>0$. One design always repeats the first stimulus; another always reverses it. The one-trial marginals match, but with $p=\Phi{}(c/\sigma{})>1/2$, the probabilities that the answers agree are respectively ${p}^{2}+{(1-p)}^{2}$ and $2p(1-p)$. Independent sensory noises do not remove this difference between joint designs.

### Exact causal differences between the mechanisms

An intervention here replaces one displayed sensory-summary equation by a specified constant while leaving the design, the other structural equations, and their noise laws unchanged. This defines a model contrast. It is not a claim that an equivalent clean intervention on a person is available or would have no other effects.

Replacing ${X}_{W}$ by $w$ leaves $L$ unchanged, whereas



$$
\begin{array}{rl}\underset{L}{\mathrm{P}\mathrm{r}}(Y=1\mid{}x,a,\mathrm{d}\mathrm{o}({X}_{W}=w)) & =\Phi{}(x/{\sigma{}}_{a}), \\ \underset{P}{\mathrm{P}\mathrm{r}}(Y=1\mid{}x,a,\mathrm{d}\mathrm{o}({X}_{W}=w)) & =\Phi{}\kern0pt{}\left(\frac{\alpha{}x+\beta{}w}{\sqrt{{\alpha{}}^{2}v+{r}_{a}}}\right).\end{array}
$$



(2)

Similarly,



$$
\underset{P}{\mathrm{P}\mathrm{r}}(Y=1\mid{}x,a,\mathrm{d}\mathrm{o}({X}_{B}=b))=\Phi{}\kern0pt{}\left(\frac{\alpha{}b+\beta{}x}{\sqrt{{\beta{}}^{2}kv+{r}_{a}}}\right).
$$



(3)

The denominators in (2) and (3) are strictly positive, including when ${r}_{a}=0$. Because $\alpha{},\beta{}>0$, these probabilities increase strictly with the intervened input. For completeness, intervening on $B$’s input in $L$ gives $\Phi{}\left(b/\sqrt{{r}_{a}}\right)$ when ${r}_{a}>0$, and the deterministic response $\mathbf{1}\{b>0\}$ when ${r}_{a}=0$.

At $k=3$, the two-input intervention means are $(x+w)/2$ and $(b+x)/2$, with variances $v/4+{r}_{a}$ and $3v/4+{r}_{a}$, respectively. Thus the simple equal-weight example already has the full causal distinction. Observational equivalence of the original outputs has not made the structural mechanisms equivalent.

### What a linked measurement would add

The observation scheme matters. Suppose that the same trial’s two continuous summaries and answer were all observed, with its stimulus and announcer known. For ${r}_{a}>0$, their conditional response laws would be



$$
\begin{array}{rl}\underset{L}{\mathrm{P}\mathrm{r}}(Y=1\mid{}{X}_{B}=b,{X}_{W}=w,x,a) & =\Phi{}\left(b/\sqrt{{r}_{a}}\right), \\ \underset{P}{\mathrm{P}\mathrm{r}}(Y=1\mid{}{X}_{B}=b,{X}_{W}=w,x,a) & =\Phi{}\left((\alpha{}b+\beta{}w)/\sqrt{{r}_{a}}\right).\end{array}
$$



At ${r}_{a}=0$, these become $\mathbf{1}\{b>0\}$ and $\mathbf{1}\{\alpha{}b+\beta{}w>0\}$. The summaries have a nondegenerate joint normal density with full support, so the indicators differ on regions of positive probability. No division by zero or measurement of the unobserved score is needed for this distinction.

There is also an exact, simpler diagnostic using only the linked $W$ summary and answer:



$$
{\mathrm{C}\mathrm{o}\mathrm{v}}_{L}({X}_{W},Y\mid{}x,a)=0,\quad{}\quad{}{\mathrm{C}\mathrm{o}\mathrm{v}}_{P}({X}_{W},Y\mid{}x,a)=\frac{\beta{}kv}{{\sigma{}}_{a}}\,{}\phi{}(x/{\sigma{}}_{a})>0.
$$



(4)

To verify (4), write ${c}_{M}={\mathrm{C}\mathrm{o}\mathrm{v}}_{M}({X}_{W},T\mid{}x,a)$, which is zero in $L$ and $\beta{}kv$ in $P$. Joint normality gives $E[{X}_{W}-x\mid{}T,x,a]={c}_{M}(T-x)/{\sigma{}}_{a}^{2}$, while $E[(T-x)\mathbf{1}\{T>0\}\mid{}x,a]={\sigma{}}_{a}\phi{}(x/{\sigma{}}_{a})$. Multiplication yields (4). It remains valid when ${r}_{a}=0$. Conditioning on the stimulus is essential: pooling varying stimuli can induce summary-answer association even in $L$.

These augmented laws are distinguishable in principle. They do not promise finite-sample certainty, feasible access to latent summaries, or a cost-free way to add private responses to an actual procedure. The covariance is an observable difference under this particular augmented measurement scheme; association alone is not offered as a general proof of causal contribution outside the specified models.

### A linked binary readout is enough for this pair

The continuous summary in (4) is more information than this particular distinction requires. Keep the structural equations and finite parameters above. On one trial with fixed finite stimulus $x$ and known announcer $a$, suppose that the additional record is only



$$
Q=\mathbf{1}\{{X}_{W}>0\},
$$



linked to that same trial’s final answer $Y$. This is an observation map on the existing model variable. Obtaining the record is assumed to leave the structural equations and noise laws unchanged. The assumption does not establish that a private commitment or report by a person would be passive, that a real measurement has this form, or that such a record is available in any actual procedure.

#### Strict conditional separation

Under this augmented observation scheme,



$$
{\mathrm{C}\mathrm{o}\mathrm{v}}_{L}(Q,Y\mid{}x,a)=0,\quad{}\quad{}{\mathrm{C}\mathrm{o}\mathrm{v}}_{P}(Q,Y\mid{}x,a)>0.
$$



In $L$, the answer is a function of ${X}_{B}$ and the independent output noise. Conditional on the fixed design, these variables are independent of ${X}_{W}$, so $Q$ and $Y$ are independent. This proves the first equality, including when output noise is zero.

In $P$, independence of the sensory summaries and output noise gives the conditional response probability



$$
g(w)=\underset{P}{\mathrm{P}\mathrm{r}}(Y=1\mid{}{X}_{W}=w,x,a)=\Phi{}\kern0pt{}\left(\frac{\alpha{}x+\beta{}w}{\sqrt{{\alpha{}}^{2}v+{r}_{a}}}\right).
$$



The residual variance ${\alpha{}}^{2}v+{r}_{a}$ is strictly positive even at ${r}_{a}=0$, because $k>1$ implies $\alpha{}>0$ and $v>0$. All parameters are finite. Since $\beta{}>0$ and the normal distribution function is strictly increasing, $g$ is strictly increasing on the real line and satisfies $0<g(w)<1$ for every finite $w$.

Because $Q$ is a function of ${X}_{W}$, taking conditional expectations in the product and the means yields



$$
{\mathrm{C}\mathrm{o}\mathrm{v}}_{P}(Q,Y\mid{}x,a)=\mathrm{C}\mathrm{o}\mathrm{v}(Q,g({X}_{W})\mid{}x,a).
$$



Define



$$
\begin{array}{rl}\pi{} & =\mathrm{P}\mathrm{r}({X}_{W}>0\mid{}x,a)=\Phi{}\kern0pt{}\left(\frac{x}{\sqrt{kv}}\right), \\ {\mu{}}_{+} & =\mathbb{E}[g({X}_{W})\mid{}{X}_{W}>0,x,a], \\ {\mu{}}_{-} & =\mathbb{E}[g({X}_{W})\mid{}{X}_{W}\le{}0,x,a].\end{array}
$$



Nondegenerate normality and finite $x$ imply $0<\pi{}<1$ and $\mathrm{P}\mathrm{r}({X}_{W}=0\mid{}x,a)=0$. On the positive half-line, $g({X}_{W})-g(0)$ is strictly positive almost surely; on the negative half-line, $g(0)-g({X}_{W})$ is strictly positive almost surely. Both conditioning events have positive probability, and the differences are bounded. Their conditional expectations are therefore strictly positive, giving



$$
{\mu{}}_{+}>g(0)>{\mu{}}_{-}.
$$



Finally,



$$
\begin{gathered}\mathrm{C}\mathrm{o}\mathrm{v}(Q,g({X}_{W})\mid{}x,a)=\pi{}{\mu{}}_{+}-\pi{}(\pi{}{\mu{}}_{+}+(1-\pi{}){\mu{}}_{-}) \\ =\pi{}(1-\pi{})({\mu{}}_{+}-{\mu{}}_{-}) \\ >0.\end{gathered}
$$



This completes the proof for every admitted stimulus, announcer, and parameter choice, including zero output noise. The two models have the same $Q$ marginal as well as the same $Y$ marginal, but the linked joint laws differ. Separate unmatched marginal observations would retain those equal marginals and would not supply the distinguishing same-trial association. Conditioning on the stimulus remains essential: common variation in the stimulus can induce association in $L$ when trials are pooled.

#### Independent errors in the binary record

Consider the same one-trial observation with a specified recording channel, common to the two models. Let $E$ be a Bernoulli error with known probability $\epsilon{}\in{}[0,1]$, independent of all model variables conditional on the fixed design, and flip $Q$ exactly when $E=1$. The recorded bit is



$$
Q\prime{}=Q+E-2QE.
$$



Independence of the error implies



$$
\mathbb{E}[Q\prime{}\mid{}Q,Y,x,a]=\epsilon{}+(1-2\epsilon{})Q.
$$



Taking expectations, first after multiplication by $Y$ and then without it, gives



$$
\begin{array}{rl}\mathbb{E}[Q\prime{}Y\mid{}x,a] & =\epsilon{}\mathbb{E}[Y\mid{}x,a]+(1-2\epsilon{})\mathbb{E}[QY\mid{}x,a], \\ \mathbb{E}[Q\prime{}\mid{}x,a] & =\epsilon{}+(1-2\epsilon{})\mathbb{E}[Q\mid{}x,a].\end{array}
$$



Subtracting the product of the means therefore proves, in either model,



$$
\mathrm{C}\mathrm{o}\mathrm{v}(Q\prime{},Y\mid{}x,a)=(1-2\epsilon{})\mathrm{C}\mathrm{o}\mathrm{v}(Q,Y\mid{}x,a).
$$



For $0\le{}\epsilon{}<1/2$, the covariance remains zero in $L$ and strictly positive in $P$. This includes perfect recording at $\epsilon{}=0$. At $\epsilon{}=1/2$, for either binary value $u$,



$$
\mathrm{P}\mathrm{r}(Q\prime{}=u\mid{}Q,Y,x,a)=\frac{1}{2}.
$$



Thus $Q\prime{}$ is a fair bit independent of $(Q,Y)$, conditionally on the design. In particular, for $u,y\in{}\{0,1\}$,



$$
\underset{M}{\mathrm{P}\mathrm{r}}(Q\prime{}=u,Y=y\mid{}x,a)=\frac{1}{2}\underset{M}{\mathrm{P}\mathrm{r}}(Y=y\mid{}x,a),\quad{}\quad{}M\in{}\{L,P\}.
$$



The right side agrees between the models, so the entire one-trial recorded pair law agrees at this endpoint. This conclusion uses independence, not merely zero covariance. It extends to an entire sequence if each trial receives a fresh fair error independent of the full model and of the other errors; independence of each error from model variables alone does not assert that cross-trial condition.

For $1/2<\epsilon{}\le{}1$, the uncorrected covariance is negative in $P$ and zero in $L$, so the pair laws still differ. Replacing the record by $1-Q\prime{}$ gives error probability $1-\epsilon{}<1/2$; at $\epsilon{}=1$, this reversal restores $Q$ exactly. The factor above also shows that, with other parameters fixed, the separation tends to zero as $\epsilon{}$ approaches $1/2$.

Independence of recording error is a substantive measurement assumption. Response-dependent reporting, shared model and recording noise, or a reporting intervention that changes the decision equations falls outside this proof. Arbitrary noisy proxies need not obey the covariance identity.

#### Probability laws and finite observations

The strict covariance difference distinguishes the specified probability laws. It does not guarantee correct selection from a finite sample. Indeed, in $L$, both $Q$ and $Y$ have probabilities strictly between zero and one and are independent. In $P$, both half-lines for ${X}_{W}$ have positive probability and $0<g(w)<1$ for every finite $w$. Integrating $g$ or $1-g$ over either half-line shows that all four values of $(Q,Y)$ have positive probability in both models, including at zero output noise. Under the original across-trial independence, every finite sequence of uncorrupted linked pairs therefore has positive probability under both models. No possible finite record rules out either member of the pair with certainty. The one-trial support overlap also persists under every error probability $\epsilon{}\in{}[0,1]$, since a bit flip only permutes the positive cells and random flipping mixes those permutations.

There is no uniform positive size of the covariance gap over the admitted stimuli. The proof gives



$$
0<{\mathrm{C}\mathrm{o}\mathrm{v}}_{P}(Q,Y\mid{}x,a)=\pi{}(1-\pi{})({\mu{}}_{+}-{\mu{}}_{-})\le{}\pi{}(1-\pi{}),
$$



and $\pi{}(1-\pi{})$ tends to zero as $|x|$ tends to infinity. Finite-stimulus strictness and practical detectability are separate questions. The result supplies a sufficient additional observation for this constructed pair; it neither establishes access to a person’s latent summary nor treats association as a general causal-identification rule. No empirical attribution follows from adding this mathematical observation map.

### Finite sample warrant under a specified observation contract

The linked-bit distinction can support a finite controlled-error test when the observation scheme and a numerical separation are specified. Repeat a single fixed design $(x,a)$ on $n$ independent trials, using the same known finite parameters in the two mechanisms. Let each trial use the same passive binary readout and known flip probability $0\le{}\epsilon{}<1/2$. Conditional on the design, the recording errors are mutually independent, and their whole vector is independent of the whole vector of sensory and output noises. These are joint independence assumptions, not merely pairwise uncorrelatedness or pairwise independence. They make the recorded pairs independent with the same distribution within each mechanism.

#### A test with a known positive margin

Write



$$
\begin{array}{rl}p\prime{} & =\mathrm{P}\mathrm{r}(Q\prime{}=1\mid{}x,a)=\epsilon{}+(1-2\epsilon{})\Phi{}\kern0pt{}\left(\frac{x}{\sqrt{kv}}\right), \\ q & =\mathrm{P}\mathrm{r}(Y=1\mid{}x,a)=\Phi{}(x/{\sigma{}}_{a}), \\ \delta{} & ={\mathrm{C}\mathrm{o}\mathrm{v}}_{P}(Q\prime{},Y\mid{}x,a)>0.\end{array}
$$



Both marginals $p\prime{}$ and $q$ agree between the mechanisms. Suppose that the baseline $p\prime{}q$ and a positive lower bound ${\delta{}}_{0}$ are known, with



$$
0<{\delta{}}_{0}\le{}\delta{}.
$$



The exact $\delta{}$ may be used if specified. Strict positivity alone is not a numerical lower bound. Estimating parameters, certifying a margin from data, or allowing uncertainty about the measurement assumptions would require additional analysis.

For trial $i$, define the Bernoulli indicator



$$
{Z}_{i}=Q{\prime{}}_{i}{Y}_{i},\quad{}\quad{}\overline{Z}=\frac{1}{n}\sum\limits_{i=1}^{n} {Z}_{i}.
$$



Its mean is ${a}_{0}=p\prime{}q$ in $L$ and ${a}_{1}=p\prime{}q+\delta{}$ in $P$. Select $P$ exactly when



$$
\overline{Z}\ge{}{a}_{0}+\frac{{\delta{}}_{0}}{2};
$$



otherwise select $L$. Then each of the two conditional error probabilities is bounded by



$$
\underset{L}{\mathrm{P}\mathrm{r}}(\mathrm{s}\mathrm{e}\mathrm{l}\mathrm{e}\mathrm{c}\mathrm{t}\ P\mid{}D)\le{}{e}^{-n{\delta{}}_{0}^{2}/2},\quad{}\quad{}\underset{P}{\mathrm{P}\mathrm{r}}(\mathrm{s}\mathrm{e}\mathrm{l}\mathrm{e}\mathrm{c}\mathrm{t}\ L\mid{}D)\le{}{e}^{-n{\delta{}}_{0}^{2}/2}.
$$



Thus, for a chosen $0<\eta{}<1$, any positive integer satisfying



$$
n\ge{}\frac{2\mathrm{l}\mathrm{o}\mathrm{g}(1/\eta{})}{{\delta{}}_{0}^{2}}
$$



makes each error at most $\eta{}$. These are frequentist probabilities conditional on the specified mechanism and design. They are not posterior probabilities of the mechanisms, guarantees for a larger model class, or logically certain attribution.

#### Complete concentration proof

Let $Z$ be a Bernoulli variable with mean $u$. For $u=0$ or $u=1$, the centered variable is identically zero. Otherwise, define for any real $\lambda{}$



$$
\begin{array}{rl}\psi{}(\lambda{}) & =\mathrm{l}\mathrm{o}\mathrm{g}\mathbb{E}[{e}^{\lambda{}(Z-u)}]=-\lambda{}u+\mathrm{l}\mathrm{o}\mathrm{g}(1-u+u{e}^{\lambda{}}), \\ {v}_{\lambda{}} & =\frac{u{e}^{\lambda{}}}{1-u+u{e}^{\lambda{}}}.\end{array}
$$



Direct differentiation gives



$$
\psi{}(0)=\psi{}\prime{}(0)=0,\quad{}\quad{}\psi{}\prime{}\prime{}(\lambda{})={v}_{\lambda{}}(1-{v}_{\lambda{}})\le{}\frac{1}{4}.
$$



The twice-integrated identity



$$
\psi{}(\lambda{})={\lambda{}}^{2}\int\nolimits_{0}^{1} (1-s)\psi{}\prime{}\prime{}(s\lambda{})\,{}ds\le{}\frac{{\lambda{}}^{2}}{8}
$$



holds for positive and negative $\lambda{}$; it also bounds the identically zero endpoint cases. For independent Bernoulli variables ${Z}_{1},\ldots{},{Z}_{n}$ with common mean $u$, multiplication of their moment-generating functions therefore yields



$$
\mathbb{E}\kern0pt{}[{e}^{\lambda{}\sum\limits_{i} ({Z}_{i}-u)}]\le{}{e}^{n{\lambda{}}^{2}/8}.
$$



For completeness, the elementary Markov inequality follows from $V\ge{}c\,{}\mathbf{1}\{V\ge{}c\}$ for any nonnegative random variable $V$ and $c>0$, by taking expectations. Apply it to the displayed exponential. For $t>0$ and $\lambda{}>0$,



$$
\mathrm{P}\mathrm{r}(\overline{Z}-u\ge{}t)\le{}\mathrm{e}\mathrm{x}\mathrm{p}\kern0pt{}\left(-\lambda{}nt+\frac{n{\lambda{}}^{2}}{8}\right).
$$



Choosing $\lambda{}=4t$ gives the upper-tail bound ${e}^{-2n{t}^{2}}$. For $\lambda{}<0$, the event $\overline{Z}-u\le{}-t$ implies ${e}^{\lambda{}\sum\limits_{i} ({Z}_{i}-u)}\ge{}{e}^{-\lambda{}nt}$, so the same argument gives



$$
\mathrm{P}\mathrm{r}(\overline{Z}-u\le{}-t)\le{}\mathrm{e}\mathrm{x}\mathrm{p}\kern0pt{}\left(\lambda{}nt+\frac{n{\lambda{}}^{2}}{8}\right)={e}^{-2n{t}^{2}}\quad{}\mathrm{w}\mathrm{h}\mathrm{e}\mathrm{n}\ \lambda{}=-4t.
$$



In $L$, the error event is $\overline{Z}-{a}_{0}\ge{}{\delta{}}_{0}/2$, to which the upper-tail bound applies. In $P$, an error requires



$$
\overline{Z}<{a}_{0}+\frac{{\delta{}}_{0}}{2},\quad{}\quad{}\overline{Z}-{a}_{1}<-\left(\delta{}-\frac{{\delta{}}_{0}}{2}\right)\le{}-\frac{{\delta{}}_{0}}{2}.
$$



It is therefore contained in the lower-tail event with $t={\delta{}}_{0}/2$. Both errors are at most ${e}^{-n{\delta{}}_{0}^{2}/2}$. A sample mean exactly on the threshold selects $P$, so it is included in the $L$ error and excluded from the $P$ error; neither tail argument omits a tie. Solving ${e}^{-n{\delta{}}_{0}^{2}/2}\le{}\eta{}$ proves the stated sample bound.

The argument requires independent repetitions with the stated common means. It does not apply unchanged to dependent trials, arbitrary pooling of designs, or a baseline estimated from the same observations. If a known lower bound for the uncorrupted covariance is ${c}_{0}>0$, the recording calculation permits ${\delta{}}_{0}=(1-2\epsilon{}){c}_{0}$. The displayed sufficient sample bound then grows as ${(1-2\epsilon{})}^{-2}$ when $\epsilon{}$ approaches $1/2$. This is a sufficient bound for this test, not a claim that the bound is necessary or optimal.

#### No uniform finite guarantee without a separation condition

The dependence on a positive margin reflects a genuine obstruction. Let ${f}_{L}$ and ${f}_{P}$ denote the one-trial probability masses of the full recorded pair on $\mathcal{S}=\{0,1{\}}^{2}$. In $L$, independence gives



$$
\begin{array}{rlrl}{f}_{L}(1,1) & =p\prime{}q, & {f}_{L}(1,0) & =p\prime{}(1-q), \\ {f}_{L}(0,1) & =(1-p\prime{})q, & {f}_{L}(0,0) & =(1-p\prime{})(1-q).\end{array}
$$



Since the marginals agree and ${f}_{P}(1,1)-p\prime{}q=\delta{}$, subtraction from those marginals and from total probability gives



$$
\begin{array}{rlrl}{f}_{P}(1,1)-{f}_{L}(1,1) & =\delta{}, & {f}_{P}(1,0)-{f}_{L}(1,0) & =-\delta{}, \\ {f}_{P}(0,1)-{f}_{L}(0,1) & =-\delta{}, & {f}_{P}(0,0)-{f}_{L}(0,0) & =\delta{}.\end{array}
$$



Consequently their total variation distance, defined here by half the sum of absolute mass differences, is exactly



$$
\mathrm{T}\mathrm{V}({f}_{P},{f}_{L})=\frac{1}{2}\sum\limits_{z\in{}\mathcal{S}} |{f}_{P}(z)-{f}_{L}(z)|=2\delta{}.
$$



For the independent $n$-trial product laws, replacing one factor at a time gives the exact telescoping identity



$$
\prod\limits_{j=1}^{n} {f}_{P}({z}_{j})-\prod\limits_{j=1}^{n} {f}_{L}({z}_{j})=\sum\limits_{i=1}^{n} \left(\prod\limits_{j<i} {f}_{P}({z}_{j})\right)({f}_{P}({z}_{i})-{f}_{L}({z}_{i}))\left(\prod\limits_{j>i} {f}_{L}({z}_{j})\right).
$$



Take absolute values, apply the triangle inequality, and sum over every $({z}_{1},\ldots{},{z}_{n})$. For each summand, every remaining probability factor sums to one. Dividing the resulting bound by two proves



$$
\mathrm{T}\mathrm{V}({f}_{P}^{\otimes{}n},{f}_{L}^{\otimes{}n})\le{}n\mathrm{T}\mathrm{V}({f}_{P},{f}_{L})=2n\delta{}.
$$



For any two probability masses, their difference sums to zero. Its positive part and the absolute value of its negative part therefore each sum to their total variation distance. It follows that the probability difference for any event is at most total variation. If $A$ is the event that a deterministic test selects $P$, its two errors thus satisfy



$$
\begin{gathered}\underset{L}{\mathrm{P}\mathrm{r}}(A\mid{}D)+\underset{P}{\mathrm{P}\mathrm{r}}({A}^{c}\mid{}D)=1-(\underset{P}{\mathrm{P}\mathrm{r}}(A\mid{}D)-\underset{L}{\mathrm{P}\mathrm{r}}(A\mid{}D)) \\ \ge{}1-\mathrm{T}\mathrm{V}({f}_{P}^{\otimes{}n},{f}_{L}^{\otimes{}n}) \\ \ge{}1-2n\delta{}.\end{gathered}
$$



The same bound holds for a randomized test: if $h$ is its probability of selecting $P$ at each observed sequence, then $0\le{}h\le{}1$, and summing $h$ against the difference of the masses is again at most the sum of the positive part. This proof permits every test using the full linked observations, not only the product-indicator test above.

Fix any finite positive $n$ and $0<\eta{}<1/2$. If an admitted pair has



$$
0<\delta{}<\frac{1-2\eta{}}{2n},
$$



then the sum of the errors is greater than $2\eta{}$; both cannot be at most $\eta{}$. Arbitrarily small positive margins occur within the stipulated Gaussian family. Before recording error, the covariance is $\pi{}(1-\pi{})({\mu{}}_{+}-{\mu{}}_{-})$, with $0<{\mu{}}_{+}-{\mu{}}_{-}<1$. Holding the other finite parameters fixed while letting the finite stimulus $x$ increase makes $\pi{}$ tend to one and this covariance tend to zero. A fixed $\epsilon{}<1/2$ multiplies it by $1-2\epsilon{}$. Alternatively, with the uncorrupted pair fixed, choosing $\epsilon{}$ arbitrarily close to $1/2$ makes the recorded margin arbitrarily small.

There is therefore no fixed finite sample size that makes both errors uniformly at most such an $\eta{}$ over this unrestricted parameter and design class. This does not prevent choosing a more informative design, imposing bounds on noise, verifying a positive margin, or using additional observations. If the recording contract is extended to $\epsilon{}=1/2$ with independent errors across trials, each recorded pair has the same law in both models, and independence makes the complete augmented law identical for every number of repetitions. The observations then provide no differential likelihood information between the pair.

#### An exact illustrative sample contract

A fully specified example gives an elementary exact margin. Take



$$
x=0,\quad{}\quad{}v=1,\quad{}\quad{}k=3,\quad{}\quad{}{r}_{a}=0,\quad{}\quad{}\epsilon{}=0,
$$



so $\alpha{}=\beta{}=1/2$. Let $U={X}_{B}$ and $V={X}_{W}/\sqrt{3}$; these are independent standard normals. Then



$$
Q=\mathbf{1}\{V>0\},\quad{}\quad{}{Y}_{P}=\mathbf{1}\{U+\sqrt{3}V>0\}.
$$



Each marginal probability is $1/2$. To calculate their joint probability directly, the joint density of $(U,V)$ is



$$
f(u,v)=\frac{1}{2\pi{}}\mathrm{e}\mathrm{x}\mathrm{p}\kern0pt{}\left(-\frac{{u}^{2}+{v}^{2}}{2}\right).
$$



With $u=\rho{}\mathrm{c}\mathrm{o}\mathrm{s}\theta{}$, $v=\rho{}\mathrm{s}\mathrm{i}\mathrm{n}\theta{}$, the area element is $\rho{}\,{}d\rho{}\,{}d\theta{}$. An angular sector of width $\omega{}$ therefore has probability



$$
\frac{\omega{}}{2\pi{}}\int\nolimits_{0}^{\infty{}} {e}^{-{\rho{}}^{2}/2}\rho{}\,{}d\rho{}=\frac{\omega{}}{2\pi{}},
$$



because the radial integral is one. Boundary rays and the origin have probability zero. The condition $V>0$ corresponds to $0<\theta{}<\pi{}$, while



$$
U+\sqrt{3}V=2\rho{}\mathrm{c}\mathrm{o}\mathrm{s}(\theta{}-\pi{}/3)>0
$$



corresponds to $-\pi{}/6<\theta{}<5\pi{}/6$, modulo a full turn. The intersection has width $5\pi{}/6$, yielding



$$
\underset{P}{\mathrm{P}\mathrm{r}}(Q=1,Y=1)=\frac{5}{12}.
$$



In $L$, $Q$ and ${Y}_{L}=\mathbf{1}\{U>0\}$ are independent with the same half-probability marginals, so



$$
\underset{L}{\mathrm{P}\mathrm{r}}(Q=1,Y=1)=\frac{1}{4},\quad{}\quad{}\delta{}=\frac{5}{12}-\frac{1}{4}=\frac{1}{6}.
$$



Use the exact margin ${\delta{}}_{0}=1/6$. For $n=216$ independent repetitions, the rule selects $P$ if at least 72 trials have both recorded bits equal to one, and selects $L$ otherwise, since



$$
{a}_{0}+\frac{{\delta{}}_{0}}{2}=\frac{1}{4}+\frac{1}{12}=\frac{1}{3},\quad{}\quad{}216\left(\frac{1}{3}\right)=72.
$$



Each conditional error is at most



$$
\mathrm{e}\mathrm{x}\mathrm{p}\kern0pt{}\left(-\frac{216}{2\cdot{}36}\right)={e}^{-3}<\frac{1}{20}.
$$



For an exact check of the final inequality, the nonnegative exponential series gives



$$
{e}^{3}>\sum\limits_{j=0}^{8} \frac{{3}^{j}}{j!}=\frac{89641}{4480}>\frac{89600}{4480}=20.
$$



These 216 repetitions constitute an illustrative mathematical contract. They are not trials that were run or a sample-size recommendation for an actual study. The bound depends on the exact known mechanisms, passive same-trial recording, and independent repetition at the specified design. At $x=0$, no truth-label convention is needed for this calculation: it concerns the joint distribution of the recorded bits rather than accuracy. Unknown parameters, a reactive measurement procedure, or additional candidate mechanisms would change the inferential task.

#### What controlled error adds to causal warrant

The positive-cell argument above shows that every finite recorded sequence has positive probability under both mechanisms under this repeated independent design, including at zero output noise. A deterministic or randomized test cannot have zero error under both laws: zero error in $L$ would require selecting $L$ with probability one on every possible sequence, which would give error one in $P$. Controlled error is compatible with this lack of finite-sample certainty.

The mathematical gain is specific. Answer-only observations have identical full laws in the constructed pair. A passive linked binary record with the specified independent error rate makes the laws distinct. A known positive margin and independent repeated design then support an explicit finite controlled-error discrimination rule. Whether the measurement contract, parameters, and restriction to this pair describe an actual group remains an empirical and explanatory question. Neither the discrimination rule nor its error bound establishes that premise.

### Sequential discrimination without a known baseline or margin

The preceding finite-sample rule requires a supplied marginal baseline and positive numerical margin. A one-sided sequential rule removes those numerical inputs while retaining the passive linked observation and independent repeated design. It controls the probability of ever selecting the pooled mechanism under the leader mechanism and eventually detects every fixed admitted positive alternative with probability one. It does not supply a terminating certificate for the leader mechanism. A separate argument below shows why uniformly reliable answers in both directions cannot also terminate almost surely under the fixed null in an unseparated subfamily of the same Gaussian construction.

#### Observation class and decision rule

Repeat one fixed design $(x,a)$ indefinitely with fixed finite model parameters. On each trial observe the same passive recorded pair $(Q{\prime{}}_{i},{Y}_{i})\in{}\{0,1{\}}^{2}$. The pairs are independent and identically distributed. In the Gaussian construction, this follows from the stipulated independent sensory and output noises together with recording errors that are mutually independent across trials and whose whole sequence is independent of the whole sequence of model noises. Each error has the same fixed probability $0\le{}\epsilon{}<1/2$. Its numerical value need not be known to the rule. The restriction to this error range and the independence and passivity assumptions remain part of the observation contract.

In $L$, the two recorded bits are independent within a trial. In each admitted $P$, their covariance is strictly positive by the binary-readout and recording calculations above. More generally, the following probability argument requires only independent identically distributed binary pairs with these respective zero and positive covariances. It does not require independence between the two bits under $P$.

For this section write the unknown population quantities as



$$
p=\mathbb{E}[Q\prime{}],\quad{}\quad{}q=\mathbb{E}[Y],\quad{}\quad{}b=\mathbb{E}[Q\prime{}Y],\quad{}\quad{}\delta{}=b-pq.
$$



The letter $a$ continues to denote the announcer. All probabilities and expectations in this section are conditional on the repeated fixed design and the specified mechanism. At each positive integer $n$, calculate



$$
{\widehat{p}}_{n}=\frac{1}{n}\sum\limits_{i=1}^{n} Q{\prime{}}_{i},\quad{}\quad{}{\widehat{q}}_{n}=\frac{1}{n}\sum\limits_{i=1}^{n} {Y}_{i},\quad{}\quad{}{\widehat{b}}_{n}=\frac{1}{n}\sum\limits_{i=1}^{n} Q{\prime{}}_{i}{Y}_{i},\quad{}\quad{}{\widehat{c}}_{n}={\widehat{b}}_{n}-{\widehat{p}}_{n}{\widehat{q}}_{n}.
$$



Choose a false-selection tolerance $0<\gamma{}<1$, and put



$$
{\varepsilon{}}_{n}=\sqrt{\frac{\mathrm{l}\mathrm{o}\mathrm{g}\kern0pt{}(6n(n+1)/\gamma{})}{2n}},\quad{}\quad{}\tau{}=\mathrm{i}\mathrm{n}\mathrm{f}\{n\ge{}1:{\widehat{c}}_{n}>3{\varepsilon{}}_{n}\}.
$$



Here $\mathrm{l}\mathrm{o}\mathrm{g}$ is the natural logarithm, and the infimum of an empty set of stopping indices is $\infty{}$. When $\tau{}<\infty{}$, select $P$. Otherwise continue sampling; this procedure never selects $L$. The statistic need not be an unbiased covariance estimator: the proof controls its error directly. The rule uses the observed pairs and the chosen tolerance, without supplied values of $p,q,b,\delta{}$, a positive lower bound for $\delta{}$, or the numerical Gaussian parameters or error rate.

The exact guarantees are



$$
\underset{L}{\mathrm{P}\mathrm{r}}(\tau{}<\infty{})\le{}\gamma{},\quad{}\quad{}\underset{P}{\mathrm{P}\mathrm{r}}(\tau{}<\infty{})=1\quad{}\mathrm{f}\mathrm{o}\mathrm{r}\ \mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\mathrm{y}\ \mathrm{f}\mathrm{i}\mathrm{x}\mathrm{e}\mathrm{d}\ \mathrm{a}\mathrm{d}\mathrm{m}\mathrm{i}\mathrm{t}\mathrm{t}\mathrm{e}\mathrm{d}\ P\ \mathrm{w}\mathrm{i}\mathrm{t}\mathrm{h}\ \delta{}>0.
$$



The first bound is simultaneous over all sample sizes, so it covers the data-dependent first crossing. The second is pointwise in the positive alternative. No finite uniform sample bound as $\delta{}$ approaches zero is asserted, and neither statement certifies the underlying observation assumptions from the data.

#### Simultaneous confidence and false selection

Each of the three sequences $Q{\prime{}}_{i}$, ${Y}_{i}$, and $Q{\prime{}}_{i}{Y}_{i}$ is a Bernoulli sequence independent across trials. The sequences need not be mutually independent within a trial. The complete concentration calculation in the preceding section, with its upper and lower tails added, gives for any one of these sequences with mean $u$



$$
\begin{gathered}\mathrm{P}\mathrm{r}(|{\overline{Z}}_{n}-u|>{\varepsilon{}}_{n})\le{}2\mathrm{e}\mathrm{x}\mathrm{p}(-2n{\varepsilon{}}_{n}^{2}) \\ =\frac{\gamma{}}{3n(n+1)}.\end{gathered}
$$



The strict deviation event is contained in the union of the two closed tail events already bounded. A union bound over the three sequences therefore gives at most $\gamma{}/[n(n+1)]$ for failure of any of their mean bounds at a particular $n$. A further union bound over every positive integer $n$ gives total failure probability at most $\gamma{}$, since



$$
\sum\limits_{n=1}^{\infty{}} \frac{1}{n(n+1)}=\underset{N\to{}\infty{}}{\mathrm{l}\mathrm{i}\mathrm{m}}\sum\limits_{n=1}^{N} \left(\frac{1}{n}-\frac{1}{n+1}\right)=\underset{N\to{}\infty{}}{\mathrm{l}\mathrm{i}\mathrm{m}}\left(1-\frac{1}{N+1}\right)=1.
$$



Neither union bound requires independence between its events. Let $G$ be the complementary event. Then $\mathrm{P}\mathrm{r}(G)\ge{}1-\gamma{}$, and on $G$, simultaneously for every $n$,



$$
|{\widehat{p}}_{n}-p|\le{}{\varepsilon{}}_{n},\quad{}\quad{}|{\widehat{q}}_{n}-q|\le{}{\varepsilon{}}_{n},\quad{}\quad{}|{\widehat{b}}_{n}-b|\le{}{\varepsilon{}}_{n}.
$$



All sample and population means lie in $[0,1]$. The exact decomposition of the product error gives



$$
\begin{gathered}|{\widehat{p}}_{n}{\widehat{q}}_{n}-pq|=|({\widehat{p}}_{n}-p){\widehat{q}}_{n}+p({\widehat{q}}_{n}-q)| \\ \le{}|{\widehat{p}}_{n}-p|{\widehat{q}}_{n}+p|{\widehat{q}}_{n}-q| \\ \le{}2{\varepsilon{}}_{n}.\end{gathered}
$$



Adding the remaining mean error proves that on this same event



$$
|{\widehat{c}}_{n}-\delta{}|\le{}|{\widehat{b}}_{n}-b|+|{\widehat{p}}_{n}{\widehat{q}}_{n}-pq|\le{}3{\varepsilon{}}_{n}\quad{}\mathrm{f}\mathrm{o}\mathrm{r}\ \mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\mathrm{y}\ n\ge{}1.
$$



In $L$, $\delta{}=0$, so the strict inequality defining $\tau{}$ cannot hold anywhere on $G$. Consequently



$$
\{\tau{}<\infty{}\}\subseteq{}{G}^{c}\quad{}\mathrm{i}\mathrm{n}\ L,\quad{}\quad{}\underset{L}{\mathrm{P}\mathrm{r}}(\tau{}<\infty{})\le{}\underset{L}{\mathrm{P}\mathrm{r}}({G}^{c})\le{}\gamma{}.
$$



This is a simultaneous-in-time confidence argument, not a fixed-sample interval reused without correction. A crossing at any observed stopping time remains a crossing in the union already controlled.

The threshold satisfies ${\varepsilon{}}_{n}\to{}0$, because its squared value is a constant plus $\mathrm{l}\mathrm{o}\mathrm{g}n+\mathrm{l}\mathrm{o}\mathrm{g}(n+1)$, all divided by $2n$. For a fixed positive alternative, choose any finite $n$ large enough that $6{\varepsilon{}}_{n}<\delta{}$. On $G$,



$$
{\widehat{c}}_{n}\ge{}\delta{}-3{\varepsilon{}}_{n}>3{\varepsilon{}}_{n},
$$



so the rule has stopped by that $n$. This gives finite detection with probability at least $1-\gamma{}$ without asking the rule to know $\delta{}$. It does not yet give the asserted probability-one statement.

#### Almost sure detection at each positive alternative

The probability-one conclusion follows separately from the same elementary concentration bounds. For one of the Bernoulli sequences and any fixed $t>0$, a union bound gives



$$
\begin{gathered}\mathrm{P}\mathrm{r}(\mathrm{s}\mathrm{o}\mathrm{m}\mathrm{e}\ n\ge{}N\ \mathrm{h}\mathrm{a}\mathrm{s}\ |{\overline{Z}}_{n}-u|>t)\le{}\sum\limits_{n=N}^{\infty{}} 2{e}^{-2n{t}^{2}} \\ =\frac{2{e}^{-2N{t}^{2}}}{1-{e}^{-2{t}^{2}}}\to{}0.\end{gathered}
$$



The event of infinitely many deviations greater than $t$ is contained in the event on the left for every $N$. Its probability is therefore bounded by arbitrarily small positive numbers and equals zero. Apply this argument for each $t=1/m$, where $m$ is a positive integer. The countable union of the resulting probability-zero events still has probability zero. Outside that union, for each $m$ only finitely many deviations exceed $1/m$. Given any positive tolerance, choose $m$ with its reciprocal smaller than that tolerance; all sufficiently late sample means then fall within the tolerance. This proves ${\overline{Z}}_{n}\to{}u$ almost surely.

Apply the argument to all three Bernoulli sequences. A union of their three exceptional null events is again null, so



$$
{\widehat{p}}_{n}\to{}p,\quad{}\quad{}{\widehat{q}}_{n}\to{}q,\quad{}\quad{}{\widehat{b}}_{n}\to{}b,\quad{}\quad{}{\widehat{c}}_{n}\to{}\delta{}\quad{}\mathrm{a}\mathrm{l}\mathrm{m}\mathrm{o}\mathrm{s}\mathrm{t}\ \mathrm{s}\mathrm{u}\mathrm{r}\mathrm{e}\mathrm{l}\mathrm{y}.
$$



The last conclusion follows also from the displayed product-error decomposition. If $\delta{}>0$, then on this convergence event, eventually ${\widehat{c}}_{n}>\delta{}/2$. Since ${\varepsilon{}}_{n}\to{}0$, eventually $3{\varepsilon{}}_{n}<\delta{}/2$ as well. Both statements hold for every sufficiently large finite $n$, so a finite crossing must have occurred. Thus ${\mathrm{P}\mathrm{r}}_{P}(\tau{}<\infty{})=1$. This proof does not identify the earlier event $G$, whose probability is only bounded below by $1-\gamma{}$, with an event of probability one.

#### Why uniformly reliable answers in both directions cannot terminate under the fixed null

The obstruction can be proved within an explicit subfamily of the original Gaussian example. Fix



$$
x=0,\quad{}\quad{}v=1,\quad{}\quad{}k=3,\quad{}\quad{}{r}_{a}=0,
$$



retain the same passive readout, and vary only the unknown independent flip probability $\epsilon{}\in{}[0,1/2)$. The exact illustrative calculation above gives uncorrupted covariance $1/6$. Under $L$, the recorded pair is uniform on $\{0,1{\}}^{2}$ for every $\epsilon{}$: the uncorrupted bits are independent and fair, and an independent flip of one fair bit preserves this law. Denote this fixed one-trial null law by ${L}_{0}$. Under ${P}_{\epsilon{}}$, both marginals remain $1/2$, and the recording identity gives



$$
{\delta{}}_{\epsilon{}}=\frac{1-2\epsilon{}}{6}>0.
$$



The equal-marginal cell calculation and product bound already proved yield



$$
\mathrm{T}\mathrm{V}({P}_{\epsilon{}},{L}_{0})=2{\delta{}}_{\epsilon{}},\quad{}\quad{}\mathrm{T}\mathrm{V}({P}_{\epsilon{}}^{\otimes{}N},{L}_{0}^{\otimes{}N})\le{}2N{\delta{}}_{\epsilon{}}\quad{}\mathrm{f}\mathrm{o}\mathrm{r}\ \mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\mathrm{y}\ \mathrm{f}\mathrm{i}\mathrm{n}\mathrm{i}\mathrm{t}\mathrm{e}\ \mathrm{p}\mathrm{o}\mathrm{s}\mathrm{i}\mathrm{t}\mathrm{i}\mathrm{v}\mathrm{e}\ N.
$$



The one-trial distance tends to zero as $\epsilon{}$ approaches $1/2$ from below. The endpoint itself need not be an admitted alternative; the same null law ${L}_{0}$ is already present for every admitted error rate.

Suppose a single sequential procedure knows this entire family but is not given $\epsilon{}$. Upon stopping it returns exactly one of $L$ and $P$. The procedure is nonanticipating: its decision by sample $N$ depends only on the first $N$ pairs and any internal randomisation. Randomisation, if used, has a common law under all mechanisms and is independent of the observation sequence. It may be represented by a random seed that supplies the procedure’s random choices. Suppose



$$
\begin{array}{rl}\underset{{L}_{0}}{\mathrm{P}\mathrm{r}}(\mathrm{t}\mathrm{e}\mathrm{r}\mathrm{m}\mathrm{i}\mathrm{n}\mathrm{a}\mathrm{t}\mathrm{e}) & =1, \\ \underset{{L}_{0}}{\mathrm{P}\mathrm{r}}(\mathrm{s}\mathrm{e}\mathrm{l}\mathrm{e}\mathrm{c}\mathrm{t}\ P) & \le{}\gamma{}, \\ \underset{{P}_{\epsilon{}}}{\mathrm{P}\mathrm{r}}(\mathrm{s}\mathrm{e}\mathrm{l}\mathrm{e}\mathrm{c}\mathrm{t}\ L) & \le{}\zeta{}\quad{}\mathrm{f}\mathrm{o}\mathrm{r}\ \mathrm{e}\mathrm{v}\mathrm{e}\mathrm{r}\mathrm{y}\ 0\le{}\epsilon{}<1/2,\end{array}\quad{}\quad{}0\le{}\zeta{}<1,\quad{}\gamma{}+\zeta{}<1.
$$



These requirements are inconsistent. To prove this, let ${A}_{N}$ be the event that the procedure has selected $L$ by sample $N$. Almost-sure termination under ${L}_{0}$ and the first error bound give eventual selection of $L$ probability at least $1-\gamma{}$. The events ${A}_{N}$ increase to that eventual-selection event. Their probabilities converge to its probability: writing the union as the disjoint union of ${A}_{1}$ and the successive differences ${A}_{N}\setminus{}{A}_{N-1}$ proves this directly from countable additivity. Choose any $\eta{}>0$ such that $\gamma{}+\zeta{}+2\eta{}<1$. Some finite positive $N$ then satisfies



$$
\underset{{L}_{0}}{\mathrm{P}\mathrm{r}}({A}_{N})>1-\gamma{}-\eta{}.
$$



Choose $\epsilon{}<1/2$ close enough to $1/2$ that $2N{\delta{}}_{\epsilon{}}<\eta{}$. This is possible because ${\delta{}}_{\epsilon{}}\to{}0$. The event ${A}_{N}$ uses only a finite observation prefix, even if the procedure may continue indefinitely on other sample paths. For completeness, for each possible prefix $z\in{}{(\{0,1{\}}^{2})}^{N}$, let ${h}_{N}(z)\in{}[0,1]$ be the probability over the independent random seed that the procedure selects $L$ by $N$ on that prefix. It is the same function under every mechanism. If ${f}_{\epsilon{}}^{(N)}$ and ${f}_{0}^{(N)}$ denote the corresponding product probability masses, then



$$
\begin{gathered}|\underset{{P}_{\epsilon{}}}{\mathrm{P}\mathrm{r}}({A}_{N})-\underset{{L}_{0}}{\mathrm{P}\mathrm{r}}({A}_{N})|=|\sum\limits_{z} {h}_{N}(z)({f}_{\epsilon{}}^{(N)}(z)-{f}_{0}^{(N)}(z))| \\ \le{}\mathrm{T}\mathrm{V}({P}_{\epsilon{}}^{\otimes{}N},{L}_{0}^{\otimes{}N}) \\ \le{}2N{\delta{}}_{\epsilon{}}<\eta{}.\end{gathered}
$$



The middle inequality holds because the mass difference sums to zero, its positive and negative parts each have total mass equal to the total variation distance, and $0\le{}{h}_{N}\le{}1$. It applies to deterministic rules as the special case in which ${h}_{N}$ is an indicator. Consequently



$$
\begin{gathered}\underset{{P}_{\epsilon{}}}{\mathrm{P}\mathrm{r}}(\mathrm{s}\mathrm{e}\mathrm{l}\mathrm{e}\mathrm{c}\mathrm{t}\ L)\ge{}\underset{{P}_{\epsilon{}}}{\mathrm{P}\mathrm{r}}({A}_{N}) \\ >1-\gamma{}-2\eta{} \\ >\zeta{},\end{gathered}
$$



contradicting the uniform alternative-side error requirement. No termination assumption under ${P}_{\epsilon{}}$, finite expected sample size, or deterministic bound on stopping time was used. The result concerns this unseparated family and observation contract. A supplied lower bound separating $\epsilon{}$ from $1/2$, a restricted candidate class, or a stronger observation scheme can change the problem.

#### Mathematical rule and numerical implementation

The sequential rule is stated in exact real arithmetic. A numerical implementation must certify the stopping comparison, including the computed statistic and the transcendental threshold, or otherwise account for its numerical errors before inheriting the bound. A certified conservative upper approximation to the threshold protects the false-selection argument when the statistic comparison is also certified. To inherit almost-sure detection by the same proof, the implemented upper thresholds must additionally tend to zero and the statistic approximation errors must vanish. An arbitrarily large conservative threshold alone would not ensure detection. No runnable sequential classifier, floating-point certification, or numerical implementation result is claimed here.

#### What the sequential result adds to causal warrant

The rule removes knowledge of the marginal baseline and positive numerical margin from the positive-detection procedure. It pays for this by permitting indefinite continuation when the observations remain consistent with zero covariance. The fixed-null impossibility argument shows that this limitation cannot generally be removed while retaining uniformly small errors in both directions over the displayed unseparated family. Failure to stop by a finite sample size is not a certified selection of $L$, and it is not a proof that a person did not contribute.

All guarantees still presuppose the independent repeated design, passive linked recording with the declared error structure, and the interpretation of positive covariance within the specified candidate model class. The numerical value of the error rate may be unknown while its restriction below one half remains an assumption. Positive covariance is not a general proof that a particular actual person causally contributed. Neither empirical validity of the observation contract nor a realized experimental result is established. The answer-only nonidentification theorem remains unchanged because the sequential rule uses additional linked observations.

### The Bayesian consequence is exactly pairwise

Treat $L$ and $P$ first as the two fully specified mechanisms with the same fixed parameters above. Finite contrasts and positive $v$ give $0<{p}_{t}<1$, so the common likelihood $q(y\mid{}D)$ in (1) is strictly positive for every finite binary sequence. Hence



$$
\frac{\mathrm{P}\mathrm{r}(y\mid{}L,D)}{\mathrm{P}\mathrm{r}(y\mid{}P,D)}=1,\quad{}\quad{}\frac{\mathrm{P}\mathrm{r}(L\mid{}y,D)}{\mathrm{P}\mathrm{r}(P\mid{}y,D)}=\frac{\mathrm{P}\mathrm{r}(L\mid{}D)}{\mathrm{P}\mathrm{r}(P\mid{}D)},
$$



(5)

provided both model prior probabilities conditional on $D$ are positive. The observed answers give no differential likelihood information between this pair. Unequal prior odds remain unequal. Under the common exogenous joint-design assumptions, the corresponding integrated likelihoods also agree wherever the common likelihood is defined and positive.

If the labels instead denote composite models with unknown parameters, pointwise equivalence does not license arbitrary prior averaging. Matching priors on the paired parameters, or more generally matching induced prior distributions of the observable response law, preserves equal marginal likelihoods. Different parameter priors can give different marginal likelihoods. Equation (5) does not assert otherwise.

In a larger hypothesis set, both models can gain posterior probability at the expense of worse-predicting alternatives while their mutual odds stay fixed. Other observations can change those odds, and prior plausibility or justified theoretical restrictions can favour one mechanism. Failure of unique identification therefore does not establish equal overall warrant or exclude all abductive support. No Bayesian reanalysis of empirical data is being claimed.

### What the result establishes

Even full announcer-conditioned output curves and the complete sequence law under a specified design can leave the contribution of one member unidentified. The counterexample preserves both latent sensory capacities across the two models and does not depend on adding integration noise. Its force is precisely the difference between an output law and a uniquely determined causal explanation of that law. Deciding among mechanisms requires further assumptions or evidence that distinguishes them; the construction does not decide what an actual group did.
