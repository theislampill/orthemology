# PMR-007 Frontier Round 18 V4 — certificate-object refinement, robust relation selection, and temporal custody

```text
round: PMR-007-FRONTIER-ROUND18
version: V4
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
current disposition: FROZEN_PENDING_DISTINCT_FRESH_REREVIEW
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Central burden

A recipient may see one observation while several concrete source/version/model
states remain possible.  Even when every concrete state has a valid temporal
repair, the recipient needs enough *truthful and authorized information* to
select one complete certificate object that is valid in the actual state.
Round 18 asks for the exact finite information boundary for that fixed
certificate-selection task.

This is a relation-selection problem.  It is not automatically exact state,
version, action, or label recovery.

## 2. Typed finite setting

Let:

```text
Q: finite concrete state set
O: finite decoder-observation set
obs : Q -> O
K: finite complete certificate-object set
A: finite surface-action set
act : K -> A
H(q) subseteq K: complete objects admitted at q
```

A complete object may include, as applicable:

```text
surface action;
source and proposition identifiers;
version/model digest;
authority and redelegation status;
provenance root;
invalidator closure;
target contract;
temporal certificate and rank witness.
```

No theorem below proves those fields true.  `H(q)` is the independently supplied
admissibility relation for the declared model.

For observation cell `C = obs^-1(o)` and object `k`, define

```text
S_C(k) = {q in C : k in H(q)}.
```

Define the complete-object refinement number

```text
rho_H(C) = min |K0|
           over K0 subseteq K such that
           C subseteq union_{k in K0} S_C(k),
```

with value infinity if no cover exists.

## 3. ORTC-EXACT — exact-state encoder characterization

Assume the encoder knows the exact state.  A deterministic `m`-message
protocol consists of

```text
e : C -> M, |M|=m
d : {o} x M -> K
```

such that `d(o,e(q)) in H(q)` for every `q in C`.

### Theorem ORTC-EXACT

The minimum message-alphabet size on cell `C` is exactly `rho_H(C)`.

### Proof

Every feasible protocol uses at most one decoded object per message.  Those
objects' supports cover `C`, so `rho_H(C) <= |M|`.  Conversely, for a minimum
cover `K0`, assign each state to one covering object and transmit that object's
index.  The decoder returns it.  Therefore `|M|=rho_H(C)` is achievable. ∎

Because the decoder sees `o`, message names may be reused across distinct
observation cells.  Hence the global exact-state minimum alphabet is

```text
R_H = max_o rho_H(obs^-1(o)).
```

## 4. ORTC-INFO — general encoder-information characterization

Let `enc : Q -> E` be the encoder's information partition.  The encoder message
must be constant on every `enc`-cell.  For a message map `c : E -> M`, define

the decoder ambiguity bucket

```text
B(o,m) = {q in Q : obs(q)=o and c(enc(q))=m}.
```

Call `c` compatible when every nonempty bucket has

```text
intersection_{q in B(o,m)} H(q) nonempty.
```

### Theorem ORTC-INFO

The minimum deterministic message-alphabet size under encoder information
`enc` is the minimum number of message values in a compatible map `c`.

### Proof

If a protocol exists, its decoder output for `(o,m)` belongs to every `H(q)` in
that bucket, so the intersection is nonempty.  Conversely, choose one object
from each nonempty intersection and use it as the decoder output. ∎

`ORTC-EXACT` is the specialization where every encoder cell is a singleton.
The exact-state cover number must not be used when the encoder itself cannot
separate the concrete states.

## 5. ORTC-FIXED-BITS — exact fixed-length and worst-case prefix-free bounds

Under the finite exact-state model, truthful authorized encoder, decoder access
to `obs(q)`, and complete admissibility data:

```text
minimum fixed-length bits = ceil(log2 R_H).
```

The same expression is the minimum *worst-case* binary prefix-free length for
the chosen finite message alphabet.  Expected prefix-free length is
distribution-dependent.  Framed variable-length, interactive, cryptographic,
randomized bounded-error, and amortized block models are different problems.

## 6. ORTC-PROJECTION — action projection can launder certificate differences

Let

```text
G(q) = {act(k) : k in H(q)}.
```

Then the surface-action cover number satisfies

```text
rho_G(C) <= rho_H(C).
```

The inequality can be strict.  If `H(q0)={k0}`, `H(q1)={k1}`, `k0 != k1`, but
`act(k0)=act(k1)=a`, the action cover is one while the complete-object cover is
two.  Surface agreement therefore does not establish shared source, version,
authority, provenance, or warrant.

## 7. ORTC-ROBUST-COMPLETION — incomplete or stale certificate data

Suppose a finite family `Theta(q)` of source/model completions is still possible
at state `q`, and completion `theta` admits `H_theta(q)`.  An object is robust
against all declared completions exactly when it lies in

```text
H_all(q) = intersection_{theta in Theta(q)} H_theta(q).
```

All previous theorems apply to `H_all`.  Replacing unknown completion data by a
union would be optimistic and unsound.

If admissible sets only shrink under a later version or stronger invalidator
set, then every complete-object cover number weakly increases.  It may become
infinite.

## 8. ORTC-ZERO-RANDOM — pointwise zero-error randomization does not reduce the alphabet

For finite `Q`, suppose a randomized protocol is pointwise zero-error: for each
state, the probability of outputting an inadmissible object is zero.  The
intersection of the corresponding probability-one seed sets over finite `Q`
has probability one.  Fixing any seed in that intersection yields a
deterministic protocol with the same message alphabet.  Hence randomization
cannot lower the pointwise zero-error alphabet requirement.

This does not cover bounded error, distributional average error, adversarially
correlated randomness, interactive protocols, or privacy constraints.

## 9. ORTC-ERROR-RELATION — exact adversarial-channel criterion

Let `c : Q -> Sigma^n` be a fixed encoder, let the channel permit at most `r`
Hamming substitutions, and let the decoder also see `o`.  For received word
`y`, define

```text
B(o,y) = {q : obs(q)=o and distance(c(q),y) <= r}.
```

### Theorem ORTC-ERROR-RELATION

A deterministic robust relation selector exists for the fixed code `c` exactly
when every nonempty `B(o,y)` satisfies

```text
intersection_{q in B(o,y)} H(q) nonempty.
```

### Proof

Necessity: one decoder output at `(o,y)` must be admitted for every state that
could have produced `y`.  Sufficiency: choose any object in each nonempty
intersection. ∎

### Exact-label recovery is stronger

If the task additionally requires recovery of one preassigned selector label,
then codewords for distinct labels need distance greater than `2r`.  That
minimum-distance condition is sufficient but not necessary for the
certificate-selection relation.

### Strict separation `R18-RELATION-BEATS-LABEL`

Let `Q={q0,q1,q2,q3}`, `K={k0,k1,k2,k3}`, and

```text
H(q_i) = K minus {k_i}.
```

Encode the states by `00,01,10,11` and permit one adversarial bit flip.  Every
radius-one ambiguity ball contains three states; the intersection of their
admissible sets is the singleton object omitted only by the excluded fourth
state.  Robust relation selection therefore succeeds with two transmitted
bits.

By contrast, exact recovery of any nonconstant binary label under one bit flip
requires code distance three and therefore at least three transmitted bits.
Exact recovery of four state labels requires at least five bits.  Relation
selection can be strictly cheaper than label recovery.

## 10. ORTC-COMPLEXITY — explicit cover instances

For an explicitly listed finite cell and admissibility matrix, deciding whether

```text
rho_H(C) <= k
```

is NP-complete.  Membership in NP is immediate.  Set Cover reduces by taking
its universe as `C` and its listed subsets as the supports `S_C(k)`.

This is standard Set Cover complexity and receives zero novelty credit.

## 11. Temporal certificate instantiation

Let `W subseteq Safe subseteq Q`, `Target subseteq W`, and let `rnk : W -> N`.
A complete object `k` with action `a=act(k)` is rank-admissible at `q` when:

```text
T1. Succ(q,a) is nonempty and contained in W;
T2. if q in Target, every successor has rank <= rnk(q);
T3. if q notin Target, every successor has rank < rnk(q);
T4. the object's model/version digest and all non-temporal guards are valid.
```

Any policy choosing a rank-admissible object at every visited state remains in
`W` and visits non-target states only finitely often.  Infinite non-target
visits would force infinitely many strict decreases in `N`.

This is a sufficient certificate architecture, not a complete characterization
of all partial-observation co-Büchi strategies.

### History and fresh-hidden-branch boundary

A selector that is sufficient now need not remain sufficient after an
unobserved branch.  There are systems in which the current cell has
`rho_H=1`, but one later merged cell has `rho_H=2`.  A one-time bit count does
not establish a history-independent policy, future model validity, dynamic
membership safety, or stale-certificate immunity.

History-dependent policies may lower communication only when the observable
history itself refines the relevant ambiguity sets.  Hidden history does not.

## 12. Countermodel register

```text
R18-CM-OBJECT-PROJECTION:
  same surface action, different complete objects; rho_action < rho_object.

R18-CM-PAIRWISE:
  pairwise intersections nonempty, total intersection empty; zero-message
  compatibility fails although two objects cover the cell.

R18-CM-EMPTY:
  one state has no admissible object; no information amount repairs the fixed
  certificate.

R18-CM-VERSION:
  same bytes, different version validity; one truthful selector bit required.

R18-RELATION-BEATS-LABEL:
  robust relation selection succeeds below exact-label error-correction cost.

R18-CM-HISTORY:
  current common object followed by a hidden branch requiring different future
  objects; current rho does not certify future policy sufficiency.

R18-CM-STALE-COMPLETION:
  union of possible completion-specific admissibility sets yields a false
  positive; only their intersection is robust.
```

## 13. Ancestry and prior-art ceiling

```text
AR2/AR3 reason-preserving transport:
  supplies source, target, version, authority, capability, invalidator,
  provenance, and execution guards.  Round 18 is a finite selector
  specialization, not a replacement.

FRLA-1:
  its component-wise nonempty intersection is the zero-message special case.

Rounds 14–16:
  supply co-Büchi, model-bound certificate, and version-action eligibility
  architecture.

Witsenhausen zero-error side information:
  established ancestry for exact zero-error communication with decoder side
  information and graph-coloring formulations.

Orlitsky–Roche coding for computing:
  established ancestry for function/relation computation with side
  information and characteristic-graph methods.

Karp Set Cover:
  establishes the explicit cover-decision complexity ceiling.
```

Round 18's abstract combinatorics receive zero general mathematical novelty.
The scoped contribution is the typed integration of complete certificate
objects, encoder information, robust relation selection, version custody, and
model-bound temporal implementation.

## 14. Admitted scope and nonclaims

The packet establishes exact finite characterizations only for the declared
models.  It does **not** establish:

```text
source truth or Arabic/source authenticity;
message authorization or cryptographic authenticity;
independent provenance roots;
common knowledge;
general distributed synthesis;
partial-observation co-Büchi completeness;
minimum expected or interactive communication;
bounded-error randomized complexity;
privacy-preserving coding;
dynamic-membership robustness;
causal restoration in daee;
world-directed metaphysics;
new Set Cover, coding, or information theory;
or any historical AR8R identity.
```

## 15. Frontier effect

```text
Candidate A:
  gains an exact finite relation-selection and encoder-information boundary
  for provenance/version-bearing communication.

Candidate B:
  gains a model-bound partial-observation implementation criterion and a sharp
  separation between present selector sufficiency and future temporal custody.

Candidate C:
  gains no metaphysical bridge; source/version messages remain operational
  inputs whose truth and authority must be independently supplied.
```

```text
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```
