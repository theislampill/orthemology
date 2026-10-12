# Replay plan for final bytes (not yet executed as final-packet verification)

## Preconditions

- Parent confirms final membership and independently reviewed versions of any Fisher/tensor or other continuation units.
- Preserve all reviewed input bytes. Do not rewrite reports, scripts, ledgers, manifests, receipts, or historical source notes to make a check pass.
- A changed reviewed target needs its own applicable updated review receipt; merely repackaging it does not extend review coverage.
- Requirements for current scripts: Python 3 and SymPy 1.14.0. Current replay uses retained text and exact algebra; no network, PDF acquisition, browser, or protected repository access is needed.

## Existing replay entry point

From the eventual extracted packet root, run:

    python geometry-transport-independent-review-20261009/verify_review.py

This checks the reviewer manifest, exact reviewed-input hashes, both author manifests, source SHA-256/Git-blob identities, retained direct remote-pin observations, and exact stdout matches for these scripts:

    python geometry-transport-independent-review-20261009/check_independent.py
    python noetic-gradient-transport-20261009/verify.py
    python information-geometry-transport-20261009/verify.py

Expected preserved counts: 45 independent controls, 33 noetic control groups, and 61 information checks including source bindings. The existing logs and exact PASS receipt are retained. The final replay must execute the actual scripts from a genuinely fresh extraction and compare their outputs to the preserved logs.

## Final archive procedure, once authorised

1. Freeze membership; verify every review receipt against its listed exact target bytes and document separately unreviewed material.
2. Verify the portable subset has no PDFs, scan images, raw transcripts, cached environments, or unrelated temporary files. Preserve source URLs, identity hashes and actual reading boundaries where known. Never invent a missing PDF-byte hash.
3. Regenerate an exhaustive manifest over the final payload and add a final scope/index describing all included units and exclusions.
4. Create a separate archive while leaving all original inputs unchanged. Record archive size and SHA-256 externally.
5. Fresh-extract into a new directory. Verify all manifest sizes/hashes, path safety, review bindings and listed-only membership before executing controls.
6. Run the existing replay entry point and separately reviewed continuation replay commands, saving stdout, stderr and exit codes outside immutable source paths.
7. Check byte-identical output where the retained contracts require it. Reverify all source hashes and manifest entries after execution.
8. Produce a final external receipt binding the archive, manifest, fresh extraction path, actual exits and control counts. Do not call the whole packet verified before these final-byte steps succeed.

## Philosophical note boundary

The duty bridge has no mathematical certification script or independently mathematical review receipt in this stage. Its manifest can establish byte identity for included inputs and retained metadata, but omitted source images/full body text must remain disclosed. Replaying the mathematical units cannot convert the duty note into independently mathematically reviewed material.
