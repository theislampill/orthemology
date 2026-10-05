# Missing outcome bounds for supported continuation

Analysis companion to the prospective validation specification v5  
Thirteenth Orthemology · 4 October 2026

These bounds retain every assigned organisation-episode and show how unknown outcomes could change success rates and contrasts. This is an elementary clarification of v5, not an amendment, an executed study or a new theorem. All examples are invented.

## 1. Keep the outcome and its observation separate

The fixed binary outcome is original-contract, whole-cell supported continuation: an actual handoff, a warranted determination on the designed-resolvable novel case, warranted uncertainty on the unresolved case, delivery within the original deadline, and the specified case-linked support evidence. Permitted compensation can satisfy whole-cell continuation without establishing incoming-role transfer. Revised-deadline fulfilment and later recovery remain separate.

For each assigned episode, apply three **assessment states**, not three substantive outcome values:

- **Known success:** every required component is established as satisfied.
- **Known failure:** at least one required component is established as failed, even if another component is unmeasured. A known timeout or failed handoff remains a failure despite missing video. Warranted DEFER on the designed-resolvable case can receive positive warrant credit yet fail primary completion; warranted uncertainty on the unresolved case satisfies that component.
- **Unknown:** no required component is established as failed, but the available evidence does not determine whether every component was satisfied.

**Resolve the evidence ambiguity.** “Case-linked support evidence” could suggest that anything absent from the investigator's dossier is failure. Sections 4–5 of v5 resolve this: trace gaps are unassessable support, and otherwise unknown composites receive bounds. Known non-delivery of a required certificate or an established unsupported scored decision can establish failure. Inability to assess a certificate's or support trace's original existence, contents, linkage or timing can instead leave status unknown. A failed required certificate component at the scored decision is not repaired by hypothesising competence. Apply v5's decision-time coding: genuinely supported re-evaluation within the original deadline is assessed at its own time; every earlier unsupported statement need not cause irrevocable episode failure.

Missing recording alone proves neither unsupported action nor absent competence; other evidence can still establish success or failure. Correct output alone does not establish success. Credible temporally linked evidence may establish earlier support; later correct reconstruction alone cannot. The upper bound permits completion of missing observations under the **same evidence-bearing endpoint**, without substituting latent ability or waiving the certificate requirement.

## 2. Bounds with the full assigned denominator

For arm *a*, let *Sₐ*, *Fₐ* and *Uₐ* count known successes, known failures and unknowns; *Nₐ = Sₐ + Fₐ + Uₐ > 0* counts **all assigned episodes**. The scoring rubric must fix admissible binary completions; an undefined criterion is not ordinary missingness. If *xₐ* unknown episodes satisfy the outcome, the completed assigned-arm success proportion is

**pₐ = (Sₐ + xₐ) / Nₐ**, where **0 ≤ xₐ ≤ Uₐ**.

Thus the worst and best rates are

**Lₐ = Sₐ / Nₐ ≤ pₐ ≤ Hₐ = (Sₐ + Uₐ) / Nₐ = 1 − Fₐ / Nₐ.**

For a contrast of arm *a* minus arm *b*, the risk-difference bounds are

**Lₐ − Hᵦ ≤ RDₐᵦ = pₐ − pᵦ ≤ Hₐ − Lᵦ.**

The lower endpoint makes all unknowns in *a* failures and all in *b* successes; the upper reverses this. The width is *Uₐ/Nₐ + Uᵦ/Nᵦ*. Nonreceipt, failed handoff, withdrawal and technical outages are classified using available component evidence; no assigned episode leaves the denominator.

**Sharpness.** The endpoints are attainable and cannot be narrowed from these counts alone if either status is consistent with each unknown's observed components and the extreme completions are jointly possible across episodes and arms. The inequalities require no statistical independence. Additional restrictions may narrow feasible completions; endpoints ruled out by those restrictions are not sharp. Finite success totals are integers, so attainable proportions and differences form discrete sets; these intervals give their extreme limits. A missingness model adds assumptions and should be reported alongside the bounds as v5 requires.

## 3. Preserve the four arm contrasts

Write **++**, **+−**, **−+** and **−−** for the access-route × interpretation-support packages. The primary contrast remains **p₊₊ − p₋₋**, joint support minus neither added support. Apply the same pairwise formula separately to the prespecified simple contrasts:

- Access at I+: *p₊₊ − p₋₊*; access at I−: *p₊₋ − p₋₋*.
- Interpretation support at A+: *p₊₊ − p₊₋*; interpretation support at A−: *p₋₊ − p₋₋*.

The interaction remains secondary and subject to adequate precision. None of these calculations conditions on achieved receipt or comprehension, changes the primary contrast, or identifies causal mediation.

## 4. Two illustrative primary contrast calculations

These counts illustrate arithmetic, not data or recommended sample size. The other two arms remain in the design but are omitted from this display.

| Example | Assigned arm | Known success S | Known failure F | Unknown U | All assigned N | Success rate bounds |
|---|---|---:|---:|---:|---:|---:|
| 1 | Joint support ++ | 15 | 3 | 2 | 20 | 75% to 85% |
| 1 | Neither added support −− | 7 | 10 | 3 | 20 | 35% to 50% |
| 2 | Joint support ++ | 10 | 4 | 6 | 20 | 50% to 80% |
| 2 | Neither added support −− | 8 | 6 | 6 | 20 | 40% to 70% |

**Example 1:** RD lies between *75% − 50% = +25* and *85% − 35% = +50 percentage points*. Even the least favourable missing-outcome completion leaves a positive difference in these assigned-arm proportions.

**Example 2:** RD lies between *50% − 70% = −20* and *80% − 40% = +40 percentage points*. Both signs are compatible with the unknown outcomes; the ordering of completed arm proportions is inconclusive.

## 5. Identification is not statistical precision

These missing-outcome identification bounds are **conditional on observed assigned-arm counts**. They quantify incomplete assessment, not randomisation or sampling uncertainty. Example 1's positive lower endpoint is not a positive lower confidence limit, proof of population benefit or power assurance.

Inference for v5's intention-to-treat package probabilities still requires organisation-level uncertainty analysis respecting assignment and any stated missingness assumptions. Members and repeated decisions are not extra independent episodes. Report counts, bounds, uncertainty and separate components together; complete-case analysis remains secondary. These calculations supply neither the unspecified planning model, minimum relevant difference, target precision nor sample size, and do not change v5's bounded population or service.

**Source:** *Prospective Validation Specification v5*, §§1–2 and 4–5. The source specification is unchanged.
