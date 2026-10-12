import RestorationCountability

open MeasureTheory Set Filter
open scoped Topology
open Orthemology.Tranche2

namespace FreshProofAudit

/-- The eventual score-correctness event is measurable, so for probability
path laws its measure is a genuine probability, not merely an outer measure. -/
theorem eventual_binary_good_measurable
    {Ω : Type*} [MeasurableSpace Ω] (a : ℝ) (e : ℕ → ℝ)
    (q : ℕ → Ω → ℝ) (hq : ∀ n, Measurable (q n)) :
    MeasurableSet {ω | ∀ᶠ n in atTop, BinaryGood a (e n) (q n ω)} := by
  have heq : {ω | ∀ᶠ n in atTop, BinaryGood a (e n) (q n ω)} =
      ⋃ N : ℕ, ⋂ n : ℕ, ⋂ (_ : N ≤ n), {ω | BinaryGood a (e n) (q n ω)} := by
    ext ω
    simp only [Set.mem_setOf_eq, Set.mem_iUnion, Set.mem_iInter, eventually_atTop]
  rw [heq]
  apply MeasurableSet.iUnion
  intro N
  apply MeasurableSet.iInter
  intro n
  apply MeasurableSet.iInter
  intro _
  exact (measurable_binaryGood a (e n)).preimage (hq n)

#print axioms eventual_binary_good_measurable
#check eventual_binary_good_measurable
end FreshProofAudit
