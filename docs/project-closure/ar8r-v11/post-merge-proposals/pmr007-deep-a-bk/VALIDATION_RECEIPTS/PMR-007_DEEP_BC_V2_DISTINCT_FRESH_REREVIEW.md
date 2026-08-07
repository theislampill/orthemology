# PMR-007 Deep BC V2 distinct fresh rereview

```text
candidate: PMR-007-UIEP-1 V2
review relation: distinct exact-rational implementation in the same Pro program
external human review: NOT PERFORMED
independent model lineage: NOT CLAIMED
disposition: PASS_WITH_NONBLOCKING_DECISION_THEORY_AND_EXPERIMENT_COMPLETENESS_NOTES
```

## Frozen-byte verification

All six frozen V2 rows matched before the independent run.

## Independent method

The rereview used three-signal experiments, random exact-rational three-to-two
garblings, three-action bounded payoff problems, and signal-permutation
controls.  It did not reuse the primary binary enumeration.

## Results

```text
garbling experiments:
20,000

decision problems:
400,000

garbling-dominance failures:
0

experiments with some strict value loss:
18,451

three-signal permutation-equivalence cases:
5,000

permutation value failures:
0

unaligned same-named postprocessing counterexample:
FOUND

frozen hash failures:
0

result:
PASS
```

The unaligned control confirms the V1 audit: mutual Blackwell equivalence does
not license arbitrary same-named postprocessing unless signal alignment or a
commuting simulation is explicit.

## Disposition

The standard garbling simulation theorem, aligned-equality noncreation result,
and architecture burden relocation survive.  The theorem applies only to the
frozen common experiment, common prior, and finite expected-reward decision
class.  It leaves open a genuinely enlarged source, intervention,
phenomenological, semantic, or metaphysical experiment.
