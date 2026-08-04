# PMR-007 Frontier Round 15 V2 fresh rereview

```text
review relation:
same-model procedural rereview over frozen repaired hashes;
separate implementation and direct temporal semantics;
not external human review;
not independent model-lineage confirmation

disposition:
PASS_WITH_NONBLOCKING_AUTHORITY_NOTES
```

## 1. Frozen-hash custody

All seven frozen repaired inputs matched:

```text
Round 15 V2 substantive packet;
shared current-valid transition record;
V2 certificate/model owner;
primary V2 checker;
primary V2 results;
V1 cold audit;
V2 repair log.
```

The primary result was treated as a frozen receipt. It was not the sole basis of
rereview.

## 2. Independent mechanisms

The rereview did not import the primary checker. It independently used:

```text
canonical compact-JSON model serialization and SHA-256;
complete memoryless-strategy enumeration for every supplied finite model;
Tarjan strongly connected components;
direct all-path CORE_ENTRY semantics;
direct no-reachable-bad-cycle co-Büchi semantics;
minimax worst-case steps to the stable kernel;
minimax worst-case bad-state occurrences;
independent guard-deletion assessment;
and the actual current-main daee validators.
```

## 3. Positive results

All three repaired certificates passed.

```text
TRC-CORE-CONTROL-1
  strategies enumerated: 1
  K = W_core = W_coB = {q_closed}
  exact core rank: q_closed -> 0

TRC-COB-R14-F01-1
  strategies enumerated: 1
  K = {q0}
  W_core = {q0,q1}
  W_coB = {q0,q1,q2}
  exact outer ranks: q0 -> 1, q1 -> 2, q2 -> 2

TRC-CORE-ATTRACTOR-2
  strategies enumerated: 2
  K = {q0}
  W_core = W_coB = {q0,q1}
  exact core ranks: q0 -> 0, q1 -> 1
```

For each certificate:

```text
canonical model digest matched;
source/version epochs matched;
successor completeness was explicitly declared;
direct region matched;
minimax rank matched;
selected strategy satisfied the direct temporal objective.
```

## 4. Negative fixtures

All seven fixtures failed at the exact intended guard:

```text
TRC-F01  winning-region-mismatch
TRC-F02  eligibility-epoch-mismatch
TRC-F03  successor-relation-not-declared-complete
TRC-F04  strategy-action-not-eligible
TRC-F05  rank-mismatch
TRC-F06  model-digest-mismatch
TRC-F07  strategy-rank-not-decreasing
```

The two cold-audit repairs are therefore effective:

```text
R15-F01 model-custody drift: CLOSED AT DECLARED V2 SCOPE
R15-F02 existential CORE strategy witness: CLOSED AT DECLARED V2 SCOPE
```

## 5. Current-main implementation regression

The shared local transition record still passes the actual current-main
transition validator. The following current validators all returned zero
failures:

```text
validate_corrective_transition.py
validate_semantic_operator_contract.py
validate_daee_current_crosswalk.py
validate_meta_noetic_memetics.py
```

No repository file was changed.

## 6. Admission and authority ceiling

```text
DAEE-TEMP-NI-1:
ADMITTED_POST_MERGE_SCOPED_RESULT

TRC-1:
ADMITTED_POST_MERGE_SCOPED_RESULT

implementation-correspondence finding:
ADMITTED_POST_MERGE_SCOPED_RESULT

external review:
OPEN

owner adoption:
PENDING

historical identity:
NONE

general mathematical novelty:
0

repository-proposal status:
EXTERNAL_REVIEW_REQUIRED + OWNER_ADOPTION_REQUIRED
```

The admitted scope is only:

```text
current-main event-local transition records do not determine future temporal
stability;

and

a model-bound finite certificate can exactly verify CORE_ENTRY or co-Büchi
persistence relative to its declared perfect-information transition model.
```

Still open:

```text
external-world model completeness;
eligibility-reference truth;
source truth;
target adequacy;
causal restoration;
hidden states or burdens;
partial-observation synthesis;
human or fiṭrah restoration;
external human review;
owner adoption;
and repository integration.
```

## 7. Frontier effect

Round 15 materially advances Candidate B because it changes the central
implementation question from vocabulary compatibility to a typed temporal
abstraction and certificate-custody problem. It also sends exact burdens to:

```text
Candidate A:
construct warranted common/information states and transport valid action
eligibility under version, authority, capability, and invalidator changes;

Candidate C:
justify source-faithful Target and evidence contracts without obtaining any
world conclusion from temporal stability alone;

daee implementation:
separate event-local CLOSURE from optional future CORE_CERTIFIED and
PERSISTENCE_CERTIFIED coordinates.
```

```text
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```
