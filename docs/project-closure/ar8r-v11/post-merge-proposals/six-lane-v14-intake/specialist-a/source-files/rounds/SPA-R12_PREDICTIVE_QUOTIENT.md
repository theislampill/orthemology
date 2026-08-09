# SPA-R12 — finite predictive-history quotient

**Status:** specialist-local finite deterministic Myhill–Nerode/predictive-state
analogue; standard ancestry expected; no new theorem identity, novelty,
architecture implementation, repository adoption, or metaphysical conclusion.

## Frozen object

For a binary deterministic horizon-two causal interface, consider the histories
reachable after the first intervention. Associate to each history its residual
signature: the next output for each possible continuation intervention.

Two histories are predictively equivalent exactly when their residual
signatures agree. The quotient class count is the minimum number of
deterministic state identifiers required at that depth:

- equivalent histories may share one state and one output decoder;
- inequivalent histories cannot share a state, because some continuation input
  would require two different outputs from the same state/input pair.

This is a depth-specific result. Reusing states across depths requires an
explicit clock/termination convention.

## Correction to the history-state upper bound

The complete-history construction gives a universal realisation but can retain
semantically redundant distinctions. Quotienting by continuation behaviour is
the representation-invariant correction. State splitting, relabelling,
learned/hand-authored tags, and off-support table entries do not increase its
semantic class count.

The quotient count can support a resource comparison only after the machine
model, clock, decoder, units, and complete rival realisation class are frozen.
It does not identify an architecture by itself.

## Deletion model

If one continuation intervention is deleted from the residual signature, two
histories can become observationally equal even though the omitted input would
separate them. Thus deletion safety remains relative to the structural
hypothesis class and the retained continuation family.

## Executable evidence

The checker exhausts all 1,024 binary horizon-two causal tables. For every
table, brute-force state assignments/output decoders agree with the residual
quotient count. The quotient is invariant on complete open-loop profile fibres,
including pairs of tables that differ only at off-support histories. It also
finds many tables compressed from two reachable histories to one predictive
class and many deletion-induced merges.

Seven mutants are killed: canonical-history minimality, raw state-count
invariance, one-input sufficiency, off-support sensitivity, label/provenance
privilege, metaphysical overreading, and prefilled state counts.

## Ancestry and anti-false-multiplicity

This belongs to the standard finite observation/predictive quotient family and
is a Myhill–Nerode analogue, not a novel theorem. Exact theorem-level ancestry
and assumptions remain for Deep Research 20. No duplicate authoritative theorem
or Lean identity is allocated here.

## Conclusion ceiling

```text
FINITE_DEPTH_SPECIFIC_DETERMINISTIC_PREDICTIVE_QUOTIENT
MINIMAL_STATE_COUNT_WITHIN_FROZEN_MACHINE_SEMANTICS
NO_STOCHASTIC_OR_MEASURABLE_GENERALISATION
NO_ARCHITECTURE_OR_METAPHYSICAL_IDENTIFICATION
```
