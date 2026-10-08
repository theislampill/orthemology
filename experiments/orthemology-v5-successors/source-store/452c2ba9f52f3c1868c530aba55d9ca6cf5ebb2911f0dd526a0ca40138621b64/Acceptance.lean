import JointFiniteInterpretation
open JointFinite

-- API contract plus semantic checks at one literal set of model constants.
#check abc_full
#check canonical_abc_same_g
#check field_guarded
#check veracity_via_component
#check J01_canonical_identity
#check J14_outside_boundary

example : Orthemology.Tranche20.OriginalBearerBridge.FullPremises framework := abc_full
example : Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness framework .x .rg .g :=
  canonical_abc_same_g.1
example : Orthemology.Tranche3.SourceIdentity.Necessary framework.existsAt .g :=
  canonical_abc_same_g.2.1
example : Orthemology.Tranche3.SourceIdentity.UniformRoot framework.existsAt framework.dep .g :=
  canonical_abc_same_g.2.2.1
example : AnchoredSourceBridge.GlobalCoverage account .g := field_coverage_without_cnd
example : AnchoredSourceBridge.ActualUnique account .g := field_guarded.2.2.2.2.1
example : VeracityBoundary.Package speech .g := veracity_package
example : VeracityBoundary.Veracity speech .g := veracity_via_component
example : B.g ≠ B.h := by decide
example : ¬ Orthemology.Tranche3.SourceIdentity.Necessary framework.existsAt .x :=
  abc_live_receipt_and_transport.2.2.2.2.2.2.2
example : productivelySupportsToken .g .v ∧ speech.asserts .w0 .x .v .absent ∧
    ¬ speech.trueAt .w0 .absent ∧ ¬ speech.asserts .w0 .g .v .absent := J12_support_not_ownership
example : ¬ AnchoredSourceBridge.Complete account .g .o := J14_outside_boundary.2.2.2.2.2.2.2.2.2

#check J02_original_resource_provision
#check J03_concrete_receipt
#check J04_field_target_link
#check J05_positive_reachability
#check J05_live_productive_support
#check J06_complete_incoming_inventory
#check J07_no_incoming_outside_source
#check J08_actual_mode_realization
#check J09_fitting_source_realization
#check J10_truth_grounding
#check J11_token_support_grounding
#check J12_support_not_ownership
#check J13_genuine_agent_identity
#check J15_strong_ownership_extension
#check reception_and_direct_support_distinct
#check finite_ancestry_compatibility
#check no_source_or_created_authentication
#check good_source_antecedent_boundary
