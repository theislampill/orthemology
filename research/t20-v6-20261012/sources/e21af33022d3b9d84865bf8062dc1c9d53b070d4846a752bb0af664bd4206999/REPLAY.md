# Independent review replay

Use Python 3.12.14 and SymPy 1.14.0 for byte-identical comparison with the frozen author reports.

    python check_review.py --output-dir /absolute/fresh/replay-directory

The output directory must not exist and must be outside this frozen review packet. This verifies the review manifest, the copied author manifest and all 13 payload hashes, replays the portable author checker (25 checks), and runs 29 independent exact controls.

To additionally check the unchanged original author packet, its six bound predecessors, and all 14 payload files in the earlier nonconvex limit packet, add:

    --original-root private-locator:8f24556a330b05a11a95

That adds the original-aware author replay (31 checks). No source file is modified. Fresh author reports must match the frozen reports byte for byte; their interpreter-version fields make the stated versions relevant. The independent report also records the interpreter and SymPy versions.

This replay verifies identities, countercontrols, and evidence preservation. The universal theorem is evaluated in the written REVIEW.md. No formal-kernel verification, external peer review, protected integration, or T20 closure is asserted.
