# PMR-007 Frontier Round 18 V3 cold audit

```text
audit epoch: ROUND18-EPOCH-B3
result: REPAIR_REQUIRED
blocking finding: R18-V3-F01
```

## R18-V3-F01 — exact label recovery is not necessary for robust relation selection

Use four states and four complete certificate objects with

```text
H(q_i) = K minus {k_i}.
```

Encode the four states by all binary words of length two.  After at most one
adversarial bit flip, the receiver's ambiguity set is a radius-one Hamming ball
containing exactly three of the four states.  The intersection of their
admissible-object sets is the singleton object omitted only by the fourth,
excluded state.  Hence a robust admissible object exists for every received
word despite complete failure of exact state-label recovery.

Even exact recovery of a nonconstant binary selector under one adversarial bit
flip needs a length-three repetition-style separation.  Exact recovery of all
four state labels needs length five.  Robust relation selection here uses
length two.

Therefore the minimum-distance condition is sufficient for exact label
recovery but is not necessary for the certificate-selection relation.

## Required repair

For code `c`, observation `o`, received word `y`, and error radius `r`, define

```text
B(o,y) = {q : obs(q)=o and distance(c(q),y)<=r}.
```

A robust relation selector exists exactly when every nonempty ambiguity set has

```text
intersection_{q in B(o,y)} H(q) nonempty.
```

Keep minimum-distance coding only as the explicitly stronger exact-label
recovery special case.

## Disposition

```text
V3: BLOCKED_FORMAL_DEFECT
historical identity: NONE
repository proposal: NOT_REPOSITORY_READY
```
