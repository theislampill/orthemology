import FiniteLikelihoodRisk
import RobustBinaryRepair

namespace Orthemology.Tranche4.RepairDecision
open Orthemology.Tranche3 Orthemology.Tranche4.RationalLikelihood

/-- Literal weak all-truth repair, including coherence. -/
def ScoreGood (a e q : ℝ) : Prop :=
  0 ≤ q ∧ q ≤ 1 ∧ excessZero a e q ≤ 0 ∧ excessOne a e q ≤ 0

theorem two_good_iff_robust (l u e q : ℝ) (hlu : l ≤ u) (he0 : 0 ≤ e) (he1 : e ≤ 1) :
    (ScoreGood l e q ∧ ScoreGood u e q) ↔ RobustGood l u e 0 q := by
  constructor
  · intro h
    exact (robustGood_iff_endpoints l u e 0 q hlu he0 he1).mpr
      ⟨h.1.1,h.1.2.1,h.1.2.2.1,h.2.2.2.2⟩
  · intro h
    exact ⟨⟨h.1,h.2.1,(h.2.2 l le_rfl hlu).1,(h.2.2 l le_rfl hlu).2⟩,
      ⟨h.1,h.2.1,(h.2.2 u hlu le_rfl).1,(h.2.2 u hlu le_rfl).2⟩⟩

theorem common_repair_iff (l u e : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u)
    (hu1 : u ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    (∃ q, ScoreGood l e q ∧ ScoreGood u e q) ↔ robustValue l u e ≤ 0 := by
  simp_rw [two_good_iff_robust l u e _ hlu he0 (by linarith)]
  exact robust_repair_exists_iff l u e 0 hl0 hlu hu1 he0 he1

theorem positive_value_disjoint (l u e : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u)
    (hu1 : u ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) (hv : 0 < robustValue l u e) :
    ∀ q, ¬(ScoreGood l e q ∧ ScoreGood u e q) := by
  intro q h
  have hh := (common_repair_iff l u e hl0 hlu hu1 he0 he1).mp ⟨q,h⟩
  linarith

noncomputable def failureMass {A : Type*} (G : A → Prop) (a : A) (m : ℝ) : ℝ :=
  by classical exact if G a then 0 else m

/-- No restriction to a preselected two-report alphabet is used here. -/
theorem disjoint_report_lower {A : Type*} (G0 G1 : A → Prop)
    (disjoint : ∀ a, ¬(G0 a ∧ G1 a)) (a : A) (u v : ℝ) (hu : 0 ≤ u) (hv : 0 ≤ v) :
    min u v ≤ failureMass G0 a u + failureMass G1 a v := by
  classical
  by_cases h0 : G0 a <;> by_cases h1 : G1 a
  · exact False.elim (disjoint a ⟨h0,h1⟩)
  · simp only [failureMass,h0,h1,↓reduceIte,zero_add]
    exact min_le_right _ _
  · simp only [failureMass,h0,h1,↓reduceIte,add_zero]
    exact min_le_left _ _
  · simp only [failureMass,h0,h1,↓reduceIte]
    exact (min_le_left u v).trans (le_add_of_nonneg_right hv)

/-- The same finite-prefix real report is evaluated in each possible model. -/
theorem finite_report_pairRisk_lower {A : Type*} (G0 G1 : A → Prop)
    (disjoint : ∀ a, ¬(G0 a ∧ G1 a)) (p q : ℝ)
    (hp : 0 ≤ p) (hp1 : p ≤ 1) (hq : 0 ≤ q) (hq1 : q ≤ 1)
    (n : ℕ) (report : Words n → A) :
    sumWords n (pairError p q n) ≤
      sumWords n (fun w => failureMass G0 (report w) (mass p n w) +
        failureMass G1 (report w) (mass q n w)) := by
  apply sumWords_mono
  intro w
  rw [pairError_eq_min]
  exact disjoint_report_lower G0 G1 disjoint (report w) _ _
    (mass_nonneg p hp hp1 n w) (mass_nonneg q hq hq1 n w)

theorem own_report_sound (a e : ℝ) (ha : 0 ≤ a) (ha1 : a ≤ 1)
    (he : 0 ≤ e) (he1 : e ≤ 1/4) : ScoreGood a e (1/2+a*e) := by
  have hprod := mul_nonneg ha he
  have hmax := mul_le_mul_of_nonneg_right ha1 he
  have hvar := mul_nonneg ha (sub_nonneg.mpr ha1)
  have hex0 : excessZero a e (1/2+a*e) = -(a*(1-a))*e^2 := by
    unfold excessZero; ring
  have hex1 : excessOne a e (1/2+a*e) = -(a*(1-a))*e^2 := by
    unfold excessOne; ring
  refine ⟨by linarith,by nlinarith,?_,?_⟩
  · rw [hex0]; nlinarith [sq_nonneg e]
  · rw [hex1]; nlinarith [sq_nonneg e]


theorem selected_common_sound (l u e : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u)
    (hu1 : u ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) (hv : robustValue l u e ≤ 0) :
    ScoreGood l e (robustReport l u e) ∧ ScoreGood u e (robustReport l u e) := by
  apply (two_good_iff_robust l u e _ hlu he0 (by linarith)).mpr
  apply (robustGood_iff_endpoints l u e 0 _ hlu he0 (by linarith)).mpr
  have hmem := robustReport_mem l u e hl0 hlu hu1 he0 he1
  exact ⟨hmem.1.le,hmem.2.le,hv,by rw [robust_crossing]; exact hv⟩

theorem positive_value_distinct (l u e : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u)
    (hu1 : u ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) (hv : 0 < robustValue l u e) : l ≠ u := by
  intro heq
  subst u
  have hs := own_report_sound l e hl0 hu1 he0 he1
  exact positive_value_disjoint l l e hl0 hlu hu1 he0 he1 hv _ ⟨hs,hs⟩

example : ScoreGood (49/100) (1/4) (999/1600) ∧ ScoreGood (51/100) (1/4) (999/1600) := by
  norm_num [ScoreGood,excessZero,excessOne]

example : robustValue (49/100) (51/100) (1/4) < 0 := by
  norm_num [robustValue,robustReport,excessZero]

example : 0 < robustValue (1/4) (3/4) (1/4) := by
  norm_num [robustValue,robustReport,excessZero]

example : failureMass (ScoreGood (49/100) (1/4)) (999/1600) 1 +
    failureMass (ScoreGood (51/100) (1/4)) (999/1600) 1 = 0 := by
  norm_num [failureMass,ScoreGood,excessZero,excessOne]

example : robustValue (1/4) (3/4) 0 = 0 ∧
    ScoreGood (1/4) 0 (1/2) ∧ ScoreGood (3/4) 0 (1/2) := by
  norm_num [robustValue,robustReport,ScoreGood,excessZero,excessOne]

#print axioms common_repair_iff
#print axioms finite_report_pairRisk_lower
end Orthemology.Tranche4.RepairDecision
