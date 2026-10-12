# Scalar-output projectability for the inherited canonical Hessian nudge

9 October 2026. Ordinary mathematical research, not integration or closure. This note recovers actual inherited score geometry and derives one scoped continuation discriminator. It does not replace the current noetic inquiry calculus with a scalar loss.

## Result first

The inherited canonical correction
[
V_i(b)=\frac{1-\sum_j b_j}{f_i''(b_i)}
]
is a genuine negative gradient of the coherence objective under its declared Hessian form. Every truth-state Bregman loss has the same instantaneous derivative, namely minus the squared coherence defect.

Nevertheless, the scalar coherence coordinate (z=\sum_i b_i) determines its own original-clock projected velocity, and hence local scalar output while the full state remains admissible, **if and only if** the reciprocal curvatures have a common affine slope:
[
1/f_i''(t)=a t+c_i.
]
This equivalence holds on the open product domain with at least two coordinates and continuous positive curvatures. It does not say that the scalar coordinate determines the maximal admissible lifetime, a boundary-STOP event, or the stopped continuation. Section 5a gives an exact failure even when the iff passes. For one coordinate the classification does not apply: z is the whole state, so every reciprocal curvature projects. It is a specialization of classical vector-field projectability and the continuous Pexider functional equation, not a new general principle.

The already inherited normalized correction (V/S), where (S=\sum_i1/f_i''(b_i)), instead gives (z'=1-z) for every such score. Thus discarding (S) can preserve the path of correction while losing its original clock. A clock/resource contract is the discriminating missing operation. Pointwise normalized nudges were already proved; the continuation interpretation below is a new candidate application.

## 1. Actual inherited source and evidence

All remotely read sources were observed at read-only snapshot
`7efc6217c090b92d65f2c4cb8b011c18eb96bf7c` of `theislampill/orthemology`.
This is a source identity, not a current-main, adopted-theory or current-CI assertion.

Exact local copies and source URLs are in `SOURCES.json`. The source-store filenames are SHA-256 identities, and the local Lean copies were checked against them.

- `sources/SmoothScalar.lean`, lines 9–30, SHA-256 `e7c0be83410fe9bda9a983f8b82a65ec77cb8377e1e3e9880137dc6d83d2864f`.
- `sources/SmoothRigidity.lean`, lines 108–140 and 273 onward, SHA-256 `64c44e997e3986ae25042f3149f5c1f139c33f725b471ce2322fabccb6752493`.
- `sources/NudgeRigidity.lean`, lines 31–106, 151–169, 177–210, SHA-256 `50968a1703261df4e2794636cbdddca8e0e1a5867854a27e543bc83b0a9afc46`.
- `sources/CoherentNudgeRigidity.lean`, especially `single_score_coherent_nudges` and its `A,S,c,hdiff` construction, SHA-256 `229b7273ce75c5e119f18593fe95901e5b4f049ccd99fef9303bda3278080917`.
- `sources/NUDGE_REVIEW.md` preserves the independent ambient/coherent-nudge audit and the pointwise separator, SHA-256 `36bf84b786280660b3ec4a5e3a110f04d98598cdbe49e7680a438de344a0dd06`.
- `sources/FORMALIZATION_SCOPE.md` supplies the inherited exact/approximate/general-hull scopes.
- `sources/CORE_RECEIPT.json` reports a source-bound custom closure completed 2 October 2026, `FRESH_KERNEL_COMPONENTS`, exit 0, Lean 4.19.0, and standard axioms only for selected readbacks. It is evidence retained in the observed repository. No new Lean execution was performed here.

### Exact score signature

A scalar `Score` contains real functions (f,df,ddf), continuity of (f) on ([0,1]), first- and second-derivative witnesses on ((0,1)), and continuous strictly positive (ddf) there. There is no bounded-endpoint-derivative or global curvature-lower-bound premise.

For a finite coordinate family,
[
F(b)=\sum_i f_i(b_i),\qquad
D_F(v,b)=F(v)-F(b)-dF_b(v-b),
]
[
H_F(b)[u,w]=\sum_i f_i''(b_i)u_iw_i.
]
The source proves positive definiteness in the interior and the actual Fréchet derivative
[
d_bD_F(v,b)[d]=H_F(b)[b-v,d].
]

The formal generality supplies continuous positive-definite forms. For a smooth generator subclass these are literal smooth Riemannian metrics. Both concrete examples below lie in that smooth interior subclass. No manifold or smoothness claim about raw records is required.

### Inherited rigidity, not a future task

For two **fixed** coordinate-additive families on a categorical simplex with at least three outcomes, universal strict common nudges at arbitrarily small transverse perturbations of **every** interior coherent point are equivalent to one common positive scale and per-coordinate affine generator terms. Universal common coherent-endpoint repair and universal coherent-endpoint-directed nudging have that same classification.

The universal quantifier and fixed-family assumptions are essential. A nudge at a single input does not imply a common improving endpoint. The audited separator uses
(F=x_0^2+x_1^2+x_2^2), (G=x_0^2+2x_1^2+2x_2^2),
(b=(1/2,7/20,7/20)), and (d=(-13/10,-1,-1)).
All six derivatives are negative, even along a direction to a common interior coherent point, but no coherent endpoint weakly improves all losses for both scores.

## 2. Restricted negative-gradient interpretation

On (U=(0,1)^n), let
[
z(b)=\sum_i b_i,\quad E(b)=\frac12(z(b)-1)^2,\quad
q_i(t)=1/f_i''(t)>0,\quad S(b)=\sum_iq_i(b_i).
]

The metric-gradient equation gives
[
\operatorname{grad}_{H_F}E=(z-1)(q_i(b_i))_i,
]
so the inherited canonical nudge is exactly (V=-\operatorname{grad}_{H_F}E).

For each categorical truth (e_j), its actual derivative is
[
dD_F(e_j,b)[V]
 = (1-z)\sum_i(b_i-(e_j)_i)=-(z-1)^2.
]
This is the inherited `canonical_nudge_gain`, not a newly claimed theorem. Also
[
dE_b[V]=-(z-1)^2S(b),\qquad dz_b[V]=-(z-1)S(b).
]

Coherence error is the declared objective for this restricted subsystem. The identity does not make truth, warrant, source ownership, or noetic soundness into that objective.

## 3. Original-clock projected-velocity iff

### Statement

Let (n\ge2), and let (q_i:(0,1)\to(0,\infty)) be continuous. Define
[
V_i(b)=(1-z(b))q_i(b_i).
]
The following are equivalent:

1. There exists a scalar function (R:(0,n)\to\mathbb R) with (dz_b[V(b)]=R(z(b))) for every (b\in U).
2. There exists (M:(0,n)\to(0,\infty)) with (S(b)=M(z(b))) for every (b\in U).
3. There are real (a,c_1,\ldots,c_n) with (q_i(t)=at+c_i>0) on ((0,1)).

When these hold,
[
M(z)=az+\sum_i c_i,\qquad
R(z)=-(z-1)(az+\sum_i c_i).
]

The theorem is about the displayed vector-field projectability equation. It gives the scalar output evolution only on the interval where the full state remains in its declared domain. It does not identify different lifts’ maximal domain-valid intervals. The same argument holds on a product of nonempty open intervals, with the positivity and domains adjusted. A condition imposed only on a single coherent simplex, or only on a restricted family of perturbation paths, is weaker and is not being substituted for this full-product statement.

### Proof

(3\Rightarrow2\Rightarrow1) follows by summation.

For (1\Rightarrow2), two points on a common sum fibre (z\ne1) have equal (S), by dividing their equal projected velocities by (1-z). If two points have sum 1, add the same sufficiently small positive increment to their first coordinate. These perturbed points remain in the open cube and have equal sums different from 1. Continuity then gives equality of their original (S) values. Thus (S) is constant on every sum fibre and defines (M).

For (2\Rightarrow3), fix distinct indices (i,j), coordinate values (t,u), and a sufficiently small increment (delta) so that (t,t+delta,u,u-delta) remain in their intervals. Holding all other coordinates fixed and comparing equal-sum points gives
[
q_i(t+delta)-q_i(t)=q_j(u)-q_j(u-delta).
]
For each small (delta), this equality makes the increment independent of the admissible base point (t); exchanging indices gives the same increment function for every coordinate. Denote it (C(delta)). On a sufficiently small interval around zero, telescoping increments gives
(C(delta+eta)=C(delta)+C(eta)) whenever the three increments remain in that interval. Continuity of any (q_i) makes (C) continuous. The continuous local Cauchy equation therefore yields (C(delta)=adelta) for one common (a). Subdividing an arbitrary interval between two points into sufficiently small increments proves
(q_i(t)=at+c_i) throughout each coordinate interval.

This proof needs no third derivatives or differentiability of reciprocal curvature. With (C^1) reciprocals there is a shorter derivative proof, but that extra assumption is unnecessary.

### Relationship to existing rigidity

The earlier rigidity theorem compares **two generator families** through common all-state improvements. This theorem classifies the continuation sufficiency of **one summary for one selected vector field**, including its clock. These are different quantified properties.

For example (F) and (2F) satisfy inherited positive-affine equivalence for every admissible (F). They therefore pass the universal common-nudge/common-repair classification even when the scalar (z) fails the present original-clock closure criterion.

## 4. Exact separating controls

Use the common pair of points
[
b=(1/2,7/20,7/20),\qquad \tilde b=(2/5,2/5,2/5).
]
Both have (z=6/5), (E=1/50), and every canonical truth-state derivative equals (-1/25).

### A. Polynomial score

Take
[
f(t)=t^2/2+t^4/12,\qquad f''(t)=1+t^2.
]
This is finite and smooth on the closed interval, with positive curvature.

At (b), (S=5796/2245) and (z'=-5796/11225).
At (	ilde b), (S=75/29) and (z'=-15/29).
These are unequal exact rationals.

Thus equal coherence objective and equal immediate all-state score decrease do not determine even the first derivative of future coherence. This does **not** say that (z) retains the full current vector of state losses.

### B. Separable Bernoulli-entropy score

Take
[
f(t)=t\log t+(1-t)\log(1-t),
]
continuously extended by (f(0)=f(1)=0). On the interior,
[
f''(t)=1/[t(1-t)],\qquad q(t)=t(1-t).
]
The unbounded endpoint derivatives are allowed by the actual inherited Score signature.

At (b), (S=141/200) and (z'=-141/1000).
At (	ilde b), (S=18/25) and (z'=-18/125).
Again they are unequal, while the immediate all-state derivative remains (-1/25).

These are exact algebraic controls. They do not establish any empirical scoring or noetic application. The tests are executable in `scalar_closure_controls.py`; their success is not a kernel proof of the general iff.

## 5. The inherited normalized field changes the answer

The coherent-directed wrapper already constructs the pointwise direction
[
W=V/S.
]
Consequently
[
dz[W]=1-z,\qquad dD_F(e_j,b)[W]=-(z-1)^2/S(b).
]
So scalar coherence has the exact solution
(z(\tau)=1+(z(0)-1)e^{-\tau}) along this normalized field while its trajectory remains in the domain. This is a scalar-flow statement, not a guarantee that the full state remains in the domain for every time.

The original and normalized fields have the same oriented local integral curves because (S>0). Along an original-clock trajectory, the change of clock
[
d\tau/dt=S(b(t))
]
gives (db/d\tau=W). The scalar normalization discards the map from (	au) back to (t) unless the omitted mobility information can be recovered. Equal unparameterized paths are therefore insufficient for a task asking about time, resource use, deadlines, or intervention schedules.

Neither scaling is selected automatically by the universal nudge theorem. A proposed geometric continuation must declare which field is implemented and what its clock denotes.

## 5a. Scalar projectability does not preserve a boundary-STOP event

This exact control was identified during independent review. Take three quadratic coordinate generators, f_i(t)=t²/2, so q_i≡1. The reciprocal-curvature iff passes with a=0 and c_i=1. Let

    a=(1/100, 4/5, 4/5),
    b=(161/300, 161/300, 161/300).

Both lie in U=(0,1)^3 and have z(0)=161/100. Their formal scalar evolution is identical:

    z(t)=1+(61/100) exp(−3t).

Every coordinate is translated by the same amount:

    x_i(t)=x_i(0)−(61/300)(1−exp(−3t)).

For the first lift, a_1 reaches zero at

    t*=(1/3) log(61/58).

The other two coordinates then equal 79/100, so this is its first exit from the open cube. For the second lift,

    b_i(t)=1/3+(61/300) exp(−3t),

which remains strictly inside the cube for all t≥0. Consequently the current summaries consisting of (z, “currently admissible”) agree, as do their formal scalar trajectories, but their future boundary-STOP observations differ.

This is a domain-contract counterexample, not a failure of the iff or of the smooth polynomial flow outside the chosen domain. If a continuation question includes first exit, maximal admissible lifetime, or STOP, additional boundary-relevant state must be retained. Knowing only z and its projectable vector field is insufficient. The positive boundary-aware repair is a separate, explicitly declared summary contract.

## 6. Recommended next discriminating operation and stopping point

Bind a declared continuation observable and clock to the actual canonical nudge:

- Positive control: constant reciprocal curvatures, or (q_i(t)=at+c_i) with a common slope.
- Negative control: either exact pair above.
- Clock-change control: repeat with (W=V/S); scalar projected-velocity closure must become valid while original-time reconstruction remains an independent obligation.
- Boundary-STOP control: the quadratic pair in §5a must fail a claim that z alone preserves stopped continuation, despite passing the projected-velocity iff.
- Application contract: preserve the noetic route eligibility and transition witness separately. No admissibility follows merely from (V), (W), or a decreasing (E).

Stop after the selected projected-scalar-output question is settled and its exact separation documented, with boundary-STOP explicitly included or excluded by the continuation contract. A dual-coordinate full-state continuation or minimal-memory theorem is a distinct extension, not needed to establish this discriminator.

## Accounting

Inherited: Score assumptions, actual Bregman derivative, positive forms, canonical reciprocal-Hessian nudge, normalized coherent-directed construction, rigidity, and pointwise nudge/endpoint separator.

Classical ancestry: vector-field projectability, additive/Pexider functional equations, positive time reparameterization, and Hessian/mirror-flow coordinate changes.

Candidate contribution here: binding those mechanisms to the inherited correction selector; exact projected-scalar-velocity classification; explicit same-coherence/same-instantaneous-gain separating instances; and the mandatory clock and boundary-lifetime distinctions.

Targeted repository searches for `projectability`, `mobility`, `reciprocal curvature`, `nudge continuation`, `clock nudge`, and `reciprocal affine`, plus direct reads of the named sources, did not locate this particular scalar-continuation classification. Search results are not an exhaustive absence or novelty proof. No protected source, repository integration, owner adoption, or programme closure was changed.

