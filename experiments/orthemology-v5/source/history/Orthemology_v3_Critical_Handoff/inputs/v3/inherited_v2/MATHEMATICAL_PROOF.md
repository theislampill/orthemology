# Internal polymorphism without the Girard interface

## Status and exact scope

This document proves a relative-model theorem for the concrete uniform
polymorphic combinatory calculus below. The polymorphic code really belongs to
its own quantifier domain. The construction does NOT externalise that code.

The accompanying Lean files express the construction and its metatheorems.
They were not compiled in this execution: Lean is not installed and the
attempted download route failed. Their syntax/elaboration and kernel acceptance
remain unverified. The mathematical arguments below do not rest on finite tests.
The Python reference checker verifies individual finite source derivations and
computation traces; that is different evidence from a proof of soundness of all
possible derivations.

This is an application of standard realisability/uniform-polymorphism ideas,
not a claim to have refuted Girard's theorem or discovered impredicativity.

## 1. Success condition

We require a universe C of codes with decoding E and, for every family
B : C -> C, a code All(B) IN C. Its objects must support abstraction,
instantiation, a computation law, and instantiation at All(B) itself.

We do not require C to be a code whose decoding is the entirety of C. Those
are different conditions:

    All(B) : C;  and  All(B) is allowed as a type argument.

is not

    C : C;  or  E(c_universe) = C.

Nor do we require E(All(B)) to be the full set of every arbitrary
set-theoretic family in product_{A:C} E(B(A)). That requirement would ignore the
admissible-morphism discipline under investigation. Instead, the admissible
families and their actual maps are defined below, not assumed by a label.

The construction makes every All(B) a code. It does not assert every such type
has an inhabitant: the type All(A -> A) does; the type All(A) does not.

## 2. Concrete computation

Let T be the inductive set of finite closed terms

    t ::= I | K | S | 0 | 1 | (t t).

The constants 0 and 1 are distinct observable syntax. They are not logical
truth values. Application is left-associative. Let -> be the relation generated
by

    I x       -> x
    K x y     -> x
    S f g x   -> (f x)(g x)
    f -> g    implies f x -> g x
    x -> y    implies f x -> f y.

Let ->* be its reflexive transitive closure. These definitions are independent
of any type assignment or proof calculus. The compatible relation permits reduction in either application position.
The reference evaluator chooses weak-head reduction within that relation; it
does not perform full reduction under all arguments. No termination claim is
made for untyped T. In particular, S I I applied to itself can loop.

## 3. The code universe is a constructed set, not a self-typing axiom

A code is a subset A of T invariant under each declared computation step:

    t -> u  implies  (t in A iff u in A).

Define C as the set of all such invariant subsets. It is a subclass of P(T)
defined without mentioning either All or typing derivations. Thus it is an
ordinary set in set theory; in Lean it is a structure containing a predicate
T -> Prop and its invariance proof.

Define E(A) = { t : T | t in A }. An element retains the actual program t.
It is not just a proof of a proposition. Define bottom = empty and top = T.
Both are codes. Bottom has no decoded element; top has at least the distinct
programs 0 and 1.

Invariance extends from -> to ->* by induction on a reduction derivation:
the reflexive case is immediate, and the step case composes two equivalences.
This proof is Code.along in the Lean source.

## 4. Arrows and universal types remain inside C

For A,B in C define

    A => B = { f in T | for every x in A, f x is in B }.

If f -> g, then f x -> g x. Invariance of B gives f x in B iff g x in B
for every x in A. Hence A => B is invariant and is itself in C.

For ANY family B : C -> C, define

    All(B) = intersection_{A in C} B(A).

This is a code because every intersection of invariant subsets is invariant.
More explicitly, if t -> u, then for every A in C,

    t in B(A) iff u in B(A),

so t belongs to their intersection iff u does.

Notice what the quantifier ranges over: the entire previously defined set C,
not a prefix of a hierarchy or a list of previously built types. Since All(B)
is in C, it is among those same arguments.

Thus

    All : (C -> C) -> C

is an actual operation in this model. It is not a separate external type
constructor with a missing internal code.

## 5. The full introduction/elimination/computation interface

An admissible section of B is a family f(A) in E(B(A)) whose underlying program
is independent of A. Equivalently, there is one r in T such that for every A,

    underlying(f(A)) = r.

This is a uniformity requirement on executable code, NOT the full relational
parametricity theorem. We do not identify the two.

Given such a section, define Abs(f) to be r with its evidence that r belongs
to every B(A). It is therefore in E(All(B)). Conversely, for
u = (r,h) in E(All(B)), define

    Inst(u,A) = (r,h(A)) in E(B(A)).

The maps are actual constructions. They satisfy

    Inst(Abs(f),A) = f(A),
    Abs(A |-> Inst(u,A)) = u.

Both equations retain the same underlying program; membership proof fields
are irrelevant to the program. In set theory these are equal elements. Lean
proves the corresponding subtype equalities using Subtype.ext. The uniform
section record is determined by its section (its uniformity field is a proof),
so these maps also give an isomorphism between E(All(B)) and the set of
uniform sections.

Most importantly,

    Inst(u,All(B)) in E(B(All(B)))

is immediately well-defined. It uses the actual internal code All(B), with no
lifting or refusal of that type argument.

For term-indexed dependent families D : E(A) -> C, a further semantic code is

    Pi(A,D) = { f | for every x in E(A), f underlying(x) is in D(x) }.

Its invariance follows by left congruence exactly as for arrows. A tracked
section g, supplied with a program r and computations

    r underlying(x) ->* underlying(g(x)),

packs into E(Pi(A,D)), and application computes to g(x). These are the precise
maps in TrackedSection, abstractPi and dependent_beta. This extension is NOT
a claim that every substitution/conversion rule of a full dependent type
theory has been supplied: arbitrary term-dependent families need a separate
extensionality discipline before adding conversion in their indices. The
internal-polymorphism theorem does not require that further extension.

## 6. Actual usable self-instantiation, with nontrivial data

Define

    IdCode = All(A |-> A => A).

For any A and x in A, I x -> x, so by invariance I x is in A. Therefore I
belongs to A => A for every A. Hence I is an element of E(IdCode).

Instantiate I at IdCode itself:

    I[IdCode] : IdCode => IdCode.

Apply that function to the polymorphic I:

    I[IdCode] I : IdCode,        I I -> I.

This is an actual internal self-instantiation followed by term application.
It is not the invalid untyped application of a polymorphic term without first
instantiating its quantified type.

Now define a data type

    BoolCode = All(A |-> A => A => A).

The program K inhabits it: K x y -> x. The program K I also inhabits it:

    (K I) x y -> I y -> y.

These are distinct programs, with different observable computations:

    K 0 1 -> 0,
    (K I) 0 1 ->* 1.

Their semantic elements in E(BoolCode) are distinct because their underlying
programs are distinct. This construction therefore goes beyond a
proof-irrelevant impredicative Prop example: the decoded types contain actual,
distinguishable computational objects.

BoolCode is itself a legal type argument. For example,

    K[BoolCode] K (K I) : BoolCode,
    K K (K I) -> K.

No equality between a truth and its negation is introduced.

## 7. Independent derivability and a soundness proof

Define a separate judgement t : A by the following rules:

    I : A => A
    K : A => B => A
    S : (A => B => D) => (A => B) => A => D

    f : A => B, x : A              entails f x : B
    for all A in C, t : B(A)       entails t : All(B)
    t : All(B), A in C             entails t : B(A)
    t : A, t ->* u                 entails u : A.

The universal-introduction rule keeps the SAME program t. It does not permit
the choice of a different t after inspecting the type argument. The rules do
not include 'semantic PASS means provable', 'self-certification means true', or
'equilibrium means theorem'. This is the semantically indexed uniform
combinatory calculus formalised by Derives. Its introduction rules may have
quantified premises; it is not claimed to be a decidable checker of arbitrary
semantic predicates.

THEOREM (soundness). If Derives(t,A), then t belongs to A.

PROOF by induction on the derivation.

I case: take x in A. Invariance transports x in A backwards along I x -> x.
K case: take x in A and y in B. Invariance transports x in A backwards along
K x y -> x.
S case: suppose f in A => B => D, g in A => B, and x in A. Then f x is in
B => D and g x is in B. Thus (f x)(g x) is in D. Invariance transports that
membership backwards along S f g x -> (f x)(g x).
Application case: by induction f is in A => B and x is in A; the definition
of the arrow gives f x in B.
Universal introduction: by the induction hypotheses, the same t belongs to
B(A) for every A, so it belongs to their intersection.
Universal elimination: membership of the intersection entails membership of
its A component, for any A, including the universal code itself.
Reduction case: induction gives t in A, and invariance along the finite
reduction gives u in A. These are all constructors. QED.

COROLLARY. There is no derivation of any t : bottom.

Otherwise soundness would yield t in the empty set.

COROLLARY. All(A |-> A) has no decoded inhabitant and no derivation.

An inhabitant would in particular belong to the component A=bottom, which
is empty. This is the intended behaviour of a universally quantified false
claim; formation of its internal code is not inhibited.

These are relative consistency/nontriviality results proved in the ambient
mathematics. They are not a proof of the ambient foundational system's own
consistency. The construction also does not imply normalisation of every raw
program; the raw computational syntax is deliberately untyped.

## 8. There are finite syntax codes, not only semantic descriptions

The companion source language of type codes is

    A ::= variable(n) | bottom | arrow(A,A) | all(A).

A code all(B) binds a de Bruijn type variable in B. Its interpretation under
an environment rho : Nat -> C is

    [variable(n)]rho = rho(n)
    [bottom]rho = bottom
    [arrow(A,B)]rho = [A]rho => [B]rho
    [all(B)]rho = All(X |-> [B](X :: rho)).

The finite syntax

    all(arrow(variable(0),variable(0)))

therefore decodes exactly to IdCode. It is available as the type argument of
an all-elimination certificate; the reference checker accepts precisely this
self-instantiation and subsequent self-application.

The finite source checker implements schematic I/K/S rules, application,
one-body type generalisation, type instantiation and checked weak-head
computation traces (a sound subrelation of the full compatible relation). It has no term-assumption context, so type-generalisation cannot
accidentally capture a term assumption depending on the new type variable.
Open type variables are checked against an explicit type-context depth.

Capture-avoiding type substitution uses the standard de Bruijn rule:
under k nested binders, replace index k by the argument shifted through k
binders, lower indices greater than k by one, and leave smaller indices
unchanged. The interpretation-substitution lemma follows by structural
induction on type syntax: the variable case is the three-way comparison,
the arrow case uses the two induction hypotheses, and the all case extends
the environment and shifts the substituted argument beneath the fresh binder.
This lemma plus induction on a finite source derivation translates it to the
semantic Derives judgement. That translation proof is written here; it is NOT
yet an independently compiled Lean theorem about reference.py.

The actual reference runs verify individual self-instantiation and data
computation certificates, not that metatheoretic translation theorem.

## 9. The exact requirement that cannot be silently restored

Take the constant family B(A)=top. There are perfectly legitimate external
families of top-elements that are not uniform. For example, define

    f(A) = 0 if I belongs to A, and 1 otherwise.

In classical ambient mathematics this is a well-defined family. It gives
f(top)=0 and f(bottom)=1.

Suppose an internal element u of E(All(A |-> top)) represented this family
using the actual instantiation operation. Every Inst(u,A) has the same
underlying program r. Beta at top would require r=0, while beta at bottom
would require r=1. Since 0 and 1 are distinct constructors, this is impossible.

Thus a general map

    ALL ambient families -> E(All(B))

cannot obey beta with this instantiation. The failure is exhibited even for
a constant family, not deferred to some unexamined exotic paradox.

This identifies a genuine change of semantic solution space. An arrow's
values are realised programs, and polymorphic abstraction acts on uniform
program sections. Their interpretations are not all ambient functions and
all arbitrary dependent families.

The standard Girard/Hurkens proof asks for more than this construction offers.
For clarity, HurkensBoundary.lean preserves a generic version of the standard
obstruction: writing DPred(X)=(X->Prop)->Prop and

    G(A) = (DPred(E(A)) -> E(A)) -> DPred(E(A)),

there is no beta-preserving retraction of the FULL ambient product
product_{A:C} G(A) into E(c) for any c in C. Its proof is an adaptation of
Mathlib's Hurkens/Girard proof, attributed in the source and included under
Apache 2.0. It introduces no global false axiom. That mathematical obstruction
is retained, not contradicted.

## 10. Even the computational diagonal-shaped universal code is internal

Define the following using the model's realised arrow, not an ambient powerset:

    Pred(A) = A => BoolCode
    DPred(A) = Pred(Pred(A))
    D(A) = (DPred(A) => A) => DPred(A)
    DCode = All(D).

DCode is in C. In fact, the SAME program K (K false) belongs to D(A) for every A:
false is in BoolCode; K false is a predicate on Pred(A), hence in DPred(A);
and K (K false) ignores an input of type DPred(A)=>A and returns that predicate.
Therefore K (K false) is an inhabitant of DCode. It can be instantiated at
DCode itself, giving an element of D(DCode).

This is useful diagnostic evidence that the construction has not merely
blacklisted 'diagonal-shaped' type expressions. It is NOT an assertion that
realised Boolean predicates are the full set of ambient Prop-valued predicates.
The distinction is essential and must not be removed when transporting results.

## 11. A precise role for Kakutani, without changing the proof target

The internal-code and soundness results above need no topological fixed-point
assumption. Kakutani has a legitimate additional role in selecting coherent
responses among already well-typed polymorphic programs.

Fix a nonempty finite list t_1,...,t_m of proved inhabitants of ONE universal
code P=All(B). Let K be the probability simplex on that list. Every q in K
selects a distribution supported only on typed programs. Since every t_j is
in P, every t_j also belongs to B(A) for every A. Consequently the SAME mixture
is type-safe at every instance, including A=P. Type selection must not change
which program-distribution is used.

Suppose a response correspondence R : K => K is upper hemicontinuous and has
nonempty closed convex values. K is nonempty, compact and convex, so Kakutani
gives q* in R(q*). Its support remains within the typed list. The implication

    typed support in All(B) -> typed support in B(A)

is independent of the existence proof and is the SafeSupport.instantiate
lemma in the Lean source. A safe support for bottom has no supported program.

For a concrete example take the polymorphic Boolean programs K and K I. An
anti-predictive binary response correspondence can be

    R(q)={1} for q<1/2,
    R(q)=[0,1] for q=1/2,
    R(q)={0} for q>1/2.

Its unique fixed point is q=1/2. This chooses a fair mixture of the TWO distinct,
already sound polymorphic selectors. It does not assign 'half truth' to False,
license a proof of the empty type, or produce the forbidden arbitrary-family
abstraction. Fixed-point existence is not a convergence theorem. These
probability/Kakutani arguments are written mathematics, not part of the claimed
Lean compilation status and not a imported axiom in the soundness proof.

## 12. Relation to Orthemology and final accounting

The narrow Orthemology contribution here is an explicit mapping of
representation and admissible operation: an internal universal code is
retained, but its permitted programs and evidence are not silently replaced
by a larger ambient family. The calculus separates the raw computational term,
its semantic type, its derivation, and any additional response policy. A
self-issued label, a convergent computation, or an equilibrium is not converted
into a derivation by a missing rule.

The earlier v1 externalisation is superseded as an answer to this task. This
v2 supplies a different mathematical model, rather than relabelling that
externalisation. It has not been adopted into the GitHub repository, and no
repository changes, publication, release or broader research closure are
claimed.

What has been supplied: the complete construction and ordinary proof for this
calculus, corresponding standalone Lean source, finite syntax examples and a
reference proof checker, source/behaviour audits and exact verification status.

What has not been supplied: a successful Lean kernel run, a formal proof of the
Python checker's implementation, a full dependent type theory with all its
conversion rules, full relational parametricity, unrestricted runtime reflection
on all semantic codes, or any contradiction of the original Girard theorem.
Those are distinct from the internal-polymorphism target proved above.
