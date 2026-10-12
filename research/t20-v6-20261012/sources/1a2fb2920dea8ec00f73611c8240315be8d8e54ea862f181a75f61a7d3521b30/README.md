# Accepted heat, affine, and graded-operator evidence

Fresh additive preservation, 10 October 2026 UTC. This archive preserves accepted ordinary mathematical research and its scoped independent reviews. It does not rebuild a baseline, integrate into protected state, publish or upload anything, close T20, or incorporate the active Lean truncation work.

## Accepted contents and exact authority

- `evidence/moment-evolution-source-comparison-20261010/RESULT.md`: bounded primary-source comparison; full-polynomial square-positive heat paths without representation on an initial interval or any prescribed finite horizon after changing the initial functional; valid-initial-law boundary; affine transport plus V-qualified killing.
- `evidence/heat-truncated-certificate-diagnostic-20261010/RESULT.md`: separate explicit rational degree-four diagnostic in three variables. Its 35 moments are not asserted to extend to a full square-positive functional.
- `evidence/heat-truncated-certificate-diagnostic-20261010/FILTERED_OPERATOR_NOTE.md`: final, explicitly linear T=mI+N (m>0, N strictly degree-lowering) obstruction. The prior note and exact clarification are preserved alongside it.
- `evidence/heat-transport-obstruction-independent-review-20261010/`: all written reviews, receipts, scripts, outputs and logs. Full-page source renderings are referenced by hashes but excluded.

The final reviews accept exactly their recorded scopes. Historical author statements saying review was pending and the comparison's then-pending wording are unchanged documentary evidence, not the current final review disposition. The later `REVIEW_RECEIPT.json` and `FILTERED_OPERATOR_REVIEW_RECEIPT.json` establish the bounded accepted dispositions without rewriting earlier records.

The uniform assertion reviewed is specifically Corollary 3.22 of arXiv:2211.04416v3. The pointwise Theorem 3.21 is not refuted. No blanket manuscript rejection or field-priority claim is made. The affine result assumes the accepted Theorem V, continuous affine velocity, and local uniform SOS radial domination; no nonlinear transport or diffusion-plus-killing conclusion is included. The graded result requires linearity, positive scalar leading action at every grade, and distinct nonnegative/SOS cones. Its Gaussian averaging projection control is outside these hypotheses.

## Inheritance

Minimal accepted proof material for G/V is included: their full proofs and source/inheritance records; their independent review prose and receipts; the tensor full-vector exhaustion/classification proof and review; and scalar/finite-channel predecessor proof texts used as historical background. These are accepted dependencies, not new reruns of older campaigns. Historical receipt references to omitted inherited logs, scripts and snapshot copies are explicitly listed in `HISTORICAL_RECEIPT_REFERENCES.json`. Included references are hash-checked; omitted inherited campaigns are not silently counted as fresh replay. The old G/V control totals remain historical. This packet's claim is the accepted heat/affine/operator scope conditional on those accepted dependencies.

## Source rights, reading boundaries, and portability

No complete modern primary PDF, full extracted primary text, full-page screenshot, or author-hosted HTML is redistributed. `EXTERNAL_PREREQUISITES.json` identifies 11 omitted artifacts with original paths, URLs, hashes, byte lengths, and purposes. The original `SOURCE_MANIFEST.json` and `READING_BOUNDARIES.md` are preserved verbatim. Inherited classical theorem URLs and exact reading boundaries are recorded; no local hash is invented where earlier source checks did not claim one.

Full fresh replay requires an explicit external root providing the exact omitted artifacts at their original relative paths. A portable recipient must retrieve the version-specific PDFs/HTML and provide or recreate the exact text and image derivatives. Derivative bytes can depend on extraction/rendering versions; a mismatch fails rather than being silently waived. Only two source artifacts, the v3 PDF and text, are consumed by the historical review control script. The preservation wrapper additionally verifies all 11 omitted source artifacts. The original script's 11 input-integrity checks therefore remain operational. The sources are copied only into the external replay sandbox, never into this archive.

Retained local source verification is not a fresh network retrieval, a new source reading, or proof that every archival source will remain reachable. Classical existence/representation theorems remain external mathematical inputs, not outputs of finite Python tests.

## Replay

Requirements: Python 3.12 and SymPy 1.14.0 (versions of this preservation run). Nothing is installed automatically. Extract the archive to a fresh directory. From its top-level directory run:

    python3 replay.py --external-root /path/to/retained-or-retrieved-source-root --output-dir /path/to/new-output-directory

The output directory must not exist and must lie outside the package. Without the exact external prerequisites the command writes `BLOCKED_MISSING_EXTERNAL_PREREQUISITES` and exits 2 before claiming mathematical replay. This is intentional fail-closed behavior. The successful receipt reports a replay with explicit external prerequisites, not a wholly self-contained source replay.

All three contained original mathematical Python files are executed unchanged in a disposable copied tree: the review controls and the two byte-identical copies of the diagnostic script. All regenerated result JSON files must match their frozen originals byte-for-byte. The preservation wrapper is additional integrity orchestration, not an additional theorem checker.

Fresh counts are separated:
- 52 named algebraic/finite-dimensional review controls
- 11 original review input-integrity checks, separately counted
- One distinct explicit diagnostic, executed twice from its two preserved copies; all assertions pass, including inverse heat on all 35 basis vectors; no arbitrary combined assertion total is claimed
- Additional package-manifest, original-copy, external-source, receipt-binding, and exact-linearity-delta checks, separately named in the replay receipt
- No new numeric tests for the universal filtered-operator proof, whose evidence is ordinary independent proof review

`MANIFEST.json` binds every payload file except itself. The external fresh-extraction receipt binds the completed ZIP's SHA-256 and size, records successful ZIP CRC testing, contains the actual replay results, and records original/prior-archive preservation. A manifest proves integrity, not theorem truth. No formal kernel or active Lean result is claimed.
