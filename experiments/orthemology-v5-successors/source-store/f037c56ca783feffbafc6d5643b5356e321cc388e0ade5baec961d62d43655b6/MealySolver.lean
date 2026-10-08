import MealyRational
import Mathlib.LinearAlgebra.Determinant

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators

variable {S : Type*} [Fintype S] [DecidableEq S]

/-- One executable backward-reachability expansion. -/
def reachStep (M : Mealy S) (A : Finset S) : Finset S :=
  Finset.univ.filter (fun q => q ∈ A ∨ M.next q false ∈ A ∨ M.next q true ∈ A)

/-- Executable bounded backward reachability from the computed domain D. -/
def reachSet (M : Mealy S) : ℕ → Finset S
  | 0 => Finset.univ.filter (fun q => deterministicBit M q = true)
  | n+1 => reachStep M (reachSet M n)

theorem mem_reachSet_succ (M : Mealy S) (q : S) (n : ℕ) :
    q ∈ reachSet M (n+1) ↔ q ∈ reachSet M n ∨
      M.next q false ∈ reachSet M n ∨ M.next q true ∈ reachSet M n := by
  simp [reachSet, reachStep]

theorem reachSet_mono (M : Mealy S) : Monotone (reachSet M) := by
  apply monotone_nat_of_le_succ
  intro n q hq
  exact (mem_reachSet_succ M q n).mpr (Or.inl hq)

/-- At most m expansions suffice: finite cardinality and deterministic recurrence
    derive permanent stationarity, rather than assume a reachability oracle. -/
theorem reachSet_stable (M : Mealy S) (n : ℕ) (hn : Fintype.card S ≤ n) :
    reachSet M n = reachSet M (Fintype.card S) := by
  have hc : (reachSet M n).card = (reachSet M (Fintype.card S)).card := by
    apply Nat.stabilises_of_monotone (f := fun n => (reachSet M n).card) (b := Fintype.card S)
    · exact fun a b hab => Finset.card_le_card (reachSet_mono M hab)
    · intro k
      exact Finset.card_le_univ _
    · intro k hk
      have he : reachSet M k = reachSet M (k+1) :=
        Finset.eq_of_subset_of_card_le (reachSet_mono M (Nat.le_succ k)) hk.ge
      have he' : reachSet M (k+1) = reachSet M (k+2) := congrArg (reachStep M) he
      exact congrArg Finset.card he'
    · exact hn
  exact (Finset.eq_of_subset_of_card_le (reachSet_mono M hn) hc.le).symm

theorem reaching_word_mem [Nonempty S] (M : Mealy S) (s : S) (u : List Bool)
    (hu : M.infiniteRel (M.finalState s u) (M.finalState s u)) :
    s ∈ reachSet M u.length := by
  induction u generalizing s with
  | nil => simpa [reachSet, deterministicBit_spec] using hu
  | cons b u ih =>
    apply (mem_reachSet_succ M s u.length).mpr
    have h := ih (M.next s b) hu
    cases b
    · exact Or.inr (Or.inl h)
    · exact Or.inr (Or.inr h)

theorem reaches_of_mem_reachSet [Nonempty S] (M : Mealy S) (s : S) (n : ℕ)
    (hs : s ∈ reachSet M n) : Reaches M s := by
  induction n generalizing s with
  | zero =>
    exact ⟨[], by simpa [reachSet, deterministicBit_spec] using hs⟩
  | succ n ih =>
    rcases (mem_reachSet_succ M s n).mp hs with h | h | h
    · exact ih s h
    · obtain ⟨u, hu⟩ := ih (M.next s false) h
      exact ⟨false :: u, hu⟩
    · obtain ⟨u, hu⟩ := ih (M.next s true) h
      exact ⟨true :: u, hu⟩

theorem reaches_iff_mem_reachSet [Nonempty S] (M : Mealy S) (s : S) :
    Reaches M s ↔ s ∈ reachSet M (Fintype.card S) := by
  constructor
  · rintro ⟨u, hu⟩
    have h := reaching_word_mem M s u hu
    by_cases hn : u.length ≤ Fintype.card S
    · exact reachSet_mono M hn h
    · simpa only [reachSet_stable M u.length (by omega)] using h
  · exact reaches_of_mem_reachSet M s _

/-- A terminating decision procedure for unbounded finite-word reachability. -/
def reachesBit (M : Mealy S) (s : S) : Bool := decide (s ∈ reachSet M (Fintype.card S))

theorem reachesBit_spec [Nonempty S] (M : Mealy S) (s : S) :
    reachesBit M s = true ↔ Reaches M s := by
  simp only [reachesBit, decide_eq_true_eq, reaches_iff_mem_reachSet]


/-- Explicit rational matrix of the computed reachability system. -/
def hittingMatrix (M : Mealy S) : Matrix S S ℚ := fun q r =>
  if deterministicBit M q = true ∨ reachesBit M q = false then
    if q = r then 1 else 0
  else
    2 * (if q = r then 1 else 0) - (if M.next q false = r then 1 else 0) -
      (if M.next q true = r then 1 else 0)

def hittingRhs (M : Mealy S) : S → ℚ := fun q => if deterministicBit M q then 1 else 0

/-- Literal graph-to-matrix correspondence, including the zero boundary on non-reaching states. -/
theorem hittingMatrix_mulVec [Nonempty S] (M : Mealy S) (f : S → ℚ) :
    (hittingMatrix M).mulVec f = hittingSystem M f := by
  classical
  funext q
  rw [hittingSystem_apply]
  have hd := deterministicBit_spec M q
  have hr := reachesBit_spec M q
  have hr0 : reachesBit M q = false ↔ ¬ Reaches M q := by
    rw [← hr]
    exact Bool.eq_false_iff
  simp only [hittingMatrix, Matrix.mulVec, dotProduct, hd, hr0]
  split_ifs <;> simp [ite_mul, sub_mul, Finset.sum_sub_distrib, Finset.mul_sum, mul_assoc]

theorem hittingMatrix_det_ne_zero [Nonempty S] (M : Mealy S) : (hittingMatrix M).det ≠ 0 := by
  have hi : Function.Injective (Matrix.toLin' (hittingMatrix M)) := by
    intro f g h
    apply hittingSystem_injective (K := ℚ) M
    simpa only [Matrix.toLin'_apply, hittingMatrix_mulVec] using h
  have hk := LinearMap.ker_eq_bot.mpr hi
  intro hz
  have h := LinearMap.bot_lt_ker_of_det_eq_zero
    (f := Matrix.toLin' (hittingMatrix M)) (by simpa only [LinearMap.det_toLin'] using hz)
  rw [hk] at h
  exact lt_irrefl _ h

/-- Explicit terminating exact solver, using finite reachability and Cramer's determinants.
    This definition is executable; it does not use a choice-based matrix inverse. -/
def solveHitting (M : Mealy S) (s : S) : ℚ :=
  (hittingMatrix M).cramer (hittingRhs M) s / (hittingMatrix M).det

theorem solveHitting_matrix_equation [Nonempty S] (M : Mealy S) :
    (hittingMatrix M).mulVec (solveHitting M) = hittingRhs M := by
  have he : solveHitting M = (hittingMatrix M).det⁻¹ • (hittingMatrix M).cramer (hittingRhs M) := by
    funext s
    simp [solveHitting, Pi.smul_apply, smul_eq_mul, div_eq_mul_inv, mul_comm]
  rw [he, Matrix.mulVec_smul, Matrix.mulVec_cramer, smul_smul,
    inv_mul_cancel₀ (hittingMatrix_det_ne_zero M), one_smul]

/-- The executable rational solver equals the actual fair infinite-input hitting probability. -/
theorem solveHitting_correct [Nonempty S] (M : Mealy S) (s : S) :
    (solveHitting M s : ℝ) = hittingReal M s := by
  classical
  have hf : ∀ q, hittingSystem M (solveHitting M) q =
      if M.infiniteRel q q then 1 else 0 := by
    intro q
    have h := congrFun (solveHitting_matrix_equation M) q
    rw [hittingMatrix_mulVec] at h
    simpa only [hittingRhs, deterministicBit_spec] using h
  have hcast : hittingSystem M (fun q => (solveHitting M q : ℝ)) =
      hittingSystem M (hittingReal M) := by
    funext q
    rw [hittingReal_system]
    have hq := hf q
    rw [hittingSystem_apply] at hq ⊢
    by_cases hd : M.infiniteRel q q
    · simp only [hd, true_or, ↓reduceIte] at hq ⊢
      exact_mod_cast hq
    · by_cases hr : Reaches M q
      · simp only [hd, hr, not_true_eq_false, or_self, ↓reduceIte] at hq ⊢
        exact_mod_cast hq
      · simp only [hd, hr, not_false_eq_true, or_true, ↓reduceIte] at hq ⊢
        exact_mod_cast hq
  exact congrFun (hittingSystem_injective (K := ℝ) M hcast) s

def solveDefect (M : Mealy S) (s : S) : ℚ := 1 - solveHitting M s

/-- Exact computational content for the nonatomic defect, with the measure bridge included. -/
theorem solveDefect_correct [Nonempty S] (M : Mealy S) (s : S) :
    (solveDefect M s : ℝ) = P02A2.defect (law M s) := by
  simp only [solveDefect, Rat.cast_sub, Rat.cast_one, solveHitting_correct, P02A2.defect,
    atomic_mass_eq_hitting_probability, hittingReal]

end Orthemology.Frontier.MealyMeasure
