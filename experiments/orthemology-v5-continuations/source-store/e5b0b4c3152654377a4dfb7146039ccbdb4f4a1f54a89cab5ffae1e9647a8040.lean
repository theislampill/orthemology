import CommonObservationBoundary

open MeasureTheory Filter Set

namespace Orthemology.Tranche2.CommonObservationBoundary

/-- With finitely many actions the candidate family may be arbitrary. The
finite obstruction consists of one rejecting target for each action. -/
theorem common_action_of_finite_actions
    {Θ Ω A : Type*} [Finite A] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω)
    (X : Ω → ℕ → A) (good : Θ → Set A)
    (hdom : ∀ θ, μ ≪ ν θ)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop, X ω n ∈ good θ) :
    ∃ a, ∀ θ, a ∈ good θ := by
  classical
  by_contra hn
  push_neg at hn
  choose reject hreject using hn
  obtain ⟨a, ha⟩ := common_action_of_dominated_eventual_success μ
    (fun a : A => ν (reject a)) X (fun a => good (reject a))
    (fun a => hdom (reject a)) (fun a => hsuccess (reject a))
  exact hreject a (ha a)

/-- Either finite target multiplicity or a finite action alphabet suffices. -/
theorem common_action_of_either_finite
    {Θ Ω A : Type*} [MeasurableSpace Ω]
    (hfinite : Finite Θ ∨ Finite A)
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω)
    (X : Ω → ℕ → A) (good : Θ → Set A)
    (hdom : ∀ θ, μ ≪ ν θ)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop, X ω n ∈ good θ) :
    ∃ a, ∀ θ, a ∈ good θ := by
  rcases hfinite with hΘ | hA
  · letI := hΘ
    exact common_action_of_dominated_eventual_success μ ν X good hdom hsuccess
  · letI := hA
    exact common_action_of_finite_actions μ ν X good hdom hsuccess

end Orthemology.Tranche2.CommonObservationBoundary

#print axioms Orthemology.Tranche2.CommonObservationBoundary.common_action_of_finite_actions
#print axioms Orthemology.Tranche2.CommonObservationBoundary.common_action_of_either_finite
