# Pilot 0 v2 — complete execution specification (v2.1; NOT RUN)

**Status (Decision 0018 vocabulary): `READY_FOR_HUMAN_MATCHING_REVIEW` · registration `NOT_REGISTERED`. NO EXECUTION HAS OCCURRED; no utility result exists; no term is adopted or retired.** The blind human matching review is the owner-gated prerequisite for `READY_TO_RUN`; running then requires the owner (model spend; ≥3 human raters; human-subjects responsibility) — see `OPEN-DECISIONS.md` and `experiments/experiment-status.yaml` (packet `TERM-P0-V2`). Version history: `../pilot0-v2-history/` (v2.0's conflicting decision rule is preserved there and superseded by §4 below).

## 1. Design

Four between-arm conditions: **A** (exposure-matched filler primer), **B** (ordinary-vocabulary primer), **C** (coined-vocabulary primer), **C′** (sham-vocabulary primer = machine-generated 1:1 lexical map of C; `scripts/gen_sham_primer.py`). Items: 9 (`items/ITEMS.json`), of which 7 substantive (6 eligible for the C-vs-C′ contrast; the false-closure item is a label-independent control) and 2 negative controls (byte-identical across arms). Every rendering = common scenario + one length-matched framing sentence + an identical question stem; all construct teaching lives in the primers (matching enforced by `scripts/audit_terminology_matching.py`, run in CI).

## 2. Executor protocol (exact)

- **System context:** `You are answering short workplace judgment questions. Answer plainly and concretely. If a primer was provided, you may use its ideas where they genuinely help.`
- **Turn 1:** the arm's primer, verbatim. **Turn 2 … n+1:** one item per turn: `scenario_common + "\n\n" + framing + " " + stem` (framing omitted when empty).
- **Output schema per item (JSON, enforced):** `{"item_id": str, "answer": str (<=250 words), "structures_invoked": [str], "one_step_fix": bool}`.
- **Repetitions:** 5 independent runs per arm × item cell, fresh context each run.
- **Sampling:** temperature 0.7, top-p 0.95 (declared, fixed); seeds recorded per run where the API exposes them; otherwise run index + timestamp recorded as the reproducibility surrogate and flagged.
- **Model pinning:** exact model ID string recorded in the run manifest before the first call; no mid-run version change; any forced change aborts the block and is logged in the deviation ledger.
- **Item order:** per run, a fixed pseudorandom permutation from seed = SHA-256(run_id) — deterministic, recorded; negative controls never first or last.
- **B variants:** item P0v2-MB-1 rotates its three single-formulation B framings across runs (run index mod 3); each run uses exactly one.

## 3. Rating protocol

- **Raters:** ≥3 human raters; unit = one (item, answer) pair scored against the item's `probes`/`expected_key` rubric (binary per probe + overhead-token count for negative controls).
- **Blinding:** raters see answers with arm labels stripped AND coined/sham/ordinary construct nouns masked by neutral placeholders (`[TERM-1]`, `[TERM-2]`, masking map generated per answer, recorded); rater assignment balanced Latin-square over arms.
- **Comprehension check:** before rating, each rater passes a 5-question rubric quiz (≥4/5; failures retrained once, then excluded).
- **Adjudication:** probe-level disagreement resolved by majority; 3-way splits escalate to a written adjudication note; all notes appended to the deviation ledger.
- **Deviation rule:** any protocol deviation is logged with timestamp, scope, and disposition; undisclosed deviations void the affected cells.

## 4. Estimands and eligibility

- **E1 (vocabulary effect):** P(probe pass | C) − P(probe pass | B), substantive items, per family and pooled.
- **E2 (label-specificity / sham):** P(probe pass | C) − P(probe pass | C′), **eligible items only** (`eligible_for_c_vs_cprime: true`; the false-closure item and negative controls are excluded by flag).
- **E3 (teaching effect):** P(probe pass | B) − P(probe pass | A), substantive items.
- **E4 (overhead guard):** added structure tokens on negative controls, each arm vs A; success = near-zero.
- Analysis command and import/export format: `python analysis/analyze_pilot0_v2.py run.json --items items/ITEMS.json --out report.json` — a v2-local frozen script (this packet; derived from the immutable v1 skeleton, adding the flag-aware `eligible_for_c_vs_cprime` filtering and descriptive E1–E4 summaries; v2.0's spec referenced a flag-aware variant that did not exist in the tree — repaired in v2.1). `--selftest` traverses synthetic mock data end-to-end and yields no feasibility or scientific outcome.
- **Decision rule (v2.1 — feasibility-only; supersedes v2.0's adopt-candidate/reject/undetermined, which conflicted with the v1 protocol's feasibility-only constraint):** Pilot 0 outputs exactly one of `ADVANCE_TO_PILOT1` · `REVISE_AND_RETEST_INSTRUMENT` · `DO_NOT_ADVANCE_THIS_ITEM_VERSION` (this item/instrument version only — never a term retirement) · `INCONCLUSIVE`, derived mechanically by the analysis script from the numeric feasibility gates of §4a. **No adoption or retirement conclusion of any kind is available from Pilot 0**; E1–E3 are computed as *descriptive estimands only* to inform Pilot 1's design. Adoption/retirement is reserved for the adequately powered confirmatory stage.

### 4a. Numeric feasibility gates (exact; no "preregistered" claim — nothing is externally registered)

- pairwise rater agreement ≥ **0.70** in every (item, arm) cell;
- sham comprehension gap |C − C′| ≤ **10 pp**;
- per-item pooled pass rate within **[0.10, 0.90]** for at least **5** of the 7 substantive items (ceiling/floor guard);
- negative-control overhead ≤ **30 tokens** added vs Arm A, every arm.

Efficacy margins (minimum important effects, noninferiority, equivalence, and harm thresholds for E1/E2) are **not** Pilot 0 parameters: they bind Pilot 1 and the confirmatory stage, are stated in `../pilot1/PILOT1-TEMPLATE.md` and `../confirmatory-v1-template/`, and any value still open there is marked `TO_BE_FROZEN_AFTER_BLIND_MATCHING_REVIEW`. Calling any local value "pre-registered" is prohibited without a named external registry record (Decision 0018).

## 5. Freeze

The packet freezes by `scripts/freeze_pilot0.py --packet pilot0-v2` (hash in `FREEZE-HASH.txt`); any post-freeze edit is a new packet version, with the prior version preserved under `../pilot0-v2-history/`. v1 (`terminology/pilot0/`, packet hash `988a6522498df73ad1c7b0f73961a054ff20862d50fff6d644d0274877412772` — the R4 correction SELF-1; v2.0 mis-stated it as `ece0412f…`) is immutable superseded history and is never edited.
