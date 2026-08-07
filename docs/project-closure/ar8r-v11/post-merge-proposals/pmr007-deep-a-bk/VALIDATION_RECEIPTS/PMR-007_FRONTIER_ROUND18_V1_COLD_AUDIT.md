# PMR-007 Frontier Round 18 V1 cold audit

```text
audit epoch: ROUND18-EPOCH-B1
frozen candidate: V1
relation to historical AR8R: NEW_POST_MERGE_RESEARCH
result: REPAIR_REQUIRED
```

## Scope audited

The audit considered only the frozen V1 theorem packet, model owner, primary
checker, primary result, and their recorded ancestry.  It did not treat the
primary executable PASS as admission.

## Blocking findings

### R18-V1-F01 — surface actions were standing in for complete certificate objects

V1 defines `G(q)` as a set of actions.  In the surrounding AR2/AR3, version,
source, authority, provenance, invalidator, and temporal-certificate setting,
two distinct complete certificate objects can project to the same surface
action.  Covering a cell by surface actions can therefore understate the
information needed to transport one *complete warranted object*.

Required repair: replace the primitive action set by a finite set `K` of
complete certificate objects and make the action map `act : K -> A` an explicit
projection.  Prove the projection inequality and preserve a strict example.

### R18-V1-F02 — exact-state side information was not separated from general encoder information

The equality `minimum labels = rho(C)` assumes an encoder that knows the exact
state and may assign a different label to any two states.  A version detector,
source checker, or local agent may itself observe only a coarser partition.

Required repair: state the exact-state theorem at its actual scope and add a
separate general deterministic encoder-information characterization in terms
of compatible message partitions.  Do not call the latter `rho(C)` unless the
exact-state guard holds.

### R18-V1-F03 — coding claims were not fully typed

The fixed-length bit equality does not extend unchanged to expected-length
prefix-free coding, variable-length framed messages, interactive protocols,
or bounded-error randomization.  Worst-case prefix-free and fixed-length coding
share the ceiling bound only after the message alphabet is fixed.

Required repair: separate fixed-length, worst-case prefix-free,
expected-length, framed variable-length, interactive, zero-error randomized,
and bounded-error models.  Prove only the finite pointwise zero-error
seed-fixing consequence.

### R18-V1-F04 — adversarial-message robustness was absent

A selector label carried through an adversarial channel need not be exactly
recoverable for the receiver to choose *some* certificate object admissible for
every state still compatible with the observation and received word.

Required repair: formulate the ambiguity-set intersection criterion for robust
relation selection.  Exact label recovery may be stated only as a stronger
special case.

### R18-V1-F05 — temporal compatibility was one-step and history-insensitive

The rank witness proves that choosing an admitted object at each visited state
is sufficient under the fixed perfect-information model.  It does not imply
that a one-time refinement label remains sufficient after hidden future
branching, stale model changes, dynamic membership, or history-dependent
observations.

Required repair: retain the finite perfect-information rank theorem, add
history/fresh-hidden-branch countermodels, and make model/version binding
explicit.

### R18-V1-F06 — prior-art and complexity ceilings were incomplete

The support-cover equality is a finite Set Cover instance; zero-error
side-information and functional-compression graph methods are established
ancestry for stronger communication formulations.  V1 said novelty zero but
did not make these boundaries load-bearing.

Required repair: record Set Cover NP-completeness for explicit cover
instances, Witsenhausen-style zero-error side-information ancestry, and
Orlitsky–Roche functional-compression ancestry.  No novelty may be assigned to
these standard mechanisms.

## Nonblocking observations

The V1 exhaustive checker correctly validates the elementary exact-state
support-cover identity and its declared finite rank witness.  Those results may
be reused after the primitive object and coding scopes are repaired.

## Disposition

```text
V1: PRESERVED_SUPERSEDED_RESEARCH_CANDIDATE
admission: WITHHELD
repository proposal: NOT_REPOSITORY_READY
blocking findings: 6
```
