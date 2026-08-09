# Deep CQ V2 — switching-standard robust viability under norm-source uncertainty

## Identity and status

```text
identity: PMR-007-NURV-1
candidate version: V2
status before rereview: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
general mathematical novelty: 0
owner adoption: PENDING
external review: OPEN
```

## Typed setting

Let `S` be a finite state space, `H` a finite nonempty family of live candidate
proper-function or norm-source standards, and `A` a finite action set. For each
`h in H`:

- `T_h subset S` is the supplied target region;
- `A_h(s) subset A` is the nonempty set of actions eligible under that
  standard’s version, authority, capability, and semantics contract;
- `F_h(s,a) in S` is the deterministic successor.

The controller observes the current state and uses one common state-feedback
policy. After the controller chooses an action, an adversary may select any
`h in H` at each step. This **switching-standard** semantics is deliberately
stronger than one unknown but temporally fixed standard.

Define

```text
A_*(s)   = intersection_h A_h(s)
T_*      = intersection_h T_h
Pre_H(X) = {s : exists a in A_*(s), forall h in H, F_h(s,a) in X}.
```

Define the robust viability and reach-and-stay regions:

```text
V_H = nu X. [T_* intersect Pre_H(X)]
W_H = mu Z. [V_H union Pre_H(Z)].
```

## Theorem CQ-1 — robust viability characterization

`V_H` is exactly the set of states from which one memoryless common policy can
keep the state inside every supplied target region forever against arbitrary
standard switching.

### Proof

The descending greatest-fixed-point iteration terminates because `S` is finite.
For each `s in V_H`, choose an action witnessing `s in Pre_H(V_H)`. The resulting
memoryless policy keeps every successor in `V_H subset T_*`, under every
standard choice.

Conversely, let `X` be the winning region of any policy that robustly maintains
all targets. Every state in `X` lies in `T_*`, and the policy’s first action has
all standard-indexed successors in `X`; hence `X subset T_* intersect Pre_H(X)`.
By greatest-fixed-point coinduction, `X subset V_H`. ∎

## Theorem CQ-2 — robust finite reach-and-stay characterization

`W_H` is exactly the set of states from which one memoryless common policy can
force finite entry into `V_H` and thereafter remain there against arbitrary
standard switching.

### Proof

Let `W_0=V_H` and `W_{k+1}=W_k union Pre_H(W_k)`. The finite iteration stabilizes
at `W_H`. Assign each state its least entry rank. At a positive-rank state,
choose an action whose every standard-indexed successor has lower rank; on
`V_H`, use the invariant policy from CQ-1. Rank decreases strictly until entry
into `V_H`, in at most `|S|` steps.

For the converse, the standard finite reachability-game attractor argument
applies. If a state is outside the least fixed point, every common eligible
action has some standard-indexed successor outside it. The adversary can choose
such a successor forever, preventing entry into `V_H`. Thus no history-dependent
policy can win from outside `W_H`, and memoryless policies suffice. ∎

## Corollary CQ-3 — uncertainty-family monotonicity

If `H' subset H` and all targets, action contracts, and dynamics are inherited
without reinterpretation, then

```text
V_H subset V_H'
W_H subset W_H'.
```

Removing standards weakens the target intersection, expands common action
eligibility, and weakens the universal successor condition. This is a formal
monotonicity result, not authority to delete a rival standard without evidence.

## Exact countermodels

1. **Individual restoration without robust restoration.** Two standards agree
   on one target but license disjoint actions. Each has an individual stable
   policy; their common-action set is empty.
2. **Fixed-hidden versus switching uncertainty.** With states
   `start, mid, target` and one action, `h0` sends
   `start -> mid -> target`, while `h1` sends `start -> target` but
   `mid -> start`. Each fixed standard reaches the target from `start`; a
   switching adversary alternates `h0` at `start` and `h1` at `mid`, avoiding
   the target forever.
3. **Inconsistent targets.** If `intersection_h T_h` is empty, no state is
   robustly viable even when each standard is individually viable.
4. **Unsupported source anchor.** A source-relative premise may shrink `H` and
   enlarge the formal kernel, but that move is licensed only after source,
   translation, referent, applicability, and world guards are independently
   warranted.
5. **Implementation deletion.** A paper policy certificate does not show that
   the daee runtime exposes the same state, action, target, or switching model.

## Proper-function and source effect

The theorem treats causal-role, selected-effect, design, learned-objective,
teleological, Plantingian, and fiṭrah-oriented standards as distinct possible
owners of `T_h` and `A_h`. It does not collapse them or decide which fixes the
objective target.

A nonempty `W_H` means only that one route is safe across the declared standard
family. It does not establish truth-linked proper function, teleology, Wisdom,
actual uptake, causal human restoration, or sound fiṭrah. Conversely, an empty
`W_H` can locate a genuine policy conflict without showing that every standard
is equally warranted.

## daee correspondence

The current repository distinguishes candidate noetic profiles, target maps,
route selection, burden transition, runtime closure, and actual human uptake.
Deep CQ supplies a finite robust-policy owner for a possible target-uncertainty
layer. It does not establish that current daee code enforces this game or that
runtime closure is human restoration.

## Theorem-family and novelty disposition

The mathematical core is standard finite robust safety and reachability-game
fixed-point machinery. Its contribution is an orthemological integration of the
proper-function target-fixing burden with stable restoration under unresolved
norm-source uncertainty.

```text
relation to T351/T352:
  adds an unresolved-target-family/common-policy layer;
relation to Round 14:
  robust safety/reachability specialization, not co-Buchi novelty;
relation to T354:
  route selection under a typed order remains distinct from scalarization;
new general mathematics:
  NONE.
```

## Nonclaims

No claim is made about partial observation, one fixed hidden standard,
stochastic or infinite dynamics, empirical human restoration, source truth,
world applicability, objective target correctness, daee runtime enforcement,
or meniscus closure.
