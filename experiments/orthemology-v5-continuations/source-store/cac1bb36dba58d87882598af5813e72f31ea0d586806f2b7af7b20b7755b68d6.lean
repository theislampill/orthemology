import Pi3Program
import CodecIndexPrimrec

/-! An effective numeric-code reduction for each fixed jointly PR normal-form
matrix. This theorem gives the reduction witness and exact quantifiers. It
neither proves an index-set membership upper bound nor supplies a universal
PR evaluator, and it makes no canonical adoption or novelty claim. -/
namespace P02A2.Pi3IndexReduction
open P02A2.ObserverCore P02A2.PRProgram P02A2.Q8Measure P02.Codec P02A2.Pi3Program

noncomputable def zeroDefectIndices : Set ℕ :=
  {e | defect (fairCantor.map (output (evaluateIndex e))) = 0}

variable (R : ℕ → ℕ → ℕ → ℕ → Prop) [∀ a i, DecidableRel (R a i)]

/-- Every fixed jointly primitive-recursive forall-exists-forall matrix has a
primitive-recursive many-one map into actual numeric P02-L1 zero-defect indices. -/
theorem exists_primrec_zero_defect_reduction
    (hR : PrimrecRel (fun p : (ℕ × ℕ) × ℕ => R p.1.1 p.1.2 p.2)) :
    ∃ f : ℕ → ℕ, Primrec f ∧ ∀ a,
      f a ∈ zeroDefectIndices ↔ ∀ i, ∃ s, ∀ t, R a i s t := by
  obtain ⟨p,hp⟩ := exists_fixed_program R hR
  exact ⟨parameterIndex p, parameterIndex_primrec p,
    fun a => numeric_zero_defect_iff R p hp a⟩

/-- The same concrete map sends failure of that Pi3 normal form to strictly
positive defect. It does not conflate full atomicity with atomlessness. -/
theorem exists_primrec_positive_defect_reduction
    (hR : PrimrecRel (fun p : (ℕ × ℕ) × ℕ => R p.1.1 p.1.2 p.2)) :
    ∃ f : ℕ → ℕ, Primrec f ∧ ∀ a,
      0 < defect (fairCantor.map (output (evaluateIndex (f a)))) ↔
        ∃ i, ∀ s, ∃ t, ¬ R a i s t := by
  obtain ⟨p,hp⟩ := exists_fixed_program R hR
  refine ⟨parameterIndex p, parameterIndex_primrec p, fun a => ?_⟩
  rw [numeric_observer_eq R p hp]
  exact OrthemologyTagged.pi3_positive_defect_iff R a

end P02A2.Pi3IndexReduction
