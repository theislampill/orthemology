# PMR-007 Deep Round E — V2 repair log

```text
identity: PMR-007-TNAC-1
pre-repair: V1
post-repair: V2
blocking findings repaired: 3
central disposition changed: false
```

- `DE-F01`: corrected the Candidate-N integration-map SHA-256 to
  `cc1eefd4db0af89f5f948ccfffb0a8f15b8d12468d23c3a4cf5e4eb2f05c34c8`.
- `DE-F02`: added executable verification of every source hash and locator.
- `DE-F03`: replaced the hard-coded “best fit” assertion with an exact N-track
  predicate-coverage calculation and renamed the result a conditional
  source-compatibility leader.

V1 remains preserved as rejected custody evidence; only V2 is eligible for
admission.
