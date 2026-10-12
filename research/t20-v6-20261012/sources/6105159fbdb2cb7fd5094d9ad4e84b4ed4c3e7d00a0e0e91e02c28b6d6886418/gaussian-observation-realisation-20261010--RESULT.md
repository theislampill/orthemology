# Gaussian observation histories: Fisher regularity does not ensure positive-probability realisation

Status: candidate written derivation under independent review. T20 remains active. No empirical, psychological or metaphysical application is asserted. This packet extends the finite fixed-target observation-history result to a continuous Gaussian family; it does not relabel classical rejection sampling or the Gaussian Fisher metric as new.

## 1. Question and exact contract

Fix an actual random vector X in R^d. Its prior is q_0=N(m_0,V_0), with V_0 positive definite. A prescribed path q_t=N(m(t),V(t)), 0<=t<=T with 0<T<infinity, has C^1 parameters and positive-definite covariance throughout. We ask whether nested events E_t, E_t subset E_s for s<=t, with E_0 certain and P(E_T)>0 can have conditional laws Law(X|E_t)=q_t. This is a selected surviving observation history for a fixed target. It is not physical motion of X, an optimisation algorithm's internal state, or a claim that every realised outcome follows q_t.

The main constructive theorem assumes C(t)=-V'(t) is continuously positive definite on the compact interval. Singular directions have separate exact endpoint and instantaneous diagnostics below; no general rank-changing path theorem is claimed.

## 2. Sharp endpoint diagnostic, including singular contraction

For any densities p,q, an event E with P(E)=b>0 and Law(X|E)=q requires b q<=p almost everywhere. Conversely a fresh independent uniform U and event U<=b q(X)/p(X) realise any such b. Thus the maximum event probability is 1/esssup(q/p), and it is zero if that essential supremum is infinite. This is the classical acceptance/rejection envelope identity, used as an observation contract; see the [complete general-algorithm proof and envelope discussion](https://cswr.nrhstat.org/reject-samp#the-general-algorithm).

For p=N(m_0,V_0), q=N(m_1,V_1), put D=V_0-V_1 and d=m_1-m_0. The maximum is positive exactly when D is positive semidefinite and d belongs to range(D). In that case

    b_max = sqrt(det(V_1)/det(V_0)) exp[-(1/2) d^T D^dagger d].

Here dagger is the Moore-Penrose inverse. D=0 permits exactly d=0 and gives b_max=1. The covariance matrices themselves remain strictly positive definite.

Proof: the log density ratio has quadratic part -(1/2)x^T(V_1^-1-V_0^-1)x. Inverse order reverses positive-definite order, so boundedness first requires D>=0. If d=Db, take x_*=m_0+V_0 b=m_1+V_1 b. Completing the square gives

    log(q/p)(x) = (1/2)log(det V_0/det V_1)+(1/2)d^T D^dagger d
                 -(1/2)(x-x_*)^T(V_1^-1-V_0^-1)(x-x_*).

No simultaneous diagonalisation is used. If d is outside range(D), some z in ker(D) has z^T d nonzero. The null direction h=V_0 z=V_1 z of the precision difference leaves a nonzero linear term z^T d, so the ratio is unbounded. A negative direction of the precision difference likewise makes the quadratic unbounded. Continuity and full support make supremum and essential supremum agree.

Consequently an arbitrarily small nonzero translation at fixed covariance is impossible as a positive-probability event posterior. This does not prohibit ordinary Gaussian conditioning on an exact continuously distributed observation, whose single realised value has probability zero. Regular conditional densities on such values answer a different question.

## 3. Instantaneous one-sided cost

Write u=m', C=-V', y=V^-1(x-m). Direct differentiation gives the score

    s_t(x)=d/dt log q_t(x)=(1/2)tr(V^-1 C)+u^T y-(1/2)y^T C y.

Its essential supremum is finite precisely when C>=0 and u in range(C), and then

    a(t)=(1/2)tr(V^-1 C)+(1/2)u^T C^dagger u.

The proof is the elementary boundedness criterion for a quadratic polynomial, with completion of its square. In particular neither finite Fisher speed nor differentiability controls this essential-supremum cost. This is an instantaneous diagnostic only at singular C; finite value at isolated times does not by itself establish path integrability or admissibility.

Under the main hypothesis C>0 continuously, a is finite continuous and nonnegative. The maximum is attained at the physical point x_*(t)=m(t)+V(t)C(t)^-1u(t).

## 4. Complete first-event construction and sharp probability

Set

    A(t)=integral_0^t a(s) ds,  b(t)=exp[-A(t)],
    S_x(t)=b(t)q_t(x)/q_0(x),
    lambda_t(x)=a(t)-s_t(x)>=0.

For each x, S_x(0)=1 and S'_x=-lambda_t(x)S_x. It is a genuine survival function on the finite interval. Define the conditional first-event law, given X=x, to have density lambda_t(x)S_x(t)dt on [0,T] and residual mass S_x(T) at a censoring symbol infinity. Its total mass is one by the fundamental theorem of calculus. It is a single first-event law, not an unproved nonexplosion claim for infinitely many events. Each x has a finite continuous hazard; uniform boundedness across all x is unnecessary.

Then P(no event by t)=b(t), and its posterior is exactly q_t. The event-time density is b(t)a(t), since integral q_t s_t=0; the latter identity also follows directly from centred Gaussian moments. At a positive-density event time the posterior density is

    r_t(x)=q_t(x)lambda_t(x)/a(t).

The whole law, including event outcomes, averages back to the prior:

    q_0(x)=b(T)q_T(x)+integral_0^T b(t)q_t(x)lambda_t(x)dt.

These formulae establish a complete observation experiment, not merely a sequence of independently designed endpoint events.

This construction is optimal even among arbitrary nested event histories, not just regular hazard models:

    P(E_T)<=exp[-integral_0^T a(t)dt].

For a partition 0=t_0<...<t_n=T, nestedness gives P(E_ti)q_ti<=P(E_t(i-1))q_t(i-1). Section 2 therefore bounds the probability ratio by the Gaussian endpoint envelope of that step. Write D_i=integral_(t(i-1))^ti C(t)dt and d_i=integral_(t(i-1))^ti u(t)dt. Summing negative log bounds gives

    -log P(E_T) >= (1/2)log(det V_0/det V_T)
                    +(1/2)sum_i d_i^T D_i^-1 d_i.

The covariance determinant terms telescope. Continuous positive-definite C on the compact interval has a uniform positive eigenvalue bound. Consequently, as mesh tends to zero, d_i^T D_i^-1 d_i equals h_i u(t_i*)^T C(t_i*)^-1u(t_i*)+o(h_i), uniformly. The sum converges to the integral in section 3. This proof assumes no regularity of the events' probability function and permits extra atoms or singular losses; those cannot improve its bound.

## 5. Endpoint versus full-path cost and exact excess

Put D=V_0-V_T=integral C, d=m_T-m_0=integral u, and b_*=D^-1d. The path cost exceeds the endpoint cost by exactly

    (1/2)integral_0^T (u-Cb_*)^T C^-1(u-Cb_*)dt.

Expanding the square gives integral u^T C^-1u minus d^TD^-1d. The log determinant contribution is identical. This works for noncommuting covariance matrices and time-dependent eigendirections.

Equality holds exactly when u(t)=C(t)b_* throughout the interval, by continuity. Equivalently m(t)+V(t)b_* is one fixed score-maximising physical point. Linear interpolation of the mean and covariance between any strictly contracting endpoints satisfies this condition and attains the endpoint probability. Slowing the same oriented curve does not alter the cost; changing its mean/covariance coordination can.

For d=1, V(t)=2-t, m(t)=t^2, 0<=t<=1, the path mean-cost is (1/2)integral(2t)^2dt=2/3 while endpoint mean-cost is 1/2. Thus the exact-history probability is exp(-1/6) times the endpoint maximum. Linear mean m(t)=t instead attains the endpoint maximum. These are conditional observation constructions, not competing psychological interventions.

## 6. Full Gaussian-family closure fails for this instrument

For minimum hazard under C>0,

    lambda_t(x)=(1/2)(y-C^-1u)^T C(y-C^-1u).

The event posterior is a Gaussian density times a nonconstant nonnegative quadratic. Its continuous density vanishes at x_*(t) and is positive elsewhere, so it cannot agree almost everywhere with any nondegenerate Gaussian density: equality almost everywhere of continuous densities implies equality everywhere. It is an absolutely continuous nonzero density, so it is not a degenerate Gaussian either.

An independent-review contribution gives a moment control as well: for m=0, V=v=2-t and C=1 in one dimension, the event density is r(x)=x^2 q(x)/v. It has mean zero, variance 3v and fourth moment 15v^2. A Gaussian with the same mean and variance has fourth moment 27v^2. This distinguishes distributions without relying only on a density value at one point.

Therefore the chosen Gaussian no-event branch does not make this complete experiment closed within the Gaussian family. Projecting the event branch back to a Gaussian discards information and requires its own approximation/error assessment. This is a concrete representational obstruction, not a claim that all Gaussian conjugate observation instruments fail to close.

## 7. Fisher geometry distinction

For the Gaussian family the squared Fisher speed is

    ||(u,V')||_F^2 = u^T V^-1u+(1/2)tr(V^-1 V' V^-1 V').

It follows directly by squaring the centred score and using Gaussian second/fourth moments; the odd cross term has zero expectation. A path m(t)=m_0+t epsilon v, V(t)=V_0 has finite Fisher length T epsilon sqrt(v^TV_0^-1v) and finite Fisher energy, as small as desired, but every t>0 has maximum positive-event probability zero. Thus no positive guarantee depending only on a small Fisher length can certify this positive-probability history contract. These are lengths of the specified path, not a false identification with ambient geodesic distance.

A stronger independent-review contribution shows why the uniform-contraction hypothesis matters. Let q_t=N(t,2-t^3/3), 0<=t<=1. Its Fisher speed is continuous and finite, and every pair of distinct-time endpoints has positive envelope probability because the variance strictly decreases. Yet the 0-to-t envelope probability is sqrt(1-t^3/6) exp[-3/(2t)], which tends to zero as t decreases to zero. For any nested history, P(E_T)<=P(E_t)<=that envelope, so P(E_T)=0. Here C=t^2 is positive for every t>0, but the mean part of the path cost is (1/2)integral_0^1 t^-2 dt=infinity. Individual endpoint feasibility and finite Fisher length together therefore still fail to guarantee the nested-history contract. This is a smooth path, not an artificial jump in the prescribed posterior.

The result does not invalidate Riemannian noetic modelling, finite-target results, or ordinary Bayesian conditioning. It identifies an extra one-sided domination requirement when a continuous-state geometric path is interpreted as a positive-probability accumulated observation branch. Gaussian closure also needs to account for the failure branches actually produced.

## 8. Evidence and ancestry

The generic density-envelope identity is classical rejection sampling. Gaussian Fisher geometry is classical; [Nielsen’s author exposition](https://franknielsen.github.io/FisherRaoMVN/) distinguishes curve length and ambient geodesic distance. Its approximation algorithms are not used here. The finite path envelope, first-event construction and reverse-Funk interpretation are inherited from gradient-evidence-realization-20261010. The present local increment is the exact matrix-Gaussian diagnostic, continuous-path cost/excess derivation, and complete-branch closure test, with the finite-to-continuous failure made explicit. No field-wide novelty is certified.

Written proofs and exact symbolic/rational controls are not Lean verification or empirical validation. Source reading and review status are recorded separately. No existing source, archive or repository baseline is overwritten.
