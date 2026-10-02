import AtomicPattern
import Mathlib.MeasureTheory.Constructions.Projective

open Set MeasureTheory Filter
namespace OrthemologyMeasure
variable {Ω ι : Type*} [MeasurableSpace Ω]

/-- Equality of every coordinate almost everywhere suffices for equality of
product-space laws, without simultaneous equality outside one null set. -/
theorem product_map_congr_coordinate_ae
    (μ : Measure Ω) [IsFiniteMeasure μ]
    {F G : Ω → (ι → Bool)} (hF : Measurable F) (hG : Measurable G)
    (h : ∀ i, (fun ω => F ω i) =ᵐ[μ] (fun ω => G ω i)) : μ.map F = μ.map G := by
  apply ext_of_generate_finite (measurableCylinders (fun _ : ι => Bool))
    generateFrom_measurableCylinders.symm isPiSystem_measurableCylinders
  · intro s hs
    obtain ⟨I, S, hS, rfl⟩ := (mem_measurableCylinders _).mp hs
    rw [Measure.map_apply hF hS.cylinder, Measure.map_apply hG hS.cylinder]
    apply measure_congr
    filter_upwards [ae_all_iff.mpr (fun i : I => h i.val)] with ω hω
    have he : I.restrict (F ω) = I.restrict (G ω) := by
      funext i
      exact hω i
    change (I.restrict (F ω) ∈ S) = (I.restrict (G ω) ∈ S)
    rw [he]
  · rw [Measure.map_apply hF MeasurableSet.univ, Measure.map_apply hG MeasurableSet.univ]
    simp

theorem arbitraryPattern_measurable {A : ι → Set Ω}
    (hA : ∀ i, MeasurableSet (A i)) : Measurable (membershipPattern A) := by
  classical
  apply measurable_pi_lambda
  intro i
  apply measurable_to_bool
  have he : (fun ω => membershipPattern A ω i) ⁻¹' {true} = A i := by
    ext ω
    simp [membershipPattern]
  rw [he]
  exact hA i

/-- The countability hypothesis can be removed for the product-sigma-algebra
law, although it cannot be removed from simultaneous almost-everywhere equality. -/
theorem arbitraryAtomicPattern_eventTV_bound
    {α : ι → Type*} [∀ i, MeasurableSpace (α i)]
    [∀ i, MeasurableSingletonClass (α i)]
    (μ ν : Measure Ω) [IsFiniteMeasure μ] [IsFiniteMeasure ν]
    {f : ∀ i, Ω → α i} (hf : ∀ i, Measurable (f i)) :
    eventTV (μ.map (membershipPattern fun i => observedSupport μ (f i)))
      (ν.map (membershipPattern fun i => observedSupport ν (f i))) ≤ eventTV μ ν := by
  classical
  let C := membershipPattern fun i => commonObservedSupport μ ν (f i)
  have hC : Measurable C := arbitraryPattern_measurable fun i =>
    commonObservedSupport_measurable μ ν (hf i)
  have hμ := product_map_congr_coordinate_ae μ
    (arbitraryPattern_measurable fun i => observedSupport_measurable μ (hf i)) hC
    (fun i => ?_)
  have hν := product_map_congr_coordinate_ae ν
    (arbitraryPattern_measurable fun i => observedSupport_measurable ν (hf i)) hC
    (fun i => ?_)
  rw [hμ, hν]
  exact eventTV_map_le μ ν hC
  all_goals
    first
    | filter_upwards [observedSupport_ae_common_left μ ν (hf i)] with ω hω
      change @decide (observedSupport μ (f i) ω) _ =
        @decide (commonObservedSupport μ ν (f i) ω) _
      simp only [hω]
    | filter_upwards [observedSupport_ae_common_right μ ν (hf i)] with ω hω
      change @decide (observedSupport ν (f i) ω) _ =
        @decide (commonObservedSupport μ ν (f i) ω) _
      simp only [hω]

end OrthemologyMeasure
#print axioms OrthemologyMeasure.product_map_congr_coordinate_ae
#print axioms OrthemologyMeasure.arbitraryAtomicPattern_eventTV_bound
