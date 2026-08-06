# PMR-007 Deep AS V1 cold audit

```text
disposition: REPAIR_REQUIRED
same-model procedural relation: yes
external independence: no
```

## Blocking findings

### AS-F01 — the adaptive recurrence did not track remaining interventions

The prose checker uses every intervention at most once, but the displayed recurrence retained the full intervention set at every child. Reuse is informationally redundant in the static deterministic model, yet the recurrence must either prove that fact or explicitly carry a remaining-intervention set to avoid circular self-reference.

### AS-F02 — the strict adaptive-gap explanation named the wrong first query

For rows `000,001,010,101`, querying the first coordinate leaves three accounts on one branch, so one further binary query cannot finish. The valid depth-two tree queries the third coordinate first; each branch then contains two accounts and is separated by a different second query.

### AS-F03 — surface responses and complete certificate objects could be conflated

Two accounts may choose the same surface action while differing in source, target, authority, version, reason, or warrant. Identification must use the declared complete response object, not an action projection unless projection sufficiency is separately proved.

### AS-F04 — intervention admissibility and state stability were not load-bearing enough

The theorem assumes feasible, authorized interventions and a fixed hidden account/response semantics. If an intervention changes the governing account, target, source contract, or environment classification, the static diagnosis theorem no longer applies.

### AS-F05 — account identification was vulnerable to truth overread

A response signature can identify which account generated the declared model without establishing that account true, normatively adequate, complete, or uniquely realized in the world.

### AS-F06 — the truth-divergence tests risked target leakage

A target/truth divergence intervention requires an independently warranted truth coordinate. Encoding the correct epistemic verdict in the intervention label or certificate is not evidence for the truth-linked account.

### AS-F07 — stochastic, randomized, and history-dependent readings were not sharply excluded

The finite theorem is deterministic and zero-error. Overlapping response distributions, sampling error, randomized policies, interactive protocols, hidden histories, and dynamic membership require different models.

### AS-F08 — theorem-family and novelty ceilings required explicit adjudication

The nonadaptive result is finite Test Cover/hitting-set theory; the adaptive result is standard decision-tree diagnosis. Candidate 1 and AR-T4 are adjacent interfaces rather than identical propositions. General mathematical novelty is zero.

## Required repair

Create V2 with a remaining-intervention recurrence, the corrected depth-two witness, complete-certificate projection guard, explicit feasibility/state-stability conditions, truth and catalogue nonclaims, independent truth/source guards, stochastic/dynamic exclusions, and exact family/novelty status.
