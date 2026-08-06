# PMR-007 Deep Round AA V3 — causal score guidance and intentional-purpose parity

```text
identity: PMR-007-CGIP-1
round: PMR-007-DEEP-AA
version: V3
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE_PENDING_DISTINCT_REREVIEW
historical_identity: NONE
repository_mutation: NONE
repair_relation: custody-complete successor to V2; substantive scope preserved
```

## 1. Frozen neutral SCM

Let all endogenous variables be Boolean and let `W` be an exogenous world
condition. The declared deterministic SCM is:

```text
S     = f_S(W)
Score = f_score(S)
A     = f_A(Score)
O     = f_O(W,A)
```

The neutral reduct contains the five variables, the four structural functions,
all observational tables under the declared exogenous values, and all
single-variable interventions on `W`, `S`, `Score`, `A`, and `O`.

The following are distinct carried coordinates rather than consequences of the
SCM:

```text
KeyAuthority
SemanticAnchor
WorldAdeq
NormAuthority
```

`Score` is an encoded evaluative/control state. It is not a norm, reason,
truth-linked state, or objectively fitting end merely because it controls
`A`.

## 2. CGIP-1A — internal causal-guidance characterization

Within the declared SCM:

\[
CausalGuidance(Score,A)
\iff
f_A(0)\neq f_A(1).
\]

Here `CausalGuidance` means that the intervention tables for
`do(Score=0)` and `do(Score=1)` assign different values to `A`.

**Proof.** Graph surgery replaces the equation for `Score` by the selected
constant. The equation for `A` then evaluates to `f_A(0)` or `f_A(1)`. They
differ exactly when `f_A` is nonconstant. ∎

This is a theorem about the frozen SCM. It is not evidence that the SCM is the
correct causal model of a runtime, organism, or world.

## 3. CGIP-1B — complete-neutral-reduct parity

Let the intended model class contain two expansions of the same complete
neutral reduct:

```text
M_imp:
  IntentionalUptake = false
  SelectionBecauseFitting = false
  FirstPersonOwnership = false
  Personality = false
  Wisdom = false

M_pers:
  one or more of those personal or intentional coordinates may be true
```

Assume these added coordinates do not alter the frozen neutral equations.
Then the expansions agree on every neutral observation and every neutral
single-variable intervention. Consequently, the complete frozen neutral reduct
plus the four carried guards does not entail intentional uptake, selection
because of fittingness, first-person ownership, personality, or Wisdom over
that intended class.

This is a logical nonentailment relative to the declared class. It does not
establish that the two expansions are metaphysically possible, equally
probable, or physically realizable.

## 4. CGIP-1C — observational fit does not certify the causal edge

Outside the frozen SCM, compare:

```text
Causal model:
  H = W
  Score = H
  A = Score

Hidden-common-cause model:
  H = W
  Score = H
  A = H
```

They have the same natural observational table for `(W,Score,A)`. Under
`H=0` and `do(Score=1)`, however, the causal model yields `A=1` while the
hidden-common-cause model yields `A=0`.

Thus observational agreement with the frozen table does not independently
certify the `Score -> A` causal edge.

## 5. Positive bridge specification

A positive intentional-purpose inference requires independently warranted
relations such as:

```text
UptakeAsReason(subject,Score)
FittingEnd(F)
SelectsBecause(subject,A,Score,F)
OwnsEpisode(subject,S,Score,A)
```

These are missing typed relations, not abbreviations for the neutral SCM.
Their conjunction can transparently specify a personal intentional episode,
but this round does not prove any of them.

## 6. Wisdom firewall

At minimum, the declared Wisdom target requires:

```text
eligible knowledge;
objectively fitting end;
intentional selection because of fittingness;
effective power;
nondefective coordination;
stable bearer and source conditions.
```

Internal score guidance supplies none of these simply by being causally
nonconstant. Even intentional purpose would not by itself establish the full
Wisdom package.

## 7. Countermodels and deletion controls

```text
AA-CM1 CAUSAL FALSE TARGET:
  f_A is nonconstant, but the semantic mapping is false or destructive.

AA-CM2 TRUE ANCHOR NO GUIDANCE:
  the semantic anchor is true, but f_A is constant.

AA-CM3 IMPERSONAL FULL-NEUTRAL GUIDANCE:
  all carried neutral guards and causal guidance hold while every personal,
  intentional, and Wisdom coordinate is false.

AA-CM4 PERSONAL TWIN:
  the same complete neutral reduct is expanded with personal coordinates.

AA-CM5 OBSERVATIONAL CAUSAL AMBIGUITY:
  the causal and hidden-common-cause models have the same natural table but
  different do(Score) behavior.

AA-CM6 SOURCE-CONDITIONAL WISDOM:
  Track-N source premises may predicate Wisdom of a source bearer; they do not
  become a neutral SCM consequence.
```

## 8. Candidate-G and proper-function effect

The SCM has genuine cross-domain dependence:

```text
S constrains Score;
Score interventions constrain A;
A and W constrain O.
```

It therefore exceeds a mere six-coordinate product record. Yet the impersonal
expansion realizes the same neutral dependency structure. Mechanism-specific
causal coupling alone does not break personal/impersonal parity.

The result also sharpens the proper-function boundary:

```text
causal efficacy
!= truth linkage
!= norm authority
!= objective fittingness
!= intentional selection because of fittingness
!= Wisdom.
```

## 9. Source, OSM, and implementation boundaries

The Sun et al. OSM source reports staged representational differentiation and a
model comparison in which CSCG best matched selected endpoint and trajectory
features among the tested models. Those observations do not establish
normative authority, intentional uptake, first-person ownership, personality,
or Wisdom.

Track-N source predication remains source-relative and requires its own
source-authentication, translation, referent, and applicability guards.

No daee, OSM, human, fiṭrī, or divine implementation is causally certified by
this finite SCM.

## 10. Ancestry, novelty, and nonclaims

```text
SCM intervention fact:
  standard

Deep M/O/P/Y relation:
  strengthened central parity application using an explicit intervention
  architecture

general mathematical novelty:
  0

historical identity:
  NONE
```

No Necessary Being, Creator, common bearer, personality, Wisdom, Speech,
source truth, world truth, integrated champion, or meniscus follows.
