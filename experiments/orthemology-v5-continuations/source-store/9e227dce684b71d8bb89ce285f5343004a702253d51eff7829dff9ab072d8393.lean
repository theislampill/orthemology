import RecursiveWinningCertificate

noncomputable section
open Finset

namespace Orthemology.Tranche2
variable {Θ A Y : Type*} [DecidableEq Θ] [DecidableEq A]

/-- The support at a stopped-prefix exit; continuing records keep the original
phase support until the first exit. On completion it returns that support. -/
def stoppedSupport (P : Θ → A → Y → ℝ) (B : Finset Θ) :
    (acts : List A) → StopObs Y acts.length → Finset Θ
  | [], _ => B
  | a::_, Sum.inl y => supportUpdate P B a y
  | _::as, Sum.inr (_,w) => stoppedSupport P B as w

omit [DecidableEq Θ] [DecidableEq A] in
lemma stoppedSupport_subset (P : Θ → A → Y → ℝ) (B : Finset Θ)
    (acts : List A) (w : StopObs Y acts.length) : stoppedSupport P B acts w ⊆ B := by
  induction acts with
  | nil => exact Finset.Subset.refl _
  | cons a as ih =>
    rcases w with y | ⟨y,w⟩
    · exact supportUpdate_subset P B a y
    · exact ih w

omit [DecidableEq A] in
/-- A positive-probability exit has an actual executed action/symbol witness.
This links the stopped block law back to the recursive one-step support rule. -/
theorem stopped_exit_witness (P : Θ → A → Y → ℝ) (B : Finset Θ)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ) (acts : List A)
    (w : StopObs Y acts.length) (hw : stopCompleted w = false)
    (hp : 0 < stoppedMass (P θ) (supportStay P B) acts w) :
    ∃ a ∈ acts, ∃ y, supportStay P B a y = false ∧ 0 < P θ a y ∧
      stoppedSupport P B acts w = supportUpdate P B a y := by
  induction acts with
  | nil => simp [stopCompleted] at hw
  | cons a as ih =>
    rcases w with y | ⟨y,w⟩
    · by_cases hs : supportStay P B a y = true
      · simp [stoppedMass, hs] at hp
      · have hs' : supportStay P B a y = false := Bool.eq_false_iff.mpr hs
        refine ⟨a, List.mem_cons_self, y, hs', ?_, rfl⟩
        simpa only [stoppedMass, hs', Bool.false_eq_true, ↓reduceIte] using hp
    · by_cases hs : supportStay P B a y = true
      · have ht : 0 < stoppedMass (P θ) (supportStay P B) as w := by
          have hm : 0 < P θ a y * stoppedMass (P θ) (supportStay P B) as w := by
            simpa only [stoppedMass, hs, ↓reduceIte] using hp
          by_contra! hn
          exact (not_lt_of_ge (mul_nonpos_of_nonneg_of_nonpos (hP θ a y) hn)) hm
        obtain ⟨b,hb,z,hz,hp,hEq⟩ := ih w hw ht
        exact ⟨b,List.mem_cons_of_mem a hb,z,hz,hp,hEq⟩
      · simp [stoppedMass, hs] at hp

end Orthemology.Tranche2
