import ActualSliceUnionBound
import RawUnrestrictedDeviation

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
open HiddenParity.Necessity HiddenParity.Stage

/-- Total actual bad count is the supremum of literal finite-prefix counts,
including the possibility of infinity. -/
theorem badCount_eq_iSup_prefix {Pair : Type*} (bad : Pair → Prop) [DecidablePred bad] (x : ℕ → Pair) :
    badCount bad x=⨆ T:ℕ,(((Finset.range T).filter (fun t => bad (x t))).card:ℝ≥0∞) := by
  rw [badCount,ENNReal.tsum_eq_iSup_nat]
  congr 1
  funext T
  simp

/-- No a-priori finiteness of total cost is needed to find an excessive finite
prefix. This is the measure-theoretically safe infinite-horizon bridge. -/
theorem exists_prefix_of_badCount_excess {Pair : Type*} (bad : Pair → Prop) [DecidablePred bad]
    (x : ℕ → Pair) (K : ℕ) (hk : (K:ℝ≥0∞)<badCount bad x) :
    ∃ T, K<((Finset.range T).filter (fun t => bad (x t))).card := by
  rw [badCount_eq_iSup_prefix] at hk
  obtain ⟨T,hT⟩ := lt_iSup_iff.mp hk
  exact ⟨T,by exact_mod_cast hT⟩

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
local notation "tail" => runTail P menu priority B₀ s₀ fallback fallbackAction reject
local notation "π" => pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)

/-- Failure of the raw deterministic-prefix deviation event implies accuracy
of every acquired history, pathwise. Random acquired counts are not assumed iid. -/
theorem all_histories_accurate_of_raw_good (σ : Model) (η : ℝ) (N : ℕ)
    (z : Unit × FlatStack (State × Action) State)
    (hg : z∉RawTailDeviation (realRows P σ) η N) :
    ∀ t,HistoryAccurate P σ η N (H z t) := by
  intro t e y hc
  by_contra hbad
  have hge : η≤|historyFrequency e y (H z t)-realRows P σ e y| := not_lt.mp hbad
  apply hg
  refine ⟨e,y,countBefore π z e t,hc,?_⟩
  change η≤|historyFrequency e y (stackHistoryTrajectory π z t)-realRows P σ e y| at hge
  rw [historyFrequency_eq_rawFrequency] at hge
  exact hge

/-- End-to-end actual generated-policy fallback tail. All interval chronology,
full-history conditioning, zero-cost skips, global counters, raw deviation and
infinite-prefix coverage are discharged. This weaker two-parameter estimate
already implies finite moments of every order; it is not the sharp MGF result. -/
theorem actual_generated_badCount_cutoff_tail
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ))
    (hs₀ : s₀∈winningRegion P menu priority B₀) (σ : Model) (hσ : σ∈B₀)
    (η : ℝ) (hηpos : 0<η) (hη : η≤ε)
    (hSep : ∀ θ∈B₀,∀ e,P.row θ e≠P.row σ e → ∃ y,ε+η≤|realRows P σ e y-realRows P θ e y|)
    (p : ℝ) (hp : 0≤p) (hp1 : p≤1)
    (hmin : ∀ e y,0<realRows P σ e y → p≤realRows P σ e y)
    (N k : ℕ) (hN : 0<N) :
    let J := Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card)
    let D := FrozenRotor.dimension State Action
    let c := (min η 1)^2/2
    let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
    μ {z | ((J*(k*D):ℕ):ℝ≥0∞)<badCount (bad σ) (x z)} ≤
      ENNReal.ofReal ((Fintype.card (State × Action):ℝ)*(Fintype.card State:ℝ)*
        (2*Real.exp (-(N:ℝ)*c)/(1-Real.exp (-c))))+
      (J:ℝ≥0∞)*ENNReal.ofReal ((1-p^D)^k) := by
  dsimp only
  let J := Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card)
  let D := FrozenRotor.dimension State Action
  let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
  let U := ⋃ j∈Finset.range J,longStartEvent P menu priority B₀ s₀ fallback fallbackAction reject σ j (k*D)
  have hInclude : ∀ᵐ z ∂μ,
      z∈{z | ((J*(k*D):ℕ):ℝ≥0∞)<badCount (bad σ) (x z)} →
      z∈RawTailDeviation (realRows P σ) η N ∪ U := by
    filter_upwards [seeded_all_tapes_supported (Measure.dirac ()) (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ)] with z hSupported
    intro hCost
    by_cases hraw : z∈RawTailDeviation (realRows P σ) η N
    · exact Or.inl hraw
    · have hAcc := all_histories_accurate_of_raw_good P menu priority B₀ s₀ fallback fallbackAction ε σ η N z hraw
      obtain ⟨T,hT⟩ := exists_prefix_of_badCount_excess (bad σ) (x z) (J*(k*D)) hCost
      obtain ⟨base,hstart,hd,hj,hbase,hslice⟩ := actual_long_history_slice_of_excess
        P menu priority B₀ s₀ fallback fallbackAction ε bad hpriority hs₀ σ hσ η hη N T (k*D) hSep z
        hSupported (by intro t ht;exact hAcc t) hT
      let j := historyProgressCount P menu priority B₀ s₀ fallback reject σ base
      let h : DangerousStart P menu priority B₀ s₀ fallback reject σ j := ⟨base,hstart,rfl,hd⟩
      exact Or.inr (Set.mem_iUnion.mpr ⟨j,Set.mem_iUnion.mpr ⟨Finset.mem_range.mpr hj,
        Set.mem_iUnion.mpr ⟨h,hbase,hslice⟩⟩⟩)
  exact (measure_mono_ae hInclude).trans ((measure_union_le _ _).trans (add_le_add
    (HiddenParity.Exponential.seeded_rawTailDeviation_exponential_all_positive (Measure.dirac ())
      (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) N hN hηpos)
    (finite_longStart_union_bound P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ p hp hp1 hmin J k)))

end HiddenParity.Cost
