import EmpiricalTailBounds
import SequentialTapeConsumption

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped BigOperators ENNReal Topology
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Adaptive

namespace HiddenParity.Empirical
universe u v
variable {A Y : Type u} {R : Type v}
variable [Fintype A] [DecidableEq A] [Inhabited Y]

/-- The literal number of acquired (a,y) receipts, represented as a real sum.
No raw-tape values or hidden parameters are arguments of this observable. -/
def historySymbolMass (a : A) (y : Y) (h : History A Y) : ℝ :=
  (h.map (fun ay => if ay.1 = a then symbolIndicator y ay.2 else 0)).sum

/-- Observable empirical frequency; it is 0 when this pair has not been used. -/
def historyFrequency (a : A) (y : Y) (h : History A Y) : ℝ :=
  historySymbolMass a y h / actionCount a h

omit [Fintype A] [Inhabited Y] in
@[simp] lemma historySymbolMass_nil (a : A) (y : Y) : historySymbolMass a y [] = 0 := rfl

omit [Fintype A] [Inhabited Y] in
@[simp] lemma historySymbolMass_cons (a b : A) (y t : Y) (h : History A Y) :
    historySymbolMass a y ((b,t)::h) =
      (if b = a then symbolIndicator y t else 0) + historySymbolMass a y h := rfl

lemma stackHistoryTrajectory_succ_receipt (π : R → History A Y → A)
    (z : R × FlatStack A Y) (n : ℕ) :
    stackHistoryTrajectory π z (n+1) =
      (stackActionTrajectory π z n, stackReceipt π z n) :: stackHistoryTrajectory π z n := by
  simp [stackHistoryTrajectory, observedHistory, feedback, stackActionTrajectory,
    stackReceipt, countBefore]

/-- Sequential consumption identifies the whole acquired receipt statistic with
the deterministic initial segment of its tape, pathwise, for every policy. -/
theorem historySymbolMass_eq_raw_sum (π : R → History A Y → A)
    (z : R × FlatStack A Y) (a : A) (y : Y) (n : ℕ) :
    historySymbolMass a y (stackHistoryTrajectory π z n) =
      ∑ i ∈ Finset.range (countBefore π z a n), symbolIndicator y (seededStackCoordinate a i z) := by
  induction n with
  | zero => simp [stackHistoryTrajectory, observedHistory]
  | succ n ih =>
      rw [stackHistoryTrajectory_succ_receipt, historySymbolMass_cons, ih, countBefore_succ]
      by_cases ha : stackActionTrajectory π z n = a
      · simp only [ha, if_pos, Finset.sum_range_succ]
        simp only [stackReceipt, ha, seededStackCoordinate]
        exact add_comm _ _
      · simp [ha]

/-- The actual history-based empirical value is the raw frequency evaluated at
its actual consumed count. This is an identity, not a random-count iid claim. -/
theorem historyFrequency_eq_rawFrequency (π : R → History A Y → A)
    (z : R × FlatStack A Y) (a : A) (y : Y) (n : ℕ) :
    historyFrequency a y (stackHistoryTrajectory π z n) =
      rawFrequency a y (countBefore π z a n) z := by
  unfold historyFrequency rawFrequency
  rw [historySymbolMass_eq_raw_sum]
  rfl

/-- A recurrent action has counts tending to infinity by actual sequential
consumption, without any probabilistic regularity premise. -/
theorem recurrent_count_tendsto (π : R → History A Y → A)
    (z : R × FlatStack A Y) (a : A)
    (hRec : ∃ᶠ n in atTop, stackActionTrajectory π z n = a) :
    Tendsto (countBefore π z a) atTop atTop :=
  (countBefore_mono π z a).tendsto_atTop_atTop
    (recurrent_action_unbounded_count π z a hRec)

/-- Pathwise transfer along actual unbounded consumption; no conditioning on
which random count the policy happens to have reached. -/
theorem historyFrequency_tendsto_of_recurrent
    (π : R → History A Y → A) (z : R × FlatStack A Y) (P : A → Y → ℝ)
    (a : A) (y : Y)
    (hRaw : Tendsto (fun m => rawFrequency a y m z) atTop (𝓝 (P a y)))
    (hRec : ∃ᶠ n in atTop, stackActionTrajectory π z n = a) :
    Tendsto (fun n => historyFrequency a y (stackHistoryTrajectory π z n)) atTop (𝓝 (P a y)) := by
  simpa only [historyFrequency_eq_rawFrequency] using hRaw.comp (recurrent_count_tendsto π z a hRec)

/-- Every adaptive observed deviation after enough uses of a pair is contained
in the deterministic raw-tape tail event. This works even at random test times. -/
theorem observed_deviation_subset_raw
    (π : R → History A Y → A) (P : A → Y → ℝ) (ε : ℝ) (N : ℕ) :
    {z : R × FlatStack A Y | ∃ a y n, N ≤ countBefore π z a n ∧
      ε ≤ |historyFrequency a y (stackHistoryTrajectory π z n) - P a y|} ⊆
      RawTailDeviation P ε N := by
  rintro z ⟨a,y,n,hn,he⟩
  exact ⟨a,y,countBefore π z a n,hn,by simpa only [historyFrequency_eq_rawFrequency] using he⟩

variable [Fintype Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

omit [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- The common probability-one event is uniform over all causal policies.
Measurability of a policy is needed only when pushing to its observed law. -/
theorem seeded_observedFrequencies_tendsto
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN),
      ∀ (π : R → History A Y → A) a,
        (∃ᶠ n in atTop, stackActionTrajectory π z n = a) →
        ∀ y, Tendsto (fun n => historyFrequency a y (stackHistoryTrajectory π z n))
          atTop (𝓝 (P a y)) := by
  filter_upwards [seeded_all_rawFrequencies_tendsto ρ P hP hN] with z hz
  intro π a hRec y
  exact historyFrequency_tendsto_of_recurrent π z P a y (hz a y) hRec

omit [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
/-- Actual adaptive all-future test error is bounded by the proved raw-tail
probability. The proof is set containment, not optional-sampling independence. -/
theorem observed_deviation_measure_le_raw
    (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (ε : ℝ) (N : ℕ) :
    (ρ.prod (stackMeasure P hP hN))
      {z : R × FlatStack A Y | ∃ a y n, N ≤ countBefore π z a n ∧
        ε ≤ |historyFrequency a y (stackHistoryTrajectory π z n) - P a y|} ≤
      (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation (R := R) P ε N) :=
  measure_mono (observed_deviation_subset_raw π P ε N)

omit [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
  [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- Empirical frequencies are measurable functions of the acquired finite
history; the statistical test can therefore be used by a causal policy. -/
lemma historyFrequency_measurable (a : A) (y : Y) :
    Measurable (historyFrequency a y : History A Y → ℝ) :=
  measurable_of_countable _

lemma countBefore_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (a : A) (n : ℕ) :
    Measurable (fun z => countBefore π z a n) :=
  (measurable_of_countable (actionCount a)).comp
    ((measurable_pi_apply n).comp (stackHistoryTrajectory_measurable π hπ))

lemma observedFrequency_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (a : A) (y : Y) (n : ℕ) :
    Measurable (fun z => historyFrequency a y (stackHistoryTrajectory π z n)) :=
  (historyFrequency_measurable a y).comp
    ((measurable_pi_apply n).comp (stackHistoryTrajectory_measurable π hπ))

lemma observed_deviation_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (P : A → Y → ℝ) (ε : ℝ) (N : ℕ) :
    MeasurableSet {z : R × FlatStack A Y | ∃ a y n, N ≤ countBefore π z a n ∧
      ε ≤ |historyFrequency a y (stackHistoryTrajectory π z n) - P a y|} := by
  simp only [Set.setOf_exists]
  apply MeasurableSet.iUnion
  intro a
  apply MeasurableSet.iUnion
  intro y
  apply MeasurableSet.iUnion
  intro n
  exact (measurableSet_le measurable_const (countBefore_measurable π hπ a n)).inter
    (measurableSet_le measurable_const ((observedFrequency_measurable π hπ a y n).sub_const _).abs)

omit [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- One finite random count makes every later observed estimate accurate,
uniformly over policies, pairs, symbols and physical test times. -/
theorem seeded_uniform_observed_tail_good
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    {ε : ℝ} (hε : 0 < ε) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN), ∃ K : ℕ,
      ∀ (π : R → History A Y → A) a y n, K ≤ countBefore π z a n →
        |historyFrequency a y (stackHistoryTrajectory π z n) - P a y| < ε := by
  filter_upwards [seeded_all_rawFrequencies_tendsto ρ P hP hN] with z hz
  obtain ⟨K,hK⟩ := eventually_atTop.mp (raw_eventually_all_close P z hz hε)
  refine ⟨K,?_⟩
  intro π a y n hn
  rw [historyFrequency_eq_rawFrequency]
  exact hK _ hn a y

omit [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- A test gated by consumed count greater than phase index cannot reject the
true row at arbitrarily large phase indices on this probability-one event. -/
theorem seeded_true_phase_rejections_bounded
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    {ε : ℝ} (hε : 0 < ε) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN), ∃ K : ℕ,
      ∀ k, K ≤ k → ∀ (π : R → History A Y → A) a y n,
        k < countBefore π z a n →
        |historyFrequency a y (stackHistoryTrajectory π z n) - P a y| < ε := by
  filter_upwards [seeded_uniform_observed_tail_good ρ P hP hN hε] with z hz
  obtain ⟨K,hK⟩ := hz
  exact ⟨K,fun k hk π a y n hn => hK π a y n (by omega)⟩

omit [Fintype Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
  [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- At a mismatching recurrent pair, a fixed false-row tolerance is eventually
violated after every fixed phase gate. -/
theorem recurrent_false_row_eventually_rejected
    (π : R → History A Y → A) (z : R × FlatStack A Y) (P Q : A → Y → ℝ)
    (a : A) (y : Y) (k : ℕ) (ε : ℝ)
    (hRaw : Tendsto (fun m => rawFrequency a y m z) atTop (𝓝 (P a y)))
    (hRec : ∃ᶠ n in atTop, stackActionTrajectory π z n = a)
    (hSep : ε < |P a y - Q a y|) :
    ∀ᶠ n in atTop, k < countBefore π z a n ∧
      ε < |historyFrequency a y (stackHistoryTrajectory π z n) - Q a y| := by
  have hc := recurrent_count_tendsto π z a hRec
  have hf := historyFrequency_tendsto_of_recurrent π z P a y hRaw hRec
  have hd := (hf.sub (tendsto_const_nhds (x := Q a y))).abs
  exact (hc.eventually (eventually_gt_atTop k)).and (hd.eventually (eventually_gt_nhds hSep))

omit [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Actual-stack AE version, with every candidate row and every causal policy
available on the same probability-one convergence event. -/
theorem seeded_false_rows_eventually_rejected
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN),
      ∀ (π : R → History A Y → A) (Q : A → Y → ℝ) a y k ε,
        (∃ᶠ n in atTop, stackActionTrajectory π z n = a) →
        ε < |P a y - Q a y| →
        ∀ᶠ n in atTop, k < countBefore π z a n ∧
          ε < |historyFrequency a y (stackHistoryTrajectory π z n) - Q a y| := by
  filter_upwards [seeded_all_rawFrequencies_tendsto ρ P hP hN] with z hz
  intro π Q a y k ε hr hs
  exact recurrent_false_row_eventually_rejected π z P Q a y k ε (hz a y) hr hs

end HiddenParity.Empirical
