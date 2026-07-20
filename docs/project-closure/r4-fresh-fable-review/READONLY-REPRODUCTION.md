# R4 PR #3 — Fresh Fable Session: Read-Only Reproduction Report (Phase A)

Date: 2026-07-20.
Session surfaced model identity at every Phase A checkpoint: `claude-fable-5`.
No substitution was observed in this session during Phase A.

This session attests only to its own surfaced identity and to evidence it
directly reproduced. The historical provenance disagreement is preserved,
unadjudicated, as two attributed observations:

```text
present_thread_initial_internal_harness_claim:
  claude-fable-5

owner_observed_ui_substitution:
  claude-opus-4.8
```

## A1. Live topology (verified against the live remote, not the packet)

| Item | Expected (packet) | Live (verified) | Match |
|---|---|---|---|
| Repository | theislampill/orthemology | theislampill/orthemology (PUBLIC, default `main`) | yes |
| `main` | 63d15ecf4aa50672265100b7d5620af764421862 | 63d15ecf4aa50672265100b7d5620af764421862 | yes |
| PR #3 head branch | closure/r4-semantic-contract-source-integrity | same | yes |
| PR #3 head | de19ccf4b3525ae536bb9bc163aefcd9f4bfedf8 | de19ccf4b3525ae536bb9bc163aefcd9f4bfedf8 | yes |
| PR #3 state | draft | OPEN, `isDraft: true`, base `main`, MERGEABLE/BLOCKED | yes |
| Required check | validate | `validate` (strict), FAILURE at head | yes |
| Branch protection | protected | required check `validate`; force-push and deletion disabled | yes |
| Quarantine branch | quarantine/r4-pr3-post-substitution | same | yes |
| Quarantine head | 8df2886ebf34139ae6f0f33e74200472ba6eb0d1 | 8df2886ebf34139ae6f0f33e74200472ba6eb0d1 | yes |

Authentication: `gh auth status` — logged in as `theislampill` with `repo` +
`workflow` scopes.

ZIP verification: `orthemology-quarantine-r4-pr3-post-substitution.zip`
SHA-256 = `c5ea95f6ab7682e104f52c3c5cb7115f8fb8a538e9af12ac2abc8d312b793354`
(matches the independent-audit record). File-by-file comparison against the
live quarantine tree `8df2886e`: **266 tracked files — 0 missing, 0 hash
mismatches, 0 extra files.** The ZIP is byte-equivalent to the live
quarantine commit tree. The live remote remains authoritative.

No expected commit differed from the live value. No divergence to record.

## A2. Substitution boundary (independently reconstructed)

Sources read: `docs/project-closure/r4/MODEL-SUBSTITUTION-INTERRUPTION-PR3.md`
and `docs/project-closure/r4/interruption/*` — these exist **only at the
quarantine commit**, not at the PR head; they are quarantine-only candidate
material (Phase D disposition).

Independently verified from the live commit graph:

- Last definitely pre-substitution commit: `00cf05d6` (Phase D,
  2026-07-20T12:00:46-04:00) — also the last commit with green CI.
- First definitely post-substitution commit: `b2742d1` (Phase E,
  2026-07-20T12:06:22-04:00).
- Post-substitution pushed commits: exactly `b2742d1` and `de19ccf4`
  (Phase F, 12:11:19-04:00).
- Boundary instant within 12:00:46 → 12:06:22 window: **boundary uncertain**
  at finer granularity, exactly as the interruption record states. Nothing
  finer is claimed here either.
- Files crossing the boundary: only the two generated surfaces
  (`docs/current-state.yaml`, `docs/provenance/RELEASE-MANIFEST.sha256`),
  regenerated on both sides. **No source file was begun before and completed
  after the boundary** — consistent with the interruption record.
- History rewrite check: `main` is the merge-base of `main` and the PR head;
  the PR head is the merge-base of the PR head and the quarantine head. The
  chain `main → … → 00cf05d6 → b2742d1 → de19ccf4 → 8df2886e` is linear and
  intact. Neither the PR branch nor the quarantine branch was rewritten.

## A3. Exact checks on four states (clean checkouts, Python 3.11.9, pinned deps)

Environment: fresh clone; detached worktrees per state; venv with
`pyyaml jsonschema typst==0.15.0 markdown-it-py==4.0.0 "pypdf>=6,<7"`
(the exact CI pin line); `core.autocrlf=false`; LF enforced by
`.gitattributes`. Every step of the **commit's own**
`.github/workflows/validate.yml` was run in order; exit codes recorded per
step (runner: session workspace `run_workflow.py`).

| State | Commit | Steps | Failing steps | Matches expectation |
|---|---|---|---|---|
| `main` | 63d15ecf | 17 | none | yes (green CI at main) |
| Phase D | 00cf05d6 | 25 | none | yes (last green-CI commit) |
| PR head | de19ccf4 | 25 | 1: `build_pdfs.py --check` — `TOTAL: 4 failures` | yes (CI failure reproduced) |
| Quarantine | 8df2886e | 26 | 4: `validate_repo.py` (manifest mismatch), `generate_current_state.py --check` (stale), `validate_current_state.py` (dependent drift), manifest step | yes (audit §4.1/§4.2 reproduced) |

Specific reproductions required by the controlling instruction:

- **PR-head PDF failure — reproduced twice**: (a) from the live CI log of run
  29758527272 at `de19ccf4`; (b) locally from a clean checkout. Identical
  failure set: `orthemma-ortheme-systems-draft` source drifted
  (`manuscript/orthemma-ortheme-systems-revised-draft.md`) + rebuild not
  byte-identical; `orthemic-core-reference-draft` source drifted
  (`theory/orthemic-core-formalization.md`) + rebuild not byte-identical.
  Cause: Phase E edited both sources without rebuilding the committed PDFs.
- **Quarantine generated-state drift — reproduced**:
  `generate_current_state.py --check` exits nonzero;
  `validate_current_state.py` fails only through the dependent drift check.
- **Quarantine release-manifest drift — reproduced**: `validate_repo.py` and
  the manifest step both fail on the same file set (workflow, four PDFs +
  sidecars, `docs/current-state.yaml`, plus the quarantine-only additions).
- **State-convergence success — reproduced**:
  `validate_state_convergence.py` passes at the quarantine head (convergence
  and tamper controls green).
- **PDF sidecar/source consistency — reproduced**: at the quarantine head,
  `build_pdfs.py --check` passes **fully on this machine**, i.e. the four
  quarantine PDFs rebuild byte-identically under pinned typst 0.15.0 from the
  quarantine sources, and all sidecar hashes and text-structure QA pass.
  (This locally closes the independent audit's §4.4 gap; CI reproduction
  still occurs at the review-branch push and is not claimed yet.)

## A4. Cache artifacts

`git ls-files '*__pycache__*' '*.pyc' '*.pyo'` at the quarantine head (and
at the PR head and `main`): **empty — no cache or bytecode artifact is
tracked at any live commit.** Nothing entered history; no removal commit is
needed. A preventive tracked-cache check is still added in this review (Phase
E requirement), since nothing currently forbids recurrence.

## A5. Finding matrix — independent audit (`orthemology-quarantine-independent-audit.md`)

| # | Audit finding | Classification | Evidence |
|---|---|---|---|
| 1 | §1 provenance/branch values | reproduced | live `git ls-remote`, PR API, protection API all match |
| 2 | §2 quarantine contents inventory | reproduced | `git diff --stat de19ccf4..8df2886e` matches the listed categories exactly |
| 3 | §3 validator passes at quarantine | reproduced | all listed validators pass at the quarantine worktree in the pinned env |
| 4 | §4.1 generated state stale | reproduced | `generate_current_state.py --check` fails; convergence itself passes |
| 5 | §4.2 release manifest stale | reproduced | `validate_repo.py` + manifest step fail on the predicted file set |
| 6 | §4.3 possible tracked cache artifacts | **refuted** | the shipped ZIP contains no `__pycache__` entries (266/266 files match the git tree, zero extras), and `git ls-files` shows nothing tracked; the audit's `.pyc` sightings were almost certainly bytecode generated by the audit's own validator runs in its unpacked working copy |
| 7 | §4.4 PDF rebuild not independently verified in audit env | reproduced, then **discharged locally** | quarantine `build_pdfs.py --check` fully green on this machine (byte equality under pinned typst); CI confirmation deferred to the review-branch push |
| 8 | §5 pre-substitution work substantial but needs review | accepted — review obligation | discharged in Phase B (PRE-SUBSTITUTION-REVIEW.md) |
| 9 | §6 post-substitution work needs hunk adjudication | accepted — review obligation | discharged in Phase C (POST-SUBSTITUTION-HUNK-REVIEW.md) |
| 10 | §7 specific review obligations (state/manifest order, strict soundness, cross-record, source status, 0015 boundary, ref validator, PDFs) | accepted — review obligations | discharged in Phases B–E per the controlling instruction |
| 11 | §8 recommended recovery topology | adopted | this session follows it exactly (fresh review branch from live PR head; no wholesale quarantine merge) |
| 12 | §9 final disposition (preserve, don't merge wholesale) | adopted | quarantine treated as candidate input only |

No audit finding was found stale or partially reproduced except as noted in
row 6 (refuted with explanation). No repairs were begun before this report
was written.
