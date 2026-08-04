# PMR-007 Frontier Round 14 V2 cold audit

```text
audit relation: same-model procedural cold audit over frozen V2 hashes
external human review: false
independent model-lineage review: false
overall disposition: PASS_WITH_NONBLOCKING_NOTES
```

## 1. Frozen custody

The audit used the frozen receipt:

```text
e3db880891dc6baf7ba48f166951ecd4ef3b66ca5afe57e5a77a00c31919505b
  PMR-007_FRONTIER_ROUND14_LOCAL_PROTOCOL_REACH_AND_STAY_FIXED_POINT_V2.md

b7b72e676f474e3f8dc3f0e870e67454c04612380e658d1fda944f1e9dda2d9d
  checks/pmr007_round14_v2_cobuchi_check.py

9789cf7cc81cd6d5a9d3bf12c8958034743017321bd9db2dfa78993794715905
  checks/pmr007_round14_v2_cobuchi_check_results.json
```

All three hashes reproduced. Round 14 V1 and its `R14-F01` finding remain
separate and byte-unchanged.

## 2. Game and quantifier audit

`PASS.` The model fixes a finite common-state, perfect-information game in which
the controller selects one eligible local fragment and the adversary selects
one successor from a nonempty successor set. `Pre(X)` has the correct quantifier
order:

```text
exists eligible controller fragment;
for all adversarial successors, successor lies in X.
```

`Pre` is restricted to safe states, while every fixed-point approximant lies in
`Safe`; an unsafe successor cannot be hidden by the operator.

The theorem does not silently claim that the common state, action eligibility,
successor relation, target, or safety predicate is truthful or causally
adequate.

## 3. Nested fixed-point audit

`PASS.` For fixed `Z`,

```text
F_Z(X) =
  (Target intersect Pre(X))
  union
  (Bad intersect Pre(Z))
```

is monotone in `X` and in `Z`. Its greatest fixed point `H(Z)` is therefore
well-defined on the finite powerset lattice, and `H` is monotone in `Z`; the
outer least fixed point is well-defined.

The positive proof uses the least outer-approximation rank correctly:

```text
target transition: rank does not increase;
bad transition: successor rank strictly decreases.
```

It follows that the number of bad-state occurrences is bounded, while target
stuttering may be unbounded. This is precisely the co-Büchi objective and no
longer forces arrival at one common target core.

The converse proof is sound. Under a fixed memoryless strategy, a reachable
cycle containing a bad state would allow the adversary to force infinitely many
bad visits. In a finite winning strategy graph, no bad state can recur on a
path; hence a finite bound on bad occurrences exists. The `R_k` post-fixed-point
induction then places every winning start in the outer least fixed point.

## 4. `W_core` versus `W_coB`

`PASS.` The surviving V1 region is correctly renamed and retained as the
stronger core-entry certificate. Any core-entry strategy satisfies co-Büchi, so
`W_core subseteq W_coB`.

The mandatory three-state regression reproduces:

```text
K      = {0}
W_core = {0,1}
W_coB  = {0,1,2}
```

Thus V2 repairs rather than suppresses `R14-F01`.

## 5. Executable audit

`PASS.` The checker compares the nested fixed point with direct memoryless
strategy enumeration and graph-cycle semantics over the declared exhaustive
class:

```text
action-menu tuples:                         5,849
Safe/Bad/Target-labelled games:           157,611
memoryless strategies evaluated:          804,585
fixed-point/direct mismatches:                   0
W_core subset failures:                          0
strict-separation cases:                        300
```

It also checked 10,000 deterministic random four- and five-state games and
164,165 memoryless strategies with zero mismatch or inclusion failure.

The antichain reduction is sound for this universal-adversary setting: if one
action's successor set strictly contains another available action's successor
set, the larger set is never more helpful for a controller objective closed
under removal of adversarial successors. The exhaustive counts therefore cover
all one-to-three-state games up to removal of dominated actions.

## 6. Memoryless and scope audit

`PASS_WITH_NONBLOCKING_NOTES.` Memoryless sufficiency is proved only for the
finite common-state perfect-information game. The packet correctly withholds:

```text
partial-observation sufficiency;
asynchronous common-state construction;
randomized or probabilistic objectives;
dynamic membership not encoded in Q;
stale-certificate safety;
causal adequacy;
source or target truth;
actual noetic restoration;
and daee implementation correspondence.
```

The outer rank is a correctness certificate, not asserted to be a minimal cost,
minimal time, or scalar restorative potential.

## 7. Ancestry and novelty audit

`PASS.` The nested co-Büchi mechanism is standard finite game theory. The packet
claims zero general mathematical novelty and records the contribution as an
architecture repair and typed integration of:

```text
local protocol/warrant eligibility;
adversarial temporal control;
core-entry versus persistence certificates;
and dependency-directed source/version reopening.
```

No historical theorem identity, source truth, world truth, Candidate-C
conclusion, or meniscus credit is transferred.

## 8. Findings

```text
blocking findings: 0
nonblocking findings: 4
```

Nonblocking findings:

1. A Lean or independently implemented proof is still absent.
2. The checker validates finite implementation but cannot validate the modeled
   source, target, successor, or causal semantics.
3. Partial-observation and evolving-membership games require a new formal
   object rather than direct reuse of this fixed point.
4. An actual daee stack audit is required before mapping either certificate to
   `RESTORE`, `PARTIAL`, `HOLD`, or `RECURSE` behavior.

## 9. Disposition

```text
repair required: false
frozen V2 may proceed to distinct direct-temporal fresh rereview: true
repository ready: false
owner adoption eligible: only after fresh rereview and owner decision
PMR-007 may close: false
meniscus: MENISCUS_NOT_REACHED
```
