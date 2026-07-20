# ER-1 baseline/treatment contract

- One canonical fact set per case (`fixtures/<case>/facts.yaml` lists the
  fact keys). The baseline arm renders every fact as an ordinary
  chronological audit log (`baseline-log.md`); the treatment arm renders the
  same facts as an explicit episode/verdict record
  (`treatment-episode.json`). `tests/test_smoke.py` fails if either
  rendering omits a fact key.
- Both arms receive the same probes (E1-E5-SPEC.yaml `probes`), the same
  budget, and the same answer format. Coined vocabulary appears in neither
  arm; benefiting from the treatment must not require it.
- Time/cost are measured in both arms (tokens, seconds) alongside diagnostic
  performance; the harm rule uses the cost ratio.
- Result correctness stays separate from pathway diagnosis throughout
  (SCORING-RUBRIC.md).
