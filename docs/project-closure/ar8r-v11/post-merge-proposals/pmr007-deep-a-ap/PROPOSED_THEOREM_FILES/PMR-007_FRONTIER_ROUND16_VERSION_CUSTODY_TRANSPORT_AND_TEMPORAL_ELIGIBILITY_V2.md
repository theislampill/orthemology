# PMR-007 Frontier Round 16 V2 — version-custody transport, reason-DAG composition, and temporal eligibility reopening

```text
round: FRONTIER_ROUND_16_VERSION_CUSTODY_AND_ELIGIBILITY
version: V2
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repair_of: PMR-007 Frontier Round 16 V1
repository mutation: NONE
current disposition: FROZEN_REPAIRED_PENDING_FRESH_REREVIEW
primary candidates: Candidate A + Candidate B interface
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Repaired scope

V1's same-byte/version countermodel, action-menu monotonicity theorem, and stale
temporal-certificate witness survived cold audit. Two defects blocked its
transport-composition checker:

```text
R16-F01:
obligations could be called preserved without having been discharged at the
input;

R16-F02:
adjacent edges were not required to share the same complete reason-DAG
boundary.
```

V2 preserves V1 as rejected pre-repair evidence and makes both requirements
mechanical.

# Part I — active evidence and ancestry

## 2. Opened evidence

Round 16 used the actual contents of:

```text
PMR-AGCOM-01;
AR2/AR3 collective-backbone reconciliation;
PMR-AGCOM-02 V2;
PMR-AGCOM-06 V2;
PMR-LANG-01 V2;
PMR-LANG-02 V2;
Round 14 V2;
Round 15 V2 and its admitted implementation correspondence.
```

The preserved AR2/AR3 reconciliation identifies:

```text
RP-T2:
exact finite reason-preserving transport relative to an independent target
warrant contract;

RP-T4:
no silent action or threshold inheritance;

RP-T32:
reason-forgetting can identify warranted and unwarranted transports;

RP-T40:
policy inheritance additionally requires authenticity/currentness,
delegation, conflict resolution, and execution scope.
```

The standalone RP-T2/RP-T40 packets were not present in the surfaced local
bytes. V2 therefore claims ancestry through the exact indexed reconciliation,
not fresh custody of their original theorem wording.

# Part II — subordinate same-byte result

## 3. LANG-VERSION-01

For one exact artifact byte string, two recipient contexts differ only in the
version guard:

```text
current-v1:
  App, Auth, Ver, Evid, Cap, Perm, InvClosed all true;
  Applicable=true.

stale-v2:
  Ver=false, every other guard true;
  Applicable=false.
```

Thus:

```text
same bytes do not entail same applicability.
```

This is a subordinate strict specialization/application of PMR-AGCOM-01,
PMR-LANG-01, RP-T2, and RP-T40. It receives no independent theorem credit and
does not close Round 16 by itself.

# Part III — repaired reason-certificate transport

## 4. Transport state

At each path boundary, the exact certificate state is:

```text
version;
frozen claim;
provenance root;
finite reason-node set;
finite directed dependency-edge set;
and actually discharged target obligations.
```

Each edge declares:

```text
input and output version/claim/root;
node map;
input and output dependency edges;
preserved obligations;
revalidated obligations;
complete target-required obligations;
semantic commutation;
authority and re-delegation scope;
and open invalidators.
```

## 5. VCT-1 — repaired finite path-composition characterization

A finite path transports warrant to its final declared contract if every edge
satisfies all of the following against the **actual preceding certificate**:

```text
1. version, claim, and root input equal the prior output;
2. node-map domain equals the prior reason-node set;
3. input dependency edges equal the prior dependency-edge set;
4. the node map sends every prior dependency edge to an output dependency edge;
5. every output dependency-edge endpoint belongs to the mapped output-node set;
6. every obligation labelled preserved was actually discharged at the input;
7. preserved plus revalidated obligations cover the complete target-required
   set;
8. the frozen-claim semantic square commutes;
9. provenance root custody is preserved, unless a separately warranted new
   independent root is explicitly introduced;
10. authority/delegation is valid, and any intermediate re-delegation is
    permitted;
11. no registered invalidator is open.
```

### Proof

Induct on the path. Conditions 1–3 establish exact boundary identity. Conditions
4–5 make the reason-node map a dependency-preserving transport of the actual
input DAG. Condition 6 prevents warrant creation by relabeling. Condition 7
closes the complete next target contract. Conditions 8–11 preserve semantic,
root, authority, and invalidator custody. The output node set, dependency set,
and discharged obligations therefore form the exact input state for the next
edge. Function and graph-map composition preserve these properties. The final
certificate satisfies every final required obligation. ∎

VCT-1 is a finite implementation-level specialization of AR3's established
reason-preserving transport architecture. It is not assigned new general
mathematical novelty.

## 6. Positive two-edge witness

The registered path transports:

```text
v1 / claim-v1 / ROOT-A
  -> v2 / claim-v2 / ROOT-A
  -> v3 / claim-v3 / ROOT-A.
```

At each step:

```text
the complete reason-DAG boundary matches;
source-authentic and reason-valid were already discharged before preservation;
version and authority are revalidated;
final capability and permission are revalidated;
semantic squares commute;
no invalidator is open.
```

The final v3 contract is therefore satisfied.

## 7. Repair regressions

Two new fixtures fail closed:

```text
VCT-F01-PRESERVED-OBLIGATION-LAUNDERING
  deletes reason-valid from the initial discharged set while the first edge
  calls it preserved;
  exact failure: preserved-obligation-not-discharged.

VCT-F02-REASON-DAG-BOUNDARY-DRIFT
  replaces one edge-2 input node with an alien node;
  exact failure: reason-dag-boundary-mismatch.
```

The four prior weakened-path controls remain:

```text
noncomposable pairwise compatibility;
dropped invalidator;
non-redelegable authority;
semantic noncommutation.
```

# Part IV — temporal eligibility

## 8. VAM-1 — fixed-model action-menu monotonicity

For fixed states, Safe, Target, observations, faults, and successor sets, if:

```text
Pi_restricted(q) subseteq Pi_full(q)
```

for every state, then:

```text
K_restricted      subseteq K_full;
W_core_restricted subseteq W_core_full;
W_coB_restricted  subseteq W_coB_full.
```

The restricted controllable predecessor is pointwise smaller. Monotonicity of
the relevant greatest, least, and nested fixed points gives the result.

The converse direction for newly admitted actions is nondecrease. No claim is
made when version change also modifies the state abstraction, Target, fault
model, observations, or successors.

## 9. VST-1 — stale action eligibility reopens restoration

For:

```text
Safe={q0,q1}; Target={q0};
q0 --hold0--> {q0};
```

version v1 admits at q1:

```text
repair -> {q0};
linger -> {q1}.
```

Version v2 receives the exact same repair bytes, but the recipient version
contract fails and removes `repair` from the eligible menu. Only `linger`
remains.

Therefore:

```text
v1: W_core = W_coB = {q0,q1};
v2: W_core = W_coB = {q0}.
```

An old temporal certificate reused without revalidating action custody
provably overclaims q1.

This gives a typed dynamic-bypass chain:

```text
source or runtime version changes
REOPEN transport/applicability obligations
RESTRICT eligible actions
CHANGE the temporal-model digest
REQUIRE winning-region recomputation.
```

# Part V — executable evidence

## 10. Primary V2 checks

```text
same-byte applicability contexts: 2 / 2 exact;
positive composed path: PASS;
repair regressions: 2 / 2 exact failure;
weakened-path controls: 4 / 4 withheld;
temporal stale-eligibility witness: PASS.
```

Action-menu monotonicity checks:

```text
exhaustive labelled games, n=1 and n=2: 444
restricted-menu pairs: 3,252
failures: 0

random labelled games, n=3 and n=4: 20,000
seed: 1607
failures: 0
```

The human proof controls the finite theorem. The checker validates its
implementation and concrete integration witness.

# Part VI — frontier changes

## 11. Candidate A

Round 16 replaces a flat receipt/applicability guard list with a path object
whose reason DAG, provenance root, semantic map, target obligations, version,
and authority are compositional. It still does not solve distributed discovery
of that path under private views, faults, or dynamic membership.

## 12. Candidate B

Round 16 closes the version-custody omission in Round 15's temporal certificate:

```text
action eligibility is a versioned reason-transport conclusion, not a static
menu annotation.
```

Stable restoration requires temporal closure and ongoing source/version
revalidation. The next Candidate-B burden is to bind this architecture to real
daee state extraction, intervention records, and successor completeness.

## 13. Other lanes

```text
TAC/SAC and false tawātur:
  retransmission does not create a new root, and a drifted certificate does not
  preserve identity or independence by byte equality;

Fusha/Qamus:
  transcluded lexical or grammatical bytes remain availability until the
  occurrence/version contract is closed;

Candidate C/source ascent:
  source-version or translation changes may reopen a premise, but temporal
  stability never supplies source truth or a world bridge;

theorem origin:
  reformatting or migrating one reason DAG does not create a new theorem root.
```

# Part VII — exact credit and repaired disposition

## 14. Family adjudication

```text
LANG-VERSION-01:
COROLLARY / APPLICATION;

VCT-1:
STRICT SPECIALIZATION / IMPLEMENTATION COMPOSITION of indexed RP-T2/RP-T40;

VCT-2 controls:
GUARD-DELETION COUNTERMODELS;

VAM-1:
STANDARD FIXED-POINT MONOTONICITY CONSEQUENCE;

VST-1:
POST-MERGE INTEGRATED APPLICATION connecting Candidate A version custody to
Candidate B temporal reopening.
```

```text
general mathematical novelty: 0
historical theorem identity: NONE
external review: OPEN
owner adoption: PENDING
repository mutation: NONE
```

## 15. Status pending distinct rereview

```text
V1 cold audit: REPAIR_REQUIRED
blocking findings repaired: R16-F01, R16-F02
V2 primary check: PASS
fresh rereview: PENDING
repository proposal: NOT YET READY
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```
