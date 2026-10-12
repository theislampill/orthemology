# Replay and scope

Run from the retained workspace:

    python valid-initial-partial-escape-20261010/check_controls.py

The script verifies the bound source hashes, then performs exact rational and symbolic finite controls. The reported pass count is 7,888. It writes CONTROL_RESULTS.json; its timestamp can change on replay. A replay does not prove the infinite theorem, which is the ordinary argument in RESULT.md.

RESULT.md is the complete proof deliverable. INPUT_BINDINGS.json distinguishes original paths from frozen copies. The law-persistence candidate is context only, not a dependency. The ordinary full-functional source and the later full-functional Lean report/receipt are separately bound so that their verification statuses are not confused. The present analytic counterpath and signed-measure construction are not kernel-checked.

FROZEN_MANIFEST.json records the author's frozen files immediately before independent review. AUTHOR_RECEIPT.json is author evidence only, not a review verdict. No protected source or accepted theorem is edited.
