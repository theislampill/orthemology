# PMR-007 Deep Round AZ V2 — crossed semantic intervention and mediation identifiability

```text
identity: PMR-007-CSII-1
round: DEEP_AZ
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: independently enlarged experiment for token versus semantic mediation
```

## 1. Authority-separated intervention setting

Let

```text
F — finite surface form, token, code, modality, or presentation set;
C — finite content set under one frozen semantic/reference/version contract;
Y — finite response, judgment, or action set.
```

The experiment must satisfy:

```text
SEM:
  C has an independently declared semantic and referential interpretation;

FEAS:
  every claimed intervention do(F=f,C=c) is operationally meaningful;

POSITIVITY:
  every cell required by the theorem is reachable with nonzero assignment
  probability or direct experimental control;

CONSISTENCY:
  the response under the assigned cell equals its potential response;

NO-INTERFERENCE:
  one unit's assignment does not change another unit's potential response at
  the declared scope;

COMMON-DESIGN:
  all compared architectures use the same interventions, coding, and response
  measurement;

STABLE-CONTRACT:
  semantic, source, and version contracts remain fixed during the experiment.
```

These guards are premises, not outputs of the theorem.

## 2. CSII-1A — deterministic crossed-table characterization

Let the complete deterministic interventional response table be

\[
y:F\times C\to Y.
\]

Define:

\[
\operatorname{FormInvariant}(y)
\iff
\forall c\;\forall f,f'\; y(f,c)=y(f',c),
\]

and

\[
\operatorname{ContentSensitive}(y)
\iff
\exists c\neq c'\;\exists f\; y(f,c)\neq y(f,c').
\]

At the declared table, exact **content-mediated response** is

\[
\operatorname{CM}(y)
=
\operatorname{FormInvariant}(y)
\land
\operatorname{ContentSensitive}(y).
\]

Under `SEM` through `STABLE-CONTRACT`, the full crossed intervention table
exactly decides `CM(y)`.

### Proof

The full table supplies every equality required by form invariance and every
pair needed to test content sensitivity.  The predicate is therefore directly
computable from the table. ∎

## 3. CSII-1B — unrestricted missing-cell impossibility

Over the unrestricted finite response-table class, omitting any one cell
`(f,c)` can make exact `CM` classification impossible: there exist two tables
that agree on every observed cell and differ only at the omitted cell, with one
satisfying `CM` and the other failing it.

This is an unrestricted-class statement.  Stronger structural assumptions may
reduce the required design.

The familiar diagonal-support control is:

```text
y_sem(f,c)=c;
y_form(f,c)=f.
```

They agree whenever `f=c` and differ on crossed cells.

## 4. CSII-1C — stochastic distributional extension

Let

\[
Q_{f,c}\in\Delta(Y)
\]

be the complete interventional response distribution.  Define distributional
form invariance by

\[
Q_{f,c}=Q_{f',c}
\quad
\text{for all }f,f',c,
\]

and content sensitivity when some `Q_{f,c}` differs from `Q_{f,c'}`.
Under the same feasibility and common-design guards, the complete family
`(Q_{f,c})` exactly decides the distributional analogue of `CM`.

Finite samples estimate rather than exactly reveal these distributions; sample
complexity and statistical error are not solved here.

## 5. What the experiment can and cannot establish

A positive crossed result establishes at most:

```text
the frozen system's response varies with the declared content coordinate;
and
the response is invariant across the tested form coordinate at the declared
scope.
```

It does not establish:

```text
that C is intrinsically or constitutively semantic;
that the semantic contract is true or natural;
first-person uptake;
personality;
selection because of fittingness;
proper function;
Wisdom;
divine Speech;
or actual-world metaphysics.
```

An impersonal semantic processor can satisfy the full result.

## 6. Controls and countermodels

```text
AZ-CM1 DIAGONAL SUPPORT COLLISION:
  y=C and y=F agree on F=C;
  observation alone does not identify mediation.

AZ-CM2 MISSING CELL:
  two unrestricted tables agree everywhere observed and differ in CM.

AZ-CM3 SEMANTIC ANCHOR DELETION:
  C is only an experimental label;
  the experiment identifies label mediation, not literal semantics.

AZ-CM4 IMPERSONAL SEMANTIC PROCESSOR:
  the system is exactly content-mediated and remains impersonal.

AZ-CM5 CANDIDATE-DEPENDENT CODING:
  A and R receive different form/content assignments;
  apparent discrimination is invalid.

AZ-CM6 VERSION DRIFT:
  the same form no longer expresses the same content under a later contract.

AZ-CM7 HISTORY DEPENDENCE:
  identical current cells have different responses after different histories;
  the static table is incomplete.

AZ-CM8 SOURCE NONMIGRATION:
  Track-N content labels enter only under source and translation guards;
  they are not neutral interventions by default.
```

## 7. Cross-lane effects

### Deep M/AD/AA/AY

Deep AZ supplies an independently enlarged experiment capable of separating
surface-token response from response to a declared semantic coordinate.  It
therefore narrows one empirical route into registered semantic mediation.

It does not close:

```text
Deep AY H7a2 constitutive semanticity;
Deep AD subject-level reason uptake;
Deep AA intentional purpose;
or the personal/impersonal architecture parity.
```

### OSM and PRH

The OSM trajectory supplies a real example in which latent task-state
structure, not raw sensory similarity alone, changes during learning.  A
crossed semantic experiment would require interventions that independently vary
task-state content and sensory form; the reported study does not by itself
instantiate this full design.

PRH alignment is a common-representation observation.  It can motivate
cross-modal form sets but does not supply the semantic contract or crossed
causal interventions.

### Language, Fusha/Qamus, and agentic communication

The design is applicable to paraphrase, translation, modality, or protocol
experiments only when occurrence meaning, source, version, authority, and
recipient contracts are fixed.  Same output across forms is not adoption or
warrant.

## 8. Theorem-family and authority ceiling

```text
abstract ancestry:
finite full-factorial causal intervention design
+
positivity/consistency identification
+
unrestricted response-table indistinguishability

AR8R contribution:
semantic-custody and personal/impersonal nontransfer integration

general mathematical novelty:
0

historical identity:
NONE

external review:
OPEN

owner adoption:
PENDING
```

## 9. Central disposition

The round supplies a concrete candidate-independent experiment for one open
Deep AN/AO gate: surface-form versus declared-content mediation.  It is not an
experiment that distinguishes the unified-personal architecture from the
strongest impersonal semantic rival, because both may pass.  The integrated
champion remains `NONE`.
