# Scoped portable replay

From the extracted checkpoint root run:

    python3 PACKING/check_manifest.py
    python3 PACKING/replay_python.py --output [OMITTED_PRIVATE_MACHINE_PATH]

Use a new output directory outside the checkpoint. Python 3.12.14 was used here; the twelve control commands require only the standard library. The harness creates a disposable copy, removes each expected generated output before its command, and compares newly produced bytes and/or stdout against the frozen results. The frozen checkpoint is hashed before and after. It does not write research outputs into the checkpoint.

The replay runs grouped author/reviewer, stable author/reviewer, interaction main author/reviewer, interaction-panel author/reviewer, absence author/reviewer and historical-transport author/reviewer controls. The historical reviewer also invokes the unchanged author control internally. Finite controls supplement the preserved written proofs; they do not prove unrestricted theorems by enumeration.

Six minimal inherited proof/manifest inputs are included solely for read-only digest checks. Their exact prior archive members are in PACKING/MINIMAL_REPLAY_DEPENDENCIES.json. No earlier stage control or historical T16–T20 package is rebuilt.

Original verify_evidence.py, verify_review.py and verify_receipt.py files are retained unchanged for provenance. They can depend on deliberately omitted predecessor directories and are not advertised as portable one-command verification from this compact ZIP. The included harness is the explicitly scoped portable route.

PACKING/REPLAY_RECEIPT.json is the successful staged run. The extraction receipt beside the ZIP records a fresh-extraction manifest check and the second scoped replay. The initial packaging-only dependency omission is documented under PACKING/initial-delivery-replay; no research script or expected result was altered to repair it.

No fresh Lean verification was performed. No Lean, mathlib or compiled payload is required or bundled. Source URLs and hashes are preserved evidence metadata, not a source-text download or fresh reading claim.
