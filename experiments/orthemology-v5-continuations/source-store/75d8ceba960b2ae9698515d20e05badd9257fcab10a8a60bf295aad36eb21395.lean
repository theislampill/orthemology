import EventualCausalRestoration

open MeasureTheory Set Filter
open scoped Topology

namespace Orthemology.Tranche2

lemma exact_parameter_repair (a e : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    BinaryGood a e (1/2+a*e) := by
  have h := mul_nonneg (mul_nonneg ha0 (sub_nonneg.mpr ha1)) (sq_nonneg e)
  constructor <;> dsimp <;> nlinarith

/-- A fixed guessed norm yields eventual exact repair iff the guess is right.
This supplies a literal sharpness construction for the countability result. -/
theorem guessed_parameter_eventual_success_iff (a guess : ℝ)
    (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (e : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0)) :
    (∀ᶠ n in atTop, BinaryGood a (e n) (1/2+guess*e n)) ↔ guess = a := by
  constructor
  · intro hg
    have h := eventual_binary_good_decodes a ha0 ha1 e
      (fun n => 1/2+guess*e n) he0 he1 he hg
    have hi : (fun n => ((1/2+guess*e n)-1/2)/e n) = fun _ => guess := by
      funext n
      field_simp [ne_of_gt (he0 n)]
    rw [hi] at h
    exact tendsto_nhds_unique tendsto_const_nhds h
  · intro h
    subst guess
    exact Eventually.of_forall fun n => exact_parameter_repair a (e n) ha0 ha1

namespace FiniteQuery

def blindAsk (_ : ℝ) : Bool := false
def blindNext (guess : ℝ) (_ : Bool) : ℝ := guess

lemma blind_run (oracle : Oracle) (guess : ℝ) (n : ℕ) :
    run blindAsk blindNext oracle guess n = (guess,0) := by
  induction n with
  | zero => rfl
  | succ n ih => simp [run,advance,blindAsk,blindNext,ih]

/-- The zero-query actual controller succeeds with exactly the prior atomic
mass at the correct norm, for arbitrary correlation with an unused oracle. -/
theorem blind_causal_success_mass
    (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (e : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0))
    (ρ : Measure ℝ) (η : Measure (ℝ × Oracle))
    (hseed : η.map Prod.fst = ρ) :
    η {z | ∀ᶠ n in atTop,
      blindAsk (run blindAsk blindNext z.2 z.1 n).1 = false ∧
      BinaryGood a (e n) (1/2+(run blindAsk blindNext z.2 z.1 n).1*e n)} = ρ {a} := by
  have hset : {z : ℝ × Oracle | ∀ᶠ n in atTop,
      blindAsk (run blindAsk blindNext z.2 z.1 n).1 = false ∧
      BinaryGood a (e n) (1/2+(run blindAsk blindNext z.2 z.1 n).1*e n)} =
      Prod.fst ⁻¹' ({a} : Set ℝ) := by
    ext z
    simp only [mem_setOf_eq,blind_run,blindAsk,Prod.fst,true_and,mem_preimage,mem_singleton_iff]
    exact guessed_parameter_eventual_success_iff a z.1 ha0 ha1 e he0 he1 he
  rw [hset,← Measure.map_apply measurable_fst (measurableSet_singleton a),hseed]

end FiniteQuery
end Orthemology.Tranche2

#print axioms Orthemology.Tranche2.guessed_parameter_eventual_success_iff
#print axioms Orthemology.Tranche2.FiniteQuery.blind_causal_success_mass
