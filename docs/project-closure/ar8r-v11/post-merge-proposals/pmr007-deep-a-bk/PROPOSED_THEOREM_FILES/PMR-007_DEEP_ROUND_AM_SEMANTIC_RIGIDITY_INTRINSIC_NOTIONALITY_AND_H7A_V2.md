# PMR-007 Deep Round AM V2 — isomorphism-natural semantics, interpretation rigidity, and the H7a boundary

```text
identity: PMR-007-SRIN-1
round: PMR-007-DEEP-AM
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_task: distinguish structural semantic canonizability from intrinsic notionality and mentality
```

## 1. Typed setting

Let `S=(X,R)` be a finite relational structure.  Let `C` be a finite content
set with no assumed action by structure automorphisms.  For every labelled copy
`S'` of `S`, let `I(S') ⊆ C^{|S'|}` be a nonempty admissible interpretation
family.  Require isomorphism stability:

```text
for every isomorphism f:S'→S'' and every i∈I(S'),
(f_* i)(f(x)) = i(x) belongs to I(S'').
```

A **natural interpretation selector** is a family `σ_{S'}∈I(S')` satisfying

```text
f_* σ_{S'} = σ_{S''}
```

for every isomorphism `f:S'→S''`.

All uniqueness claims below are literal at the declared content-label level.
A quotient-relative variant is obtained only after separately declaring an
equivalence relation on interpretations.

## 2. SRIN-1 — natural-selector fixed-point characterization

For one isomorphism class of finite structures, a natural interpretation
selector exists **iff** `I(S)` contains an interpretation fixed by every
automorphism of `S`.

### Proof

If `σ` is natural, apply naturality to every automorphism `g:S→S`.  Then
`g_*σ_S=σ_S`, so the selected interpretation is fixed.

Conversely, let `i∈I(S)` be fixed by every automorphism.  For a copy `S'`,
choose any isomorphism `f:S→S'` and define `σ_{S'}=f_*i`.  If `h:S→S'` is
another isomorphism, then `h^{-1}f` is an automorphism of `S`; fixedness gives
`f_*i=h_*i`.  Thus the definition is independent of the choice and is natural.

## 3. Three distinct semantic statuses

Define

```text
Fix_I(S) = {i∈I(S): g_*i=i for every g∈Aut(S)}.
```

Then:

```text
NO_STRUCTURAL_CANONICAL_INTERPRETATION:
  |Fix_I(S)| = 0;

STRUCTURAL_SEMANTIC_MULTIPLICITY:
  |Fix_I(S)| > 1;

INTERPRETATION_RIGIDITY_RELATIVE_TO_I:
  |Fix_I(S)| = 1.
```

These statuses are relative to the declared admissible family, content
identity, and structural signature.  Expanding the signature or restricting
`I` can change them.

## 4. Exact H7a decomposition

The earlier H7a burden must be split:

```text
H7a1 STRUCTURAL_CANONIZABILITY:
  the structural object selects an isomorphism-natural interpretation at the
  declared semantic quotient;

H7a2 CONSTITUTIVE_SEMANTICITY:
  the selected semantics is intrinsic to, or constitutive of, the relevant
  ground rather than assigned by an external law or downstream interpreter;

H7a3 MENTAL_REALIZATION:
  the constitutive semantic content is realized in a mental or intellectual
  host.
```

`SRIN-1` exactly characterizes H7a1.  It does not establish H7a2 or H7a3.
Deep AI's `NM-HOST` conditional applies only after genuine notional
representation has independently been established.

## 5. Countermodels and positive controls

### AM-CM1 — symmetric nonconstant semantics

Two structurally indiscernible positions must receive different contents.
Their swap automorphism has no fixed admissible interpretation.  No natural
selector exists.

### AM-CM2 — rigid impersonal semantic law

An asymmetric structure has exactly one admissible natural interpretation,
but the interpretation is fixed by an impersonal law.  There is no mental
host, de se owner, agency, personality, or Wisdom.

### AM-CM3 — signature-relative rigidity

A distinguished parameter makes one interpretation rigid.  Removing the
parameter restores symmetry and semantic multiplicity.  Rigidity therefore
tracks the declared explanatory resources.

### AM-CM4 — kernel/reference nonidentity

A global permutation of content labels preserves the equality/similarity
kernel while changing reference.  Kernel identity or alignment does not by
itself determine literal semantics.

### AM-CM5 — downstream mental abstraction

An impersonal external order obtains; one or more downstream minds abstract
notions representing it.  This satisfies the secondary Taymiyyan
mental/external reconstruction without making the external order itself an
intrinsic notion.

### AM-CM6 — distributed interpretation

Several representational subsystems jointly realize one interpretation
without one subject owning the complete semantic state.

### AM-CM7 — local-grammar convergence

Multiple local grammars converge on a shared structural profile while distinct
admissible reference assignments remain.  Shared structure does not identify
one ultimate mental grammar.

## 6. PRH and OSM evidence use

The PRH paper defines alignment through representation-induced kernels and
presents a hypothesis of convergence toward a shared statistical model of
reality.  Its own limitations include information mismatch, modality-specific
content, special-purpose shortcuts, metric dependence, and incomplete
alignment.  It supplies evidence for shared structure, not unique literal
reference or mentality.

The hippocampal OSM paper reports progressive neural decorrelation into
orthogonalized task-state representations and finds that, among the tested
models, CSCG reproduced both selected endpoint structure and the learning
trajectory.  This constrains computational accounts of the experiment.  It
does not prove intrinsic semanticity, objective proper function, one subject,
or an ultimate grammar.

## 7. Source-relative mental/external adjudication

El-Tobgui's secondary reconstruction presents Ibn Taymiyya as holding that
external reality contains particular entities and their attributes, while
universal notions are abstractions subsisting in minds.  This supports the
`downstream mental abstraction` model as source-compatible at that secondary
scope.  It does not independently establish H7a2, H7a3, an ultimate mind, or a
world-directed conceptualist metaphysics.

## 8. Candidate-G and architecture effect

Interpretation rigidity can create a real semantic restriction: it may remove
some reference assignments from the admissible profile space.  Under Candidate
G's parity theorem this counts as cross-profile structure only when the
admissible family and semantic identity are independently motivated.

It still does not prefer Architecture A over the strongest impersonal rival,
because the rival can include a unique impersonal interpretation law.  An
A-only discriminator requires evidence for H7a2 or H7a3, not merely H7a1.

## 9. Theorem-family and novelty disposition

The abstract mechanism is a standard group-action/equivariant-choice fixed-point
fact.  The contribution is a scoped H7a and uncreated-grammar decomposition,
plus exact empirical and source nontransfer controls.

```text
general_mathematical_novelty: 0
historical_identity: NONE
repository_status: PROPOSAL_EVIDENCE_ONLY
external_review: OPEN
owner_adoption: PENDING
```

## 10. Nonclaims

No result here establishes:

```text
intrinsic notionality;
mental or intellectual ground;
personal subjecthood;
proper function or Wisdom;
one unique ultimate grammar;
Necessary Being or Creatorhood;
divine Speech or revelational identification;
PRH metaphysical realism;
OSM semantic truth;
integrated champion;
meniscus;
or natural closure.
```
