# PMR-001 blocking-repair log

## Input

Cold audit disposition: `REPAIR_REQUIRED`.

## Repair PMR001-R01 — split originator from necessary/external bridge

Changed `PMR_M3_01_CANDIDATE.md`:

```text
pre-repair:
  B_origin: O(y) → ∃x(R(x,y) ∧ N(x) ∧ E(x))

post-repair:
  B_orig: O(y) → ∃xR(x,y)
  B_NE:   R(x,y) → N(x) ∧ E(x)
```

Results are now staged separately:

```text
ORIG + B_orig → originator
ORIG + B_orig + B_NE → necessary external originator
```

The Creator nonentailment and guarded implication were updated accordingly.

## Repair PMR001-R02 — explicit distinct-object and originator-only controls

Changed `finite_model_check.py` and `PMR_R5_01_CANDIDATE.md`:

- added a named `u ≠ e` impersonal necessary external originator model;
- added an originator-only model showing `B_orig` does not entail `N` or `E`;
- split the R5 comparison into originator-only and necessary-external impersonal variants.

## Re-execution

```text
first-order structures checked: 262,144
ORIG + B_orig models: 135,168
ORIG + B_orig + B_NE models: 16,128
full guarded models: 663
AGCOM Boolean recipient states: 256
overall finite check: PASS
```

## Scope effects

No historical theorem, source file, repository file, or Git state changed. General mathematical novelty remains zero. The repair narrows source/formal attribution and strengthens the countermodel evidence.
