# SPA-R4 — observation-uniform co-Büchi control

**Status:** specialist-local specialization of the existing finite dynamic /
co-Büchi family; no new fixed-point mechanism or novelty.

## Frozen model

A finite deterministic transition system has two common actions, a frozen
observation map, stationary strategies, a finite initial belief set, and a
co-Büchi objective: the eventual cycle must lie entirely in the declared good
set.

## Criterion

An observation-based stationary strategy `τ : O → A` is exactly a
perfect-information state strategy `σ : S → A` that is constant on every
observation fibre. Therefore:

```text
observation-based winning from belief B
iff
there exists one observation-uniform state strategy winning from every s ∈ B.
```

The fact that every state in `B` is individually perfect-information winning is
necessary but not sufficient; the individual witnesses may require conflicting
actions inside one observation class.

## Countermodel

States `s0` and `s1` share an observation. At `s0`, action 0 reaches a good sink
and action 1 reaches a bad sink; at `s1`, the actions are reversed. Each state is
perfect-information winning, but no observation-based stationary strategy wins
from belief `{s0,s1}`.

## Executable evidence

The checker exhausts all declared deterministic games with two or three states,
all good sets, all observation partitions, and all nonempty initial beliefs:
204,504 cases. Direct observation-strategy enumeration and observation-uniform
state-strategy enumeration agree in every case. It finds 8,234 distinct
statewise-false-sufficiency countermodels.

Six mutants are killed, including statewise sufficiency, ignored uniformity,
observation labels treated as no-ops, prefilled counters, repeated-witness
substitution, and extrapolation to adversarial or infinite games.

## Lean status

`lean/ObservationUniformity.lean` drafts the strategy-factorization interface.
It is source-only and unverified in this runtime. Its factorization component is
classified in the existing fibre family, not as a new theorem origin.

## Conclusion ceiling

No randomized, adversarial-nondeterministic, history-dependent,
infinite-state, asynchronous-protocol, or metaphysical conclusion follows.
