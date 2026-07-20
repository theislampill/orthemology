# ER-1 scoring rubric (programmatic, arm-blind)

Answers are parsed to `OUTPUT.schema.json` records and scored by
`analysis/analyze_er.py` against the frozen keys in `E1-E5-SPEC.yaml`:

- **Defect discovery:** `defect_identified` must equal the case's
  `ground_truth.pathway_defect` (exact normalized string; "none" for E1/E3
  result-side-only cases per the key). Free-text answers are normalized by
  the parser's frozen synonym table before comparison; the table ships in the
  parser and is part of the freeze.
- **Remedy:** `remedy` must equal `ground_truth.correct_remedy` (same
  normalization).
- **False-closure prevention:** `endorse_completion` must be false whenever
  `closure_legitimate` is false; endorsing a legitimate completion (E1) is
  correct, and refusing it scores as an invented defect for the E1 harm
  guard.
- **Traceability:** `grounding_element` must name a record element (baseline:
  a log line; treatment: a record field) — scored present/absent
  programmatically, with correctness audited in the run's adjudication step.
- **Robustness (E5):** `neighbors_used` must be true and the defect answer
  must reference the marker/property gap; an answer using only the original
  case fails this key.
- **Cost:** `answer_tokens` and `seconds` are recorded per answer; no
  quality score depends on them (they feed the cost ratio only).

Result-correctness judgments are never mixed into pathway scoring: E2/E4
have correct results with defective pathways, E3 the reverse — the keys
score the pathway diagnosis, and completion endorsement is scored separately.
