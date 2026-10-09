# Interaction absence is not a terminating Cauchy-oracle decision

8 October 2026 UTC. New sibling; the frozen interaction-calibration classification and finite-panel appendix remain unchanged. This is an explicit observation-oracle obstruction inside the same fixed finite unguarded single-effect independent-route model. It is not a claim about philosophical nonexistence, physical reality, latent mixtures or a sampling experiment.

## 1. Result and scope

The full exact response function identifies whether an AB support is present. Nevertheless, over the unrestricted finite-count and unknown-homeomorphic-calibration class, there is **no procedure that always terminates and correctly decides AB presence versus absence from finitely many adaptive, positive-error population Cauchy queries**. Correctness here is required for every valid approximation name of every allowed response function.

The obstruction already holds when:

- the known labeled root set is exactly {A,B};
- the inventory is fixed, with no guards, mixtures or B-only routes;
- n_AB is promised to be either zero or one;
- the B calibration is the known identity;
- every calibration is static, coordinatewise, continuous, strictly increasing and endpoint preserving;
- all response curves are computable and satisfy the same known sup-norm Lipschitz bound 3.

The nuisance A-only count is unbounded across the allowed worlds, although finite in each world. No known count ceiling or uniform regularity bound on the hidden calibration maps is assumed. This witness does not settle those restricted classes.

The obstruction strengthens the earlier appendix's statement that its particular half-integer routine does not terminate on zero support. It rules out every always-terminating, universally correct procedure under the stated oracle contract. It does not contradict exact full-function identifiability or the positive-support-promised Cauchy recovery theorem.

## 2. Explicit fixed-inventory worlds

Let a,b be nominal commands in [0,1], and put u=1-a.

The base world W_0 has exactly one A-only route and no AB route, with identity calibrations. Its probability of no effect is

    Q_0(a,b)=1-a=u.

For every positive integer N, let W_N have N independent A-only routes and one AB route. Set

    r_A,N(a)=1-(1-a)^(1/N),   r_B(b)=b.

Each r_A,N is a continuous strictly increasing endpoint-preserving homeomorphism. One and the same r_A,N is used by every A incidence, including the AB route. The inventory is fixed within its world, and successes of its distinct route occurrences are independent. Thus

    Q_N(a,b)=(1-r_A,N(a))^N [1-r_A,N(a)b]
            =u[1-b+b u^(1/N)]
            =(1-b)u+b u^(1+1/N).                              (1)

Every W_N has AB present, with multiplicity exactly one. The base has AB absent. There is no support-specific calibration, cross-talk, changing inventory or hidden mixture in this construction.

### Exact uniform distance

From (1),

    Q_0(a,b)-Q_N(a,b)=b u(1-u^(1/N)) >=0.

The maximum over b is attained at b=1. Parameterize u=t^N with t in [0,1]. The remaining difference is t^N(1-t), whose derivative is

    t^(N-1) [N-(N+1)t].

It has a unique interior maximum at t=N/(N+1), giving

    ||Q_N-Q_0||_infinity
      = [N/(N+1)]^N /(N+1)
      = N^N/(N+1)^(N+1)
      < 1/(N+1).                                              (2)

The maximum occurs at b=1 and a=1-[N/(N+1)]^N. Hence Q_N converges uniformly to Q_0 on the entire closed command square.

The bound includes every face, corner and attenuation mask. In particular Q_N(a,0)=Q_0(a,0)=1-a; Q_N(0,b)=Q_0(0,b)=1; and Q_N(1,b)=Q_0(1,b)=0. The b=1 face contains the strict maximum, so endpoint access has not been omitted from the supremum argument. Under the unguarded law, issued-root profiles are already represented by zero masks, and adding those profile queries does not escape (2).

### A common observable continuity modulus

Write p=1+1/N, so 1<p<=2. On the interior,

    |partial Q_N / partial a|=(1-b)+b p u^(p-1)<=2,
    |partial Q_N / partial b|=u-u^p<=1.

The same bounds hold by one-sided limits at the boundary, and Q_0 has even smaller derivatives. Therefore every response curve obeys

    |Q(x)-Q(y)| <=2|a-a'|+|b-b'| <=3 ||x-y||_infinity.          (3)

Supplying the same known Lipschitz constant 3, or the continuity modulus it induces, does not separate these worlds.

This is a regularity statement about Q, not about its hidden calibrations. The r_A,N do not share a common uniform continuity modulus: r_A,N(1)=1 while r_A,N(1-2^(-N))=1/2, at nominal points whose distance tends to zero. For N>1 their derivative is unbounded near one. The counterexample therefore cannot be imported unchanged into a class with a promised common calibration Lipschitz bound or modulus.

## 3. Exact oracle contract

A pointwise population Cauchy query consists of:

- a rational command point x=(a,b) in [0,1]^2, with boundary points allowed;
- a positive rational error tolerance epsilon.

A valid oracle returns a rational number q_hat satisfying

    |q_hat-Q(x)| <= epsilon.

The algorithm may choose later commands and tolerances from the entire previous transcript, use the supplied common response modulus, and perform arbitrary finite computations between queries. It must halt after finitely many such queries in every allowed world and for every valid oracle name, returning exactly one of “AB absent” and “AB present.” Failure to terminate, abstention or a wrong answer does not count as a decision.

An oracle name is a fixed total assignment of a valid reply to every possible query. It does not change worlds in response to the algorithm. Requiring correctness for every valid name is the ordinary representation-independent approximation contract: error bounds convey accuracy, not additional semantic information encoded in arbitrary digits or rounding choices.

The base admits the computable exact-reply name

    O_0(x,epsilon)=1-a.

It is rational for rational a, and has strict error slack for every positive epsilon. Each Q_N likewise has computable names: positive N-th roots of rational u can be enclosed by rational interval bisection, and formula (1) propagates those intervals to Q_N. Thus the impossibility is not caused by selecting noncomputable response functions or requiring uncomputable oracle replies.

Dyadic tolerances would suffice. Allowing arbitrary positive rational tolerances, arbitrary rational interior or boundary commands, and a known observable modulus does not invalidate the proof.

## 4. No always-terminating exact decider

Suppose a deterministic algorithm met the stated contract. Run it on W_0 using O_0. Since it must halt and be correct, it returns “AB absent” after a finite transcript.

If it asks no queries, the same answer is immediately wrong in every W_N. Otherwise, let epsilon_min>0 be the minimum of the finitely many requested tolerances. Choose a positive integer N large enough that

    1/(N+1)<epsilon_min.

By (2), every exact base reply in the transcript is also a valid response for Q_N at that same command and tolerance. The queries may have been adaptive; their being determined by identical prior replies ensures the entire finite path remains identical.

To make this a **fixed total alternative name**, rather than an informal adversarial transcript, define

    O_N(x,epsilon)=Q_0(x)  if epsilon>1/(N+1),

and at all finer tolerances use any fixed rational-bisection approximation to Q_N with error at most epsilon/2. This is a computable valid Q_N name at every query: the first branch is valid by (2), and the second by construction. It reproduces every query response on the halted base transcript. Therefore the algorithm returns “AB absent” in W_N, where the AB support is present. This contradiction proves the result.

The oracle does not grant an exact rational-value flag merely because a particular reply happens to equal the true base value. In the alternative world the identical reply is an allowed approximation. Treating the numerical center as exact would violate the specified evidence contract.

## 5. Separated randomized corollary

The same family rules out a randomized procedure that halts almost surely for every allowed world/name and has uniform error at most a fixed delta<1/2. The randomness here is internal algorithmic randomness; the oracle still supplies certified population approximations. This is not a finite-sample theorem.

Assume such a procedure exists. With the exact base name O_0, let E_P be the event that the procedure returns “AB absent,” halts, and every requested tolerance is at least 2^(-P). A path with no queries satisfies the tolerance condition. The events E_P increase with P. Almost-sure termination and positive tolerances ensure their union is the event of an absent return, whose probability is at least 1-delta. Since 1-delta>delta, some finite P has

    Pr_(O_0)(E_P)>delta.

Choose N with 1/(N+1)<2^(-P). Define one fixed Q_N oracle to return Q_0(x) whenever epsilon>=2^(-P), and to approximate Q_N at finer requests. The first branch is valid uniformly by (2); this name is selected once, before the internal random seed is drawn.

Couple the base and alternative executions using the same random seed. On E_P every reply, subsequent command and stopping decision is identical. The alternative consequently returns “AB absent” with probability at least Pr(E_P)>delta, violating its error bound. In particular a zero-error almost-surely terminating randomized decision procedure is impossible.

This corollary assumes the usual measurability of the randomized protocol and its halting/output events. It does not rule out procedures that are permitted not to halt on absent support, promises that exclude the base world, or a different oracle furnishing exact comparisons.

## 6. Why the earlier positive results remain valid

For every N and any interior a,b>0, W_N has the isolated multiplicative contrast

    E_AB(a,b)=Q_N(a,b)/[Q_N(a,0)Q_N(0,b)]
              =1-b+b(1-a)^(1/N)<1,

whereas the base contrast is exactly one. Thus the exact full-law classification separates every individual W_N from W_0. Uniform proximity is not equality. Inverting the mask quotient near a vanishing denominator can amplify a small raw-Q difference; the all-one boundary is not a legitimate division by zero.

Under the separate promise that the AB support is positive, the earlier half-integer determinant method still terminates and recovers its positive integer multiplicity from a finite panel with arbitrary-precision population access. All alternatives here have that count equal to one. The obstruction concerns deciding whether that promise holds at all, particularly certifying the zero case.

Positivity can be semidecided at a fixed interior contrast: refine valid intervals until E_AB<1 is certified. In each positive world this eventually succeeds. In the base world it never certifies positivity, and the present theorem says no always-terminating total replacement can decide both cases over the declared class. It does not make every individual zero instance undecidable under every stronger prior or observation representation.

The following are different contracts, not covered by this obstruction:

- exact real comparison/equality access, a symbolic response formula or complete exact function supplied as a manipulable object;
- an oracle that promises exact rational values, rather than rational approximation centers with positive error bars;
- a specially prescribed name or rounding convention that supplies discontinuous extra information not available from arbitrary valid Cauchy names;
- a known common count ceiling, an additional restrictive calibration-error band, or an effective common regularity bound on the hidden calibration maps;
- independently observed calibration, internal route channels or a different generative model.

The statement about known ceilings is a scope exclusion: the present sequence uses N tending to infinity. No affirmative recovery theorem under a ceiling is claimed here. Likewise the common response-curve modulus (3) is explicitly included in the negative result and must not be confused with an unprovided hidden-calibration modulus.

No physical calibration, admissible intervention, metaphysical source existence/nonexistence, source-level causal adequacy, protected integration, owner acceptance or T20 closure follows from this observation-oracle theorem.
