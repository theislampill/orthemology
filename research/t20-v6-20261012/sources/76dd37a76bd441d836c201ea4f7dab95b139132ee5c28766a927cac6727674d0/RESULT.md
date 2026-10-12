# Source withdrawal and positive-time tail recovery

11 October 2026 UTC. Participating root derivation prompted by the newly received provisional authorial synthesis. Ordinary mathematical application of inherited characteristic dynamics; not a new general regularisation theorem, kernel proof, empirical cognition result or T20 closure.

## Accepted incoming result and its precise use

The received `Cross_Front_Theorems.md`, Theorem L, gives a correct envelope transfer: if the original law controls exp(beta Psi), the audit grows at most C exp(gamma Psi), and the transported envelope is bounded by A Psi+B, then the normalised audited transport controls exp(eta Omega) when eta A+gamma <= beta. Its proof is direct integration, with the positive normaliser retained. This is a useful source-revision interface to an existing tail theorem, rather than a replacement for that theorem's particular envelope and represented-input hypotheses.

For A=0, the stronger direct bound is simply E exp(eta Omega) <= exp(eta B), for every finite eta>=0, under the stipulated valid normalised audited law. No growth-budget condition is needed for that separate bounded-output argument. The boxed C exp(eta B)M/Z estimate retains its own stated assumptions. Failure of its sufficient budget condition is not a proof of tail failure.

The countable source-withdrawal example is also correct. Let

    C0 = sum_{n>=0} 1/(n+1)^2,
    mu(n) = 1/[C0(n+1)^2],
    L(n) = (n+1)^2/4^n.

Here 1<=C0<=2 by the integral comparison for x^-2. Also 0<L(n)<=1 since n+1<=2^n, proved by induction. The report normaliser is 4/(3C0), and its posterior is (3/4)4^-n. Withdrawal by 1/L restores mu exactly, with finite normaliser 3C0/4. The restored law is a valid probability, but for every b>0 its exp(bn)-weighted terms fail to tend to zero. Its mean is also infinite. Finite truncation tests illustrate the cancellation; this series argument establishes the infinite-law statement.

## Constructive continuation using an actual inherited flow

The negative example is an immediate post-withdrawal class failure. It does not establish permanent failure under a later admissible correction. Suppose the quadratic objective

    F(x)=x^2/2

and the unit transport/centred-reaction correction remain independently retained after the source revision. This assumption is material: a source that also changes the objective or its interpretation can require a different replay or prospective-correction contract.

Apply the inherited full-law characteristic evolution to the restored mu:

    X_t(n)=exp(-t)n,
    c_t=(1-exp(-2t))/4,
    Z_t=sum_n mu(n)exp(-c_t n^2),
    mu_t=(X_t)_# [exp(-c_t n^2)mu/Z_t].

The coefficient follows by integrating F(X_s)=n^2 exp(-2s)/2 from 0 to t. The characteristic solution belongs to the inherited arbitrary-initial-probability theorem. No finite initial moment is being supplied or silently required.

For every t>=0,

    1/2 <= 1/C0 = mu(0) <= Z_t <= 1.

For t>0 put

    a_t=c_t exp(2t)=(exp(2t)-1)/4 > 0.

Then an exact cancellation proves

    integral exp(a_t x^2) dmu_t(x)
      = sum_n exp(a_t exp(-2t)n^2)exp(-c_t n^2)mu(n)/Z_t
      = 1/Z_t <= 2.                                      (1)

Thus a valid, explicit positive quadratic-exponential certificate is recovered at every positive time. In particular, for any b>0, Young's inequality gives

    b x <= a_t x^2 + b^2/(4a_t),
    integral exp(bx) dmu_t(x) <= 2 exp[b^2/(4a_t)].        (2)

For every integer k>=0 one consequently has

    integral x^k dmu_t <= k! b^-k 2 exp[b^2/(4a_t)].      (3)

These statements are not merely ordinary finiteness: at a supplied computable t>0 and b>0 their constants are computable and provide numerical bounds. They are not uniform as t decreases to zero. The restored initial law still has its demonstrated tail and mean failures.

For an exact checkpoint, t=log 2 gives X=n/2, c=3/16, a=3/4 and

    integral exp(3x^2/4) dmu_t <= 2,
    integral exp(bx) dmu_t <= 2 exp(b^2/3).

## Effectivity and identity boundaries

The existing exponential-tail continuation theorem takes a uniformly computable full raw-moment name in addition to a computable exponential bound. An envelope alone is not that input. For this explicit countable example, it can be supplied as follows. Set

    S_k(t)=sum_{n>=0} n^k exp(-c_t n^2)/(n+1)^2,
    m_k(mu_t)=exp(-kt) S_k(t)/S_0(t),

with n^0=1, including n=0. The unknown normalising factor C0 cancels and S_0>=1. At any supplied computable t>0 choose a positive rational c_*<c_t. Since n^k <= k!(2/c_*)^k exp(c_* n/2) and n^2>=n for integer n>=1, the tail after N>=0 is bounded by

    sum_{n>N} n^k exp(-c_t n^2)/(n+1)^2
      <= k!(2/c_*)^k q^(N+1)/(1-q),
    q=exp(-c_*/2)<1.                                  (4)

A computable rational upper bound q_bar<1 supplies a terminating truncation search, uniform in k and requested accuracy. Each finite summand is computable. The known lower denominator 1, an upper numerator bound obtained from the same series estimate, and standard division error budgeting give a uniform full moment name. Thus the represented input required by the inherited interior continuation theorem is actually available for this explicit positive-time law. No moment oracle for the divergent-mean initial law is used.

At t=log 2 one may take c_*=1/8 and q_bar=16/17, since exp(-x)<=1/(1+x). A fully rational tail bound is then 17 k!16^k(16/17)^(N+1). This is an existence/effectivity algorithm, not a claimed efficient numerical recovery method or a fresh implementation of a general real-number oracle.

The construction does not supply moment names for arbitrary unspecified laws merely from existence of an envelope. It also does not extend the inherited strict-interior algorithm to its noncomputable endpoint.

A further consequence was identified during independent review. For any computable finite ordinary tilt parameter u, choose b=1+abs(u). Then u>-b, (2) gives a computable positive b-exponential certificate, and (4) supplies the uniform moment name. The inherited interior algorithm therefore computes every raw moment and normaliser of the tilt exp(-u x) for this repaired law. This covers all finite signed linear tilt parameters by selecting an appropriate certificate for each request. It does not turn the weaker general endpoint input representation into an effective one, permit an infinite parameter, or furnish a uniform bound as t decreases to zero.

The correction changes the law. It does not recover the former geometric posterior, restore the withdrawn report's warrant, authenticate a source, or make a counterfactual corrected history become the actual past. The source-withdrawal and prospective-correction operations remain distinct. No claim about practical cognitive improvement follows merely from this mathematical evolution.

The received source-withdrawal loss example and this continuation are compatible. The incoming Theorem L prevents falsely inheriting a tail certificate across revision. The established arbitrary-law correction supplies a permitted means of subsequently obtaining a new certificate. This is the useful cross-front consequence.

## Inheritance and evidence

- Received provisional `Cross_Front_Theorems.md` §15 owns the audit-envelope lemma and the explicit geometric-to-heavy-tail withdrawal example.
- `full-law-gradient-action-tail-20261010/RESULT.md` owns the stated characteristic evolution, its arbitrary-law positive-time moment envelope and the initial-time action qualifications. The frozen full-law predecessor supplies its existence/convergence basis.
- `exponential-tail-effectivity-20261010/RESULT.md` supplies the represented-input, strict-interior continuation theorem and endpoint obstructions. No endpoint effectivity inference is made here.
- The increment here is the explicit positive-time certificate after this particular valid source withdrawal, including computable constants and the distinct-operation interpretation.

Independent review is separate. The short exact checker supplements, and does not replace, the displayed infinite-series and inequality proofs. Frozen received and inherited files remain unchanged.
