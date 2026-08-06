# PMR-007 Deep Round V V2 — profile/warrant diagnostic product and world firewall

```text
identity: PMR-007-SWPC-1
round: PMR-007-DEEP-V
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
```

## 1. Exact problem and source ceiling

Fable Round 1's two proposed cores ask different questions:

```text
Core A:
  does the declared target factor through the declared profile?

Core B:
  does a reason-bearing warrant object survive the declared provenance,
  version, authority, and invalidator conditions?
```

Only Core A's central fibre characterization has a Lean kernel receipt, and even
that receipt is for a repaired scoped interpretation of T299. The full Core B
calculus remains `DERIVED_BUT_UNVERIFIED`. This round therefore does not verify
Core B. It formalizes a minimal joint diagnostic around one frozen warrant
object.

## 2. Typed paired bearer

An `EvaluationEpisode` is a finite record:

```text
E = (
  W, P, L_declared, L_world,
  item, target, recipient_scope,
  required_roots, transported_roots,
  authority_valid, version_valid, invalidators_closed
).
```

The classification system and warrant object refer to the same declared target
and recipient scope. This typed pairing prevents an arbitrary Core-A verdict
from being multiplied by an unrelated Core-B verdict.

Define:

```text
ProfileCert(E):
  L_declared is constant on every attained P-fibre.

FrozenRootComplete(E):
  required_roots are a subset of transported_roots,
  and authority_valid, version_valid, invalidators_closed all hold.

WorldAdeq(E):
  L_declared = L_world on every registered background.
```

`L_world` is an independently supplied parameter of the finite model. Equality
with it is checkable; its epistemic or metaphysical authority is not established
by this theorem.

## 3. SWPC-1 — coarsest exact two-axis diagnostic

Let

```text
J2(E) = (ProfileCert(E), FrozenRootComplete(E)).
```

Both coordinates factor through `J2` by projection. Conversely, if
`q : Episodes -> Q` is any profile through which both coordinates factor, then:

```text
q(E) = q(E')
  implies
J2(E) = J2(E').
```

Therefore `J2` is the coarsest exact joint diagnostic, up to a bijection on its
attained image.

This is a product/factorization theorem. It does not reduce one coordinate to
the other, derive their coordination, or create a unified proof calculus.

## 4. SWPC-2 — exact fixed-length information lower bound

The frozen witness class realizes all four values of `{0,1}^2`. Hence any exact
joint diagnostic code must distinguish four attained states. Its alphabet has
size at least four, and an exact fixed-length binary code needs at least two
bits.

This is a worst-case/fixed-length result only. No expected-length, interactive,
randomized, or adversarial-channel optimum is claimed.

## 5. SWPC-3 — release is strictly coarser than diagnosis

The one-bit predicate

```text
Release(E) = ProfileCert(E) and FrozenRootComplete(E)
```

correctly decides whether both axes pass, but its false value merges:

```text
PROFILE_ONLY:  (true, false)
WARRANT_ONLY:  (false, true)
NEITHER:       (false, false).
```

Thus a one-bit release gate may be adequate for a bounded release decision while
being inadequate for diagnosis, repair selection, burden landing, or audit
attribution.

## 6. SWPC-4 — product order and noncanonical priority

Order the two-axis values coordinatewise with `false <= true`. Then:

```text
(false,false) <= (true,false) <= (true,true)
(false,false) <= (false,true) <= (true,true)
```

while `(true,false)` and `(false,true)` are incomparable.

There are exactly two linear extensions of this finite product order, differing
only in which mixed state is placed first. None is invariant under swapping the
profile and warrant axes. Monotone scalar scores exist, but:

```text
equal positive weights:
  tie the two mixed states;

unequal positive weights:
  impose an extra priority between profile failure and warrant failure.
```

The typed product therefore supplies no uniquely warranted strict route order.
A runtime that ranks the mixed states must declare its policy, target, and cost
of each failure mode.

## 7. SWPC-5 — world and target adequacy remain independent

Define:

```text
J3(E) = (
  ProfileCert(E),
  FrozenRootComplete(E),
  WorldAdeq(E)
).
```

The frozen witness class realizes all eight values of `{0,1}^3`. In particular,
there are episodes with:

```text
ProfileCert = true
FrozenRootComplete = true
WorldAdeq = false.
```

Consequently, profile certifiability plus root-complete warrant transport does
not entail that the declared target is correct. An exact three-axis diagnostic
over this class needs at least eight values, or three fixed-length bits.

This third axis is still not a proof of world truth. It only formalizes the need
for an independently warranted target/world relation.

## 8. Concrete independence witnesses

The model owner contains eight two-background episodes. It computes:

```text
ProfileCert:
  by fibre constancy of L_declared over P;

FrozenRootComplete:
  by required-root inclusion plus three explicit guards;

WorldAdeq:
  by equality of L_declared and L_world.
```

All eight triples occur. The model also exhibits independent transitions:

```text
semantic/profile repair can change ProfileCert while warrant status is fixed;
root reacquisition can change FrozenRootComplete while ProfileCert is fixed;
target correction can change WorldAdeq while both other axes are fixed.
```

## 9. Fable burden disposition

```text
FABLE-R1-B06:
  NARROWED_AT_DIAGNOSTIC_PRODUCT_LEVEL
```

A common finite diagnostic wrapper exists and has an exact minimum attained
alphabet. What remains open is the stronger question:

```text
Is there one nontrivial integrated calculus or architecture that explains,
generates, and preserves both profile/semantic adequacy and warrant-chain
integrity without merely storing them side by side?
```

The product does not solve Core A's false-closure vulnerability, Core B's
unverified rules, profile integrity, target independence, source truth, causal
execution, or world truth.

## 10. Theorem-family and prior-art disposition

```text
joint factorization:
  APPLICATION_OF_UNIVERSAL_PRODUCT_AND_FIBRE_FACTORIZATION

four-state structure:
  SHARED_PRODUCT_MECHANISM_WITH_BELNAP_GINSBERG_BILATTICE_TRADITION

exact relation to those logics:
  NOT_IDENTICAL — their truth/information orders and connectives are not the
  profile-certification/warrant-completeness axes defined here

AR2/AR3 relation:
  DIAGNOSTIC_WRAPPER_FOR_REASON_AND_TRANSPORT_COORDINATES

Deep T relation:
  REINFORCES_AUTHORITY_NONSELECTION_AND_NONSCALAR_POLICY_BOUNDARY

Deep U relation:
  PROCESS_EVIDENCE_MAY_REFINE_PROFILECERT_WITHOUT_SUPPLYING_WARRANT_OR_WORLD

general mathematical novelty:
  ZERO
```

## 11. Central flywheel effects

```text
profile/fibre certification -> proper orthing:
  supplies one exact declared-target coordinate;
  does not supply warrant, source truth, or world truth.

reason/provenance transport -> proper orthing:
  supplies one target-local warrant coordinate;
  does not supply semantic adequacy or target correctness.

source-formal-implementation-world crosswalk:
  now has a concrete three-axis independence control.

route-gradient and restoration:
  mixed failures are Pareto-incomparable until a policy assigns their costs;
  release success does not diagnose which burden failed.

OSM/process evidence:
  can refine the profile axis by trajectory evidence;
  does not automatically improve warrant or world adequacy.

transcendental/source ascent:
  source eligibility and formal certifiability remain separate from world truth;
  no metaphysical bridge is added.
```

## 12. Exact disposition and nonclaims

```text
candidate status:
  REPAIRED_POST_MERGE_RESEARCH_CANDIDATE

mathematical authority:
  finite exact factorization and order result, pending distinct rereview

Core B authority:
  minimal root-completeness model only; full calculus unverified

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

This round does not adopt either Fable core, establish a reductive common core,
prove a truth-linked target, validate a source, demonstrate causal execution,
or establish any metaphysical, personal, attribute, Speech, or revelational
conclusion.
