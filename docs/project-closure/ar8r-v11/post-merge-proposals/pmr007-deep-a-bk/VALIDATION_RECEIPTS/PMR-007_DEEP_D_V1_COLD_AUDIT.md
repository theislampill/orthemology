# PMR-007 Deep Round D V1 — cold audit

```text
audit epoch: B
candidate: PMR-007-UGEN-1 V1
disposition: REPAIR_REQUIRED
blocking findings: 2
```

## DD-F01 — nonbridge model controls were hard-coded

The primary checker set `articulability_not_mentality`,
`mentality_not_speech`, and `created_token_not_uncreated_content` to `true`
without loading the frozen model owner.  The prose models are intelligible, but
the advertised executable control was not independent.

**Required repair:** load the YAML model and verify every UG7, UG8, and UG9
antecedent/conclusion separation from its typed fields.

## DD-F02 — source-asymmetry check was tautological

The V1 code tested `apply(g,x) != apply(g,x)`, which cannot fail.  The intended
control is that the identity map on a nontrivial G-set is equivariant while the
selected source point is itself non-invariant.

**Required repair:** check both `F(g.x)=g.F(x)` and non-invariance of at least one
selected source point.  Also execute the external-selector and non-equivariant
constant controls rather than recording them as literals.

## Nonblocking notes

- UGEN-1 is a standard equivariant-map fixed-point theorem with zero general
  novelty.
- The full symmetric-group examples illustrate but do not prove the general
  theorem; the written proof does.
- “Absolute unorthability” is represented only relative to a declared group of
  distinctions.  The choice of group is a metaphysical bridge, not a theorem.
- Symmetric distributions can have non-symmetric samples; the realized seed is
  an asymmetry carrier.
- An impersonal abstract grammar is a model-theoretic rival, not a source claim
  or demonstrated world possibility under every metaphysics.
