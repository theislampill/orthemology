# PMR-007 Deep AW V1 cold audit

```text
disposition: REPAIR_REQUIRED
frozen packet: PMR-007_DEEP_AW_V1_FROZEN_HASHES.sha256
review relation: same-session procedural cold audit
external independence: NOT CLAIMED
```

## Blocking findings

### AW-F01 — adversarial errors were conflated with identified erasures

V1 used `d_R>f` for both.  Exhaustive checking found 1,248 error-threshold
failures.  A distance-two code survives one known erasure but cannot correct
one unmarked substitution.  Repair to:

```text
erasures: d_R >= f+1;
adversarial substitutions: d_R >= 2f+1.
```

### AW-F02 — the corruption unit needs exact provenance semantics

The theorem counts authenticated roots, not messages, tests, witnesses, or
files.  Every output derived from one root is jointly corruptible in the
model.  Multiple within-root tests may be bundled into one root-level symbol,
but they contribute at most one Hamming coordinate.

### AW-F03 — root authentication and independence were presupposed

Displayed labels can alias one root, and apparently separate institutions can
share a common cause.  The theorem begins only after actual corruption units
are authenticated.  It cannot certify that premise or creed-internal tawatur.

### AW-F04 — the root response was static and deterministic

The code model assumes one candidate-independent root response symbol per
hypothesis, fixed version, and fixed membership.  Adaptive queries, stochastic
responses, history dependence, dynamic membership, collusion across roots, and
mobile adversaries require separate models.

### AW-F05 — error model and adversary timing were underspecified

Specify a worst-case adversary that may replace all information from at most
`f` selected roots after seeing the code and true hypothesis.  The decoder sees
root positions but not which substitutions are corrupt.  Erasures are marked.

### AW-F06 — diagnosis was too close to warrant and action

Correctly decoding a hypothesis label does not establish source truth,
certificate authenticity, recipient warrant, authorization, applicability,
adoption, execution, common knowledge, or stable restoration.

### AW-F07 — selection ancestry and complexity were missing

For `f=0`, selecting a minimum root subset that separates every hypothesis pair
is Test Cover.  For general `f`, it is a pair-separation multicover.  Robust
coding uses the classical Hamming-distance mechanism.  No new general coding or
complexity theorem is eligible.

### AW-F08 — copies and aliases need explicit countermodels

A copied root may make forty apparent messages but contributes one corruption
coordinate.  Conversely, contracting two displayed roots after authentication
can lower minimum distance.  Preserve both controls.

## Required repair

1. Preserve V1 and its 1,248 error-threshold failures.
2. Prove separate error and erasure characterizations.
3. Type the root-level code, adversary, decoder, version, and membership.
4. Prove the root-subset pair-multicover criterion.
5. Deny warrant, truth, authorization, and common-knowledge transfer.
6. Run a distinct ternary-alphabet rereview with independent Hamming-ball
   construction.
