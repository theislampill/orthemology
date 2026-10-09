# Coordinate-only dependent gates restore an interaction-count ambiguity

8 October 2026 UTC. This is a new scratch sibling. Earlier stages are preserved. The result is a conditional probability-model countercontrol, not a physical experiment, a psychological-manipulability claim, a metaphysical counterexample, a new copula family, protected integration, or T20 closure.

## 1. Result and exact scope

Consider a fixed, finite pure AB inventory with n>=1 independent route occurrences. Each route succeeds when its A and B gates both succeed. In the baseline model those gates are independent, with probabilities a and b. The one-effect absence response is

    Q_n(a,b) = (1-ab)^n,       0<=a,b<=1.

The baseline a,b may themselves be arbitrary fixed coordinate-calibration homeomorphisms of nominal commands. Working in their true-rate coordinates loses no information.

For every integer m>=n there is an alternative with exactly m independent, identically distributed route occurrences, fixed endpoint-preserving coordinatewise calibration homeomorphisms, and dependent A/B gates within each occurrence, whose entire endpoint response is Q_n. The construction uses the already established Joe copula at parameter theta=m/n. It even has one fixed random-threshold coupling across all commands, so each gate depends pathwise only on its own command.

Among alternatives with a single common per-route response law, coordinate-only endpoint-preserving marginal calibrations, and route-to-route independence, the possible counts reproducing Q_n are **exactly the integers m>=n**. Section 4 first proves this in the homogeneous case, then extends the same count fibre to heterogeneous within-route joint laws when all occurrences still share the same two coordinatewise marginal maps. It does not cover occurrence-specific marginal calibrations, route-to-route dependence, arbitrary multiple-support inventories, or additional observation channels.

Thus the interaction-calibration anchor is not robust to replacing within-route root-product factorization by an unknown admissible dependence law. Its conclusion remains valid under its stated factorization premise. This example isolates that premise while retaining the other declared restrictions relevant to a pure two-root inventory.

## 2. Direct construction of a joint distribution

Put c=n/m, and define

    H_c(z)=1-(1-z)^c,
    F_c(a,b)=H_c(ab).

For every c>0, H_c is a continuous strictly increasing endpoint-preserving homeomorphism of [0,1]. For 0<c<=1, F_c is a genuine joint CDF with both marginal CDFs H_c. Here is a direct proof, independent of any copula reference.

F_c is continuous and grounded: F_c(a,0)=F_c(0,b)=0. Its upper corner is one, and its margins are F_c(a,1)=H_c(a), F_c(1,b)=H_c(b). On the open square its mixed derivative is

    f_c(a,b) = c (1-ab)^(c-2) (1-cab) > 0.

On every compact rectangle in the open square, the rectangular increment of F_c is the integral of f_c, hence nonnegative (strictly positive for a nondegenerate rectangle). Rectangles touching the boundary follow by continuity, as limits of interior rectangles. This establishes 2-increasingness, including the corner where the density may diverge. Grounding, continuity, total mass one, and nonnegative rectangular increments establish a probability distribution on [0,1]^2. No finite density value at (1,1) is assumed or needed.

Draw a threshold pair (X,Y) with this distribution. At commands a,b let

    G_A(a)=1{X<=a},      G_B(b)=1{Y<=b}.

Then P(G_A=1)=H_c(a), P(G_B=1)=H_c(b), and P(G_A=G_B=1)=H_c(ab). Both sample-path gates are nondecreasing in their own command and ignore the other command. This is stronger than checking independent Bernoulli tables separately at each command setting: it supplies a common, command-independent probability space realizing every setting.

The four Bernoulli cells, in order 11,10,01,00, are

    J, u-J, v-J, 1-u-v+J,
    u=H_c(a), v=H_c(b), J=H_c(ab).

They are the F_c masses of [0,a]x[0,b], [0,a]x(b,1], (a,1]x[0,b], and (a,1]x(b,1], respectively, and so are nonnegative and sum to one. In particular, this directly proves the relevant Frechet bounds max(0,u+v-1)<=J<=min(u,v).

Take m independent copies of this threshold pair. A route succeeds exactly when both gates in its copy succeed. Independence is retained between every pair of distinct route occurrences; dependence is confined to the two gates within an occurrence. Therefore

    Q'_m(a,b)=(1-J)^m=((1-ab)^c)^m=(1-ab)^n.

This identity includes all boundary commands. In nominal coordinates x,y with baseline maps r_A,r_B, use marginal calibrations H_c composed with r_A and H_c composed with r_B. These are still fixed coordinate-only homeomorphisms shared by all the m occurrences. No command cross-talk, random inventory, missing support, guard, repeated root incidence, or route-to-route common shock has been introduced.

## 3. Exact mapping to the established Joe family

The inverse is H_c^(-1)(u)=1-(1-u)^(1/c). Uniformize the thresholds by U=H_c(X), V=H_c(Y). Their copula is

    C_c(u,v)=H_c(H_c^(-1)(u) H_c^(-1)(v))
             =1-[(1-u)^(1/c)+(1-v)^(1/c)
                   -(1-u)^(1/c)(1-v)^(1/c)]^c.

Setting theta=1/c=m/n>=1 yields exactly

    C_Joe,theta(u,v)
      =1-[(1-u)^theta+(1-v)^theta
             -(1-u)^theta(1-v)^theta]^(1/theta).

This formula and parameter range are given in the software authors' [vinecopulas documentation, Table 1, Joe row](https://vinecopulas.readthedocs.io/en/stable/vinecopulas.html#fitting-a-vine-copula). The [CRAN copula package implementation](https://raw.githubusercontent.com/cran/copula/master/R/joeCopula.R) independently encodes the equivalent product-form CDF and lower parameter bound one. These were targeted formula/parameter inspections, not complete paper or package reviews.

The [CRAN acopula generator documentation](https://search.r-project.org/CRAN/refmans/acopula/html/generator.html) gives the Joe generator phi_theta(u)=-log(1-(1-u)^theta), theta>=1. Direct substitution gives phi_theta(u)=-log H_c^(-1)(u), and its inverse is phi_theta^(-1)(t)=H_c(exp(-t)). Hence phi_theta^(-1)(phi_theta(u)+phi_theta(v)) equals C_c above. This is a second direct algebraic check of the parameter orientation: c<=1 corresponds to theta>=1, not theta=c.

At c=1, C_c(u,v)=uv and m=n. For c<1 the gates are genuinely dependent. For example c=1/2 and a=b=1/2 give J=1-sqrt(3)/2, while uv=(1-1/sqrt(2))^2; their difference is strictly positive. The construction is an application and semantic transport of this named pre-existing family. No field-wide novelty is asserted.

A copula is a CDF in uniform marginal coordinates. Except at c=1, F_c(a,b) itself is not a copula because its margins are H_c rather than uniform. It is nevertheless a valid joint CDF when c<=1. The distinction matters for the failed transport below.

## 4. Why count reduction is impossible in this homogeneous relaxation

Suppose m>=1 independent occurrences have one shared per-route joint-success function J(a,b), with coordinate-only marginal success probabilities alpha(a), beta(b). Let both marginal maps preserve zero and one. Suppose their endpoint absence law is Q_n on the entire square.

Equality of nonnegative m-th powers forces

    J(a,b)=1-(1-ab)^(n/m)=H_c(ab).

At b=1, the B gate succeeds almost surely, so J(a,1)=alpha(a), forcing alpha=H_c. Similarly beta=H_c. These facts do not assume a threshold coupling across command settings.

If m<n, then c>1. At a=b=1-epsilon the forced 00-cell probability is

    1-2H_c(1-epsilon)+H_c((1-epsilon)^2)
       =epsilon^c [2-(2-epsilon)^c].

Choose 0<epsilon<2-2^(1/c), which is possible for every c>1. The bracket is negative, contradicting even a single valid two-gate Bernoulli table. Thus m<n is impossible under the stated homogeneous alternative. Together with the construction, m>=n is the exact count fibre in this enlarged class.

This does not say n is the actual count when the data came from an unknown dependent-gate world. It says n is the smallest count in this particular observational-equivalence fibre, whose other members can have arbitrarily many routes. A semantic interpretation of counts still has to be supplied.

### Separate strengthening: heterogeneous joint laws with shared marginals

Allow route k to have its own valid joint success function J_k(a,b), without requiring common copulas or a threshold coupling across commands. Retain independence between route occurrences, and require every occurrence to have the same A marginal alpha(a) and the same B marginal beta(b), both endpoint-preserving. These are substantive restrictions.

On the b=1 face every B gate succeeds almost surely, so

    product_k (1-J_k(a,1)) = (1-alpha(a))^m = (1-a)^n.

Thus alpha=H_c, and the other face forces beta=H_c. At a=b=1-epsilon, the union bound on each valid two-gate distribution gives

    1-J_k(a,b) <= P(A gate fails)+P(B gate fails)=2 epsilon^c.

Route-to-route independence therefore gives

    Q'(a,b) <= 2^m epsilon^(cm)=2^m epsilon^n.

But the required target is epsilon^n(2-epsilon)^n. If m<n, choose 0<epsilon<2-2^(m/n); then (2-epsilon)^n>2^m, a contradiction. No equality of the J_k functions was used. Since the homogeneous Joe construction realizes every m>=n, the exact compatible-count set is again {n,n+1,...} in this larger shared-marginal class.

This strengthening does not allow route-specific marginal maps. It also does not replace independence between routes by a bound inferred from marginal probabilities. Both missing premises would invalidate the displayed endpoint product argument. The parent proposed this Frechet/union-bound extension, and independent review covers it separately.

## 5. Valid and invalid rectangles; a failed cross-domain map

### Valid example

For c=1/2 and a=b=1/2 the table is

    p11 = 1-sqrt(3)/2,
    p10 = p01 = (sqrt(3)-sqrt(2))/2,
    p00 = sqrt(2)-sqrt(3)/2.

Every cell is strictly positive. The 00 cell is exactly the rectangle mass of (1/2,1]x(1/2,1] under F_(1/2); positivity follows already from 2>3/4. Two independent such route pairs have endpoint absence (sqrt(3)/2)^2=3/4, equal to a single baseline independent AB route. Their marginal gate success probability is 1-1/sqrt(2), not 1/2.

### Invalid example and general failure

For c=2, F_2(a,b)=2ab-a^2b^2. It is probability-valued, continuous, grounded, and increasing in each argument, with F_2(1,1)=1. Nevertheless

    Delta F_2((3/4,1]x(3/4,1]) = -17/256.

Indeed at a=b=3/4 the forced Bernoulli table is (207,33,33,-17)/256. Thus the superficially similar count-two to count-one construction is not a joint gate model with marginals H_2. A smaller interior rectangle (3/4,7/8]x(3/4,7/8] has mass -41/4096. In contrast, (0,1/2]x(0,1/2] has positive mass 7/16: spot checks in only low-command regions can miss the defect.

For every real c>1, f_c is negative wherever ab>1/c, so a nondegenerate compact rectangle inside that region has negative mass. In particular H_n(ab) for each integer n>1 is not a joint CDF and cannot be made a copula just by the marginal reparameterization above; monotone coordinate changes preserve the sign of rectangle masses. Its nonuniform margins already rule out calling it a copula in the original a,b coordinates.

There is no contradiction in H_n(ab) being the legitimate probability of at least one successful baseline route under a separately chosen command (a,b). An intervention-indexed success-response surface need only be a valid probability at each setting. Interpreting it as the joint CDF of two fixed thresholds additionally requires nonnegative masses for every rectangle. That is exactly the failed map here. One must not silently import CDF semantics from coordinatewise monotonicity and values in [0,1].

## 6. Comparison with inherited countercontrols

1. The shared-bearer gate control in productive-identifiability shares a root gate across occurrences. Duplicate and absorbed supports collapse because route outcomes depend on common gates. The present construction instead uses independent pairs across occurrences. Its ambiguity cannot be dismissed as duplicate aliases or failure of route-to-route independence.
2. The interaction-calibration anchor's cross-talk control keeps independent within-route gates but lets A's success calibration depend on B's command. The present alternative keeps both marginal and pathwise gate response coordinate-only. It changes their joint law. The two countercontrols relax different assumptions.
3. The inherited support-specific-calibration control breaks the sharing of A's calibration between AB and unary-A supports. This construction has one pure AB support and uses a single common map per root across every occurrence. It does not claim automatic extension over overlapping support inventories.
4. The inherited noise-aware correlation control already establishes that correct gate marginals do not establish independence. That general lesson is retained with attribution. The current contribution is an explicit all-command, cross-count equality preserving route independence and coordinate-only calibration, its valid Joe coupling, and an exact one-sided count fibre in the stated homogeneous class.
5. The earlier route-level Bernoulli implementation realizes the same product-dependent route success without identifying physical incidence architecture. Here the per-route probability itself differs from the product of its newly calibrated marginals. Thus the anchor theorem's actual response-factorization premise, not merely an implementation story, is violated.

The four-value determinant theorem from the anchor appendix remains sound in its separable model. On the same endpoint data it returns n. If those data actually arise from the m>n dependent alternative, the matrix of inferred per-route successes at m is H_(n/m)(a_p b_q), which is not rank one; its strict positive determinant is precisely why the separable fit rejects m. The panel identifies a count conditional on within-route factorization. Neither it nor the entire endpoint surface certifies that factorization against this enlarged model class.

With fresh independent route-pair draws on each trial, equality of Q also gives equal adaptive endpoint transcript laws by the usual common-protocol, fresh-uniform coupling. That extension requires the stated conditional trial independence. It says nothing about arbitrary temporal dependence, gate-level readouts, or jointly observed counterfactual outcomes at multiple commands.

## 7. Boundary and attribution

The parent proposed the H_(n/m) construction, candidate Joe correspondence, and failed H_n CDF warning. The present work verifies them directly, develops the fixed-threshold realization, verifies the homogeneous count-fibre converse and parent-proposed heterogeneous shared-marginal strengthening, checks exact rectangles, and compares the inherited controls. The named Joe family and ordinary CDF/copula mathematics are pre-existing. SOURCE_AUDIT.md identifies precisely what was read and what was only bibliographically checked.

No psychological actuator, physical calibration, intervention admissibility, causal ontology, source-level perfection, or actual independently operative productive occurrence is certified. The result concerns the information carried by one declared stochastic endpoint interface relative to explicit alternatives. It supplies an assumption-isolation countermodel, not T20 closure.
