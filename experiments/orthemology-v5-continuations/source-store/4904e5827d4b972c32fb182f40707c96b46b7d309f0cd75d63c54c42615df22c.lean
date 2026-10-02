import GeneratedPrefixProduct
import ActualTotalCostTail
import Mathlib.MeasureTheory.Integral.Lebesgue.Markov

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
open HiddenParity.Necessity HiddenParity.Stage

/-- Rounded block charges dominate the exponential of the physical dangerous
cost. The inequality is deterministic; the exponential product need not have
independent factors. -/
theorem exponential_count_le_block_product (L : ℕ → ℕ) (J D count : ℕ)
    (hD : 0 < D) (hCount : count ≤ ∑ j ∈ Finset.range J,L j)
    (a : ℝ) (ha : 1 ≤ a) :
    ENNReal.ofReal (Real.exp (Real.log a*(count:ℝ)/(D:ℝ))) ≤ 
      ∏ j ∈ Finset.range J,ENNReal.ofReal a^(L j ⌈/⌉ D) := by
  have ha0 : 0 < a := lt_of_lt_of_le zero_lt_one ha
  let S := ∑ j ∈ Finset.range J,L j ⌈/⌉ D
  have hn : count ≤ D*S := by
    apply hCount.trans
    dsimp [S]
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro j hj
    exact le_smul_ceilDiv hD
  have hDr : (0:ℝ) < D := by exact_mod_cast hD
  have hh : (count:ℝ)/(D:ℝ) ≤ (S:ℝ) := (div_le_iff₀ hDr).mpr (by exact_mod_cast (show count≤S*D by simpa only [Nat.mul_comm] using hn))
  rw [Finset.prod_pow_eq_pow_sum,← ENNReal.ofReal_pow ha0.le]
  apply ENNReal.ofReal_le_ofReal
  have he : Real.exp (Real.log a*(S:ℝ))=a^S := by rw [mul_comm,Real.exp_nat_mul,Real.exp_log ha0]
  rw [← he]
  apply Real.exp_le_exp.mpr
  rw [mul_div_assoc]
  exact mul_le_mul_of_nonneg_left hh (Real.log_nonneg ha)

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
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject
local notation "progress" => runProgress P menu priority B₀ s₀ fallback fallbackAction reject
local notation "L" => runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε

/-- The actual finite bad-count is covered by the first J_N dangerous slot
lengths, with all zero-cost physical gaps retained in the original path. -/
theorem accurate_bad_prefix_le_slot_sum
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ))
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (η : ℝ) (hη : η ≤ ε) (N T : ℕ)
    (hSep : ∀ θ ∈ B₀,∀ e,P.row θ e ≠ P.row σ e → ∃ y,ε+η ≤ |realRows P σ e y-realRows P θ e y|)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k,0 < realRows P σ e (z.2 (e,k)))
    (hAcc : ∀ t,t < T → HistoryAccurate P σ η N (H z t)) :
    let J := Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card)
    ((Finset.range T).filter (fun t => bad σ (x z t))).card ≤ ∑ j ∈ Finset.range J,L σ T j z := by
  dsimp only
  let J := Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card)
  let S := fun j => (Finset.range T).filter (fun t => progressCount (progress σ z) t=j ∧
    historyDanger P menu priority B₀ s₀ fallback reject σ (H z t))
  have hJ : (truncatedProgressEnds (progress σ z) T).card ≤ J := by
    rw [truncatedProgressEnds_eq_generatedCharges]
    exact accurate_generated_charge_budget P menu priority B₀ s₀ fallback fallbackAction ε σ η hη N T
      hs₀ hσ hSep z hSupported hAcc
  have hsub : (Finset.range T).filter (fun t => bad σ (x z t))⊆(Finset.range J).biUnion S := by
    intro t ht
    obtain ⟨htT,hbad⟩ := Finset.mem_filter.mp ht
    have hj := (progressCount_lt_endpoint_card (progress σ z) t T (Finset.mem_range.mp htT)).trans_le hJ
    refine Finset.mem_biUnion.mpr ⟨progressCount (progress σ z) t,Finset.mem_range.mpr hj,?_⟩
    exact Finset.mem_filter.mpr ⟨htT,rfl,bad_action_implies_danger P menu priority B₀ s₀ fallback fallbackAction ε
      bad hpriority hs₀ σ hσ z hSupported t hbad⟩
  exact (Finset.card_le_card hsub).trans Finset.card_biUnion_le

/-- End-to-end exponential two-term tail of the actual generated bad count.
The product is over actual bounded-horizon chronological slots; continuity from
below handles infinite total cost without assuming a.s. finiteness. -/
theorem actual_generated_badCount_exponential_cutoff_tail
    (bad : Model → (State × Action) → Prop) [∀ σ,DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ))
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (η : ℝ) (hηpos : 0 < η) (hη : η ≤ ε)
    (hSep : ∀ θ ∈ B₀,∀ e,P.row θ e ≠ P.row σ e → ∃ y,ε+η ≤ |realRows P σ e y-realRows P θ e y|)
    (p : ℝ) (hp : 0 < p) (hp1 : p ≤ 1)
    (hmin : ∀ e y,0 < realRows P σ e y → p ≤ realRows P σ e y)
    (N : ℕ) (hN : 0 < N) (t : ℝ) (ht : 0 ≤ t) :
    let J := Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card)
    let D := FrozenRotor.dimension State Action
    let c := (min η 1)^2/2
    let lam := Real.log (2/(1+(1-p^D)))
    let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
    μ {z | ENNReal.ofReal t < badCount (bad σ) (x z)} ≤ 
      ENNReal.ofReal ((Fintype.card (State × Action):ℝ)*(Fintype.card State:ℝ)*
        (2*Real.exp (-(N:ℝ)*c)/(1-Real.exp (-c)) ))+
      ENNReal.ofReal ((2:ℝ)^J*Real.exp (-(lam*t/(D:ℝ)))) := by
  dsimp only
  let J := Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card)
  let D := FrozenRotor.dimension State Action
  let a := 2/(1+(1-p^D))
  let lam := Real.log a
  let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
  let raw := RawTailDeviation (R := Unit) (realRows P σ) η N
  let count := fun T z => ((Finset.range T).filter (fun i => bad σ (x z i))).card
  let E := fun T => {z | ENNReal.ofReal t < (count T z:ℝ≥0∞)}∩rawᶜ
  have hD : 0 < D := Nat.mul_pos Fintype.card_pos
    (pow_pos (Fintype.card_pos_iff.mpr (show Nonempty Action from ⟨fallbackAction⟩)) _)
  have hDr : (0:ℝ) < D := by exact_mod_cast hD
  have hq : 0 ≤ 1-p^D := sub_nonneg.mpr (pow_le_one₀ hp.le hp1)
  have ha : 1 < a := by
    dsimp [a]
    apply (lt_div_iff₀ (by linarith : (0:ℝ) < 1+(1-p^D))).mpr
    have := pow_pos hp D
    linarith
  have hlam : 0 < lam := Real.log_pos ha
  have hm : Monotone E := by
    intro T U hTU z hz
    have hc : count T z ≤ count U z := Finset.card_le_card
      (Finset.filter_subset_filter _ (Finset.range_mono hTU))
    exact ⟨(show ENNReal.ofReal t<(count T z:ℝ≥0∞) from hz.1).trans_le
      (show (count T z:ℝ≥0∞)≤(count U z:ℝ≥0∞) by exact_mod_cast hc),hz.2⟩
  have hFinite (T:ℕ) : μ (E T) ≤ ENNReal.ofReal ((2:ℝ)^J*Real.exp (-(lam*t/(D:ℝ)))) := by
    let F := fun z => ∏ j ∈ Finset.range J,ENNReal.ofReal a^(L σ T j z ⌈/⌉ D)
    have hF : Measurable F := Finset.measurable_prod _ (fun j hj =>
      (measurable_of_countable (fun n:ℕ => ENNReal.ofReal a^(n ⌈/⌉ D))).comp
        (runSlotLength_measurable P menu priority B₀ s₀ fallback fallbackAction ε σ T j))
    have hInclude : ∀ᵐ z ∂μ,z ∈ E T → ENNReal.ofReal (Real.exp (lam*t/(D:ℝ))) ≤ F z := by
      filter_upwards [seeded_all_tapes_supported (Measure.dirac ()) (realRows P σ)
        (realRows_nonnegative P σ) (realRows_normalized P σ)] with z hSupported
      rintro ⟨hCost,hRaw⟩
      have hAcc := all_histories_accurate_of_raw_good P menu priority B₀ s₀ fallback fallbackAction ε σ η N z hRaw
      have hc := accurate_bad_prefix_le_slot_sum P menu priority B₀ s₀ fallback fallbackAction ε
        bad hpriority hs₀ σ hσ η hη N T hSep z hSupported (by intro i hi;exact hAcc i)
      have he := exponential_count_le_block_product (fun j => L σ T j z) J D (count T z) hD hc a ha.le
      have htr : t < (count T z:ℝ) := by
        change ENNReal.ofReal t<(count T z:ℝ≥0∞) at hCost
        rw [← ENNReal.ofReal_natCast] at hCost
        exact (ENNReal.ofReal_lt_ofReal_iff_of_nonneg ht).mp hCost
      apply le_trans (ENNReal.ofReal_le_ofReal (Real.exp_le_exp.mpr ?_)) he
      exact div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_left htr.le hlam.le) hDr.le
    have hMarkov := meas_ge_le_lintegral_div (μ := μ) hF.aemeasurable
      (ENNReal.ofReal_ne_zero_iff.mpr (Real.exp_pos (lam*t/(D:ℝ)))) ENNReal.ofReal_ne_top
    have hProd := actual_generated_slot_product_bound P menu priority B₀ s₀ fallback fallbackAction ε
      hs₀ σ hσ p hp hp1 hmin T J
    apply (measure_mono_ae hInclude).trans (hMarkov.trans ((ENNReal.div_le_div_right hProd _).trans_eq ?_))
    have htwo : (2:ℝ≥0∞)^J=ENNReal.ofReal ((2:ℝ)^J) := by rw [ENNReal.ofReal_pow (by norm_num)];norm_num
    rw [htwo,← ENNReal.ofReal_div_of_pos (Real.exp_pos _)]
    congr 1
    rw [div_eq_mul_inv,← Real.exp_neg]
  have hUnion : μ (⋃ T,E T) ≤ ENNReal.ofReal ((2:ℝ)^J*Real.exp (-(lam*t/(D:ℝ)))) := by
    rw [hm.measure_iUnion]
    exact iSup_le hFinite
  have hsub : {z | ENNReal.ofReal t < badCount (bad σ) (x z)}⊆raw∪⋃ T,E T := by
    intro z hz
    by_cases hr : z ∈ raw
    · exact Or.inl hr
    · change ENNReal.ofReal t<badCount (bad σ) (x z) at hz
      rw [badCount_eq_iSup_prefix] at hz
      obtain ⟨T,hT⟩ := lt_iSup_iff.mp hz
      exact Or.inr (Set.mem_iUnion.mpr ⟨T,hT,hr⟩)
  exact (measure_mono hsub).trans ((measure_union_le _ _).trans (add_le_add
    (HiddenParity.Exponential.seeded_rawTailDeviation_exponential_all_positive (Measure.dirac ())
      (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) N hN hηpos) hUnion))

end HiddenParity.Cost
