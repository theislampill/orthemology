import ActualCostMoments

noncomputable section
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage
universe u v w
variable {State Action : Type u} {Model : Type w} {R : Type v}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]
variable [MeasurableSpace R]

/-- Common lawful finite-mean policy in the same seeded/history interface as the
accepted semantic winning definition. Nonempty support excludes vacuous winners. -/
structure FiniteCostPolicy (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (d : State × Action) (B : Finset Model) (s₀ : State) where
  nonempty : B.Nonempty
  seedLaw : Measure R
  probability : IsProbabilityMeasure seedLaw
  policy : R → History Action State → Action
  measurable : Measurable (fun z : R × History Action State => policy z.1 z.2)
  lawful : Lawful P menu B s₀ policy seedLaw
  finiteMean : ∀ σ ∈ B, (∫⁻ H,badCount (bad σ) (historyAction d H)
    ∂markovHistoryLaw P σ s₀ policy seedLaw) < ⊤

namespace FiniteCostPolicy

/-- Finite mean implies actual a.s. coBüchi for any permitted private seed law;
this direction makes no claim that arbitrary a.s.-winning policies have moments. -/
def toWinning
    {P : RationalKernel Model (State × Action) State}
    {menu : Finset Model → State → Finset Action}
    {bad : Model → (State × Action) → Prop} [∀ σ,DecidablePred (bad σ)]
    {d : State × Action} {B : Finset Model} {s₀ : State}
    (w : FiniteCostPolicy (R := R) P menu bad d B s₀) :
    WinningPolicy (R := R) P menu (fun σ => coBuchiPriority (bad σ)) d B s₀ := by
  refine ⟨w.nonempty,w.seedLaw,w.probability,w.policy,w.measurable,w.lawful,?_⟩
  intro σ hσ
  have hf := w.finiteMean σ hσ
  have hm : Measurable (fun H : ℕ → History (State × Action) State => badCount (bad σ) (historyAction d H)) :=
    (badCount_measurable (bad σ)).comp (historyAction_measurable d)
  filter_upwards [ae_lt_top hm hf.ne] with H hH
  exact (cobuchi_parity_iff_badCount_finite (bad σ) (historyAction d H)).mpr hH

end FiniteCostPolicy

/-- Source-generated deterministic policy with all natural moments for every
live true model simultaneously. The source's single finite tolerance and choices
are made before σ is quantified; the model is never given to the controller. -/
theorem computed_region_has_all_moment_policy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (B : Finset Model) (s₀ : State) (d : State × Action)
    (hs₀ : s₀ ∈ winningRegion P menu (fun σ => coBuchiPriority (bad σ)) B) :
    ∃ w : FiniteCostPolicy (R := Unit) P menu bad d B s₀,
      ∀ σ ∈ B, ∀ k:ℕ,(∫⁻ H,badCount (bad σ) (historyAction d H)^k
        ∂markovHistoryLaw P σ s₀ w.policy w.seedLaw) < ⊤ := by
  let priority := fun σ => coBuchiPriority (bad σ)
  have hB := winningRegion_mem_support_nonempty P menu priority B s₀ hs₀
  obtain ⟨fallback,hFallback⟩ := hB
  have hAvail := winningRegion_safe_action_available P menu priority B ⟨fallback,hFallback⟩ s₀ hs₀
  obtain ⟨e,he,hes⟩ := Finset.mem_image.mp hAvail
  obtain ⟨ε,hε,hSep⟩ := finite_row_separation P B
  let π := generatedPhasePolicy P menu priority B s₀ fallback e.2 (empiricalReject P ε)
  have hAll : ∀ σ ∈ B,∀ k:ℕ,(∫⁻ H,badCount (bad σ) (historyAction d H)^k
      ∂markovHistoryLaw P σ s₀ π (Measure.dirac ())) < ⊤ := by
    intro σ hσ k
    exact generated_actual_badCount_all_moments P menu priority B s₀ fallback e.2 ε bad rfl hε
      hs₀ σ hσ (fun θ hθ a hNe => hSep θ hθ σ hσ a hNe) d k
  let w : FiniteCostPolicy (R := Unit) P menu bad d B s₀ :=
    ⟨⟨fallback,hFallback⟩,Measure.dirac (),inferInstance,π,
      generatedPhasePolicy_measurable P menu priority B s₀ fallback e.2 (empiricalReject P ε),
      generatedPhasePolicy_lawful P menu priority B s₀ hs₀ fallback e.2 (empiricalReject P ε),
      fun σ hσ => by simpa only [pow_one] using hAll σ hσ 1⟩
  exact ⟨w,hAll⟩

/-- Computed coBüchi region equals the common lawful finite-expected-bad-visit
region. This is an existence characterization, not a claim about all winning
policies, and the witnessing policy is the unchanged generated source. -/
theorem computed_region_iff_finiteMean_policy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (B : Finset Model) (s₀ : State) (d : State × Action) :
    s₀ ∈ winningRegion P menu (fun σ => coBuchiPriority (bad σ)) B ↔
      Nonempty (FiniteCostPolicy (R := Unit) P menu bad d B s₀) := by
  constructor
  · intro hs
    obtain ⟨w,_⟩ := computed_region_has_all_moment_policy P menu bad B s₀ d hs
    exact ⟨w⟩
  · rintro ⟨w⟩
    exact winning_policy_mem_winningRegion P menu (fun σ => coBuchiPriority (bad σ)) d B s₀ w.toWinning

/-- Allowing an arbitrary measurable private seed cannot enlarge the finite
mean region; every such witness has a deterministic all-moments replacement. -/
theorem arbitrary_seed_finiteMean_has_all_moment_witness
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (B : Finset Model) (s₀ : State) (d : State × Action)
    (w : FiniteCostPolicy (R := R) P menu bad d B s₀) :
    ∃ v : FiniteCostPolicy (R := Unit) P menu bad d B s₀,
      ∀ σ ∈ B,∀ k:ℕ,(∫⁻ H,badCount (bad σ) (historyAction d H)^k
        ∂markovHistoryLaw P σ s₀ v.policy v.seedLaw) < ⊤ := by
  exact computed_region_has_all_moment_policy P menu bad B s₀ d
    (winning_policy_mem_winningRegion P menu (fun σ => coBuchiPriority (bad σ)) d B s₀ w.toWinning)

end HiddenParity.Cost
