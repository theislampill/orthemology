# PMR-007 Frontier Round 16 repair log

```text
repair relation: V2 repairs frozen Round 16 V1
repository altered: false
historical identity assigned: false
blocking findings addressed: 2 / 2
fresh rereview: PENDING AT FREEZE
```

## R16-R01 — prior-discharge enforcement

Repairs `R16-F01`.

```text
before:
preserved obligations were copied into the next discharged set without proving
they existed at the input;

after:
preserved_obligations must be a subset of the actual prior discharged set.
```

Regression:

```text
VCT-F01 removes reason-valid from the initial certificate and is rejected with
preserved-obligation-not-discharged.
```

## R16-R02 — exact reason-DAG boundary custody

Repairs `R16-F02`.

```text
before:
only version, claim, and root were chained between edges;

after:
node-map domain must equal the current reason-node set, input dependency edges
must exactly equal the current dependency graph, mapped edges must appear in
the output graph, and every output edge endpoint must lie in the output node
set.
```

Regression:

```text
VCT-F02 injects an alien edge-2 input node and is rejected with
reason-dag-boundary-mismatch.
```

## Preserved ceiling

The repair does not establish:

```text
source truth;
external model completeness;
original RP-T2/RP-T40 byte custody;
general novelty;
external review;
owner adoption;
or repository readiness before fresh rereview.
```
