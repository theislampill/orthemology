# Fixed marginal correction review packet

REVIEW.md gives the finding, ordinary proof review, source boundaries, participating contributions, and the conditional-recentering feasibility/optimality distinction. REVIEW_BINDINGS.json records frozen author custody and fresh replays. Author bytes are retained unchanged in author-snapshot/.

Run the independent controls with:

    python3 check_independent.py --output-dir private-locator:991caaac95655d090024

Replay the author snapshot portably with:

    python3 author-snapshot/verify.py --output-dir private-locator:f2cc7ef0fd49780bc4da

The original author replay additionally used --original-root with the workspace root. It passed 49 controls; the portable replay passed 43 because original-location checks are optional. All 50 independent symbolic controls passed. The analytic Hilbert, inequality, ODE, and scope arguments remain ordinary written proofs.

The reviewer-supplied rate-six inequality is expressly participating, not independently certified by its originator. The initial mislabeled recentring control and its passing output are preserved under snapshots/; the final checker explicitly verifies feasibility and the optimality gap. No author edits, protected integration, or T20 closure.
