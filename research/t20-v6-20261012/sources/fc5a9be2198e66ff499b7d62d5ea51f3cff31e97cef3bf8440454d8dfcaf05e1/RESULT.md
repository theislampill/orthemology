# An explicit moving two-atom moment chart

10 October 2026 UTC. Additive conditional mathematics in active T20. Ordinary derivation and exact algebraic checks; no kernel verification, historical novelty, actual noetic identification, protected modification, or research closure claimed.

## Constructive result

Write m0=1, m1=a, m2=b, m3=c and D=b−a². The complete space of probability laws on the real line with exactly two distinct positive atoms is smoothly parametrised by

    U = {(a,b,c) in R³ : D>0}.

There is no assumed known support. Set

    s=(c−ab)/D,     p=(ac−b²)/D,
    Delta=s²−4p=(c−3ab+2a³)²/D²+4D>0,
    x=(s−sqrt(Delta))/2,  y=(s+sqrt(Delta))/2,
    w=(y−a)/(y−x).

Then x<y and x<a<y: the identity a²−sa+p=−D<0 places a strictly between the roots. Consequently 0<w<1. The law w delta_x+(1−w) delta_y has the supplied first moment. Both atoms satisfy z²=sz−p, so its second moment is sa−p=b and its third is sb−pa=c. Conversely any distinct positive two-atom law has D=w(1−w)(x−y)²>0. The two recurrence equations b=sa−p and c=sb−pa uniquely determine s,p because D>0, and hence determine its ordered roots and weight. All displayed maps are smooth on U.

Thus the parametrisation is a global smooth coordinate system for unordered two-atom laws (using the canonical real ordering of their support). It is not an identification of all probability laws with three moments: e.g. a standard normal shares (a,b,c)=(0,1,0) with the law on {-1,1}. The rank-two premise is indispensable. The earlier finite Vandermonde kernel packages assumed a known support; their Lean status does not cover this moving-support chart.

All subsequent moments are smooth rational functions on U:

    m_(n+2)=s m_(n+1)−p m_n.

This supplies exact finite closure on the specified two-atom model. It does not assert that the same finite coordinates close the dynamics over arbitrary laws.

## Genuine metric in these coordinates

On ordered support coordinates (w,x,y), use

    G = dw²/[w(1−w)] + w dx² + (1−w) dy².

This is positive definite. Let J be the Jacobian of (a,b,c) with respect to (w,x,y). Direct algebra gives

    det J=w(1−w)(x−y)^4>0,     det G=1.

The moment cometric is B=J G^(-1) J^T, with entries for i,j in {1,2,3}

    B_ij = i j m_(i+j−2) + m_(i+j) − m_i m_j.

Its determinant is

    det B = w²(1−w)²(x−y)^8 = D² Delta² >0.

Therefore h=B^(-1) is an actual smooth Riemannian metric on U. Pulling h back by the displayed moment map gives exactly G. It is not the Euclidean metric on three raw moments, or an assumed ambient Fisher metric. The higher moments in B are obtained from the recurrence, not free unknown inputs or measured quantities silently supplied.

For any differentiable objective E(a,b,c), its negative h-gradient is −B grad E. The specific linear-potential case E=L(F) has the moving-atom/Fisher-reweighting dynamics in the joint atomic geometry result. General nonlinear E requires its own trajectory existence/nonexplosion checks; this chart alone does not supply them.

## Quadratic objective: an exact autonomous finite ODE

For F(z)=z²/2, E=b/2, the natural-gradient equation is

    a' = −a −(c−ab)/2,
    b' = −2b −(m4−b²)/2,
    c' = −3c −(m5−bc)/2,
    m4 = s c−p b,     m5=s m4−p c.

This is a smooth rational vector field throughout U. It is globally forward realised by

    x_t=e^(−t)x_0,   y_t=e^(−t)y_0,
    q(t)=(1−e^(−2t))/4,
    w_t = w_0 exp(−q(t)x_0²) /
          [w_0 exp(−q(t)x_0²)+(1−w_0)exp(−q(t)y_0²)].

In particular D_t=w_t(1−w_t)e^(−2t)(x_0−y_0)² remains strictly positive for every finite t. The trajectory cannot cross a spurious moment boundary. Its dissipation is

    E' = −b −(m4−b²)/4 ≤ −2E,

because b is the expectation of z² and m4−b² its nonnegative variance. Every such law converges weakly to delta_0 as t grows, although finite-time transitions remain injective on their image. This is exact asymptotic loss of recoverability at the limiting law, not finite-time erasure or a claim of numerical stability.

## Two scope controls

1. The positive rank-two laws (delta_-1+delta_1)/2 and delta_-2/5+4 delta_(1/2)/5 agree through degree two, but have third moments 0 and −3/2. Dropping c destroys this particular unknown-support chart.
2. Points (a,b,c)=(0,epsilon,1), epsilon>0, all lie in U. As epsilon tends to zero the triple tends to (0,0,1), which is not a probability moment triple: zero variance and zero mean force a point mass at zero and hence third moment zero. Thus the Euclidean closure of U is not automatically a space of valid limiting laws. The formulas do not license arbitrary boundary continuation. This is compatible with the separate nonexplosion safeguards already proved.

## Evidence and inheritance

Direct predecessor reading: finite-moment-recovery-lean-20261009/README.md; separating-projection-lean-20261009/README.md; complete-flow-finite-rank-20261010/RESULT.md. The first two establish known-support recovery and finite separating projections with bounded kernel credit. The third supplies a complete abstract-hierarchy lifting theorem under explicit rank and characteristic conditions. The metric computation here is direct finite calculus; the broader joint geometry author and independent reviewer are assessing its source interface separately.

check_exact.py verifies the chart identities, Jacobian, cometric, determinant, recurrence and quadratic dynamics, and the two-positive-law control. These algebra checks do not replace the inequalities or analytic proof above. No empirical interpretation of weights, atoms or objective has been established here.
