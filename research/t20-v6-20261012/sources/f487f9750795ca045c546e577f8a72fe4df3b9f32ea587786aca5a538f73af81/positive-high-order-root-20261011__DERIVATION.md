# Positive reciprocal Taylor correction: root derivation

11 October2026 UTC. Collaborative prospective mathematics. The inaccessible external R3 claims a second-order repair; this document neither verifies that artifact nor asserts priority over it. First-order reciprocal repair is inherited.

Let P_m(z)=sum_(j=0)^m z^j/j!, w(z)=1/P_m(z), m≥1, z≥0. Taylor's remainder gives

    0 ≤ w(z)−exp(−z)
      = (exp(z)−P_m(z))/(P_m(z)exp(z))
      ≤ z^(m+1)/((m+1)!P_m(z)) ≤ z^(m+1)/(m+1)!.

Both weights lie in (0,1]. For a fixed nonnegative finite loss V and probability μ, define ν_h by density w(hV)/Z_h. Normalization is strictly positive; no finite loss moment is needed merely to define the law. The expansion/error claim needs separate moment hypotheses.

At a fixed terminal time T with n equal steps and unchanged V, intermediate normalizers cancel. The resulting law has unnormalized density w(TV/n)^n. Since 0<exp(−z)≤w(z)≤1,

    0 ≤ w(z)^n−exp(−nz) ≤ n(w(z)−exp(−z)).

If Eμ[V^(m+1)]<infinity, the difference in normalizing constants is at most

    T^(m+1) Eμ[V^(m+1)] / ((m+1)! n^m).

For ordered nonnegative densities f≥g with integrals A≥B>0,

    μ_f = (B/A) μ_g + ((A−B)/A) μ_(f−g),

unless A=B, in which case they coincide. Thus total variation is at most (A−B)/A≤(A−B)/B. Here B=Eμ exp(−TV)>0 is fixed. This proves global order m in TV under the stated moment condition. No state-dependent V, adaptive centering or general time-varying/noncommuting flow is included.

Weighted observable error requires its own integrability, e.g. Eμ[|Q|V^(m+1)] finite and Eμ|Q| finite, to control both the numerator error and normalization correction. A TV bound alone does not control unbounded polynomial Q.

Moment determinacy under bounded density has a simple measure-theoretic proof. If μ is determined by its polynomial moments and ν≤Cμ with C>0, and ν' has the same moments as ν, then Cμ−ν+ν' is a positive measure with the same polynomial moments as Cμ. Determinacy forces equality with Cμ, so ν'=ν. This uses an already determinate μ with the necessary finite polynomial moments; the update does not authenticate its actual empirical law or recover discarded finite-summary information. Each normalized reciprocal step is bounded above by μ/Z_h and so retains that conditional property.

## Stronger endpoint bound supplied by the author and checked by root

The moment hypothesis above is sufficient but is not necessary for fixed-positive-endpoint order. Retaining the weight in Taylor's remainder and telescoping gives, with r=m+1,

    0≤w(z)^n−e^(−nz)≤n z^r/(r!P_m(z)^n)
                         ≤n z^r/(r!(1+z)^n).

For n>r, the scalar maximum of z^r/(1+z)^n occurs at z=r/(n−r) and equals r^r(n−r)^(n−r)/n^n≤r^r/n^r. Hence the unnormalised error is uniformly at most r^r/(r!n^m), independently of z. The same bound at n=r follows by the limiting supremum1. With z=TV/n and Zexp(T)>0, normalization therefore gives TV error at most r^r/(r!Zexp(T)n^m) for every supplied probability law with finite nonnegative V almost surely, without initial loss moments. Root checked this calculus/telescoping argument; attribution remains collaborative.

Algorithmic distinction: on one fixed mesh h=T/N, the step count at time t_k is k, so the bound yields orderm uniformly away from zero (t_k≥τ>0), but does not give orderm over the initial layer near t=0. If each terminal t is instead computed by exactly n separately resized steps h=t/n, the n-asymptotic bound is uniform t∈[0,T] using Zexp(t)≥Zexp(T). These are different numerical procedures. No contradiction with a low-moment first-step obstruction follows.

For h>0, P_m(hV)≥1+hV also implies E_(ν_h)V≤1/(hZ_h), even if EμV is infinite. This is a score-integrability fact, not a warrant claim.

## Observable endpoint strengthening

The improved uniform density bound removes the mixed-moment requirement for fixed-endpoint comparisons when Eμ|Q| is finite. For Q=V^s, s a nonnegative integer, it even removes initial moment requirements. Put r=m+1 and z=TV/n. For n≥r+s,

    V^s [w(TV/n)^n−e^(−TV)]
       ≤ n^(s+1) z^(r+s) / (T^s r! (1+z)^n)
       ≤ (r+s)^(r+s)/(T^s r! n^m).

Here T>0 if s>0. The exact tilted numerator M_g=Eμ[V^s e^(−TV)] is finite, bounded by sup_(v≥0) v^s e^(−Tv); for s>0 that supremum is (s/(eT))^s. The approximate numerator is finite too, by its pointwise difference bound. With A=Eμw(TV/n)^n≥B=Eμe^(−TV)>0, c_s=(r+s)^(r+s)/(T^s r!) and c_0=r^r/r!,

    |M_f/A−M_g/B| ≤ [c_s/B + |M_g|c_0/B²] n^(−m).

Thus every fixed polynomial in V has fixed-positive-endpoint orderm for arbitrary supplied initial μ with finite V almost surely. Constants deteriorate as T tends to zero. This does not cover arbitrary state-polynomial observables unless their growth is controlled by V or independently integrable. It also does not preserve their numerical moments exactly; it approximates the corresponding exponentially tilted moments.

## Sharp asymptotic and geometric scope check

The independent reviewer contributed a sharpness refinement, which root checked separately. For r=m+1 and t>0, the scalar expansion gives n^m(f_n−g)→g(tV)^r/r!, while the uniform earlier bound gives constant μ-integrable domination. Normalizing therefore gives L1(μ) convergence to (g/B)t^r(V^r−E_SV^r)/r!. Taking absolute integrals yields scaled TV limit t^r E_S|V^r−E_SV^r|/(2r!). It is positive exactly when V is not constant almost surely. This remains ordinary collaborative mathematics, not a kernel result.

Reviewer also correctly distinguishes the initial-time L1 derivative from the classical Fisher–Rao tangent: finite EμV suffices for the former; the latter has squared norm Varμ(V), requiring finite variance for finite speed at zero. At positive times exponential damping makes every loss moment finite. Root agrees with this qualification.

A fixed pointwise reciprocal rule is not invariant under adding a constant to V, unlike its normalized exponential target. A qualified gauge repair is possible when a fixed ambient state space and finite ambient infimum are independently specified: use V−inf_ambient V. Additive shifts then cancel and the centering is independent of an audit. Recomputing the infimum over currently positive-probability support is a different rule and can fail commutation after a support-deleting audit. This is a conditional modelling convention, not an automatically supplied datum.

Root derivation frozen after this section on11 October2026 UTC. Earlier sufficient moment bounds remain valid; later sections explicitly strengthen them rather than pretending they were necessary conditions.
