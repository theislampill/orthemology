# R7E Sol Independent Repair Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to execute this plan task-by-task, with a fresh `gpt-5.6-sol` implementer and a separate `gpt-5.6-sol` reviewer for each task.

**Goal:** Repair every independently reproduced blocker in the cumulative R7E candidate, prove the strengthened contracts under adversarial mutation and a clean clone, then conditionally perform the authorized protected PR cascade and verify merged `main`.

**Architecture:** Preserve the existing source/generated boundary. Add typed, offline contracts and pure validation helpers first; migrate prose and publication math only after failing semantic tests exist. Treat R7E as a candidate and its LLM-mediated workflow as a provenance-qualified observational witness, never empirical validation or comparative evidence.

**Tech stack:** Python 3.11.9; PyYAML; jsonschema; markdown-it-py; Typst 0.15.0; pypdf 6.14.2; Markdown/YAML/JSON/JSON Schema; GitHub Actions and protected pull requests.

**Exact environment:** `C:\workspace\ai\orthemology-r7\venv-lock\Scripts\python.exe` with `requirements-ci.lock.txt`. Set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` for Windows command parity. Do not use the ambient Python environment to generate artifacts.

Before running plan commands in PowerShell:

```powershell
$PY = 'C:\workspace\ai\orthemology-r7\venv-lock\Scripts\python.exe'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
```

**Controlling design:** `docs/superpowers/specs/2026-07-21-r7e-sol-independent-repair-design.md`

**Base and branch:** `review/r7e-sol-independent-repair` from `candidate/r7e-orthing-supplementation@cbab14747835855d232448f648eefa1d4e36074e`.

**Universal task protocol:** Before each task, verify root and agent metadata still surface `gpt-5.6-sol`, verify the branch and clean/expected dirty state, write the task brief, and run the narrow baseline. The implementer must write a red test before behavior changes, observe the intended failure, implement the smallest coherent repair, run narrow and affected checks, inspect the diff, update generated state and manifest when tracked sources change, commit, and write a report. A separate reviewer then inspects the commit and reruns the decisive tests. Reviewer findings are fixed by a fresh implementer before proceeding.

---

## Task 1: Establish the durable Sol review control plane

**Files:**

- Create: `docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json`
- Create: `docs/project-closure/r7e-sol/R7E-SOL-READONLY-REPRODUCTION.md`
- Create: `docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml`
- Create: `docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md`
- Modify: `docs/project-closure/HISTORICAL-STATUS-INDEX.yaml`
- Modify: `scripts/validate_review_state.py`
- Create: `tests/test_r7e_sol_review_state.py`
- Create: `docs/decisions/0034-r7e-sol-independent-repair-contract.md`
- Modify: `docs/decision-status.yaml`
- Modify: `.github/workflows/validate.yml`

**Step 1 — red:** Add tests requiring the R7E-Sol closure prefix, exact base/head-at-observation, model gate, baseline command accounting, all audit finding IDs, all ten PR #12 changed paths, and only `keep|revise|drop|provenance-only` dispositions. Require Decision 0034 to be `proposed-candidate` on PR #12 without changing Decisions 0001–0022.

**Step 2 — observe failure:**

```powershell
& $PY tests/test_r7e_sol_review_state.py
```

Expected: missing R7E-Sol state/reproduction/finding/hunk artifacts.

**Step 3 — implement:** Record the verified topology, Python/dependency versions, 53 direct validator passes, three unchanged UTF-8 reruns, six byte-identical PDF rebuilds, and clean-tree result. Populate the finding matrix with `reproduced|refuted|partially-reproduced|unverified`, evidence loci, severity, repair task, and terminal status. Review each R7E hunk against R7D; do not classify the binary PDF or manifest as semantically independent changes. Add the workflow test command.

**Step 4 — verify:**

```powershell
& $PY tests/test_r7e_sol_review_state.py
& $PY scripts/validate_review_state.py
& $PY scripts/validate_decision_dependencies.py
& $PY scripts/validate_repo.py
```

**Step 5 — generated state and commit:** Regenerate `docs/current-state.yaml`, then `docs/provenance/RELEASE-MANIFEST.sha256`; rerun checks and commit `docs: establish R7E Sol review control plane`.

## Task 2: Generate and validate the complete candidate topology

**Files:**

- Create: `schemas/candidate-topology.schema.json`
- Create: `schemas/candidate-overlay.schema.json`
- Create: `docs/project-closure/r7e-sol/CANDIDATE-TOPOLOGY-INPUT.yaml`
- Create: `scripts/generate_candidate_state.py`
- Replace generated content: `docs/current-candidate-state.yaml`
- Modify: `scripts/validate_candidate_state.py`
- Modify: `README.md`
- Create: `tests/test_candidate_state.py`

**Step 1 — red:** Refactor design around pure `build_overlay(data)` and `collect_issues(data, decisions)` functions. Tests must reject omitted PR #11/#12, duplicate or noninteger PR, placeholder/non-40-hex head, broken parent link, wrong merge order, stale frozen observation, missing provenance layer, decision-allocation drift, candidate self-promotion, or evidence-free `merged|independent_signoff|ready_for_merge`.

**Step 2 — observe failure:**

```powershell
& $PY tests/test_candidate_state.py
& $PY scripts/generate_candidate_state.py --check
```

Expected: present overlay is stale and no generator exists.

**Step 3 — implement:** Freeze observed PRs #8–#12 with exact branch/base/head/state/draft/CI/provenance and observation timestamp. Use `head_at_observation`; never claim a tracked file contains its own final branch head. Generate the overlay deterministically and make the validator consume the generated model, not the obsolete R7C overlay or a PR #10 constant. Update README candidate wording.

**Step 4 — verify and mutate:** Run each test plus hand mutations for omitted leaf, broken base, placeholder, duplicate PR, and self-promotion. Then:

```powershell
& $PY scripts/validate_candidate_state.py
& $PY scripts/validate_schemas.py
& $PY scripts/validate_current_state.py
```

**Step 5 — commit:** Regenerate current state and manifest; commit `fix: generate complete R7 candidate topology`.

## Task 3: Supersede the R7E provenance and backlog claims

**Files:**

- Create: `schemas/orthing-candidate-ledger.schema.json`
- Create: `docs/project-closure/r7e-sol/ORTHING-CANDIDATE-LEDGER.json`
- Create: `docs/project-closure/r7e-sol/R7E-INPUT-PROVENANCE.json`
- Create: `docs/project-closure/r7e-sol/R7E-PROVENANCE-AND-BACKLOG-AUDIT.md`
- Create: `scripts/validate_candidate_provenance.py`
- Create: `tests/test_candidate_provenance.py`
- Preserve unchanged: `docs/project-closure/r7e/AUTONOMOUS-R7E-STATE.json`
- Preserve unchanged: `docs/project-closure/r7e/ORTHING-CANDIDATE-BACKLOG.md`

**Step 1 — red:** Tests reject duplicate immutable IDs, missing or multiply mapped legacy rows, inconsistent totals, truncated text marked complete, missing artifacts marked verified, agent sourcing promoted to scholarship, malformed extensionless references, or swarm/token/count statistics marked independently verified.

**Step 2 — observe failure:**

```powershell
& $PY tests/test_candidate_provenance.py
```

Expected: 221 legacy rows include only 172 unique legacy IDs, 49 reused rows across 19 duplicate IDs; the repository has only eight rejection bullets for the attributed sixteen.

**Step 3 — implement:** Map every preserved legacy row exactly once with a new immutable ID, `legacy_id`, `legacy_line`, target, proposal/rejection availability, evidence state, review state, and disposition. Record the missing journal, per-agent reports, full drafts, REBAKE attachment, maximaltrajectory attachment, eight rejection records, and reported statistics as missing/unresolved/implementing-run-attributed as supported. Never invent absent rejection entries or commit session JSONL/transcripts.

**Step 4 — verify:**

```powershell
& $PY tests/test_candidate_provenance.py
& $PY scripts/validate_candidate_provenance.py
& $PY scripts/validate_repo.py
& $PY scripts/validate_internal_references.py
```

**Step 5 — commit:** Update finding/hunk records, generated state, and manifest; commit `fix: supersede unreconstructible R7E provenance claims`.

## Task 4: Classify R7E as a bounded LLM-mediated orthing witness

**Files:**

- Create: `schemas/llm-mediated-orthing-witness.schema.json`
- Create: `docs/project-closure/r7e-sol/R7E-LLM-MEDIATED-ORTHING-WITNESS.yaml`
- Create: `docs/project-closure/r7e-sol/R7E-LLM-MEDIATED-ORTHING-WITNESS.md`
- Create: `scripts/validate_r7e_llm_witness.py`
- Create: `tests/test_r7e_llm_witness.py`
- Modify after the ledger validates: `manuscript/orthemma-ortheme-systems-revised-draft.md`

**Step 1 — red:** Require evidence-qualified fields for orthemmata, declared analysis, executor/subagent roles, governing types, case-bound applications, sources, candidate findings/profiles, routes, integrated actions, residual backlog, successor state, and higher-order audit. Reject missing artifacts labeled verified, aggregate statistics promoted to repository fact, duplicate witness IDs, missing evidence references, self-certifying higher-order audit, or language implying correctness, comparative utility, exact internal ontology, empirical validation, terminology benefit, or cross-model/domain generalization.

**Step 2 — observe failure:**

```powershell
& $PY tests/test_r7e_llm_witness.py
```

**Step 3 — implement:** Use only `repository-verified|attachment-observed|implementing-run-attributed|missing|unresolved`. Classify `llm_applicability` as supported, `llm_mediated_realizability` as provisional/partially supported, and `comparative_utility` as not established. Cross-reference the orthing-episode, metaortheme, metaorthemma, claim-ledger, and verdict contracts without changing Decisions 0001–0022. Add the suggested bounded manuscript paragraph only if every clause has a ledger reference.

**Step 4 — verify:** Run witness tests, schema validation, evidence-boundary validation, claim-source validation, and manuscript/PDF checks if prose changed.

**Step 5 — commit:** Regenerate state/artifacts as required and commit `docs: classify the bounded R7E LLM orthing witness`.

## Task 5: Add the typed DAEE semantic-operator contract

**Files:**

- Create: `applications/daee-epistemics/SEMANTIC-OPERATOR-CONTRACT.schema.json`
- Create: `applications/daee-epistemics/SEMANTIC-OPERATOR-CONTRACT.yaml`
- Create: `applications/daee-epistemics/SEMANTIC-OPERATOR-FIXTURES.yaml`
- Create: `scripts/validate_semantic_operator_contract.py`
- Modify: `applications/daee-epistemics/CURRENT-RUNTIME-CROSSWALK.yaml`
- Modify: `applications/daee-epistemics/NOETIC-FIELD-DYNAMICS.yaml`
- Modify: `applications/daee-epistemics/CORRECTIVE-TRANSITION.schema.json`
- Modify: `applications/daee-epistemics/CORRECTIVE-TRANSITION-FIXTURES.yaml`
- Modify: `scripts/validate_daee_current_crosswalk.py`
- Modify: `scripts/validate_corrective_transition.py`
- Create: `tests/test_semantic_operator_contract.py`

**Step 1 — red:** Add mutations for literal differentiable gradient, divergence/curl without a typed multi-node target field, transition-as-correctness, omitted whole-state reread, closure-as-uptake/restoration, hidden-burden deletion, unauthorized global revision, and strict soundness inferred from mere admissibility.

**Step 2 — observe failure:** Run the new tests and preserve the three historical false-pass demonstrations in the reproduction record.

**Step 3 — implement:** Type route pressure, event transition, field divergence, field curl, loop break, reread, and closure with inputs/outputs, target field, preconditions, semantic kind, claim role, non-claims, correctness relation, and pathway relation. Keep `AdmissibleCorrectiveTransition`, `LocallyImprovingTransition`, `TransitionPathwayAdequate`, `ClaimRelevantReasoningPathAdequate`, and factive claim-relative `StrictlySoundReasoning_q` distinct.

**Step 4 — verify:**

```powershell
& $PY tests/test_semantic_operator_contract.py
& $PY scripts/validate_semantic_operator_contract.py
& $PY scripts/validate_daee_current_crosswalk.py
& $PY scripts/validate_corrective_transition.py
& $PY scripts/validate_noetic_targets.py
& $PY scripts/validate_claim_reasoning_paths.py
```

**Step 5 — commit:** Add the validator to CI, regenerate state/manifest, commit `fix: type DAEE corrective operators and boundaries`.

## Task 6: Repair epistemology and meta-noetic evidence semantics

**Files:**

- Create: `applications/daee-epistemics/TAWATUR-WARRANT.schema.json`
- Modify: `applications/daee-epistemics/TAWATUR-WARRANT.example.yaml`
- Modify: `applications/daee-epistemics/FALSE-TAWATUR-FIXTURES.yaml`
- Modify: `applications/daee-epistemics/NOETIC-CLAIM.schema.json`
- Modify: `applications/daee-epistemics/NOETIC-CLAIM-FIXTURES.yaml`
- Modify: `applications/daee-epistemics/EPISTEMOLOGICAL-AND-METAPHYSICAL-BOUNDARY.md`
- Modify: `applications/daee-epistemics/META-NOETIC-MEMETICS-AND-DYNAMIC-ORTHING.md`
- Modify: `companion/CONCRETE-AND-SOUND-REASON.md`
- Modify: `scripts/validate_memetic_ecology.py`
- Modify: `scripts/validate_noetic_claims.py`
- Modify: `scripts/validate_meta_noetic_memetics.py`

**Step 1 — red:** Reject tawātur-by-count/popularity/graph degree, missing transmitter quality or subject-relative conditions, common-cause copies treated as independent, fiṭrah as scalar/coordinate/algorithm/metaortheme/soul readout/guaranteed attractor, corruption inferred circularly from dissent, and mental representation/conceivability/universal abstraction entailing external existence, possibility, or unseen modality.

**Step 2 — implement:** Keep evidence-access status distinct from claim role. Add `computational-analogy` to the six claim roles without corrupting `references/source-status.yaml`. Mark El-Tobgui/Turner claims as secondary reconstruction and proper-function warrant as modern comparison. Preserve objective truth while making acquisition conditions subject-relative and routes plural.

**Step 3 — verify:** Run noetic claims, memetic ecology, meta-noetic memetics, reason fixtures, noetic application, type/token semantics, schemas, and recursive mutations.

**Step 4 — commit:** Regenerate state/manifest; commit `fix: bound fitrah tawatur and mental existence claims`.

## Task 7: Correct the OSM/CSCG comparison and object firewall

**Files:**

- Modify: `applications/latent-state-orthing/OSM-CSCG-ORTHEME-CROSSWALK.yaml`
- Modify: `applications/latent-state-orthing/OSM-DYNAMICS-DEFINITIONS.yaml`
- Modify: `applications/latent-state-orthing/DYNAMIC-FIXTURES.yaml`
- Modify: `applications/latent-state-orthing/DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md`
- Modify: `docs/related-work/LATENT-STATE-INFERENCE-AND-ORTHEMOLOGY.md`
- Modify: `applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md`
- Modify: `scripts/validate_dynamic_orthing.py`

**Step 1 — red:** Reject clone=neuron, posterior=world/profile, parameter=geometry, Viterbi-as-training, all-methods-as-gradient-ascent, Adam omission, adaptation-as-correctness/convergence/generalization, and OSM as validation of Orthemology or theology.

**Step 2 — implement:** Preserve world/task → observation → biological response → population representation → CSCG clone → latent posterior → parameter → geometry → inferred profile → actual profile. State Baum–Welch as EM likelihood estimation, Viterbi as decoding/refinement, BPTT as gradient computation, and Adam as optimizer with the reported loss. Use bounded progressive adaptation/differentiation and note that CSCG-like representation is not necessary for task performance.

**Step 3 — verify:** Run dynamic orthing, latent-state fixtures, source status, claim sources, cross-document consistency, and new mutations.

**Step 4 — commit:** Remove or directly re-source the absent REBAKE prose citation; update ledgers, state, manifest; commit `fix: bound OSM as a task-specific computational analogy`.

## Task 8: Repair the argument map, metaphysical bridges, and divine Speech

**Files:**

- Modify: `companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml`
- Create: `scripts/generate_argument_map.py`
- Modify generated section: `companion/dynamic-orthing-noetic-learning-and-orthability.md`
- Modify: `companion/orthability-and-the-ground-of-intelligibility.md`
- Modify: `companion/ARGUMENT-MAP-ORTHABILITY.md`
- Modify: `companion/OBJECTIONS-AND-REPLIES.md`
- Modify: `companion/orthability-divine-attributes-and-speech-athari.md`
- Modify: `scripts/validate_argument_map.py`
- Create: `tests/test_argument_map_semantics.py`

**Step 1 — red:** Require stable IDs, scope, bridge/inference type, source role and references, strongest objection, rival exit, and generated count/ID parity. Reject objective-gradient language, convergence, empirical learnability yielding normativity without a bridge, premise/conclusion circularity, capacity implying actual Speech, OSM/DAEE support for theology, unsafe “created Arabic wording,” and upper-rung empirical promotion.

**Step 2 — implement:** Repair rung 8 so it does not assume the personal attributes it argues for. Route the naturalist, primitivist, Platonist, modal, aseity/bootstrapping, Euthyphro/fittingness, and impersonal exits explicitly. Separate created convention; created creaturely speech/recitation/writing; created voice/breath/ink/page/screen/media; Allah's act of speaking; revealed Arabic wording as Allah's Speech; and created creaturely hearing/reception. Capacity for disclosure is not actual divine Speech.

**Step 3 — verify:**

```powershell
& $PY tests/test_argument_map_semantics.py
& $PY scripts/generate_argument_map.py --check
& $PY scripts/validate_argument_map.py
& $PY scripts/validate_quran_loci.py
& $PY scripts/validate_source_status.py
& $PY scripts/validate_claim_sources.py
& $PY scripts/validate_companion_references.py
```

**Step 4 — commit:** Rebuild affected PDFs only after committing sources per Task 12; for now commit source/tests/generator as `fix: repair metaphysical and divine Speech argument boundaries`.

## Task 9: Correct terminology provenance without adopting terminology

**Files:**

- Modify: `manuscript/orthemma-ortheme-systems-revised-draft.md`
- Modify: `terminology/orthemic-terminology-pilot-protocol.md`
- Modify: `references/orthemology.bib`
- Modify: `references/source-status.yaml`
- Create: `tests/terminology-etymology-fixtures.yaml`
- Create or modify: `scripts/validate_terminology_etymology.py`
- Do not modify frozen `terminology/pilot0/` or `terminology/pilot0-v2/` packets.

**Step 1 — red:** Reject claims that `-emma` is an inherited productive English token suffix, that Greek `ema` derives `-ma`, that the coinages are already adopted, or that the system supplies universal primitives/proven isomorphism.

**Step 2 — implement:** Say “constructed but morphologically grounded”; preserve established `orth-` and English `-eme`; ground `-emma` only in Greek `-ma/-mat-` result/object/instance morphology; treat `ema` only as deliberately superposed possessive resonance. Frame cross-domain usefulness as benchmark-gated mnemonic/meta-schema hypothesis. If primer semantics must change, create a new frozen packet version instead of editing an old one.

**Step 3 — verify:** Run the new validator, source-status, terminology matching, both freeze checks, claim sources, and relevant PDF source conversion.

**Step 4 — commit:** Regenerate state/manifest and commit `docs: correct terminology provenance and utility claims`.

## Task 10: Replace the math allowlist with locus-sensitive classification

**Files:**

- Replace model: `docs/math-source-inventory.yaml`
- Modify: `docs/math-migration-status.yaml`
- Modify: `scripts/validate_math_source.py`
- Modify: `tests/test_math_pipeline.py`
- Create: `tests/test_math_source_inventory.py`

**Step 1 — red:** Inventory all inline-code occurrences in the seven publication sources as `literal-code|semantic-registry-id|mathematics`, keyed by file/locus/occurrence. Reject a new formula-like backtick, a copied allowlisted formula in another file, duplicate occurrence, orphan inventory row, false registry-ID classification, formula lacking current operator regex such as `V1(e)`, combining accent, removed build source, or removed gallery symbol.

**Step 2 — observe failure:** The present global-text allowlist and misleading `migrated: true` statuses must fail the new contract.

**Step 3 — implement:** Split `glyph_defect_repaired` from `full_math_source_migrated`, add complete publication coverage and visual-QA state, and require zero math-classified backticks for a migrated source. Do not mechanically convert code or registry identifiers.

**Step 4 — verify:** Run inventory tests, math pipeline tests, math source validator, and adversarial copies/moves/deletions.

**Step 5 — commit:** Commit classification/validator changes before source migration as `test: enforce complete publication math classification`.

## Task 11: Migrate all seven publication sources to mathematical markup

**Files:**

- Modify: `manuscript/orthemma-ortheme-systems-revised-draft.md`
- Modify: `theory/orthemic-core-formalization.md`
- Modify: `theory/orthemic-multi-actor-conflict-note.md`
- Modify: `companion/orthability-and-the-ground-of-intelligibility.md`
- Modify: `companion/orthability-divine-attributes-and-speech-athari.md`
- Modify: `companion/dynamic-orthing-noetic-learning-and-orthability.md`
- Modify: `docs/notation-gallery.md`
- Modify: `docs/math-source-inventory.yaml`
- Modify: `docs/math-migration-status.yaml`
- Modify translator/tests only when a reviewed expression requires bounded syntax.

**Step 1 — tests first:** For each source batch, add the unique expressions to translation/compile tests before editing prose. Include literal dollars in code, escaped currency, math in tables/links, multiline aligned expressions, semantic `\operatorname{...}`, malformed delimiters, and hard failures for unsupported raw HTML/images.

**Step 2 — migrate in small batches:** Use `unicode_math_to_latex.py` only to propose replacements. Review every expression for mathematical meaning, upright semantic operators/IDs, collision-free notation, inline versus display form, citations/links, and adjacent ASCII/accessibility explanation.

**Step 3 — verify each batch:**

```powershell
& $PY tests/test_math_pipeline.py
& $PY tests/test_math_source_inventory.py
& $PY scripts/validate_math_source.py
```

Expected final state: every publication source has `full_math_source_migrated: true`, `expected_notdef: 0`, and zero unapproved formula backticks.

**Step 4 — source commit:** Regenerate current state and manifest, run affected prose/semantic validators, then commit source migration separately as `docs: complete publication math source migration`. Do not generate PDF sidecars before this commit exists.

## Task 12: Repair PDF provenance, candidate status, and artifact generation

**Files:**

- Modify: `scripts/build_pdfs.py`
- Modify: `scripts/validate_pdf_math.py`
- Modify: `tests/test_math_pipeline.py`
- Modify: six `artifacts/*.pdf`
- Modify: six `artifacts/*.sources.json`
- Create: `docs/project-closure/r7e-sol/R7E-SOL-PDF-VISUAL-QA.md`

**Step 1 — red:** Add tests that every sidecar `source_commit` contains each recorded source hash, tool identity includes exact versions plus lock hash, status copy comes from explicit candidate-state input rather than hard-coded R5 wording, committed-PDF rasterization clears stale output, and all six artifacts are covered.

**Step 2 — implement:** Use the Task 11 source commit as sidecar provenance. Correct the hard-coded R5 preamble. Make `--check` materialize/verify source bytes at `source_commit`. Keep double-build and text-structure checks. Add committed-PDF rasterization or a separate deterministic QA command; `--png` source rendering alone is insufficient.

**Step 3 — build in pinned environment:**

```powershell
$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'
& $PY scripts/build_pdfs.py
& $PY scripts/validate_math_source.py
& $PY tests/test_math_pipeline.py
& $PY scripts/validate_pdf_math.py
& $PY scripts/build_pdfs.py --check
```

**Step 4 — visual QA:** Render every page of all six committed PDFs at readable resolution. Inspect formulas, missing glyphs, clipping/overflow, blank pages, tables, links, headings, page numbers, and status pages. Record every artifact hash, page count, rendered-page count, issue and disposition in the QA record. Use the PDF skill and inspect every page, not a sample.

**Step 5 — artifact commit:** Regenerate the manifest last, verify no source drift, and commit `build: regenerate verified publication PDFs`.

## Task 13: Run the complete adversarial and recursive mutation program

**Files:**

- Modify: `tests/schema-mutations/mutation-spec.json`
- Modify: `scripts/validate_recursive_mutations.py`
- Create: `docs/project-closure/r7e-sol/R7E-SOL-ADVERSARIAL-REPORT.md`
- Modify all new fixture files as required.

**Step 1:** Make every mandatory attack durable: stale/omitted topology; self-promotion; literal gradient; div/curl without field; transition-as-correctness; omitted reread; closure-as-uptake; hidden burden deletion; unauthorized global revision; strict soundness from admissibility; tawātur by count/popularity; fiṭrah coordinate; mental-to-external entailment; OSM identity collapse; argument-map contradiction; unsafe created wording; witness overclaim; and unapproved formula spans.

**Step 2 — prove each attack is rejected:** Run every new focused test against its valid control and invalid mutation. The report records command, mutation ID, intended invariant, exit code, and result. A phrase-presence-only rejection is insufficient where structured semantics are available.

**Step 3 — run recursive mutations:**

```powershell
& $PY scripts/validate_negative_fixtures.py
& $PY scripts/validate_recursive_mutations.py
```

**Step 4 — reviewer:** A fresh Sol reviewer attempts counterexamples and checks for false negatives/false positives. Fix every blocker, then commit `test: close R7E semantic mutation gaps`.

## Task 14: Run the exact pinned full suite and clean-clone candidate proof

**Files:**

- Update: `docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json`
- Create: `docs/project-closure/r7e-sol/R7E-SOL-CLEAN-CLONE-VERIFICATION.md`
- Update: `docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml`
- Update: `docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md`

**Step 1 — local full suite:** Extract and execute every `.github/workflows/validate.yml` command in order under the pinned venv. Record the exact command count. The final manifest regeneration must leave no diff and `build_pdfs.py --check` must pass. Record any Windows UTF-8 wrapper without altering the underlying validator.

**Step 2 — final whole-branch review:** A fresh Sol reviewer inspects `cbab147..HEAD`, every finding disposition, every PR #12 hunk disposition, source boundaries, math sources, PDFs, and tests. Resolve all blocking findings.

**Step 3 — clean clone:** Push the review branch only after the local gate, clone it into a new explicit directory, create a new venv from `requirements-ci.lock.txt`, rerun the exact full suite, rebuild/check PDFs, rasterize and inspect all pages, and confirm `git status --porcelain` is empty. Do not reuse caches or untracked control artifacts as evidence.

**Step 4 — closure commit:** Update records with immutable commit/hash evidence, regenerate state and manifest, run the full suite once more if the records affect it, and commit `docs: record clean-clone R7E Sol verification`.

## Task 15: Perform the authorized protected integration cascade

**Preconditions:** Root metadata still reports `gpt-5.6-sol`; all findings terminal; all tests and attacks green; math/PDF/clean-tree/clean-clone gates green; no owner-only blocker; exact live PR topology unchanged except expected review-branch commits.

**Step 1 — review branch to PR #12 branch:** Push `review/r7e-sol-independent-repair`, open a non-draft PR into `candidate/r7e-orthing-supplementation`, wait for required CI, verify exact heads, merge by ordinary merge commit without squash/force, and rerun/wait for PR #12 CI.

**Step 2 — serial child-to-parent merges:** For each step, refresh model identity, branch heads/bases, mergeability, protection, and required checks; merge only after green; then wait for the parent PR's CI before proceeding:

1. PR #12 → PR #11
2. PR #11 → PR #10
3. PR #10 → PR #9
4. PR #9 → PR #8
5. PR #8 → protected `main`

Stop before the next write/merge on any red check, stale head, unexpected commit, changed topology/protection, surviving semantic attack, model substitution, or genuine owner-only blocker. Preserve exact state and leave all affected PRs unmerged.

**Step 3 — merged-main proof:** Fresh-clone merged `main`, install only the exact lock, rerun the complete suite, rebuild/check all PDFs, rasterize/inspect every page, verify the clean tree, and record the actual main merge SHA.

**Step 4 — non-self-referential verification record:** If the merge SHA could not be included beforehand, create a protected follow-up branch/PR containing the final merged verification record, generated state, and manifest. Run CI, merge normally, then read back protected `main` and verify the record names the earlier merge and its own follow-up commit honestly.

**Final evidence:** Report exact commits, PR merge commits, CI run URLs/conclusions, full-suite commands/results, PDF hashes/page counts/visual record, clean-clone paths and tree status, adopted/revised/dropped/provenance-only R7E hunks, and any claims explicitly not established.
