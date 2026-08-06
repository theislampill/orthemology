# PMR-007 Frontier Round 15 V2 — DAEE local closure, temporal nonidentifiability, and model-bound restoration certificates

```text
round: FRONTIER_ROUND_15_DAEE_TEMPORAL_CERTIFICATE
version: V2
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repair_of: PMR-007 Frontier Round 15 V1
repository mutation: NONE
repository snapshot: cc91f41fec364ea3910b80d57252bb1e0a050278
current disposition: FROZEN_REPAIRED_PENDING_FRESH_REREVIEW
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Repair boundary

Round 15 V1 established two substantive points:

```text
1. the current daee transition contract enforces event-local governance and
   closure honesty but does not own a multi-step temporal model;

2. one exact current-valid CLOSURE record is compatible both with stable
   persistence and with a future dynamic bypass.
```

Its cold audit found two blocking certificate defects:

```text
R15-F01:
certificate identity was not cryptographically bound to canonical model bytes;

R15-F02:
CORE_ENTRY strategy checking showed only possible reachability of the kernel,
not forced progress under every adversarial successor.
```

V1 remains preserved and unadmitted. V2 repairs only those reproduced defects
and adds a nontrivial two-state attractor control.

# Part I — exact current-main implementation evidence

## 2. Repository snapshot and opened owners

The supplied current-main archive identifies:

```text
repository: theislampill/orthemology
main SHA: cc91f41fec364ea3910b80d57252bb1e0a050278
archive SHA-256:
ec5314442cc6212cad0cd5cd9fcdfb835567f4847830445c8f7529ea8422a04e
```

The following actual implementation owners were opened and inspected:

```text
applications/daee-epistemics/CORRECTIVE-TRANSITION.schema.json
applications/daee-epistemics/CORRECTIVE-TRANSITION.example.json
applications/daee-epistemics/CORRECTIVE-TRANSITION-FIXTURES.yaml
applications/daee-epistemics/SEMANTIC-OPERATOR-CONTRACT.yaml
applications/daee-epistemics/NOETIC-FIELD-DYNAMICS.yaml
applications/daee-epistemics/CURRENT-RUNTIME-BOUNDARY.md
applications/daee-epistemics/CURRENT-RUNTIME-CROSSWALK.yaml
scripts/validate_corrective_transition.py
scripts/validate_semantic_operator_contract.py
scripts/validate_daee_current_crosswalk.py
scripts/validate_meta_noetic_memetics.py
```

All four current validators reproduce with zero failures.

## 3. Current mechanical scope

The current `orthemology-corrective-transition-v2` schema and validator enforce,
among other conditions:

```text
selected route belongs to eligible routes;
a ranking witness exists;
strict soundness may not be claimed by a runtime transition;
CLOSURE requires a performed reread;
runtime closure may not be equated with observed human uptake;
addressed and carried-forward burdens exactly and disjointly partition the
  live burdens;
global revision requires explicit authorization and a reference;
runtime_closure is true exactly when terminal_posture is CLOSURE;
historical-v1 bytes and migration provenance are preserved.
```

The semantic-operator contract keeps route pressure, event-local transition,
field diagnostics, loop break, whole-state reread, and runtime closure typed as
non-factive control, diagnostic, or runtime predicates. The field-dynamics
owner calls the G1 order a `proposed-candidate`, rejects raw burden count as a
potential, permits incomparability and holds, and records
`no-guaranteed-convergence`.

Those are real governance guards. They are not a temporal stability theorem.

The base transition contract has no typed, mechanically checked owner for:

```text
finite states;
Safe and Target predicates;
controller action menus;
adversarial successor sets;
source/version epoch binding of action eligibility;
successor-model completeness;
certificate kind;
canonical model digest;
stable target kernel;
co-Büchi winning region;
strategy witness;
fixed-point/progress rank;
or the distinction between invariant-core entry and branch-dependent eventual
persistence.
```

# Part II — exact current-stack nonidentifiability result

## 4. Shared current-valid record

The local record

```text
models/PMR007_ROUND15_SHARED_CURRENT_TRANSITION_RECORD.json
SHA-256:
da0b58ac75391c8ba4387332e5c7be3bdda578a4363f23c626d1f08e102d799f
```

passes the actual current-main transition validator. It reports local CLOSURE,
a performed reread, exact empty live-burden accounting, no strict-soundness
claim, no observed human uptake, and explicit nonclaims about future successors
and persistence.

## 5. DAEE-TEMP-NI-1 — local closure does not determine temporal stability

Two finite future-transition models share that exact current-valid record.

### Stable extension

```text
states = {q_closed}
Safe = Target = {q_closed}
q_closed --hold--> {q_closed}
```

Then:

```text
q_closed in W_core
q_closed in W_coB
```

### Dynamic-bypass extension

```text
states = {q_closed,q_bad}
Safe = {q_closed,q_bad}
Target = {q_closed}
q_closed --reopen--> {q_bad}
q_bad --persist_bad--> {q_bad}
```

Then:

```text
q_closed not in W_core
q_closed not in W_coB
```

Therefore, over this extension class:

```text
current corrective-transition record
  does not determine invariant-core membership;
current corrective-transition record
  does not determine co-Büchi persistence.
```

This is an implementation-scope boundary, not a defect in the current record at
its declared episode-local purpose.

# Part III — V2 model-bound certificate architecture

## 6. Separate certificate object

V2 does not overload the current transition record. It adds a separate local
research object containing:

```text
certificate and model identities;
canonical model SHA-256;
finite states;
Safe and Target sets;
a nonempty action menu at every state;
nonempty adversarial successor sets;
source/version epoch;
per-action eligibility reference and epoch;
a declared successor-completeness assertion for the certificate scope;
certificate kind: CORE_ENTRY or CO_BUCHI_PERSISTENCE;
exact declared winning region;
selected memoryless strategy;
progress rank;
stable kernel for CORE_ENTRY;
transition-record digest;
and explicit nonclaims.
```

The transition record can support an eligibility reference. It is not itself
the finite temporal model.

## 7. Canonical model custody

The `model_digest` is SHA-256 over compact UTF-8 JSON with sorted keys. Its
owned fields are exactly:

```text
source_version_epoch;
sorted states;
sorted Safe states;
sorted Target states;
model_completeness;
and, sorted by state and action ID:
  state,
  action_id,
  sorted successors,
  eligibility_ref,
  eligibility_epoch.
```

It deliberately excludes:

```text
certificate identity and kind;
transition-record digest;
declared theorem answer and witnesses;
and nonclaims.
```

Thus a state, target, action, successor, eligibility, epoch, or completeness
edit changes model custody, while a different certified objective over the same
model need not create a false second model identity.

## 8. TRC-1 — exact model-relative acceptance characterization

At the declared finite perfect-information scope:

```text
CORE_ENTRY certificate acceptance
iff
  its model digest matches the canonical finite model;
  its stable kernel and winning region equal the exact K and W_core fixed
    points;
  its selected strategy keeps every successor in the winning region;
  every selected successor from K remains in K;
  every selected successor outside K has strictly smaller attractor rank;
  and its declared rank equals the exact least-attractor rank.

CO_BUCHI_PERSISTENCE certificate acceptance
iff
  its model digest matches the canonical finite model;
  its winning region equals the exact nested W_coB fixed point;
  its selected strategy keeps every successor in that region;
  target-state successors weakly decrease the exact outer rank;
  bad-state successors strictly decrease it;
  no reachable strategy-induced directed cycle contains a bad state;
  and its declared rank equals the exact least outer-approximation rank.
```

The fixed points are those admitted in Round 14 V2:

```text
K      = nu X. [Target intersect Pre(X)]
W_core = mu Y. [K union Pre(Y)]

W_coB  = mu Z. nu X. [
           (Target intersect Pre(X))
           union
           ((Safe minus Target) intersect Pre(Z))
         ]
```

with:

```text
Pre(X) = {
  q in Safe:
  exists eligible action pi with Succ(q,pi) subseteq X
}.
```

### Proof basis

For CORE_ENTRY, the exact attractor layer of a non-kernel winning state is
positive. Choosing an action whose every successor lies in the prior layer
strictly decreases rank under every adversarial choice. Kernel actions remain
inside K. Finiteness forces entry and permanent residence.

For co-Büchi persistence, Round 14 V2 proves that target steps can be selected
to remain within the current outer approximation while bad-state steps enter
the preceding approximation. Therefore target steps weakly decrease outer rank
and bad steps strictly decrease it. Conversely, a reachable bad-containing
cycle would let the adversary force infinitely many bad visits. Exact region
recomputation, rank checking, and the direct cycle test jointly fail closed.

# Part IV — repaired executable controls

## 9. Valid certificates

Three certificates pass:

```text
TRC-CORE-CONTROL-1
  one-state stable kernel;

TRC-COB-R14-F01-1
  the mandatory Round-14 strict-separation model:
  K={q0}, W_core={q0,q1}, W_coB={q0,q1,q2};

TRC-CORE-ATTRACTOR-2
  a genuine two-state attractor in which q1 must select reach0->{q0}, not
  linger->{q0,q1}.
```

The canonical model digests are:

```text
TRC-CORE-CONTROL-1
4b8b1ebf7959b47c4192f64c8cfe3b312b6ca29387a963e3cd9f800654e9221a

TRC-COB-R14-F01-1
1fc1d879fae4e8fbf2a4e98e4bf6d511d4b783a6e1dd9c8b34ab8d45e0b9b0cb

TRC-CORE-ATTRACTOR-2
3e0526ba0db9e1fc6e9a7c517e1c9273e9cb6ebf6d0d2b861a2ccadb24c2062f
```

Seven negative fixtures fail at their exact registered guard:

```text
TRC-F01  false CORE_ENTRY region;
TRC-F02  stale action-eligibility epoch after legitimate digest recomputation;
TRC-F03  no declared complete successor relation after legitimate digest
         recomputation;
TRC-F04  nonexistent selected action;
TRC-F05  false fixed-point rank;
TRC-F06  model-digest drift;
TRC-F07  nonforcing CORE_ENTRY strategy with a nondecreasing adversarial
         successor.
```

The V2 checker also reruns the four current-main daee validators and reproduces
the stable/bypass collision before admitting the local certificate checks.

# Part V — exact authority ceiling

## 10. What acceptance establishes

Acceptance establishes only:

```text
model custody under the declared canonicalization;
and
exact temporal status and witness validity relative to the declared finite
perfect-information model.
```

It does not establish:

```text
external-world model completeness;
truth or sufficiency of an eligibility reference;
source truth;
target adequacy;
causal burden landing;
absence of hidden states or burdens;
human uptake or interior restoration;
fiṭrah restoration;
soul access;
partial-observation implementability;
randomized or unbounded-state correctness;
or world-directed truth.
```

The field

```text
declared_successor_relation_complete_for_scope: true
```

is an explicit model-owner assertion. A local checker can require and bind it;
it cannot prove that omitted real transitions do not exist.

## 11. Relation to current terminal postures

Current main uses:

```text
STOP / HOLD / PARTIAL / RECURSE / CLOSURE.
```

V2 does not rename CLOSURE as RESTORE. It supplies two optional, distinct
future-facing coordinates:

```text
CORE_CERTIFIED;
PERSISTENCE_CERTIFIED.
```

They may accompany a local posture only after their own model and evidence
custody is satisfied. Neither substitutes for source, target, causal, or human
restoration verdicts.

# Part VI — whole-program consequences

## 12. Candidate B

Round 15 changes a central Candidate-B burden:

```text
before:
  whether current daee closure and reread vocabulary already enforced stable
  restoration was unresolved at implementation level;

after:
  current main is exactly event-local;
  temporal stability is not identifiable from its present transition record;
  a separate model-bound certificate can enforce exact finite core-entry or
  co-Büchi persistence relative to a declared transition abstraction.
```

The next burden is constructive and causal:

```text
derive or audit the state abstraction, action eligibility, successor relation,
source/version reopening rules, target semantics, and model-completeness claim
against the actual daee runtime and interventions.
```

## 13. Candidate A and AR3

The action menu `Pi(q)` presupposes locally implementable, warrant-bearing
fragments. AR3 reason transport, recipient version custody, authority,
capability, invalidators, and authorization determine which fragments are
eligible. Under partial observation, common-state construction itself becomes a
Candidate-A distributed-synthesis burden.

## 14. Candidate C

Source-faithful and metaphysical work may constrain Target and evidence
contracts. No temporal certificate validates those source or world premises. A
stable represented predicate can remain source-misbound or world-false.

## 15. T351–T354 and T363–T365

V2 operationalizes, without duplicating theorem credit:

```text
cutset and burden-accounting guards;
dynamic-bypass sensitivity;
local-step versus stable-region separation;
source-semantic and reread boundaries;
and the non-scalar route-order firewall.
```

Its rank is an objective-specific progress witness, not one uniquely warranted
scalar route-gradient and not a total noetic-improvement measure.

# Part VII — family, novelty, and disposition

## 16. Theorem family and prior-art class

```text
finite reachability/core and co-Büchi fixed points:
  standard game/model-checking mechanisms;

canonical model digest and certificate recomputation:
  standard proof-carrying/model-checking custody pattern;

current-record temporal nonidentifiability:
  exact current-stack application of the established profile/fibre boundary;

general mathematical novelty:
  0.
```

The integrated contribution is an exact implementation diagnosis and a repaired
certificate architecture that keeps event-local closure, temporal stability,
source custody, causal landing, and human restoration formally separate.

## 17. Repaired disposition pending rereview

```text
DAEE-TEMP-NI-1:
ADMITTED CANDIDATE PENDING FRESH REREVIEW

TRC-1:
ADMITTED CANDIDATE PENDING FRESH REREVIEW

proof status:
human derivation plus primary executable check

cold audit:
V1 REPAIR_REQUIRED — R15-F01 and R15-F02

repair status:
IMPLEMENTED IN V2

external review:
OPEN

owner adoption:
PENDING

repository readiness:
NOT YET — distinct fresh rereview required

historical identity:
NONE

general novelty:
0

integrated champion:
NONE

meniscus:
MENISCUS_NOT_REACHED
```
