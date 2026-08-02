# AR8R-RC-T366-v1 — Declared-profile exact-certification factorization

## Provenance

This is a post-campaign canonical semantic reconstruction associated with historical identity AR8R-T366. The original historical bytes remain unavailable.

## Setting

Let `X` be a declared class of states, `O : X → Y` a declared observational profile, and `F : X → {0,1}` a declared target predicate. A profile-only certifier is a map `d : Y → {0,1}`.

## Statement

There exists a certifier `d` satisfying `F(x)=d(O(x))` for every `x ∈ X` if and only if `F` is constant on every fibre of `O`:

`O(x)=O(x') ⇒ F(x)=F(x')` for all `x,x' ∈ X`.

## Proof

If `F=d∘O`, equal profile values give equal certifier values and hence equal target values. Conversely, assume fibre constancy. On every observed value `y∈O(X)`, define `d(y)` as the unique target value shared by states in that fibre; define `d` arbitrarily outside `O(X)`. Fibre constancy makes the definition well-defined, and then `d(O(x))=F(x)` for every state.

## Countermodel and falsifier

Two states `x,x'` with `O(x)=O(x')` and `F(x)≠F(x')` rule out every exact profile-only certifier.

## Scope and nonclaims

- `X`, `O`, and `F` must be declared independently of the certifier being assessed.
- The theorem does not establish the truth or completeness of `F`.
- It does not establish source fidelity, profile adequacy, causal restoration, or metaphysical interpretation.
- The factorization mechanism is standard and receives zero general mathematical novelty credit.
- Any source or implementation value lies in the audited application, not in this abstract equivalence.
