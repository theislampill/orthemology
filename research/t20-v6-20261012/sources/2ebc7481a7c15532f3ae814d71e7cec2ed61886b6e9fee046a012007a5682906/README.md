# Compact observation-to-repair boundary

A separate classical extension, 2026-09-30. The earlier source return and both query/common-observation audit seals remain unchanged. Main source and deletion controls compile with only standard Lean axioms. Independent review passed in the separate compact-observation-audit packet; INDEPENDENT_REVIEW.json binds its exact manifest and receipt. A five-module portable replay also passed.

## Result

Let candidate path laws nu_theta all dominate one NONZERO reference mu, in the direction mu << nu_theta. Let X be the same action-output map under every candidate. Suppose that, for each fixed target good_theta, X is eventually in that target almost surely under nu_theta.

A common accepted action exists for an arbitrary target family if the action space is compact and all targets are closed. More generally it suffices that X is eventually confined under mu to one compact set C, with all targets closed in the ambient action space. The conclusion then supplies an action in C accepted by every target.

One compact target is enough: success for that target transfers to mu and supplies the required confinement. The whole action space need not be compact.

The proof uses absolute continuity to transfer each success to mu, finite intersections to meet each finite target subfamily, and compactness's finite-intersection property to meet the whole arbitrary family. There is no theorem-priority claim.

## Concrete score interface

For continuous real-valued losses L_theta,j(a), each nonworsening set

    {a | for every truth constraint j, L_theta,j(a) <= baseline_theta,j}

is closed, even for infinitely many truth constraints or standards. The literal score wrapper assumes that, within each fixed standard theta's success event, ALL truth constraints j are eventually satisfied simultaneously. It does not assume or conclude a common almost-sure success event across the arbitrary theta family. The compact-confinement theorem yields one common nonworsening output.

The module includes a concrete weighted-quadratic specialization on the convex hull of finitely many truth vectors. That hull is compact. The output lies in the same hull and satisfies every weighted quadratic comparison. Positive weights are not needed for the topological closedness step; their normative/proper-score role would be an additional application premise.

Combining this with an independently proved empty common-repair region shows that candidate success laws cannot share the required nonzero full-path reference. This is a genuine conditional observation/geometry crosswalk; it neither chooses the authoritative score nor supplies original representation or intellectual hosting.

## Exact boundaries

- Domination is for COMPLETE path laws, not merely all finite prefixes and not two laws dominated by a third
- The action-output map, target sets and score baselines are fixed across the comparison. A time-varying disturbance or score cannot be silently dropped from the action/state contract. Adding a limit point to compactify a changing problem may introduce an artificial common action
- The confinement theorem asks for eventual confinement under the reference itself. Merely naming a compact C does not suffice
- In the compact-space version, closedness is in the chosen action topology; the action space may itself be a coherent domain with its subspace topology. In the ambient compact-confinement version, the literal theorem assumes ambient-closed targets
- The proved success hypothesis is eventual EXACT membership in each fixed target. Approximate or convergence-only formulations need their own theorem; this result does not silently substitute them
- Generator continuity does not imply forecast-loss continuity at singular endpoints. Smooth scores with unbounded endpoint derivatives need a separate closed-target or lower-semicontinuity argument before using this score wrapper. The quadratic specialization is globally continuous
- For an infinite target family, the common accepted action need not be realised by X at any time. For example, reciprocal outputs approach the common point 0 of the closed targets [0,1/(theta+1)] without ever taking that value. No common almost-sure joint tail event or computable selector is established
- Constructing the actual path laws and a measurable/nonanticipating output is separate from this set-theoretic consequence once success events are given

## Deletion controls

The nonclosed-target control uses X_n=1/(n+1), confined to compact [0,1], with fixed targets (0,1/(theta+1)]. Every target is eventually met under the SAME Dirac probability law, but their intersection is empty. The omitted limit point 0 is exactly why closedness fails.

The noncompact control uses natural-number actions X_n=n and closed tail targets [theta,infinity). Every fixed target is eventually met under the SAME nonzero law, but no action is accepted by all targets. The module proves that the natural-number action space is not compact.

The independent reviewer separately verified a missing-confinement control and the stronger conclusion control where the unique common point is never output and there is no uniform simultaneous-target tail. The previous common-observation audit already supplies reversed-domination, zero-reference and finite-prefix/full-path controls.

## Files and kernel targets

- lean/CompactObservationBoundary.lean: compact-confinement theorem, compact-space and one-compact-target wrappers, closed nonworsening targets, continuous-score theorem, finite-hull quadratic application
- lean/CompactBoundaryControls.lean: explicit nonclosed and noncompact deletion controls
- evidence/: author compilation and qualification logs

Main frozen SHA-256: 874ceabb1267306eaff41f28fa4e2450c47d6bc10cdde2e7cee4ce5819dd1b10. This is an extension of the previously audited classical boundary, not a replacement for policy-law CIRS necessity or a meniscus promotion.
