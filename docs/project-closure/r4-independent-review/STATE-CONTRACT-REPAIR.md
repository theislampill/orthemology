# Phase B — generated-state contract repair (R4 independent review)

**Date:** 2026-07-20 · **Session:** independent Fable review of PR #3 (harness identity `claude-fable-5`).

## What was broken

1. **Non-convergent drift key.** `generate_current_state.py` embedded `git rev-parse HEAD` in the tracked `docs/current-state.yaml` and `--check` demanded exact file equality. Any commit containing a regeneration created a new HEAD, so the check failed forever — the sole failing CI step on the R4 candidate head (run 29751470223).
2. **Fuzzy "exact" surface validation.** `validate_current_state.py`'s docstring promised OPEN-DECISIONS "lists exactly the authored owner-only burdens" but implemented first-three-words substring matching, banned three phrases, and could not detect extra, duplicate, or stale burdens. README counts were validated by loose regex over prose.
3. **Deprecated Actions runtimes.** `actions/checkout@v4` / `actions/setup-python@v5` produced the Node-runtime deprecation warning (a warning, not the failure).

## Repair

| Item | Change |
|---|---|
| Drift key | `derived.source_tree_digest`: SHA-256 over sorted `relpath NUL file-sha256 LF` records of the declared source-input set. Pure content function; no commit hash anywhere in the state file. |
| Input policy | `docs/project-state-inputs.yaml` (machine-readable): excludes the state file itself, the release manifest, `artifacts/`, `docs/generated/`, `docs/project-closure/`; each exclusion has a recorded reason and its own guarding check. |
| Convergence proof | `scripts/validate_state_convergence.py`, run in CI: throwaway git repo → regenerate → commit → `--check` **passes on the commit containing the regenerated file**; idempotence; source-tamper control fails; excluded-path control passes. |
| Decision record | Dated amendment appended to Decision 0014 (body preserved) explaining non-convergence, the new invariant, source/generated/artifact distinction, and the reread procedure. |
| Burden IDs | Stable IDs `OWNER-LICENSE`, `OWNER-CITATION-IDENTITY`, `OWNER-EMPIRICAL-EXECUTION`, `OWNER-EXTERNAL-PUBLICATION`, `OWNER-PRIVATE-MATERIAL`, `OWNER-PAID-SOURCE` in `authored.owner_only_burdens` (`id`/`text`/`detail`). `OPEN-DECISIONS.md` carries `<!-- owner-burden:ID -->` markers. |
| Exact validation | `validate_current_state.py` now enforces: exact burden-ID set equality (missing/extra/duplicate all fail) + verbatim titles on marker lines; VERSION first line exactly equals the authored revision label; README decision range and example count through `<!-- state:... -->` markers by exact comparison; STATUS carries a marker-wrapped `claim-status-by-lane` block compared verbatim (whitespace-normalized) per lane against `authored.claim_status_wording`. |
| Workflow | `actions/checkout@v6`, `actions/setup-python@v6`, `permissions: contents: read`, new convergence-proof step. Python and package pins unchanged; no caching added. |

## Why the new invariant converges

The digest depends only on the contents of files that the generator does not write. The generator writes exactly one file (`docs/current-state.yaml`), which is excluded. Therefore regenerating and committing is a fixed point after one pass: the commit changes HEAD but no digest input, so `--check` compares identical bytes. This is proven mechanically by the CI convergence step, including the negative (tamper) and exclusion controls.

## Verification (at repair time, re-derived from the tree)

- `generate_current_state.py --check`: **0 failures** (previously the sole CI failure).
- `validate_current_state.py`: **0 failures** with the strict checks in force.
- `validate_state_convergence.py`: **6/6 PASS** including commit-boundary convergence and both controls.
