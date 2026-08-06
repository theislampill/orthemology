# PMR-007 Deep Round AO V1 — cold audit

```text
candidate: PMR-007-RPDS-1 V1
disposition: REPAIR_REQUIRED
review relation: same-program procedural cold audit; not external review
```

## Blocking findings

### AO-F01 — support-relative minimality was implemented incorrectly

The theorem removes points with `P(x)=Q(x)=0`, but the V1 checker retained them
as a special likelihood-ratio class. An exact representation need not refine a
class consisting only of impossible points. This produced 1,580 primary
minimality failures. The minimality theorem must be stated and checked only on
the union support.

### AO-F02 — exact Bayes-factor preservation and TV equality were not separated

Likelihood-ratio constancy is sufficient for full pointwise Bayes-factor
preservation. Equality in total-variation data processing has a weaker
fibre-sign condition and must not be conflated with full sufficiency.

### AO-F03 — deterministic and stochastic channels were not typed separately

The V1 proof concerns deterministic maps. A common stochastic Markov kernel
also cannot increase total variation, but pointwise likelihood-ratio recovery
requires a separate sufficiency condition.

### AO-F04 — zero-support posterior cases need explicit semantics

Finite ratios, infinite ratios, and impossible `0/0` points require different
treatment. Posterior-odds equality is asserted only where the relevant
likelihood ratio is defined in the extended sense.

### AO-F05 — minimality is pair- and experiment-relative

The likelihood-ratio statistic is coarsest only for the frozen binary
experiment `(P,Q)` on its union support. It is not a natural vocabulary or a
universal sufficient representation.

### AO-F06 — adaptive representation selection can invalidate evaluation

A representation selected using held-out outcomes or the final score can
manufacture apparent performance through leakage. The theorem requires a
common preregistered channel or a separately modelled selection process.

### AO-F07 — new measurement was conflated with recoding

A sensor, intervention, or query can acquire new evidence. Data processing says
a common recoding cannot create discrimination from a frozen experiment; it
does not say an enlarged experiment cannot add information.

### AO-F08 — PRH and OSM source claims require scope firewalls

PRH reports kernel alignment and a shared-reality hypothesis. The OSM paper
reports hippocampal state orthogonalization and model comparisons, including
trajectory fit. Neither supplies a likelihood over personal versus impersonal
metaphysical architectures.

### AO-F09 — theorem-family and prior-art ceiling must be explicit

The result is a standard statistical-sufficiency/data-processing application
and a specialization of the recurring fibre/factorization family. General
mathematical novelty is zero.

### AO-F10 — predictive sufficiency was overread toward metaphysics

Preserved predictive evidence does not establish proper function, mentality,
personality, Wisdom, source truth, or a Necessary Being.
