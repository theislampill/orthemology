# PMR-007 Frontier Round 17 V1 cold audit

```text
review relation:
read-only same-model cold audit over frozen V1 hashes;
not external human review;
not independent model-lineage confirmation

disposition:
REPAIR_REQUIRED
```

## Frozen custody

The V1 theorem packet, model owner, primary checker, and primary result matched
`PMR-007_FRONTIER_ROUND17_V1_FROZEN_HASHES.sha256` before review.

## Mathematical review

The equivalence among:

```text
admissible no-same-fibre-collision descent;
pointwise trivial holonomy on the selected invariant subbundle;
and collision-free transport-generated orbits
```

is correct at the declared connected invertible-transport scope. The proof does
not assume global flatness when applied to the singleton root subbundle.

### R17-F01 — reduced-realization hypothesis missing from uniqueness claim

V1 says the quotient realization is unique up to a unique bijection commuting
with the fibre maps. That is false for an arbitrary codomain `U`: one may add
unused elements to `U`, or permit automorphisms on unused elements, without
changing any `j_w`.

Required repair:

```text
define a reduced realization by U = union_w image(j_w),
then assert uniqueness up to unique commuting bijection;

or restrict uniqueness to the canonical quotient itself.
```

Severity: **blocking formal defect**.

## Executable-evidence review

The flatness/no-collision enumeration is internally consistent and returned
zero mismatches. The R5 portion, however, did not mechanically discharge every
property attributed to the model in the prose.

### R17-F02 — necessary/external root guards not checked

The model lists the root in `Necessary` and `External`, but the primary checker
did not test or report either coordinate while the packet described them as an
exactly verified part of the common model.

Severity: **blocking evidence-scope defect**.

### R17-F03 — full structure-isomorphism claim not checked

The common model claimed full structure-preserving root transport, but V1's
model/checker supplied only bearer-role mapping. It did not supply an effect
transport map or verify preservation/reflection of `Act` and `Dep`.

Required repair:

```text
add effect transport;
represent dependence explicitly;
check bearer/effect bijectivity;
check Act and Dep preservation and reflection;
then re-evaluate singleton universal-underived status.
```

Severity: **blocking evidence-scope defect**.

## Source-authority review

### R17-F04 — intra-world unity critique must not be recast as direct transworld evidence

The translated-primary Asfahani commentary criticizes a particular
intra-world argument from shared necessity and individuation to composition and
unity. That is relevant as an anti-shortcut and as a source-relative warning
about mental universals. It is not a direct source statement about Kripke
counterparts, graph holonomy, or transworld numerical identity.

Required repair: mark the relation to `RSD-1` as `PARTIAL_OVERLAP / SOURCE-
RELATIVE ANTI-SHORTCUT`, not direct source support for the transworld theorem.

Severity: **blocking authority-scope defect**.

## Nonblocking notes

1. `B_ID` is deliberately a semantic bridge. It must remain labeled as the
   unresolved interpretation burden, not as explanatory evidence for itself.
2. `RSD-1` and its flatness corollary are standard descent/groupoid facts;
   general novelty remains zero.
3. The common-model integration may receive scoped post-merge value only after
   the repaired structure checks pass.

## Required disposition

```text
V1:
PRESERVE_UNADMITTED_RESEARCH_CANDIDATE

blocking findings:
R17-F01
R17-F02
R17-F03
R17-F04

next action:
create V2; repair only the four reproduced defects; freeze it; run an
independent orbit/fundamental-cycle and source-authority rereview.
```
