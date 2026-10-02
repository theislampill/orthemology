import RawEmpiricalRows

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped BigOperators ENNReal Topology
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Empirical
universe u v
variable {A Y : Type u} {R : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- A deviation in any actual raw tape, at any deterministic count beyond N.
The quantifier includes all pairs/symbols, not only the ones a policy selects. -/
def RawTailDeviation (P : A → Y → ℝ) (ε : ℝ) (N : ℕ) : Set (R × FlatStack A Y) :=
  {z | ∃ a y n, N ≤ n ∧ ε ≤ |rawFrequency a y n z - P a y|}

omit [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
lemma rawTailDeviation_measurable (P : A → Y → ℝ) (ε : ℝ) (N : ℕ) :
    MeasurableSet (RawTailDeviation (R := R) P ε N) := by
  unfold RawTailDeviation
  simp only [Set.setOf_exists]
  apply MeasurableSet.iUnion
  intro a
  apply MeasurableSet.iUnion
  intro y
  apply MeasurableSet.iUnion
  intro n
  by_cases hn : N ≤ n
  · simp only [hn, true_and]
    exact measurableSet_le measurable_const ((rawFrequency_measurable a y n).sub_const _).abs
  · simp only [hn, false_and, Set.setOf_false]
    exact MeasurableSet.empty

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace R]
  [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma rawTailDeviation_antitone (P : A → Y → ℝ) (ε : ℝ) :
    Antitone (RawTailDeviation (R := R) P ε) := by
  intro N M hNM z hz
  obtain ⟨a,y,n,hn,he⟩ := hz
  exact ⟨a,y,n,hNM.trans hn,he⟩

omit [DecidableEq A] [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A]
  [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- Finite simultaneous convergence gives a common pathwise eventual bound. -/
lemma raw_eventually_all_close
    (P : A → Y → ℝ) (z : R × FlatStack A Y)
    (h : ∀ a y, Tendsto (fun n => rawFrequency a y n z) atTop (𝓝 (P a y)))
    {ε : ℝ} (hε : 0 < ε) :
    ∀ᶠ n in atTop, ∀ a y, |rawFrequency a y n z - P a y| < ε := by
  apply eventually_all.mpr
  intro a
  apply eventually_all.mpr
  intro y
  have ht : Tendsto (fun n => |rawFrequency a y n z - P a y|) atTop (𝓝 0) := by
    simpa using ((h a y).sub (tendsto_const_nhds (x := P a y))).abs
  exact ht.eventually_lt_const hε

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- The decreasing all-future bad events have null intersection, derived from
simultaneous actual-stack consistency. -/
theorem rawTailDeviation_inter_null
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    {ε : ℝ} (hε : 0 < ε) :
    (ρ.prod (stackMeasure P hP hN)) (⋂ N, RawTailDeviation (R := R) P ε N) = 0 := by
  rw [measure_zero_iff_ae_nmem]
  filter_upwards [seeded_all_rawFrequencies_tendsto ρ P hP hN] with z hz
  obtain ⟨N,hN'⟩ := eventually_atTop.mp (raw_eventually_all_close P z hz hε)
  intro hb
  obtain ⟨a,y,n,hn,he⟩ := Set.mem_iInter.mp hb N
  exact (not_le_of_gt (hN' n hn a y)) he

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- A probability statement about all future deterministic counts, stronger
than convergence in probability at one selected count. -/
theorem rawTailDeviation_measure_tendsto_zero
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    {ε : ℝ} (hε : 0 < ε) :
    Tendsto (fun N => (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation (R := R) P ε N))
      atTop (𝓝 0) := by
  have ht := tendsto_measure_iInter_atTop
    (fun N => (rawTailDeviation_measurable P ε N).nullMeasurableSet)
    (rawTailDeviation_antitone (R := R) P ε)
    (show ∃ N, (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation P ε N) ≠ ∞ from
      ⟨0, measure_ne_top _ _⟩)
  rw [rawTailDeviation_inter_null ρ P hP hN hε] at ht
  exact ht

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Deterministic burn-in, with a caller-supplied positive error budget. -/
theorem exists_raw_burnin
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    {ε : ℝ} (hε : 0 < ε) {δ : ℝ≥0∞} (hδ : 0 < δ) (N₀ : ℕ) :
    ∃ N, N₀ ≤ N ∧ (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation (R := R) P ε N) ≤ δ := by
  have ht := (rawTailDeviation_measure_tendsto_zero ρ P hP hN hε).eventually_lt_const hδ
  obtain ⟨N,hN',hM⟩ := ((eventually_ge_atTop N₀).and ht).exists
  exact ⟨N,hN',le_of_lt hM⟩

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- A deterministic summable budget schedule for the all-pair/all-symbol tail
error. This is existential, not a computable or logarithmic-rate assertion. -/
theorem exists_summable_raw_burnin
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    {ε : ℝ} (hε : 0 < ε) :
    ∃ N : ℕ → ℕ, (∀ k, k+1 ≤ N k) ∧
      (∀ k, (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation (R := R) P ε (N k)) ≤
        (1/2 : ℝ≥0∞)^k) ∧
      (∑' k, (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation (R := R) P ε (N k))) ≤ 2 := by
  have hex : ∀ k : ℕ, ∃ N, k+1 ≤ N ∧
      (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation (R := R) P ε N) ≤ (1/2 : ℝ≥0∞)^k := by
    intro k
    exact exists_raw_burnin ρ P hP hN hε (zero_lt_iff.mpr (pow_ne_zero k (by norm_num))) (k+1)
  choose N hN' hB using hex
  refine ⟨N,hN',hB,?_⟩
  calc
    _ ≤ ∑' k : ℕ, (1/2 : ℝ≥0∞)^k := ENNReal.tsum_le_tsum hB
    _ = 2 := by rw [ENNReal.tsum_geometric]; norm_num

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- The burn-in can be chosen without knowing which member of a supplied finite
model family is true. It controls every row and symbol under each actual law. -/
theorem exists_uniform_model_burnin {I : Type*} [Fintype I]
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : I → A → Y → ℝ) (hP : ∀ i a y, 0 ≤ P i a y)
    (hN : ∀ i a, ∑ y, P i a y = 1)
    {ε : ℝ} (hε : 0 < ε) {δ : ℝ≥0∞} (hδ : 0 < δ) (N₀ : ℕ) :
    ∃ N, N₀ ≤ N ∧ ∀ i, (ρ.prod (stackMeasure (P i) (hP i) (hN i)))
      (RawTailDeviation (R := R) (P i) ε N) ≤ δ := by
  classical
  have hex := fun i => exists_raw_burnin ρ (P i) (hP i) (hN i) hε hδ N₀
  choose Ns hNs hB using hex
  refine ⟨max N₀ (Finset.univ.sup Ns), le_max_left _ _, ?_⟩
  intro i
  have hi : Ns i ≤ max N₀ (Finset.univ.sup Ns) :=
    (Finset.le_sup (f := Ns) (Finset.mem_univ i)).trans (le_max_right _ _)
  exact (measure_mono (rawTailDeviation_antitone (P i) ε hi)).trans (hB i)

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- One deterministic schedule simultaneously supplies summable phase-error
budgets under every member of the finite input model family. -/
theorem exists_uniform_summable_burnin {I : Type*} [Fintype I]
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : I → A → Y → ℝ) (hP : ∀ i a y, 0 ≤ P i a y)
    (hN : ∀ i a, ∑ y, P i a y = 1)
    {ε : ℝ} (hε : 0 < ε) :
    ∃ N : ℕ → ℕ, (∀ k, k+1 ≤ N k) ∧
      (∀ i k, (ρ.prod (stackMeasure (P i) (hP i) (hN i)))
        (RawTailDeviation (R := R) (P i) ε (N k)) ≤ (1/2 : ℝ≥0∞)^k) ∧
      (∀ i, (∑' k, (ρ.prod (stackMeasure (P i) (hP i) (hN i)))
        (RawTailDeviation (R := R) (P i) ε (N k))) ≤ 2) := by
  have hex : ∀ k : ℕ, ∃ N, k+1 ≤ N ∧ ∀ i,
      (ρ.prod (stackMeasure (P i) (hP i) (hN i)))
        (RawTailDeviation (R := R) (P i) ε N) ≤ (1/2 : ℝ≥0∞)^k := by
    intro k
    exact exists_uniform_model_burnin ρ P hP hN hε
      (zero_lt_iff.mpr (pow_ne_zero k (by norm_num))) (k+1)
  choose N hN' hB using hex
  refine ⟨N,hN',fun i k => hB k i,?_⟩
  intro i
  calc
    _ ≤ ∑' k : ℕ, (1/2 : ℝ≥0∞)^k := ENNReal.tsum_le_tsum (fun k => hB k i)
    _ = 2 := by rw [ENNReal.tsum_geometric]; norm_num

end HiddenParity.Empirical
