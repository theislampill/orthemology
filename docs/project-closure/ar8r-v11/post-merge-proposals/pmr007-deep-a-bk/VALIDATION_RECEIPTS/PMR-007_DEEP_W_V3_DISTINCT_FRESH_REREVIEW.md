# PMR-007 Deep W V3 distinct fresh rereview

Disposition: `PASS_WITH_NONBLOCKING_CONTRACT_AUTHORITY_NOTES`.

The rereview used a grouped natural-join implementation, compatible-cone
enumeration independent of the primary checker, single-coordinate erasure
tests, and a raw-versus-valid subobject comparison.

## Results

```text
frozen hash rows:
9

frozen hash mismatches:
0

valid pair pullback objects:
4

valid triple pullback objects:
3

pair compatible cones checked:
341

pair universal-property failures:
0

triple compatible cones checked:
13

triple universal-property failures:
0

full-key fields independently exercised:
6 / 6

raw-pullback pairs containing an invalid component:
3
```

The rereview confirms:

1. exact full-key equality characterizes membership in the declared finite valid
   pullback;
2. every tested compatible finite cone factors uniquely through that pullback;
3. removing any one of the six contract-key coordinates admits at least one
   false pair in the frozen model;
4. restricting to independently valid component subobjects is load-bearing;
5. the three-way construction aligns contract identity but does not validate the
   world bridge.

## Nonblocking authority notes

- The six-field key is a declared finite contract, not a theorem of universal
  completeness.
- `referent_id` and source fields require independent H12/H16-style evidence.
- The pullback does not establish component truth, target truth, common bearer,
  numerical identity, intentional subjecthood, or causal realization.
- The mathematical mechanism is standard category theory with zero general
  novelty.
- Same-session staged rereview is not external review.
