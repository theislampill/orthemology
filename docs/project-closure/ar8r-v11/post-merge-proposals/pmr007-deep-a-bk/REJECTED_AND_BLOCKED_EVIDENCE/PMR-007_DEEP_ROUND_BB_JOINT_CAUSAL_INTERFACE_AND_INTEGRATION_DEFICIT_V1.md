# PMR-007 Deep Round BB V1 — joint causal-interface quotients and integration deficit

```text
identity: PMR-007-JCIQ-1
round: DEEP_BB
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: Candidate G real unification versus carrier boxing
```

## 1. Common controlled system and typed interfaces

Fix one finite deterministic controlled system `(X,A,delta)` and `k` declared
interfaces

\[
I_i=(A,\lambda_i),\qquad \lambda_i:X\to L_i.
\]

Let `equiv_i` be the all-word trace equivalence from Deep BA, `Q_i=X/equiv_i`,
and let the joint interface use

\[
\lambda_\wedge(x)=(\lambda_1(x),\ldots,\lambda_k(x)).
\]

Write `equiv_wedge` and `Q_wedge` for its trace equivalence and quotient.

The interfaces must be independently typed.  Merely duplicating one interface,
renaming it, or defining one coordinate from another does not supply an
independent explanandum.

## 2. JCIQ-1A — common-refinement characterization

\[
\equiv_\wedge=\bigcap_{i=1}^{k}\equiv_i.
\]

### Proof

Two states have the same joint trace for every word exactly when every
coordinate trace agrees for every word. ∎

## 3. JCIQ-1B — dynamic subdirect-product theorem

The map

\[
\Phi:Q_\wedge\to\prod_i Q_i,
\qquad
[x]_\wedge\mapsto([x]_1,\ldots,[x]_k)
\]

is an injective label- and transition-preserving map.  Each coordinate
projection of its image onto `Q_i` is surjective.  The image is invariant under
the diagonal action transitions of the product.

Thus the joint minimal interface state is canonically a finite action-invariant
**subdirect subobject** of the product of the individual minimal interface
states.

### Proof

Common-refinement equality makes `Phi` well defined and injective.  Every
individual quotient class has an original state representative, proving
projection surjectivity.  Quotient transition definitions commute with every
coordinate projection, so the image is action invariant. ∎

## 4. JCIQ-1C — product-realizability characterization

`Phi` is surjective exactly when every tuple of individual quotient classes has
nonempty intersection in `X`:

\[
\forall(C_1,\ldots,C_k)\in\prod_iQ_i,
\quad
\bigcap_i C_i\neq\varnothing.
\]

Define the finite raw product deficit

\[
D_{raw}(I_1,\ldots,I_k)
=
\prod_i|Q_i|-|Q_\wedge|.
\]

Then `D_raw>=0`, and `D_raw=0` exactly when the joint quotient realizes the
full product of the registered individual quotient states.

A proper image records exact excluded interface combinations and dynamic
cross-interface constraints.  It does not yet explain why the constraints
hold.

## 5. Candidate-G interpretation

```text
full product image:
  the registered interface states are freely recombinable at this scope;
  one common carrier may merely box them.

proper action-invariant subdirect image:
  some registered combinations are impossible and the shared dynamics preserve
  that restriction; a completely independent product rival must add a coupling
  law or remove states.
```

This is a stronger dynamic nonproduct certificate than bearer counting or one
common output.  It can narrow a carrier-boxed rival.

However, an impersonal law, powers field, plural architecture with coupling,
distributed controller, or personal ground can realize the same subdirect
system.  The theorem does not discriminate those realizers.

## 6. Controls

```text
BB-CM1 FULL PRODUCT CARRIER BOX:
  one bearer realizes every tuple and diagonal dynamics; D_raw=0.

BB-CM2 DIAGONAL COUPLING:
  only matching pairs occur; D_raw>0 and the image is action invariant.

BB-CM3 DUPLICATED INTERFACE:
  I2 is a copy of I1.  D_raw can be positive even though no independent domain
  was integrated.  Independent typing is load bearing.

BB-CM4 DEFINABLE INTERFACE:
  I2 is a deterministic function of I1; nonproduct support may be definitional
  rather than explanatory.

BB-CM5 IMPERSONAL SUBDIRECT REALIZER:
  a rigid impersonal transition law realizes the same proper image.

BB-CM6 DISTRIBUTED COUPLED REALIZER:
  plural modules plus a coupling protocol realize the same image.

BB-CM7 HIDDEN LATENT PRODUCT:
  omitted latent coordinates restore a product architecture; resource and
  interface completeness fail.

BB-CM8 VERSION/TARGET SHIFT:
  changing one target or version changes an individual quotient and the joint
  image.

BB-CM9 PAIRWISE VERSUS GLOBAL:
  for k>=3 every pairwise projection may be full while the full joint image is
  proper, as in a parity constraint.

BB-CM10 LABEL RELABELING:
  the subdirect structure is invariant under quotient-state renaming and does
  not fix literal semantics.
```

## 7. Fable, OSM, PRH, and Deep-Z effect

Deep Z constructs a six-coordinate typed common object without reducing its
coordinates.  Deep BB adds an exact test for whether the attained joint state
space is a full product or a proper dynamically closed subobject.  This narrows
`FABLE-R1-B06-REDUCTIVE_OR_EXPLANATORY` but does not discharge it: support
restriction is not yet a derivation or explanation.

OSM/PRH alignment can suggest shared constraints, but neither paper supplies
the complete action/label interface required to compute this quotient from the
reported summaries.  A common learned representation may discover a proper
joint image; it does not thereby establish proper function or personal unity.

## 8. Ancestry and authority

```text
abstract ancestry:
  intersections of congruences;
  subdirect products;
  partition common refinements;
  finite automata/bisimulation quotients

relation to Deep B:
  DYNAMIC_STATE-SPACE STRENGTHENING OF REAL DERIVATIONAL UNITY

relation to Deep AE:
  SUPPORT/TRANSITION NONPRODUCT COMPLEMENT TO MOBIUS INTERACTION SUPPORT

relation to Deep Z:
  EXACT NONPRODUCT TEST FOR THE TYPED COMMON OBJECT

general mathematical novelty:
  0
historical identity:
  NONE
external review:
  OPEN
owner adoption:
  PENDING
```

## 9. Nonclaims

No result establishes independent semantic typing, completeness, causation,
explanatory priority, numerical bearer unity, one subject, personality,
proper function, Wisdom, Necessary Being, source truth, world truth, integrated
champion, meniscus, or natural closure.
