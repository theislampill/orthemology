# Independent review: posterior-equivalent stopping and lawful transport

10 October 2026 UTC. **PASS_SCOPED, ordinary mathematics and exact rational controls.** The all-word posterior-equivalence counterexample, its exact-stopping separation, the sure-decision preservation statement, the predictive stopped-law corollary, and the uniform-prefix-domination repair are sound under their explicit history, permission, and target contracts. No blocking defect remains in the accepted snapshot.

Accepted ADDENDUM.md SHA-256:

`ba10cde70c12e6594ee769088415b2743485ca28cf97d2f561271305292f82ee`.

Accepted author MANIFEST.json SHA-256:

`587b8bbdfce227f706404f5430b35b80ab1c78dcff6e5d71cf757ca6cf951171`.

The complete accepted addendum was read, including the subsequently added domination subsection. All six inherited inputs are copied and bound in the separate snapshot. The earlier main theorem review and its source hashes remain unchanged. The author's pending-review status is retained as its historical freeze status; this later review does not rewrite it.

## 1. The counterexample meets the actual stronger interface

This is one fixed four-state instrument with the same action and receipt alphabets, target-label interpretation, inquiry permission, and reporting permission. It does not obtain the separation by changing the likelihood table between initial laws.

The all-word proof is exhaustive by cases:

- Opposite reveal labels in the same word make it impossible under both laws.
- A word with at least one reveal of exactly one label identifies the same single revealing-mode state under both laws. The target posteriors agree, while q gives half the word probability assigned by p.
- Every wait-only word remains feasible and has fair target posterior under both laws. Its probabilities are respectively 2^(-n) and 1/2+2^(-n-1).

Thus equality holds for the established all-finite-word posterior and feasibility contract, not merely the current posterior or a finite sample of words. Nonetheless the wait-only infinite continuation has mass zero under p and mass 1/2 under q. With only one inquiry action, a zero-error policy cannot avoid this obstruction by exploring differently. At any finite wait-only history, both answer labels have positive conditional mass. Randomized finite stopping there would therefore have positive error. Waiting for a reveal attains stopping probability one under p and exactly one half under q.

The different hidden supports are explicit and essential to the exhibited pair. This does not contradict the main theorem's qualitative invariance among positive laws on the same support. It is a failure of the coarser posterior-only equivalence to preserve that support-sensitive temporal objective.

## 2. Sure finite decision still transfers

With common history-based inquiry menus and report permissions, the same exact finite decision tree has the same feasible branches under posterior-only equivalence. Point-mass terminal target posteriors coincide. Finite branching converts pathwise everywhere-termination into a uniform finite depth, so existence of a sure finite exact protocol transfers both ways. The counterexample does not undermine this statement: both laws admit arbitrarily long ambiguous waits and neither has a sure finite protocol.

This distinction is load-bearing. Feasibility preserves which finite branches can occur; it does not determine how much probability remains on an unresolved infinite continuation.

## 3. The positive predictive transport is correctly scoped

For a shared behavioral history policy, every finite observed-history/target mass equals the corresponding open-loop word/target mass times the same policy factors. Those factors include decisions to continue, choose actions, stop, and report. Equality of word probabilities and target numerators therefore gives equality of every finite-horizon stopped-output/true-label law.

The event of finite stopping is the increasing union of stopping-by-n events. The total stopped-error event is likewise the increasing union of its finite-horizon versions. Continuity from below supplies equality of stopping and error probabilities. Matching policy classes, through matched inquiry and terminal permissions, yields the two-way existence result.

This is an elementary corollary of the inherited full predictive history-law contract. It does not establish a new stochastic-process mechanism, an optimal policy, or a theorem for representations that omit lawful policy correspondence. The report correctly treats permissions as an additional obligation; preserving answer laws does not by itself preserve permission to acquire them.

## 4. Uniform prefix domination is a sound weaker repair

Suppose Q(h)≤CP(h) with one finite C independent of the finite history, the same lawful history-policy class, and the stated posterior compatibility. Common policy and continuation factors preserve this inequality. Summing over all nonstopped histories of length n gives Q(tau>n)≤CP(tau>n). If the P tail tends to zero, so does the Q tail. Matching finite stopped-label posteriors transfers zero error. Mutual domination gives the reverse implication as well.

A separate, stronger labelled statement handles two initial laws with the same support for one finite instrument. The finite positive minimum and maximum of q(x)/p(x) bound every word-and-target probability, since it is a nonnegative linear functional of the initial law. These labelled bounds transfer both termination and error events even if numerical target posteriors differ. The revised addendum explicitly distinguishes this corollary from the preceding equal-posterior lemma.

The R/N counterexample has Q(w^n)/P(w^n)=2^(n-1)+1/2, so no uniform bound exists in the failing direction. This is a sufficient transport test, not a characterization of all possible successful representation transports. Exact predictive equality is not claimed necessary.

## 5. Independent controls and author replay

Run `python replay_review.py` in this review directory. The only executable dependency outside the review scripts is the exact bound solver copied into the snapshot. Python standard-library arithmetic is used throughout.

The independently written controls check a family q_alpha=(alpha/2,alpha/2,(1-alpha)/2,(1-alpha)/2), with 64 positive rational alpha values. For every alpha>0 its finite posterior/feasibility signature agrees with the revealing-only law. Exact zero-error almost-sure stopping is accepted precisely at alpha=1. The all-word case proof, not the grid, establishes the general statement.

Executed independent evidence:

- 23,296 word comparisons for the 64-mixture family through length five
- 64 corresponding solver classifications and 4,160 exact survival-prefix checks
- An alpha=0 boundary check showing why positivity of the revealing mass is necessary for language equality
- 9,841 same-support word and target-mass domination checks through length eight, using unequal target priors and bounds 9/4 and 8/3
- 65 exact checks of the displayed unbounded R/N likelihood-ratio formula
- 511 finite-word controls for a fixed potential instrument with state-dependent permission differences; potential predictive equality alone still does not transfer winningness
- 379 prefixes of a nontrivial history-dependent randomized policy in a four-state-to-two-state full predictive quotient, giving identical 12 stopped-time/label entries through horizon six

The permission control retains one potential instrument and changes initial supports over permitted versus forbidden duplicate states. The positive quotient control uses a history-dependent action probability, rather than only replaying a single forced action. Both corroborate the stated interface requirements.

The unchanged author scripts were replayed separately. Their eight-mass audit support map, 9,841 posterior/feasibility word controls, 9,841 labelled domination cases, 30 survival/ratio prefixes, exact three-dimensional closed paired-tensor span, and opposite almost-sure solver answers all pass. The two author result JSON files reproduce byte-for-byte. These are author replay counts, not additional independent cases.

The ordinary proofs carry the unbounded and universal conclusions. Finite controls and exact arithmetic are not kernel proofs or empirical evidence about source reliability.

## 6. Inheritance, value, and boundary

The counterexample directly tests the posterior-only equivalence already established in the audit-continuation work. It changes existence of a zero-error almost-surely terminating policy while leaving every finite conditional answer and finite feasible word unchanged. This is a substantive additional temporal interface boundary, rather than another choice of expected-score vector.

The finite-law transport and bounded-density reasoning are inherited or elementary measure-theoretic consequences. Initial-label tracking, robust permissions, the exact stopping criterion, and the paired-tensor machinery are not awarded new general credit. The root's construction and the author's development are shared work; the present review and independent controls are separately identified.

The original eight-mass audit quotient satisfies the stronger law and permission contract, and its support transitions are checked directly. Nothing here requires retaining a literal full transcript or equating abstract model certification with actual human knowledge, warrant, or authority.

All fifteen frozen files, including the six inherited dependencies, are hash-checked before and after replay. The main packet and main review have not been modified. This scoped review grants no field-novelty judgment, empirical calibration, repository integration, protected-source edit, or T20 closure.
