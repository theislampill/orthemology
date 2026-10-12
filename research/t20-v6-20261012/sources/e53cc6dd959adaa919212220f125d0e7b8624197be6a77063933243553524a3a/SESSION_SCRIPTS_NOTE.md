# Scope of preserved reconstruction scripts

The three adjacent reconstruction scripts are an audit trail of this review's local source reconstruction. They contain original `/mnt/data` session paths and intermediate-stage checks. They are **not the portable packet entry point** and should not be run against a repository. The final, all-true record is `PUBLICATION_RECONSTRUCTION.json`; early stage results are not claimed as final.

The reviewer found and corrected an initially overbroad identifier matcher during local reconstruction before accepting the final tree. That temporary attempt was never used to alter GitHub, and its wrong reconstructed sources are not distributed as the authoritative public tree. The final exact Git subtree match and complete bindings determine the accepted result.

Use `../../tools/verify_packet.py` for portable read-only packet verification. The original private alias map is deliberately retained here for the owner; do not publish it.
