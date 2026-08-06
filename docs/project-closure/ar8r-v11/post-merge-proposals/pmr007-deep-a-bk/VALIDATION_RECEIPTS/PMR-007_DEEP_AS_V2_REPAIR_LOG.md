# PMR-007 Deep AS V2 repair log

```text
candidate repaired: PMR-007-PFIT-1 V1
repaired version: V2
blocking findings repaired: 8 / 8
```

| Finding | Repair |
|---|---|
| AS-F01 | Replaced the circular recurrence with `V(S,J)` and explicit removal of the queried intervention. |
| AS-F02 | Corrected the strict-gap tree to query `i2` first, then `i1` or `i0`. |
| AS-F03 | Typed `O` as complete response/certificate objects and added a projection-sufficiency guard. |
| AS-F04 | Made feasibility, authorization, fixed hidden account, target, source/version, environment, and semantics explicit. |
| AS-F05 | Added account-truth and catalogue-completeness nonclaims. |
| AS-F06 | Required an independently warranted truth coordinate and added target-leakage controls. |
| AS-F07 | Excluded stochastic, bounded-error, interactive, history-dependent, state-changing, adversarial, and dynamic-membership readings. |
| AS-F08 | Classified Test Cover/decision-tree ancestry and set general mathematical novelty to zero. |

No substantive conclusion was strengthened beyond the deterministic finite account-identification scope.
