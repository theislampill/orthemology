# Asymptotic gradient selection and exact entropy transport

10 October 2026 UTC. Additive T20 mathematical supplement by the participating root researcher. The underlying convergence theorem is inherited from the separately reviewed nonconvex limit packet. The Gibbs variational identity and conditional expectation are classical. The new application identifies their exact dynamic costs and the correct transport through endpoint merging. No field-priority, kernel verification, empirical noetic identification, protected integration or tranche closure is claimed.

## The inherited dynamic quantities

Let F be a coercive polynomial on finite-dimensional Euclidean space and μ any Borel probability. The accepted `nonconvex-atomic-limit-classification-20261010/RESULT.md` proves, for the gradient flow Φ and its normalised killing by F:

- q(x)=lim Φ_t(x) exists and is a critical point.
- c(x)=F(q(x)) takes finitely many values.
- I(x)=integral_0^infinity [F(Φ_t(x))−c(x)]dt is finite and nonnegative for every x.
- If c* is the least critical value whose basin has positive μ mass, S={x:c(x)=c*} has positive mass.
- A=integral_S exp(−I)dμ lies in (0,1], and the limiting probability on initial coordinates is π*=1_S exp(−I)μ/A.
- The physical limiting law is ρ*=q_#π*.
- The integrated ensemble gap is integral_0^infinity [E(t)−c*]dt=−log A. This includes the inherited improper-integral treatment when the initial expected energy is infinite.

These facts are assumptions imported from that theorem, not re-proved by the entropy calculation. Its input identity is recorded in INPUT_BINDING.json. Neither q nor I is assumed computable from finite data.

## A precise variational consequence

For a probability π absolutely continuous with respect to μ, with π(S)=1, define

    J(π)=KL(π||μ)+integral I dπ.

Both summands are nonnegative, with +infinity allowed. Measures failing the absolute-continuity or concentration condition are assigned J=+infinity. Here concentration on S means π(S)=1, not containment of topological support in the possibly nonclosed basin S. For every π with finite J,

    J(π)=KL(π||π*)−log A.                              (1)

Indeed π* has density exp(−I)/A on S, strictly positive there. On S the logarithmic density identity is

    log(dπ/dπ*)=log(dπ/dμ)+I+log A.

The finite-J hypothesis makes the terms integrable. The negative part of f log f is integrable under a probability reference because r log r≥−1/e; this prevents an undefined subtraction. Integrating gives (1). Nonnegativity of relative entropy follows from r log r−r+1≥0, with equality only for the unit density. Thus J(π)≥−log A, and equality is possible only for π=π*.

The minimiser itself has finite J. Since I exp(−I)≤1/e,

    integral I dπ* ≤ 1/(eA)<infinity.

Its logarithmic density is −I−log A on S, so

    KL(π*||μ)+integral I dπ* = −log A.                  (2)

Consequently π* is the unique minimiser, including over the extended-value domain. Combining (2) with the accepted dynamic identity gives

    integral_0^infinity [E(t)−c*]dt
      = KL(π*||μ)+integral I dπ*.                      (3)

This is a decomposition of the ensemble's cumulative excess into a change of initial-coordinate distribution and its selected average transient particle excess. It does not turn the physical endpoint law into a probability on the original coordinates. It does not say the evolving flow globally minimises F, that every finite-time update minimises this limiting objective, or that the potential measures epistemic warrant.

## Endpoint merging requires an exponential conditional average

Put ν=q_#μ, the unweighted distribution of limiting endpoints. Euclidean Borel spaces admit conditional expectation with respect to q. Define a ν-almost-everywhere function

    r(y)=E_μ[exp(−I(x)) | q(x)=y].

No pointwise conditional probability on a zero-mass individual endpoint is presumed. This formula denotes a measurable conditional expectation; alternatively r is the Radon–Nikodym derivative of q_#(exp(−I)μ) with respect to ν. Since 0<exp(−I)≤1 μ-almost everywhere, 0<r≤1 ν-almost everywhere. For positivity, a measurable set where r=0 would have zero integral of a strictly positive variable, and therefore zero ν mass.

Let C={y:F(y)=c*}. Since S=q^−1(C), the exact endpoint law is

    ρ*(dy)=1_C(y) r(y) ν(dy)/A,
    A=integral_C r dν.                                (4)

Define the effective endpoint cost J_eff(y)=−log r(y), finite and nonnegative ν-almost everywhere. The same elementary argument as (1) proves that ρ* uniquely minimises

    KL(ρ||ν)+integral J_eff dρ

over probabilities ρ absolutely continuous with respect to ν and satisfying ρ(C)=1, with optimum −log A. Assign the objective +infinity outside this domain, and choose any finite nonnegative value for J_eff on the ν-null exceptional set; the admitted integrals do not depend on that choice. Therefore this transport preserves the normalising constant, selected endpoint law and variational optimum. It is a genuine mathematical transport of the Gibbs structure, not just a resemblance of vocabulary.

The cost is generally NOT E_μ[I|q]. Conditional Jensen gives

    J_eff ≤ E_μ[I|q],

with the right side allowed infinite. Equality holds only when I is conditionally constant almost surely in each relevant fibre; for finite conditional mean this is the strict Jensen equality criterion for exp(−u). If the conditional mean is infinite, equality is impossible because J_eff is finite. Replacing J_eff by the conditional arithmetic mean can change the endpoint law.

## An exact source-compatible countercontrol

Use the accepted double-well F(x)=(x²−1)²/4, and initial μ=(δ_−1+δ_1+δ_2)/3. The first two particles are already at their endpoints with I=0. The particle starting at 2 ends at 1 and has

    I_2=(3−log 4)/8>0,        a=exp(−I_2) in (0,1).

All endpoint energies equal zero, so all three initial coordinates belong to S. The endpoint prior is ν=(δ_−1+2δ_1)/3. The correct conditional factors are r(−1)=1 and r(1)=(1+a)/2. Therefore

    ρ*({1})=(1+a)/(2+a).

Using the arithmetic conditional mean of I would instead give r_wrong(1)=sqrt(a), and

    ρ_wrong({1})=2sqrt(a)/(1+2sqrt(a)).

These are different: their cross-multiplied positive-numerator difference is

    (1+a)(1+2sqrt(a))−2sqrt(a)(2+a)
      =(1−sqrt(a))²>0.

Thus coarse averaging the transient cost underweights the endpoint reached by two histories. The example uses genuine trajectories and costs from the accepted polynomial dynamics; it does not assign arbitrary costs and call them a physical realisation.

## Scope and scientific credit

The frozen ancestor owns analytic convergence, finite critical values, positive-time regularisation and the exact law limit. Standard entropy algebra owns the variational formula. This supplement supplies their exact composition and shows which cost must survive a many-to-one endpoint map. The finite control distinguishes an exact transport from an attractive but incorrect averaging rule.

It does not infer psychological identifiability, truthful recognition, proper function, metaphysical necessity, a general Bayesian data-generating model, or actual DAEE implementation from this conditional mathematics. Interpreting F, the initial probability, q and I in an applied domain remains a separate semantic and evidential task. Endpoint merging loses histories; the formula does not reconstruct them.

The proof is ordinary written mathematics with symbolic algebra controls. All predecessor bytes remain unchanged. Independent review, when supplied, has its own frozen receipt and is not implied by this author's statement.
