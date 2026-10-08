# Exact proof map and interpretation boundary

The authoritative code is in lean/GroundExtension.lean, lean/GroundExtensionControls.lean and lean/ModalCapacityControl.lean. All use only Lean4.19's Init closure, directly or through the preceding local module. The replay and axiom audit bind the final bytes separately.

## General definitions

- `Path R a b`: finite reflexive-transitive reachability, oriented from source to recipient.
- `Acyclic R`: no direct edge a→b followed by a path b→*a.
- `addRoot R B`: adds `none` with arrows to the old nodes satisfying B; no edge enters `none`.
- `Root E S w a`: actual existence at w and no incoming support arrow at w.
- `Coverage E S w`: every existing node at w is reached from an existing root.
- `Necessary E a`: the same individual exists at every supplied modal index.
- `extSupport`: uses the roots of the distinguished actual index w₀ as a fixed set of new ground targets at every index.
- `GroundNecessitates`: each stated grounding edge necessitates target existence across indices, conditional on source existence. This is not imposed on all support or production.
- `liftProfile`: exact preservation on tuples of old individuals. Its index type is arbitrary; quantification over newly added metaphysical individuals is not concealed inside the claim.
- `liftHolderWith Q H`: the new root's standing-holder predicate is Q, while every old holder value stays fixed.

## Design-to-theorem mapping

| Design claim | Kernel-checked declarations | Scope |
| --- | --- | --- |
| G1 old profile | `old_profile_iff`, `old_productive_iff`, `productive_power_preserved`, `old_necessary_iff` | Old-agent tuples and old modalities only; no invariance of broad originality or full-domain formulas. |
| G2 exact old paths | `path_lift`, `path_old_endpoints`, `old_path_iff`, `path_to_new` | Both directions, including closures rather than merely direct-edge preservation. |
| G3 acyclicity | `acyclic_preserved` | Optional base acyclicity; no cycle can enter the new root. |
| G4 well-foundedness | `accessible_new`, `accessible_old`, `wellFounded_preserved` | Source-before-recipient ancestry orientation. Coverage does not imply well-foundedness. |
| G5 actual completion | `new_is_root`, `no_old_actual_root`, `actual_root_iff_new`, `actual_coverage_preserved` | New root is original at every index; uniqueness and transferred coverage are stated at w₀ only. |
| G6 grounding | `ground_necessitation_preserved`, `ground_path_necessitates`, `ground_in_support_preserved`, `support_endpoints_preserved` | Added targets must be necessary actual roots. Closure composition is for grounding paths, not mixed support paths. |
| G7 separation | `necessary_original_particular`, `no_original_power_bearer` | First variant deliberately assigns no standing power to the new root. It omits any further perfection axiom requiring power. |
| Standing-power variant | `original_holder_iff_ground_holder`, `no_original_actual_producer`, `capable_ground_without_actual_production` | An original standing holder is available with Q=true, while actual productive attribution remains absent. Predicate interpretation alone is not a complete modal theory of ability. |

The mathematical root is an adjoined individual in `Option A`. It is not inferred to exist in the actual world. Whether a proposed noncausal fact supplies such an individuated reality is the philosophical premise kept visible in the appraisal.

`Root` records absence of incoming edges in the represented support relation. Reading it as complete existential nonreceipt requires that relation to exhaust the relevant support; the code does not prove that representation claim. Likewise, `Necessary` quantifies over the supplied indices. Interpreting those indices as every metaphysically possible circumstance is an additional application claim. No accessibility logic or universal ontology of dependence is smuggled into either definition.

## Discriminating controls

`GroundExtensionControls` supplies a nonempty two-node productive base at two modal indices. Its actual agent is a necessary original holder; the actual effect is contingent. The base has actual coverage, well-founded ancestry and a real productive edge. The extension preserves coverage and necessitating grounding while eliminating actual original holders in its powerless interpretation. `finite_extended_productive_nonempty` verifies that genuine old productivity remains.

Three proved negative controls locate essential statement boundaries:

1. `mixed_support_countercontrol`: a mixed support path from the necessary new ground reaches an effect absent at another index. Grounding necessitation therefore cannot be silently assigned to the whole support closure.
2. `other_world_old_root`: a node which was not an actual root becomes an additional root at another index. Actual root uniqueness cannot be advertised as all-world uniqueness without further premises.
3. `missing_necessity_countercontrol`: if an old actual root is contingent, the newly added grounding edge can violate grounding necessitation. This violates the necessary-root hypothesis, not the accepted programme's metaphysical principle.

The infinite positive control is acyclic and covered by an original root but has an indefinitely descending subordinate ancestry. `infinite_not_wellFounded` is proved alongside `infinite_coverage` and `infinite_acyclic`. Every node is allowed genuine capacity. The main completion theorem still applies, as `infinite_extended_coverage` checks. No causal infinitism is thereby established as metaphysically possible.

`ModalCapacityControl` gives the added ground a nonvacuous capacity: `modalAble` means an actual productive exercise at some modal index. The new ground produces an extra effect nonactually but has no actual productive edge or productive ancestry to the old actual effect. It remains necessary and original at all indices. `modal_old_existence_exact`, `modal_old_productive_exact`, `modal_old_support_exact` and `modal_old_capacity_exact` verify the old-field correspondence. `modal_nonvacuous_separation` collects the result. This is an interpreted bounded capacity, not a certification of all-pure-perfection semantics.

## What the proof does not establish

It does not establish the metaphysical possibility, actual existence or equal credibility of an autonomous noncausal ground. It does not prove the source's contingency-as-need principle, actual particularity of every fact, perfection eligibility, or the source reading itself. It supplies no necessity-to-agency theorem with those premises omitted. It changes no T17 affirmative appraisal and proves no actual revelation attribution. Full dependency-DAG and premise-removal work remains the separately assigned later task.
