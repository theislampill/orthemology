# One-command archive verification

From the extracted archive root, with Python 3.11+:

    python3 -B verification/verify_native_integration.py --root .

Only the standard library is needed. The command checks finite members, hashes/lengths, checksum manifest, source reconstruction, original-container safety, actual native patch/clean-apply fields, and two distinct review scopes: inherited whole review at fadbecad and the new final-tree delta review. It refuses scope/hash substitution.

The exact finite OWNER_LINK_RECEIPT.json was parsed during assembly with the already installed native Markdown parser. This command needs no Markdown parser installation. It verifies the recorded source bytes and recomputes each local target relative to the actual owner document, including target byte identities. Merely finding an archive-root alias does not satisfy a nested relative URL. Scope is the receipt's named Markdown files; fragment anchors, raw HTML and external URL availability are not claimed.

To verify/extract the outer ZIP into a fresh destination, use owner_archive.py verify-zip, then run the one-command native verifier on the extracted root. Existing destinations, unsafe/colliding paths, symlinks, alternate ZIP filename metadata, changed bytes and inconsistent modes are refused.

These checks do not execute Git application, scientific research, native gates or network operations. The archived native receipts own those execution claims. Required exact PDF CI remains blocked locally, and old-head CI is not final-candidate CI. Original receipt paths keep their execution-context meaning; PATCH_PAYLOADS.json and NATIVE_RECEIPT_BINDINGS.json give the exact included archive paths.

No seal, upload or remote mutation is performed by verification. Final sealing separately requires root approval of the exact recomputed delivery-content contract digest.
