# PMR-007 Deep Round AS — proper-function intervention basis and norm-source diagnosability V2

```text
campaign: AR8R_POST_MERGE_MENISCUS_PROGRAM_V1
wave: PMR-007
round: Deep AS
canonical post-merge identity: PMR-007-PFIT-1
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
repository authority inspected: 4c3dc103e8c753690fa5de560ab82157392ced4c
```

## 1. Central burden

The proper-function program now distinguishes frequency, causal role, organizational role, selected effect, design, learned target, success surface, truth linkage, teleology, Plantingian proper function, and fiṭrah-oriented function. Deep AQ relocates architecture discrimination to source exclusion, predictive/interventional surplus, or a defended prior. Deep AS asks for the exact finite intervention burden needed to discriminate a **declared set of norm-source accounts**.

This is an experiment-design and impossibility result. It identifies response models, not which account is true.

## 2. Frozen deterministic episode

Let:

- `H` be a finite declared account set;
- `I` be a finite set of feasible and authorized interventions;
- `O` be a finite set of complete account-relative response/certificate objects;
- `r:H×I→O` be a deterministic response map;
- the hidden account, target contract, source/version contract, environment classification, and response semantics remain fixed during the episode.

A surface action is not automatically a complete response object. If `π:O→A_surface` forgets source, target, authority, reason, version, provenance, or warrant coordinates, action-level identification is licensed only when the target account label factors through `π∘r`.

For `h≠h'`, define

\[
D(h,h')=\{i\in I:r(h,i)\ne r(h',i)\}.
\]

## 3. PFIT-1A — exact nonadaptive basis

A set `J⊆I` identifies every account exactly iff

\[
\forall h\ne h',\quad J\cap D(h,h')\ne\varnothing.
\]

Equivalently, the signature map

\[
h\longmapsto (r(h,i))_{i\in J}
\]

is injective. Therefore

\[
\delta_{NA}(H,I,r)
=
\min\{|J|:J\text{ hits every pairwise disagreement set}\}.
\]

If some pair has `D(h,h')=∅`, no intervention in the declared episode distinguishes that pair and `delta_NA` is undefined/infinite.

### Proof

Missing one disagreement set leaves two identical selected signatures. Hitting every pair makes every two signatures differ. This is the finite Test Cover/hitting-set equivalence.

## 4. PFIT-1B — exact adaptive decision-tree recurrence

For a current candidate set `S⊆H` and remaining interventions `J⊆I`, define

\[
V(S,J)=0\quad\text{when }|S|\le1.
\]

For `|S|>1`,

\[
V(S,J)
=
1+
\min_{i\in J\;:\;i\text{ splits }S}
\max_{o\in O}
V(S_{i,o},J\setminus\{i\}),
\]

where

\[
S_{i,o}=\{h\in S:r(h,i)=o\}.
\]

If no remaining intervention splits a non-singleton `S`, set `V(S,J)=∞`.

Then `delta_AD=V(H,I)` is exactly the minimum worst-case depth of a deterministic zero-error adaptive decision tree.

### Proof

Every strategy must choose one remaining intervention at the current node. The response determines a fibre `S_{i,o}` and the adversary may place the true account in the deepest nonempty branch. This gives the lower bound. Choosing a minimizing intervention and recursively optimal subtrees gives the upper bound. Repeating an already queried intervention is redundant because the static deterministic response is already known; the explicit remaining-set recurrence prevents circular reuse.

## 5. PFIT-1C — adaptivity can strictly reduce the test burden

Every nonadaptive basis can be queried sequentially, so

\[
\delta_{AD}\le\delta_{NA}
\]

whenever exact identification is possible.

For the response matrix

```text
       i0 i1 i2
h0      0  0  0
h1      0  0  1
h2      0  1  0
h3      1  0  1
```

all three columns are required nonadaptively:

```text
omit i0: h1 and h3 collide;
omit i1: h0 and h2 collide;
omit i2: h0 and h1 collide.
```

Yet an adaptive depth-two tree exists:

```text
query i2 first;
response 0 leaves {h0,h2}, separated by i1;
response 1 leaves {h1,h3}, separated by i0.
```

Thus `delta_NA=3` and `delta_AD=2`.

## 6. PFIT-1D — intervention deletion and enlargement

Adding a feasible intervention cannot increase either optimal burden. Deleting an intervention cannot decrease it. This monotonicity concerns the frozen response model; adding an intervention that changes the account, target, or semantic contract is not mere enlargement of `I`.

## 7. Proper-function horn discrimination

### Target-relative versus truth-linked

If every admissible episode keeps installed-target success aligned with independently correct truth/fittingness, the accounts may have identical response rows. No declared test identifies their norm source.

A separating intervention must create an independently certified target/truth divergence. Harmful corrigibility is the control: perfect correction to a destructive or false target while the truth-linked account rejects it. The truth coordinate must be independently warranted rather than encoded by the experimenter as the desired label.

### Design versus truth-linked

A malicious or incompetent design plan can preserve designed function while defeating truth direction. Distinguishing the accounts requires independently typed design intention and truth outcome.

### Selected effect versus truth-linked

A deceptive trait may be selected because deception succeeds. Distinguishing selected effect from truth-linked function requires actual selection-history evidence and a truth-divergence case.

### Plantinga-style versus generic design

The stronger account adds truth aim, proper operation, suitable environment, and favorable objective truth probability. An intervention must vary at least one of those coordinates while preserving generic design status; output success alone cannot do so.

### Fiṭrah/source-relative account

A Track-N fiṭrah account additionally requires source authentication, correct reconstruction, version, applicability, health/impairment classification, and the declared reminder/restoration relation. These coordinates may distinguish a source-relative model but do not migrate into a neutral theorem without independent bridges.

## 8. Countermodels and experiment defects

```text
AS-CM-ALIGNED-REGIME:
all account-fixing coordinates co-vary on every feasible intervention;
identification is impossible.

AS-CM-HARMFUL-CORRIGIBILITY:
target-relative success with truth-linked failure.

AS-CM-MALICIOUS-DESIGN:
design function with false or vicious target.

AS-CM-SELECTED-DECEPTION:
selected-effect function with systematic falsehood.

AS-CM-SOURCE-VERSION:
same operational profile, different authenticated source/version applicability.

AS-CM-TARGET-LEAKAGE:
response or intervention label encodes the account verdict.

AS-CM-SURFACE-PROJECTION:
accounts choose the same action but carry different warrant/source certificates.

AS-CM-STATE-CHANGE:
the intervention rewrites the governing account; static PFIT-1 no longer applies.
```

## 9. Candidate A/B/C and flywheel effects

### Candidate A

The result provides exact finite local/collective diagnosis quantities for account hypotheses, but only after provenance-valid complete response objects are available. Deep AR blocks copy count from masquerading as independent tests.

### Candidate B

A restorative runtime cannot claim proper-function diagnosis from target success alone. It needs interventions that split the relevant account family while preserving target, source, version, and causal custody.

### Candidate C

A source-conditioned fiṭrah account can be discriminated within Track N only through source-eligible coordinates. Neutral proper-function evidence does not yield a personal designer, Wisdom, or Necessary Being.

### Deep AQ

PFIT-1 operationalizes `GATE E` for a finite deterministic norm-source family. If every pairwise disagreement set is empty under admissible experiments, the gate is blocked at theorem strength rather than merely untested.

### T299/T300 and OSM

A revised causal/profile-blindness experiment should be selected because it separates live account predictions, not because it repeats the same operation under more seeds. Endpoint or trajectory representations help only when the candidate accounts predict different complete response objects.

## 10. Ancestry, prior art, and novelty ceiling

```text
nonadaptive theorem:
standard finite Test Cover / pair-separation hitting set.

adaptive theorem:
standard deterministic decision-tree diagnosis recurrence.

Candidate 1:
adjacent exact query-complexity interface for a different hidden-matching target.

AR-T4 and collective diagnosis:
shared finite discrimination mechanism; not the same proposition.

Deep A/F/K/P/X/Y:
proper-function and norm-source application owners.

Deep AQ/AO/AR:
evidence, representation, and provenance guards.

general mathematical novelty:
0.

historical identity:
NONE.
```

The scoped contribution is an exact intervention-basis invariant, an adaptive/nonadaptive separation, and a proper-function experiment-design burden map.

## 11. Nonclaims

- Identifiability does not establish truth, warrant, objective fittingness, or explanatory superiority.
- The declared account family may be incomplete or miss hybrid accounts.
- Deterministic responses do not cover stochastic or bounded-error diagnosis.
- The theorem does not cover history-dependent policies, state-changing interventions, adversarial messages, or dynamic membership.
- Intervention feasibility, ethics, authorization, source truth, and world adequacy remain external.
- No personal designer, Wisdom, source truth, Necessary Being, or integrated champion follows.
- Proposal-level admission does not authorize repository adoption.
