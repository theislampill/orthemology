import GeneratedSlotMoment
import PrefixWeightedProduct

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal BigOperators Function
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
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "label" => generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction reject
local notation "progress" => runProgress P menu priority B₀ s₀ fallback fallbackAction reject
local notation "L" => runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε
local notation "π" => pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)

def BoundedDangerousStart (σ : Model) (T j : ℕ) :=
  {h : History (State × Action) State |
    historyIsStart P menu priority B₀ s₀ fallback reject σ h ∧
    historyProgressCount P menu priority B₀ s₀ fallback reject σ h=j ∧
    historyDanger P menu priority B₀ s₀ fallback reject σ h ∧ h.length < T}

/-- A nonzero dangerous slot has exactly the kind of finite observed start
used in the prefix-free product argument. This also discharges zero padding. -/
theorem positive_runSlotLength_has_start (σ : Model) (T j : ℕ)
    (z : Unit × FlatStack (State × Action) State) (hpos : 0 < L σ T j z) :
    ∃ h : BoundedDangerousStart P menu priority B₀ s₀ fallback ε σ T j,
      H z h.val.length=h.val := by
  unfold runSlotLength slotLength at hpos
  obtain ⟨t,ht⟩ := Finset.card_pos.mp hpos
  obtain ⟨htT,hidx,hdanger⟩ := Finset.mem_filter.mp ht
  have ht' := Finset.mem_range.mp htT
  let s := lastIntervalStart (progress σ z) t
  have hst : s ≤ t := lastIntervalStart_le (progress σ z) t
  have hs := lastIntervalStart_is_start (progress σ z) t
  have hpc : progressCount (progress σ z) s=j := (progressCount_at_lastStart (progress σ z) t).trans hidx
  have hHist : historyProgressCount P menu priority B₀ s₀ fallback reject σ (H z s)=j := by
    rw [historyProgressCount_run];exact hpc
  have hl : label z t=label z s := by
    have he := run_label_eq_of_no_progress P menu priority B₀ s₀ fallback fallbackAction reject σ z s (t-s)
      (by intro i his hit;exact no_progress_since_start (progress σ z) t i his (by omega))
    simpa only [Nat.add_sub_of_le hst] using he
  have hdStart : historyDanger P menu priority B₀ s₀ fallback reject σ (H z s) := by
    rw [← historyDanger_eq_of_label_eq P menu priority B₀ s₀ fallback ε σ (H z t) (H z s) hl]
    exact hdanger
  have hlen : (H z s).length=s := observedHistory_length _ _ _ _ _ _
  refine ⟨⟨H z s,(historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z s).mpr hs,
    hHist,hdStart,by rw [hlen];omega⟩,?_⟩
  change H z (H z s).length=H z s
  rw [hlen]

/-- Actual finite-horizon exponential product over chronological dangerous
slots. Complete old history determines all earlier factors, and a missing
future dangerous start contributes one. No independence is assumed. -/
theorem actual_generated_slot_product_bound
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (p : ℝ) (hp : 0 < p) (hp1 : p ≤ 1)
    (hmin : ∀ e y,0 < realRows P σ e y → p ≤ realRows P σ e y) (T J : ℕ) :
    let D := FrozenRotor.dimension State Action
    let a := ENNReal.ofReal (2/(1+(1-p^D)))
    (∫⁻ z,∏ j ∈ Finset.range J,a^(L σ T j z ⌈/⌉ D) ∂
      (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))) ≤ 2^J := by
  dsimp only
  let D := FrozenRotor.dimension State Action
  let a := ENNReal.ofReal (2/(1+(1-p^D)))
  let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
  let factor := fun j z => a^(L σ T j z ⌈/⌉ D)
  have hf (j:ℕ) : Measurable (factor j) :=
    (measurable_of_countable (fun n:ℕ => a^(n ⌈/⌉ D))).comp
      (runSlotLength_measurable P menu priority B₀ s₀ fallback fallbackAction ε σ T j)
  induction J with
  | zero => simp
  | succ J ih =>
      let I := BoundedDangerousStart P menu priority B₀ s₀ fallback ε σ T J
      let E := fun h:I => {z | H z h.val.length=h.val}
      let past := fun z => ∏ i ∈ Finset.range J,factor i z
      let value := fun h:I => ∏ i ∈ Finset.range J,
        a^(historySlotLength P menu priority B₀ s₀ fallback ε σ h.val i ⌈/⌉ D)
      have hπ := pairPolicy_measurable s₀ _ (generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject)
      have hE (h:I) : MeasurableSet (E h) := (measurableSet_singleton h.val).preimage
        ((measurable_pi_apply h.val.length).comp (stackHistoryTrajectory_measurable π hπ))
      have hd : Pairwise (Disjoint on E) := by
        intro h g hne
        apply Set.disjoint_left.mpr
        intro z hh hg
        have hsh := (historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z h.val.length).mp
          (hh.symm ▸ h.property.1)
        have hsg := (historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z g.val.length).mp
          (hg.symm ▸ g.property.1)
        have hch := historyProgressCount_run P menu priority B₀ s₀ fallback fallbackAction reject σ z h.val.length
        have hcg := historyProgressCount_run P menu priority B₀ s₀ fallback fallbackAction reject σ z g.val.length
        rw [hh,h.property.2.1] at hch
        rw [hg,g.property.2.1] at hcg
        have he := start_eq_of_progressCount_eq (progress σ z) h.val.length g.val.length hsh hsg (hch.symm.trans hcg)
        apply hne;apply Subtype.ext;exact hh.symm.trans (he ▸ hg)
      have hPast : Measurable past := by
        exact Finset.measurable_prod _ (fun i hi => hf i)
      have hknown : ∀ h:I,∀ z,z ∈ E h → past z=value h := by
        intro h z hz
        apply Finset.prod_congr rfl
        intro i hi
        dsimp only [factor]
        rw [runSlotLength_prior_known P menu priority B₀ s₀ fallback fallbackAction ε σ T J i
          (Finset.mem_range.mp hi) h.val h.property.2.2.2.le h.property.2.1 z hz]
      have hbound : ∀ h:I,(∫⁻ z in E h,factor J z ∂μ) ≤ 2*μ (E h) := by
        intro h
        exact generated_slot_prefix_moment P menu priority B₀ s₀ fallback fallbackAction ε hs₀ σ hσ T J h.val
          h.property.1 h.property.2.1 h.property.2.2.1 p hp hp1 hmin
      have hOutside : ∀ z,z ∉ ⋃ h:I,E h → factor J z=1 := by
        intro z hz
        have hzero : L σ T J z=0 := by
          by_contra hn
          obtain ⟨h,hh⟩ := positive_runSlotLength_has_start P menu priority B₀ s₀ fallback fallbackAction ε σ T J z
            (Nat.pos_of_ne_zero hn)
          exact hz (Set.mem_iUnion.mpr ⟨h,hh⟩)
        simp only [factor,hzero,zero_ceilDiv,pow_zero]
      have hb := prefix_family_weighted_bound μ E hE hd past (factor J) hPast (hf J) value hknown
        2 (by norm_num) hbound hOutside
      simp only [Finset.prod_range_succ]
      exact hb.trans (by simpa only [pow_succ,mul_comm] using mul_le_mul_left' ih 2)

end HiddenParity.Cost
