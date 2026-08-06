# PMR-007 Deep Round W V2 — contract-aligned pullback and target-identity firewall

```text
identity: PMR-007-TIPC-1
round: PMR-007-DEEP-W
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
```

## 1. Exact role

Deep V supplies a two-axis diagnostic product. Deep W asks how component
objects can be combined without silently pairing a profile certificate for one
target with a warrant object for another.

The result is a **contract-aligned integration interface**, not a common
explanatory calculus.

## 2. Full finite contract key

For this declared model, let:

```text
K = (
  target_id,
  target_version,
  recipient_scope,
  analysis_version,
  referent_id,
  semantic_contract_digest
).
```

This key is not universally complete. New evidence can require additional
coordinates. In particular:

```text
referent_id:
  requires independent referent binding;

semantic_contract_digest:
  requires an independently adequate contract and canonicalization;

source-related fields:
  require source authentication and do not migrate Track-N premises into Track T.
```

## 3. Valid component subobjects

Let:

```text
A*:
  independently admitted profile/semantic certificate objects;

B*:
  independently admitted warrant/provenance certificate objects;

C*:
  independently admitted world/target-adequacy bridge objects.
```

Each object carries a map to `K`:

```text
alpha : A* -> K
beta  : B* -> K
gamma : C* -> K.
```

The pullback does not establish component validity. Validity is a prerequisite
to entry into `A*`, `B*`, or `C*`.

## 4. TIPC-1 — exact contract-aligned pair

Define:

```text
A* x_K B*
  = { (a,b) : alpha(a) = beta(b) }.
```

Membership is equivalent to exact equality of the full declared contract key.
The projections preserve each component object and its status.

This rejects the exhibited:

```text
target-version mismatch;
recipient-scope mismatch;
analysis-version mismatch;
referent mismatch;
semantic-contract mismatch.
```

Same bytes, same storage, or the same structural carrier does not replace key
equality or authorized transport.

## 5. TIPC-2 — universal compatibility property

For every finite set `X` with maps:

```text
f : X -> A*
g : X -> B*
```

such that:

```text
alpha ∘ f = beta ∘ g,
```

there exists a unique map:

```text
h : X -> A* x_K B*
```

whose projections are `f` and `g`.

This is the standard pullback universal property. It says that every exact
contract-compatible integration factors through the target-indexed pairing.
It does not explain or prove the component predicates.

## 6. TIPC-3 — three-way source/formal/world interface

Conditional on a separately admitted `C*`, define:

```text
A* x_K B* x_K C*.
```

This forces all three objects to address the same full contract key. It does
not entail world truth merely from agreement. An invalid world-bridge object is
excluded upstream; the pullback cannot validate it.

## 7. Countermodel and firewall suite

### W-CM-1 — Cartesian target mismatch

`A* x B*` pairs every profile object with every warrant object, including
version, scope, analysis, referent, and contract mismatches. A Cartesian product
alone is unsafe.

### W-CM-2 — coarse-key referent alias

A key omitting `referent_id` admits a profile object about `R1` with a warrant
object about `R2`. Printed target names and versions can match while referents
differ.

### W-CM-3 — same bytes, different version

The same bytes and carrier occur under `v1` and `v2`. The full pullback rejects
the silent pairing. This instantiates the version-custody boundary rather than
proving version validity.

### W-CM-4 — invalid component in the raw pullback

Invalid profile and warrant objects with equal keys inhabit the raw pullback.
Restricting to independently valid subobjects is load-bearing.

### W-CM-5 — source-key nonauthentication

A copied source or referent identifier can satisfy key equality without H12
source authentication or H16 referent identification. Key equality is a
contract check, not source truth.

### W-CM-6 — compatible pair without one bearer

A profile certificate and warrant certificate may be distinct objects carried
by different systems. Their pullback pair does not establish numerical
identity, one intentional subject, one metaphysical bearer, or one causal
realizer.

### W-CM-7 — aligned false target

Profile, warrant, and world-bridge records can all name one target contract
while the independently selected target semantics are mistaken. The
architecture preserves declared alignment; it does not select or prove the
ultimate target.

## 8. Exact executable evidence

The finite owner contains:

```text
5 profile objects;
6 warrant objects;
4 world-bridge objects.
```

The primary checker compares Cartesian, coarse-key, full-key, and valid-subobject
pullbacks; verifies every mismatch control; and exhaustively checks the pair
universal property for all compatible cones from finite domains of size at most
two.

The repaired model uses the full key and valid subobjects as canonical. The
coarse key remains only as rejected evidence.

## 9. Program effects

```text
FABLE Core A/Core B:
  a target-indexed common integration interface now exists;
  the common proof calculus and explanatory core remain open.

AR2/AR3 reason transport:
  target-local reason preservation becomes the B* input;
  Deep W does not reprove AR3.

version custody:
  same bytes do not authorize cross-version pairing.

OSM/Deep U:
  task, model, encoding, analysis version, and trajectory contract can enter K;
  endpoint similarity does not erase those coordinates.

Track N/Deep S/T:
  source and referent fields constrain admissibility only when independently
  authenticated; no neutral migration follows.

Candidate G/common bearer:
  compatible component objects do not establish one numerical or intentional
  bearer.

source-formal-implementation-world crosswalk:
  exact contract alignment is now distinguished from component validity and
  world truth.
```

## 10. Theorem-family and prior-art disposition

```text
mathematical mechanism:
  STANDARD_PULLBACK_IN_FINITE_SETS

program relation:
  TARGET_INDEXED_APPLICATION_TO_PROFILE_WARRANT_WORLD_BINDING

independent theorem origin:
  NO

general mathematical novelty:
  ZERO
```

The construction is useful because it repairs a real target-mismatch failure in
the current program, not because the pullback is new mathematics.

## 11. Exact disposition and nonclaims

```text
candidate status:
  REPAIRED_POST_MERGE_RESEARCH_CANDIDATE

repository status:
  PROPOSAL_ONLY

external review:
  OPEN

owner adoption:
  PENDING

integrated champion:
  NONE

meniscus:
  MENISCUS_NOT_REACHED

natural closure:
  NOT_REACHED
```

Deep W does not verify the full Core B calculus, prove target-key adequacy,
authenticate a source, establish world truth, identify one bearer, or add a
metaphysical, personal, attribute, Speech, or revelational bridge.
