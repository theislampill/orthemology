import StackActionLaw

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2.PolicyEmbedding
universe u v w
variable {A Y : Type u} {R : Type v} {Θ : Type w}
    [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

def rawActionPath (π : R → History A Y → A) (d : A) (z : Input R A Y) : ℕ → A :=
  historyAction d (historyTrajectory ∅ π z)

lemma rawActionPath_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (d : A) : Measurable (rawActionPath π d) :=
  (historyAction_measurable d).comp (historyTrajectory_measurable ∅ π hπ)

/-- The canonical law is explicitly the shared-seed/product-feedback mixture. -/
lemma actionLaw_raw_map (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (d : A) :
    actionLaw π ρ P hP hN d =
      (ρ.prod (feedbackLaw P P hP hN hP hN)).map (rawActionPath π d) := by
  rw [actionLaw,observedTraceLaw,Measure.map_map (historyAction_measurable d)
    (historyTrajectory_measurable ∅ π hπ)]
  rfl

/-- Under a fixed seed, the only remaining randomness is fresh feedback. -/
lemma actionLaw_dirac_seed (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (d : A) :
    actionLaw π (Measure.dirac r) P hP hN d =
      (feedbackLaw P P hP hN hP hN).map (fun ω => rawActionPath π d (r,ω)) := by
  rw [actionLaw_raw_map π hπ,Measure.dirac_prod,
    Measure.map_map (rawActionPath_measurable π hπ d)
      (show Measurable (Prod.mk r) from measurable_const.prodMk measurable_id)]
  rfl

/-- Finite-model, common-seed derandomization in the actual canonical law.
One seed works simultaneously in every model. No model-dependent seed choice,
conditional posterior, or abstract mixture representation is assumed. -/
theorem common_seed_derandomization [Fintype Θ]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A)
    (hgood : ∀ θ, ∀ᵐ x ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d,
      ∀ᶠ n in atTop, x n ∈ good θ) :
    ∃ r : R, ∀ θ, ∀ᵐ x ∂actionLaw π (Measure.dirac r) (P θ) (hP θ) (hN θ) d,
      ∀ᶠ n in atTop, x n ∈ good θ := by
  have hr : ∀ θ, ∀ᵐ r ∂ρ, ∀ᵐ ω ∂feedbackLaw (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ),
      ∀ᶠ n in atTop, rawActionPath π d (r,ω) n ∈ good θ := by
    intro θ
    have hh := hgood θ
    rw [actionLaw_raw_map π hπ] at hh
    exact Measure.ae_ae_of_ae_prod (ae_of_ae_map (rawActionPath_measurable π hπ d).aemeasurable hh)
  obtain ⟨r,hr⟩ := (ae_all_iff.mpr hr).exists
  refine ⟨r,fun θ => ?_⟩
  rw [actionLaw_dirac_seed π hπ r]
  apply (ae_map_iff ((rawActionPath_measurable π hπ d).comp (measurable_const.prodMk measurable_id)).aemeasurable
    (measurableSet_eventually_mem (good θ))).mpr
  exact hr θ
end Orthemology.Tranche3
