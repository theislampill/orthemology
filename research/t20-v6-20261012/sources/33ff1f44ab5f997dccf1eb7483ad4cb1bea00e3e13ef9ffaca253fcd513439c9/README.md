# Orthemology P03 — engine refinement research checkpoint

**Disposition: PARTIAL for U03, U04 and Q1f.** The scoped research and portable delivery are complete; the primary universal/formal obligations are not closed. This checkpoint is separate proposal work, not canonical implementation or integration replay.

The preserved merged boundary is main `03e2604dfcef278b01c60d19b05370fcec4194b6`, tree `3d06e80277ce39286c94307e0f14b215bc94ed83`, PR #28 merged, no Integration DAG cells remaining. No GitHub write, merge, release, public-index change, source-status promotion, owner-policy adoption, external review, empirical/world authority or historical recovery credit occurred. Reading pinned public R15/R16 sources does not grant any of those effects.

## Results and open gates

| Obligation | Result delivered | Why the obligation remains PARTIAL |
|---|---|---|
| U03 — whole parser/checker/exporter refinement | Two concrete counterexamples; two tested repair proposals; ordinary shift/substitution argument; checker/export constructor mapping; budget/refusal interface; bounded independently structured comparison | No whole-Python/JSON formal semantics or extraction proof; native ownership and host exceptions remain explicit; exported Lean syntax was not kernel checked here |
| U04 / CV-O — implementation refinement | Complete Gamma/issued-record/lock-state proposal; read-set, absence, version, persistence and atomicity/linearisation analysis; deterministic input-mutation counterexample and tested snapshot repair | Full concurrent-history and failure-refinement proof remains open; U03 and probability-extension interfaces cannot be presumed passed |
| Q1f — guarded reason/version base and optional TRC | Exact pinned R15/R16 source comparison; two graph countermodels against an untyped extrapolation; ordinary ranked-DAG argument; new graph-only Lean proposal; explicit full-VCT and optional-TRC gates | No new Lean execution; graph transport is not warrant transport; target-indexed evidence, authority/version semantics and P12/DAEE wrapper dependencies remain open |

### Three concrete findings

**P03-U03-CE01:** The unchanged encoder can return 202 bytes containing 101 nested containers which its own decoder rejects at the JSON depth guard. The witness is a transport value, not a false certificate. The proposal refuses that encoder output without weakening the decoder.

**P03-U03-CE02:** Malformed native exporter rows escape through `TypeError`/`ValueError` before structured rejection. The proposal validates row type/arity before unpacking. Its exact list/tuple row grammar is an explicit proposed restriction of formerly tolerated arbitrary two-item iterables, requiring later review.

**P03-U04-CE01:** An observation setter validates caller-owned values before waiting for the registry lock but copies them only after obtaining it. A deterministic test changes those values during the wait, causing successful commitment of unvalidated data. The proposal validates and commits one bounded flat tuple captured before the wait. It does not claim universal deep-snapshot safety or refute the existing lock-held check/use result.

The two Q1f graph countermodels show why edge preservation, even with injectivity in the second example, does not by itself guarantee an acyclic target. They do **not** refute VCT when its declared finite-DAG premise is enforced. The new ranked-DAG encoding is a reviewable proposal, not a silent change to accepted source.

## Executed evidence

The final three-file source proposal passed **199 test methods in normal Python and 199 in optimised Python**: 183 supplied methods plus 16 new methods, across four commands per mode. The new regression tests first failed on unchanged original source. Raw commands, outputs, exits, source hashes and environment are in `evidence/`.

An independent finite specification compared **4,928 shifts, 94,864 substitutions and 3,405 head-step terms**, with no mismatch. These are bounded experiments, not universal or kernel proof. A fresh portable reconstruction matched all **70** candidate source files and again passed the 183 supplied methods in each Python mode.

Actual `lean --version` could not launch (exit 127); no new `.olean`, declaration/type readback or axiom readback is claimed. The helper's negative control rejects the real Python executable as the wrong pin; that is only a refusal test, not Lean proof evidence. The graph source and its five-target audit are **UNVERIFIED at Lean 4.19.0**. The exact later executor commands are supplied.

Accepted mapped-native 4.19.0 statements remain accepted only at their supplied scope. Separate 4.32.2 evidence remains separate. The original strict-wrapper genuine compiler FAIL is preserved as FAIL and is not relabelled as this conversation's missing executable. Old finite evidence, generic-wrapper non-novelty, repaired VCT/TRC negatives and inaccessible historical identities are retained.

## Reading map

Start with `inputs/OBLIGATION_CONFIRMATIONS.json` for exact original statements, statuses, predecessors and source hashes. `inputs/ACCEPTED_SCOPED_READBACKS.json` contains selected prior accepted type/axiom readbacks, explicitly not newly executed.

The substantive reports are `research/U03_REFINEMENT_AND_COUNTERMODELS.md`, `research/U04_COMPLETE_STATE_SIMULATION.md`, and `research/Q1F_SOURCE_COMPARISON_AND_PROPOSAL.md`. `research/NEGATIVE_FINDINGS.md` and `research/UNRESOLVED_DEPENDENCIES.md` state the remaining limits. `proposal/PATCH_MAP.json` binds the three exact preimages/postimages and diffs; the separate definition/status ledger identifies all proposed semantic/domain changes without adopting them.

`handoff/CODEX_IMPLEMENTATION_HANDOFF.md` gives isolated reconstruction, Python tests, pinned Lean commands, rejection gates and subsequent proof work. The helper scripts never require modification of an existing repository. No canonical manifest or public index has been regenerated.

## Custody and verification

The original uploaded ZIP is embedded unchanged:

```text
Orthemology_Pro_P03_Engine_Refinement.zip
bytes: 1819667
sha256: 050aac77db52ad70e0155bbeb76f903a4dae65a36977a4159c8dcaf5634bcab0
```

Its 621 manifest bindings, 619 receipt-output bindings, 541 source bindings and 54 accepted-evidence projection bindings verify. The source subset is not represented as a complete live checkout. Two supplemental public statement files were read at the exact frozen commit and matched their returned Git blob identities. Their bytes, hashes and source status are separate from the original input archive.

`MANIFEST.json` hashes all payload files. Four control members are deliberately excluded to avoid self-hash cycles: the manifest, its detached digest, the receipt and its detached digest. The receipt binds the manifest and its sidecar; deterministic sidecars and the detached outer ZIP digest cover the control chain. Every ZIP member is checked by the supplied fresh-process verifier, which also reopens the embedded original input and rechecks all its declared bindings.

The final outer SHA-256 and actual fresh-reopen result travel beside the ZIP, not inside a circular self-referential manifest. The external verification report includes the SHA-256 of every member. “Independent reopen” means a separate read-only verification process, not independent expert review or owner acceptance.

**Stop boundary:** this checkpoint ends P03's bounded research round. It grants no permission to expand into another research family.
