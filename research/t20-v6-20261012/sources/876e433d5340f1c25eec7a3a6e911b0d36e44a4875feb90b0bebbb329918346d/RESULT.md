# Objective order when correction moves its states

10 October 2026 UTC. Additive T20 mathematical interface deduction. Written proof with exact symbolic controls, not a kernel theorem, empirical cognitive model, or field-priority claim. Review is separate.

## Question and inherited distinction

The finite-switch pure-reweighting result in `tensor-objective-switching-20261010/RESULT.md` preserves one underlying law and integrates the successive objective functions. For fixed functions and equal durations, those multiplication weights commute. The accepted polynomial-gradient packets additionally move the states by their characteristic flows. Does the old order neutrality survive this stronger mechanism?

**It does not in general.** The first order-sensitive term is exactly a transport bracket; the direct killing contribution cancels at this order. This is a local statement about the specified equations. It neither supplies the epistemic meaning of an objective nor models a human intervention.

## Precise local proposition

Let F,G be smooth functions on Euclidean space, with enough derivatives for the following third-order local expansions. For definiteness take polynomials and a compactly supported initial probability μ. Choose a sufficiently small common time interval so all relevant characteristic images of its support remain in one compact set. Coercive polynomial objectives have global forward gradient flows, but global existence is not needed for this local proposition.

Define the unnormalized observable operator

    B_F p = −∇F·∇p − Fp,

and the actual characteristic operator

    T_F(t)p(x) = exp(−integral_0^t F(Φ_F(s,x))ds) p(Φ_F(t,x)).

Here Φ_F solves x′=−∇F. Its derivative at zero is B_F. Smooth ODE dependence and compactness give T_F(t)p = p+t B_Fp+t² B_F²p/2+O(t³), uniformly on the relevant support, for each fixed polynomial observable p. The same applies to the products of these operators. All remainder constants may depend on the support and observable.

Let μ_FG^t be the law obtained by evolving for time t under F, normalizing, then evolving for time t under G and normalizing. Intermediate normalization cancels, so

    μ_FG^t(p) = μ(T_F(t)T_G(t)p) / μ(T_F(t)T_G(t)1).

The reversed protocol uses T_G(t)T_F(t). This observable order is important: F is the first physical stage in the displayed F,G product.

Put b_F=−∇F and b_G=−∇G. Direct expansion of the first-order differential operators gives

    [B_F,B_G]p
      = (Db_G b_F − Db_F b_G)·∇p
        + (b_F·∇(−G) − b_G·∇(−F))p
      = (Hess(G)∇F − Hess(F)∇G)·∇p.             (1)

The scalar term is ∇F·∇G−∇G·∇F=0. In particular [B_F,B_G]1=0. The two numerator expansions therefore differ by t² μ([B_F,B_G]p)+O(t³), while their denominator expansions agree through degree two and tend to one. Division yields

    μ_FG^t(p) − μ_GF^t(p)
      = t² μ((Hess(G)∇F − Hess(F)∇G)·∇p)+O(t³). (2)

No transport-density Jacobian was omitted: T is the pullback of the weighted pushforward, and normalizing its value at 1 accounts for total mass. Equation (2) is an observable statement; it does not assert total-variation differentiability of moving atomic laws.

## Exact, globally admissible discriminator

In one dimension take F(x)=x²/2 and G(x)=(x−a)²/2. Both are coercive; their gradient flows exist for all positive times. Starting from any Dirac law δ_z, normalization leaves a Dirac law, and with q=exp(−t):

    F then G:  q² z + a(1−q),
    G then F:  q² z + a q(1−q),
    difference: a(1−q)².                              (3)

For a≠0 and every t>0 the endpoints differ. The bracket in (1) is the constant vector a, so the expansion of (3) is a t²+O(t³), with the same sign as (2). This is a counterexample to carrying pure-tilt order neutrality over to moving-state gradient dynamics. It is not a contradiction of the pure-tilt theorem.

There is no corresponding claim that all distinct objectives fail to commute. For pure reweighting (b_F=b_G=0), multiplication operators commute exactly, and normalization preserves that equality. Vanishing bracket also removes the displayed second-order obstruction; a full global commutation theorem requires the relevant flow/domain hypotheses and is not established merely by the truncation (2).

## Why the cancellation must be scoped

The direct killing term cancels in the first commutator because both velocities are the negative Euclidean gradients of their own killing functions. Arbitrary independently chosen drifts and killing functions need not have this property. Higher nested commutators need not remain pure transport either. For F=x²/2 and the above bracket C=a∂_x,

    [B_F,C]p = a∂_x p + a x p.

Thus (1) does not authorize discarding reweighting from finite protocols or their higher-order errors.

## Consequence and limits

A changing-objective model must retain the ordered control history when states move. The unordered sum of objective-duration pairs, adequate for the inherited pure-tilt schedule, need not determine its continuation. An actual observation model about an unchanged latent target is a further interface, not supplied by these dynamics; the inherited complete-experiment results remain intact.

This is an exact distinction among mathematical mechanisms, not an assertion that the user’s noetic calculus currently implements either protocol. Nor does order sensitivity itself establish beneficial correction, manipulation, knowledge, or warrant.

## Evidence boundary

The local deduction is by operator expansion and exact characteristic calculation. `check.py` verifies the operator identities on symbolic arbitrary test functions, the quadratic flow composition and small-time coefficient, non-gradient and higher-commutator controls. These are algebraic checks supporting the written proof, not an exhaustive proof by sampling. `INPUT_BINDINGS.json` records relevant inherited packet hashes. A bounded search of current top-level RESULT/REPORT files found no earlier report of this exact moving-gradient order calculation; it is not a search of all mathematics.
