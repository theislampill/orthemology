# Participating geometric transport derivation

10 October 2026 UTC. Proposed ordinary mathematical deduction from the retained lognormal moment-indeterminacy and endpoint-continuation results. Submitted for independent scrutiny. No new classical moment theorem, no kernel or empirical claim.

Let nu+ and nu- be the inherited distinct lognormal Stieltjes pair, with common m_r=exp(r^2/2). For either source law write Z(v)=integral exp(-v*x)dnu, psi(v)=log Z(v), q(v)=-psi'(v), V(v)=psi''(v), for v>=0. They are not identified as probability laws merely because their endpoint moment records agree.

## Finite-distance regular endpoint

On [0,a], let D=Z(a)>0. Then Z(v)>=D, so E_v[X^2]<=m_2/D, and 0<V(v)<=m_2/D. Positivity follows because every tilted lognormal density remains nondegenerate. At v=0, V(0)=m_2-m_1^2=e^2-e>0. The Fisher length of this particular parameterised curve is at most a*sqrt(m_2/D); no geodesic minimality is needed. It follows that the endpoint is at finite intrinsic distance along this leaf.

Every derivative of Z on the right at zero is justified by domination by the finite moment of the corresponding grade. Thus psi, q and V have smooth one-sided extensions, and every corresponding endpoint derivative agrees across the two laws. This does not assert an exponential-family open-domain extension to negative v.

## Mean-coordinate transport

Since q'(v)=-V(v)<0, the curve has a one-sided smooth inverse v=v(q) near q_0=m_1. Take natural parameter eta=-v and dual potential

Phi(q)=-v(q)*q-psi(v(q)).

Then Phi'(q)=-v(q), Phi''(q)=1/V(v(q))>0. At the endpoint Phi(q_0)=0 and Phi'(q_0)=0. Repeated differentiation/inversion expresses its full one-sided jet from the common cumulants and nonzero V(0); therefore both laws have identical full Phi jets there. The metric transforms as V(v)dv^2=(1/V(v(q)))dq^2.

For two points v,w on the SAME source leaf,

KL(nu_v || nu_w) = (w-v)q(v)-psi(v)+psi(w)
                 = D_Phi(q(v),q(w)).

This is an exact density-ratio calculation, not a transport between the two different source laws. The source index is retained.

## Distinct germs and nonanalyticity

If the two variance functions V(v) agreed on any right neighbourhood of zero, equality of their initial psi value and first derivative would make their log-normalisers, hence Laplace transforms, agree there. Analytic uniqueness on v>0 and Laplace injectivity would identify the laws, contrary to the inherited construction. Their variance germs therefore differ.

If the mean-coordinate Hessian germs agreed, the equations dq/dv=-1/Phi''(q) with the same q(0)=q_0 would have the same locally Lipschitz right-hand side, hence the same solution near zero. This reduces to the preceding contradiction. Full metric/potential germs in the declared control and mean coordinates retain distinctions which their infinite endpoint jets erase. This is not a claim of abstract intrinsic nonisometry: one-dimensional positive Riemannian metrics can be locally straightened by arc length. The mean observable and the affine/Hessian structure belong to the intended statistical interface; an arbitrary reparameterisation that changes those meanings is not the transport being tested.

The common moment derivatives cannot be the Taylor coefficients of an analytic Z at zero: (m_r/r!)^(1/r) tends to infinity. If psi or its second derivative V had an analytic extension, integration and exponentiation would give such an extension of Z. If Phi had a real-analytic extension with Phi''(q_0)>0, the analytic inverse function theorem and Legendre relation would again give analytic psi. Thus no such analytic extension exists. A smooth ambient extension, if constructed, need not be a probability/exponential-family extension and is not excluded here.

## Identity and scope

For the original reverse-damped mu=T_a nu, log Z_mu(u)=psi(u+a)-log D. Its endpoint constant may differ between the laws; do not call the uncentred potentials identical. Hessians and Bregman divergences ignore the additive constant. Retaining original input/normalisation history avoids the endpoint moment-state collapse.

Finite Fisher distance and a nonzero smooth endpoint metric therefore do not establish continuation adequacy of the moment/jet quotient. The assertion is not that metric completion itself merges these laws, nor that Fisher geometry is universally uninformative. No psychological, normative or metaphysical warrant follows from this statistical example.
