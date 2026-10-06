import Mathlib

/-!
# Finite-family probability bounds for randomized algorithms

The index `W` denotes fixed problem instances; `Ω` denotes complete random-coin
outcomes. All statements quantify over a fixed probability law on `Ω`. In
particular, they do not grant an adversary access to a realized coin outcome.

For a finite instance family, an almost-sure guarantee for each fixed instance
holds simultaneously for all instances outside one null set. Thus pointwise
failure of some instance implies positive measure of failure for one fixed
instance. The finite union bound also gives the quantitative lower bound
`1 / Fintype.card W`.

No measurability assumptions on the predicates are needed: `μ s` is defined for
all sets as outer measure. If failure events are measurable, the numeric bounds
are bounds on their ordinary probabilities. The almost-everywhere conclusions
need no event-measurability assumption.
-/

open MeasureTheory Filter Set
open scoped ENNReal BigOperators

namespace CoveringKernel.RandomizedFinite

variable {Ω W : Type*} [MeasurableSpace Ω]

/-- An almost-sure guarantee for every fixed member of a finite family gives one
common conull set on which every member succeeds. It does not give a pointwise
guarantee for every coin outcome. -/
theorem ae_all_of_ae_each [Finite W] (μ : Measure Ω) (Success : W → Ω → Prop)
    (h : ∀ w, ∀ᵐ ω ∂μ, Success w ω) :
    ∀ᵐ ω ∂μ, ∀ w, Success w ω :=
  ae_all_iff.mpr h

/-- On a probability space the common conull success set is nonempty. -/
theorem exists_coin_success_all [Finite W] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (Success : W → Ω → Prop) (h : ∀ w, ∀ᵐ ω ∂μ, Success w ω) :
    ∃ ω, ∀ w, Success w ω :=
  (ae_all_of_ae_each μ Success h).exists

/-- Even if the cover by failures holds only almost everywhere, one fixed
instance cannot have an almost-sure no-failure guarantee. -/
theorem exists_fixed_failure_not_ae_of_ae_cover [Finite W]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (Fail : W → Ω → Prop)
    (hcover : ∀ᵐ ω ∂μ, ∃ w, Fail w ω) :
    ∃ w, ¬ (∀ᵐ ω ∂μ, ¬ Fail w ω) := by
  classical
  by_contra h
  push_neg at h
  have hcommon := ae_all_of_ae_each μ (fun w ω => ¬ Fail w ω) h
  obtain ⟨ω, hω, hfail⟩ := (hcommon.and hcover).exists
  obtain ⟨w, hw⟩ := hfail
  exact hω w hw

/-- A pointwise cover by failure events forces positive measure for a single
fixed instance, without choosing that instance after drawing the coins. -/
theorem exists_fixed_failure_not_ae [Finite W]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (Fail : W → Ω → Prop)
    (hcover : ∀ ω, ∃ w, Fail w ω) :
    ∃ w, ¬ (∀ᵐ ω ∂μ, ¬ Fail w ω) :=
  exists_fixed_failure_not_ae_of_ae_cover μ Fail (ae_of_all μ hcover)

/-- Outer-measure form of the fixed-instance failure conclusion. -/
theorem exists_fixed_failure_pos [Finite W]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (Fail : W → Ω → Prop)
    (hcover : ∀ ω, ∃ w, Fail w ω) :
    ∃ w, 0 < μ {ω | Fail w ω} := by
  obtain ⟨w, hw⟩ := exists_fixed_failure_not_ae μ Fail hcover
  refine ⟨w, pos_iff_ne_zero.mpr ?_⟩
  simpa only [ae_iff, not_not] using hw

/-- The sum of the failure-event outer measures is at least one if their union
covers the probability space. -/
theorem one_le_sum_failure [Fintype W]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (Fail : W → Ω → Prop)
    (hcover : ∀ ω, ∃ w, Fail w ω) :
    1 ≤ ∑ w, μ {ω | Fail w ω} := by
  have hunion : (⋃ w, {ω | Fail w ω}) = (Set.univ : Set Ω) := by
    ext ω
    simp only [mem_iUnion, mem_setOf_eq, mem_univ, iff_true]
    exact hcover ω
  simpa only [hunion, measure_univ] using
    measure_iUnion_fintype_le μ (fun w => {ω | Fail w ω})

/-- Quantitative finite-family lower bound. When failure events are measurable,
this says that one fixed instance fails with probability at least `1 / |W|`.
The `Nonempty W` assumption is explicit to make the denominator nonzero. -/
theorem exists_fixed_failure_ge_inv_card [Fintype W] [Nonempty W]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (Fail : W → Ω → Prop)
    (hcover : ∀ ω, ∃ w, Fail w ω) :
    ∃ w, 1 / (Fintype.card W : ℝ≥0∞) ≤ μ {ω | Fail w ω} := by
  have hcard0 : (Fintype.card W : ℝ≥0∞) ≠ 0 := by simp
  have hcardtop : (Fintype.card W : ℝ≥0∞) ≠ ∞ := by simp
  have hsum : (∑ _w : W, 1 / (Fintype.card W : ℝ≥0∞)) = 1 := by
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    exact ENNReal.mul_div_cancel hcard0 hcardtop
  have hle : (∑ _w : W, 1 / (Fintype.card W : ℝ≥0∞)) ≤
      ∑ w, μ {ω | Fail w ω} := by
    rw [hsum]
    exact one_le_sum_failure μ Fail hcover
  obtain ⟨w, _, hw⟩ := ENNReal.exists_le_of_sum_le Finset.univ_nonempty hle
  exact ⟨w, hw⟩

/-- Transfer a deterministic lower bound, valid for every coin outcome on some
instance, to any cap that holds almost surely for each fixed instance. -/
theorem lower_bound_of_ae_cap [Finite W]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (cost : W → Ω → ℕ)
    (lower cap : ℕ) (hlower : ∀ ω, ∃ w, lower ≤ cost w ω)
    (hcap : ∀ w, ∀ᵐ ω ∂μ, cost w ω ≤ cap) :
    lower ≤ cap := by
  obtain ⟨ω, hω⟩ := exists_coin_success_all μ (fun w ω => cost w ω ≤ cap) hcap
  obtain ⟨w, hw⟩ := hlower ω
  exact hw.trans (hω w)

/-- A convenient cap form: if every coin outcome exceeds `cap` on some fixed
instance, then some fixed instance does not satisfy the cap almost surely. -/
theorem exists_fixed_cost_not_ae_le [Finite W]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (cost : W → Ω → ℕ) (cap : ℕ)
    (hlarge : ∀ ω, ∃ w, cap < cost w ω) :
    ∃ w, ¬ (∀ᵐ ω ∂μ, cost w ω ≤ cap) := by
  simpa only [not_lt] using
    exists_fixed_failure_not_ae μ (fun w ω => cap < cost w ω) hlarge

/-- Quantitative cap form: one fixed instance exceeds the cap with outer measure
at least `1 / |W|`. -/
theorem exists_fixed_cost_gt_ge_inv_card [Fintype W] [Nonempty W]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (cost : W → Ω → ℕ) (cap : ℕ)
    (hlarge : ∀ ω, ∃ w, cap < cost w ω) :
    ∃ w, 1 / (Fintype.card W : ℝ≥0∞) ≤ μ {ω | cap < cost w ω} :=
  exists_fixed_failure_ge_inv_card μ (fun w ω => cap < cost w ω) hlarge

end CoveringKernel.RandomizedFinite
