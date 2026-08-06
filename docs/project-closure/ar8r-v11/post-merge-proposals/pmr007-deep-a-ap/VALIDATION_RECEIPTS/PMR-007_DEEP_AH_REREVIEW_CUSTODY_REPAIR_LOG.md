# PMR-007 Deep Round AH — rereview custody repair

The first distinct rereview returned `FAIL` solely because two literal source
anchor probes were mis-specified:

```text
line 493 was queried for text that is actually on line 487;
the line-502 probe used lowercase `volition` while the source begins
`Volition`.
```

The failed checker and result are preserved as `FAILED_V1` evidence.  No
candidate theorem, model, source file, primary result, cold-audit finding, or
V2 frozen hash changed.  The rereview implementation was repaired only by
correcting those two literal custody probes and then rerun from the same frozen
candidate hashes.
