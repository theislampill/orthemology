# Lean status: candidate source only

`BridgeDiagnostics.lean` contains thirteen fully written declarations corresponding to selected written lemmas and the rotating-witness control. **It has not been compiled here.** No Lean executable was found; network/toolchain acquisition was unavailable in the producing environment. Its presence in a verified archive does not give it kernel credit.

The successful executable evidence for this delivery is the exact Python replay. It is independent of this file and cannot certify Lean elaboration or its axiom readback.

For optional follow-on qualification, use an existing Lean 4.19.0 toolchain in a disposable directory:

```sh
/absolute/path/to/lean-4.19.0/bin/lean BridgeDiagnostics.lean
```

Read the declaration signatures and `#print axioms` output. No installation, Lake project or Mathlib is required by the source. Do not change inherited results or claim a philosophical conclusion merely because compilation succeeds. These candidates contain no `sorry`, user `axiom` declaration, or `native_decide`, but that text inspection is not a compiler run.
