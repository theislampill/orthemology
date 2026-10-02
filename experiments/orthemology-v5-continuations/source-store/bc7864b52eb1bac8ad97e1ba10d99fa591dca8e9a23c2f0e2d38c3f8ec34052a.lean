import StoppedBlock
import SelfVerifyingSupport

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {A Y Θ : Type*} [Fintype Y]

lemma stayMass_nonneg (p : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (a : A) : 0 ≤ stayMass p stay a := by
  apply Finset.sum_nonneg
  intro y _
  split_ifs <;> first | exact hp a y | exact le_rfl

lemma stayMass_le_one (p : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (hNorm : ∀ a, ∑ y, p a y = 1) (a : A) :
    stayMass p stay a ≤ 1 := by
  calc
    _ ≤ ∑ y, p a y := by
      apply Finset.sum_le_sum
      intro y _
      split_ifs <;> first | exact le_rfl | exact hp a y
    _ = 1 := hNorm a

lemma stayMass_lt_one_of_exit (p : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (hNorm : ∀ a, ∑ y, p a y = 1) (a : A)
    (hexit : ∃ y, stay a y = false ∧ 0 < p a y) : stayMass p stay a < 1 := by
  classical
  obtain ⟨y, hy, hpos⟩ := hexit
  have he : 0 < ∑ z, if stay a z then 0 else p a z := by
    apply Finset.sum_pos'
    · intro z _
      split_ifs <;> first | exact le_rfl | exact hp a z
    · exact ⟨y, Finset.mem_univ _, by simpa [hy] using hpos⟩
  have hs : stayMass p stay a + (∑ z, if stay a z then 0 else p a z) = 1 := by
    unfold stayMass
    rw [← Finset.sum_add_distrib]
    convert hNorm a using 1
    apply Finset.sum_congr rfl
    intro z _
    cases hz : stay a z <;> simp [hz]
  linarith

lemma mapped_prod_nonneg (r : A → ℝ) (h0 : ∀ a, 0 ≤ r a) (acts : List A) :
    0 ≤ (acts.map r).prod := by
  induction acts with
  | nil => simp
  | cons a as ih => exact mul_nonneg (h0 a) ih

lemma mapped_prod_le_one (r : A → ℝ) (h0 : ∀ a, 0 ≤ r a) (h1 : ∀ a, r a ≤ 1)
    (acts : List A) : (acts.map r).prod ≤ 1 := by
  induction acts with
  | nil => simp
  | cons a as ih =>
    change r a * (as.map r).prod ≤ 1
    calc
      _ ≤ 1 * (as.map r).prod := mul_le_mul_of_nonneg_right (h1 a) (mapped_prod_nonneg r h0 as)
      _ ≤ 1 := by simpa using ih

lemma mapped_prod_le_member (r : A → ℝ) (h0 : ∀ a, 0 ≤ r a) (h1 : ∀ a, r a ≤ 1)
    (acts : List A) (a : A) (ha : a ∈ acts) : (acts.map r).prod ≤ r a := by
  induction acts with
  | nil => simp at ha
  | cons b bs ih =>
    change r b * (bs.map r).prod ≤ r a
    rcases List.mem_cons.mp ha with hab | ha
    · rw [hab]
      simpa using mul_le_mul_of_nonneg_left (mapped_prod_le_one r h0 h1 bs) (h0 b)
    · calc
        _ ≤ 1 * (bs.map r).prod := mul_le_mul_of_nonneg_right (h1 b) (mapped_prod_nonneg r h0 bs)
        _ ≤ r a := by simpa using ih ha

lemma survivalMass_lt_one_of_progress (p : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (hNorm : ∀ a, ∑ y, p a y = 1) (acts : List A)
    (hprogress : ∃ a ∈ acts, ∃ y, stay a y = false ∧ 0 < p a y) :
    survivalMass p stay acts < 1 := by
  obtain ⟨a, ha, hexit⟩ := hprogress
  rw [survivalMass_product]
  exact (mapped_prod_le_member (stayMass p stay) (stayMass_nonneg p stay hp)
    (stayMass_le_one p stay hp hNorm) acts a ha).trans_lt
      (stayMass_lt_one_of_exit p stay hp hNorm a hexit)

theorem survivalAffinity_lt_one_of_progress (p q : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (hq : ∀ a y, 0 ≤ q a y)
    (hsp : ∀ a, ∑ y, p a y = 1) (hsq : ∀ a, ∑ y, q a y = 1) (acts : List A)
    (hprogress : ∃ a ∈ acts, ∃ y, stay a y = false ∧ 0 < q a y) :
    survivalAffinity p q stay acts < 1 := by
  rw [survivalAffinity_eq_killed]
  apply affinity_lt_one_of_mass_lt_right
  · exact killedLaw_nonneg _ _ (stoppedMass_nonneg p stay hp acts)
  · exact killedLaw_nonneg _ _ (stoppedMass_nonneg q stay hq acts)
  · exact survivalMass_le_one p stay hp hsp acts
  · exact survivalMass_lt_one_of_progress q stay hq hsq acts hprogress

lemma residualActionAffinity_nonneg (p q : A → Y → ℝ) (stay : A → Y → Bool) (a : A) :
    0 ≤ residualActionAffinity p q stay a := by
  apply Finset.sum_nonneg
  intro y _
  split_ifs <;> first | exact mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _) | exact le_rfl

lemma residualActionAffinity_le_full (p q : A → Y → ℝ) (stay : A → Y → Bool) (a : A) :
    residualActionAffinity p q stay a ≤ affinity (p a) (q a) := by
  apply Finset.sum_le_sum
  intro y _
  split_ifs <;> first | exact le_rfl | exact mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)

theorem survivalAffinity_lt_one_of_informative (p q : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (hq : ∀ a y, 0 ≤ q a y)
    (hsp : ∀ a, ∑ y, p a y = 1) (hsq : ∀ a, ∑ y, q a y = 1) (acts : List A)
    (hinfo : ∃ a ∈ acts, p a ≠ q a) : survivalAffinity p q stay acts < 1 := by
  obtain ⟨a, ha, hne⟩ := hinfo
  rw [survivalAffinity_product p q stay hp hq]
  have h1 : ∀ a, residualActionAffinity p q stay a ≤ 1 := fun a =>
    (residualActionAffinity_le_full p q stay a).trans
      (affinity_le_one _ _ (hp a) (hq a) (hsp a) (hsq a))
  exact (mapped_prod_le_member (residualActionAffinity p q stay)
    (residualActionAffinity_nonneg p q stay) h1 acts a ha).trans_lt
      ((residualActionAffinity_le_full p q stay a).trans_lt
        (affinity_lt_one _ _ (hp a) (hq a) (hsp a) (hsq a) hne))

/-- The finite source certificate forces a strict residual deficit for every
actually harmful candidate, whether it progresses by revelation or learning. -/
theorem certificate_implies_strict_residual [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (stay : A → Y → Bool)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hNorm : ∀ θ a, ∑ y, P θ a y = 1)
    (θ σ : Θ) (acts : List A)
    (hcert : (∃ a ∈ acts, ∃ y, stay a y = false ∧ 0 < P σ a y) ∨
      SelfVerifying good (fun η ζ a => P η a = P ζ a) σ acts.toFinset)
    (hbad : ¬ acts.toFinset ⊆ good θ) :
    0 < 1-survivalAffinity (P θ) (P σ) stay acts := by
  apply sub_pos.mpr
  rcases hcert with hp | hs
  · exact survivalAffinity_lt_one_of_progress (P θ) (P σ) stay
      (hP θ) (hP σ) (hNorm θ) (hNorm σ) acts hp
  · have hi : ∃ a ∈ acts, P θ a ≠ P σ a := by
      by_contra! h
      apply hbad
      apply hs.2 θ
      intro a ha
      exact (h a (List.mem_toFinset.mp ha)).symm
    exact survivalAffinity_lt_one_of_informative (P θ) (P σ) stay
      (hP θ) (hP σ) (hNorm θ) (hNorm σ) acts hi

end Orthemology.Tranche2
