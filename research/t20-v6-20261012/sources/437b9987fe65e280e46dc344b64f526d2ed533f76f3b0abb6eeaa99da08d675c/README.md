# Posterior deterministic checker construction formal supplement

Author candidate 1, submitted for independent source and kernel review. This six-module supplement formalizes the local restriction-preservation part of the separately accepted ordinary checker reduction. It does not assume posterior determinism, an ATM acceptance equivalence, or EXPTIME hardness as a Lean axiom.

## Exact constructed objects

- A checker state is a live tuple (checked index, stored symbol, machine control, head) or one of two terminal sinks. Both indices have type Fin m. For finite symbol/control alphabets its cardinality is proved to be m²|Γ||Q|+2.
- An action is a claimed read symbol and a Boolean branch choice. The supplied machine table specifies a written symbol, next control and signed integer head movement, and identifies universal controls.
- `advance` validates the checked cell's read, computes the signed next head, rejects an out-of-bounds move before examining even an accepting next control, updates only the checked cell when it is under the head, and handles the terminal controls.
- `kernel` is an actual Mathlib PMF on receipt/successor pairs. Existential rows are point masses. Universal rows are pushforwards of a normalized exact fair-bit PMF. Five receipts distinguish ordinary motion, the two universal branches, acceptance and rejection. Terminal branches sharing a receipt share their sink. Every joint entry is proved to be 0, 1/2 or 1.
- `initialBelief` samples one index uniformly in Fin m, with its supplied initial tape symbol, control and head. Its support is exactly the initial checker family. Every checker has mass 1/m, every such mass is positive, and the finite total is one. Nonempty(Fin m) is the positive-tape-size condition. No hidden selection transition is inserted.

## Main proved claims

`kernel_posterior_deterministic` proves that any fixed old state, action and receipt has at most one positive-probability successor in this constructed kernel. The theorem has no PD assumption. Some restriction lemmas are valid for more general alphabet carriers; the stated finite instance is supplied by Fintype and the explicit cardinality theorem.

`honest_running_step` proves the one-step global-tape coordinate invariant for every checker: a truthful read followed by a nonterminal valid machine step produces exactly the updated tape's corresponding checker. `honest_branch_receipt` and `honest_receipt_law` prove that truthful steps have the same actual public receipt distribution for every checked index, including terminal merging. They do not prove the full history, posterior, policy or alternating-language argument.

## Deterministic state observations

The lift retains three kinds of nonterminal last receipt and separate accepting/rejecting sinks. The actual state count is 3m²|Γ||Q|+2, and an at-most-fivefold bound relative to the source state count is proved.

`lifted_kernel_posterior_deterministic` proves the state-labelled unique-successor property. `lifted_joint_row_exact` proves that observing the next copy's label and erasing its extra receipt field recovers the original joint row exactly. This is a PMF equality, not a supplied correspondence premise. The accepting target is globally visible and absorbing. Erasing the mixed initial lift recovers the original belief, while its observation law is a point mass at the common ordinary label.

The copy function has a total fallback for an inconsistent nonterminal/terminal-label input. `kernel_support_valid` proves such an input is absent from every actual source row. Thus this fallback is unreachable, rather than an unacknowledged alteration of a received observation.

## Checked controls

Controls prove exact checked writes, retention of an unmonitored symbol, false-read rejection, rejection of accepting out-of-bounds moves on both sides of the tape, in-bounds acceptance, separate half-mass universal outcomes, merged terminal branches, and both positive initial checker masses.

Two explicit normalized counterkernels are also constructed and proved not PD:

1. A known single boot state selects one of two hidden checkers under one common receipt
2. The same physical universal updates suppress their branch receipt

These are positive Lean counterexample theorems. No failed proof or finite enumeration is substituted for the generic PD theorem. The concrete finite cardinalities 18 source states, 50 lifted states and five receipts are checked as well.

## Limits and ancestry

This package contains no formal ATM language, source normalization/clock theorem, global honest-computation invariant, first-false-claim probability argument, policy extraction, full path-law correspondence, or EXPTIME reduction theorem. The ordinary accepted reduction remains the source for those claims. The source includes typed finite machine data, not an external file parser, validated binary model builder, production solver or formal bit-cost analysis. No universal host-language refinement is asserted.

The private checker is classical: CDHR2007 supplies its direct ancestry and CDH2010 supplies the bounded-horizon randomization background. SOURCE_PROVENANCE.json links those sources and the exact separately reviewed ordinary proof. No historical novelty is claimed. Formalizing the local construction does not promote the whole ordinary complexity result to Lean credit.

## Fresh replay

Run:

    python -B replay.py --environment /path/to/recovery/environment --output /new/absent/output

The output must be absent and outside this candidate. The script checks payload census/hashes, the pinned Lean binary and version, Mathlib and official package revisions and tracked cleanliness, official import paths, absence of custom import shadows, and source admissions. It compiles all six custom modules into that new directory and validates all 24 declared axiom readbacks. The allowed footprints are subsets of propext, Classical.choice and Quot.sound.

Pinned Lean 4.19.0 and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b are used. Installed official dependency objects remain trusted and are not rebuilt from all upstream source. No custom .olean or interpreter cache is distributed or reused. The source root contains 656 Lean lines; this is a coverage description, not a count of independent discoveries.
