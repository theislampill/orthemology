# Codex integration handoff

This is a proposed consolidated T20 research reader and source projection, prepared locally for owner review. It has not been published, adopted, committed or merged. The research cutoff is 2026-10-11T11:32:55Z. The separate kickoff prompt is for a future authorised task.

The bounded [version 2 scope](../../PUBLIC_BOUNDARIES.md#reference-056) adds ET-23 and supersedes the undelivered first local candidate.

## Minimal integration path

For mechanical integration, read this handoff, INTEGRATION_PINS, the top-level scope and exclusions in PUBLIC_PROJECTION, and REPLAY_SCOPE. Then use the validation and additive-application commands below. Do not reread or reconstruct the entire scientific programme before copying a sealed proposed reader.

The science chapters and README_FIRST are available to the owner/reviewer and for resolving a specific semantic ambiguity. The four claim records control hypotheses, evidence and remaining obligations. CLAIM_REGISTER is a compiled navigation index; DEPENDENCY_INDEX distinguishes premise, source support, interpretation, comparison and currentness. These are preserved inputs, not an instruction to re-prove unchanged work.

PUBLIC_PROJECTION binds exact original and public bytes. SOURCE_INDEX locates selected owners. PROOF_FAMILY_LAYOUTS retains isolated later source trees; proofs/FORMAL_REPLAY_MAP selects actual entry and dependency bytes. Equal bytes can occur in required import-relative layouts; unequal same-named modules must never be merged. Physical copies do not multiply scientific results.

## Package checks

From this directory, with Python 3.10 or newer:

    python -B validate_package.py
    python -B -m unittest discover -s tool-tests -v
    python -B replay_selected.py --list
    python -B replay_selected.py --suite finite-contracts

The integrity check is offline and standard-library only. It verifies every sealed member, rejects missing/extra files and symlinks, and checks original/public binding claims. It is not a proof checker. The replay runner copies the named finite suite to a temporary directory; it does not mutate this package. Other selected finite suites require the already-installed dependencies in REPLAY_SCOPE. It installs nothing and fetches nothing. The hash manifest is an integrity seal, not a cryptographic signature.

## Additive application after explicit integration authority

Keep this input package outside the target checkout. The exact approved base is commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`, tree `906b592fb2591ed918c5f0caf485ef79dca513ab`, in `theislampill/orthemology`.

    python -B apply_additive.py /path/to/clean/checkout
    python -B apply_additive.py /path/to/clean/checkout --apply

The first command performs checks only. The second requires the owner's separate integration authority and adds only the new `research/t20-consolidated-20261011` subtree. It refuses baseline drift, dirty/untracked state, altered actual preimage bytes (including index-hidden changes), symlink preimages/ancestors, and an existing destination. It does not stage, commit, push, add a navigation pointer, change authored state, apply the DAEE candidate, or alter historical CP sources. An interrupted filesystem copy can leave a partial new subtree; inspect it and remove only that new partial output before retrying, never overwrite it.

Do not change the pins to work around drift. Reconcile the changed baseline and obtain the needed integration approval. Preserve all existing source/result owners and repository conventions; this package-local record format requires no new global schema or broad validator exemption.

## Established repository gates

After authorised staging of the selected new public files, use the repository's documented derived-state and release-manifest regeneration workflow. Preserve its authored state block. Run the current required gates, including:

    python -B tests/test_internal_references.py
    python -B scripts/validate_internal_references.py
    python -B scripts/generate_current_state.py --check
    python -B scripts/validate_v5_successors.py
    python -B scripts/validate_repo.py
    git diff --check --cached

Run strict whitespace checks on the actual proposed delta and report historical advisories separately. EXACT_SOURCE_WHITESPACE records the actual inherited exact-byte diagnostics, including blank-at-EOF cases. Whole-delta strict whitespace is not reported as passing. Authored/amended material is clean. The baseline already uses narrowly scoped exact-source attributes; PROPOSED_EXACT_SOURCE_ATTRIBUTES gives exact per-file entries for owner/Codex review only. The apply tool does not add them or change protected root attributes. Do not weaken validators, add dummy targets, or reseal original scientific sources to conceal a failure. This local preparation did not execute a full current-repository validation; three inherited native reference targets and the controlling validator preimages were verified read-only at the pinned baseline.

## Reproduction limits

REPLAY_SCOPE separates five package-local finite controls from source-preserved historical suites. Kernel source closure, original receipts, fresh kernel execution, ordinary proof, finite controls, external human review and repository adoption are different evidence axes. Official pinned Lean/Mathlib dependencies are external, never replaced by cached compiled binaries in this package. Historical scripts containing omitted machine locators require a new environment-bound driver before execution. Rebuild only the affected cluster when the integration actually changes a proof or its prerequisites; a new reader is not reason to repeat all unchanged historical research.

The DAEE implementation dependency is not republished; its reviewed proposal remains explicitly unadopted. Raw archives, transcripts, private identifiers, primary-source collections, unfiltered logs and private custody maps are excluded. The package carries research appraisals and source identities, not a newly authenticated historical-source corpus.
