# PMR-007 Deep Round G V1 custody-audit correction

## Disposition

```text
REPAIR_REQUIRED
```

The first cold-audit report stated that the source hashes passed, but the frozen executable source-custody result actually had `pass: false`: one wording locator normalized the section-title proposition instead of matching the supplied byte sequence.

This is a blocking procedural defect. The prior `PASS_WITH_NONBLOCKING...` report is preserved as superseded evidence and cannot support admission.

Required repair:

1. bind the disputed source point to exact phrases present in the supplied translation;
2. rerun source and archive-member custody;
3. create a custody-repaired V2 candidate without changing the mathematical theorem;
4. perform a new cold audit over the repaired bytes;
5. run a distinct fresh rereview.
