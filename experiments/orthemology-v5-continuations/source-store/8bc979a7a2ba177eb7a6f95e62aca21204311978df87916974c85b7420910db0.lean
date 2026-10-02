import ResidualStability

open Set MeasureTheory Filter

namespace OrthemologyMeasure
variable {Ω ι : Type*} [MeasurableSpace Ω] [Countable ι]

noncomputable def membershipPattern (A : ι → Set Ω) (ω : Ω) : ι → Bool :=
  fun i => @decide (ω ∈ A i) (Classical.propDecidable _)

theorem membershipPattern_measurable {A : ι → Set Ω}
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

theorem membershipPattern_ae (μ : Measure Ω) {A B : ι → Set Ω}
    (h : ∀ i, A i =ᵐ[μ] B i) : membershipPattern A =ᵐ[μ] membershipPattern B := by
  classical
  filter_upwards [ae_all_iff.mpr h] with ω hω
  funext i
  change decide (A i ω) = decide (B i ω)
  rw [hω i]

/-- Countably many law-dependent positive-mass tests have one shared measurable
representative, giving a joint, not merely coordinatewise, stability bound. -/
theorem atomicPattern_eventTV_bound
    {α : ι → Type*} [∀ i, MeasurableSpace (α i)]
    [∀ i, MeasurableSingletonClass (α i)]
    (μ ν : Measure Ω) [IsFiniteMeasure μ] [IsFiniteMeasure ν]
    {f : ∀ i, Ω → α i} (hf : ∀ i, Measurable (f i)) :
    eventTV (μ.map (membershipPattern fun i => observedSupport μ (f i)))
      (ν.map (membershipPattern fun i => observedSupport ν (f i))) ≤ eventTV μ ν := by
  let C := membershipPattern fun i => commonObservedSupport μ ν (f i)
  have hμ : membershipPattern (fun i => observedSupport μ (f i)) =ᵐ[μ] C :=
    membershipPattern_ae μ fun i => observedSupport_ae_common_left μ ν (hf i)
  have hν : membershipPattern (fun i => observedSupport ν (f i)) =ᵐ[ν] C :=
    membershipPattern_ae ν fun i => observedSupport_ae_common_right μ ν (hf i)
  rw [Measure.map_congr hμ, Measure.map_congr hν]
  exact eventTV_map_le μ ν (membershipPattern_measurable fun i =>
    commonObservedSupport_measurable μ ν (hf i))

/-- Every measurable classification of the entire positive-mass pattern obeys
one joint total-variation bound, including first-loss and residual decoders. -/
theorem decodedAtomicPattern_eventTV_bound
    {α : ι → Type*} [∀ i, MeasurableSpace (α i)]
    [∀ i, MeasurableSingletonClass (α i)]
    {Z : Type*} [MeasurableSpace Z]
    (μ ν : Measure Ω) [IsFiniteMeasure μ] [IsFiniteMeasure ν]
    {f : ∀ i, Ω → α i} (hf : ∀ i, Measurable (f i))
    {decode : (ι → Bool) → Z} (hd : Measurable decode) :
    eventTV ((μ.map (membershipPattern fun i => observedSupport μ (f i))).map decode)
      ((ν.map (membershipPattern fun i => observedSupport ν (f i))).map decode)
      ≤ eventTV μ ν := by
  exact (eventTV_map_le _ _ hd).trans (atomicPattern_eventTV_bound μ ν hf)

end OrthemologyMeasure
#print axioms OrthemologyMeasure.atomicPattern_eventTV_bound

#print axioms OrthemologyMeasure.decodedAtomicPattern_eventTV_bound
