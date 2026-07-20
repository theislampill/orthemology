# R7 — Read-Only Reproduction Report (Phase A)

Date: 2026-07-20. Session surfaced model: `claude-fable-5`; no substitution
observed. Historical model observations preserved, unadjudicated.

## A1. Topology

Live `main` = `43fee0f519e2f6984fb143c1e621c83382e71ec7` (= archive comment;
archive SHA-256 `0f4c5dcf…9e95b` per the audit record). Protection intact
(required `validate`, strict). Latest main Actions run 29773896337: success.
Decision range 0001–0019. **DAEE pinned commit for every citation in this
pass: `theislampill/daee-epistemics @ c86b3c6673147b8802fe222373a165a37d4d24a8`
(main, 2026-06-18).**

## A2. Full current suite

All 34 workflow steps green from a fresh clone under the exact lock
(`requirements-ci.lock.txt`), including both packet smoke tests, the mutation
suite, and the deterministic PDF rebuild.

## A3. Experiment finding matrix (audit §4)

FCSP-1: (1) no executor adapter/harness — **reproduced** (packet contains only
generator/analysis/simulation/smoke scripts); (2) no parser or re-prompt —
**reproduced** (zero parser/adapter/re-prompt constructs in
`analyze_fcsp.py`, which reads pre-parsed JSONL); (3) analysis computes only
false-closure rate, raw AURC, and one unadjusted false-closure contrast —
**reproduced**; (4) declared secondary endpoints not computed — **reproduced**
(missed-residual, abstention, route, result, burden-disposition, excess-AURC,
overhead, LOFO, worst-case bounds all absent); (5) AURC ignores the declared
item→family hierarchy and pools item-repeats directly — **reproduced** (the
docstring even claims ENDPOINTS conformity); (6) no Holm/decision-outcome
execution — **reproduced** (the script defers adjudication); (7) power sim
treats repeats as independent Bernoulli draws — **reproduced**; (8)
temperature-0 repeats may be identical — **reproduced** (accepted fact of the
design); (9) scenario templates state target defects in near-diagnostic
language — **reproduced** (16 leakage-phrase hits in `items/ITEMS.json`);
(10) smoke tests validate traversal, not inferential readiness — **reproduced**.

ER-1: (1) no harness — **reproduced**; (2) no parser/synonym table despite
the rubric's promise — **reproduced**; (3) **E1 scoring bug live-reproduced**:
`score()` returns `false_closure_prevented=True` for BOTH
`endorse_completion=True` and `False` on legitimate-closure E1; (4) E5
accepts the bare `neighbors_used` flag — **reproduced**; (5) traceability
accepts any nonempty string — **reproduced**; (6) diagnostic titles
("stopped-clock", "justified rare miss", "defective binding", "metamorphic
marker probe") name the keys — **reproduced**; (7) `binding_defect: true` and
interpretation-bearing `reliability_note` leak treatment truth —
**reproduced** (present in E2/E4 treatment fixtures); (8) simple arm means
only — **reproduced**; (9) no decision rules/Holm/failed-run/power in the
analyzer — **reproduced**; (10) five repeated archetypes ≠ independent unit —
**reproduced** (no unit argument exists).

All 20 findings: **reproduced**. None refuted.

## A4. DAEE integration finding (audit §3)

Read at the pinned commit: `README.md`, `atomics/skill/SKILL.md`,
`references/diagnostics/diagnostic-ir.md`, `recursive-state-transitions.md`,
`routing-precedence.md`, `rubrics/output-release.md`,
`diagnostics/inference-boundary.md`, `diagnostics/seven-deformations.md`.

**Reproduced**: the repository presents itself as "a modular LLM skill and
governed diagnostic framework for epistemic operations and noetic analysis…
designed to examine the condition of the qalb (heart-mind) and the ʿaql
(intellect) before replying to doubts…", whose "governing aim is… to restore
sound cognition so that foundational knowledge, inference, testimony, signs,
and revelation are encountered in their proper order"; the Diagnostic IR is a
typed dispatch-gating intermediate representation; recursive state re-read,
owner/TTP routing, bounded release, and an explicit inference boundary are
runtime governance. The current Orthemology mapping
(`docs/integrations/daee-epistemics-orthemology-mapping.md`) treats it as a
donor of five generic engineering controls and rejects the deformation
taxonomy wholesale — **the audit's "too shallow" finding is reproduced**.

No repair was begun before this report was written.
