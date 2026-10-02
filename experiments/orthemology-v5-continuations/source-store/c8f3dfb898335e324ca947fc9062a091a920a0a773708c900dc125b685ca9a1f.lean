import MealyAtoms
import MealyRational

namespace Orthemology.Frontier.MealyMeasure.Fixtures
open Set MeasureTheory
open scoped ENNReal
open P02A2.Q8Measure

/-- One-state deterministic output. -/
def zeroMachine : Mealy Unit where
  next _ _ := ()
  out _ _ := false

/-- One-state fair input copying. -/
def copyMachine : Mealy Unit where
  next _ _ := ()
  out _ b := b

theorem zero_deterministic : zeroMachine.infiniteRel () () := by
  exact (deterministicBit_spec zeroMachine ()).mp (by decide)

theorem copy_nondeterministic : ¬ copyMachine.infiniteRel () () := by
  intro h
  have he := (h 1 false true).1
  exact Bool.false_ne_true he

theorem zero_atomic_mass_one : P02A2.mass (law zeroMachine ()) = 1 := by
  rw [atomic_mass_eq_hitting_probability]
  have he : hits zeroMachine () = univ := by
    ext x
    simp only [hits, mem_setOf_eq, mem_univ, iff_true]
    exact ⟨0, zero_deterministic⟩
  rw [he, measure_univ]

theorem copy_atomic_mass_zero : P02A2.mass (law copyMachine ()) = 0 := by
  apply (atomic_mass_zero_iff_unreachable copyMachine ()).mpr
  intro u
  exact copy_nondeterministic

/-- A real three-state mixture: first bit chooses deterministic zero or permanent fresh-bit copying. -/
def splitMachine : Mealy (Fin 3) where
  next s b := if s = 0 then (if b then 2 else 1) else s
  out s b := if s = 2 then b else false

theorem split_domain (s : Fin 3) : splitMachine.infiniteRel s s ↔ s = 1 := by
  rw [← deterministicBit_spec]
  fin_cases s <;> decide

theorem split_state_succ (x : Cantor) (n : ℕ) :
    state splitMachine 0 x (n+1) = if x 0 then 2 else 1 := by
  induction n with
  | zero => simp [state, splitMachine]
  | succ n ih =>
    change splitMachine.next (state splitMachine 0 x (n+1)) (x (n+1)) = _
    rw [ih]
    cases h : x 0 <;> norm_num [splitMachine, show (2 : Fin 3) ≠ 0 by decide]

theorem split_hits_cylinder : hits splitMachine 0 = cylinder [false] := by
  ext x
  simp only [hits, mem_setOf_eq, split_domain]
  constructor
  · rintro ⟨n, hn⟩
    cases n with
    | zero => simp [state] at hn
    | succ n =>
      rw [split_state_succ] at hn
      cases h : x 0 <;> simp_all [cylinder, pref, List.ofFn_succ]
  · intro hx
    refine ⟨1, ?_⟩
    have hx0 : x 0 = false := by simpa [cylinder, pref, List.ofFn_succ] using hx
    simp [state, splitMachine, hx0]

theorem split_atomic_mass_half : P02A2.mass (law splitMachine 0) = (1/2 : ℝ≥0∞) := by
  rw [atomic_mass_eq_hitting_probability, split_hits_cylinder, measure_cylinder]
  simp

/- Executable finite-horizon checks supplement, but do not replace, the kernel proofs above. -/
#eval hittingProbabilityQ zeroMachine () 4
#eval hittingProbabilityQ copyMachine () 4
#eval hittingProbabilityQ splitMachine 0 0
#eval hittingProbabilityQ splitMachine 0 1
#eval hittingProbabilityQ splitMachine 0 4

end Orthemology.Frontier.MealyMeasure.Fixtures
