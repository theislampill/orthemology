import MealyMeasure
import Mathlib.Algebra.BigOperators.Fin

/-! Literal finite constraints on consecutive fair-bit blocks. No input-law premise. -/
namespace Orthemology.RationalLaw
open MeasureTheory Set
open scoped ENNReal BigOperators
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.Q8Measure (fairCantor)

variable {I : Type*} [DecidableEq I]

def words : List (Finset I) → Finset (List I)
  | [] => {[]}
  | A :: As => (A ×ˢ words As).image (fun p => p.1 :: p.2)

theorem mem_words {As : List (Finset I)} {w : List I} :
    w ∈ words As ↔ List.Forall₂ (fun A a => a ∈ A) As w := by
  induction As generalizing w with
  | nil => simp [words]
  | cons A As ih =>
      cases w with
      | nil => simp [words]
      | cons a w => simp [words, ih]

theorem words_length {As : List (Finset I)} {w : List I} (h : w ∈ words As) :
    w.length = As.length := (mem_words.mp h).length_eq.symm

theorem card_words (As : List (Finset I)) :
    (words As).card = (As.map Finset.card).prod := by
  induction As with
  | nil => simp [words]
  | cons A As ih =>
      rw [words, Finset.card_image_of_injective]
      · simp [Finset.card_product, ih]
      · intro a b h
        exact Prod.ext (List.cons.inj h).1 (List.cons.inj h).2

/-- Block j reads the actual consecutive bits at jL,...,jL+L-1. -/
def block (L j : ℕ) (x : Cantor) : Mealy.Block L := fun i => x (j*L+i)

def constraintEvent {L : ℕ} (As : List (Finset (Mealy.Block L))) : Set Cantor :=
  {x | ∀ (i : ℕ) (hi : i < As.length), block L i x ∈ As[i]}

theorem constraintEvent_eq {L : ℕ} (As : List (Finset (Mealy.Block L))) :
    constraintEvent As = {x : Cantor | blocks L As.length x ∈ words As} := by
  ext x
  simp only [constraintEvent, mem_setOf_eq, mem_words, List.forall₂_iff_get,
    blocks_length, true_and]
  constructor
  · intro h i hi hj
    simpa [blocks, block] using h i hi
  · intro h i hi
    simpa [blocks, block] using h i hi (by simpa [blocks_length] using hi)

theorem measurableSet_constraintEvent {L : ℕ} (As : List (Finset (Mealy.Block L))) :
    MeasurableSet (constraintEvent As) := by
  rw [constraintEvent_eq, block_event_eq_union _ (fun _ h => words_length h)]
  exact MeasurableSet.biUnion (Set.to_countable _) (fun _ _ => measurableSet_cylinder _)

/-- The mass is derived from actual finite cylinders in the original fair tape. -/
theorem measure_constraintEvent {L : ℕ} (As : List (Finset (Mealy.Block L))) :
    fairCantor (constraintEvent As) =
      ((As.map fun A => (A.card : ℝ≥0∞)).prod) * (1/2 : ℝ≥0∞)^(As.length*L) := by
  rw [constraintEvent_eq, measure_block_event _ (fun _ h => words_length h), card_words]
  congr 1
  induction As with
  | nil => simp
  | cons A As ih => simp [ih]

/-- Equivalent normalized form: multiply each literal block's accepted fraction. -/
theorem measure_constraintEvent_product {L : ℕ} (As : List (Finset (Mealy.Block L))) :
    fairCantor (constraintEvent As) =
      (As.map fun A => (A.card : ℝ≥0∞) * (1/2 : ℝ≥0∞)^L).prod := by
  rw [measure_constraintEvent]
  induction As with
  | nil => simp
  | cons A As ih =>
      simp only [List.map_cons, List.prod_cons, List.length_cons, Nat.add_mul, pow_add]
      rw [← ih]
      ac_rfl


theorem block_shift (L n i : ℕ) (x : Cantor) :
    block L i (shift (n*L) x) = block L (n+i) x := by
  funext j
  simp [block, shift, Nat.add_mul, Nat.add_assoc]

theorem constraintEvent_append {L : ℕ} (As Bs : List (Finset (Mealy.Block L))) (x : Cantor) :
    x ∈ constraintEvent (As ++ Bs) ↔
      x ∈ constraintEvent As ∧ shift (As.length*L) x ∈ constraintEvent Bs := by
  simp only [constraintEvent, Set.mem_setOf_eq]
  constructor
  · intro h
    constructor
    · intro i hi
      have hh := h i (by simp; omega)
      rw [List.getElem_append_left hi] at hh
      exact hh
    · intro i hi
      have hh := h (As.length+i) (by simp; omega)
      rw [List.getElem_append_right (by omega)] at hh
      simpa only [block_shift, Nat.add_sub_cancel_left] using hh
  · rintro ⟨hA,hB⟩ i hi
    by_cases hia : i < As.length
    · rw [List.getElem_append_left hia]
      exact hA i hia
    · have hib : i-As.length < Bs.length := by simp only [List.length_append] at hi; omega
      rw [List.getElem_append_right (by omega)]
      have hh := hB (i-As.length) hib
      have he : As.length+(i-As.length)=i := by omega
      simpa only [block_shift, he] using hh

end Orthemology.RationalLaw
