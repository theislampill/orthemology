# R7E Sol Task 15 clean-clone verification

**Status:** TASK 15 VERIFIED CANDIDATE — TASK 16 INTEGRATION PENDING.

This record closes the local, remote, and fresh-clone evidence surface for the
reviewed candidate. It does not record a merge, publication, release, or
protected-branch write.

## Exact identity and review

- Candidate: `ad57371b8ef88c313f9b92c43c7618500337e0ed`.
- Parent: `c9fcf44d64208b8defcec9b809fbbb3ceb39a65c`.
- Remote branch: `review/r7e-sol-independent-repair`.
- Remote head at verification:
  `ad57371b8ef88c313f9b92c43c7618500337e0ed`.
- Fresh independent verdict on the candidate: `APPROVED`.
- Exact-SHA GitHub Actions run:
  [30313374447](https://github.com/theislampill/orthemology/actions/runs/30313374447),
  `SUCCESS`.
- Protected `main` observed before the candidate push:
  `43fee0f519e2f6984fb143c1e621c83382e71ec7`.
- The protected stack remained open, draft, mergeable, and ordered as PR #12
  through PR #8. No PR branch or protected branch was changed in Task 15.

The first remote run exposed missing source history. The second exposed a
manifest/configuration identity mix-up in the PDF runtime probe. Both failures
remain preserved in GitHub Actions. Each repair was test-first, append-only,
independently reviewed, and rerun on a new exact SHA. The successful run does
not reuse either failed parent result.

## Pinned environment and command surfaces

- Python: `3.11.9`.
- Dependency owner: `requirements-ci.lock.txt`.
- Dependency-lock SHA-256:
  `3011af491f65eef07ff9f3854ead9c0b69ea42c031a0bd863b43cd80f5d997fd`.
- TeX image manifest:
  `sha256:ccf0168bb3dc1e5ba18094131ebb57177f90eca37ab2727bc2d2afb54ad60a51`.
- TeX image configuration:
  `sha256:58b5c7718b4fd239c651873cd267b6c7c82caa5d9a25fe22845d1b8720fff6b1`.
- Poppler: `25.07.0`, installed from the complete 61-package explicit lock.
- UTF-8 wrapper: `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`.

The workflow was re-extracted from the fresh clone. It contained exactly 71
commands, byte-for-byte equal to the locally reviewed inventory. All 71 passed
in order, including generated-state drift, recursive mutations, release
manifest convergence, and the final six-artifact PDF parity gate.

These eight supplemental commands also passed:

```text
python tests/test_publication_profile.py
python scripts/validate_publication_profile.py
python tests/test_latex_source_generation.py
python scripts/generate_latex_sources.py --check
python scripts/validate_latex_sources.py
python tests/test_arxiv_source_package.py
python scripts/validate_arxiv_source_package.py
python scripts/build_pdfs.py --check
```

The fresh clone used a new lock-only virtual environment. Its `HEAD` equaled
the remote candidate, `pip check` passed, and both index and worktree remained
clean after the full validation surface.

## PDF and source-package evidence

| Artifact | Pages | PDF SHA-256 |
|---|---:|---|
| `orthemma-ortheme-systems-draft` | 26 | `ceb2dc682547667dde20ec95150b7581670d836b2d1f9ea3e804767f54e3d2c9` |
| `orthemic-core-reference-draft` | 14 | `d3c405415f82702247a96fab1865c63a1b3c62789d6b3e9e3e6076eca21f481c` |
| `orthability-ground-of-intelligibility-draft` | 8 | `a6a2de01830781834c60f1775bd257b5b426b1307cfea422261776b58de0a9ee` |
| `orthability-divine-speech-athari-draft` | 6 | `ab22cd7d7a467c24c52e59f530c52af73f9416591cb2a0a8e2eef5c3a6ea53f7` |
| `dynamic-orthing-noetic-learning-orthability-draft` | 5 | `752697fb702e3cd0fa3a0af577041945f095e87913cd47513d2bd5135752114e` |
| `notation-gallery` | 2 | `3d5cddca2c72b3bb8169d6cc9cfb6764c6cb22815ff35109fc82a1c8fc8ec824` |

All six source packages passed repository validation and clean unpacked-build
checks. The six PDFs total 61 pages. Two independent 150-dpi raster passes
produced 61 images each; their ordered SHA-256 lists were identical. Every page
was visually inspected. No clipping, overlap, blank or missing page, missing
glyph, incomplete formula, broken table, duplicated heading, or invalid
single/two-column transition was observed.

The tracked tree, decompressed source-package paths and members, and PDF text
and metadata contained zero prohibited fictional-franchise terminology. One
short byte pattern in opaque compressed data was classified
`UNRELATED_ACRONYM_OR_FALSE_POSITIVE`; the decompressed archive name and
contents were clean and carried no semantic occurrence.

## Normative and ownership closeout

The normative/core owners are the schemas, registries, validators, fixtures,
`docs/current-candidate-state.yaml`, the seven authoritative publication
sources, and the six governed artifact sets. The DAEE crosswalk remains a
typed application boundary, not an identity claim. Existing episode, verdict,
evidence, residual, action, actor/handoff, and represented-standard records
remain their own owners.

Claimant identity and episode identity remain distinct. An indeterminate
claimant selection is not promoted to episode irresolution. Episode
reification remains a typed record operation; it does not establish awareness
or an external runtime. Activation and evaluator versions remain explicit
where applicable. Valid controls, invalid fixtures, direct Task 14 probes, and
recursive mutations remain separate evidence classes.

Contract authorship remains repository-authored and fixture-bound. The Task 14
program accounts for 77 explicit variants through 154 separate control and
mutation processes. The recursive engine generated 1,813 mutants across 27
families: 1,546 schema-rejected, 248 semantically rejected, and 19 justified
equivalents, with zero unjustified survivors.

Recurrence is specified and validated through governed references and
comparators; no unrecorded live reference operation is claimed. Anchors,
reference corpora, comparators, and independence judgments remain distinct.
The R7E episode is a bounded repository-history witness with missing private
capture evidence explicitly retained as missing.

Somnus run, assessment, reopening, and idempotency fixtures remain separately
identified. Retrospective defect loci do not rewrite earlier event truth.
Assessment, intervention, proposal, authorization, application, and outcome
remain separate typed stages. Legacy proposal provenance is not laundered into
grounded provenance, and no-change fixtures remain non-actuating.

The three collective modes preserve synchronized-but-individuated agents,
shared-state coordination, and a possible collective epistemic bearer as
distinct models. Transclusion levels, local adoption/authorization, dissent,
provenance, privacy, and security boundaries remain explicit. Outline-only
candidates and adoption profiles do not become implementation or downstream
authority.

No skill package, external repository mutation, network service, shared
service, scheduled job, writeback engine, transclusion transport, automatic
patch, or external runtime mutation was created or established. Successor work
for live capture, scheduling, conflict detection, replay, verdict
decomposition, governed propose/apply/revert, later outcome evaluation, and
federated or council runtime evidence remains outside this candidate.

Interrupted AR6 research remains `INTERRUPTED_IN_PROGRESS`. Its negative
evidence informed the official attack inventory where dispositioned, but no
interrupted conjecture, candidate proof, theorem, source claim, executable
artifact, or proposed patch was promoted.

## Remaining gate

Task 16 is the only remaining tracked task. Before each write it must freshly
verify exact reviewed identity, clean/generated state, ancestry, PR topology,
branch protection, mergeability, and required exact-SHA CI. Every merge-created
SHA requires its own CI result. No parent-SHA success may be reused.
