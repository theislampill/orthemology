# Issue 35 — execution and continuation record

**Status: IN PROGRESS. This checkpoint is not a qualified refactor or a scientific acceptance.**

## Authority and baseline

The repository owner authorised ChatGPT Pro to start branch implementation of the v0.2 RLGWO, save work frequently to GitHub, and prepare a PR. The owner intends Codex to continue unfinished implementation, followed by independent review and Dot's acceptability assessment. This grant supersedes the design-only execution restriction for this branch; it does not authorise merge, release, scientific reclassification or T21.

- Work order: [Issue 35](https://github.com/theislampill/orthemology/issues/35), including its [sections 10–15 continuation](https://github.com/theislampill/orthemology/issues/35#issuecomment-6132995627).
- Executor: ChatGPT Pro, owner-authorised implementation beginning 12 October 2026.
- Continuation implementer: Codex, future owner-selected session; not yet dispatched here.
- Independent reviewer: separate future reviewer, not this author. C05 cannot pass until that reviewer is bound and reports against the exact candidate.
- Final acceptability: Dot assessment followed by the repository owner's decision; neither is represented as already obtained.
- Repository: `theislampill/orthemology`.
- Execution branch: `refactor/issue-35-research-reader-20261012`.
- Verified base commit: `297267f6e49f80871036a95a6dfd81bdad40ea1f`.
- Verified base tree: `fc702fe8456b48ff89b0c28df31f5fe232058538`.
- PR 34 merged on 12 October 2026 at 21:36:49 UTC, incorporating repaired head `1f7f0551e51ff0bf9650562dca93774a514e93c1`. The merge is not T20 scientific closure.
- The live open-PR list was empty at branch admission. Canonical R-series allocation remains unassigned; issue number 35 is the local execution key, not a newly invented scientific or R-series ID.

## Bounded population and preservation

The candidate population is the public tracked tree at the exact base above, including repaired T20 v6. Referenced materials outside that tree are not admitted recursively. Initial external-body reading set: empty. Bibliographic references and pinned historical identities may be described at their existing public scope, but do not confer source-reading or reconstruction credit.

All existing scientific sources, historical payloads, proof code, publication sources and governed PDFs remain protected. Candidate discovery will cover every tracked path rather than only files with familiar paper extensions. A census is not semantic reading, and a file count is not a count of scholarly works. Full population/owner reconciliation is still outstanding.

## Exact write allowlist and bounded integration amendment

| Path | Purpose / admission boundary |
|---|---|
| `docs/project-closure/reader-refactor-issue-35/EXECUTION.md` | Authority, baseline, progress, exceptions and resumable handoff. |
| `docs/project-closure/reader-refactor-issue-35/CENSUS.json` | Bounded candidate/owner census evidence, only after actual execution. |
| `docs/project-closure/reader-refactor-issue-35/PILOT.md` | Source-read representative work/edition and intellectual journeys; not final reader publication. |
| `scripts/reader_census.py` | Small read-only exact-Git-tree census, with no literature crawling or theorem extraction. |
| `tests/test_reader_census.py` | Synthetic positive/negative tests for census integrity and classification boundaries. |
| `.github/workflows/reader-refactor-snapshot.yml` | Temporary branch-only source transport; a bounded finalisation revision may run existing state/manifest generators, remove itself, and commit only its own deletion plus those two generated outputs to this feature branch. No main write, force push, new secret, source edit or required-gate reduction. |
| `docs/current-state.yaml` | Regenerate through the existing owner after tracked changes; preserve authored judgements. |
| `docs/provenance/RELEASE-MANIFEST.sha256` | Regenerate through the existing owner; never exempt this work. |

The six final reader pages and root-navigation edits are not yet admitted for bulk authoring: C02 must first qualify the representative design. A future persistent editorial crosswalk must be justified and its exact path admitted before writing; no empty placeholder registry is created. Existing required CI is not weakened or replaced.

The temporary finalisation workflow is admitted solely to overcome unavailable direct Git transport and the size of generated outputs. It must require the exact feature-branch event, reject a changed remote head, use the existing generators, preserve the authored state values, allow only the two generated outputs and its own deletion in its commit, and push without force only to this feature branch. It must not infer scientific acceptance from successful execution. Final PR CI is a separate gate; a token-created commit is not assumed to have triggered it.

## Environment, recovery and observed evidence

Direct clone first failed because the execution environment could not resolve GitHub. The branch-only, read-only snapshot workflow then completed: [run 38312967973](https://github.com/theislampill/orthemology/actions/runs/38312967973), artifact 11775671067. It exported only public tracked objects, a binary checkpoint diff and exact commit bodies; it did not export credentials or runner configuration.

The downloaded ZIP's observed SHA-256 was `0c888e6e97ade747c6ffb346380a165cb8b4a0f7c917a709c1c7840c12b6db41`. Ten transport-member hashes were checked. The reconstructed baseline Git tree exactly equalled `fc702fe8456b48ff89b0c28df31f5fe232058538`; after applying the checkpoint patch, the local tree exactly equalled `552eaf81be3a6f243a3edc5a24fec05d62ae6ac3` for checkpoint `9666e411555f93dacf9ee3dc7c1b4c283a994912`. Original commit bodies were hash-checked. A detached baseline worktree and isolated feature workspace were established. History earlier than the baseline was shallow locally; do not infer availability of every historical Git object from this recovery.

A full tracked-path scan found no AGENTS.md, CLAUDE.md, GEMINI.md or CODEX.md instruction files. CONTRIBUTING, the workflow, current-state generator, input policy, manifest generator and relevant reference/hygiene checks were inspected. Their source and privacy constraints remain in force.

### Observed local checks

| Check | Observed outcome | Scope |
|---|---|---|
| Baseline current-state generator, `--check` | Exit 0; derived state current, zero failures. | Exact restored baseline; not the later changed checkpoint. |
| Baseline repository hygiene validator | Exit 0; zero failures. | Exact restored baseline; not full repository CI. |
| New census tests before implementation | Ten failures at the explicit missing-implementation assertion. | Observed RED; synthetic real Git repositories, not fabricated scientific failures. |
| New census tests after implementation | Ten tests passed normally; ten passed with Python optimisation. | Observed GREEN; pinned-object coverage, dirty/untracked separation, unfamiliar paths, duplicate identities, unusual names, symlinks, modes/gitlinks, invalid refs, missing owners and deterministic output. |
| Pilot reference targets | All 18 reference-definition destinations exist. | File-target inspection, not rendered GitHub navigation or comprehension. |

The local interpreter was Python 3.13.5, not the repository-pinned 3.11.9. The first baseline subprocesses also emitted an unrelated environment startup/warm-up traceback after the repository output; their zero exit status and repository output were observed, but they are not clean-room CI evidence. Subsequent census tests used `-S` to avoid that unrelated startup hook, with the available package path supplied explicitly. An interrupted internal-reference test attempt is **not** counted as a pass. Native pinned-environment tests and full required CI remain separate obligations.

The census script and tests were subsequently checkpointed to GitHub. [CENSUS.json](CENSUS.json) records 16,073 baseline tracked blob paths, 14,439 distinct blob objects, all root/suffix/mode counts, and 19 exact discovery-owner bindings. The canonical full-entry digest is `b920fc6db020680b9bc8477f1cd9604b4d0c8ef181b9b06a783014cc2099076c`. These are object statistics, not paper counts or semantic-reading credit. The script can reproduce the full rows with its `--entries` option; a second giant checked-in inventory is unnecessary.

[PILOT.md](PILOT.md) preserves the actual representative reading and its limits: composite reference, ambiguous edition relationship, non-PDF finite-mediator mathematics, recognition/correction and broader tawatur, full tensor/coercive dynamics, finite-audit Fisher geometry, and the occurrence/empirical joint-feasibility bridge. The stronger coercive successor must not disappear behind the predecessor's older open bridge. The later positive foundational appraisal must not be flattened into a blanket unresolved label. These are source-bound editorial findings, not fresh scientific acceptance.

### Checkpoint integration boundary

Early recovery commits deliberately saved work before generated state and manifest were reconciled. They were not claimed as green CI or merge-ready; the owner's frequent-save instruction did not waive the final checks. The bounded finalisation revision uses the normal generators and removes its transport workflow. Its actual results, final commit and the subsequent PR CI must be read from GitHub, not predicted from this note. No required validator is disabled.

## Obligation ledger

| Obligation | State | Remaining |
|---|---|---|
| C00 | PARTIAL, anchored | Baseline/authority/isolation and source instructions recorded; native/full baseline evidence and final role/review bindings remain. |
| C01 | OBJECT CENSUS EXECUTED; OWNER RECONCILIATION PARTIAL | Complete owner/work-family reconciliation, especially predecessor continuations and substantive AR8R collections; independently reconcile candidate dispositions. Nineteen owner seeds are not the full owner denominator. |
| C02 | PREPARATORY PILOT WRITTEN; NOT ACCEPTED | Preserve the actual reading; complete C01 admission/reconciliation, independently test the representative work/edition and intellectual design, and observe rendered reading routes. |
| C03 | NOT STARTED | Full semantic crosswalk and six integrated reader pages after the tested design; do not equate this sample with complete coverage. |
| C04 | CENSUS CONTROLS EXECUTED; OVERALL NOT COMPLETE | Required maintenance exercises, 18 RLGWO discriminating controls, native state/manifest convergence and applicable full CI. The ten census unit tests are not those 18 controls. |
| C05 | NOT STARTED | Independent exact-candidate review; this executor cannot self-certify it. |
| C06 | NOT AUTHORISED FOR MERGE | Dot assessment, owner decision and any subsequently authorised post-merge readback. |

## Resume without repeating the work

1. Read Issue 35 and its continuation, then this record, the census and pilot. Recheck actual main and this branch. Preserve unrelated changes and re-anchor only affected predicates if main advances.
2. Reproduce the census with its existing owner paths; add further verified owner bindings rather than inventing a competing scientific registry. Do not repeat the already source-bound pilot from scratch.
3. Complete the C01 owner/candidate reconciliation and review the representative design. Then perform comprehensive substantive mapping and the six pages. The pilot's source links and exact inspected sections are reusable inputs, not exhaustive reading receipts.
4. Exercise the full RLGWO controls/journeys/maintenance cases. Use the existing full CI and publication pins. Inspect any failed early checkpoint honestly; do not solve drift by exemptions.
5. Keep the PR draft until implementation and independent review are complete. Do not use an automatic issue-closing keyword or merge this checkpoint merely because infrastructure checks pass.

## Continuation rule

Resume this branch and its committed evidence; do not restart the analysis or substitute the earlier unmerged PR 34 head. Read the entire Issue 35 body and continuation. Do not treat this checkpoint, an Actions snapshot, a census, a polished sample or passing link checks as completed scholarly curation. Preserve recorded failures and outstanding acceptance predicates. Save coherent checkpoints frequently, then regenerate and qualify the final candidate without skipping required gates.
