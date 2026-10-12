# Codex handoff — P03 attempt-0002

## Authority and purpose

This packet contains research and proposed source, not permission to change the repository. Preserve main `03e2604dfcef278b01c60d19b05370fcec4194b6`, tree `3d06e80277ce39286c94307e0f14b215bc94ed83`, merged PR28 and the closed Integration DAG. A later owner-authorised implementation/review is separate from this handoff. Do not replay private historical commands or promote old strict-wrapper failure to success.

## 1. Research results already established

Ordinary source-level results and their explicit host/model assumptions are in the four research notes. They establish partial transport/checker/export correspondence, a complete-state operational relation with a forward-stuttering construction, a failure-atomic precommit proposal, and a probability-carrying family under a matching joint environment law. New countermodels refute unrestricted borrowed-input round trips, deployed interrupted-write atomicity, trace-support-to-law inference and two proposed overstrong finite-probability converses.

P02 was consumed from its exact 4,192,393-byte archive. All five P02 obligation statuses remain PARTIAL. Its ordinary finite measure, fibre, budget and finite-table results discharge the actual finite-engine prerequisites at their stated hypotheses; unrelated U08/CV-C/parity formal gaps are not gating the engine. No P02 kernel declaration was imported as proved. Infinite-history claims retain `J` and explicit measurability.

The full ordinary VCT layer analysis and finite-DAG/rank equivalence are supplied. The formal candidate retains local evidence transport, target coverage, semantic maps, version/invalidator guards, per-hop authority with re-delegation and root-path witnesses. It does not derive direct authority, world truth or final root equality without extra hypotheses.

## 2. Proposals ready for implementation review

The two new named modules are `proposal/safe_frontend.py` and `proposal/atomic_engine.py`. Proposed destination paths and exact hashes are in `proposal/PATCH_AND_STATEMENT_MAP.json`. Their destination preimage is absent in the supplied source subtree; a later executor must check actual repository absence before adding files. Do not overwrite an existing file on that assumption.

The adapters can run over either exact canonical source or the exact attempt-0001 three-patch source. Both bases passed the final fifteen-method adapter suite in normal/optimised Python. The large history/probability probes used the attempt-0001 base; this is not a claim that every probe was separately repeated on canonical source.

Prefer retaining legacy endpoint names and adding the new owned endpoints. In particular, `export_module_owned` has a declared exact list/tuple row domain, while the canonical legacy `proof_export.module` has observable arbitrary-two-item-iterable tolerance. Adopting the parent's restrictive row patch under the old name requires a separate compatibility decision; it is not needed to expose the new strict API.

The old three patches and all preimages/postimages remain unchanged inside attempt-0001. The new wrappers neither erase their evidence nor automatically adopt them. Rejected new draft preimages document the reentry and exporter count-capture corrections. Do not deploy those drafts.

## 3. Formal results actually kernel-checked here

**None.** Fourteen graph/VCT targets are proposed, with zero observed declaration types, zero axiom readbacks and zero new `.olean` artifacts. Candidate syntax/type correctness is not inferred from static inspection or Python tests.

The expected pin is Lean `4.19.0 / 6caaee842e94`; Lake `5.0.0-6caaee8`; the larger canonical mapped project pins Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The new three-file candidate requires only that exact compiler's core library. Existing scoped 4.19.0 and separate 4.32.2 acceptance remain predecessor facts, not fresh proof of these targets.

`evidence/TOOLCHAIN_STATUS.json` distinguishes HOST_EXECUTION_BLOCKED from UNPROVED and binds actual failed acquisition commands. Both negative runner controls reject: a missing compiler, and a real native executable with the wrong version. No fake-positive runner or wrapper is accepted as a compiler.

## 4. Portable reconstruction and verification commands

Start from the freshly verified, extracted attempt-0002 directory. These commands create only a new temporary research workspace; they do not clone, edit or install into the authoritative repository.

```bash
set -euo pipefail
ROOT="$(pwd)"
TESTROOT="$(mktemp -d "${TMPDIR:-/tmp}/orthemology-p03-a2.XXXXXX")"
python3 -B "$ROOT/tools/prepare_workspace.py" --out "$TESTROOT/workspace"
export P03_BASE="$TESTROOT/workspace/source"
python3 -B "$ROOT/tools/test_new_frontier.py" -v
python3 -B -O "$ROOT/tools/test_new_frontier.py" -v
python3 -B "$ROOT/tools/explore_histories.py" --out "$TESTROOT/histories-normal"
python3 -B -O "$ROOT/tools/explore_histories.py" --out "$TESTROOT/histories-optimised"
python3 -B "$ROOT/tools/probe_probability_bridge.py" --out "$TESTROOT/probability-normal"
python3 -B -O "$ROOT/tools/probe_probability_bridge.py" --out "$TESTROOT/probability-optimised"
python3 -B "$ROOT/tools/probe_vct_layers.py" --out "$TESTROOT/vct-normal"
python3 -B -O "$ROOT/tools/probe_vct_layers.py" --out "$TESTROOT/vct-optimised"
P03_BASE="$TESTROOT/workspace/canonical" python3 -B "$ROOT/tools/test_new_frontier.py" -v
P03_BASE="$TESTROOT/workspace/canonical" python3 -B -O "$ROOT/tools/test_new_frontier.py" -v
```

The history runner requires threads, tracing and bounded scheduling waits. A scheduling timeout is an explicit environmental failure, not permission to mark the history passed. Raw delivered commands show the exact previously executed source-regression commands; their 183 methods are a reconstruction/compatibility check, not a new historical census.

## 5. Minimal exact native formal execution

The minimal packet is `handoff/P03_Lean419_Execution_Packet.zip`. It contains three Lean source files, exact target/source bindings, a core-only toolchain pin and the same runner. It contains no compiler and no purported compiled proof.

With an independently acquired official native Linux compiler, run the following from the full packet or the extracted minimal packet:

```bash
set -euo pipefail
ROOT="$(pwd)"
: "${LEAN419_NATIVE:?Set this to the exact native Lean 4.19.0 bin/lean path}"
AUDITROOT="$(mktemp -d "${TMPDIR:-/tmp}/orthemology-p03-lean419.XXXXXX")"
"$LEAN419_NATIVE" --version
python3 -B "$ROOT/tools/run_formal419.py" \
  --lean "$LEAN419_NATIVE" --out "$AUDITROOT/build"
```

For a reversible exact-version acquisition on a host with normal network access, one possible external command sequence is:

```bash
set -euo pipefail
ACQUIRE="$(mktemp -d "${TMPDIR:-/tmp}/orthemology-lean419-download.XXXXXX")"
curl --fail --location --proto '=https' --tlsv1.2 \
  'https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst' \
  --output "$ACQUIRE/lean-4.19.0-linux.tar.zst"
sha256sum "$ACQUIRE/lean-4.19.0-linux.tar.zst" > "$ACQUIRE/DOWNLOAD.sha256"
mkdir "$ACQUIRE/toolchain"
tar --zstd -xf "$ACQUIRE/lean-4.19.0-linux.tar.zst" -C "$ACQUIRE/toolchain"
mapfile -t CANDIDATES < <(find "$ACQUIRE/toolchain" -type f -path '*/bin/lean')
[[ ${#CANDIDATES[@]} -eq 1 ]]
export LEAN419_NATIVE="${CANDIDATES[0]}"
"$LEAN419_NATIVE" --version
"$(dirname "$LEAN419_NATIVE")/lake" --version
```

This is an **unexecuted external acquisition recipe**, not an assertion that a download occurred here. Verify official release provenance and the compiler/core identities independently; a recorded hash or printed version alone does not establish origin. No official compiler digest is invented in this packet. The runner additionally requires native ELF, exact version/commit text, the core Init artifact, frozen source hashes, fresh nonempty outputs and raw audits. It rejects nonzero exit, stale/missing artifacts, wrong version, error/sorry markers, and missing or unexpected axiom readbacks.

A zero runner exit is `BUILD_READBACK_PASS_PENDING_INDEPENDENT_TYPE_AND_ORIGIN_REVIEW`, not automatic Q1f PASS. Review every emitted declaration/type against `formal/EXPECTED_TARGETS.json`, the explicit main-type restatement in `P03Audit.lean`, model definitions, source guards, full transitive axiom outputs and compiler origin. Re-execute independently before granting fresh formal credit. Preserve any compile failure; repair only separately versioned candidate source and regenerate its hashes and audit expectations. Never add `sorry`, `sorryAx`, a new unjustified axiom, or an assumption that merely restates the global target.

The larger parser/export bridge is not part of this minimal core-only packet. Later exact native export qualification must use the accepted **mapped-native** source preparation and the provided Lake/Mathlib pins, not assume the original strict-wrapper replay passes. Mathematical constructor correspondence is supplied; arbitrary actual exported-text kernel acceptance is still unclaimed.

## 6. Implementation steps that remain Codex/owner work

After separate authorisation, verify destination preimages against the exact selected repository revision, choose the new public API routing and import layout, add the two reviewed modules and appropriate tests, and bind the actual deployed entrypoints to owned ingress and guarded publication. Source files in this packet are proposals until that happens; successful tests here do not change the installed engine.

Review failure/cancellation semantics with callers: precommit registry failure is no-effect, but postcommit cancellation may leave a committed pending result. There is no durable crash-recovery or transparent exactly-once retry guarantee. Preserve issuer identity, complete read sets, absence tombstones, finite version/freshness budgets and insertion-order projection semantics.

Run the relevant complete project test/validation commands after integration, without using this proposal's finite probes as substitutes. Any canonical source/index/manifest/publication updates remain separate effects, and need their own actual post-effect readbacks. Do not reopen the old Integration DAG or claim integration credit from these research tests.

## 7. Claims that remain open and must not be promoted

The exact new Lean declarations remain unproved until native evidence and review exist. No mechanised CPython/JSON semantics or full deployed extraction proof was produced. Universal host correctness, absence of reflection/private-state compromise, live authority/currentness beyond a fixed epoch, real entropy/scheduler law, model-to-world identification, durability and future infinite-history completeness are not established by this packet.

Conditional joint-law and measurable-history theorems are complete as conditional mathematical results; do not remove their premises. Full-history defect includes `J`. Do not replace pointwise probability refinement with almost-sure completeness or erase representation-dependent arithmetic refusal. Do not infer direct authority or endpoint root identity from a legal VCT path. Optional TRC/P12 temporal/application work is not a missing Q1f pure premise.

No external-review, owner-adoption, source-truth, novelty, licensing or historical-recovery credit is granted. Preserve attempt-0001 and actual P02 byte-for-byte in all later custody transfers.
