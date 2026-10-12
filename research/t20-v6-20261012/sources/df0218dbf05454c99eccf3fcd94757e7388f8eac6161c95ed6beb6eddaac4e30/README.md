# Tensor likelihood closure independent review

Read REVIEW.md for the result and its scope. No blocking main-theorem defect was found; two wording/scope clarifications and one explicitly handled dependency drift are recorded.

Portable replay, from this directory:

    python3 independent_controls.py
    python3 replay_author.py --portable

Expected results: 12 independent exact groups and 13 original author groups. The author_replay tree is intentionally included and bound: it preserves the exact old cone dependency needed by the frozen tensor checker. The prior cone bytes were reconstructed by reversing two recorded edits and verified against the original digest; this is disclosed in the review.

The no-flag replay_author.py is a diagnostic for the original workspace's mutable sibling paths, not the portable archive command. MANIFEST.json lists hashes of all delivered artifacts other than itself.

Ordinary mathematical AI review only. No formal audit, formal kernel certification, field-wide novelty, empirical warrant, repository integration, or T20 closure is conferred.
