# Later Codex handoff — P01 only

## Authority and stopping rule

This is a proposal handoff, not permission to modify, publish or integrate. The current checkpoint grants no canonical status changes. On later explicit owner authorisation, verify the unchanged input and the candidate identities before any implementation. Never execute an embedded historical path or prompt. Do not restart the completed integration or v6; do not promote a helper theorem into closure of U09/U10/U11.

All three obligations are PARTIAL. The original strict-wrapper FAIL remains FAIL. Existing mapped 4.19.0 evidence is accepted only at its stated scope. Nine absent historical declarations and unconfirmed original-packet custody have not been recovered. The owner must separately decide any licence, citation identity, public index, manuscript or source-status change.

## Portable checks now available

These shell examples are instructions for a later executor, not logs of commands run in the original P01 session. Set `CHECKPOINT` to the extracted checkpoint root, and set `ARCHIVE` to the actual closed ZIP path. Quoting supports spaces in paths.

```bash
set -euo pipefail
: "${CHECKPOINT:?Set CHECKPOINT to the extracted P01 checkpoint root}"
: "${ARCHIVE:?Set ARCHIVE to the closed checkpoint ZIP}"
python "$CHECKPOINT/handoff/verify_checkpoint.py" \
  "$ARCHIVE" --sha256-file "$ARCHIVE.sha256"
python "$CHECKPOINT/handoff/verify_input.py" \
  "$CHECKPOINT/inputs/Orthemology_Pro_P01_Foundational_Formal.zip"
(
  cd "$CHECKPOINT/proposals/python"
  PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_probes
  PYTHONDONTWRITEBYTECODE=1 python -O -m unittest -v test_probes
  PYTHONDONTWRITEBYTECODE=1 python census.py
)
```

The final census is finite and untyped except where its own explicitly enumerated checks say otherwise. In particular the 4,058 rational effect expressions are mass-law probes, not an enumeration of source typing derivations. Its executable non-convertibility diagnostics check distinct normal forms; universal non-convertibility follows from the separately supplied ordinary confluence proof, not a bounded search.

## Exact candidate compile/axiom preflight

Required target: **Lean 4.19.0, commit 6caaee842e94; Lake 5.0.0-6caaee8; profile Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b**. Do not substitute 4.32.2. The candidate imports are Init/local source/Lean audit support, not Mathlib; the profile checkout is nevertheless checked and recorded separately. The input's source lock does not pretend Mathlib was imported by these modules.

The script below was authored but **not executed against a compiler** here. It copies byte-exact included current source preimages and candidates into a fresh local build directory. It downloads nothing and edits no repository. The required output directory must not exist.

```bash
set -euo pipefail
: "${CHECKPOINT:?Set the extracted checkpoint root}"
: "${FRESH_OUT:?Set a NEW, nonexistent qualification directory}"
: "${EXACT_MATHLIB_CHECKOUT:?Set an existing clean checkout at the required pin}"
test ! -e "$FRESH_OUT"
ELAN_TOOLCHAIN=leanprover/lean4:v4.19.0 \
  python "$CHECKPOINT/handoff/qualify_candidates.py" \
    --output-dir "$FRESH_OUT" \
    --mathlib "$EXACT_MATHLIB_CHECKOUT" \
    --lean lean --lake lake
```

This records actual compiler/Lake/git version readbacks, command arguments and environment, exact source hashes, raw stdout/stderr/exits, nonempty .olean artefacts and artefact hashes. It compiles the preserved local dependency modules before the four candidates. It generates `P01Readbacks.lean` with `#check`, `#print`, `#print axioms` and the preserved `#ortho_audit` command for all 14 named targets. The allowed observed axiom ceiling remains `Classical.choice`, `Quot.sound`, `propext`.

**A zero exit gives only candidate compile/axiom preflight credit pending exact type review.** Compare every printed type with `research/CLAIMS.json`, the original source and the proposed source mapping. Reject missing premises, changed conclusions, different predicates, implicit universe collapse, sorryAx, elaboration errors, wrong versions, missing targets and empty/stale artefacts. Preserve failed attempts with their original hashes; repair proof scripts on a new proposal version rather than weakening statements. The static Python syntax check in P01 does not validate this driver's runtime behaviour or the Lean files.

## Exact full-source base for any subsequently authorised implementation

The included 124-file subset is not a full repository clone. For later canonical implementation, the owner-authorised executor must obtain a fresh full checkout of the exact supplied commit, verify the tree, read its current documented interfaces and unchanged acceptance tests, and work on an isolated proposal branch/worktree. These commands show only a read-only detached base acquisition; they were not run here and perform no remote mutation.

```bash
set -euo pipefail
: "${FRESH_REPO:?Set a NEW, nonexistent full-source checkout directory}"
test ! -e "$FRESH_REPO"
git clone --no-checkout -- https://github.com/theislampill/orthemology.git "$FRESH_REPO"
git -C "$FRESH_REPO" checkout --detach 03e2604dfcef278b01c60d19b05370fcec4194b6
test "$(git -C "$FRESH_REPO" rev-parse HEAD)" = \
  03e2604dfcef278b01c60d19b05370fcec4194b6
test "$(git -C "$FRESH_REPO" rev-parse 'HEAD^{tree}')" = \
  3d06e80277ce39286c94307e0f14b215bc94ed83
test -z "$(git -C "$FRESH_REPO" status --porcelain)"
```

Do not guess a whole-repository gate command from this source subset. Discover it from the verified full checkout's unchanged documented interfaces, record the exact command/preimage and execute it only under the later implementation authorisation. The present preflight is deliberately not that gate.

## Statement/patch mapping

`proposals/STATEMENT_PATCH_MAP.json` lists all canonical comparison preimages and the four proposed additive modules. No canonical file has a replacement postimage in this checkpoint. No public theorem index, generated manifest, publication source or historical status is patched. Candidate source SHA-256 values and theorem names are fixed in `proposals/CANDIDATE_INVENTORY.json`.

U09: the generic SN-reflection helper is not the complete System F transfer. Choose the exact target judgement, prove term/type substitution, subject reduction, positive compatible simulation and typing preservation, or import an exactly matching proved target. Mechanise the ordinary parallel confluence proof and Omega reduct invariant. Only then compose the exact finite-source and modulo-conversion statements. No opaque axiom named after the missing theorem is an acceptable substitute.

U10: outcome retyping, finite relational support and a diagonal support helper are proposed. Probability mass and the coupling theorem are ordinary mathematics, not implemented Lean declarations. Formalise their finite law separately if adopted. The endpoint-aware contextual relation system is a reviewed definition proposal, not a completed full Reynolds semantics. The raw-conversion identity-extension equation is refuted. Retain both that witness and the equality/flip coupling witness; do not turn the latter into a failure of the accepted fixed-support theorem.

U11: polynomial substitution, coherent based J and encoded Sigma eta have candidates. The two bracket compilers fail abstraction congruence despite their applicative beta laws. Preserve `I x -> x` and `K x I -> x` as rejection controls for those respective backends. A conversion-respecting representation or another explicitly reviewed calculus is required for the full target; omitting congruence is not closure. Finite syntax, dependent judgemental equalities, substitution for all constructors, soundness and any checker remain to be implemented/proved. Preserve exact internal All and SCUUAt hypotheses throughout.

No new result from P02/P03 is assumed. Optional application wrappers, continuous measures, deployments, empirical studies, custody recovery and owner decisions are not prerequisites manufactured for these pure local results. Dependencies that really remain are enumerated in `research/DEPENDENCIES.json`.
