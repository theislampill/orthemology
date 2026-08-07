# PMR-007 Frontier Round 12 cold audit — structure-preserving modal root bundles

```text
audit relation: same-model procedural audit over frozen V1 hashes
external human review: false
independent model-lineage review: false
overall disposition: PASS_WITH_NONBLOCKING_NOTES
```

## Typed structure and edge invariance

`PASS.` The packet defines separate bearer and effect domains and requires
bijective preservation **and reflection** of both actualization and dependence.
Those guards are sufficient to preserve and reflect the two derived predicates:

```text
Universal(b) := forall declared effects e, Act(b,e)
Underived(b) := no c with Dep(b,c).
```

The proof uses effect-domain surjectivity for the universal-role converse and
bearer-domain surjectivity for the underivability converse. It does not rely on
shared labels or a profile-only map.

## SMRB-1

`PASS.` Every based loop composite is a structure automorphism at the anchor
node. Any automorphism preserves the definable set of universal bearers. When
that set is a singleton, the unique root is fixed by every loop. MLT-1 then
supplies the unique coherent section; inverse transport proves uniqueness of
the universal bearer at every node, and dependence isomorphism preserves
underivability.

The result correctly improves on global flatness: the full holonomy group may
act nontrivially on non-root records while fixing the singleton root. This is a
strictly weaker root-coordinate requirement than identity holonomy everywhere.

The executable check examined:

```text
unique-root/underived finite structures:      1,728
structure automorphisms:                      2,064
nontrivial automorphisms fixing the root:       336
root-fix failures:                                0
underivability-preservation failures:             0
```

## Guard-deletion countermodels

`PASS.` Each deletion model attacks a different inference:

1. two universal roots permit a root-swapping structure automorphism and
   nontrivial root holonomy;
2. an arbitrary bearer bijection need not preserve the actualizer role;
3. preserving actualization without dependence can lose underivability;
4. disconnected coverage leaves an uncontrolled component;
5. an incomplete effect reduct can create a false universal root;
6. a unique counterpart section does not establish numerical identity.

The first three were executable and passed. The latter three are exact semantic
scope countermodels.

## Cross-candidate and authority audit

`PASS_WITH_NONBLOCKING_NOTES.` The Candidate-A and Candidate-B applications are
valid only when their complete obligation/target/dependency structures are
actually transported by isomorphism. They do not inherit truth, authority,
recipient applicability, causal efficacy, or actor-local implementability.

For Candidate C, the theorem composes Round 10's conditional singleton-root
premise with Round 11's transport criterion. It does not verify `COMMON`,
`ANCHOR`, effect/bearer completeness, the modal domain, the dependence
relation, the transport maps, or numerical-identity semantics.

Nonblocking burdens:

1. full structure isomorphism may be too strong for nontrivial modal variation;
   a later result must distinguish exact preservation from guarded
   homomorphism, simulation, or invariant-fragment transport;
2. a singleton root in the formal reduct may be a closed-world artefact;
3. structure preservation can secure role persistence without metaphysical
   numerical identity;
4. no mentality or Divine-attribute bridge is supplied.

## Ancestry, novelty, and significance

`PASS.` The mathematical core is standard definability under isomorphism plus
the elementary fact that automorphisms fix a definable singleton. The
substantive contribution is the exact cross-candidate burden reduction:
root-coordinate path independence follows from singleton definability and full
structure preservation, without requiring whole-fibre flatness. No general
novelty, historical identity, external-review completion, integrated champion,
or meniscus credit is claimed.

## Result

```text
blocking findings: 0
nonblocking structure/modal/identity notes: 4
repair required: false
fresh rereview required: true
PMR-007 may close: false
```
