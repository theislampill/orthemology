# Exact admissibility of canonical Hessian correction

9 October 2026. Ordinary conditional mathematics extending the recovered source interface. No protected repository changes, integration, or closure. Earlier reports remain unchanged.

## Main conclusions

For the inherited canonical field, an exact dual-coordinate interval determines forward admissibility, including actual time to the domain boundary.

1. An interior coherent dual root gives a forward-global interior trajectory converging to that root.
2. Without that root, the maximal interior lifetime is exactly a one-dimensional travel-time integral.
3. A coherent boundary can be reached in finite time. Curvature may vanish at the boundary under the actual Score assumptions; coherence of the limiting state does not establish infinite-time arrival.
4. For n=2 every interior start converges to an interior coherent point. For every n≥2, all subcoherent starts do.
5. For n≥3, every interior start survives for all finite forward times if and only if every lower derivative endpoint f_i′(0+) is −∞. In that case all starts converge to interior coherent points.
6. For n≥3, combining all-start safety with original-clock scalar projectability selects exactly scaled convex negative-Shannon-entropy generators, up to coordinate-affine terms, for this canonical field.

The contribution is the source-bound admissibility and joint-compression classification. Inverse-function reduction, one-dimensional phase-line analysis, travel-time integration, barrier reasoning, and logistic solutions are classical ancestry. No general uniqueness claim about safe metrics or noetic inquiry follows.

## 1. Actual inherited assumptions

SmoothScalar.Score supplies f continuous on [0,1], an actual derivative df on (0,1), an actual derivative h=ddf of df on (0,1), and h continuous and strictly positive there. No bounded endpoint derivative or curvature lower bound is assumed.

Let n≥1 be a finite integer. For a family of n coordinate scores let

    F(b)=Σ_i f_i(b_i),        U=(0,1)^n,
    H(b)=diag(h_i(b_i)),      z(b)=Σ_i b_i,
    q_i(t)=1/h_i(t),
    V_i(b)=(1−z(b))q_i(b_i).

The source proves positive definiteness in U, the actual Bregman loss derivative H(b)[b−v,d], and the canonical all-truth-state derivative −(z−1)^2. V is exactly the negative H-gradient of E=(z−1)^2/2. Smooth generators give literal smooth Riemannian instances; the broader Score signature suffices below without an added third derivative.

The inspected files are SmoothScalar.lean, SmoothRigidity.lean, NudgeRigidity.lean, and CoherentNudgeRigidity.lean under ../hessian-frontier-recovery-20261009/sources. SOURCE_BINDINGS.json binds the exact paths and SHA-256s to observed read-only GitHub snapshot 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c. Source identity is not adoption or current-main status. No new Lean execution is claimed.

## 2. Exact dual interval and unique local dynamics

Fix b⁰∈U. Define

    α_i=df_i(b⁰_i),
    ℓ_i=lim_(x↓0)df_i(x),       u_i=lim_(x↑1)df_i(x).

Since h_i>0, df_i is strictly increasing. Its image is the open interval I_i=(ℓ_i,u_i), allowing ℓ_i=−∞ and u_i=+∞. Its inverse φ_i:I_i→(0,1) is C¹, with

    φ_i′(y)=1/h_i(φ_i(y))>0.

Define the maximal common dual-shift interval

    J=⋂_i(I_i−α_i)=(L,R),
    L=max_i(ℓ_i−α_i),          R=min_i(u_i−α_i).

Then L<0<R. Put

    Z(λ)=Σ_i φ_i(α_i+λ),       λ∈J.
    Z′(λ)=Σ_i q_i(φ_i(α_i+λ))>0.

The canonical flow is exactly

    λ′=1−Z(λ),                λ(0)=0,
    b_i(t)=φ_i(α_i+λ(t)).

Proof: y_i=df_i(b_i) satisfies y_i′=h_i(b_i)b_i′=1−z, so every y_i−α_i equals a common λ. Conversely the inverse-function derivative reconstructs V from the scalar equation.

The transformed field is C¹. Its initial-value problem has a unique maximal solution, and the inverse transformation gives a unique maximal solution of the original field. Thus local Lipschitzness of V in b coordinates was not smuggled into the merely continuous-curvature assumptions.

Let Z_L and Z_R be the one-sided limits of Z at L and R. They exist in [0,n].

## 3. Interior-root and maximal-lifetime theorem

### Interior root

There is an interior coherent point on the dual orbit exactly when

    Z_L<1<Z_R.

It is unique. Write Z(λ*)=1.

If Z(0)=1, the state is stationary. Otherwise λ moves monotonically toward λ*. The full state remains in the coordinate rectangle between b⁰ and b*=φ(α+λ*), a compact subset of U. It exists for every t≥0 and converges to b*.

A nonstationary solution cannot reach an interior root in finite time: Z is C¹ with 0<Z′(λ*)<∞, so |1−Z(λ)| is asymptotic to Z′(λ*)|λ−λ*|. The travel-time integral diverges logarithmically. Uniqueness at an equilibrium gives the same conclusion.

### No root in the direction of travel

If Z(0)>1 and Z_L≥1, the solution moves left and approaches L. Its maximal interior lifetime is

    T=∫_L^0 dλ/(Z(λ)−1),      possibly +∞.

If Z(0)<1 and Z_R≤1, it moves right and approaches R. Its maximal lifetime is

    T=∫_0^R dλ/(1−Z(λ)).

These formulas classify both finite and infinite endpoint arrival. A finite T means continuous completion reaches the boundary at T and the open-domain flow must stop. T=∞ means every finite-time state remains interior, although the limiting state can lie on the boundary.

Proof: where 1−Z has fixed nonzero sign, separation of variables produces a strictly increasing travel-time map. Its inverse constructs the unique solution until the endpoint. A finite limiting point inside J with nonzero velocity would permit continuation. Therefore the endpoint and time integral are exact, not merely bounds.

The scalar classification is stated generally; the following cube geometry eliminates its upper failure case when n≥2.

## 4. Consequences for the actual open cube

Assume n≥2.

### No upper-directed failure

Always Z_R>1. If R is finite, at least one coordinate tends to 1, while every other coordinate remains at least its strictly positive initial value along increasing λ. If R=+∞, all upper derivative endpoints are +∞ and all coordinates tend to 1, giving Z_R=n>1.

Every initial state with z(b⁰)<1 therefore has an interior coherent root, stays in U for every t≥0, and converges to that root.

### Lower-directed failures

Only z(b⁰)>1 and Z_L≥1 can fail to have a root.

Then L is finite: L=−∞ would require every lower derivative endpoint to be −∞, making all coordinates tend to zero and Z_L=0.

At finite L at least one coordinate tends to zero. Denote the boundary limit by c∈[0,1)^n.

If Z_L=Σc_i>1, exit is necessarily finite:

    (−L)/(Z(0)−1) ≤ T ≤ (−L)/(Z_L−1) < ∞.

If Z_L=1, c is coherent, but either T<∞ or T=∞ is possible. The exact distinction is the improper integral ∫_L^0 dλ/(Z(λ)−1).

A useful sufficient condition for infinite arrival is bounded Z′ near L. Then Z(λ)−1≤M(λ−L), forcing logarithmic divergence of the time integral. The source does not impose this bound. Unbounded Z′ alone is not asserted sufficient for finite arrival.

### Two coordinates

For n=2 every interior start has an interior coherent root. At a finite lower endpoint, one coordinate is zero and the other is strictly below its initial value, hence below 1. Thus Z_L<1. At L=−∞ it is zero. Combine this with Z_R>1.

For n=1 no coherent point lies in U=(0,1); the two-coordinate corollary and subsequent all-start classification do not cover it.

## 5. Exact coherent-boundary controls

### Finite arrival under the inherited Score assumptions

Take

    f₁(t)=t³/6,             h₁(t)=t,
    f₂(t)=f₃(t)=t²/2,      h₂(t)=h₃(t)=1,
    b⁰=(1/2,5/8,5/8).

These generators are continuous on [0,1], with strictly positive continuous curvature on (0,1). h₁ tends to zero at the excluded boundary, as the actual assumptions permit.

The initial dual coordinates are α=(1/8,5/8,5/8) and L=−1/8. Let u=λ+1/8. Then

    b₁=√(2u)=x,            b₂=b₃=1/2+u=1/2+x²/2,
    Z(λ)=1+x+x².

While x>0, u′=−x−x² and u=x²/2 give

    x′=−1−x,               x(t)=(3/2)e^(−t)−1.

The maximal interior lifetime is exactly T=log(3/2). The first coordinate reaches zero and the others tend to 1/2. This is the first domain exit. Equivalently,

    T=∫_0^(1/8) du/(√(2u)+2u)
      =∫_0^(1/2) dx/(1+x)
      =log(3/2).

The limit (0,1/2,1/2) is coherent but outside U, and H degenerates there. This refutes the inference from boundary coherence to infinite arrival time without contradicting uniqueness at an interior equilibrium.

### Infinite arrival to the same coherent boundary

Take all f_i(t)=t²/2 and b⁰=(1/4,3/4,3/4). Writing

    b(t)=(x(t),1/2+x(t),1/2+x(t))

gives x′=−3x, hence x(t)=(1/4)e^(−3t). All finite-time states remain inside U, while the limit is again (0,1/2,1/2). The time integral is infinite.

Both examples have initial z=7/4 and the same coherent boundary limit, but opposite finite-lifetime outcomes.

## 6. All-start interior-safety classification

Fix the Score family and assume n≥3. The following are equivalent:

A. Every b⁰∈U has a solution that stays in U for every finite forward time.
B. Every b⁰∈U has a forward-global solution converging to an interior coherent point.
C. Every lower derivative endpoint is −∞:

       lim_(t↓0)df_i(t)=−∞ for every i.

B⇒A is immediate.

For C⇒B, every common lower endpoint is L=−∞, so Z_L=0. Section 4 gives Z_R>1. The interior-root theorem applies to every initial state.

For A⇒C, argue contrapositively. Suppose ℓ_i is finite. Choose fixed r_j∈(0,1), j≠i, with Σ_(j≠i)r_j>1, possible because n−1≥2. Set b⁰_j=r_j and choose b⁰_i increasingly close to zero.

The available negative dual shift in coordinate i is δ=df_i(b⁰_i)−ℓ_i→0. For sufficiently small δ, the other dual coordinates remain interior after shift −δ. Coordinate i therefore determines L=−δ. The other coordinates at that endpoint approach r_j as δ↓0, so their sum stays greater than 1 for sufficiently small δ. Thus Z_L>1 and the trajectory exits in finite time, contradicting A.

This constructs a failure for the fixed family whenever a lower derivative endpoint is finite. It is not a claim that all starts then fail. The n≥3 restriction is essential: two coordinates are always safe.

No upper derivative barrier is required. A subcoherent trajectory reaches coherence before an upper boundary could be hit.

## 7. Joint scalar-compression and all-start-safety classification

The earlier, separately qualified scalar report proves, for continuous positive reciprocals on the full product and n≥2:

    z′ depends only on z for every b∈U
    iff q_i(t)=a t+c_i with one common slope a.

This statement is original-clock projected-velocity closure. It does not on its own preserve stopped trajectories. Its ancestry is vector-field projectability and the continuous Pexider equation.

For n≥3, this scalar property and all-start safety hold jointly exactly when

    q_i(t)=a t for every i, for one common a>0,

equivalently

    f_i(t)=(t log t)/a + β_i t + γ_i,

where t log t is continuously extended by zero at t=0.

Proof: positivity of at+c_i on (0,1) forces c_i≥0. If c_i>0, h_i=1/(at+c_i) is bounded near zero, making the lower derivative endpoint finite. The all-start criterion therefore forces c_i=0 for every i, and positivity forces a>0. Conversely q_i=at makes df_i=(log t)/a plus a constant, giving the required lower barriers. Integrating yields the stated generators.

For this exact class,

    b_i′=a(1−z)b_i,
    z′=a z(1−z),
    b_i(t)/z(t)=b⁰_i/z(0),
    z(t)=z(0)/[z(0)+(1−z(0))e^(−at)].

All coordinates remain interior for t≥0. If z(0)>1, they decrease to b⁰_i/z(0)<1. If z(0)<1, they increase to those normalized coordinates, each strictly below 1 because n≥2 and all initial coordinates are positive. Thus the coherent limit is b⁰/z(0).

This is a fixed-selector, fixed-clock joint classification. It does not say negative Shannon entropy is the unique safe geometry: Bernoulli entropy has the lower barriers and is safe, but generally fails scalar original-clock autonomy. It does not exclude safe guarded controllers, different summaries, or other vector fields.

## 8. Normalization changes boundary timing

The inherited normalized direction is W=V/S, where S(b)=Σ_iq_i(b_i)>0. Along an original-clock trajectory define

    τ(t)=∫_0^t S(b(s)) ds.

Then db/dτ=W. For the positive residual r(t)=z(t)−1 in a lower-directed boundary case,

    r′=−rS,                 τ(t)=log(r(0)/r(t)).

If the boundary residual is zero, τ→∞. This remains true when the original boundary time T is finite, as in the cubic/quadratic example. The same oriented path therefore reaches its boundary in finite original time but only asymptotically in normalized time.

If the limiting boundary residual is positive, the total normalized time is instead finite:

    τ_exit=log(r(0)/(Z_L−1)).

This explains why an unqualified “the correction path is unchanged” does not preserve time-sensitive STOP semantics. Normalization changes the clock; it does not move the limiting boundary point into the interior.

## 9. Assurance and stopping boundary

The result is an ordinary proof grounded in the exact Score signature. controls.py verifies finite exact algebraic identities in the coherent-boundary examples and entropy-class flow. These checks are not a kernel proof of the analytic theorems.

The theorem settles the open-cube admissibility question for this canonical field. Additional noetic guards, route witnesses, source changes, action costs, resets, or evidence acquisition require separate transition contracts. None is inferred from H or E. No additional general minimal-memory theorem is claimed.

Earlier frozen reports and their review were not changed. Any review of this supplement is a separate evidence event.

