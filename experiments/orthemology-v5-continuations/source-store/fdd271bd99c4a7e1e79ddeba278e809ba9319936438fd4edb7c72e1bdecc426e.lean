import RecursiveNecessity

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

/-- Arbitrary common-seed necessity follows by a proved finite-model
simultaneous derandomization, then all-branch support induction. -/
theorem seeded_recursive_necessity
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B : Finset Θ) (hB : B.Nonempty) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A)
    (hlegal : ∀ r h, ActionCompatible π r h → (historySupport P B h).Nonempty →
      π r h ∈ menu (historySupport P B h))
    (hgood : ∀ θ ∈ B, ∀ᵐ x ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d,
      ∀ᶠ n in atTop, x n ∈ good θ) : RecursiveWinning P good menu B := by
  obtain ⟨r,hr⟩ := common_seed_derandomization
    (fun θ : {θ // θ ∈ B} => P θ.val) (fun θ : {θ // θ ∈ B} => good θ.val)
    (fun θ => hP θ.val) (fun θ => hN θ.val) π hπ ρ d
    (fun θ => hgood θ.val θ.property)
  exact fixedSeedWinning_recursive_necessity P good menu hP hN d B hB π r
    ⟨hπ,hlegal r,fun θ hθ => hr ⟨θ,hθ⟩⟩

/-- Exact zero-support/support-menu restoration iff in ONE literal canonical
seeded-history policy and actionLaw interface. No transfer, representation,
continuation, rank, or successful-controller premise is supplied. -/
theorem seeded_policy_exists_iff_recursiveWinning
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B : Finset Θ) (hB : B.Nonempty) (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    (∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      (∀ r h, ActionCompatible π r h → (historySupport P B h).Nonempty →
        π r h ∈ menu (historySupport P B h)) ∧
      ∀ θ ∈ B, ∀ᵐ x ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d,
        ∀ᶠ n in atTop, x n ∈ good θ) ↔ RecursiveWinning P good menu B := by
  constructor
  · rintro ⟨π,hπ,hl,hg⟩
    exact seeded_recursive_necessity P good menu hP hN B hB π hπ ρ d hl hg
  · intro hw
    obtain ⟨π,hπ,hl,hg⟩ := recursive_certificate_canonical_policy_exists P good menu hP hN B hw ρ d
    exact ⟨π,hπ,hl,fun θ hθ => (hg θ hθ).2⟩

/-- Count integrability implies qualitative restoration for any physical law.
The converse below concerns existence of a suitable policy, not every policy. -/
theorem eventually_good_of_total_bad_budget (G : Finset A) (μ : Measure (ℕ → A)) (C : ℝ)
    (hbudget : (∫⁻ x, ∑' t, badActionCost G (x t) ∂μ) ≤ ENNReal.ofReal C) :
    ∀ᵐ x ∂μ, ∀ᶠ t in atTop, x t ∈ G := by
  classical
  let c : A → ℕ := fun a => if a ∈ G then 0 else 1
  have he : ∀ a, (c a : ℝ≥0∞) = badActionCost G a := by
    intro a
    by_cases ha : a ∈ G <;> simp [c,badActionCost,ha]
  have hf : ∀ n, (∫⁻ x, pathCharge (fun a => (c a : ℝ≥0∞)) 0 n x ∂μ) ≤ ENNReal.ofReal C := by
    intro n
    apply le_trans (lintegral_mono ?_) hbudget
    intro x
    simp only [pathCharge,Nat.zero_add,he]
    exact ENNReal.sum_le_tsum (Finset.range n)
  have ha := (trajectory_nat_charge_eventually_zero μ c C hf).2
  filter_upwards [ha] with x hx
  filter_upwards [hx] with t ht
  by_contra hbad
  simp [c,hbad] at ht

/-- Existence of a licensed almost-surely restoring policy is equivalent to
existence of one with finite expected total error count, for this finite fixed
model/support-menu class. The constructive direction gives the chain bound. -/
theorem finite_budget_policy_exists_iff_recursiveWinning
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B : Finset Θ) (hB : B.Nonempty) (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    (∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      (∀ r h, ActionCompatible π r h → (historySupport P B h).Nonempty →
        π r h ∈ menu (historySupport P B h)) ∧
      ∀ θ ∈ B, ∃ C : ℝ,
        (∫⁻ x, ∑' t, badActionCost (good θ) (x t) ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d) ≤
          ENNReal.ofReal C) ↔ RecursiveWinning P good menu B := by
  constructor
  · rintro ⟨π,hπ,hl,hg⟩
    apply seeded_recursive_necessity P good menu hP hN B hB π hπ ρ d hl
    intro θ hθ
    obtain ⟨C,hC⟩ := hg θ hθ
    exact eventually_good_of_total_bad_budget (good θ) _ C hC
  · intro hw
    obtain ⟨π,hπ,hl,hg⟩ := recursive_certificate_canonical_policy_exists P good menu hP hN B hw ρ d
    exact ⟨π,hπ,hl,fun θ hθ => ⟨recursiveChainBudget P good menu hP θ ⟨B,hw⟩,(hg θ hθ).1⟩⟩

/-- The same iff is the original bottom-up greatest-support stage criterion,
using its checked certificate equivalence rather than a new winning definition. -/
theorem seeded_policy_exists_iff_recursive_stage
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B : Finset Θ) (hB : B.Nonempty) (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    (∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      (∀ r h, ActionCompatible π r h → (historySupport P B h).Nonempty →
        π r h ∈ menu (historySupport P B h)) ∧
      ∀ θ ∈ B, ∀ᵐ x ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d,
        ∀ᶠ n in atTop, x n ∈ good θ) ↔
      StageCertificate (fun θ : {θ // θ ∈ B} => good θ.val)
        (fun η ζ a => P η.val a = P ζ.val a)
        (recursiveAllowed P good menu B) (recursiveProgress P good menu B) := by
  rw [seeded_policy_exists_iff_recursiveWinning P good menu hP hN B hB ρ d,
    recursiveWinning_iff_stage]
  exact and_iff_right hB
end Orthemology.Tranche3
