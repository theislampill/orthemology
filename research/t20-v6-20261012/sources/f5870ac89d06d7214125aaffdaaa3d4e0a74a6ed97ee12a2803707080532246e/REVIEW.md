# Independent review: finite polynomial state closure boundary

11 October 2026 UTC. Review disposition: **PASS for the stated ordinary mathematical claims on the exact bound packet.** No mathematical revision is required. This is evidence and a scoped review recommendation, not an integration, release, audit-lifecycle or programme-closure decision.

## Exact object and independence

The author object is `finite-polynomial-state-no-go-20261011/FROZEN_MANIFEST.json`, SHA-256:

`ec678fb09461e8ea32a2826ee736919e3b7e780084fff9d491049f5715343dff`

Its 18 listed payload files were individually length/hash checked and copied into `candidate_snapshot/` before replay. The theorem file is `RESULT.md`, SHA-256 `1e84ad0f475e9051dba08b1c447c73c63657929ebff75d0a6e79546eb96aac74`. The author verifier is SHA-256 `336e93760d27548474b49753404d71d41dbaf14afd87e90d081bd3195f2e596b`. `AUTHOR_BINDING.json` gives the full inventory. Early orientation hashes in `BASELINE.json` are explicitly not acceptance pins; final prose added the relevant leafwise antecedent before freezing.

This reviewer did not author the candidate or companion note, edited neither, and used no reviewer children. The independent controls were written without importing author code. The root-proposed candidate and companion degree note are participating same-session context, not prior independent proof. The subsequent author-verifier replay is distinguished from the separate independent suite.

## Proof review

### Degree and finite-evaluation separation

For nonzero p of degree K and nonconstant F of degree D, the top homogeneous part of B_F p is −F_D p_K. The polynomial ring over the reals has no zero divisors; the drift term has degree at most D+K−2 and cannot cancel that product. Thus the degree is D+K. With K,D at least one, this exceeds max(K,D), so B_F p does not lie in S=span{1,F,phi_1,...,phi_m}. Redundant, constant and zero coordinates do not affect the argument, provided at least one retained coordinate is nonconstant.

The evaluation lemma is valid for a finite-dimensional function space W=S+R g. Evaluations span W*, because a function annihilated by every evaluation is the zero element of W. Expressing the coefficient-of-g functional in an evaluation basis gives a signed finite measure with zero mass and nonzero g integral. Its positive and negative parts have equal strictly positive mass, so their normalization produces two genuine probability laws. The combined support is at most dim(S)+1, hence at most m+3. This is a sufficient upper bound, not a sharpness theorem. Adding the same strictly positive finite-support law preserves the equality constraints and scales the gap, establishing the claimed finite-simplex interior version.

### Normalization and actual trajectories

The atom ODE has local solutions because a polynomial gradient is smooth. A finite union of initial supports permits a common positive existence interval and, after shortening it, a common compact bound on the trajectories. Exponentials of the finite time integrals of F are finite and positive; their weighted sum is positive. Differentiating the actual normalized finite sums therefore gives

    (mu_t p)' = mu_t(B_F p) + mu_t(F) mu_t(p).

The two initial laws agree on F and p as well as every retained coordinate. Their normalization terms cancel exactly. They nevertheless have different B_F p expectations, hence different retained velocities at the same retained state. An arbitrary nonlinear or discontinuous vector field cannot assign both values. No assumption that a nonlinear closure must be linear is used.

There is no hidden requirement of global completeness. For example, F(x)=−x^3/3 gives x'=x^2 and x(t)=u/(1−ut), which escapes at t=1/u for u>0. The independent suite checks this local characteristic and its positive weighting. The theorem needs only the common local interval; the explicit quadratic witness separately has global forward trajectories.

### Time quantifiers

The accepted quantifier order is: for every admissible F and finite descriptor, there exist one pair of finite laws and epsilon>0 such that the pair has the same initial descriptor, both trajectories exist on [0,epsilon), and their retained outputs differ at every t in (0,epsilon). Indeed h(0)=0 and h'(0) is nonzero, so h(t)/t has a nonzero limit. For each such t no decoder from the initial descriptor alone can recover all defined outputs, since it already fails on this pair.

This is not a uniform epsilon over all descriptors or laws, not a claim of global existence for every polynomial, and not a failure assertion for every positive time. It does not use uniqueness of a hypothetical coarse ODE. The candidate's explicit statements preserve these distinctions.

### Explicit witness

For M=D+K, choose v avoiding the zeros of F_D p_K. Even and odd binomial laws on jv are normalized and match every polynomial of total degree below M. Forward differences give the exact normalized derivative gap

    (−1)^(M+1) M! F_D(v) p_K(v) / 2^(M−1).

The sign and coefficient are correct. The integer-grid construction for rational inputs is valid: a nonzero polynomial of coordinatewise degree at most M cannot vanish on the entire (M+1)-point grid in every coordinate. It is an existence/exact-search construction, not an efficiency guarantee or an algorithm for unrepresented arbitrary real coefficients.

For F=x^2/2 and descriptor (x,x^2,x^3), the displayed laws match moments through degree four. Their fifth moments are 340 and 695/2. Their cubic velocities are −605/4 and −155, so the difference is 15/4. Direct differentiation of their actual weighted contracting trajectories, independently of the generator formula, confirms these values. The common-support interior mixture has gap 15/8.

## Boundaries and deduplication

- The no-go applies to the class of all finitely supported initial laws for the specified gradient-and-killing operation. It does not refute a known-support interpolation representation or a fixed-rank atomic chart.
- A concrete independent boundary control uses the rank-two law with equal weights at (5−sqrt(5))/2 and (5+sqrt(5))/2. It has the same displayed three-coordinate descriptor but cubic velocity −275/2, a third value. Its fourth moment is 175/2, whereas both rank-three laws have fourth moment 90. Fitting these three moments to the rank-two chart does not establish the rank promise. The rank-two model remains internally correct because its rank premise selects its own law. The binomial pair each has rank three.
- For F=x^2/2, the stated Gaussian mean and variance formulas follow from completing the square and contraction. Exact differentiation gives a'=−a−av and v'=−2v−v^2. For v_0>0 and t>=0 their denominator is positive. This is a valid invariant-family positive control; it does not cover all finite laws or classify all invariant families.
- Constant F yields a stationary normalized law; all-constant descriptors have zero derivative. Drift-only quadratic dynamics preserve every bounded polynomial degree. These controls show why the hypotheses and killing term matter.
- No conclusion is licensed about arbitrary nonpolynomial summaries, arbitrary law encodings, history/extra-state systems, approximation quality, unrestricted finite-dimensional cognition, source warrant, or empirical prediction.

The targeted antecedent readings distinguish the existing equal-state/different-velocity criterion, finite-product normalized-decoder and leafwise objective obstructions, known-support and rank-restricted positive closures, and the all-orders moment-indeterminacy result. The present increment is the elementary all-finite-law, arbitrary-finite-polynomial-descriptor specialization with actual normalized trajectories and explicit witnesses. The general factorization mechanism and degree argument receive no new independent priority credit.

The reviewer reproduced the author's recorded bounded pattern scan: all 222 recorded file hashes still matched and all 11 matching lines reproduced (`DEDUP_REVIEW.json`). This verifies the recorded scan, not absence from unscanned nested manuscripts or historical literature.

Two primary comparisons were independently opened on 11 October 2026. [Brunton et al. (2016)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0150171), invariant-subspace and continuous-time example sections, supports the classical invariant-observable ancestry and positive polynomial drift cases. No broad topological assertion from it is needed here. [Walker and Byrne (2025)](https://link.springer.com/article/10.1007/s11538-025-01446-w), sections 4.3 and 5.2.1, addresses exact moment closures and degree cancellation for a different discrete growth/flux generator. Neither comparison establishes historical originality. The mathematical proof here is self-contained.

## Executed checks and portable replay

- Isolated author verifier replay: **616 exact controls passed**. Both replay output files are byte-for-byte identical to the retained author outputs.
- Independent `independent_controls.py`: **117 exact controls passed**. These include sparse and mixed multivariate polynomials, repeated/zero/constant descriptor entries, D=K=1, three separate finite-evaluation/Jordan constructions, generator iterates, exact binomial identities, actual normalized trajectory derivatives, common-support rational weights, rank-two and Gaussian positive boundaries, and the local finite-escape example.
- A preliminary independent run detected Python float coercion in a missing-weight default in the review-only mixture builder. Replacing that default by an exact symbolic zero and adding a rational-type assertion resolved it; the full suite was rerun. This was a test-implementation defect, not a mathematical counterexample.

Run `python3 replay.py --output-dir /a/separate/writable/directory` from this review directory. Python 3 and SymPy are required. The replay checks bound payload bytes, runs the copied author verifier and the independent controls, and compares the author results exactly. It writes only into the selected output directory. The nine original source paths are provenance; their copied bytes supply the author verifier's inputs. No live original directory, network, cloud account, toolchain download or other packet is required for portable replay. The optional current-source scan verification is already recorded and is not a replay dependency.

These checks do not turn the ordinary universal proof into a formal-kernel theorem. Hashes identify retained bytes; they do not authenticate original sources. Preservation and any integration remain separately owned.
