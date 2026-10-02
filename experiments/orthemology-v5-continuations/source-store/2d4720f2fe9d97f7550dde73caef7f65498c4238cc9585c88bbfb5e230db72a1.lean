import GuardedObserver
import ContextualObserver

namespace IndependentObserverControls
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver
open MeasureTheory Set
open scoped ENNReal

def echo : Mealy Unit where
  next _ _ := ()
  out _ b := b

def counter : Mealy ℕ where
  next n _ := n+1
  out _ b := b

def zero : Mealy Unit where
  next _ _ := ()
  out _ _ := false

def counterEcho : Simulation counter echo where
  relates _ _ := True
  out_eq := by intro s t _ b; rfl
  next_rel := by intro s t _ b; trivial

theorem arbitrary_state_measurable : Measurable (output counter 0) :=
  Orthemology.CertifiedObserver.output_measurable counter 0

theorem arbitrary_state_law : law counter 0 = law echo () :=
  simulation_law counterEcho trivial

theorem infinite_counter_solver :
    (solveDefect echo () : ℝ) = P02A2.defect (law counter 0) :=
  certified_defect_exact counterEcho trivial

theorem echo_not_input_independent : ¬ echo.infiniteRel () () := by
  intro h
  have hx := (h 1 false true).1
  cases hx

theorem no_false_echo_simulation :
    ¬ ∃ R : Simulation zero echo, R.relates () () := by
  rintro ⟨R,h⟩
  have hx := R.out_eq h true
  cases hx

def delayed : Mealy ℕ where
  next n _ := n+1
  out n _ := decide (0<n)

theorem same_initial_output : ∀ b, delayed.out 0 b = zero.out () b := by
  intro b
  rfl

theorem next_obligation_is_essential :
    ¬ ∃ R : Simulation delayed zero, R.relates 0 () := by
  rintro ⟨R,h⟩
  have hx := R.out_eq (R.next_rel h false) false
  change true = false at hx
  cases hx

def allBad : GuardedSimulation zero echo where
  relates _ _ := True
  bad _ _ _ := True
  out_eq := by intro s t _ b h; exact (h trivial).elim
  next_rel := by intro s t _ b _; trivial

theorem vacuous_guard_is_whole_failure : badRun allBad () () = Set.univ := by
  ext x
  simp [badRun,badAt,allBad]

theorem actual_guard_event_measurable : MeasurableSet (badRun allBad () ()) :=
  badRun_measurable allBad () ()

def clean : GuardedSimulation counter echo where
  relates _ _ := True
  bad _ _ _ := False
  out_eq := by intro s t _ b _; rfl
  next_rel := by intro s t _ b _; trivial

theorem empty_guard : badRun clean 0 () = ∅ := by
  ext x
  simp [badRun,badAt,clean]

theorem clean_whole_output (x : Cantor) : output counter 0 x = output echo () x :=
  guarded_output clean trivial (by rw [empty_guard]; simp)

-- A declared observer can erase all source terms. The core does not assert source faithfulness.
theorem term_ignoring_start_erases_source {Γ : P01D.Context} {A : P01D.Ty Γ}
    (O : ObserverFamily A) (hc : ∀ γ x y, O.start γ x = O.start γ y)
    (t u : P01D.Tm Γ A) (γ : Γ.Val) : O.observe t γ = O.observe u γ := by
  unfold ObserverFamily.observe
  rw [hc γ]

-- Same-input simulation may relate distinct states without an inverse abstraction.
def duplicateEcho : Mealy Bool where
  next s _ := !s
  out _ b := b

def quotientEcho : Simulation duplicateEcho echo where
  relates _ _ := True
  out_eq := by intro s t _ b; rfl
  next_rel := by intro s t _ b; trivial

theorem two_states_one_observer : law duplicateEcho false = law duplicateEcho true := by
  exact (simulation_law quotientEcho (s:=false) (t:=()) trivial).trans
    (simulation_law quotientEcho (s:=true) (t:=()) trivial).symm

end IndependentObserverControls
