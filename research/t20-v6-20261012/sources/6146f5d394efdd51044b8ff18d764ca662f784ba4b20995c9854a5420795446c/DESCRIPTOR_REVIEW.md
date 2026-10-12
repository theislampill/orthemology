# Independent frozen constructor-descriptor review

Verdict: PASS for the frozen descriptor/encoding layer only.

Candidate identity: `hase-certificate-code-validity-20261010/validation/DESCRIPTION_FREEZE.json`.

Fresh selected Lean 4.19.0 `--trust=0` replay compiled AuxiliaryCodeCore, StepCode, PolyCode, ConstructorDescriptors, CertificateDescriptions, and two independent review modules. All 96 actual-constructor encoding equations and nine primitive-recursiveness theorems passed an axiom audit, allowing only propext, Classical.choice, and Quot.sound. The freeze and all selected retained source/import/toolchain pin entries matched before and after. No frozen source or author's receipt was edited, and the protected baseline was not rebuilt.

Independent coverage extraction compared retained declarations directly with SCHEMA.json: names, order, arities, and field types agree for 5 StepCert, 2 RedCert, 7 FiniteCert, 8 PolyCert, 2 LookupCert, 6 Claim, 63 Rule, 1 SerialCert, and 2 SerialCertList constructors. The 96 compiled equations verify exact retained external leaf wrappers versus unwrapped recursive fields and exact payload packing.

Nine independent kernel controls establish:
- Local shape admits a StepCert payload containing invalid Term code zero and a Claim payload containing invalid Tel code one. Local shape is not global canonical validity.
- SerialCertList cons with zero payloads is locally well formed and exposes both expected-sort dependencies `(13, 0)` and `(14, 0)`.
- Unsupported StepCert and Rule tags reject locally.
- A node where an external leaf wrapper is required rejects locally.
- A nonzero payload terminator rejects locally.
- Term.zero and TypeCode.bottom have identical natural encodings. Sort-indexed expected-domain checks cannot be replaced by global numeric-sort disjointness.

One reviewer-control attempt overflowed the kernel reduction stack when `decide` expanded the concrete unsupported Rule tag 63. Rewriting only that control with symbolic `simp [localShape, ruleDescription]` passed. The failed source/log are retained; this was a test-proof reduction problem, not candidate acceptance or a candidate source repair.

Evidence: DESCRIPTOR_REVIEW_RECEIPT.json, DESCRIPTOR_REVIEW_PINS.json, SCHEMA_COVERAGE_RECEIPT.json, descriptor-replay-final/, DescriptorReviewControls.lean, and DescriptorReviewAudit.lean.

No global certificate canonical-validity theorem, original decoder equivalence, checker computability, source derivability enumeration, or T20 closure is accepted here. The global grammar layer remains subject to a separate final freeze and review.
