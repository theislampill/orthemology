import MealySolver
import MealyMeasureFixtures

namespace Orthemology.Frontier.MealyMeasure.Fixtures
open Set MeasureTheory
open scoped ENNReal
open P02A2.Q8Measure

/-- Four-state gambler's ruin: 0 is deterministic; 3 copies every fresh input bit. -/
def gamblerThird : Mealy (Fin 4) where
  next s b := if s = 0 then 0 else if s = 3 then 3
    else if s = 1 then (if b then 2 else 0) else (if b then 3 else 1)
  out s b := if s = 3 then b else false

theorem gambler_zero_deterministic : gamblerThird.infiniteRel 0 0 := by
  intro n
  induction n with
  | zero => trivial
  | succ n ih =>
    intro b c
    constructor
    · rfl
    · exact ih

theorem gambler_domain (s : Fin 4) : gamblerThird.infiniteRel s s ↔ s = 0 := by
  constructor
  · intro hs
    by_contra hn
    have hdiff : gamblerThird.outputWord s [false, false, false] ≠
        gamblerThird.outputWord s [true, true, true] := by
      fin_cases s <;> simp_all (config := { decide := true })
    exact hdiff ((gamblerThird.approx_iff_words 3 s s).mp (hs 3)
      [false, false, false] [true, true, true] rfl rfl)
  · rintro rfl
    exact gambler_zero_deterministic

theorem gambler_deterministicBit (s : Fin 4) :
    deterministicBit gamblerThird s = decide (s = 0) := by
  rw [Bool.eq_iff_iff, deterministicBit_spec, decide_eq_true_eq]
  exact gambler_domain s

theorem gambler_reaches (s : Fin 4) : Reaches gamblerThird s ↔ s ≠ 3 := by
  constructor
  · rintro ⟨u, hu⟩ rfl
    have hf : gamblerThird.finalState 3 u = 3 := by
      clear hu
      induction u with
      | nil => rfl
      | cons b u ih => exact ih
    have he := (gambler_domain _).mp hu
    rw [hf] at he
    exact (by decide : (3 : Fin 4) ≠ 0) he
  · intro hs
    have hword : gamblerThird.finalState s [false, false] = 0 := by
      fin_cases s <;> simp_all (config := { decide := true })
    exact ⟨[false, false], by rw [hword]; exact gambler_zero_deterministic⟩

theorem gambler_reachesBit (s : Fin 4) :
    reachesBit gamblerThird s = decide (s ≠ 3) := by
  rw [Bool.eq_iff_iff, reachesBit_spec, decide_eq_true_eq]
  exact gambler_reaches s

def gamblerHittingVector (s : Fin 4) : ℚ :=
  if s = 0 then 1 else if s = 1 then 2/3 else if s = 2 then 1/3 else 0

theorem gambler_vector_solves :
    (hittingMatrix gamblerThird).mulVec gamblerHittingVector = hittingRhs gamblerThird := by
  classical
  have hd (s : Fin 4) : gamblerThird.infiniteRel s s ↔ s = 0 := by
    rw [← deterministicBit_spec, gambler_deterministicBit, decide_eq_true_eq]
  have hr (s : Fin 4) : Reaches gamblerThird s ↔ s ≠ 3 := by
    rw [← reachesBit_spec, gambler_reachesBit, decide_eq_true_eq]
  rw [hittingMatrix_mulVec]
  funext s
  rw [hittingSystem_apply]
  simp only [hd, hr, not_not, hittingRhs, gambler_deterministicBit, decide_eq_true_eq]
  fin_cases s <;> norm_num (config := { decide := true }) [gamblerHittingVector, gamblerThird]

theorem gambler_solver_exact : solveHitting gamblerThird = gamblerHittingVector := by
  apply hittingSystem_injective (K := ℚ) gamblerThird
  rw [← hittingMatrix_mulVec, solveHitting_matrix_equation, ← gambler_vector_solves,
    hittingMatrix_mulVec]

/-- Non-dyadic infinite-horizon mass from a literal finite binary Mealy machine. -/
theorem gambler_atomic_mass_two_thirds :
    (P02A2.mass (law gamblerThird 1)).toReal = (2/3 : ℝ) := by
  rw [atomic_mass_eq_hitting_probability]
  change hittingReal gamblerThird 1 = _
  rw [← solveHitting_correct, gambler_solver_exact]
  norm_num [gamblerHittingVector]

/-- The verified executable program returns a genuinely non-dyadic defect. -/
theorem gambler_defect_one_third : P02A2.defect (law gamblerThird 1) = (1/3 : ℝ) := by
  rw [P02A2.defect, gambler_atomic_mass_two_thirds]
  norm_num

#eval solveHitting zeroMachine ()
#eval solveHitting copyMachine ()
#eval solveHitting splitMachine 0
#eval solveHitting gamblerThird 1
#eval solveDefect gamblerThird 1

end Orthemology.Frontier.MealyMeasure.Fixtures
