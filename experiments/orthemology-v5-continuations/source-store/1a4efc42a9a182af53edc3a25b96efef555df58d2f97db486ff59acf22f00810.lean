import ObservedHistoryLicensing

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Set Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2
open Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {Θ A Y : Type u} {R : Type v}
    [Fintype Θ] [Fintype A] [Fintype Y] [DecidableEq Θ] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Fix one seed for both target success and an observable-history property,
simultaneously across the finite family. The property may include dynamic safety. -/
theorem common_seed_success_and_history_event
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A)
    (E : Θ → Set (ℕ → History A Y)) (hE : ∀ θ, MeasurableSet (E θ))
    (hgood : ∀ θ, ∀ᵐ x ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d, ∀ᶠ n in atTop, x n ∈ good θ)
    (hhist : ∀ θ, ∀ᵐ H ∂observedTraceLaw ∅ π ρ (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ), H ∈ E θ) :
    ∃ r : R, ∀ θ,
      (∀ᵐ x ∂actionLaw π (Measure.dirac r) (P θ) (hP θ) (hN θ) d, ∀ᶠ n in atTop, x n ∈ good θ) ∧
      (∀ᵐ H ∂observedTraceLaw ∅ π (Measure.dirac r) (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ), H ∈ E θ) := by
  have hr : ∀ θ, ∀ᵐ r ∂ρ, ∀ᵐ ω ∂feedbackLaw (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ),
      (∀ᶠ n in atTop, rawActionPath π d (r,ω) n ∈ good θ) ∧ historyTrajectory ∅ π (r,ω) ∈ E θ := by
    intro θ
    have hg := hgood θ
    rw [actionLaw_raw_map π hπ] at hg
    have hga := ae_of_ae_map (rawActionPath_measurable π hπ d).aemeasurable hg
    have hs := hhist θ
    unfold observedTraceLaw at hs
    have hsa := ae_of_ae_map (historyTrajectory_measurable ∅ π hπ).aemeasurable hs
    exact Measure.ae_ae_of_ae_prod (hga.and hsa)
  obtain ⟨r,hr⟩ := (ae_all_iff.mpr hr).exists
  refine ⟨r,fun θ => ⟨?_,?_⟩⟩
  · rw [actionLaw_dirac_seed π hπ r]
    apply (ae_map_iff ((rawActionPath_measurable π hπ d).comp (measurable_const.prodMk measurable_id)).aemeasurable
      (measurableSet_eventually_mem (good θ))).mpr
    exact (hr θ).mono (fun _ h => h.1)
  · rw [observedTraceLaw_dirac_raw π hπ r]
    apply (ae_map_iff ((historyTrajectory_measurable ∅ π hπ).comp (measurable_const.prodMk measurable_id)).aemeasurable
      (hE θ)).mpr
    exact (hr θ).mono (fun _ h => h.2)

/-- The recursive criterion also characterizes existence under the weaker
almost-sure observed-history licensing presentation. The original randomized
policy need not be safe on null seeds or impossible histories. -/
theorem ae_licensed_policy_exists_iff_recursiveWinning
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B : Finset Θ) (hB : B.Nonempty) (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    (∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      ∀ θ ∈ B,
        (∀ᵐ H ∂observedTraceLaw ∅ π ρ (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ),
          LicensedHistoryPath P menu B d H) ∧
        (∀ᵐ x ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d, ∀ᶠ n in atTop, x n ∈ good θ)) ↔
      RecursiveWinning P good menu B := by
  constructor
  · rintro ⟨π,hπ,hw⟩
    obtain ⟨r,hr⟩ := common_seed_success_and_history_event
      (fun θ : {θ // θ ∈ B} => P θ.val) (fun θ : {θ // θ ∈ B} => good θ.val)
      (fun θ => hP θ.val) (fun θ => hN θ.val) π hπ ρ d
      (fun _ => {H | LicensedHistoryPath P menu B d H})
      (fun _ => measurableSet_licensedHistoryPath P menu B d)
      (fun θ => (hw θ.val θ.property).2) (fun θ => (hw θ.val θ.property).1)
    have hsafe : ∀ θ ∈ B, ∀ᵐ H ∂observedTraceLaw ∅ π (Measure.dirac r)
        (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ), LicensedHistoryPath P menu B d H :=
      fun θ hθ => (hr ⟨θ,hθ⟩).2
    apply fixedSeedWinning_recursive_necessity P good menu hP hN d B hB π r
    exact ⟨hπ,fixed_seed_ae_license_is_pointwise P menu hP hN B π hπ r d hsafe,
      fun θ hθ => (hr ⟨θ,hθ⟩).1⟩
  · intro hw
    obtain ⟨π,hπ,hl,hg⟩ := recursive_certificate_canonical_policy_exists P good menu hP hN B hw ρ d
    exact ⟨π,hπ,fun θ hθ => ⟨pointwise_license_implies_ae_license P menu hP hN B π hπ ρ d hl θ hθ,(hg θ hθ).2⟩⟩

/-- With almost-sure observable licensing as well, qualitative existence is
equivalent to existence of a finite expected total physical error budget. -/
theorem ae_licensed_finite_budget_exists_iff_recursiveWinning
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B : Finset Θ) (hB : B.Nonempty) (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    (∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      ∀ θ ∈ B,
        (∀ᵐ H ∂observedTraceLaw ∅ π ρ (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ),
          LicensedHistoryPath P menu B d H) ∧
        (∃ C : ℝ, (∫⁻ x, ∑' t, badActionCost (good θ) (x t)
          ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d) ≤ ENNReal.ofReal C)) ↔
      RecursiveWinning P good menu B := by
  constructor
  · rintro ⟨π,hπ,hw⟩
    apply (ae_licensed_policy_exists_iff_recursiveWinning P good menu hP hN B hB ρ d).mp
    refine ⟨π,hπ,?_⟩
    intro θ hθ
    obtain ⟨C,hC⟩ := (hw θ hθ).2
    exact ⟨(hw θ hθ).1,eventually_good_of_total_bad_budget (good θ) _ C hC⟩
  · intro hw
    obtain ⟨π,hπ,hl,hg⟩ := recursive_certificate_canonical_policy_exists P good menu hP hN B hw ρ d
    exact ⟨π,hπ,fun θ hθ => ⟨pointwise_license_implies_ae_license P menu hP hN B π hπ ρ d hl θ hθ,
      ⟨recursiveChainBudget P good menu hP θ ⟨B,hw⟩,(hg θ hθ).1⟩⟩⟩
end Orthemology.Tranche3
