# ER-1 — Episode-Reification Incremental-Value Test: Protocol

**Packet:** `ER-1` · **Status:** see `STATUS.yaml` (canonical index: `../experiment-status.yaml`) · **No run has occurred.** Frozen, deterministic, preregistration-ready packet — not a study report, not externally registered (Decision 0018).

## 1. Primary question

Not "can an episode record be written?" (the repository's schemas already show that). The question is **incremental value**:

> Does an explicit occurrence-anchored episode/verdict record improve pathway-defect discovery, correct remedy selection, audit traceability, robustness diagnosis, and false-closure prevention over a matched ordinary audit record carrying the same underlying facts?

## 2. Arms

- **Baseline (B):** the auditor (model or human, fixed per run manifest) receives each case's facts as an ordinary chronological audit log (`fixtures/*/baseline-log.md`) and answers the probe questions.
- **Treatment (T):** the auditor receives the same facts as an explicit episode/verdict record (`fixtures/*/treatment-episode.json`: occurrence identity/version, evidence with scope and validity, governing-rule binding, execution trace, per-verdict statuses, burden ledger) and answers the same probes.
- Both arms use ordinary language in the probes; coined vocabulary is not required to benefit and appears in neither arm's materials. Information content is matched by construction: both forms are generated from one canonical fact set per case (`fixtures/*/facts.yaml`), and `tests/test_smoke.py` checks fact-key coverage of both renderings.
- Time/cost are measured (reading + answering time, token counts) alongside diagnostic performance.

## 3. Case family E1–E5

Specified exactly in `E1-E5-SPEC.yaml`:

- **E1** nominal: correct result via adequate pathway (control — extra structure must not fabricate defects);
- **E2** correct result through an unreliable procedure (stopped-clock);
- **E3** incorrect result through an adequate configured procedure (justified rare miss);
- **E4** correct result under a defective governing binding with faithful execution;
- **E5** metamorphic pathway probe: a weak rule (pass iff a marker string is present) yields the correct current result; neighboring perturbations (correct-without-marker; incorrect-with-marker) separate truth-linkage/robustness from marker coincidence.

Migration note: the manuscript's earlier prose (§13.2) named this family "E1–E5" loosely with only E5 specified; this packet fixes the family exactly. No historical fixture files existed under these labels, so no label migration is needed; this note records that fact rather than silently defining over prior usage.

## 4. Endpoints and scoring

Per case and probe (rubric: `SCORING-RUBRIC.md`; keys in `E1-E5-SPEC.yaml`): pathway-defect discovery rate; defect-localization accuracy; correct-remedy selection; false-closure prevention (does the auditor endorse the case's draft completion claim when it is illegitimate?); robustness diagnosis on E5 neighbors; audit-traceability score (can the auditor point to the record element grounding each answer?); result-correctness judgments kept separate from pathway diagnosis throughout. Cost: reading/answer tokens and wall time.

## 5. Procedure, blinding, analysis

Randomized case order per repeat (seeds in `DECISION-RULES.yaml` parameters); the auditor never sees scoring keys or the other arm's materials; scoring is programmatic against frozen keys with the same parser for both arms (`analysis/analyze_er.py`); deviations recorded in `DEVIATION-LEDGER.md`; outcomes per `DECISION-RULES.yaml` (`supports incremental value` / `does not yet support incremental value` / `evidence of harm or failure` / `inconclusive`, with predeclared gates).

## 6. What this packet is not

Deterministic fixtures and smoke traversals here are engineering validation of the instrument, never empirical outcomes. No run exists; no result exists; success or failure here transfers nothing to FCSP-1 or the terminology benchmark.
