import MixedGeometry

set_option maxHeartbeats 1000000
noncomputable section
open scoped BigOperators
open Set PolynomialAND MixedHull MixedScore MixedGeometry

namespace CouplingLPValues

def context : Vec := ![1/4,1/4,1/2,1/2,1/2,1/2]
def coefficientG (v w : Vec) : ℝ := 1/4-∑ i, (context i-v i)*w i
def coefficientF (v w : Vec) : ℝ :=
  1+9*(1/4-v 0)-3*(1/4-v 1)-∑ i, coordDDF i (context i)*(context i-v i)*w i

def coupledCorrection : Vec := ![12/41,12/41,3/328,3/328,-3/328,-3/328]
def productCorrection : Vec := ![15/26,15/26,0,0,0,0]
def productTruth (a : Fin 2) (i : Fin 6) : Vec :=
  ![(a.val:ℝ),(a.val:ℝ),truth i 2,truth i 3,truth i 4,truth i 5]

lemma curvature_deriv (s : ℝ) : HasDerivAt curvature (96*s) s := by
  convert (hasDerivAt_const s 1).add (((hasDerivAt_id s).pow 2).const_mul 48) using 1 <;>
    simp [curvature] <;> ring

lemma context_curvature : curvature (context 0)=4 ∧ 96*context 0=24 := by
  norm_num [context,curvature]

lemma coupled_primal :
    coupledCorrection ∈ tangent ∧
    (∀ i : Fin 6, (7:ℝ)/82≤coefficientG (truth i) coupledCorrection ∧
      (7:ℝ)/82≤coefficientF (truth i) coupledCorrection) := by
  constructor
  · norm_num [tangent,highSum,coupledCorrection]
    try dsimp only [Matrix.cons_val]
    norm_num
  · intro i
    fin_cases i <;>
      norm_num [coefficientG,coefficientF,context,coupledCorrection,truth,coordDDF,curvature,Fin.sum_univ_succ]

lemma coupled_dual_identity (w : Vec) :
    (100:ℝ)/123*coefficientG (truth 5) w+
      (11:ℝ)/123*coefficientF (truth 5) w+
      (12:ℝ)/123*coefficientF (truth 0) w=7/82 := by
  norm_num [coefficientG,coefficientF,context,truth,coordDDF,curvature,Fin.sum_univ_succ]
  try dsimp only [Matrix.cons_val]
  ring

/-- This upper bound applies to every ambient correction, and hence to every
allowed tangent correction, not only the exhibited symmetric optimizer. -/
lemma coupled_dual_upper (w : Vec) (tau : ℝ)
    (hG : ∀ i : Fin 6, tau≤coefficientG (truth i) w)
    (hF : ∀ i : Fin 6, tau≤coefficientF (truth i) w) : tau≤7/82 := by
  have hi := coupled_dual_identity w
  have hg := hG 5
  have hf0 := hF 5
  have hf1 := hF 0
  linarith

lemma product_primal :
    productCorrection ∈ tangent ∧
    (∀ a : Fin 2, ∀ i : Fin 6,
      (-1:ℝ)/26≤coefficientG (productTruth a i) productCorrection ∧
      (-1:ℝ)/26≤coefficientF (productTruth a i) productCorrection) := by
  constructor
  · norm_num [tangent,highSum,productCorrection]
    try dsimp only [Matrix.cons_val]
    norm_num
  · intro a i
    fin_cases a <;> fin_cases i <;>
      norm_num [coefficientG,coefficientF,context,productCorrection,productTruth,truth,
        coordDDF,curvature,Fin.sum_univ_succ]

lemma product_dual_identity (w : Vec) :
    (6:ℝ)/13*coefficientG (productTruth 0 0) w+
      (6:ℝ)/13*coefficientG (productTruth 0 5) w+
      (1:ℝ)/26*coefficientF (productTruth 1 0) w+
      (1:ℝ)/26*coefficientF (productTruth 1 5) w = -1/26 := by
  norm_num [coefficientG,coefficientF,context,productTruth,truth,coordDDF,curvature,Fin.sum_univ_succ]
  try dsimp only [Matrix.cons_val]
  ring

lemma product_dual_upper (w : Vec) (tau : ℝ)
    (hG : ∀ a : Fin 2, ∀ i : Fin 6, tau≤coefficientG (productTruth a i) w)
    (hF : ∀ a : Fin 2, ∀ i : Fin 6, tau≤coefficientF (productTruth a i) w) : tau≤ -1/26 := by
  have hi := product_dual_identity w
  have hg0 := hG 0 0
  have hg1 := hG 0 5
  have hf0 := hF 1 0
  have hf1 := hF 1 5
  linarith

def firstDirection : Vec := ![1/2,1/2,0,0,0,0]
def disturbed (eps : ℝ) : Vec := ![1/4+eps,1/4,1/2,1/2,1/2,1/2]
def curved (w : Vec) (eps : ℝ) : Vec := context+eps • firstDirection+eps^2 • w

def remainderG (w : Vec) (eps : ℝ) : ℝ :=
  -(w 0+w 1)/2-eps*(∑ i, (w i)^2)/2

def highSquare (w : Vec) : ℝ := (w 2)^2+(w 3)^2+(w 4)^2+(w 5)^2

def remainderF (v w : Vec) (eps : ℝ) : ℝ :=
  (9-14*v 0+2*v 1-(5-12*v 0)*w 0-(5-12*v 1)*w 1)+
  (21/2-(5-12*v 0)*(w 0)^2-(5-12*v 1)*(w 1)^2-
    (9-12*v 0)*w 0-(9-12*v 1)*w 1-50*highSquare w)*eps+
  (-(18-24*v 0)*(w 0)^2-(18-24*v 1)*(w 1)^2-6*(w 0+w 1))*eps^2+
  (-(12-16*v 0)*(w 0)^3-(12-16*v 1)*(w 1)^3-18*((w 0)^2+(w 1)^2))*eps^3-
  24*((w 0)^3+(w 1)^3)*eps^4-12*((w 0)^4+(w 1)^4)*eps^5

lemma succ_2_fin_3 : Fin.succ (2:Fin 3) = (3:Fin 4) := rfl
lemma succ_2_fin_4 : Fin.succ (2:Fin 4) = (3:Fin 5) := rfl
lemma succ_3_fin_4 : Fin.succ (3:Fin 4) = (4:Fin 5) := rfl
lemma succ_2_fin_5 : Fin.succ (2:Fin 5) = (3:Fin 6) := rfl
lemma succ_3_fin_5 : Fin.succ (3:Fin 5) = (4:Fin 6) := rfl
lemma succ_4_fin_5 : Fin.succ (4:Fin 5) = (5:Fin 6) := rfl

/-- Actual gain identity binds every ambient correction vector to the rational
LP data. All declared truth vectors have v0=v1, so the linear term vanishes. -/
lemma coefficientG_binding (v w : Vec) (eps : ℝ) :
    scoreG v (disturbed eps)-scoreG v (curved w eps) =
      eps*(v 1-v 0)/2+eps^2*(coefficientG v w+eps*remainderG w eps) := by
  simp [scoreG,divergence_eq_sum,coordG,coordDG,disturbed,curved,context,firstDirection,
    coefficientG,remainderG,Fin.sum_univ_succ]
  try dsimp only [Matrix.cons_val]
  simp only [Matrix.vecHead,Matrix.vecTail,Function.comp_apply,Pi.smul_apply,smul_eq_mul]
  simp only [Fin.succ_zero_eq_one',Fin.succ_one_eq_two',succ_2_fin_3,succ_2_fin_4,succ_3_fin_4,succ_2_fin_5,succ_3_fin_5,succ_4_fin_5]
  ring

lemma coefficientF_binding (v w : Vec) (eps : ℝ) :
    scoreF v (disturbed eps)-scoreF v (curved w eps) =
      2*eps*(v 1-v 0)+eps^2*(coefficientF v w+eps*remainderF v w eps) := by
  simp [scoreF,divergence_eq_sum,coordF,coordDF,coordDDF,psi,dpsi,curvature,
    disturbed,curved,context,firstDirection,coefficientF,remainderF,highSquare,Fin.sum_univ_succ]
  try dsimp only [Matrix.cons_val]
  simp only [Matrix.vecHead,Matrix.vecTail,Function.comp_apply,Pi.smul_apply,smul_eq_mul]
  simp only [Fin.succ_zero_eq_one',Fin.succ_one_eq_two',succ_2_fin_3,succ_2_fin_4,succ_3_fin_4,succ_2_fin_5,succ_3_fin_5,succ_4_fin_5]
  ring

#print axioms coupled_primal
#print axioms coupled_dual_upper
#print axioms product_primal
#print axioms product_dual_upper
end CouplingLPValues

#print axioms CouplingLPValues.coefficientG_binding
#print axioms CouplingLPValues.coefficientF_binding
