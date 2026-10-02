import TaggedMass
import Sigma2RowLaw

open Set MeasureTheory
namespace OrthemologyTagged
open P02A2 P02A2.Q8Measure

variable {A : Type*} (R : A → ℕ → ℕ → ℕ → Prop)
  [∀ a i, DecidableRel (R a i)]

noncomputable def pi3Observer (a : A) : Cantor → Cantor :=
  tagged (P02A2.Sigma2RowLaw.observer (R a))

theorem pi3Observer_measurable (a : A) : Measurable (pi3Observer R a) :=
  tagged_measurable (P02A2.Sigma2RowLaw.observer_measurable (R a))

noncomputable def pi3Law (a : A) : Measure Cantor := fairCantor.map (pi3Observer R a)

instance pi3Law_probability (a : A) : IsProbabilityMeasure (pi3Law R a) := by
  constructor
  rw [pi3Law, Measure.map_apply (pi3Observer_measurable R a) MeasurableSet.univ]
  simp

/-- Exact semantic Π3-shaped equivalence under the actual fair-source law.
This alone does not assert an effective numeric-index reduction or hierarchy completeness. -/
theorem pi3_zero_defect_iff (a : A) :
    defect (pi3Law R a) = 0 ↔ ∀ i, ∃ s, ∀ t, R a i s t := by
  unfold pi3Law pi3Observer
  rw [tagged_zero_defect_iff (P02A2.Sigma2RowLaw.observer_measurable (R a))]
  exact forall_congr' fun i => P02A2.Sigma2RowLaw.defect_zero_iff_witness (R a) i

theorem pi3_defect_nonnegative (a : A) : 0 ≤ defect (pi3Law R a) := by
  have hm : mass (pi3Law R a) ≤ 1 := (positive_le_total _).trans_eq measure_univ
  have ht : (mass (pi3Law R a)).toReal ≤ 1 := by
    simpa using ENNReal.toReal_mono (by simp : (1 : ENNReal) ≠ ⊤) hm
  unfold defect
  linarith

/-- The complementary positive-defect condition retains the quantifier order. -/
theorem pi3_positive_defect_iff (a : A) :
    0 < defect (pi3Law R a) ↔ ∃ i, ∀ s, ∃ t, ¬ R a i s t := by
  classical
  constructor
  · intro hpos
    have hn : ¬ ∀ i, ∃ s, ∀ t, R a i s t :=
      (not_congr (pi3_zero_defect_iff R a)).mp (ne_of_gt hpos)
    push_neg at hn
    exact hn
  · intro hbad
    have hz : defect (pi3Law R a) ≠ 0 := by
      intro hzero
      obtain ⟨i,hi⟩ := hbad
      obtain ⟨s,hs⟩ := (pi3_zero_defect_iff R a).mp hzero i
      obtain ⟨t,ht⟩ := hi s
      exact ht (hs t)
    exact lt_of_le_of_ne (pi3_defect_nonnegative R a) (Ne.symm hz)

end OrthemologyTagged
#print axioms OrthemologyTagged.pi3_zero_defect_iff
#print axioms OrthemologyTagged.pi3_positive_defect_iff
