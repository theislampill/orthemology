# PMR-007 Frontier Round 20 V1 — cold audit

```text
audited identity: PMR-007-PRRC-1-V1
audited hashes: PMR-007_FRONTIER_ROUND20_V1_FROZEN_HASHES.sha256
audit relation: read-only same-model procedural audit
disposition: REPAIR_REQUIRED
external independence: NOT ESTABLISHED
```

## 1. Hash custody

The V1 theorem packet, model owner, primary checker, and primary results match
the frozen hash receipt.  The primary checker reports `PASS` over 13,293
exhaustive single-path cases and 449,924 random multi-path `(system,f)` cases.
That evidence is necessary but not sufficient for admission.

## 2. Blocking findings

### R20-F01 — root-set semantics is not yet typed sharply enough

The prose says a root corruption disables an action when it intersects
`R(a)`, but the model owner still describes the root set as a generic
"support" and explicitly leaves conjunctive dependency versus redundant
alternative support pending clarification.

Those readings are mathematically different.  For one action with
`R(a)={r1,r2}`:

```text
conjunctive-dependency reading:
  corruption of either root disables the action;

redundant-alternative-support reading:
  the action remains available while either root survives.
```

The transversal characterization is exact only for the first reading (or for
a representation already expanded into minimal disabling sets).  The theorem
must define `R_req(a)` as the set of individually load-bearing required roots,
so any one corrupted member disables the action.  Alternative redundant
supports require a different hypergraph over minimal disabling sets.

**Severity:** blocking.

### R20-F02 — “portfolio survives” overstates a pathwise certificate

The theorem's direct semantics proves:

```text
for every static corruption set and every registered path,
there exists at least one surviving blocker of that path.
```

It does not prove that one jointly executable set of blockers can be selected
across all paths when actions conflict, consume shared resources, alter one
another, or must be scheduled sequentially.  The incompatible-repair
countermodel already demonstrates the gap.

The admitted theorem must be named as a static pathwise root-robustness
characterization.  An executable-portfolio corollary may be stated only under
an explicit joint-compatibility and no-interaction guard.

**Severity:** blocking.

### R20-F03 — certificate/execution and actual-root/displayed-label authority need separate conclusions

V1 gives the authentication warning, but the conclusion should explicitly
state that `kappa` is computed over actual root identities or an independently
validated canonical-root quotient.  A high value over displayed labels is not
a certificate about actual corruption resilience.

This is not a defect in the finite theorem once its input type is fixed, but it
is blocking for the claimed implementation/certification reading.

**Severity:** blocking for application wording; nonblocking for the abstract
finite equivalence.

## 3. Quantifier-order audit

The following order is valid for the static theorem:

```text
portfolio I fixed;
adversary sees I and chooses one static F with |F| <= f;
for every declared path p, some blocker survives F.
```

The theorem does not cover:

```text
controller chooses an action;
adversary observes that action and corrupts a root before execution;
controller may or may not retry.
```

The adaptive one-shot countermodel correctly preserves this boundary.

## 4. Completeness and dynamic-system audit

The proof is exact only for a fixed complete path family and fixed blocking
relation.  Dynamic rerouting, repair-created paths, hidden paths, stale root
bindings, or action-generated deformations remain governed by T352's G1/G4
style guards.  V2 must keep these as theorem assumptions or explicit
nonclaims.

## 5. Theorem-family and novelty audit

The mathematical core is the equality between:

```text
minimum corruption size that disables every blocker of one path
and
minimum transversal size of that path's required-root hypergraph.
```

This is standard finite hypergraph transversal theory composed with T351/T352
path families.  Replacing vertices by provenance roots does not create a new
general mathematical origin.  The eligible contribution is a scoped
orthemological robustness certificate and false-multiplicity control.

## 6. Required repair

1. Replace generic `R(a)` support language with exact `R_req(a)` conjunctive
   dependency semantics.
2. Rename the theorem to static pathwise provenance-root robustness.
3. Add an executable-portfolio corollary only under joint compatibility,
   no-interaction, and simultaneous availability guards.
4. State that roots are actual authenticated identities or an independently
   validated quotient.
5. Preserve all dynamic, adaptive, partial-registry, redundant-support, and
   unauthenticated-label countermodels.
6. Freeze V2 and run a distinct checker that enumerates action systems and
   direct corruption semantics independently of the primary family-based
   implementation.
