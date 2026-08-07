# PMR-007 Deep Round C V1 — cold audit

```text
audit epoch: B
candidate: PMR-007-ICR-1 V1
disposition: REPAIR_REQUIRED
blocking findings: 3
```

## DC-F01 — conclusion absence was partly metadata, not interpretation

The V1 checker treated `withheld_conclusions: true` as evidence that the
conclusion predicates were false.  A nonentailment witness requires explicit
predicate extensions or independently evaluated definitions.  Merely naming a
conclusion “withheld” is circular.

**Required repair:** give empty extensions for personality, intellect, agency,
Wisdom, Speech, revelation, Creatorhood, and common-bearer predicates and make
the checker evaluate those extensions.

## DC-F02 — Creatorhood failure lacked a complete scoped definition

`x` failed to originate `q_w`, but V1 did not explicitly classify `q_w` as a
contingent particular or state the scoped Creator conditions.  The control was
therefore under-typed.

**Required repair:** type contingent particulars and define the scoped Creator
condition using complete origination, agency, and nonborrowed efficacy.  Check
that no object satisfies it.

## DC-F03 — functional unity was asserted rather than instantiated

V1 stored the Deep-B equations but did not provide the full profile table or
check that the two-factor rival actually realizes the four allowed profiles and
excludes the other 28 marginal profiles.

**Required repair:** include and verify the explicit table and its proper-subset
property.

## Nonblocking authority notes

- “Necessary” remains necessity in the declared two-world constant-domain model,
  not an unconditional metaphysical result.
- “Externally real” and “abstract” are stipulated typed predicates used to test
  entailment; the checker does not establish their world truth.
- The bridge-deletion models are scoped formal controls, not exhaustive
  metaphysical possibility proofs.
- The theorem has zero general mathematical novelty.
