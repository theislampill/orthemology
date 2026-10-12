# An explicit economical separator at autonomous time one

10 October 2026 UTC. Separate additive ordinary research artifact. The frozen valid-initial-partial-escape theorem and its optional effectivity addendum are unchanged. This packet provides an actually computed certificate, rather than another existence proof or semidecision procedure. Independent review is separate. No formal-kernel or protected-source integration claim is made.

## 1. Result

For exactly the specified r=1, k=2, g(z)=z^2 construction, at t=1, take

    q(z)=z^1024,
    H(z,u,v)=q(z)^2 F(u,v)
            =z^2048 (1+u^4 v^2+u^2 v^4-u^2 v^2).

Then H is globally nonnegative and

    L_1(H)<-4/3<0.

An explicit rational enclosure, with its large integer endpoint represented in exact power notation, is

    -3^2097161 < L_1(H) < -4/3.

This deliberately loose lower endpoint is not expanded into millions of decimal digits. The strict upper bound is the useful certificate. The sparse polynomial has four nonzero monomials with coefficients +1,+1,+1,-1, total degree 2054, and q has one coefficient. Every nonzero polynomial-square evaluation remains strictly positive under the inherited theorem. H is a nonnegative-polynomial separator, not a failed square test.

The complete exact arithmetic replay took approximately 0.03 seconds on the recorded replay (excluding process start). It used Schur indices only through 10, signed-measure blocks only through degree six, and six rational Taylor enclosures for elementary constants. There was no quadrature, floating-point sign decision, eigensolver, high-degree hidden Schur computation, dependency rebuild, or unbounded enumeration.

## 2. Exact hidden constant computation

Write B=N(F), with N exactly the sum of negative parts of the degree-by-degree signed blocks in the frozen theorem, using its least admissible strictly increasing integer radii. The exact computation through degree six gives the following radii:

    R_1 = 1
    R_2 = 544
    R_3 = 5326848
    R_4 = 1210631850670080
    R_5 = 114502302747635522324083834880000
    R_6 = 1631190472850543123295836647062767816302697363159516479654977517978.

The corresponding nonzero block atom counts are 0,5,7,13,19,26. All corrected moments through each stage and every stage's lower-degree absolute-moment inequality were recomputed exactly. The largest required inherited Schur index was 10. The rational N_<=6(F) has a 2058-bit numerator and 1887-bit denominator. Its full exact value is retained in HIDDEN_BOUND.json, rather than rounded here.

The proven signed-block tail modulus gives

    0 <= B-N_<=6(F) <= 4 sum_(n>6) 2^(-n) = 1/16.

The exact rational comparison in the replay verifies

    N_<=6(F)+1/16 < 2^171,

so B<2^171. The coarse size is roughly 0.734 times 2^171, but no decimal approximation is used in the sign certificate. Crucially, a high active degree does not require high hidden moments: H only uses hidden moments of degree at most six.

## 3. Continuous active integral lower bound

Let

    I = I_2048(1)
      = (2pi)^(-1/2) integral_R exp(2048x-exp(2x)-x^2/2) dx.

On the rational interval 69/20 <= x <= 7/2, whose length is 1/20,

    2048x-exp(2x)-x^2/2
       >= 2048(69/20)-exp(7)-49/8
       > 2048(69/20)-1097-49/8
       = 238499/40
       > 5962.

Use exp(7)<1097 and (2pi)^(-1/2)>1/3; the latter follows from pi<4. Thus

    I > exp(5962)/60 > exp(5957),

where exp(5)>60 is another elementary rational Taylor bound.

## 4. Discrete active integral upper bound

Let

    h(j)=2048j-j^2/2-exp(2j),
    J=J_2048(1)=S^(-1) sum_(j in Z) exp(h(j)),
    S=sum_(j in Z) exp(-j^2/2)>=1.

All summands are positive. Split the numerator into j<=2, j=3, and j>=4.

For j<=2, h(j)<=2048j, so

    sum_(j<=2) exp(h(j))
       <= exp(4096)/(1-exp(-2048))
       < 2 exp(4096),

using exp(1)>2.

At j=3, exp(6)>400 gives

    h(3)=6144-9/2-exp(6)<5739.5<5740.

At j=4, exp(8)>2980 gives

    h(4)=8192-8-exp(8)<5204.

For every integer j>=4, exp(2)>7 and exp(2j)>=exp(8)>2980 imply

    h(j+1)-h(j)
      =2048-j-1/2-(exp(2)-1)exp(2j)
      <2048-9/2-6(2980)
      <-1.

Consequently

    sum_(j>=4) exp(h(j))
       < exp(5204)/(1-exp(-1))
       < 2 exp(5204).

Because 4096<5204 and exp(536)>4,

    2 exp(4096)+2 exp(5204)<4 exp(5204)<exp(5740).

Combining these inequalities and S>=1 yields

    J < 2 exp(5740) < exp(5741).

These are bounds for the entire infinite lattice, not a truncated numerical sum or an unverified discarded tail.

## 5. Negative value and normalized enclosure

The inherited factorization says

    W=-I+B J,
    L_1(H)=W/D,
    D=I_0(1)+n_0 J_0(1),
    0<D<=1+n_0<=3/2.

Since 2<exp(1), Sections 2 and 4 give

    B J < 2^171 exp(5741) < exp(5912).

Section 3 therefore gives

    W < exp(5912)-exp(5957)
      = exp(5912)(1-exp(45))
      < -exp(5912)
      < -2.

It follows directly that L_1(H)<-4/3.

For the optional finite rational lower endpoint, B J>=0 and the unweighted Gaussian exponential moment give

    W >= -I >= -exp(2048^2/2) > -3^2097152.

Jensen's inequality gives I_0(1)>=exp(-exp(2)). Since exp(1)<3,

    D>=I_0(1)>exp(-9)>3^(-9).

Together these imply L_1(H)>-3^2097161. Thus the stated interval has rigorously rational endpoints and a strictly negative upper endpoint. No approximation to the normalizing constant is necessary.

Finally, F>=3/4 globally by the inherited elementary proof, and z^2048>=0 globally, so H>=0. This establishes its separating role without testing sampled points.

## 6. Why a one-term q works

At a high positive active moment, the continuous tilted lognormal integral can draw mass from a narrow interval between two support points of the discrete representative. The lattice misses that interval. With degree 2048 and t=1, the interval of logarithmic coordinates [3.45,3.5] already suffices to overcome the entire hidden multiplier B. This is a direct quantitative use of the given continuous/discrete pair. It avoids approximating a compactly supported function by a general polynomial.

The computation therefore does not encounter the potential high-index Schur explosion. It would be misleading to report an exhausted finite-search frontier: no such search was necessary or run. The certificate is sparse and easy to verify, though its total polynomial degree is 2054. No optimality or minimum-degree claim is made, and this particular q is only claimed for t=1.

## 7. Exact replay and evidence limits

Run from the workspace root:

    python valid-initial-escape-computed-separator-20261010/check_certificate.py

The script invokes compute_hidden_bound.py, recomputes the signed prefix using the inherited exact Schur implementation, verifies B<2^171, and checks the finite rational inequalities above. Rational bounds for exp(x) use

    T_n(x)=sum_(k=0)^n x^k/k!,
    T_n(x)<exp(x)<=T_n(x)+(x^(n+1)/(n+1)!)/(1-x/(n+2)),

for x>0 and n+2>x. The upper bound follows by bounding every subsequent ratio of series terms by x/(n+2). The recorded Taylor orders for x=1,2,5,6,7,8 are 12,20,30,40,50,60. Both exact rational endpoints are retained in CERTIFICATE.json. Twenty-eight final arithmetic checks pass in addition to the stage-by-stage exact signed-prefix assertions.

INPUT_BINDINGS.json records hashes of the inherited proofs and implementation. HIDDEN_BOUND.json records the full exact hidden value, radii, arithmetic sizes and timing; CERTIFICATE.json records q, H, the enclosure, Taylor bounds and checks; REPLAY.log records the executed result. The infinite signed-block tail theorem, Gaussian moment identity, positivity theorem, and the all-integer estimates written above remain ordinary mathematics. This is not a Lean proof and does not replace the prior theorem's independent review.
