# Deep BX — Feasible minimal bridge-anchor cover (custody reissue V1)

## Custody and authority

```text
custody class: SEMANTIC_REISSUE_OR_REGENERATED_CUSTODY_COPY
original ephemeral packet bytes preserved: false
fresh consolidated recheck: PASS
historical identity: NONE
owner adoption: PENDING
external review: OPEN
general mathematical novelty: 0
repository adoption: NONE
GitHub mutation: NONE
```

The original files produced earlier in this execution block were lost at a runtime boundary before durable delivery. This packet is a semantic reissue grounded in retained execution outputs and a fresh consolidated checker. It is not exact-byte recovery of the lost packet.

## Proposal identity and disposition

```text
identity: PMR-007-MBAC-1
status: ADMITTED_POST_MERGE_SCOPED_CENTRAL_RESIDUAL_ANCHOR_COVER_RESULT
```

## Exact scoped claim

Let C be the set of model pairs with equal baseline experiment profile and different target values. Each independently eligible anchor h resolves the subset C_h of conflicts on which its values differ. A compatible anchor set S identifies the target together with the baseline profile if and only if the union of C_h over h in S equals C. With declared nonnegative costs, the minimum eligible bridge cost is exactly the weighted set-cover optimum over C. If one conflict lies in no eligible C_h, no combination from the frozen registry identifies the target.

## Proof or construction

The joint evidence tuple is equal on a conflict pair exactly when every selected anchor is equal on that pair. Thus target factorization fails exactly on uncovered conflicts. Feasibility and compatibility constraints merely restrict the available subsets; minimizing declared cost over identifying subsets is the corresponding constrained weighted set-cover problem.

## Mandatory controls

- target-equivalent anchor solves the mathematics but is epistemically ineligible
- unknown anchor values are not differences
- mutually incompatible anchors cannot be combined
- cardinality and declared cost may disagree
- sampling uncertainty is outside exact-map scope

## Conclusion ceiling

- no authority for any particular anchor
- no efficient algorithm claim
- no universal minimum across unregistered evidence

## Theorem-family relation

Finite fibre factorization plus standard constrained set cover; residual-correction parameter, zero novelty.
