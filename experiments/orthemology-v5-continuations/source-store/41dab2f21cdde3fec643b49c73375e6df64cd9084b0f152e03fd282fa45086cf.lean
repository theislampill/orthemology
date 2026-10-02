import StoppedBlock

namespace Orthemology.Tranche2
variable {A Y : Type*}

/-- A non-completed stopped-prefix record has zero probability when every
exit-labelled one-step observation has zero mass. -/
theorem stoppedMass_zero_of_no_exit (p : A → Y → ℝ) (stay : A → Y → Bool)
    (hzero : ∀ a y, stay a y = false → p a y = 0)
    (acts : List A) (w : StopObs Y acts.length) (hw : stopCompleted w = false) :
    stoppedMass p stay acts w = 0 := by
  induction acts with
  | nil => simp [stopCompleted] at hw
  | cons a as ih =>
    rcases w with y | ⟨y,w⟩
    · cases hs : stay a y
      · simpa only [stoppedMass, hs, Bool.false_eq_true, ↓reduceIte] using hzero a y hs
      · simp [stoppedMass, hs]
    · have ht : stopCompleted w = false := hw
      simp only [stoppedMass, ih w ht, mul_zero]
      split_ifs <;> rfl

end Orthemology.Tranche2
