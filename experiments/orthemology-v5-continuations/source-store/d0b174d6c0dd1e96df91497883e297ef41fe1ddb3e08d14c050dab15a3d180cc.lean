import ActualExponentialMoments

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
open HiddenParity.Necessity HiddenParity.Stage

/-- Finite minima preserve positive open ranges, while retaining a separate
property that does not depend on the rate. The empty family is allowed. -/
private theorem finite_common_positive_range {ι : Type*} [DecidableEq ι]
    (S : Finset ι) (F : ι → Prop) (G : ι → ℝ → Prop)
    (h : ∀ i ∈ S, ∃ r : ℝ, 0 < r ∧ F i ∧ ∀ t : ℝ, 0 ≤ t → t < r → G i t) :
    ∃ r : ℝ, 0 < r ∧ (∀ i ∈ S, F i) ∧
      ∀ t : ℝ, 0 ≤ t → t < r → ∀ i ∈ S, G i t := by
  induction S using Finset.induction_on with
  | empty => exact ⟨1, by norm_num, by simp, by simp⟩
  | @insert a S ha ih =>
    obtain ⟨ra, hra, hfa, hga⟩ := h a (Finset.mem_insert_self a S)
    obtain ⟨rs, hrs, hfs, hgs⟩ := ih (fun i hi => h i (Finset.mem_insert_of_mem hi))
    refine ⟨min ra rs, lt_min hra hrs, ?_, ?_⟩
    · intro i hi
      rcases Finset.mem_insert.mp hi with rfl | hi
      · exact hfa
      · exact hfs i hi
    · intro t ht htr i hi
      rcases Finset.mem_insert.mp hi with rfl | hi
      · exact hga t ht (htr.trans_le (min_le_left _ _))
      · exact hgs t ht (htr.trans_le (min_le_right _ _)) i hi

universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]
variable (P : RationalKernel Model (State × Action) State)
variable (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
variable (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
variable (ε : ℝ)
local notation "reject" => empiricalReject P ε

/-- One positive open exponential range works for every admitted model in the
fixed finite input. The same Unit-seed generated policy is used throughout.
Strict row separation is required for every admitted true model, rather than
only one selected model. The range may depend on this whole fixed instance. -/
theorem generated_actual_badCount_common_positive_exponential_moments
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority = fun σ => coBuchiPriority (bad σ)) (hε : 0 < ε)
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (hSep : ∀ σ ∈ B₀, ∀ τ ∈ B₀, ∀ e, P.row τ e ≠ P.row σ e →
      ∃ y, ε < |realRows P σ e y - realRows P τ e y|)
    (d : State × Action) :
    ∃ rate : ℝ, 0 < rate ∧
      (∀ σ ∈ B₀, ∀ᵐ H ∂markovHistoryLaw P σ s₀
        (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ()),
        badCount (bad σ) (historyAction d H) < ⊤) ∧
      ∀ θ : ℝ, 0 ≤ θ → θ < rate → ∀ σ ∈ B₀,
        (∫⁻ H, ENNReal.ofReal (Real.exp (θ * (badCount (bad σ) (historyAction d H)).toReal))
          ∂markovHistoryLaw P σ s₀
            (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ())) < ⊤ := by
  apply finite_common_positive_range B₀
  intro σ hσ
  exact generated_actual_badCount_positive_exponential_moments P menu priority B₀ s₀
    fallback fallbackAction ε bad hpriority hε hs₀ σ hσ (hSep σ hσ) d

/-- At each rate strictly below the common range, a finite maximum bounds the
exponential integrals of all admitted models. This is an existential bound for
one fixed input, with no effective numeric constant or instance-independent rate. -/
theorem generated_actual_badCount_common_finite_exponential_bound
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority = fun σ => coBuchiPriority (bad σ)) (hε : 0 < ε)
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (hSep : ∀ σ ∈ B₀, ∀ τ ∈ B₀, ∀ e, P.row τ e ≠ P.row σ e →
      ∃ y, ε < |realRows P σ e y - realRows P τ e y|)
    (d : State × Action) :
    ∃ rate : ℝ, 0 < rate ∧
      (∀ σ ∈ B₀, ∀ᵐ H ∂markovHistoryLaw P σ s₀
        (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ()),
        badCount (bad σ) (historyAction d H) < ⊤) ∧
      ∀ θ : ℝ, 0 ≤ θ → θ < rate → ∃ K : ℝ≥0∞, K < ⊤ ∧ ∀ σ ∈ B₀,
        (∫⁻ H, ENNReal.ofReal (Real.exp (θ * (badCount (bad σ) (historyAction d H)).toReal))
          ∂markovHistoryLaw P σ s₀
            (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ())) ≤ K := by
  obtain ⟨rate, hrate, hfinite, hexp⟩ :=
    generated_actual_badCount_common_positive_exponential_moments P menu priority B₀ s₀
      fallback fallbackAction ε bad hpriority hε hs₀ hSep d
  refine ⟨rate, hrate, hfinite, ?_⟩
  intro θ hθ hθrate
  let f : Model → ℝ≥0∞ := fun σ =>
    ∫⁻ H, ENNReal.ofReal (Real.exp (θ * (badCount (bad σ) (historyAction d H)).toReal))
      ∂markovHistoryLaw P σ s₀
        (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ())
  refine ⟨B₀.sup f, ?_, ?_⟩
  · exact (Finset.sup_lt_iff (show (⊥ : ℝ≥0∞) < ⊤ by simp)).mpr (hexp θ hθ hθrate)
  · intro σ hσ
    exact Finset.le_sup (s := B₀) (f := f) hσ

/-- The accepted finite-row separation lemma chooses one tolerance before the
true model. For this single generated policy, a positive exponential range and
finite bound at every rate in that range are common to the whole admitted set. -/
theorem generated_actual_badCount_exists_common_exponential_range
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority = fun σ => coBuchiPriority (bad σ))
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (d : State × Action) :
    ∃ ε : ℝ, 0 < ε ∧ ∃ rate : ℝ, 0 < rate ∧
      (∀ σ ∈ B₀, ∀ᵐ H ∂markovHistoryLaw P σ s₀
        (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε)) (Measure.dirac ()),
        badCount (bad σ) (historyAction d H) < ⊤) ∧
      ∀ θ : ℝ, 0 ≤ θ → θ < rate → ∃ K : ℝ≥0∞, K < ⊤ ∧ ∀ σ ∈ B₀,
        (∫⁻ H, ENNReal.ofReal (Real.exp (θ * (badCount (bad σ) (historyAction d H)).toReal))
          ∂markovHistoryLaw P σ s₀
            (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε)) (Measure.dirac ())) ≤ K := by
  obtain ⟨ε, hε, hSep⟩ := finite_row_separation P B₀
  refine ⟨ε, hε, ?_⟩
  exact generated_actual_badCount_common_finite_exponential_bound P menu priority B₀ s₀
    fallback fallbackAction ε bad hpriority hε hs₀
    (fun σ hσ τ hτ e hne => hSep τ hτ σ hσ e hne) d

end HiddenParity.Cost
