import ANDCorrection

noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND ANDCorrection

namespace ANDScore

def mean (h1 h2 : ℝ) : ℝ := (h1+h2)/2
def variance (h1 h2 : ℝ) : ℝ := (h1-h2)^2/4

def gLoss (a l r t1 t2 z w : ℝ) : ℝ :=
  ((t1-a)^2+(t2-a)^2+(z-l)^2+(w-r)^2)/2

def fLoss (a l r t1 t2 z w : ℝ) : ℝ :=
  scalarDiv a t1+scalarDiv a t2+50*(z-l)^2+50*(w-r)^2

def gRem (h1 h2 hz hw b g eps : ℝ) : ℝ :=
  -b*(h1+h2)-g*(hz+hw)-eps*(b^2+g^2)

def fRem (s a h1 h2 hz hw b g eps : ℝ) : ℝ :=
  let m := mean h1 h2
  let d2 := 1+144*s^2-96*a*s
  let d3 := 48*s-16*a
  (d3*(h1^3+h2^3-2*m^3)-2*d2*m*b-100*g*(hz+hw)) +
  (12*(h1^4+h2^4-2*m^4)-d2*b^2-6*d3*m^2*b-100*g^2)*eps +
  (-6*d3*m*b^2-96*m^3*b)*eps^2 +
  (-2*d3*b^3-144*m^2*b^2)*eps^3 +
  (-96*m*b^3)*eps^4 + (-24*b^4)*eps^5

lemma variance_pos (h1 h2 : ℝ) (hne : h1 ≠ h2) : 0 < variance h1 h2 := by
  dsimp [variance]
  exact div_pos (sq_pos_of_ne_zero (sub_ne_zero.mpr hne)) (by norm_num)

/-- Exact identity for the real quadratic losses, not an assumed expansion. -/
theorem g_gain_identity (s z w h1 h2 hz hw b g a l r eps : ℝ) :
    gLoss a l r (s+eps*h1) (s+eps*h2) (z+eps*hz) (w+eps*hw) -
      gLoss a l r (s+eps*mean h1 h2+eps^2*b) (s+eps*mean h1 h2+eps^2*b)
        (z+eps*hz+eps^2*g) (w+eps*hw+eps^2*g) =
    eps^2*(variance h1 h2-2*(s-a)*b+(l+r-z-w)*g+eps*gRem h1 h2 hz hw b g eps) := by
  dsimp [gLoss, mean, variance, gRem]
  ring

/-- Exact degree-eight identity for the real nonlinear Bregman losses. -/
theorem f_gain_identity (s z w h1 h2 hz hw b g a l r eps : ℝ) :
    fLoss a l r (s+eps*h1) (s+eps*h2) (z+eps*hz) (w+eps*hw) -
      fLoss a l r (s+eps*mean h1 h2+eps^2*b) (s+eps*mean h1 h2+eps^2*b)
        (z+eps*hz+eps^2*g) (w+eps*hw+eps^2*g) =
    eps^2*(curvature s*variance h1 h2+(s-a)*(96*s*variance h1 h2-2*curvature s*b)+
      100*(l+r-z-w)*g+eps*fRem s a h1 h2 hz hw b g eps) := by
  dsimp [fLoss, scalarDiv, psi, dpsi, mean, variance, fRem, curvature]
  ring

def truth : Fin 4 → (Fin 4 → ℝ) :=
  ![![0,0,0,0], ![0,0,1,0], ![0,0,0,1], ![1,1,1,1]]

def hull : Set (Fin 4 → ℝ) := convexHull ℝ (Set.range truth)

def baseline (s z w h1 h2 hz hw eps : ℝ) : Fin 4 → ℝ :=
  ![s+eps*h1, s+eps*h2, z+eps*hz, w+eps*hw]

def candidate (s z w h1 h2 hz hw eps : ℝ) : Fin 4 → ℝ :=
  let b := beta s (z+w) (variance h1 h2)
  let g := gamma s (z+w) (variance h1 h2)
  let q := s+eps*mean h1 h2+eps^2*b
  ![q,q,z+eps*hz+eps^2*g,w+eps*hw+eps^2*g]

def scoreG (v c : Fin 4 → ℝ) : ℝ := gLoss (v 0) (v 2) (v 3) (c 0) (c 1) (c 2) (c 3)
def scoreF (v c : Fin 4 → ℝ) : ℝ := fLoss (v 0) (v 2) (v 3) (c 0) (c 1) (c 2) (c 3)

lemma hull_of_inequalities (q z w : ℝ) (hq : 0 ≤ q) (hz : q ≤ z) (hw : q ≤ w)
    (hsum : z+w ≤ 1+q) : ![q,q,z,w] ∈ hull := by
  let weights : Fin 4 → ℝ := ![1+q-z-w,z-q,w-q,q]
  apply mem_convexHull_of_exists_fintype weights truth
  · intro i
    fin_cases i <;> simp [weights] <;> linarith
  · simp [weights, Fin.sum_univ_succ]
  · intro i
    exact Set.mem_range_self i
  · ext i
    fin_cases i <;> simp [weights, truth, Fin.sum_univ_succ] <;> ring

lemma g_loss_inside_continuous (s z w h1 h2 hz hw a j : ℝ) :
    Continuous (fun eps : ℝ => leadG s (z+w) (variance h1 h2) a j +
      eps*gRem h1 h2 hz hw (beta s (z+w) (variance h1 h2))
        (gamma s (z+w) (variance h1 h2)) eps) := by
  unfold gRem
  fun_prop

lemma f_loss_inside_continuous (s z w h1 h2 hz hw a j : ℝ) :
    Continuous (fun eps : ℝ => leadF s (z+w) (variance h1 h2) a j +
      eps*fRem s a h1 h2 hz hw (beta s (z+w) (variance h1 h2))
        (gamma s (z+w) (variance h1 h2)) eps) := by
  unfold fRem
  fun_prop

end ANDScore
