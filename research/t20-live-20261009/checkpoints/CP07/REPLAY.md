# Portable delivery-assurance replay

From the extracted checkpoint root:

```
python3 PACKING/check_manifest.py
python3 PACKING/replay_python.py --output [OMITTED_PRIVATE_MACHINE_PATH]
```

Keep the output outside the checkpoint. The harness makes a disposable copy, deletes each declared generated output before execution, runs only CONTROL_PLAN.json commands, requires matching frozen outputs/stdout, and checks the original packet hashes before and after. Assertions remain enabled. A replay with no frozen stdout target checks exit status plus every listed generated file; this is stated in its receipt.

Recorded environment: Python 3.12.14, SymPy 1.14.0, mpmath 1.3.0. Packages are not bundled or installed. Missing dependencies block affected replay; they never imply a pass. Exact stdout containing version text requires the recorded versions. High-precision and binary64 diagnostic output may be platform-sensitive; any discrepancy must be reported rather than rewriting frozen expectations.

The original fixed-pair read-only verifier is included with its exact prerequisites. All-rate verifier scope is stated in CONTROL_PLAN.json. Included inherited research scripts are hash inputs only and not rerun. No claim is made about an unlisted historical/full-source verifier. Do not create stubs for omitted sources, change frozen hashes or run mutating original authoring workflows in a frozen tree.
