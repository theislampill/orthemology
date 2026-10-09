# Reviewer harness correction

The first symbolic-control run passed the determinant polynomial identity, then failed a secondary assertion comparing unevaluated SymPy matrix expressions with structural `==`. Expanding the entire difference independently produced the zero matrix. The assertion was corrected to compare that expanded polynomial difference with the zero matrix. Final replay passes. This was a reviewer-test representation issue, not an author determinant failure.

The exact-rational controls passed before and after adding the separate interior/compression extension. Final shell replay uses `set -o pipefail` so Python failure cannot be masked by `tee`.

The initial frontier incorporation binding detected an author change while packaging (the explicit delta domain was added). Its hash assertion correctly prevented a stale receipt. The full updated main report was reread, then rebound to SHA-256 89b17388c4f243f555dbcb2232a3f106683cc3cc23edf0e3f7371bec3e018db7.
