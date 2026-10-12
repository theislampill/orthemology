# P03 exact-source qualification and modeled refinement

Start with QUALIFICATION_STATUS.json, then constructor-square/SOURCE_MAP.md and constructor-square/NATIVE_DECODER_SCOPE.md.

The supplied attempt-0002 remains immutable. Its graph/VCT source initially failed exact Lean 4.19.0 compilation; the separate shadow repairs actual recursive-index and guarded-authority proof defects without weakening the main target. A readback-regex defect was separately repaired and tested. See CHANGE_LEDGER.json, patches/, baseline-formal/ and repaired-formal-2/.

New work then supplies an independently evaluated seven-rule source-AST checker, a resource-aware evaluator, explicit trace/substitution correspondence, a partial constructor-export square, and a validated finite native-tree decoder. The native grammar has exact fields, explicit duplicate policy, arbitrary field-order completeness and refusal-preserving outcome equivalence. See constructor-square/fresh-build-3/RECEIPT.json for a fresh build of 24 modules and 30 type/axiom readbacks.

This does not certify the actual CPython interpreter, raw UTF-8/JSON library, mutable snapshot capture, complete registry/locking runtime or all textual exporter behavior. Source-check success does not imply exporter success: a verified 7,916-node input exceeds the distinct 512-constructor export gate. No repository adoption, historical identity or canonical obligation closure is implied.

Concrete execution results and exact source identities are preserved in evidence/, export-probes/, constructor-square/cross-language-final/, constructor-square/work-accounting/ and constructor-square/native-cross-language-final/. Earlier failed proof/harness attempts remain as diagnostic history; only the named fresh receipts establish accepted builds.

P02_INTERFACE_DELTA.md records the newer P02 handoff separately. It does not rewrite the attempt-0001 dependency used by the original P03 checkpoint.


## Sealed successor and reproduction

MANIFEST.json binds every payload file; RECEIPT.json binds that manifest and the qualified scope. The outer ZIP SHA and fresh reopen report are external, avoiding circular hashes. The exact original P03 attempt-0002 ZIP is embedded under inputs/.

Current authoritative proof receipt: constructor-square/fresh-build-final/RECEIPT.json. Earlier failed and successful build logs remain historical evidence. Only fresh-build-final contains the full current model object set; cross-language-final, native-cross-language-final and work-accounting retain the current named fixture objects. Graph repair objects remain under repaired-formal-2. Old duplicate object files are omitted while their exact receipt digests/logs/sources are preserved.

Rebuild from an extracted successor with the exact archived Linux Lean 4.19.0 executable:

    python -B constructor-square/verify_fresh.py --lean /path/to/lean-4.19.0-linux/bin/lean --out /fresh/output/directory

The driver requires an empty output path, verifies the pinned native executable identity, copies both inherited owners and every current model source into it, compiles from that fresh source set and checks all thirty type/axiom readbacks. It downloads nothing. The fixed-name tests, raw JSON fixtures and historical Python scripts are preserved; some historical scripts retain their original absolute execution paths as evidence.

This sealed object is ready for a new independent review of the native extension. The previous source-model review does not automatically review the later native decoder.
