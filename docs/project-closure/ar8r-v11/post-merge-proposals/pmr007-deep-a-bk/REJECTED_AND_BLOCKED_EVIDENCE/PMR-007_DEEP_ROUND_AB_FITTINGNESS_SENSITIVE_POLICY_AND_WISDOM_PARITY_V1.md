# PMR-007 Deep Round AB V1 — fittingness-sensitive policy and Wisdom parity

```text
identity: PMR-007-FSPW-1
round: PMR-007-DEEP-AB
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_bridge:
  objective fittingness + counterfactual policy conformity + causal guidance
  -> selection because fitting / intentional subject / Wisdom
```

## 1. Typed finite setting

Let:

```text
C      finite contexts;
A      finite actions;
Theta  finite fittingness-profile states;
Best(theta,c) subseteq A, nonempty;
I      information supplied to the selector;
pi     deterministic policy.
```

`Best` is a carried objective-fitness coordinate. This round does not establish
its truth, authority, or world adequacy.

A profile-aware policy has type:

\[
\pi:C\times\Theta\to A.
\]

A profile-blind policy has type:

\[
\pi_0:C\to A.
\]

Define:

```text
EXT_FIT(pi):
  for every theta,c, pi(c,theta) is in Best(theta,c).

PROFILE_RESP(pi):
  whenever theta and theta' give disjoint singleton best sets at c,
  pi(c,theta) differs from pi(c,theta').

STABLE_EXT_FIT(pi):
  EXT_FIT holds across every registered theta in the declared class.
```

These are extensional and counterfactual policy properties. They are not yet
intentional or first-person predicates.

## 2. FSPW-1A — exact finite existence boundary

A profile-aware deterministic policy satisfying `EXT_FIT` exists exactly when
`Best(theta,c)` is nonempty for every `(theta,c)`.

A profile-blind deterministic policy satisfying every registered profile exists
exactly when:

\[
\bigcap_{\theta\in\Theta} Best(\theta,c)\neq\varnothing
\quad\text{for every }c\in C.
\]

### Proof

For the aware policy, choose one member of each nonempty finite best set.
Conversely, an empty best set makes the requirement impossible.

For the blind policy, the selected action at `c` must lie in every best set,
so the intersection condition is necessary. Choosing one action from each
nonempty intersection is sufficient. ∎

## 3. FSPW-1B — counterfactual fittingness sensitivity

If `EXT_FIT(pi)` holds and two profiles have distinct singleton best sets at the
same context, then `PROFILE_RESP(pi)` holds automatically. Thus a complete
profile-aware argmax policy is causally responsive to changes in the supplied
fittingness profile at every such contrast.

This strengthens Deep AA's generic `Score -> A` guidance: the changed control
coordinate is now typed as a carried fittingness profile and the selected action
is always extensionally best in the registered class.

## 4. FSPW-1C — impersonal implementation and personal parity

Every finite `EXT_FIT` policy has an impersonal lookup-table or argmax
implementation. Expand the same complete policy and intervention table in two
ways:

```text
M_imp:
  IntentionalUptake = false
  SelectionBecauseFitting = false
  FirstPersonOwnership = false
  Personality = false
  Wisdom = false

M_pers:
  those coordinates may be true
```

The expansions agree on:

```text
all Best relations;
all profile/context inputs;
all selected actions;
all profile interventions;
all outcome tables supplied downstream;
all carried target, semantic, world, and norm guards.
```

Therefore complete extensional fittingness, registered counterfactual
responsiveness, and internal causal guidance do not entail intentional
selection because of fittingness, first-person ownership, personality, or
Wisdom in an intended class containing both expansions.

## 5. Positive personal-Wisdom bridge specification

The stronger target requires independently warranted relations:

```text
ApprehendsAsFitting(subject,theta,c);
SelectsBecauseFitting(subject,a,theta,c);
OwnsEpisode(subject,theta,c,a);
EligibleKnowledge(subject,theta,c);
EffectivePower(subject,a);
NondefectiveCoordination(subject);
StableBearerAndSource(subject).
```

This is a bridge specification. `EXT_FIT` and `PROFILE_RESP` do not prove these
relations.

## 6. Countermodels

```text
AB-CM1 IMPERSONAL ARGMAX:
  all extensional and counterfactual policy conditions hold;
  every personal and Wisdom coordinate fails.

AB-CM2 FALSE OR UNAUTHORIZED FITNESS:
  the policy perfectly tracks Best, but Best is not independently true,
  authoritative, or objectively fitting.

AB-CM3 PROFILE-BLIND COLLISION:
  two registered profiles require different singleton best actions;
  no profile-blind policy succeeds.

AB-CM4 ACCIDENTAL LOOKUP:
  a fixed lookup happens to match every registered profile but lacks the
  declared sensitivity outside the frozen registry.

AB-CM5 DISTRIBUTED FITTINGNESS PIPELINE:
  distinct bearers encode fitness, select, and execute; no one subject owns
  the episode.

AB-CM6 ONE-EPISODE FIT:
  one extensionally fitting act occurs; stable Wisdom fails.

AB-CM7 SOURCE-CONDITIONAL WISDOM:
  Track-N source predication may supply Wisdom in a source-expanded model;
  it is not a neutral consequence of the policy table.
```

## 7. Source and proper-function relation

The translated Asfahani commentary distinguishes praiseworthy from blameworthy
volition and speech, and describes benefit and praiseworthy ends as signs of
mercy and Wisdom. This supports a Track-N distinction between bare causal
selection and praiseworthy exercise.

It does not independently establish the neutral truth of `Best`, the existence
of a personal subject, or the world-level Wisdom bridge.

Deep K's `WD/EW/SW` contracts remain controlling. Deep AB supplies a stronger
extensional and counterfactual policy condition but not `W_F`, `OWN`, or the
full stable-Wisdom package.

## 8. Ancestry and novelty

```text
finite choice and intersection characterization:
  elementary

relation to Deep K and Deep AA:
  strengthened central application

relation to Round 18 selector family:
  shared information/fibre mechanism only

general mathematical novelty:
  0

historical identity:
  NONE
```

## 9. Nonclaims

No actual objective fittingness relation, intentional subject, personality,
Wisdom, source truth, world truth, Necessary Being, Creator, common bearer,
integrated champion, or meniscus is established.
