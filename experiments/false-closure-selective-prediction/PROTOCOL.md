# FCSP-1 — False-Closure / Selective-Prediction Benchmark: Protocol

**Packet:** `FCSP-1` · **Status:** see `STATUS.yaml` (canonical index: `../experiment-status.yaml`) · **No run has occurred.** This is a frozen, deterministic, preregistration-ready protocol, not a study report. External preregistration has **not** occurred; submitting this protocol to a registry is an owner/external act (Decision 0018).

## 1. Question and estimand

Does the incremental machinery of manuscript §§5/7 — maintained candidate families, typed/scoped/expiring evidence, route composition, and a per-burden residual/closure ledger — reduce false closure and improve selective-prediction behaviour over a matched ordinary baseline, at matched information and matched budget?

Primary estimand: the difference (treatment − baseline) in per-item false-closure rate and in AURC over the frozen item set, for a fixed executor configuration, averaged over the preregistered repeats. Cluster-robust aggregation is by item family (see `ENDPOINTS.yaml`).

## 2. Arms (both stated in ordinary language — coined vocabulary is not a confound)

- **Baseline (B):** the executor receives each scenario and an ordinary instruction set: decide the classification/handling outcome, state confidence, and produce a simple completion record (done / not done, with notes). It may abstain or escalate if it judges that appropriate. Prompt text: `baselines/BASELINE-ARM.md`.
- **Treatment (T):** the executor receives the same scenario and the same budget, plus the structured handling contract in ordinary words: maintain the set of still-live alternatives explicitly; record for each piece of evidence what it covers and when it expires; check identity/version before reusing any earlier finding; select a route consistent with what remains unresolved; and close only over an explicit list of remaining obligations, each with a disposition. Prompt text: `treatments/TREATMENT-ARM.md`.
- Neither arm uses the coined terms. Both arms' outputs are mapped by the same parser to `OUTPUT.schema.json` records.

## 3. Items

`items/ITEMS.json` is generated deterministically by `scripts/generate_items.py` (frozen seed 20260720) and committed; `tests/` verify committed = regenerated. Nine scenario families (§4): the eight substantive families carry 4 items each and the ninth family is 8 negative controls = **40 items**. Every scenario is synthetic and public; none derives from the private casebook or transcript material. Each item carries machine-scorable ground truth: correct placement, live-alternative set, per-evidence validity, residual burdens with correct dispositions, route admissibility, and whether closure is legitimate.

## 4. Scenario families

F1 observational aliasing (two states share the observable); F2 identity/version uncertainty (successor or reused slot); F3 mis-scoped green check (validator scope does not intersect claim); F4 stale evidence (validity expired or superseded); F5 co-holding defects (two defects obtain together); F6 route-sufficient-but-identity-incomplete (safe route despite open identity); F7 false closure over deferred/transferred/risk-accepted burdens; F8 hard-constraint route conflict; F9 negative controls (simple cases where the extra machinery should not help and must not add spurious structure).

## 5. Procedure

Randomize item order per repeat (seeds in `DESIGN.yaml`); run each item in both arms with the same executor version and sampling parameters; parse outputs to records; score with the frozen keys; adjudicate parse failures per `DESIGN.yaml` §run-failure; compute endpoints (`ENDPOINTS.yaml`) with `analysis/analyze_fcsp.py`; apply `DECISION-RULES.yaml`; record every deviation in `DEVIATION-LEDGER.md`.

## 6. Blinding and leakage controls

Scoring is programmatic against frozen keys (no human scorer sees arm labels); the executor never sees ground truth, family labels, or scoring keys; arm prompts are matched in length band (±15%) and reading level to limit verbosity confounds; negative controls detect structure-for-structure's-sake; the analysis script is frozen before any run.

## 7. Outcomes

`supports incremental value` / `does not yet support incremental value` / `evidence of harm or failure` / `inconclusive` — exact numeric mapping in `DECISION-RULES.yaml`. A negative result cannot be reclassified as `inconclusive` except by the predeclared power criterion stated there.

## 8. What this packet is not

Not a run; not a result; not evidence for any claim in the manuscript; not externally registered. The simulation under `simulation/` uses clearly labeled synthetic assumptions and is not pilot evidence.
