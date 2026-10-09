# Independent review of adaptive second-face replay

8 October 2026 UTC. This is a fresh review of the separate adaptive-two-face-corollary successor. The reviewer did not propose or author its identity, theorem, or screening counterexample. The reviewer independently derived the identity and checked the observation contract, randomization, boundaries, supremum, sequential transport, and cost counterexample. Only this new review sibling was written; the frozen predecessor and seventh checkpoint were not changed.

## Disposition and scope

The mathematical claims pass within their stated scope. Final applicability is bound to the author payload hashes in REVIEW_RECEIPT.json. No adaptive KL optimum, complete characterization of adaptive optimizers, longer replay word, physical implementation, sharp testing constant, protected integration, or T20 closure is certified.

One nonblocking precision edit was requested and resolved: explicitly include the first command in the recorded transcript when claiming that randomized first-command divergences average exactly. The final RESULT.md now does so. The mathematical upper bounds also hold if that command is hidden, by data processing; equality need not. The final receipt records the resolution and reviewed bytes.

## Exact deterministic identity

Fix an interior first rate a and write A=(1-a)^n. For a fixed second rate b, let B=(1-b)^n and let Delta be the difference between the alternative and reference (X,Y)=(1,1) mass. Equal margins force the four mass differences to be (Delta,-Delta,-Delta,Delta). Reference independence gives the reference conditional Y law Bernoulli(B) in each first-bit branch. Hence

    A chi²(P1(Y|X=1,b) || P0(Y|X=1,b))
      = Delta²/[A B(1-B)]
      = (1-A) d_chi(a,b),

    (1-A) chi²(P1(Y|X=0,b) || P0(Y|X=0,b))
      = Delta²/[(1-A) B(1-B)]
      = A d_chi(a,b).

The weights on the fixed-pair divergences are therefore 1-A on the X=1 selected rate and A on the X=0 selected rate. They are not the corresponding branch probabilities. This reversal is correct because each conditional covariance deviation contains the inverse branch probability. The exact rational control detects the tempting swapped-weight error: the actual divergence is 53/9600, whereas the incorrectly swapped expression is 1/300.

The first bit has the same law in both worlds, so chi-squared divergence of the complete two-branch experiment is the sum of these branch contributions. This proves the asserted weighted-average identity. Its derivation uses the actual retained-threshold conditional experiment: choosing b after X does not redraw or recouple the latent vector. It would be invalid to infer the conditional law merely from separate contextwise marginal tables without that observation contract.

## Randomization, aborts, and first-rate choice

At a fixed available history, the branch kernel mu_x must be the same in both worlds and may use no latent information beyond that history and X. The transcript law on the selected rate and possible second observation then has the common measure factor mu_x(db). That factor cancels from the likelihood ratio, and integration gives the stated formula for discrete, continuous, or mixed kernels. No density of mu_x with respect to Lebesgue measure is assumed. Since the relevant integrands are nonnegative, the integration is justified by ordinary nonnegative integration even before applying the uniform finite bound.

An abort leaves a deterministic continuation at the observed branch and selected abort action. Its likelihood ratio is one and its contribution is zero. Treating abort as an additional action with d_chi(a,abort)=0 puts both branch kernels on probability spaces and preserves the convex bound. An outcome-dependent abort probability itself adds no information beyond the observed X, because the conditional policy is common.

A randomized first rate, when recorded, has a common distribution before the fresh vector is sampled. Its conditional chi-squared divergences average, again because its likelihood factor cancels. An unrecorded first rate or unrecorded second action can only reduce chi-squared and KL. The independent rational randomized-abort control verifies strict loss from hiding the second rate: the labeled divergence is 263/72000, while the coarsened divergence is 2384573/766443600. Therefore it is appropriate that the author limits exact equality to the enlarged recorded transcript and invokes data processing when labels are hidden.

## Literal boundaries and supremum

At a=0 or a=1, the first bit is deterministic and identical in both worlds. On its realized branch, every selected second-face marginal is also identical, so the complete attempt has zero divergence. The impossible first branch is removed rather than assigned a conditional law. For interior a, a selected second rate b=0 or b=1 produces an identical deterministic second bit and contributes zero. No 0/0 formula is evaluated. These statements concern literal boundary commands and do not assume continuity of chi-squared under limiting commands.

The adaptive chi-squared value is bounded above by sup_b d_chi(a,b), and then by the global fixed-pair supremum. Conversely the adaptive class contains every fixed pair, by choosing the same b in both branches. Therefore the two global suprema are equal for every n. This inclusion argument does not assume a finite-n maximizer exists and remains valid despite possible boundary discontinuities. The predecessor's global chi-squared asymptotic and its attaining nonadaptive rate sequence consequently transfer. No additional uniform-asymptotic argument is needed for that specific transfer.

There is no corresponding exact KL identity asserted. For KL, write the two weighted conditional divergences as A D_1(b) and (1-A) D_0(b). Each is nonnegative and is at most the full fixed-pair KL at the same b. Thus arbitrary two-branch selection yields at most twice the fixed-pair KL supremum. This general factor-two argument is valid and independently corroborated. For this reference law, the chi-squared identity and KL<=chi-squared instead give the stronger uniform 32768/n^4 KL bound. They do not by themselves prove equality of adaptive and nonadaptive KL suprema or transfer the predecessor's half-chi-squared optimal KL constant.

## Sequential cost and stopping

Every attempt starts with a fresh latent vector conditionally independent of the full earlier history. Its first rate and branch policy are common conditional kernels. These assumptions ensure that the one-attempt channel bound holds at each realized earlier history even when its distribution differs between worlds. Common actions contribute no conditional KL. Attempts aborted after their first bit still count; a stop after the first bit is an abort with terminal continuation.

Grouping observations into attempts gives a finite-prefix KL sum bounded by (32768/n^4) times the world-1 expected number of started attempts. A prefix cut inside an attempt cannot invalidate this upper bound: discarding the remainder is data processing, and the attempt has already been charged. Independent fresh single-endpoint trials add zero only when they cannot later be reused as retained first probes or used to preselect a latent vector for a nominally new attempt.

The unconditional terminal-correctness condition is essential. The event of stopping and rejecting by prefix T increases to finite terminal rejection. Its world-1 probability is at least 1-alpha in the limit and its world-0 probability is at most alpha. Binary data processing, monotone convergence for attempt counts, and lower semicontinuity of binary KL therefore give the declared lower bound. Infinite expected attempt cost satisfies it trivially. Correctness conditional on termination alone would not support the result.

Endpoint-probe count is at least attempt count, so it inherits the same lower bound, without asserting a factor of two when aborts are allowed. If every attempt completes two probes, the usual factor of two holds. The world-1 expectation is correctly retained throughout; no unproved world-0 bound is substituted.

The independent controls enumerate a stopped two-attempt tree with a history-dependent next first rate, branch-dependent next second rate, and an abort branch. Its direct terminal-transcript KL, 0.00049457301417820516344..., agrees with the conditional chain-rule calculation. Its expected attempt and endpoint costs under world 1 are 1.643828290779... and 2.969128581558..., respectively. This is a finite control, not a replacement for the general stopping argument.

## Free-screening counterexample

The new counterexample is correct with its explicit changed cost convention. With B=1/2 fixed, write x=1-a and y=1-b. For each fixed n, the function z^c is differentiable near the positive y, so

    [y+x(1-y)]^c-y^c = O(x),
    S/x^c = 1-O(x^(1-c)) -> 1,
    J1/A = (S/x^c)^(n+1) -> 1.

The limit is taken for each fixed n; there is no unproved uniformity claim in n. Consequently an n-dependent interior a can make the selected alternative probability at least 3/4. Repeated independent screening cycles give independent selected bits, with reference probability 1/2 and alternative probability at least 3/4. A test rejecting when their average is at least 5/8 has each one-sided error at most exp(-N/32), so N>=ceil[32 log(1/alpha)] selected completions suffice. The geometric screening count carries no information by itself, but its first probes still incur expected cost N/A under the declared instrument. This validates the distinction between charged attempts and free screening followed by charged completions.

The independent numerical check uses the direct S formula at 550 decimal digits, separately from the author's log-domain implementation. For n in {1,3,13,64} and x=10^(-k(n+1)) with k in {1,2,4}, all twelve selected alternative probabilities exceed 3/4 and increase toward one. The corresponding log10 expected first-probe costs range from 2 to 16640. An additional moderate-rate geometric control gives 15.625 expected first probes and 16.625 endpoint probes per single completed pair, with its KL exactly equal to expected attempts times one-attempt KL.

## Verification and ancestry

The independent control script imports no author module. It checks exact rational identities, randomized aborts, a strict coarsening negative control, 864 explicit Joe transcript cases including 288 deterministic-first-bit cases, fixed-grid supremum equality at every first rate, KL<=chi-squared, the generic two-branch KL envelope, the stopped history-dependent tree, and twelve direct free-screening limit cases. The maximum observed Joe identity discrepancy at 160-digit precision is about 1.12e-162. Finite grids and floating-point checks are supplementary controls; universal claims rest on the derivations above.

All six final author payloads were inspected. The author controls were rerun into this review directory; their output matches the author output byte for byte. The author correctly labels artificial rational channels as algebraic controls rather than claiming they are actual Joe laws. Literal Joe boundaries are independently covered here. A separate source-binding check passed the five declared inputs and all fourteen predecessor manifest entries, nineteen provenance bindings in total.

The directly read ancestry is the frozen arbitrary-face-replay-design RESULT.md and ASYMPTOTIC_DESIGN.md, plus its manifest and review-status record. Its governing final review receipt was read and its read-only verification script passed all 23 bindings. Section 9 of the earlier contributing note was also read to check the bounded attribution: it contains an explicitly unreviewed factor-two chi-squared observation. That prior receipt expressly excluded second-command adaptation; the present review approves only this new successor's explicitly enlarged contract. Ancestry hash checks establish provenance and unchanged bytes, not fresh independent recertification of every file in the prior closure. The seventh checkpoint remains outside this successor's mutation scope and excludes it.

The review receipt hashes every reviewed author payload and all substantive review evidence. Later author packaging, including freeze/status manifests, may refer to this receipt but is not silently added to its mathematical review scope. Any changed reviewed payload requires a new receipt.
