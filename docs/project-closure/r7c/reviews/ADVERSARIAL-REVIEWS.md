# R7C — Phase I + J adversarial reviews and negative-probe corpus

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE

Each guard was **attacked**, not merely asserted. Eight mechanical injection
attacks mutate a guard's input, confirm the guard **fails** (catches the attack),
and revert (tree clean). Two of them (P1 formula-in-backtick; P12 runtime=
restoration) initially **breached** and drove a real hardening — the exact value
of an adversarial pass.

## Phase I — negative-probe corpus (audit's 12 required rejections)

| # | Probe the validators must reject | Guard | Result |
|---|---|---|---|
| 1 | formula hidden in backticks | `validate_math_source.py` (inventory-allowlist) | **HELD** (breached first → fence-strip fix, then caught) |
| 2 | latent state declared an ortheme without ablation | `validate_dynamic_orthing.py` | **HELD** |
| 3 | represented standard equated to metaorthemma | `validate_meta_noetic_memetics.py` | **HELD** |
| 4 | subject-level profile attached to discourse token | `validate_noetic_targets.py` (R1) | **HELD** |
| 5 | quoted standard treated as endorsed | represented-standard `stance` enum (schema) | structurally prevented (stance is explicit; mention ≠ endorsement) |
| 6 | copied sources treated as independent tawātur | `validate_memetic_ecology.py` (warrant rule) | **HELD** |
| 7 | hard-constraint-violating route ranked as improvement | `validate_meta_noetic_memetics.py` (feasibility-first) | **HELD** |
| 8 | model update silently transported as same analysis | `UPDATE-COUPLING.yaml` + DYN-14/DYN-19 | structurally prevented (transport must be declared) |
| 9 | latent parameter equality used as endpoint equivalence | D5 corrected to `Geom_A` (not parameters) | structurally prevented (formula fixed) |
| 10 | many-to-many relation encoded as a function | D6 corrected to `ProfileOf_A ⊆ Z_A × Π_A` | structurally prevented (formula fixed) |
| 11 | candidate decision marked adopted-merged | `validate_candidate_state.py` | **HELD** |
| 12 | runtime closure asserted as human restoration | `validate_noetic_application.py` (N19 + hardened) | **HELD** (breached first → hardening, then caught) |

**8/8 mechanical attacks held; 4 probes structurally prevented.** Reproducible via
the injection harness; tree clean after each.

## Phase J — 14 adversarial reviews

| # | Audit | Verdict |
|---|---|---|
| 1 | target/bearer | **HELD** — five bearers (Decision 0027); P4 caught subject-type-on-discourse |
| 2 | interior-state humility | **HELD** — subject claims held/underdetermined, no-soul-access non-claim (R2); N19/P12 |
| 3 | represented-standard identity | **HELD** — μ̃ typed (id/version/stance/fidelity/lineage); P3 caught the conflation |
| 4 | carrier/stance | **HELD** — 8-mode stance enum; mention ≠ endorsement (probe 5) |
| 5 | tawātur/dependence | **HELD** — warrant rule; P6 caught count-as-independence |
| 6 | memetic mutation/lineage | **HELD** — mutation_identity (ablation-based) required on mutation edges |
| 7 | OSM biological/model/formal | **HELD** — the clones/state-cells row split into 4 typed rows (B8); no cell=clone=ortheme |
| 8 | update-level transport | **HELD** — UPDATE-COUPLING governs transport/reopening/rollback; DYN-14/19 |
| 9 | constrained-descent | **HELD** — feasibility-first partial order, two timescales; P7 caught rankable-hard-constraints |
| 10 | epistemology/source-status | **HELD** — 4-tier source status; secondary ≠ primary; concrete ≠ sound (companion §1/§3) |
| 11 | metaphysical-bridge | **HELD** — 10-rung argument map; OSM/DAEE prove only rungs 1–3 (companion §9) |
| 12 | math semantics/typesetting | **HELD** — gallery zero notdef; P1 caught formula-in-backtick; parity by evidence |
| 13 | candidate-state/provenance | **HELD** — honest merged/candidate split (Decision 0026); P11 caught self-promotion |
| 14 | false-closure | **HELD** — no artifact claims merged/signed-off; every R7C decision carries the CANDIDATE label; PR unmerged |

## Result

**12/12 probes addressed (8 mechanical held, 4 structural); 14/14 audits held.**
Two genuine validator weaknesses were found and hardened this pass (probe 1
fence-strip; probe 12 restoration-assertion) — the pass was adversarially useful,
not ceremonial. This is an Opus candidate self-review; it does **not** substitute
for the required fresh-Fable review of every hunk.
