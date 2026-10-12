import PolynomialAND
import ANDCorrection
import ANDScore
import ANDRepair
import ANDPotentialBinding
import FiniteHullWeights
import ANDIntrinsic
import IsolatedObstruction
import AuditReadback
import IndependentReadback
import AuditControls
set_option pp.universes true
set_option pp.explicit true
#check @universal_strict_repair
#print axioms universal_strict_repair
#check @universal_Bregman_repair
#print axioms universal_Bregman_repair
#check @potential_hasFDerivAt
#print axioms potential_hasFDerivAt
#check @intrinsic_universal_Bregman_repair
#print axioms intrinsic_universal_Bregman_repair
#check @no_isolated_common_repair
#print axioms no_isolated_common_repair
#check @ANDIntrinsic.intrinsic_universal_Bregman_repair
#print axioms ANDIntrinsic.intrinsic_universal_Bregman_repair
#check @ANDPotentialBinding.coordF_deriv
#print axioms ANDPotentialBinding.coordF_deriv
#check @ANDPotentialBinding.coordDF_deriv
#print axioms ANDPotentialBinding.coordDF_deriv
#check @ANDPotentialBinding.potential_hasFDerivAt
#print axioms ANDPotentialBinding.potential_hasFDerivAt
#check @ANDPotentialBinding.common_hessian_normal
#print axioms ANDPotentialBinding.common_hessian_normal
#check @ANDPotentialBinding.potentialF_contDiff
#print axioms ANDPotentialBinding.potentialF_contDiff
#check @IsolatedObstruction.no_isolated_all_state_repair
#print axioms IsolatedObstruction.no_isolated_all_state_repair
#check @IsolatedObstruction.isolated_slope_violation
#print axioms IsolatedObstruction.isolated_slope_violation
#check @ANDIntrinsic.transverse_iff
#print axioms ANDIntrinsic.transverse_iff
#check @PolynomialAND.certificateP_lower
#print axioms PolynomialAND.certificateP_lower
#check @ANDCorrection.all_leading_positive
#print axioms ANDCorrection.all_leading_positive
#check @ANDScore.g_gain_identity
#print axioms ANDScore.g_gain_identity
#check @ANDScore.f_gain_identity
#print axioms ANDScore.f_gain_identity
#check @ANDScore.hull_of_inequalities
#print axioms ANDScore.hull_of_inequalities
#check @ANDRepair.universal_strict_repair
#print axioms ANDRepair.universal_strict_repair
#check @ANDPotentialBinding.coordF_curvature_positive
#print axioms ANDPotentialBinding.coordF_curvature_positive
#check @ANDPotentialBinding.scoreF_is_actual_Bregman
#print axioms ANDPotentialBinding.scoreF_is_actual_Bregman
#check @ANDPotentialBinding.scoreG_is_actual_Bregman
#print axioms ANDPotentialBinding.scoreG_is_actual_Bregman
#check @ANDPotentialBinding.universal_Bregman_repair
#print axioms ANDPotentialBinding.universal_Bregman_repair
#check @FiniteHullWeights.intrinsicInterior_positive_barycentric
#print axioms FiniteHullWeights.intrinsicInterior_positive_barycentric
#check @IsolatedObstruction.no_isolated_common_repair
#print axioms IsolatedObstruction.no_isolated_common_repair
#check @full_success_with_projected_failure
#print axioms full_success_with_projected_failure
#check @transverse_baseline_outside
#print axioms transverse_baseline_outside
#check @tangent_not_strict
#print axioms tangent_not_strict
#check @natural_truth_binding
#print axioms natural_truth_binding
#check @psi_strictConvex
#print axioms psi_strictConvex
