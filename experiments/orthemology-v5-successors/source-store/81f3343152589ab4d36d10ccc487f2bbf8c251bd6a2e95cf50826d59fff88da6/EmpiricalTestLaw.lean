import ObservedRowTest

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Actual true-model tests are all negative after a finite random phase index,
uniformly over every policy and every physical testing time. -/
theorem empiricalReject_true_eventually_never
    (P : RationalKernel Model (State × Action) State) (σ : Model)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (ε : ℝ) (hε : 0 < ε) :
    ∀ᵐ z ∂ρ.prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)),
      ∃ K : ℕ, ∀ k, K ≤ k → ∀ (π : R → History (State × Action) State → State × Action) n,
        empiricalReject P ε σ k (stackHistoryTrajectory π z n) = false := by
  filter_upwards [seeded_true_phase_rejections_bounded ρ (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) hε] with z hz
  obtain ⟨K,hK⟩ := hz
  refine ⟨K,?_⟩
  intro k hk π n
  by_contra hNot
  have ht : empiricalReject P ε σ k (stackHistoryTrajectory π z n) = true := by
    cases he : empiricalReject P ε σ k (stackHistoryTrajectory π z n) <;> simp_all
  obtain ⟨e,y,hCount,hBad⟩ := (empiricalReject_iff P ε σ k _).mp ht
  exact not_le_of_gt (hK k hk π e y n hCount) hBad

/-- Any genuinely mismatching recurrent row eventually triggers the literal
observed-history test at every fixed phase index. -/
theorem empiricalReject_recurrent_mismatch
    (P : RationalKernel Model (State × Action) State) (B₀ : Finset Model)
    (σ : Model) (hσ : σ ∈ B₀) (ρ : Measure R) [IsProbabilityMeasure ρ] (ε : ℝ)
    (hSep : ∀ θ ∈ B₀, ∀ e, P.row θ e ≠ P.row σ e →
      ∃ y, ε < |realRows P σ e y - realRows P θ e y|) :
    ∀ᵐ z ∂ρ.prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)),
      ∀ (π : R → History (State × Action) State → State × Action) θ, θ ∈ B₀ →
        ∀ e ∈ recurrentSet (stackActionTrajectory π z), P.row θ e ≠ P.row σ e →
          ∀ k, ∀ᶠ n in atTop, empiricalReject P ε θ k (stackHistoryTrajectory π z n) = true := by
  filter_upwards [seeded_false_rows_eventually_rejected ρ (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ)] with z hz
  intro π θ hθ e he hNe k
  obtain ⟨y,hy⟩ := hSep θ hθ e hNe
  have h := hz π (realRows P θ) e y k ε ((mem_recurrentSet _ e).mp he) hy
  filter_upwards [h] with n hn
  exact (empiricalReject_iff P ε θ k _).mpr ⟨e,y,hn.1,hn.2.le⟩

end HiddenParity.Sufficiency
