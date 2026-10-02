import PolynomialAND

noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND

namespace ANDCorrection

def theta (s T : ℝ) : ℝ :=
  9600*s^2*(T-2*s)/(curvature s*T*(100-curvature s))
def gamma (s T e : ℝ) : ℝ := 96*e*s^2/(T*(100-curvature s))
def beta (s T e : ℝ) : ℝ := (48*e*s-100*gamma s T e)/curvature s

def leadG (s T e a j : ℝ) : ℝ :=
  e-2*(s-a)*beta s T e+(j-T)*gamma s T e

def leadF (s T e a j : ℝ) : ℝ :=
  curvature s*e+(s-a)*(96*s*e-2*curvature s*beta s T e)+100*(j-T)*gamma s T e

lemma curvature_ge_one (s : ℝ) : 1 ≤ curvature s := by
  dsimp [curvature]
  nlinarith [sq_nonneg s]

lemma curvature_lt_100 (s : ℝ) (hs0 : 0 < s) (hs1 : s < 1) :
    curvature s < 100 := by
  have hs2 : s^2 < 1 := by nlinarith
  dsimp [curvature]
  nlinarith

lemma theta_lt_one (s T : ℝ) (hs0 : 0 < s) (hs1 : s < 1)
    (hT0 : 2*s < T) (hT1 : T < 1+s) : theta s T < 1 := by
  have hr := curvature_pos s
  have hr100 := curvature_lt_100 s hs0 hs1
  have h100pos : 0 < 100-curvature s := sub_pos.mpr hr100
  have hT : 0 < T := by linarith
  have hden : 0 < curvature s*T*(100-curvature s) := by positivity
  have hP : 0 < certificateP s := by
    have hh := certificateP_lower s hs0.le hs1.le
    linarith
  let C := curvature s*(100-curvature s)-9600*s^2
  have hid : certificateP s = (1+s)*C+19200*s^3 := by
    dsimp [C, certificateP, curvature]
    ring
  have hN : 0 < curvature s*T*(100-curvature s)-9600*s^2*(T-2*s) := by
    by_cases hC : 0 ≤ C
    · have hCT : 0 ≤ T*C := mul_nonneg hT.le hC
      have hs3 : 0 < s^3 := pow_pos hs0 3
      have heq : curvature s*T*(100-curvature s)-9600*s^2*(T-2*s) = T*C+19200*s^3 := by
        dsimp [C]
        ring
      rw [heq]
      positivity
    · have hC' : C < 0 := lt_of_not_ge hC
      have hm : 0 < (T-(1+s))*C := mul_pos_of_neg_of_neg (by linarith) hC'
      have heq : curvature s*T*(100-curvature s)-9600*s^2*(T-2*s) =
          certificateP s+(T-(1+s))*C := by
        rw [hid]
        dsimp [C]
        ring
      rw [heq]
      positivity
  dsimp [theta]
  apply (div_lt_one hden).2
  linarith

lemma gamma_pos (s T e : ℝ) (hs0 : 0 < s) (hs1 : s < 1)
    (hT : 0 < T) (he : 0 < e) : 0 < gamma s T e := by
  have hr100 := curvature_lt_100 s hs0 hs1
  have h100pos : 0 < 100-curvature s := sub_pos.mpr hr100
  dsimp [gamma]
  positivity

lemma leadG_zero (s T e : ℝ) (hT : T ≠ 0) (h100 : 100-curvature s ≠ 0) :
    leadG s T e 0 0 = e*(1-theta s T) := by
  have hr : curvature s ≠ 0 := ne_of_gt (curvature_pos s)
  dsimp [leadG, beta, gamma, theta]
  field_simp
  ring

lemma leadF_zero (s T e : ℝ) (hT : T ≠ 0) (h100 : 100-curvature s ≠ 0) :
    leadF s T e 0 0 = curvature s*e*(1-theta s T) := by
  have hr : curvature s ≠ 0 := ne_of_gt (curvature_pos s)
  dsimp [leadF, beta, gamma, theta]
  field_simp
  ring

lemma leadF_both (s T e : ℝ) (hT : T ≠ 0) (h100 : 100-curvature s ≠ 0) :
    leadF s T e 1 2 = curvature s*e*(1-theta s T) := by
  have hr : curvature s ≠ 0 := ne_of_gt (curvature_pos s)
  dsimp [leadF, beta, gamma, theta]
  field_simp
  ring

lemma leadG_both (s T e : ℝ) (hT : T ≠ 0) (h100 : 100-curvature s ≠ 0) :
    leadG s T e 1 2 = e*(1-theta s T)+96*e*s*(T-2*s)/(curvature s*T) := by
  have hr : curvature s ≠ 0 := ne_of_gt (curvature_pos s)
  dsimp [leadG, beta, gamma, theta]
  field_simp
  ring

lemma leadG_middle (s T e : ℝ) :
    leadG s T e 0 1 = leadG s T e 0 0+gamma s T e := by
  dsimp [leadG]
  ring

lemma leadF_middle (s T e : ℝ) :
    leadF s T e 0 1 = leadF s T e 0 0+100*gamma s T e := by
  dsimp [leadF]
  ring

/-- All six actual second-order leading coefficients are strictly positive,
for every interior AND-hull parameter and nonzero transverse variance. -/
theorem all_leading_positive (s T e : ℝ) (hs0 : 0 < s) (hs1 : s < 1)
    (hT0 : 2*s < T) (hT1 : T < 1+s) (he : 0 < e) :
    0 < leadG s T e 0 0 ∧ 0 < leadG s T e 0 1 ∧ 0 < leadG s T e 1 2 ∧
    0 < leadF s T e 0 0 ∧ 0 < leadF s T e 0 1 ∧ 0 < leadF s T e 1 2 := by
  have hT : 0 < T := by linarith
  have hTne := ne_of_gt hT
  have h100 : 100-curvature s ≠ 0 := by
    have hh := curvature_lt_100 s hs0 hs1
    linarith
  have hm : 0 < e*(1-theta s T) := mul_pos he (sub_pos.mpr (theta_lt_one s T hs0 hs1 hT0 hT1))
  have hgam := gamma_pos s T e hs0 hs1 hT he
  have hr := curvature_pos s
  have hg0 : 0 < leadG s T e 0 0 := by rw [leadG_zero s T e hTne h100]; exact hm
  have hf0 : 0 < leadF s T e 0 0 := by
    rw [leadF_zero s T e hTne h100]
    nlinarith [mul_pos hr hm]
  refine ⟨hg0, ?_, ?_, hf0, ?_, ?_⟩
  · rw [leadG_middle]
    positivity
  · rw [leadG_both s T e hTne h100]
    have hA : 0 < T-2*s := sub_pos.mpr hT0
    positivity
  · rw [leadF_middle]
    positivity
  · rw [leadF_both s T e hTne h100]
    nlinarith [mul_pos hr hm]

end ANDCorrection
