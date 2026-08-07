# PMR-007 Deep Round AW V2 — Provenance-root robust exact diagnosis

## Candidate disposition

```text
identity: PMR-007-PRAD-1
provenance: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
general mathematical novelty: 0
external review: OPEN
owner adoption: PENDING
```

## 1. Frozen root-level code model

Let `H` be a finite hypothesis set.  Let `G` be a finite set of independently
authenticated provenance/acquisition roots at one fixed version and membership
epoch.  For each root `g`, a complete deterministic certificate symbol

\[
c_g(h)\in\Sigma_g
\]

is declared for every `h in H`.  All messages, paraphrases, repeated tests, and
artifacts derived from one actual root are bundled into this single root-level
symbol and are one corruption unit.

For selected roots `R subset G`, define

\[
c_R(h)=(c_g(h))_{g\in R},
\qquad
d_R=\min_{h\neq h'} d_H(c_R(h),c_R(h')).
\]

The adversary knows the code and true hypothesis and may corrupt all information
from at most `f` selected roots.  In the substitution model, corrupt roots may
return arbitrary unmarked symbols.  In the erasure model, failed root positions
are marked `⊥`.

## 2. PRAD-1A — exact adversarial-substitution characterization

A deterministic decoder that identifies every `h` after every substitution of
at most `f` root coordinates exists iff

\[
d_R\ge 2f+1.
\]

### Proof

If `d_R>=2f+1`, Hamming balls of radius `f` around distinct codewords are
disjoint, so decoding to the unique ball center succeeds.

If two codewords have distance `d<=2f`, partition their differing coordinates
into two sets of size at most `f`.  Form a received word by taking the second
codeword on the first set, the first codeword on the second, and their common
symbols elsewhere.  It lies within distance `f` of both, so no exact decoder
exists. ∎

## 3. PRAD-1B — exact identified-erasure characterization

A deterministic decoder that identifies every `h` after erasure of at most `f`
root coordinates exists iff

\[
d_R\ge f+1.
\]

### Proof

When every pair differs in more than `f` roots, at least one differing root
remains visible after any `f` erasures.  Conversely, if a pair differs in at
most `f` roots, erasing exactly those positions makes their visible words
identical. ∎

## 4. PRAD-1C — root-subset multicover form

For each hypothesis pair define its separating-root set

\[
D(h,h')=\{g\in G:c_g(h)\neq c_g(h')\}.
\]

Then selected roots `R` support:

```text
f substitution errors
iff |R intersect D(h,h')| >= 2f+1 for every pair;

f identified erasures
iff |R intersect D(h,h')| >= f+1 for every pair.
```

Thus minimum robust root selection is a pair-separation multicover.  At `f=0`
it reduces to the finite Test Cover/pair-separation problem.  This is an
application of standard coding and covering theory, not new general
mathematics.

## 5. Provenance and false-multiplicity controls

### AW-CM1 — copied-root false multiplicity

Forty copies of one root remain one coordinate.  Copy count can rise from one
to forty while `d_R` and the corruption budget remain unchanged.

### AW-CM2 — common bottleneck

Many apparent tests can all depend on one root.  Corrupting that root defeats
them jointly.

### AW-CM3 — displayed-label alias

Two displayed root labels may be one actual root.  Contracting them from two
coordinates to one can reduce minimum distance and invalidate a robustness
claim.

### AW-CM4 — independent-root positive construction

Three authenticated roots whose symbols differ between every pair of two
hypotheses give distance three and correct one substitution error.  Distance
two corrects one marked erasure but not one unmarked error.

### AW-CM5 — certificate projection laundering

Two hypotheses can share the same surface action while their complete
certificate symbols differ in source, version, authority, or provenance.
Projecting to the action can lower distance and destroy diagnosis.

### AW-CM6 — dynamic/mobile adversary

A root set satisfying the static theorem may fail when membership changes,
versions drift, or an adversary corrupts different roots over time.  These
models are outside the theorem.

## 6. Cross-lane effects

### Candidate A

The theorem gives an exact positive characterization for provenance-bearing
fault-robust diagnosis and distinguishes independent roots from copied
availability.  It does not settle adaptive, asynchronous, or common-knowledge
protocols.

### Candidate B

A restorative system needing robust diagnosis of a noetic state must bind its
certificate to authenticated root coordinates.  Surface action agreement or
many copied reports can have insufficient root distance.  Diagnosis still does
not prove causal landing or stable restoration.

### Candidate C / Track N

Multiple source presentations strengthen a conclusion only when they occupy
separately authenticated root coordinates and yield a target-relevant
separation.  The theorem supplies no source truth, tawatur warrant, or
metaphysical conclusion.

### Deep AQ/AR/AS/AT/AU

```text
Deep AQ:
  GATE E requires an actually discriminating experiment;

Deep AR:
  copies do not multiply likelihood as independent roots;

Deep AS:
  intervention selection becomes root-aware robust Test Cover;

Deep AT:
  trace-equivalent hypotheses have d_R=0 for every registered root transcript;

Deep AU:
  root-span rank and Hamming separation are distinct invariants;
  rank measures linear direction, distance measures pairwise robust diagnosis.
```

## 7. Authority and nonclaims

```text
mathematical ancestry:
Hamming error correction plus Test Cover/pair multicover

general mathematical novelty:
0

historical identity:
NONE

historical TAC/SAC terminology:
NOT ASSIGNED
```

The theorem does not authenticate roots, establish conditional independence,
truth, honesty, competence, tawatur, recipient warrant, authorization,
applicability, adoption, execution, common knowledge, or world truth.  It does
not cover stochastic/adaptive protocols, dynamic membership, version drift,
collusion, or mobile corruption.
