# Deep CN V2 — authority-indexed anchor covers and guarded context migration

## Identity and status

```text
identity: PMR-007-AIAC-1
canonical version: V2
status: ADMITTED_POST_MERGE_SCOPED_CROSS_LANE_AUTHORITY_AND_IDENTIFIABILITY_RESULT
historical identity: NONE
repository scientific adoption: NONE
owner adoption: PENDING
external review: OPEN
general mathematical novelty: 0
```

## 1. Typed finite setting

Let:

```text
M       finite declared model class;
Q:M→C   target coordinate;
K       authority/evidence contexts;
A       candidate anchors;
A_k     anchors independently eligible in context k.
```

Every anchor in `A_k` must be a total map on `M` with stable type and value
semantics in context `k`. Eligibility is an input established outside the
combinatorial theorem; the context does not authorize itself.

For a target-conflict pair `{m,m'}` with `Q(m) != Q(m')`, an eligible anchor
`a` resolves the pair when `a(m) != a(m')`.

Define:

```text
κ_Q(k) = the minimum cardinality of an eligible anchor family covering
         every Q-conflict pair, or infinity if no such family exists.
```

`κ_Q(k)` is a registry cardinality. It is not evidence strength, proof cost,
resource cost, or metaphysical simplicity. A weighted version requires
independently warranted costs.

## 2. Characterization and monotonicity

At the frozen finite exact-profile scope:

```text
Q is identifiable from eligible anchors in context k
iff
κ_Q(k) is finite.
```

Equivalently, target identification holds iff every target-conflict pair is
split by at least one eligible anchor.

If contexts `k,d` preserve every old anchor's type and value map and satisfy

```text
A_k ⊆ A_d,
```

then:

```text
κ_Q(d) ≤ κ_Q(k)
```

whenever the left and right sides are finite in the usual extended-order
sense. If version drift, reinterpretation, or target-dependent implementation
changes an anchor map, this monotonicity comparison is inapplicable rather than
false.

## 3. Context-migration firewall

An anchor may move from `k` to `d` only through an explicit transport contract
preserving or revalidating:

```text
anchor identity;
type;
semantics;
version;
authority;
and applicability.
```

Extensional similarity of partitions is not sufficient. In particular:

```text
Track-N source predication
≠ neutral common intervention;

receipt bytes
≠ version compatibility;

formal target coordinate
≠ eligible observable;

actual-world selector
≠ source-role profile.
```

## 4. Three exact applications

### Architecture U/I/P

```text
neutral context:
κ = infinity;

formal-coordinate context:
κ = 2, witnessed by common bearer + intentional uptake;

Track-N conditional context:
κ = 2, witnessed by common bearer + the complete source/Wisdom package;

forbidden target-oracle context:
κ = 1, demonstrating why eligibility is load-bearing.
```

### Same bytes, different recipient version

```text
receipt-only context:
κ = infinity;

version-aware context:
κ = 1, witnessed by version compatibility.
```

This recovers the exact application boundary that identical bytes do not
settle applicability.

### Source-role versus world-personality classification

```text
translated-role-only context:
κ = infinity;

Track-N guarded context:
κ = 1 relative to the frozen two-candidate class,
with either intensional predicate preservation or actual-world selection
splitting the candidate pair.
```

Those anchors have different authority types and are not interchangeable. The
application remains source/world conditional and does not establish that either
anchor is actually warranted.

## 5. Anti-unification

The shared structure is:

```text
finite context-indexed conflict cover.
```

The native structures remain different:

```text
architecture:
common-intervention semantics and architecture target types;

recipient transport:
version, authority, capability, invalidators, adoption, execution;

source/world:
source custody, translation, referent, predicate strength,
actual-world selection, applicability.
```

Thus Deep CN provides a genuine common typed layer and a guarded transfer
firewall, not an identity among the domains.

## 6. Executable evidence and checker custody

The first primary checker was preserved as failed: its direct oracle wrongly
required one joint signature per target value and therefore rejected legitimate
refinements within a target class.

The repaired primary checker returned:

```text
random finite systems: 30,000
criterion failures: 0
eligibility-expansion monotonicity failures: 0
all three frozen application tables: PASS
```

## 7. Theorem family and central effect

```text
general mechanism:
finite fibre constancy + constrained set cover;

ancestry:
Deep BX, Deep BV, Deep CL, AR8R-T294, standard partition refinement;

new central contribution:
explicit authority-context index, migration contract, and one common
formal layer spanning architecture, recipient version, and source/world
classification while preserving their nonidentity;

new general mathematics:
NONE.
```

Deep CN makes the current UI residual more exact:

> the missing item is not merely another coordinate; it is an independently
> eligible coordinate in the neutral or otherwise declared comparison context.

The Track-N package can split the residual only within its guarded source/world
context. The currently certified neutral context still has no finite cover.

## 8. Conclusion ceiling

```text
neutral U/I/P discriminator: NONE
Track-N conditional discriminator: PRESENT ONLY UNDER FULL GUARDS
recipient version discriminator: PRESENT WHEN VERSION CONTRACT IS ELIGIBLE
cross-context migration: REQUIRES EXPLICIT TRANSPORT
proper-function/personal bridge: UNESTABLISHED
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```
