# PMR-007 Deep Round X V2 — target-key authority and radical-correction anti-self-authorization

```text
identity: PMR-007-TKAA-1
round: PMR-007-DEEP-X
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
```

## 1. Exact central burden

Deep W's pullback aligns independently valid profile, warrant, and world-bridge
objects relative to one supplied target-contract key:

```text
k = (target identity, target version, recipient scope,
     analysis version, referent identity, semantic-contract digest).
```

The pullback does not authorize `k`. Candidate E's exact historical theorem
rules out only one authority source: complete token-autonomous authority for a
correction that defeats the current token basis in the same respect. This round
specializes that result to target contracts and tests the remaining authority
horns against the current integrated architecture.

## 2. Typed predicates

Let `C_s` be the closure of the token basis constituted by state `s`.

```text
CorrectionClaim_k(t,s):
  the system classifies t as correcting s under k.

ObjCorr_k(t,s):
  t is an objective correction of s under k.

Auth(X,k,ObjCorr_k(t,s)):
  X confers undefeated scoped authority on that objective correction.

Def(C_s,t,s):
  the correction defeats or renders insufficient the authority wholly
  constituted by C_s for the issue in question.
```

Define:

```text
TokenKeyAuth(k,t,s) :=
  exists X [Con_s(X) and X subset C_s
            and Auth(X,k,ObjCorr_k(t,s))].
```

For an authority source `Y`, define:

```text
IndependentSource_s(Y):
  Y's relevant authority is not wholly constituted by the defeated token
  closure C_s.

KeyAuthority(k,t,s) :=
  exists Y [IndependentSource_s(Y)
            and not Defeated(Y,t,s)
            and Auth(Y,k,ObjCorr_k(t,s))].
```

`KeyAuthority` is scoped authority for the correction. It does not entail that
`Y` is self-authenticating, truth-linked, teleological, personal, divine, or
world-complete.

Assume:

```text
CL:
  if X is wholly constituted by s, X subset C_s, and X authorizes q,
  then C_s authorizes q.

AA:
  Def(C_s,t,s) -> not Auth(C_s,k,ObjCorr_k(t,s)).
```

Define:

```text
Rad_k(t,s) :=
  ObjCorr_k(t,s)
  and Def(C_s,t,s)
  and no retained meta-rule in C_s authorizes ObjCorr_k(t,s).
```

Thus `Rad -> ObjCorr` by definition.

## 3. TKAA-1 — no token-autonomous radical target-key authority

For all `s,t,k`:

```text
AA and CL and Rad_k(t,s)
  -> not TokenKeyAuth(k,t,s).
```

**Proof.** If some token-constituted `X subset C_s` authorized the objective
correction, `CL` would lift that authority to `C_s`. `Rad` supplies
`Def(C_s,t,s)`, and `AA` denies that `C_s` authorizes the same correction.
Contradiction.

This is Candidate E's no-token-autonomous-radical-correction theorem with the
target-contract key made explicit. It is not a new general theorem origin.

## 4. TKAA-2 — repaired authority-source horn result

Use Candidate E's source roles:

```text
M — retained meta-standard in the current token basis;
T — trans-state or type-level standard;
H — holistic normative fixed point/global structure;
P — primitive normative fact or primitive authority;
E — denial, error theory, or relativization of objective radical correction.
```

Assume `PART`: every proposed authority source is classified by these roles.
The roles may overlap.

Then:

```text
ObjCorr_k(t,s) and Rad_k(t,s) and PART
  -> T or H or P.
```

`M` is excluded by radicality. `E` is an exit from accepting `ObjCorr`, so:

```text
E -> not ObjCorr_k(t,s).
```

The result identifies the remaining authority locations; it does not establish
that any one is true, sufficient, personal, purposive, or wise.

## 5. TKAA-3 — target-contract compatibility does not authorize its key

There are episodes with identical full key and identical valid compatible
profile/warrant/world-bridge objects but different authority status:

```text
ANCHORED:
  an undefeated independent source supplies scoped KeyAuthority;

SELF-INSTALLED:
  the current token state merely installs k and claims its own radical
  correction; AA/CL reject its token-autonomous authority.
```

Therefore:

```text
Compatible_k(a,b,c)
  does not entail
KeyAuthority(k,t,s).
```

The pullback universal property factors compatible objects through an already
supplied key. It does not establish the key's source, authority, or truth.

## 6. TKAA-4 — ordinary self-amendment boundary

A retained meta-standard can authorize an update that replaces every
first-order rule. Such a transition may satisfy `TokenKeyAuth` while failing
`Rad`. The theorem therefore does not prohibit governed self-amendment; it
prohibits reclassifying an update as radical in the same respect while retaining
complete token-autonomous authority.

## 7. TKAA-5 — two distinct impersonal controls

### 7.1 Order-only nonestablishment model

```text
underived modal order: true;
externally actual impersonal realizer: true;
full target-contract compatibility: true;
CorrectionClaim: true;
ObjCorr: not established;
KeyAuthority: false;
proper function: false;
personal ground: false.
```

Hence underived order, actuality, and compatibility do not establish objective
correction or target authority.

### 7.2 Primitive-norm impersonal model

```text
primitive P-source: true;
ObjCorr and scoped KeyAuthority: true;
truth-linked teleological proper function: not established;
Wisdom: false;
personal ground: false.
```

Even granting primitive objective norm authority does not entail a personal
designer, purposive Wisdom, one common bearer, or a source-conditioned divine
architecture. This is a live R5 stopping point.

## 8. Track-N source-relative authority

Within Track N, define an explicit premise:

```text
TrackNSourceAuthorityAccepted(Y,k)
```

which is eligible only after the frozen H12 source-authentication and H16
referent-identification guards. Conditional on that premise, `Y` may instantiate
a trans-state `T` authority source for a Track-N target.

This does not:

```text
authenticate the source by itself;
verify Arabic-primary wording;
prove world-target adequacy;
migrate into neutral Track T;
or establish a personal ground through the formal theorem.
```

## 9. Proper function and transcendental consequences

The round establishes a negative bridge boundary:

```text
contract compatibility
+ stable/path-independent correction structure
+ underived modal order
  does not entail
independently authoritative target
or truth-linked proper function.
```

A target's authority must still be supplied by a defended `T`, `H`, or `P`
account, or the objective correction claim is denied/relativized. None of those
accounts by itself supplies teleology, praiseworthy ends, Wisdom, personality,
or divine authorship.

## 10. Theorem-family and provenance disposition

```text
Candidate E:
  DIRECT_TARGET_KEY_SPECIALIZATION

AR4 anti-self-authorization:
  SHARED_HISTORICAL_FAMILY

Deep W:
  SUPPLIES_COMPATIBILITY_OBJECT_NOT_AUTHORITY

Deep V:
  TARGET_AUTHORITY_IS_AN_ADDITIONAL_COORDINATE

Deep N:
  EXACT_ADDITIVE_POTENTIAL_DOES_NOT_AUTHORIZE_THE_NORM

Deep S / Track N:
  SOURCE_RELATIVE_T_HORN_UNDER_H12_H16_AND_EXPLICIT_ACCEPTANCE

R5:
  ORDER_ONLY_AND_PRIMITIVE_NORM_IMPERSONAL_CONTROLS_SURVIVE

general mathematical novelty:
  ZERO
```

## 11. Central flywheel update

```text
Candidate E -> Deep W:
  compatibility must be supplemented by a non-token authority source for
  radical objective correction;

Deep W -> proper function:
  target-indexed transport still presupposes target authority;

transcendental ascent -> proper function:
  underived order does not generate normativity or teleology;

R5 -> ascent:
  primitive and impersonal norm sources preserve the current neutral package;

Track N -> proper function:
  can supply a source-relative authority premise only under explicit custody
  and acceptance guards;

proper function -> Candidate G:
  no common subject, purposive selection, or Wisdom follows from authority
  location alone.
```

## 12. Nonclaims and authority ceiling

```text
no proof that objective radical correction exists;
no proof that AA, CL, or PART is world-true;
no exclusive authority-source classification;
no defeat of constitutivism, coherentism, primitive normativity, or error theory;
no source authentication or neutral source migration;
no proper-function, Wisdom, personality, or divine-ground theorem;
no integrated champion;
no owner adoption;
no external independent review.
```
