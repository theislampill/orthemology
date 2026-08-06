# PMR-007 Deep AV V1 cold audit

```text
disposition: REPAIR_REQUIRED
frozen packet: PMR-007_DEEP_AV_V1_FROZEN_HASHES.sha256
review relation: same-session procedural cold audit over frozen bytes
external independence: NOT CLAIMED
```

## Blocking findings

### AV-F01 — V1's unique-bridge claim is false

The exhaustive one-source/one-neutral/one-target checker found 13 valid
entailment pairs with multiple neutral interpolants.  `S_A=exists X A` is the
strongest neutral consequence of `A`, not the unique interpolant.  Repair by
characterizing the complete interval between `S_A` and `T_C=forall Y C`.

### AV-F02 — vacuous entailment was not isolated

An inconsistent source antecedent entails every conclusion.  A tautological
target likewise gives no architecture discrimination.  Logical validity must
be separated from evidentially nonvacuous source-to-world support by explicit
satisfiability and nontriviality guards.

### AV-F03 — neutral vocabulary can smuggle the target

If `PERSONAL`, `WISE`, `SPEAKS`, an actual-world label, or an equivalent proxy
is placed in `N`, a target-laden interpolant may be immediate.  The theorem
cannot certify the neutrality of its shared vocabulary.  Add a typed vocabulary
registry and target-import audit.

### AV-F04 — source predication and neutral derivation were conflated

When the source directly predicates the target, the target symbol occurs in the
antecedent and can occur in a Craig interpolant.  That is source-relative
predication, not an independently defended neutral bridge.  Record it as such.

### AV-F05 — finite propositional and first-order scopes were blurred

The executable theorem is finite propositional.  Classical first-order Craig
interpolation is prior art with its own hypotheses.  It cannot be silently
transferred to finite-model-only, modal, higher-order, fixed-point,
probabilistic, intensional, paraconsistent, or source-governed semantics.

### AV-F06 — an interpolant is not automatically explanatory or usable

Interpolation may yield a large, unnatural, nonunique, or computationally
intractable bridge.  Existence does not establish explanatory merit, causal
mechanism, proper function, source truth, or implementation.

### AV-F07 — translation and world-link coordinates remain premises

The theorem operates on truth tables already supplied.  It does not verify
source bytes, locus, translation, attribution, proposition reconstruction,
source acceptance, referent identity, candidate-world completeness, or
actual-world truth.

### AV-F08 — premise truth and model-class adequacy remain open

A valid conditional can be irrelevant if `A` is false or if the declared
valuation class omits live rivals.  Add model-class and premise-status
firewalls.

### AV-F09 — ancestry and novelty need correction

The finite result is a constructive propositional interpolation fact; the
first-order ancestor is Craig's interpolation theorem.  Deep AF already owns
the Beth/implicit-definability frontier.  Deep AV must be classified as a
source-neutral bridge-audit extension, with zero general mathematical novelty.

## Required repair

1. Preserve the V1 uniqueness failure.
2. Prove the exact interpolant interval and count.
3. Introduce a finite `bridge_slack` invariant at fixed vocabulary.
4. Add satisfiability, target-nontriviality, and vocabulary-neutrality guards.
5. Separate finite propositional, classical first-order, and other logics.
6. Run a distinct two-neutral-variable rereview using set projection rather
   than the primary bit-table implementation.
