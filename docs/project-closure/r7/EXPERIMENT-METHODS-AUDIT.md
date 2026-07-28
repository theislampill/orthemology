# R7 — Experiment Methods Audit (Decision 0022)

Surfaced model: `claude-opus-4-8` (owner-observed substitution from Fable 5;
see `MODEL-SUBSTITUTION-INTERRUPTION-R7.md`). This audit is delivered in a
draft PR and is **not** merged by this session.

Human-readable companion to `scripts/validate_experiment_methods.py`. For each
current benchmark packet, the READY_TO_RUN gate (Decision 0022) requires all
of the following; the validator exercises each on the deterministic mock
adapter.

## FCSP-2 (`experiments/false-closure-selective-prediction-v2/`)

| Gate | Evidence |
|---|---|
| Executable run harness + mock/cmd adapters; provider interface cannot live-call in CI | `harness/run_fcsp.py` (MockAdapter offline; ProviderAdapterInterface raises) |
| Public/scoring isolation | prompts assembled only from `items/PUBLIC-ITEMS.json`; the harness has no code path reading `items/KEYS.json`; `--dump-payloads` audited by the smoke test — no key/label/truth token in any payload |
| Strict parser + logged format retry + recorded failures | `parse_strict` + one `FORMAT_REMINDER` retry; failed item-repeats recorded, never dropped |
| Neutral stimuli (audit B5) | facts are inferable, never stated (e.g. an evidence date outside a stated validity window); lexical + field-name leakage scans pass |
| Every declared endpoint implemented (audit B2) | `analysis/analyze_fcsp2.py` computes false-closure, AURC, missed-residual, abstention, route, result, burden-disposition, excess-AURC, overhead, LOFO, worst-case bounds |
| AURC aligned to the declared estimand (audit B3) | item-level AURC (per-item confidence/error), equal-family and LOFO sensitivity; "cluster-robust" language removed |
| Inference + multiplicity | paired arm-swap permutation tests, bootstrap CIs, Holm over the two primaries |
| Unit discipline (audit B4) | unit = item, paired; repeats are within-item replicates; pre-run `simulation/design_sensitivity.py`, **no observed-power rescue** |
| Mechanical decision execution | `decide()` unit-tested (supports / does-not-yet / harm / named-inconclusive); synthetic runs adjudicate nothing |

## ER-2 (`experiments/episode-reification-v2/`)

| Gate | Evidence |
|---|---|
| Harness + adapters | `harness/run_er.py` (mock offline; provider interface cannot live-call) |
| Information match, label-free (audit B8/H2) | both arms rendered from one canonical fact list; the packet smoke suite proves fact-atom parity and label-free payloads |
| Strict parser + retry | `parse_strict` + `FORMAT_REMINDER` |
| E1 completion scoring fixed (audit B6) | `completion_correct = (endorse_completion == closure_legitimate)`; refusing legitimate closure scores wrong + false-positive (unit-tested live) |
| Semantic E5 + traceability (audit B7) | E5 requires both neighbor verdicts + mismatch + remedy; traceability requires cited fact IDs to exist and intersect the supporting set (unit-tested) |
| Complete inference (audit B9) | paired case-level permutation tests, Holm, E1 false-positive + cost-ratio harm rules, failed-run gate, mechanical decision execution |
| Unit discipline | unit = case, paired; archetypes are strata with 4 neutral variants each; repeats are within-case replicates |

## No-run guard

No non-synthetic output exists in either current packet tree; every mock
traversal is stamped `synthetic_smoke` and adjudicates no scientific outcome.

## Result

Both FCSP-2 and ER-2 **pass** the Decision 0022 methods gate and are
`READY_TO_RUN`. The historical R6 `FCSP-1`/`ER-1` do not and are preserved as
`DETERMINISTICALLY_VALIDATED` historical versions (Decision 0020). Execution,
spend, ethics, and external registration remain owner/external acts; **no run
has occurred and no result exists.**
