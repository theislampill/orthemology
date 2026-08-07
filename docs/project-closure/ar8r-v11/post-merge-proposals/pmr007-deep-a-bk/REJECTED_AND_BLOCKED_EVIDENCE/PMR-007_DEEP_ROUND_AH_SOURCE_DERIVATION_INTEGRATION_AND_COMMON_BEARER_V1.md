# PMR-007 Deep Round AH V1 — source derivation integration and common-bearer adjudication

```text
identity: PMR-007-SDIG-1
round: PMR-007-DEEP-AH
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_task: Track-N source-formal-world adjudication after the strengthened R5 common model
```

## 1. Exact source objects used

The selected English translated-primary-access snapshot is
`A-Commentary-on-the-Creed-of-Asfahani-v2.3(1).md`.

The source strata are kept separate:

```text
al-Asfahani creed text:
  lines 68–95 in the supplied Markdown;

Ibn Taymiyyah commentary in English translation:
  lines 97–128, 481–548, and 1761–1816;

translation authority:
  TRANSLATED_PRIMARY_ACCESS;

Arabic-primary verification:
  NOT PERFORMED.
```

The creed co-predicates Creator, unity, knowledge, ability, life, volition,
speech, hearing, and sight of one grammatical referent.  The commentary calls
that package true, but then repairs or criticizes several proposed arguments.
In particular:

```text
creation/volition -> knowledge:       lines 500–503;
choice -> ability:                    lines 523–530;
knowledge + ability -> life:          lines 534–536;
specification -> volition:            lines 538–548;
engenderment/command -> speech:       lines 124–128;
perfection/qiyas routes:              lines 1761–1816;
shared necessity -> one bearer proof: criticized at lines 481–495.
```

## 2. Selected typed role graph

Let

```text
V = {
  CREATION,
  SPECIFICATION,
  CHOICE,
  VOLITION,
  KNOWLEDGE,
  ABILITY,
  LIFE,
  SPEECH,
  PERFECTION
}.
```

Freeze the source-dependency supports

```text
{CREATION,VOLITION}
{VOLITION,KNOWLEDGE}
{SPECIFICATION,VOLITION}
{CHOICE,ABILITY}
{KNOWLEDGE,ABILITY,LIFE}
{CREATION,SPEECH}
{SPEECH,PERFECTION}
```

as a typed abstraction of the selected passages.  This is not claimed to be a
complete graph of Ibn Taymiyyah's theology.

## 3. Candidate results

### SDIG-1A — source-role nonflatness

The selected support hypergraph is connected.  Equivalently, every nontrivial
partition of `V` is crossed by at least one source-dependency support.  Thus the
selected Track-N role package contains genuine cross-role constraints and is
not merely nine isolated labels.

### SDIG-1B — connected derivation does not entail one bearer

Let a realization assign a bearer to each role.  If local support satisfaction
records only that the role relation is instantiated, without an equality or
co-reference clause, then every bearer partition—including the injective
nine-bearer assignment—is compatible with the same connected role graph.
Therefore:

```text
connected source-dependency graph
DOES NOT ENTAIL
one common bearer.
```

### SDIG-1C — source binder as an independent Track-N premise

The supplied creed/commentary package explicitly co-predicates the selected
attributes of one source referent.  When that co-reference statement is
accepted as an authenticated, applicable Track-N premise, the injective plural
realization is source-incompatible at the selected scope.

This is source-relative model restriction.  It is not a neutral proof of one
bearer, because the generic unity argument from shared necessity and
individuation is itself criticized in the commentary.

### SDIG-1D — source dependency is not source-to-world transfer

The same abstract dependency graph can be implemented in an impersonal formal
system.  Source identity, translation adequacy, premise acceptance, referent
identity, and world adequacy are therefore separate guards.  Without them the
selected source graph does not exclude the strengthened R5 neutral rival.

## 4. Positive construction

`AH-POS-TRACK-N` assigns every selected role to one bearer `g`, instantiates all
seven support relations, and marks the source binder, source identity,
translation, applicability, and source-to-world guards separately.

At the Track-N conditional level it is a connected, common-bearer source
architecture.  Its common-bearer status comes from the source binder; its
nonflatness comes from the cross-role supports.  Those are different facts.

## 5. Mandatory countermodels

```text
AH-CM1 DISTRIBUTED-SOURCE-SHAPE:
  nine bearers realize the same role graph; source binder false.

AH-CM2 CARRIER-BOXING:
  one bearer carries all role labels while every cross-role dependency is
  deleted; one carrier alone is not derivational unity.

AH-CM3 IMPERSONAL-GRAPH-REALIZER:
  one impersonal automaton realizes the full role graph while PERSONAL,
  FIRST_PERSON_OWNERSHIP, WISDOM, and DIVINE_SPEECH are false.

AH-CM4 AUTHORITY-DELETION:
  source-shaped predicates without source identity/applicability/world guards
  do not create a world-directed conclusion.

AH-CM5 GENERIC-UNITY-FAILURE:
  two individuated necessary-role bearers share an abstract necessity
  predicate; shared abstract predication does not force numerical identity.

AH-CM6 SPEECH-NONTRANSFER:
  command/speech dependency at source-relative scope does not make formal
  articulability entail mentality, uncreated Speech, or revelation neutrally.

AH-CM7 QIYAS-GUARD-DELETION:
  a predicate that is creaturely available but not independently established
  as pure perfection cannot be transferred by the selected a-fortiori route.
```

## 6. Candidate-G and R5 effect

Deep AG's strongest neutral impersonal rival survives the neutral reduct.  Deep
AH supplies a distinct result:

```text
accepted Track-N source binder:
  excludes the plural role assignment source-relatively;

selected source dependencies:
  prevent a flat role inventory inside Track N;

neutral common-bearer theorem:
  still absent;

world truth of the source package:
  not established by the graph.
```

Thus Candidate N may be a genuinely integrated source architecture at the
selected translated-source scope while remaining unable to replace Candidate
G's neutral derivational-unification burden or the transcendental bridge.

## 7. Conclusion ceiling

This packet does not establish Arabic-primary wording, source authentication,
translation adequacy, world truth, Necessary Being, Creatorhood, numerical
unity, personality, Wisdom, divine Speech, revelational identification, an
integrated champion, meniscus, or natural closure.

## 8. Ancestry and novelty

```text
Candidate N source architecture:
  SOURCE-RELATIVE APPLICATION AND ADJUDICATION;

Deep AE interaction hypergraph:
  SHARED CONNECTED-SUPPORT MECHANISM ONLY;

Deep AG strengthened R5 common model:
  CHAMPION–CHALLENGER INPUT;

general mathematical novelty:
  0;

historical identity:
  NONE.
```
