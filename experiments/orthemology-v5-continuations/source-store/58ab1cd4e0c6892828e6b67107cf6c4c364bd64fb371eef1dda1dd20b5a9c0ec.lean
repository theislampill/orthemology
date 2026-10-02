import ANDIntrinsic
import IsolatedObstruction

set_option maxRecDepth 4096

open Set PolynomialAND ANDCorrection ANDScore ANDRepair ANDPotentialBinding

#check @PolynomialAND.certificateP_lower
#check @PolynomialAND.psi_deriv
#check @PolynomialAND.dpsi_deriv
#check @PolynomialAND.curvature_pos
#check @ANDCorrection.theta_lt_one
#check @ANDCorrection.all_leading_positive
#check @ANDScore.g_gain_identity
#check @ANDScore.f_gain_identity
#check @ANDScore.hull_of_inequalities
#check @ANDRepair.universal_strict_repair
#check @ANDPotentialBinding.potential_hasFDerivAt
#check @ANDPotentialBinding.coordF_deriv
#check @ANDPotentialBinding.coordDF_deriv
#check @ANDPotentialBinding.coordF_curvature_positive
#check @ANDPotentialBinding.scoreF_is_actual_Bregman
#check @ANDPotentialBinding.scoreG_is_actual_Bregman
#check @ANDPotentialBinding.universal_Bregman_repair
#check @FiniteHullWeights.intrinsicInterior_positive_barycentric
#check @ANDPotentialBinding.potentialF_contDiff
#check @ANDPotentialBinding.common_hessian_normal
#check @ANDIntrinsic.transverse_iff
#check @IsolatedObstruction.no_isolated_all_state_repair
#check @ANDIntrinsic.interior_parameters
#check @ANDIntrinsic.intrinsic_universal_Bregman_repair
#check @IsolatedObstruction.no_isolated_common_repair
#check @IsolatedObstruction.isolated_slope_violation

#print axioms PolynomialAND.certificateP_lower
#print axioms ANDCorrection.all_leading_positive
#print axioms ANDScore.g_gain_identity
#print axioms ANDScore.f_gain_identity
#print axioms ANDScore.hull_of_inequalities
#print axioms ANDRepair.universal_strict_repair
#print axioms ANDPotentialBinding.potential_hasFDerivAt
#print axioms ANDPotentialBinding.coordF_curvature_positive
#print axioms ANDPotentialBinding.scoreF_is_actual_Bregman
#print axioms ANDPotentialBinding.scoreG_is_actual_Bregman
#print axioms ANDPotentialBinding.universal_Bregman_repair
#print axioms FiniteHullWeights.intrinsicInterior_positive_barycentric
#print axioms ANDIntrinsic.intrinsic_universal_Bregman_repair
#print axioms IsolatedObstruction.no_isolated_common_repair
#print axioms IsolatedObstruction.isolated_slope_violation

#print PolynomialAND.psi
#print PolynomialAND.dpsi
#print PolynomialAND.curvature
#print ANDScore.truth
#print ANDScore.hull
#print ANDScore.baseline
#print ANDScore.candidate
#print ANDPotentialBinding.coordF
#print ANDPotentialBinding.coordDF
#print ANDPotentialBinding.coordG
#print ANDPotentialBinding.coordDG
#print ANDPotentialBinding.divergence
