import CausalTreeLaw

noncomputable section
set_option linter.unusedSectionVars false
open Finset
open scoped BigOperators
attribute [local instance] Classical.propDecidable
namespace Orthemology.Tranche3
open Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*} [∀ p a, Fintype (Obs p a)]

/-- Convert the killed-history weighted potential to a conditional-on-the
acquired-prefix value. This does not condition on an infinite no-exit event. -/
def normalizedResetPotential
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool) (θ : Θ)
    (V : (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ) (D : Phase → ℝ)
    (s : ResetState (Obs := Obs)) : ℝ :=
  if 0 < dHistoryMass (continuingKernel K stay s.1) θ s.2 then
    V s.1 s.2 / dHistoryMass (continuingKernel K stay s.1) θ s.2 + D s.1 else 0

omit [(p : Phase) → (a : Θ) → Fintype (Obs p a)] in
lemma normalizedResetPotential_nonneg
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool) (θ : Θ)
    (V : (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ) (D : Phase → ℝ)
    (hV : ∀ p h, 0 ≤ V p h) (hD : ∀ p, 0 ≤ D p) (s : ResetState (Obs := Obs)) :
    0 ≤ normalizedResetPotential K stay θ V D s := by
  unfold normalizedResetPotential
  split_ifs with hm
  · exact add_nonneg (div_nonneg (hV _ _) hm.le) (hD _)
  · exact le_rfl

/-- The normalized potential has a one-block conditional drift bound on every
positive-likelihood valid macro state. Zero-mass branches contribute exactly zero. -/
theorem normalizedResetPotential_step
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p a, ∑ y, K p θ a y = 1)
    (I : Phase → Prop)
    (V : (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ) (hV : ∀ p h, 0 ≤ V p h)
    (hStep : ∀ p, I p → ∀ h,
      cost p (π p h) * dHistoryMass (continuingKernel K stay p) θ h +
        (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) ≤ V p h)
    (D : Phase → ℝ)
    (hExit : ∀ p a y, I p → stay p a y = false → 0 < K p θ a y →
      V (next p a y) [] + D (next p a y) ≤ D p)
    (p : Phase) (h : PhaseHistory (Obs := Obs) p) (hip : I p)
    (hm : 0 < dHistoryMass (continuingKernel K stay p) θ h) :
    cost p (π p h) + ∑ y, K p θ (π p h) y *
      normalizedResetPotential K stay θ V D (resetUpdate stay next π ⟨p,h⟩ y) ≤
      normalizedResetPotential K stay θ V D ⟨p,h⟩ := by
  let m := dHistoryMass (continuingKernel K stay p) θ h
  have hm' : 0 < m := hm
  have hchild : ∀ y : Obs p (π p h),
      K p θ (π p h) y * normalizedResetPotential K stay θ V D (resetUpdate stay next π ⟨p,h⟩ y) ≤
        (if stay p (π p h) y then V p (⟨π p h,y⟩::h) / m else 0) + D p * K p θ (π p h) y := by
    intro y
    by_cases hk : 0 < K p θ (π p h) y
    · cases hs : stay p (π p h) y
      · have hu : resetUpdate stay next π ⟨p,h⟩ y = ⟨next p (π p h) y,[]⟩ := by
          simp [resetUpdate,hs]
        rw [hu]
        simp only [hs,Bool.false_eq_true,↓reduceIte,normalizedResetPotential,
          dHistoryMass,zero_lt_one,div_one,zero_add]
        exact (mul_le_mul_of_nonneg_left (hExit p (π p h) y hip hs hk) (hK p θ (π p h) y)).trans_eq (mul_comm _ _)
      · have hmchild : 0 < dHistoryMass (continuingKernel K stay p) θ (⟨π p h,y⟩::h) := by
          simpa only [dHistoryMass,continuingKernel,hs,↓reduceIte] using mul_pos hm hk
        have hu : resetUpdate stay next π ⟨p,h⟩ y = ⟨p,⟨π p h,y⟩::h⟩ := by
          simp [resetUpdate,hs]
        rw [hu]
        simp only [hs,↓reduceIte,normalizedResetPotential,if_pos hmchild,
          dHistoryMass,continuingKernel,hs,↓reduceIte]
        dsimp [m]
        simp only [mul_pos_iff_of_pos_left hm,if_pos hk]
        apply le_of_eq
        field_simp [hm.ne', hk.ne']
        ring
    · have hz : K p θ (π p h) y = 0 := le_antisymm (le_of_not_gt hk) (hK _ _ _ _)
      rw [hz,zero_mul,mul_zero,add_zero]
      split_ifs
      · exact div_nonneg (hV _ _) hm'.le
      · exact le_rfl
  have hd := div_le_div_of_nonneg_right (hStep p hip h) hm.le
  have hd' : cost p (π p h) +
      (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) / m ≤ V p h / m := by
    simpa only [add_div,mul_div_cancel_right₀ _ hm.ne'] using hd
  rw [normalizedResetPotential,if_pos hm]
  calc
    _ ≤ cost p (π p h) + ∑ y : Obs p (π p h),
        ((if stay p (π p h) y then V p (⟨π p h,y⟩::h) / m else 0) + D p * K p θ (π p h) y) :=
      add_le_add_left (Finset.sum_le_sum (fun y _ => hchild y)) _
    _ = (cost p (π p h) +
        (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) / m) + D p := by
      rw [Finset.sum_add_distrib,← Finset.mul_sum,hNorm,mul_one]
      have he : (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) / m else 0) =
          (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) / m := by
        rw [Finset.sum_div]
        apply Finset.sum_congr rfl
        intro y _
        split_ifs <;> simp
      rw [he]
      ring
    _ ≤ _ := add_le_add_right hd' _
end Orthemology.Tranche3
