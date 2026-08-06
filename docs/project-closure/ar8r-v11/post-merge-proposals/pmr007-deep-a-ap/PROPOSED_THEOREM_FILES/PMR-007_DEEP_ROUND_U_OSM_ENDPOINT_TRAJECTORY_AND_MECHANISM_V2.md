# PMR-007 Deep Round U V2 — OSM endpoint/trajectory refinement and mechanism nontransfer

```text
identity: PMR-007-TRPD-1
round: PMR-007-DEEP-U
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
```

## 1. Exact source and authority boundary

The frozen source is Sun et al., *Learning produces an orthogonalized state
machine in the hippocampus*, DOI `10.1038/s41586-024-08548-w`, accessed through
an owner-supplied Markdown copy with SHA-256:

```text
0d097cba7bbb25a949e2bf95af28b5a2259bd8d60b0e5fac5a74cdf7d05aa814
```

The article reports a longitudinal mouse experiment and computational model
comparisons. This round does not reanalyse raw calcium data, reproduce official
code, or identify a biological mechanism.

The source-level comparison supports three bounded observations:

1. Several tested model families attain selected final OSM-like structure or
   high task performance without matching the same learning trajectory.
2. The default CSCG comparison most closely reproduces both the reported final
   organization and the ordered decorrelation trajectory in the tested set.
3. Alternative sensory serializations within CSCG can preserve selected final
   learned transition structure while changing the pre-R1/pre-R2 decorrelation
   order.

Accordingly, the evidential object is not merely an endpoint. It includes a
model identity, encoding, longitudinal trajectory signature, evaluated task,
and source-defined comparison procedure.

## 2. Typed registered extraction

Let each registered comparison instance have:

```text
E(m): selected final OSM-like endpoint status;
F(m): model-family label;
S(m): sensory-sequence encoding;
T(m): independently declared ordered trajectory signature.
```

Let the reported animal signature be:

```text
T_animal = OFFDIAGONAL_THEN_PRE_R2_THEN_PRE_R1.
```

Define the bounded comparison target by:

```text
Match(m) iff T(m) = T_animal.
```

The target is therefore derived from an ordered trajectory object. It is not a
Boolean label copied into the certifying profile.

## 3. TRPD-1 — endpoint insufficiency

The registered class contains endpoint-matched models with different trajectory
signatures. Therefore there exist `m1,m2` such that:

```text
E(m1) = E(m2) = true
but
Match(m1) != Match(m2).
```

Hence no deterministic exact endpoint-only certifier `c` satisfies:

```text
Match = c ∘ E
```

on the registered class.

This is an application of the existing profile/fibre factorization mechanism;
it receives zero general mathematical novelty credit.

## 4. TRPD-2 — an independently measured trace refines the endpoint

On the frozen extraction, the profile

```text
P_trace(m) = (E(m), T(m))
```

is constant only on classes with a constant `Match` value, because `Match` is
computed by comparing `T(m)` with the independently declared animal signature.
Thus `Match` factors through `P_trace` on this finite class.

This is a **registered comparison characterization**, not a claim that the
chosen trajectory signature is complete for hippocampal mechanism, learning,
or cognition. A richer experiment may reveal models that share this coarse
signature while differing on other temporal or causal coordinates.

## 5. TRPD-3 — family identity is too coarse

The default CSCG and source-reported encoding controls share the family label
`CSCG` and selected final structure while differing in trajectory signature.
Therefore model family alone does not decide the registered trajectory target.
Encoding, objective, architecture, initialization, data ordering, and learning
procedure remain part of the evidence contract.

## 6. TRPD-4 — among-tested narrowing, not universal uniqueness

Within the bounded seven-instance extraction, the animal-matching trajectory
signature retains the default CSCG comparison among the endpoint-matched
computational instances. This is an among-tested source result. It does not
exclude:

```text
untested algorithms;
other CSCG parameterizations;
other biological mechanisms;
several mechanisms with the same coarse trajectory;
or mechanisms that agree on the reported summary while differing elsewhere.
```

## 7. TRPD-5 — mechanism nontransfer

Consider two formal expansions with the same endpoint and ordered trajectory
signature but different internal mechanism identities:

```text
M1: CSCG_BAUM_WELCH_EM;
M2: DISTINCT_LATENT_SEQUENCE_REALIZER.
```

Both realize the same `P_trace` value. Therefore a unique mechanism identity
does not factor through endpoint-plus-trajectory evidence without an additional
mechanism-sensitive coordinate or causal intervention.

The formal twin is a logical control, not an empirical claim that `M2` is an
actual neural mechanism. It blocks the inference:

```text
same endpoint and registered trajectory
therefore
same computational mechanism or biological implementation.
```

## 8. Object and soundness firewalls

The following remain distinct:

```text
world/task state;
sensory observation;
biological population activity;
individual neural response;
CSCG latent clone;
CSCG transition graph;
model posterior or occupancy probability;
representation geometry;
inferred orthemic profile.
```

No transition matrix estimated directly from neural recordings is reported in
the access copy. The transition graph belongs to the CSCG model comparison.

Likewise:

```text
global orthogonalization
is neither necessary nor sufficient for
strict soundness, truth linkage, pathway adequacy, or proper function.
```

High task performance can coexist with a different global geometry; matching a
selected geometry or trajectory does not establish that the learned target is
true, objectively fitting, or the system's proper function.

## 9. Flywheel effects

```text
OSM/Fable source lane -> Candidate G / Deep T:
  SUPPLIES a concrete endpoint-fibre refinement by longitudinal evidence;
  DOES_NOT_SUPPLY intentional ownership, personality, or one bearer.

OSM/Fable source lane -> Candidate E / Deep P:
  SUPPLIES a task-relative trajectory discriminator;
  DOES_NOT_SUPPLY truth-linked norm authority or proper function.

OSM/Fable source lane -> PRH / convergence:
  CHALLENGES endpoint or kernel alignment as a mechanism-identity criterion;
  SUPPLIES longitudinal process evidence as an additional comparator.

OSM/Fable source lane -> dynamic orthing:
  OPERATIONALIZES the need to distinguish world transition, episode inference,
  representation learning, and analysis-version change;
  DOES_NOT_VALIDATE orthemology or metaphysical ascent.
```

## 10. Exact disposition and nonclaims

```text
source-formal result:
  ENDPOINT_NONSufficiency_ESTABLISHED_AT_REGISTERED_SCOPE
  TRAJECTORY_REFINEMENT_ESTABLISHED_AT_REGISTERED_SCOPE
  MODEL_FAMILY_NONSufficiency_ESTABLISHED_AT_REGISTERED_SCOPE
  MECHANISM_NONTRANSFER_ESTABLISHED_AS_FORMAL_CONTROL

empirical authority:
  SOURCE_REPORTED_NOT_REPRODUCED

mathematical novelty:
  ZERO

integrated champion:
  NONE

meniscus:
  MENISCUS_NOT_REACHED
```

This round does not establish a unique biological mechanism, causal
identification, truth-linked proper function, mentality, personality, a
Necessary Being, divine attributes, divine Speech, or revelational
identification.
