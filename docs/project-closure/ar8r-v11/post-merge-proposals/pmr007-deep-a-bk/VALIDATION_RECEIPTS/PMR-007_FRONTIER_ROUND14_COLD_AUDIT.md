# PMR-007 Frontier Round 14 cold audit — locally implementable reach-and-stay

```text
audit relation: same-model procedural audit over frozen V1 hashes
external human review: false
independent model-lineage review: false
overall disposition: PASS_WITH_NONBLOCKING_NOTES
```

## Fixed-point construction

`PASS.` `K` is the greatest target-contained set with a locally implementable
fragment whose every adversarial successor remains inside the set. The
increasing `Y_n` sequence is the least safe controllable predecessor attractor
to `K`. Nonempty successor sets prevent vacuous winning actions.

The rank proof is sound: every reach-phase transition strictly lowers the least
attractor rank, so all paths enter `K` within a uniform finite bound. The hold
witness then remains inside `K subseteq Target`. Conversely, under a fixed
memoryless winning strategy, any failure of uniform finite entry in a finite
graph yields a reachable cycle outside the stable target kernel. The strategy's
permanently-target region is a post-fixed point and hence lies in `K`.

## Local-protocol guard

`PASS_WITH_NONBLOCKING_NOTES.` Restricting `Pi(q)` to Round-13-admissible local
fragments blocks the hidden central predecessor. The theorem additionally
requires `q` to be common protocol information. If agents cannot distinguish
two `q` states, state-indexed choices must be refactored through their actual
local histories; the packet explicitly preserves that guard.

The theorem does not construct common protocol states or enumerate all local
fragments. Those remain independent A-lane burdens.

## Executable evidence

`PASS.` The checker compared the fixed points against explicit enumeration of
all memoryless strategies over:

```text
exhaustive two-state games plus deterministic three-state samples;
3,441 games;
24,624 memoryless strategies;
2,000 successor-enlargement monotonicity cases.
```

No fixed-point/strategy mismatch or monotonicity violation occurred. The
one-step-target/dynamic-bypass game has empty stable kernel and winning region;
the stable control has `K={q1}` and `W={q0,q1}`.

The sample counts support the implementation, not a general theorem-authority
claim; the proof remains controlling.

## Source, target, and causal firewalls

`PASS.` The packet does not infer objective target adequacy, source truth,
causal landing, whole-field reread, or actual noetic restoration from the game.
A stale certificate or omitted successor can create a false kernel; source and
version changes therefore reopen both fragment eligibility and transition
closure.

Nonblocking burdens:

1. `Succ` must be causally and operationally adequate for every claimed
   intervention/fault path;
2. `Target` and `Safe` remain independently interpreted predicates;
3. actor-local fragment derivation may be computationally hard outside the
   Round-13 equality specialization;
4. asynchronous fairness, randomized strategies, evolving common knowledge,
   and unbounded state remain outside the finite memoryless scope.

## Ancestry, novelty, and cross-candidate audit

`PASS.` The fixed points are standard finite safety/reachability mechanisms and
reuse the admitted dynamic-restoration family. The substantive new packet is a
composition with locally implementable, fault-robust, warrant-bearing protocol
fragments. It receives no independent general theorem origin.

Candidate C may constrain target and fragment eligibility, but operational
stability does not establish metaphysical truth, numerical unity, or Divine
attributes. The firewall is intact.

## Result

```text
blocking findings: 0
nonblocking protocol/causal/authority notes: 4
repair required: false
fresh rereview required: true
PMR-007 may close: false
```
