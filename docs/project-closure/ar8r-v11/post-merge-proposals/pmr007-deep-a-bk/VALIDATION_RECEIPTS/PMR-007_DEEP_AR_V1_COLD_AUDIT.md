# PMR-007 Deep AR V1 cold audit

```text
disposition: REPAIR_REQUIRED
same-model procedural relation: yes
external independence: no
```

## Blocking findings

### AR-F01 — actual root identity was assumed from labels

The theorem requires an independently authenticated root partition. Printed identifiers, carriers, routes, or storage nodes cannot define acquisition roots by stipulation.

### AR-F02 — distinct roots were treated as independent

Likelihood multiplication requires conditional independence given the candidate. Distinct root IDs or paths do not establish that factorization.

### AR-F03 — the retransmission channel was not required to be candidate-independent

A candidate-dependent transmitter can create evidence and is a changed experiment, not conservation under retransmission.

### AR-F04 — exact copies and lossy transformations were conflated

An exact likelihood-ratio-sufficient copy preserves the root ratio. A paraphrase or compressed message may lose evidence. The theorem must distinguish preservation from nonincrease.

### AR-F05 — support and logarithm conventions were incomplete

Likelihood and log-evidence statements require denominator/support guards. The additive log invariant applies only to finite positive ratios.

### AR-F06 — evidence ordering was overread

Total variation and likelihood ratios characterize a frozen hypothesis experiment. They do not yield truth, warrant, or a total ordering across unrelated experiments without a declared comparison.

### AR-F07 — provenance independence was allowed to migrate into warrant and tawātur

Machine root independence does not establish source truth, competence, impossibility of collusion, testimonial warrant, recipient applicability, mutual knowledge, or common knowledge.

### AR-F08 — ancestry and novelty ceilings were incomplete

The result composes standard data processing with AR2/AR3 provenance transport, false-tawātur controls, Round 19 root access, and T227 root authentication. General mathematical novelty is zero.

## Required repair

Create V2 with authenticated root partitions, candidate-independent channels, conditional-independence factorization, exact/lossy copy separation, finite-support guards, explicit warrant nontransfer, root alias/merge controls, and exact ancestry/novelty ceilings.
