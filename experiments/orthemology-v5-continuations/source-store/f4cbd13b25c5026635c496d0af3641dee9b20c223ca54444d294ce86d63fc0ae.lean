import MixedReadback

noncomputable section
open Set PolynomialAND MixedHull MixedScore CouplingLPValues
open scoped BigOperators

namespace IndependentMixedAudit

def highOnly : Vec := ![0,0,1,1,1,1]

lemma high_only_candidate (eps : ℝ) : candidateWith context highOnly 0 0 eps=context := by
  ext i
  fin_cases i <;> norm_num [candidateWith,context,highOnly,ANDScore.mean,kappa,highSum]
  all_goals dsimp only [Matrix.cons_val]
  all_goals norm_num

/-- A genuinely transverse high-block-only input has exact positive gains.
The duplicated flag is not disturbed at all. -/
theorem high_only_exact_gains (eps : ℝ) (i : Fin 6) :
    scoreG (truth i) (context+eps • highOnly)-scoreG (truth i) context=2*eps^2 ∧
    scoreF (truth i) (context+eps • highOnly)-scoreF (truth i) context=200*eps^2 := by
  have h01 : context 0=context 1 := rfl
  have hs : highSum context=2 := by
    change (1/2:ℝ)+1/2+1/2+1/2=2
    norm_num
  have hg := MixedScore.gainG context highOnly 0 0 eps i h01 hs
  have hf := MixedScore.gainF context highOnly 0 0 eps i h01 hs
  rw [high_only_candidate] at hg hf
  have he : ANDScore.variance (highOnly 0) (highOnly 1)=0 := by
    norm_num [ANDScore.variance,highOnly]
  have hn : normalEnergy highOnly=2 := by
    change 2*(((1:ℝ)+1+1+1)/4)^2=2
    norm_num
  have hrG : gRemMixed highOnly 0 0 eps=0 := by
    norm_num [gRemMixed,ANDScore.gRem,highRem]
  have hrF : fRemMixed context highOnly (truth i 0) 0 0 eps=0 := by
    norm_num [fRemMixed,ANDScore.fRem,ANDScore.mean,highOnly,highRem]
  constructor
  · simpa only [he,hn,hrG,mul_zero,zero_mul,add_zero,zero_add,sub_zero,sub_self,mul_comm] using hg
  · calc
      _ = eps^2*(100*2) := by
        simpa only [he,hn,hrF,mul_zero,zero_mul,add_zero,zero_add,sub_zero,sub_self] using hf
      _ = _ := by ring

lemma high_only_transverse : highOnly ∉ MixedGeometry.tangent := by
  change ¬ (highOnly 0=highOnly 1 ∧ highSum highOnly=0)
  intro hh
  have hs : highSum highOnly=4 := by
    change (1:ℝ)+1+1+1=4
    norm_num
  linarith [hh.2]

lemma coupled_truth_first_order_vanishes (i : Fin 6) : truth i 1-truth i 0=0 := by
  fin_cases i <;> norm_num [truth]
lemma product_truth_first_order_vanishes (a : Fin 2) (i : Fin 6) :
    productTruth a i 1-productTruth a i 0=0 := by simp [productTruth]

#check @MixedRepair.universal_strict_Bregman_repair
#check @MixedGeometry.transverse_iff
#check @MixedGeometry.no_free_coordinate
#check @ProductObstruction.no_product_four_tests
#check @CouplingLPValues.coefficientG_binding
#check @CouplingLPValues.coefficientF_binding
#check @CouplingLPValues.coupled_dual_upper
#check @CouplingLPValues.product_dual_upper
#check @high_only_exact_gains
#print axioms high_only_exact_gains
#print axioms high_only_transverse
#print axioms coupled_truth_first_order_vanishes
#print axioms product_truth_first_order_vanishes
#print MixedHull.truth
#print MixedHull.candidateWith
#print MixedHull.coefficients
#print MixedGeometry.tangent
#print MixedScore.divergence
#print CouplingLPValues.context
#print CouplingLPValues.coefficientG
#print CouplingLPValues.coefficientF
#print CouplingLPValues.firstDirection
end IndependentMixedAudit
