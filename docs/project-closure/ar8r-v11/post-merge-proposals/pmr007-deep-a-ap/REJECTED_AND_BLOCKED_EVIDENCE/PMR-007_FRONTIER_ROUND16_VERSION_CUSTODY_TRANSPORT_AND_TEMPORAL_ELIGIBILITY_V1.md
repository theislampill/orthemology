# PMR-007 Frontier Round 16 V1 — version-custody transport, action eligibility, and temporal-certificate reopening

```text
round: FRONTIER_ROUND_16_VERSION_CUSTODY_AND_ELIGIBILITY
version: V1
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repository mutation: NONE
current disposition: FROZEN_PENDING_COLD_AUDIT
primary candidates: Candidate A + Candidate B interface
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Central burden

Round 15 established that finite temporal restoration certificates are exact
only relative to a declared action/successor model. Round 16 asks when an action
whose implementation artifact was warranted under one source/target version
remains eligible after communication, migration, or runtime version change.

The central distinction is:

```text
same artifact bytes
!=
same recipient applicability
!=
same authority
!=
same action eligibility
!=
same temporal winning region.
```

The goal is not another isolated profile nonimplication. It is a composition and
reopening architecture connecting AR3-style reason transport to Round-14/15
stable-restoration games.

# Part I — exact institutional ancestry

## 2. Evidence used

The following exact current post-merge artifacts were opened:

```text
PMR-AGCOM-01
  recipient contract:
  Rec, App, Auth, Ver, Evid, Cap, Perm, InvClosed;
  target-local characterization is a strict specialization of AR3 RP-T2;
  permission/execution separation is an RP-T40 application.

AR2/AR3 collective-backbone reconciliation
  RP-T2: exact finite reason-preserving transport relative to an independent
         target-warrant contract;
  RP-T4: no silent action/threshold inheritance;
  RP-T32: forgetting reasons can merge warranted and unwarranted transports;
  RP-T40: policy inheritance additionally needs authenticity/currentness,
          delegation, conflict resolution, and execution scope.

PMR-AGCOM-02
  surface receipt does not determine direct bearer, independent provenance
  root, or authority.

PMR-AGCOM-06
  delivery, acknowledgment, finite higher-order knowledge, and common
  knowledge are distinct protocol states.

PMR-LANG-01
  version and authority can be load-bearing coordinates for a frozen target
  query even where one proposition survives translation.

PMR-LANG-02
  token type alone does not decide occurrence meaning; richer context/version
  profiles are sufficient only when the target is constant on their fibres.

Round 14 V2
  exact CORE_ENTRY and co-Büchi winning regions.

Round 15 V2
  current daee transition records are event-local;
  model-bound temporal certificates bind action eligibility to a source/version
  epoch.
```

The original standalone RP-T2 and RP-T40 theorem packets were not surfaced in
the present local byte set. Their preserved indexed reconciliation controls the
ancestry classification; this packet does not reconstruct their wording.

# Part II — same bytes and local contract change

## 3. LANG-VERSION-01 — same bytes, different applicability

Fix one artifact byte string and one recipient-side finite contract:

```text
Applicable(c,a)
iff
App and Auth and Ver and Evid and Cap and Perm and InvClosed.
```

Two contexts receive the exact same artifact bytes:

```text
current-v1:
  every guard true;
  Applicable=true.

stale-v2:
  Ver=false;
  every other guard true;
  Applicable=false.
```

This is the declared subordinate `PMR-007-LANG-VERSION-01` countermodel. It is a
strict specialization/application of PMR-AGCOM-01, PMR-LANG-01, RP-T2, and
RP-T40. It receives no independent theorem credit.

# Part III — finite reason-certificate transport

## 4. Typed path

A context carries:

```text
version;
frozen claim;
provenance root;
finite reason-certificate dependency DAG;
and a set of discharged target obligations.
```

A transport edge contains:

```text
input and output versions;
input and output claims;
input and output provenance roots;
a node map between reason DAGs;
input and output dependency edges;
preserved obligations;
revalidated target-local obligations;
the complete target-required obligation set;
semantic-commutation witness;
authority/delegation witness;
re-delegation scope;
and open invalidators.
```

## 5. VCT-1 — guarded finite path composition

For a finite transport path, suppose every edge satisfies:

```text
1. input version, claim, root, and reason-certificate boundary equal the prior
   edge output;
2. its node map preserves every load-bearing dependency edge;
3. every obligation called preserved was discharged at the input;
4. preserved plus revalidated obligations cover the target contract;
5. the semantic square commutes for the frozen claim;
6. provenance root custody is preserved or any new independent root is
   separately warranted;
7. authority/delegation is valid and any intermediate re-delegation is
   authorized;
8. no registered invalidator remains open.
```

Then the composed path yields a final certificate satisfying the final finite
target contract.

### Proof

Induct on path length. The empty path is its input certificate. At an edge,
conditions 1–3 make the map applicable to the actual preceding certificate;
condition 2 preserves its dependency DAG; conditions 4–5 preserve the target
claim and close the complete next contract; conditions 6–8 preserve root,
authority, and invalidator custody. The resulting output is therefore a valid
input certificate for the next edge. Composition of the node and semantic maps
preserves the same properties. At the final edge, the discharged set covers the
final required set. ∎

This is a finite compositional specialization of the established AR3
reason-transport architecture, not a new general transport theorem.

## 6. VCT-2 — local-looking edges need not compose

Four length-two controls block weakened readings:

```text
VCT-CM-NONTRANSITIVE-COMPATIBILITY
  pairwise compatibility labels exist, but no composed semantic migration map;

VCT-CM-DROPPED-INVALIDATOR
  an intermediate revocation is omitted by the next incomplete contract;

VCT-CM-NONREDELEGABLE-AUTHORITY
  A delegates to B without re-delegation power, while B purports to delegate
  to C;

VCT-CM-SEMANTIC-NONCOMMUTATION
  local maps exist but their composition changes the frozen target claim.
```

These are not world-complete communication models. They isolate exact custody
guards.

# Part IV — action-menu and temporal consequences

## 7. VAM-1 — action-eligibility refinement is monotone

Fix the state set, Safe set, Target set, and successor sets. Let two versions of
the controller action menus satisfy:

```text
Pi_restricted(q) subseteq Pi_full(q)
```

for every state. Then:

```text
K_restricted      subseteq K_full;
W_core_restricted subseteq W_core_full;
W_coB_restricted  subseteq W_coB_full.
```

### Proof

The restricted controllable predecessor is pointwise contained in the full
predecessor:

```text
Pre_restricted(X) subseteq Pre_full(X).
```

Greatest and least fixed points are monotone in a monotone operator parameter.
The target-kernel operator, the core-attractor operator (including the already
shrunk kernel), and both operators in the nested co-Büchi fixed point therefore
preserve the inclusion. ∎

Adding newly warranted actions yields the dual nondecrease result. No statement
is made if state, Safe, Target, successor, observation, or fault semantics also
change.

## 8. VST-1 — stale eligibility can invalidate a temporal certificate

Use two safe states with `Target={q0}`:

```text
q0:
  hold0 -> {q0}

q1 under current-v1:
  repair -> {q0}
  linger -> {q1}

q1 under stale-v2:
  linger -> {q1}
```

The `repair` action has the same bytes in both contexts but loses version
applicability at v2 and is removed from the eligible action menu.

Then:

```text
v1:
  W_core = W_coB = {q0,q1}

v2:
  W_core = W_coB = {q0}.
```

A v1 temporal certificate reused at v2 without eligibility revalidation
therefore overclaims q1.

This is the exact reverse edge from version/source custody into Candidate-B
stable restoration:

```text
version change
REOPENS action eligibility
REQUIRES temporal-model digest change
REQUIRES winning-region recomputation.
```

# Part V — executable evidence

## 9. Checks

The local checker confirms:

```text
same-byte applicability collision: PASS;
positive two-edge transport example: PASS;
four weakened-path countermodels: PASS;
VST-1 temporal reopening witness: PASS.
```

It also tests `VAM-1`:

```text
exhaustive one- and two-state labelled games: 444
restricted-menu pairs: 3,252
monotonicity failures: 0

random three- and four-state cases: 20,000
seed: 1607
monotonicity failures: 0
```

The theorem proof controls the general finite statement. Enumeration validates
the implementation and the concrete witness.

# Part VI — cross-lane significance

## 10. Candidate A

Round 16 narrows the distributed-transport burden from generic receipt to a
path-compositional certificate with exact target-contract and dependency-DAG
custody. The still-open theorem-strength problem is distributed construction of
a truthful common/information state and a complete set of admissible transports
under private observations, faults, and dynamic membership.

## 11. Candidate B

Round 16 supplies the version-custody rule missing from Round 15:

```text
an action remains in Pi(q) only while its exact recipient contract and
source/version certificate remain valid at q.
```

Stale eligibility is a formal dynamic-bypass mechanism. Stable restoration
therefore needs both temporal fixed-point evidence and version/source closure.

## 12. Candidate C, source work, and Fusha/Qamus

A source or translation update can change the semantic and authority contract
without changing rendered bytes. This can reopen a formal or runtime action,
but it does not itself settle source truth or a metaphysical conclusion.
Occurrence-level Fusha/Qamus transclusion is correspondingly availability, not
final applicability, until the occurrence/version contract is re-orthed.

# Part VII — ancestry and disposition

## 13. Theorem-family adjudication

```text
LANG-VERSION-01:
  COROLLARY / APPLICATION of PMR-AGCOM-01 and PMR-LANG-01;

VCT-1:
  STRICT SPECIALIZATION / IMPLEMENTATION-LEVEL COMPOSITION of AR3 RP-T2 and
  RP-T40, subject to the preserved indexed ancestry rather than reconstructed
  historical wording;

VCT-2:
  guard-deletion controls for VCT-1;

VAM-1:
  STANDARD MONOTONICITY CONSEQUENCE of Round 14 fixed points;

VST-1:
  integrated current-program application connecting version custody to
  temporal-certificate reopening.
```

```text
general mathematical novelty: 0
historical theorem identity: NONE
external review: OPEN
owner adoption: PENDING
repository mutation: NONE
```

## 14. Pre-audit status

```text
LANG-VERSION-01:
COMPLETE AS SUBORDINATE APPLICATION PENDING AUDIT

VCT-1 / VCT-2 / VAM-1 / VST-1:
FROZEN POST-MERGE CANDIDATES PENDING COLD AUDIT

integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```
