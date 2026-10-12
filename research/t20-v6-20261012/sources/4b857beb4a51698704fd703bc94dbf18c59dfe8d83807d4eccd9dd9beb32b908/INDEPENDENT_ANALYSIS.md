# Independent test: nonseparable normalized Bregman repair

Prepared before reading the author's report, 2026-10-09. This is mathematical review, not a claim of field novelty, formal proof certification, repository mutation, or T20 closure.

## Verdict on the candidate

The full-positive-cone classification is correct. C1 suffices for the classification. The C2 Hessian, divergence, radial flow, convergence, and finite-boundary score claims are correct with their stated extra assumptions. A strictly convex C2 function need not have positive-definite Hessian; inversion requires a separate assumption. There is also a separately provable open-box extension.

## 1. Classification and its exact assumptions

Write C=(0,infinity)^n, n>=2, Delta={p>0: sum p=1}. For differentiable strictly convex F:C->R, define D_F(x,b)=F(x)-F(b)-dF(b)[x-b]. Let N(b)=b/(sum b). Then the following are equivalent:

1. N(b) is the unique minimizer of x->D_F(x,b) on Delta, for every b in C.
2. With f=F|Delta, there is a unique differentiable a:(0,infinity)->R with a(1)=0 such that F(sp)=s f(p)+a(s).

Proof of necessity: the minimizer p at b=sp is interior relative to the affine simplex, so dF(sp)[v]=dF(p)[v] for every tangent v with sum v=0. Consequently d_p(F(sp)-s f(p))[v]=0. For fixed s this function is constant on connected Delta. Taking a(s)=F(su)-sF(u) for one fixed u in Delta proves the formula and regularity; a(1)=0 follows. Strict convexity is not needed for this necessary stationary-point argument.

Proof of sufficiency: writing b=tq and x=sp gives the divergence identity below; for x in Delta it reduces to D_f(p,q)+D_a(1,t). Restriction of strictly convex F to Delta makes f strictly convex, so D_f(p,q)>=0 with equality only for p=q. Thus q is the attained unique minimum despite Delta being open.

Canonicality: f=F|Delta fixes a uniquely. For an arbitrary chosen f one can move a term linear in s between sf and a; do not claim uniqueness without the canonical restriction.

## 2. Convexity is characterized exactly

For the displayed perspective-plus-radial representation, F is convex iff f and a are convex, and F is strictly convex iff f and a are strictly convex. Necessity follows by restriction to Delta and to a fixed ray, where subtracting s f(p) changes only an affine term. For sufficiency, take x=sp, y=tq and 0<lambda<1, set r=lambda s+(1-lambda)t, and apply convexity of f at weights lambda s/r and (1-lambda)t/r, then convexity of a at r. If s!=t, strictness of a makes the result strict; if s=t and x!=y, p!=q and strictness of f does so.

This does not identify strict convexity with Hessian positivity.

## 3. Divergence and Hessian identities

Use the relative derivative df(q) on the tangent space. For s,t>0 and p,q in Delta,

D_F(sp,tq) = s [f(p)-f(q)-df(q)[p-q]] + a(s)-a(t)-a'(t)(s-t)
             = s D_f(p,q)+D_a(s,t).

Indeed dF(tq)[sp-tq]=(f(q)+a'(t))(s-t)+s df(q)[p-q].

For C2 functions and h in R^n, set sigma=sum h and v=h-p sigma. At b=sp,

h^T H_F(sp) h = (1/s) D2 f(p)[v,v] + a''(s) sigma^2.

The map h -> (v,sigma) is an isomorphism between R^n and TDelta x R. Hence H_F(sp) is positive definite iff the tangent Hessian D2f(p) is positive definite and a''(s)>0. Polarization with h=p gives H_F(sp)p=a''(s) 1.

Negative control: f(p)=||p||^2/2 and a(s)=(s-1)^4 yield a smooth strictly convex F with normalized projection, but H_F is singular in the radial direction at s=1. An inverse-Hessian flow is undefined there without some separately specified extension.

## 4. Canonical inverse-Hessian dynamics

Assume F is C2 and H_F is positive definite everywhere. The specified field is

b_dot=-(s-1) H_F(b)^(-1) 1 = -(s-1) p/a''(s).

Thus p_dot=0 and s_dot=-(s-1)/a''(s). This is a forward-global unique flow for all initial b>0 and converges to N(b0). If s0=1 it is constant. Otherwise the solution stays strictly between s0 and 1. On that compact positive interval a'' is positive and continuous, so the field cannot escape or blow up. Separation of variables gives elapsed time = integral from s(t) to s0 of a''(r)/(r-1) dr for s0>1 (with the corresponding oriented expression when s0<1). Positivity and continuity at 1 make the integral diverge logarithmically at 1. The equilibrium is therefore approached only as t->infinity. Uniqueness away from 1 follows by separation; at 1 the locally bounded ratio 1/a''(s) gives a linear growth bound and uniqueness, without requiring C3.

The claim is forward-global, not complete in both time directions. With a''=1 and s0<1, the explicit backward solution reaches s=0 in finite negative time.

## 5. Boundary losses and strict improvement

If f has a finite continuous extension to the closed simplex, define F at its nonzero boundary points by the same perspective formula. In particular F(e_i)=f(e_i) is finite. No derivative at e_i is needed for D_F(e_i,b), because differentiation occurs at its second argument b>0. Then

D_F(e_i,sp)=D_f(e_i,p)+D_a(1,s),
D_F(e_i,sp)-D_F(e_i,p)=D_a(1,s)>0 when s!=1,
d/dt D_F(e_i,b(t))=-(s(t)-1)^2.

The same identity holds for every coherent first argument q in the closed simplex. The derivative follows from d_b D_F(e_i,b)[b_dot]=(b-e_i)^T H_F(b)b_dot. In fact this derivative identity holds for any C2 positive-definite F under the stated canonical field, provided F(e_i) is finite; it does not by itself establish normalization or radiality for other F.

A finite boundary assumption is essential for finite truth-state losses. The choice f(p)=-sum log p_i with any positive radial curvature gives normalized projection but divergent values at every vertex. No claim about such vertex losses is warranted. Continuity on the closed simplex is a sufficient condition, stronger than merely providing some usable finite first-argument values.

This is a geometric repair property, not evidence that a changed credence is empirically warranted or metaphysically correct.

## 6. Quadratic nonentropy example

Let F(b)=||b||^2/(2s)+s^2/2. Canonically f(p)=||p||^2/2+1/2 and a(s)=(s^2-s)/2. Its tangent Hessian is the identity and a''=1, so H_F is positive definite. Explicitly,

D_F(sp,tq)=(s/2)||p-q||^2+(1/2)(s-t)^2.

At coherent states this is the squared Euclidean/Brier geometry, not common-entropy geometry. The coherent loss D_F(e_i,p)=||e_i-p||^2/2 is finite. The flow is s(t)=1+(s0-1)e^(-t), p(t)=p0. The radial repair gain is (s0-1)^2/2 for every truth-state loss.

The example is genuinely nonseparable in b. For n=2 its mixed Hessian entry is 1-2b1*b2/s^3, not identically zero. It therefore does not contradict a theorem restricted to separable potentials.

## 7. Separate open-box extension

The classification also holds on B=(0,1)^n, with s in (0,n), and must be proved separately rather than inferred by extending F to the cone. For fixed s let U_s={p in Delta: s p_i<1 for every i}. This is nonempty, open, convex, and connected; it contains the barycenter u=(1/n,...,1/n) for every 0<s<n. The same stationary argument gives constancy of F(sp)-s f(p) on U_s. Defining a(s)=F(su)-sF(u) therefore gives the representation everywhere on B. Conversely the divergence proof gives the normalized projection because every N(b) belongs to Delta within B. Convexity and Hessian conclusions follow as above; radial a is tested on the barycentric ray. A forward normalization trajectory remains in B since it is the line segment between b0 and N(b0).

No extension to arbitrary star-shaped or disconnected radial-slice domains is asserted. Connectedness of the slices is doing real work.

## 8. Restricted-null-likelihood and orientation negative control

This section was added after root identified the restricted-null-likelihood scope issue and the author reported a cone-only reverse-projection bump. The box-compatible variant below was derived independently by this reviewer.

Global first-argument normalization is the hypothesis. Knowing only that P_F(cp)=p for coherent p and 0<c<=1 does not justify the classifier at masses above 1 once separability is removed. On the cone or open box in n=2 take

F*(b)=F0(b)+(b1+b2/2-1)_+^4,
F0(b)=||b||^2/(2s)+s^2/2.

The added term is C3 convex, and F0 has positive-definite Hessian, so F* is C3 with positive-definite Hessian. If s<=1, b1+b2/2<1; the perturbation and its gradient vanish both at b and at every coherent p. All such restricted null-likelihood rays therefore retain normalized first-argument projection.

At b=(9/10,4/5), which belongs to the open box, z=b1+b2/2-1=3/10. The perturbation's gradient difference is 2z^3=27/500. At N(b)=(9/17,8/17), the first-argument simplex stationarity residual in direction (1,-1) is consequently -27/500, not zero. The actual first-argument minimizer is (9/17+27/1000,8/17-27/1000), which is still interior and differs from N(b).

Moreover F*(q)=F0(q) and dF*(q)=dF0(q) for all q in Delta. Thus D_F*(b,q)=D_F0(b,q)+(b1+b2/2-1)_+^4; the added term is independent of q. Reverse projection min_q D_F*(b,q) continues to normalize for all b. Reverse normalization is therefore insufficient for the stated forward classifier.

If "smooth" is intended to mean C-infinity rather than C2/C3, replace u_+^4 by the C-infinity convex function r(u)=0 for u<=0 and r(u)=integral_0^u (u-v) exp(-1/v^2) dv for u>0. Then r''(u)=exp(-1/u^2)>0 for u>0, its derivatives glue flatly at zero, and the same vanishing/active-gradient argument applies.

## 9. Ancestry scope

The root's targeted primary-source note, nonseparable-repair-prior-check-20261009/NOTE.md, identifies Nock, Menon and Ong, "A scaled Bregman theorem with applications," NIPS 2016, Theorem 1 (affine-scale case), as an ancestor of the perspective-divergence identity. Adding the radial generator supplies the displayed split by linearity. This review proves and checks the mathematics directly; it does not independently certify bibliography completeness, theorem priority, or field novelty. The root's described source-reading limits remain in force.

Primary links recorded by the root:
- https://papers.neurips.cc/paper/6176-a-scaled-bregman-theorem-with-applications.pdf
- https://users.cecs.anu.edu.au/~rnock/docs/nips16-nmo-camera-ready-supplementary-material.pdf

Additional report-domain guard: finite continuous extension of f permits vertices as first arguments of the loss, while predictions remain in the positive cone (or the simplex interior). It does not, by itself, define gradients or Bregman losses with a vertex as the second argument. Any claim allowing boundary-valued reports needs its own convention and verification.

## 10. Coordinate-free transport (added on root request)

Let V be a finite-dimensional real vector space, C an open convex cone closed under multiplication by every positive scalar, and ell a linear functional strictly positive on C. Let B={p in C:ell(p)=1}. Then B is nonempty and connected, every b in C uniquely has b=s p with s=ell(b)>0 and p in B, and the same classification holds with tangent space ker ell. The convexity, divergence, and Hessian formulas become

D_F(sp,tq)=s D_f(p,q)+D_a(s,t),
H_F(sp)[h,h]=(1/s)D2f(p)[h-p ell(h),h-p ell(h)]+a''(s)ell(h)^2.

View H_F(b) intrinsically as a linear map V->V*; the correct field is

b_dot=-(ell(b)-1) H_F(b)^(-1) ell.

Since H_F(sp)p=a''(s)ell, the same global-forward radial convergence proof applies. No inner-product identification of ell is required, and B need not be bounded. This is a conditional finite-dimensional mathematical result.

For real symmetric or complex Hermitian positive-definite matrices, use their real vector space and ell=trace. The normalized base consists of positive-definite trace-one matrices. A valid quadratic example uses the Frobenius norm in the perspective term; the trace covector corresponds to the identity matrix only after choosing the usual trace inner product. This does not assert that arbitrary noetic tensors form this cone, does not derive a matrix Bayes update, and does not establish empirical or metaphysical warrant. Boundary matrices/pure states require the same separate finite-extension conditions for first-argument losses.
