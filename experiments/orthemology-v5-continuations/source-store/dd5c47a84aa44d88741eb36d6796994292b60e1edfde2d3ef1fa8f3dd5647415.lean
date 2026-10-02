import FinitePrefixBoundary

open Set MeasureTheory
open scoped ENNReal
namespace OrthemologyMeasure
open P02A2 P02A2.Q8Measure

noncomputable def atomicBit {X : Type*} [MeasurableSpace X]
    (μ : Measure X) (x : X) : Bool :=
  @decide (x ∈ positive μ) (Classical.propDecidable _)

theorem atomicBit_measurable {X : Type*} [MeasurableSpace X] [MeasurableSingletonClass X]
    (μ : Measure X) [IsFiniteMeasure μ] : Measurable (atomicBit μ) := by
  apply measurable_to_bool
  have he : atomicBit μ ⁻¹' {true} = positive μ := by
    ext x
    simp [atomicBit]
  rw [he]
  exact positive_measurable μ

theorem atomicBit_dirac_self {X : Type*} [MeasurableSpace X] (x : X) :
    atomicBit (Measure.dirac x) x = true := by
  simp [atomicBit, positive, Measure.dirac_apply_of_mem]

theorem atomicBit_fair_zero : atomicBit fairCantor = fun _ => false := by
  classical
  funext x
  simp only [atomicBit, positive, Set.mem_setOf_eq, fairCantor_singleton_zero,
    lt_self_iff_false, decide_false]

/-- Atomic classification of a law cannot be replaced, uniformly across laws,
by one measurable Boolean function of a single realised source point. -/
theorem no_universal_atomic_classifier :
    ¬ ∃ g : Cantor → Bool, Measurable g ∧
      ∀ μ : Measure Cantor, IsProbabilityMeasure μ → μ.map g = μ.map (atomicBit μ) := by
  rintro ⟨g, hg, h⟩
  have hgtrue : g = fun _ => true := by
    funext x
    have hx := h (Measure.dirac x) inferInstance
    rw [Measure.map_dirac hg, Measure.map_dirac (atomicBit_measurable _), atomicBit_dirac_self] at hx
    exact injective_dirac hx
  have hf := h fairCantor inferInstance
  rw [hgtrue, atomicBit_fair_zero, Measure.map_const, Measure.map_const] at hf
  simp only [measure_univ, one_smul] at hf
  have he : (true : Bool) = false := injective_dirac hf
  cases he

/-- Randomising a law-blind single-point test does not repair the obstruction:
its measurable success probability would have to integrate to atomic mass for
every input law, which is impossible even for Dirac laws and fair Cantor. -/
theorem no_universal_randomised_atomic_test :
    ¬ ∃ g : Cantor → ℝ≥0∞, Measurable g ∧
      ∀ μ : Measure Cantor, IsProbabilityMeasure μ → (∫⁻ x, g x ∂μ) = mass μ := by
  rintro ⟨g, hg, h⟩
  have hg1 : g = fun _ => 1 := by
    funext x
    have hx := h (Measure.dirac x) inferInstance
    rw [lintegral_dirac] at hx
    have hm : mass (Measure.dirac x) = 1 :=
      countable_carrier_mass_one (Measure.dirac x) (Set.countable_singleton x)
        (by simp) (measure_univ)
    exact hx.trans hm
  have hf := h fairCantor inferInstance
  have hp : positive fairCantor = ∅ := by
    ext x
    change (0 < fairCantor {x}) ↔ False
    rw [fairCantor_singleton_zero]
    simp
  rw [hg1] at hf
  simp [mass, hp] at hf

end OrthemologyMeasure
#print axioms OrthemologyMeasure.no_universal_atomic_classifier

#print axioms OrthemologyMeasure.no_universal_randomised_atomic_test
