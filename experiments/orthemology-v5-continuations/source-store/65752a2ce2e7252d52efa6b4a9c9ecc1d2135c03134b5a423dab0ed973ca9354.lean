import WinningContinuation

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2.PolicyEmbedding CanonicalMicro
universe u v
variable {A Y : Type u} {R : Type v} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- A positive-branch history invariant yields all-time action safety in the
original canonical law, not merely eventual safety or support after a block. -/
theorem canonical_always_of_invariant (π : History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (D : Finset A) (I : History A Y → Prop) (hI : I [])
    (hnext : ∀ h y, I h → 0 < P (π h) y → I ((π h,y)::h))
    (hlegal : ∀ h, I h → π h ∈ D) (d : A) :
    ∀ᵐ x ∂actionLaw (ignoreSeed π) ρ P hP hN d, ∀ n, x n ∈ D := by
  have hb := canonical_total_cost_of_drift π ρ P hP hN (badActionCost D) (fun _ => 0) I hI hnext
    (by intro h hh; simp [badActionCost,hlegal h hh]) d
  have hz : (∫⁻ x, ∑' t, badActionCost D (x t) ∂actionLaw (ignoreSeed π) ρ P hP hN d) = 0 :=
    le_antisymm hb (zero_le _)
  have ha := (lintegral_eq_zero_iff (total_bad_measurable D)).mp hz
  filter_upwards [ha] with x hx
  intro n
  have hn := ENNReal.le_tsum (f := fun t => badActionCost D (x t)) n
  rw [hx] at hn
  by_contra hbad
  simp [badActionCost,hbad] at hn

/-- The same invariant theorem for a fixed private seed of an arbitrary shared
policy. The fixed-seed law identity is proved from its actual row evaluator. -/
theorem fixedSeed_always_of_invariant (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (r : R)
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (D : Finset A) (I : History A Y → Prop) (hI : I [])
    (hnext : ∀ h y, I h → 0 < P (π r h) y → I ((π r h,y)::h))
    (hlegal : ∀ h, I h → π r h ∈ D) (d : A) :
    ∀ᵐ x ∂actionLaw π (Measure.dirac r) P hP hN d, ∀ n, x n ∈ D := by
  rw [actionLaw_congr_fixed_seed π (ignoreSeed (π r)) hπ (ignoreSeed_measurable (π r)) r
    (fun _ => rfl) P hP hN d]
  exact canonical_always_of_invariant (π r) (Measure.dirac r) P hP hN D I hI hnext hlegal d
end Orthemology.Tranche3
