# PMR-007 Frontier Round 14 V2 — invariant-core entry versus general co-Büchi restoration

```text
round: FRONTIER_ROUND_14_LOCAL_PROTOCOL_REACH_AND_STAY
version: V2
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repair_of: PMR-007 Round 14 V1
repository mutation: NONE
current disposition: FROZEN_PENDING_COLD_AUDIT
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Repair boundary

Round 14 V1 correctly characterized the stronger objective

```text
CORE-ENTRY:
force finite entry into one certified controller-invariant target core.
```

It incorrectly presented that region as complete for the weaker temporal
objective

```text
CO-BUCHI TARGET:
remain safe and have only finitely many non-target visits.
```

Fresh rereview produced `R14-F01`: a target state may stutter forever in one
branch, while another branch makes one final non-target visit and then settles
in a different target component. Every branch is eventually always target, but
there is no forced entry into one common invariant target kernel.

V2 preserves the V1 packet unchanged as rejected evidence and separates the two
winning regions.

# Part I — exact finite game model

## 2. Common protocol-state game

Let `Q` be finite. A state `q in Q` is a **common protocol state**: it is
available to every correct controller whose local decisions are represented by
the game, or has already been compiled into every correct local view. The model
does not prove that this common summary is truthful, complete, causally
adequate, or obtainable under an asynchronous protocol.

For each `q`, let:

```text
Pi(q):
  a finite nonempty set of locally implementable protocol fragments;

Succ(q,pi):
  a finite nonempty set of adversarial successor states.
```

A fragment is eligible for `Pi(q)` only after its one-step local choices pass
the declared local-factorization and warrant conditions, including the Round-13
`FRLA-1` correct-view component test where that specialization applies. The
controller chooses `pi`; the adversary chooses any state in `Succ(q,pi)`.

Let:

```text
Safe subseteq Q;
Target subseteq Safe;
Bad = Safe minus Target.
```

A path is winning for the general restoration objective iff it stays in `Safe`
and visits `Bad` only finitely many times. Equivalently, it is eventually always
in `Target`.

Define the safe controllable predecessor:

```text
Pre(X) = {
  q in Safe :
  exists pi in Pi(q), Succ(q,pi) subseteq X
}.
```

Every successor set is nonempty, so `Pre` has no vacuous winning action.

# Part II — the stronger invariant-core objective

## 3. Stable target kernel and core-entry region

Define:

```text
K = nu X. [Target intersect Pre(X)].
```

`K` is the greatest target-contained region in which the controller can keep
every permitted successor inside the same region.

Define:

```text
W_core = mu Y. [K union Pre(Y)].
```

Equivalently, start from `Y_0=K` and repeatedly add safe states with an eligible
fragment whose successors all lie in the preceding approximation.

### CORE-1 — exact core-entry characterization

A state lies in `W_core` iff a memoryless locally implementable strategy keeps
every path safe, forces finite entry into `K`, and keeps every later state in
`K subseteq Target`.

This is the exact surviving scope of V1. Its rank argument is unchanged: least
attractor rank decreases on every pre-kernel transition.

# Part III — general co-Büchi restoration

## 4. Nested fixed point

For a fixed `Z subseteq Safe`, define:

```text
F_Z(X) =
  (Target intersect Pre(X))
  union
  (Bad intersect Pre(Z)).
```

Let:

```text
H(Z) = nu X. F_Z(X).
```

The candidate general region is:

```text
W_coB = mu Z. H(Z)
      = mu Z. nu X. [
          (Target intersect Pre(X))
          union
          (Bad intersect Pre(Z))
        ].
```

The outer least fixed point counts the remaining admissible non-target visits.
The inner greatest fixed point permits arbitrary target stuttering while
requiring every actual non-target step to enter a lower outer approximation.

## 5. COB-1 — finite perfect-information co-Büchi characterization

At the declared finite common-state scope, a state `q` belongs to `W_coB` iff
there exists a memoryless locally implementable strategy such that every
adversarial path from `q`:

```text
1. remains in Safe; and
2. visits Bad only finitely many times.
```

### 5.1 Positive direction and strategy extraction

Let:

```text
Z_0 = empty;
Z_(i+1) = H(Z_i).
```

Because `H` is monotone and `Q` is finite, the sequence is increasing and
stabilizes at `W_coB`. For each `q in W_coB`, let `r(q)` be the least positive
index with `q in Z_r(q)`.

At a bad state `q in Z_r`, the fixed-point equation supplies a fragment with:

```text
Succ(q,pi) subseteq Z_(r-1).
```

At a target state `q in Z_r`, it supplies a fragment with:

```text
Succ(q,pi) subseteq Z_r.
```

Fix one such fragment per state. The resulting strategy is memoryless. Target
steps never increase outer rank. Every bad-state step strictly lowers it. Hence
an adversarial path from rank `r` has at most `r` bad-state occurrences. All
selected successor sets lie in `Safe`. Therefore every path is safe and
eventually always target.

### 5.2 Converse direction

Fix a memoryless strategy winning the co-Büchi objective from `q`. In the
strategy-induced directed graph, no reachable directed cycle contains a bad
state: if one did, the adversary could traverse that cycle indefinitely and
produce infinitely many bad visits.

For `k >= 0`, let `R_k` be the set of states from which every induced path has at
most `k` future bad-state occurrences, counting the current state when it is
bad. Let `R_-1=empty`. Finiteness and the absence of a reachable bad cycle imply
that every winning start belongs to some `R_k`; indeed, no bad state can recur
on a path.

For every `k`:

```text
target q in R_k  => every selected successor is in R_k;
bad q in R_k     => every selected successor is in R_(k-1).
```

Thus `R_k` is a post-fixed point of `F_(R_(k-1))`, so:

```text
R_k subseteq H(R_(k-1)).
```

Inductively, `R_(k-1) subseteq Z_k`; monotonicity of `H` then gives:

```text
R_k subseteq H(Z_k) = Z_(k+1).
```

Every memoryless winning start therefore lies in the outer least fixed point
`W_coB`. This proves the equivalence. ∎

## 6. Memoryless sufficiency and exact ceiling

The proof constructs a memoryless strategy and shows that any memoryless
winning strategy is represented by the fixed point. At this finite,
perfect-information, turn-based controller/adversary scope, memoryless
strategies are therefore sufficient.

Nothing in `COB-1` establishes memoryless sufficiency under:

```text
partial observation;
private or inconsistent protocol-state views;
adversarially forged message histories;
dynamic membership not compiled into Q;
stale certificate eligibility;
randomized or probabilistic objectives;
unbounded state;
or nondeterministic local observations not already resolved in Pi(q).
```

Those settings require a belief/information-state game, a cross-state local
factorization constraint, a different acceptance objective, or additional
memory.

# Part IV — relation between the two regions

## 7. Inclusion

```text
W_core subseteq W_coB.
```

A strategy that forces finite entry into one invariant target kernel has only
finitely many bad visits, so `CORE-ENTRY` implies the co-Büchi objective.

## 8. Strict separation: mandatory `R14-F01` regression

Let all three states be safe and:

```text
Target = {0,2}.

state 0:
  only successor set {0};

state 1:
  only successor set {0};

state 2:
  only successor set {0,1,2}.
```

Then:

```text
K       = {0};
W_core  = {0,1};
W_coB   = {0,1,2}.
```

From state 2, one branch stays in target state 2 forever. Another makes one
final bad visit to state 1 and then stays in target state 0 forever. The
adversary cannot force infinitely many bad visits, but state 2 cannot force
entry into the single invariant kernel `{0}` because self-successor 2 remains
available.

Thus:

```text
certified finite entry into one common target core
is strictly stronger than
general branch-dependent eventual target persistence.
```

The executable check preserves this witness and finds 300 strict-separation
cases in the exhaustive three-state antichain-reduced class.

# Part V — executable verification

## 9. Declared exhaustive class

The checker removes controller actions whose successor set strictly contains
another available action: such an action is dominated under universal
adversarial choice and cannot enlarge either winning region. It then exhausts:

```text
all nonempty antichain action menus per state;
all action-menu tuples;
all Safe/Bad/Target state labelings;
all memoryless strategies;
all games with one, two, or three states.
```

Direct temporal truth is computed independently from the fixed point: for each
memoryless strategy, it constructs the induced graph and rejects a start iff an
unsafe state or a bad-containing directed cycle is reachable.

Results:

```text
action-menu tuples:                         5,849
Safe/Bad/Target-labelled games:           157,611
memoryless strategies evaluated:          804,585
fixed-point/direct mismatches:                   0
W_core subset failures:                          0
strict W_core subset W_coB cases:              300
```

A deterministic larger-state challenge additionally checked:

```text
random seed:                                 1402
four- and five-state labelled games:        10,000
memoryless strategies evaluated:           164,165
fixed-point/direct mismatches:                   0
W_core subset failures:                          0
```

These checks validate the implementation and preserve the regression. The
mathematical proof, not finite enumeration, controls the general finite claim.

# Part VI — guard deletion and adversarial extensions

## 10. Delete common-state observability

Suppose two global states require different fragments, but a correct agent has
the same local history in both. A strategy indexed by hidden `q` is a central
chooser. Applying `COB-1` directly to those global states is unsound. One must
quotient them into an information state or solve the corresponding
partial-observation game.

## 11. Delete stable fragment eligibility

A fragment may pass `FRLA-1` at one source, version, membership, or invalidator
state and become unwarranted later. If `Pi(q)` is not recomputed or its expiry is
not represented in `Succ`, the fixed point certifies a stale policy. Version and
source changes reopen both predecessor and target membership.

## 12. Delete successor adequacy

Omitting an adversarial transition can manufacture both `W_core` and `W_coB`.
Adding a permitted successor can only shrink them. Neither region certifies that
`Succ` is a complete causal or operational model.

## 13. Delete target adequacy

A state can be stable under the represented predicate while the substantive
burden remains unlanded, the source is false, or the target is proxy-blind.
`COB-1` proves a temporal strategy theorem relative to `Target`; it does not
establish target truth or restoration.

## 14. Dynamic membership and adversarial messages

When membership, authentication, or message semantics evolves, either:

```text
1. compile the relevant epoch and certificate state into Q and recompute Pi,
   Succ, Safe, and Target; or
2. move to a richer game whose information and transition objects expose the
   change.
```

A static common-state game cannot silently absorb dynamic membership.

# Part VII — ancestry and credit

## 15. Theorem-family relation

| Object | Ancestry | Exact relation | Credit ceiling |
|---|---|---|---|
| `W_core` | V1, T363–T364 finite invariance, standard reachability | `PRESERVED_STRONGER_OBJECTIVE` | no new general game credit |
| `W_coB` nested fixed point | standard finite co-Büchi game theory | `APPLICATION_WITH_ORTHEMIC_PROTOCOL_FILTER` | no new general mathematical novelty |
| local fragment eligibility | FRLA-1, LIF-1, AR2/AR3 transport | `COMPOSITION` | no duplicate local-synthesis origin |
| source/version reopening | AR3/AR4 dependency and contract families | `SCOPED_APPLICATION` | no source-truth credit |
| `R14-F01` | fresh post-merge defect witness | `BLOCKING_COUNTERMODEL_AND_SCOPE_REPAIR` | governance and architecture-repair value |

The substantive gain is not discovery of the standard co-Büchi calculus. It is
the exact repair of the integrated architecture:

```text
local implementability and warrant filter
+
finite adversarial temporal game
+
explicit separation of common-core certification from branch-dependent
persistence.
```

# Part VIII — cross-lane consequences

## 16. Candidate B

Round 14 V2 replaces one overloaded restoration predicate with two typed
certificates:

```text
CORE_CERTIFIED:
finite entry into one invariant target core, with one reusable core witness;

PERSISTENCE_CERTIFIED:
every path has finitely many bad visits, possibly through branch-dependent
terminal target components.
```

This changes the route-gradient burden. A runtime may legitimately return a
persistence certificate without possessing one global invariant-core
certificate. Conversely, daee may require the stronger core object when it
needs a durable reusable source/target certificate rather than eventual output
behavior.

Still open:

```text
causal landing;
source and target truth;
whole-field reread completeness;
dynamic bypass outside the frozen model;
metaortheme mutation;
non-scalar route selection;
actual daee implementation correspondence.
```

## 17. Candidate A and AR3

`FRLA-1` supplies only the one-state fragment filter. Candidate A must still
construct common protocol states and preserve local implementability across
histories, faults, version changes, and dynamic membership. AR3 transport
contracts may remove fragments or transitions; successful transport does not
itself produce common knowledge of the current game state.

## 18. Candidate C

A strategy can reach or persist in a represented state labelled `one root` while
world-level unity, numerical identity, source fidelity, or mentality is false.
Candidate C can supply constraints on `Target` and fragment eligibility, but it
cannot inherit operational temporal success as a metaphysical conclusion.

## 19. daee implementation correspondence requirement

A future implementation audit must determine whether daee distinguishes:

```text
stable invariant target core;
eventual target persistence;
transient bad-state visits;
source/version invalidation;
reopened burden;
STOP/HOLD/RECURSE/PARTIAL/RESTORE dispositions;
and causal versus merely represented transition closure.
```

Vocabulary compatibility is insufficient. No exact implementation audit is
claimed in this packet.

# Part IX — disposition

## 20. Authority ceiling

```text
candidate identity:
PMR-007-ROUND14-V2 / COB-1

provenance:
POST_MERGE_RESEARCH_CANDIDATE pending audit

historical identity:
NONE

proof authority:
human-readable proof plus executable finite verification;
not Lean parsed, elaborated, or kernel checked;
not externally reviewed.

source/world authority:
NONE beyond declared typed game assumptions.

general mathematical novelty:
0; standard finite co-Büchi fixed-point mechanism.

orthemological value:
blocking repair, typed certificate separation, and integration constraint for
local-protocol restoration.

repository readiness:
NOT YET — cold audit and distinct fresh rereview required.

meniscus:
MENISCUS_NOT_REACHED.
```
