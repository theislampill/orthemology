# Independent scientific-interface review

9 October 2026 UTC. Bounded review of the provenance/likelihood transport report. Outcome: **no blocking mathematical or source-interface finding in the reviewed snapshot**. This is not protected integration, owner adoption, programme closure, empirical validation, or proof-assistant certification. T20 remains active.

## 1. Frozen author snapshot

Author directory: `provenance-learning-transport-20261009/`.

- `RESULT.md`: SHA-256 `7b4d4bd3efe0e2588a1e8751a99fcbc197ca4aa9733f98ec6b7ad452203c93e2`.
- `verify_models.py`: SHA-256 `cccf954e15c29f135a68f67743d386e6a1579b9cc7fe4294eafd71a8400f2a09`.
- `MANIFEST.json`: SHA-256 `9809a5baef8cfde850a9e596ac759f886177ba22028cf3e29e875d1d61c4d0dd`.

I read the report and author control code, replayed the full author controls, independently examined the mathematical claims, checked the relevant source passages, and wrote separate exact controls. No author file was modified.

## 2. Mathematical findings

### Idempotent-source / group-target obstruction

Proposition 1 is correct. A semilattice element satisfies E∪E=E, so every homomorphism into a group has f(E)=f(E)^2 and therefore f(E)=1. No unit-preservation assumption is needed. Positive likelihoods modulo a common positive scalar do form an abelian group. A nonconstant likelihood is a nonidentity element. The full-support prior permits cancellation when translating the group statement to posterior updates.

The positivity and support qualifications matter. Indicator likelihoods can define idempotent hard constraints but are outside the group; zero products may have no normalized posterior. Likewise, a likelihood nonconstant on the whole hypothesis set can act trivially on a prior supported only where it is constant. The report requires strictly positive prior and likelihoods and therefore does not make either overclaim.

### Signed overlap correction

The root-set identity W(E∪F)=W(E)W(F)/W(E∩F) is valid componentwise and in the positive projective group. The posterior formula q_{E∪F}=N(q_E q_F/q_{E∩F}) is also correct: exactly one common prior and one factor for each shared root remain after cancellation. In the disjoint case the denominator is the prior, not the constant vector. The two-posterior collision example correctly proves that overlap cannot in general be recovered from the posterior pair alone.

### Exact continuation quotient

Theorem 2 is valid for the stated full Boolean store domain, with all named activations alone, all named deactivations alone, and their union. The sufficient statistic is precisely informative-root membership E∩I. Constant likelihood factors never affect an output and remain irrelevant under the named operations. Differing nonconstant memberships are distinguishable by the report's prescribed common continuation. Thus there are exactly 2^{|I|} behavioral equivalence classes, not necessarily 2^k when some roots are constant.

The report properly ties the lower bound to the declared operation alphabet and state domain. Changing reachability, admissible commands, the target readout, or root semantics can change the quotient. This is an exact deterministic-state distinguishability result; it is not automatically a RAM-layout, real-coordinate dimension, or physical-memory claim.

### A nonblocking strengthening: depth one already suffices

The supplied proof is correct but stronger witness control is available. Suppose E and F differ at informative root i.

- If q_E≠q_F, the empty continuation distinguishes them.
- Otherwise write q_E=q_F=q, with q strictly positive. Suppose i∈E and i∉F. Under activation A_i, the first posterior stays q and the second becomes N(qL_i). These differ because L_i is nonconstant.
- Under withdrawal D_i, the first becomes N(q/L_i) and the second stays q. These also differ.

Therefore either restricted alphabet distinguishes every inequivalent pair in at most one operation. The current output together with all its one-step activation outputs already induces the full continuation quotient; the analogous withdrawal readout does too. This is a simplification and bounded sharpening of the reviewed result, not a necessary correction or a new research campaign.

### Posterior injectivity versus numerical dimension

The report's injectivity criterion is correct. Posterior-only state works exactly when equal posterior values force equal informative-root memberships. When k roots share one nonconstant vector, k+1 posterior values coexist with 2^k continuation classes. Conversely, binary-place exponents in one log-odds direction make all subset sums distinct, so rank one can encode every finite store state injectively. The report explicitly distinguishes this likelihood-vector span from Deep AU's provenance-root-signature space and does not identify either with probabilistic independence.

## 3. Scientific and epistemic interface

The finite positive vectors admit the stated Bernoulli realization: each vector can be rescaled into (0,1), and conditional independence makes the likelihood of all selected positive outcomes a product. This proves consistency of the stipulated model, not actual source reliability, identity authentication, or calibrated likelihoods.

The selection/history qualification is essential and adequately stated. Even a neutral root observation can yield an informative posterior when selection into the accepted set is state-dependent through another signal. Likewise, administrative withdrawal of a factor changes the stipulated store's output; it does not erase an observed historical event or itself authorize Bayesian deconditioning. The report does not infer knowledge loss, lack of warrant, psychological forgetting, or revoked truth from its deletion command.

The source-credit check is appropriately bounded:

- Deep AX and AR already own joint Bayes, conditional factorization, exact-copy invariance, and the separate source/world and warrant gates.
- Deep AU treats a declared linear root-signature space, not arbitrary nonlinear epistemic capacity.
- The typed-core document explicitly downgrades its Core B claims to `DERIVED_BUT_UNVERIFIED`; this report preserves that status rather than borrowing settled authority.
- The MOAT source's idempotent constraint intersection is not identified with positive likelihood multiplication.
- The CP04/CP12 basing sources warn against manufacturing operative mental grounds from arbitrary numeric or gateable variables. The accepted-evidence store does not claim such a mapping.

This was a targeted comparison with the cited passages, not an exhaustive audit of repository history or a field-wide priority review. The report's no-general-novelty ceiling is appropriate.

## 4. Fresh verification

The full author command exited 0. Its JSON output matches `CONTROL_RESULTS.json` exactly, including 5,460 overlap pairs and 21 finite-state partition refinements. The author's partition refinement is a legitimate independent computation relative to its stated membership formula; finite checks do not establish the universal theorem.

Separate reviewer controls used paired-transition-system breadth-first search, not the author's refinement algorithm. They passed:

- 1,164 paired-store comparisons across activation-only, withdrawal-only, and mixed alphabets;
- 833 overlap formulas with nonuniform priors and up to four hypotheses;
- exact inverse-factor cancellations, repeated likelihood vectors, constant roots, a singleton hypothesis, and an empty root catalogue;
- the rank-one injective example, prior double-counting, the full-support limitation, dependent copies, informative selection, and the distinction between administrative removal and unchanged historical evidence.

The seven source files match their recorded Git-framed SHA-1 blob identities. All twelve author-manifest entries match their byte counts and SHA-256 hashes. The same author report, script, and manifest digests were checked after the review.

Artifacts are `AUTHOR_REPLAY.json`, `independent_controls.py`, and `INDEPENDENT_RESULTS.json` in this review directory. General claims rest on the written proofs reviewed above; these are exact finite controls, not formal-kernel or empirical certification.
