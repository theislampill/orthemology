# U11 — tracked dependent core and partial proof-replay refinement

New attempt-0003 source/proposal. The six surviving attempt-0002 documents are
immutable evidence. The code in this checkpoint is newly authored from their
mathematical specifications, not represented as recovered code or recovered tests.
Ordinary constructions/proofs below are separate from uncompiled Lean candidates.

## 1. The repaired equality architecture

Four relations are deliberately distinct:

1. Raw canonical `Conv` is compatible SKI conversion; I and S K K are different.
2. Lambda beta conversion belongs to U09's target and is not reflected into Conv.
3. `EqTm` is type-relative equality in the NEW tracked PER interpretation.
4. The frontend's explicit computational-path equality is a sufficient, finite
   evidence rule. It is not a decision oracle for all semantic PER equalities.

No eta/extensionality axiom is added to the source. The failed bracket pairs
`S(KI)I`/I and `S K(K I)`/I remain distinct raw normal forms. Body-normalisation
before bracket abstraction remains refuted as a general substitution-natural
repair. The replacement proves abstraction congruence by **related applications**
in a dependent function PER. It never asserts raw equality of the compiled
abstractions themselves.

## 2. Objects and exact formation obligations

`PER` is a partial equivalence relation on canonical raw Terms, with symmetry,
transitivity and saturation in both endpoints under canonical Conv.
`P.dom t` means P(t,t). Contexts use valid valuations: a `Context` has a carrier,
an equivalence relation and an environment of raw Terms. A contextual `Ty Γ`
assigns a PER to each valuation, with equality of fibres whenever the valuations
are related. These equalities are explicit proof obligations.

A `Tm Γ A` contains ONE finite SKI polynomial p and a proof

    γ ~Γ δ ⇒ A(γ)(eval p γ, eval p δ).

It is not an arbitrary set-theoretic section. An untracked function cannot enter
this term object by being labelled a section. Every introduction/elimination in
`P01DependentCore` constructs an actual finite polynomial and proves its tracking
property. This is an **intrinsic, proof-carrying contextual core**, not a claim
that arbitrary JSON has already been reified as such an object.

A substitution Δ→Γ has a valuation map respecting context equality, polynomial
images of variables, and exact evaluation/tracking equations. Only finitely many
images are used by any finite term. The frontend uses finite syntax, not arbitrary
host functions, to describe those used images.

## 3. Structural laws and two kinds of binder

Polynomial substitution is homomorphic. Structural induction gives identity,
composition and evaluation-substitution equations. Substitution composition
composes valuation maps and substitutes the inner tracker into the outer
tracker. Its tracking proof is the evaluation-substitution equation followed by
the two supplied tracking equations. Identity and associativity hold on maps and
actual polynomial codes; proof-field identity is not an extra axiom. The new
`SubEq` names this stronger code-exact relation. The predecessor semantic
substitution equality is retained separately as `SubRel`: related input
valuations must map to related output valuations. It is an equivalence, respects
composition, and code-exact equality implies it. Related substitutions give
equal reindexed fibres and related substituted terms. Thus the stronger
implementation equality is not silently substituted for the older semantic law.

Pulling a type back means composing its PER family with the substitution map.
Pulling a term back substitutes its code. The type coherence and term validity
proofs use the substitution's respectfulness and tracking equations. Thus
`typing_under_substitution` is proved, not included as an unverified input law.

Term context extension contains pairs (γ,a) with a in A(γ)'s domain. The relation
uses γ~δ and A(γ)(a,b). Fibre coherence proves it an equivalence relation.
The environment extension puts a at index0 and shifts old variables. Weakening,
the last variable, substitution extension and single instantiation are built
with actual polynomial trackers and the matching valuation maps.

Type extension is a different operation: a valuation additionally contains a
PER parameter; related valuations have equal parameter PERs. It does not add a
runtime term variable. Type weakening, the new type variable and instantiation
are supplied as coherent family/substitution constructions.

The executable frontend implements the corresponding capture-avoiding two-sort
substitution. Under a term binder it shifts term indices in *both* term images
and type images (types may contain term endpoints). Under a type binder it
shifts type indices in *both* sorts. A based-J motive binds an endpoint and then
an equality proof, so both term lifts are applied. These cases have focused
positive/negative tests; the tests do not replace the structural proofs.

## 4. Pi, actual abstraction and the beta/congruence theorem

For a domain PER P and coherent fibre family B, define

    Pi(P,B)(f,g) ⇔ ∀x,y, P(x,y) ⇒ B(x)(f x,g y).

Symmetry transports from B(y) to B(x). Transitivity uses related-domain membership
and fibre coherence; saturation follows from raw application congruence.
The family is only semantically relevant on the domain. The implementation
uses a specified bottom PER outside that domain, not an arbitrary incoherent
choice that is silently read at an untyped argument.

K-priority bracket abstraction is defined on finite open SKI polynomials. If the
last variable is absent, use K on the decremented polynomial. For that variable
use I. For an application containing it, use S on the two recursively compiled
parts. Induction proves application beta after *every* closing environment:

    eval([x]b,γ) a Red eval(b,(γ,a)).

The application case performs the S step then lifts the two induction paths.
The K case performs a real K step; the I case a real I step. The preserved stronger literal square is also supplied:
`abstract(psub(pup σ,p)) = psub(σ,abstract(p))`. Its proof shows that lifted
substitution preserves freeZero, commutes with dropping an absent binder, and
therefore preserves the whole-subterm K priority. This is naturality for actual
capture-avoiding substitution, NOT congruence for arbitrary body conversion.
The separate after-application conversion square remains available as well.

Lambda introduction uses this polynomial and body validity at related extended
valuations. Raw saturation transports the two beta results into the fibre PER.
Application uses the Pi relation. The same argument, with related bodies instead
of one body, proves type-relative abstraction congruence. Beta soundness is thus
proved in the intended typed equality without modifying raw Conv.

## 5. Represented Sigma and its exact eta domain

The raw pairing/projection combinators are the accepted pairTerm/firstTerm/
secondTerm. Define represented z by

    Conv z (pairTerm (firstTerm z) (secondTerm z)).

The Sigma PER requires representation of both endpoints, related first
projections and second projections related in the first projection's fibre.
`SigmaPER` is proved equivalent to the witness presentation using actual encoded
pairs. Pair introduction uses the exact projection beta results and coherence;
first/second elimination use the defining clauses. Eta is raw Conv to the
re-encoded projections **for represented inhabitants**. There is no untyped
eta rule equating every raw Term to an encoded pair.

The contextual pair/fst/snd constructors supply actual polynomial trackers.
The frontend `eta` constructor is an identity proof for a well-typed Sigma
inhabitant; it is not a new raw reduction rule on arbitrary terms.

## 6. Identity and based J, including proof-coordinate coherence

The proposed identity PER is

    Id(P,x,y)(p,q) ⇔ P(x,y) ∧ Conv p I ∧ Conv q I.

Refl is tracked by I. This proof-irrelevant, represented identity is a proposed
layer, not a rewriting of the accepted canonical concept. A based motive lives
over the **two-coordinate** extension Γ,y:A,p:Id(A,x,y). Its coherent-family
proof therefore relates (x,I) to (y,p) whenever p is a valid identity witness.
Transport gives the equality of motive fibres at those two points.

The J tracker is `(K (K d)) y p`, which reduces to d by two K steps. Transport the
base relation into the target fibre, then use saturation at both tracker
endpoints. This constructs `P01D.j`; `j_computation` records the actual raw path.
It is not merely a transport premise substituted for an eliminator.

The negative control chooses one fibre when p is literally I and a different
fibre at I I. Since I I Conv I, this proof-inspecting family is not coherent.
`proof_inspection_not_coherent` records that failure. Endpoint coherence alone
never substitutes for proof-coordinate coherence.

## 7. Parametric All and the universe boundary

The stronger U10 replacement is preserved unchanged. Its relation data are
endpoint-aware links, not arbitrary unrelated predicates. In the formal core,
`ParamFamily` explicitly supplies the two-endpoint body relation and identity
extension for that body. `AllFormation` binds this to the contextual body family
and carries environmental coherence. These are typed, proof-carrying formation
interfaces, not assumptions about every canonical Code.

`allIntro` deliberately requires a uniformity proof in addition to unary body
validity. Unary membership alone is insufficient, as the preserved countermodel
shows. The preserved ordinary finite/dependent abstraction theorem explains how
to discharge that premise for the specified source language. The new source
contains generic All formation/elimination and nonempty examples, including
polymorphic identity with its uniformity proof actually supplied. It does **not**
claim a newly kernel-checked recursive implementation of the entire U10
ordinary relational interpretation.

AllPER is itself a PER, so it can be the argument of allElim: legal internal
self-instantiation survives. `P01UniverseBoundary` explicitly distinguishes this
from the much stronger reification of every ambient GirardFamily section. It
specialises the preserved `no_self_product` to Realiser(P)={t | P.dom t}: a
beta-preserving pack/unpack for the exact full ambient family would imply False.
No such pack/unpack, same-level Type:Type, or blanket closure is constructed.
The original canonical All(B)∈C statement and original SCUU boundary are untouched.

## 8. The finite executable surface

The new frontend accepts strict finite tuple/list ASTs. Types: tv, bot, pi, sig,
id, all. Terms: indexed variables; annotated I/K/S; lambda/application;
annotated pairs/projections; refl/represented eta; based J; allI/allE; explicit
casts. Markers parse but have no typing rule. A context is a finite list of type
declarations checked in order; later declarations cannot be referenced early.

Malformed tags/arity, booleans masquerading as indices, negative/out-of-scope
indices, cyclic input, unsupported shapes and invalid reduction addresses
refuse. Depth, node and work guards refuse rather than return a false typing or
inequality statement. The input is copied/frozen and not mutated. No arbitrary
Lean identifier or source string is an accepted AST constructor.

Synthesis is syntax-directed. Pi application substitutes its actual argument
into the codomain; Sigma's second projection substitutes the first projection;
J checks the base at (x,refl x) and returns the motive at (y,p). allI shifts the
old context's type variables, preventing generalisation of a fixed assumption
as the freshly bound variable. Cast checks both types well-formed and verifies
explicit paths to a common expression. There is no semantic PER oracle.

`step_at` recomputes the contraction at the exact address. Path composition is
checked finitely. The raw-source Lean checker `P01Certificate.replay` separately
returns an actual Red proof; `checkJoin` returns Conv only after actual endpoints
agree. A frontend path and a raw source path are not interchangeable: type beta,
casts and annotations can erase to zero tracker steps. U09's positive simulation
is **not** falsely extended to the whole dependent frontend.

## 9. Exact partial refinement — what is proved and what is not

There are three distinct stages:

    frontend syntactic result → proposed bound target object → kernel replay.

The frontend label ACCEPTED is not semantic/kernel admission. This is explicit
in every Result and export record. A finite export must bind the *actual* target
Term and TypeCode to an actual canonical `Checked` object. A dependent export
must bind the actual finite polynomial and intrinsic contextual Ty to a real
`Tm Γ A`. The binding equalities are proof obligations, not JSON booleans.

### Finite exporter theorem (ordinary algorithm proof)

For every successful `export_finite(r)`, r is rechecked and the result is in the
specified finite target image. `_encode` is structural. I/K/S produce their exact
canonical certificates; application checks the arrow/domain equality. allI
requires the empty runtime context and checks under the incremented type depth;
allE carries the actual syntactic type. The cast branch is allowed only when its
finite target type is literally unchanged.

For lambda, `_abstract_cert` has a simultaneous derivation invariant: each free
variable has its recorded simple TypeCode. If index0 is absent, weaken/drop the
unused assumption and use K. At index0, use I with the exact domain type. For an
application, the S axiom combines the two recursively abstracted derivations.
Other variable-containing polymorphic cases refuse. Induction gives the expected
arrow type and the same K-priority code as `compile_poly`. TypeCode conversion
is permitted only on the exact image (no Id/Sigma); inside that image there are
no term endpoints to be erased from dependent types. Renderer constructors are
fixed constants, and indices are validated naturals. Finally both expected type
and separately compiled code must match. Therefore the finite returned
certificate has the claimed FiniteDerives derivation, as an ordinary algorithm
argument. Universal machine verification of Python's interpreter is NOT claimed.

The six concrete generated Lean fixture files go further once compiled: canonical
`check` computes each actual Cert with `by decide`, and exact term/type binding
proofs construct FiniteEnvelope. Here they remain uncompiled examples, not proof
credit or a simulation of compiler output.

### Kernel-admission theorem (formal candidate)

For any producer, even a buggy frontend, the replay stage accepts only a real
`FiniteEnvelope(t,A)` or `DependentEnvelope(Γ,A,p)`. By their data and the existing
soundness/tracking theorem,

    finite replay accepted ⇒ FiniteDerives(t,A) ⇒ SN_source(t),
    dependent replay accepted ⇒
      ∀γ~δ, A(γ)(eval p γ, eval p δ).

`ReplayResult.refused reason` yields no accepted proof. These are universal
proof-replay soundness/refusal theorems, not an axiom that Python is correct.
The exact commitment is to the decoded target objects in the theorem statement;
a source filename, textual hash or frontend message alone does not identify
an intrinsic type or prove that an arbitrary JSON interpretation is its image.

### Why total exact export is false, and why that is not an unsoundness claim

The unchanged TypeCode has no identity or Sigma constructor. By constructor
disjointness, no literal TypeCode image is an identity/Sigma shape.
A frontend term such as λx:bot.refl x synthesises Pi(bot,Id(bot,x,x)); it is typed
on the new surface but cannot be exported by the unchanged *literal* finite
vocabulary. The actual exporter refuses it. A represented dependent pair gives
a second typed refusal. Resource guards supply further intentional partiality.

This refutes the statement “every frontend acceptance yields an exact canonical
Cert export without refusal.” It does not prove unsoundness of accepted Certs,
and does not rule out a future different encoding with a proved correspondence.
The correct replacement is the explicitly partial, binding-preserving,
refusal-preserving replay interface above. It is complete as that interface;
**a total Python/JSON-to-intrinsic dependent interpreter is not supplied or
claimed**. Adding such a total interface is not made a premise of these results,
and cannot be smuggled into canonical main by treating partiality as a success.

## 10. Qualifications and final boundary

The corrected core is a newly proposed intrinsic calculus. Its constructors,
structural laws, Pi/Sigma/J/All operations, tracker interpretation and replay
interface all have authored proof bodies. No source placeholder is intended.
The source can still contain elaboration/tactic errors: exact Lean 4.19.0 has not
run. No theorem is labelled kernel-checked and no `.olean` is claimed.

All new proposal tests are executed with durable normal/optimised outputs and
are replayed again from the final ZIP. They are newly authored tests, because
the old attempt-0002 test sources/results did not survive. The tests support the
finite implementation only; they neither prove all semantic families coherent
nor supply the missing compiler. The external driver must compile, read back
all exact targets and audit axioms before any formal acceptance. Adoption of
this new core/admission interface remains an owner/Codex decision; it is not
performed here.
