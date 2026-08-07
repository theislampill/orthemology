# PMR-007 Deep AT V2 distinct fresh rereview

```text
identity: PMR-007-NIBE-1
frozen version: V2
disposition: PASS_WITH_NONBLOCKING_EXPERIMENT_ALGEBRA_AND_ONTOLOGY_NOTES
same-model procedural relation: yes
external review: no
```

## Preserved primary failure

The V1 primary checker correctly verified every actual two-state horizon comparison but returned `FAIL` because it required a length-three delayed witness inside that subclass. The theorem never claimed that the upper bound is tight in every subclass. The failed checker and result remain preserved.

The repaired V2 primary checker removed the false requirement and verified a separate three-state pair that agrees through horizon two and diverges at horizon three.

## Independent method

The distinct rereview did not invoke either primary checker. It independently:

1. verified all eight frozen V2 hashes;
2. represented each candidate pair as one block-diagonal weighted automaton;
3. constructed the reachable row space by exact rational Gaussian elimination;
4. tested equivalence by annihilation of the terminal vector on that space;
5. compared the result with direct word probabilities through a longer horizon;
6. found a distinct pair of deterministic two-state machines with the same complete trace signature;
7. enumerated all 128 deterministic adaptive policies through horizon three for that pair;
8. rechecked the three-state delayed witness.

## Results

```text
frozen files checked: 8
hash mismatches: 0
random rational model pairs: 200
reachable-space / long-horizon mismatches: 0
distinct trace-equivalent machine-pair controls: 1
adaptive policies checked: 128
adaptive-policy mismatches: 0
delayed-witness controls: 1
failures: 0
```

## Rereview judgment

The V2 trace-equivalence, adaptive-policy, and finite reachable-space claims are correct at the declared finite controlled weighted-system scope. If the unified-personal and impersonal rivals share the full registered trace language, no candidate-independent adaptive policy over that language distinguishes them.

## Nonblocking notes

- The registered action/observation algebra may omit a genuine discriminator.
- Trace equivalence is weaker than hidden-state isomorphism, causal identity, numerical identity, or ontological identity.
- Trace difference supplies an experiment, not a truth or proper-function verdict.
- Source-conditioned predicates remain outside the neutral observation algebra unless independently admitted.
