# Review E — build/state audit (fresh Fable recovery review)

Scope: generated surfaces, artifacts, manifest, CI workflow on the final
review branch. Surfaced model: `claude-fable-5`.

- **Non-convergent generated state**: none; the source-tree digest contains
  no HEAD hash; `validate_state_convergence.py` proves commit-boundary
  convergence, idempotence, source-tamper failure, and excluded-path
  immunity — green at every state tested including the final tree.
- **Stale PDF sidecars**: none; the four PDFs were rebuilt from verified
  byte-identical sources; sidecar source hashes match the tree; zero commits
  have touched a PDF source since the rebuild's recorded source revision;
  `build_pdfs.py --check` (double clean rebuild + byte equality +
  text-structure QA) green at the final tree.
- **Manifest ordering errors**: none; the D3 order (cache check → registry
  surfaces → PDFs → current-state → convergence → manifest LAST →
  `git diff --exit-code`) was followed at every commit that changed tracked
  content; manifest step green at the final tree (269 entries at Phase E).
- **Dirty generated outputs**: `git status --porcelain` empty after every
  phase commit; all `--check` modes green.
- **Tracked caches**: none at `main`, the PR head, the quarantine head, or
  the review branch; standing guard added (`validate_repo.py` check 0),
  probed live (P10).
- **CI/local mismatch**: the one known class — local Windows console
  cp1252 encoding — was controlled by forcing UTF-8; the suite runner
  executes each commit's own workflow steps. Local/CI equality for THIS
  branch is verified at the push gate (protected CI) and again from the
  fresh clone; it is not claimed before those runs exist.
- **Source/artifact commit confusion**: none; sidecars record the source
  revision, and the artifact-introducing commit is the two-stage
  `git log -- artifacts/` note; the `--check` contract rebuilds from the
  sidecar's recorded epoch, so reproducibility holds on any later commit.

Blocking findings: **none**.
