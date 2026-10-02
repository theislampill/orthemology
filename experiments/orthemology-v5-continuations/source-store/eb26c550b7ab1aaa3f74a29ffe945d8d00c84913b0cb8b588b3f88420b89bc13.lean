import MixedScore
import IsolatedObstruction

noncomputable section
open scoped BigOperators
open Set PolynomialAND MixedHull MixedScore

namespace ProductObstruction

def prodTruth (a : ℝ) (top : Bool) : Vec :=
  if top then ![a,a,1,1,0,0] else ![a,a,0,0,1,1]
def baseline (eps : ℝ) : Vec := ![1/4+eps,1/4,1/2,1/2,1/2,1/2]
def report (q z w u v : ℝ) : Vec := ![q,q,z,w,u,v]
def spread (z w u v : ℝ) : ℝ := (z-1/2)^2+(w-1/2)^2+(u-1/2)^2+(v-1/2)^2

lemma averageG_identity (eps q z w u v : ℝ) :
    scoreG (prodTruth 0 true) (report q z w u v)+scoreG (prodTruth 0 false) (report q z w u v)-
      (scoreG (prodTruth 0 true) (baseline eps)+scoreG (prodTruth 0 false) (baseline eps)) =
    2*(q^2-IsolatedObstruction.baseA eps)+spread z w u v := by
  simp [scoreG,divergence_eq_sum,coordG,coordDG,prodTruth,report,baseline,spread,
    IsolatedObstruction.baseA,Fin.sum_univ_succ]
  ring

lemma averageF_identity (eps q z w u v : ℝ) :
    scoreF (prodTruth 1 true) (report q z w u v)+scoreF (prodTruth 1 false) (report q z w u v)-
      (scoreF (prodTruth 1 true) (baseline eps)+scoreF (prodTruth 1 false) (baseline eps)) =
    2*(IsolatedObstruction.endpointLoss q-IsolatedObstruction.nonlinearBaseline eps)+100*spread z w u v := by
  simp [scoreF,divergence_eq_sum,coordF,coordDF,prodTruth,report,baseline,spread,
    IsolatedObstruction.endpointLoss,IsolatedObstruction.nonlinearBaseline,scalarDiv,psi,dpsi,Fin.sum_univ_succ]
  ring

/-- Four actual product truth comparisons alone are impossible. The candidate
high coordinates are unrestricted real numbers, so coherent product repairs
are excluded a fortiori. -/
theorem no_product_four_tests (eps : ℝ) (he : 0<eps) (hu : eps≤1/100) :
    ¬ ∃ q ∈ Icc (0:ℝ) 1, ∃ z w u v : ℝ,
      scoreG (prodTruth 0 true) (report q z w u v)≤scoreG (prodTruth 0 true) (baseline eps) ∧
      scoreG (prodTruth 0 false) (report q z w u v)≤scoreG (prodTruth 0 false) (baseline eps) ∧
      scoreF (prodTruth 1 true) (report q z w u v)≤scoreF (prodTruth 1 true) (baseline eps) ∧
      scoreF (prodTruth 1 false) (report q z w u v)≤scoreF (prodTruth 1 false) (baseline eps) := by
  rintro ⟨q,hq,z,w,u,v,hG0,hG1,hF0,hF1⟩
  apply IsolatedObstruction.no_isolated_common_repair eps he hu
  have hs : 0≤spread z w u v := by dsimp [spread]; positivity
  refine ⟨q,hq,?_,?_⟩
  · have hh := averageG_identity eps q z w u v
    linarith
  · have hh := averageF_identity eps q z w u v
    linarith

#print axioms no_product_four_tests
end ProductObstruction
