# PMR-007 Deep Round AV V2 — Neutral bridge interval and source-to-world interpolation firewall

## Candidate disposition

```text
identity: PMR-007-NBIF-1
provenance: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
general mathematical novelty: 0
external review: OPEN
owner adoption: PENDING
```

## 1. Typed finite propositional setting

Fix finite Boolean variable sets with a declared partition:

```text
X — source-, translation-, architecture-, or evidence-exclusive coordinates;
N — independently defended neutral/shared bridge coordinates;
Y — target-, world-, or conclusion-exclusive coordinates.
```

Let `A(X,N)` be a source/formal antecedent and `C(N,Y)` a target conclusion.
Define the strongest neutral consequence of `A` and the weakest neutral
sufficient condition for `C`:

\[
S_A(n):=\exists x\,A(x,n),
\qquad
T_C(n):=\forall y\,C(n,y).
\]

The words *source*, *neutral*, and *world* are type declarations whose
justification lies outside the theorem.  A target predicate or an equivalent
proxy may not be placed in `N` without independent authority.

## 2. NBIF-1A — exact finite neutral-bridge criterion

The following are equivalent:

```text
1. A entails C over all X,N,Y valuations;
2. S_A entails T_C;
3. there exists a neutral formula/table I(N) such that
   A entails I and I entails C.
```

### Proof

If `A(x,n)` holds, then `S_A(n)` holds.  If `S_A(n)` implies `T_C(n)`, then
`C(n,y)` holds for every `y`, proving `A entails C`.

Conversely, suppose `A entails C` and `S_A(n)` holds.  Some `x` satisfies
`A(x,n)`.  Since the entailment holds for every `y`, `C(n,y)` holds for all
`y`; hence `T_C(n)`.  Taking `I=S_A` proves existence.  Any interpolant also
gives the entailment by transitivity. ∎

## 3. NBIF-1B — complete interpolant interval

A neutral table `I(N)` is an interpolant exactly when

\[
S_A \Rightarrow I \Rightarrow T_C.
\]

Thus:

```text
S_A is the strongest neutral consequence of A;
T_C is the weakest neutral sufficient condition for C;
interpolants form the Boolean interval [S_A,T_C].
```

Define the finite **neutral bridge slack** at the frozen vocabulary:

\[
\sigma_N(A,C)
:=
|\{n:T_C(n)=1\text{ and }S_A(n)=0\}|.
\]

When `A entails C`, the number of semantically distinct neutral truth-table
interpolants is exactly

\[
2^{\sigma_N(A,C)}.
\]

In particular, the neutral bridge is semantically unique iff

\[
S_A=T_C,
\]

i.e. iff `sigma_N=0`.

### Proof

On valuations with `S_A=1`, every interpolant must be one.  On valuations with
`T_C=0`, every interpolant must be zero.  Exactly the `sigma_N` remaining
valuations are free, independently yielding `2^{sigma_N}` tables. ∎

The count is vocabulary- and representation-relative.  It is not an invariant
of natural-language explanation or metaphysical structure.

## 4. NBIF-1C — source/neutral/world transfer firewall

At the declared classical logical scope, a genuine source-to-neutral/world
entailment with source-exclusive and target-exclusive vocabulary must expose a
bridge in the shared neutral vocabulary.  There are four distinct cases:

```text
NEUTRAL BRIDGE:
  a separately defensible I(N) mediates the entailment;

DIRECT SOURCE PREDICATION:
  the target predicate already occurs in the source package;
  this is source-relative, not neutral derivation;

TARGET IMPORT:
  a target or equivalent proxy was placed in N;
  the apparent bridge is question-begging;

NO ENTAILMENT:
  S_A does not imply T_C;
  a deletion/rival valuation survives.
```

The theorem provides an audit location.  It does not decide which vocabulary is
legitimately neutral.

## 5. Classical first-order ancestry

Craig's interpolation theorem supplies the ordinary first-order analogue: if a
first-order sentence entails another, an interpolant exists using only their
shared nonlogical vocabulary.  Deep AV does not reprove that theorem and does
not transfer it to logics lacking interpolation.

Deep AF's Beth result addresses a different question—whether a target relation
is implicitly fixed by a reduct.  Deep AV addresses whether an entailment can
be factored through shared vocabulary.  The two form complementary gates:

```text
Beth/Deep AF:
  does the neutral theory determine the target across expansions?

Craig/Deep AV:
  if an entailment exists, what shared-vocabulary bridge must mediate it?
```

## 6. Mandatory controls

### AV-CM1 — satisfiable source, contingent target, no shared bridge

With no informative shared coordinate, a satisfiable source claim cannot entail
a contingent target claim over all target valuations.

### AV-CM2 — inconsistent source

`A=false` entails every `C`; `S_A=false`.  This is logical vacuity, not evidence
for the conclusion.

### AV-CM3 — tautological target

If `C=true`, every `A` entails it and bridge slack can be large.  No
architecture discriminator follows.

### AV-CM4 — hidden target import

Declaring `PERSONAL` or `WISE` neutral makes `I=PERSONAL` or `I=WISE` available.
The logical derivation is valid but the research bridge was imported.

### AV-CM5 — direct Track-N predication

A source may directly predicate knowledge, will, life, speech, or another
attribute of one source referent.  That can constrain a Track-N model class but
is not a school-neutral derivation of the same predicate.

### AV-CM6 — translation/world deletion

Source bytes plus a formal interpolant do not establish translation adequacy,
referent identity, candidate-world completeness, or actual-world truth.

### AV-CM7 — nonunique bridge

A satisfiable antecedent `A=N` and tautological target have both `I=N` and
`I=true` as interpolants.  V1's uniqueness claim fails.

### AV-CM8 — finite-model/logic overread

Bounded finite absence of a countermodel does not establish first-order,
modal, intensional, or metaphysical entailment.

## 7. Central program effects

### Transcendental ascent

Every arrow from underived order to actuality, Creatorhood, unity, mentality,
Wisdom, Speech, or revelational identification must either expose a neutral
shared-vocabulary interpolant or be classified as source-relative predication,
target import, or an unproved bridge.

### Candidate N / Track N

Candidate N can supply source predicates and relations at its actual authority.
Deep AV prevents those predicates from silently migrating into Track T.  A
neutral bridge must be independently defended and vocabulary-clean.

### Candidate G / integrated architecture

A common bearer label or one source name is not an interpolant unless it
actually entails the target under the frozen theory.  Bridge slack records how
many neutral valuations remain unconstrained at the finite declared scope.

### Source–formal–implementation–world crosswalk

The theorem distinguishes syntactic/logical mediation from source truth,
implementation correspondence, causal validity, and world truth.  Those remain
separate coordinates.

## 8. Scope, authority, and nonclaims

```text
finite theorem:
constructive propositional interpolation interval

first-order relation:
APPLICATION OF CRAIG INTERPOLATION

Deep AF relation:
COMPLEMENTARY_TO_BETH_DEFINABILITY_NOT_A_NEW_BETH_ORIGIN

general mathematical novelty:
0

historical identity:
NONE
```

No source premise, translation, neutral vocabulary, actual world, metaphysical
bridge, personal ground, divine attribute, integrated champion, meniscus, or
natural closure is established by the logical theorem alone.
