import MealyMeasureFixtures
import Sigma2Witnesses
import LoopInliningWitnesses
import LoopPrimrec

namespace IndependentObserverAudit
open Set MeasureTheory
open scoped ENNReal
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.Frontier.MealyMeasure.Fixtures
open P02A2.Q8Measure (fairCantor)

/-- Deleting avoidance from fixed-output fibre nullity gives an outright false claim. -/
theorem constant_fibre_measure_one :
    fairCantor {x : Cantor | output zeroMachine () x = fun _ => false} = 1 := by
  have he : {x : Cantor | output zeroMachine () x = fun _ => false} = Set.univ := by
    ext x
    simp only [Set.mem_setOf_eq, Set.mem_univ, iff_true]
    rfl
  rw [he, measure_univ]

/-- Without a zero boundary on non-reaching components, homogeneous harmonic uniqueness fails. -/
theorem nonreaching_harmonic_countermodel :
    (∀ q : Unit, copyMachine.infiniteRel q q → (1 : ℚ) = 0) ∧
    (∀ q : Unit, 2 * (1 : ℚ) = 1 + 1) ∧
    (fun _ : Unit => (1 : ℚ)) ≠ 0 := by
  refine ⟨?_, by norm_num, ?_⟩
  · intro q h
    exact (copy_nondeterministic h).elim
  · intro h
    have he := congrFun h ()
    norm_num at he

def exceptionalInput : Cantor := fun n => decide (n = 0)

theorem exceptional_output : output splitMachine 0 exceptionalInput = fun _ => false := by
  funext n
  cases n with
  | zero => simp [output, state, splitMachine]
  | succ n => simp [output, split_state_succ, exceptionalInput, splitMachine]

theorem exceptional_avoids : exceptionalInput ∉ hits splitMachine 0 := by
  rw [split_hits_cylinder]
  simp [Orthemology.Frontier.MealyMeasure.cylinder, pref, List.ofFn_succ, exceptionalInput]

theorem zero_output_positive : (fun _ => false) ∈ P02A2.positive (Orthemology.Frontier.MealyMeasure.law splitMachine 0) := by
  have hhit : (fun _ => false) ∈ hits splitMachine 0 := by
    rw [split_hits_cylinder]
    simp [Orthemology.Frontier.MealyMeasure.cylinder, pref, List.ofFn_succ]
  have hp := hits_output_positive splitMachine 0 hhit
  have he : output splitMachine 0 (fun _ => false) = fun _ => false := by
    funext n
    cases n with
    | zero => simp [output, state, splitMachine]
    | succ n => simp [output, split_state_succ, splitMachine]
  rwa [he] at hp

/-- Equality of atomic mass and hitting probability is not equality of input events. -/
theorem positive_output_can_avoid_D :
    ∃ x : Cantor, output splitMachine 0 x ∈ P02A2.positive
      (Orthemology.Frontier.MealyMeasure.law splitMachine 0) ∧ x ∉ hits splitMachine 0 := by
  exact ⟨exceptionalInput, by rw [exceptional_output]; exact zero_output_positive, exceptional_avoids⟩

def repeatFirst (x : Cantor) : Cantor := fun _ => x 0

theorem repeatFirst_measurable : Measurable repeatFirst :=
  measurable_pi_lambda _ (fun _ => measurable_pi_apply 0)

noncomputable def repeatedLaw : Measure Cantor := fairCantor.map repeatFirst

/-- Infinitely many output ticks reveal only one bit if coordinates are reused. -/
theorem repeated_bit_defect_zero : P02A2.defect repeatedLaw = 0 := by
  let C : Set Cantor := Set.range (fun b : Bool => fun _ : ℕ => b)
  have hC : C.Finite := Set.finite_range _
  have hfull : repeatedLaw Cᶜ = 0 := by
    rw [repeatedLaw, Measure.map_apply repeatFirst_measurable hC.measurableSet.compl]
    have he : repeatFirst ⁻¹' Cᶜ = ∅ := by
      apply Set.eq_empty_iff_forall_not_mem.mpr
      intro x hx
      exact hx ⟨x 0, rfl⟩
    rw [he, measure_empty]
  have hprob : repeatedLaw Set.univ = 1 := by
    rw [repeatedLaw, Measure.map_apply repeatFirst_measurable MeasurableSet.univ]
    simp
  letI : IsProbabilityMeasure repeatedLaw := ⟨hprob⟩
  have hm := P02A2.countable_carrier_mass_one repeatedLaw hC.countable hfull hprob
  simp [P02A2.defect, hm]

open P02A2.ObserverCore P02A2.LoopPrimrec
/-- A finite-store bound that omits a written register destroys simulation. -/
theorem omitted_register_breaks_simulation :
    exec (.set 1 (.constant 7)) (P02A2.LoopPrimrec.extend (fun _ : Fin 1 => 0)) 1 = 7 ∧
    P02A2.LoopPrimrec.extend (execFin 1 (.set 1 (.constant 7)) (fun _ => 0)) 1 = 0 := by
  decide +kernel

#print axioms constant_fibre_measure_one
#print axioms nonreaching_harmonic_countermodel
#print axioms positive_output_can_avoid_D
#print axioms repeated_bit_defect_zero
#print axioms omitted_register_breaks_simulation
end IndependentObserverAudit
