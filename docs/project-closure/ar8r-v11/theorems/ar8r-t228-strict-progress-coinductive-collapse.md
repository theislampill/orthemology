# AR8R-T228 — strict progress is sufficient, but not necessary, for finite unary coinductive collapse

Status: validated after identity repair; canonical identity fixed by theorem-origin authority V5; no general mathematical novelty.

## Typed setting

For finite `V`, facts `F⊆V`, and edges `E⊆V×V`, define

```text
T(S) = F ∪ {v in V : some u in S has (u,v) in E}.
```

Let `mu T` and `nu T` be the least and greatest fixed points. A strict progress certificate is `r:V→N` satisfying `r(u)<r(v)` on every edge.

## Theorem

1. A strict progress certificate exists exactly when `E` is acyclic.
2. A strict progress certificate implies `mu T = nu T = Reach_E(F)`.
3. If `mu T != nu T`, no strict progress certificate exists.
4. The converse is false: `mu T = nu T` may hold despite a directed cycle.

Thus strict progress is sufficient, but not necessary, for least/greatest fixed-point agreement.

## Proof

Strict increase around a directed cycle is impossible, while a topological ordering of a finite DAG supplies a strict rank. AR8R-T218 gives

```text
mu T = Reach_E(F)
nu T = Reach_E(F union Cyc(E)).
```

A strict rank makes `Cyc(E)` empty, proving equality. The third clause is the contrapositive. For nonnecessity, take `V={a,b}`, `F={a}`, and edges `a→b`, `b→a`: both fixed points are `{a,b}`, but no strict rank exists.

## Boundaries

The rank must cover every edge in the operator. The result is finite and unary-body. It does not establish rank legitimacy, objective fittingness, source truth, the impossibility of non-well-founded metaphysics, one foundation, one bearer, or a Necessary Being.

The mathematical mechanism is a direct corollary of standard finite DAG ranking with T218/T224. The pre-renumbering exact payload was labeled T227; it is historical custody only. The canonical identity is T228, with zero duplicate theorem or novelty credit.
