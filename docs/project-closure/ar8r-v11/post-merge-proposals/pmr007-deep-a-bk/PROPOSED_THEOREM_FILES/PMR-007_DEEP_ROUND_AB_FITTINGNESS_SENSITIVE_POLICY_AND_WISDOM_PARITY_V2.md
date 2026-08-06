# PMR-007 Deep Round AB V2 — fittingness-sensitive policy, because-of selection, and Wisdom parity

```text
identity: PMR-007-FSPW-1
round: PMR-007-DEEP-AB
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_bridge:
  registered fittingness conformity + profile-sensitive control
  -> selection because fitting -> intentional subject -> stable Wisdom
```

## 1. Authority-separated finite setting

Let `C`, `A`, and `Theta` be finite nonempty sets of contexts, actions, and
registered fittingness-profile indices.  Let

\[
H(\theta,c)\subseteq A
\]

be a supplied nonempty **certificate-admissibility/fittingness relation**.  The
formal theorems below use only the extension of `H`.  They do not establish any
of the following independently required coordinates:

```text
FIT_AUTH:   the target key and fittingness rule are authorized;
FIT_TRUTH:  the rule is truth-linked or objectively correct;
FIT_WORLD:  it applies to the actual target world;
FIT_SRC:    its source, version, and provenance are valid;
FIT_SCOPE:  the registered profile class is complete for the claimed scope;
FIT_HIST:   current observation contains the history needed for policy choice.
```

A profile-aware policy has type

\[
\pi:C\times\Theta\to A,
\]

whereas a profile-blind policy has type

\[
\pi_0:C\to A.
\]

Define:

```text
EXT_H(pi):
  for every theta,c, pi(c,theta) belongs to H(theta,c).

BLIND_H(pi0):
  for every theta,c, pi0(c) belongs to H(theta,c).

PROFILE_RESP(pi):
  if H(theta,c) and H(theta',c) are distinct singleton sets,
  then pi(c,theta) differs from pi(c,theta').
```

These are extensional policy properties.  `H` may be interpreted as objective
fittingness only when the corresponding authority, truth, world, source, and
scope guards are independently warranted.

## 2. FSPW-1A — exact finite selector characterization

A deterministic profile-aware policy satisfying `EXT_H` exists exactly when
all fibres `H(theta,c)` are nonempty.

A deterministic profile-blind policy satisfying `BLIND_H` exists exactly when

\[
\bigcap_{\theta\in\Theta}H(\theta,c)\neq\varnothing
\quad\text{for every }c\in C.
\]

### Proof

For the aware policy, finite choice selects one member from each nonempty
fibre.  If one fibre is empty, no policy can satisfy it.

For the blind policy, the one action selected at `c` must belong to every
registered fibre, so the intersection condition is necessary.  Choosing one
member from each nonempty intersection is sufficient. ∎

## 3. FSPW-1B — functional and frozen-SCM sensitivity

If `EXT_H(pi)` holds and two registered profiles at one context have distinct
singleton admissibility sets, then `PROFILE_RESP(pi)` follows: both policy
values are forced and are different.

This yields a limited causal result only in the frozen deterministic SCM

```text
C      exogenous or held fixed;
Theta  exogenous manipulable profile input;
Act := pi(C,Theta);
```

with the policy equation and all other structural equations held fixed.  In
that SCM,

\[
do(\Theta=\theta)\neq do(\Theta=\theta')
\]

at the selected action coordinate whenever the two singleton fibres differ.
This is **profile-input intervention sensitivity in the declared SCM**.  It is
not a claim about hidden history, a changing policy, a different source model,
or causal structure outside the frozen SCM.

## 4. FSPW-1C — personal-realizer parity

Let the complete neutral reduct contain:

```text
C, A, Theta, H, pi;
all registered profile interventions and selected actions;
FIT_AUTH, FIT_TRUTH, FIT_WORLD, FIT_SRC, FIT_SCOPE, FIT_HIST;
any declared downstream outcome table.
```

Suppose the intended model class contains two expansions of the same reduct:

```text
M_imp:
  ApprehendsAsFitting = false
  SelectsBecauseFitting = false
  FirstPersonOwnership = false
  Personality = false
  Wisdom = false

M_pers:
  one or more of those predicates are true
```

and the added predicates do not alter the neutral structural equations.  Then
no sentence in the neutral reduct distinguishes the two expansions.  Hence the
full registered policy, including exact conformity and the frozen profile
interventions, does not entail:

```text
semantic uptake of the profile as a reason;
selection because of its fittingness;
first-person episode ownership;
personality;
or Wisdom.
```

This is a reduct-relative logical underdetermination result.  It does not prove
that an impersonal realization is metaphysically actual, physically realizable,
or equally probable.

## 5. Positive because-of and Wisdom bridge specification

A stronger personal-Wisdom model must independently supply at least:

```text
SUBJ:    one eligible subject/bearer;
UPTAKE:  the subject apprehends the fittingness content as a reason;
BFIT:    the fittingness of the end is part of the selection explanation;
KNOW:    eligible knowledge of end, means, and circumstances;
MEANS:   means are proportioned to the fitting end;
POWER:   practical efficacy or capacity;
OWN:     representation, evaluation, selection, and execution are owned by
         the same subject in the relevant episode;
STAB:    the reason-responsive pattern is stable over the declared relevant
         counterfactual class;
NDEF:    no defect or rival explanation defeats the attribution.
```

The contract can support a conditional attribution if its guards are
independently warranted.  `EXT_H` and profile-input intervention sensitivity do
not prove any of `SUBJ`, `UPTAKE`, `BFIT`, `OWN`, `STAB`, or `NDEF`.

## 6. Countermodels and strict controls

```text
AB-CM1 IMPERSONAL ARGMAX:
  all neutral guards, EXT_H, and frozen profile interventions hold;
  personal and Wisdom coordinates fail.

AB-CM2 FALSE OR UNAUTHORIZED H:
  the controller tracks H perfectly while FIT_AUTH or FIT_TRUTH fails.

AB-CM3 PROFILE-BLIND COLLISION:
  one context has registered fibres with empty total intersection;
  no profile-blind policy succeeds.

AB-CM4 REGISTRY-LIMITED LOOKUP:
  the lookup succeeds on every registered profile but fails after an
  unregistered profile or version is introduced; FIT_SCOPE fails.

AB-CM5 HISTORY COLLISION:
  two episodes share the current (c,theta) pair but require different actions
  because hidden history differs; FIT_HIST fails.

AB-CM6 DISTRIBUTED PIPELINE:
  source custody, fittingness evaluation, selection, and execution occur in
  different bearers; no one intentional subject owns the episode.

AB-CM7 ONE-EPISODE CONFORMITY:
  one action conforms to H but STAB and standing Wisdom fail.

AB-CM8 SOURCE-CONDITIONAL WISDOM:
  a Track-N source-expanded model predicates Wisdom; this is source-relative
  content, not a neutral consequence of the policy reduct.

AB-CM9 HIDDEN MODEL CHANGE:
  action changes when the profile label changes only because the policy or
  source model also changes; the frozen-SCM causal claim is inapplicable.
```

## 7. Source, proper-function, and unification adjudication

The supplied Asfahani English translation distinguishes praiseworthy from
blameworthy speech and volition and places the Wise among names whose meanings
are praiseworthy.  It also treats beneficial and praiseworthy ends as source-
relative evidence in the attribute discussion.  The exact local source is:

```text
A-Commentary-on-the-Creed-of-Asfahani-v2.3(1).md
SHA-256:
932abd7e2d7b3702d5d6d77d2a4a95ecfb3a9ccbcfbbce7ae750b2bcf55bef7c

authority:
TRANSLATED_PRIMARY_TEXT_ACCESS
NOT ARABIC_PRIMARY_VERIFICATION BY THIS PROJECT
```

This changes the admissible Track-N model class when the source and its
applicability are accepted.  It does not establish `FIT_TRUTH`, a neutral
personal subject, or a school-neutral Wisdom entailment.

Deep K remains the controlling role decomposition: proper function, reliable
representation, objective fittingness, because-of selection, common-bearer
ownership, execution, and stable Wisdom are distinct.  Deep AB strengthens the
**extensional conformity and profile-input sensitivity** coordinates but does
not close the because-of, subject, or stable-Wisdom bridges.

Candidate G also remains controlling.  A single data structure containing `H`,
`pi`, authority bits, and personal labels is carrier-boxing unless it introduces
independently justified cross-profile restrictions or derivations.  Since the
same complete neutral reduct admits personal and impersonal expansions, Deep AB
does not break rival parity.

## 8. Ancestry and novelty ceiling

```text
finite selection/intersection theorem:
  elementary finite choice/constraint fact

Round 18 relation:
  shared selector/information mechanism; different target and authority burden

Deep K relation:
  strict central application and stronger extensional policy guard

Deep AA relation:
  specialization of causal-guidance/personal-realizer parity to a registered
  fittingness profile

Candidate G relation:
  carrier-boxing and derivational-parity control

general mathematical novelty:
  0

historical identity:
  NONE
```

The central contribution is negative but load-bearing: even a complete,
authorized, truth-linked, world-adequate, profile-sensitive controller does not
select a personal or Wise realizer unless an intentional because-of/ownership
bridge is independently supplied.

## 9. Scope and nonclaims

The result is limited to finite declared classes, deterministic policies, fixed
policy equations, exact registered admissibility data, and the stated frozen
intervention semantics.  It does not establish variable-length communication,
randomized or interactive control, partial observation, dynamic membership,
source truth, objective fittingness, human or fiṭrī restoration, a personal
ground, Necessary Being, Creatorhood, divine Wisdom, integrated champion, or
meniscus.
