# PMR-007 Deep Round AD V2 — registered reason-variable mediation and the subjecthood firewall

```text
identity: PMR-007-RSMF-1
round: PMR-007-DEEP-AD
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_bridge:
  semantic/reason-variable causal mediation
  -> subject-level selection because fittingness
```

## 1. Authority-separated finite setting

Let `C`, `R`, `P`, and `A` be finite nonempty sets of contexts, registered
reason-variable states, declared nuisance/proxy states, and actions.  Let

\[
H(r,c)\subseteq A
\]

be a supplied nonempty admissibility relation and

\[
\pi:C\times R\times P\to A
\]

be a deterministic policy.

The finite results use only the extensional structure.  A semantic application
requires independently warranted guards:

```text
SEM_VALID:
  R is correctly interpreted as the relevant reason/fittingness content;

TRUTH_LINK + TARGET_AUTHORITY + WORLD_ADEQUACY:
  the content and H relation are truth-linked, authorized, and world-applicable;

R_INTERVENTION_VALID:
  surgical interventions on R are coherent in the declared SCM and do not
  silently change the policy, world equations, or target;

P_NUISANCE:
  P is genuinely irrelevant to the target semantic/normative content once C,R
  are fixed, rather than an omitted evidence, authority, indexical, or source coordinate;

HIST_COMPLETE:
  C,R,P contain all history needed for the claimed memoryless decision;

POLICY_FIXED:
  pi and the remaining structural equations are held fixed across interventions;

REGISTRY_COMPLETE:
  the declared R and P classes are complete for the claimed scope.
```

## 2. RSMF-1A — exact nuisance-fibre factorization

Define

```text
P_INV(pi):
  for each fixed c,r, pi(c,r,p) is constant over all declared p.
```

Then `P_INV(pi)` holds exactly when there is a unique map

\[
g:C\times R\to A
\]

such that

\[
\pi(c,r,p)=g(c,r)
\]

for all `c,r,p`.

### Proof

`P_INV` is precisely constancy on each fibre of the projection
`(c,r,p) -> (c,r)`.  The common fibre value defines `g`; any such factorization
is fibre-constant; uniqueness is immediate. ∎

This is a direct application of the recurring fibre/factorization mechanism and
the present T366 reconstruction family.  It receives zero new general
mathematical novelty.

## 3. RSMF-1B — registered reason-variable mediation

Define:

```text
R_CONFORM(pi):
  pi(c,r,p) belongs to H(r,c) for every declared c,r,p.

R_CONTRAST(pi):
  if H(r,c) and H(r',c) are disjoint singleton sets, then all policy outputs
  under r differ from all outputs under r'.
```

Under `P_INV`, `R_CONFORM`, and the authority/application guards above, call the
policy **registered reason-variable mediated** at the declared scope when:

```text
1. surgical P interventions holding C,R fixed do not change the action;
2. surgical R interventions across a declared disjoint-singleton contrast
   change the action;
3. every selected action conforms to H.
```

In the frozen SCM

```text
C,R,P exogenous;
Act := pi(C,R,P),
```

with `POLICY_FIXED`, these are exact variable-level intervention statements.
They are stronger than observational correlation, endpoint agreement, or
trajectory similarity.

The theorem does **not** say every change of semantic content must change the
action.  Overlapping or non-singleton admissibility sets can license one action
under several reason states.

## 4. RSMF-1C — registered mediation does not entail subject-level because-of

Keep separate:

```text
R_MED_SYS:
  the complete registered system satisfies the intervention, nuisance-
  invariance, and conformity contract;

R_UPTAKE_SUBJ:
  one subject apprehends the represented content as a reason;

BECAUSE_FIT_SUBJ:
  that apprehended fittingness contributes to the subject's motivating
  explanation of the act;

OWN:
  the representation, evaluation, selection, and act are owned by that subject
  in the relevant episode;

PERSONALITY / WISDOM:
  further bearer-level and stable attribute predicates.
```

Let the complete neutral reduct include every registered variable, structural
equation, observation, intervention, authority bit, semantic contract, source
and version record, target key, and outcome table.  If the intended comparison
class contains two expansions of that same reduct—one with the subject-level
predicates false and one with them true—then no neutral-reduct sentence entails
`R_UPTAKE_SUBJ`, `BECAUSE_FIT_SUBJ`, `OWN`, personality, or Wisdom.

This is reduct-relative logical underdetermination.  It does not establish the
actuality, physical realizability, causal completeness, or equal probability of
the impersonal expansion.

## 5. Positive subject-level bridge specification

A personal reason-attribution requires independent evidence for at least:

```text
SUBJECT;
CONTENT_ACCESS;
SEMANTIC_UPTAKE;
RECOGNIZES_AS_REASON;
MOTIVATING_CAUSAL_ROLE;
FIRST_PERSON_OWNERSHIP;
COMMON_BEARER;
DEFEATER_CLOSURE;
STABLE_COUNTERFACTUAL_INTEGRATION;
and, for Wisdom, independently fitting ends and proportioned means.
```

`R_MED_SYS` can serve as one operational constraint on a candidate personal
model.  It is neither necessary under every theory of agency nor sufficient for
subjective reason recognition.

## 6. Countermodels and application controls

```text
AD-CM1 PROXY SHORTCUT:
  observational reason/action correlation is carried entirely by P; P_INV fails.

AD-CM2 MISIDENTIFIED R:
  factorization and interventions hold, but SEM_VALID or TRUTH_LINK fails.

AD-CM3 EVIDENCE-BEARING P:
  P contains real source, authority, indexical, or world information;
  P_NUISANCE fails, so invariance would erase relevant evidence.

AD-CM4 IMPERSONAL SEMANTIC TRANSDUCER:
  all system-level guards and interventions hold; subject predicates fail.

AD-CM5 ACCIDENTAL PERSONAL CONFORMITY:
  a subject selects the admissible action for an unrelated motive;
  R_MED_SYS may hold while BECAUSE_FIT_SUBJ fails.

AD-CM6 DISTRIBUTED REASON PIPELINE:
  semantic interpretation, evaluation, selection, and execution are distributed;
  no common subject owns the episode.

AD-CM7 HIDDEN CONFOUNDER OR MODEL CHANGE:
  the apparent R intervention also changes hidden world/policy equations;
  R_INTERVENTION_VALID or POLICY_FIXED fails.

AD-CM8 HISTORY COLLISION:
  identical current C,R,P states require different actions because hidden
  history differs; HIST_COMPLETE fails.

AD-CM9 PARTIAL REGISTRY:
  the policy passes registered tests but fails on an omitted reason or proxy;
  REGISTRY_COMPLETE fails.

AD-CM10 IMPLEMENTATION NONTRANSFER:
  an OSM, daee, PRH, biological, or agentic representation resembles R or P but
  no validated semantic/intervention correspondence is supplied.

AD-CM11 TRACK-N SOURCE EXPANSION:
  a source-expanded model predicates personal agency or Wisdom; this changes
  Track N only and does not become a neutral consequence of R_MED_SYS.
```

## 7. Cross-lane contribution

```text
Deep Y -> AD:
  semantic-anchor and truth-linkage guards;

Deep AA -> AD:
  intervention-sensitive neutral causal architecture and personal-realizer parity;

Deep AB -> AD:
  fittingness conformity and profile-input sensitivity;

Deep AD -> Candidate B / implementation:
  exact testable distinction between reason-variable interventions and nuisance
  proxy changes, subject to correspondence validation;

Deep AD -> Candidate C:
  even a stronger semantic-intervention profile leaves subjecthood and Wisdom
  outside neutral entailment.
```

The Sun et al. OSM source, PRH alignment results, and current implementation
crosswalks may constrain candidate representations, but they do not themselves
supply `SEM_VALID`, causal identification, or subject-level uptake.

## 8. Ancestry and novelty ceiling

```text
T366 / fibre-factorization family:
  DIRECT APPLICATION

Deep Y, Deep AA, Deep AB:
  COMPOSITIONAL CENTRAL-BRIDGE SYNTHESIS

Candidate G:
  PERSONAL/IMPERSONAL PARITY AND CARRIER-BOXING CONTROL

general mathematical novelty:
  0

historical identity:
  NONE
```

The substantive contribution is the operational bridge map, not a new abstract
factorization theorem.

## 9. Scope and nonclaims

The result is finite, deterministic, static, memoryless relative to the declared
state, and SCM-relative.  It establishes no actual semantic anchor, observational
causal identification, human or biological subjecthood, daee/OSM/PRH compliance,
first-person ownership, personality, Wisdom, Necessary Being, Creator, source
truth, divine attribute, integrated champion, or meniscus.
