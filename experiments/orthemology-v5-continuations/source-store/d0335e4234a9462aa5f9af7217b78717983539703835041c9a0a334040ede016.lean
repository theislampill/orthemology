import PolicyTailTransfer
import SelfVerifyingSupport

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2.PolicyEmbedding
universe u v w
variable {R : Type v} {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

lemma actionLaw_isProbability (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (d : A) :
    IsProbabilityMeasure (actionLaw π ρ P hP hN d) := by
  haveI : IsProbabilityMeasure (observedTraceLaw ∅ π ρ P P hP hN hP hN) := by
    unfold observedTraceLaw
    exact isProbabilityMeasure_map (historyTrajectory_measurable ∅ π hπ).aemeasurable
  unfold actionLaw
  exact isProbabilityMeasure_map (historyAction_measurable d).aemeasurable

/-- Full-support CIRS necessity for arbitrary measurable seeded causal policies.
The actual interaction law is constructed from fresh row observations. The
policy law embedding, positive-tail transfer and recurrence selection are all
proved; none is supplied as a transfer or success-preservation hypothesis. -/
theorem seeded_policy_self_verifying_necessity {Θ : Type w}
    (P : Θ → A → Y → ℝ) (G : Θ → Finset A)
    (hP : ∀ θ a y, 0 < P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A)
    (hgood : ∀ θ, ∀ᵐ x ∂actionLaw π ρ (P θ) (fun a y => (hP θ a y).le) (hN θ) d,
      ∀ᶠ n in atTop, x n ∈ G θ) (θ : Θ) :
    ∃ U : Finset A, U.Nonempty ∧ SelfVerifying G (fun η ζ a => P η a = P ζ a) θ U := by
  let μ := fun η => actionLaw π ρ (P η) (fun a y => (hP η a y).le) (hN η) d
  haveI : ∀ η, IsProbabilityMeasure (μ η) := fun η =>
    actionLaw_isProbability π hπ ρ (P η) (fun a y => (hP η a y).le) (hN η) d
  have hs := RecurrentSupport.abstract_self_verifying_support μ (id : (ℕ → A) → ℕ → A) G
    (fun η ζ U => ∀ a ∈ U, P η a = P ζ a) hgood
    (fun η ζ U N hag hp => canonical_positive_tail_transfers U π hπ ρ (P η) (P ζ)
      (hP η) (hN η) (hP ζ) (hN ζ) hag d N hp) θ
  obtain ⟨U,hne,hsub,hall⟩ := hs
  exact ⟨U,hne,hsub,hall⟩

/-- The same necessary condition is the exact finite greatest-kernel test. -/
theorem seeded_policy_kernel_nonempty {Θ : Type w}
    (P : Θ → A → Y → ℝ) (G : Θ → Finset A)
    (hP : ∀ θ a y, 0 < P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A)
    (hgood : ∀ θ, ∀ᵐ x ∂actionLaw π ρ (P θ) (fun a y => (hP θ a y).le) (hN θ) d,
      ∀ᶠ n in atTop, x n ∈ G θ) (θ : Θ) :
    (supportKernel G (fun η ζ a => P η a = P ζ a) θ).Nonempty :=
  (supportKernel_nonempty_iff G _ θ).mpr
    (seeded_policy_self_verifying_necessity P G hP hN π hπ ρ d hgood θ)

end Orthemology.Tranche2.PolicyEmbedding
