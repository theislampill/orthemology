# A polynomial version of the universal AND-hull rescue

2026-10-01. This replaces the positive-part potential only for the strongest kernel-verification target. The previous construction remains valid. The truth hull and constructive second-order method are unchanged.

Use the Boolean AND truth hull from GLUING_AND_COUPLING.md and

    ψ(t)=t²/2+4t⁴,      r(s)=1+48s²,
    F(x,y,z,w)=ψ(x)+ψ(1−y)+50z²+50w²,
    G(x,y,z,w)=(x²+y²+z²+w²)/2.

These are finite C∞ polynomial potentials, strictly convex everywhere. At s=1/4,

    (log r)'=6 > 16/3=1/[s(1−s)],

so the projected isolated rank-one block fails. Yet the full pair has common strict local repairs at every relative-interior point of the AND hull, in every transverse direction.

## Uniform parameter inequality

With ρ=100/r and λ=96s/r, the same starred primal construction works if

    λ < (1+s)(1−r/100)/[s(1−s)].

Multiplying by the positive denominator gives

    P(s)=(1+s)r(s)(100−r(s))−9600s²(1−s)
        =−2304s⁵−2304s⁴+14304s³−4896s²+99s+99>0.

For s∈[0,1], P(s)≥132/5. An exact degree-five Bernstein expansion on each of the eight intervals [j/8,(j+1)/8] proves this lower bound. All coefficients are at least132/5. This rational certificate is the first target in lean/PolynomialAND.lean.

## Correction in simpler rational form

For p=(s,1−s,z,w), put T=z+w and A=T−2s. Relative interior gives 0<s<1 and 0<A<1−s. Let h₁,h₂ be the transformed first-two direction coordinates, let h_z,h_w be the free directions, and put

    μ=(h₁+h₂)/2,     e=(h₁−h₂)²/4>0,
    γ=96e s²/[T(100−r)],
    β=(48e s−100γ)/r,
    θ=9600s²A/[r T(100−r)],     m=1−θ>0.

Then use

    q=s+εμ+ε²β,
    z_c=z+εh_z+ε²γ,
    w_c=w+εh_w+ε²γ.

These are exactly the earlier starred correction after simplification. The G leading gains for the truth classes (AND,input-sum)=(0,0),(0,1),(1,2) are

    em,    em+γ,    em+e λA/T,

and the F leading gains are

    r em,  r em+100γ,  r em.

Every leading gain is at least em>0 since r≥1. The two mixed-input vertices have identical leading gains.

## Actual gains, rather than assumed Taylor coefficients

The scalar divergence has the polynomial identity

    D_ψ(v,t)=(v−t)²/2+4v⁴+12t⁴−16vt³.

Consequently the full gains are exactly ε² times their stated leading term plus ε³ times a polynomial in ε. The G remainder has degree one; each of the two possible AND truth values gives an F remainder of degree five. Those identities can be checked by ring normalization without trusting a Taylor oracle or assuming the asymptotic relation.

For each remainder polynomial R(ε)=Σ_j c_j ε^j, set ‖R‖₁=Σ_j|c_j|. For 0≤ε≤1, |R(ε)|≤‖R‖₁. Let M be the sum of the three coefficient norms (G,F-at-0,F-at-1). Then every gain is at least

    ε²[em−εM].

In particular it is strictly positive whenever

    0<ε<min(1, em/[2(M+1)]).

## A genuine feasible scale

The AND-hull barycentric coefficients of the candidate are

    q, z_c−q, w_c−q, 1+q−z_c−w_c.

At ε=0 these are s,z−s,w−s,1+s−z−w, all strictly positive. Put b₀ equal to their minimum. Let L be the sum of absolute values of all linear and quadratic coefficients of these four polynomials. For 0≤ε≤1, each coefficient changes by at most εL, so they remain positive for ε<b₀/[2(L+1)].

To keep the baseline in the forecast cube, let p₀=min(s,1−s,z,1−z,w,1−w)>0 and H=1+|h₁|+|h₂|+|h_z|+|h_w|. One fully explicit admissible threshold is

    δ=min(1, em/[2(M+1)], b₀/[2(L+1)], p₀/[2H])>0.

For every 0<ε<δ the baseline is in the open cube, the candidate is genuinely in the relative interior of the AND truth hull, and all four truth-state losses strictly decrease under both scores. δ may depend on p and h; no uniform boundary threshold is claimed.

The kernel theorem will identify its exact realized scope. The existence of positive leading coefficients alone must not be described as a kernel proof of the actual nonlinear score inequalities.
