# Independent review: same-threshold cross-command replay

Prepared independently before receipt of the frozen author manifest. This file is a mathematical review, not an integration or closure decision.

## 1. Necessary model statement

Let m be a fixed finite positive integer and n a positive integer. Route j carries a pair (U_j,V_j), with different route pairs mutually independent. Each U_j and V_j is uniform on [0,1]; within-pair dependence may differ by route. Let alpha,beta map [0,1] into [0,1], share the same calibration across every route, and preserve 0 and 1. Define

C_j(a,b) = P(U_j <= alpha(a), V_j <= beta(b)).

Consequently C_j(a,1)=alpha(a), C_j(1,b)=beta(b), C_j(a,0)=C_j(0,b)=0. These common-marginal identities, rather than endpoint preservation alone, are essential. Equivalent formulations may state those identities directly and need not assume a specific uniform-threshold representation.

A fresh ordinary probe reports whether any route has both gates open. Thus its no-hit probability is Q(a,b)=product_j(1-C_j(a,b)). A cross-command replay holds each complete threshold pair fixed, first probes (a,1), and then probes (1,b), with no state change caused by probing. Both probes have no hit exactly when every route has U_j>alpha(a) and V_j>beta(b). Therefore J(a,b)=product_j(1-alpha(a)-beta(b)+C_j(a,b)).

No assumption of within-route independence is made. Independence of the route-pair vectors is essential to the displayed product formulas. It suffices instead to posit those product laws directly as the observational model, but then their physical derivation is outside the theorem.

## 2. Rigidity theorem and independent proof

Assume, at every command pair in [0,1]^2,

Q(a,b)=(1-ab)^n, and J(a,b)=[(1-a)(1-b)]^n.

Then m=n, alpha(a)=a, beta(b)=b, and C_j(a,b)=ab for every route and command pair.

### 2.1 Faces identify the shared calibration up to the count ratio

On b=1, Q(a,1)=(1-alpha(a))^m=(1-a)^n. Both bases are nonnegative, so the unique nonnegative mth root gives alpha(a)=1-(1-a)^c, with c=n/m>0. The other face gives beta(b)=1-(1-b)^c. This includes the endpoints. No differentiability assumption is used; the identified form is smooth in a neighborhood of zero. If an empty inventory had been allowed, its Q would be identically one and contradict n>=1, so m>0 would follow anyway.

### 2.2 Near-zero cross-command replay identifies c

Put h(t)=1-(1-t)^c. For every j,

0 <= C_j(t,t) <= 1-Q(t,t) = n t^2 + O(t^4).

The inequality follows from product_k(1-C_k)<=1-C_j. Finiteness of m therefore gives C_j(t,t)=O(t^2) uniformly over the finitely many routes. Taking logarithms of Q yields

-sum_j C_j(t,t)+O(t^4)=n log(1-t^2)=-n t^2+O(t^4),

hence sum_j C_j(t,t)=n t^2+O(t^4). This does not differentiate C_j.

For sufficiently small positive t, h(t)=c t-c(c-1)t^2/2+O(t^3) and every replay factor 1-2h(t)+C_j(t,t) is positive. Set x_j=-2h+C_j. Since x_j=O(t), and h C_j=O(t^3),

log(1-2h+C_j)=-2h+C_j-2h^2+O(t^3).

After summing over the fixed finite inventory,

log J(t,t)=-2m h(t)+sum_j C_j(t,t)-2m h(t)^2+O(t^3)
            =-2n t-n c t^2+O(t^3).

The target is 2n log(1-t)=-2n t-n t^2+O(t^3). Subtract, divide by t^2, and let t decrease to zero. Since n>0, c=1. Thus m=n and both calibrations are identity. No smoothness, derivatives, Taylor expansion, or positive density of C_j has been assumed.

### 2.3 Two AM-GM equalities identify every within-route law

Fix 0<a,b<1. Define R_j=1-C_j(a,b), S_j=1-a-b+C_j(a,b), r=1-ab, and s=(1-a)(1-b). All factors are nonnegative probability values. Both target products are strictly positive in the interior, so all R_j,S_j are positive. The assumptions, now with m=n, give product R_j=r^n and product S_j=s^n.

AM-GM implies mean_j R_j>=r and mean_j S_j>=s. But every R_j+S_j=2-a-b=r+s. The two nonnegative AM-GM gaps sum to zero, so each is zero. Equality in AM-GM forces R_j=r for every j, hence C_j(a,b)=ab. This argument works also for n=1.

At a=0 or b=0, C_j=0 by the marginal identities. At a=1, C_j=b; at b=1, C_j=a. The four corners are included. The boundary result therefore needs no continuity argument and never takes a logarithm of zero.

## 3. What the result does and does not identify

It identifies the fixed pure-AB route-occurrence count and the full operational within-route threshold law under the specified shared-marginal calibration model and both exact all-command observational laws. With route-pair independence, it implies mutual probabilistic independence of the resulting 2n threshold coordinates. It does not establish metaphysical original-source independence, absence of common causes, physical controllability, psychological manipulability, or individual causal source identities. No finite-sample statement follows from exact population identities alone.

The theorem's extra capability is reuse of the same pair across two distinct commands. Merely retaining the route inventory while independently redrawing threshold pairs between probes gives the product of the two no-hit marginals. Once the face laws are matched, that product equals [(1-a)(1-b)]^n regardless of within-route copulas and adds no such identification. Replaying the identical command against held threshold pairs repeats the same deterministic bit; it also adds no information. These conclusions assume noiseless observation and the stated no-state-change/re-draw semantics.

## 4. Finite-grid limitation: global copula factorization only

Fix any finite sets A,B of predeclared command coordinates, including 0 and 1. For a countermodel it is enough to use identity calibration. Choose nonzero polynomials f,g vanishing at every element of A,B, respectively; for example, f(x)=x(1-x) product_{r in A intersect (0,1)}(x-r), and analogously for g. Distinct roots are used once. Since f and g are nonzero polynomials vanishing at both endpoints, their derivative sup norms L_f,L_g are finite and strictly positive. Choose a nonzero epsilon with |epsilon| L_f L_g <= 1/2.

The density p_epsilon(u,v)=1+epsilon f'(u)g'(v) is at least 1/2. Its row and column integrals are one, because f(1)=f(0)=g(1)=g(0)=0. The resulting copula is

C_epsilon(a,b)=ab+epsilon f(a)g(b).

It agrees with ab at every grid vertex in A x B and differs at some off-grid pair. Rectangle-cell probabilities are the alternating sum of the four corner copula values, so its entire finite-grid threshold-cell distribution is exactly the independent distribution.

Any noiseless transcript using only these grid coordinates and held thresholds is a deterministic function of the route-level cell indices. With independent route pairs, identical cell distributions imply identical full transcript laws, including arbitrary probe order, repetition, aggregation over routes, and within-grid choices based on earlier observed bits. The same conclusion holds for independent fresh batches with the same cell law. A bounded deterministic adaptive protocol with finitely many binary observation branches can be covered by taking the union of the finitely many coordinates on all branches. This does not cover unrestricted continuously randomized coordinates or an unbounded growing grid.

Keeping the route count fixed at m=n, perturbing one route or every route supplies the counterexample. Therefore a fixed finite grid does not certify global factorization in the unrestricted copula class, even from its exact transcript law. This is not a claim that no finite panel can certify the route count. Parametric restrictions on the copula family may also change the conclusion.

## 5. Exact high-command ambiguity control

Take target n=1, alternative m=2, and t=3/4. Let alpha=beta=H_(1/2), so alpha(t)=beta(t)=1/2. Let D_1(u,v)=min(u,v) and D_2(u,v)=(max(u+v-1,0)+uv)/2. The first is realized by (W,W) with W uniform; the second is an equal mixture of (W,1-W) and an independent uniform pair. They are valid copulas, and independent draws of the two route vectors give the required route independence.

At the panel, D_1(1/2,1/2)=1/2 and D_2(1/2,1/2)=1/8. Hence Q=(1/2)(7/8)=7/16=1-(3/4)^2. Since 1-alpha-beta=0, J=(1/2)(1/8)=1/16=(1-3/4)^2. Each face no-hit probability is (1-1/2)^2=1/4=1-3/4.

A stronger exact check is available at this one interior command plus its faces. Let X,Y be aggregate face hit bits and Z the interior hit bit, all under the same held pairs. Route 1 has either both gate bits zero or both one at its equal thresholds. Consequently Z=X AND Y. The full (X,Y,Z) distribution is 000:1/16, 100:3/16, 010:3/16, 111:9/16, identical to the single-route independent baseline at thresholds 3/4. This control does not assert agreement outside the panel or at arbitrary asymmetric command points.

## 6. Review status before frozen-payload inspection

The two mathematical claims and the exact stated control pass this independent derivation, subject to the explicit model assumptions and scoped conclusions above. A frozen-author-payload conformity review and source/hash bindings remain pending; no author content has been read in preparing this derivation.
