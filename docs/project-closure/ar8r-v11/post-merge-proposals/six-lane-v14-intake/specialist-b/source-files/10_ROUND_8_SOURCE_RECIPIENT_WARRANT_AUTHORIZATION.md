# Specialist B round 8 — source truth, authority, recipient warrant, and execution

```text
round: SPECIALIST_B_ROUND_8
packet-local candidate: SB-C8
packet-local rivals:
  SB-R37 SOURCE_CUSTODY_WITHOUT_WORLD_TRUTH
  SB-R38 AUTHORITY_TRUTH_SPLIT
  SB-R39 RECIPIENT_INDEX_SHIFT
  SB-R40 FALSE_MULTIPLICITY_EVIDENCE
  SB-R41 WARRANT_WITHOUT_EXECUTION
status: FROZEN NONAUTHORITATIVE RESEARCH CANDIDATE
repository authority: 9b80f2dfdf73a768ccad6a6ea2f2998c70ebdcf3
GitHub mutation: NONE
```

## 1. Frozen problem

The source-ascent owners correctly separate source text, interpretation, formal
predicate, world truth, bearer applicability, authority, revelation, and
recipient warrant. The remaining risk is to compress these into a single
boolean such as `SOURCE_ACCEPTED` or `AUTHORIZED`, then let that hidden scalar
perform several logically different jobs.

This round freezes a recipient-indexed certificate and its ceiling. It does not
choose a theory of warrant and does not treat source authority as neutral
experimental semantics.

## 2. Typed source-recipient coordinates

Let:

```text
Source, Version, Locus, Language, Token, Proposition,
World, Bearer, Authority, Recipient, Time, EvidenceRoute, Action : Type
```

Keep separate predicates for:

```text
ExactBytes(s,v,l)
VersionCustody(s,v,t)
CorrectAttribution(s,a)
TranslationAdequate(s,v,l,p)
MorphologyAdequate(s,v,l,p)
SyntaxAdequate(s,v,l,p)
OccurrenceMeaningAdequate(s,v,l,p)
FormalizationFaithful(p,phi)
WorldTrue(w,phi)
RefersTo(s,v,l,w,b)
ApplicableTo(w,phi,b)
AuthorityWithin(a,p,scope)
Revealed(s,v,l)
RecipientAccess(r,s,v,l,t)
RecipientCompetence(r,language,domain,t)
RouteReliable(route,r,s,v,l,t)
EvidenceIndependent(route)
DefeaterControlled(r,p,t)
TargetRelevant(p,q)
RecipientBelieves(r,p,t)
RecipientAssents(r,p,t)
Executes(r,p,action,t)
```

`Revealed`, `AuthorityWithin`, and `WorldTrue` are distinct coordinates. An
authority may be scoped, a proposition may be true without being authoritative,
and a recipient may lack warrant despite source truth.

## 3. Candidate SB-C8 — recipient-warrant readiness certificate

Define an audit object rather than an unconditional epistemic theorem:

```text
SourceWorldReady(r,p,w,b,t) :=
  exact source/version/locus custody
  and adequate translation/morphology/syntax/occurrence meaning
  and faithful formalization
  and world truth
  and correct referent
  and bearer applicability
  and authority within the claimed scope, when authority is part of the claim
  and recipient access
  and recipient competence
  and route reliability
  and declared independence/nonincest of evidence
  and defeater control
  and target relevance.
```

Then:

```text
SourceWorldReady
  not=> RecipientBelieves
  not=> RecipientAssents
  not=> Executes
  not=> warrant under every epistemology.
```

A chosen epistemic account may add an explicit bridge:

```text
WARRANT_RULE(account):
  SourceWorldReady(account-specific fields) -> RecipientWarrant
```

The resulting warrant claim is conditional on that account. Plantingian proper
function, reliabilism, evidentialism, testimony theories, and source-relative
fiṭrah accounts need not supply the same bridge.

## 4. Index-shift firewall

Every recipient conclusion must retain:

```text
recipient;
time;
source version and locus;
translation/interpretation state;
evidence route and provenance;
known defeaters;
authority scope;
target proposition;
world and bearer coordinates.
```

The following shifts are invalid without new premises:

```text
some recipient is warranted -> every recipient is warranted;
recipient r was warranted at t0 -> r is warranted at t1;
source authority over P -> authority over Q;
true proposition P -> source S is authoritative;
source S is revealed -> every translation of S is exact;
recipient is warranted -> recipient assents or executes;
source says bearer b has F -> b actually has F;
source/world bridge for F -> source/world bridge for personality, Wisdom, or
revelational identity.
```

## 5. Countermodels and deletion tests

### SB-CM64 — exact source, false world claim

Bytes, version, translation, and formalization are exact, but the proposition is
false in the candidate world. Textual custody does not establish world truth.

### SB-CM65 — true proposition, wrong referent

The formal predicate is true of `b1`, while the source expression refers to
`b2`. Truth somewhere does not establish bearer applicability.

### SB-CM66 — authority without truth

A genuine authority speaks within a social role but makes a false empirical
claim. Authority status alone does not make every proposition true.

### SB-CM67 — truth without authority

An unauthorised speaker states a true proposition. Truth does not confer Name,
legal, revelational, or source authority.

### SB-CM68 — revealed source, mistranslated occurrence

Revelation is granted conditionally, but the recipient uses a translation that
reverses scope or attachment. Revelation of the source does not validate the
recipient’s occurrence meaning.

### SB-CM69 — accurate package, inaccessible recipient

All source/world predicates hold, but recipient `r` never receives the evidence.
World truth and authority do not create recipient warrant by causal magic.

### SB-CM70 — access without competence

The recipient possesses the text but cannot interpret its language, technical
terms, or inferential role. Access is not understanding.

### SB-CM71 — reliable route with undefeated defeater

The route is ordinarily reliable, but the recipient has a specific undefeated
reason to distrust this token or attribution. Generic reliability does not
remove recipient-indexed defeat.

### SB-CM72 — duplicate dependent testimony

Several reports trace to one unverified source. Apparent multiplicity does not
supply independent confirmation or stronger warrant.

### SB-CM73 — warranted belief without assent

The recipient has sufficient evidence but suspends or refuses assent. Warrant
readiness is not the psychological occurrence of belief.

### SB-CM74 — assent without execution

The recipient sincerely assents but does not recite, disclose, obey, or perform
the relevant act. Belief and execution remain distinct.

### SB-CM75 — recipient/time drift

A recipient is warranted at `t0`; a version change or new defeating evidence at
`t1` alters the status. Warrant is not automatically transportable across time.

### SB-CM76 — authority-scope expansion

A source is authoritative for a narrow transmitted wording. That status is
silently expanded to settle a property ontology or neutral metaphysical bridge.
The target relevance and scope guards fail.

## 6. Proper-function effects

Current reliable output, social success, declared norm sensitivity, and runtime
closure do not by themselves establish that a recipient’s cognition functions
properly under any selected-effect, design, Plantingian, or fiṭrah account.
Conversely, an independently defended proper-function account does not remove
translation, referent, truth, authority-scope, or defeater burdens.

The certificate therefore carries a typed `WARRANT_RULE(account)` rather than
silently treating “proper function” as one uniform predicate.

## 7. Source, Speech, and Name effects

```text
positive qualification != authorized Name;
source wording != occurrence meaning;
occurrence meaning != world truth;
world truth != bearer applicability;
bearer applicability != recipient warrant;
recipient warrant != actual Speech occurrence;
actual Speech occurrence != one authenticated revealed wording;
revealed wording != every recitation or execution token.
```

The Aṣfahāniyyah p. 13 distinction between true positive meanings and Beautiful
Name authorization is an exact source-relative example of this noncollapse. It
is not a neutral proof of the complete certificate.

## 8. Classification

```text
formal status:
  definition of an audit certificate and index discipline
mathematical theorem:
  NONE beyond elementary conjunction projections and existing fibre/source-
  interpretation families
new repository-level object:
  permissible SourceRecipientWarrantReadiness record
source authority:
  conditional and scope-indexed
world truth:
  independent bridge
recipient warrant:
  account-relative and recipient-indexed
```

## 9. Flywheel effect

```text
source-formal-world node:
  extended to recipient/time/route/defeater indices.

authority node:
  blocked from acting as a neutral world-truth or experiment-semantic scalar.

proper-function node:
  account parameter made explicit.

Speech/Name node:
  authorization, wording, occurrence, recitation, warrant, and execution remain
  distinct.

transcendental ascent:
  no improvement toward Necessary Being, personality, Wisdom, Creatorhood, or
  revelation from the certificate alone.
```

## 10. Exact next atomic action

Ask Specialist A to type the readiness record and index-shift countermodels, and
ask Deep Research 21 for exact primary-source loci on testimony, source
attribution, Name authorization, Speech wording/meaning, and recipient duties
without treating one school’s epistemology as neutral.
