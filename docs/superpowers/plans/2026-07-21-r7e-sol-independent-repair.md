# R7E Sol Independent Repair Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to execute this plan task-by-task, with a fresh `gpt-5.6-sol` implementer and a separate `gpt-5.6-sol` reviewer for each task.

**Goal:** Repair every independently reproduced blocker in the cumulative R7E candidate, prove the strengthened contracts under adversarial mutation and a clean clone, then conditionally perform the authorized protected PR cascade and verify merged `main`.

**Architecture:** Preserve the existing source/generated boundary. Add typed, offline contracts and pure validation helpers first; migrate prose and publication math only after failing semantic tests exist. Treat R7E as a candidate and its LLM-mediated workflow as a provenance-qualified observational witness, never empirical validation or comparative evidence. Preserve waking `t1` records append-only; type later `t2` somnic assessment through versioned activation/evaluator contracts; demonstrate only deterministic residual recurrence over fixtures and a retrospective R7E case, never a deployed agent skill or scheduler.

**Tech stack:** Python 3.11.9; PyYAML; jsonschema; markdown-it-py; PDFLaTeX through `latexmk` in a pinned arXiv-supported TeX Live generation; the repository-declared bibliography processor; Poppler; pypdf 6.14.2; Markdown/YAML/JSON/JSON Schema; GitHub Actions and protected pull requests. Typst 0.15.0 remains a historical, noncanonical compatibility surface only.

**Exact environment:** A task-specific virtual environment outside the repository, created with Python 3.11 and installed only from `requirements-ci.lock.txt`. Set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` for Windows command parity. Do not use the ambient Python environment to generate artifacts.

Before running plan commands in PowerShell:

```powershell
$venvDir = Join-Path ([System.IO.Path]::GetTempPath()) 'orthemology-r7e-sol-py311'
$venvPython = Join-Path $venvDir 'Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython)) {
  py -3.11 -m venv $venvDir
  & $venvPython -m pip install -r requirements-ci.lock.txt
}
$PY = $venvPython
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
& $PY --version
& $PY scripts/validate_dependency_lock.py
```

**Controlling design:** `docs/superpowers/specs/2026-07-21-r7e-sol-independent-repair-design.md`

**Base and branch:** `review/r7e-sol-independent-repair` from `candidate/r7e-orthing-supplementation@cbab14747835855d232448f648eefa1d4e36074e`.

**Universal task protocol:** Before each task, verify root and agent metadata still surface `gpt-5.6-sol`, verify the branch and clean/expected dirty state, write the task brief, and run the narrow baseline. The implementer must write a red test before behavior changes, observe the intended failure, implement the smallest coherent repair, run narrow and affected checks, inspect the diff, update generated state and manifest when tracked sources change, commit, and write a report. A separate reviewer then inspects the commit and reruns the decisive tests. Reviewer findings are fixed by a fresh implementer before proceeding.

**Publication profile amendment for Tasks 11–13:** The target is a `generic arXiv-compatible two-column technical-paper profile`. This is venue-neutral and must not be described as an official arXiv template or as evidence of venue selection, submission, processing, endorsement, acceptance, or publication. The seven Markdown sources remain the authoritative owners of substantive prose. A deterministic tracked LaTeX tree is generated from them and may not acquire independent semantic edits. PDFs, sidecars, and source archives are derived artifacts.

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
# Run the focused provenance test created in this task.
```

Expected: 221 legacy rows include only 172 unique legacy IDs, 49 reused rows across 19 duplicate IDs; the repository has only eight rejection bullets for the attributed sixteen.

**Step 3 — implement:** Map every preserved legacy row exactly once with a new immutable ID, `legacy_id`, `legacy_line`, target, proposal/rejection availability, evidence state, review state, and disposition. Record the missing journal, per-agent reports, full drafts, REBAKE attachment, maximaltrajectory attachment, eight rejection records, and reported statistics as missing/unresolved/implementing-run-attributed as supported. Never invent absent rejection entries or commit session JSONL/transcripts.

**Step 4 — verify:**

```powershell
# Run the focused provenance test and validator created in this task.
& $PY scripts/validate_repo.py
& $PY scripts/validate_internal_references.py
```

**Step 5 — commit:** Update finding/hunk records, generated state, and manifest; commit `fix: supersede unreconstructible R7E provenance claims`.

## Task 4: Specify waking/somnic contracts and residual-recurrence v0

**Files:**

- Create: `docs/decisions/0035-somnic-orthing-and-activation-contracts.md`
- Create: `schemas/activation-contract.schema.json`
- Create: `schemas/orthing-event.schema.json`
- Create: `schemas/meta-orthability-assessment.schema.json`
- Create: `schemas/somnus-run.schema.json`
- Create: `schemas/somnic-assessment.schema.json`
- Create: `schemas/residual-recurrence-report.schema.json`
- Create: `examples/somnus/activation-contract-fixtures.yaml`
- Create: `examples/somnus/somnus-record-fixtures.yaml`
- Create: `applications/agentic-runtime/SOMNUS-CANDIDATE-INVENTORY.yaml`
- Create: `applications/agentic-runtime/HERMES-WRITEBACK-ADOPTION-PROFILE.yaml`
- Create: `applications/agentic-runtime/COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml`
- Create: `applications/agentic-runtime/README.md`
- Create: `scripts/validate_somnic_orthing.py`
- Create: `tests/test_somnic_orthing.py`
- Modify: `.github/workflows/validate.yml`
- Modify where crosswalk requires it: `schemas/orthing-episode.schema.json`
- Modify where crosswalk requires it: `schemas/verdict-record.schema.json`
- Modify where crosswalk requires it: `schemas/claim-ledger.schema.json`
- Modify where crosswalk requires it: `manuscript/orthemma-ortheme-systems-revised-draft.md`

**Step 1 — brownfield map:** Prove which existing episode, verdict, evidence, residual, route, analysis, metaortheme, metaorthemma, and provenance fields already satisfy the contract. Extend or crosswalk them; do not create a parallel episode ontology, verdict registry, evidence vocabulary, or duplicate field.

**Step 2 — red:** Add focused production-path mutations for all eighteen controlling attacks: target-history overwrite; missing target identity; collapsed identity levels; missing contract/evaluator versions; keyword-only applicability; binary-only evaluation; later evidence relabeled as `t1`; retrospective R7E capture relabeled live; accepted contract without fixture outcomes; non-bootstrap contract without authoring orthing; revision rewriting historical conformity; reopen without material delta; duplicate idempotency output; copy-count inflated recurrence; threshold treated as defect proof; automatic patch/promotion/closure from v0; provisional placement self-authorizing irreversible action; and outline-only candidates represented as implemented/deployed. Add positive, negative near-boundary, indeterminate, and overlap activation fixtures, including mixed lexical and genuinely overlapping cases.

Add the second precision fixture family: one turn with two occurrences and two episodes; one occurrence with several claimant assessments; indeterminate claimant plus an applicable selected claimant; inapplicable claimant retained; new anchor matched to an old already-assessed comparator without reopening it; closed assessment absent from the next frontier until material delta; reopening without historical rewrite; repeated malformed-input family failing declared independence; recurrence equality without causal diagnosis; assessment with no proposal; conflicted placement without mutation authority; `t1` versus `t2` evidence; and correct placement with defective pathway.

Add the writeback/subsumption fixture family: assessment warranting memory proposal; assessment warranting skill proposal; contract locus instead of skill patch; no-change outcome; two alternative proposals without auto-authorization; rejected proposal and failed application leaving assessment history unchanged; applied mutation requiring later outcome evaluation; legacy versus Somnus-grounded proposal provenance; unwarranted user-state persistence rejected; fact correction deferred to upstream evidence defect; correct skill output with defective pathway producing governing-artifact proposal; and mutation attacks that try to force every assessment into a proposal. Use existing verdict/action/transition owners rather than a separate harness.

Add outline-profile mutations for collective-mode collapse; shared type treated as transport; actor/ledger/version erasure; source applicability copied to recipient; receipt promoted directly to local governance or execution; transclusion called non-semantic or lossless; multi-operator count promoted to independence, tawatur, truth, or authorization; source-envelope rewrite; collective synthesis erasing dissent; redacted projection labeled complete; and automatic adoption/writeback/network claims. The collective profile remains downstream and does not expand local v0 into a network implementation.

**Step 3 — implement:** Define waking versus somnic orthing and keep meta-orthability as its applicability/assessability gate. Enforce the two-time append-only rule, incremental checkpoint capture, and distinct session/episode/occurrence/claim-attempt/claimant-assessment/orthing/somnic-assessment/proposal identities without a false turn-based hierarchy. Apply privacy/source limits, capture the occurrence, then gate claiming; preserve inapplicable and indeterminate attempts. Separate claimant-level results, candidate set, selected/provisional route, episode placement/closure, and claimant residuals.

Implement four-way evidence timing, capture modes, versioned activation contracts, separate evaluator, tri-state result, plural fallback/no-claim, bootstrap versus normal authorship provenance, and conflict/authorization separation. Split the somnus anchor frontier from the historical reference corpus and actual comparators. Closed assessments are assessable but not automatically requeued; reopening requires a material delta and never rewrites history. Limit v0 to controlled residual fingerprints and deterministic recurrence reports. Keep pattern equivalence, suspected locus, causal diagnosis, and proposed intervention separate; report dependence dimensions and say distinct episodes unless an independence rule passes. Preserve the eight retrospective defect loci rather than one sound/unsound field.

Crosswalk assessment, intervention disposition, proposal, authorization, application, and later outcome evaluation through existing owners. Represent zero/one/several proposals, investigation/evidence requests, residual preservation, ordinary writeback targets, governing-artifact targets, and no change. Preserve `legacy_reflective_proposal` versus `somnus_grounded_proposal` and independent `t1`-`t5` times. Do not implement replay, counterfactual replay, consequence classification, guarded apply/revert, runtime writeback, governed learning, patching, promotion, closure, or governance mutation.

For the downstream collective profile, distinguish C1 independent type convergence, C2 federated reference-preserving transclusion with local re-orthing, and C3 intentional council coordination. Preserve actor/ledger-indexed events and the normative-type/represented-standard/case-bound-binding/execution separation. Outline evidential, normative, and operational DSL/IR transclusion gates; immutable source envelope plus appended receiving assessment; local meta-orthability and authorization; bounded plural closure; dependence dimensions; privacy/disclosure limits; cycle/integrity/version/injection/poisoning/Sybil defenses; and no-soul/no-uptake boundaries. Do not add a collective runtime or claim that NAR/field-witness similarity proves semantic identity.

**Step 4 — application boundary:** Land only an outline-only inventory for orthability checking, append-only ledgering, separate live residual recording and later recurrence assessment, conflict handling, intervention/no-change disposition, verdict-aware patch proposals, guarded writeback actuation, a somnus orchestrator, export/import, represented-standard transclusion, bounded collective assessment/council comparison, and a transclusion ledger. Every entry declares inputs, outputs, dependencies, event emissions, authority limit, residual behavior, external/downstream owner, and non-claims. The adoption profile says Somnus subsumes the ordinary reflective-writeback question while treating mature proposal/review/dry-run/apply/revert machinery as a first-class downstream actuator, not the ontology's center or an unrelated accessory. Comparisons to Hermes Dreaming remain externally supplied and pending source/license/commit/test verification; describe it as coarser or more implicit, not non-reasoning. The collective profile uses the three-mode formulation, treats transclusion as availability for local orthing, and states `implemented in orthemology: no`, `automatic adoption: prohibited`, `automatic execution: prohibited`, and `automatic writeback: prohibited`.

Do not create or clone an external repository, distributed agent network, shared-memory service, skill package, private prompt, host configuration, scheduler, daemon, scheduled workflow, live emitter, writeback engine, transclusion transport, or external runtime mutation. Implement a direct deterministic reference analyzer only if an existing repository execution owner is proven; otherwise record the exact successor trigger and keep this task schema/fixture/validator-only.

**Step 5 — verify and commit:** Run the focused test/validator created in this task, schemas, cross-record validation, recursive mutations, internal references, repo hygiene, current-state/convergence, manifest parity, and the affected pinned suite. Record fixture and mutation counts, activation/evaluator versions, authorship mode, recurrence fixture/run identities, anchor/reference/comparator behavior, idempotency and reopening outcomes, assessment/proposal/authorization separation, legacy/grounded provenance, no-change survival, collective profile mode/transclusion/adoption boundaries, and explicit non-runtime status. Commit `feat: specify bounded somnic orthing contracts`.

## Task 5: Classify R7E as a bounded LLM-mediated orthing witness

**Files:**

- Create: `schemas/llm-mediated-orthing-witness.schema.json`
- Create: `docs/project-closure/r7e-sol/R7E-LLM-MEDIATED-ORTHING-WITNESS.yaml`
- Create: `docs/project-closure/r7e-sol/R7E-LLM-MEDIATED-ORTHING-WITNESS.md`
- Create: `scripts/validate_r7e_llm_witness.py`
- Create: `tests/test_r7e_llm_witness.py`
- Create: `docs/project-closure/r7e-sol/R7E-SOMNIC-CASE-CROSSWALK.yaml`
- Modify after the ledger validates: `manuscript/orthemma-ortheme-systems-revised-draft.md`

**Step 1 — red:** Require evidence-qualified fields for orthemmata, declared analysis, executor/subagent roles, governing types, case-bound applications, sources, candidate findings/profiles, routes, integrated actions, residual backlog, successor state, and higher-order audit. Reject missing artifacts labeled verified, aggregate statistics promoted to repository fact, duplicate witness IDs, missing evidence references, self-certifying higher-order audit, turn/episode/orthing collapse, retrospective reconstruction labeled live capture, later evidence inserted into `t1`, higher-order assessment without meta-orthability disposition, or language implying correctness, comparative utility, exact internal ontology, empirical validation, terminology benefit, cross-model/domain generalization, live append-only capture, claimant-level contract enforcement, recurrence detection, idempotent frontier processing, full Somnus/writeback chain, or nightly autonomy.

**Step 2 — observe failure:**

```powershell
# Run the focused LLM-witness test created in this task.
```

**Step 3 — implement:** Use only `repository-verified|attachment-observed|implementing-run-attributed|missing|unresolved` for evidence and the approved capture-mode vocabulary for reconstructed records. Classify `llm_applicability` as supported, `llm_mediated_realizability` as provisional/partially supported, and `comparative_utility` as not established. Cross-reference the existing episode/governance/evidence/verdict contracts and the Task 4 append-only/meta-orthability contracts without changing Decisions 0001–0022. Treat original R7E as a waking episode or family only where supported, and the independent Sol review as a later human/LLM-mediated retrospective assessment, not proof of deployed somnus. Preserve missing journals/reports/drafts, duplicate IDs, incomplete rejections, unresolved attachment bindings, and attributed statistics. Add the bounded manuscript paragraph only if every clause has a ledger reference.

**Step 4 — verify:** Run witness tests, schema validation, evidence-boundary validation, claim-source validation, and manuscript/PDF checks if prose changed.

**Step 5 — commit:** Regenerate state/artifacts as required and commit `docs: classify the bounded R7E LLM orthing witness`.

## Task 6: Add the typed DAEE semantic-operator contract

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
# Run the focused semantic-operator test and validator created in this task.
& $PY scripts/validate_daee_current_crosswalk.py
& $PY scripts/validate_corrective_transition.py
& $PY scripts/validate_noetic_targets.py
& $PY scripts/validate_claim_reasoning_paths.py
```

**Step 5 — commit:** Add the validator to CI, regenerate state/manifest, commit `fix: type DAEE corrective operators and boundaries`.

## Task 7: Repair epistemology and meta-noetic evidence semantics

**Files:**

- Create: `applications/daee-epistemics/TAWATUR-WARRANT.schema.json`
- Modify: `applications/daee-epistemics/TAWATUR-WARRANT.example.yaml`
- Modify: `applications/daee-epistemics/FALSE-TAWATUR-FIXTURES.yaml`
- Modify: `applications/daee-epistemics/NOETIC-CLAIM.schema.json`
- Modify: `applications/daee-epistemics/NOETIC-CLAIM.example.json`
- Modify: `applications/daee-epistemics/NOETIC-CLAIM-FIXTURES.yaml`
- Modify: `applications/daee-epistemics/NOETIC-FIELD-DYNAMICS.yaml`
- Modify: `applications/daee-epistemics/EPISTEMOLOGICAL-AND-METAPHYSICAL-BOUNDARY.md`
- Modify: `applications/daee-epistemics/META-NOETIC-MEMETICS-AND-DYNAMIC-ORTHING.md`
- Modify: `companion/CONCRETE-AND-SOUND-REASON.md`
- Modify: `scripts/validate_memetic_ecology.py`
- Modify: `scripts/validate_noetic_claims.py`
- Modify: `scripts/validate_meta_noetic_memetics.py`

**Scope amendment (2026-07-22):** `NOETIC-CLAIM.example.json` is the positive
record governed by the schema changed in this task and must receive the new
required fields. `NOETIC-FIELD-DYNAMICS.yaml` is the authoritative fiṭrah model
read by `validate_meta_noetic_memetics.py` and must carry the positive and
negative boundaries that validator enforces. Omitting either owner would force
schema drift or validator weakening, so both are added narrowly to Task 7.

**Second scope amendment (2026-07-22):**
`applications/daee-epistemics/NOETIC-EVIDENCE-REGISTRY.schema.json` is the
structural owner of evidence currentness, validity, scope, relation, and typed
support semantics. Its prior free-text scope and relation fields cannot express
or validate which evidence role and target type an authoritative record may
support. Fixture-specific case or literal matching, prose-substring matching,
and evidence-ID allowlisting are prohibited. `applications/daee-epistemics/NOETIC-EVIDENCE-REGISTRY.example.json`
is the authoritative record set resolved by the production validator and must
carry those typed roles and target-type bounds, including a current, valid,
independently relevant external-premise bridge control. These two owners are
therefore added narrowly to Task 7; no other scope is changed.

**Step 1 — red:** Reject tawātur-by-count/popularity/graph degree, missing transmitter quality or subject-relative conditions, common-cause copies treated as independent, fiṭrah as scalar/coordinate/algorithm/metaortheme/soul readout/guaranteed attractor, corruption inferred circularly from dissent, and mental representation/conceivability/universal abstraction entailing external existence, possibility, or unseen modality.

**Step 2 — implement:** Keep evidence-access status distinct from claim role. Add `computational-analogy` to the six claim roles without corrupting `references/source-status.yaml`. Mark El-Tobgui/Turner claims as secondary reconstruction and proper-function warrant as modern comparison. Preserve objective truth while making acquisition conditions subject-relative and routes plural.

**Step 3 — verify:** Run noetic claims, memetic ecology, meta-noetic memetics, reason fixtures, noetic application, type/token semantics, schemas, and recursive mutations.

**Step 4 — commit:** Regenerate state/manifest; commit `fix: bound fitrah tawatur and mental existence claims`.

### Post-Task-7 remote CI checkpoint amendment

Before Task 8, close the two inherited infrastructure failures that block the
ordered matrix and exact-head remote checkpoint. This amendment does not
renumber Tasks 8–16 and does not reopen or modify Task 7 semantic owners.
Task 7 remains approved at exact commit
`79e0bac9c3da7b6a6b6f6e783fcd73f9e6df18cd`; both micro-scope commits must be
descendants and may not alter or revert that commit or any Task 7 semantic
owner.

**Dependency-classification micro-scope — files:**

- Modify: `scripts/validate_dependency_lock.py`
- Create: `tests/test_dependency_lock.py`
- Modify: `.github/workflows/validate.yml` only to run the focused dependency test beside the existing production validator, without adding or changing any package-install path
- Regenerate: `docs/current-state.yaml`
- Regenerate: `docs/provenance/RELEASE-MANIFEST.sha256`

**Dependency-classification micro-scope — red and repair:** Use Python 3.11's
`sys.stdlib_module_names` as the authoritative standard-library namespace while
retaining explicit `IMPORT_TO_DIST` ownership and repository-local exclusion.
Prove RED for `__future__`, a second old-hint omission such as `zoneinfo` or
`tomllib`, mixed partitioning, and the retained repository import. Preserve
mapped third-party, local-module, missing-pin, and unknown-import-fails-closed
controls. Do not add `__future__` to the dependency lock or import map and do
not remove the legitimate future import.

**Internal-reference test micro-scope — files:**

- Modify: `tests/test_internal_references.py`
- Modify: `.github/workflows/validate.yml` only to run the focused test beside the unchanged production validator, without adding or changing any package-install path
- Regenerate: `docs/current-state.yaml`
- Regenerate: `docs/provenance/RELEASE-MANIFEST.sha256`

**Internal-reference test micro-scope — red and repair:** Preserve the two
current stale assertions as RED, then replace their live-roadmap missing-path
fixture with an isolated temporary committed Git corpus and synthetic exact
`- Create:` sentinel. Prove exact planned-output exemption, current-evidence
and ordinary-line rejection, materialized-path resolution, untracked and
staged-only non-authority, malformed-create rejection, and unchanged real-tree
production validation. Materializing the sentinel must resolve the exact
`- Create:` occurrence, ordinary-plan reuse, and separate current-evidence
occurrence. The temporary corpus must be removed on success or failure without
tracked, staged, or ignored repository residue. Do not rotate the sentinel to another Task 8–16 output,
fabricate a permanent plan entry, remove the real Task 5 witness, or change
`scripts/validate_internal_references.py` unless isolated RED demonstrates a
separate production defect.

Implement the two micro-scopes as separate test-first descendant commits with
separate finite independent reviews. After both are approved, rerun the exact
23-command matrix and require 23/23 GREEN, deterministic state/manifest parity,
clean tracked state, and a new exact-SHA push/PR CI checkpoint before Task 8.
Preserve runs `29939915234` and `29939917400` as failed dependency evidence for
exact SHA `48570f4ee43b3139ca387617ccc7c1c8732936b3`, not as internal-reference
evidence. The new push and PR runs must both resolve to one exact descendant
SHA and pass before Task 8. No force-push, rebase, amend, or history rewrite is
authorized.

## Task 8: Correct the OSM/CSCG comparison and object firewall

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

## Task 9: Repair the argument map, metaphysical bridges, and divine Speech

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
# Run the focused argument-map test and generator drift check created in this task.
& $PY scripts/validate_argument_map.py
& $PY scripts/validate_quran_loci.py
& $PY scripts/validate_source_status.py
& $PY scripts/validate_claim_sources.py
& $PY scripts/validate_companion_references.py
```

**Step 4 — commit:** Rebuild affected PDFs only after committing sources per Task 13; for now commit source/tests/generator as `fix: repair metaphysical and divine Speech argument boundaries`.

## Task 10: Correct terminology provenance without adopting terminology

**Files:**

- Modify: `manuscript/orthemma-ortheme-systems-revised-draft.md`
- Modify: `terminology/orthemic-terminology-pilot-protocol.md`
- Modify: `references/orthemology.bib`
- Modify: `references/source-status.yaml`
- Create: `tests/terminology-etymology-fixtures.yaml`
- Create: `scripts/validate_terminology_etymology.py`
- Do not modify frozen `terminology/pilot0/` or `terminology/pilot0-v2/` packets.

**Step 1 — red:** Reject claims that `-emma` is an inherited productive English token suffix, that Greek `ema` derives `-ma`, that the coinages are already adopted, or that the system supplies universal primitives/proven isomorphism.

**Step 2 — implement:** Say “constructed but morphologically grounded”; preserve established `orth-` and English `-eme`; ground `-emma` only in Greek `-ma/-mat-` result/object/instance morphology; treat `ema` only as deliberately superposed possessive resonance. Frame cross-domain usefulness as benchmark-gated mnemonic/meta-schema hypothesis. If primer semantics must change, create a new frozen packet version instead of editing an old one.

**Step 3 — verify:** Run the new validator, source-status, terminology matching, both freeze checks, claim sources, and relevant PDF source conversion.

**Step 4 — commit:** Regenerate state/manifest and commit `docs: correct terminology provenance and utility claims`.

## Task 11: Replace the math allowlist with locus-sensitive classification

**Files:**

- Replace model: `docs/math-source-inventory.yaml`
- Modify: `docs/math-migration-status.yaml`
- Modify: `scripts/validate_math_source.py`
- Modify: `tests/test_math_pipeline.py`
- Create: `tests/test_math_source_inventory.py`
- Create: `schemas/publication-profile.schema.json`
- Create: `docs/publication-profile.yaml`
- Create: `scripts/validate_publication_profile.py`
- Create: `tests/test_publication_profile.py`

**Step 1 — red:** Inventory all inline-code occurrences in the seven publication sources as `literal-code|semantic-registry-id|mathematics`, keyed by file/locus/occurrence. Reject a new formula-like backtick, a copied allowlisted formula in another file, duplicate occurrence, orphan inventory row, false registry-ID classification, formula lacking current operator regex such as `V1(e)`, combining accent, removed build source, or removed gallery symbol. Also reject venue branding or status fabrication, an unrecorded profile exception, a missing entry point, conflicting bibliography owners, system-font or hidden-environment dependencies, shell escape, absolute paths, unsupported packages, undeclared hard limits, a missing appendix policy, or removal of source qualifications.

**Step 2 — observe failure:** The present global-text allowlist and misleading `migrated: true` statuses must fail the new contract.

**Step 3 — implement:** Split `glyph_defect_repaired` from `full_math_source_migrated`, add complete publication coverage and visual-QA state, and require zero math-classified backticks for a migrated source. Do not mechanically convert code or registry identifiers. The publication profile maps all seven substantive sources to the existing six artifact identities and records each artifact as `technical-paper` or the explicit `diagnostic-reference` exception. It owns the entry point, bibliography owner, engine, TeX Live generation, bibliography processor, overfull-box tolerance, package policy, appendix policy, and source-package owner. The five paper-shaped artifacts use article-class 10-point US Letter output with two-column bodies and references, full-width title and abstract front matter, and single-column technical appendices. The notation gallery is the diagnostic-reference exception but remains subject to the same provenance, font, extraction, packaging, clean-build, and visual gates.

**Step 4 — verify:** Run inventory tests, math pipeline tests, math source validator, and adversarial copies/moves/deletions.

**Step 5 — commit:** Commit classification/validator changes before source migration as `test: enforce complete publication math classification`.

## Task 12: Migrate all seven publication sources to mathematical markup

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
- Create: `publication/latex/`
- Create: `scripts/generate_latex_sources.py`
- Create: `scripts/validate_latex_sources.py`
- Create: `tests/test_latex_source_generation.py`
- Modify translator/tests only when a reviewed expression requires bounded syntax.

**Step 1 — tests first:** For each source batch, add the unique expressions to translation/compile tests before editing prose. Include literal dollars in code, escaped currency, math in tables/links, multiline aligned expressions, semantic `\operatorname{...}`, malformed delimiters, and hard failures for unsupported raw HTML/images. Require deterministic LaTeX generation, one declared bibliography owner, the profile-owned front matter/body/appendix layout, and rejection of shell escape, absolute paths, venue metadata, or semantic divergence from the Markdown owners.

**Step 2 — migrate in small batches:** Use `unicode_math_to_latex.py` only to propose replacements. Review every expression for mathematical meaning, upright semantic operators/IDs, collision-free notation, inline versus display form, citations/links, and adjacent ASCII/accessibility explanation. Generate the tracked LaTeX tree deterministically from the authoritative Markdown sources. Do not edit generated LaTeX as an independent prose owner.

**Step 3 — verify each batch:**

```powershell
& $PY tests/test_math_pipeline.py
# Run the focused math-source inventory test created in Task 11.
& $PY scripts/validate_math_source.py
```

Expected final state: every publication source has `full_math_source_migrated: true`, `expected_notdef: 0`, and zero unapproved formula backticks.

**Step 4 — source commit:** Regenerate current state and manifest, run affected prose/semantic and LaTeX-source validators, then commit the authoritative prose and generated LaTeX tree separately as `docs: complete publication math source migration`. Do not include PDFs, sidecars, source archives, build logs, auxiliary files, or frozen QA output before this commit exists.

## Task 13: Repair PDF provenance, candidate status, and artifact generation

**Files:**

- Modify: `scripts/build_pdfs.py`
- Modify: `scripts/validate_pdf_math.py`
- Modify: `tests/test_math_pipeline.py`
- Modify: six `artifacts/*.pdf`
- Modify: six `artifacts/*.sources.json`
- Create: `scripts/validate_arxiv_source_package.py`
- Create: `tests/test_arxiv_source_package.py`
- Create: six `artifacts/*.source.tar.gz`
- Create: six `artifacts/*.source-manifest.json`
- Create: `docs/project-closure/r7e-sol/R7E-SOL-ARXIV-COMPATIBILITY.md`
- Create: `docs/project-closure/r7e-sol/R7E-SOL-PDF-VISUAL-QA.md`

**Step 1 — red:** Add tests that every sidecar `source_commit` contains each recorded Markdown and generated-LaTeX source hash, tool identity includes exact versions plus lock and publication-profile hashes, status copy comes from explicit candidate-state input rather than hard-coded R5 wording, committed-PDF rasterization clears stale output, and all six artifacts are covered. Reject removal of the appendix switch, absolute paths, missing declared styles or bibliography, unresolved references or citations, undeclared fonts, clipping, and developer-only packages.

**Step 2 — implement:** Use the Task 12 source commit as sidecar provenance. Correct the hard-coded R5 preamble. Build with PDFLaTeX through `latexmk` using the pinned TeX Live generation and declared bibliography processor. Make `--check` materialize and verify source bytes at `source_commit`. Each sidecar records Markdown and LaTeX hashes, source commit, exact tool versions, profile hash, entry point, build command, build time, source-package hash, source-manifest hash, and PDF hash. Produce one deterministic, self-contained source package per artifact that builds offline without shell escape, private fonts, hidden dependencies, stale auxiliary state, conversion, or files outside the package. Keep double-build and text-structure checks. Add committed-PDF rasterization or a separate deterministic QA command; `--png` source rendering alone is insufficient.

**Step 3 — build in pinned environment:**

```powershell
$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'
& $PY scripts/build_pdfs.py
& $PY scripts/validate_math_source.py
& $PY tests/test_math_pipeline.py
& $PY scripts/validate_pdf_math.py
& $PY scripts/build_pdfs.py --check
```

**Step 4 — visual QA:** Build twice with byte identity, reject unresolved references or citations and overfull boxes above the profile-declared tolerance, and require embedded fonts with no Type 3 fonts. Verify extracted structure, absence of rasterized text and active JavaScript, links, page order, glyphs, and source-package clean builds. Render every page of all six committed PDFs at readable resolution. Inspect formulas, missing glyphs, clipping/overflow, blank pages, tables, links, headings, page numbers, and status pages. Record every artifact hash, package hash, page count, rendered-page count, exact build/runtime versions, issue, and disposition in the QA record. Use the PDF skill and inspect every page, not a sample.

**Step 5 — artifact commit:** Regenerate the manifest last, verify no source drift, and commit `build: regenerate verified publication PDFs`.

The only final compatibility claim permitted by this task is: `A venue-neutral, generic arXiv-compatible two-column technical paper with full-width front matter and single-column technical appendices.`

## Task 14: Run the complete adversarial and recursive mutation program

**Files:**

- Modify: `tests/schema-mutations/mutation-spec.json`
- Modify: `scripts/validate_recursive_mutations.py`
- Create: `docs/project-closure/r7e-sol/R7E-SOL-ADVERSARIAL-REPORT.md`
- Modify all new fixture files as required.

**Step 1:** Make every mandatory attack durable: stale/omitted topology; self-promotion; literal gradient; div/curl without field; transition-as-correctness; omitted reread; closure-as-uptake; hidden burden deletion; unauthorized global revision; strict soundness from admissibility; tawātur by count/popularity; fiṭrah coordinate; mental-to-external entailment; OSM identity collapse; argument-map contradiction; unsafe created wording; witness overclaim; unapproved formula spans; historical-record overwrite; collapsed identity levels; missing activation/evaluator version; indicator-only applicability; binary-only evaluation; later evidence relabeled as `t1`; false live capture; unfixture-tested accepted contract; missing authoring orthing; retroactive conformity rewrite; delta-free reopen; duplicate idempotency output; copy-inflated recurrence; threshold-as-proof; v0 automatic mutation; placement-as-authorization; outline-as-runtime; turn-as-orthing; gate-before-capture; claimant indeterminacy promoted to episode irresolution; frontier/reference-corpus collapse; comparator auto-reopen; closed-assessment auto-requeue; episode-ID independence; recurrence promoted to causation; retrospective-locus collapse; forced proposal; assessment/proposal/authorization/application collapse; legacy proposal provenance laundering; writeback actuation self-validation; Somnus/Hermes implementation or learning overclaim; C1/C2/C3 collapse; shared-type-as-transport; actor/ledger erasure; receipt-as-adoption/execution; recipient applicability copied from source; transclusion semantic-identity overclaim; multi-operator independence/tawatur/truth promotion; collective dissent erasure; projection completeness overclaim; and distributed-runtime overclaim.

**Step 2 — prove each attack is rejected:** Run every new focused test against its valid control and invalid mutation. The report records command, mutation ID, intended invariant, exit code, and result. A phrase-presence-only rejection is insufficient where structured semantics are available.

**Step 3 — run recursive mutations:**

```powershell
& $PY scripts/validate_negative_fixtures.py
& $PY scripts/validate_recursive_mutations.py
```

**Step 4 — reviewer:** A fresh Sol reviewer attempts counterexamples and checks for false negatives/false positives. Fix every blocker, then commit `test: close R7E semantic mutation gaps`.

## Task 15: Run the exact pinned full suite and clean-clone candidate proof

**Files:**

- Update: `docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json`
- Create: `docs/project-closure/r7e-sol/R7E-SOL-CLEAN-CLONE-VERIFICATION.md`
- Update: `docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml`
- Update: `docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md`

**Step 1 — local full suite:** Extract and execute every `.github/workflows/validate.yml` command in order under the pinned venv. Record the exact command count. The final manifest regeneration must leave no diff. Publication-profile validation, LaTeX regeneration parity, source-package validation, clean unpacked package builds, PDF conformance, and all-page rendering must pass alongside `build_pdfs.py --check`. Record any Windows UTF-8 wrapper without altering the underlying validator.

**Step 2 — final whole-branch review:** A fresh Sol reviewer inspects `cbab147..HEAD`, every finding disposition, every PR #12 hunk disposition, source boundaries, math sources, PDFs, and tests. Resolve all blocking findings.

**Step 3 — clean clone:** Push the review branch only after the local gate, clone it into a new explicit directory, create a new venv from `requirements-ci.lock.txt`, rerun the exact full suite, regenerate LaTeX, build each source package from a clean unpacked directory, rebuild/check PDFs, rasterize and inspect all pages, and confirm `git status --porcelain` is empty. Do not reuse caches or untracked control artifacts as evidence.

**Step 4 — closure commit:** Update records with immutable commit/hash evidence, regenerate state and manifest, run the full suite once more if the records affect it, and commit `docs: record clean-clone R7E Sol verification`. The closeout names exact normative/core files; crosswalks to existing episode/verdict/evidence/residual/action/actor-handoff/represented-standard owners; claimant-level and episode-level identity behavior; activation/evaluator versions; fixture counts by class; contract-authorship mode; mutation counts; whether recurrence was implemented as a direct reference operation or only specified/validated; anchor/reference/comparator and independence behavior; R7E capture mode and missing evidence; somnus run/assessment fixture IDs, reopening and idempotency results; retrospective defect loci; assessment/intervention/proposal/authorization/application/outcome separation; legacy versus grounded proposal provenance; no-change fixtures; three collective modes, transclusion levels, local-adoption/authorization and privacy/security boundaries; outline-only candidates/adoption profiles and downstream owners; explicit absence of skill package, external repository/network/shared service, cron, writeback engine, transclusion transport, automatic patch, or external runtime mutation; and successor triggers for live capture, scheduling, conflict detection, replay, verdict decomposition, governed proposal/apply/revert, later outcome evaluation, and federated/council runtime evidence. End with the waking/somnus/frontier/ledger and collective local-re-orthing distinctions intact.

## Task 16: Perform the authorized protected integration cascade

**Preconditions:** Root metadata still reports `gpt-5.6-sol`; all findings terminal; all tests and attacks green; math/PDF/clean-tree/clean-clone gates green; no owner-only blocker; exact live PR topology unchanged except expected review-branch commits.

**Step 1 — review branch to PR #12 branch:** Push `review/r7e-sol-independent-repair`, open a non-draft PR into `candidate/r7e-orthing-supplementation`, wait for required CI, verify exact heads, merge by ordinary merge commit without squash/force, and rerun/wait for PR #12 CI.

**Step 2 — serial child-to-parent merges:** For each step, refresh model identity, branch heads/bases, mergeability, protection, and required checks; merge only after green; then wait for the parent PR's CI before proceeding:

1. PR #12 → PR #11
2. PR #11 → PR #10
3. PR #10 → PR #9
4. PR #9 → PR #8
5. PR #8 → protected `main`

Stop before the next write/merge on any red check, stale head, unexpected commit, changed topology/protection, surviving semantic attack, model substitution, or genuine owner-only blocker. Preserve exact state and leave all affected PRs unmerged.

**Step 3 — merged-main proof:** Fresh-clone merged `main`, install only the exact lock, rerun the complete suite, regenerate LaTeX, build every source package from a clean unpacked directory, rebuild/check all PDFs, rasterize/inspect every page, verify the clean tree, and record the actual main merge SHA.

**Step 4 — non-self-referential verification record:** If the merge SHA could not be included beforehand, create a protected follow-up branch/PR containing the final merged verification record, generated state, and manifest. Run CI, merge normally, then read back protected `main` and verify the record names the earlier merge and its own follow-up commit honestly.

**Final evidence:** Report exact commits, PR merge commits, CI run URLs/conclusions, full-suite commands/results, PDF hashes/page counts/visual record, clean-clone paths and tree status, adopted/revised/dropped/provenance-only R7E hunks, and any claims explicitly not established.
