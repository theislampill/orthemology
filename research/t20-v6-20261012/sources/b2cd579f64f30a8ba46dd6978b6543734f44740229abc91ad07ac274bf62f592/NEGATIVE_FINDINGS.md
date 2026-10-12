# Negative findings and non-promotions

## New findings at exact scope

| ID | Subject | Outcome | What it does not refute |
|---|---|---|---|
| P03-U03-CE01 | Successful encoder range included in decoder domain | FALSE on original: 101 nested containers / 202 bytes | Finite checker soundness; the witness is not a proof |
| P03-U03-CE02 | Malformed native exporter rows uniformly use Rejection | FALSE on original: TypeError/ValueError before row validation | Correctness of emitted/compiled certificates |
| P03-U04-CE01 | Successful observation commits are validated without caller-stability premise | FALSE on original deterministic wait/mutation schedule | V4-O3's lock-held revision/check-use guarantee |
| P03-Q1f-CE01 | Edge preservation and image endpoints imply output DAG | FALSE: collapsed edge becomes self-loop | VCT already typed over well-formed DAGs |
| P03-Q1f-CE02 | Adding injectivity alone repairs that graph inference | FALSE: additional reverse edge creates a cycle | A checker explicitly validating target acyclicity |
| P03-U03-BUDGET01 | Decoder success implies encoder budget success | FALSE but legitimate refusal: UTF-8 input expands under ASCII escaping | The actual bounded transport contract |

The first three have proposal patches, exact preimages/postimages and red→green evidence. The graph countermodels are models of a proposed untyped interpretation, not tests of the historical VCT checker. The budget counterexample is intentionally **not repaired** by weakening limits.

## Preserved historical/scoped negatives

The original strict wrapper remains ORIGINAL_STRICT_FAIL_PRESERVED, exit 1, with BoundaryResults compilation failure in the recorded original Lean run. This is distinct from P03's current missing executable and from accepted mapped-native Lean 4.19.0 results. Exact originals and their source status are not overwritten. The original bulk archives are not newly recovered; this packet carries the supplied compact accepted-evidence projection and its hashes.

Eight generated examples, the old normal/optimised finite tests and censuses, and P03's new finite tests remain finite. CV-R/CV-C/CV-O ordinary mathematical text is not promoted to an unsupplied Lean theorem. Separate 4.32.2 results are not substitutes for 4.19.0 targets.

Q1f preserves the R16 laundering/boundary-drift negatives, R15 digest/forced-progress negatives, missing historical declarations, Specialist A R7/R9 and observation-scope limits, Specialist B index limits and Q0's scoped reuse. Accessible R15/R16 source was read at the fixed commit, without inventing the absent historical source identities.

## Unresolved strengthening attempts deliberately withheld

Whole CPython/JSON semantics, universal native-input snapshot safety, strong crash/OOM atomicity, helper-module semantic refinement, full concurrent-history proof and full VCT/TRC formalisation are not established. A pinned kernel invocation for the new candidate could not run. No new declaration/type/axiom acceptance, imported cache acceptance, owner policy, licence judgement, publication decision, empirical authority, expert-review impersonation or automatic canonical closure is granted.

No accepted theorem was weakened, given a new unrecorded premise or silently renamed. Proposed definitions and interface-domain changes are explicitly mapped in the reports and patch map.
