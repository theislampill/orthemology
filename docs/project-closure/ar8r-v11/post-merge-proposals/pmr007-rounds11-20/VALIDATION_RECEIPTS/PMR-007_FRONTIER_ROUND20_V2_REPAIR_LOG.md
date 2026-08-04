# PMR-007 Frontier Round 20 — V2 repair log

```text
source candidate: PMR-007-PRRC-1-V1
cold-audit disposition: REPAIR_REQUIRED
repair target: PMR-007-PRRC-1
historical identity: NONE
```

## Blocking repairs

### R20-R01 — exact required-root semantics

V2 uses `R_req(a)`: every member is individually load-bearing, and corruption
of any one required root disables the action.  Redundant alternative supports
are excluded unless first compiled into their minimal disabling-set
representation.

### R20-R02 — pathwise certificate renamed and scoped

V2 calls the result `STATIC_PATHWISE_ROOT_ROBUSTNESS`.  It does not use the
unqualified phrase “executable portfolio survives.”

### R20-R03 — executable corollary guarded

V2 adds a separate corollary requiring all surviving actions to be jointly
compatible, noninteracting, and simultaneously executable.  Without that
guard, the incompatible-repair model remains a blocker.

### R20-R04 — actual-root authority

V2 requires actual authenticated root identities or an independently validated
canonical quotient.  Display labels alone are not theorem inputs for a
world/runtime claim.

### R20-R05 — preserved failures and boundaries

The static/dynamic, fixed/adaptive, complete/partial, conjunctive/redundant,
authenticated/aliased, and certificate/execution distinctions remain explicit.
No countermodel was deleted to obtain admission.
