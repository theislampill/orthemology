# Fixed-pair replay lower-bound review

Start with REVIEW.md for the bounded mathematical verdict. REVIEW_RECEIPT.json binds the exact frozen author artifacts and prerequisite results; MANIFEST.json binds this review's own payload. FINAL_VERIFICATION.json records the latest verification output. No verdict applies to unbound author changes.

INDEPENDENT_DERIVATION.md was recorded and hashed before the author RESULT.md was read. It gives the all-n argument and finite-prefix stopping proof. BOUNDARY_ATTACKS.md records the contracts whose removal breaks the argument. SOURCE_AUDIT.md identifies attribution and the precisely targeted external reading.

Reproduce the independent exact controls with python independent_controls.py. Its output is deterministic. Verify all bound source/payload bytes with python verify_review.py. Author controls are copied under author_snapshot so any reviewer replay avoids modifying the original author packet.

Finite exact examples supplement the analytic proof. This packet makes no empirical validation, formal kernel verification, physical capability, protected-integration, checkpoint-inclusion, research-readiness, or T20-closure claim.
