# PMR-001 cold audit over frozen Epoch A candidates

## Frozen custody

The audit reviewed the candidate hashes recorded in `candidate_hashes.sha256`:

```text
PMR-M3-01  edc96157c1044f29d205553739c478cd657f1a3357ffe0b122f0989dd5fb5840
PMR-R5-01  bc5f344c464ab33defd9301cf3115d98eff3ed1fd7bb83a1c6d1f7f2c07fe6de
PMR-AGCOM-01 d2a4d6a7a20cf32546da0b683266e7c3497aaecaa320f301b934018c3fd907a7
checker c95fd33cf9318f0c0ec62cedad869f9a05b40a1c91c55803a4da12f9adfce7cb
results 7253e67599b218d7c99f472232628ecdcb77aeb8f25433a021f41dac1e02e742
```

This was a frozen-artifact audit, not a review of candidate-generation commentary. It is procedurally separate but not external human or independently trained-model review.

## Finding PMR001-A-F01 — originator and necessary/external bridges were collapsed

```text
disposition: REPAIR_REQUIRED
severity: BLOCKING_SOURCE_SCOPE_DEFECT
```

`B_origin` was defined as:

```text
O(y) → ∃x(R(x,y) ∧ N(x) ∧ E(x)).
```

The Asfahani locus directly supports the move from originated to **originator**, while the necessity and external-actuality status require further premises. Bundling `N` and `E` into `B_origin` hides a load-bearing ascent step and makes Result M3-01B sound formally but too strong as a source-aligned bridge.

Required repair:

```text
B_orig:
  O(y) → ∃x R(x,y)

B_NE:
  R(x,y) → N(x) ∧ E(x)
```

Then report separately:

```text
ORIG + B_orig entails an originator;
ORIG + B_orig + B_NE entails a necessary external originator.
```

## Finding PMR001-A-F02 — executable witness did not enforce distinct originated effect and originator

```text
disposition: REPAIR_REQUIRED
severity: NONBLOCKING_MODEL_CLARITY_DEFECT
```

The exhaustive checker found a valid countermodel in which one object was both originated and its own originator. That still proves the formal nonentailment in the unconstrained class, but the candidate prose froze a two-object `u,e` model. The executable evidence should explicitly validate the named distinct-object model rather than rely only on the first enumerated witness.

Required repair: add a direct check of `u ≠ e`, `O(e)`, and `R(u,e)` with `N(u),E(u)` and no Creator guards.

## Finding PMR001-A-F03 — necessary existence nonentailment

```text
disposition: PASS
```

`∃xN(x) ⊭ ∃xC(x)` is witnessed by a one-object model. No hidden world or source premise is needed. The candidate correctly limits this to formal nonentailment and a translated-primary source boundary.

## Finding PMR001-A-F04 — guarded Creator implication

```text
disposition: PASS_WITH_SCOPE_NOTE
```

The implication under `B_creator` and the W/P/K guard package is valid. Its force is conditional on the declared classification bridge. The candidate correctly denies that the formal implication validates the bridge or completes the attribute ascent.

## Finding PMR001-A-F05 — R5 rival comparison

```text
disposition: PASS_AFTER_F01_REPAIR
```

The impersonal-originator control is a valid minimal inference countermodel. Its matrix must distinguish which premise creates originator status and which separately creates necessary/external status.

## Finding PMR001-A-F06 — AGCOM receipt-profile result

```text
disposition: PASS_WITH_NONBLOCKING_SCOPE_NOTE
```

The profile collision and deletion countermodels are valid. The local re-orthing equivalence is a characterization relative to a stipulated finite target contract, not an independently discovered general theorem. The candidate correctly classifies it as an RP-T2/RP-T4/RP-T32/RP-T40 application with zero general novelty.

## Finding PMR001-A-F07 — ancestry and provenance

```text
disposition: PASS
```

No candidate claims a historical identifier, exact T367/T368 recovery, or independent theorem-origin credit. Candidate 1, PRR-T1, M11–M13, and TAC/SAC remain separate.

## Cold-audit disposition

```text
REPAIR_REQUIRED
blocking findings: PMR001-A-F01
nonblocking repairs: PMR001-A-F02
```
