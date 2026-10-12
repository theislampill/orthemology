# Correlated-target independent review

Read REVIEW.md for the frozen-candidate disposition and INDEPENDENT_DERIVATION.md for the separate ordinary proof. No blocking mathematical finding. The author snapshot is unchanged; no protected edits or integration were made.

From the workspace root:

    python3 correlated-target-independent-review-20261011/check_independent.py --output-dir private-locator:f83921ed302462db6796
    python3 -O correlated-target-independent-review-20261011/check_independent.py --output-dir private-locator:7f9ea78d0d827c05cb35
    python3 correlated-target-independent-review-20261011/author-snapshot/verify.py --output-dir private-locator:981251901413a325a17f --original-root .
    python3 correlated-target-independent-review-20261011/verify_bindings.py --original-root .

For a portable replay without the live original workspace, omit --original-root on the two commands accepting it. The copied author verifier still checks its own frozen dependency snapshots. Write replay outputs outside this frozen packet. The mathematical and identity checks are distinct. Neither changes external state or confers audit closure authority.
