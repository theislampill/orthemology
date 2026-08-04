# Formal reconstruction — Candidate E

## 1. Types and primitives

Let:

- `S` be a nonempty set of system or agent states;
- `R` be a set of respects of assessment;
- `B : S → P(Σ)` assign each state its token standard basis;
- `Corr_r(t,s)` mean that `t` is an objective correction of `s` in respect `r`;
- `Auth_r(X,q)` mean that facts or standards in `X` are jointly sufficient to confer undefeated normative authority on proposition `q` in respect `r`;
- `Def_r(X,t,s)` mean that the correctness of `t` over `s` includes the insufficiency or defeat of every standard whose authority is wholly constituted by `X` for settling the relevant issue in `r`;
- `Con_s(X)` mean that `X` is wholly constituted by the current token state `s`;
- `Meta_s(m)` mean that `m ∈ B(s)` is a retained higher-order revision rule;
- `Global(H)` mean that the normative relation is constituted only by a holistic structure `H` over multiple states rather than by any one token;
- `Prim(q)` mean that `q` or its authority is primitive.

`Corr` is intentionally not analyzed as mere transition, goal attainment, social approval, selected effect, or reward maximization.

## 2. Token-closure thesis

For respect `r`, state `s`, and proposed correction `t`, define:

```text
TokenClosure(B_s,r,t,s) :=
  ∃X [Con_s(X) ∧ X ⊆ Closure(B_s,s) ∧ Auth_r(X, Corr_r(t,s))].
```

The strong thesis says that all sufficient normative authority for the correction is wholly constituted by the current token state.

## 3. Radical correction

```text
Rad_{B_s,r}(t,s) :=
  Corr_r(t,s)
  ∧ Def_r(Closure(B_s,s),t,s)
  ∧ ¬∃m [Meta_s(m) ∧ Auth_r({m}, Corr_r(t,s))].
```

This excludes ordinary self-amendment. A transition that follows a retained amendment rule may replace every first-order rule while remaining authorized by a higher-order standard in the original basis.

## 4. Authority-adequacy constraint

```text
AA:
∀X,r,t,s [Def_r(X,t,s) → ¬Auth_r(X,Corr_r(t,s))].
```

`AA` is not a universal grounding axiom. It explicates the intended content of saying that `X` is insufficient as an authority for the very assessment in question. Rejecting `AA` is permitted, but then “defeated/insufficient authority” no longer excludes complete sufficient authority and the vocabulary ceases to mark a contrast.

## 5. No-token-autonomous-radical-correction theorem

For all `s,t,r`:

```text
AA ∧ Rad_{B_s,r}(t,s)
→ ¬TokenClosure(B_s,r,t,s).
```

### Derivation

1. Assume `Rad_{B_s,r}(t,s)`.
2. Then `Def_r(Closure(B_s,s),t,s)`.
3. By `AA`, `¬Auth_r(Closure(B_s,s), Corr_r(t,s))`.
4. Every `X` wholly constituted by `s` and admitted by strong token closure is a subset of `Closure(B_s,s)` and obtains its putative authority only through that closure.
5. Therefore no such `X` is sufficient for the radical correction.
6. Hence token closure fails.

Step 4 is a monotonicity/closure convention and must be stated. A theory that assigns emergent authority to a subset while denying it to the full closure is not a token-basis theory in this sense unless it supplies a selection rule; that selection rule becomes the relevant standard and must itself enter the audit.

## 6. Source partition

Given `Corr_r(t,s)`, exhaust the logical roles for its authority source:

```text
M: ∃m Meta_s(m) and m authorizes the revision;
T: ∃X ¬Con_s(X) and X supplies authority;
H: ∃H Global(H) and H fixes Corr;
P: Prim(Corr or its authority);
E: Corr is denied or reduced to a relative/descriptive relation.
```

Subject to classical exhaustiveness over `constituted by current token / not constituted by current token`, and then over `structured/global / primitive / denied`, at least one of `M,T,H,P,E` obtains. The partition can overlap: a type-level standard may itself be primitive; a holistic fixed point may contain retained meta-rules.

## 7. Recursive sequence

Let `B_i` be the authority basis operative at stage `i` and let `C_i := Corr(B_{i+1},B_i)` denote correction of `B_i` by `B_{i+1}`.

Define strict deferred authority:

```text
Deferred(i) :=
  authority(C_i) is wholly derived from B_{i+1}
  ∧ authority(B_{i+1}) is unsettled until C_{i+1}.
```

An infinite sequence of `Deferred(i)` does not by itself produce contradiction. It fails as a completed explanation only if the authority of the initial correction is supposed to be available only after the completion of the entire dependency chain and no holistic constitution is admitted. This is an explanatory-direction condition, not a bare anti-infinity premise.

## 8. Countermodel classes

The theorem is intentionally compatible with:

- truth as a constitutive norm of belief;
- agency-wide constitutive aims;
- biological proper function;
- practice-level norms;
- social-historical norms;
- coherentist reflective equilibrium;
- irreducible normative facts;
- error theory.

These models occupy different horns. The theorem excludes only the conjunction of radical objective correction with complete token-autonomous authority.

## 9. Quantifier discipline

The result is existentially conditional:

```text
If there exists a genuinely objective radical correction relative to a token basis,
then its sufficient authority is not wholly constituted by that token basis.
```

It does not assert that every change is correction, that global objective normativity exists, or that every standard is corrigible.
