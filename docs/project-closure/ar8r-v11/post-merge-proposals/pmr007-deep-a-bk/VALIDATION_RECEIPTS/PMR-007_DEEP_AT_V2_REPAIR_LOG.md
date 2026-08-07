# PMR-007 Deep AT V2 repair log

```text
candidate repaired: PMR-007-NIBE-1 V1
repaired version: V2
blocking findings repaired: 8 / 8
```

| Finding | Repair |
|---|---|
| AT-F01 | Defined `M_{u,o}` as the joint transition-and-next-observation matrix and required `Σ_o M_{u,o}` row-stochastic. |
| AT-F02 | Stated the exact reachable-row dimension bound `r-1`, with `r≤n_A+n_R`, and the stabilization proof. |
| AT-F03 | Preserved the failed V1 checker, removed the false tightness requirement, and added a verified three-state pair equal through horizon two but different at horizon three. |
| AT-F04 | Required one candidate-independent policy kernel over public histories and independent private randomness. |
| AT-F05 | Factored adaptive transcript probabilities into shared policy factors and model word probabilities. |
| AT-F06 | Added hidden-state, identity, ontology, causality, truth, and personality nonclaims. |
| AT-F07 | Made action/observation/source/version/target experiment relativity explicit. |
| AT-F08 | Classified weighted-automata/trace-equivalence ancestry and set general novelty to zero. |

The repair did not add a personal predicate, actual-world selector, or source-conditioned conclusion to the neutral observation algebra.
