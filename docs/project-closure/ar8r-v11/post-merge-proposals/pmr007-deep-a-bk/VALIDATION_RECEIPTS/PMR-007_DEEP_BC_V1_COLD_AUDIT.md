# PMR-007 Deep BC V1 cold audit

```text
disposition: REPAIR_REQUIRED
candidate: PMR-007-UIEP-1 V1
primary executable result: PASS
review relation: same-program cold audit over frozen bytes
external independence: NOT CLAIMED
```

## Blocking findings

### BC-F01 — mutual Blackwell equivalence is not preserved by arbitrary same-named post-processing

V1 says that mutual Blackwell equivalence is preserved under every common
kernel `K`.  This is false without a commuting/alignment condition.  Two
experiments related by a signal permutation are decision equivalent, but
applying the same asymmetric channel to their unaligned signal names can yield
different postprocessed experiments.  V2 must restrict unconditional
postprocessing preservation to **identical aligned experiments**.

### BC-F02 — primary equality-postprocessing test is tautological

The primary checker compares `mul(E,G)` with itself.  It does not test a second
independently constructed copy or the alignment issue.  The V1 output remains
preserved, but V2 requires a meaningful signal-permutation/noncommuting-channel
control.

### BC-F03 — controlled-system corollary needs policy transport

Quotient isomorphism and equal transition/output laws induce equal transcript
experiments only when initial laws, action names, policy information, and
policy choices are transported under the isomorphism.  Candidate-specific
policies or differently interpreted actions define different experiments.

### BC-F04 — expected-reward decision scope

Garbling dominance is stated for finite expected-reward decision problems with
a common prior and utility.  It is not a theorem for every non-expected-utility,
robust, lexicographic, deontic, or source-authority decision theory.

### BC-F05 — experiment completeness is assumed

Equality of a registered transcript law may reflect an impoverished horizon,
sensor, action set, or source/world map.  The result relocates the burden to a
new experiment; it does not show that no such experiment exists.

### BC-F06 — metaphysical and source parity overreach

Decision equivalence under a frozen experiment is not equal metaphysical
possibility, prior probability, source truth, or actual-world fit.  V2 must
repeat those ceilings in the central conclusion.

## Nonblocking notes

The forward garbling simulation proof is standard Blackwell decision theory.
General mathematical novelty is zero.
