# Specialist B round 2 — from declared-frame root to self-subsistence

```text
packet-local candidate: SB-C2 GROUNDING_COMPLETENESS_CERTIFICATE
packet-local rivals:
  SB-R7 HIDDEN_GROUNDER
  SB-R8 FRAME_EXTENSION
  SB-R9 MULTIPLE_NONBORROWED_ROOTS
  SB-R10 UNIQUE_IMPERSONAL_NONCREATOR
  SB-R11 ABSTRACT_ORDER_PLUS_GROUNDED_CONCRETE_ROOT
status: ELEMENTARY GUARDED IMPLICATION; METAPHYSICAL ASCENT OPEN
nearest owners: Deep BK; bridge ledger B4, B5, B6
```

## 1. Residual selected after ancestry check

Deep BK already separates:

```text
actual root;
worldwise root-role persistence;
coherent transport;
one numerical global bearer;
concrete exemplification;
metaphysical necessity beyond a declared frame.
```

It proves only that its full package yields a
`DECLARED_FRAME_PERSISTENT_CONCRETE_ROOT`. Deep BK explicitly refuses to infer
self-subsistence, nonborrowed actuality, Necessary Being, originator,
actualizer, Creator, unity, intellect, personality, Wisdom, or Speech.

This round therefore does **not** rerun Deep BK. It advances one arrow:

```text
declared-frame-persistent concrete root
  ?
nonborrowed/self-subsistent concrete ground.
```

The repeated residual is a missing **grounding-domain completeness** coordinate,
not another role-persistence condition.

## 2. Typed grounding language

Fix:

```text
W : type of worlds or modal indices
G : type of candidate bearers/entities
Exists(w,x)
Grounds(w,y,x)       -- y is an actual ground of x in w
Recorded(w,y,x)      -- the declared model records y as a ground of x
Concrete(w,x)
```

Define:

\[
\operatorname{RecordedRoot}(w,x)
:= Exists(w,x)\land\neg\exists y\,Recorded(w,y,x).
\]

\[
\operatorname{Nonborrowed}(w,x)
:= Exists(w,x)\land\neg\exists y\,Grounds(w,y,x).
\]

The smallest sufficient completeness guard for this implication is incoming
completeness at the target:

\[
\operatorname{IncomingComplete}(w,x)
:=\forall y\,[Grounds(w,y,x)\rightarrow Recorded(w,y,x)].
\]

A stronger fidelity certificate may also require soundness:

\[
Recorded(w,y,x)\rightarrow Grounds(w,y,x).
\]

Soundness is useful for interpreting recorded edges, but only incoming
completeness is needed to rule out a hidden ground of a recorded root.

## 3. Elementary guarded theorem

### SB-C2A — recorded root under incoming completeness

\[
IncomingComplete(w,x)\land RecordedRoot(w,x)
\Rightarrow Nonborrowed(w,x).
\]

**Proof.** Assume a true ground `y`. Incoming completeness records it, contrary
to recorded-root status. The existence conjunct is inherited.

Classification:

```text
general mathematical novelty: 0
theorem class: elementary relation-restriction implication
repository role: guard/certificate for interpreting Deep BK roots
not: a proof that the chosen grounding relation is complete or metaphysically correct
```

### SB-C2B — frame-persistent nonborrowed root

Suppose Deep BK’s package supplies a single global bearer `g` with a concrete
root occurrence `s(w)` at every `w` in declared frame `F`. Add:

```text
INCOMING_COMPLETENESS:
  every true incoming ground of each s(w) in the intended grounding domain is
  represented by the declared relation;

OCCURRENCE/GLOBAL LINK:
  nonborrowedness of s(w) is the intended bearer-level nonborrowedness of g;

FRAME_SCOPE:
  the conclusion is only over F.
```

Then `g` has a concrete nonborrowed occurrence throughout `F`.

This remains **frame-relative**. To conclude metaphysical necessity requires a
separate modal adequacy premise:

```text
FRAME_COMPLETE:
  F exhausts the worlds/possibilities relevant to the modal conclusion,
  or the quantified model already ranges over every relevant possibility.
```

To conclude essential self-subsistence requires a separate interpretation:

```text
NONBORROWED_SEMANTICS:
  absence of a Grounding predecessor in the complete domain is sufficient for
  the intended metaphysical independence/self-subsistence predicate.
```

Neither premise follows from the finite model.

## 4. Modal and causal distinctions

Keep at least these coordinates separate:

```text
MNEC_F(x): x exists at every world in declared frame F;
MNEC(x): x exists at every metaphysically possible world under the intended semantics;
UNG_w(x): x has no ground in world w;
ESS_UNG(x): x is ungrounded wherever it exists across the intended modal range;
UNCAUSED(x): x has no efficient cause under a chosen causal theory;
SELF_SUBSISTENT(x): theory-specific independence predicate;
ORIGINATES(x,z): x originates z;
ACTUALIZES(x,z): x actualizes z;
CREATOR_SCOPE(x,D): x creates every member of domain D under the intended sense.
```

No equivalence among these is available merely from notation. In particular:

```text
root in a recorded graph != ungrounded in reality;
ungrounded in one world != modally necessary;
exists in all declared worlds != necessary in itself;
uncaused != cause of anything;
originator of one effect != Creator of the cosmos;
one root role != numerically unique being;
concrete != personal or agentic.
```

## 5. Avicennian and Taymiyyan ancestry firewall

Avicenna’s necessary-in-itself/possible-in-itself division belongs to a richer
causal-modal metaphysics. In the secondary scholarly map, what is possible in
itself is dependent/caused and what is necessary in itself is uncaused;
`Ilāhiyyāt I.6` and `VIII.1–4` are the primary loci requiring exact Marmura-page
verification. That system cannot be reduced to “no incoming edge in a finite
graph” without an interpretation theorem establishing that the graph exhausts
the relevant causal dependence relation.

The translated Aṣfahāniyyah commentary makes a distinct critical point at
printed p. 29: a conclusion of necessary existence alone does not establish a
Creator/originator of the heavens and earth. In AR8R terms, even a valid
necessary-existence bridge leaves a separate originator/actualizer/Creator
coordinate.

Therefore:

```text
Avicennian modality/causality: a substantive philosophical architecture;
Taymiyyan criticism at this locus: a source-relative warning that the bare
  necessary-existence conclusion is insufficient for Creatorhood;
SB-C2: an elementary model-fidelity theorem.
```

These are neither identical nor competing formulations of one theorem.

## 6. Countermodels and load-bearing deletions

### SB-CM9 — hidden ground in an incomplete graph

True grounding contains `y → x`; the recorded graph omits it. `x` is a recorded
root and concrete, but not nonborrowed. Deleting incoming completeness defeats
SB-C2A.

### SB-CM10 — frame-persistent root with world-indexed hidden grounders

`x` is the same concrete bearer in `w0` and `w1`. The recorded relation has no
incoming edge at either world. In reality `y0` grounds `x` in `w0` and `y1`
grounds `x` in `w1`. Persistence, concreteness, and B_ID all hold while
self-subsistence fails.

### SB-CM11 — frame extension

The full package holds on `F={w0,w1}`. An intended possibility `w2` is omitted;
there `x` is absent or grounded. Deleting frame completeness defeats the
metaphysical modal conclusion.

### SB-CM12 — abstraction/concretion split

A necessary abstract order persists across the frame. A concrete bearer
instantiates or realizes it but remains grounded by another concrete or
structural condition. Necessary order does not entail a nonborrowed concrete
being.

### SB-CM13 — multiple nonborrowed concrete roots

`x` and `z` are both concrete, persistent, and ungrounded in the complete
domain. Nonborrowedness does not imply numerical uniqueness. B6 remains open.

### SB-CM14 — unique impersonal noncreator

One concrete nonborrowed field exists across the declared complete frame. It has
no mentality, intention, speech, or productive relation and causes nothing.
Uniqueness plus nonborrowedness does not yield personality or Creatorhood.

### SB-CM15 — uncaused originator of a restricted domain

`x` is uncaused and actualizes one event but not the remaining domain. An
originator relation needs scope before it becomes Creatorhood.

### SB-CM16 — source-referent deletion

An authenticated source predicates Creatorhood of `d`; the neutral model has a
nonborrowed root `x`; no identity/referent bridge establishes `x=d`.

### SB-CM17 — grounding-theory variance

A powers theorist treats `x` as primitive; a grounding realist represents a
further ground; a nominalist paraphrases the relation; a conceptualist treats
it as scheme-relative. The same recorded profile does not identify the intended
metaphysical grounding relation.

## 7. Dependency and noncircularity audit

A grounding-completeness certificate is legitimate only if it is defended
independently of the desired conclusion. Circular forms include:

```text
defining the “complete domain” as exactly the edges that preserve x as root;
excluding rival grounders because they make x borrowed;
treating source identification of x as Creator as evidence that the neutral
  grounding graph was complete;
defining metaphysical possibility as the finite frame on which x persists;
or defining self-subsistence as recorded-root status.
```

The guard should instead specify:

```text
domain of entities and relations;
criterion for admitting a grounding edge;
coverage argument;
observation/source limitations;
modal scope;
identity semantics;
and independently reviewable failure conditions.
```

## 8. Proper-function and ontology effects

Proper function does not repair grounding incompleteness. A system can have a
selected effect, designed role, truth aim, or fitrah-relative function while
being derivative. Conversely, a nonborrowed ground need not have a function,
norm, intellect, or purpose.

Property ontology remains orthogonal: the relata and grounding relation can be
modeled in nominalist, trope, realist, powers, conceptualist, or plural terms.
Property dualism adds no route from graph-root status to necessary personal
being.

## 9. Disposition

```text
Deep BK duplicated: NO
new result: incoming-grounding completeness identified as the next exact guard
formal status: elementary implication, finite checker PASS
Necessary Being: NOT ESTABLISHED
self-subsistence: CONDITIONAL ON COMPLETE GROUNDING SEMANTICS
Creatorhood: NOT ESTABLISHED
unity/personality/Wisdom/Speech: NOT REACHED
strongest rivals preserved:
  hidden grounder;
  multiple nonborrowed roots;
  unique impersonal noncreator;
  abstract order + derivative concrete bearer.
```

## 10. Next atomic action

Ask Specialist A to formalize the relation-theoretic implication and its
frame-lift without importing source or metaphysical axioms. Ask Deep Research
20 for exact mathematical/metaphysical ancestry of “root under complete
relation” versus ontological grounding, and ask Deep Research 21 for primary
Avicennian and Taymiyyan locators. The central integrator should add a
`GROUNDING_DOMAIN_COMPLETENESS` burden between Deep BK’s persistent root and
any self-subsistence claim.
