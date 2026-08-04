# PMR-007 Frontier Round 13 V1 — fault-robust local agreement and restorative certificates

```text
round: FRONTIER_ROUND_13_FAULT_ROBUST_LOCAL_AGREEMENT
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
current disposition: FROZEN_PENDING_COLD_AUDIT
```

# Part I — finite fault-scenario class

## 1. Scenarios, correct local views, and warranted outputs

Fix a finite agent set `I`, finite local-view sets `L_i`, and a finite typed
output space `U`. An output object may contain:

```text
action;
reason certificate;
source/provenance root;
target and version;
authority and permission;
restorative route;
execution and resource witness.
```

A finite scenario `s` specifies:

```text
M_s subseteq I       participating members;
F_s subseteq M_s     faulty or adversarial members;
C_s = M_s \ F_s      correct members, required nonempty;
l_i(s) in L_i        complete local view of each correct i;
O_s subseteq U       outputs both correct and warranted in s.
```

The local view already includes every delivered message, source/version tag,
certificate fragment, and fault-generated datum visible to that agent. The
scenario family must therefore include every adversarial message pattern,
membership state, snapshot, and source/target state covered by the claim.

A deterministic local agreement protocol is a family

```text
f_i : L_i -> U
```

such that in every scenario `s` all correct agents output one common object
`u_s in O_s`:

```text
for all i,j in C_s, f_i(l_i(s)) = f_j(l_j(s)) = u_s in O_s.
```

Faulty agents need not comply. The theorem concerns only the declared finite
one-step scenario class; it does not solve asynchronous Byzantine agreement in
general.

# Part II — exact component characterization

## 2. Correct-view agreement graph

Create one vertex for every correct local-view token `(i,l)` that appears in a
scenario. For each scenario `s`, connect all vertices

```text
{(i,l_i(s)) : i in C_s}
```

into one clique. Reappearance of the same `(i,l)` token across scenarios uses
the same vertex. Let `K(s)` be the connected component containing the correct
view tokens of `s`; the scenario clique guarantees they lie in one component.

For each used component `K`, define

```text
O(K) = intersection { O_s : K(s)=K }.
```

## 3. FRLA-1 — exact fault-scenario local-agreement criterion

A deterministic local agreement protocol exists **iff**

```text
O(K) is nonempty for every used component K.
```

### Proof

Necessity: one local-view token has one deterministic output. Equality inside
every scenario clique and token reuse along a path force the same output on an
entire connected component. That output must belong to `O_s` for every scenario
in the component, hence to `O(K)`.

Sufficiency: choose `u_K in O(K)` for every used component and define each
appearing token in `K` to output `u_K`. Extend arbitrarily to unused local
views. Every scenario's correct tokens lie in one component and therefore agree
on an object belonging to its `O_s`. ∎

## 4. Algorithmic consequence

With output sets represented extensionally, the criterion is decidable by:

```text
union-find over correct-view tokens and scenario cliques;
then one intersection of output sets per component.
```

This is linear up to output-set intersection cost. It is a closed-form
specialization of the general local-factorization CSP, not a new distributed
computing algorithm.

# Part III — fault, membership, and provenance controls

## 5. Hidden fault-pattern countermodel

Use three agents `A,B,C` and two scenarios:

```text
s0:
  correct = {A,B};
  local views = {A:x, B:y0};
  O_s0 = {alpha};

s1:
  correct = {A,C};
  local views = {A:x, C:z1};
  O_s1 = {beta};
```

Each scenario separately has a valid common output. Agent `A` has the same
local view in both, so the agreement graph connects both scenario cliques into
one component. Its output intersection is empty. No deterministic local
protocol is robust to both fault/membership possibilities.

A centralized chooser that sees the scenario can choose `alpha` or `beta`; that
does not provide a locally implementable protocol.

## 6. Same action, incompatible warrant

Let `alpha=(RESTORE,c_alpha)` and `beta=(RESTORE,c_beta)`. The surface action is
identical while the recipient-valid certificates are disjoint. A protocol that
outputs only `RESTORE` hides the warrant failure. FRLA-1 must be applied to
complete typed output objects, not action labels alone.

Thus behavioral agreement is weaker than warranted agreement, and copied action
availability does not create transport of its reason.

## 7. Monotonicity under a larger adversarial class

Adding scenarios, fault patterns, message patterns, or membership states can:

```text
add constraints to an existing component;
merge components through a reused local view;
or add a new component.
```

It cannot enlarge any pre-existing component intersection. Therefore
feasibility is monotone nonincreasing as the declared adversarial scenario class
is enlarged. Removing a scenario or fault pattern may restore feasibility but
weakens the claim.

## 8. Public evidence can split the component

Suppose a truthful public bit `q(s)` is received and known by every correct
agent. Replace each token `(i,l_i(s))` by `(i,l_i(s),q(s))`. In the two-scenario
countermodel, `q(s0)=0` and `q(s1)=1` splits the previously shared `A:x` token;
each new component has a nonempty output intersection.

This is a repair only when the bit is:

```text
truthful;
commonly available to all correct members;
source/currentness bound;
and allowed by the communication and fault model.
```

A private or forgeable bit does not automatically refine the common component.

# Part IV — relation to established families

## 9. Exact ancestry adjudication

| Round-13 object | Established ancestor | Relation | Credit consequence |
|---|---|---|---|
| one-step local functions | Round 4 LIF-1 / AR2 local-uniform synthesis family | `STRICT_SPECIALIZATION` | no independent theorem origin |
| component equality closure | equality-CSP connected-component elimination | `COROLLARY` | no general novelty |
| complete output intersection | Candidate A A1 warranted terminal cells | `APPLICATION_ONLY` | no duplicate hypergraph theorem |
| reason-certificate object | AR3 RP-T2/RP-T40 family | `APPLICATION_ONLY` | no silent inheritance |
| fault/membership scenarios | AR2 fault/membership boundaries | `SCOPED_RECONCILIATION` | exact historical payload not renamed |

FRLA-1 is substantive because it converts the static fault/membership
agreement subcase of LIF-1 into an exact component-intersection test and makes
the hidden-central-chooser obstruction explicit. It is not a new general
Byzantine-agreement theorem.

# Part V — cross-candidate flywheel

## 10. Candidate A

Transferred:

```text
private-view indistinguishability;
correct-agent agreement;
provenance-bearing output objects;
fault and dynamic-membership scenario expansion;
public-evidence repair.
```

Not transferred:

```text
common knowledge beyond the declared public signal;
randomized/asynchronous termination;
Byzantine threshold bounds;
causal independence of evidence roots;
truth of certificates.
```

Round 13 closes the one-step deterministic equality-constraint subcase of
`A-FRONTIER-2`. The multi-round, asynchronous, randomized, resource-bounded,
and actively queried cases remain open.

## 11. Candidate B

Let `O_s` contain only restorative action-certificate pairs that are target,
source, route, custody, and execution valid in scenario `s`. FRLA-1 then
characterizes when one locally implementable common restorative object exists
across the fault/view component.

Not transferred:

```text
reach-and-stay dynamics;
causal landing;
dynamic bypass resistance;
whole-field reread;
objective target adequacy;
scalar restorative value.
```

A one-step common action can still lead to different future states or reopen
error paths. Round 13 supplies an actor-local entry condition for Candidate B,
not stable restoration.

## 12. Candidate C cross-attack

A population can locally agree on one root label or one source certificate
through FRLA-1 while the corresponding metaphysical unity, numerical identity,
modal persistence, or source truth is false. Conversely, strengthening the
world/source obligations shrinks `O_s` and can destroy operational agreement.

Operational convergence therefore neither proves nor is guaranteed by the
Candidate-C world claim.

# Part VI — exact evidence use and next frontier

## 13. Evidence-use record

```text
upstream supplied:
  Round 4 LIF-1 local-factorization CSP;
  Candidate A terminal-cell and provenance distinctions;
  Round 6 hidden-target/fault-class sensitivity;
  Round 8 communication rectangles;
  AR3 reason-certificate and policy-transport coordinates;
  Candidate B restorative action/certificate split.

transferred:
  local-view variables;
  equality obligations among correct agents;
  complete typed output sets;
  scenario-class expansion;
  hidden-central-chooser falsifier.

not transferred:
  historical theorem identity;
  general Byzantine-agreement novelty;
  common knowledge;
  certificate truth;
  causal restoration;
  metaphysical unity.

reverse feedback:
  Candidate A must expose every fault/message/membership scenario that can
  reuse a correct local view;
  Candidate B must combine FRLA feasibility with robust dynamic winning and
  causal certificates;
  Candidate C cannot use operational consensus as a unity bridge.
```

## 14. Updated integrated A/B frontier

```text
AB-FRONTIER-2:
extend the component-intersection criterion to repeated locally implementable
belief games with evolving private histories, asynchronous or adversarial
messages, changing membership, source/version drift, certificate-fragment
composition, fairness/resource bounds, and intervention-dependent dynamics;
characterize when a common local protocol achieves causally certified
reach-and-stay rather than one-step agreement.
```

## 15. Round disposition

```text
positive object:
  FRLA-1 exact correct-view-component intersection characterization.

negative objects:
  hidden fault/membership central chooser;
  same-action/incompatible-certificate failure;
  monotone loss under expanded adversarial classes;
  private/forgeable signal nonrepair.

novelty:
  strict specialization and closed-form elimination of established local-CSP
  and AR2/AR3 families; no general theorem novelty claimed.

integrated champion:
  NONE.

meniscus:
  MENISCUS_NOT_REACHED.
```
