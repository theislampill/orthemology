# Bounded literature comparison: the missing Church proof principle

10 October 2026. Research and mathematical comparison only. No source grammar, conversion, compiler, predecessor evidence, repository, or certificate calculus was changed. This report introduces no source rule and declares no new source inhabitant.

## Result and constructive choice

The relevant independently specified principle is **self-parametricity of an arbitrary polymorphic value**, with well-formed graph relations available for relational instantiation. A source-facing alternative is **uniqueness of the Church recursor**, i.e. initiality of the existing zero/successor algebra. Either can supply the graph projection equations once its translation into the actual identity judgment is established. Existing `piExt`/`allExt` provide neither missing premise.

There are three materially different outcomes:

1. **Unchanged original HasE and its literal universal target:** the checked homogeneous-PER countermodel settles noninhabitation. The literature is explanatory and cannot restore an inhabitant.
2. **The existing HasC literal certificate result:** retain it as a separate positive result. Nothing below imports HasC into HasE, weakens the countermodel, or asserts a HasC proof of universal W without a separate source derivation.
3. **A constructive investigation without new source rules:** formulate recursor uniqueness as an explicit hypothesis using the existing All/Pi/Id language and derive a conditional consequence. Discharging that hypothesis for every original Church value remains a separate, impossible-in-unchanged-HasE obligation if the proposed source mapping succeeds.

The known dependent refinement method instead supplies naturality with each element of a *different, restricted domain*. It does not discharge the hypothesis for all original `n:N`. This is the principal reason not to treat that method as completion of the literal old target.

## Exact local boundary

Read in full: `homogeneous-per-model-20261010/{RESULT,FOLLOW_ON_SCOPE,MATHEMATICAL_CONSTRUCTION}.md`, `hase-internal-graph-20261010/RESULT.md`, and `hase-graph-bridge-assembly-20261010/RESULT.md`. The latter two retain their earlier historical OPEN wording; the later noninhabitation result supersedes that status, not their positive derivations.

The exact original graph data are:

- S = Sigma N N, with original diagonal step Delta and seed z0;
- G = Sigma s:S. Sigma x:A. Id_A(x, snd(s) f a);
- graph step g and seed b, with all four projection/step/seed computations checked;
- r = n g b, with an actual source inhabitant of Id_A(fst(snd r), snd(fst r) f a).

The two formed bridge types are

    Id_S(fst(n g b), n Delta z0)
    Id_A(fst(snd(n g b)), n f a).

The retained assembly theorem consumes **HasE derivations** of these types and returns the exact literal `HasE [] c3 (W originalQ)`. A theorem in some other logic, a semantic relation, or a derivation in another calculus does not meet those premises merely because its displayed endpoints match.

The new countermodel has one erased semantic value nu whose behavior depends on the seed's atom/function tag. It validates all actual HasE rules, including both extensionality rules, but violates the scalar bridge. This establishes a sharper local fact than observing that raw Church reduction lacks a fusion law.

## What the primary literature actually supplies

### Plotkin–Abadi, 1993

[A Logic for Parametric Polymorphism](https://www.dcs.ed.ac.uk/home/gdp/publications/Par_Poly.pdf), TLCA 1993, DOI 10.1007/BFb0037118. References here use the author's 16-page PDF.

Section 2, pp.3–5, adds a **logic over System F**, including definable-relation substitution and a universal relational-parametricity schema. It applies to an arbitrary polymorphic variable. Equality is a formula of that logic, not a System F identity type. The written §2.2 p.8 dinaturality proof instantiates parametricity with a function graph, applies Logical Relations, then Identity Extension. Its stated initiality theorem (§3.4, Theorem 8) has no proof there. The independent Church specialization below avoids importing that unprinted proof. The p.13 binary-induction display is overstrong as printed; taking the relation to be equality diagnoses the issue. It is not used.

Full relevant assumptions, p.8 proof expansion, source-scan checks, and clearly labelled independent reconstructions are in `plotkin-abadi/research.md`. The Logical Relations lemma alone retains relation hypotheses for free variables; it does not create self-parametricity for an arbitrary source Church variable.

### Wadler, 1990, revised 2008/2014

[Recursive types for free!](https://homepages.inf.ed.ac.uk/wadler/papers/free-rectypes/free-rectypes.txt), especially “Least fixpoints as initial algebras” and “Iterators and recursors.”

The complete argument distinguishes weak initiality, supplied by the encoded fold's computation, from uniqueness. His law (3) is preservation of algebra morphisms by fold. It implies self-fold identity using term/type eta, hence initiality. He expressly separates that law from polymorphic reduction and explains the additional identity-extension requirement behind a relational free-theorem argument. The recursor section then derives a projection identity by specializing the algebra-morphism law. This is the ordinary Church-encoding analogue of the current graph gap, not a proof in the actual dependent HasE grammar.

### Awodey–Frey–Speight, 2018

[Impredicative Encodings of (Higher) Inductive Types](https://www.contrib.andrew.cmu.edu/~awodey/preprints/impred.pdf), LICS 2018, DOI 10.1145/3209108.3209130, §§2 and 4.2, equation (4.5), Theorem 4.2.

Their small-set encoding is a subtype of the unrestricted Church encoding, pairing each iterator with algebra-morphism naturality evidence. The complete eta proof applies that stored evidence first to a fold map, establishing reification, then to an arbitrary algebra morphism, establishing uniqueness. It uses function extensionality and proof-irrelevant subtype fibers. Their setting has an impredicative universe, strong Sigma, identity types, and a hierarchy supporting the set subuniverse. The article cites a separate initiality-to-dependent-elimination result; that external theorem is not imported here. In particular, their proof never manufactures the stored evidence for every unrefined Church value.

### Geuvers, 2026: a useful non-transfer

[Non-Derivability Results in Polymorphic Dependent Type Theory](https://doi.org/10.4204/EPTCS.441.9), EPTCS 441, pp.148–165, published 4 March 2026. [Official proceedings](https://cgi.cse.unsw.edu.au/~eptcs/Published/LTT2026/Proceedings.pdf), PDF pages 158–175.

Sections 3–5 construct polyset models for lambda-P2 and an identity/Sigma/UIP extension. Lemma 5.9 explicitly refutes FunExt: two boolean maps agree at every admitted boolean, but their function identity is empty. Lemma 5.10 and Theorem 5.11 give induction nonderivability in the stated extension. Consequently that model cannot certify HasE soundness: HasE has the relevant function extensionality rule. His identity interpretation also forces equality of endpoints in the underlying untyped algebra; the current HasE interpretation uses endpoint PER-relatedness. No named allExt or Raw/proofErase counterpart was identified in that paper. Shared notation does not provide an embedding.

The parent separately checked the continuous Lemma 4.2–Theorem 5.11 passage. That is a contextual participating check, not an independent whole-paper review.

Rummelhoff's *Polynat in PER models* (2004) was located bibliographically, but a full primary text was not obtained in this bounded pass. No construction or transfer is claimed from its abstract. The foregoing read proofs already establish the relevant historical distinction; no field-novelty claim is needed.

## Complete independent graph specialization

This is our mathematical specialization, not a source derivation or a quotation of an omitted literature proof.

For an arbitrary n of Church type, self-parametricity at A, B and a relation R says:

    ((R => R) => (R => R))(n_A, n_B).

Let h:A→B and define R(x,y) by Id_B(h x,y), in a reasoning system where such graph relations and equality substitution are available. Suppose

    e(x): Id_B(h(f x), g(h x))
    e0: Id_B(h a,b).

For any R(x,y), congruence of g followed by e(x) gives R(f x,g y). Thus f and g are R-related endomorphisms. Parametricity applied to those steps and then the R-related seeds gives R(n_A f a,n_B g b). Expanding R yields

    Id_B(h(n_A f a), n_B g b).

No Church-number induction occurs. No separate Identity Extension or extensionality invocation is needed for this pointwise graph equation: the chosen relation already ends in identity. Extensionality is needed if it is repackaged as equality of functions. The unresolved source obligations are availability of the relation principle and production of a typed identity witness, not the displayed four-line inference.

For the existing bridges use respectively:

    A=G, B=S, h=fst, f=g, g=Delta, a=b, b=z0;
    A=G, B=scalar A, h=fst∘snd, f=g, g=scalar f, a=b, b=scalar a.

Names on each side of these assignments denote the appropriate local source/target data; the already checked projection equations supply e and e0.

There is also a shorter direct application with source carrier S, target scalar A, map h(s)=snd(s) f a, steps Delta and f, seed z0, and h(z0)=a. This uses the retained `image_delta` and original-compiler computation. It avoids constructing the graph iteration again. Its full source typing and identity evidence still have to be proved in the calculus being used.

## Independently specified source-facing candidate: recursor uniqueness

In mathematical binder notation, using **the original N and original constructors**, consider the following proposition. This is a specification of a possible explicit hypothesis, not a new rule or a supplied inhabitant:

    All A.
    Pi a:A. Pi f:(A→A). Pi u:(N→A).
    Id_A(u zero,a) →
    (Pi k:N. Id_A(u(succ k), f(u k))) →
    Id_(N→A)(u, λk.k f a).

It uses only existing kinds of type constructors. Its fully indexed `Ty` expression, formation, and source proof manipulations were not checked by this research pass.

Why this supplies fold transport, independently of assuming fusion:

1. The original Church computation shows `fold(f,a)(zero)=a` and `fold(f,a)(succ k)=f(fold(f,a)(k))`.
2. Set u(k)=h(k f a). The commuting-square and seed evidence give u's zero and successor equations for target algebra (B,g,b).
3. Apply recursor uniqueness at that target algebra to obtain Id_(N→B)(u,fold(g,b)).
4. Identity congruence at n gives the desired fold-transport identity.
5. Specialize twice to the projection algebras above, then reconstruct the retained assembly derivation in the context containing the uniqueness hypothesis.

This is not asserted to be the weakest possible principle. It is independently specified by the constructor algebra, has a complete mathematical implication to the required transport, and does not use the desired fold law as its own premise.

A suggested binder ledger for a formal investigation uses a,f,u,e0,es in that order. At the final conclusion, indices are es=0, e0=1, u=2, f=3, a=4; the fold endpoint is `abstract (app (app (var 0) (var 4)) (var 5))`. This ledger remains unverified. It is supplied to the separate source worker solely for a formation/feasibility check.

## Intended semantics and the remaining mapping obligations

The actual paired semantics already supports the requisite *semantic* graph relation. In `P01PER.lean`, a Link has supported endpoints and respects endpoint PER equality. In `AllPredicates.lean`, F_all explicitly requires each endpoint to preserve every P,Q,Link; G_all carries heterogeneous preservation. Thus, for a supported h:P→Q, define

    R_h(x,y) := P(x,x) and Q(h x,y).

The typed h makes this a respectful Link. The commuting square and g's respect prove step preservation; the seed identity proves seed relatedness. N's actual uniformity clause gives Q(h(n f a),n g b). The current identity interpretation then admits I semantically. This directly explains compatibility with the intended relational interpretation; it is not a soundness-to-typing converse.

The uniqueness candidate also has an independent intended-model justification. In the retained full-PER setting, use its carrier-specific Church standardness theorem: external induction on the representing numeral shows any supported u satisfying the two constructor equations agrees with the fold at every N element. PER function equality then proves uniqueness. In the paired relational setting, apply graph preservation to each evaluation fold to show that n N succ zero and n agree at every carrier/step/seed; semantic extensionality gives their equality at N. Apply graph preservation again to an arbitrary algebra morphism u and replace that reification by n. This proves the candidate uniqueness property mathematically. A compiled rule-soundness theorem, with its actual source evidence and all context obligations, is still absent from this research pass.

Before any stronger source proof principle is adopted, all of the following remain explicit obligations:

1. **Actual syntax and formation.** Bind the exact original zero, successor, N, compiler, contexts, substitutions, scopes, All/Pi/Id types, and proof polynomials. No type-indexed semantic operation may replace the erased source polynomial.
2. **Open-value strength.** Supply a principle for an arbitrary `n:N`, not only closed definable numerals or a metatheoretic family of proofs indexed by closed terms.
3. **Relation language.** PA quantifies over binary relations; HasE has no such primitive relation-variable binder. A full PA translation is not provided by All alone. A graph-specific internal type or the uniqueness proposition avoids naming a new relation syntax, but does not supply its inhabitant.
4. **Dependent carriers.** The actual graph type has Sigma and an identity depending on s,f,a. Ordinary System F theorems do not directly cover that syntax. At a fixed semantic environment it is a carrier PER; that observation is semantic only.
5. **Identity evidence.** Translate logical equality to a typed source Id derivation, with formed J motives. Semantic endpoint-relatedness or an extensional equality of erased terms is insufficient. No completeness/reflection rule is available.
6. **Substitution and contextual stability.** Any new proof contract must survive source term/type substitution and type instantiation at these context-dependent carriers, including the allExt and proofErase cases if a whole calculus is proposed.
7. **Intended-model preservation.** Check the exact rule's unary and heterogeneous soundness in the chosen intended interpretation. The graph argument supports a candidate; it is not a verified soundness theorem for an unspecified successor.
8. **Assembly transport.** A new judgment is not HasE. Either derive a conditional in unchanged HasE with an explicit hypothesis, or prove inclusion and reassemble the proof in a separately named extension. Never feed a foreign proof into the existing HasE-only theorem by assertion.
9. **Literal target and prior positive result.** Preserve originalQ, W and c3. Preserve the separate HasC certificate theorem, and the established failure of a type-preserving all-closed HasC→HasE translation.

## Rejected shortcuts

- A full-PER validation is not a source inhabitant, nor a carrier-independent theorem about every PER model.
- “All closed Church terms are standard” does not quantify over every element of an arbitrary model's N, and yields no uniform proof for a source variable.
- The same erased term having two typings does not supply a cross-carrier graph identity.
- Graph formation, graph-invariant iteration, and J transport along an already supplied identity do not create the projection bridges.
- Adding proof irrelevance or citing a model with it does not repair the missing graph preservation; the current separation already uses I-supported identity evidence.
- Replacing original N by a naturality/induction-certified subtype changes the quantified domain. A forgetful map to N does not provide a section on all original N; such a section with the required projection law would recreate the missing uniform principle.
- A finite literal HasC certificate does not establish general internal parametricity or an inclusion between the two source calculi.

## Verification status

This is a source-bound research comparison, with complete written mathematical implications and explicitly unproved source mappings. It is not a Lean formalization or an independent replay of predecessor certificates. Source downloads and fingerprints are recorded in `SOURCES.json`. The separate PA note contains detailed reading evidence; the externally useful report is this bounded synthesis, not the raw source excerpts.
