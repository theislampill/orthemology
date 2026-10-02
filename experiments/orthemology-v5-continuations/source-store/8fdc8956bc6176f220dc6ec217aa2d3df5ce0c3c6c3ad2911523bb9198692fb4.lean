import Mathlib
import SelfVerifyingSupport

open MeasureTheory Filter Set

namespace Orthemology.Tranche2.CommonObservationBoundary

/-- If finitely many target demands hold eventually under laws all dominating
one nonzero reference, they must share an action. No finite action alphabet is
required. Domination here concerns the complete observed path, not its finite
prefixes. -/
theorem common_action_of_dominated_eventual_success
    {Θ Ω A : Type*} [Finite Θ] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω)
    (X : Ω → ℕ → A) (good : Θ → Set A)
    (hdom : ∀ θ, μ ≪ ν θ)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop, X ω n ∈ good θ) :
    ∃ a, ∀ θ, a ∈ good θ := by
  have hs : ∀ θ, ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ good θ := by
    intro θ
    exact (Measure.ae_le_iff_absolutelyContinuous.mpr (hdom θ)) (hsuccess θ)
  obtain ⟨ω, hω⟩ := (eventually_all.mpr hs).exists
  obtain ⟨n, hn⟩ := (eventually_all.mpr hω).exists
  exact ⟨X ω n, hn⟩

/-- Same full observed law is a particularly transparent case. -/
theorem common_action_of_same_law
    {Θ Ω A : Type*} [Finite Θ] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (X : Ω → ℕ → A) (good : Θ → Set A)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ good θ) :
    ∃ a, ∀ θ, a ∈ good θ := by
  obtain ⟨ω, hω⟩ := (eventually_all.mpr hsuccess).exists
  obtain ⟨n, hn⟩ := (eventually_all.mpr hω).exists
  exact ⟨X ω n, hn⟩

/-- A common accepted action gives a deterministic constant solution under
any observation laws; no inference about which target is authoritative follows. -/
theorem constant_action_success
    {Θ Ω A : Type*} [MeasurableSpace Ω]
    (ν : Θ → Measure Ω) (good : Θ → Set A) (a : A)
    (ha : ∀ θ, a ∈ good θ) :
    ∀ θ, ∀ᵐ _ω ∂ν θ, ∀ᶠ _n : ℕ in atTop, a ∈ good θ := by
  intro θ
  exact Eventually.of_forall (fun _ => Eventually.of_forall (fun _ => ha θ))

/-- Pure support-kernel form, requiring no probability assumptions. -/
theorem selfVerifying_iff_common_target
    {Θ A : Type*} (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ)
    (hall : ∀ σ a, same θ σ a) (U : Finset A) :
    SelfVerifying good same θ U ↔ ∀ σ, U ⊆ good σ := by
  constructor
  · intro h σ
    exact h.2 σ (fun a _ => hall σ a)
  · intro h
    exact ⟨h θ, fun σ _ => h σ⟩

/-- Finite candidate scope cannot just be deleted when the action space is
infinite: action n eventually lies in every fixed tail target {a | θ ≤ a},
yet there is no action in all those targets. -/
theorem infinite_target_counterexample :
    (∀ θ : ℕ, ∀ᶠ n : ℕ in atTop, θ ≤ n) ∧
      ¬ (∃ a : ℕ, ∀ θ : ℕ, θ ≤ a) := by
  constructor
  · intro θ
    exact eventually_ge_atTop θ
  · rintro ⟨a, ha⟩
    have h := ha (a + 1)
    omega

end Orthemology.Tranche2.CommonObservationBoundary

#print axioms Orthemology.Tranche2.CommonObservationBoundary.common_action_of_dominated_eventual_success
#print axioms Orthemology.Tranche2.CommonObservationBoundary.common_action_of_same_law
#print axioms Orthemology.Tranche2.CommonObservationBoundary.constant_action_success
#print axioms Orthemology.Tranche2.CommonObservationBoundary.selfVerifying_iff_common_target
#print axioms Orthemology.Tranche2.CommonObservationBoundary.infinite_target_counterexample
