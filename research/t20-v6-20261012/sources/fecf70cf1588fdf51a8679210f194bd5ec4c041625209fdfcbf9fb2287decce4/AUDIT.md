# Independent audit of the compact common-observation extension

**PASS at the frozen theorem's stated scope.** The compact extension and its three pinned local dependencies passed a fresh independent build. Seven theorem/helper type and axiom readbacks were inspected. The argument is a classical finite-intersection compactness corollary; no novelty or full CIRS necessity claim follows from this audit.

Main frozen source: `874ceabb1267306eaff41f28fa4e2450c47d6bc10cdde2e7cee4ce5819dd1b10`.

## The actual quantified result

The main theorem has an arbitrary index type of targets. It requires one nonzero reference measure mu, full-path absolute continuity in the direction mu << nu_theta for every candidate, one common output map X, closed target sets, and one compact C that eventually contains X almost surely under mu. Each candidate law separately gives eventual membership in its own fixed target. The conclusion is one point of C belonging to every target.

The proof transfers each candidate's success to mu. For each finite target subfamily, it intersects only finitely many almost-sure events with confinement, chooses one path, and intersects only finitely many eventual-time conditions. This gives the finite-intersection property inside C. The final step is exactly Mathlib's `IsCompact.inter_iInter_nonempty`, whose hypotheses were checked against the source at `Mathlib/Topology/Compactness/Compact.lean:266`.

No uncountable intersection of probability-one events is formed. The common point need not be an output ever produced by X. The theorem does not supply a measurable selector, an algorithm, one uniform time, or an almost-sure path satisfying every target simultaneously. The index family can be uncountable because compactness acts on closed sets after the finite probability argument is complete.

The reference need only be nonzero, rather than a probability or SFinite measure. The proof consumes the stated almost-sure predicates; it does not construct path laws or prove that X is a measurable, causal stochastic-process output. Those remain application obligations.

## Wrappers and score domains

The compact-space wrapper takes C to be the whole action space. The one-compact-target wrapper transfers success for its explicitly selected target to the reference, obtaining the needed confinement. Neither wrapper changes the direction or full-path nature of absolute continuity.

The continuous-score wrapper forms closed intersections of weak sublevel sets. Targets and baselines are fixed. Its success premise puts “for every truth constraint j” inside eventual membership for each fixed theta. The theorem does not replace this with a joint probability-one statement over the arbitrary theta family. It establishes weak nonworsening comparisons, not strict improvement.

The quadratic specialization uses the convex hull of finitely many vectors in a finite-dimensional real space. The compactness and score continuity conditions are discharged in Lean. The vectors need not lie in a unit cube for this topological result. Positive weights are not needed for continuity or closedness; positivity and proper-score interpretation remain separate application conditions.

For the confinement theorem, target closedness is in the declared ambient topology. The action space can instead be explicitly chosen as a coherent domain with its subspace topology when using the compact-space wrapper. Continuity of a generating potential alone does not establish forecast-loss continuity at singular boundary points. The exact hypothesis is continuity of the displayed real-valued loss; the quadratic case satisfies it globally.

The result concerns exact eventual membership in fixed targets. It does not silently cover time-dependent shrinking targets, changing baselines, or convergence toward a target that is never entered. Compactifying a different problem by adding an artificial limiting action changes the action/target contract.

## Deletion controls

The frozen author controls were separately copied and replayed against this audit's fresh dependencies. They establish:

- **Closedness is essential:** X_n=1/(n+1) remains in compact [0,1] and eventually belongs to each fixed target (0,1/(theta+1)] under the same Dirac probability law. Their common intersection is empty. The module proves that the target at theta=0 is not closed. Here theta indexes a fixed family; the target does not change with time along a single success requirement
- **Compactness is essential:** natural-number outputs X_n=n eventually satisfy every fixed closed tail target [theta,infinity) under the same law, with no common accepted action. The module separately proves noncompactness of the natural-number action space

The independent `ConfinementControl.lean` adds the missing-confinement deletion: C={0}, target={1}, and X constantly 1 under a common Dirac probability law. C is compact, the target is closed, absolute continuity holds reflexively, and exact eventual success holds. There is no accepted action in C. A second theorem verifies that reference-law eventual confinement actually fails. Thus merely naming a compact C cannot replace its confinement premise.

The separate `ConclusionScopeControl.lean` keeps closed targets [0,1/(theta+1)]. Their unique common point is 0, while every output 1/(n+1) is positive. The module proves that each fixed target is eventually met, no observed output meets every target, and no uniform eventual tail meets all targets simultaneously. This confirms the distinction between a common accepted point and an actually realized common output without weakening any fixed-target requirement.

The earlier independently checked common-observation boundary already contains reversed-domination, zero-reference and finite-prefix/full-path controls. They were not duplicated here. This extension retains those exact premises. In particular, mutual absolute continuity of every finite transcript prefix is insufficient for its full-path premise.

## Evidence and custody

`REPLAY_RESULT.json` binds the fresh four-module build. `logs/TypeReadback.log` contains seven exact type/axiom readbacks. `logs/CompactBoundaryControls.log`, `logs/ConfinementControl.log` and `logs/ConclusionScopeControl.log` record ten control theorem readbacks. Only `propext`, `Classical.choice` and `Quot.sound` occur in the inspected axiom reports.

No author-produced local `.olean` was used. The three local dependencies were rebuilt before the extension, using the pinned Lean binary and Mathlib/package build paths. Author sources and earlier sealed packets were preserved. The final receipt and manifest bind the precise source, control and log bytes covered by this verdict.
