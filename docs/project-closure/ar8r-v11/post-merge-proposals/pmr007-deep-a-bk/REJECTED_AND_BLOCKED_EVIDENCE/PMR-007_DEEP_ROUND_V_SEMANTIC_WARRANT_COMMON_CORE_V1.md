# PMR-007 Deep Round V V1 — semantic/warrant common core

```text
identity: PMR-007-SWPC-1
round: PMR-007-DEEP-V
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
```

## 1. Target burden

Fable Round 1 leaves `FABLE-R1-B06` open because its two rival typed cores
answer different questions:

```text
Core A:
  is the declared target uniform on the attained semantic/profile fibres?

Core B:
  does a warrant-bearing derivation survive the declared provenance,
  version, authority, and invalidator transport?
```

The frozen packet reports all four verdict quadrants and says neither core
refines the other. This round asks whether one finite common diagnostic can
answer both without identifying the questions.

## 2. V1 joint object

For a finite evaluation episode `e`, define two Booleans:

```text
Sem(e):
  the declared target is certifiable from the declared profile;

War(e):
  the declared certificate/warrant chain is valid in the recipient setting.
```

Define:

```text
J(e) = (Sem(e), War(e)).
```

V1 proposes that `J` is the common core of Core A and Core B.

## 3. Candidate claims

### SWPC-1 — joint factorization

Both coordinates factor through `J` by projection. If `q : E -> Q` is any
other profile through which both `Sem` and `War` factor, then:

```text
q(e) = q(e')
  implies
J(e) = J(e').
```

Thus `J` is the coarsest exact joint diagnostic, up to a bijection on its
attained image.

### SWPC-2 — four-state lower bound

When all four pairs in `{0,1}^2` are attained, every exact joint diagnostic
needs at least four values. A fixed-length binary encoding therefore needs at
least two bits.

### SWPC-3 — release versus diagnosis

The one-bit release predicate

```text
Release(e) = Sem(e) and War(e)
```

decides whether both axes pass, but merges three distinct failure modes:
semantic-only, warrant-only, and neither. One-bit release is not a substitute
for the exact two-axis diagnosis.

### SWPC-4 — no neutral strict scalarization

The coordinatewise order on `{0,1}^2` leaves `(1,0)` and `(0,1)` incomparable.
There is no axis-swap-invariant strict total order extending that product
order. Any strict scalar ranking of the mixed states therefore adds an
independently warranted priority between semantic and warrant failure.

### SWPC-5 — world-truth nontransfer

Even `Sem(e) = War(e) = true` does not entail that the declared target matches
an independently fixed world target. Adding

```text
WorldAdeq(e): declared target = independently fixed world target
```

yields an independent third axis. If all eight triples are attained, an exact
three-axis diagnostic needs at least eight values, or three fixed-length bits.

## 4. Finite witness family

The model owner contains eight evaluation episodes. Each episode has:

```text
a two-background declared classification system;
a profile map;
a declared target label;
an independently fixed world target;
a frozen certificate root set;
a target-local root transport domain.
```

The semantic axis is computed by fibre constancy, the warrant axis by complete
transport of required roots, and the world axis by equality of declared and
world targets. The construction realizes every element of `{0,1}^3`.

## 5. Proposed central consequence

V1 proposes to close `FABLE-R1-B06` by treating the product diagnostic as a
common core. It also proposes that this product is the minimum non-scalar
state needed by any implementation that must distinguish semantic failure from
warrant failure.

## 6. Authority ceiling

```text
general mathematical novelty:
  ZERO

Core A kernel theorem:
  LEAN_FORMALIZED_AT_SCOPED_T299_INTERPRETATION

Core B full calculus:
  NOT_MACHINE_VERIFIED

current repository status:
  PROPOSAL_ONLY

owner adoption:
  PENDING

integrated champion:
  NONE

meniscus:
  MENISCUS_NOT_REACHED
```
