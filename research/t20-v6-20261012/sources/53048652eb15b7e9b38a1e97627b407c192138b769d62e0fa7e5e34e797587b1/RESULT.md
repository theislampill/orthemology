# A finite family certifying universal positive audit covariance

11 October 2026 UTC. Additive mathematical follow-on to received `Cross_Front_Theorems.md` §13, Theorem J. No received or inherited artifact is changed. This is a direct proof and explicit countercontrol, not a formal-kernel certificate, literature-priority claim, integration decision, or closure claim.

## Result and inheritance

On the entire positive labelled simplex times a fixed context domain, exact flow commutation with the 2(n−1) coordinate audits that multiply one nonreference weight by 2 or 3 already implies commutation with every positive audit. The assumption is a functional identity at every state and for local times, not successful evaluation at finitely many states or time steps.

The received theorem already warns that integer-generated restricted groups can admit periodic log-odds fields. The addition here is a concrete sufficient finite-family certificate, plus a complete nonlinear fixed-energy Fisher-gradient realization of that warning. The general universal-audit classification and its metric corollary remain Theorem J's results. No new classification of arbitrary audit groups is claimed.

## The finite family theorem

Let n≥2 and M=Δ°_(n−1)×X, where X is a fixed open smooth domain. Let F be a C1 vector field on M, with its unique local flow Φ_t. For positive r, define

    T_r(w,x)=(B_r(w),x),     B_r(w)_j=r_j w_j / Σ_k r_k w_k.

For each i<n and a∈{2,3}, let r^(i,a) have entry a in coordinate i and entries 1 elsewhere. Suppose, for each of these 2(n−1) audits and every z∈M,

    Φ_t(T_r z)=T_r Φ_t(z)

for all sufficiently small t for which the two sides are defined. Then the flow commutes with every positive audit wherever defined, and

    xdot=v(x),
    wdot_i=w_i(c_i(x)−Σ_j w_j c_j(x)).

Conversely, every field of this form satisfies the finite-family identities. Thus those identities are equivalent to Theorem J's universal audit covariance. No global completeness assumption is needed. For n=1 the finite family is empty and the conclusion is automatic: the weight is fixed and every position field qualifies.

### Proof

Set u_i=log(w_i/w_n), i<n. This is a global coordinate system Δ°_(n−1)≅R^(n−1). In these coordinates the audits are translations u↦u+(log a)e_i, leaving x unchanged. Differentiating the assumed flow identities at t=0 makes the transformed field G invariant under each such translation, for every (u,x).

Because the entire u-space is available, substituting u−(log a)e_i gives invariance under its negative as well. Composition gives invariance under every translation in

    H=(Z log 2 + Z log 3)^(n−1).

The ratio log 2/log 3 is irrational: a rational ratio would imply 2^q=3^p for positive integers p,q. The scalar group Z log 2+Z log 3 is dense in R. For completeness, pigeonholing multiples of log 3 modulo log 2 supplies nonzero elements of the group arbitrarily close to zero; integer multiples of a positive such element approximate any real number with error at most half that element. Applying this independently in each coordinate makes H dense in R^(n−1).

For any h∈R^(n−1), choose h_k∈H with h_k→h. Continuity now gives

    G(u+h,x)=lim_k G(u+h_k,x)=G(u,x).

Hence G=(c_1(x),…,c_(n−1)(x),v(x)). Set c_n=0 and transform back using Σ_i wdot_i=0 to obtain the displayed centred replicator field. Its invariance under every log-odds translation gives full vector-field equivariance. Transforming a solution by any T_r gives another solution of the same field, so uniqueness yields flow commutation. Since T_r and its inverse are global diffeomorphisms of M, transformed solutions have the same maximal time intervals. The converse follows directly. ∎

Under the additional connected Cartesian-product position-domain, C2 energy, and fixed joint metric hypotheses of Theorem J's metric corollary, the same finite-family identities therefore force E(w,x)=Σ_i w_i V_i(x_i)+C. No position-domain extension or unlabelled-law descent is supplied by this observation.

## An explicit nonlinear gradient countercontrol for one audit

Take the binary simplex (p,1−p), 0<p<1, with Fisher metric

    g_p(dp,dp)=dp²/[p(1−p)].

Fix 0<ε<1, L=log 2, and define

    u=log(p/(1−p)),
    c(u)=1+ε cos(2πu/L),
    E(p)=−∫_(1/2)^p [1+ε cos(2π log(s/(1−s))/L)] ds.

The energy is C∞ on the interior. Its derivative E'(p)=−c(u) is nonconstant, so E is genuinely nonaffine in the weights. The negative Fisher-gradient equation is

    pdot=−p(1−p)E'(p)=p(1−p)c(u),
    udot=c(u).

Because 1−ε≤c(u)≤1+ε and c is smooth with bounded derivative, the u-flow exists uniquely for all real time and stays finite at each finite time. Therefore the p-flow is complete within the positive simplex, approaching its boundary only asymptotically. Along every trajectory,

    dE/dt=−p(1−p)c(u)²<0.

Auditing the first weight by a sends p↦ap/[1+(a−1)p] and u↦u+log a. Since c has period log 2, the complete flow commutes with audit a=2, and hence with its integer powers and inverse powers.

It does not commute with audit a=3. At u=0,

    c(0)=1+ε,
    c(log 3)=1+ε cos(2π log 3/log 2)<1+ε,

because log 3/log 2 is not an integer. The infinitesimal log-odds velocities in the two orders therefore differ. More explicitly, writing ψ_t for the u-flow,

    ψ_t(log 3)−[ψ_t(0)+log 3]
      =t ε[cos(2π log 3/log 2)−1]+o(t),

which is nonzero for all sufficiently small positive t. This is an exact countercontrol, not a numerical estimate. Completeness, strict positivity, smooth fixed energy, and strict gradient descent do not turn one restricted audit symmetry into universal symmetry. For the scaled metric g/α, replace E by E/α to retain this same flow.

## Applicability guard

The theorem certifies finitely many audit *maps*, each through an exact identity on the full fixed-context domain. Approximate commutation, equality at finitely many sampled states, or equality for a single nonzero time step does not satisfy its hypothesis and receives no error estimate here.

There is also no qualitative rigidity conclusion from merely small global generator residuals without an additional common regularity bound. For positive integers q, set

    c_q(u)=1+ε cos(2πq u/log 2).

These fields commute with audit 2 exactly, while their audit-3 log-odds field residual is

    sup_u |c_q(u+log 3)−c_q(u)|
      =2ε |sin(πq log 3/log 2)|.

By rational approximation of the irrational ratio log 3/log 2, this residual tends to zero along an unbounded integer subsequence. Nevertheless every c_q has oscillation 2ε and sup-norm distance ε from the set of constant fields. Their derivatives have no common bound as q grows. Each produces the same kind of complete strictly descending Fisher-gradient example by substituting c_q for c in the energy integral. Thus even a small *global* residual in this log-odds field norm, without a common regularity or frequency bound, does not establish closeness to a universally covariant field. This is not a bound for finite-time flow residuals or another coordinate norm.

The inverses and compositions used in the proof follow mathematically from a globally valid identity on the same full domain. They do not authorize new source operations. If a source token is usable once, an audit is admissible only on some states, or an operation changes the objective, metric, labels, or another context field, this fixed-context closure argument is not automatically an applicable model. One must first establish the corresponding action and identities on the actual enlarged or restricted state space.

Repeated reweighting in this mathematical group does not make repeated evidence independently corroborative. Nothing here asserts that actual sources provide factors 2 and 3, warrant their repetitions, or satisfy the required global covariance identities.

## Bounded comparison and stopping point

Read received `Cross_Front_Theorems.md` §13 and `authorial-audit-flow-review-20261011/REVIEW.md` directly; targeted phrase checks additionally covered the received `Research_Review.md`, `Dot_Handoff.md`, `finite-audit-gradient-classification-20261010/RESULT.md`, and `posterior-gradient-descent-20261010/RESULT.md`. The periodic-field warning is inherited. The explicit factor-2/factor-3 certificate and complete nonlinear fixed-energy realization are not stated in those compared materials. This is a bounded comparison, not a corpus-wide novelty claim. The proofs above establish the mathematical claims without finite numerical testing.
