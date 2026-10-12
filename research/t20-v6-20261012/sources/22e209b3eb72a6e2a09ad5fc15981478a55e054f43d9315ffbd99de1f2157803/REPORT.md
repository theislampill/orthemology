# Independent review: conditional AS preservation and matching-rival necessity

## Verdict and source identity

**ACCEPT_DERIVED_CONDITIONAL_AS_PARITY_AND_LOCAL_MATCHING_RIVAL_NECESSITY.** Original almost-sure properties are transported by actual restriction, normalization and observable continuation readout. Actual parity tail invariance discharges the stability condition. The local matching-rival even-minimum theorem derives the conditional-AS and conditional-law steps from original-law premises.

Input: AS-preservation candidate v1, master manifest SHA-256 `cd17a13ef361de796b590ab37579d11ae235efbdc75a28750f4e0db9f53bd55d`. The included unchanged author ZIP has SHA-256 `5b59e4a2a1c4c2d455327dd69605faefe5d31d27fc4bf78ba816cc0c8b410e36`. Thirty-two sources are exact copies of continuation candidate `6997015ee7db05f3cbed3c5a0b6e00c35aa71be5dcddb520e0f871a946f9b387`; `ParityTailInvariance.lean` is byte-identical to the frozen adaptive packet. The two new sources are `ConditionalAlmostSure` and `AlmostSureControls`. This reviewer did not author them.

## Semantic audit

The action readout takes the action recorded at history coordinate n+1. Applying the actual continuation readout therefore gives exactly original action n+length(h), for every history path. This is a proved deterministic identity using the existing readout, not a new tail process offered as a premise.

`conditional_ae_of_prefix_imp` starts with an original AS property Before. Restriction preserves this AS statement and places the normalized restricted law on the actual fixed-prefix event. A deterministic caller-proved implication on that prefix transforms Before into After of the continuation. The measurable continuation map then pushes the resulting AS property forward. After's measurability is explicit. The implication is not the probabilistic conclusion in disguise: it is pointwise and can express genuinely different before/after invariants. The independent probe instantiates it with an original property that stays in a pair set only after the fixed prefix, yielding a continuation property that stays there from time zero.

`conditional_ae_tail_property` instead requires a measurable action-path property preserved by finite deletion. `conditional_ae_parity` discharges that requirement with the actual minimum-recurrent-priority parity definition and the independently inspected recurrence-shift proof. Finite transient priorities are irrelevant; recurring priorities, not the minimum over the whole path, determine parity. The model's priority function is a mathematical objective parameter and is not added to the causal policy's observation.

The Markov restart theorem composes this AS transport with the separately proved observable conditional restart law. The resulting process uses the latest observed state, the original policy with the observed prefix right-appended, and the normalized common compatible-seed posterior. Positive prefix mass is retained where this is claimed to be a probability restart.

The matching-rival endpoint first transfers the positive candidate conditional exact-recurrent/no-outside event to the rival through full-row matching on its retained pair set. It separately derives rival conditional AS parity from original rival AS parity. A point in the positive event satisfying the AS parity property then identifies the recurrent set with the retained set and yields an even minimum. Desired conditional-AS statements, equality of restart laws, and fresh latent-tail laws are not assumptions. Old-prefix likelihoods need not agree, but both observed prefixes must be positive.

The generic algebraic restriction/normalization transport is valid even for a null prefix because its normalized restriction is the zero measure; every AS predicate is then vacuous. This is accurately separated from the positive-prefix probability restart theorem. The independent null-prefix probe establishes that even False is AE under that zero continuation law.

## Fresh evidence

* A separate no-reuse build compiled all 35 custom modules and read back all 415 selected declarations. Only propext, Classical.choice and Quot.sound occur.
* Source identity checks establish all 32 inherited continuation copies and the separate parity-shift copy exactly.
* Eight independent printed Lean probes compile with standard axioms. They check genuinely prefix-relative stay transport, null-prefix vacuity, expanded original-AS-to-actual-restart parity, the contradiction consequence that an odd matching rival minimum forces zero conditional recurrent-event mass, and an infinite deterministic lasso whose transient odd symbol is not recurrent and whose eventual even symbol gives parity after every finite deletion.
* The author's original first-value/shifted-first-value Dirac controls also replay with the full source closure. They correctly demonstrate that arbitrary AS predicates cannot be transported unchanged without a stability proof.
* The separate accepted continuation review provides 340,512 independent exact observed-law assertions, including unequal prefix likelihood and source/history/kill adversaries. Those finite controls are not used as a substitute for this AS measure proof.

## Scope limits

This is a local positive-prefix necessity interface, not a complete winning-region theorem. It does not choose a positive observed history, establish a global lawful-menu invariant, derive every candidate/rival prefix-positivity premise, perform recurrent graph extraction, or construct the state/support induction. The generic before/after transport intentionally requires the caller's deterministic implication and measurable after-property; later uses must prove them rather than relabeling them as automatic AS preservation.

Raw latent iid-tail marginal identification remains unclaimed and unnecessary for these observable results. The old bounded posterior and continuation review scopes are not retroactively broadened by this distinct acceptance.

## Portable replay

The review archive includes the unchanged author source ZIP, every independent probe and a self-contained driver. Run `python -B replay.py --environment /path/to/pinned/environment --out /new/absent/output`. It verifies the embedded ZIP digest, extracts its entire source/runner closure, performs a fresh 35-module/415-readback build and recompiles the eight probes. Only pinned official Lean/Mathlib binaries/caches are external. A successful whole-driver receipt is retained.
