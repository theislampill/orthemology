# Valid initial moments do not force positive-time realizability

10 October 2026 UTC. Separate additive research note. The existing realizable-moment-dynamics-20261010 classification is unchanged. This is an ordinary mathematical counterexample, not a formal-kernel certificate, sampling result, canonical integration, or field-novelty claim.

## 1. Answer

For every prescribed finite horizon 0<T<∞, there is a coordinatewise C∞ hierarchy solution on [0,T) such that:

- m_0(t)=1 and m_r'(t)=−m_(r+1)(t)+m_1(t)m_r(t) for all r≥0;
- every coordinate is strictly positive throughout [0,T);
- the complete initial sequence is represented by an explicitly supplied probability with all moments finite;
- at no positive time is the complete sequence represented by a probability on [0,∞).

Consequently initial Stieltjes validity cannot replace the positive-time realizability premise of the existing classification. The example does not contradict the global Bernstein–Widder theorem: its complete-monotonicity conclusion is only asserted on a prescribed finite interval, and the chosen perturbation depends on its length.

## 2. Two explicit measures with identical moments

Let μ be the standard lognormal probability, with density

    dμ(x) = (2π)^(-1/2) x^(-1) exp(−(log x)^2/2) dx, x>0.

Define

    S = Σ_(k∈Z) exp(−k²/2),
    η = S^(-1) Σ_(k∈Z) exp(−k²/2) δ_(exp k).

The series S is finite and positive. Completing the square and shifting the integer index gives, for every integer r≥0,

    ∫x^r dμ = exp(r²/2),
    ∫x^r dη = S^(-1) Σ_k exp(rk−k²/2)
             = exp(r²/2) S^(-1) Σ_k exp(−(k−r)²/2)
             = exp(r²/2).

In particular η({1})=S^(-1), while μ({1})=0. This is a classical discrete lognormal moment representative, rechecked directly here; no novelty is claimed for it.

## 3. Parameter choice and initial validity

Fix T∈(0,∞). Put p=μ([1,2])>0, and choose

    0<ε<min{S^(-1), exp(−T)p}.

For example half the displayed minimum is an explicit choice. Necessarily ε<1. The measure

    ρ_0 = (η−εδ_1)/(1−ε)

is positive, has total mass one, and has all moments finite. Its moment sequence is

    c_r = [exp(r²/2)−ε]/(1−ε), r≥0.

Thus c_0=1 and this is a valid full Stieltjes moment sequence, not merely a finite prefix or a sequence of nonnegative numbers.

For clarity, this initial sequence is indeterminate. For any 0<θ<1−εS, the different positive probability

    [(1−θ)η+θμ−εδ_1]/(1−ε)

has the same moments. This construction does not settle the separate strengthening with a determinate initial sequence.

## 4. The strictly positive hierarchy solution

For r≥0 and t≥0 define

    B_r(t) = ∫x^r exp(−tx)dμ(x),
    A_r(t) = B_r(t)−ε exp(−t).

Every B_r, and hence every A_r, is C∞ up to zero in the right-boundary sense. This follows from dominated convergence using the finite moments of μ; its k-th derivative is (−1)^k B_(r+k). Thus

    A_r'(t)=−A_(r+1)(t).

For x∈[1,2], r≥0, and 0≤t<T,

    x^r exp(−tx) = exp(−t) x^r exp(−t(x−1))
                 ≥ exp(−t) exp(−T).

It follows, uniformly over all grades, that

    A_r(t) ≥ exp(−t)[p exp(−T)−ε] > 0.             (1)

In particular A_0 never vanishes on [0,T). Define

    m_r(t) = A_r(t)/A_0(t).

These are strictly positive C∞ functions, m_0=1, and the quotient rule gives the exact hierarchy

    m_r' = −m_(r+1)+m_1 m_r.

At zero A_0(0)=1−ε and m_r(0)=c_r, whose positive representative was supplied in §3.

To match the classification's normalized unnormalization, put

    a_r(t)=A_r(t)/(1−ε).

Then a_0(0)=1, a_r=(−1)^r a_0^(r)>0, and a_0=exp(−∫_0^t m_1(v)dv). Thus this is also directly a local completely monotone function with a valid complete initial derivative sequence.

## 5. No positive-time sequence is realizable

Fix s∈(0,T), and suppose a positive probability ρ_s represented all m_r(s). Define two positive finite measures

    κ_s = A_0(s)ρ_s + ε exp(−s)δ_1,
    λ_s(dx) = exp(−sx)μ(dx).

For every r≥0 their moments agree:

    ∫x^r dκ_s = A_0(s)m_r(s)+ε exp(−s)
              = A_r(s)+ε exp(−s)
              = B_r(s)
              = ∫x^r dλ_s.

But λ_s has an exponential moment: for example

    ∫exp((s/2)x)dλ_s = ∫exp(−(s/2)x)dμ ≤ 1.

A positive finite measure with a finite positive exponential moment is determined by its moments. Therefore κ_s=λ_s. This is impossible at {1}, because

    κ_s({1})≥ε exp(−s)>0,     λ_s({1})=0.

This contradiction proves nonrealizability at every s>0 in the claimed interval.

For completeness, the determinacy fact used here requires no finite-interval representation theorem. If two positive finite measures share the moments of λ and ∫exp(bx)dλ<∞, monotone convergence of the exponential series gives the same finite exponential integral for the second measure. Their Laplace transforms consequently have the same absolutely convergent Taylor series for |u|<b. They agree there, and by real analyticity throughout u>0. Laplace uniqueness follows by pushing forward under y=exp(−x) to [0,1], using equality at nonnegative integer parameters, and polynomial density in continuous functions on [0,1].

## 6. Why no positive initial law can produce this scalar path

The scalar path is the Laplace transform of the finite signed measure

    ν=(μ−εδ_1)/(1−ε),

which has ν({1})<0 but the valid initial moment sequence c. If any positive probability had its Laplace transform equal to a_0 on an open subinterval of (0,T), positive-time differentiation would represent all corresponding a_r, contradicting §5. Equivalently, analytic continuation and finite signed Laplace uniqueness would identify that probability with ν, contradicting its negative atom.

The obstruction is precise: monomial-exponential tests x^r exp(−tx), simultaneously over all r and bounded time, can remain positive on a signed measure even though positivity on all polynomial squares fails after damping. Initial moments hide the negative atom by admitting a different positive representing law. At positive time exponential integrability removes that ambiguity and exposes the atom.

## 7. Attribution, scope, and verification

The discrete representative in §2 belongs to the classical Chihara–Leipnik lognormal moment construction. An inspected research source is Richard Arratia, Larry Goldstein, and Fred Kochman, “Size bias for one and all,” Probability Surveys 16 (2019), 1–61, §9, Theorem 9.1; DOI https://doi.org/10.1214/13-PS221, author-hosted text https://dornsife.usc.edu/sergey-lototsky/wp-content/uploads/sites/211/2023/06/SizeBiasing-Survey.pdf. That paper attributes the family to Chihara and Leipnik. The sum calculation above is included in full, so the counterexample does not depend on an unverified historical attribution or inaccessible original theorem. The original Leipnik DOI https://doi.org/10.1137/1126095 was located but its full text was not accessible in this check; no claim is made to have inspected it.

The use of this classical pair to separate initial validity from positive-time realizability in the specified hierarchy is the bounded result of this note. No exhaustive literature comparison or field-priority claim is made.

The result is proved by exact formulas, an all-grade/all-time inequality, and positive-measure determinacy. No numerical sampling is used as evidence for a universal statement. A small symbolic control file separately checks the index-shift and derivative/quotient identities; these checks supplement rather than establish the measure-theoretic proof.

The frozen parent theorem remains valid and is not edited. Its RESULT.md SHA-256 before this work was c5aeeeed56b5bf5edfa9b87570249f142e3d1be9c06218d8007013c66f5eb688.
