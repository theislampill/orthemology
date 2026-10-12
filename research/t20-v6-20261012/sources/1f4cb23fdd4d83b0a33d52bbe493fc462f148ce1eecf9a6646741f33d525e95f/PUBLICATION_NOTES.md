# Additive public packaging

The scientific source freezes and independent acceptance are unchanged. Their
historical status fields and path-specific helpers are intentionally preserved.
The later independent acceptance receipt supplies the accepted disposition;
the earlier author manifests alone do not.

Only README, REPRODUCING, public dependency metadata, ORIGINAL_TO_PUBLIC,
PUBLIC_MANIFEST and replay.py are new packaging. They neither edit nor extend
the reviewed theorem statements. Public replay explicitly includes Regression
and all supplementary/independent controls.

The packaging-evidence directory records the public entrypoint validation before
these evidence files were added to the ZIP. Its manifest hash therefore names
that earlier staging snapshot, not the final archive. The final archive's
fresh-extraction replay and ZIP digest are bound by the separately delivered
ATTRIBUTION_KERNEL_PUBLIC_REPLAY_RECEIPT.json. This avoids a self-referential ZIP
hash and retains the exact validated scientific inputs throughout.
