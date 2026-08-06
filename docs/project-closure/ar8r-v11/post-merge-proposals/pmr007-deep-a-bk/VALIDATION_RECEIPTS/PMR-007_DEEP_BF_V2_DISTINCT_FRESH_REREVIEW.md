# PMR-007 Deep Round BF V2 — distinct fresh rereview

```text
identity: PMR-007-ILRC-1
candidate version: V2
review relation: same-program distinct procedural rereview; not external review
primary checker imported: false
disposition: PASS_WITH_NONBLOCKING_FIELD_CAUSAL_AND_ONTOLOGY_NOTES
```

## Frozen-custody result

```text
V2 frozen hash rows checked: 7
hash mismatches: 0
V1 hash verification: PASS 4 / 4
```

## Independent methods

The rereview did not import or call the primary checker. It used:

```text
- independent exact Gaussian elimination over Fractions;
- exhaustive 2x2 count-table classification;
- independent support-rectangle-cover dynamic programming for every
  nonempty 3x3 support;
- direct diagonal support lower bounds through n=6;
- exact mixtures generated in probability-normalized form rather than U,V form;
- canonical H=X saturation reconstructed independently;
- independently generated column-stochastic channels and factor pushforward;
- explicit strict-contraction and stronger-reading controls;
- frozen source and field-scope checks.
```

## Results

```text
exhaustive 2x2 probability tables:
7,314

2x2 rank-one:
796

2x2 rank-two:
6,518

2x2 rectangle-lower-bound failures:
0

all nonempty 3x3 support patterns:
511

rectangle-cover solver failures:
0

diagonal exact witnesses:
n = 2 through 6, all PASS

exact latent-mixture trials:
30,000

latent-mixture failures:
0

canonical H=X saturation trials:
20,000

saturation failures:
0

common stochastic-channel trials:
30,000

factor-pushforward failures:
0

strict rank-3 to rank-1 common-channel witness:
PASS

real/rational scope checks:
PASS
```

## Rereview conclusions

1. The normalization proof correctly converts every nonzero real
   nonnegative rank-one term into a positive mixture component and deletes only
   identically zero terms.
2. The bivariate product-mixture width is exactly real nonnegative rank.
3. Common Markov channels cannot increase a supplied latent-product width, and
   strict decrease is possible.
4. Support rectangle cover gives a valid lower bound and is exact on the
   diagonal witnesses.
5. The finite exact checks do not compute generic minimum real nonnegative rank.
6. Rational executable evidence does not collapse real and rational fields.
7. Width is not a bearer, subject, causal-source, agency, personality, or Wisdom
   count.
8. One observational law does not identify an interventional latent model or a
   multiway tensor factorization.

## Nonblocking notes

```text
external mathematical review:
OPEN

factorization-field distinction:
ESSENTIAL AND PRESERVED

causal/interventional interpretation:
NOT ESTABLISHED

formal impersonal realization:
NOT METAPHYSICAL ACTUALITY

general mathematical novelty:
0
```

## Admission recommendation

Admit only the scoped real-field bivariate observational characterization and
its exact width-bounded-rival consequence. Preserve all stronger readings as
countermodels or open burdens.
