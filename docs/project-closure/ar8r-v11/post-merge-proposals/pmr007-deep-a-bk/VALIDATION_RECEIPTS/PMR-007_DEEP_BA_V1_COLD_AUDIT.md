# PMR-007 Deep BA V1 cold audit

```text
disposition: REPAIR_REQUIRED
candidate: PMR-007-IRCQ-1 V1
primary executable result: FAIL
review relation: same-program cold audit over frozen bytes
external independence: NOT CLAIMED
```

## Blocking findings

### BA-F01 — checker conflates refinement with deterministic realization

The V1 theorem correctly states only:

```text
interface-sufficient deterministic representation -> ker(r) subset equiv_I.
```

The V1 checker instead tested the false converse:

```text
partition refines equiv_I -> partition itself is a deterministic
label/transition congruence.
```

An arbitrary split of one trace-equivalence class can send same-block states to
different split successor blocks.  It refines the canonical quotient but need
not support a deterministic represented transition.  This produced 6,048
failures.  The checker must test implication, not equivalence.

### BA-F02 — failed executable evidence must remain visible

The V1 `FAIL` is a checker-specification defect, not evidence for the theorem.
It must remain frozen as failed evidence; V2 requires a new checker and result
rather than rewriting the V1 output.

### BA-F03 — operational-content language risks metaphysical overread

The exact theorem yields a canonical **interface state quotient**, or an
operational content object only by an explicitly declared convention.  V2 must
state that it does not establish content intrinsic to the system outside that
interface, literal semantics, truth, or mentality.

### BA-F04 — minimality scope must exclude unreachable/invented represented states

The cardinality and uniqueness result is for `r(X)`, not all elements of an
ambient representation carrier `Y`.  V2 must retain this restriction in every
summary statement.

### BA-F05 — interface monotonicity requires a common base system

Action or label strengthening is monotone only when the underlying state set
and old transitions/labels are held fixed and the new interface genuinely
extends the old one.  V2 must make the comparison map explicit.

### BA-F06 — deterministic all-word authority ceiling

The theorem does not apply to hidden stochastic processes, partial observation,
learned approximate states, finite samples, or noisy interventions.  These
require probabilistic bisimulation, causal-state, or statistical-sufficiency
machinery and separate evidence.

### BA-F07 — empirical nontransfer

Sun et al. and PRH may motivate comparison surfaces, but no raw-data/code
reproduction establishes that any measured representation is the exact
quotient.  V2 must classify those links as source-reported motivation and
nontransfer controls.

## Nonblocking notes

- The trace-equivalence and quotient statements are standard Moore-machine /
  Myhill–Nerode / deterministic-bisimulation results.
- The `|X|-1` witness bound is safe but not advertised as sharp.
- General mathematical novelty remains zero.
