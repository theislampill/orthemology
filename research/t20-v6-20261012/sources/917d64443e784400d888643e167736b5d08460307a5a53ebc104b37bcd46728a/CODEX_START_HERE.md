# Codex: one bounded T20 v4 handoff

Read CURRENT_STATUS.json, EDITION_V4.md, INTEGRATION_PINS.json, the scope/exclusions of PUBLIC_PROJECTION.json, and REPLAY_SCOPE.json. This is a complete successor to v3, not a second separately installable tranche. Original T20 snapshot cutoff 2026-10-11T11:32:55Z remains historical; authorised same-day depth research belongs to T20 through the final seal. T21 has not begun.

## Validate once

    python -B validate_package.py
    python -B -m unittest discover -s tool-tests -v
    python -B validate_depth.py
    python -B replay_selected.py --list

Integrity is offline and standard-library only. The byte manifest is not a signature or proof certificate. depth/REVIEW_CURRENTNESS.json binds source reviews; DEPTH_REPLAY_VERIFICATION.json records selected fresh portable executions. All inherited receipts keep their original scopes. Do not replay unchanged source families merely to copy an unchanged reader. For a particular affected new target, run its declared suite, for example:

    python -B replay_selected.py --suite depth-proof-inquiry

Every advertised new suite copies exact source modules and explicit portable fixtures into a disposable directory. The runner installs and fetches nothing. Grounding is normal-only because its source uses bare assertions. Kernel source closure, inherited receipts, fresh kernel execution, ordinary proof and external human review are different axes.

## Apply only after explicit owner authority

Keep this package outside a clean target checkout. Exact approved base: commit 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c, tree 906b592fb2591ed918c5f0caf485ef79dca513ab, theislampill/orthemology. The supplied readback does not rerun CI. Do not change pins to work around drift.

    python -B apply_additive.py /path/to/clean/checkout
    python -B apply_additive.py /path/to/clean/checkout --apply

The second command requires separate authority. It adds only research/t20-consolidated-20261011 and does not stage, commit, push, modify authored state, apply DAEE or replace historical CP sources. It refuses dirty/drifted preimages and existing destination. Preserve repository conventions; do not create a global schema, blanket waiver or dummy targets.

After authorised staging, use the repository's documented derived-state/release-manifest regeneration and current gates, including tests/test_internal_references.py, scripts/validate_internal_references.py, scripts/generate_current_state.py --check, scripts/validate_v5_successors.py, scripts/validate_repo.py and git diff --check --cached. Report unchanged-source whitespace advisories honestly; do not normalize original source bytes or report blanket strict PASS. Existing exact-path attribute proposals remain review-only.

## Scientific reading only when needed

For result interpretation read depth/cross_front_synthesis/RESULT.md and its typed EDGES.json; then the relevant RESULT/REVIEW pair and source-owned claim. The complete old programme remains in the original chapters and coverage crosswalk. No wholesale corpus rereading, universal re-proof or new research campaign is requested. If one current binding or dependency fails, isolate that target and report it without silently weakening the claim.

R3 reported second-order overlap and priority remain unknown, historical hours unverified, and repository adoption absent. Completion of a local sealed handoff must not be described as a merge, fresh all-corpus execution or T21 start.
