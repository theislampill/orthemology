# PMR-007 Frontier Round 18 V1 — observation refinement, version bits, and robust temporal certificates

```text
round: FRONTIER_ROUND_18_OBSERVATION_REFINEMENT_VERSION_BITS_TEMPORAL_CERTIFICATES
version: V1
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repository mutation: NONE
current disposition: FROZEN_PENDING_COLD_AUDIT
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

# 1. Central Candidate-A / Candidate-B question

Rounds 13, 14, 15, and 16 established, at their declared finite scopes, that:

```text
one-step local agreement requires a common warranted output inside each joined
correct-view component;

general co-Büchi restoration differs from forced entry into one common invariant
core;

current daee closure bytes do not determine future temporal stability without a
model-bound temporal certificate;

and the same artifact bytes can be applicable in one version/recipient context
and stale or inapplicable in another.
```

The present load-bearing question is:

```text
How much truthful, authorized state/version information is exactly required to
implement one already-fixed robust temporal certificate when several concrete
states are observationally merged?
```

This is not another profile nonimplication. It yields an exact information
invariant and a constructive implementation theorem for a fixed certificate.

# 2. Certificate-local action sets

Let `Q` be a finite set of concrete states, `A` a finite action set, and

```text
obs : Q -> O
```

an observation map. For each `q`, let `G(q) subseteq A` be the actions admitted
by one common, independently specified certificate. The certificate-local
assumption is substantive:

```text
CERT-COMP:
any state-dependent policy that chooses an action in G(q) at every visited q
satisfies the same declared safety/liveness certificate.
```

The theorem below is exact only relative to `G` and `CERT-COMP`. It does not say
that `G(q)` contains every winning action, that the certificate is complete, or
that a message carrying a selector also carries source truth or warrant.

For an observation cell `C=obs^-1(o)` and action `a`, define its support

```text
S_C(a) = {q in C : a in G(q)}.
```

Define the **certificate refinement number**

```text
rho(C) = min |A0|
         over A0 subseteq A such that C subseteq union_{a in A0} S_C(a),
```

with `rho(C)=infinity` if any state in `C` has `G(q)=empty` or no such cover
exists.

# 3. ORTC-1 — exact observation-refinement characterization

A `k`-label refinement of one observation cell is a pair

```text
e : C -> {1,...,k}
d : {1,...,k} -> A
```

such that `d(e(q)) in G(q)` for every `q in C`.

## Theorem ORTC-1

The minimum number of refinement labels required for `C` is exactly `rho(C)`.

### Proof

If a `k`-label refinement exists, collect the at most `k` actions decoded by
its labels. Every `q` is assigned a label whose decoded action belongs to
`G(q)`, so those actions' supports cover `C`. Hence `rho(C) <= k`.

Conversely, let `A0={a_1,...,a_r}` be a minimum support cover. For every `q`,
choose one `a_i in G(q)` and send label `i`; decode `i` as `a_i`. This is an
`r=rho(C)`-label refinement. ∎

## Corollary ORTC-2 — fixed-length side-information bits

Assume:

```text
1. the encoder knows the exact concrete state;
2. the encoder is truthful and authorized to disclose the selector;
3. the decoder already knows the original observation o;
4. a fixed-length deterministic b-bit message is used;
5. the message only selects among actions already admitted by the fixed
   certificate.
```

Then a global side channel of `b` bits suffices for all observation cells iff

```text
2^b >= max_o rho(obs^-1(o)).
```

Therefore the minimum is

```text
b_min = ceil(log2(max_o rho(obs^-1(o))))
```

when all values are finite. Labels may be reused between cells because the
decoder also sees `o`; without that guard the global problem is different.

## Corollary ORTC-3 — version/action deletion monotonicity

If a later version, recipient contract, source status, or invalidator set only
removes certificate-admissible actions,

```text
G'(q) subseteq G(q) for every q,
```

then

```text
rho_G'(C) >= rho_G(C)
```

for every cell. Thus stale-version drift cannot reduce the required selector
information and may make implementation impossible.

If the observation partition is truthfully refined, the maximum refinement
number cannot increase, because every new cell is a subset of an old cell.

# 4. RTC-1 — a nondecorative temporal source for G(q)

Let `W subseteq Safe subseteq Q`, let `Target subseteq W`, and let

```text
r : W -> natural numbers
```

be a common rank certificate. An action `a` is rank-admissible at `q in W` when:

```text
R1. Succ(q,a) is nonempty and contained in W;
R2. if q is in Target, every successor q' has r(q') <= r(q);
R3. if q is outside Target, every successor q' has r(q') < r(q).
```

Let `G_r(q)` be all rank-admissible actions.

## Lemma RTC-1

Every policy—memoryless or history-dependent—that always chooses from `G_r(q)`
keeps all paths in `W` and satisfies the co-Büchi objective

```text
eventually always Target.
```

### Proof

Ranks never increase. Every transition out of a non-target state strictly
decreases the natural-number rank. Infinitely many non-target visits would
therefore produce infinitely many strict decreases, impossible in the natural
numbers. ∎

Thus `G_r` satisfies `CERT-COMP`. The refinement theorem can be applied to a
real temporal certificate rather than to arbitrary “locally good” labels.

This rank architecture is sufficient, not claimed complete for every co-Büchi
winning policy. Round 14's exact nested fixed point remains the complete
perfect-information characterization at its admitted scope.

# 5. Exact countermodels and constructions

## 5.1 Same bytes, different version applicability

Two hidden states expose the same visible artifact bytes:

```text
q_v1: current version; only EXECUTE is rank-admissible;
q_v2: superseded version; only HOLD_REVALIDATE is rank-admissible.
```

Both states are individually winning under perfect information. Their merged
cell has

```text
G(q_v1)={EXECUTE}
G(q_v2)={HOLD_REVALIDATE}
rho=2
b_min=1.
```

Zero-bit observation-only implementation is impossible. One truthful version
bit is sufficient. The bit does not establish that either version is authentic,
that the source is true, or that execution is authorized; those are prior
contract guards.

## 5.2 Pairwise-overlap trap

For three merged states:

```text
G(q0)={a,b}
G(q1)={b,c}
G(q2)={a,c}.
```

Every pair intersects, but the total intersection is empty. There is no
unrefined action. The supports of any two actions cover the cell, so `rho=2`
and one bit suffices. Pairwise compatibility is not a substitute for one
cell-wide policy.

## 5.3 Impossible state

If `G(q)=empty` for one possible state, no amount of selector information can
implement this fixed certificate. The required repair is to change the model,
certificate, action set, source/recipient contract, or target—not to send more
bits.

## 5.4 Temporal hidden-state witness

Let hidden states `x` and `y` share one observation, and let `g` be a target
state. Use ranks `r(x)=r(y)=1`, `r(g)=0` and actions:

```text
EXECUTE: x -> g, y -> y
HOLD_REVALIDATE: x -> x, y -> g
STAY: g -> g.
```

Then:

```text
G_r(x)={EXECUTE}
G_r(y)={HOLD_REVALIDATE}
G_r(g)={STAY}.
```

Each hidden state is perfect-information co-Büchi winning, but their merged
observation is not certificate-implementable without one selector bit.

# 6. Ancestry, theorem family, and novelty

```text
AR2/AR3 RP-T2 and RP-T40:
SUPPLIES the independent target-contract, authenticity/currentness,
authorization, invalidator, and execution guards.

PMR-AGCOM-01 / PMR-AGCOM-02:
SUPPLIES receipt/adoption and surface-profile/bearer-root separations.

PMR-AGCOM-06:
LIMITS the epistemic status of a private selector message; delivery is not
common knowledge.

PMR-LANG-01 / PMR-LANG-02:
SUPPLIES version/context and occurrence-relative applicability distinctions.

FRLA-1:
SHARED MECHANISM — nonempty intersection characterizes the zero-label case;
ORTC-1 gives the exact minimum refinement when the intersection is empty.

Round 14 / Round 15 / Round 16:
SUPPLIES the temporal objective, certificate-custody, and version-action
eligibility architecture.

Candidate 1:
NATURAL QUERY/INFORMATION INTERFACE ONLY. Candidate 1 is an adaptive edge-query
minimax theorem. ORTC-2 is a one-shot exact-state selector bound and neither
reproves nor strengthens Candidate 1.
```

The combinatorial equality with minimum set cover is standard. General
mathematical novelty is zero. The post-merge contribution is the exact
integration of certificate compositionality, partial observation, version
custody, and minimum authorized selector information.

# 7. Authority ceiling and nonclaims

The results establish only:

```text
minimum labels/bits for implementing one fixed robust certificate under the
declared deterministic finite observation model;

an exact impossibility when the support cover is too large or absent;

and monotonic worsening under deletion of admissible actions.
```

They do not establish:

```text
source truth;
message authenticity;
recipient authority;
common knowledge;
full distributed synthesis;
partial-observation co-Büchi completeness;
minimum adaptive query complexity;
minimum communication under variable-length, randomized, interactive, or
cryptographic protocols;
causal restoration in daee;
world-directed metaphysics;
or a historical AR8R theorem identity.
```

# 8. Frontier effect

Candidate A gains an exact one-shot information invariant for transporting a
warranted local protocol across hidden state/version distinctions.

Candidate B gains a precise partial-observation obstruction: perfect-information
restoration in every concrete state does not imply implementable restoration
under a merged view, and `rho` measures the exact refinement burden relative to
one certificate.

Candidate C receives no metaphysical bridge; the result only disciplines what a
source/version selector can operationally establish.

```text
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```
