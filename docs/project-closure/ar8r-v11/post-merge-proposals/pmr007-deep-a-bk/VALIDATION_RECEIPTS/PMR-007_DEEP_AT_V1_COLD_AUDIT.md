# PMR-007 Deep AT V1 cold audit

```text
disposition: REPAIR_REQUIRED
same-model procedural relation: yes
external independence: no
```

## Blocking findings

### AT-F01 — the weighted-system timing convention required an exact normalization clause

The packet must state whether `M_{u,o}` combines transition then observation or observation then transition, and require `sum_o M_{u,o}` to be row-stochastic. Otherwise the word expression need not define a probability law.

### AT-F02 — the finite witness bound needed its reachable-space guard stated more carefully

The exact bound is `r-1`, where `r` is the dimension of the combined reachable row space, and only then the looser `n_A+n_R-1`. The proof relies on stabilization of `V_k`, not on an assumption that every step increases dimension.

### AT-F03 — the V1 checker incorrectly required a tight length-three witness inside its two-state deterministic subclass

The theorem establishes an upper bound, not tightness in every subclass. The primary checker therefore returned a false blocking result (`no_delayed_witness`) even though all actual bound comparisons passed. Preserve the failure, repair the harness, and separately exhibit a valid delayed witness in a larger finite class.

### AT-F04 — the adaptive-policy equivalence needed candidate-independent policy kernels

A randomized or deterministic policy must choose actions using only the common public history and private randomness independent of the candidate label. Candidate-dependent action selection is a changed experiment.

### AT-F05 — transcript probabilities needed action-policy factors distinguished from model word probabilities

For adaptive policies, a transcript probability is the product of common policy action factors and the model's action-observation word probability. Equality follows because the policy factors are shared, not because actions are probabilistic outputs of the model.

### AT-F06 — behavioral equivalence was vulnerable to ontology and causality overread

Equal registered trace laws do not establish same hidden state, numerical identity, causal mechanism, subject, ontology, or metaphysical possibility. A trace difference likewise does not identify which model is true.

### AT-F07 — the experiment algebra and version/source custody were underemphasized

Nonidentifiability is relative to the registered action and observation alphabets, target contract, source version, and representation. Enlarging any of them defines a new experiment.

### AT-F08 — theorem-family and novelty ceilings required explicit adjudication

The result is standard finite weighted-automata / hidden-state trace equivalence and linear-algebra reachability. Its significance is the central AR8R application, not new general mathematics.

## Required repair

Create V2 with the precise probability convention, reachable-space bound, candidate-independent policy factors, explicit experiment-relative and ontological nonclaims, the preserved V1 checker failure, a repaired V2 checker, and a valid three-state delayed witness.
