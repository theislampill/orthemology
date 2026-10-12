import PolynomialAND
import ANDCorrection
import ANDScore
import ANDRepair
import ANDPotentialBinding
import FiniteHullWeights
import ANDIntrinsic
import IsolatedObstruction
import MixedHull
import MixedScore
import MixedRepair
import MixedGeometry
import ProductObstruction
import CouplingLPValues
import MixedReadback
import IndependentMixedAudit
set_option pp.universes true
set_option pp.explicit true
#check @ANDRepair.universal_strict_repair
#print axioms ANDRepair.universal_strict_repair
#check @ANDPotentialBinding.universal_Bregman_repair
#print axioms ANDPotentialBinding.universal_Bregman_repair
#check @ANDPotentialBinding.potential_hasFDerivAt
#print axioms ANDPotentialBinding.potential_hasFDerivAt
#check @ANDIntrinsic.intrinsic_universal_Bregman_repair
#print axioms ANDIntrinsic.intrinsic_universal_Bregman_repair
#check @IsolatedObstruction.no_isolated_common_repair
#print axioms IsolatedObstruction.no_isolated_common_repair
#check @MixedRepair.universal_strict_Bregman_repair
#print axioms MixedRepair.universal_strict_Bregman_repair
#check @MixedGeometry.span_directions_eq
#print axioms MixedGeometry.span_directions_eq
#check @MixedGeometry.common_hessian_normal
#print axioms MixedGeometry.common_hessian_normal
#check @MixedGeometry.no_free_coordinate
#print axioms MixedGeometry.no_free_coordinate
#check @ProductObstruction.no_product_four_tests
#print axioms ProductObstruction.no_product_four_tests
#check @CouplingLPValues.coupled_primal
#print axioms CouplingLPValues.coupled_primal
#check @CouplingLPValues.coupled_dual_upper
#print axioms CouplingLPValues.coupled_dual_upper
#check @CouplingLPValues.product_primal
#print axioms CouplingLPValues.product_primal
#check @CouplingLPValues.product_dual_upper
#print axioms CouplingLPValues.product_dual_upper
#check @CouplingLPValues.coefficientG_binding
#print axioms CouplingLPValues.coefficientG_binding
#check @CouplingLPValues.coefficientF_binding
#print axioms CouplingLPValues.coefficientF_binding
#check @MixedHull.coefficients_center
#print axioms MixedHull.coefficients_center
#check @MixedHull.candidate_eventually_mem
#print axioms MixedHull.candidate_eventually_mem
#check @MixedScore.coordF_deriv
#print axioms MixedScore.coordF_deriv
#check @MixedScore.coordDF_deriv
#print axioms MixedScore.coordDF_deriv
#check @MixedScore.coordF_curvature_positive
#print axioms MixedScore.coordF_curvature_positive
#check @MixedScore.potential_hasFDerivAt
#print axioms MixedScore.potential_hasFDerivAt
#check @MixedScore.gainG
#print axioms MixedScore.gainG
#check @MixedScore.gainF
#print axioms MixedScore.gainF
#check @MixedGeometry.transverse_iff
#print axioms MixedGeometry.transverse_iff
#check @IndependentMixedAudit.high_only_exact_gains
#print axioms IndependentMixedAudit.high_only_exact_gains
#check @IndependentMixedAudit.high_only_transverse
#print axioms IndependentMixedAudit.high_only_transverse
#check @IndependentMixedAudit.coupled_truth_first_order_vanishes
#print axioms IndependentMixedAudit.coupled_truth_first_order_vanishes
#check @IndependentMixedAudit.product_truth_first_order_vanishes
#print axioms IndependentMixedAudit.product_truth_first_order_vanishes
