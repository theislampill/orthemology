# R5 Review A — current-state / false-closure attacks

Surfaced model: `claude-fable-5`. Five attacks executed live against the tree; every one must fail a validator, and did:

| Attack | Defender | Result |
|---|---|---|
| STATUS reverts to "CANDIDATE PASS, REQUIRES INDEPENDENT REVIEW" | validate_review_state (banned phrase + wording) | DEFEATED |
| primary header drifts to "candidate revision pending independent review" | validate_review_state | DEFEATED |
| Decision 0011 drops its review-discharged notice while registry says adopted | validate_review_state (pairing rule) | DEFEATED |
| pre-merge fresh-review state JSON reclassified `current` in the historical index | validate_review_state (classification rule) | DEFEATED |
| item-7 discharge banner stripped from the R4 owner-actions snapshot | validate_review_state | DEFEATED |

Clean tree back to 0 failures after each restore. No blocking findings.
