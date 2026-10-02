import SafeSetTailTransfer
import SeededPolicyNecessity
import RecursiveCanonicalSufficiency

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Set Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2
open Orthemology.Tranche2.PolicyEmbedding
open RelativeTransfer
universe u v w
variable {A Y : Type u} {R : Type v} {Θ : Type w}
    [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- The statistical half of recursive necessity with observation zeros. If one
true model stays in the all-branch admissible action set and its positive symbols
remain possible in every live rival there, recurrent good actions contain a
nonempty live self-verifying support. -/
theorem stable_model_self_verifying_necessity
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (B : Finset Θ) (D : Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) (θ : Θ) (hθ : θ ∈ B)
    (hgood : ∀ η ∈ B, ∀ᵐ x ∂actionLaw π ρ (P η) (hP η) (hN η) d,
      ∀ᶠ n in atTop, x n ∈ good η)
    (hD : ∀ᵐ x ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d, ∀ n, x n ∈ D)
    (hstable : ∀ η ∈ B, ∀ a ∈ D, ∀ y, 0 < P θ a y → 0 < P η a y) :
    ∃ U : Finset A, U.Nonempty ∧ U ⊆ D ∧ U ⊆ good θ ∧
      ∀ η ∈ B, (∀ a ∈ U, P θ a = P η a) → U ⊆ good η := by
  let μ := fun η => actionLaw π ρ (P η) (hP η) (hN η) d
  haveI : ∀ η, IsProbabilityMeasure (μ η) := fun η => actionLaw_isProbability π hπ ρ (P η) (hP η) (hN η) d
  have hg : ∀ᵐ x ∂μ θ, ∀ᶠ n in atTop, x n ∈ good θ ∩ D := by
    filter_upwards [hgood θ hθ,hD] with x hx hd
    filter_upwards [hx] with n hn
    exact Finset.mem_inter.mpr ⟨hn,hd n⟩
  obtain ⟨U,hne,hsub,hpos⟩ := RecurrentSupport.exists_positive_recurrent_support (μ θ) id (good θ ∩ D) hg
  obtain ⟨N,htail⟩ := RecurrentSupport.exists_positive_tail_index (μ θ) id U hpos
  have hUD : U ⊆ D := fun a ha => (Finset.mem_inter.mp (hsub ha)).2
  refine ⟨U,hne,hUD,fun a ha => (Finset.mem_inter.mp (hsub ha)).1,?_⟩
  intro η hη hag
  have he : (RecurrentSupport.tailEvent id U N ∩ alwaysIn D : Set (ℕ → A)) =ᵐ[μ θ] (RecurrentSupport.tailEvent id U N : Set (ℕ → A)) := by
    filter_upwards [hD] with x hx
    apply propext
    change (_ ∧ ∀ n, x n ∈ D) ↔ _
    exact ⟨fun hh => hh.1,fun hh => ⟨hh,hx⟩⟩
  have hp : 0 < μ θ (RecurrentSupport.tailEvent id U N ∩ alwaysIn D) := by rwa [measure_congr he]
  have hr := canonical_positive_tail_on_safe_actions D U hUD π hπ ρ (P θ) (P η)
    (hP θ) (hN θ) (hP η) (hN η) (hstable η hη) hag d N hp
  have hx : 0 < μ η (RecurrentSupport.exactRecurrentEvent id U) :=
    hr.trans_le (measure_mono (Set.inter_subset_left.trans Set.inter_subset_left))
  exact RecurrentSupport.support_subset_of_positive_exact_event (μ η) id (good η) U (hgood η hη) hx

end Orthemology.Tranche3
