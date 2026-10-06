import GeneratedSlotLengths

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
open HiddenParity.Necessity HiddenParity.Stage HiddenParity.ResidualSeed
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
local notation "π" => pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)
local notation "L" => runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε

/-- Uniform exponential factor bound on an actual dangerous starting-history
cylinder. The duration is the literal finite-horizon chronological slot count;
its conditional tail is derived from source alignment, not supplied. -/
theorem generated_slot_prefix_moment
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (T j : ℕ) (base : History (State × Action) State)
    (hstart : historyIsStart P menu priority B₀ s₀ fallback reject σ base)
    (hj : historyProgressCount P menu priority B₀ s₀ fallback reject σ base=j)
    (hdanger : historyDanger P menu priority B₀ s₀ fallback reject σ base)
    (p : ℝ) (hp : 0 < p) (hp1 : p ≤ 1)
    (hmin : ∀ e y,0 < realRows P σ e y → p ≤ realRows P σ e y) :
    let D := FrozenRotor.dimension State Action
    let q := 1-p^D
    let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
    (∫⁻ z in {z | H z base.length=base},ENNReal.ofReal (2/(1+q))^(L σ T j z ⌈/⌉ D) ∂μ)
       ≤ 2*μ {z | H z base.length=base} := by
  dsimp only
  let D := FrozenRotor.dimension State Action
  let q := 1-p^D
  let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
  let E := {z | H z base.length=base}
  have hπ := pairPolicy_measurable s₀ _ (generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject)
  have hE : MeasurableSet E := (measurableSet_singleton base).preimage
    ((measurable_pi_apply base.length).comp (stackHistoryTrajectory_measurable π hπ))
  have hD : 0 < D := Nat.mul_pos Fintype.card_pos
    (pow_pos (Fintype.card_pos_iff.mpr (show Nonempty Action from ⟨fallbackAction⟩)) _)
  have hq : 0 ≤ q := sub_nonneg.mpr (pow_le_one₀ hp.le hp1)
  have hq1 : q < 1 := by have hr := pow_pos hp D;dsimp [q];linarith
  have ht (k:ℕ) : μ (E∩{z | k*D < L σ T j z}) ≤ μ E*ENNReal.ofReal (q^k) := by
    have hi : ∀ᵐ z ∂μ, z ∈ E∩{z | k*D < L σ T j z} →
        z ∈ E∩{z | historySlice P menu priority B₀ s₀ fallback reject σ base
          (runTail P menu priority B₀ s₀ fallback fallbackAction reject z base.length (k*D))} := by
      filter_upwards [seeded_all_tapes_supported (Measure.dirac ()) (realRows P σ)
        (realRows_nonnegative P σ) (realRows_normalized P σ)] with z hSupported
      rintro ⟨hbase,hLong⟩
      exact ⟨hbase,runSlotLength_long_implies_slice P menu priority B₀ s₀ fallback fallbackAction ε
        hs₀ σ hσ T j (k*D) base hstart hj z hSupported hbase hLong⟩
    exact (measure_mono_ae hi).trans (stack_historySlice_inter_bound P menu priority B₀ s₀ fallback fallbackAction reject
      hs₀ σ hσ base hdanger p hp.le hp1 hmin k)
  by_cases hz : μ E=0
  · rw [Measure.restrict_eq_zero.mpr hz,lintegral_zero_measure,hz,mul_zero]
  · let ν := normalizedRestriction μ E
    haveI : IsProbabilityMeasure ν := ProbabilityTheory.cond_isProbabilityMeasure hz
    have htail : ∀ k:ℕ,ν {z | k*D < L σ T j z} ≤ ENNReal.ofReal (q^k) := by
      intro k
      dsimp [ν,normalizedRestriction]
      rw [Measure.restrict_apply' hE]
      change (μ E)⁻¹*μ ({z | k*D < L σ T j z}∩E) ≤ _
      rw [Set.inter_comm]
      calc
        _  ≤  (μ E)⁻¹*(μ E*ENNReal.ofReal (q^k)) := mul_le_mul_left' (ht k) _
        _ = _ := by rw [← mul_assoc,ENNReal.inv_mul_cancel hz (measure_ne_top μ E),one_mul]
    have hm := geometric_block_tail_factor_two ν (L σ T j)
      (runSlotLength_measurable P menu priority B₀ s₀ fallback fallbackAction ε σ T j) D hD q hq hq1 htail
    dsimp [ν,normalizedRestriction] at hm
    rw [lintegral_smul_measure] at hm
    simp only [smul_eq_mul] at hm
    have hh := mul_le_mul_left' hm (μ E)
    rw [← mul_assoc,ENNReal.mul_inv_cancel hz (measure_ne_top μ E),one_mul] at hh
    simpa only [mul_comm] using hh

end HiddenParity.Cost
