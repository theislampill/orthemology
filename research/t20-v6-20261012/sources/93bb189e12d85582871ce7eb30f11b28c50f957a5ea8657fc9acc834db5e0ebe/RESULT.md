# A finite-horizon repair for the fixed-calibration path-law obstruction

11 October2026 UTC. Additive mathematical application. Elementary classical moment algebra, with explicit source semantics; no general novelty or cognitive-warrant claim.

## Question inherited from the preceding obstruction

A single Bernoulli calibration p is reused for two fresh trials, independent conditional on p. Endpoint kernels p=0,1 miss the largest mismatch probability, and the convex hull of full two-trial laws has infinitely many exposed points. Does this prohibit a finite exact representation? No: finite vertices and finite sufficient coordinates are different requirements.

## Exact two-trial representation

For any probability measure rho on p in[0,1], let mu=E_rho[p], nu=E_rho[p²]. The ordered two-trial law is exactly

  (P00,P01,P10,P11)=(1−2mu+nu, mu−nu, mu−nu, nu).

The feasible coordinate set is exactly

  0<=mu<=1,  mu²<=nu<=mu.

This is the body of mixtures of the declared conditional-i.i.d. fixed-calibration laws. A single deterministic calibration lies on nu=mu². Mere finite exchangeability does not suffice: the symmetric two-trial law(0,1/2,1/2,0) has mu=1/2,nu=0 and lies outside this body. No general representation of all exchangeable testimony is claimed.

Necessity follows from E[(p−mu)²]>=0 and p²<=p. For sufficiency, mu=0 forcesnu=0 and delta0 suffices. For mu>0, nu>0 and the distribution assigning mass mu²/nu to p=nu/mu and the remaining mass to0 has the specified two moments. The supportpoint and weight are both in[0,1]. This finite decomposition depends on the represented point; it supplies no fixed finite vertex list for the entire curved body.

Any declared loss of the two ordered observations has expected value linear in (1,mu,nu). Hence robust evaluation over this entire joint-law hull reduces exactly to optimisation of that declared linear expression over the displayed curved feasible body. For fixed meanmu, mismatch probability is2(mu−nu), so its attainable range is[0,2mu(1−mu)]. The upperendpoint is a fixed calibration p=mu; the lowerendpoint is a mixture of calibrations0 and1. They have different across-trial dependence despite the same single-trial law.

The mixture rho can mean a supplied Bayesian hyperprior, or merely a convex-law representation used to evaluate worst-case linear losses. Neither interpretation is automatically licensed by calibration bounds alone. Optimising a linear path-law loss over all fixed p or over their convex hull gives the same extremal value; that equivalence does not say that every mixed law is a possible original physical calibration. In all cases p is selected once for the paired trials, not independently resampled before each trial.

## Sharp continuation limit at the next trial

Consider two measures on calibration:

  rhoA: mass3/4 at p=1/3, mass1/4 at p=1;
  rhoB: mass1/4 at p=0, mass3/4 at p=2/3.

Both have (mu,nu)=(1/2,1/3), hence exactly the same two-trial law (1/3,1/6,1/6,1/3). But their third moments are5/18 and2/9. After observing two successes, their predictive probability for a third fresh success is respectively5/6 and2/3. The conditioning event has probability1/3 under both, so this is not a null-event artefact or mere missing event-frequency issue.

Thus the two-coordinate repair is complete for its two-trial loss contract and incomplete for three-trial continuation. Retaining additional source/calibration structure or the needed higher moment is a substantive contract extension. This is an explicit finite instance of inherited tensor/moment continuation principles, not a new general finite-moment impossibility theorem.

## Credit and limitations

The parent derived this constructive repair after the reviewer-confirmed kernel-vertex failure in credal-inquiry-root-controls-20261011/DERIVATION.md. H-Continuation already owns operation-relative sufficient moments and their closure requirement. The new local contribution is an exact feasible moment body, point-dependent decomposition, and next-trial discriminator for that specific fixed-calibration obstruction. No claim about actual source reliability, human understanding, metaphysical possibility or proper-function warrant follows from the representation alone.

Exact rational controls supplement the written universal arguments. No Lean or external empirical replay is claimed. Existing reviewed reports and archives are untouched; this is a separate continuation result.
