import EffectiveAtoms
import MealySolverFixtures

namespace Orthemology.Frontier.MealyMeasure.Fixtures
open Set MeasureTheory
open scoped ENNReal
open P02A2.Q8Measure

def falseTarget : Generator Unit where
  next _ := ()
  out _ := false

def trueTarget : Generator Unit where
  next _ := ()
  out _ := true

/-- Exact singleton mass when all D-hitting paths produce the specified target. -/
theorem singleton_eq_hitting_of_unique_output {S : Type*} [Finite S] [Nonempty S]
    (M : Mealy S) (s : S) (y : Cantor)
    (hunique : ∀ x ∈ hits M s, output M s x = y) :
    law M s {y} = fairCantor (hits M s) := by
  rw [law, Measure.map_apply (output_measurable M s) (measurableSet_singleton _)]
  have hsub : hits M s ⊆ output M s ⁻¹' {y} := fun x hx => hunique x hx
  have he := measure_inter_add_diff (μ := fairCantor) (output M s ⁻¹' {y}) (measurableSet_hits M s)
  have hz : fairCantor ((output M s ⁻¹' {y}) \ hits M s) = 0 := avoidMatch_null M s y
  rw [inter_eq_right.mpr hsub, hz, add_zero] at he
  exact he.symm

theorem zero_false_target_mass : law zeroMachine () {falseTarget.stream ()} = 1 := by
  rw [law]
  change (fairCantor.map (fun _ : Cantor => fun _ : ℕ => false)) {fun _ : ℕ => false} = 1
  rw [Measure.map_const]
  simp

theorem zero_true_target_mass : law zeroMachine () {trueTarget.stream ()} = 0 := by
  rw [law]
  change (fairCantor.map (fun _ : Cantor => fun _ : ℕ => false)) {fun _ : ℕ => true} = 0
  rw [Measure.map_const]
  simp
  intro h
  exact Bool.false_ne_true (congrFun h 0)

theorem copy_false_target_mass : law copyMachine () {falseTarget.stream ()} = 0 := by
  rw [law, Measure.map_apply (output_measurable copyMachine ()) (measurableSet_singleton _)]
  apply measure_mono_null (t := avoidMatch copyMachine () (falseTarget.stream ()))
  · intro x hx
    refine ⟨hx, ?_⟩
    rintro ⟨n, hn⟩
    exact copy_nondeterministic hn
  · exact avoidMatch_null _ _ _

theorem split_hit_output_false (x : Cantor) (hx : x ∈ hits splitMachine 0) :
    output splitMachine 0 x = falseTarget.stream () := by
  rw [split_hits_cylinder] at hx
  have hx0 : x 0 = false := by simpa [cylinder, pref, List.ofFn_succ] using hx
  funext n
  cases n with
  | zero => rfl
  | succ n =>
    change splitMachine.out (state splitMachine 0 x (n+1)) (x (n+1)) = false
    rw [split_state_succ, hx0]
    rfl

theorem split_false_target_mass : law splitMachine 0 {falseTarget.stream ()} = (1/2 : ℝ≥0∞) := by
  rw [singleton_eq_hitting_of_unique_output _ _ _ split_hit_output_false,
    ← atomic_mass_eq_hitting_probability]
  exact split_atomic_mass_half

theorem target_solver_zero_correct : targetMassQ zeroMachine falseTarget () () = 1 := by
  have h := targetMassQ_correct zeroMachine falseTarget () ()
  rw [zero_false_target_mass] at h
  exact_mod_cast h

theorem target_solver_never_correct : targetMassQ zeroMachine trueTarget () () = 0 := by
  have h := targetMassQ_correct zeroMachine trueTarget () ()
  rw [zero_true_target_mass] at h
  exact_mod_cast h

theorem target_solver_copy_correct : targetMassQ copyMachine falseTarget () () = 0 := by
  have h := targetMassQ_correct copyMachine falseTarget () ()
  rw [copy_false_target_mass] at h
  exact_mod_cast h

theorem target_solver_split_correct : targetMassQ splitMachine falseTarget 0 () = 1/2 := by
  have h := targetMassQ_correct splitMachine falseTarget 0 ()
  rw [split_false_target_mass] at h
  norm_num at h
  apply Rat.cast_injective (α := ℝ)
  simpa using h

#eval targetMassQ zeroMachine falseTarget () ()
#eval targetMassQ zeroMachine trueTarget () ()
#eval targetMassQ copyMachine falseTarget () ()
#eval targetMassQ splitMachine falseTarget 0 ()
#eval enumerateAtoms zeroMachine () 0
#eval enumerateAtoms zeroMachine () 1

end Orthemology.Frontier.MealyMeasure.Fixtures
