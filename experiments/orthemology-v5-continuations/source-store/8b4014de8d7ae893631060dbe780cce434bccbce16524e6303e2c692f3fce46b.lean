import ActualTotalCostTail
import PolynomialTailMoments
import GeneratedCostLaw

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
open HiddenParity.Necessity HiddenParity.Stage

/-- Every finite family of real entries has a strictly positive lower bound on
its positive entries. The empty-positive-set case is harmless and explicit. -/
theorem finite_positive_entry_bound {A Y : Type*} [Fintype A] [Fintype Y] (P : A → Y → ℝ) :
    ∃ p:ℝ,0 < p ∧ p ≤ 1 ∧ ∀ a y,0 < P a y → p ≤ P a y := by
  classical
  let vals : Finset ℝ := (Finset.univ : Finset (A × Y)).image (fun e => P e.1 e.2)
  let positive := vals.filter (fun x => 0 < x)
  by_cases hn : positive.Nonempty
  · have hp : 0 < positive.min' hn := (Finset.mem_filter.mp (Finset.min'_mem positive hn)).2
    refine ⟨min 1 (positive.min' hn),lt_min (by norm_num) hp,min_le_left _ _,?_⟩
    intro a y h
    have hm : P a y ∈ positive := Finset.mem_filter.mpr ⟨Finset.mem_image.mpr ⟨(a,y),Finset.mem_univ _,rfl⟩,h⟩
    exact (min_le_right _ _).trans (Finset.min'_le positive _ hm)
  · refine ⟨1,by norm_num,le_rfl,?_⟩
    intro a y h
    exact (hn ⟨P a y,Finset.mem_filter.mpr ⟨Finset.mem_image.mpr ⟨(a,y),Finset.mem_univ _,rfl⟩,h⟩⟩).elim

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
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject

/-- All natural moments of the actual generated stack cost, obtained from the
proved cutoff/union tail. No assumed a.s. cost finiteness or interval MGF is used. -/
theorem generated_stack_badCount_all_moments_of_margin
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ))
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (η : ℝ) (hηpos : 0 < η) (hη : η ≤ ε)
    (hSep : ∀ θ ∈ B₀,∀ e,P.row θ e ≠ P.row σ e → ∃ y,ε+η ≤ |realRows P σ e y-realRows P θ e y|) :
    ∀ k:ℕ,(∫⁻ z,badCount (bad σ) (x z)^k ∂
      (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))) < ⊤ := by
  obtain ⟨p,hp,hp1,hmin⟩ := finite_positive_entry_bound (realRows P σ)
  let q := Fintype.card (State × Action)
  let m := B₀.card
  let D := FrozenRotor.dimension State Action
  let α := q+2*m
  let β := q*(m-1)+2*m*m
  let c := (min η 1)^2/2
  let A : ℝ := (q:ℝ)*(Fintype.card State:ℝ)*2/(1-Real.exp (-c))
  let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
  have hm : 0 < m := Finset.card_pos.mpr ⟨σ,hσ⟩
  have hAction : 0 < Fintype.card Action := Fintype.card_pos_iff.mpr ⟨fallbackAction⟩
  have hD : 0 < D := Nat.mul_pos Fintype.card_pos (pow_pos hAction _)
  have hc : 0 < c := by dsimp [c];have h := lt_min hηpos (show (0:ℝ) < 1 by norm_num);positivity
  have hden : 0 < 1-Real.exp (-c) := by have := Real.exp_lt_one_iff.mpr (show -c < 0 by linarith);linarith
  have hαβ : 0 < (α:ℝ)+β := by
    have hn : 0 < α+β := by dsimp [α,β];omega
    exact_mod_cast hn
  have hJ : ∀ N:ℕ, q*(N+m-1)+2*m*(N+m)=α*N+β := by
    intro N
    dsimp [α,β]
    rw [Nat.add_sub_assoc (by omega : 1 ≤ m)]
    ring
  have hMeas : Measurable (fun z => badCount (bad σ) (x z)) :=
    (badCount_measurable (bad σ)).comp (stackActionTrajectory_measurable
      (pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject))
      (pairPolicy_measurable s₀ _ (generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject)))
  apply Orthemology.PolynomialTail.cutoff_union_tail_all_moments μ _ hMeas
    (D:ℝ) (α:ℝ) (β:ℝ) A c (p^D) (by exact_mod_cast hD) (by positivity) (by positivity)
    hαβ (by dsimp [A];positivity) hc (pow_pos hp _) (pow_le_one₀ hp.le hp1)
  intro N k hN hk
  have hb := actual_generated_badCount_cutoff_tail P menu priority B₀ s₀ fallback fallbackAction ε
    bad hpriority hs₀ σ hσ η hηpos hη hSep p hp.le hp1 hmin N k (by omega)
  change μ {z | ((q*(N+m-1)+2*m*(N+m))*(k*D):ℕ) < badCount (bad σ) (x z)} ≤ _ at hb
  rw [hJ N] at hb
  have hThreshold : ENNReal.ofReal ((D:ℝ)*(k:ℝ)*((α:ℝ)*(N:ℝ)+β))=
      (((α*N+β)*(k*D):ℕ):ℝ≥0∞) := by
    rw [show (D:ℝ)*(k:ℝ)*((α:ℝ)*(N:ℝ)+β)=(((α*N+β)*(k*D):ℕ):ℝ) by push_cast;ring]
    exact ENNReal.ofReal_natCast _
  rw [hThreshold]
  apply hb.trans_eq
  have hq : 0 ≤ 1-p^FrozenRotor.dimension State Action := sub_nonneg.mpr (pow_le_one₀ hp.le hp1)
  rw [← ENNReal.ofReal_natCast (α*N+β),← ENNReal.ofReal_mul (by positivity : (0:ℝ) ≤ ((α*N+β:ℕ):ℝ)),
    ← ENNReal.ofReal_add (by positivity) (by positivity)]
  congr 1
  dsimp [A,c,q,D] at *
  push_cast
  ring

/-- The original source tolerance hypotheses suffice; positive slack and a
positive transition lower bound are derived from the finite actual input. -/
theorem generated_stack_badCount_all_moments
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ)) (hε : 0 < ε)
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (hSep : ∀ θ ∈ B₀,∀ e,P.row θ e ≠ P.row σ e → ∃ y,ε < |realRows P σ e y-realRows P θ e y|) :
    ∀ k:ℕ,(∫⁻ z,badCount (bad σ) (x z)^k ∂
      (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))) < ⊤ := by
  obtain ⟨η,hη,hηε,hs⟩ := finite_test_margin P B₀ σ ε hε hSep
  exact generated_stack_badCount_all_moments_of_margin P menu priority B₀ s₀ fallback fallbackAction ε
    bad hpriority hs₀ σ hσ η hη hηε.le (by intro θ hθ e hne;obtain ⟨y,hy⟩ := hs θ hθ e hne;exact ⟨y,hy.le⟩)

/-- Exact actual-history-law all-moment theorem for the unchanged generated
controller. The accepted full cost-law identity transports every natural power,
including the first executed action and no synthetic initial charge. -/
theorem generated_actual_badCount_all_moments
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ)) (hε : 0 < ε)
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (hSep : ∀ θ ∈ B₀,∀ e,P.row θ e ≠ P.row σ e → ∃ y,ε < |realRows P σ e y-realRows P θ e y|)
    (d : State × Action) (k : ℕ) :
    (∫⁻ H,badCount (bad σ) (historyAction d H)^k ∂markovHistoryLaw P σ s₀
      (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ())) < ⊤ := by
  rw [generated_badCount_moment_eq_stack]
  exact generated_stack_badCount_all_moments P menu priority B₀ s₀ fallback fallbackAction ε
    bad hpriority hε hs₀ σ hσ hSep k

end HiddenParity.Cost
