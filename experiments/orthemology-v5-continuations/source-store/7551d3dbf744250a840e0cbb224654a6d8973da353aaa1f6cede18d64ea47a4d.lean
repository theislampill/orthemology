import CorrelatedOracleMeasure

open MeasureTheory Set Filter
open scoped Topology

namespace Orthemology.Tranche2.FiniteQuery

/-- On actual executions, the finite-query event is exactly eventual absence
of probing. The final result therefore concerns a single eventual target. -/
lemma actual_eventual_target {S : Type*}
    (ask : S → Bool) (next : S → Bool → S) (a : ℝ)
    (e : ℕ → ℝ) (score : ℕ → S → ℝ) (z : S × Oracle) :
    run ask next z.2 z.1 ∈ finiteQueryTrace ∩
      {t | ∀ᶠ n in atTop, BinaryGood a (e n) (score n (t n).1)} ↔
    ∀ᶠ n in atTop, ask (run ask next z.2 z.1 n).1 = false ∧
      BinaryGood a (e n) (score n (run ask next z.2 z.1 n).1) := by
  simp only [mem_inter_iff, finiteQueryTrace, mem_iUnion, mem_setOf_eq,
    boundedTrace]
  rw [show (∃ N, ∀ n, (run ask next z.2 z.1 n).2 ≤ N) ↔
      ∀ᶠ n in atTop, ask (run ask next z.2 z.1 n).1 = false from
    bounded_iff_eventually_no_query ask next z.2 z.1]
  exact eventually_and.symm

lemma measurable_eventual_score {S : Type*} [MeasurableSpace S]
    (a : ℝ) (e : ℕ → ℝ) (score : ℕ → S → ℝ)
    (hscore : ∀ n, Measurable (score n)) :
    MeasurableSet {t : Trace S | ∀ᶠ n in atTop, BinaryGood a (e n) (score n (t n).1)} := by
  simp only [eventually_atTop, setOf_exists, setOf_forall]
  apply MeasurableSet.iUnion
  intro N
  apply MeasurableSet.iInter
  intro n
  apply MeasurableSet.iInter
  intro _
  exact (measurable_binaryGood a (e n)).preimage
    ((hscore n).comp (measurable_pi_apply n).fst)

/-- At most countably many norms have positive probability of one eventual
target: no more probes AND literal all-state improvement at every late step.
The oracle may have arbitrary dependence on the initial private random state;
only that state's marginal must be shared across norms. -/
theorem countable_positive_eventual_causal_restoration
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) [IsProbabilityMeasure ρ]
    (inputLaw : ℝ → Measure (S × Oracle)) [∀ a, IsProbabilityMeasure (inputLaw a)]
    (hseed : ∀ a, (inputLaw a).map Prod.fst = ρ)
    (e : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0))
    (score : ℕ → S → ℝ) (hscore : ∀ n, Measurable (score n)) :
    Set.Countable {a : ℝ | a ∈ Icc 0 1 ∧
      0 < inputLaw a {z | ∀ᶠ n in atTop,
        ask (run ask next z.2 z.1 n).1 = false ∧
        BinaryGood a (e n) (score n (run ask next z.2 z.1 n).1)}} := by
  have h := countable_positive_shared_seed_query_repairs ask next ha hn
    ρ inputLaw hseed e he0 he1 he score hscore
  convert h using 1
  ext a
  simp only [mem_setOf_eq]
  unfold jointTraceLaw
  rw [Measure.map_apply (measurable_trajectory ask next ha hn)
    (measurable_finiteQueryTrace.inter (measurable_eventual_score a e score hscore))]
  have hset : {z : S × Oracle | ∀ᶠ n in atTop,
      ask (run ask next z.2 z.1 n).1 = false ∧
      BinaryGood a (e n) (score n (run ask next z.2 z.1 n).1)} =
      (fun z => run ask next z.2 z.1) ⁻¹'
        (finiteQueryTrace ∩ {t | ∀ᶠ n in atTop, BinaryGood a (e n) (score n (t n).1)}) := by
    ext z
    exact (actual_eventual_target ask next a e score z).symm
  rw [hset]

end Orthemology.Tranche2.FiniteQuery

#print axioms Orthemology.Tranche2.FiniteQuery.countable_positive_eventual_causal_restoration
#check Orthemology.Tranche2.FiniteQuery.countable_positive_eventual_causal_restoration
