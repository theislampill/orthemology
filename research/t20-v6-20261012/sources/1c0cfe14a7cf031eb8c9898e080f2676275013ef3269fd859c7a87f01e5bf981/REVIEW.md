# Independent review: advanced-alignment recognition guard

## Verdict

[checker] **Confirmed, bounded conformance defect at pinned commit c86b3c6673147b8802fe222373a165a37d4d24a8.** The actual custom `validate_instance` path and both unmodified custom CLI entrypoints accept synthetic records with `alignment_state = alignment-advanced` and `recognition_strength = none`, `weak`, or `medium`. The complete declared JSON Schema rejects those same records for precisely `recognition_strength`; its otherwise-identical `strong` control passes.

This is more than an isolated `schema_errors` observation. It is not evidence that the entire repository CI, compiled runtime, downstream consumers, or a live model accepts the records.

[decision] Classification: confirmed checker/schema conformance defect, requiring owner remediation before relying on this checker to enforce this acceptance-state guard. No release-blocking verdict, release readiness claim, or audit closure is made in this research review.

## Controlled result

| Record | `validate_instance` errors | Main custom CLI | Compatibility CLI | Complete JSON Schema |
|---|---:|---:|---:|---:|
| Unchanged embedded positive | 0 | exit 0 | exit 0 | exit 1: unrelated routing-gate mismatch |
| Only original reason category changed to 1 | 0 | exit 0 | exit 0 | exit 0 |
| Advanced alignment, strong recognition | 0 | exit 0 | exit 0 | exit 0 |
| Same control, medium recognition | 0 | exit 0 | exit 0 | exit 1: recognition only |
| Same control, weak recognition | 0 | exit 0 | exit 0 | exit 1: recognition only |
| Same control, no recognition | 0 | exit 0 | exit 0 | exit 1: recognition only |

Each candidate custom CLI output reports one expected-valid IR instance, no ignored files, all 54 embedded negative samples checked, and `diagnostic IR instance integrity: PASS`. Thus the acceptance was not caused by ignoring the candidate or by expected-invalid-fixture handling.

The unchanged official `tests/ir-fixtures/valid/field-witness-closure-graph.json` also passes the custom CLI. The unchanged embedded self-check suite exits 0.

[fixture] The official embedded positive has `reason_category: 3` and `routing_gate: open`, which conflicts with a separate conditional in the published schema (`allOf[8]`). Its schema failure is recorded, not suppressed or attributed to the recognition mutation. A separate control changes `reason_category` to 1, sets alignment to advanced, and recognition to strong. That entire record passes the complete schema. Only recognition strength changes in the three experimental records. This is explicit synthetic fixture surgery, not an empirical reassessment of a person or proof that every prose-level case interpretation is valid.

## Why this survives the full custom path

[source] `atomics/skill/references/diagnostics/diagnostic-ir.schema.json:1774–1792` has the advanced-alignment conditional requiring strong recognition. The complete schema checks fail at `allOf[17].then.properties.recognition_strength.const` and no other location in the three controlled variants.

[source] `atomics/skill/references/diagnostics/diagnostic-ir.md:1008–1060` also distinguishes advanced alignment and strong recognition and lists advanced alignment with any non-strong recognition as an invalid inconsistency. The finding is not based on inventing a stronger semantic rule than the pinned source states.

[checker] `tools/check_ir_instance_integrity.py:1602–1727` performs selective schema-adjacent checks. It does not evaluate all JSON Schema conditionals and lacks this particular guard. `integrity_errors` at lines 2223–2325 checks catalogue, map, source-basis, and post-render consistency, without this guard. `validate_instance` at lines 2347–2358 concatenates those two result lists. `main` calls that path and does not invoke a general JSON Schema validator.

[checker] `tools/check_diagnostic_ir_catalogue_integrity.py` imports the same `main`; running it is not a second independent schema validation stage. The pinned CI workflow calls both custom entrypoints at lines 83–84, but this review did not run or make claims about the rest of that workflow.

## Dependency reconstruction and provenance limits

The author supplied pinned source copies and `SOURCE_BINDINGS.json`. I independently checked SHA-256, Git blob SHA-1, and byte counts of all 28 supplied entries, then copied and rehashed the 12 inputs needed for the bounded replay. I did not duplicate remote downloads or independently re-fetch the commit-to-blob mapping.

The generated `compiled-module-map.json` is not provided as a committed complete runtime artifact. I independently reconstructed only the two entries needed here, M1-self-refutation and M8-reductio, using the pinned `BUNDLE_SOURCES`, `load_source_doc`, and the metadata expression in `tools/build_compiled_runtime.py:1895–1915`. These entries exactly match the author's independently produced two-entry projection. No complete runtime build was performed and no freshness claim is made.

The projection is sufficient for this exact replay: the inspected integrity function only reads a matched module's map entry and nonempty bundle path; the target records match precisely those two owners; both real CLIs and all their embedded checks run successfully. Removing either entry makes the full `validate_instance` control reject with that missing owner's map-resolution error. Reconstructing the needed dependency does not substitute a stub validator or bypass its map lookup.

## Preserved positive boundary

[checker] Full `validate_instance` still rejects each independent mutation:

- Runtime closure moved to the interlocutor field: closure operator must be `𝒞(Ψᴺ)`.
- Transfer marked as guaranteed: transfer mode must be `coupling-attempt`.
- Transfer made to originate from the interlocutor field: transfer source must be `Ψᴺ`.

The source/model distinction remains intact in these tested boundaries. Neither a checker pass nor rejection establishes actual knowledge, willingness, prior acquisition, recovery/restoration, or warrant. The defect is a missing enforcement check on an already-declared relation between labels.

## Required remedy and regression evidence

No patch was applied.

1. The checker owner should enforce the existing advanced-alignment/strong-recognition requirement on the real validation path, or explicitly reconcile an intended contract change in the schema and prose. Do not silently relax the source rule to accommodate the current false pass.
2. Add complete-schema-clean positive and negative fixtures: advanced/strong must pass; otherwise-identical advanced/none, advanced/weak, and advanced/medium must fail through `validate_instance` and the actual CLI.
3. Retain the unchanged baseline results and reconcile its independent category-3/open-gate mismatch separately. Adding complete JSON Schema validation without addressing this baseline would newly fail current embedded positives; a wholesale validator swap is not established as a safe one-line remedy.
4. Preserve the tested runtime/interlocutor closure and non-guaranteed-transfer checks.

This closes the uncertainty over whether the candidate is merely a raw-helper omission or reaches the actual custom CLI. It does not close repository-wide conformance, generated-runtime correctness, real-user semantics, source-to-knowledge conclusions, integration, or T20.

## Commands, files, and evidence

Primary independent command, run successfully on 2026-10-09 UTC:

`python -B noetic-guard-peer-review-20261009/replay_peer.py`

The driver invokes both unchanged copied CLI scripts with `--file`, the main checker with `--samples-only`, and a separate complete-Draft-2020-12-schema process on the exact same fixture files. Every command, exit code, stdout, and stderr is in `logs/*.json`. Environment: Python 3.12.14, jsonschema 4.26.0.

- `PEER_REVIEW_RESULTS.json`: machine-readable results, mutations, fixture hashes, map counterchecks, and limits.
- `SOURCE_BINDINGS.json`: the 12 copied pinned inputs with Git blob hashes, SHA-256, and byte counts.
- `replay_peer.py`: independent replay driver.
- `validate_full_schema.py`: complete-schema process with explicit success/failure exit code.
- `pinned-inputs/peer-fixtures/`: six records tested through both routes.
- `pinned-inputs/skill/compiled-module-map.json`: explicitly labelled two-entry dependency projection.
- `logs/`: per-command evidence.

Key SHA-256 values:

- Pinned checker: `ea6630a53ce8c77d6cc3102ae6ffd5aba0dc84539f1ffe5350fbc1aa4d9c4d1a`
- Pinned schema: `c2cac1a403d64f27bb7597c4e7e0d7b3f2663e91303960ba68817608e8ffd566`
- Advanced/strong control: `dbed06d7dc3be2668cba49765dbe889eba53760bf05460f0887292ec0e0cd4e7`
- Advanced/none candidate: `020c199dc1f4051581e7f018d428c2139d723a52ae9e090b29f8a9445e9c214f`

No protected repository files were modified. All generated replay files are isolated in this peer-review directory. The next smallest safe action is to retain this evidence and request an owner-scoped checker regression fix if implementation is desired; no source repair is authorized or performed by this review.
