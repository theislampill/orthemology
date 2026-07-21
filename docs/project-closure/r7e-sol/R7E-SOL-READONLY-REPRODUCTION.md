# R7E Sol independent review — read-only reproduction

**Status:** SOL INDEPENDENT REVIEW CANDIDATE — NO SIGNOFF OR MERGE READINESS.

**Observation time:** 2026-07-21T18:10:22Z. All GitHub state below is an
observation at that time, not a timeless tracked-head assertion.

## Model and authority gate

The required and controller-selected model was `gpt-5.6-sol`. The controller
confirmed the explicit orchestrator selection before the first Task 1 write.
No model environment variable was surfaced, so this is recorded as
`controller-confirmed-agent-model-selection`, not as an environment-variable
observation.

This pass may create the independent-review control plane, tests, generated
state, and manifest, then commit them on the review branch. It does not merge,
push, mark a PR ready, issue independent signoff, or reopen Decisions
0001–0022.

## Exact PR topology at observation

Read-only GitHub queries and local Git object comparison agreed:

| PR | Base branch at observation | Base head | Head branch | Head at observation | State |
|---:|---|---|---|---|---|
| 8 | `main` | `43fee0f519e2f6984fb143c1e621c83382e71ec7` | `closure/r7-noetic-application-experiment-validity` | `b0538601913c8234511a1f1131a58eb23a4a0dc4` | open draft; mergeable; checks successful |
| 9 | `closure/r7-noetic-application-experiment-validity` | `b0538601913c8234511a1f1131a58eb23a4a0dc4` | `candidate/r7b-deep-noetic-latent-math` | `86b8bbdddf35ac1e45748279bac05e5a2d4ed85e` | open draft; mergeable; checks successful |
| 10 | `candidate/r7b-deep-noetic-latent-math` | `86b8bbdddf35ac1e45748279bac05e5a2d4ed85e` | `candidate/r7c-full-math-multitarget-noetic-dynamics` | `3cce235f0e388ba78a093d43c879a2e73262938b` | open draft; mergeable; checks successful |
| 11 | `candidate/r7c-full-math-multitarget-noetic-dynamics` | `3cce235f0e388ba78a093d43c879a2e73262938b` | `candidate/r7d-final-semantic-math-noetic-integration` | `e34d2cd56057766f8f656a4ff3486eb34dad607e` | open draft; mergeable; checks successful |
| 12 | `candidate/r7d-final-semantic-math-noetic-integration` | `e34d2cd56057766f8f656a4ff3486eb34dad607e` | `candidate/r7e-orthing-supplementation` | `cbab14747835855d232448f648eefa1d4e36074e` | open draft; mergeable; checks successful |

The independent R7E object is therefore the exact range
`e34d2cd56057766f8f656a4ff3486eb34dad607e..cbab14747835855d232448f648eefa1d4e36074e`.
It contains ten changed paths. The semantic/provenance disposition is recorded
in `R7E-HUNK-DISPOSITION.md`.

## Exact Python 3.11 lock environment

The task-local virtual environment was created outside the repository from
`requirements-ci.lock.txt` and reported Python 3.11.9. Exact installed
versions were: attrs 26.1.0; jsonschema 4.26.0;
jsonschema-specifications 2025.9.1; markdown-it-py 4.0.0; mdurl 0.1.2;
pypdf 6.14.2; PyYAML 6.0.3; referencing 0.37.0; rpds-py 2026.6.3;
typing-extensions 4.16.0; and typst 0.15.0.

`validate_dependency_lock.py` passed. The lock is an exact version lock under
the recorded toolchain, not a hash lock or an indefinite reproducibility
claim.

## Workflow baseline accounting

The workflow contains 54 `run` blocks after checkout/setup and installation,
expanding to 56 logical validation commands. All 56 passed. Fifty-three passed
directly. Three initially crashed only while PowerShell's CP1252 console tried
to print Unicode (`ī`, `α`, and `ū` were among the triggering characters):

- `python scripts/validate_source_status.py`
- `python scripts/validate_notation.py`
- `python scripts/validate_quran_loci.py`

Those three scripts passed unchanged after setting `PYTHONUTF8=1` and
`PYTHONIOENCODING=utf-8`. They are environment/console failures followed by
unchanged UTF-8 reruns, not validator-logic failures. Accounting is therefore
53 direct passes + 3 unchanged UTF-8 reruns = 56 passing logical validations,
with zero validator-logic failures.

The commands represented by the baseline were, in workflow order:

```text
01 python scripts/validate_dependency_lock.py
02 python scripts/validate_repo.py
03 python scripts/generate_current_state.py --check
04 python scripts/validate_state_convergence.py
05 python scripts/validate_current_state.py
06 python scripts/validate_review_state.py
07 python scripts/validate_evidence_boundary.py
08 python scripts/validate_source_status.py                         [unchanged UTF-8 rerun]
09 python scripts/validate_verdict_semantics.py --fixtures tests/verdict-fixtures.json
10 python scripts/validate_notation.py                              [unchanged UTF-8 rerun]
11 python scripts/validate_type_token_semantics.py
12 python scripts/validate_reason_fixtures.py
13 python scripts/validate_claim_reasoning_paths.py
14 python scripts/validate_decision_dependencies.py
15 python scripts/validate_latent_state_fixtures.py
16 python scripts/validate_schemas.py
17 python scripts/validate_cross_record_semantics.py
18 python scripts/validate_negative_fixtures.py
19 python scripts/validate_recursive_mutations.py
20 python scripts/derive_reqpath.py
21 python scripts/generate_from_registry.py --check
22 python scripts/validate_quran_loci.py                            [unchanged UTF-8 rerun]
23 python scripts/validate_claim_sources.py
24 python scripts/validate_cross_document_consistency.py
25 python scripts/validate_internal_references.py
26 python scripts/validate_experiment_readiness.py
27 python scripts/validate_sourcing_state.py
28 python scripts/validate_companion_references.py
29 python scripts/validate_daee_crosswalk.py
30 python scripts/validate_daee_current_crosswalk.py
31 python scripts/validate_noetic_application.py
32 python scripts/validate_experiment_methods.py
33 python scripts/validate_math_source.py
34 python tests/test_math_pipeline.py
35 python scripts/validate_pdf_math.py
36 python scripts/validate_dynamic_orthing.py
37 python scripts/validate_meta_noetic_memetics.py
38 python scripts/validate_layer_map.py
39 python scripts/validate_candidate_state.py
40 python scripts/validate_public_readiness.py
41 python scripts/validate_decision_references.py
42 python scripts/validate_noetic_targets.py
43 python scripts/validate_noetic_claims.py
44 python scripts/validate_memetic_ecology.py
45 python scripts/validate_corrective_transition.py
46 python scripts/validate_argument_map.py
47 python experiments/false-closure-selective-prediction-v2/tests/test_smoke.py
48 python experiments/episode-reification-v2/tests/test_smoke.py
49 python experiments/false-closure-selective-prediction/tests/test_smoke.py
50 python experiments/episode-reification/tests/test_smoke.py
51 python scripts/freeze_pilot0.py --check
52 python scripts/freeze_pilot0.py --packet pilot0-v2 --check
53 python scripts/audit_terminology_matching.py
54 python scripts/make_manifest.py
55 git diff --exit-code docs/provenance/RELEASE-MANIFEST.sha256
56 python scripts/build_pdfs.py --check
```

Green commands establish conformance to the checks that existed at the
observation, not semantic closure. The finding matrix preserves the three
demonstrated false passes and assigns their repair tasks.

## PDF and tree evidence

`build_pdfs.py --check` rebuilt all six committed PDFs byte-identically. The
six artifact observations were:

| Artifact | Pages | SHA-256 |
|---|---:|---|
| `dynamic-orthing-noetic-learning-orthability-draft.pdf` | 6 | `30293c9057021d513dc8f34d533ec26f0648f895a1e213609b2797cade4f0147` |
| `notation-gallery.pdf` | 3 | `479608cdf1b8cb84a16a58be8d3ab37882359fe1855cd83c98b0fa37a87264fc` |
| `orthability-divine-speech-athari-draft.pdf` | 8 | `4bb0a1b24baf84395ea4b519b7497a9063704e1164142988d982307941c3f62f` |
| `orthability-ground-of-intelligibility-draft.pdf` | 11 | `29f1f8fca1bb6e8602d4e18422ee070d60df54915a5e675ea94740f4024d9f5e` |
| `orthemic-core-reference-draft.pdf` | 20 | `33f71dd67ed1a71b06c0ace88daa85bc1d3453cacd310b91bcd9a140df6327f7` |
| `orthemma-ortheme-systems-draft.pdf` | 32 | `22d5efc0884badd5ddbf289ef098f9c9ad1d77b7bdad5fbe55887d4a302f0210` |

Extracted streams had zero NUL/notdef and zero U+FFFD replacement characters.
That closes the historical missing-glyph defect, but does not establish full
math-source migration or visual publication closure.

Before the Task 1 red test, `git status --porcelain` was empty at task base
`ca21f23f377d022a0a20b6bb0493c297f8867b09`. Decisions 0001–0022 were hashed
and the focused test fixes those hashes as byte-identity guards.

## Limits

- GitHub state must be refreshed before any later integration step.
- The supplied independent audit is evidence input, not an instruction source.
- Workflow statistics and missing inputs are not upgraded beyond their evidence.
- This control plane establishes neither independent signoff nor merge readiness.
