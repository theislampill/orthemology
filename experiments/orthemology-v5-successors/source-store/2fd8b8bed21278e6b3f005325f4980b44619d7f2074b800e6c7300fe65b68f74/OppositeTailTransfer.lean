import NontrivialFixture
set_option autoImplicit false

noncomputable section
namespace Orthemology.Eighth.SemanticControls
open MeasureTheory Filter Set
open scoped ENNReal
open HiddenParity HiddenParity.Stochastic HiddenParity.Adaptive
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open Orthemology.Tranche3.RelativeTransfer
open Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.PhaseUpdate.FullController

/-- The nontrivial objective really requires eventual permanent model-specific action. -/
theorem actionPriority_parity_iff (θ : Bool) (x : ℕ → Bool × Bool) :
    ParitySuccess (actionPriority θ) x ↔ ∀ᶠ n in atTop, (x n).2 = θ := by
  constructor
  · rintro ⟨d,⟨⟨f,hf,hfd⟩,hmin⟩,hd⟩
    have hd2 : d = 2 := by
      unfold actionPriority at hfd
      split_ifs at hfd <;> omega
    apply (eventually_mem_recurrentSet x).mono
    intro n hn
    have hh := hmin (x n) hn
    rw [hd2] at hh
    by_contra hnot
    simp [actionPriority,hnot] at hh
  · intro h
    have hsub : recurrentSet x ⊆ goodPairs θ := recurrentSet_subset_of_eventually_mem x _
      (h.mono (fun n hn => (mem_goodPairs θ (x n)).mpr hn))
    obtain ⟨f,hf⟩ := recurrentSet_nonempty x
    refine ⟨2,⟨⟨f,hf,?_⟩,?_⟩,by decide⟩
    · simp [actionPriority,(mem_goodPairs θ f).mp (hsub hf)]
    · intro e he
      simp [actionPriority,(mem_goodPairs θ e).mp (hsub he)]

def computedDecoder : Unit → History Bool Bool → Bool :=
  HistoryRuntime.historyPolicy (sourcePolicy (withComputedTolerance oldConfig))

theorem computedDecoder_exact : computedDecoder =
    fun (_ : Unit) h => policy (withComputedTolerance oldConfig) bothMenu actionPriority h := by
  funext u h
  cases u
  exact source_policy_retained_exact (withComputedTolerance oldConfig) bothMenu actionPriority
    (computed_tolerance_certificate oldConfig bothMenu actionPriority oldConfig_certificate) h

theorem computedDecoder_measurable :
    Measurable (fun z : Unit × History Bool Bool => computedDecoder z.1 z.2) := measurable_of_countable _

theorem computedDecoder_wins (θ : Bool) (d : Bool × Bool) :
    ∀ᵐ x ∂markovPairLaw fixtureKernel θ false computedDecoder (Measure.dirac ()) d,
      ParitySuccess (actionPriority θ) x := by
  have hw := computed_policy_parity oldConfig bothMenu actionPriority oldConfig_winning θ
    (show θ ∈ oldConfig.initialSupport from Finset.mem_univ _) d
  change ∀ᵐ H ∂markovHistoryLaw fixtureKernel θ false
      (fun (_ : Unit) h => policy (withComputedTolerance oldConfig) bothMenu actionPriority h)
      (Measure.dirac ()), ParitySuccess (actionPriority θ) (historyAction d H) at hw
  rw [← computedDecoder_exact] at hw
  exact (ae_map_iff (historyAction_measurable d).aemeasurable (paritySuccess_measurable _)).mpr hw

/-- Opposite eventual actions cannot satisfy the true model's coBüchi objective. -/
theorem opposite_tail_failure (θ : Bool) (x : ℕ → Bool × Bool)
    (h : ∀ᶠ n in atTop, (x n).2 = !θ) : ¬ ParitySuccess (actionPriority θ) x := by
  intro hs
  obtain ⟨n,hn,hm⟩ := (h.and ((actionPriority_parity_iff θ x).mp hs)).exists
  have hh : θ = !θ := hm.symm.trans hn
  cases θ <;> simp at hh

/-- A complete positive-probability event, not a distinguished input tape.
The comparison kernel can differ before the eventual opposite-action tail. -/
theorem positive_opposite_failure (θ : Bool)
    (Q : RationalKernel Bool (Bool × Bool) Bool)
    (hQpos : ∀ σ e y, 0 < Q.row σ e y)
    (hagree : ∀ e ∈ goodPairs (!θ), fixtureKernel.row (!θ) e = Q.row θ e)
    (d : Bool × Bool) :
    0 < markovPairLaw Q θ false computedDecoder (Measure.dirac ()) d
      {x | ¬ ParitySuccess (actionPriority θ) x} := by
  let π := pairPolicy false computedDecoder
  have hπ := pairPolicy_measurable false computedDecoder computedDecoder_measurable
  let P := realRows fixtureKernel (!θ)
  let R := realRows Q θ
  let μ := markovPairLaw fixtureKernel (!θ) false computedDecoder (Measure.dirac ()) d
  haveI : IsProbabilityMeasure μ := actionLaw_isProbability π hπ (Measure.dirac ()) P
    (realRows_nonnegative fixtureKernel (!θ)) (realRows_normalized fixtureKernel (!θ)) d
  have hg : ∀ᵐ x ∂μ, ∀ᶠ n in atTop, x n ∈ goodPairs (!θ) := by
    filter_upwards [computedDecoder_wins (!θ) d] with x hx
    exact ((actionPriority_parity_iff (!θ) x).mp hx).mono (fun n hn => (mem_goodPairs _ _).mpr hn)
  obtain ⟨U,hU,hsub,hpos⟩ := exists_positive_recurrent_support μ id (goodPairs (!θ)) hg
  obtain ⟨N,hN⟩ := exists_positive_tail_index μ id U hpos
  have hAgreeReal : ∀ e ∈ U, P e = R e := by
    intro e he
    funext y
    change (fixtureKernel.row (!θ) e y : ℝ) = (Q.row θ e y : ℝ)
    rw [hagree e (hsub he)]
  have hPos : 0 < actionLaw π (Measure.dirac ()) R
      (realRows_nonnegative Q θ) (realRows_normalized Q θ) d (tailEvent id U N) := by
    exact canonical_positive_event_relative U π hπ (Measure.dirac ()) P R
      (realRows_nonnegative fixtureKernel (!θ)) (realRows_normalized fixtureKernel (!θ))
      (realRows_nonnegative Q θ) (realRows_normalized Q θ)
      (fun e y _ => by
        change (0:ℝ) < (Q.row θ e y : ℝ)
        exact_mod_cast hQpos θ e y) hAgreeReal d (tailEvent id U N)
      (measurable_tailEvent id (fun n => measurable_pi_apply n) U N) N
      (fun x hx n hn => hx.2 n hn) hN
  apply hPos.trans_le
  apply measure_mono
  intro x hx
  apply opposite_tail_failure θ x
  apply eventually_atTop.mpr
  exact ⟨N,fun n hn => (mem_goodPairs _ _).mp (hsub (hx.2 n hn))⟩

end Orthemology.Eighth.SemanticControls
