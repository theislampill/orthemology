# Independent adversarial review: robust replay certificate and sampling test

8 October 2026 UTC. Separate prospective mathematical scratch review. Excluded from the sixth checkpoint being assembled.

**PASS for the stated conditional four-coordinate separation theorem and its bounded-sample reference test.** No mathematical defect was found in the explicit radius, uniform exclusion of all wrong positive integer counts, or the two statistical error guarantees under the declared contracts. This verdict does not validate those contracts in an application, certify empirical activity, establish protected integration, or confer T20 or other closure.

## Reviewed object and bounded scope

The reviewed author file is `finite-panel-replay-robustness/RESULT.md`, with verified SHA256:

    3f12f86b3c1699448c350de05add930e67a3ccacc0c54d6dd3e134edb3c92ebe

The predecessor `finite-panel-replay/RESULT.md` was read and independently checked where the new theorem uses it. Its verified SHA256 is:

    327b6fb25944ac90e7ecd6010a427993b69400fbdc9b79928d731120b6d62243

The earlier `finite-panel-replay-review/REVIEW.md` was read for context. Its verdict was not substituted for checking the new proof. This review covers the mathematical statement, its necessary observation and sampling contracts, the transfer of the predecessor's gap to the explicit function F_m, the perturbation bounds, and the sampling test. It does not review an implementation, experimental data, an operational calibration procedure, or a larger integration packet.

All inequalities below were checked analytically. Independent symbolic calculations also confirmed the displayed rational identities and derivative formula; these calculations are consistency checks, not a replacement for the all-integer arguments. No author or predecessor file was edited.

## 1. Reduction and the positive neighborhood

Endpoint preservation, coordinate-only common marginals, and mutual independence of the m route pairs correctly give

    p = A^(1/m), q = B^(1/m), u = 1-p, v = 1-q.

For one common collection of valid route tables, x_j is joint success, y_j=1-x_j, and z_j=1-u-v+x_j. Thus

    Q = product y_j, J = product z_j, y_j+z_j = p+q.

The identity for J specifically requires the two replay probes to use the same realized gate variables, and the identity for Q requires the same pair law in the fresh diagonal batch. Neither follows from shared inventories or shared marginal laws alone.

Writing k=n+1, Bernoulli's inequality gives A0=B0>=2/3 and J0>=4/9. Since n/k^2<=1/4, it also gives Q0>=35/36. The radius 1/(10000 k^2) is at most 1/40000. Consequently every probability vector under consideration and the segment joining it to the reference has A,B>1/2 and all four coordinates >1/3. Each coordinate remains at most one along this segment.

For m>=2, A^(1/m)>=sqrt(A) and similarly for B, so

    sqrt(2)-1 < s = p+q-1 <= 1.

This establishes a positive differentiability domain along the entire segment. The segment need not itself consist of feasible route models: it only needs to lie in the domain of the explicit residual functions, which it does. No smoothness of the unknown calibration maps is invoked.

## 2. Larger counts: uniform baseline gap and perturbations

For every m>n, valid x_j lie in [0,1], and

    sum x_j >= 1-product(1-x_j) = 1-Q.

Expanding product(s+x_j), with s>0 and x_j>=0, therefore proves the necessary inequality

    J >= F_m(A,B,Q) = s^m + (1-Q)s^(m-1).

At the reference, let c=n/m, p0=(1-t)^c, u0=1-p0, d=u0/p0, and s0=1-2u0. The exact identity s0=p0^2-u0^2 gives an identity for F_m itself:

    F_m(A0,B0,Q0)/J0 = (1-d^2)^m [1+(1-Q0)/s0].

Thus the predecessor's argument genuinely supplies a lower bound for this explicit function, rather than merely a constraint on a hypothetical feasible J. Concavity gives d<=ct/(1-t); the integer separation m>=n+1 gives c<=n/(n+1). Therefore

    m d^2 <= A_* = n^2/[(n+1)(3n+2)^2] < 1.

Integer Bernoulli and s0<=1 give positive factors that can safely be multiplied. Also 1-Q0>=W=n/[9(n+1)^2+n]. Direct subtraction confirms

    (1-A_*)(1+W)-1
      = n(n^2+7n+4)/[(n+1)(9(n+1)^2+n)(3n+2)^2]
      = delta_n.

The coarse simplifications are correct:

    delta_n >= n/(90 k^3) >= 1/(180 k^2),
    F_m(A0,B0,Q0)-J0 >= 1/(405 k^2).

The second inequality in the first line uses n/(n+1)>=1/2 and includes n=1.

Direct differentiation confirms

    partial_A F_m
      = A^(1/m-1)[s^(m-1)+(1-Q)(1-1/m)s^(m-2)].

On the segment, A^(1/m-1)<=1/A<=2, both powers of s are at most one, and 0<=1-Q<=1. Thus the bounds 4,4,1 for the absolute A,B,Q derivatives are valid uniformly over all m>=2. Including the coefficient-one J term yields the claimed total perturbation bound 10 epsilon_n.

The resulting necessary residual has the strictly incompatible lower bound

    F_m(A,B,Q)-J
      >= [1/405-1/1000]/k^2
       = 119/(81000 k^2) > 0.

There is no omitted large-m regime, passage of a limit through an inequality, or bound whose constant deteriorates with m. Integrality supplies the gap from m=n; a finite upper bound on m is unnecessary.

## 3. Smaller counts: scaled Holder and strong convexity

For nonnegative route-table entries, generalized Holder gives

    Q^(1/m)+J^(1/m) <= product(y_j+z_j)^(1/m)
                       = A^(1/m)+B^(1/m).

Consequently R_m=m[A^(1/m)+B^(1/m)-Q^(1/m)-J^(1/m)] must be nonnegative. Scaling by m removes the derivative factor 1/m: each absolute coordinate derivative is x^(1/m-1)<=1/x<=3 on the segment. The four-coordinate perturbation is therefore at most 12 epsilon_n. This includes m=1, where the derivatives actually have magnitude one.

For m<n, put c=n/m>1. The two arguments x_plus=1-t^2 and x_minus=(1-t)^2 have midpoint 1-t and half-separation t(1-t). On their interval,

    f''(x)=c(c-1)x^(c-2) >= c(c-1)(1-t)^(2n).

For 1<c<2, x^(c-2)>=1. For c>=2, use x>=(1-t)^2 and c<=n; the claimed lower bound is deliberately looser than the resulting bound with exponent 2(c-2). The strong-convexity midpoint inequality supplies exactly the factor stated by the author: the two quadratic remainder contributions sum to the curvature bound times the squared half-separation, with no missing factor of two.

Finally,

    m c(c-1)=n(c-1)>=n/(n-1)>1,
    (1-t)^(n+1)>=1-(n+1)t=2/3.

These give

    -R_m(A0,B0,Q0,J0) >= 4/(81 k^2),
    R_m(A,B,Q,J) <= [-4/81+3/2500]/k^2
                  = -9757/(202500 k^2) < 0.

All smaller positive integer counts are therefore excluded. For n=1 this part is correctly vacuous. The larger-count proof remains valid, with t=1/6, delta_1=6/925, and epsilon_1=1/40000. There is no missing n=1 case.

## 4. Sampling theorem and the exact meaning of its guarantee

For replay replicate i, X_i,Y_i are the two absence indicators and Z_i=X_iY_i is exactly the joint-absence indicator. Under independent fresh draws of the latent vector between replicates, each coordinate sequence separately is iid Bernoulli. Dependence between X_i,Y_i,Z_i within a replicate is expected and harmless for the argument. The diagonal sequence is iid Bernoulli with mean Q under the same fixed route count, calibrations, and per-route pair laws.

Hoeffding at h=epsilon_n/2 gives, for each coordinate, an error probability at most 2 exp(-N epsilon_n^2/2). The union bound over four coordinates gives

    P(max coordinate estimation error > epsilon_n/2)
      <= 8 exp(-N epsilon_n^2/2) <= alpha

when

    N >= ceil(2 epsilon_n^(-2) log(8/alpha))
       = ceil(200000000 k^4 log(8/alpha)).

Neither independence of the four estimators nor independence between the two batches is needed by this union bound. The stated independent-batch design supplies a sufficient sampling contract. In that design there are 2N independent latent-vector replicates and 3N probe evaluations.

At the exact reference vector, the simultaneous accuracy event implies acceptance. Under a wrong-count model, accuracy and acceptance together would put its true vector within epsilon_n of the reference in every coordinate, contradicting the deterministic theorem. Closed acceptance and accuracy inequalities are compatible with the strict wrong-count discrepancy. Thus reference rejection is at most alpha and wrong-count acceptance is at most alpha.

The latter guarantee is uniform because the same concentration bound and deterministic radius apply to every model in the alternative class. It is a supremum-of-risk statement, not a simultaneous experiment over all infinitely many candidate counts; no additional union bound over m is required.

This is correctly presented as an exact-reference test, not a total count estimator. For example, at n=m=1 and t=1/6, comonotone A/B gates have the correct face probabilities but Q=J=5/6. Their deviations from Q0=35/36 and J0=25/36 are both 5/36, far beyond epsilon_1. Such a same-count model is rejected with high probability. Conversely, a nonproduct threshold copula that preserves the finite panel is accepted with the same reference guarantee. Acceptance cannot certify global gate independence.

## 5. Adversarial contract checks

The following attacks fall outside the author's explicit class. They verify that the exclusions are substantive boundaries, not facts established by acceptance.

### Common marginals

If route-specific marginal calibrations are permitted, split each reference route into two independent routes. At the tested level give Route I both marginals and joint success t^2. Give Route II both marginals t/(1+t) and joint success zero. Both tables are valid. Their combined face absence is 1-t, diagonal absence is 1-t^2, and replay absence is (1-t)^2. Repeating independently n times yields an exact m=2n alias. The earlier boundary construction supplies endpoint-preserving calibration and fixed-threshold realizations. Common marginals cannot be inferred from the four observations.

### Mutual route independence

Duplicate each reference route a fixed number r>1 of times, using perfect copies of its realized gate pair. The resulting m=rn routes share the reference marginals and preserve the union of successful routes, hence all four observations. Distinct routes are no longer mutually independent. The theorem requires mutual independence, not merely an inventory of individually valid route tables.

### One fixed pair law across the two observation modes

There is an explicit n=1,m=2 alias if the replay and diagonal batches may use different within-route couplings. Put

    p=sqrt(5/6), u=1-p, x_D=1-sqrt(35/36).

Give both routes marginals u. In the replay batch use independent A/B gates, whose joint success is u^2. Then A=B=p^2=5/6 and J=p^4=25/36. In the diagonal batch instead use joint success x_D, obtaining Q=(1-x_D)^2=35/36. The diagonal table is valid because 0<x_D<u<1/2; the comparison x_D<u follows from 35/36>5/6. These exactly match the n=1 reference, but use different laws across batches. The author expressly rules this out.

### No-mutation, retained-realization replay

Use the same n=1,m=2 marginals u and valid diagonal joint success x_D from the preceding example for a single stationary gate law. If the two face probes independently redraw their gate vectors, their joint absence is A B=25/36 automatically. Together with A=B=5/6 and Q=35/36, this is another exact wrong-count alias. It is excluded precisely because a fresh redraw is not retained-gate replay. Merely preserving the inventory, calibration, or law is insufficient.

### Stationarity and independent replicates

Even exact reference marginal probabilities do not yield the statistical guarantee if all nominal replicates reuse one latent vector. Then each empirical coordinate is zero or one. Since A0 lies strictly between zero and one and is farther than epsilon_n/2 from either endpoint, the exact-reference acceptance probability is zero, however large N is. Thus the iid-replicate assumption is essential. Likewise, changing coupling laws across batches can produce the exact alias above; shared calibration alone is not stationarity.

### Known/selectable calibrated commands

Treating nominal t as true rate t without calibration is unjustified. For example, if the reference's actual coordinate calibration is h(a)=a^2, evaluating nominal t gives reference face absence (1-t^2)^n rather than (1-t)^n. The finite design therefore needs known/selectable commands realizing true rates t, or remains a latent-coordinate result. The new theorem does not claim to invert unknown calibration maps.

## 6. Disposition and remaining limits

**PASS within the declared finite-count, shared-marginal, mutually independent-route, same-gate replay, fixed-law iid sampling, and calibrated-command contracts.** The rational radius is sufficient, all four coordinates may move simultaneously, and the bounds apply uniformly to unbounded positive integer alternatives. The sample-size expression and both error probabilities are correct; its conservatism is appropriately disclosed.

The proof does not validate the structural contracts, identify all same-count alternatives, establish universal model validity, certify global independence, or turn unknown nominal calibration into an operational finite panel. It describes no empirical experiment or physical intervention. This separate review makes no checkpoint integration, readiness, or closure claim.
