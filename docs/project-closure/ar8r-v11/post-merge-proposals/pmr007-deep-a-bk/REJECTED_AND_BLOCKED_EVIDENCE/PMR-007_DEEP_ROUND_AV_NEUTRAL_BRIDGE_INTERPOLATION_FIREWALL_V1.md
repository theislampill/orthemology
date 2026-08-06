# PMR-007 Deep Round AV V1 — neutral bridge interpolation firewall

## Candidate status

```text
identity: PMR-007-NBIF-1-CANDIDATE-V1
provenance: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
general mathematical novelty: NOT CLAIMED
```

## 1. Finite propositional source/formal/world partition

Let the finite propositional variables be partitioned into:

```text
X — source-exclusive, translation-exclusive, or architecture-exclusive inputs;
N — declared neutral/shared bridge vocabulary;
Y — target/world-exclusive conclusion coordinates.
```

Let `A(X,N)` be an antecedent/source theory represented by its truth table and
`C(N,Y)` a target conclusion.

Define the source projection and target core:

```text
S_A(N) := exists X . A(X,N)
T_C(N) := forall Y . C(N,Y).
```

## 2. Candidate claims

### NBIF-1A — finite interpolation criterion

```text
A entails C
iff
S_A entails T_C.
```

### NBIF-1B — proposed canonical bridge

V1 proposes that whenever `A entails C`, the unique neutral bridge is `S_A`:

```text
A entails S_A entails C.
```

### NBIF-1C — source/neutral transfer reading

If a Track-N source package entails a Track-T or world conclusion without
sharing target-laden vocabulary, then the entailment must pass through a
formula in the neutral shared vocabulary.  Direct source predication of the
target is source-relative, not a neutral derivation.

## 3. Intended controls

- no shared vocabulary;
- inconsistent antecedent;
- tautological target;
- target predicate smuggled into the shared vocabulary;
- translation or interpretation relation treated as neutral without warrant;
- source-relative predication versus world truth.

The finite theorem does not establish the truth of `A`, the adequacy of the
translation, actual-world selection, or the source/world mapping.
