# Independent review: countable port signatures

8 October 2026. This review covers the frozen countable-signature-identification core. Earlier finite-signature, noise-aware and Lean reviews remain unchanged. A separately commissioned general finite-mixture moment result is outside this freeze.

## Verdict

The finite base-4 identification theorem, effective decoders, factorization-free polynomial-bit improvement, guarded-query obstruction and carefully qualified infinite-route audit are correct at their declared scopes. The approximation-oracle, limit-learning and particular mixture controls also match their stated mathematical claims. No unresolved mathematical blocker was found in the frozen core.

Two wording issues identified during review have been repaired: the finitude certificate requires every route to affect the compared absence event, and the precision obstruction rules out a uniform tolerance rather than declaring an exact second measurement universally necessary. The gcd decoder includes the needed complete-prime-power selector condition.

## Arithmetic and source verification

The calibration x_i=4^(-2^i) maps a nonempty finite positive support S to the integer e=sum_(i in S)2^i and failure factor f_e=1-4^(-e). The known port alphabet is the natural numbers. What is unknown is the finite active signature; no unknown real-world ontology or naming scheme is recovered from scratch.

Zsigmondy's original specialised order theorem was inspected visually on printed page 283. Its listed exceptions exclude base 4, and its next paragraph explicitly uses that base for arbitrary orders. The retained PDF matches both its recorded SHA-256 and the MD5 on the verified repository record. This is targeted source verification, not a claim to have reread the entire 1892 proof. [Original article and scan](https://zenodo.org/records/2131326).

The relevant source premise is that for every e>=1 there is a prime p with multiplicative order e for base 4. Cases e=1,2 also have the direct witnesses 3 and 5. The modern Cambridge research article independently corroborates the n>2 theorem and the order interpretation. Source locations and hashes are recorded in sources/SOURCE_REVIEW.json.

For two different finite histograms with equal readout, choose their largest differing exponent e. Its primitive prime divides f_e's numerator and none of the smaller numerators or any denominator. Larger count differences are zero. Its valuation contradicts the assumed equality. This proves finite multiplicative independence, not independence for infinite products or arbitrary real coefficients.

The corresponding prime matrix is triangular, not diagonal. An order-e prime also divides the numerator at every multiple of e. The implementation correctly processes candidates downward. The example 255/256 has candidate orders 1,2,4 but only the exponent-4 count is nonzero.

## Decoding and computational scope

Under the finite premise, the reduced denominator is exactly 4^M with M=sum(e n_e). Factoring the numerator and computing prime orders therefore gives a finite candidate superset. Descending valuation elimination, integer nonnegativity and full reconstruction recover the histogram. The factorization-based reference implementation is correct and claims no efficient factorization algorithm.

The newer gcd implementation avoids factorization. Repeatedly stripping each A_e=4^e-1 against earlier generators leaves a nontrivial complete new-prime component K_e. The checks include K_e dividing A_e, coprimality with earlier generators and gcd(K_e,A_e/K_e)=1. After larger generators are removed, maximal composite K_e-power divisibility gives the exact count, followed by removal of the complete A_e power from the original residual.

Early numerator coverage stops at exactly the largest active exponent on valid finite inputs. A full-weight path is also available. The sizes and number of integer operations are polynomial in the explicitly expanded rational input length: M is bounded by that length, generators have O(M) bits, and the history has O(M²) bits. This is not polynomial in a compressed expression, latent histogram description, port index or sample budget, and does not solve arbitrary integer factorization. GCD_DECODER_REVIEW.md gives the independent argument and implementation details.

The independent reviewer also used finite partition enumeration as a distinct small-case decoder. Enumeration proves an effective alternative using the observable denominator bound; it is not given the gcd algorithm's polynomial complexity claim.

## Guards and approximation oracles

A finite list of issued subsets gives each index one finite membership pattern. Two fresh indices outside any finite baseline share a pattern; a route requiring one present and the other absent is disabled throughout that transcript. This works even when profiles are infinite and rates vary. A deterministic adaptive algorithm stopping on the baseline therefore stops identically on the augmented model. The proof applies to the unrestricted class closed under adding such a route.

The author keeps this deterministic finite-stopping claim separate from randomized lower bounds. GUARDED_ORACLE_BOUNDARY.md additionally proves that N exact profile queries cannot uniformly identify an arbitrary guard index among M candidates with average success above 2^N/M. It also explains why a promised one-route family may still admit variable-budget eventual identification. Neither argument applies to arbitrary pooled-profile mixture oracles or direct route inspection.

For a Cauchy-bound oracle under the fixed calibration, a sufficiently rare added high-index route preserves any finite transcript of allowed error centres. Thus a deterministic learner cannot always stop with the exact finite histogram. The centre's rational denominator is not a certified denominator of the true response. Effective least-consistent enumeration nevertheless learns finite models in the limit; fair profile/precision dovetailing similarly separates guarded finite hypotheses. The implemented finite prefixes are controls, not observed certificates of eventual stabilization.

Even a known route count of one does not provide a uniform finite-sample margin across unbounded indices. The response gap at high i shrinks on the scale 4^(-2^i). The exact-rational and polynomial-expanded-input results do not remove that measurement cost.

## Infinite inventories and conditional finitude

The greedy construction gives a computable countable inventory with support codes above E, multiplicities at most four, and real no-effect product exactly f_E. Its finite prefixes have strict explicit error bounds and never equal the target. This verifies why the finite inverse cannot by itself certify actual finitude in the expanded model. Valuations and denominator grades cannot be moved through this real limit.

The second-profile certificate is sound under its extra premises. With no guards, every route affecting the compared event, independent positive success factors and finite support per route, equality q_R0=q_full>0 excludes every route touching outside the decoded finite R0. Positive absence then excludes infinite multiplicity among the finitely many inside support types. The inventory is finite and the original inverse applies.

This conclusion is about the relevant route inventory, not the number of existing beings, merely capable agents or unused ports. Issued-profile restriction can activate a guarded inside route and defeat the inference; mere outside-rate suppression with guards frozen is a different intervention. The reviewed guarded infinite-tail counterexample correctly changes the issued profile.

No uniform positive near-equality tolerance survives unbounded indices. With an already exact first readout, however, a candidate-dependent inside-count bound gives finitely many possible second responses and a positive discrete gap. A sufficiently narrow warranted enclosure may then establish equality; ordinary samples supply only the corresponding confidence statement. No rationality decision for arbitrary real probabilities is claimed. FINITENESS_REVIEW.md records these distinctions.

## Algebraic and process extensions

The monoid embedding does not imply arbitrary real-intensity or mixture identifiability. The exact two-port identity q_A+q_B=q_OR+q_AND makes two distinct resampled-inventory mixtures agree at every one-trial rate/profile response. Holding one latent inventory fixed across two conditionally independent trials gives a second-moment difference xy(1-x)(1-y), verified algebraically and on a separate rational grid. Resampling the inventory between repeats removes that distinction.

This is a repair for that particular pair under an added grouping premise, not a claim that two moments recover arbitrary mixtures. Separate trial episodes are not extra original producers jointly creating one token.

ARITHMETIC_BOUNDARY.md also checks that the primitive-prime condition is sufficient but not individually necessary: the exponent-2 exception at bases a=2^k-1>=3 is handled by a nonsingular two-column valuation block. All integer bases a>=3 remain finitely independent. Base 2 has the genuine relation f_6 f_1=f_2² f_3. These refinements remain distinct from the implemented base-4 theorem and carry no field-wide priority claim.

## Frozen evidence

- Author suites: 15 countable/finite controls, 6 gcd controls and 8 oracle/extension controls, all passing against frozen copies.
- Independent countable suite: 7 control groups; 2,714 distinct weighted finite histograms, 26 partition-decoder reconstructions, primitive-order checks through exponent 24, profile witnesses and greedy bounds through exponent 40.
- Independent LCM-history gcd implementation: 55 additional model checks, including 1,000-fold multiplicity with early stopping at exponent 1.
- Frozen cross-implementation replay: 66 product-history/LCM-history comparisons through support code 256, 25 comparisons also involving the prime-order decoder, and 25 independent second-moment mixture controls.
- Separate exceptional-base block controls: eight bases and sixteen finite coefficient pairs per base.

Counts describe verification coverage. They are not separate discoveries, empirical interventions or replacements for the written general arguments. No new Lean kernel proof of Zsigmondy, the countable theorem or the infinite-product audit is claimed.

The final receipt binds author snapshots, independent controls, reports, logs and primary-source provenance. Calibration, route individuation and aliasing, independence, trial stability, complete compared output and source-admissible intervention remain external obligations. No protected integration, owner acceptance, research closure or retrospective research-time certificate follows.

The exact author freeze is MANIFEST.json SHA-256 43681d0c2d070e30200afb7b3dc557396150bff9c8012e75bd0a72328a27a974. All 33 listed distributable files were independently checked for byte size and SHA-256. The eleven reviewed core files still match the frozen copies. The manifest's excluded modern full-article inspection files are not copied into this review's delivery sources.
