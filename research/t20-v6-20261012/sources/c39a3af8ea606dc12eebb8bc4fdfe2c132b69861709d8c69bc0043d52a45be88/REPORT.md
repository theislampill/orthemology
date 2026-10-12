# Author report: SOS-dissipative polynomial gradient reverse lift

## Outcome

The stronger certificate theorem is valid under the precise hypotheses in RESULT.md:

    F+C is SOS,
    x·∇F−κ|x|^4+λ|x|²+D is SOS,
    κ>0, λ,D,C≥0.

Every normalized, full-square-positive, coordinatewise C¹ all-polynomial gradient/selection hierarchy for this fixed F is exactly one normalized weighted forward-characteristic evolution from an initial probability with all moments. No initial law, rank promise, or initial tail-growth condition is assumed. Conversely every all-moment initial probability generates such a global path.

The decisive new class-level estimate is A_t(|x|^(2n))≤Y(t)^n, with Y(t)=(λ+Δ coth(Δt))/(2κ), Δ²=λ²+4κD, and Y(t)=1/(2κt) when Δ=0. It is derived before representation using the square-only radial interpolation already proved in the diffusion ancestor. Its Riccati coefficients are independent of n, so it forces compact positive-time laws. Comparison against positive finite-initial scalar solutions handles zero radial moments; no strict-positivity assumption is smuggled in.

The compact polynomial-to-PDE step and tight initial recovery follow the radial quartic predecessor's proof order, with F+C, the appropriate flow growth bound, and image-only smooth invertibility. The flow is forward complete and injective; global surjectivity is neither used nor true. The normalized constant C cancels. The usual representing-law-fibre and finite-initial-rank consequences follow after the law is forced.

## Scope discriminators

The principal example is the nonconvex multiwell F=(|x|²−1)²/4, with κ=λ=1 and D=C=0. Its exact logistic characteristic and integrated killing formulas are checked. Unlike the original radial monomial, it has non-minimizing stationary δ_0 and stationary laws on the unit sphere. Thus neither universal collapse to δ_0 nor convergence to a global minimizer is imported.

The shifted quartic F=(x−1)^4/4 has a short D>0 SOS certificate and a δ_0 path that immediately leaves zero. This tests the zero-root handling and the coordinate restriction removed by D. Its translated dynamics is credited as an inherited coordinate corollary. One explicit two-dimensional nonradial two-well potential demonstrates that the certificate class is not merely radial. These controls do not expand into an unrelated example campaign.

## Evidence and source limits

The initial author run passed 266 finite exact controls, including preservation of the bound old inputs. The final replay count is recorded in EXACT_CHECKS.json; adding input hashes can increase that count without changing the mathematical controls. check_exact.log records the actual run. The symbolic checks cover general scalar formulas and representative polynomial dimensions, not an enumeration-based proof of the infinite hierarchy.

The specialized existence source is Putinar–Schmüdgen, *Multivariate Determinateness*, https://arxiv.org/pdf/0810.0840v1, printed p.24, Theorem 25 and its following attribution to Nussbaum. The inherited primary PDF and page extraction were inspected and hash-bound, and the current primary-web statement was cross-checked. It starts with a positive-semidefinite full multisequence and marginal Carleman conditions; a vector measure is not assumed. No external transport uniqueness theorem, diffusion theorem, or new literature-priority claim is imported.

The author and parent participated in proof development. A separate reviewer was assigned, but no review verdict is claimed by this author packet. The frozen file manifest is the exact handoff boundary for that review.

## Terminal boundary

- Additive written proof and executed exact controls: complete as an author deliverable.
- Bound predecessor bytes: preserved at final replay.
- Protected edits, theorem integration, universal proof-kernel verification, empirical/noetic identification, and T20 closure: not performed or claimed.

The initial D=0 clock estimate remains as a subsidiary refinement. The more general D≥0 certificate is the actual main theorem; the unchanged accepted radial quartic packet remains its own bounded result.
