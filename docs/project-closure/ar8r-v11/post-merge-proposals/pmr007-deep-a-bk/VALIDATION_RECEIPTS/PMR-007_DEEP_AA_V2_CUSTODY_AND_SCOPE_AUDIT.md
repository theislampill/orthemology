# PMR-007 Deep AA V2 custody and scope audit

```text
identity: PMR-007-CGIP-1
input_version: V2
disposition: REPAIR_REQUIRED
review_relation: same-session custody and scope audit; not external independence
```

## Blocking custody finding

### AA-CUST-F01 — one frozen source owner is absent

`PMR-007_DEEP_AA_V2_FROZEN_HASHES.sha256` names:

```text
checks/pmr007_deep_aa_causal_guidance_primary_check_v1.py
expected SHA-256:
d6b0b06d761f1316b9848d57b4843c9ece38015b9b484d6ee0d4901747580670
```

The live research directory contains the corresponding JSON result but not the
checker source. The missing bytes cannot be reconstructed as the historical
file or treated as hash-verified. V2 therefore cannot pass complete frozen
custody.

## Scope attacks retained from V1 audit

The V2 statement is substantively bounded correctly only if the following
remain explicit:

1. `Score` is an encoded control state, not normative authority.
2. `do(Score)` establishes causal relevance only inside the frozen SCM.
3. Personal and impersonal twins establish intended-class logical
   nonentailment, not actuality, metaphysical possibility, or equal
   probability.
4. Key authority, semantic anchoring, world adequacy, and norm authority are
   carried assumptions.
5. Intentional uptake, selection because of fittingness, first-person
   ownership, personality, and Wisdom are not recoverable from the neutral
   reduct merely by naming them.
6. Source-relative predicates do not migrate into neutral entailments.
7. OSM, daee, human cognition, fiṭrah, and divine-attribute interpretations are
   not validated by the finite SCM.

## Required repair

Preserve V2 and its missing-file record. Create a custody-complete V3 with:

- a newly written primary checker whose provenance is explicitly post-boundary;
- a distinct checker using a different relational/intervention construction;
- a new frozen-hash receipt containing every exact V3 owner;
- an independently verified observational-equivalence/interventional-
  divergence control outside the frozen SCM;
- no admission overlay until the distinct rereview passes.
