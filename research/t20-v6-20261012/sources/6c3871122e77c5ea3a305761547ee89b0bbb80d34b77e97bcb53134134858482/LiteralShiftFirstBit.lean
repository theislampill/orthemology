import LiteralShiftPrefix
import FiniteOutputTable

open Set MeasureTheory
open scoped ENNReal
namespace P02.LiteralShift
open P02A2 P02A2.ObserverCore P02A2.Q8Measure P02A2.FiniteOutputTable

theorem compiledOutput_first (body : Stmt) (output a b : ℕ) (x : Cantor) :
    compiledOutput body output a b x 0 = x 0 := by
  rcases firstCut_or_unresolved a b x with ⟨k,side,hk⟩ | hu
  · exact compiledOutput_copied_prefix body output a b k 0 x side hk (by have := hk.1; omega)
  · exact congrFun (compiledOutput_unresolved body output a b x hu) 0

/-- Every literal output keeps a fair first bit, including zero shift. -/
theorem compiledOutput_first_probability (body : Stmt) (output a b : ℕ) :
    fairCantor.map (compiledOutput body output a b) {x | x 0 = true} = 1/2 := by
  have hm : Measurable (compiledOutput body output a b) := output_measurable _
  have he : (compiledOutput body output a b) ⁻¹' {x | x 0 = true} =
      AtomicMembership.cylinder 1 (fun _ => true) := by
    ext x
    simp only [Set.mem_preimage, Set.mem_setOf_eq, compiledOutput_first]
    change (x 0 = true) ↔ AtomicMembership.bitsPrefix 1 x = fun _ => true
    constructor
    · intro h
      funext i
      have hi : i.val = 0 := by omega
      simpa [AtomicMembership.bitsPrefix, hi] using h
    · intro h
      exact congrFun h ⟨0, by omega⟩
  have hE : MeasurableSet {x : Cantor | x 0 = true} :=
    measurableSet_eq_fun (measurable_pi_apply 0) measurable_const
  rw [Measure.map_apply hm hE, he,
    fair_cylinder]
  simp

theorem skip_base_first_probability :
    fairCantor.map (P02A2.ObserverCore.output (programValue .skip 2))
      {x | x 0 = true} = 0 := by
  have hE : MeasurableSet {x : Cantor | x 0 = true} :=
    measurableSet_eq_fun (measurable_pi_apply 0) measurable_const
  rw [Measure.map_apply (output_measurable _) hE]
  have he : P02A2.ObserverCore.output (programValue .skip 2) ⁻¹' {x | x 0 = true} = ∅ := by
    ext x
    simp [P02A2.ObserverCore.output, programValue, exec, initial]
  rw [he, measure_empty]

/-- Zero shift has the same defect as the base but not the same whole law.
This guards against dropping the literal copied stopping prefix. -/
theorem literal_zero_law_ne_base (b : ℕ) :
    fairCantor.map (compiledOutput .skip 2 0 b) ≠
      fairCantor.map (P02A2.ObserverCore.output (programValue .skip 2)) := by
  intro h
  have he := congrArg (fun μ : Measure Cantor => μ {x | x 0 = true}) h
  dsimp only at he
  rw [compiledOutput_first_probability, skip_base_first_probability] at he
  norm_num at he

end P02.LiteralShift
