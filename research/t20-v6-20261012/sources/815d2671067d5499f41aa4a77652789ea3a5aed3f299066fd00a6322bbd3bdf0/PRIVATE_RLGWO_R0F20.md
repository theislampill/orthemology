# R0F20 — T20 live checkpoint publication and future research re-entry

**Type:** Research-Lab-Grade Work-Order (PRIVATE OWNER HANDOFF, NOT A GITHUB ISSUE)  
**Owner / decision authority:** repository owner; Codex may implement on a new branch only after owner supplies this archive.  
**Programme:** Orthemology v5 / T20 ACTIVE (no T21 or scientific closure).  
**Source freeze:** 22 numbered checkpoints plus one unnumbered later warranted-discrimination research-and-Lean supplement.  
**Current live Git ancestor:** `3a0bdeaa1394c656245cae9599adcb143e885059` (Oct 8; PRs #30 #31 #32 merged).  
**Category:** low-reasoning-cost custodial publication, indexed constructive research, not theory adjudication or adoption.

## RLGWO problem and evidence

The live repository already contains the frozen Oct 7 T17–T20 integration (262 status records / 3,828 source records). Subsequent T20 checkpoints 1–22 and the later S01 research supplement are not collectively navigable in that frozen tree. Reintegrating the entire T20 research and inherited predecessors would duplicate public scientific artifacts, consume excessive agent quota, and risk rewriting historical judgements. Dot requires a stable, commit-specific Git re-entry location for continued T20 investigations.

**Evidence:** the private `SOURCE_ARCHIVES/` contains exact original ZIP bytes; `inventory/CHECKPOINT_ARCHIVES.json` fixes input identities; `inventory/ALL_MEMBERS.json` binds every original member, its SHA-256, output status and selected projection; `inventory/PUBLIC_PROJECTION.json` fixes each Git-destined byte string. Source member coverage is exhaustive, but public source disclosure is deliberately scoped.

## Semantic ownership and invariants

- `docs/provenance/v5-successors/RESULT_STATUS.json` and existing T20 guide retain authority for the **frozen** Oct 7 scientific scope. Do not replace, renumber, reinterpret, or silently expand 262/3,828 canonical counts.
- The new root `research/t20-live-20261009/` is a **supplementary public reader** under a new namespace, not an alternative canonical owner of accepted v5 science.
- Checkpoint IDs CP01–CP22 are ordered historical preservation increments; S01 is unnumbered and expressly additional. Checkpoints are additive/noncumulative; each private ZIP stands on its own, and no archive is substituted for the complete set.
- Published source bytes are either exact (`projection:exact`) or `projection:machine_locator_redacted`. Never equate projected redacted bytes with original source evidence. Private logs/raw source text remain private.
- Keep distinct WRITTEN_MATHEMATICS, FINITE_REFERENCE_TESTED, FRESH_LEAN_KERNEL, SOURCE_ASSESSMENT, OWNER_ADOPTION, EXTERNAL_REVIEW, CURRENT/RELEASE status. No new status promotions from packaging or CI.
- S01 kernel result is a warranted-discrimination/residual-certificate result within its assumptions. Its adaptive Bellman minimum-cost inquiry theorem has written proof and finite tests **not a claimed Lean theorem**. Do not conflate.
- Preserve existing published Sixth and T7–T20 trees byte-for-byte except the globally generated release-manifest hash file, if required by the existing acceptance contract.
- No owner-authorised merge/auto-merge/release/term adoption; no forced push; PR only.

## Authorised actions (bounded)

1. Verify the 23 exact ZIPs, their original members and the candidate public bytes **without running archive-supplied scripts** (`python3 tools/verify_package.py`).
2. Inspect the owner-publication warnings and private-locator redactions; refuse unresolved privacy, third-party source text or licensing hazards (no blanket endorsement).
3. Verify the live repository is a clean descendant of the fixed baseline and that the frozen T20 baseline file has the pinned Git blob SHA. Resolve changed baseline ONLY with owner approval; no rebase sweep.
4. From the clean current-main ancestor, perform a read-only dry-run, then create a NEW integration branch before applying the already-prepared additive publication projection with `tools/apply_to_repo.py`. It must write solely under `research/t20-live-20261009/` and must fail for any nonidentical existing path.
5. Stage that root, regenerate `docs/provenance/RELEASE-MANIFEST.sha256` using repository-native `python3 scripts/make_manifest.py` after `git add`, then stage the manifest. No other governed registries automatically changed.
6. Focused smoke checks + required GitHub CI once; fix narrowly and rerun only actually invalidated scopes. Do not perform a new entire-tranche ingestion or scientific theorem reproduction campaign to qualify copy/preservation.
7. Create **one** new PR for owner/independent review; do not merge. Provide exact head SHA, diffstat, emitted target identities, focused verification, known public omissions, redaction ledger and CI links if available.

## Out of scope / hard prohibitions

- No automated GitHub issue posting, no RLGWO issue filing, no main edit, no direct push to main, no automatic merge.
- No rewriting PR31 or the frozen Oct7 main records. No new `RESULT_STATUS`, `SOURCE_MAP`, `SUPERSESSION`, or `EVIDENCE_BINDINGS` rows without a separate specifically reviewed semantic import contract.
- No pushing `SOURCE_ARCHIVES`, private handoff documents, unfiltered `.log/.txt/.gz`, third-party source bodies, toolchain caches or machine-user locators to public GitHub.
- No generalised scientific novel-theorem claim, retrospective review score, inflated Lean scope, confidence promotion or closure.
- No `pip install`/Lean/mathlib downloads for staging; dependency installation only if a **narrow changed-surface validation** explicitly needs it and owner permits cost.

## Dependency and currentness / re-entry

`M00` (verified current/main) precedes manifest attestation `M01`, public boundary `M02`, no-drift local dry-run `M03`, deterministic application `M04`, native generated manifest `M05`, bounded checks `M06`, Git PR `M07`, independent review `M08`, and owner-controlled merge `M09`. Dot re-entry `M10` is blocked until actual merged SHA and reviewed public scope. `DAG.json` carries exact prerequisites, stop conditions and deliverables.

## Discriminating tests and negative controls

- Each of 23 source ZIP SHA-256 values matches the private register; decompression has no bad member, zip-slip or symlinks. All 2821 original bytes compare to manifest.
- Every projected source's output bytes match the exact registered SHA-256; public redaction labels agree with underlying transformations. An altered archive member or projected file must be rejected.
- A synthetic clean Git descendant accepts dry-run and copy. A dirty worktree, missing frozen source, divergent main, path collision and content hash drift must each be rejected without overwriting historical work.
- New Git tree contains only the declared additive root plus the deterministic `docs/provenance/RELEASE-MANIFEST.sha256` rewrite; all legacy source paths remain unchanged.
- Public overlay scan finds no absolute private machine locator or credential-token pattern under the declared filter. All `source_only` and raw original ZIPs remain outside public root.
- S01 native finite verifier runs successfully on its isolated unmodified extracted private source (where Python available). Lean recheck has its own original prerequisites and must not be marked completed merely because historical logs are present.
- Current Git HEAD stays traceable to the accepted PR31/PR32 baseline. PR remains unmerged until separately approved.

## Closure authority / acceptable PASS scope

**Custody/presentation PASS** only if all 23 ZIP identities, member dispositions, precomputed public files, source-to-public manifests, Git diff/collisions, focused tests and required CI are independently checked for the exact PR head. A narrow copy-verified PR does **not** imply T20 research closure, formal proof audit, metaphysical truth, rights clearance, or owner merge. A failure or missing authorisation is HOLD with actionable affected cells; do not suppress it, invent PASS or spend quota on a full redevelopment.
