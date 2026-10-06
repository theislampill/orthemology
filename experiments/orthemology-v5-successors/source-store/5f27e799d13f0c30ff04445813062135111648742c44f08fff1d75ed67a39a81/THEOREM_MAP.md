# Ordinary-to-formal statement map

All theorem names below are prefixed CoveringKernel unless stated otherwise. Every main result quantifies over arbitrary finite label types and parameters.

| Accepted ordinary obligation | Formal statement | Exact limit |
|---|---|---|
| A path avoids T iff its complement contains T | disjoint_iff_subset_compl; complement_portfolio_iff | Finite label sets; no physical inference from the definition |
| Complementary q portfolios and (m−q) covers have the same cardinality | complement_card; portfolio_cover_sizes_iff | Families are sets; repeated trials are handled separately |
| Least portfolio size is C(m,m−q,k) | least_portfolio_eq_coveringNumber; coveringNumber_attained; coveringNumber_le_portfolio_card; minimal_portfolio_attained | Attainment uses k≤m−q and q≤m |
| Numeric C depends only on label count | coveringNumber_equiv; coveringNumber_eq_C | Full equivalence transport, not one numerical case |
| Adaptive failures follow one ordered portfolio | Actions.common_history_of_spine_failure; Actions.actual_failure_history_and_spine; Actions.success_iff_portfolio | Full actions/commands, full observations, arbitrary history dependence; opaque constraint only on compatible failure prefixes |
| Adaptivity cannot beat a cover | Actions.deterministic_cap_lower_bound | Fixed prepared family, uniform q supports; opaque macro observations |
| Exhaust a minimum portfolio | deterministic_cap_attained; Actions.fullCommand_root_world_cap_attained | Fresh nonce and fixed repair body proved in the latter; physical macro closure remains a premise |
| Exact feasible cap | exact_opaque_cap_iff | Canonical symbolic observer with truthful receipt; full-command lower bound separately generalizes arbitrary action choices |
| At m=3k+1, q=2k+1, N=choose(3k+1,k) | self_blocks_forced; coveringNumber_self; minimum_labels_exact_cap; minimum_labels_cap_iff | Generic k; no finite-case enumeration |
| Maximal-world covering equals compatible-root availability | available_source_iff; source_cover_iff | Imports exact copied RootImage/Availability dependency; B,c≥1 |
| Every uncovered T is one fixed compatible actual-root world | deterministic_below_cover_fixed_root_world | A has cardinality c; S contains actual roots and has cardinality B |
| Per-world almost-sure caps cannot improve deterministic optimum | RandomizedFinite.exists_coin_success_all; Actions.randomized_ae_cap_lower_bound | Finite candidate worlds; arbitrary seed space; one world-independent probability law |
| One fixed map/fault set has non-null cap failure | Actions.randomized_below_cover_fixed_root_world | A,S chosen outside AE quantifier; no coin oracle |
| Intervention hit corresponds to target achievement only with the right initial condition | RepairState.after_true_iff; RepairState.defective_start_iff_successWithin; RepairState.correct_start_already_done | Canonical identity-or-repair target coordinate; defective start for lower bound, zero attempts permitted if initially correct |
| Homogeneous full replies remain possible with truthful effect receipts | Actions.canonical_opaque; canonical_opaque | Symbolic observation-law construction; physical admissibility remains source premise |

## Dependency correspondence

Copied dependencies/RootImage.lean and dependencies/Availability.lean are byte-identical to the attribution central-v1 checkpoint. Availability.maximal_taint_realizable establishes for every T of size B+c−1:

- an A with |A|=c;
- S contained in actualRoots A with |S|=B;
- taintedLabels A S = T.

Availability.available_iff proves robust actual-root availability ↔ maximal-label-set availability by realizing every maximal T and extending every smaller actual taint set. SourceCorrespondence uses these exact theorems rather than assuming independent label faults. The full-command upper theorem also returns to actual-root availability, so the source's ≤B cases are all covered.

## Smaller path-only adapter

OpaqueSearch and RandomizedSearch provide readable specializations where selected paths are the actions and the attempt index represents freshness. They are not the sole formal basis of the complete observation claim. OpaqueActions and FullCommandInterface retain arbitrary full-command choices, full history-dependent observations, and proved fresh nonces for the upper construction.

## Not encoded as new conclusions

Safety against all allowed q/r pairs, durable authenticated cancellation, real service, and phase/horizon accounting are retained accepted premises and/or separate existing kernels. This packet does not claim to mechanize the complete physical temporal protocol. Its new verification credit is the quantified covering/search optimum, probability-cap argument, and explicit actual-root correspondence.
