# Portable assurance checks

From the extracted checkpoint root:

```
python3 PACKING/check_manifest.py
python3 PACKING/replay_python.py --output [OMITTED_PRIVATE_MACHINE_PATH]
```

The output directory must be outside the checkpoint. The replay copies the complete packet into disposable scratch, deletes each generated output before its named control, executes the twelve unchanged programs in `PACKING/CONTROL_PLAN.json`, and requires byte-identical outputs/stdout. Original packet files are hash-checked before and after. Python optimization is disabled so assertions run.

The recorded interpreter is Python 3.12.14; the only external requirement is SymPy 1.14.0 for the finite-panel symbolic script. The checkpoint does not bundle/install Python packages. A missing package or different environment is a replay blocker, never a fabricated pass. That script prints version text, so exact frozen stdout requires the recorded versions.

The bounded independent control additionally hashes 91 inherited files. Those precise immutable dependencies are included and itemized; it does not rerun their historical scripts. Two inherited replay-contract texts are also preserved. All other listed controls use only their own code/outputs and delivered theorem/review hash bindings.

The original stage-level full verifiers are outside this portable replay scope. Some require excluded raw primary sources or historical corpus. Their historical PASS records are not fresh passes. In particular the hypergraph composite verifier remains UNREPLAYED here, and the same-threshold reviewer `verify_evidence.py` is a mutating authoring workflow. See `EVIDENCE_BOUNDARIES.json`. Never fill omitted files with stubs, edit hashes to bypass checks, or call this harness a replacement for a full original verifier.
