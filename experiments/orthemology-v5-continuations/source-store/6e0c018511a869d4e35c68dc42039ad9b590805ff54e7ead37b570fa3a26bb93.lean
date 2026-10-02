import AtomicPattern

open Set MeasureTheory Filter
open scoped NNReal ENNReal
namespace OrthemologyMeasure
variable {Ω ι : Type*} [MeasurableSpace Ω] [Countable ι]
variable {α : ι → Type*} [∀ i, MeasurableSpace (α i)]
  [∀ i, MeasurableSingletonClass (α i)]

/-- The law-specific atomic classification defines an additive positive
measure-valued operator, despite lacking a universal pointwise classifier. -/
noncomputable def atomicPatternLaw (μ : Measure Ω) (f : ∀ i, Ω → α i) : Measure (ι → Bool) :=
  μ.map (membershipPattern fun i => observedSupport μ (f i))

theorem observedSupport_add {X : Type*} [MeasurableSpace X]
    (μ ν : Measure Ω) {f : Ω → X} (hf : Measurable f) :
    observedSupport (μ + ν) f = commonObservedSupport μ ν f := by
  ext ω
  simp only [observedSupport, commonObservedSupport, mem_preimage, mem_union,
    P02A2.positive, mem_setOf_eq, Measure.map_add μ ν hf, Measure.add_apply]
  exact add_pos_iff

theorem atomicPatternLaw_add
    (μ ν : Measure Ω) [IsFiniteMeasure μ] [IsFiniteMeasure ν]
    {f : ∀ i, Ω → α i} (hf : ∀ i, Measurable (f i)) :
    atomicPatternLaw (μ + ν) f = atomicPatternLaw μ f + atomicPatternLaw ν f := by
  let C := membershipPattern fun i => commonObservedSupport μ ν (f i)
  have hC : Measurable C := membershipPattern_measurable fun i =>
    commonObservedSupport_measurable μ ν (hf i)
  have hadd : membershipPattern (fun i => observedSupport (μ + ν) (f i)) = C := by
    exact congrArg membershipPattern (funext fun i => observedSupport_add μ ν (hf i))
  have hμ : membershipPattern (fun i => observedSupport μ (f i)) =ᵐ[μ] C :=
    membershipPattern_ae μ fun i => observedSupport_ae_common_left μ ν (hf i)
  have hν : membershipPattern (fun i => observedSupport ν (f i)) =ᵐ[ν] C :=
    membershipPattern_ae ν fun i => observedSupport_ae_common_right μ ν (hf i)
  unfold atomicPatternLaw
  rw [hadd, Measure.map_add μ ν hC, Measure.map_congr hμ, Measure.map_congr hν]

theorem observedSupport_smul {X : Type*} [MeasurableSpace X]
    (μ : Measure Ω) (r : ℝ≥0) (hr : r ≠ 0) (f : Ω → X) :
    observedSupport (r • μ) f = observedSupport μ f := by
  ext ω
  change (0 < (r • μ).map f {f ω}) ↔ 0 < μ.map f {f ω}
  rw [Measure.map_smul, Measure.coe_nnreal_smul_apply]
  have hrp : (0 : ℝ≥0∞) < r := by exact_mod_cast (pos_iff_ne_zero.mpr hr)
  simpa only [hrp, true_and] using
    (ENNReal.mul_pos_iff : 0 < (r : ℝ≥0∞) * μ.map f {f ω} ↔ 0 < (r : ℝ≥0∞) ∧ 0 < μ.map f {f ω})

theorem atomicPatternLaw_smul (μ : Measure Ω) (r : ℝ≥0)
    (f : ∀ i, Ω → α i) :
    atomicPatternLaw (r • μ) f = r • atomicPatternLaw μ f := by
  by_cases hr : r = 0
  · simp [hr, atomicPatternLaw]
  · have he : membershipPattern (fun i => observedSupport (r • μ) (f i)) =
        membershipPattern (fun i => observedSupport μ (f i)) :=
      congrArg membershipPattern (funext fun i => observedSupport_smul μ r hr (f i))
    unfold atomicPatternLaw
    rw [he, Measure.map_smul]

end OrthemologyMeasure
#print axioms OrthemologyMeasure.atomicPatternLaw_add

#print axioms OrthemologyMeasure.atomicPatternLaw_smul
