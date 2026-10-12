# Independent review: polynomial-coordinate transport continuation

10 October 2026 UTC. Bounded ordinary mathematical review of the root-authored polynomial-transport continuation. Accepted Theorem V is used as a dependency, not independently proved again. The earlier heat, affine, filtered-operator, and truncated-functional review artifacts are unchanged.

## Verdict

PASS under the stated supplied-path hypotheses. The reverse-representation proof, converse, polynomial-coordinate transfer of joint determinacy, nonlinear shear example, and convergent coordinate Carleman series are sound. No additional initial-representation assumption is needed. The full proof remains conditional on V's hypotheses for the pulled-back killing family and on the supplied globally invertible polynomial maps; it is not a theorem for arbitrary polynomial vector fields.

Reviewed proof: polynomial-transport-continuation-20261010/RESULT.md, SHA-256 4f41143b4e4a529952468de8c599c81aa3c6a1737159794cf80080f700e280a9. The written proof, all 36 symbolic controls, input bindings, and author receipt were read. The control script was replayed in the separate isolated-replay/ directory and reproduced the author's EXACT_RESULTS.json byte-for-byte.

## 1. Polynomial and time-regularity obligations

On each compact time window the degree bounds make all substitutions occur in fixed finite-dimensional polynomial spaces. In particular:

- For a fixed q, q∘Psi_t has bounded degree and C¹ coefficients because Psi_t does.
- v_t=(∂t Phi_t)∘Psi_t is a polynomial with continuous coefficients and a common finite degree bound. C¹ regularity of Phi_t is sufficient; a second derivative is unnecessary.
- k_t=h_t∘Phi_t has continuous coefficients and a common finite degree bound. The hypothesis k_t+C−c|y|² SOS, with c>0 uniform on the window, is exactly the additional geometric condition needed by V. If C was not chosen nonnegative, replace it by max(C,0); the extra nonnegative constant is SOS.

The coefficientwise C¹ regularity of L_t makes the derivative of L_t(q∘Psi_t) a finite coefficientwise product rule. No representing measure or differentiation of an infinite series is involved. Both the original hierarchy and the characteristic identity are valid at every time in their supplied domain, with right derivatives at zero.

## 2. Inverse-map and generator cancellation

The maps are assumed mutually inverse on all of R^d, not merely inverse at the initial time or on the support of a prospective measure. Their polynomial identities give

    Psi_t(Phi_t(y))=y,
    Phi_t(Psi_t(x))=x.

Differentiating the first identity yields

    (∂t Psi_t)(Phi_t(y))
      +D Psi_t(Phi_t(y)) (∂t Phi_t)(y)=0.

Substituting y=Psi_t(x) and applying the chain rule to q proves

    ∂t(q∘Psi_t)+v_t·∇(q∘Psi_t)=0.

Consequently M_t(q)=L_t(q∘Psi_t) satisfies

    M'_t(q)=−M_t(k_tq)+M_t(k_t)M_t(q).

Here M_t(k_tq)=L_t(h_t(q∘Psi_t)) follows from Phi_t∘Psi_t=id, and M_t(k_t)=L_t(h_t). Normalization and square positivity are preserved by polynomial substitution. Phi_0=id also implies Psi_0=id, so M_0=L_0. The exact hypotheses of V therefore hold before any law has been introduced.

V gives one uniquely identified initial law for the entire supplied M path. To recover L_t(p), substitute q=p∘Phi_t at that fixed time; this is a polynomial, and (p∘Phi_t)∘Psi_t=p. The author's stated representation follows. It is a reverse-existence result for the abstract hierarchy, not only propagation of an assumed initial measure.

## 3. Converse and integrability

For an initial probability with all polynomial moments, every absolute polynomial moment is finite: |p|≤(1+p²)/2 is sufficient. Put K_t(y)=∫_0^t k_s(y)ds. The SOS premise implies k_s(y)≥−C, so e^(−K_t(y))≤e^(CH) for 0≤t≤H.

For every fixed p, p∘Phi_t, its time derivative, k_t, and their products have uniformly bounded coefficients and finite degree on a compact window. Their absolute values are bounded by a fixed multiple of 1+|y|^N for some finite integer N. An even polynomial power bounds this radial expression if needed. Thus the integrand and its first time derivative have an initial-law-integrable bound. Differentiation under the integral, including the right derivative at zero, is legitimate.

The normalizer is finite and strictly positive because its integrand is positive at every finite y and the initial measure is a probability. The derivative of p(Phi_t(y)) is (v_t·∇p)(Phi_t(y)), while the derivative of the weight is −k_t(y)e^(−K_t(y)). The quotient rule therefore gives precisely the displayed normalized transport-plus-killing hierarchy, with the stated sign.

These facts also justify the full-law-to-path correspondence. Unique continuation means continuation along a supplied compatible future (Phi,h) pair that retains the local-window hypotheses. It does not select an unspecified future vector field or killing schedule.

## 4. Determinacy and the role of a polynomial inverse

At a fixed t>0, let rho be any alternative positive representative of the full functional L_t. Normalization makes rho a probability. Each polynomial has finite absolute rho-integral using the full even moments. Since Psi_t is polynomial, its pushforward (Psi_t)_*rho has all absolute polynomial moments and

    ∫q d((Psi_t)_*rho)=∫q∘Psi_t d rho=M_t(q).

V makes M_t determinate, so its representing measure is unique. Pushing forward by Phi_t then makes rho unique as well. No original-coordinate Carleman hypothesis was used. The maps are global continuous inverses, hence Borel isomorphisms; there is no measurable-inverse gap.

For a fixed initial moment record, its full representing-law fibre therefore parametrizes the admissible transported paths exactly as in V. Different initial laws cannot produce the same complete path: the inverse-coordinate M path would coincide, contrary to V's unique-law conclusion. This does not say that the initial record alone is determinate.

## 5. Nonlinear shear and original-coordinate failure

For every integer m≥3,

    Phi_t(u,z)=(u,z+t u^m),
    Psi_t(x,y)=(x,y−t x^m)

are mutually inverse polynomial maps, with common degree m and smooth time coefficients. Their supplied global path avoids finite-time escape. Direct differentiation and substitution give v_t=(0,x^m) and k_t(u,z)=u²+z². Thus the transformed certificate is exact with c=1,C=0.

The original energy h_t=x²+(y−t x^m)² is coercive for each fixed t: if h_t stayed bounded along a sequence, x and y−t x^m would both stay bounded, forcing y bounded as well. However, for any fixed t>0, c>0, and finite C, the curve y=t x^m gives

    h_t+C−c(x²+y²)=(1−c)x²−c t² x^(2m)+C →−∞.

The candidate is therefore not even nonnegative, and cannot be SOS. This verifies that the example genuinely lies outside V's original-coordinate radial-domination hypothesis. The claim does not need a non-SOS subtlety: pointwise negativity already excludes the certificate. The theorem works because its hypothesis concerns the pulled-back energy instead.

## 6. Gaussian example and factorial bound

The initial density π^(-1)e^(−u²−z²) is normalized. The transformed killing k=u²+z² gives the tilted density

    (1+t)π^(-1)e^(−(1+t)(u²+z²)).

Hence U,Z are independent centered Gaussians with variance sigma_t²=1/[2(1+t)], and the original variables are X=U, Y=Z+t U^m. The preceding inverse-coordinate argument makes their full joint record determinate.

For fixed t>0, expand (Z+tU^m)^(2n). In a term with k factors of U^m, a nonzero centered Z moment requires 2n−k even, hence k even. The corresponding power mk of U is also even. All nonzero terms are nonnegative, for both odd and even m. Retaining k=2n gives

    E[Y^(2n)]≥t^(2n)sigma_t^(2mn)(2mn−1)!!.

For integer r≥1, each factor 2j−1 is at least j, so (2r−1)!!≥r!. Also

    log(r!)=Σ_(j=1)^r log j
      ≥∫_1^r log u du=r log r−r+1≥r log r−r,

which proves r!≥(r/e)^r. Taking the negative 1/(2n) power with r=mn reverses the lower bound exactly as needed:

    (E[Y^(2n)])^(−1/(2n))
      ≤t^(−1)sigma_t^(−m)(e/(mn))^(m/2).

The right side is a fixed constant times n^(−m/2) for the chosen positive t. Its series converges when m>2, so the Y-coordinate Carleman series converges. The argument is not uniform as t decreases to zero, and makes no such claim. Convergence of this sufficient-test series does not prove that the Y marginal is indeterminate. The author correctly confines the conclusion to failure of that coordinate test while retaining joint determinacy.

## 7. Verification boundary

The isolated replay passed all 36 author controls for m=3,4,5 and the selected monomial tests. The result file exactly matches the frozen author's output. These examples supplement the universal chain-rule and factorial arguments above; they do not prove the entire infinite hierarchy or encode V in a formal kernel. The supplied INPUT_BINDINGS.json and all author-receipt file hashes were independently checked. No source campaign, full-functional counterexample claim, field-priority claim, protected edit, or T20 closure is added.
