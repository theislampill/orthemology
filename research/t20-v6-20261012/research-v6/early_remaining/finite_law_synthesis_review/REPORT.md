# Independent review of synthesis §4.2

**Accepted after two bounded precision repairs.** The reviewed synthesis is SHA-256 `9988b9d4328cc8386b62ace2a2bcad5b019c59c93012aed0cc58d72ef44b9a6f`, lines 124–134. This review concerns that paragraph sequence only. It does not supersede the previous whole-synthesis review or certify later edits.

The four exact controlling original bodies were independently read in full, 454 lines, reusing root's earlier whole-body examination as prior provenance rather than as a substitute for this challenge:

- Static reduction `cf5c163cdc2d79443740c6bf892c2132d6b3746817700dab65f27b88d77974e7`, 1–110.
- Regenerative reduction `623904df068e2695284b2e54b65f8cdce4dc0b0627f656fd70e2318c62081da0`, 1–119.
- Stopped-transcript reduction `57acfff3020ad894e6d6975f3dd81a4d61d57a8f1f55ea886539692617737607`, 1–155.
- Independent historical review `465c603b11348ce2e142f4753c886f164eb4773c322be834f8950db123d10bd9`, 1–70.

## 1. Tensor interpolation and the quantifiers

For a nonempty finite catalogue of m distinct laws on one finite alphabet, the source's pairwise separating coordinate statistic ell_ij has expectations one at law i and zero at law j. Putting the m−1 factors on distinct independent observation positions makes the expectation of their product factor. Under any other catalogue law k, its j=k factor has zero mean. Summing these product statistics therefore realizes arbitrary prescribed catalogue expectation values. The resulting tensor-power law vectors are indeed linearly independent: these statistics provide a dual separating system. One observation is used and ignored when m=1; the needed statistic is then constant. No independence between different summed product statistics is needed, and all may reuse the same positions.

The synthesis's degree/sample-count claim is therefore correct. Its Bernoulli example is also correct: a one-bit statistic has affine expectation, which cannot take (1,0,1) at the three equally spaced parameters. Two-bit expectation has degree at most two and the supplied product construction interpolates those values. This is existence of a bounded statistic on a finite sample alphabet, not a deterministic identification of the hidden catalogue member from that sample.

No uniform bound on its size or error-control sample budget follows across catalogues. Separating probability differences can approach zero, causing coefficients and the statistic bound B to diverge. Consequently the synthetic gap delta=1/(2B) can vanish along catalogue sequences. The synthesis preserves this limit and does not challenge an unrestricted finite-summary impossibility by using a fixed known finite catalogue.

## 2. Hidden correctness and static sufficiency

The initial wording could have been read as imposing constancy of the raw target-goodness predicate on each observation-law class. That is stronger than the source requires. The repaired text correctly defines the **synthetic** high/low label on the whole class: the stable class is high only if every member makes the support good. If raw goodness differs across an indistinguishable class, its label is low. A low arm may still be physically harmless in the actual model; only the implication high ⇒ all internal physical actions good is needed.

The synthetic reward is computed from known tables and received observations; no hidden target label enters the policy. Its range has width at most one after scaling, mean zero for high classes and minus delta for low ones, with a high arm in each actual model. Conditional fresh sampling gives the adaptive arm law using disjoint physical samples. The classical bounded-regret application supplies the static sufficient policy, not the necessity or pruning iff. The cited-policy normalization and strict-gap qualifications remain inherited assessments of the cited source. No external primary paper was newly read in this review.

## 3. Regenerative navigation and switching

The repaired paragraph explicitly states finite observed state and common support. These are important: action-retaining complete return cycles recover each used row by positive prefix conditioning and eventual completion. State-only words may recover only the averaged kernel. The finite irreducible component and anchor-start assumptions supply almost-sure finite complete cycles, while common support makes the identifying prefixes available under both models.

The bottom strongly connected region is essential to lawful navigation among all chosen anchors; an arbitrary winning region need not permit returning from irreversible branches. The sticky cumulative-count rule is a separate proved construction. Fixed ordinal sample-count deviation events pay for cyclic advances and low-arm continuations. Uniform conditional expected duration at the start of each navigation or low macro then pays physical cost. The synthesis correctly avoids reward-duration independence and does not equate bounded low-arm regret with bounded switching cost.

## 4. Censoring, hazard and licence

The stopped experiment distinguishes EXIT from NO-EXIT even at equal terminal lengths. Row recovery from a stopped transcript is asserted only at zero exit probability. Positive-exit arms can be high and physically costly. The physical stage agrees with an uncensored comparison only up to its first actual exit; survival-conditioned rewards need not have the original iid arm law. Stable low physical pulls are a pathwise prefix subset of virtual low pulls, while the expected number of begun positive-exit attempts is separately bounded by the reciprocal minimum positive macro hazard.

At every exit, the certificate supplies every live nonempty strict successor and the controller switches before its next action. This preserves even nonmonotone menus. The randomized version uses unused independent support-indexed seed streams; strict descent prevents prior inspection at entry. The source's deterministic sticky alternative supplies the claimed alternative without demanding rich private randomness. The synthesis correctly treats these as contractual premises, not cosmetic implementation choices.

## Verdict and evidence ceiling

No remaining material source-scope overclaim was found in the accepted §4.2. The connection is useful and mathematically faithful: repeated-product interpolation, synthetic reward design, sticky regenerative control and censored-stage hazard accounting form an inherited sufficient-direction chain. These are not new v6 discoveries, sharp-runtime results, a full iff, observable final-correctness certificates, or evidence authenticating an external source.

This was an independent ordinary mathematical/source interpretation review. No supplied checker, compiler or solver was run. Historical source reviews retain their original assurance scopes. The missing historical common-support note is handled in the independently read review by an explicit common-support restriction of its recovered support-changing theorem; it is not falsely represented as recovered exact original bytes.
