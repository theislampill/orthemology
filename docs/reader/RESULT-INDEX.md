# Selected results and collection owners

> **C02 reader-design preview — partial coverage.** This branch tests the representative works mapped for Issue 35. It is not the completed C03 catalogue, a new scientific assessment, or the replacement for the current root guide. [Coverage and qualification](../project-closure/reader-refactor-issue-35/PILOT-QUALIFICATION.md).

[Atlas](RESEARCH-ATLAS.md) · [Works](PAPER-CATALOGUE.md) · [Results](RESULT-INDEX.md) · [Frontiers](CURRENT-FRONTIERS.md) · [Applications](APPLICATIONS.md) · [Verification](VERIFICATION-GUIDE.md)

## What this index does

This is a **selected result lookup**, not a replacement scientific registry. Existing result identifiers keep their collection scope. A source-located theorem without a registry entry is reached by its source title and section; the refactor does not mint it a new scientific ID.

For background and editions, use the [work catalogue](PAPER-CATALOGUE.md). For the meaning of proof/review/replay labels, use the [verification guide](VERIFICATION-GUIDE.md).

## Finite mediator

**Existing entry: `T12-FINITE-MEDIATOR`.** [Collection statement and evidence scope][twelfth] · [Ordinary proof, section 5][coordination].

Let `S` have a centred Gaussian law of variance `n > 0`, let `M` have at most `N` values, and suppose `Y` and `S` are conditionally independent given `M`. For a fixed interval `I` of length `L ≥ 0` and a positive integer `N`,

```text
P(Y + S ∈ I) ≤ 2 Φ(NL/(2√n)) − 1.
```

The source supplies a matching fixed-horizon construction. The conclusion quantifies complete-mediation capacity; it does not identify a finite program's description length with a complete mediator. Side information, prescribed state marginals, a common history across horizons and forward-causal realisation are separate conditions. **Evidence here:** written mathematics and the source's scoped records, not a new replay by this reader layer.

## Tensor moments

**Source-located Theorem G:** [Square positivity forces exact dynamics for every coercive polynomial, section 1][coercive]. Related [tensor predecessor][tensor].

In finite-dimensional real space, let `h` be a coercive real polynomial. On an interval beginning at zero, require normalised real linear polynomial functionals `L_t`, coordinatewise `C1` regularity including continuous right derivatives at zero, square positivity for **every** real polynomial, and the full hierarchy

```text
L_t(1) = 1
L_t(q^2) >= 0
L_t'(p) = -L_t(h p) + L_t(h) L_t(p)
for every polynomial p.
```

The written theorem produces exactly one probability law for that **complete path**, with all absolute polynomial moments finite, such that

```text
Z_t = ∫ exp(-t h) dμ
L_t(p) = ∫ p exp(-t h) dμ / Z_t
```

Positive-time full moment records are determinate and the path extends uniquely. A fixed initial moment record can nevertheless admit several representing laws and hence several paths. Initial representability is obtained from the path hypotheses, not assumed.

The successor explicitly removes the predecessor's quadratic/sum-of-squares bridge restriction for this coercive case. It does not replace all-grade square positivity with finitely many positive-semidefinite tests. The objects are commutative polynomial moments, equivalently symmetric tensor moments of a numerical vector, not arbitrary ordered/noncommutative tensors. **Evidence here:** an ordinary written result with its original qualifications; no new kernel proof or human-cognition identification is asserted.

## Fisher geometry

**Existing corollary: `V6-C02`.** [Contribution owner][contributions] · [Fixed-fibre corollary][sidecar] · [Controlling finite-audit source, sections 2–3 and 9][fisher] · [Existing ordinary review][sidecar-review].

The full-source geometry starts from a strictly positive joint law `mu[j,i] = w[j] p[j,i]`. Its categorical Fisher metric is

```text
g = sum_j dw[j] d'w[j] / w[j]
  + sum_j w[j] sum_i dp[j,i] d'p[j,i] / p[j,i].
```

Fix positive normalised conditional columns `P`, with at least two outcomes per column, and a mixture `q = Qw` admitting a positive weight representation. The weight fibre is `W = {w > 0 : Qw = q}`, of dimension `d = k - rank(Q)`.

The corollary requires preservation of selected **ambient full-source** squared gradient norms:

```text
||grad p[j,i]||^2 = p[j,i] (1 - p[j,i]) / w[j].
```

For fixed known conditionals, these norms recover the weights. Therefore a positive-dimensional fibre cannot have an exact finite-valued supplement under this contract. A continuous supplement needs, and on this fixed fibre can use, `d` real coordinates.

This is not the gradient intrinsic to a fibre on which the conditionals are fixed. It is not a globally continuous minimal chart across changing-rank strata, and it does not require full weight retention for the weaker posterior-answer-only task. The contribution owner records an ordinary reviewed corollary, with no external-novelty claim; its existing review is not a new independent review of this refactor.

### A metric with observable consequences

The controlling Fisher paper also gives an explicit dynamical test, not only a counting obstruction. With a two-state target, retain the three conditional laws

```text
p₁ = (1/4, 3/4)
p₂ = (1/2, 1/2)
p₃ = (3/4, 1/4)
```

Both weight vectors `(1/4, 1/2, 1/4)` and `(1/8, 3/4, 1/8)` give the same mixture `(1/2, 1/2)`. For the stipulated objective `J = p₁,₁`, however, the negative full-source Fisher velocity of `p₁` is respectively `(-3/4, 3/4)` and `(-3/2, 3/2)`. A record can therefore preserve the conditional answers and current mixture while failing to preserve their dynamics. The source’s [section 9 control][fisher-control] supplies the example; the refactor is not claiming a new experiment.

The positive classification is also useful: for the source’s ambient `C2` objective on the full strictly positive domain, with more audit outcomes than target states, its negative full-source Fisher gradient flow projects consistently to the retained signature exactly when the restricted objective is a function of the current target alone. Here “descend” means the same projected dynamics for every admissible discarded-weight representative, not merely making a loss smaller. For this case the source supplies a closed target flow. Restricted source families, other metrics and the complementary cardinality regime have different conclusions. The [classification and assumptions][fisher] must accompany any application; numerical decrease is not itself epistemic warrant.


## Joint feasible readings and completions

**Existing join: `V6-R04`.** [Contribution owner][contributions] · [Join report][join] · [Source-relative occurrence records][occurrences] · [Missing-outcome analysis][missing] · [Existing review][join-review].

The selected complete occurrence relation has only `(M,M,G)` and `(G,G,G)`. Its coordinate marginals also admit `(M,G,G)` and `(G,M,G)` when combined freely, but those extra rows lack a complete witness in that selected relation. The incomplete row is not a wildcard.

For missing outcomes, the source's endpoint bounds require jointly feasible completions to be sharp. Two binary coordinates may each permit zero and one while the feasible joint relation permits only `(0,1)` and `(1,0)`. Their total is then always one.

The shared operation is retention of the admissible joint relation before projection or optimisation. The owner records this as an inherited source-bound join, not a new general theorem, fresh primary acquisition or actual empirical coupling. Its linguistic and empirical contracts remain distinct.

## Philosophical arguments have source routes too

The positive recognition/correction route is not forced into a theorem status it does not own. Read the [atlas account](RESEARCH-ATLAS.md#recognition-sound-cognition-and-correction), the [source substrate][sound] and the [later retained-passage qualification][retained]. Their arguments, premises and source scopes are visible without either declaring them kernel-verified or erasing their affirmative content under a blanket “open” label.

## Collection owners

These collections must remain separately discoverable when the full index is completed. Their presence here is a coverage route, not proof that every contained result has been substantively re-read for this preview.

| Collection | Existing lookup / evidence owner | Keep distinct |
|---|---|---|
| Original v5 consolidation | [Theorem/argument index][v5-index] and [provenance guide][v5-guide] | Original statements, derived adapters and source-construction scope. |
| Predecessor continuations and final-Sixth overlay | [Result status][continuation-results] and [continuation guide][continuation-guide] | Earlier families, later overlays and exact suite variants. |
| Seventh–Twentieth successors | [Result status][successor-results], [evidence bindings][successor-evidence], [twelve avenues][avenues] | Registered statement scopes, source owners and scientific evidence. |
| Later T20 live checkpoints and S01 | [Collection guide][live-guide] and [checkpoint index][live-index] | This additive collection does not simply replace the frozen registry. |
| T20 v6 synthesis and repaired sources | [Contributions][contributions], [source recovery][source-recovery], [current source graph][source-graph] | Reused/public/held source identities, formal components and ordinary work. |
| AR8R theorem and research records | [Collection guide][ar8r-guide] and [theorem-origin owner][ar8r-origin] | Historical theorem identities, bounded interpretations and recorded failures. |
| AR8R proposals and semantic reissues | [Post-merge proposal guide][ar8r-proposals] and [evidence catalogue][ar8r-post] | Preservation or intake is not proposal adoption or replacement of an old verdict. |
| Designed public experiments | [Packet status][experiment-status] | A runnable smoke test, planned experiment and empirical result are different things. |

The independent [candidate/owner map][owner-map] retains all baseline paths, including substantive candidates outside those obvious paper directories. The next stage must reconcile the actual works and results against that population. It must not silently treat the selected entries above as comprehensive coverage.

[twelfth]: ../../experiments/orthemology-v5-successors/groups/t12-written/README.md
[coordination]: ../../experiments/orthemology-v5-successors/source-store/c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7/BOUNDED_COORDINATION_INFORMATION_v1.md
[tensor]: ../../research/t20-v6-20261012/sources/449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a/tensor-realizability-extension-20261010__RESULT.md
[coercive]: ../../research/t20-v6-20261012/sources/204f63e544b1afd9538230f95f8ebfbc613b9847c579dfb901de6d10e40ebb10/coercive-square-positivity-20261010__RESULT.md
[fisher]: ../../research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md
[sidecar]: ../../research/t20-v6-20261012/research-v6/root_math/FINITE_SIDECAR_GEOMETRY_BOUNDARY.md
[sidecar-review]: ../../research/t20-v6-20261012/research-v6/type_collective/GEOMETRY_SIDECAR_REVIEW.md
[join]: ../../research/t20-v6-20261012/research-v6/root_math/occurrence_feasibility_join/REPORT.md
[occurrences]: ../../experiments/orthemology-v5-successors/source-store/67f405c245093546dd26c142db7fd09eea1513b9fb853521d496bca7a70e8a62/source_rows.json
[missing]: ../../experiments/orthemology-v5-successors/source-store/8bb522943f659e2f50a97fe8987f48d851a7fc1577f020995ac43dc31ebfe115/MISSING_OUTCOME_ANALYSIS_v1.md
[join-review]: ../../research/t20-v6-20261012/research-v6/type_collective/terminal_synthesis_reconciliation/OCCURRENCE_DELTA_REVIEW.json
[sound]: ../../research/t20-v6-20261012/sources/55bc1626342a1d5863ec271f64a121bc1615aa796a542b513f042f536a2c1810/sound-reason-epistemology.md
[retained]: ../../research/t20-v6-20261012/research-v6/foundations/retained_passage40/REPORT.md
[contributions]: ../../research/t20-v6-20261012/research-v6/synthesis/CROSS_CONTRIBUTIONS.json
[v5-index]: ../provenance/v5-consolidation/THEOREM_INDEX.md
[v5-guide]: ../provenance/v5-consolidation/README.md
[continuation-results]: ../provenance/v5-research-continuations/RESULT_STATUS.json
[continuation-guide]: ../../experiments/orthemology-v5-continuations/README.md
[successor-results]: ../provenance/v5-successors/RESULT_STATUS.json
[successor-evidence]: ../provenance/v5-successors/EVIDENCE_BINDINGS.json
[avenues]: ../provenance/v5-successors/TWELVE_AVENUES.json
[live-guide]: ../../research/t20-live-20261009/README.md
[live-index]: ../../research/t20-live-20261009/INDEX.json
[source-recovery]: ../../research/t20-v6-20261012/SOURCE_RECOVERY.md
[source-graph]: ../../research/t20-v6-20261012/CURRENT_SOURCE_GRAPH.json
[ar8r-guide]: ../project-closure/ar8r-v11/README.md
[ar8r-origin]: ../project-closure/ar8r-v11/provenance/AR8R-CANONICAL-THEOREM-ORIGIN-REGISTRY-V5-PUBLIC-SANITIZED.yaml
[ar8r-proposals]: ../project-closure/ar8r-v11/post-merge-proposals/README.md
[ar8r-post]: ../project-closure/ar8r-v11/AR8R-V11-POST-MERGE-EVIDENCE-CATALOG.yaml
[experiment-status]: ../../experiments/experiment-status.yaml
[owner-map]: ../project-closure/reader-refactor-issue-35/OWNER-MAP.json
[fisher-control]: ../../research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md#9-decisive-controls-and-the-connection-to-inquiry-value
