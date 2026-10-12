import CheckedTargetOperation

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2
open HiddenParity.Recurrence
open scoped ENNReal BigOperators

namespace RecurrenceIndependentReview
abbrev Two := Fin 2

def biasedChain : FiniteChain Two where
  prob s t := if s = 0 then (if t = 0 then 3/4 else 1/4) else (if t = 0 then 1 else 0)
  nonnegative s t := by split_ifs <;> norm_num
  normalized s := by fin_cases s <;> norm_num [Fin.sum_univ_two]

/-- One coordinate includes the initial state, not one future transition. -/
theorem initial_coordinate_checked :
    avoid biasedChain 0 1 0 = 0 ∧ avoid biasedChain 1 1 0 = 1 := by
  norm_num [avoid, biasedChain, Fin.sum_univ_two]

theorem weighted_second_and_third_coordinates :
    avoid biasedChain 1 2 0 = 3/4 ∧ avoid biasedChain 1 3 0 = 9/16 := by
  norm_num [avoid, biasedChain, Fin.sum_univ_two]

theorem actual_initial_integral (target start : Two) :
    (∫⁻ x, pathAvoid target 0 1 x ∂markovTrajectory (transitionKernel biasedChain) start) =
      ENNReal.ofReal (avoid biasedChain target 1 start) := by
  rw [trajectory_integral_prefix (transitionKernel biasedChain) (pathAvoid target 0 1)
    (pathAvoid_measurable target 0 1) 0 (pathAvoid_depends target 0 0) start]
  exact lmarginal_pathAvoid biasedChain target 0 0 (fun _ => start)

theorem actual_initial_index_distinguishes_target :
    (∫⁻ x, pathAvoid 0 0 1 x ∂markovTrajectory (transitionKernel biasedChain) 0) = 0 ∧
    (∫⁻ x, pathAvoid 1 0 1 x ∂markovTrajectory (transitionKernel biasedChain) 0) = 1 := by
  rw [actual_initial_integral, actual_initial_integral,
    initial_coordinate_checked.1, initial_coordinate_checked.2]
  norm_num

theorem biased_strong : ∀ s t, Relation.ReflTransGen
    (fun s t => 0 < biasedChain.prob s t) s t := by
  intro s t
  fin_cases s <;> fin_cases t
  all_goals first
    | exact Relation.ReflTransGen.refl
    | apply Relation.ReflTransGen.single; norm_num [biasedChain]

theorem biased_all_recur :
    ∀ᵐ x ∂markovTrajectory (transitionKernel biasedChain) 0,
      ∀ t, ∃ᶠ n in atTop, x n = t :=
  all_states_recur_almost_surely biasedChain 0 biased_strong

theorem biased_geometric_bound (k : ℕ) (s : Two) :
    avoid biasedChain 1 (k*2) s ≤ (3/4 : ℝ)^k := by
  apply avoid_blocks_bound biasedChain 1 2 (3/4) (by norm_num)
  intro t
  fin_cases t <;> norm_num [avoid, biasedChain, Fin.sum_univ_two]

#print axioms initial_coordinate_checked
#print axioms weighted_second_and_third_coordinates
#print axioms actual_initial_integral
#print axioms actual_initial_index_distinguishes_target
#print axioms biased_strong
#print axioms biased_all_recur
#print axioms biased_geometric_bound
end RecurrenceIndependentReview
