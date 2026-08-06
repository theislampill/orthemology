# PMR-007 Frontier Round 14 V1 — locally implementable reach-and-stay under faults and drift

```text
round: FRONTIER_ROUND_14_LOCAL_PROTOCOL_REACH_AND_STAY
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
current disposition: FROZEN_PENDING_COLD_AUDIT
```

# Part I — common protocol-state game

## 1. Finite guarded game

Let `Q` be a finite set of **common protocol states**. The current `q in Q`
must be commonly available to the correct participants or be encoded in every
correct local view. It may summarize a public belief, source/version state,
membership epoch, or reread state; the theorem does not make that summary
complete or truthful.

At each `q`, freeze:

```text
Scen(q)      finite fault/message/membership scenario family;
Pi(q)        finite set of one-step locally implementable protocol fragments;
Succ(q,pi)   nonempty set of adversarial successor protocol states.
```

Every `pi in Pi(q)` is required to have passed the Round 13 FRLA-1 criterion on
`Scen(q)` with one complete typed action-certificate object per correct-view
component. Thus `Pi(q)` contains actor-local protocol fragments, not centralized
scenario-contingent actions.

Let

```text
Safe subseteq Q;
Target subseteq Safe.
```

`Target` is the declared target-satisfying set; membership does not establish
objective adequacy, source truth, or causal restoration.

## 2. Stable target kernel

Define the monotone operator

```text
Hold(X) = {
  q in Target :
  exists pi in Pi(q), Succ(q,pi) subseteq X
}.
```

Its greatest fixed point

```text
K = nu X. Hold(X)
```

is the largest declared target region in which a locally implementable protocol
can keep every permitted successor inside the region.

## 3. Finite safe attractor

Starting from `Y_0=K`, define

```text
Y_{n+1} = Y_n union {
  q in Safe :
  exists pi in Pi(q), Succ(q,pi) subseteq Y_n
}.
```

Let

```text
W = union_n Y_n.
```

Because `Q` is finite, the sequence stabilizes in at most `|Q|` strict growth
steps.

# Part II — exact theorem

## 4. LPRS-1 — local-protocol reach-and-stay characterization

A state `q` lies in `W` iff there exists a memoryless strategy selecting one
locally implementable fragment at every reached common protocol state such that
every adversarial path:

```text
remains inside Safe;
reaches K in finitely many steps;
and thereafter remains in Target forever.
```

### Proof

If `q in K`, choose a witnessing hold fragment. Greatest-fixed-point closure
keeps all successors in `K subseteq Target`. If `q` first enters `Y_{n+1}`, choose
a fragment whose successors lie in `Y_n`; the least admission rank decreases on
every transition, so every path reaches `K` in at most `n+1` steps while
remaining safe. Memoryless choices can be fixed once per state using the least
rank or a hold witness.

Conversely, let a memoryless strategy satisfy the objective. Its target states
from which every future path remains in `Target` form a post-fixed point of
`Hold`, hence lie in `K`. Every winning start must force finite arrival at that
set; backward induction on the maximum remaining path length places it in the
least attractor `W`. In a finite graph, if no uniform finite bound existed, an
adversary could follow a reachable cycle outside `K` and violate eventual
permanent entry. ∎

## 5. Monotonicity

The admitted sets `K` and `W` can only shrink when any of the following occurs:

```text
Pi(q) loses a locally implementable fragment;
Succ(q,pi) gains an adversarial successor;
Safe or Target is strengthened/shrunk;
a source/version/fault scenario removes a fragment from Pi(q).
```

They can grow only under a weaker claim or genuinely new protocol/evidence.
This is a dependency-directed reread rule, not a truth theorem for the target.

# Part III — strongest-reading and deletion countermodels

## 6. Delete local implementability

At one public state, suppose a central chooser can see which of the Round 13
fault scenarios is actual and choose `alpha` or `beta`, but a correct agent has
the same local view in both and the complete output sets are disjoint. A
centralized game may put the state in its predecessor while `Pi(q)` is actually
empty. The locally implementable game correctly excludes it.

Thus ordinary statewise `exists action` can hide a central chooser.

## 7. Delete the stable kernel

Use states `q0,q1` with:

```text
q1 in Target;
q0 not in Target;
q0 --pi--> q1;
q1 --rho--> q0.
```

A one-step local protocol reaches the target, but no target-invariant kernel
exists. Initial correction does not certify stable restoration; this is the
finite game form of dynamic bypass.

## 8. Delete common protocol-state custody

Let two globally different protocol states require different local fragments,
but some correct agent has the same complete local view and no common state
identifier. A strategy indexed by the hidden global `q` is a central chooser.
The states must be merged into one information state or subjected to a new
cross-state local-factorization constraint.

Thus `q` being common is a load-bearing guard, not a notational convenience.

## 9. Delete source/version closure

A fragment can be locally implementable and transition-successful while its
certificate is stale or invalid under a successor source/target version. If
that successor is omitted from `Succ` or the fragment remains in `Pi` after its
warrant expires, `K` is a false stable region.

The transition model and fragment eligibility must be reread after source,
version, membership, or invalidator change.

## 10. Delete causal adequacy

The game can encode a transition `q --pi--> q'` that correlates with
restoration without being its cause. LPRS-1 proves a strategy theorem relative
to `Succ`; it does not certify the causal model, burden landing, no-confounding,
or a substantive noetic transition.

# Part IV — computational and family status

## 11. Explicit finite computation

Given extensional `Pi` and `Succ`, both fixed points are computed in polynomial
time by repeated predecessor scans. This does not include the cost of deriving
`Pi(q)` from local-view constraints; Round 4 classifies the general finite
factorization as a CSP, and Round 13 gives a linear component test only for the
equality-output specialization.

## 12. Exact ancestry

| Object | Ancestor | Relation | Credit consequence |
|---|---|---|---|
| greatest target kernel | Candidate B / T363–T364 finite invariance family | `APPLICATION_ONLY` | no duplicate dynamic theorem |
| least safe attractor | standard finite reachability game / Round 3 | `COROLLARY` | no general novelty |
| local fragment filter | Round 13 FRLA-1 and Round 4 LIF-1 | `COMPOSITION` | no new local-synthesis origin |
| source/version reread | AR3/AR4 transport and impact families | `SCOPED_APPLICATION` | no historical identity |

The substantive result is the exact composition: public reach-and-stay choices
are restricted to actor-local, fault-robust, warrant-bearing protocol fragments.
It is not a new general game theorem.

# Part V — cross-candidate flywheel

## 13. Candidate A

LPRS-1 turns one-step fault-robust agreement into a repeated common-state
strategy. It preserves:

```text
private-view local implementability inside Pi;
complete typed output objects;
public/common protocol-state indexing;
adversarial successors;
source/version invalidation of fragments.
```

It does not settle asynchronous common-state construction, randomized
protocols, Byzantine thresholds, message authentication, or dynamic common
knowledge.

## 14. Candidate B

This is the strongest current integrated finite operational result in the B
lane:

```text
actor-local protocol feasibility
+ declared safe reachability
+ target invariance
=> finite reach-and-stay under every permitted successor.
```

Still not transferred:

```text
objective target adequacy;
causal efficacy;
whole-field reread completeness;
source-semantic truth;
actual human/noetic restoration;
unique scalar gradient.
```

## 15. Candidate C cross-attack

A locally implementable strategy can reach and stably remain in a represented
state labeled `one root` while the world-level unity premise is false,
incomplete, counterpart-relative, or source-misbound. Conversely, Candidate-C
source/world obligations may invalidate fragments and shrink `W`.

Operational stability and metaphysical truth remain separate coordinates.

# Part VI — evidence use and frontier

## 16. Exact evidence-use record

```text
upstream supplied:
  Round 3 public-belief reachability;
  Round 6 robust target/version game and dynamic bypass;
  Round 9 target-relative rank;
  Round 13 correct-view component criterion;
  T351–T364 cutset/dynamic-restoration family at preserved scope;
  AR3/AR4 version and dependency-reopening distinctions.

transferred:
  finite fixed-point mechanism;
  local-protocol eligibility filter;
  target-invariance condition;
  adversarial successor closure;
  rank-decrease certificate;
  source/version reread trigger.

not transferred:
  target truth;
  causal landing;
  common-state construction;
  asynchronous/fault threshold results;
  numerical identity or metaphysical unity;
  general game novelty.

reverse feedback:
  Candidate A must make common protocol-state formation and fragment
  composition explicit;
  Candidate B must causally certify Succ and target membership before calling
  W restorative;
  Candidate C can only constrain target/fragment eligibility, not inherit
  operational proof as world truth.
```

## 17. Updated A/B frontier

```text
AB-FRONTIER-3:
construct or sharply bound the common protocol-state and locally implementable
fragment layer under asynchronous/private communication, Byzantine messages,
dynamic membership, certificate-fragment composition, and resource/fairness
constraints; then causally validate the transition and target predicates used
by LPRS-1 and test bypass under source/version change.
```

## 18. Round disposition

```text
positive object:
  LPRS-1 exact finite locally implementable reach-and-stay characterization.

negative objects:
  hidden central predecessor;
  one-step target with dynamic bypass;
  noncommon protocol-state chooser;
  stale-version false kernel;
  correlation/causality nonbridge.

novelty:
  exact composition of standard fixed-point and established local-protocol
  mechanisms; no new general mathematics claimed.

integrated champion:
  NONE.

meniscus:
  MENISCUS_NOT_REACHED.
```
