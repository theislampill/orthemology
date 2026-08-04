# PMR-007 Frontier Round 15 repair log

```text
repair relation: V2 repairs frozen Round 15 V1
historical payload altered: false
repository altered: false
blocking findings addressed: 2 / 2
fresh rereview: PENDING AT FREEZE
```

## R15-R01 — canonical model custody

Repairs cold-audit finding `R15-F01`.

Implemented:

```text
canonical compact UTF-8 JSON over:
  source/version epoch;
  sorted states, Safe, and Target;
  complete model-completeness mapping;
  sorted state/action records with action ID, sorted successors,
  eligibility reference, and eligibility epoch;

SHA-256 model_digest required before theorem witnesses are accepted;

negative fixture TRC-F06 mutates only the digest and must fail with
model-digest-mismatch;

TRC-F02 and TRC-F03 legitimately recompute the digest after changing model
content, proving that their own epoch/completeness guards remain independently
load-bearing.
```

The digest excludes the certificate kind and declared answer so that two
objectives over the same transition model do not create false model
multiplicity.

## R15-R02 — universal CORE_ENTRY progress

Repairs cold-audit finding `R15-F02`.

Implemented:

```text
for q in stable kernel K:
  every selected successor remains in K;

for q in W_core minus K:
  every selected successor has strictly smaller exact attractor rank;

redundant reachability-to-K check retained as defense against rank
implementation error.
```

Added:

```text
TRC-CORE-ATTRACTOR-2:
  q0 is the kernel;
  q1 has reach0->{q0} and linger->{q0,q1};
  the valid strategy chooses reach0;

TRC-F07:
  chooses linger and must fail with strategy-rank-not-decreasing.
```

## Additional co-Büchi hardening

The V2 checker now verifies the Round-14 outer-rank witness directly:

```text
target-state selected successors weakly decrease rank;
bad-state selected successors strictly decrease rank;
no reachable selected-strategy cycle contains a bad state.
```

This is not a new cold-audit finding; it closes the analogous witness gap
proactively.

## Preserved nonclaims

No repair claims:

```text
external model completeness;
source truth;
target adequacy;
causal or human restoration;
partial-observation implementability;
new general mathematics;
historical theorem identity;
or owner adoption.
```
