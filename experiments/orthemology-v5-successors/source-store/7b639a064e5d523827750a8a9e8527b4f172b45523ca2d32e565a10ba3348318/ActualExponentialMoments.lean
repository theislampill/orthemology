import GeneratedExponentialTail
import ActualCostMoments
import AffineTailOptimization
import TailMoments

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
open HiddenParity.Necessity HiddenParity.Stage

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

/-- Actual generated-cost affine tail. The stochastic tail is derived from the
actual stopped-slot product theorem; it is not an input premise. -/
theorem generated_stack_badCount_affine_tail_of_margin
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ))
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (η : ℝ) (hηpos : 0 < η) (hη : η ≤ ε)
    (hSep : ∀ θ ∈ B₀,∀ e,P.row θ e ≠ P.row σ e → ∃ y,ε+η ≤ |realRows P σ e y-realRows P θ e y|) :
    ∃ B V : ℝ,0 < V ∧ ∀ u : ℝ,0 ≤ u →
      ((Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ)
        (realRows_normalized P σ))) {z | ENNReal.ofReal (B+V*u) < badCount (bad σ) (x z)} ≤
        ENNReal.ofReal (Real.exp (-u)) := by
  obtain ⟨p,hp,hp1,hmin⟩ := finite_positive_entry_bound (realRows P σ)
  let q := Fintype.card (State × Action)
  let m := B₀.card
  let D := FrozenRotor.dimension State Action
  let α := q+2*m
  let β := q*(m-1)+2*m*m
  let c := (min η 1)^2/2
  let A : ℝ := (q:ℝ)*(Fintype.card State:ℝ)*2/(1-Real.exp (-c))
  let lam := Real.log (2/(1+(1-p^D)))
  let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
  have hm : 0 < m := Finset.card_pos.mpr ⟨σ,hσ⟩
  have hAction : 0 < Fintype.card Action := Fintype.card_pos_iff.mpr ⟨fallbackAction⟩
  have hD : 0 < D := Nat.mul_pos Fintype.card_pos (pow_pos hAction _)
  have hDr : (0:ℝ) < D := by exact_mod_cast hD
  have hc : 0 < c := by dsimp [c];have h := lt_min hηpos (show (0:ℝ) < 1 by norm_num);positivity
  have hden : 0 < 1-Real.exp (-c) := by have := Real.exp_lt_one_iff.mpr (show -c < 0 by linarith);linarith
  have hq : 1 ≤ (q:ℝ) := by
    have hn : 0 < q := by
      dsimp [q]
      rw [Fintype.card_prod]
      exact Nat.mul_pos Fintype.card_pos hAction
    exact_mod_cast (show 1 ≤ q by omega)
  have hs : 1 ≤ (Fintype.card State:ℝ) := by exact_mod_cast (show 1 ≤ Fintype.card State from Fintype.card_pos)
  have hA : 1 ≤ A := by
    dsimp [A]
    apply (le_div_iff₀ hden).mpr
    have hnum : 1 ≤ (q:ℝ)*(Fintype.card State:ℝ) := by nlinarith
    have he := Real.exp_pos (-c)
    nlinarith
  have hpD : 0 < p^D := pow_pos hp D
  have hpD1 : p^D ≤ 1 := pow_le_one₀ hp.le hp1
  have hlam : 0 < lam := by
    apply Real.log_pos
    apply (lt_div_iff₀ (by linarith : (0:ℝ) < 1+(1-p^D))).mpr
    linarith
  have hJ : ∀ N:ℕ,q*(N+m-1)+2*m*(N+m)=α*N+β := by
    intro N
    dsimp [α,β]
    rw [Nat.add_sub_assoc (by omega : 1 ≤ m)]
    ring
  let B := Orthemology.AffineTail.offset (D:ℝ) lam (α:ℝ) (β:ℝ) A c
  let V := Orthemology.AffineTail.slope (D:ℝ) lam (α:ℝ) c
  have hV : 0 < V := by
    dsimp [V,Orthemology.AffineTail.slope]
    have hlog : 0 < Real.log 2 := Real.log_pos (by norm_num)
    positivity
  refine ⟨B,V,hV,?_⟩
  apply Orthemology.AffineTail.optimized_affine_tail
    (fun t => μ {z | ENNReal.ofReal t < badCount (bad σ) (x z)})
    (D:ℝ) lam (α:ℝ) (β:ℝ) A c hDr hlam (by positivity) (by positivity) hA hc
  intro N hN t ht
  have hb := actual_generated_badCount_exponential_cutoff_tail P menu priority B₀ s₀ fallback fallbackAction (ε/2)
    bad hpriority hs₀ σ hσ η hηpos hη hSep p hp hp1 hmin N (by omega) t ht
  change μ {z | ENNReal.ofReal t < badCount (bad σ) (x z)} ≤
    ENNReal.ofReal ((q:ℝ)*(Fintype.card State:ℝ)*(2*Real.exp (-(N:ℝ)*c)/(1-Real.exp (-c))))+
    ENNReal.ofReal ((2:ℝ)^(q*(N+m-1)+2*m*(N+m))*Real.exp (-(lam*t/(D:ℝ)))) at hb
  rw [hJ N] at hb
  apply hb.trans_eq
  rw [← ENNReal.ofReal_add (by positivity) (by positivity)]
  congr 1
  have he : Real.exp (((α:ℝ)*(N:ℝ)+β)*Real.log 2-lam*t/(D:ℝ)) =
      (2:ℝ)^(α*N+β)*Real.exp (-(lam*t/(D:ℝ))) := by
    rw [show (α:ℝ)*(N:ℝ)+β=((α*N+β:ℕ):ℝ) by push_cast;rfl,
      sub_eq_add_neg,Real.exp_add,Real.exp_nat_mul,Real.exp_log (by norm_num : (0:ℝ)<2)]
  rw [he]
  dsimp [A]
  rw [show -(N:ℝ)*c = -c*(N:ℝ) by ring]
  ring

/-- Positive exponential range for the unchanged actual generated stack count.
The original tolerance/separation assumptions suffice; the analysis margin and
positive transition minimum are derived from the finite input. Finiteness is
stated alongside toReal, so infinite counts cannot be hidden by that conversion. -/
theorem generated_stack_badCount_positive_exponential_moments
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ)) (hε : 0 < ε)
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (hSep : ∀ θ ∈ B₀,∀ e,P.row θ e ≠ P.row σ e → ∃ y,ε < |realRows P σ e y-realRows P θ e y|) :
    ∃ rate : ℝ,0 < rate ∧
      (∫⁻ z,badCount (bad σ) (x z) ∂(Measure.dirac ()).prod
        (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))) < ⊤ ∧
      (∀ᵐ z ∂(Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ)
        (realRows_normalized P σ)),badCount (bad σ) (x z) < ⊤) ∧
      ∀ θ : ℝ,0 ≤ θ → θ < rate →
        (∫⁻ z,ENNReal.ofReal (Real.exp (θ*(badCount (bad σ) (x z)).toReal)) ∂
          (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ)
            (realRows_normalized P σ))) < ⊤ := by
  obtain ⟨η,hη,hηε,hs⟩ := finite_test_margin P B₀ σ ε hε hSep
  obtain ⟨B,V,hV,htail⟩ := generated_stack_badCount_affine_tail_of_margin P menu priority B₀ s₀ fallback fallbackAction ε
    bad hpriority hs₀ σ hσ η hη hηε.le (by intro θ hθ e hne;obtain ⟨y,hy⟩ := hs θ hθ e hne;exact ⟨y,hy.le⟩)
  have hC : Measurable (fun z => badCount (bad σ) (x z)) :=
    (badCount_measurable (bad σ)).comp (stackActionTrajectory_measurable
      (pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject))
      (pairPolicy_measurable s₀ _ (generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject)))
  obtain ⟨hmean,hfinite,hexp⟩ := Orthemology.TailMoments.affine_tail_finite_moments
    ((Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ)
      (realRows_normalized P σ))) _ hC B V hV htail
  exact ⟨1/V,by positivity,hmean,hfinite,hexp⟩

/-- The complete accepted action-law identity transports the exponential cost
integrand, including the first executed action, rather than only a parity event. -/
theorem generated_badCount_exponential_eq_stack
    (σ : Model) (bad : (State × Action) → Prop) [DecidablePred bad]
    (d : State × Action) (θ : ℝ) :
    (∫⁻ H,ENNReal.ofReal (Real.exp (θ*(badCount bad (historyAction d H)).toReal))
      ∂markovHistoryLaw P σ s₀
        (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ())) =
    ∫⁻ z,ENNReal.ofReal (Real.exp (θ*(badCount bad (x z)).toReal))
      ∂(Measure.dirac ()).prod (stackMeasure (realRows P σ)
        (realRows_nonnegative P σ) (realRows_normalized P σ)) := by
  let π := generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject
  have hπ := generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject
  have hpair := pairPolicy_measurable s₀ π hπ
  let f : (ℕ → State × Action) → ℝ≥0∞ := fun w => ENNReal.ofReal (Real.exp (θ*(badCount bad w).toReal))
  have hf : Measurable f := ((measurable_const.mul (badCount_measurable bad).ennreal_toReal).exp).ennreal_ofReal
  change (∫⁻ H,f (historyAction d H) ∂markovHistoryLaw P σ s₀ π (Measure.dirac ())) = _
  rw [← lintegral_map hf (historyAction_measurable d)]
  change (∫⁻ w,f w ∂actionLaw (pairPolicy s₀ π) (Measure.dirac ())
    (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) d) = _
  rw [← stackActionTrajectory_law (pairPolicy s₀ π) hpair (Measure.dirac ())
    (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) d,
    lintegral_map hf (stackActionTrajectory_measurable (pairPolicy s₀ π) hpair)]
  rfl

/-- Actual canonical-history positive exponential moments for the original
Unit-seed generated policy. This does not assert such moments for arbitrary
private-seed policies, nor does it replace the count by physical elapsed time. -/
theorem generated_actual_badCount_positive_exponential_moments
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ)) (hε : 0 < ε)
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (hSep : ∀ θ ∈ B₀,∀ e,P.row θ e ≠ P.row σ e → ∃ y,ε < |realRows P σ e y-realRows P θ e y|)
    (d : State × Action) :
    ∃ rate : ℝ,0 < rate ∧
      (∀ᵐ H ∂markovHistoryLaw P σ s₀
        (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ()),
        badCount (bad σ) (historyAction d H) < ⊤) ∧
      ∀ θ : ℝ,0 ≤ θ → θ < rate →
        (∫⁻ H,ENNReal.ofReal (Real.exp (θ*(badCount (bad σ) (historyAction d H)).toReal))
          ∂markovHistoryLaw P σ s₀
            (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ())) < ⊤ := by
  obtain ⟨rate,hrate,hmean,hfinite,hexp⟩ := generated_stack_badCount_positive_exponential_moments
    P menu priority B₀ s₀ fallback fallbackAction ε bad hpriority hε hs₀ σ hσ hSep
  have hm := generated_actual_badCount_all_moments P menu priority B₀ s₀ fallback fallbackAction ε
    bad hpriority hε hs₀ σ hσ hSep d 1
  simp only [pow_one] at hm
  refine ⟨rate,hrate,ae_lt_top ((badCount_measurable (bad σ)).comp (historyAction_measurable d)) hm.ne,?_⟩
  intro θ hθ hθrate
  rw [generated_badCount_exponential_eq_stack]
  exact hexp θ hθ hθrate

end HiddenParity.Cost
