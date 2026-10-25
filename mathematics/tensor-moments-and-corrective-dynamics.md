# Tensor moments and corrective dynamics

## Abstract

A tensor of expectations can describe a state without determining how that state will respond to a later intervention. This chapter develops the exact boundary between those two tasks for Fisher gradient flows and polynomial reweighting of probability laws. On a known finite numerical support, interpolation gives an exact finite closure of the tensor hierarchy. On compact supports, all moments determine the law; on unbounded supports, even the complete moment record and every derivative at the initial time can leave the future undetermined.

The central existence results start from polynomial functionals rather than presumed probability laws. For autonomous coercive polynomial energies, the full hierarchy and positivity on every polynomial square force an actual normalized exponential tilt. Signed energies require a different hypothesis on the initial weighted energy distributions. Time-dependent sums of squares admit a cumulative coercivity theorem, including rates that are rank one at every instant. With a fixed controlled subspace, zero hidden coordinates give automatic existence and identification, one hidden coordinate gives existence with possible ambiguity, and two or more permit strictly square-positive paths that cease to represent any law immediately after a genuinely valid initial state. Complete proofs, counterexamples, effective recovery under explicit promises, and finite diagnostic limits are developed together.

This is a public mathematical exposition. It preserves the accepted editions of the established Orthemology papers and makes no adoption or priority claim. In particular, a moment hierarchy on a fixed numerical state space does not complete the unfinished programme of an original n-person noetic field. The constructive results here supply conditional mathematical components; their application to cognition, normativity, or a field of persons requires separate scientific arguments.

## 1. States, records, and actual operations

Let $`\mathcal P_\infty(\mathbb R^d)`$ denote the Borel probability measures having every absolute polynomial moment, with $`1\le d<\infty`$. A law $`\mu`$ defines the real linear functional

```math
L_\mu(p)=\int_{\mathbb R^d}p(x)\,d\mu(x),
\qquad p\in\mathbb R[x_1,\ldots,x_d].
```

Its full moment record consists of all numbers $`L_\mu(x^\alpha)`$, equivalently all symmetric tensors $`M_r=\int x^{\otimes r}\,d\mu`$. The coordinate dimension is finite; the set of tensor grades is infinite. The record belongs to a product of finite-dimensional tensor spaces. It is generally not an element of their algebraic direct sum, whose elements have only finitely many nonzero grades.

A real polynomial functional $`L`$ is normalized when $`L(1)=1`$. Independently of normalization, it is **square-positive** when $`L(q^2)\ge0`$ for every real polynomial $`q`$. Equivalently, every finite polynomial Gram matrix $`(L(p_i p_j))_{i,j}`$ is positive semidefinite. Positive scalar multiples preserve square positivity. All hierarchy records in this chapter are normalized; their unnormalized intermediate functionals retain square positivity without being required to have mass one.

Square positivity and nonnegativity of individual monomial coordinates are different conditions on a real polynomial algebra; neither implies the other in general. On $`\mathbb R[x]`$, evaluation at $`-1`$ is square-positive because $`L(q^2)=q(-1)^2\ge0`$, although $`L(x)=-1`$. Conversely, the normalized functional specified by $`m_0=m_1=1`$ and $`m_r=0`$ for $`r\ge2`$ has no negative monomial coordinate, but $`L((1-x)^2)=1-2+0=-1`$. Square positivity imposes cross-moment consistency that individual sign checks miss, while allowing negative odd moments on a real state space. It is necessary for a positive representing measure, but in several variables it is not sufficient, as the explicit construction in §9.1 will show.

A polynomial is a **sum of squares**, abbreviated SOS, if it is a finite sum of real polynomial squares. Square positivity allows evaluation of an SOS as nonnegative; it does not allow that inference for every pointwise nonnegative polynomial.

Three questions must therefore be separated:

1. **Existence:** does a proposed record have a probability representative?
2. **Identification:** is that representative unique within the declared state space?
3. **Continuation:** do all representatives produce the same declared later observations under the admitted operations?

For a real energy $`h`$, the actual reweighting operation, whenever all required integrals exist, is

```math
\mathcal T_t^h\mu(dx)
  =\frac{e^{-t h(x)}}{Z_\mu(t)}\,\mu(dx),
\qquad
Z_\mu(t)=\int e^{-t h}\,d\mu>0.
```

For a supplied time-dependent energy $`h_t`$, replace $`t h`$ by $`H_t=\int_0^t h_s\,ds`$. Adding a scalar depending only on time does not change the normalized law. A likelihood that depends on an unobserved coordinate is a different operation from one that acts only on the observed coordinates.

A **coordinatewise $`C^1`$ hierarchy** means that every polynomial coordinate is continuous on $`[0,T)`$, continuously differentiable in the interior, and has its continuous right derivative at zero. It does not assume a norm on the infinite sequence, a uniform bound in the degree, or a Banach-space uniqueness theorem. For autonomous polynomial energy the hierarchy is

```math
\frac{d}{dt}L_t(p)
 =-L_t(hp)+L_t(h)L_t(p),
\qquad p\in\mathbb R[x_1,\ldots,x_d].
\quad\text{(1)}\quad
```

The finite sum defining $`hp`$ makes every equation meaningful. Whether a solution of these equations is an actual law-level evolution is a theorem to prove, not a definition to smuggle in.

The background measure results used below are classical: one-dimensional Hamburger and Stieltjes existence, Carleman determinacy, the multivariate Carleman existence theorem, the compact algebraic-set moment theorem, and Haviland's representation theorem. Their precise roles are cited at the point of use. Most of the chapter consists of direct arguments linking those results to the specified dynamics.

## 2. Finite channels: exact tensor closure and its limits

### 2.1 Fisher gradient descent produces a moment hierarchy

Let $`K`$ be an $`m\times n`$ column-stochastic matrix, with nonnegative entries and columns $`k_i\in\Delta_m`$. Zero rows are permitted. Let $`p`$ lie in the interior of the fine probability simplex, put $`q=Kp`$, and use the Fisher metric

```math
\langle a,b\rangle_p=\sum_{i=1}^n\frac{a_i b_i}{p_i},
\qquad
\sum_i a_i=\sum_i b_i=0.
```

For a fixed covector $`g\in\mathbb R^m`$, consider $`J_g(p)=g\cdot Kp`$. Its negative gradient is

```math
\dot p_i=-p_i\bigl(g\cdot k_i-g\cdot q\bigr).
\quad\text{(2)}\quad
```

Indeed, the displayed vector has zero sum and its Fisher pairing with every tangent vector $`a`$ is $`-\sum_i(g\cdot k_i)a_i=-dJ_g(a)`$. This verifies the constrained gradient directly. The Fisher–Shahshahani interpretation of replicator dynamics is classical; see [Harper](#references). The present concern is what a coarse record retains about that dynamics.

Collect identical columns into the distinct numerical support points $`\kappa_1,\ldots,\kappa_N`$, and let $`w_j`$ be the total fine mass of the corresponding class. Equation (2) preserves ratios inside each class and induces

```math
\dot w_j=-w_j(g\cdot\kappa_j-g\cdot q),
\qquad
q=\sum_jw_j\kappa_j.
```

Every strictly positive aggregate vector is realized by a strictly positive fine law. This aggregation concerns the specified numerical channel and controls. It does not identify source tokens, provenance, or fine labels for a later operation that distinguishes them.

Define $`M_0=1`$ and $`M_r=\sum_jw_j\kappa_j^{\otimes r}`$. Let $`\iota_g`$ contract exactly one tensor slot with $`g`$. Differentiating gives

```math
\dot M_r=-\iota_gM_{r+1}+(g\cdot M_1)M_r,
\qquad
\dot q=-(M_2-qq^{\mathsf T})g.
\quad\text{(3)}\quad
```

There is no factor $`r+1`$ in this contraction convention. Symmetry here reflects repeated numerical coordinates in a product; it does not symmetrize distinct semantic roles. Since contracting every slot with the all-ones vector gives one, all tensor grades are nonzero even for this finite support.

### 2.2 Exact finite closure on known support

**Theorem 1 (known-support closure).** For fixed distinct support points $`\kappa_1,\ldots,\kappa_N`$, moments through degree $`N-1`$ determine the aggregate law. Every higher moment is a fixed linear function of those moments, so (3) has an exact finite closure on its admissible moment image.

**Proof.** Choose $`v\in\mathbb R^m`$ outside the finitely many hyperplanes $`v\cdot(\kappa_i-\kappa_j)=0`$. Then $`a_j=v\cdot\kappa_j`$ are distinct. The contractions $`s_r=\langle v^{\otimes r},M_r\rangle=\sum_jw_j a_j^r`$ are available for $`0\le r<N`$. Write the Lagrange polynomials as

```math
\ell_j(z)=\prod_{\ell\ne j}\frac{z-a_\ell}{a_j-a_\ell}
        =\sum_{r=0}^{N-1}c_{jr}z^r.
```

Their values on the support are Kronecker deltas, hence $`w_j=\sum_r c_{jr}s_r`$. Therefore, for every degree $`k`$,

```math
M_k=\sum_{r=0}^{N-1}
       \left(\sum_{j=1}^N c_{jr}\kappa_j^{\otimes k}\right)s_r.
\quad\text{(4)}\quad
```

In particular, this replaces the top missing grade in (3). The resulting system is conjugate to the aggregate equation on the image of the positive simplex. Arbitrary tensor tuples outside that image are not admitted states. For $`N=1`$, the known support and degree-zero mass already determine the stationary law. ∎

For rational support points, a separating vector can be found by a finite exact search. Use $`v(t)=(1,t,\ldots,t^{m-1})`$. Each pair contributes a nonzero polynomial with at most $`m-1`$ roots. Some integer among $`0,\ldots,(m-1)N(N-1)/2`$ therefore separates all points. Arbitrary real support descriptions do not automatically give an effective equality test. Nor does exact interpolation imply stability: nearby projected support values can make its coefficients poorly conditioned.

The cutoff is sharp in the worst case within this family of moment records. Place $`N`$ distinct points on the line $`\kappa_j=(x_j,1-x_j)`$. The equations $`\sum_jh_jx_j^r=0`$ for $`0\le r\le N-2`$ have a nonzero solution $`h`$. The full Vandermonde matrix implies $`\sum_jh_jx_j^{N-1}\ne0`$. Small positive and negative perturbations of uniform weights in direction $`h`$ are positive laws with equal lower moments and different next moments. This is not a lower bound on every conceivable state encoding. The original weights themselves are already a finite encoding.

### 2.3 Exact continuation and a single discriminating experiment

For a locally finite piecewise-constant control $`g(t)`$, put $`U(t)=\int_0^t g(s)\,ds`$. Integration of the logarithmic weight ratios gives

```math
w_j(t)=
\frac{w_j(0)e^{-U(t)\cdot\kappa_j}}
     {\sum_\ell w_\ell(0)e^{-U(t)\cdot\kappa_\ell}},
\qquad
\mathcal T_a\mathcal T_b=\mathcal T_{a+b}.
\quad\text{(5)}\quad
```

Finite cumulative controls preserve strictly positive weights. The endpoint depends on the cumulative covector, although the intervening observation history can depend on the schedule. A scalar component parallel to the all-ones vector is a normalization gauge.

**Theorem 2 (finite continuation equivalence).** For two aggregate laws on the same known finite support, the following are equivalent: equality of the weights; equality of all coarse histories under all admitted controls; equality under all constant controls; equality of the scalar response $`v\cdot q(t)`$ under one separating constant control $`g=v`$ on an initial interval of positive length; and equality of the moment record through degree $`N-1`$.

**Proof.** All implications from equal weights, and the moment implication, follow from (4)–(5). For the single-control implication let $`z_w(t)=\sum_jw_je^{-ta_j}`$. Then $`v\cdot q(t)=-(\log z_w)'(t)`$. Equal responses and $`z_w(0)=1`$ give equal normalizers on the interval. Their derivatives at zero through order $`N-1`$ give equal projected moments, and the Vandermonde matrix gives equal weights. ∎

The observation in this theorem is an exact function on an interval. It is not a finite sampled experiment or a noise-robust reconstruction procedure. With a nonlinear objective $`J(q)`$, one may substitute $`g=\nabla J(q)`$ when the usual finite-dimensional uniqueness hypotheses hold; a single fixed objective need not distinguish states. A constant objective distinguishes none.

### 2.4 When does the first moment suffice?

**Theorem 3 (coarse closure).** The vector field for $`q`$ in (3) depends only on $`q`$, for every covector $`g`$, exactly when the distinct support points are affinely independent.

**Proof.** Affine independence makes $`w\mapsto q`$ injective, so sufficiency is immediate. Conversely, form the matrix with columns $`(1,\kappa_j)`$, and let $`V`$ be its row space, viewed as functions on the support. A kernel vector $`h`$ can be used for small positive perturbations of any interior law. Equal first moments and equal coarse vector fields for all $`g`$ imply $`\sum_jh_j\kappa_j\kappa_j^{\mathsf T}=0`$. Thus every product of two coordinate functions lies in $`V`$, the annihilator of that kernel. Since $`V`$ is spanned by one and the coordinate functions, it is closed under products. A separating linear function belongs to $`V`$; its Lagrange polynomials give every point indicator. Therefore $`V=\mathbb R^N`$, and the matrix has column rank $`N`$. ∎

This is a criterion for descent of the specified vector field. It does not assert equality of an induced coarse metric with a chosen canonical Fisher metric.

Two examples show why the distinction matters. With columns $`(1,0),(0,1),(1/2,1/2)`$, weights $`(1/4,1/4,1/2)`$ and $`(3/8,3/8,1/4)`$ share $`q=(1/2,1/2)`$, but their second tensors are

```math
\begin{pmatrix}3/8&1/8\\1/8&3/8\end{pmatrix},
\qquad
\begin{pmatrix}7/16&1/16\\1/16&7/16\end{pmatrix}.
```

For $`g=(1,0)`$, their velocities are $`(-1/8,1/8)`$ and $`(-3/16,3/16)`$. On the same three-point support, writing $`Q=E[X]`$, $`S=E[X^2]`$, and $`\lambda=g_1-g_2`$ gives the exact closure

```math
\dot Q=-\lambda(S-Q^2),\qquad
\dot S=-\lambda\bigl((3/2-Q)S-Q/2\bigr).
```

The admissible weights at $`1,1/2,0`$ are respectively $`2S-Q`$, $`4(Q-S)`$, and $`1-3Q+2S`$, all positive. On four points $`0,1/3,2/3,1`$, the weights $`(5,9,3,7)/24`$ and $`(7,3,9,5)/24`$ instead share both first and second moments. Their third moments differ by $`1/54`$, and under unit linear damping their second mean derivatives differ by that amount, since $`Q''=E[X^3]-3QS+2Q^3`$. Equality of an immediate velocity is weaker than equality of a future trajectory. These finite results incorporate [the finite-channel proof][finite-source].

## 3. Complete records on compact and unbounded spaces

### 3.1 Compactness and the absence of a universal finite cutoff

**Proposition 4 (compact numerical states).** On a fixed compact subset $`K\subset\mathbb R^d`$, the full polynomial record determines the law. It consequently determines every normalized linear exponential tilt.

**Proof.** Coordinate polynomials contain constants and separate points. Their algebra is uniformly dense in $`C(K)`$ by Stone–Weierstrass. Equal polynomial integrals therefore give equal continuous integrals and equal finite Borel measures. The exponential of any linear functional is bounded above and below on $`K`$, so the tilt is well defined. Alternatively, expand the exponential uniformly: if $`|x|\le B`$, the absolute series is bounded by $`e^{|u|B}`$, with another factor $`B`$ for the mean numerator. ∎

This applies to the aggregate distribution of any measurable map into a fixed finite-output simplex, even if there are infinitely many underlying source states. It does not recover distinctions lost by that map.

There is no universal finite degree on arbitrary compact supports. For any proposed cutoff $`D`$, choose $`D+2`$ distinct collinear points and perturb positive weights along the kernel of the truncated Vandermonde matrix, as in Theorem 1. Full compact determination and finite known-support closure are different statements. A single generic projection also need not identify an arbitrary multivariate compact law.

### 3.2 Actual half-line evolution

For $`\mu\in\mathcal P_\infty([0,\infty))`$, set

```math
A_r(t)=\int x^r e^{-tx}\,d\mu(x),\quad
Z(t)=A_0(t),\quad
m_r(t)=\frac{A_r(t)}{Z(t)},\quad t\ge0.
\quad\text{(6)}\quad
```

Every integral is finite and $`Z(t)>0`$. Dominated differentiation, including the right boundary derivative, gives $`A_r^{(k)}=(-1)^kA_{r+k}`$ and

```math
m_r'=-m_{r+1}+m_1m_r,\qquad
m_1'=-\mathrm{Var}_{\mathcal T_t\mu}(X).
\quad\text{(7)}\quad
```

At zero, the bound $`|(e^{-ux}-1)/u|\le x`$ justifies the first derivative; higher moments give the rest. The actual laws obey the semigroup rule and have exactly the same null sets as their initial law at every finite time.

In score coordinates, the Fisher pairing is $`E_\mu[ab]`$ for mean-zero square-integrable scores. The mean functional has gradient score $`X-E_\mu X`$, so (7) is its negative gradient trajectory, with squared speed equal to the variance. This does not make all positive densities an open Hilbert manifold or make every $`L^2`$ direction a positive two-sided perturbation.

Within a law-level class of positive densities relative to $`\mu`$, with almost-everywhere absolutely continuous log density satisfying $`\partial_t\log f_t=-(x-q(t))`$ and locally integrable $`q`$, integration and normalization force (6). That uniqueness statement is about the specified densities. It does not by itself classify arbitrary infinite moment sequences solving (7).

### 3.3 A full-moment ambiguity with different continuations

Let $`f(x)=e^{-(\log x)^2/2}/(x\sqrt{2\pi})`$ on $`x>0`$, and define

```math
d\mu_\pm(x)=f(x)
 \left(1\pm\frac12\sin(2\pi\log x)\right)\,dx.
\quad\text{(8)}\quad
```

These are distinct positive probabilities. For every integer $`n\ge0`$,

```math
E[e^{nZ}\sin(2\pi Z)]
  =e^{n^2/2-2\pi^2}\sin(2\pi n)=0,
\qquad Z\sim N(0,1).
```

Thus both have moments $`e^{n^2/2}`$. This is a classical lognormal Stieltjes-class mechanism, not a new discovery; see [Schmüdgen's moment lectures](#references), §2.1. For a general lognormal $`\log X\sim N(a,\sigma^2)`$, the phase must be $`2\pi(\log X-a)/\sigma^2`$ for the same integer cancellation.

**Proposition 5 (equal records, distinct dynamics).** The laws (8) have the same full initial moment sequence and every finite initial derivative of (7), but different full moment records at every positive time. Their means differ somewhere in every open positive-time interval.

**Proof.** First, a finite measure on $`[0,\infty)`$ is determined by its Laplace transform. Push it forward by $`y=e^{-x}`$ onto $`(0,1]`$, assign zero mass to zero, and observe that Laplace values at positive integers give its polynomial moments. The total mass and polynomial approximation on $`[0,1]`$ identify the pushforward, hence the original law.

Laplace transforms are analytic on $`\mathrm{Re}\,t>0`$. If the means of two tilted laws coincide on an open interval, the logarithmic derivatives of their normalizers coincide there. Analytic continuation makes those normalizers proportional on the positive half-line; their limits one at zero remove the factor. Laplace uniqueness would identify the original laws, contradicting (8).

At positive time $`t`$, a tilted law has the exponential moment $`E_{\mathcal T_t\mu}e^{tX/2}=Z(t/2)/Z(t)<\infty`$. Such a law is moment-determinate: any competitor inherits the exponential moment from its nonnegative series, its convergent moment expansion identifies the Laplace transform near zero, and uniqueness finishes the argument. Equality of the full tilted records at one positive time would thus give equal tilted laws. Multiplying by $`e^{tx}`$ and normalizing recovers equal initial laws, again a contradiction.

Finally, repeatedly differentiating (7) expresses every finite coordinate derivative at zero in finitely many initial moments. Hence all those derivatives agree. The initial mean and its first two derivatives are $`e^{1/2}`$, $`e-e^2`$, and $`e^{9/2}-3e^{5/2}+2e^{3/2}`$. The difference of the mean curves is flat at zero while failing to vanish on any positive interval. ∎

The formal series for the normalizer has terms $`(-t)^n e^{n^2/2}/n!`$. Their absolute ratio is $`|t|e^{n+1/2}/(n+1)`$, so its radius of convergence is zero. Positive-time analyticity does not supply analyticity at the boundary. No ordinary Banach-space uniqueness theorem is contradicted: no suitable locally Lipschitz vector field on a specified sequence norm was assumed.

An exact repair is to retain the Laplace profile itself:

```math
Z_{\mathcal T_u\mu}(s)=\frac{Z_\mu(s+u)}{Z_\mu(u)},
\qquad
E_{\mathcal T_u\mu}X=-\frac{Z_\mu'(u)}{Z_\mu(u)}.
\quad\text{(9)}\quad
```

Even the countable values $`Z_\mu(n)`$ determine the law set-theoretically, since they are the moments of $`e^{-X}\in[0,1]`$. That does not provide an error modulus for the unbounded observable $`-\log y`$ near zero. A complete exact record, a computable inverse, and a stable finite-data procedure remain distinct. The proofs and limits in this section incorporate [the unbounded continuation analysis][moment-boundary-source].



## 4. Scalar hierarchies: realizability is an additional condition

### 4.1 Exhaustion of all realizable solutions

**Theorem 6 (scalar classification).** Suppose $`m_0=1`$ and every $`m_r:[0,T)\to\mathbb R`$ is coordinatewise $`C^1`$ and satisfies (7). If the sequence at every time has a Stieltjes probability representative on $`[0,\infty)`$, then there is a unique initial law $`\mu\in\mathcal P_\infty([0,\infty))`$ whose tilt gives the whole path. The same conclusion holds under the weaker assumptions $`m_r(t)\ge0`$ for every degree and time and existence of a representative at just one positive time.

For a fixed valid initial record $`c`$, its realizable hierarchy paths are therefore in bijection with its representing laws. Every such path extends uniquely to all nonnegative times.

**Proof.** Define
```math
a_0(t)=\exp\!\left(-\int_0^t m_1(u)\,du\right),
\qquad a_r(t)=a_0(t)m_r(t).
```
Then $`a_r'=-a_{r+1}`$ and all $`a_r`$ are nonnegative. Iterating the equations makes every coordinate smooth. Taylor's formula backwards from $`t`$ to $`t-b\ge0`$, with its integral remainder of positive sign, gives
```math
\sum_{k=0}^{N}\frac{b^k}{k!}a_{r+k}(t)\le a_r(t-b).
\quad\text{(10)}\quad
```
In particular $`a_n(t)\le n!/t^n`$. On a compact interior time interval, choose a common shorter backward distance. Applied to each fixed $`r`$, (10) bounds its derivatives by $`C_r n!b^{-n}`$, proving real analyticity there.

Choose the positive time $`s`$ in the hypothesis and a probability representative $`\rho_s`$. The finite measure $`\lambda_s=a_0(s)\rho_s`$ has moments $`a_r(s)`$. By the nonnegative exponential series and (10),
```math
\int x^r e^{bx}\,d\lambda_s(x)\le a_r(s-b),
\qquad 0\lt{}b\lt{}s.
\quad\text{(11)}\quad
```
Thus $`G(u)=\int e^{(s-u)x}\,d\lambda_s`$ is analytic for every $`u>0`$. At $`u=s`$ all its derivatives agree with those of $`a_0`$. The identity theorem gives $`G(u)=a_0(u)`$ throughout $`0<u<T`$, and differentiation gives all the other coordinates. As $`u\downarrow0`$, monotone convergence yields
```math
\mu(dx)=e^{sx}\lambda_s(dx),\qquad
\int x^r\,d\mu=\lim_{u\downarrow0}a_r(u)=m_r(0).
```
In particular, $`\mu`$ is a probability with every moment. Dividing the recovered $`a_r`$ by $`a_0`$ proves the assertion. Laplace uniqueness proves uniqueness of the initial law for the complete path.

Conversely, (6) supplies such a path for every initial representative. Distinct representatives give distinct records at every positive time by Proposition 5's determinacy and inverse-tilt argument. The explicit formula supplies the unique global extension. ∎

The uniqueness is attached to the **complete realizable path**, not merely to its initial moment sequence. If that initial sequence is indeterminate, several realizable paths begin there. The proof does not select a measurable family of representatives; one positive-time representative is enough.

The distinction cannot be removed by checking individual signs. Let $`b(t)=1-\varepsilon e^{-1/t}`$ for $`t>0`$, extend it smoothly by $`b(0)=1`$, and take $`0<\varepsilon<1`$. Put $`a_r=(-1)^r b^{(r)}`$ and $`m_r=a_r/b`$. These solve the hierarchy and start from the valid record of $`\delta_0`$, but
```math
a_2(t)=\varepsilon e^{-1/t}\frac{2t-1}{t^4}<0
\quad (0\lt{}t<1/2).
```
This is a formal solution outside the positive cone. Conversely, $`a_0=(T-t)/T`$, $`a_1=1/T`$, and $`a_r=0`$ for $`r\ge2`$ give nonnegative coordinates on $`[0,T)`$ but negative variance. Their initial sequence is already invalid, so this second example does not settle what can happen from a valid initial record. The next construction does. These classification and boundary arguments incorporate [the scalar realizability proof][scalar-source].

### 4.2 Loss of realizability from a determinate initial law despite positive coordinates

**Proposition 7 (strictly positive coordinates without a law).** There is a smooth scalar hierarchy whose initial sequence has a unique probability representative, while every coordinate remains strictly positive and no positive-time sequence has a Stieltjes representative.

**Proof.** Let $`\mu`$ be the standard lognormal law, with moments $`b_r=e^{r^2/2}`$. The classical Krein extremal measure $`\eta_K`$ for this indeterminate Stieltjes problem is a discrete representative with an atom $`w=\eta_K(\{0\})\in(0,1)`$. The full-atom-deletion theorem of Berg and Christensen states that deleting one whole atom of an extremal measure leaves a Hamburger-determinate measure. Consequently
```math
\rho=\frac{\eta_K-w\delta_0}{1-w},
\qquad
c_0=1,\quad c_r=\frac{e^{r^2/2}}{1-w}\ (r\ge1)
\quad\text{(12)}\quad
```
is a determinate probability sequence. Full deletion matters: the theorem used here is not an assertion about arbitrary partial subtraction.

Write $`B_r(t)=\int x^r e^{-tx}\,d\mu`$, and define
```math
a_0(t)=\frac{B_0(t)-w}{1-w},
\qquad
a_r(t)=\frac{B_r(t)}{1-w}\ (r\ge1),
\qquad m_r(t)=\frac{a_r(t)}{a_0(t)}.
\quad\text{(13)}\quad
```
Since $`B_0(t)\ge1-te^{1/2}`$, the denominator is positive for
$`0\le t<T_0=(1-w)/(2e^{1/2})`$. Every coordinate is positive, the equations $`a_r'=-a_{r+1}`$ hold, and the initial record is (12).

Suppose a probability $`\sigma`$ represented the record at some $`t>0`$. Then
$`(B_0(t)-w)\sigma+w\delta_0`$ would have all moments of $`e^{-tx}\mu`$. That latter finite measure has a positive exponential moment and is determinate. The two measures would be equal, although the first has mass at least $`w`$ at zero and the second has none. This is impossible. ∎

The construction uses established extremal-measure results, with the zero-atom premise supplied by [Jabłoński, Jung and Stochel](#references), §2.1, and the full deletion step by [Berg and Christensen](#references), Theorem 7. The logical lesson is precise: uniqueness of the initial representative plus positivity of every *individual moment* does not force later moment realizability.

Here the atom is itself computable. With $`q=e^{-1}`$, the finite Christoffel extremal values are
```math
w_N=
\frac{\det(b_{i+j})_{0\le i,j\le N}}
     {\det(b_{i+j})_{1\le i,j\le N}}
 =\prod_{j=1}^{N}(1-q^j),
\qquad
w=\prod_{j=1}^{\infty}(1-q^j),
\qquad
0\le w_N-w\le\frac{q^{N+1}}{1-q}.
\quad\text{(14)}\quad
```
For the determinant identity, factor the powers $`q^{-i^2/2}`$ and $`q^{-j^2/2}`$ from rows and columns, leaving a Vandermonde matrix in $`q^{-j}`$; the ratio cancels all but the displayed factors. Extremality makes the orthogonal polynomials complete in $`L^2(\eta_K)`$. Evaluation at the atom has squared norm $`1/w`$, so Parseval identifies the decreasing Christoffel limit with $`w`$. The final error bound follows from $`1-\prod(1-u_j)\le\sum u_j`$. This gives exact names for (12)–(13), not merely a nonconstructive counterexample.

The shifted Hankel matrices remain positive definite:
$`\sum v_i v_j B_{i+j+1}(t)=\int x(\sum v_i x^i)^2e^{-tx}\,d\mu>0`$.
Only the unshifted positivity can fail. For $`G_N(t)=(B_{i+j}(t))_{0\le i,j\le N}`$, the unnormalized unshifted matrix is
```math
G_N(t)-w e_0e_0^{\mathsf T}.
```
It is positive semidefinite exactly when
$`w\le(e_0^{\mathsf T}G_N(t)^{-1}e_0)^{-1}`$, by completing the square after applying $`G_N^{1/2}`$. At zero this threshold is $`w_N>w`$, so each fixed truncation passes on some initial interval. At every positive time some truncation must fail, by the Stieltjes existence theorem. The necessary detecting degree therefore tends to infinity towards zero.

One can locate a strict negative quadratic form effectively at any fixed rational positive time in the stated interval. Express
$`B_r(t)=E[\exp(rZ-te^Z)]`$. For $`M>r`$, the omitted two tails are bounded by
$`e^{r^2/2}\{Q(M-r)+Q(M+r)\}`$, and the usual Gaussian bound
$`Q(u)\le e^{-u^2/2}/(\sqrt{2\pi}u)`$ makes this computable. On the compact integration interval, the derivative is the integrand times $`r-te^z-z`$, giving a certified quadrature bound. Together with (14), this computes
$`\sum v_i v_j B_{i+j}(t)-wv_0^2`$. Enumerating rational vectors and dovetailing strict upper-bound tests eventually finds a negative one. There is no uniform degree or termination-time estimate near zero.

The predecessor calculation also gave an actual low-degree witness at $`t=1/10`$, namely $`1-17x/50`$, with a negative interval between $`-0.038075910`$ and $`-0.032572829`$ for the unnormalized quadratic form. That numerical certificate and its independent review are retained as historical evidence; the general proof above does not treat a fresh numerical or kernel execution as having occurred. This section incorporates [the determinate-initial construction][coordinate-counterexample-source], [its Hankel diagnosis][coordinate-diagnostic-source], and [its computational refinement][coordinate-computation-source].

### 4.3 A sufficient condition that really restores the scalar implication

**Theorem 8 (Stieltjes–Carleman recovery).** Suppose a coordinatewise nonnegative scalar hierarchy has a valid initial Stieltjes record $`c`$ satisfying
```math
\sum_{n=1}^{\infty}c_n^{-1/(2n)}=\infty.
\quad\text{(15)}\quad
```
Then the hierarchy is the actual tilt of its unique initial law.

**Proof.** If $`c_1=0`$, that law is $`\delta_0`$; since $`a_1'=-a_2\le0`$ and $`a_1(0)=0`$, all the required conclusions follow. Otherwise fix $`s>0`$ in the supplied interval. The backward Taylor argument in Theorem 6 gives an analytic generating function
```math
a_0(s(1-z))
 =\sum_{j=0}^{\infty}p_j z^j,\qquad
p_j=\frac{s^j a_j(s)}{j!}\ge0,\quad 0\le z<1.
```
Monotone convergence as $`z\uparrow1`$ gives $`\sum p_j=1`$. Thus these numbers define an integer-valued random variable $`N`$. Differentiating the generating function and taking the same boundary limit yields factorial moments
$`E(N)_r=s^r c_r`$.

Let $`X`$ have the initial representing law, and let $`Y`$, conditionally on $`X`$, be Poisson with mean $`sX`$. It has the same factorial moments, hence the same ordinary moments
```math
d_n=\sum_{k=0}^{n}S(n,k)s^k c_k,
```
where $`S(n,k)`$ are Stirling numbers of the second kind. The estimate
$`S(n,k)\le\binom nk n^{n-k}`$ follows by choosing one representative per block and assigning the other elements to at most $`n`$ possibilities. Hölder gives $`c_k\le c_n^{k/n}`$. Therefore
```math
d_n\le\bigl(s c_n^{1/n}+n\bigr)^n,
\qquad
d_n^{-1/(2n)}
 \ge\frac1{\sqrt2}
       \min\{s^{-1/2}c_n^{-1/(2n)},\,n^{-1/2}\}.
\quad\text{(16)}\quad
```
The sequence $`b_n=c_n^{-1/(2n)}`$ is nonincreasing. Cauchy condensation proves divergence of the right-hand series: at the dyadic indices its condensed terms are the minimum of the divergent terms $`s^{-1/2}2^k b_{2^k}`$ and $`2^{k/2}`$. If the latter bound is active infinitely often, the terms do not even tend to zero; if it is active only finitely often, divergence is inherited from the first series. The minimum is itself nonincreasing before condensation.

Thus $`d`$ satisfies the Stieltjes Carleman condition. Both $`N`$ and $`Y`$ are nonnegative laws, so they have the same distribution. Their probability generating functions give
$`a_0(s(1-z))=E[e^{-s(1-z)X}]`$ for $`0\le z<1`$. Differentiation and analytic continuation identify every $`a_r`$, hence the whole path. ∎

The relevant criterion is (15), not the stronger series $`\sum c_n^{-1/n}`$. For example, $`c_n=(2n)!`$ satisfies (15) but not that stronger condition. The mixed-Poisson argument is related to the determinacy transfer studied by [Kuba and Panholzer](#references), but their quoted Hamburger formulation is not silently substituted for the Stieltjes transfer proved here. Proposition 7 and Theorem 8 delimit different hypotheses: determinacy alone is weaker than the quantitative Carleman condition. The proof is part of [the same scalar correction][coordinate-counterexample-source].



## 5. Coercive polynomial energies: positivity forces actual laws

The scalar argument uses the order of the half-line. In several variables, nonnegative coordinates are no longer an adequate substitute for positivity on squares, and square positivity alone is not a general representation theorem. Dynamics supplies additional restrictions. This section proves that those restrictions are sufficient for **every coercive polynomial energy**, not only quadratic energies or energies with a convenient SOS certificate.

### 5.1 Unnormalization and exhaustion under actual representability

For any solution of (1), define
```math
a(t)=\exp\!\left(-\int_0^tL_u(h)\,du\right),
\qquad A_t(p)=a(t)L_t(p).
```
Then
```math
A_t'(p)=-A_t(hp),\qquad
A_t^{(n)}(p)=(-1)^nA_t(h^np).
\quad\text{(17)}\quad
```
The second identity follows by repeatedly applying the first to a polynomial. It requires no unbounded-operator calculus.

**Lemma 9 (lower-bounded exhaustion).** Let $`h`$ be a lower-bounded polynomial. A normalized coordinatewise $`C^1`$ solution of (1) that has an actual probability representative at every time is the moment path of $`\mathcal T_t^h\mu`$ for some initial $`\mu\in\mathcal P_\infty(\mathbb R^d)`$. More generally, after shifting $`h\ge0`$, it suffices to assume $`A_t(q^2h^n)\ge0`$ for every $`q,n,t`$ and a representative at one positive time.

**Proof.** A constant shift changes $`a`$ but not $`L`$. With $`h\ge0`$, the backward Taylor argument gives
```math
\sum_{n=0}^{N}\frac{b^n}{n!}A_t(q^2h^n)
 \le A_{t-b}(q^2),\qquad 0\lt{}b\le t.
\quad\text{(18)}\quad
```
It proves interior analyticity of $`A_t(q^2)`$, hence of every $`A_t(p)`$ by
$`p=((p+1)^2-(p-1)^2)/4`$. Choose the one representative $`\rho_s`$ and set $`\lambda_s=a(s)\rho_s`$. Monotone convergence in (18) gives
$`\int q^2e^{bh}\,d\lambda_s\le A_{s-b}(q^2)`$ for $`b<s`$.
The analytic function
$`u\mapsto\int q^2e^{(s-u)h}\,d\lambda_s`$ has the same derivatives at $`s`$ as $`A_u(q^2)`$, so the two agree throughout $`u>0`$ in the supplied interval. Monotone convergence as $`u\downarrow0`$ gives
$`\mu=e^{sh}\lambda_s`$, with $`\int q^2\,d\mu=A_0(q^2)`$. Its mass is one. The bound $`|p|\le(1+p^2)/2`$ gives every absolute polynomial moment. Polarization recovers all coordinates and normalization gives the claimed tilt. ∎

The supplied path determines its continued moment record even when it does not identify its initial law. For two initial laws under a fixed lower-bounded $`h`$, the exact equivalence is
```math
\mu\sim_h\nu
\quad\Longleftrightarrow\quad
h_*(p\mu)=h_*(p\nu)
\ \text{as finite signed measures for every polynomial }p.
\quad\text{(19)}\quad
```
Indeed, equality of the normalized path fixes the unnormalizer from $`L_t(h)`$ and hence fixes every integral $`\int p e^{-th}\,d\mu`$. Signed Laplace uniqueness gives (19); the reverse implication is immediate. Thus the set of paths from a fixed initial moment record is its representing fibre modulo (19). Inverse multiplication by the positive weight identifies the law-level lifts of any one complete path with the representing fibre at any positive time. A unique lift is equivalent to determinacy at one, and then at every, positive time. A determinate initial record guarantees a unique path, but the converse fails for a constant energy: every initial representative then gives the same constant record.

### 5.2 Even derivatives yield exponential energy control

**Lemma 10 (interior energy bounds).** For an arbitrary real polynomial $`h`$, a square-positive solution of (1) has analytic unnormalized coordinates at every positive interior time. At $`s`$ and any $`b>0`$ with $`[s-b,s+b]\subset[0,T)`$,
```math
A_s(q^2h^{2n})
 \le C_q\,\frac{(2n)!}{b^{2n}},
\qquad
C_q=\frac{A_{s-b}(q^2)+A_{s+b}(q^2)}2.
\quad\text{(20)}\quad
```

**Proof.** For $`f(t)=A_t(q^2)`$, (17) gives
$`f^{(2n)}(t)=A_t((qh^n)^2)\ge0`$.
Taylor expansion to order $`2N+1`$ at $`s`$ in the two directions has nonnegative even-order integral remainders. Adding the expansions cancels the odd terms:
```math
\sum_{n=0}^{N}\frac{b^{2n}}{(2n)!}A_s(q^2h^{2n})
 \le\frac{f(s-b)+f(s+b)}2.
```
This proves (20). The Cauchy–Schwarz inequality for a positive polynomial functional follows from the discriminant of $`A((u+\lambda v)^2)\ge0`$. Applied to $`u=qh^n`$, $`v=qh^{n+1}`$, it bounds the odd derivatives by
$`\sqrt2 C_q(2n+1)!b^{-(2n+1)}`$.
Taking a common smaller $`b`$ in a neighborhood of $`s`$ gives uniform derivative bounds. Taylor's remainder tends to zero there, proving analyticity for squares and then by polarization for every polynomial. ∎

This is an interior assertion. The flat examples at zero remain possible outside the required positivity classes. The radius $`b`$ in (20) is common to all polynomials; their constants $`C_q`$ may differ. That common radius matters in the next existence argument.

### 5.3 From energy fibres to a joint representing measure

**Lemma 11 (compact algebraic fibres).** Let $`\Lambda`$ be a nonzero square-positive polynomial functional. Suppose each level set $`K_r=\{x:h(x)=r\}`$ is compact, and for one common $`b>0`$ and every polynomial $`q`$ there is $`C_q<\infty`$ such that
```math
\Lambda(q^2h^{2n})\le C_q(2n)!b^{-2n}
\quad(n\ge0).
\quad\text{(21)}\quad
```
Then $`\Lambda`$ has a positive joint representing measure.

**Proof.** For each $`q`$, the one-variable functional
$`r\mapsto\Lambda(q^2r(h))`$ is positive on squares, hence has a Hamburger representative $`\nu_{q^2}`$. By the nonnegative series for $`\cosh`$ and (21),
$`\int\cosh(cz)\,d\nu_{q^2}(z)<\infty`$ whenever $`0<c<b`$.
Since $`e^{c|z|}\le2\cosh(cz)`$, these measures have an exponential absolute moment and are unique. The zero-mass case is the zero measure. More generally, a finite signed measure with an exponential absolute moment is determined by its polynomial moments: its Laplace transform is analytic in a strip, and zero moments force a zero Fourier transform there and hence a zero measure.

Define, by polarization,
```math
\nu_p=\frac{\nu_{(p+1)^2}-\nu_{(p-1)^2}}4.
```
Its moments are $`\Lambda(ph^n)`$. Signed uniqueness proves linearity in $`p`$ and $`\nu_{hp}(dz)=z\,\nu_p(dz)`$. It also proves that this definition for a square agrees with its positive scalar representative. For every Borel set $`B`$, the map $`p\mapsto\nu_p(B)`$ is square-positive. Its Cauchy–Schwarz inequality gives
```math
|\nu_p(B)|^2\le\nu_{p^2}(B)\nu_1(B).
```
Consequently every $`\nu_p`$ is absolutely continuous with respect to $`\nu_1`$.

Take Radon–Nikodym derivatives $`f_\alpha`$ for the countable family of monomials. Outside one common null set, $`f_0=1`$; all rational-coefficient square inequalities hold; and the finitely supported coefficient relations for $`\nu_{hx^\alpha}=z\nu_{x^\alpha}`$ hold. Define
$`\ell_z(\sum p_\alpha x^\alpha)=\sum p_\alpha f_\alpha(z)`$.
Continuity in each finite coefficient space extends positivity from rational to real squares. Thus $`\ell_z`$ is normalized, positive on all squares, and annihilates every multiple of $`h-z`$.

The compact algebraic-set moment theorem now applies: a positive functional annihilating that ideal is represented on the compact real zero set $`K_z`$. This is precisely the algebraic existence statement in [Schmüdgen](#references), revised Chapter 12, Corollary 12.34(iv). Empty fibres cannot carry such a normalized functional.

For any polynomial $`P`$ nonnegative on all of $`\mathbb R^d`$, the fibre representation gives $`\ell_z(P)\ge0`$ almost everywhere. Integration gives $`\Lambda(P)\ge0`$. Haviland's theorem therefore supplies a joint measure on $`\mathbb R^d`$ representing $`\Lambda`$. No measurable selection of the individual fibre measures has been used: only their implication for the measurable quantities $`\ell_z(P)`$ is integrated. ∎

The first scalar Hamburger step is not already a joint representation. Nor is uniqueness of an existing joint measure a substitute for this existence step. The proof preserves both distinctions.

### 5.4 The arbitrary coercive theorem

**Theorem 12 (coercive square-positivity theorem).** Let $`h\in\mathbb R[x_1,\ldots,x_d]`$ be coercive, meaning $`h(x)\to+\infty`$ as $`|x|\to\infty`$. Every normalized coordinatewise $`C^1`$ square-positive solution of (1) is the full moment path of $`\mathcal T_t^h\mu`$ for a unique $`\mu\in\mathcal P_\infty(\mathbb R^d)`$. Its record is determinate at every positive time. For each valid initial record, its square-positive hierarchy paths are in bijection with its initial representing laws; every such path has a unique global continuation.

**Proof.** Coercivity gives compact level sets. At each interior positive time, Lemmas 10–11 give an actual representative. This part does not assume that a nonnegative polynomial is SOS or that the initial record already has a measure. Shift $`h`$ by its finite lower bound so that $`h\ge0`$. The positive-time representatives now imply $`A_t(q^2h^n)\ge0`$; continuity gives the same at zero. Lemma 9 produces an initial measure and the actual tilt.

It remains to establish determinacy. Let $`\lambda`$ be a positive-time unnormalized measure. The backward bound gives $`\int e^{bh}\,d\lambda<\infty`$ for some $`b>0`$. If $`\lambda'`$ has the same polynomial moments, the nonnegative exponential series in the polynomial $`h`$ gives the same finite bound for $`\lambda'`$. For each polynomial $`p`$, Cauchy–Schwarz shows that
$`\tau_p=h_*(p\lambda-p\lambda')`$ has a positive exponential absolute moment, at a smaller rate. All its moments vanish, so signed uniqueness gives $`\tau_p=0`$.

For each $`R`$, it follows that the restrictions of $`\lambda`$ and $`\lambda'`$ to the compact sublevel set $`\{h\le R\}`$ agree on all polynomials. Polynomial density on that compact set gives equality of the restrictions. Exhausting the space gives $`\lambda=\lambda'`$. Positive-time determinacy and inverse weighting identify the initial law for the whole path. Conversely, the lower bound on $`h`$ makes the tilt well defined for every nonnegative time and permits polynomial dominated differentiation. This proves the bijection and global extension. ∎

The compact-sublevel proof also works on a fixed closed support set whose energy sublevels are compact. A direct disintegration theorem with a **strictly determinate** base is not invoked under the weaker claim of ordinary determinacy; the compact-sublevel argument avoids that mismatched hypothesis. This corrects a potential shortcut identified in [the independent tensor review][tensor-review-source].

There is a useful independent proof in the quadratic case. For $`h=|x|^2`$, the difference $`h^n-x_i^{2n}`$ is SOS. Equations (18) therefore give
```math
L_t(x_i^{2n})\le\frac{n!}{a(t)t^n}.
```
Each marginal Carleman series diverges, since its terms are bounded below by a constant times $`n^{-1/2}`$. The multivariate Carleman theorem supplies existence from full square positivity and uniqueness from all marginal conditions. More generally, $`h-c|x|^2`$ SOS gives the same argument with $`ct`$. The relevant theorem, recalled by [Putinar and Schmüdgen](#references), Theorem 25, gives existence when all but at most one marginal satisfy Carleman, and determinacy when all do. This separate route will matter for hidden coordinates below.

A polynomial change of coordinates may make that quadratic route available without a radial bound in the original coordinates. If $`\Phi`$ is a polynomial automorphism with polynomial inverse and $`h=|\Phi(x)|^2+C`$, apply the quadratic argument in $`\Phi`$-coordinates. For example, $`\Phi(x,y)=(x,y-x^k)`$ gives
$`h=x^2+(y-x^k)^2`$. Along $`(r,r^k)`$, this is $`r^2`$, so for $`k\ge3`$ it need not dominate even the first power of the ambient norm at infinity. Coercivity, rather than a presumed quadratic growth rate, is the invariant condition in Theorem 12.

The theorem also genuinely exceeds the SOS-dominance route. The Motzkin form
```math
M(x,y,z)=x^4y^2+x^2y^4+z^6-3x^2y^2z^2
```
is nonnegative by the arithmetic–geometric mean inequality. The energy $`h=M+x^2+y^2+z^2`$ is coercive, but no choice of scalar $`C`$ and $`c>0`$ makes $`h+C-c|x|^2`$ SOS. Otherwise its leading homogeneous part $`M`$ would be a sum of squares of cubics. The zero coefficients of $`x^6,y^6`$ eliminate the cubic monomials $`x^3,y^3`$ from every summand. The zero coefficients of $`x^4z^2,y^4z^2`$ then eliminate $`x^2z,y^2z`$, and those of $`x^2z^4,y^2z^4`$ eliminate $`xz^2,yz^2`$. The coefficient of $`x^2y^2z^2`$ would consequently be a sum of squares of the remaining $`xyz`$ coefficients, and so could not equal $`-3`$. Theorem 12 nevertheless applies.

These arguments reconcile [the vector realizability theorem][tensor-source] with [its stronger coercive-polynomial successor][coercive-source]. The earlier unresolved general-coercive question is closed by the latter proof; it is not retained here as an open problem.

### 5.5 What the hypotheses prevent

Full energy information alone need not be full state information. Take independent $`X`$ uniformly distributed on $`\{0,1\}`$ and $`Y`$ with either law in (8). Under $`h(x,y)=x^2`$, only the first coordinate tilts. All mixed moment paths coincide, although the joint laws remain distinct. This is the noncoercive equivalence in (19).

Even identical energy distributions can conceal different full responses under a coercive energy. On the two half-lines, put densities
$`\tfrac12 f(r)(1+\varepsilon\sin(2\pi\log r))`$ at $`+r`$ and
$`\tfrac12 f(r)(1-\varepsilon\sin(2\pi\log r))`$ at $`-r`$, and reverse the signs for a second law. Their odd moments vanish, their even moments equal $`e^{2n^2}`$, and their $`x^2`$ distributions agree. Nevertheless the full records under $`h=x^2`$ differ at every positive time by Theorem 12. The first moments have opposite signs as functions and cannot agree on any positive interval, though a claim that the first moments differ at every individual time would be stronger than proved.

Lower bounds also control the time horizon. For mass $`2^{-n-1}`$ at $`x=-n`$ and energy $`h=x`$, the normalizer is
$`Z(t)=(2-e^t)^{-1}`$, finite only for $`t<\log2`$, and the tilted mean is $`-e^t/(2-e^t)`$. A real quadratic polynomial $`x^{\mathsf T}Bx+b\cdot x+c`$ is bounded below exactly when the symmetric matrix $`B`$ is positive semidefinite and $`b`$ lies in its range. A negative eigenvector gives quadratic descent to minus infinity; a linear component along the kernel gives linear descent; otherwise completing the square gives a lower bound. Signed energies require the different analysis that follows.



## 6. Signed energies, finite horizons, and exact null ideals

A scalar shift cannot make an arbitrary polynomial energy nonnegative. For signed energies, forward damping can become amplification on part of the support. The backward monotonicity used in Lemma 9 must then be replaced by the even-derivative argument and a hypothesis about the initial energy distributions.

### 6.1 Weighted energy determinacy

**Theorem 13 (signed-energy exhaustion).** Let $`h`$ be any real polynomial, and let a normalized square-positive coordinatewise $`C^1`$ solution of (1) have initial moment functional $`L_0=L_\mu`$ for $`\mu\in\mathcal P_\infty(\mathbb R^d)`$. Suppose that, for every polynomial $`q`$, the finite positive measure
$`h_*(q^2\mu)`$ on $`\mathbb R`$ is Hamburger-determinate. Then throughout the supplied interval,
```math
A_t(p)=\int p(x)e^{-th(x)}\,d\mu(x),\qquad
L_t(p)=\frac{\int p e^{-th}\,d\mu}{\int e^{-th}\,d\mu}.
\quad\text{(22)}\quad
```
In particular, the existence of the square-positive path forces all these weighted integrals to be finite. No positive-time joint representative is assumed.

**Proof.** For a fixed $`q`$ and positive interior $`t`$, the scalar functional
$`r\mapsto A_t(q^2r(h))`$ is positive on squares. Hamburger existence gives a measure $`\sigma_t^q`$ with moments $`A_t(q^2h^n)`$. Lemma 10 and the cosh series give a positive exponential absolute moment, hence uniqueness of this scalar measure.

For sufficiently close positive times $`u,v`$, the analytic function
$`v\mapsto\int e^{-(v-u)z}\,d\sigma_u^q(z)`$ has exactly the derivatives of $`A_v(q^2)`$ at $`u`$. Equality near $`u`$ and differentiation identify all moments at $`v`$. The scalar measures are determinate there, so
```math
\sigma_v^q(dz)=e^{-(v-u)z}\sigma_u^q(dz).
\quad\text{(23)}\quad
```
A common smaller time radius on any compact interior interval follows from (20); a finite chain of overlapping neighborhoods extends (23) between any two positive times.

Fix $`s>0`$ and put $`\tau_q=e^{sz}\sigma_s^q`$. To see that this is a finite measure with the correct initial moments, use (23) and let $`u\downarrow0`$. On $`z\ge0`$, the even-moment integrands $`z^{2n}e^{(s-u)z}`$ increase monotonically. On $`z<0`$, they are dominated by their value at one fixed earlier positive time. Their limits therefore have moments $`A_0(q^2h^{2n})`$. Bounds by neighboring even powers handle the odd moments. In particular $`\tau_q`$ is finite and represents the entire initial scalar sequence $`L_\mu(q^2h^n)`$.

The hypothesis now identifies $`\tau_q=h_*(q^2\mu)`$. Evaluating (23) at total mass gives
$`A_t(q^2)=\int q^2e^{-th}\,d\mu`$. Polarization gives (22) for every polynomial, and its value at one is the normalizer. ∎

Two readily checked sufficient conditions are useful. If $`|h|\le M`$ almost surely under $`\mu`$, every weighted energy measure has support in $`[-M,M]`$ and is determinate. This conclusion does not require compact joint support. If instead $`\int e^{a|h|}\,d\mu<\infty`$ for some $`a>0`$, Cauchy–Schwarz with $`q^4`$ gives an exponential absolute moment for every weighted energy measure at rate $`a/2`$, and hence the same determinacy. The weighted integrals needed for a path are then finite at least for $`0\le t<a/2`$.

The exact forward domain for a specified initial law is the set of times at which
$`\int q^2e^{-th}\,d\mu<\infty`$ for every polynomial $`q`$. On the interior of any such interval starting at zero, the normalized tilt satisfies (1). To justify differentiation, bracket an interior time by two nearby times and split according to the sign of $`h`$; the two endpoint weights dominate the derivative with each fixed polynomial factor. At zero use an available positive endpoint on $`h<0`$ and the original moments on $`h\ge0`$. Thus if $`T_\mu`$ is the supremum of these open forward intervals, the actual path exists on $`[0,T_\mu)`$. The supremum is not automatically an admissible endpoint. Theorem 13 precludes a square-positive continuation beyond a true weighted-integrability obstruction under its determinacy hypothesis.

### 6.2 Algebraic degeneracy is preserved exactly

**Corollary 14 (null ideals and finite Gram ranks).** Every normalized square-positive solution of the autonomous hierarchy, even without an assumed initial representing measure, satisfies
```math
I_t:=\{q:L_t(q^2)=0\}=I_0
\quad(0\le t\lt{}T).
\quad\text{(24)}\quad
```
For every fixed finite polynomial family, its Gram matrix has the same kernel and rank throughout the interval.

**Proof.** Construct the scalar $`\sigma_s^q`$ and its boundary measure $`\tau_q`$ as in Theorem 13; this construction used positivity and continuity, not the initial representation or determinacy hypothesis. Their masses are respectively $`A_s(q^2)`$ and $`A_0(q^2)`$, and $`\tau_q=e^{sz}\sigma_s^q`$. Multiplication by a strictly positive finite function has zero total mass exactly when the original positive measure is zero. This proves both directions of (24).

Cauchy–Schwarz shows that a null polynomial pairs to zero with every polynomial. In particular,
$`L(q^2r^2)=L(q\cdot qr^2)=0`$, so the null space is an ideal. The kernel of the Gram matrix for $`p_1,\ldots,p_N`$ consists of coefficient vectors whose polynomial $`\sum c_i p_i`$ lies in that ideal. Equation (24) gives the conclusion. ∎

The result concerns an exact kernel, not uniform eigenvalue bounds or conditioning. Nor does it prevent a rank change in an infinite-time limit. It strengthens a merely forward-persistence claim: no polynomial null relation can appear or disappear at a finite time inside the admitted interval.

### 6.3 Examples separating the hypotheses

With $`\mu=N(0,1)`$ and $`h=x`$, the normalizer is $`e^{t^2/2}`$ and the tilted law is $`N(-t,1)`$ for all $`t\ge0`$. With the same initial law and $`h=-x^2`$, instead,
```math
Z(t)=(1-2t)^{-1/2},\qquad
L_t(x^{2n})=(2n-1)!!(1-2t)^{-n},
\quad 0\le t<1/2.
```
The energy has an initial exponential absolute moment, so Theorem 13 applies. The actual divergence at $`t=1/2`$ cannot be crossed by another finite coordinatewise square-positive solution with the same initial law and hierarchy.

Bounded energy does not imply joint-law identification. Let $`X`$ take $`\pm1`$ equally, let an independent $`Y`$ have either lognormal law (8), and set $`h=X`$. The normalizer is $`\cosh t`$ and
```math
L_t(X^aY^b)=e^{b^2/2}
\begin{cases}
1,&a\text{ even},\\
-\tanh t,&a\text{ odd}.
\end{cases}
```
Both distinct joint laws give the same full path. The weighted energy distributions are supported on two points, so Theorem 13 identifies the dynamics for each proposed initial law without identifying which joint law was chosen.

Signed energies also invalidate a nonnegative-derivative shortcut even on finite support. For atoms $`(0,1),(1/2,1/2),(1,0)`$ with weights $`(1/2,1/3,1/6)`$ and energy $`h=x-y`$, the weights at $`t=\log2`$ are $`(12,4,1)/17`$, with mean $`(3,14)/17`$ and energy mean $`-11/17`$. For $`q=1-x`$, the unnormalized derivative $`A_0'(q^2)`$ is $`1/2>0`$, not nonpositive. The same finite support admits nonlinear signed energy $`x^3-3y`$, with values $`-3,-11/8,1`$, so no linearity of the energy is being assumed.

On a compact initial support, every polynomial energy is bounded there. The same support persists, and any competing joint measure with the same moments is confined to a compact box by its high even moments; compact polynomial density then gives uniqueness. Applying Theorem 13 successively therefore allows locally finite piecewise-autonomous **signed** schedules. Their actual law is $`e^{-\int_0^t h_sds}\mu`$ after normalization. For the preceding three atoms, applying $`h=x-y`$ for duration $`\log2`$ and then $`-h`$ for duration $`\log3`$ gives weights $`(4,4,3)/11`$. This conclusion does not assert a theorem for arbitrary continuously changing signed polynomials on noncompact supports.

The flat construction with $`b=1-\varepsilon e^{-1/t}`$ also works algebraically for $`h=x`$ on the line, but its negative $`L_t(x^2)`$ excludes square positivity. Such a solution is not a counterexample to Theorem 13 or Corollary 14. This section incorporates [the corrected signed-energy proof][signed-source]; its [earlier edition][signed-earlier-source] and [independent reviews][signed-review-source] retain their distinct historical evidence boundaries.



## 7. Time-dependent damping and cumulative control

Instantaneous coercivity is stronger than the dynamics needs. A succession of rank-one dampings may control every direction cumulatively, even though no single instantaneous energy does.

### 7.1 Cumulative SOS coercivity

Let $`h_t`$ be polynomials whose coefficients are continuous in time and whose degrees are bounded on each finite time interval. Assume that on every such interval a continuous scalar $`\beta(t)`$ can be chosen so that
$`g_t=h_t+\beta(t)`$ is SOS. Write
```math
K_{s,t}(x)=\int_s^t g_u(x)\,du,\qquad R(x)=|x|^2.
```
Assume that for each $`t>0`$ there is $`c(t)>0`$ with
```math
K_{0,t}-c(t)R\ \text{SOS}.
\quad\text{(25)}\quad
```
No regularity of the chosen $`c`$, no lower bound proportional to $`t`$, and no coercivity on every subinterval is assumed.

**Theorem 15 (cumulative damping).** Every normalized square-positive coordinatewise $`C^1`$ solution of
```math
L_t'(p)=-L_t(h_tp)+L_t(h_t)L_t(p)
\quad\text{(26)}\quad
```
under these assumptions has the form
```math
L_t(p)=\frac{\int p(x)e^{-H_t(x)}\,d\mu(x)}
             {\int e^{-H_t(x)}\,d\mu(x)},
\qquad H_t=\int_0^t h_u\,du,
\quad\text{(27)}\quad
```
for a unique $`\mu\in\mathcal P_\infty(\mathbb R^d)`$ attached to the complete path. Every positive-time record is determinate. The paths from a fixed valid initial record are in bijection with its representing laws.

**Proof.** Fix a finite horizon and its scalar shift. Put
$`a(t)=\exp(-\int_0^tL_u(g_u)\,du)`$ and $`A_t=a(t)L_t`$.
Then $`A_t'(p)=-A_t(g_tp)`$ and $`0<a(t)\le1`$.

**Finite backward expansion.** Repeatedly integrate
$`A_s(p)=A_t(p)+\int_s^tA_u(pg_u)\,du`$. For every finite $`N`$ this gives
```math
A_s(p)=\sum_{k=0}^{N}\frac{A_t(pK_{s,t}^{\,k})}{k!}+E_{N+1}(s,t;p),
\quad\text{(28)}\quad
```
where
```math
E_m(s,t;p)=
 \int_{s\le u_1\le\cdots\le u_m\le t}
 A_{u_m}\!\left(p\prod_{j=1}^{m}g_{u_j}\right)
 \,du_1\cdots du_m.
```
The remainder functional is evaluated at the **latest** time $`u_m`$. At each finite stage, continuous coefficients and bounded degree justify ordinary finite-dimensional integration. In the terminal terms the polynomial factors commute, so integration over the ordered simplex is $`1/k!`$ times integration over the cube, producing $`K_{s,t}^k`$. No convergent infinite operator expansion has been assumed.

For $`p=q^2`$, the remainder is nonnegative, since products of SOS polynomials are SOS. Let $`c=c(t)`$. Because $`K_{0,t}-cR`$ is SOS,
$`K_{0,t}^n-c^nR^n`$ is SOS by the difference-of-powers factorization. Hence
```math
\sum_{n=0}^{N}\frac{c^n}{n!}A_t(q^2R^n)\le A_0(q^2).
\quad\text{(29)}\quad
```
The coordinate moments obey
$`L_t(x_i^{2n})\le n!/[a(t)c^n]`$.
The multivariate Carleman existence and uniqueness theorem therefore supplies a unique positive-time probability $`\rho_t`$. Let $`\nu_t=a(t)\rho_t`$. Taking the **whole partial sum** in (29) and then using monotone convergence gives the endpoint estimate
```math
\int q^2e^{cR}\,d\nu_t\le A_0(q^2).
\quad\text{(30)}\quad
```
Using only the separate factorial bounds would prove this at smaller rates, not automatically at the endpoint $`c`$.

**From polynomial coordinates to a weak measure equation.** On an interior interval $`[\eta,H]`$, each $`A_t(q^2R^n)`$ is nonincreasing, because its derivative is the negative of an SOS evaluation. Thus the same Gaussian bound with $`c=c(\eta)`$ holds uniformly throughout that interval.

For $`\xi\in\mathbb R^d`$, approximate $`e^{i\xi\cdot x}`$ by its Taylor polynomial of degree $`N`$. With $`k=N+1`$, its integrated remainder is at most
```math
\frac{|\xi|^k\sqrt{k!}}{k!\,c^{k/2}}.
```
If $`|g_t(x)|\le B(1+|x|^D)`$ uniformly on this interval, the derivative remainder is at most
```math
\frac{B|\xi|^k}{k!}
\left(\frac{\sqrt{k!}}{c^{k/2}}
      +\frac{\sqrt{(k+D)!}}{c^{(k+D)/2}}\right).
\quad\text{(31)}\quad
```
Both tend to zero uniformly for $`t`$ and for $`\xi`$ in a compact set. For the last term, the ratio is
$`|\xi|\sqrt{k+D+1}/(\sqrt c\,(k+1))\to0`$.
Taking limits in the differentiated polynomial identities gives
```math
\frac{d}{dt}\int e^{i\xi\cdot x}\,d\nu_t
 =-\int g_t(x)e^{i\xi\cdot x}\,d\nu_t.
```
The Fourier transforms are jointly continuous. Fourier inversion now yields
$`\frac d{dt}\int\phi\,d\nu_t=-\int g_t\phi\,d\nu_t`$ for $`\phi\in C_c^\infty`$. The exchange with the Fourier integral uses the frequency-independent bounds $`\nu_t(1)\le1`$ and $`|\int g_te^{i\xi\cdot x}d\nu_t|\le A_t(g_t)`$, which are locally bounded. It does not integrate the growing estimate (31) over all frequencies.

For a time-varying test $`\psi_t`$ with common compact support, continuous time derivative, and with both $`\psi_t`$ and $`\partial_t\psi_t`$ smooth in space, the difference quotient gives
```math
\frac d{dt}\int\psi_t\,d\nu_t
 =\int(\partial_t\psi_t-g_t\psi_t)\,d\nu_t.
```
Choose $`\psi_u=\phi e^{K_{s,u}}`$. Its derivative cancels the energy term, giving
```math
\nu_s=e^{K_{s,t}}\nu_t,\qquad 0\lt{}s\lt{}t\lt{}T.
\quad\text{(32)}\quad
```
Initially this is equality against compactly supported tests. Both sides are locally finite positive measures, so exhaustion by compact sets makes it a global equality and proves finiteness of the right side.

**Recovery of the boundary law.** Let $`s\downarrow0`$ in (32). Since $`g_u\ge0`$, the weights increase to $`e^{K_{0,t}}`$. Monotone convergence for $`q^2`$ and continuity of $`A_s(q^2)`$ give
$`\mu=e^{K_{0,t}}\nu_t`$ with $`\mu(1)=1`$ and every polynomial square moment. Polarization recovers all coordinates. Undoing the scalar shift gives (27). Positive-time determinacy and inverse weighting make this $`\mu`$ unique for the whole path.

Conversely, $`e^{-H_t}\le\exp(\int_0^t|\beta(u)|du)`$ on each finite horizon. Polynomial domination and the local degree bound justify (26) for every initial law with all moments, including the boundary derivative. This proves the stated bijection. ∎

Only the supplied schedule is classified. A global extension follows when an appropriate schedule is supplied globally; the theorem does not choose future controls.

A related elementary point explains integration of SOS polynomials without selecting time-dependent square factors. In a fixed degree bound, write an SOS polynomial as $`z_m^{\mathsf T}Qz_m`$ with $`Q\ge0`$ and $`z_m`$ the monomials through degree $`m`$. The matrix
$`B=\int_{|x|\le1}z_mz_m^{\mathsf T}\,dx`$ is positive definite. Coefficient convergence bounds $`\mathrm{tr}(QB)`$, hence bounds $`Q`$. A convergent subsequence of these Gram matrices has a positive semidefinite limit. The SOS cone of bounded degree is therefore closed. Riemann sums and closure show that an integral of continuous bounded-degree SOS polynomials is SOS. Neither this fact nor Theorem 15 requires continuous choices of their individual square factors.

### 7.2 Rank-one rates with full cumulative control

For $`g_t(x,y)=(x+ty)^2`$,
```math
K_{0,t}=tx^2+t^2xy+\frac{t^3}{3}y^2.
```
Its matrix has determinant $`t^4/12`$ and trace $`t+t^3/3`$, so it is positive definite for every $`t>0`$. A completely explicit SOS certificate is
```math
c(t)=\frac{t^3}{4(t^2+3)},\qquad
a(t)=\frac{3t(t^2+4)}{4(t^2+3)},
```
```math
K_{0,t}-c(t)(x^2+y^2)
 =a(t)\left(x+\frac{2t(t^2+3)}{3(t^2+4)}y\right)^2
  +\frac{t^5}{12(t^2+3)(t^2+4)}y^2.
\quad\text{(33)}\quad
```
At each instant the energy vanishes along $`\lambda(-t,1)`$, so no scalar shift can make it dominate a positive radial quadratic there. Moreover $`c(t)`$ is of order $`t^3`$ at zero, not bounded below by a positive multiple of $`t`$. Thus this example lies genuinely beyond instantaneous radial coercivity.

For rotating rank-one energy $`(x\cos t+y\sin t)^2`$, the cumulative eigenvalues are $`(t\pm|\sin t|)/2`$, both positive for $`t>0`$. Control need not continue rotating. If
$`g_t=(x+\min(t,1)y)^2`$, then after time one every later subinterval has only rank-one cumulative energy, while
```math
K_{0,t}-\frac1{16}(x^2+y^2)
 =\frac{15}{16}\left(x+\frac8{15}y\right)^2
   +\frac{y^2}{240}+(t-1)(x+y)^2,\qquad t\ge1.
```
The earlier accumulated control is enough. Finally, the rank of the cumulative energy matrix is not the covariance rank of the law: an initial point mass remains a point mass with zero covariance.

### 7.3 Polynomial coordinate transport

A genuine drift can be included when it arises from a specified polynomial change of coordinates with polynomial inverse. Let $`\Phi_t`$ and $`\Psi_t`$ be inverse polynomial automorphisms, with $`\Phi_0=\mathrm{id}`$, locally bounded degrees and $`C^1`$ coefficients. Put
$`v_t=(\partial_t\Phi_t)\circ\Psi_t`$.
Suppose the pulled-back energy $`k_t=h_t\circ\Phi_t`$ satisfies Theorem 15. A square-positive functional solving
```math
L_t'(p)=L_t(v_t\cdot\nabla p)-L_t(h_tp)+L_t(h_t)L_t(p)
\quad\text{(34)}\quad
```
then has the law
```math
(\Phi_t)_*\left(
 \frac{e^{-\int_0^t k_s\,ds}\mu}
      {\int e^{-\int_0^t k_s\,ds}\,d\mu}
\right).
\quad\text{(35)}\quad
```

Indeed, set $`M_t(q)=L_t(q\circ\Psi_t)`$. The inverse relation gives
$`\partial_t(q\circ\Psi_t)+v_t\cdot\nabla(q\circ\Psi_t)=0`$.
The two transport terms cancel in (34), leaving exactly the hierarchy for $`k_t`$. Polynomial composition preserves square positivity. Apply Theorem 15, then push the resulting law forward. Any competitor with the same current moments pulls back, through the polynomial inverse, to a competitor for the determinate pulled-back law, proving determinacy. Gaussian control belongs to the pulled-back coordinates and need not be an ordinary Gaussian tail in the current coordinates.

For example,
$`\Phi_t(u,z)=(u,z+tu^m)`$ has inverse $`\Psi_t(x,y)=(x,y-tx^m)`$ and drift $`v_t=(0,x^m)`$. Taking
$`h_t(x,y)=[x+t(y-tx^m)]^2`$ gives
$`k_t(u,z)=(u+tz)^2`$, so (33) supplies the required cumulative control. General polynomial vector fields need not have polynomial global flows or polynomial inverses; no such generalization is asserted.

The full argument, its examples, and this transport result incorporate [the cumulative damping proof][cumulative-source]. The [independent review][cumulative-review-source] matters particularly for the smooth time-varying test step: spatial smoothness of the time derivative is included explicitly above.



## 8. A fixed controlled subspace and hidden coordinates

Write the state as $`(z,y)\in\mathbb R^r\times\mathbb R^k`$, with $`r\ge1`$. Suppose the SOS energies $`g_t(z)`$ depend only on the controlled coordinates, and
```math
K_t(z)=\int_0^t g_u(z)\,du,\qquad
K_t-c(t)|z|^2\ \text{SOS},\quad c(t)>0\ (t>0).
\quad\text{(36)}\quad
```
The full functional still acts on **all** polynomials in $`z`$ and $`y`$, and is assumed square-positive on that entire algebra. The schedule has the same coefficient continuity and local degree bounds as in §7. An admissible scalar shift may be made as before.

Partial control does not justify asserting joint existence first and disintegrating afterward. The following construction instead extracts the parts that can be represented without that assertion.

### 8.1 Canonical signed measures on the controlled space

**Lemma 16 (controlled projections).** For every such square-positive hierarchy and every hidden polynomial $`b(y)`$, there is a canonical finite signed measure $`\sigma_{t,b}`$ on $`\mathbb R^r`$ at each positive time, with
```math
\int f(z)\,d\sigma_{t,b}(z)=A_t(f(z)b(y))
\quad\text{for every polynomial }f.
\quad\text{(37)}\quad
```
For hidden squares these measures are positive. On every compact interior interval they have uniform Gaussian absolute-moment bounds and satisfy
```math
\sigma_{u,b}=e^{K_s-K_u}\sigma_{s,b}
\quad(s,u>0).
\quad\text{(38)}\quad
```

**Proof.** The same finite Volterra expansion as (28) gives
$`\sum_{n=0}^N c(t)^n A_t(b(y)^2|z|^{2n})/n!\le A_0(b^2)`$.
The controlled functional $`f\mapsto A_t(f(z)b(y)^2)`$ is square-positive. If its mass is zero it is identically zero by Cauchy–Schwarz. Otherwise normalization and the factorial bounds give Carleman in all $`r`$ controlled coordinates, so there is a unique positive representative $`\tau_t^b`$, with
$`\int e^{c(t)|z|^2}\,d\tau_t^b\le A_0(b^2)`$.

For an arbitrary hidden polynomial $`b`$, define
```math
\sigma_{t,b}=\frac{\tau_t^{\,b+1}-\tau_t^{\,b-1}}4.
```
It has the moments (37), and
```math
\int e^{c(t)|z|^2}\,d|\sigma_{t,b}|
 \le M_b,\qquad M_b=\frac{A_0(b^2)+1}{2}.
\quad\text{(39)}\quad
```
A finite signed measure with a Gaussian absolute moment is determined by its polynomial moments. Indeed, its Fourier transform has an everywhere convergent Taylor expansion, using the same factorial estimates as in (31). Thus polarization gives a unique signed measure, is linear in $`b`$, and agrees with the positive representative when $`b`$ is a square.

For $`t\ge\eta>0`$, the mixed square bounds at $`\eta`$ propagate because $`A_t(b^2|z|^{2n})`$ is nonincreasing. Hence (39) holds uniformly with $`c=c(\eta)`$. Apply the Fourier argument of Theorem 15 in the $`z`$ variables alone to $`A_t(f(z)b(y))`$. With $`|g_t(z)|\le B(1+|z|^D)`$, the integrated derivative remainders are bounded by $`M_b`$ times the expression in (31), and the Fourier derivative itself has the frequency-independent bound
$`BM_b(1+\sqrt{D!}\,c^{-D/2})`$.
Consequently
$`\partial_t\sigma_{t,b}=-g_t\sigma_{t,b}`$ against compact smooth tests. Compactly supported integrating factors give (38) locally as signed measures. Equality on a compact exhaustion identifies the full signed measures; their finite total variations, rather than an unproved exchange of an unbounded weight with an integral, supply the global conclusion. ∎

This proof does not choose any family of joint measures. The scalar projections are canonically fixed by the mixed moment record.

### 8.2 One positive-time law is enough, and when it is automatic

**Theorem 17 (persistence and the one-hidden-coordinate threshold).** Under (36), if the full joint record has a representative at one positive time, then the entire path is the record of
```math
\rho_t=\frac{e^{-K_t(z)}\mu(dz,dy)}
                 {\int e^{-K_t(z)}\,d\mu}
\quad\text{(40)}\quad
```
for some $`\mu\in\mathcal P_\infty(\mathbb R^{r+k})`$. Every representative at that time gives exactly one such lift. Positive-time joint representability is therefore an all-or-none property along the path.

For $`k=0`$, representation is automatic and unique at every positive time. For $`k=1`$, representation is automatic, but it may not be unique. For $`k\ge2`$, the one-positive-time representation hypothesis cannot be dropped.

**Proof.** Suppose $`\rho_s`$ represents $`L_s`$ and put $`\nu_s=a(s)\rho_s`$. Its controlled projection weighted by any hidden polynomial is the canonical $`\sigma_{s,b}`$: the Gaussian bounds follow from the full partial-sum estimate, and signed uniqueness identifies it. Define the positive measure
$`\nu_u=e^{K_s-K_u}\nu_s`$ for any $`u>0`$.

Its mass is finite and equals $`A_u(1)`$ by (38) with $`b=1`$. For each hidden even monomial $`y^{2\alpha}`$, positivity and (38) identify its controlled projection with $`\sigma_{u,y^{2\alpha}}`$. Monotone integration of $`|z|^{2m}`$ against this positive measure gives finite mixed even moments. Cauchy–Schwarz therefore gives every absolute mixed polynomial moment. Only after that integrability is established may signed mixed moments be transported; (38) then gives all coordinates $`A_u`$.

As $`u\downarrow0`$, the positive weights increase to $`e^{K_s}`$. Monotone convergence for polynomial squares and continuity of the corresponding coordinates give
$`\mu=e^{K_s}\nu_s`$, with mass one and all moments. This proves (40) and its inverse correspondence.

For $`k=0`$, Theorem 15 applies. For $`k=1`$, the full positive functional has Carleman bounds in $`r=d-1`$ coordinates. The multivariate Carleman existence theorem therefore supplies a joint measure; it does not promise determinacy in the remaining coordinate. This proves automatic existence in that case. The counterexamples in §9 prove the final assertion for $`k\ge2`$. ∎

With no controlled coordinates and exactly one hidden coordinate, a purely scalar-time energy gives a stationary Hamburger moment problem: existence follows from positivity, while uniqueness can still fail. This degenerate case is not a radial-control theorem.

There is a distinct direct proof for quadratic controlled energies that is useful to retain. Suppose $`g_t(z)=z^{\mathsf T}Q_tz`$ with $`Q_t\ge0`$ and continuous. On an interior compact interval choose $`C`$ with $`g_t\le C|z|^2`$ in the SOS order and write $`B=C|z|^2`$. The identity
```math
B^m-\prod_{j=1}^{m}g_{u_j}
 =\sum_{i=1}^{m}B^{m-i}(B-g_{u_i})
        \prod_{j\lt i}g_{u_j}
```
is SOS. Uniform Gaussian factorial bounds therefore imply
```math
A_v\!\left(q^2\prod_{j=1}^{m}g_{u_j}\right)
 \le m!(C/c)^m A_0(q^2).
```
The backward Volterra remainder has functional time $`u_m`$, as in (28). The analogous forward, alternating expansion has functional time $`u_1`$, the **earliest** time. The simplex volume makes both remainders at most
$`A_0(q^2)(C|t-s|/c)^m`$.
For $`C|t-s|<c`$, they tend to zero. Monotone convergence in the backward expansion and domination by $`q^2e^{K_{s,t}}`$ in the forward expansion give both exponential transport identities for any endpoint representative. Patching finitely many such intervals and then taking the boundary limit proves the lift without assuming joint determinacy.

This argument explains why both time directions are needed when representatives are nonunique. It is also specifically quadratic: an energy such as $`g_t(z)=z^4+t^2z^2`$ has cumulative energy $`tz^4+t^3z^2/3`$, but cannot be bounded by $`Cz^2`$. Lemmas 16–17 cover it through the Fourier projection argument, without importing that false quadratic bound. They reconcile [the original partial-control theorem][partial-control-source], [the general SOS extension][partial-sos-source], and [the arbitrary-hidden persistence theorem][hidden-persistence-source].

### 8.3 Exact information retained by fixed-subspace operations

For an actual initial law define the finite signed measures
```math
m_{\mu,\alpha}
  =(\pi_z)_*(y^\alpha\mu),
\qquad \alpha\in\mathbb N^k.
\quad\text{(41)}\quad
```
They record the controlled distribution and all hidden polynomial averages conditional on the controlled variable, in an integrated form.

**Proposition 18 (fixed-subspace continuation equivalence).** Two initial laws with all moments have the same full positive-time moment record under one schedule satisfying (36) if and only if
$`m_{\mu,\alpha}=m_{\nu,\alpha}`$ for every $`\alpha`$. This condition is also equivalent to equality of their full paths under every such schedule acting on the same controlled subspace. It identifies their moment continuation, not necessarily their joint laws.

**Proof.** At positive time the signed controlled measures weighted by $`y^\alpha`$ have a Gaussian absolute moment. Equality of all mixed moments identifies these signed measures by Fourier uniqueness. For normalized laws this says
$`Z_\mu^{-1}e^{-K_t}m_{\mu,\alpha}=Z_\nu^{-1}e^{-K_t}m_{\nu,\alpha}`$.
Invert the positive weight on these already known finite measures. For $`\alpha=0`$, integration over the controlled space gives $`1/Z_\mu=1/Z_\nu`$, since both initial laws are probabilities. This removes the scalar factor for every $`\alpha`$ and proves (41). Conversely, (41) gives every damped mixed moment and normalizer directly for any allowed controlled schedule. ∎

Thus a complete path has a unique joint lift exactly when its record is determinate at one positive time. An extension along the same supplied controlled space is unique as a **moment path**: every such extension contains the old positive-time representative and must obey the same canonical signed-projection transport. It need not identify the original joint law.

A useful sufficient condition for joint identification is determinacy of the hidden conditional law for almost every controlled value. Equality of (41) gives equal controlled marginals and, outside one common null set for the countable hidden monomials, equal conditional hidden moments. Conditional determinacy then identifies the conditional laws. No necessity statement is inferred from this argument.

An indeterminate hidden marginal does not prevent conditional identification. Let $`Z`$ be Gaussian and let $`Y=e^Z`$. Its lognormal marginal is indeterminate, but the conditional law of $`Y`$ given $`Z=z`$ is the point mass at $`e^z`$. The measures $`m_0=\gamma`$, $`m_1=e^z\gamma`$, and $`m_2=e^{2z}\gamma`$ already force the relation: any compatible joint law satisfies
$`\int(y-e^z)^2=0`$.
The nonpolynomial cross integral is legitimate because the specified conditional signed measure gives $`\int ye^z=\int e^{2z}d\gamma`$, with finiteness supplied by Cauchy–Schwarz. Under $`g_t=(1+t)z^2`$, the conditional graph persists while the hidden marginal remains a nondegenerate lognormal.

Conversely, full-support ambiguity is possible. Let $`\eta_\pm=(\mu_\pm+\gamma_1)/2`$, where (8) is embedded on the real line and $`\gamma_1`$ is a standard Gaussian. Then $`\gamma_r\otimes\eta_\pm`$ are distinct full-support joint laws with all the same mixed moments, and every fixed-subspace controlled schedule leaves their hidden factors untouched. Rank-one controlled matrices at different times may fail to commute as matrices; the scalar polynomials in the weighting factors still commute. These are different algebraic questions.

### 8.4 Enlarging the allowed operations can reveal hidden distinctions

The preceding equivalence depends on the declared controlled subspace. At a positive time $`s`$, the last example has the form
$`\zeta_s\otimes\eta_\pm`$, with a Gaussian exponential moment in the controlled variables. Activate the previously hidden coordinate by applying $`e^{-\varepsilon y^2}`$, $`\varepsilon>0`$. The resulting laws remain distinct: equal normalized hidden factors would, after inverse multiplication by $`e^{\varepsilon y^2}`$ and normalization, identify $`\eta_+`$ and $`\eta_-`$.

The new joint laws have a Gaussian exponential moment in every coordinate. They are therefore moment-determinate, so distinctness now implies a difference in at least one finite polynomial moment. This proves existence of a finite distinguishing record, not a uniform degree or a practical discovery algorithm. It does not contradict Proposition 18, because activating $`y`$ changes the admitted operation family. The complete activation argument is incorporated from [the public activation proof][activation-source].



## 9. Sharp failure with two hidden coordinates

The distinction between squares and all nonnegative polynomials is essential, not an artifact of a truncated matrix calculation. We first construct a functional on the **whole** polynomial algebra, then place it inside the dynamics.

### 9.1 A complete strictly square-positive functional without a measure

**Theorem 19 (an explicit nonmoment functional).** There is a normalized functional $`\Lambda:\mathbb R[u,v]\to\mathbb R`$, with computable dyadic values on every monomial, such that $`\Lambda(p^2)>0`$ for every nonzero polynomial $`p`$, but
```math
F(u,v)=1+u^4v^2+u^2v^4-u^2v^2\ge\frac34,
\qquad \Lambda(F)=-1.
\quad\text{(42)}\quad
```
Consequently $`\Lambda`$ has no positive representing measure.

**Proof.** Order the first ten monomial exponents as
```math
(0,0),(2,1),(1,2),(1,1),(1,0),(0,1),
(2,0),(0,2),(3,0),(0,3).
```
For total degree $`a+b\ge4`$, assign index
$`m(a,b)=b+1+(a+b)(a+b+1)/2`$. This orders successive degree blocks, giving a bijection with the positive integers.

If two distinct exponents have an integral midpoint, that midpoint occurs before the later exponent. In degrees at least four, either its total degree is smaller, or its second coordinate lies strictly between the two second coordinates in the same degree block. The exceptional low-degree pairs, stated as index pairs followed by their midpoint index, are
```math
(1,7;5),(1,8;6),(2,6;4),(2,10;3),(3,5;4),
(3,9;2),(5,9;7),(6,10;8),(7,8;4).
```
They exhaust the pairs in the parity classes
$`\{1,7,8\},\{2,6,10\},\{3,5,9\},\{4\}`$.
Thus all required off-diagonal entries below are already defined when their later index is reached.

Set $`j_1=j_2=j_3=1`$, $`j_4=4`$, and $`A_4=\mathrm{diag}(1,1,1,4)`$, with $`B_4=A_4^{-1}`$. For basis exponents $`p_i,p_j`$, the intended entry is zero when their sum has an odd coordinate, and otherwise is $`j_{m((p_i+p_j)/2)}`$. Suppose the first $`n-1`$ diagonal choices and matrices are constructed. Let $`v_n`$ be the already determined off-diagonal column, and put
```math
w_n=B_{n-1}v_n,\quad
q_n=v_n^{\mathsf T}w_n,\quad j_n=1+q_n,
```
```math
A_n=
\begin{pmatrix}
A_{n-1}&v_n\\
v_n^{\mathsf T}&1+q_n
\end{pmatrix},
\qquad
B_n=
\begin{pmatrix}
B_{n-1}+w_nw_n^{\mathsf T}&-w_n\\
-w_n^{\mathsf T}&1
\end{pmatrix}.
\quad\text{(43)}\quad
```
Direct block multiplication proves $`A_nB_n=I`$. The quadratic form identity
```math
(a,t)A_n(a,t)^{\mathsf T}
 =(a+t w_n)^{\mathsf T}A_{n-1}(a+t w_n)+t^2
```
proves strict positive definiteness by induction. The Schur complement is one, so $`\det A_n=4`$. All entries are dyadic and computed by finite rational operations; there is no unbounded search for a positive completion.

Define $`\Lambda(u^av^b)=0`$ if either exponent is odd, and otherwise define it as $`j_{m(a/2,b/2)}`$. Midpoint precedence makes every finite Gram block agree with the corresponding $`A_n`$. A nonzero polynomial uses a finite number of these basis monomials, so its square has strictly positive evaluation. Also $`\Lambda(1)=1`$ and the four terms of $`F`$ have values $`1,1,1,4`$, giving $`\Lambda(F)=-1`$.

To verify nonnegativity, put $`s=u^2+v^2`$. Then
$`F=1+u^2v^2(s-1)`$. For $`s\ge1`$ this is at least one. For $`s\le1`$, the bounds $`u^2v^2\le s^2/4\le1/4`$ and $`1-s\le1`$ give $`F\ge3/4`$. A positive measure could not integrate it to $`-1`$. ∎

Neither a large finite positive prefix nor setting an uncomputed tail to zero proves this theorem. The recursive diagonal choices need not be monotone; the predecessor computation has $`j_{11}=479723268580926`$ and $`j_{12}=5/4`$. A zero tail after the ten-term prefix can even give a negative square. The full recurrence and the proof that every polynomial lies in a compatible positive block are the essential ingredients.

The seed ordering and positive nonmoment witness belong to the classical construction discussed by [Schmüdgen](#references), *The Moment Problem*, Propositions 13.4–13.5, with attribution there to J. Friedrich. The explicit Schur-complement recurrence is the public constructive treatment incorporated from [the full algebraic proof][nonmoment-source]; this exposition does not claim a new discovery.

The formal status has also advanced beyond an early scalar-only certificate. The received later [formalization result][full-formal-source], its [independent review][full-formal-review-source], and the actual [final Lean declaration][countermodel-lean-source] establish the scope of a construction on $`\mathrm{MvPolynomial}(\mathrm{Fin}\ 2,\mathbb R)`$: a full linear functional, normalization, strict positivity for every nonzero polynomial square, the pointwise witness bound, and its negative evaluation. This is stronger than merely checking the four scalar witness values. The executable dyadic algorithm, determinant identity, and measure-integration contradiction remain distinct ordinary mathematical claims. The present chapter has not rerun that kernel build; its formal sources and verification inputs remain independently necessary.

### 9.2 Strict positivity can persist without any joint law

Apply Theorem 19 in two hidden coordinates and tensor it with Gaussian laws in any additional hidden coordinates. Denote the resulting hidden functional by $`\Lambda_k`$, $`k\ge2`$. Under an arbitrary controlled schedule satisfying (36), define
```math
A_t(p)=\int
 \Lambda_k\!\bigl(p(z,\cdot)\bigr)e^{-K_t(z)}\,d\gamma_r(z),
\qquad
L_t=\frac{A_t}{A_t(1)}.
\quad\text{(44)}\quad
```
Every evaluation is a finite sum of Gaussian polynomial integrals. Dominated differentiation proves the hierarchy. For a nonzero joint polynomial, its hidden polynomial is nonzero on a nonempty open set of the remaining variables; the Gaussian measure gives that set positive mass and the hidden functional is strictly square-positive there. Hence $`L_t(p^2)>0`$ for every nonzero $`p`$. Yet $`L_t(F)=-1`$ for every time, so no joint law exists.

This example is not necessarily stationary. Freeze a time at which the controlled energy is nonconstant. The derivative of its expectation, holding that polynomial fixed while differentiating, is minus its variance under the actual controlled Gaussian tilt, and is strictly negative. One must not include a time derivative of the polynomial itself in this diagnostic. Cumulative radial control ensures that the energy is nonconstant at some time.

This proves the sharpness of the hidden-coordinate count in Theorem 17. It does not yet start from a valid joint record. The following stronger construction does; it incorporates [the full hidden-boundary argument][hidden-boundary-source] rather than treating (44) as the answer to a different question.

### 9.3 A positive measure can dominate a nonmoment functional

The next auxiliary construction explains how an initial genuine law can conceal the nonmoment component.

**Lemma 20 (signed moment realization).** Every real array $`(c_\alpha)_{\alpha\in\mathbb N^k}`$ is the polynomial moment array of a finite signed atomic measure with every absolute polynomial moment. If $`c_0=1`$, it can be written as $`P-N`$, with $`P,N`$ positive, $`P(1)=1+N(1)`$, and $`N(1)\le1/2`$.

**Proof.** Begin with $`c_0\delta_0`$. For a multiindex $`|\alpha|=n\ge1`$ and integer $`R\ge1`$, define
```math
D_{\alpha,R}
 =\frac1{\alpha!\,R^n}
   \sum_{0\le j\le\alpha}
    (-1)^{n-|j|}\binom{\alpha}{j}\delta_{Rj}.
\quad\text{(45)}\quad
```
Repeated finite differences give
$`\int x^\beta\,dD_{\alpha,R}=\delta_{\alpha\beta}`$ whenever $`|\beta|\le n`$. Indeed, a lower total degree has some coordinate below its difference order; at equal degree, the only surviving multiindex is $`\beta=\alpha`$, with value one. For $`m\ge0`$,
```math
\int |x|^m\,d|D_{\alpha,R}|
 \le\frac{2^n n^m}{\alpha!}\,R^{m-n}.
\quad\text{(46)}\quad
```

Suppose degrees below $`n`$ have already been matched. Let $`r_\alpha`$ be the degree-$`n`$ residuals, put
$`B_n=\sum_{|\alpha|=n}|r_\alpha|2^n/\alpha!`$, and choose a strictly increasing integer
$`R_n\ge\max(1,2^n n^{n-1}B_n)`$.
The block $`\rho_n=\sum_{|\alpha|=n}r_\alpha D_{\alpha,R_n}`$ corrects that degree without changing lower degrees. For every $`m<n`$, (46) gives
$`\int|x|^m\,d|\rho_n|\le2^{-n}`$.
Thus the series of blocks converges in total variation, and for each fixed absolute moment its tail is summable. Later blocks have zero contribution to every already fixed moment, so the resulting signed measure has exactly the prescribed array.

When $`c_0=1`$, combine coincident atoms within each finite block before taking its positive and negative parts. Each block has total mass zero; therefore its negative mass is half its total variation and at most $`2^{-n-1}`$. Set
$`P=\delta_0+\sum\rho_n^+`$ and $`N=\sum\rho_n^-`$. This gives the required masses and moments. ∎

Apply the lemma to the functional $`\Lambda`$ in Theorem 19. The positive measure $`P`$ dominates that functional on squares, because $`\Lambda=P-N`$ and $`N`$ is positive. Tensor with Gaussian laws for extra hidden coordinates if needed. Write $`n_0=N(1)`$ and $`C=1+n_0`$, so $`1<C\le3/2`$; the strict inequality follows because $`N=0`$ would make $`\Lambda`$ a positive measure.

### 9.4 Immediate loss of joint representability from a genuine initial law

**Theorem 21 (valid-initial escape).** With at least two hidden coordinates, there are normalized, strictly square-positive, coordinatewise $`C^1`$ hierarchies satisfying (36) (smooth for autonomous energies) whose initial record is represented by a genuine probability with all moments, but which have no representing measure at any positive time. Their initial record is indeterminate. The theorem makes no such assertion for a determinate joint initial record.

**Proof.** On one controlled coordinate, let $`\alpha_1`$ be the continuous standard lognormal law. Define the discrete law
```math
\beta_1=\frac1S\sum_{j\in\mathbb Z}e^{-j^2/2}\delta_{e^j},
\qquad S=\sum_{j\in\mathbb Z}e^{-j^2/2}.
\quad\text{(47)}\quad
```
For every integer $`m\ge0`$, shifting the index in the sum gives
$`\int z^m\,d\beta_1=e^{m^2/2}=\int z^m\,d\alpha_1`$.
Tensor both with the same Gaussian in the other $`r-1`$ controlled coordinates, obtaining $`\alpha,\beta`$. They have equal moments and are mutually singular: for
$`E=\{z:z_1=e^j\text{ for some }j\in\mathbb Z\}`$,
$`\alpha(E)=0`$ and $`\beta(E^c)=0`$.

Use the positive measures $`P_k,N_k`$ from Lemma 20, with $`\Lambda_k=P_k-N_k`$, and put
```math
\alpha_t=e^{-K_t}\alpha,\quad \beta_t=e^{-K_t}\beta,
\qquad
A_t=\frac{\alpha_t\otimes\Lambda_k+\beta_t\otimes N_k}{C},
\qquad L_t=\frac{A_t}{A_t(1)}.
\quad\text{(48)}\quad
```
The expression defines a polynomial functional; it is not asserted to be a positive joint measure. Its mass
$`A_t(1)=(\alpha_t(1)+n_0\beta_t(1))/C`$ is positive. Strict positivity on every nonzero square follows from the first tensor term: the controlled law has positive density on an open half-space, the remaining Gaussian factors are positive on open sets, and $`\Lambda`$ is strictly square-positive. The second term is positive. Finite polynomial expansion and domination by the original all-moment measures justify the hierarchy and all needed derivatives.

At zero, the equal controlled moments make (48) agree on every polynomial with the genuine probability
$`\mu_0=\alpha\otimes(P_k/C)`$.
It also agrees with $`\beta\otimes(P_k/C)`$. Those two laws are distinct, so the initial record is indeterminate.

Fix $`t>0`$. If a positive measure $`\nu`$ represented $`A_t`$, then the controlled exponential moment obtained from its moments would be finite, because $`K_t\ge c|z|^2`$. The measure
$`\sigma=(\pi_z)_*(F\nu)`$ would be positive, since $`F\ge3/4`$. Cauchy–Schwarz with $`F^2`$ gives a Gaussian absolute moment for $`\sigma`$ at a smaller rate. Its polynomial moments, from (48), are those of
```math
w_t=\frac{-\alpha_t+N_k(F)\beta_t}{C}.
\quad\text{(49)}\quad
```
The latter signed measure also has a Gaussian absolute moment. Signed moment uniqueness therefore gives $`\sigma=w_t`$. But
$`w_t(E^c)=-\alpha_t(1)/C<0`$, contradicting positivity. Hence no positive-time representative exists. ∎

The genuine initial law $`\mu_0`$ also has its ordinary tilt, which is a second, realizable hierarchy with the same initial record. For autonomous controlled energy, both paths are smooth and all their initial derivatives agree, because repeated hierarchy differentiation uses only initial polynomial moments. Thus full initial jets do not exclude this escape. The all-or-none statement of Theorem 17 concerns **positive times** and does not turn a valid boundary point into a positive-time representative.

There is also a finite polynomial separator at every positive time. Let $`m_t=\alpha_t+\beta_t`$. Polynomials are dense in $`L^2(m_t)`$: a function orthogonal to them would define a signed measure with a Gaussian absolute moment, by Cauchy–Schwarz, and with all moments zero; Fourier uniqueness makes that measure zero. Choose a nonzero smooth controlled function $`\phi`$ supported in a strip $`1<z_1<e`$. The discrete measure gives it zero mass while the continuous measure gives positive mass. Thus $`\int\phi^2\,dw_t<0`$. Approximate $`\phi`$ in $`L^2(m_t)`$ by polynomials $`q_n`$. The density of $`w_t`$ relative to $`m_t`$ is bounded, and $`q_n^2\to\phi^2`$ in $`L^1(m_t)`$, so some $`q_n`$ satisfies
$`L_t(q_n(z)^2F(y))<0`$ although $`q_n^2F\ge0`$ pointwise. This is an existence proof for a finite separator. Its later effective and explicit refinements appear in §10.

The signed-moment construction and the escape theorem incorporate [the genuine-initial escape proof][valid-initial-escape-source]. The earlier permanently invalid path (44) remains a useful independent control; it is not substituted for this stronger result.

### 9.5 Every fixed finite prefix can remain genuinely valid

**Theorem 22 (finite-prefix validity delay).** Let $`L_t`$ be a normalized polynomial-coordinate path continuous at zero. Suppose $`L_0`$ is an actual all-moment probability functional and $`L_0(q^2)>0`$ for every nonzero polynomial $`q`$. For each total degree $`D`$, there is $`\varepsilon_D>0`$ such that, for $`0\le t<\varepsilon_D`$, the restriction of $`L_t`$ to degree at most $`D`$ is represented by a probability on at most
$`\binom{d+D}{D}`$ atoms. Moreover $`L_t(P)>0`$ for every nonzero globally nonnegative polynomial of degree at most $`D`$.

**Proof.** Let $`V_D`$ be the finite-dimensional coefficient space of those polynomials, and let $`C_D`$ be its closed cone of globally nonnegative polynomials. A nonzero $`P\in C_D`$ has $`L_0(P)>0`$: otherwise positivity of the representing measure would give $`P=0`$ almost surely and thus $`L_0(P^2)=0`$, contrary to strict square positivity. The intersection of $`C_D`$ with the coefficient unit sphere is compact. Hence $`L_0`$ has a positive minimum $`\delta_D`$ there. Coordinate continuity makes the dual norm of $`L_t-L_0`$ less than $`\delta_D/2`$ for sufficiently small $`t`$. This proves strict positivity uniformly on that cone.

Let $`v_D(x)`$ be the vector of monomials through degree $`D`$, and let $`M_D`$ be the conic hull of its evaluation vectors. Its dual cone is exactly $`C_D`$, so finite-dimensional separation gives $`\overline{M_D}=C_D^*`$. The strict margin just obtained places the moment vector of $`L_t`$ in the interior of $`C_D^*`$. This is an ordinary full-dimensional interior: the evaluation vectors span the space, since a polynomial vanishing at every point is zero.

For a full-dimensional convex set, the interior of its closure equals its interior. One direct proof chooses a small simplex around an interior point, approximates its vertices by points of the original convex set, and keeps the point inside the perturbed simplex by continuity of the positive barycentric coordinates. Thus this moment vector belongs to $`M_D`$ itself, not merely to its closure. Conic Carathéodory reduces its representation to at most $`\dim V_D=\binom{d+D}{D}`$ evaluation vectors. The constant coordinate is one, so their nonnegative weights sum to one. ∎

Apply this theorem to (48). At every positive time the complete record is invalid, yet each fixed finite degree remains exactly representable on its own initial interval. The least degree of **any** nonnegative polynomial separator therefore tends to infinity as time approaches zero. This strengthens the corresponding conclusion for separators of the special form $`q^2F`$. The finite representing laws need not be compatible across degrees, have a common support, or extend to a joint representing law. No effective bound on $`\varepsilon_D`$ is claimed.

The theorem also covers odd $`D`$ and $`D=0`$; it does not require the cone of nonnegative polynomials itself to span $`V_D`$. The full finite-prefix proof and its later completed review are incorporated from [the finite-prefix refinement][finite-prefix-source] and [its independent review][finite-prefix-review-source]. An earlier pending-review label does not override that received successor.



## 10. Effective recovery and finite certificates

The preceding existence and uniqueness theorems concern exact mathematical records. They neither supply a practical finite-data reconstruction method nor make validity or determinacy decidable. Some effective statements are nevertheless available under explicit input promises.

### 10.1 Computing an actual determinate law from all its moments

A **uniform moment name** is an oracle which, on input $`(r,k)`$, returns a rational number within $`2^{-k}`$ of the $`r`$th moment. Giving a finite prefix, or giving separate nonuniform existence claims for each moment, is weaker.

**Theorem 23 (promised determinate recovery).** Given a uniform moment name, promised to be the valid moments of a Stieltjes-determinate probability $`\mu\in\mathcal P_\infty([0,\infty))`$, one can compute the law in the weak topology and in ordinary $`W_1`$, every normalized tilt by $`e^{-tx}`$ for computable $`t\ge0`$, all its polynomial moments, and any finite set of its time derivatives. The procedure is uniform under the promises; it does not decide validity or determinacy and has no asserted practical complexity bound.

**Proof.** Compactify by $`y=x/(1+x)`$ and work in the probability measures on $`[0,1]`$ with their $`W_1`$ metric. This is effectively compact. Explicitly, move a probability onto the grid $`j/n`$, then round the first $`n`$ weights down to multiples of $`1/Q`$ and place the remainder at the final grid point. The resulting finite list of rational atomic laws is a $`(1/n+n/Q)`$ net. By refining nets and checking a positive margin, finite covers by rational open balls can be semidecided; a genuine finite cover has a positive Lebesgue margin.

Define the continuous clipping functions
```math
c_N(y)=\min\!\left(\frac{y}{1-y},N\right),\quad c_N(1)=N.
```
They are Lipschitz with constant $`(1+N)^2`$, and $`c_N^r`$ has Lipschitz constant $`rN^{r-1}(1+N)^2`$. The compactified representing fibre is exactly the set of probabilities $`\lambda`$ satisfying, for every $`r,N\ge1`$,
```math
m_r-\frac{m_{r+1}}N
 \le\int c_N^r\,d\lambda\le m_r.
\quad\text{(50)}\quad
```
The tail inequality $`x^r-\min(x,N)^r\le x^{r+1}/N`$ proves necessity. Conversely, the upper bound for $`r=1`$ excludes an atom at $`y=1`$. Monotone convergence and both bounds as $`N\to\infty`$ give exactly every prescribed moment.

Strict violations of (50) are semidecidable open conditions, by the uniform names and the explicit Lipschitz constants. Thus this fibre is an effectively closed subset of an effectively compact space. The determinacy promise makes it a singleton. To approximate its point, enumerate rational atomic centers $`q`$ and search for a finite cover of the whole probability space by $`B(q,\varepsilon)`$ together with finitely many enumerated open pieces of the fibre's complement. Such a cover certifies that the singleton lies in that ball. Some search terminates because there is a rational center close enough to the point. This is an explicit instance of effective compact singleton extraction; see [Galatolo, Hoyrup and Rojas](#references).

To recover a law on the original half-line, push the rational approximation through $`c_R`$. If $`H>m_1`$, the mass beyond $`R`$ is at most $`H/R`$, while compactified $`W_1`$ error is magnified by at most $`(1+R)^2`$ on the clipped part. For ordinary $`W_1`$, the discarded first-moment tail is at most $`m_2/R`$. Computable rational upper bounds on these moments therefore give an effective original-space approximation.

For tilted moments, let $`U>t`$ be rational and use the clipped integrand
$`c_R(y)^r e^{-t c_R(y)}`$. For $`r\ge1`$ it is bounded by $`R^r`$ and has the explicit Lipschitz bound
```math
\bigl[rR^{r-1}+UR^r\bigr]\bigl(1+R\bigr)^2.
\quad\text{(51)}\quad
```
For $`r=0`$ use $`U(1+R)^2`$. Changing $`t`$ by $`\Delta t`$ changes the clipped integral by at most $`R^{r+1}|\Delta t|`$. The unclipped tail error is at most $`2m_{r+1}/R`$ for $`r\ge1`$, and at most $`m_1/R`$ for $`r=0`$. This computes
$`A_r(t)=\int x^r e^{-tx}d\mu`$, including $`t=0`$ without trying to decide whether a real input is exactly zero.

Jensen's inequality gives $`Z(t)\ge e^{-Um_1}`$, so a computable positive rational lower bound $`D`$ is available. If numerator and denominator are approximated within $`\eta<D/2`$ and the true numerator is at most $`K`$, the quotient error is at most
$`2\eta/D+2K\eta/D^2`$. Hence every normalized moment is computable. The identity $`A_r'=-A_{r+1}`$ supplies finite derivatives. On bounded time intervals,
$`|A_r'|\le m_{r+1}`$ and
$`|m_r'|\le m_{r+1}/D+m_rm_1/D^2`$, providing effective continuity as well. The actual tilted law follows by weighted integration or by applying the same recovery argument to its now computed determinate moment record. ∎

One can equivalently place computable upper envelopes $`B_r>m_r`$ on all clipped integrals. On that effective compact class, the bound $`B_{r+1}/R`$ makes each unbounded moment a uniformly computable continuous functional. This is the tail control behind the proof, not an implicit appeal to computability of arbitrary unbounded integrals from weak convergence. The relevant effective integration framework is developed by [Hoyrup and Rojas](#references).

Computability need not come from a convergent Taylor series. The density $`\tfrac12e^{-\sqrt x}`$ on $`[0,\infty)`$ has moments $`(2r+1)!`$ and no positive exponential moment in $`x`$. It is nevertheless determinate. Given any competitor, symmetrize $`Y=\pm\sqrt X`$. For $`0<b<1`$, the even moment series gives
```math
E\cosh(bY)=\sum_{r=0}^{\infty}(2r+1)b^{2r}
          =\frac{1+b^2}{(1-b^2)^2}<\infty.
```
Both symmetric laws have an exponential absolute moment and the same moments, hence are equal; squaring identifies the original laws. Yet the ratio of successive absolute terms in the formal Laplace series is
$`|t|(2r+3)(2r+2)/(r+1)`$, tending to infinity. Theorem 23 computes the continuation despite zero Taylor radius at the origin.

A calibrated Fisher jet can be another input format, but only with its actual-law and fixed-parameter promises. If $`F(t)=\log Z(t)`$, $`q=-F'`$, and $`V=F''`$, then
```math
\kappa_1=q(0),\qquad
\kappa_n=(-1)^nV^{(n-2)}(0)\quad(n\ge2),
```
```math
m_{n+1}=\sum_{j=0}^{n}\binom nj\,\kappa_{j+1}m_{n-j},
\qquad m_0=1.
\quad\text{(52)}\quad
```
The second relation follows by differentiating the exponential generating identity between moments and cumulants coefficient by coefficient; only finitely many quantities enter each coefficient. It converts a uniform calibrated jet name into a moment name. An uncalibrated metric jet does not determine the missing mean or parameter scale, and no nonsingular inverse mean coordinate is automatically supplied.

There is a readout-only variant. If a computable continuous readout on an effectively compact representing fibre is promised constant there, its image is an effectively compact singleton and the same extraction computes that common value, even when the law is not unique. For the entire half-line mean continuation, constancy over the fibre is equivalent to determinacy, by Laplace uniqueness. Neither fibre constancy nor determinacy is decided by the extraction.

Two controls show why the promises matter. For any finite cutoff $`D`$, put $`n=D+1`$ and distribute the binomial weights $`\binom nj/2^{n-1}`$ on the even, respectively odd, integers $`j\in\{0,\ldots,n\}`$. Finite differences show equality of the first $`D`$ moments. Their probability generating functions are
$`[(1+z)^n\pm(1-z)^n]/2^n`$.
With $`h(z)=((1-z)/(1+z))^n`$, the difference of their logarithmic derivatives contains $`2h'(z)/(1-h(z)^2)`$, which is nonzero at $`z=1/2`$. Thus their damped means differ at $`t=\log2`$.

Moreover a weakly computable law need not have computable unbounded moments. For a machine that halts at a late stage $`j`$, use
$`(1-1/j)\delta_0+(1/j)\delta_j`$; if it never halts, use $`\delta_0`$. A finite simulation approximates the law weakly uniformly, because a late halt changes only mass at most $`1/j`$. Its mean, however, is the halting bit. This family does not provide the uniform moment name required above. Nor does Theorem 23 recover an indexed hidden $`\ell^1`$ representation from an unlabelled law. The complete argument is incorporated from [the exact original effectivity proof][effective-law-source], including the corrected bound (51).

### 10.2 What can be detected by enumerating negative witnesses?

Under the promise of an exact coercive hierarchy with computable coefficients and uniformly certified polynomial coordinates at rational times, Theorem 12 gives a semidecision for failure of realizability somewhere: if the path is not representable, it cannot be square-positive throughout. Some square evaluation is strictly negative. Continuity and finite dependence on polynomial coefficients give a rational time and rational-coefficient polynomial with the same strict sign. Dovetailing their certified upper bounds eventually finds such a witness. A negative boundary value also persists at a nearby positive time. This does not verify a positive path in finite time, decide the hierarchy promises, or provide a uniform degree or running time. It is different from the hidden-coordinate case, where **every** square may remain positive and a nonnegative nonsquare witness is needed.

For the explicit valid-initial escape (48), that second type of witness can also be searched effectively in one controlled coordinate with energy $`g=z^2`$ and two hidden coordinates. The Schur values are rational, and the finite-difference construction uses computable rational residuals and a least admissible integer radius at each step. For a hidden polynomial $`p`$ of degree $`d`$, the uncomputed positive/negative-block tail after degree $`M\ge d`$ is bounded by its coefficient-sum constant times $`2^{-M}`$. In particular,
$`N(F)`$ has a tail bound $`4\cdot2^{-M}`$, and $`n_0=N(1)`$ has bound $`2^{-M-1}`$.

Define at a fixed rational $`t>0`$
```math
I_m(t)=E[e^{mZ-te^{2Z}}],
\qquad
J_m(t)=\frac1S\sum_{j\in\mathbb Z}
 e^{-j^2/2+mj-te^{2j}}.
```
For $`R>m`$, the continuous tails are at most
$`2e^{m^2/2}e^{-(R-m)^2/2}`$. On $`[-R,R]`$, the integrand derivative is bounded by a computable multiple of
$`(m+2te^{2R}+R)e^{mR}`$, giving certified interval quadrature. If $`J+1\ge\max(1,4m)`$, the discrete tail is bounded by
```math
\frac{2e^{-(J+1)^2/4}}{1-e^{-(2J+3)/4}},
```
and $`S\ge1`$. Thus all these quantities and the full coordinates
```math
L_t(z^mu^av^b)=
\frac{\Lambda(u^av^b)I_m(t)+N(u^av^b)J_m(t)}
     {I_0(t)+n_0J_0(t)}
\quad\text{(53)}\quad
```
are uniformly computable. Jensen's inequality supplies the positive denominator bound
$`I_0+n_0J_0\ge(1+n_0)e^{-te^2}`$.

Set $`B=N(F)`$ and, for a rational polynomial $`q`$, put
```math
W_t(q)=-I_t(q^2)+B J_t(q^2),
\qquad
L_t(q^2F)=\frac{W_t(q)}{I_0+n_0J_0}.
\quad\text{(54)}\quad
```
The existence argument after Theorem 21 gives a real polynomial with negative $`W_t`$; finite-degree continuity gives a rational one. Enumerate rational polynomials and precision requests, dovetailing strict negative upper bounds. The search terminates at every fixed rational positive time. It is $`q^2F`$ that is nonnegative; $`q`$ need not be. If the certified intervals are $`W_t\in[w_l,w_h]`$ with $`w_h<0`$ and denominator $`D\in[d_l,d_h]`$ with $`d_l>0`$, the correct normalized interval is
```math
L_t(q^2F)\in[w_l/d_l,\ w_h/d_h].
\quad\text{(55)}\quad
```
The order of the denominator endpoints reflects the negative numerator.

This is a proof of a terminating search under exact input promises, not a claim that a generic search was executed here. The least degree can diverge near zero. For this special family, $`W_0(q)=(B-1)\int q^2d\alpha`$ and $`B-1=P(F)>0`$, so every fixed-degree quadratic form remains positive on some initial interval. Theorem 22 is stronger: it protects the entire finite truncated moment problem, not just the family (54). These effective refinements incorporate [the corrected witness-search proof][effective-escape-source] and preserve [its review's actual first corrections][effective-escape-review-source].

### 10.3 An actually computed sparse separator

The later public work goes beyond existence and a terminating-search proof. For $`t=1`$, it supplies the explicit polynomial
```math
H(z,u,v)=z^{2048}F(u,v),
\qquad
-3^{2097161}\lt{}L_1(H)<-\frac43.
\quad\text{(56)}\quad
```
It has four monomials, total degree $`2054`$, and is nonnegative everywhere. This is the square choice $`q=z^{1024}`$ in (54). The analytic bounds are given here, while the exact finite hidden-arithmetic input remains a separately retained computational dependency.

That input is the strict rational bound $`B=N(F)<2^{171}`$, obtained by summing the negative parts of the finite-difference blocks through degree six and adding the tail $`1/16`$. The exact radii used are
```math
\begin{aligned}
R_1&=1,& R_2&=544,& R_3&=5326848,\\
R_4&=1210631850670080,\\
R_5&=114502302747635522324083834880000,\\
R_6&=1631190472850543123295836647062767816302697363159516479654977517978.
\end{aligned}
```
Only Schur indices through ten are needed for this hidden polynomial. The finite atomic counts through degree six are $`0,5,7,13,19,26`$. The source and its independent review report exact rational reproduction of this bound. Their arithmetic input and checker are retained; reading the result and review does not constitute a fresh execution of those files.

For the continuous term, on $`x\in[69/20,7/2]`$ the exponent is bounded by
```math
2048x-e^{2x}-x^2/2
 >2048\frac{69}{20}-1097-\frac{49}{8}
 =\frac{238499}{40}>5962,
```
using $`e^7<1097`$. Since the interval length is $`1/20`$, $`1/\sqrt{2\pi}>1/3`$, and $`e^5>60`$,
```math
I_{2048}(1)>\frac{e^{5962}}{60}>e^{5957}.
```
For the lattice exponent $`h(j)=2048j-j^2/2-e^{2j}`$, the sum over $`j\le2`$ is less than $`2e^{4096}`$. At $`j=3`$, $`h(3)<5740`$ because $`e^6>400`$; at $`j=4`$, $`h(4)<5204`$ because $`e^8>2980`$. For $`j\ge4`$,
$`h(j+1)-h(j)=2048-j-1/2-(e^2-1)e^{2j}<-1`$.
Thus the remaining tail is less than $`2e^{5204}`$. The two outer contributions together are less than $`e^{5740}`$, since $`e^{536}>4`$. Dividing by $`S\ge1`$ yields
```math
J_{2048}(1)<2e^{5740}\lt{}e^{5741}.
```
Since $`2^{171}<e^{171}`$, the witness numerator satisfies
$`W_1<-e^{5957}+e^{5912}<-2`$.
The denominator is at most $`1+n_0\le3/2`$, so $`L_1(H)<-4/3`$.

For the lower bound, $`W_1\ge-I_{2048}(1)\ge-e^{2048^2/2}>-3^{2097152}`$.
Jensen gives the denominator at least $`I_0(1)\ge e^{-e^2}>e^{-9}>3^{-9}`$. Dividing gives the lower bound in (56). The elementary inequalities used above can all be certified by finite rational Taylor sums and geometric remainder bounds; the source uses orders $`12,20,30,40,50,60`$ for exponents $`1,2,5,6,7,8`$ respectively. No floating eigenvalue, quadrature estimate, or numerical sign guess enters this separator proof.

The [computed separator result][computed-separator-source] and [independent exact-arithmetic review][computed-separator-review-source] supersede the older statement that no actual separator had been computed. They do not turn this chapter's source receipt into a new run, a general complexity result, or a reason to discard its unique computational inputs.



## 11. What the consolidated results establish

A hierarchy is a record of how expectations must change. Its equations alone do not make the record a probability law, and a law-level existence theorem alone does not make the record identify its law. The results above give the following exact distinctions.

| State and operation class | Sufficient record or condition | Warranted conclusion |
|---|---|---|
| Known finite numerical support of size $`N`$ | Moments through degree $`N-1`$ | Exact finite closure and complete continuation under the specified linear controls |
| Fixed compact numerical support | All polynomial moments | Unique law and exact bounded exponential reweighting |
| Half-line linear damping | Actual realizability, or nonnegative hierarchy plus one positive-time representative | Unique initial law for each complete realizable path; multiple paths can share an indeterminate initial record |
| Half-line coordinate-positive hierarchy | Valid initial record satisfying Stieltjes–Carleman | Actual evolution forced; mere initial determinacy is insufficient |
| Autonomous coercive polynomial energy | Full square positivity and the full hierarchy | Joint existence, positive-time determinacy, and exact exponential tilt |
| Arbitrary signed polynomial energy | Full square positivity and determinacy of every initial square-weighted energy distribution | Exact tilt on its actual weighted-integrability horizon |
| Time-dependent SOS energy | Cumulative radial SOS control from the origin | Joint existence and positive-time determinacy, even with instantaneously rank-one rates |
| Fixed controlled subspace with one hidden coordinate | Full joint square positivity and cumulative control | Joint existence, possible ambiguity, and exact signed-projection continuation |
| Fixed controlled subspace with at least two hidden coordinates | The preceding conditions alone | No automatic joint existence; a valid initial record may lose it immediately |
| Uniform full scalar moment name | Promised validity and Stieltjes determinacy | Computable law and nonnegative tilt, without a finite validity test or complexity guarantee |

For actual laws under a fixed operation, inverse positive weighting preserves null sets. At the polynomial-functional level, Corollary 14 establishes the stronger algebraic null-ideal identity for every autonomous square-positive hierarchy, even before joint existence is known. Neither statement supplies quantitative stability. Likewise, the rank of a cumulative energy form measures which directions its weighting controls; it is not a covariance rank, a dimension of persons, or a count of independent scientific explanations.

The counterexamples also distinguish different failures. The lognormal pair gives two genuine laws with the same complete initial record and different future responses. The scalar atom-deletion example begins with a determinate law but preserves only coordinate positivity. The hidden-coordinate escape preserves strict positivity of every square and begins with a genuine **indeterminate** joint record. Its explicit nonsquare witness and the finite-prefix delay theorem show why arbitrarily many successful finite tests do not imply full realizability.

Some conditions can be checked within narrower models, but the general statements do not supply uniform finite certificates of success. No degree cutoff independent of the support is available for compact moment recovery. No uniform detecting degree near time zero follows for the escape examples. A computable complete record under a determinacy promise need not yield a stable or efficient inverse, and positive-time analyticity need not extend to the initial boundary. For the lognormal examples, $`\int e^{cX}d\mu=\infty`$ for every $`c>0`$: the term $`ce^z`$ overwhelms the Gaussian exponent in logarithmic coordinates. The bounded perturbations in (8) preserve this divergence. Thus forward nonnegative damping cannot be promoted to unrestricted signed amplification.

A point-concentration defect is also too coarse to distinguish the relevant unbounded states. If it is defined as $`1-\sup_x\mu(\{x\})`$, it equals one for every atomless law, including distinct continuous moment-equivalent laws and many determinate ones. It does not decide moment determinacy, continuation equivalence, or the admissibility of a new operation.

The exact hierarchy remains indispensable. For example, taking the flat function $`b=1-\varepsilon e^{-1/t}`$, setting the odd moments to zero and $`A_t(x^{2n})=(-1)^n b^{(n)}(t)`$ gives a formal solution for the coercive energy $`h=x^2`$ with initial record $`\delta_0`$. But $`A_t(x^4)=\varepsilon e^{-1/t}(2t-1)/t^4`$ is negative for $`0<t<1/2`$. Coercivity does not repair a violation of the square-positivity hypothesis. Conversely, with $`h=0`$, Theorem 19 gives a constant strictly square-positive nonmoment hierarchy; the lack of compact energy fibres is substantive.

The arguments here do not decide whether additional hypotheses can prevent hidden-coordinate escape from every **jointly determinate** initial law. They do not classify all noncoercive polynomial energies, general polynomial transport flows without polynomial inverses, or continuously varying signed schedules on unbounded state spaces. Those questions require their own hypotheses and evidence. The proofs do settle the previously narrower gaps addressed here: arbitrary coercive polynomial energies, general controlled SOS rates, all-or-none positive-time joint representation, the full nonmoment functional, an actual sparse escape certificate, and exact finite-prefix representability.

For Orthemology, these results provide a rigorous account of what a numerical tensor state does and does not preserve under corrective reweighting. They can support a theory of inquiry only after its state variables, observations, and admissible operations are specified. They do not establish that a tensor is a complete semantic state, that numerical symmetry identifies distinct cognitive roles, or that a finite-dimensional probability model constitutes the original unfinished n-person noetic field. The accepted papers retain their editions and scientific authority; constructive companions and broader geometric programmes remain distinct. The present contribution is the coherent mathematical treatment of this particular family of state, existence, continuation, and diagnostic problems.

## References

1. Marc Harper. *Information Geometry and Evolutionary Game Theory*. 2009. [arXiv:0911.1383](https://arxiv.org/abs/0911.1383), especially §§2.2–2.4 for the Fisher–Shahshahani setting.
2. Konrad Schmüdgen. *Ten Lectures on the Moment Problem*. 2020. [arXiv:2008.12698](https://arxiv.org/pdf/2008.12698). Theorems 1.9, 1.12, 1.15 and 2.7 supply the Haviland, Hamburger, Stieltjes and Stieltjes–Carleman statements; §2.1 treats indeterminate lognormal examples.
3. Mihai Putinar and Konrad Schmüdgen. *Multivariate Determinateness*. 2008. [arXiv:0810.0840](https://arxiv.org/pdf/0810.0840), Theorem 25 for the multivariate Carleman existence and uniqueness conditions. The stronger base hypothesis in Theorem 31 and Corollary 32 is kept separate.
4. Konrad Schmüdgen. *Chapter 12: The Moment Problem on Compact Semi-Algebraic Sets (Revised Version)*. 2023. [arXiv:2309.10052](https://arxiv.org/pdf/2309.10052), Corollary 12.34(iv).
5. Konrad Schmüdgen. *The Moment Problem*. Graduate Texts in Mathematics 277. Springer, 2017. [DOI:10.1007/978-3-319-64546-9](https://doi.org/10.1007/978-3-319-64546-9). Propositions 13.4–13.5 and the chapter's historical notes give the classical nonmoment-functional antecedent. [Public text](https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf).
6. Christian Berg and J. P. R. Christensen. “Density questions in the classical theory of moments.” *Annales de l'Institut Fourier* **31**(3), 99–114, 1981. [DOI:10.5802/aif.840](https://doi.org/10.5802/aif.840); [full text](https://www.numdam.org/article/AIF_1981__31_3_99_0.pdf). Theorem 7 is the full-atom-deletion result used in Proposition 7.
7. Zenon Jan Jabłoński, Il Bong Jung and Jan Stochel. *A Non-hyponormal Operator Generating Stieltjes Moment Sequences*. 2011. [arXiv:1110.0249](https://arxiv.org/pdf/1110.0249), §2.1, especially the Krein extremal measure and its zero atom.
8. Markus Kuba and Alois Panholzer. *On Moment Sequences and Mixed Poisson Distributions*. 2014 author version. [Full text](https://www.dmg.tuwien.ac.at/kuba/preprintMomseq.pdf), Lemma 1. Its Hamburger Carleman formulation is distinguished from the Stieltjes transfer proved in Theorem 8.
9. Stefano Galatolo, Mathieu Hoyrup and Cristóbal Rojas. *Dynamics and Abstract Computability: Computing Invariant Measures*. [Author text](https://members.loria.fr/MHoyrup/computinvmeas.pdf), §2, especially Proposition 1, Remark 4 and Lemma 2.12 for effective compactness, singleton extraction and probability-measure spaces.
10. Mathieu Hoyrup and Cristóbal Rojas. *Computability of Probability Measures and Martin-Löf Randomness over Metric Spaces*. [Author text](https://members.loria.fr/MHoyrup/random_metric.pdf), especially §4.3 for effective integration.

The public Orthemology proofs cited in the text authenticate the particular statements and corrections consolidated here. They are linked at fixed historical editions so that the derivations can be compared without making historical file reconstruction part of ordinary reading. Full mathematical arguments are given above; the accompanying source-incorporation review distinguishes redundant prose from independently necessary formal, computational and review evidence.



[activation-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/research-v6/type_collective/cumulative_damping_prose/ACTIVATION_BOUNDARY.md
[coercive-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/204f63e544b1afd9538230f95f8ebfbc613b9847c579dfb901de6d10e40ebb10/coercive-square-positivity-20261010__RESULT.md
[computed-separator-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/8e026e569b52b6495050111ce92a063291d298c6e496a13775c5fa222dc99ff6/COMPUTED_SEPARATOR_REVIEW.md
[computed-separator-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/b04978552464b25a93fe39c4a61ccf80dcf64bc04e17c23ff6fd6242667f1a20/RESULT.md
[coordinate-computation-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/862a4b005351c1f980e1daf2820d8d871fa16835d53029ce27941244d248915f/RESULT.md
[coordinate-counterexample-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/cafc520026c66f94442346ff308ed4e202d70e10be8963b8a24ad17bda4e1e0a/RESULT.md
[coordinate-diagnostic-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/5d0e97c5f4e50ac7981765292b6aa161076a4d0b6af7fbc46aa18e40bd89c2b2/DIAGNOSTIC.md
[countermodel-lean-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/7ebe9f1bc3b7e7e8d7fb966a5b0c82f7fa9a53d84e6d0887b260847fed1e443e/Countermodel.lean
[cumulative-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/6405258b6c2523f2e28d06d5cb9cb054fa876aa3744690856e79cc078dbd62ea/REVIEW.md
[cumulative-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/a530a5341497e3416345a7ec325e986a7e54f2c254954f80fd32f1f596e6244f/RESULT.md
[effective-escape-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/c4205f111e660f91a8f28f6987351af64f71dae95246c564055843e895132db4/REVIEW.md
[effective-escape-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/dbfb6e5190a12d943c4f2530350ad66760f1f093fe631b3c6884de5ab38d00d5/RESULT.md
[effective-law-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/9661eef2d88370d2d996e68f666777c6ac0ffb93155d102ec50873f155e91383/RESULT.md
[finite-prefix-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/477b75c8887e768f130b475f9e07516584e5780ce78f93d7a291c9fa0423d492/REVIEW.md
[finite-prefix-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/f7f06518e210b860502c0971aa9ad47a410198d84c519b149a49b953f67c242f/RESULT.md
[finite-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/03f027122c0a908f1f6bcfcc61951223ca1fca547d8599aac2aa3437e3c01a11/RESULT.md
[full-formal-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/e9f8ac99e4df6f23171028bcd3ef99eb562f69e2229e056ec3a13fbf3954ccec/REVIEW.md
[full-formal-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/d15611cd809d5aeeda80a124d1ef524b4ddf13f1b3fb1d55e2a51db49b6ecc97/RESULT.md
[hidden-boundary-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/12d3e23f4f01f934cce554503368ccc2755ad8cef9055c432380f7b6271abd3f/SHARP_HIDDEN_BOUNDARY.md
[hidden-persistence-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/cf9b6626b24329f8dd27d2ff2d78027ea4e222f45a6b7621209aa4d39b840fe3/RESULT.md
[moment-boundary-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/a0fa9117ff47df9f07133c1ed49c682c7c2e73d20881e83f3c242dfb3faeb9e3/RESULT.md
[nonmoment-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/08fdec67591a4a0639fa4ca721293bd8c480ec405dcd1a7c5a08d3244aa84c80/PROOF.md
[partial-control-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/047ec278a738cdc018b7118113afa93a8fa6d0aa1a315d33440f2aa0586a53ea/RESULT.md
[partial-sos-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/9f20a6b0125b98a659d87b0a3758630b4e3ded99ba376e1bf4fbcc31d49765db/GENERAL_SOS_BRIDGE.md
[scalar-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/c5aeeeed56b5bf5edfa9b87570249f142e3d1be9c06218d8007013c66f5eb688/RESULT.md
[signed-earlier-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/adbbea04d51ac90692d167c5d522fa4cda23558dcc2e093c6bcf76e24f3a3553/RESULT.md
[signed-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/a297237142d62fb1cb655dc08844103f60044fa4035cc865aa11fa94d8d5b2f8/REVIEW.md
[signed-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/2ac90188cc0cb17d3bb80f3ba63d9dfe62742db5919cf86d7001c7e0baf39e55/RESULT.md
[tensor-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/448ace340a04d56aaa26b1cab0d7f720dcda56c3fe1a37bdff76c8375c30ad07/tensor-realizability-independent-review-20261010__REVIEW.md
[tensor-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a/tensor-realizability-extension-20261010__RESULT.md
[valid-initial-escape-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/c6dc162591a6827b8ae09a3b0be902ee53573435ae5b4f4ecfb1fc66ed835ada/RESULT.md
