import SeparatingProjection

noncomputable section

open scoped BigOperators

namespace FiniteMoment.Checks

variable {K : Type*} [Field K]

/-- Empty support is admitted in every finite dimension. -/
theorem empty_support [Infinite K] (d : ℕ) (x : Fin 0 → Fin d → K) :
    ∃ v : Fin d → K, Function.Injective (fun i => projection v (x i)) :=
  exists_separating_projection x (Function.injective_of_subsingleton x)

/-- A single support point is admitted, including in dimension zero. -/
theorem singleton_support [Infinite K] (d : ℕ) (x : Fin 1 → Fin d → K) :
    ∃ v : Fin d → K, ∀ w : Fin 1 → K,
      recover (fun i => projection v (x i))
        (record (fun i => projection v (x i)) w) = w := by
  obtain ⟨v, _, hv⟩ := exists_projection_recovery x (Function.injective_of_subsingleton x)
  exact ⟨v, hv⟩

omit [Field K] in
/-- An injectively enumerated zero-dimensional support necessarily has at most
one point, so the general theorem has no impossible nontrivial zero-dimensional case. -/
theorem zero_dimension_card_le_one {N : ℕ} (x : Fin N → Fin 0 → K)
    (hx : Function.Injective x) : N ≤ 1 := by
  letI : Subsingleton (Fin N) := ⟨fun i j => hx (Subsingleton.elim _ _)⟩
  simpa using (Fintype.card_le_one_iff_subsingleton.mpr (inferInstance : Subsingleton (Fin N)))

/-- Empty, zero-dimensional support also has valid exact recovery. -/
theorem empty_zero_dimension [Infinite K] (x : Fin 0 → Fin 0 → K) :
    ∃ v : Fin 0 → K, ∀ w : Fin 0 → K,
      recover (fun i => projection v (x i))
        (record (fun i => projection v (x i)) w) = w := by
  obtain ⟨v, _, hv⟩ := exists_projection_recovery x (Function.injective_of_subsingleton x)
  exact ⟨v, hv⟩

/-- Over every finite field, the entire two-dimensional space is a finite
set of distinct vectors with no injective scalar projection. -/
theorem finite_field_counterexample [Fintype K] :
    ∃ (N : ℕ) (x : Fin N → Fin 2 → K),
      Function.Injective x ∧
      ∀ v : Fin 2 → K, ¬ Function.Injective (fun i => projection v (x i)) := by
  classical
  let e := Fintype.equivFin (Fin 2 → K)
  refine ⟨Fintype.card (Fin 2 → K), e.symm, e.symm.injective, ?_⟩
  intro v hv
  have hc := Fintype.card_le_of_injective (fun i => projection v (e.symm i)) hv
  have hcard : Fintype.card K * Fintype.card K ≤ Fintype.card K := by
    simpa only [Fintype.card_fin, Fintype.card_fun, pow_two] using hc
  exact (not_lt_of_ge hcard)
    (lt_mul_of_one_lt_right (Fintype.card_pos) (Fintype.one_lt_card))

end FiniteMoment.Checks
