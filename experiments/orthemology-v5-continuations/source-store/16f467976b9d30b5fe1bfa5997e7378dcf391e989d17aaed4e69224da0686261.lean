import EventualCausalRestoration

open MeasureTheory Set Filter
open scoped Topology

namespace Orthemology.Tranche2

/-- All-state repair allowing a nonnegative additive loss tolerance. -/
def BinaryApproxGood (a e eta q : ℝ) : Prop :=
  q^2 ≤ a*(1/2+e)^2+(1-a)*(1/2)^2+eta ∧
  (1-q)^2 ≤ a*(1/2-e)^2+(1-a)*(1/2)^2+eta

/-- Robustness: vanishing tolerance relative to the disturbance still forces
exact asymptotic norm identification. -/
theorem eventual_approximate_binary_good_decodes
    (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (e eta q : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (heta : ∀ n, 0 ≤ eta n) (he : Tendsto e atTop (𝓝 0))
    (hratio : Tendsto (fun n => eta n / e n) atTop (𝓝 0))
    (hgood : ∀ᶠ n in atTop, BinaryApproxGood a (e n) (eta n) (q n)) :
    Tendsto (fun n => (q n-1/2)/e n) atTop (𝓝 a) := by
  apply tendsto_iff_norm_sub_tendsto_zero.mpr
  have hbound : ∀ᶠ n in atTop,
      ‖(q n-1/2)/e n-a‖ ≤ e n/2+2*(eta n/e n) := by
    apply hgood.mono
    intro n hn
    have h := RepairObstruction.binary_parameter_decoder a (e n) (q n) (eta n)
      ha0 ha1 (he0 n) (he1 n) (heta n) hn.1 hn.2
    simpa [Real.norm_eq_abs, mul_div_assoc] using h
  have hlim : Tendsto (fun n => e n/2+2*(eta n/e n)) atTop (𝓝 0) := by
    simpa using (he.div_const 2).add (hratio.const_mul 2)
  exact squeeze_zero' (Eventually.of_forall fun n => norm_nonneg _) hbound hlim

/-- The first-order scale is sharp: a fixed coherent forecast needs no norm
information if tolerance equals the disturbance size. -/
theorem no_information_linear_tolerance (a e : ℝ)
    (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (he : 0 ≤ e) :
    BinaryApproxGood a e e (1/2) := by
  have hae := mul_nonneg ha0 he
  have haee := mul_nonneg ha0 (sq_nonneg e)
  have hbe := mul_nonneg (sub_nonneg.mpr ha1) he
  constructor <;> dsimp <;> nlinarith

/-- Countability under event-restricted trace domination, now robust to every
sublinear additive tolerance. -/
theorem countable_positive_eventual_approximate_repairs
    {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (ν : ℝ → Measure Ω)
    (F : Set Ω) (hF : MeasurableSet F)
    (e eta : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (heta : ∀ n, 0 ≤ eta n) (he : Tendsto e atTop (𝓝 0))
    (hratio : Tendsto (fun n => eta n/e n) atTop (𝓝 0))
    (q : ℕ → Ω → ℝ) (hq : ∀ n, Measurable (q n))
    (hdom : ∀ a, (ν a).restrict F ≪ μ.restrict F) :
    Set.Countable {a : ℝ | a ∈ Icc 0 1 ∧
      0 < ν a (F ∩ {ω | ∀ᶠ n in atTop, BinaryApproxGood a (e n) (eta n) (q n ω)})} := by
  let f : ℕ → Ω → ℝ := fun n ω => (q n ω-1/2)/e n
  have hf : ∀ n, Measurable (f n) := fun n => ((hq n).sub_const (1/2)).div_const (e n)
  apply (countable_positive_limit_values (μ.restrict F) f hf).mono
  rintro a ⟨⟨ha0,ha1⟩,hpos⟩
  have hsub : F ∩ {ω | ∀ᶠ n in atTop, BinaryApproxGood a (e n) (eta n) (q n ω)} ⊆
      {ω | Tendsto (fun n => f n ω) atTop (𝓝 a)} := by
    intro ω hω
    exact eventual_approximate_binary_good_decodes a ha0 ha1 e eta (fun n => q n ω)
      he0 he1 heta he hratio hω.2
  by_contra hz
  have hzero : (μ.restrict F) {ω | Tendsto (fun n => f n ω) atTop (𝓝 a)} = 0 :=
    le_antisymm (le_of_not_gt hz) (zero_le _)
  have hs := measure_mono_null hsub (hdom a hzero)
  rw [Measure.restrict_apply' hF] at hs
  have hset : (F ∩ {ω | ∀ᶠ n in atTop, BinaryApproxGood a (e n) (eta n) (q n ω)}) ∩ F =
      F ∩ {ω | ∀ᶠ n in atTop, BinaryApproxGood a (e n) (eta n) (q n ω)} := by
    ext ω
    simp only [mem_inter_iff]
    tauto
  rw [hset] at hs
  exact (ne_of_gt hpos) hs

end Orthemology.Tranche2

#print axioms Orthemology.Tranche2.eventual_approximate_binary_good_decodes
#print axioms Orthemology.Tranche2.no_information_linear_tolerance
#print axioms Orthemology.Tranche2.countable_positive_eventual_approximate_repairs

namespace Orthemology.Tranche2.FiniteQuery

lemma measurable_eventual_approximate_score {S : Type*} [MeasurableSpace S]
    (a : ℝ) (e eta : ℕ → ℝ) (score : ℕ → S → ℝ)
    (hscore : ∀ n, Measurable (score n)) :
    MeasurableSet {t : Trace S | ∀ᶠ n in atTop,
      BinaryApproxGood a (e n) (eta n) (score n (t n).1)} := by
  simp only [eventually_atTop, setOf_exists, setOf_forall]
  apply MeasurableSet.iUnion
  intro N
  apply MeasurableSet.iInter
  intro n
  apply MeasurableSet.iInter
  intro _
  let f : Trace S → ℝ := fun t => score n (t n).1
  have hf : Measurable f := (hscore n).comp (measurable_pi_apply n).fst
  exact (measurableSet_le (hf.pow_const 2) measurable_const).inter
    (measurableSet_le ((measurable_const.sub hf).pow_const 2) measurable_const)

/-- Robust causal no-go, with only domination of initial-state marginals.
Both the loss tolerance and actual oracle correlations are handled explicitly. -/
theorem countable_positive_approximate_causal_restoration
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) [IsProbabilityMeasure ρ]
    (inputLaw : ℝ → Measure (S × Oracle))
    (hseed : ∀ a, (inputLaw a).map Prod.fst ≪ ρ)
    (e eta : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (heta : ∀ n, 0 ≤ eta n) (he : Tendsto e atTop (𝓝 0))
    (hratio : Tendsto (fun n => eta n/e n) atTop (𝓝 0))
    (score : ℕ → S → ℝ) (hscore : ∀ n, Measurable (score n)) :
    Set.Countable {a : ℝ | a ∈ Icc 0 1 ∧
      0 < inputLaw a {z | ∀ᶠ n in atTop,
        ask (run ask next z.2 z.1 n).1 = false ∧
        BinaryApproxGood a (e n) (eta n) (score n (run ask next z.2 z.1 n).1)}} := by
  let μ : Measure (Trace S) := traceLaw ask next ρ fairOracle
  haveI : IsFiniteMeasure μ := by dsimp [μ,traceLaw]; infer_instance
  have h := countable_positive_eventual_approximate_repairs μ
    (fun a => jointTraceLaw ask next (inputLaw a)) finiteQueryTrace
    measurable_finiteQueryTrace e eta he0 he1 heta he hratio
    (fun n t => score n (t n).1)
    (fun n => (hscore n).comp (measurable_pi_apply n).fst)
    (fun a => correlated_finite_query_trace_domination ask next ha hn (inputLaw a) ρ (hseed a))
  convert h using 1
  ext a
  simp only [mem_setOf_eq]
  unfold jointTraceLaw
  rw [Measure.map_apply (measurable_trajectory ask next ha hn)
    (measurable_finiteQueryTrace.inter (measurable_eventual_approximate_score a e eta score hscore))]
  have hset : {z : S × Oracle | ∀ᶠ n in atTop,
      ask (run ask next z.2 z.1 n).1 = false ∧
      BinaryApproxGood a (e n) (eta n) (score n (run ask next z.2 z.1 n).1)} =
      (fun z => run ask next z.2 z.1) ⁻¹'
        (finiteQueryTrace ∩ {t | ∀ᶠ n in atTop,
          BinaryApproxGood a (e n) (eta n) (score n (t n).1)}) := by
    ext z
    simp only [mem_preimage, mem_inter_iff, mem_setOf_eq, finiteQueryTrace,
      mem_iUnion, boundedTrace]
    rw [show (∃ N, ∀ n, (run ask next z.2 z.1 n).2 ≤ N) ↔
        ∀ᶠ n in atTop, ask (run ask next z.2 z.1 n).1 = false from
      bounded_iff_eventually_no_query ask next z.2 z.1]
    exact eventually_and
  rw [hset]

end Orthemology.Tranche2.FiniteQuery

#print axioms Orthemology.Tranche2.FiniteQuery.countable_positive_approximate_causal_restoration
#check Orthemology.Tranche2.FiniteQuery.countable_positive_approximate_causal_restoration
