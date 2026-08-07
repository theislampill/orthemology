# PMR-007 Deep Round BH V1 — truth-calibrated radical correction and the proper-function boundary

```text
identity: PMR-007-TCRPF-1
round: DEEP_BH
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
```

## 1. Typed setting

Let `G=(V,E)` be a finite connected undirected revision graph. Every oriented
edge has an antisymmetric declared correction increment

\[
d(u,v)=-d(v,u)\in\mathbb Z.
\]

Let

\[
L:V\to\mathbb Z
\]

be an independently supplied truth-loss coordinate: smaller `L` is better.
Choose a spanning tree `T`.

## 2. Candidate theorem — finite truth-calibration certificate

The following are equivalent:

```text
A. For every oriented edge (u,v), d(u,v)=L(u)-L(v).

B. On every oriented tree edge, d(u,v)=L(u)-L(v), and the signed sum of d
   around every fundamental cycle determined by T is zero.

C. There is a potential N, unique up to one additive constant, with
   d(u,v)=N(v)-N(u) on every edge and N(v)=C-L(v) on every vertex.
```

Thus truth-calibrated radical correction can be certified using one spanning
tree plus a fundamental cycle basis.

## 3. Proof

`A -> B` is immediate: truth-loss differences telescope around every cycle.

For `B -> C`, root the tree at `r` and define

\[
N(v)=N(r)+\sum_{e\in r\leadsto v}d(e).
\]

Tree calibration gives `N(v)=C-L(v)`. For each non-tree edge, zero sum on its
fundamental cycle forces its increment to equal the potential difference.
Connectedness gives uniqueness up to `N(r)`.

`C -> A` follows from `N(v)=C-L(v)`.

## 4. Proper-function boundary

The theorem establishes an exact truth-linked correction potential **relative
to the supplied truth-loss coordinate**. It does not establish that the system
has the proper function of truth acquisition.

The same calibrated graph admits account-expansions in which the function is or
is not:

```text
frequent;
causally useful;
organizationally sustaining;
selected because of truth-conducive effects;
designed for truth;
learned under a truth aim;
teleologically authoritative;
Plantingian proper function;
or fitrah-oriented proper function.
```

Those accounts require different function-fixing evidence.

## 5. Countermodels

```text
BH-CM1 PATH-INDEPENDENT BUT ANTI-TRUTH:
  d is exact but calibrated to increasing truth loss.

BH-CM2 TREE-ALIGNED BUT CYCLE-INCONSISTENT:
  all tree edges match L, but one off-tree edge has nonzero holonomy.

BH-CM3 ZERO-HOLONOMY BUT TRUTH-UNRELATED:
  d has a potential N that is not an affine negative of L.

BH-CM4 ACCIDENTAL TRUTH SUCCESS:
  all corrections reduce L, but no selection history, design assignment,
  teleology, or source purpose fixes that as the system's function.

BH-CM5 SELECTED EFFECT WITHOUT TRUTH AIM:
  historical selection fixes a function, but the selected effect is unrelated
  or opposed to truth.

BH-CM6 DESIGN WITHOUT LEGITIMATE TRUTH AUTHORITY:
  a designer assigns a role, but the design plan's truth aim or authority is
  absent.

BH-CM7 SOURCE-RELATIVE FITRAH:
  a fitrah-oriented purpose can be supplied inside an authenticated Track-N
  model while remaining unavailable as a neutral theorem premise.
```

## 6. Central consequence

Truth calibration answers:

```text
Which revision is better relative to L?
```

Proper function additionally asks:

```text
Why is truth loss the authoritative end of this system, and by what
function-fixing relation is the system supposed to track it?
```

An underived order, one bearer, causal efficacy, or successful correction does
not by itself answer that question. The proper-function bridge remains a
separate premise in the transcendental ascent.

## 7. Initial authority ceiling

This is a graph-potential/fundamental-cycle application plus a typed
proper-function nontransfer. It does not establish the truth or completeness of
`L`, teleology, designer intention, Plantingian warrant, fitrah world truth,
Wisdom, a personal ground, or general mathematical novelty.
