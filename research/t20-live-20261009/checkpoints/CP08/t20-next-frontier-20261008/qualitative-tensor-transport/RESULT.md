# Finite predicate-functor transport into Boolean tensors

8 October 2026. Scratch research, T20 active. No integration, repository mutation, metaphysical adjudication, or closure.

## Result first

There is an exact, basis-declared transport of the finite extensional predicate-functor semantics into Boolean-semiring coefficient tensors. It preserves the source's actual mixed-arity conjunction, first-coordinate existential projection, leading padding, permutations, identity, and shared-variable identification. Negation requires either pointwise Boolean complement or an explicitly different truth-wire tensor representation. The bare positive tensor operations cannot manufacture complement from a single truth coefficient.

The inherited real graded-tensor framework supplies the representation interface, augmentation contraction, and information-fibre criterion. It does **not** already identify its arithmetic contraction with existential truth. Natural-number or nonnegative-real contraction sums weights. Taking support gives the Boolean positive fragment exactly, but loses counts/weights. Signed-real support fails under cancellation. These are standard semiring facts, not new general theorems.

One source detail must remain visible. The printed Appendix declares all permutation terms arity-preserving, but its unrestricted unary iota satisfaction clause literally accesses the second coordinate; sigma at arity zero is also not specified by its displayed indexing formula. Our theorem uses the explicit conventional completion that both permutations act as identity below arity two. It agrees with every well-typed displayed clause. A faithful arity-indexed model of the *literal uncompleted* unary clause is impossible. This is a local typing boundary, not a refutation of predicate-functor logic or of the source's metaphysical proposal.

The transport does not establish that qualitative universals are identical with their extensions, that a fact obtains, that logical implication establishes metaphysical priority, or that a productive resource has or lacks a bearer. It also does not collapse indiscernible but numerically distinct model elements.

## 1. Inputs, exact reuse, and scope

### Primary source read

Dasgupta, *Individuals: an essay in revisionary metaphysics*, Philosophical Studies 145 (2009), 35–67, DOI [10.1007/s11098-009-9390-x](https://doi.org/10.1007/s11098-009-9390-x), author's [journal PDF](https://www.shamik.net/papers/dasgupta%20individuals.pdf). This operation read section 3 (printed pp. 49–56) and the complete Appendix (pp. 62–66) from the retained layout extraction. Page images 56, 63 and 64 were inspected for the functor glyphs, arities, and sequence clauses. The image shows Greek sigma and iota: the extraction's `r` and `ı` are not reliable typography. We write sigma and iota below. Section 3.3's exact example is at pp. 55–56, including notes 32–33.

The source characterizes the property-domain interpretation before borrowing model-theoretic semantics from predicate-functor logic. Its p. 63 property-identifying biconditional is expressly not mere material equivalence. Consequently an extension table in a chosen finite model is a representation of its comparison semantics, not a proof that a universal is a set or that extension equality establishes property identity. We do not reprove Quine/Kuhn expressibility or claim a new completeness theorem.

### Inherited mathematical interface verified at the current pin

The relevant original is *Graded Representations, Witnessed Revision, and Inquiry Landscapes*, version 1, at `theory/lineages/h-formalisation/orthing_formalisation_v1.md`. It was fetched read-only at current research commit `3a0bdeaa1394c656245cae9599adcb143e885059`. Its blob `c094a9c44fae26484426df67ac5afd9e2190eb4d` and SHA-256 `cd5070341a46658c0e4ac2c077d343d276cf16e50f0305f61ebb90ba0b624c2e` equal the preserved historical binding at commit `fd0903d99d657c35e32fddcc8864d2a77930cf40`. Exact length is 93,523 bytes and 1,157 lines. [Pinned source](https://github.com/theislampill/orthemology/blob/3a0bdeaa1394c656245cae9599adcb143e885059/theory/lineages/h-formalisation/orthing_formalisation_v1.md).

Sections 2–6 and the section 11 quotient interface were read directly. Exact reuse is:

- Definition 2.1 fixes the scalar field, role spaces, observables, extraction, and permitted representation changes. Changing from real vector spaces to Boolean semimodules changes this declaration; it is not a hidden identification.
- Section 3 uses the algebraic direct sum of typed tensor powers. Its multiplication concatenates factors. It explicitly warns that semantic composition need not be this multiplication and that multi-degree forgets order.
- Proposition 4.1 encodes an injectively atomized finite record. This proves that a record can be retained. It does not show that a chosen encoding intertwines these predicate-functor operations. That intertwining is the missing test executed here.
- Theorem 4.2 and Corollary 4.3 say exactly that a target is preserved iff it is constant on every retained-record fibre. These supply the entire generic impossibility argument for the source's separated-existence record. We only supply the source-specific record and pair; there is no new factorisation theorem.
- Theorem 5.1 uses signed differences of nonnegative probability tensors, with augmentation contraction erasing parity. This is inherited mathematics. We do not rerun parity, count it as a discovery, or pretend the source's three existential assertions are literally that proper-marginal example.
- Section 6 supplies covector contraction and makes the chosen basis/augmentation substantive. Counterexample 6.3 rejects automatic semantic preservation by contraction. Proposition 6.2 excludes a nonzero real covector invariant under all basis changes. Our basis boundary is a direct application.
- Theorem 11.2 concerns descent of specified dynamics, observables, and landscapes. No dynamics or landscape is asserted in this finite semantic transport, so the theorem is not repackaged as a metaphysical conclusion.

The later 12-page *Information, Composition, and Self-Revision* is a different source. Its sections 1–3 were also consulted: equation (1) repeats the fibre criterion, and equation (12) already states that a nonnegative marginal's support is the projection of its support. The prior `historical-mathematical-transport` and `productive-identifiability/RESULT.md` were inspected for reuse boundaries. The latter's incidence histogram, joint-output inversion, and occurrence alias controls do not already perform this predicate-functor map. No new stochastic identification or sampling result is claimed.

### Established external ancestry

Green, Karvounarakis, and Tannen's [*Provenance Semirings*](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf), PODS 2007, §3, directly defines coefficient-valued relations, sum projection, product join, and renaming; Proposition 3.5 gives commutation with semiring homomorphisms. The definitions, Boolean/bag examples, and that proposition were read. These support the positive-algebra ancestry; they are not credited to this operation. Negation is outside that positive signature. Kuhn's 1983 article was located bibliographically, but publisher full-text/PDF opens did not return the article; we do not claim to have verified its low-arity convention. Our primary semantic source remains the pages of Dasgupta actually read.

## 2. Exact finite declaration

Fix a finite **nonempty** domain D, retaining every model element as a distinct index, and let B = ({0,1}, OR, AND, 0,1). For n >= 0 put

    T_n(D;B) = {T : D^n -> B},       D^0 = {()}.

These are finite free Boolean semimodule tensor powers, identified through the specified basis indexed by D. Grade zero is one Boolean scalar. A relation A subset D^n has characteristic tensor chi_A, with entry 1 exactly on A. The inverse reads its support. Thus the map is a bijection on the relations of each grade. It is not injective on syntactically different terms or on distinct property intensions having the same extension in this model.

All grades can be assembled in an arity-tagged family or algebraic graded direct sum. Individual finite expressions use finitely many grades. Do not complement an entire infinite graded direct sum at once: complement is defined separately in the declared finite cube D^n. A finite model signature or a finite expression's required vocabulary may be stored with relation-symbol tags. The paper's countably many atomic symbols need not all be packed into one finite-support tensor.

To instantiate this inside the inherited typed-word scheme, take a declared copy of the free space on D for each predicate argument role, retain the predicate-symbol/role tags, and supply explicit role-to-domain alignment maps. Equality across two roles tests their aligned **domain elements**, not equality of display labels. The old interaction basis `[r,v]` includes occurrence metadata; it cannot be silently replaced by a basis of qualitative values. If starting from those records, one needs a declared assignment of each role occurrence to its model element and must retain occurrence records separately whenever they remain required observables. Repeated records of the same relation tuple do not create a second model element; two distinct elements with the same label do. The theorem begins after this interpreted extraction is supplied. It proves the evaluation intertwining, not that arbitrary episode records supply that extraction or that it is metaphysically complete.

For tensors P of grade n and Q of grade m, k=max(n,m), define:

1. Negation: (not P)(a_1,...,a_n)=1-P(a_1,...,a_n), with Boolean values.
2. Source conjunction: (P & Q)(a_1,...,a_k)=P(a_1,...,a_n) AND Q(a_1,...,a_m).
3. Sigma: for n>=2, (sigma P)(a_1,...,a_n)=P(a_n,a_1,...,a_(n-1)).
4. Iota: for n>=2, (iota P)(a_1,...,a_n)=P(a_2,a_1,a_3,...,a_n).
5. c: for n>=1, (cP)(a_2,...,a_n)=OR_(a_1 in D) P(a_1,...,a_n); c is identity at n=0.
6. p: (pP)(a_1,...,a_(n+1))=P(a_2,...,a_(n+1)).
7. I: I(a,b)=1 iff a=b.

Sigma and iota are stipulated identity when n<2. This completion and its source limitation are discussed in §4. The source's p is padding, not a permutation. Its conjunction aligns initial positions and has grade max(n,m), not n+m. Padding p adds an ignored **leading** position, whereas the implicit padding for mixed-arity conjunction adds ignored **trailing** positions. Confusing these gives the wrong source example.

### Transport statement and proof

For every term of this typed finite semantics, every finite nonempty model M, and every assignment to its n slots, tensor evaluation equals the term's satisfaction value. Hence grade-zero tensor truth equals truth of the corresponding obtains sentence in the model-theoretic comparison.

Proof by structural induction. Atomic relations are characteristic tensors by definition and I is exactly equality. Complement reverses membership. Prefix-aligned products give the two conjuncts under the same assignment, including mixed arities. Sigma and iota pull back along the displayed permutations. c is 1 precisely when at least one first-slot witness satisfies the subterm. p ignores precisely the added first slot. Grade zero is the singleton empty assignment, with c retaining the scalar. These are all term constructors, so induction applies. Conversely, every coefficient is the term's membership value, and support recovers its extension. This is an exact many-sorted algebra isomorphism between finite relation extensions and Boolean arrays under these operations; it is not an isomorphism between bare tensor-algebra multiplication and the source's conjunction.

For an open n-place predicate the Appendix's notion of truth **on a model** universally quantifies the assignment: every coefficient must be 1. Fully contracting an array with c instead gives its **existential closure**. These agree for grade-zero expressions but not in general. For F={0} on D={0,1}, existential closure is true while universal model-truth of F is false. The executable `total()` helper performs existential closure, never universal truth for an open predicate. The all-assignment induction above preserves both readings when they are used correctly. It follows that truth and consequence **restricted to finite nonempty models** are preserved. This operation does not infer unrestricted first-order consequence from finite checking, does not assume the finite-model property, and does not replace the source's all-model Quine/Kuhn result.

## 3. What tensor contraction really does here

Let epsilon(e_a)=1 for every distinguished domain basis vector. Then c in positive degree is contraction with epsilon in the first factor, performed over B: its sum is OR. This gives existential projection. An arity-preserving cylindric existential operation, if desired, is p followed after c, so that (p c P)(a_1,...,a_n) ignores a_1. Dasgupta's actual c lowers arity; conflating these two conventions would change the operation.

Padding is insertion of the all-one vector u=sum_(a in D) e_a: pP=u tensor P. Permutations use the declared factor isomorphisms. Identity is the diagonal tensor delta_(a,b). Conjunction is Hadamard product after the specified lifts. It can itself be realised by a tensor product followed by equality/copy wiring, rather than pretending ordinary outer product already binds shared witnesses.

The complete slot-wiring operation is useful for making identification exact. For any map alpha:{1,...,n}->{1,...,k}, define

    (alpha* P)(a_1,...,a_k) = P(a_(alpha(1)),...,a_(alpha(n))).

This covers permutations, padding, repeated variables, and unused free slots. In either B or N its equality-network realization is

    (alpha* P)(a) = SUM_(b in D^n) P(b) PRODUCT_(j=1..n) delta(b_j,a_(alpha(j))).

For a fixed a there is exactly one b satisfying all these equalities, so the sum returns exactly the indicated coefficient. The proof works in any unital semiring. It does not require, or permit, identifying distinct elements of D with equal descriptive labels. Repeated alpha values tie occurrences to the **same** index.

For example, P(x,x) is the diagonal pullback of a binary P. Merely tracing P gives SUM_x P(x,x), a scalar, and loses the remaining x slot. Likewise multiplying independent contractions of two tensors generally loses the shared witness. The source's explicit I together with conjunction, padding, permutations, and c can enforce identification: c(P & I) at y equals P(y,y). This is an operation built from the declared source signature, not an added individuality predicate.

This factorization is a structured decomposition of semantic data, retaining common axes and equality wiring. It demonstrates that the specific separated-existence record is lossy, not that every structured decomposition is lossy. The common-domain interpretation and binding information are substantive retained structure; using them does not settle the source's complaint about primitive individuals or its proposed metaphysical priority.

## 4. Literal low-arity boundary, inspected rather than hidden

Printed p. 62 permits iota P^n and sigma P^n at every n, preserving n. Page 63 explains iota by swapping x_1,x_2, without a special low-arity clause. Page 64's satisfaction clause says to evaluate Q on (d_2,d_1,d_3,...), again without restriction. For a unary Q whose extension on D={0,1} is {0}, sequences d=(0,0,...) and d'=(0,1,...) have the same first coordinate. The literal iota clause makes the first true and the second false. It therefore cannot be represented by a function of D^1 alone. At arity zero sigma's displayed d_n uses an undefined index; page 64 also does not restate page 63's explicit c-at-zero clause.

The separate reviewer strengthened this locality check: under those literal unrestricted sequence clauses, c(iota F), syntactically grade zero, evaluates as F(d_1) and can still vary with its environment. Indeed c first prepends its witness and iota swaps that witness with the old first coordinate. This is why the typed completion is part of the theorem's hypotheses, not a convention added only after proving all-syntax correctness. It still does not identify an error in Kuhn's own system or rule out a tacit intended convention in this presentation.

The appropriate bounded response is to state the typed completion: permutations act trivially on arities below two, and c fixes scalars. Then every displayed clause in its natural arity range commutes with the array operations. Alternatively restrict permutation terms to their well-typed arities. We do not silently announce the literal Appendix fully implemented. This is a presentational edge-case limitation, with an executable unary failure witness, and does not touch the binary orientation or plurality examples. No claim is made that Kuhn's original system has this deficiency.

## 5. Numerical transport: what survives, what changes

### Positive N and nonnegative real coefficients

Set s(x)=0 if x=0 and 1 if x>0. On N, and on nonnegative real numbers with exact finite arithmetic, s preserves 0,1, addition and multiplication:

    s(x+y)=s(x) OR s(y),       s(xy)=s(x) AND s(y).

A finite sum is positive exactly when some summand is positive; a product is positive exactly when both factors are positive. Applying these identities entrywise proves that support commutes with every positive tensor network made of finite contractions, products, permutations, padding, and equality wiring. This is the inherited semiring-homomorphism mechanism, specialized here.

Accordingly raw N contraction counts witnesses. For a conjunction of atomic 0/1 factors sharing the correct axes, its fully contracted value counts satisfying assignments to the contracted variables. More elaborate nested bag-style expressions may count combinations of witnesses/proofs rather than just distinct assignments to one flat matrix. Logical idempotence can already fail numerically: repeated derivations add, and a self-join squares a weight. Only the support quotient has the Boolean semantics.

For P=(1,1) on a two-element domain, c_N(P)=2 while c_B(P)=1. Moreover c_N(p_N(P))=|D|P, whereas c_B(p_B(P))=P because D is nonempty and Boolean addition is idempotent. Thus embedding Boolean coefficients as real or natural 0/1 numbers is not a homomorphism preserving contraction/addition. It is an injective representation before the operation; the quotient s after arithmetic is the exact positive transport.

The support map is surjective but not injective: 1 and 2 have the same support. It intentionally discards counts and weights. Distinct objects are nevertheless still separately indexed before contraction; forgetting a witness count is not the same operation as quotienting the underlying domain by qualitative labels.

### Negation requires an explicit additional operation

Pointwise `1-T` implements complement only while T is Boolean-valued. After c_N(1,1)=2 it returns -1, not the false truth value and not even a natural number. Support by nonzero test would wrongly call -1 true. A correct N extension uses the zero-test

    z(x) = 1 if x=0, else 0.

Then s(z(x))=not s(x), and induction extends the support transport to arbitrary nested terms if each negation uses z. The operation is nonlinear and is not supplied by ordinary N-semiring addition/multiplication. The same zero-test works on nonnegative real coefficients. Alternatively Booleanize the relevant array before applying complement. A raw counting array cannot be complemented as if it were a probability or a truth table.

The impossibility of generating coefficient complement from positive Boolean tensor networks is elementary: sums/products with fixed Boolean coefficients and finite contractions are monotone in each input coefficient, whereas complement reverses the order 0<1. The proof concerns this **single-coefficient encoding**, not every conceivable tensor encoding of logic.

If an all-contraction representation of negation is desired, use a different, truth-wire declaration. Encode each truth b as the one-hot vector v_b with components v_b(a)=1 iff a=b, a in {0,1}. The fixed Boolean gate tensor for a truth function f is G_f(a_1,...,a_r,b)=1 iff b=f(a_1,...,a_r). Contracting G_f with v_(b_1),...,v_(b_r) returns v_(f(b_1,...,b_r)), because exactly one input assignment survives. NOT is a two-leg swap gate; AND and OR are three-leg truth-table gates; a finite-domain existential is a finite OR gate/tree. Wire-copy tensors share intermediate truth values. This gives full Boolean circuit evaluation with Boolean contractions, including negation. The initial lift b -> (not b,b) already carries both rails and is not monotone or semiring-linear in the original coefficient b. Thus it does not refute the preceding obstruction or make complement an inherited real linear contraction. The gate construction is standard, and its role here is to distinguish available representations accurately.

### Signed real coefficients and basis changes

On all of R, nonzero support fails to preserve addition: 1+(-1)=0 although both inputs have nonempty support. A signed tensor (1,-1) contracts to zero under epsilon, while Boolean contraction of its coefficient support is true. The positive-part test x>0 also fails as a multiplicative truth map on all of R, since two negative values multiply to a positive one. In fact no unital semiring homomorphism from a nonzero ring to B can exist: 0=s(1+(-1))=1 OR s(-1), a contradiction.

The inherited signed difference argument remains valid on its own terms: cancellation of a *difference of two probability tensors* proves equality of their marginals. That does not interpret the signed difference as a positive relation or a truth predicate.

The basis must be declared. For instance g=[[1,0],[-1,1]] sends the coefficient vector (1,0) to (1,-1). Reusing the old all-ones covector after this invertible coordinate change gives zero. Transporting the covector too gives epsilon g^(-1)=(2,1), which correctly returns one. General linear transport preserves the numerical calculation only when every piece of structure moves consistently; the new signed coefficients do not acquire the old entrywise membership meaning. Domain permutations, by contrast, preserve the distinguished basis, diagonal equality, and epsilon and commute with the operations. No arbitrary-GL-invariant truth, Riemannian metric, smooth dynamics, or physical inference follows.

A real linear functional cannot implement existential OR on every characteristic vector of D with |D|>=2: it would need L(e_a)=L(e_b)=1 but L(e_a+e_b)=1, contradicting linearity. Restriction to nonnegative tensors followed by support, or a different Boolean/truth-wire representation, is essential.

## 6. Source-faithful loss of endpoint binding

Keep D={a,b}, F={a}, G={b}. Compare

    M_forward: R={(a,b)};        M_reverse: R={(b,a)}.

Both models satisfy every assertion in the paper's actual separated record:

    exists x F(x);       exists x G(x);       exists x exists y R(x,y).

The third assertion is already relational. Both domains also have two distinct members; even an exact two-object cardinality assertion does not recover orientation. The source's joint target

    exists x exists y [F(x) AND G(y) AND R(x,y) AND x!=y]

is true only in M_forward. Its exact tensor value is

    OR_(x,y) F(x) AND G(y) AND R(x,y) AND not I(x,y).

Equivalently use the source term c c (F & p G & R & not I). Source conjunction implicitly pads F at the end while p explicitly shifts G into the second position. All witness and orientation bindings are retained until the final contraction.

The retained scalar record is (1,1,1) in both worlds; with a separate distinctness scalar it is (1,1,1,1) in both. Even replacing those existential bits by the simple numerical counts gives (1,1,1) in both. It is the missing linkage, not merely Boolean saturation, that causes this failure. Symmetrising R also merges the two orientations. Retaining F, G, and the full **oriented** R on common axes permits the displayed computation.

Apply inherited Theorem 4.2/Corollary 4.3 with the two finite models as input set, the separated record as representation, and joint-target truth as observable. The observable differs on one representation fibre, so no decoder of that record can recover it. That is exact inherited reuse, not another newly proved information theorem. It exposes the cost of this particular compression and gives a positive repair (retain role-binding structure). It neither disproves every structured decomposition nor selects a grounding direction for the whole and its consequences.

## 7. Numerical plurality and semantic labels

Let F hold of every element of D, so every object has the same unary F label. The term c c (F & p F & not I) is true exactly when |D|>=2. Its Boolean tensor value is 0 for a singleton and 1 for two or three objects; its N value is |D|(|D|-1), the count of ordered distinct witnesses. Identity therefore retains numerical plurality without adding primitive names to the object language.

Replacing D with a single node for each qualitative unary label would send the two-object model to the singleton and change the sentence's truth. That is an invalid quotient for the declared target. The tensor basis indexes the model's numerical elements; no claim is made that indexing supplies an independently justified metaphysical individuation. Renaming those indices by a bijection changes no closed-sentence value.

### The source nonemptiness assumption cannot be borrowed as actual existence

The source explicitly assumes D nonempty (p. 64). The identity c(p(P))=P uses it: at positive scalar truth P^0=1, padding produces a unary function constantly one on D, and existential contraction returns one only if D is inhabited. If D is empty, D^0 still contains the empty tuple, so a true grade-zero scalar is available; its padded unary array has no entries, and OR over that empty array is zero. Thus c(p(1_0))=0 differs from 1_0. The convention c(P^0)=P^0 is a separate operation and remains identity; it must not be mistaken for dummy-variable existential elimination.

The executable empty-domain controls are explicitly outside Dasgupta's nonempty source-model class. They locate the premise required to carry the identity into a possibly empty created/emergent-token sort. A genus/capacity carrier and its token extension cannot be identified just to import that premise: an inhabited carrier does not prove an inhabited token extension. Nor is the arity-zero scalar, empty tuple, or tensor unit an actual event, actual resource, extra individual, or extra Necessary Being. These are algebraic conventions and domain assumptions, not an actuality inference. In many-sorted use every quantified sort needs its own declared inhabitedness if a nonempty-domain identity depends on it.

## 8. Assurance, accounting, and stopping boundary

`controls.py` uses two separate finite evaluators: sets with direct images/products/intersections for the source semantics, and coefficient arrays with semiring sums/products for tensors. Exhaustive primitive checks include D sizes 1,2,3, scalars, mixed arities, binary and ternary tables; full equality-wire contraction is compared with direct arbitrary slot-map pullback, including repeated positions. Generated composite terms test nested complement and projection under both Boolean coefficients and N plus zero-test. Further controls check the source orientation pair, label-preserving plurality, basis cancellation, and truth-wire gates.

The verified run produces `CONTROL_RESULTS.json` with exact assertion counts (553,359 assertions after the final explicit shared-witness and empty-domain controls). Those counts are repetitions in finite families, not independent discoveries or proofs of unrestricted finitary or infinitary claims. The written induction, one-surviving-index argument, and algebraic counterexamples supply the general justification. No Lean formalisation was added: mechanically encoding these direct identities would add little assurance compared with the independent evaluators and readable proofs. Existing formal material is untouched.

The first run exposed a Python report-assembly defect: the source pair's helper closed over a domain-size loop variable later changed by the plurality controls. It was corrected to use the input tensor's domain; no failed mathematical assertion preceded that reporting defect. The successful rerun and source hashes are recorded. Earlier files remain unchanged.

Scientific accounting: inherited predicate-functor/semiring facts, inherited graded representation and fibre criteria, and newly executed concrete source transport tests. No full theorem already present in Orthemology is counted again. The result resolves the local representation question under an explicit finite typing contract and records the exact failures of raw numerical transport. It leaves ontology, actuality, explanatory priority, admissible productive resource interpretation, and bearers where the source-warrant inquiry left them.
