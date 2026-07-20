# Pilot 0 v2 — complete execution specification (NOT RUN)

**Status: instrument-ready specification. NO EXECUTION HAS OCCURRED; no utility result exists; no term is adopted.** Running this requires the owner (model spend; ≥3 human raters; human-subjects responsibility) — see `docs/project-closure/UNAVOIDABLE-OWNER-ACTIONS.md` item 3.

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
- Analysis commands and import/export format: `analysis/analyze_pilot0.py --in runs.jsonl --items items/ITEMS.json --out report.json` (script inherited from v1 with flag-aware eligibility filtering; runs.jsonl schema: one JSON object per executor output, plus run manifest header row).
- **Decision rule (three-outcome, frozen before any run):** per term family — *adopt-candidate* (E1 and E2 both positive with pre-registered margins), *reject* (E1 ≤ 0 or E2 ≤ 0 with margins), *undetermined* (otherwise → Pilot 1). No result of this pilot adopts a term by itself; adoption is gated on the confirmatory study.

## 5. Freeze

The packet freezes by `scripts/freeze_pilot0.py --packet pilot0-v2` (hash in `FREEZE-HASH.txt`); any post-freeze edit is a new packet version. v1 (`terminology/pilot0/`, hash ece0412f…) is immutable superseded history and is never edited.
