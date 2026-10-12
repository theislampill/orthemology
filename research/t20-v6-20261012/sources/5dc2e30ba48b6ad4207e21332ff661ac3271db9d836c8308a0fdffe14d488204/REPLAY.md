# Replay this independent check

Prerequisites are the same local sealed inputs and Lean/package paths recorded in `RECEIPT.json`. Inputs are read-only. The driver does not fetch dependencies or run author scripts.

Create a new empty output directory. Copy `rebuild.py` and `controls.py` there and execute `python rebuild.py` from that copy. It will verify the pinned archive, canonical Git blobs, package revisions and source identities, then freshly create `sources/`, `artifacts/`, and `evidence/`, build 30 local modules, and audit all 19 targets. An existing output directory containing those directories is deliberately rejected.

After the fresh rebuild succeeds, copy the supplied `sources/ScopeControls.lean` into the new output's `sources/` and execute `python controls.py` from the new directory. This proves the 13 independent controls, reads their exact types/axioms, and checks the three expected compiler rejections. The main inputs are not changed.

Author-reported types/axioms are comparison data only: the independent audit elaborates each target, inspects the compiler's checked environment and theorem/definition kind, invokes Lean.collectAxioms, and emits its own #check / #print axioms output. Review `RECEIPT.json` and `CONTROLS.json` statuses and the complete evidence logs rather than relying on object hashes alone.

`MANIFEST.json` binds the delivered report, scripts, fresh sources, artifacts, receipts, and retained control-draft failure. `SEALED_RESULT.json` and the archive SHA256 sidecar identify the delivery archive; they are external to that archive to avoid self-reference.
