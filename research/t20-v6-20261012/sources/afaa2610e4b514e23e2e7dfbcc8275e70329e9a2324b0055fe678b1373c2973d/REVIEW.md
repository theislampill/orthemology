# Independent review of finite Bayesian constraint compatibility

10 October 2026 UTC. Bounded mathematical review of the frozen source identified below. This reviewer did not develop or author the reviewed results. The author and root jointly developed the proof ideas, so their verification is not being relabelled as independent review.

## Result

The support-face classification, support-restricted affine kernel and rank criterion, RREF component criterion, preserving-channel corollary, and exact fixed-block KL countermodel withstand independent written-proof inspection and exact controls. No defect was found in those central results under their stated hypotheses.

One small but genuine scope qualification is requested in Section 5: after allowing an arbitrary feasible set C, the sentence about strict convexity ensuring uniqueness should explicitly require C to be convex. The general argmin-set identity is correct for arbitrary C; the affine and fixed-block applications already have convex feasible sets. This qualification does not change the main results.

This is an independent computational and mathematical review within the task. It is not Lean certification, a proof-kernel result, external expert validation, a field-wide novelty assessment, repository integration, or T20 closure.

## Reviewed target and preservation

Reviewed source: `../bayes-feasibility-compatibility-20261010/RESULT.md`.

- SHA-256: `571d64fe9d91c72c84d056b593b79784149f685fd3a0837dbf63db89351e4a6c`
- Bytes: 25,720
- Exact copy: `reviewed_target/RESULT.md`
- Source bindings and source manifest are copied into `reviewed_target/` as well

All five source manifest entries and all seven listed local inputs matched their bound SHA-256 hashes and lengths. The two Git blob identifiers were recomputed from the retained bytes and matched. This checks content addressing against the supplied bindings; it does not independently authenticate a remote repository or establish current remote status.

Before-and-after SHA-256 checks found all 13 original packet/input files unchanged. Only the separate review directory was written. The author verifier writes beside itself, so it was run from an unchanged copy in `author_rerun/`, never against the original directory. Its 10 control groups and generated JSON reproduce byte for byte.

## Claim by claim assessment

### Positive action and support faces

For any positive p and q on exactly the same support, the choice L_i=q_i/p_i on that support gives B_L(p)=q. Off-support coordinates are immaterial. Thus the support strata are exactly the action orbits, including singleton supports. Universal forward preservation gives full invariance because the repertoire includes reciprocal likelihoods.

For an invariant set described by a finite support family, strict convex mixtures have support equal to the union. This proves the union-closure equivalence. Closure of each positive stratum supplies every nonempty subsupport, while a downward-closed family is a finite union of closed faces. The nonempty, closed, convex case consequently has one maximal support and contains exactly its entire face. Both supplied necessity controls are valid. The n=1 case is covered.

The nonnegative-likelihood extension is also correct: defined zeroing updates reach each nonempty subsupport. Positivity of the denominator is indispensable. No value is assigned to an impossible branch, and no invertibility conclusion is borrowed for a singular diagonal.

Finite enumeration checks the combinatorics, not the universal orbit or geometric proof. The proof itself does the latter work.

### Homogenized affine preservation

M=A−b1ᵀ correctly identifies the cone K with the nonnegative homogeneous solutions. If C is nonempty, averaging coordinate witnesses produces a feasible p* that is strictly positive on the actual support S. Translating an arbitrary v in ker(M_S) by a sufficiently large multiple of p*_S makes it nonnegative without leaving the kernel. This proves the essential span(K|S)=ker(M_S) equality.

Consequently forward preservation of the feasible cone implies preservation of the entire support-restricted linear kernel. Conversely a positive diagonal preserving that kernel preserves its nonnegative cone. The annihilator, row-span and stacked-rank tests are equivalent by elementary finite-dimensional linear algebra. Invertibility of a positive diagonal turns the kernel inclusion into equality, and its positive inverse preserves the cone. The conclusion B_L(C)=C is therefore justified for these affine equality families.

The actual-support restriction cannot be removed. For M=(0,1,1), feasible laws form {e1}; every positive likelihood preserves them although (1,2,3) fails the unreduced row-span test. The proof does not assume a full-dimensional family or an interior point of the ambient simplex.

The inequality example correctly refutes a broader forward-inclusion-implies-equality claim. Nonemptiness, positivity, and the affine-equality form remain material hypotheses.

### RREF components and channels

For the nullspace basis vector indexed by free coordinate j, row r of RDv is R_rj(L_j−L_pivot(r)). Each nonzero pivot/free incidence therefore forces exactly one equality. The connected-component condition is necessary and sufficient, with isolated coordinates retained. No further graph theorem is required for the proof.

Changing pivots, redundant row presentations, or the row basis cannot alter the admissible diagonals. Distinct components can receive distinct positive values, which also makes the component partition intrinsic. Independent controls checked all 120 coordinate orders for each of two five-coordinate systems, as well as redundant row changes.

Applying the criterion to every row of a positive stochastic channel proves the factorization through component labels. Stochasticity descends to the component channel. Products of passing likelihoods cancel in within-component odds. The adaptive extension is correct with the stated fixed target and feasible family, passing conditional channels, and absence of an additional state-dependent selection signal. It is not permission to observe and does not imply that every positive weight is available in one fixed channel.

### Current prior and global preservation

At the actual prior, posterior membership is exactly MD_Lp=0 because normalization only multiplies this expression by a positive scalar. This is substantially weaker than family-wide preservation. The supplied positive binary experiment passes at its first prior under both outcomes but its repeated plus outcome leaves C, exactly as claimed.

A useful additional control: for that example, reciprocal L applied at the original prior gives (3/7,3/7,1/7), outside C. Reciprocal L applied at the reached posterior returns the original prior. Thus the inverse group law is not an excuse to promote current-prior preservation to global preservation. The report does not make that mistake.

### Perspective repair and the convexity qualification

The inherited decomposition D_F(r,sp)=D_f(r,p)+D_a(1,s) is used in its stated orientation. Its r-independent radial term yields identical argmin sets on any C where both objectives are defined. The interior second argument and finite continuous boundary-first-argument extension are correctly retained. Neither existence nor a single-valued projection is furnished by equality of argmin sets alone.

Section 5 first broadens to any independently imposed feasible C, then states that strict convexity of the objective on C gives uniqueness. Read literally without a convex-domain convention, this is too broad. For f(q)=||q||²/2, p=(1/2,1/2), and C={(1/4,3/4),(3/4,1/4)}, both feasible points have D_f(q,p)=1/16 despite the ambient objective being strictly convex. C is compact and nonconvex. The same example lies within a Bayes-compatible quadratic perspective extension.

Recommended replacement:

> Compact C with a finite continuous objective gives existence; convex C together with strict convexity of the objective on C gives uniqueness.

If the author uses “strictly convex on C” only when C is itself convex, this makes the existing convention explicit. It still prevents misuse after the preceding arbitrary-C generalization. The countercontrol is retained in `PROJECTION_QUALIFICATION.json`.

The subsequent statement that a unique projection equals the ordinary interior posterior exactly when that posterior belongs to C is sound under the inherited strict-convexity assumptions: the interior posterior is already the unique zero-divergence minimizer on the whole simplex, including the boundary by the inherited boundary argument.

### Fixed block KL update and lost information

The KL decomposition follows by writing q_i=w_a q(i|I_a). It correctly minimizes KL(q||r), with positive r and positive block weights. Conditional KL terms are nonnegative and uniquely minimized by preserving r's within-block conditionals. This proves the displayed Jeffrey marginal-replacement formula, including boundary first arguments through the usual zero convention.

Substitution of B_L(p) gives the displayed block-normalized update U_L. The intermediate within-block denominators cancel under composition; common scaling cancels; and U_1=id and U_(1/L)U_L=id hold on the specified positive fixed-block domain. Likelihoods constant within blocks act identically under U even when the original Bayes update changes block masses.

The declared binary likelihoods are strictly positive and each state column sums to one. Direct joint-distribution scoring independently gives:

- Prior half-Brier risk: 5/16
- Correct expected posterior risk: 17/64
- Constrained expected risk: 5/16
- Foregone information gain and posterior regret: 3/64

The plus-plus posterior is (9/10,1/20,1/20), while repeated U stays at p. All 16 length-four histories also leave the repaired report fixed while conventional Bayes tracks the observation sequence. This confirms erasure from the reported state, not a claim that the observation never occurred or that evidence records have physically disappeared.

Fresh conditional independence is explicitly declared. The multiplication is not illicit repeated counting of one report. The prior expected risk is unchanged by the repaired procedure; the claim is loss of the available gain, not expected deterioration below that prior.

### Jeffrey boundary and normative scope

The countermodel refutes identification of U with ordinary Bayes under the unchanged channel. It does not refute Jeffrey updating. A genuine replacement-evidence interpretation must include the chosen marginal replacement and the retention of the current within-block conditionals. Correct replacement marginals alone do not establish that every possible observation protocol preserves those conditionals. The report's independently justified replacement-contract and observation-model qualifications should be retained.

The separation between prior restrictions, posterior-report restrictions, action constraints, source legitimacy, and normative authority is necessary and is present. A prohibition is not a probability-zero assertion. Nothing reviewed here demonstrates a probability representation of arbitrary noetic hard constraints, revises those constraints, or establishes actual warrant or closure.

## Executable evidence and implementation limits

The original verifier is a small research-control script, not a production guard. Its finite tests and symbolic identities support the examples and help detect mistakes; they do not prove universal real-coefficient theorems. The copied script was inspected before execution. Its outputs match the retained originals exactly.

The new reviewer verifier imports no author implementation and uses Fraction arithmetic with a separately implemented Gaussian elimination and basic-feasible-solution enumerator. Nine groups passed:

1. Support-family enumeration through n=4, including 32,767 nonempty families at n=4
2. 18,090 likelihood instances across exhaustive ordered ternary two-row presentations in n=3 and ternary one-row presentations in n=4
3. 975 additional affine instances covering redundant equations, nonzero affine right sides, forced zeros, singleton laws, full simplex, disconnected components, and n=1
4. 240 coordinate orders and two redundant row-basis changes
5. 81 positive binary channels and four adaptive histories
6. Exact KL stationarity ratios, composition, inverse, scalar neutrality and blockwise likelihood gauges
7. Direct joint-law risk calculation and all 16 length-four erasure histories
8. Current-prior, repeated-update and inverse boundaries
9. Empty-family, zero-mass and strict-forward-inclusion controls

The 18,090 cases are presentation/likelihood instances, not 18,090 distinct feasible sets. Some presentations are redundant or define the same family. The results file reports distinct row spaces and feasible presentation counts explicitly.

The mathematical rank condition applies over the reals. An implemented “exact” decision requires exact representable coefficients or a certified decision method; ordinary floating-point rank thresholds are not the theorem. Actual support also has to be computed correctly. No numerical stability or production software correctness claim is supplied here.

The first reviewer-script attempt had a syntax-only unmatched parenthesis and executed no controls. It was corrected in the review script; the subsequent complete execution exited successfully. No failed mathematical assertion was suppressed or weakened.

## Ancestry and bounded programme contribution

The retained warranted-learning packet restricts its original normalization characterization to the full simplex. The nonseparable packet already supplies the perspective decomposition. The noetic-gradient packet distinguishes radial normalization from tangent correction and auxiliary metric transport. The pinned G1 source remains a proposed feasibility-first candidate, and Deep AX V2 retains joint likelihoods, factorization conditions, duplicate invariance, and separately typed source/world obligations. The retained audit-continuation packet already acknowledges inherited invariant-observable constructions. The current packet's comparisons do not claim those constructions anew.

This review directly inspected the relevant passages and supplies a keyword navigation index over four inherited result packets. That is not an exhaustive repository or field-wide priority search. The bounded programme contribution is the feasibility guard and the fixed-channel countercontrol at this inherited repair interface, subject to a separately justified representation bridge.

For classical ancestry, the publisher abstract and keywords support the existing compositional-perturbation/group-operation framing; the paywalled full text was not reviewed. [Aitchison and Ng 2005](https://journals.sagepub.com/doi/10.1191/1471082X05st091oa)

The publisher-indexed record supports Krogdahl's dependence-graph ancestry. Direct full-page retrieval again failed, so no exact theorem from that article is imported or independently verified. The RREF argument above is self-contained. [Krogdahl 1977](https://www.sciencedirect.com/science/article/pii/0012365X77901182)

Grünwald and Halpern, Sections 5.1–5.2, give Jeffrey's partition-weight update, its relative-entropy interpretation, and the need for an appropriate observation protocol. Those passages were independently read. They support the report's ancestry and boundary claims rather than confer novelty or external validation on this packet. [Updating Probabilities](https://arxiv.org/pdf/cs/0306124)

Csiszár's original article was not read in this review. Its secondary bibliographic ancestry is not promoted to a directly inspected proof source.

## Disposition

Retain the central mathematics with its hypotheses. Make the Section 5 convexity qualification explicit before presenting the arbitrary-feasible-set discussion as a uniqueness guarantee. Preserve the existing Jeffrey, positive-domain, current-prior/global, source-authority, and programme-status boundaries.

The author packet remains unchanged by this reviewer. Any later revised packet has a different review target and needs a delta check. This review has no release, repository mutation, closure, or authority-changing effect.
