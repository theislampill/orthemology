# Plotkin–Abadi: exact logical strength and Church iterator specialization

## Result

The useful comparison is relational naturality in an *added logic over System F*. It does not supply a System F proof term, much less an inhabitant of another source calculus's identity type. The Church iterator argument below is a complete independent reconstruction; it is not presented as an omitted proof recovered from the paper.

## Verified primary source and citation map

- Gordon Plotkin and Martín Abadi, *A Logic for Parametric Polymorphism*, TLCA 1993, LNCS 664, published pp. 361–375; DOI https://doi.org/10.1007/BFb0037118.
- Author-hosted text: https://www.dcs.ed.ac.uk/home/gdp/publications/Par_Poly.pdf, linked by https://homepages.inf.ed.ac.uk/gdp/publications/pubs.html.
- Identical mirror: https://www.cs.ru.nl/~freek/courses/tt-2016/papers/plotkin_abadi.pdf.
- Both downloads SHA-256: `6bf2ffd5585fb8997be6212ffdb013588c411d0b0243dee162a46dbc4c0723b0`.
- This author version has 16 unnumbered PDF pages; references below use one-based PDF pages, not guessed proceedings page numbers.

Source landmarks: §2 pp.3–5 defines formula equality, definable relations, relational instantiation, βη/congruence, and the parametricity axiom. Lemmas 1–2, p.6, state Identity Extension and Logical Relations; Lemma 3, §2.1 p.7, is the Graph Lemma. §2.2 p.8 actually derives dinaturality. §3.4 p.12 states Theorems 8–9 (initiality and least-relation characterization), without their proofs. §1 p.2 explicitly warns that proofs are generally omitted. The p.13 induction display has the defect analyzed below. §2 p.5 mentions a PER interpretation with double-negation-closed relations; the presented syntax has no separate admissibility side condition.

## 1. Formal premises, normalized and type-correct

The following mathematical ledger transcribes the relevant content using normalized names. A few printed typographical problems are noted separately below.

### 1.1 Types, formulae, and definable relations

Object types and object terms are those of System F:

    T ::= X | T → T | ∀X.T
    t ::= x | λx:T.t | t u | ΛX.t | t T

Equations `t =_T u` are **formulae** of a distinct logic, with consequence judgment `Γ ⊢_{E;G} φ`. They are not a constructor `Id_T(t,u)` of the displayed object-type grammar. The environments track well-typed terms and well-formed relations; all substitutions avoid capture.

Any well-formed formula φ(x,y), including formulae with other permitted parameters, forms a definable binary relation:

    ρ := (x:A, y:B).φ(x,y)  ⊂ A × B.

Here `⊂ A × B` describes the relation's source and target. It does not require a source-language pair or subtype object. Define

    eq_A(x,y)  :⇔ x =_A y
    Graph(h)(x,y) :⇔ y =_B h x,       for h:A→B.

The rule for universal relational elimination permits substituting **any well-formed definable relation**:

    Γ ⊢ ∀R⊂A×B.ψ[R]       E;G ⊢ ρ⊂A×B
    ------------------------------------------------
                       Γ ⊢ ψ[ρ].

Universal introduction has the usual freshness condition: a bound variable cannot occur in undischarged assumptions. This is formula-level relation comprehension/substitution, not an object-language subtype-comprehension rule.

### 1.2 Logical relation interpretation

For ρ⊂A×B and σ⊂C×D, the type-correct arrow clause is

    (ρ ⇒ σ)(f,g) :⇔ ∀a:A.∀b:B. ρ(a,b) ⇒ σ(f a,g b).

A type expression acts on relations recursively:

    X_i[ρ_1,...,ρ_k] = ρ_i
    (U→V)[ρ] = U[ρ] ⇒ V[ρ]
    (∀X.U)[ρ](u,v)
      :⇔ ∀A.∀B.∀R⊂A×B. U[ρ,R](u A,v B).

The source PDF p.4 writes one domain annotation in the first display as A′; the surrounding declared types show that the right argument must range over B. The normalized clause above is well typed.

### 1.3 The added parametricity schema

For a System F type expression T[X,Y_1,...,Y_k], the schema is equivalently:

    ∀Y_1...Y_k. ∀u:∀X.T[X,Y].
      ∀A.∀B.∀R⊂A×B.
        T[R,eq_Y_1,...,eq_Y_k](u A,u B).

Without parameters:

    ∀u:∀X.T[X]. ∀A.∀B.∀R⊂A×B. T[R](u A,u B).

This is a universally quantified **axiom in the logic**, so it applies to an arbitrary variable u of the polymorphic type. That is stronger than merely knowing that closed definable System F terms satisfy a metatheoretic abstraction theorem.

### 1.4 Equality and extensionality resources

The logical equality axioms include reflexivity and substitution into binary relations:

    R(x,y) ∧ x=x′ ∧ y=y′  ⇒ R(x′,y′).

Together with definable-relation substitution, these provide ordinary equality reasoning. The logic also has β for term and type application, both η equalities, and these congruence schemas:

    (∀x:A. t =_B u) ⇒ (λx:A.t) =_{A→B} (λx:A.u)
    (∀X. t =_B u) ⇒ (ΛX.t) =_{∀X.B} (ΛX.u).

Consequently it supports logical function extensionality and polymorphic extensionality:

    (∀x. f x = g x) ⇒ f = g
    (∀X. u X = v X) ⇒ u = v.

These are equalities in the logic. They cannot simply be treated as definitional reduction or transported into an unrelated intensional identity type.

### 1.5 Lemmas invoked by the written p.8 proof

Identity Extension (Lemma 1):

    T[eq_X_1,...,eq_X_k](u,v) ⇔ u =_T v.

Logical Relations (Lemma 2): if `X, x_1:T_1,...,x_m:T_m ⊢ t:U` is a System F typing derivation, then the logic proves

    (∧_i T_i[R](a_i,b_i)) ⇒ U[R](t[A,a],t[B,b]).

Lemma 2 is stated to need no parametricity schema. Crucially, its hypotheses include the relations for **every free term variable**. It does not, on its own, remove the relational hypothesis for an arbitrary polymorphic variable.

A dependency check for Identity Extension can be reconstructed by induction on T. At a variable it is the definition of eq. At an arrow, specialize the related-input premise to identical inputs, invoke the induction hypothesis on the codomain, and use function extensionality; the converse follows by equality substitution and the induction hypotheses. At ∀X.U, specialize the quantified relation to eq_X to obtain pointwise equality, then use polymorphic extensionality. For the converse at ∀, the parametricity schema supplies self-relatedness of an arbitrary polymorphic value, which equality substitution transports to an equal value. Thus the lemma is not being silently treated as an axiom-free property of arbitrary logical-relations semantics.

The separate Graph Lemma (Lemma 3) says that for a type constructor with only negative occurrences of variables V and only positive occurrences of W,

    Graph(T[f,g]) = T[Graph(f)^op,Graph(g)],

where equality of relations means pointwise equivalence. This is not the lemma explicitly invoked by p.8's proof.

## 2. Complete expansion of the p.8 dinaturality calculation

This section expands the mathematical derivation in §2.2, making the variable assignments and elementary relation checks explicit. Let T[V,W] have V only negatively and W only positively; consider the no-extra-parameters case treated there.

Data:

    u : ∀Z.T[Z,Z]
    h : A → B
    G := Graph(h) ⊂ A×B.

The sign condition supplies the definable System F map operation

    T[p,q] : T[V,W] → T[V′,W′]
      when p:V′→V and q:W→W′.

1. Instantiate the parametricity axiom for u at A, B, G:

       T[G,G](u A,u B).

2. Form the two arrows to the common codomain T[A,B]:

       L := T[id_A,h] : T[A,A] → T[A,B]
       M := T[h,id_B] : T[B,B] → T[A,B].

3. Check the two input relations required by the Logical Relations Lemma for the map operation:

       (eq_A ⇒ G)(id_A,h)
       (G ⇒ eq_B)(h,id_B).

   For the first, a=a′ entails h(a′)=h(a). For the second, b=h(a) entails h(a)=b. These use equality substitution/symmetry and the definition of G.

4. Apply Lemma 2 to the System F term defining the map operation. Its source-variable relations are G,G; its target-variable relations are eq_A,eq_B. Step 3 supplies the hypotheses for the negative and positive map arguments. The result is

       (T[G,G] ⇒ T[eq_A,eq_B])(L,M).

5. Apply this arrow relation to step 1:

       T[eq_A,eq_B](L(u A),M(u B)).

6. Identity Extension converts step 5 to

       T[id_A,h](u A) =_{T[A,B]} T[h,id_B](u B).

7. Generalizing u and using logical function extensionality yields the displayed equality of evaluation composites:

       eval_A ; T[id_A,h] = eval_B ; T[h,id_B].

Dependencies: definability of G and relational ∀ elimination; the parametricity schema for u; the syntactically defined map and its sign condition; Logical Relations with all free-variable premises discharged; Identity Extension; and congruence/η if packaging the pointwise result as equality of maps. No induction over Church numbers occurs. No premise asserts an object-level identity witness.

The earlier, more general dinaturality display on p.8 has inconsistent A/B lettering. The subsequent simpler statement and the typed calculation above are the usable, internally coherent proof.

## 3. Independent reconstruction: Church iterator graph naturality

This shorter specialization is *our derivation*, not a Church-number theorem explicitly printed in the source.

Set

    N := ∀X.(X→X)→X→X.

Suppose

    n:N,  A,B types,
    f:A→A,  g:B→B,  h:A→B,
    ∀a:A. h(f a) = g(h a).

Let G(a,b) mean b=h a.

1. For arbitrary a,b with G(a,b), equality substitution gives

       g b = g(h a) = h(f a),

   so G(f a,g b). Thus `(G⇒G)(f,g)`.

2. The parametricity schema instantiated for n gives

       ((G⇒G) ⇒ (G⇒G))(n A,n B).

3. Apply step 2 to the related step functions f,g. Then apply the resulting arrow relation to the related bases a,h a (related by reflexivity):

       G(n A f a, n B g(h a)).

4. Expand G and use symmetry if desired:

       h(n A f a) = n B g(h a).

This is the iterator algebra-homomorphism/naturality equation. No Identity Extension invocation and no function extensionality are needed for this **pointwise equation**, because the chosen relation itself ends in equality. The graph must nevertheless be available among the relations over which n is parametric.

Define

    fold(A,f,a) := λm:N. m A f a.

If h a=b, the pointwise equation gives

    h(fold(A,f,a) n) = fold(B,g,b) n.

Only when upgrading this to

    fold(A,f,a) ; h = fold(B,g,b)

does the presented derivation use function extensionality. Beta conversion and equality substitution normalize these displays.

## 4. Independent reconstruction: reification and initiality

Define the standard f-first Church constructors:

    zero := ΛX.λf:X→X.λa:X.a
    succ := λm:N.ΛX.λf:X→X.λa:X. f(m X f a)
    reify(n) := n N succ zero.

### 4.1 Reification identity

Fix arbitrary X,f:X→X,a:X. Let

    k := fold(X,f,a) : N→X.

By β equalities:

    k zero = a
    ∀m:N. k(succ m) = f(k m).

Apply §3's graph naturality to n with source algebra `(N,succ,zero)`, target `(X,f,a)`, and h=k:

    k(reify(n)) = n X f a.

Expand k:

    reify(n) X f a = n X f a.

The logical equality rules now abstract over a, then f, then X; the η equalities identify the η-expansions. Hence

    reify(n) =_N n.

This last step is extensional. It is not a β computation for an arbitrary variable n. The only self-parametricity used is that of this arbitrary n, supplied by the added schema.

### 4.2 Existence and uniqueness of the fold map

For an algebra X,f,a, the term fold(X,f,a) satisfies zero and successor equations by β. Suppose h:N→X also satisfies

    h zero = a
    ∀m:N. h(succ m) = f(h m).

Apply §3 to n with source `(N,succ,zero)` and this h:

    h(reify(n)) = n X f(h zero) = n X f a.

Use reify(n)=n to get

    h n = fold(X,f,a) n.

Function extensionality yields h=fold(X,f,a). Thus there is exactly one map obeying the algebra equations **up to the logic's equality**.

This is initiality for the one-zero/one-successor algebra signature, equivalently the usual 1+X algebra presentation once the appropriate product/sum encoding results are in place. It is not yet a source-dependent elimination term.

## 5. Independent reconstruction: logical unary Church induction

For any well-formed logical predicate formula P(m) on N, assume

    P(zero)
    ∀m:N. P(m) ⇒ P(succ m).

Define the permitted binary relation

    R(u,v) :⇔ P(u).

Then R(zero,zero), and `(R⇒R)(succ,succ)`: the latter follows directly from the successor closure of P and does not require anything about v. Parametricity of n:N instantiated at N,N,R gives

    R(n N succ zero, n N succ zero),

hence P(reify(n)). Equality substitution along §4's logical reification identity gives P(n). Generalize n.

This construction demonstrates logical unary induction for this particular Church-number signature. It should not be cited as a theorem explicitly proved in the PA paper. It also does not supply `Πn:N. P(n)` as an object term when P is a dependent **type family** in some source theory. Moving from a logical formula theorem to that dependent type inhabitation requires a separately established interpretation/reflection.

## 6. Source typo and safe use of Theorems 8–9

The PDF scan, not merely extracted text, confirms that §3.4 p.13 prints an off-diagonal conclusion of the form

    closure(ρ) ⇒ ∀x,y:μF. ρ(x,y).

As printed, this cannot be the consequence of Theorem 9 and Identity Extension. Their combination instead gives

    closure(ρ) ⇒ ∀x,y:μF. (x=y ⇒ ρ(x,y)),

or equivalently the diagonal version

    closure(ρ) ⇒ ∀x:μF. ρ(x,x).

Diagnostic countercheck: taking ρ to be equality, the closure premise follows from Identity Extension for F and congruence of `in`. The printed off-diagonal conclusion would then identify every pair of elements of μF, including distinct Church numerals in a parametric model. The diagonal correction does not do that.

The source also says that it does not obtain the expected *general* unary induction schema for arbitrary positive A[Z]. Do not extrapolate that remark into a claim that §5's direct Church-number logical induction is impossible. Conversely do not use §5 to assert that the general unary relational-lifting induction issue is settled.

## 7. Comparison boundary and assumption ledger

| Conclusion | Extra resources used here | What it does not establish |
|---|---|---|
| Pointwise Church iterator naturality | Self-parametricity of n over a graph relation; well-formed graph substitution; equality reasoning | Internal parametricity from arbitrary source typing alone |
| Equality of folds as functions | Previous row plus congruence/η extensionality | Definitional equality of open terms |
| `n N succ zero = n` | Graph naturality plus term/type extensionality | Source `Id(reify(n),n)` inhabitation |
| Church initiality | Previous row, β algebra equations, graph naturality for candidate h, function extensionality | Dependent source eliminator |
| Logical Church induction | Predicate-definable relation, n's parametricity, logical reification equality, equality substitution | Object-level induction proof term without interpretation |
| General p.8 dinaturality | Added schema + Logical Relations + Identity Extension; sign-respecting definable map | An axiom-free derivation in System F's term calculus |

No unrestricted set-theoretic full-comprehension model is assumed by this derivation. Syntactically, the PA logic permits all well-formed definable relations. A semantic transfer must show that each graph or predicate relation used is among the model's allowed relations. In settings with admissibility restrictions, graph-admissibility and predicate-admissibility are new proof obligations; the total System F presentation itself has no domain-theoretic fixpoint rule or admissibility test.

The fundamental distinction for a source judgment such as `HasE Γ n NatE` is that the PA logical schema is an additional premise of the target reasoning system. Lemma 2 alone retains relational hypotheses for open variables. To conclude a source identity inhabitant, one needs a proved translation and an adequate internalization/reflection result (or a source-level parametricity witness with the needed elimination principles). None is supplied just by citing this paper.

## Materials inspected

- Complete 16-page author version obtained and extracted; relevant §§2, 2.1, 2.2, 3.4 read in full.
- Visual inspection of PDF pp.5, 8, 13 to check axioms, the actual dinaturality derivation, and the induction display.
- Local files: `Par_Poly-author.pdf`, identical `plotkin_abadi.pdf`, text extraction `plotkin_abadi.txt`, and page renders `page-05.png`, `page-08.png`, `page-13.png`.

No project source files were inspected or modified.
