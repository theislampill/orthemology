# Independent review of the fixed channel classification

10 October 2026 UTC. Ordinary independent AI proof review of a frozen author packet. This is a mathematical review with small exact controls, not a formal audit-assess run, proof-assistant certificate, external validation, field-novelty assessment, integration decision, or T20 closure.

## Result

**No blocking mathematical defect found.** The four equivalent conditions in Theorem 1 are correct under the stated finite, nonnegative, normalized, passive-channel hypotheses and the nonempty closed convex law-class assumption. The extreme-point proof correctly removes any physical repeatability premise. The minimal stable hull, strictly positive surjectivity consequence, and diagonal observable-algebra crosswalk also follow as stated.

The source keeps the essential distinctions intact: a complete experiment feasible at one prior is weaker than global preservation; structural closed-convex closure is different from finite posterior reachability; distinct observation-law columns are different from state revelation by a receipt; ideal word probabilities are different from a realized observation sequence. No substantive correction to the frozen result is requested.

The inspected author controls reproduce their recorded outputs exactly. Seven separately written exact control groups pass. All seven files in the source packet and all eight bound inherited input files have identical before/after hashes. No original file was edited.

## Frozen target and evidence

Reviewed target: `../repeatable-channel-constraints-20261010/RESULT.md`.

SHA-256: `8542fbf86cc2914790bfd0fdcd22920bae8fee9569927524df4e2af3ec527336`.

The complete target, its complete `verify.py`, `INPUT_BINDINGS.json`, `SOURCES.json`, `MANIFEST.json`, and recorded controls were inspected. The manifest's six listed file hashes and sizes match. The source packet also contains the manifest itself, making seven preserved packet files.

Inherited content was read selectively for this review:

- `constrained-learning-possibility-20261010/RESULT.md`: the opening contract, finite splitting, fixed-prior extreme-point corollary and surrounding interpretation, with adjacent face and adaptive-tree statements inspected. This confirms the ancestry of the Bayes-plausibility/extreme-prior step, without requiring a new proof of that whole packet.
- `tensor-moment-continuation-20261009/H_CONTINUATION_SOURCE.md`: complete finite instrument setup, Theorem 2 and its proof, plus relevant contract passages. This is the substantive source check for the observable-span crosswalk.
- `bayes-feasibility-compatibility-20261010/RESULT.md`: Sections 1–2 and selected affine-family/fixed-channel/current-prior passages. The older universal-likelihood and affine-equality scope is distinct from the present arbitrary closed convex fixed-channel result.
- `stochastic-exact-inquiry-20261010/RESULT.md`: opening inheritance, fixed-target-label contract, finite stopping distinction, theorem and first discriminator. This confirms that the present packet does not replace the inherited exact-stopping contract.
- `stochastic-inquiry-quotient-transport-20261010/ADDENDUM.md`: opening contract and selected posterior-versus-predictive/stopping passages, not a full independent rereview.
- `posterior-inquiry-value-20261010/RESULT.md`: counterexample, exact compatibility criterion and interpretation. The fixed-channel classifier does not claim to preserve expected inquiry value from posterior answers alone.
- `warranted-learning-20261009/RESULT.md`: Sections 6–8, including the barycenter, conditional factorization and duplicate-receipt distinction.
- `measure-bayes-face-transport-20261010/RESULT.md`: opening result and definitions, to confirm that the infinite-space/topology problem has separate quantifiers.

All eight inherited byte bindings were checked. This review does not revalidate every theorem in those inputs. The external bibliography's descriptions were read as source claims, but external sites and publication-priority assertions were not independently researched. The main theorem and crosswalk have complete local arguments, so that limitation does not leave a dependency gap in this proof review.

## Main theorem proof review

### Contract and zero branches

Source lines 19–44 fix a finite target that the observation does not change. Each column is a probability vector. Stability means every posterior that has a positive denominator, for every prior in C, remains in C. It does not assign a posterior to an impossible outcome. Equal-column blocks use the entire channel, including outcomes that may be impossible at particular priors.

The hypotheses handle n=1, a single outcome, identical columns, omitted block intersections, lower-dimensional C, supported states with zero prior mass elsewhere, and globally impossible outcome rows. Nonemptiness prevents an empty classification convention from entering the proof.

### Bayes plausibility and extreme points

Source lines 48–52 and 66–70 are valid. Column normalization gives a finite positive-weight barycentric representation of p by the defined posteriors. If p is extreme and there are at least two distinct posterior terms, any one unequal term can be grouped against the normalized mixture of the others, contradicting extremality. The sole-positive-outcome case is handled separately by the same identity.

For a supported coordinate i and a live branch, cancellation of p_i gives K(y|i)=alpha_y(p). For a zero-alpha branch, every summand p_i K(y|i) is nonnegative, so every supported state's likelihood is zero. Consequently every supported column agrees at every outcome. This last zero-branch step is necessary for the nonnegative extension and is present in the proof. No repeated experiment, limiting posterior, or access to reciprocal likelihoods enters this implication.

### Compact convex generation

Source lines 54–62 give a complete finite-dimensional argument for ordinary convex-hull generation, rather than merely its closure. The nearest-point inequality follows by differentiating squared distance along a segment in Q. Because x belongs to Q, the nearest-point distance is at most the distance to x, giving the displayed bound on a_r−x. A convergent subsequence of unit separating directions has nonzero limit in the direction space of aff(Q).

The limiting supporting hyperplane contains x. Its equality face is proper: a nonzero direction in the affine direction space cannot be orthogonal to all of that space. The equality face therefore has smaller affine dimension. An extreme point of that face is extreme in Q because any Q-segment through it lies entirely in the equality face. At a relative interior point, a nondegenerate line has two distinct boundary endpoints by compactness and the local interior property. The induction produces a finite convex combination in each case. Compactness of C follows from its closedness in the finite simplex. No omitted infinite-dimensional theorem or unproved extreme-point existence assumption is needed.

### The remaining implications and exact parametrization

Source lines 72–82 are valid:

1. Extreme-point generation places C inside the hull of the block-face intersections; convexity provides the reverse inclusion.
2. Restricting a finite mixture to one block removes all other block terms. Renormalizing gives p conditioned on that block as a convex combination within C_j.
3. Every defined posterior is a convex combination of the unchanged within-block conditional laws, with masses proportional to w_j kappa_j(y). Zero weights can be omitted without defining any zero-denominator posterior.
4. For arbitrary nonempty closed convex families chosen in disjoint block faces, the finite mixture map from their compact product and a weight simplex has compact image. Convexity follows by regrouping same-block terms. If a resulting mixture is supported in one selected block, every positive-weight component must be in that block, so the intersection is exactly the chosen family. Unselected blocks have empty intersections.

Thus the claimed classification is exact. The within-block constraint can be curved or given by inequalities; it need not be a polytope or affine-equality slice.

## Consequences and hypothesis boundaries

### Smallest stable closed convex hull

Source lines 100–106 correctly identify H_K(p)=conv{p conditioned on I_j : p(I_j)>0}. The block conditionals have disjoint nonempty supports, so they are affinely independent and their convex weights are the block masses. The hull is compact, contains p and is stable by the same reweighting formula. Any competing nonempty closed convex stable family containing p contains all its block conditionals by Theorem 1 and hence contains this hull.

This is minimality among the specified families. It does not say every point in the hull is a finite update from p. The source explicitly retains that restriction.

### Positive outcomes are onto

Source lines 108–112 follow from the classification. For a target law q in C, write q=sum_j v_j q^j. For a positive outcome with block factors c_j, put

    w_j = (v_j/c_j) / sum_k(v_k/c_k).

Then p=sum_j w_j q^j belongs to C and B_y(p)=q. This proves surjectivity without treating an inverse likelihood as an available signal. The same argument works for any positive block-constant likelihood. For a nonnegative outcome the inverse can be unavailable and blocks can disappear; the source appropriately makes no general surjectivity assertion there.

### Guards against stronger interpretations

The paper's closedness, convexity and complete-normalized-channel discriminators are correct. In particular, stability for a single favorable likelihood is insufficient: feasibility of all branches is what makes the barycenter argument available.

The disk control is exact: squared radius 1/18 lies below squared distance 1/6 to the simplex boundary; both first posteriors are on the disk boundary; the repeated + posterior has squared distance 1/6. A single current-prior feasible experiment therefore cannot be rejected merely because its channel fails the stronger global test. Algebraically applying a second Bayes map witnesses a failure at another prior in D; an actual second observation would additionally need the fresh conditional channel.

The copy control uses conditional likelihood 1 after the first receipt and so leaves the posterior unchanged. The resetting instrument concerns a successor target and therefore lies outside the passive fixed-target theorem. Both boundaries agree with the inherited source.

For the positive binary example, every finite word leaves every previously supported state positive. At equal initial odds, the odds after a word are 3^d for an integer d. The law (2/5,3/5) has odds 2/3, which is not an integer power of 3, so even a full-support interior law can fail to be exactly reachable. This supports the source's careful separation of the structural hull, finite reachability, and finite zero-error identification. It supplies no Blackwell equivalence to perfect disclosure.

The optional repeated-word argument is also sound under strict positivity. Rounded empirical outcome frequencies converge to the selected block column; the log-likelihood-ratio limit is a strictly negative KL divergence for every different column. Finite global algebraic stability and closedness then give the selected block conditional. It is genuinely optional and unnecessary for the nonnegative main proof. Its products represent actual repeated observations only with the stated fresh conditional-independence interpretation.

## Observable algebra and the law observation distinction

Source lines 180–192 specialize the inherited theorem correctly. With no additional terminal readouts and D_y=diag(K(y|·)), the starting space is span{1}. The inherited products D_w 1 are exactly pointwise products of likelihood rows. Their span is a unital algebra because multiplication concatenates words. All its functions are constant on equal-column blocks.

The displayed interpolation polynomial is valid even when no single likelihood row distinguishes every block. For each competing block k, its selected factor vanishes on I_k and equals one on I_j. All denominators are nonzero by their selection rule. Thus the polynomial is exactly the indicator of I_j. The one-block empty-product case is correct. The algebra is therefore exactly the block-constant function space, of dimension m.

The correspondence is with the inherited least invariant observable space, not with a general set of feasible inquiries or a promise of physical repetition. Extra terminal readouts in the inherited contract could distinguish states within a channel block; this specialization explicitly starts with the constant readout alone.

An exact useful clarification, already compatible with the source, is that the displayed indicators have degree at most m−1. Ideal word probabilities through that horizon suffice to recover the block masses. This is a statement about known probability-law data. It is not a finite-sample or receipt-based zero-error reconstruction claim and need not be added to the original packet.

A separate review control makes the distinction concrete. Take binary likelihood rows (1/4,1/2,3/4) and (3/4,1/2,1/4), whose three columns are distinct. The different full-support priors

    p=(1/4,1/2,1/4),        q=(3/8,1/4,3/8)

have the same one-shot outcome law (1/2,1/2), while their ideal ++ probabilities are 9/32 and 19/64. Thus even knowing the complete one-shot outcome law does not necessarily recover the prior, despite column separation and the coordinate-face classification. Formal repeated-law observables add information; an individual finite positive history still retains all prior-supported states. This is a reinforcing control, not a defect in the source wording.

## Executed exact controls

`verify_review.py` reads the author module by compiling and executing its definitions under a non-main name. It calls the nine inspected control functions and their binding check. It deliberately does not call the author main function, which would rewrite the frozen `CHECK_RESULTS.json`. The replayed results equal the recorded results exactly.

Seven independently implemented groups use only exact rational arithmetic:

1. Twenty-seven three-state nonnegative binary channels with an appended impossible outcome, each tested on all seven nonempty uniform supports: 189 barycenter and singleton-fixed-law/equal-column checks. The one-state edge case is checked separately.
2. Fifteen positive block-reweighting and explicit inverse checks on a two-block stable hull, including endpoint laws and a likelihood that is not one of the channel's rows.
3. A nonnegative branch whose image is a proper subfamily and which is undefined at the other block endpoint.
4. A four-block, three-outcome example with no individually separating outcome row and a duplicated target column: exact interpolation, 40 word observables through length three, and ranks 1,3,4,4. Distinct within-block conditionals have the same word laws.
5. The displayed full-support one-shot-law collision with different two-step laws.
6. All 63 binary words through length five for support preservation and the exact odds lattice. The all-finite-length claim is established by the direct product argument, not by this bounded test.
7. Separate disk and copied-versus-fresh arithmetic.

Run from this review directory with `python3 verify_review.py`. `CHECK_RESULTS.json` and `verification.txt` record the successful run. `INPUT_HASHES.json` binds all 15 preserved source/input files and records before/after equality. These calculations corroborate the review; the universal conclusion rests on the inspected and reconstructed proof.

## Disposition

The frozen theorem and specified consequences pass this ordinary independent AI review, with no required mathematical revisions. Retain the source's global-versus-local quantifier, defined-branch restriction, passive fixed-target premise, and law-versus-realized-observation distinction whenever the result is reused. This disposition grants no protected-change, integration, release, formal audit, external validation, novelty, or programme-closure status.
