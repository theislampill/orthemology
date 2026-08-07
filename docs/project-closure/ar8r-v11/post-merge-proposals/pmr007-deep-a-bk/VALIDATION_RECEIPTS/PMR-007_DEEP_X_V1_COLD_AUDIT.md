# PMR-007 Deep X V1 cold audit

```text
disposition: REPAIR_REQUIRED
frozen_input: PMR-007_DEEP_X_V1_FROZEN_HASHES.sha256
review_relation: DISTINCT_PROCEDURAL_LANE_WITH_SHARED_MODEL_LINEAGE
external_independence: NO
```

## Scope

Audit the frozen V1 candidate for typing, quantifier discipline, model
consistency, source nonmigration, theorem-family ancestry, and central-bridge
overreach. The primary truth-table PASS is treated as necessary but not
sufficient.

## Blocking findings

### X-F01 — error-theory exit is not separated from accepted objective correction

V1 says an objective radical correction leaves `T/H/P` or exits through `E`,
but the executable partition permits `objective=true` and `E=true`. `E` is an
exit from the objective-correction claim and cannot discharge the authority of
an accepted objective radical correction.

**Required repair:** distinguish `CorrectionClaim` from `ObjCorr`; under the
partition assumption prove:

```text
ObjCorr and Rad -> T or H or P;
E -> not ObjCorr.
```

### X-F02 — the R5 order-only model is internally mislabelled

`X-R5-IMPERSONAL` declares `objective_correction: true` while also declaring no
key authority and no world-target adequacy. The intended model shows that
underived order, actuality, and compatibility do not themselves establish an
objective correction.

**Required repair:** split it into:

```text
ORDER_ONLY:
  correction claim present, objective correction not established;

PRIMITIVE_IMPERSONAL:
  a primitive P-source supplies scoped objective authority while personal,
  teleological, and Wisdom predicates remain false.
```

### X-F03 — `KeyAuthority` is an unexplained primitive in the nonimplication model

The candidate needs a typed relation between a key's authority and a source of
that authority. Otherwise compatibility/nonauthority is a vacuous extra Boolean
coordinate.

**Required repair:** define scoped `KeyAuthority(k,t,s)` as authority supplied
by at least one undefeated source not wholly constituted by the defeated token
closure. Keep the source's truth and fittingness as separate burdens.

### X-F04 — the primary checker omits two load-bearing implications

It does not enforce:

```text
Rad -> ObjCorr;
E -> not ObjCorr.
```

Its partition PASS therefore validates a weaker and partly incoherent table.

**Required repair:** independently encode both implications and rerun.

### X-F05 — Track-N authorization wording overreaches the formal model

H12/H16 can make a source object eligible in the frozen source-expanded class,
but do not establish source authenticity, Arabic-primary wording, or world
truth. Saying that the source premise “authorizes” the target without a declared
Track-N acceptance relation is too strong.

**Required repair:** add `TrackNSourceAuthorityAccepted` as an explicit
school/source-relative premise and retain neutral nonmigration.

## Nonblocking notes

1. TKAA-1 is a direct target-key specialization of Candidate E and the AR4
   anti-self-authorization family. General novelty is zero.
2. `AA` and `CL` carry the theorem. Their semantic appropriateness remains a
   philosophical burden; the proof cannot establish them.
3. The authority-source roles need not be mutually exclusive.
4. A trans-token authority source does not entail truth linkage, teleology,
   personal design, or Wisdom.
5. Compatibility, component validity, and target/world truth remain distinct.

## Required rereview

After repair, use a separately implemented exhaustive semantics that:

- constructs `Rad`, `ObjCorr`, `TokenKeyAuth`, and `KeyAuthority` from primitive
  assignments rather than trusting model labels;
- enforces `E -> not ObjCorr` and `Rad -> ObjCorr`;
- checks all four live authority routes and both R5 controls;
- verifies source nonmigration and compatibility nonauthorization;
- rechecks frozen hashes.
