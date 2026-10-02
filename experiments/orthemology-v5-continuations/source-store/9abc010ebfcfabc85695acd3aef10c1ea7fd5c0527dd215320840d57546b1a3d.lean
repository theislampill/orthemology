import ProductObservationLaw

noncomputable section
open MeasureTheory ProbabilityTheory Set Finset
open scoped BigOperators

namespace Orthemology.Tranche2.PolicyEmbedding
universe u
variable {I J Ω Ξ : Type*} {E F : Type u} [MeasurableSpace Ω] [MeasurableSpace Ξ]
    [MeasurableSpace E] [MeasurableSpace F]

abbrev FamilyValue (E F : Type u) : I ⊕ J → Type u := Sum.elim (fun _ => E) (fun _ => F)
instance familyValueMeasurable (k : I ⊕ J) : MeasurableSpace (FamilyValue E F k) := by
  cases k with
  | inl _ => exact (inferInstance : MeasurableSpace E)
  | inr _ => exact (inferInstance : MeasurableSpace F)

def productFamily (X : I → Ω → E) (Y : J → Ξ → F) :
    (k : I ⊕ J) → Ω × Ξ → FamilyValue E F k
  | Sum.inl i, ω => X i ω.1
  | Sum.inr j, ω => Y j ω.2

/-- Families independent in separate factors form one independent tagged
family under the actual product measure. -/
theorem independent_product_families (μ : Measure Ω) (ν : Measure Ξ)
    [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    (X : I → Ω → E) (Y : J → Ξ → F) (hX : iIndepFun X μ) (hY : iIndepFun Y ν) :
    iIndepFun (productFamily X Y) (μ.prod ν) := by
  classical
  rw [iIndepFun_iff_measure_inter_preimage_eq_mul]
  intro S sets hs
  have he : (⋂ k ∈ S, productFamily X Y k ⁻¹' sets k) =
      (⋂ i ∈ S.toLeft, X i ⁻¹' sets (Sum.inl i)) ×ˢ
      (⋂ j ∈ S.toRight, Y j ⁻¹' sets (Sum.inr j)) := by
    ext ω
    simp only [Set.mem_iInter,Set.mem_preimage,Set.mem_prod,Finset.mem_toLeft,Finset.mem_toRight]
    constructor
    · intro h
      exact ⟨fun i hi => h (Sum.inl i) hi, fun j hj => h (Sum.inr j) hj⟩
    · rintro ⟨hx,hy⟩ k hk
      cases k with
      | inl i => exact hx i hk
      | inr j => exact hy j hk
  rw [he,Measure.prod_prod,
    hX.measure_inter_preimage_eq_mul _ (fun i hi => hs _ (Finset.mem_toLeft.mp hi)),
    hY.measure_inter_preimage_eq_mul _ (fun j hj => hs _ (Finset.mem_toRight.mp hj)),
    Finset.prod_sum_eq_prod_toLeft_mul_prod_toRight]
  congr 1
  · apply Finset.prod_congr rfl
    intro i _
    have hp : productFamily X Y (Sum.inl i) ⁻¹' sets (Sum.inl i) =
        (X i ⁻¹' sets (Sum.inl i)) ×ˢ Set.univ := by ext ω; simp [productFamily]
    rw [hp,Measure.prod_prod,measure_univ,mul_one]
  · apply Finset.prod_congr rfl
    intro j _
    have hp : productFamily X Y (Sum.inr j) ⁻¹' sets (Sum.inr j) =
        Set.univ ×ˢ (Y j ⁻¹' sets (Sum.inr j)) := by ext ω; simp [productFamily]
    rw [hp,Measure.prod_prod,measure_univ,one_mul]

end Orthemology.Tranche2.PolicyEmbedding
