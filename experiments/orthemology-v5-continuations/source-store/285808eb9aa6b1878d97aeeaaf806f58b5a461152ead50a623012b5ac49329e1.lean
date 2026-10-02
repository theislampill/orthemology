import InnovationMeasure
import SurvivorPrimrec
import Q8Compiler

/-! Actual fair-Cantor law for the Σ2 least-surviving-candidate row family.
The zero-defect endpoint is ∃s∀t; its negation gives singleton-null defect one.
This is not yet a numeric-code compiler theorem or a Π3 tagged-row mixture. -/
namespace P02A2.Sigma2RowLaw
open P02A2.ObserverCore P02A2.Q8Measure P02A2.InnovationMeasure
open P02A2.SurvivorCandidates P02A2.SurvivorPrimrec
open MeasureTheory Set

variable {α : Type*} (R : α → ℕ → ℕ → Prop) [∀ a, DecidableRel (R a)]

def observer (a : α) : Cantor → Cantor := output (prefixFunction R a)

theorem observer_eq_switched (a : α) : observer R a = switched (innovation (R a)) := by
  funext x n
  unfold observer output prefixFunction
  cases h : innovation (R a) n
  · simp [h, switched]
  · simp only [h, ↓reduceIte, Nat.mod_mod, switched]
    rw [P02A2.Q8Compiler.sentinel_prefix_last]
    cases x n <;> rfl

theorem observer_measurable (a : α) : Measurable (observer R a) := by
  rw [observer_eq_switched]
  exact switched_measurable _

noncomputable def rowLaw (a : α) : Measure Cantor := fairCantor.map (observer R a)

theorem rowLaw_eq (a : α) : rowLaw R a = law (innovation (R a)) := by
  unfold rowLaw law
  rw [observer_eq_switched]

instance rowLaw_probability (a : α) : IsProbabilityMeasure (rowLaw R a) := by
  rw [rowLaw_eq]
  infer_instance

theorem finite_innovation_iff_witness (a : α) :
    (copied (innovation (R a))).Finite ↔ ∃ s, ∀ t, R a s t := by
  rw [finite_copied_iff_eventually_false]
  exact (witness_iff_eventually_no_innovation (R a)).symm

theorem defect_zero_iff_witness (a : α) :
    defect (rowLaw R a) = 0 ↔ ∃ s, ∀ t, R a s t := by
  rw [rowLaw_eq, defect_zero_iff_finite_copied]
  exact finite_innovation_iff_witness R a

theorem defect_one_iff_no_witness (a : α) :
    defect (rowLaw R a) = 1 ↔ ¬ ∃ s, ∀ t, R a s t := by
  rw [rowLaw_eq, defect_one_iff_infinite_copied]
  exact not_congr (finite_innovation_iff_witness R a)

theorem witness_finite_carrier (a : α) (h : ∃ s, ∀ t, R a s t) :
    ∃ C : Set Cantor, C.Finite ∧ rowLaw R a Cᶜ = 0 := by
  obtain ⟨N,hN⟩ := (witness_iff_eventually_no_innovation (R a)).mp h
  rw [rowLaw_eq]
  exact eventually_false_finite_carrier _ N hN

theorem no_witness_singletons_zero (a : α) (h : ¬ ∃ s, ∀ t, R a s t) (y : Cantor) :
    rowLaw R a {y} = 0 := by
  rw [rowLaw_eq]
  apply infinite_copied_singleton_zero
  exact fun hfin => h ((finite_innovation_iff_witness R a).mp hfin)

theorem defect_dichotomy (a : α) : defect (rowLaw R a) = 0 ∨ defect (rowLaw R a) = 1 := by
  classical
  by_cases h : ∃ s, ∀ t, R a s t
  · exact Or.inl ((defect_zero_iff_witness R a).mpr h)
  · exact Or.inr ((defect_one_iff_no_witness R a).mpr h)

theorem joint_prefix_primitive_recursive [Primcodable α]
    (hR : PrimrecRel (fun p : α × ℕ => R p.1 p.2)) :
    Primrec₂ (fun p : α × ℕ => prefixFunction R p.1 p.2) :=
  prefixFunction_primrec R hR

end P02A2.Sigma2RowLaw
