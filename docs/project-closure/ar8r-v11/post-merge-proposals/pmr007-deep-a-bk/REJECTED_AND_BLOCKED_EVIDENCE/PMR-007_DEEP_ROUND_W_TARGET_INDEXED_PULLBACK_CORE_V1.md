# PMR-007 Deep Round W V1 — target-indexed pullback core

```text
identity: PMR-007-TIPC-1
round: PMR-007-DEEP-W
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
```

## 1. Motivation

Deep V shows that profile certification and warrant completeness form two
independent diagnostic coordinates. A bare Cartesian product still permits a
profile certificate for one target to be paired with a warrant object for a
different target, version, or recipient scope.

V1 proposes a target-indexed integration architecture.

## 2. Candidate structure

Let:

```text
A:
  profile/semantic certificate objects;

B:
  warrant/provenance certificate objects;

K:
  target-contract keys;

alpha : A -> K;
beta  : B -> K.
```

Define the pullback:

```text
A x_K B = { (a,b) in A x B : alpha(a) = beta(b) }.
```

The candidate target key is:

```text
(target_id, version, recipient_scope).
```

## 3. TIPC-1 — compatibility characterization

A pair of component certificates is target-compatible exactly when it belongs
to the pullback. Any system that maps to both components while preserving the
same target key factors uniquely through the pullback.

## 4. TIPC-2 — Cartesian false-pairing boundary

The ordinary Cartesian product permits target, version, and scope mismatch.
The pullback rejects those mismatches.

## 5. TIPC-3 — three-way extension

With a world/target-adequacy certificate class `C -> K`, the iterated pullback

```text
A x_K B x_K C
```

forces profile, warrant, and world objects to name one target contract.

## 6. Proposed program consequence

V1 proposes the pullback as a nontrivial common core of Core A, Core B, and the
world bridge. It is stronger than Deep V's product because target compatibility
is built into the object rather than checked after pairing.

## 7. Authority ceiling

```text
mathematical novelty:
  ZERO — standard finite pullback

source/world authority:
  NOT ESTABLISHED

integrated champion:
  NONE

meniscus:
  MENISCUS_NOT_REACHED
```
