# PMR-007 Frontier Round 15 V1 cold audit

```text
audit relation: same-model procedural cold audit over frozen V1 hashes
external human review: false
independent model-lineage review: false
overall disposition: REPAIR_REQUIRED
```

## 1. Frozen packet

The following frozen hashes reproduced:

```text
51a6ca884f40945824de8313812c8ce3f6f648ce8596c4f3ae0a8ff37a402ee5
  PMR-007_FRONTIER_ROUND15_DAEE_TEMPORAL_CERTIFICATE_ARCHITECTURE_V1.md

da0b58ac75391c8ba4387332e5c7be3bdda578a4363f23c626d1f08e102d799f
  models/PMR007_ROUND15_SHARED_CURRENT_TRANSITION_RECORD.json

17ed6c842069f52d7682bd7ecde9057d861d069c40af8fce146d113b5127b84e
  models/PMR007_ROUND15_TEMPORAL_RESTORATION_CERTIFICATES.yaml

cfe612f46434d494e235aea7a313c428d143f80a66cccc0fabb4d087aa6c9997
  checks/pmr007_round15_temporal_certificate_check.py

02465b1e7f505bba152aef8697ceb4f66097c7999e3745a87d7be523d20dfb6a
  checks/pmr007_round15_temporal_certificate_check_results.json
```

## 2. Current-main implementation audit

`PASS.` The packet uses the actual current-main transition schema, validator,
semantic-operator contract, runtime boundary, current crosswalk, and field
model. Four current validators reproduce with zero failures.

The implementation conclusion is appropriately bounded:

```text
current main enforces event-local governance and closure honesty;
it does not mechanically own a finite successor game or temporal certificate.
```

The stable/bypass twins share one exact current-valid record and differ in both
`W_core` and `W_coB`. This is a valid current-stack nonidentifiability witness.

## 3. Blocking finding R15-F01 — no certificate model digest

The prose requires a model identity and digest, but the V1 certificate objects
contain only `model_id`. The checker recomputes against whichever state/action
model happens to be present in the YAML and does not bind the certificate to a
canonical model digest.

Consequences:

```text
a later state, target, action, successor, or epoch edit can silently change the
model while retaining the same certificate identity;
validation proves the edited object, not custody of the originally reviewed
model.
```

Required repair:

```text
define canonical model bytes over:
  source_version_epoch;
  states;
  Safe;
  Target;
  action IDs;
  successors;
  eligibility references;
  eligibility epochs;
  model-completeness declaration;

require `model_digest` to equal SHA-256 of those canonical bytes;
add a digest-tampering negative fixture.
```

## 4. Blocking finding R15-F02 — CORE_ENTRY strategy witness is checked existentially

For a `CORE_ENTRY` certificate, V1 checks:

```text
reachable(selected_strategy,q) intersects K.
```

That only shows that **some** branch can reach the kernel. Under adversarial
successors, the strategy must force every branch into `K`.

A two-state control exposes the gap:

```text
K={q0};
q1 has action reach0 -> {q0};
q1 also has action loop1 -> {q1};
W_core={q0,q1}.
```

A certificate can declare the correct region and rank while selecting `loop1`.
The V1 checker accepts closure of the strategy inside `W_core`, and
`reachable(q1)` intersects no kernel only if the graph has no alternate path;
more generally an action with successors `{q0,q1}` would pass the existential
check while allowing the adversary to remain at `q1` forever.

Required repair:

```text
for q in K:
  every selected successor remains in K;

for q in W_core minus K:
  every selected successor has strictly lower declared attractor rank;

add a correct two-state attractor certificate and a negative fixture whose
selected action permits nondecreasing rank.
```

## 5. Nonblocking authority notes

1. `declared_successor_relation_complete_for_scope: true` remains an owner/model
   assertion, not external proof of model completeness.
2. Eligibility references are typed locators; their substantive warrant is not
   revalidated by this checker.
3. The current-transition validator's PASS does not establish temporal, causal,
   source, or target adequacy.
4. The certificate architecture is standard model checking plus exact
   current-stack integration; general mathematical novelty remains zero.

## 6. Disposition

```text
blocking findings: 2
nonblocking findings: 4
repair required: true
V1 admission: prohibited
Round 15 may close: false
PMR-007 may close: false
meniscus: MENISCUS_NOT_REACHED
```
