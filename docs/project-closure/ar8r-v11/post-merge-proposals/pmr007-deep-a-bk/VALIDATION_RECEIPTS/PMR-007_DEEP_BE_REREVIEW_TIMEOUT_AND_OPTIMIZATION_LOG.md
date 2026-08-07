# PMR-007 Deep BE rereview timeout and optimization log

```text
failed harness:
rereviews/pmr007_deep_be_distinct_walsh_rereview_v2.py

failure mode:
120-second execution timeout during exact symbolic rank computation

research status:
NO THEOREM DEFECT ESTABLISHED
NO REREVIEW PASS CLAIMED
```

The failed harness attempted full SymPy rational ranks of the binary marginal
constraint matrices through arity seven.  It is preserved as a failed
rereview implementation.  The replacement uses modular Gaussian elimination.
Because the parity vector is an explicit rational null vector, a modular rank of
`2^k-1` proves the rational rank is exactly `2^k-1`: rational rank is at least
the modular rank and at most `2^k-1`.

A second replacement using dense modular elimination also exceeded the
120-second execution window and is preserved as
`rereviews/pmr007_deep_be_distinct_modular_walsh_rereview_v3.py`.
The V4 harness uses bitset Gaussian elimination over GF(2).  A rank of
`2^k-1` modulo 2 is a lower bound for rational rank, while the explicit
rational parity null vector gives the matching upper bound.

The V4 harness timed out because its exact-Fraction marginal checks scaled to
thousands of arity-ten arrays.  The V5 harness preserves the independent GF(2)
rank certificate and replaces the slow Fraction loop with integer-count
probability tables at lower but still higher-than-primary arities.
