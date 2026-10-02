import RationalNormalForm
import FiniteOutputTable
import Pi3IndexReduction

open Set MeasureTheory
open scoped ENNReal NNReal
namespace AtomicMembership
open P02A2 P02A2.Q8Measure P02A2.FiniteOutputTable P02A2.ObserverCore P02.Codec

/-- An exact finite, executable rational comparison predicate. No probability
measure or infinite-output test is evaluated in this definition. -/
def finiteMassTest (e : ℕ) (q : ℚ≥0) (k n : ℕ) : Prop :=
  q ≤ rationalHeavyMass (indexTable e) k n

instance (e : ℕ) (q : ℚ≥0) (k n : ℕ) : Decidable (finiteMassTest e q k n) :=
  inferInstanceAs (Decidable (q ≤ rationalHeavyMass (indexTable e) k n))

theorem numeric_zero_defect_normal (e : ℕ) :
    e ∈ P02A2.Pi3IndexReduction.zeroDefectIndices ↔
      ∀ q : ℚ≥0, q < 1 → ∃ k, ∀ n, finiteMassTest e q k n := by
  exact defect_zero_rational_normal (outputLaw (evaluateIndex e)) (indexTable e)
    (indexTable_exact e)

theorem numeric_not_zero_defect_normal (e : ℕ) :
    e ∉ P02A2.Pi3IndexReduction.zeroDefectIndices ↔
      ∃ q : ℚ≥0, q < 1 ∧ ∀ k, ∃ n, ¬ finiteMassTest e q k n := by
  rw [numeric_zero_defect_normal]
  push_neg
  rfl

def rationalOfCode (i : ℕ) : ℚ≥0 := NNRat.divNat (Nat.unpair i).1 (Nat.unpair i).2

theorem rationalOfCode_surjective : Function.Surjective rationalOfCode := by
  intro q
  refine ⟨Nat.pair q.num q.den, ?_⟩
  simp [rationalOfCode, Nat.unpair_pair]

/-- The matrix contains only natural inputs, exact rational arithmetic, finite
word enumeration and the total decoded LOOP evaluator. -/
def membershipMatrix (e i k n : ℕ) : Prop :=
  rationalOfCode i < 1 → finiteMassTest e (rationalOfCode i) k n

instance (e i k n : ℕ) : Decidable (membershipMatrix e i k n) :=
  inferInstanceAs (Decidable (rationalOfCode i < 1 → finiteMassTest e (rationalOfCode i) k n))

theorem numeric_zero_defect_nat_normal (e : ℕ) :
    e ∈ P02A2.Pi3IndexReduction.zeroDefectIndices ↔
      ∀ i, ∃ k, ∀ n, membershipMatrix e i k n := by
  rw [numeric_zero_defect_normal]
  constructor
  · intro h i
    by_cases hi : rationalOfCode i < 1
    · obtain ⟨k,hk⟩ := h (rationalOfCode i) hi
      exact ⟨k,fun n _ => hk n⟩
    · exact ⟨0,fun _ hh => (hi hh).elim⟩
  · intro h q hq
    obtain ⟨i,hi⟩ := rationalOfCode_surjective q
    obtain ⟨k,hk⟩ := h i
    refine ⟨k,fun n => ?_⟩
    simpa only [hi] using hk n (by simpa only [hi] using hq)

theorem numeric_not_zero_defect_nat_normal (e : ℕ) :
    e ∉ P02A2.Pi3IndexReduction.zeroDefectIndices ↔
      ∃ i, ∀ k, ∃ n, ¬ membershipMatrix e i k n := by
  rw [numeric_zero_defect_nat_normal]
  push_neg
  rfl

end AtomicMembership
