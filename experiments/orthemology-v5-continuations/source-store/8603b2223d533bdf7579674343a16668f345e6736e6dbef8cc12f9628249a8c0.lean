import GuardedObserver
import MealyMeasureFixtures

namespace Orthemology.CertifiedObserver.Fixtures
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.Frontier.MealyMeasure.Fixtures
open Set MeasureTheory
open scoped ENNReal
open P02A2.Q8Measure (fairCantor)

/-- A genuinely infinite concrete state carrier, preserving an unbounded
counter through every real transition. -/
def counterLift {S : Type*} (M : Mealy S) : Mealy (S × ℕ) where
  next z b := (M.next z.1 b, z.2+1)
  out z b := M.out z.1 b

def counterSimulation {S : Type*} (M : Mealy S) : Simulation (counterLift M) M :=
  simulationOfMap (counterLift M) M Prod.fst (fun _ _ => rfl) (fun _ _ => rfl)

theorem counter_law {S : Type*} (M : Mealy S) (s : S) (n : ℕ) :
    law (counterLift M) (s,n) = law M s := simulation_law (counterSimulation M) rfl

theorem unbounded_split_defect (n : ℕ) :
    P02A2.defect (law (counterLift splitMachine) (0,n)) = (1/2 : ℝ) := by
  rw [counter_law, P02A2.defect, split_atomic_mass_half]
  norm_num

theorem split_solver_exact : solveDefect splitMachine 0 = (1/2 : ℚ) := by
  have h : (solveDefect splitMachine 0 : ℝ) = (1/2 : ℝ) := by
    rw [solveDefect_correct, P02A2.defect, split_atomic_mass_half]
    norm_num
  apply Rat.cast_injective (α := ℝ)
  simpa only [Rat.cast_div, Rat.cast_one, Rat.cast_ofNat] using h

theorem unbounded_split_solver (n : ℕ) :
    (solveDefect splitMachine 0 : ℝ) = P02A2.defect (law (counterLift splitMachine) (0,n)) ∧
    solveDefect splitMachine 0 = (1/2 : ℚ) :=
  ⟨certified_defect_exact (counterSimulation splitMachine) rfl, split_solver_exact⟩

#eval solveDefect splitMachine 0

/-- On the good branch the one-shot splitter exactly refines zero output.
The escape guard is evaluated in the actual source/target run. -/
def splitZeroGuard : GuardedSimulation splitMachine zeroMachine where
  relates s _ := s = 0 ∨ s = 1
  bad s _ b := s = 0 ∧ b = true
  out_eq := by
    intro s t hs b hb
    rcases hs with rfl | rfl <;> rfl
  next_rel := by
    intro s t hs b hb
    rcases hs with rfl | rfl
    · have hbf : b = false := by cases b <;> simp_all
      simp [splitMachine, hbf]
    · simp [splitMachine]

theorem split_badAt_zero : badAt splitZeroGuard 0 () 0 = cylinder [true] := by
  ext x
  simp [badAt, state, splitZeroGuard, MealyMeasure.cylinder, pref, List.ofFn_succ]

theorem split_badAt_succ (n : ℕ) : badAt splitZeroGuard 0 () (n+1) = ∅ := by
  ext x
  simp only [badAt, mem_setOf_eq, splitZeroGuard, split_state_succ, mem_empty_iff_false,
    iff_false, not_and]
  cases h : x 0 <;> simp

theorem split_badRun : badRun splitZeroGuard 0 () = cylinder [true] := by
  ext x
  simp only [badRun, mem_iUnion]
  constructor
  · rintro ⟨n, hn⟩
    cases n with
    | zero => simpa only [split_badAt_zero] using hn
    | succ n => simp only [split_badAt_succ, Set.mem_empty_iff_false] at hn
  · intro hx
    exact ⟨0, by simpa only [split_badAt_zero] using hx⟩

theorem split_budget_exact : fairCantor (badRun splitZeroGuard 0 ()) = (1/2 : ℝ≥0∞) := by
  rw [split_badRun, measure_cylinder]
  simp

theorem split_guarded_error :
    |P02A2.defect (law splitMachine 0) - (solveDefect zeroMachine () : ℝ)| ≤ (1/2 : ℝ) := by
  have h := guarded_defect_error splitZeroGuard (s := 0) (t := ()) (Or.inl rfl)
  rw [split_budget_exact] at h
  norm_num at h ⊢
  exact h

/-- Arbitrarily long exact finite-prefix agreement can hide a unit
infinite-law defect error. The source really uses an unbounded clock. -/
def delayedCopy (N : ℕ) : Mealy ℕ where
  next n _ := n+1
  out n b := if N ≤ n then b else false

theorem delayed_state (N s : ℕ) (x : Cantor) (n : ℕ) :
    state (delayedCopy N) s x n = s+n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change state (delayedCopy N) s x n + 1 = s+(n+1)
      rw [ih]
      omega

theorem delayed_output (N : ℕ) : output (delayedCopy N) 0 =
    P02A2.Q8Measure.switched (fun n => decide (N ≤ n)) := by
  funext x n
  simp only [output]
  rw [delayed_state]
  simp [delayedCopy, P02A2.Q8Measure.switched]

theorem delayed_defect_one (N : ℕ) : P02A2.defect (law (delayedCopy N) 0) = 1 := by
  unfold law
  rw [delayed_output]
  exact P02A2.Q8Measure.eventually_defect_one _ N (fun n hn => by simp [hn])

theorem delayed_prefix_exact (N : ℕ) (x : Cantor) :
    pref N (output (delayedCopy N) 0 x) = pref N (output zeroMachine () x) := by
  apply (prefix_eq_iff _ _ _).mpr
  intro i hi
  simp only [output]
  rw [delayed_state]
  simp [delayedCopy, zeroMachine, Nat.not_le.mpr hi]

theorem zero_defect : P02A2.defect (law zeroMachine ()) = 0 := by
  rw [P02A2.defect, zero_atomic_mass_one]
  norm_num

theorem finite_prefix_is_not_defect_certificate (N : ℕ) :
    (∀ x, pref N (output (delayedCopy N) 0 x) = pref N (output zeroMachine () x)) ∧
    |P02A2.defect (law (delayedCopy N) 0) - P02A2.defect (law zeroMachine ())| = 1 := by
  exact ⟨delayed_prefix_exact N, by rw [delayed_defect_one, zero_defect]; norm_num⟩

theorem split_error_sharp :
    |P02A2.defect (law splitMachine 0) - (solveDefect zeroMachine () : ℝ)| = (1/2 : ℝ) := by
  rw [solveDefect_correct, zero_defect, P02A2.defect, split_atomic_mass_half]
  norm_num

/-- Matching outputs only at the initial related states omits the invariant. -/
theorem transition_omission_fails :
    (∀ b, (delayedCopy 1).out 0 b = zeroMachine.out () b) ∧
    output (delayedCopy 1) 0 ≠ output zeroMachine () := by
  refine ⟨fun _ => rfl, ?_⟩
  intro h
  have he := congrFun (congrFun h (fun _ => true)) 1
  simp [output, state, delayedCopy, zeroMachine] at he

/-- Matching transitions alone leaves observations unconstrained. -/
theorem output_omission_fails :
    (∀ s b, copyMachine.next s b = zeroMachine.next s b) ∧
    output copyMachine () ≠ output zeroMachine () := by
  refine ⟨fun _ _ => rfl, ?_⟩
  intro h
  have he := congrFun (congrFun h (fun _ => true)) 0
  cases he

end Orthemology.CertifiedObserver.Fixtures
