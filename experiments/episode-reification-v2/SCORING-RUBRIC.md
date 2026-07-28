# ER-2 scoring rubric (programmatic, arm-blind)

Answers are parsed to `OUTPUT.schema.json` and scored by
`analysis/analyze_er2.py` against `fixtures/KEYS.json`. **Repairs of the ER-1
defects (audit B6/B7) are enforced here:**

- **Defect discovery / remedy:** exact match to the case's keyed
  `defect_category` / `remedy_category` (closed vocabularies; the answer
  chooses from them, so no free-text normalization/synonym table is needed —
  the ER-1 promise of a shipped synonym table is retired by using a closed
  answer schema instead, audit H3).
- **Completion correctness (EQUALITY — the ER-1 E1 bug fix):**
  `completion_correct = (endorse_completion == closure_legitimate)`. Refusing
  a legitimate completion (A1) is a **false positive** and feeds the
  E1-false-positive harm rule; endorsing an illegitimate completion is a
  false-closure miss. Both are scored wrong.
- **Traceability (semantic — not a presence flag):** every cited
  `grounding_fact_id` must **exist** in the case's `facts.json` AND the cited
  set must **intersect** the keyed `supporting` fact IDs. An empty, invented,
  or off-target citation scores 0.
- **E5 robustness (A5 only, semantic):** requires BOTH neighbor verdicts
  correct (marker-removed → FAIL; marker-present-wrong → PASS), the
  `mismatch_identified` flag, AND the correct defect category. A bare
  `neighbors_used`-style flag is insufficient.
- **Cost:** `answer_tokens` recorded per answer; no quality score depends on
  it (it feeds the cost-ratio harm rule only).

Result-correctness and pathway diagnosis stay separate: A2/A4 have
legitimate-looking results with defective pathways, A3 the reverse; the keys
score the pathway diagnosis and the completion decision independently.
