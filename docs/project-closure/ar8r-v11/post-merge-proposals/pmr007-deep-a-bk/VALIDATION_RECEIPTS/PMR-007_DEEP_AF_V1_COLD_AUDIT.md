# PMR-007 Deep Round AF V1 — cold audit

```text
candidate: PMR-007-NRID-1 V1
disposition: REPAIR_REQUIRED
review relation: same-program procedural cold audit; not external review
```

## Blocking findings

### AF-F01 — finite attained-class recovery was conflated with theory-level definability

V1 moved without a guard from a finite table of attained reducts to explicit
first-order definability.  The finite lookup theorem is elementary.  The
classical Beth theorem concerns first-order theories over their full model
class and does not follow from the finite executable test.

### AF-F02 — equality of reducts and isomorphism of reducts were not separated

Exact same-domain reduct equality is enough for the basic twin model.  A
representation-independent classifier should instead be invariant under
reduct isomorphism.  V2 must type both relations.

### AF-F03 — the intended model class was doing substantive work

Implicit definability is relative to a declared class.  Excluding an
impersonal expansion by fiat produces a singleton fibre but no argument.
Closure, admissibility, source, and metaphysical guards must be explicit.

### AF-F04 — the neutral vocabulary could smuggle the conclusion

Adding `PERSONAL_PROXY := P` to `L0` trivially restores definability.  A neutral
coordinate is eligible only if independently specified and justified without
defining the target into the reduct.

### AF-F05 — observational, causal, semantic, and full structural reducts were conflated

Two systems may share observations while differing causally.  V2 must state
that the barrier applies only to the complete declared reduct actually used by
the proposed entailment.

### AF-F06 — exact entailment was conflated with abductive or probabilistic support

Same-reduct twins block exact definition.  They do not by themselves establish
equal prior probability, equal explanatory merit, or no Bayesian update under
extra evidence.

### AF-F07 — classical Beth scope was overextended

Classical first-order Beth definability cannot be silently transferred to
finite-model-only, modal, second-order, non-elementary, intensional, or
source-governed classes.  V2 may cite it only as a guarded prior-art theorem.

### AF-F08 — source-conditioned restriction and neutral migration were blurred

An authenticated Track-N source contract may restrict the expanded model class.
That is source-relative implicit determination, not a neutral `L0` theorem.

### AF-F09 — metaphysical possibility was overread from formal expansion

A formal impersonal expansion witnesses nonentailment in the intended formal
class.  It does not prove that the expansion is metaphysically possible,
actual, physically realizable, or equally plausible.

### AF-F10 — theorem-family novelty and significance were understated

The finite criterion is the existing fibre/factorization mechanism; the
first-order connection is standard Beth definability.  Novelty is zero.  The
central value is consolidating the repeated parity family and imposing a
search-policy stop: more `L0`-definable invariants cannot break a same-reduct
personal/impersonal twin.
