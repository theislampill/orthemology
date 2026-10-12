# Independent review: explicit time-one separator

10 October 2026 UTC. Ordinary proof review, pinned-input replay, and independent
exact controls. No generic witness search, numerical quadrature, kernel build,
or change to the frozen main theorem.

## Verdict

PASS for the explicit rational-coefficient polynomial

    H(z,u,v)=z^2048(1+u^4v^2+u^2v^4−u^2v^2)

at t=1 on the specified autonomous path. H is globally nonnegative, has total
degree 2054, and satisfies

    −3^2097161 < L_1(H) < −4/3 < 0.

This is a sparse four-monomial certificate. It is not a claim of low degree,
minimum degree, a witness at every time, or a negative polynomial-square test.

Reviewed computed RESULT.md SHA-256:
b04978552464b25a93fe39c4a61ccf80dcf64bc04e17c23ff6fd6242667f1a20.
The seven-file original freeze is retained in computed-author-frozen-copy.

## Exact hidden value and separation margin

My independently assembled forward-difference construction through degree 8
has exactly the same degree-six negative-prefix F value as the author's full
rational in HIDDEN_BOUND.json. Its numerator has 2058 bits and denominator
1887 bits. Adding the rigorous remaining-tail bound 1/16 gives exactly the
author's rational upper endpoint, and exact integer comparison confirms that
it is below 2^171. The degree-six computation only needs inherited Schur
indices through 10; the large active monomial exponent creates no demand for
large hidden Schur indices.

For the continuous active integral, the strip [69/20,7/2] has width 1/20.
Throughout it, the exponent exceeds 238499/40>5962, using exp(7)<1097.
Since π<4 gives 1/sqrt(2π)>1/3, I_2048(1)>exp(5962)/60. The exact Taylor
bound exp(5)>60 then yields I_2048(1)>exp(5957).

The discrete bound covers the entire integer lattice. For j≤2, dropping
the two nonpositive terms gives the convergent geometric majorant
exp(4096)/(1−exp(−2048))<2 exp(4096). The j=3 term is below exp(5740),
using exp(6)>400. The j=4 term is below exp(5204), using exp(8)>2980.
For every j≥4 the exact successive exponent difference is strictly below
2048−9/2−6·2980<−1, using exp(2)>7. Thus the upper tail is less than
2 exp(5204). The two outer tails together are below exp(5740), because
4096<5204 and exp(536)>4. Adding the j=3 term and dividing by S≥1 gives
J_2048(1)<2 exp(5740)<exp(5741).

All six rational Taylor endpoint pairs were recomputed independently by
direct powers and factorials, rather than the author's incremental recurrence.
Their thresholds and tail-ratio conditions hold exactly. No floating-point
approximation determines a sign here.

Since B<2^171<exp(171), the positive term BJ is below exp(5912), while I
exceeds exp(5957). The 45-unit exponent gap gives W=−I+BJ<−2. The genuine
normalizer satisfies 0<D≤1+n_0≤3/2; dividing a negative numerator by this
positive upper-bounded denominator gives L_1(H)<−4/3, with the correct
inequality direction.

For the lower endpoint, I≤exp(2048²/2)<3^2097152 and BJ≥0 give
W>−3^2097152. Jensen and exp(2)<9 give D>exp(−9)>3^(−9). These imply
L_1(H)>−3^2097161. The huge integer in compact power notation is an exact
rational endpoint, not a decimal approximation.

## Replay, provenance, and recovery

The frozen author's checker passed all 28 final arithmetic checks in an
isolated replay workspace. No input hash check was disabled. Its historical
effectivity input is pinned to the original draft preimage, hash aff8999b…,
because the optional effectivity wording was subsequently corrected. The
mathematical certificate uses the signed-block tail theorem in the unchanged
frozen main proof; it does not depend on the corrected optional wording.
PINNED_REPLAY_DISPOSITION.json records the exact hashes and workspace.

check_computed_independently.py passed 53 further exact assertions, in addition
to the 7,206 effective-construction assertions it invokes. These validate the
independent prefix equality, Taylor bounds, all finite exponent arithmetic,
degree, and interval endpoints. The universal all-integer and infinite-block
tail arguments remain the ordinary proofs reviewed above.

A root replay had overwritten only the elapsed_seconds fields in the two
timing-bearing JSON results. Those replay outputs were captured separately.
The unchanged original REPLAY.log supplied the original elapsed_seconds
values; candidate recovered files matched the original manifest SHA-256
digests before restoration. Both originals were then restored, and all seven
original manifest entries were reverified. Recovery and the root replay
outputs are retained in root-replay-observation. The accurate provenance
statement is byte-identical restoration and verification, not that these two
files had never been modified.

No mathematical blocker or required correction was found in this computed
certificate. The ordinary inherited strict-square theorem remains intact.
