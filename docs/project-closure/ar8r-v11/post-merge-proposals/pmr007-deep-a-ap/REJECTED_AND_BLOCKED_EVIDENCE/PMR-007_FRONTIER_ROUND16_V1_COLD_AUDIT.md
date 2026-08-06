# PMR-007 Frontier Round 16 V1 cold audit

```text
audit relation: same-model procedural cold audit over frozen V1 hashes
external human review: false
independent model-lineage review: false
overall disposition: REPAIR_REQUIRED
```

## 1. Frozen packet

All four V1 hashes reproduced:

```text
1e8b9ed10b1dd615e77c3e56f5d381bc6e9fcf0fe602aa85f430f1dd84d3c764
  PMR-007_FRONTIER_ROUND16_VERSION_CUSTODY_TRANSPORT_AND_TEMPORAL_ELIGIBILITY_V1.md

af3bd9c881e7c94ffc51afcda9a0a0cdaf82fd0df5186074da9d17e62f8d2fd7
  models/PMR007_ROUND16_VERSION_CUSTODY_AND_ELIGIBILITY.yaml

f252ca34705fd1d2eb09175af0c168a5ae4d859eb30353aaa7be2bd369e5fe32
  checks/pmr007_round16_version_custody_check.py

729dc63b47a8956850e74759feac7ffe0a4260b67619bba1afe1977048ee99a7
  checks/pmr007_round16_version_custody_check_results.json
```

## 2. Valid surviving results

The following are mathematically and semantically sound at their stated scope:

```text
LANG-VERSION-01 same-byte applicability collision;
VAM-1 action-menu restriction monotonicity for fixed Q, Safe, Target, and
successor semantics;
VST-1 two-state stale-eligibility reopening witness;
the four stated weakened-composition countermodels as abstract guard controls;
zero general mathematical novelty and AR3-application ancestry ceiling.
```

The finite monotonicity checker is consistent with the proof and reports zero
failures across the declared exhaustive and random classes.

## 3. Blocking finding R16-F01 — preserved-obligation laundering

The V1 theorem correctly requires:

```text
every obligation called preserved was discharged at the edge input.
```

The V1 checker does not enforce that requirement. At each edge it simply sets:

```text
discharged := preserved_obligations union revalidated_obligations
```

without checking:

```text
preserved_obligations subseteq prior discharged.
```

A path can therefore manufacture a missing warrant by relabeling it
`preserved`.

### Required repair

```text
track the actual discharged set across edges;
require every preserved obligation to be present at the input;
add a length-one or length-two negative fixture in which `reason-valid` is
missing initially but called preserved;
require exact failure: preserved-obligation-not-discharged.
```

## 4. Blocking finding R16-F02 — reason-DAG boundary not chained

The V1 theorem requires the complete input reason-certificate boundary of an
edge to equal the prior edge output. The checker compares only:

```text
version;
claim;
root.
```

It checks each edge's internal dependency-map inclusion, but does not require:

```text
edge i+1 node-map domain = edge i output nodes;
edge i+1 input dependency edges = edge i output dependency edges.
```

Two individually well-formed maps over unrelated reason DAGs can therefore be
spliced into one purported path.

### Required repair

```text
carry the current reason-node set and dependency-edge set;
require exact node-domain and input-edge boundary matches at every edge;
require output-edge endpoints to lie in the mapped output-node set;
add a boundary-drift fixture;
require exact failure: reason-dag-boundary-mismatch.
```

## 5. Nonblocking authority and method notes

1. The standalone RP-T2/RP-T40 theorem bytes are not in the presently surfaced
   local corpus. The indexed AR2/AR3 reconciliation supports the ancestry
   classification, but not a claim of fresh inspection of those original
   packets.
2. The four path countermodels are explicit abstract controls, but the V1
   executable checks reduce them to registered booleans rather than a common
   typed path validator.
3. Pairwise version compatibility need not be a transitive relation; the
   positive architecture correctly needs composable migration maps instead.
4. VAM-1 is monotonicity only under a fixed state/target/fault/observation
   model. A version change may alter more than action eligibility in reality.
5. Same bytes can also change semantics, not merely applicability. V1 does not
   claim otherwise.
6. Same-model cold audit and future rereview are not external independence.

## 6. Disposition

```text
blocking findings: 2
nonblocking findings: 6
V1 admission: PROHIBITED
repair required: true
Round 16 may close: false
PMR-007 may close: false
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```
