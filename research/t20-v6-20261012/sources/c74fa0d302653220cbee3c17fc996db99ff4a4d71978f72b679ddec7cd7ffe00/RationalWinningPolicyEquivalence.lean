import RationalWinningWitness
import AELicensedEquivalence

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche3
namespace Orthemology.Tranche4.RationalWinning
variable {m k l : ℕ}

lemma checked_nonneg (T : Tables m k l) (hv : validTable T = true) :
    ∀ θ a y, 0 ≤ realKernel T θ a y := (table_valid_sound T hv).1
lemma checked_normalized (T : Tables m k l) (hv : validTable T = true) :
    ∀ θ a, ∑ y, realKernel T θ a y = 1 := (table_valid_sound T hv).2

universe v
variable {R : Type v} [MeasurableSpace R] [Inhabited (Fin l)]

/-- Exact executable existence test under the inherited canonical hypotheses.
A default action and an inhabited receipt type are supplied, never fabricated. -/
theorem validated_winning_iff_policy (T : Tables m k l) (B : Finset (Fin m))
    (hv : validTable T = true) (hB : B.Nonempty) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (d : Fin k) :
    decideWinning T B = .winning ↔
      (∃ π : R → History (Fin k) (Fin l) → Fin k,
        Measurable (fun z : R × History (Fin k) (Fin l) => π z.1 z.2) ∧
        ∀ θ ∈ B,
          (∀ᵐ H ∂observedTraceLaw ∅ π ρ (realKernel T θ) (realKernel T θ)
            (checked_nonneg T hv θ) (checked_normalized T hv θ)
            (checked_nonneg T hv θ) (checked_normalized T hv θ),
            LicensedHistoryPath (realKernel T) T.menu B d H) ∧
          (∀ᵐ x ∂actionLaw π ρ (realKernel T θ) (checked_nonneg T hv θ)
            (checked_normalized T hv θ) d, ∀ᶠ n in atTop, x n ∈ T.good θ)) := by
  rw [decideWinning_winning_iff]
  exact (and_iff_right hv).trans
    (ae_licensed_policy_exists_iff_recursiveWinning (realKernel T) T.good T.menu
      (checked_nonneg T hv) (checked_normalized T hv) B hB ρ d).symm

/-- A valid nonempty losing result rejects every shared measurable seeded
history policy in that same observable-licensing/action-law contract. -/
theorem validated_losing_iff_no_policy (T : Tables m k l) (B : Finset (Fin m))
    (hv : validTable T = true) (hB : B.Nonempty) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (d : Fin k) :
    decideWinning T B = .losing ↔
      ¬ (∃ π : R → History (Fin k) (Fin l) → Fin k,
        Measurable (fun z : R × History (Fin k) (Fin l) => π z.1 z.2) ∧
        ∀ θ ∈ B,
          (∀ᵐ H ∂observedTraceLaw ∅ π ρ (realKernel T θ) (realKernel T θ)
            (checked_nonneg T hv θ) (checked_normalized T hv θ)
            (checked_nonneg T hv θ) (checked_normalized T hv θ),
            LicensedHistoryPath (realKernel T) T.menu B d H) ∧
          (∀ᵐ x ∂actionLaw π ρ (realKernel T θ) (checked_nonneg T hv θ)
            (checked_normalized T hv θ) d, ∀ᶠ n in atTop, x n ∈ T.good θ)) := by
  rw [decideWinning_losing_iff]
  simp only [hv,hB,true_and]
  exact (not_congr (ae_licensed_policy_exists_iff_recursiveWinning (realKernel T) T.good T.menu
    (checked_nonneg T hv) (checked_normalized T hv) B hB ρ d)).symm

/-- Existence of a finite expected total target-error policy is decided by the
same Boolean, not by compiling such an infinite controller here. -/
theorem validated_winning_iff_finite_budget (T : Tables m k l) (B : Finset (Fin m))
    (hv : validTable T = true) (hB : B.Nonempty) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (d : Fin k) :
    decideWinning T B = .winning ↔
      (∃ π : R → History (Fin k) (Fin l) → Fin k,
        Measurable (fun z : R × History (Fin k) (Fin l) => π z.1 z.2) ∧
        ∀ θ ∈ B,
          (∀ᵐ H ∂observedTraceLaw ∅ π ρ (realKernel T θ) (realKernel T θ)
            (checked_nonneg T hv θ) (checked_normalized T hv θ)
            (checked_nonneg T hv θ) (checked_normalized T hv θ),
            LicensedHistoryPath (realKernel T) T.menu B d H) ∧
          (∃ C : ℝ, (∫⁻ x, ∑' n, badActionCost (T.good θ) (x n)
            ∂actionLaw π ρ (realKernel T θ) (checked_nonneg T hv θ)
              (checked_normalized T hv θ) d) ≤ ENNReal.ofReal C)) := by
  rw [decideWinning_winning_iff]
  exact (and_iff_right hv).trans
    (ae_licensed_finite_budget_exists_iff_recursiveWinning (realKernel T) T.good T.menu
      (checked_nonneg T hv) (checked_normalized T hv) B hB ρ d).symm

end Orthemology.Tranche4.RationalWinning
