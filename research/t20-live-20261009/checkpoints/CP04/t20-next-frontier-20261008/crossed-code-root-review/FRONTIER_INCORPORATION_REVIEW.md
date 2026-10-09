# Narrow incorporation review: calibration-design-frontier/RESULT.md

8 October 2026 UTC. This supplements, and does not enlarge, the independent root-certificate review into the arbitrary-rate count appendix.

## Verdict and bound version

**Pass for the crossed-code content of the bound main report.** Reviewed SHA-256:

`89b17388c4f243f555dbcb2232a3f106683cc3cc23edf0e3f7371bec3e018db7`.

The snapshot is `frozen/FRONTIER_RESULT.md`. Its companion receipt explicitly excludes `ARBITRARY_RATE_COUNT_BOUND.md`, the count-rate claim in Main finding 3, other appendix claims repeated in the main report, and the author's source/executable-control audit. No completeness or closure is implied for those excluded items.

## Findings

1. **Faithful inherited result.** The main report correctly distinguishes rate attenuation from issued-root profiles, catalogue histograms from physical architectures, population identification from finite numerical recovery, and the exact-corner instrument from the predecessor's strictly interior base4 calibration. Its adaptive kernel, persistence, single-fixed-panel rank, ordered-code, weight-floor, and oracle assumptions match the independently checked root result.

2. **Known product-channel extension.** The newly added §2 subsection constructs the correct ordered-pair matrix and uses the independently verified determinant, including its sign and its exact nonzero criterion for swapped profiles. Its explicit conditional-product premise prevents importing it into the later arbitrary-coupling guarantee. A/B count equality in that paragraph retains the same product-channel premise. No claim that independence is necessary for every possible invertible known joint channel is made.

3. **Independent nonidentical groups.** The extension in §3 is valid. Each code indicator may have mean `p_(g,i)`, but the per-group error bounds give the same separation for their average. The exponential moment product is bounded using `sum_g p_(g,i)`, so the Chernoff proof uses its average p exactly as written. Hoeffding for independent bounded variables likewise gives `sqrt(log(8/delta)/(2n))`; adding the uniform bias allowance beta is valid. Shared drift requires the additional conditional promises identified in the text.

4. **Calibration confounding.** Section 5 gives an exact fixed pair of indistinguishable worlds, not merely a failed sufficient bound. Pure A at rates `(1,0),(epsilon,1)` produces ordered probabilities `(0,0,1-epsilon,epsilon)` in order 00,01,10,11. The ideal-corner mixture `(1-epsilon)A+epsilon OR` produces the same vector. Both obey the per-label corner-error promise, including for absent catalogue labels, and the positive-weight floor is epsilon when `0<epsilon<=1/2`. The author adopted the requested explicit `0<w<=1/2` range in the impossibility statement. This does not contradict the small-error sufficient regime `eta<=w/16`.

5. **General code/antichain statement.** Section 6 correctly extends the union-bound support argument to a known finite catalogue with distinct ideal words. Assigning unused words arbitrarily cannot hurt the guarantee on the ideal word. The `N<=2^R` bit bound is explicitly restricted to deterministic single-transcript labelling. For the finite unguarded route model, a corner T responds exactly when it contains a present support; its inclusion-minimal responding sets are exactly the inclusion-minimal present supports. This proves the antichain quotient in both directions. Multiplicities and absorbed supports are lost. The mathematical proof, rather than a finite check, supplies the general result.

## Additional exact controls

`frontier_incorporation_controls.py` independently checks four rational calibration-confounding examples and all 27 histograms with multiplicities 0,1,2 on supports A,B,AB. These yield precisely five corner-response equivalence classes, in bijection with their minimal-support antichains. Three optional pure-label examples show how the confounding obstruction could also be extended to larger floors by using common half-rate calibration; the author appropriately does not rely on this unneeded extension.

The already recorded exact and symbolic determinant controls cover the newly incorporated known-channel subsection. Final replay and final live-source binding both passed. These are mathematical controls only; they do not validate the response law or calibration in a physical apparatus.
