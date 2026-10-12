import GenericQueryReference
import Mathlib.Probability.Distributions.Geometric

noncomputable section
open MeasureTheory Set Filter
open scoped ENNReal BigOperators Topology
open Orthemology.Tranche2.FiniteAlphabetQuery

namespace GenericAuditControls

def onceAsk {Y : Type*} : Option Y → Bool
  | none => true
  | some _ => false

def onceNext {Y : Type*} : Option Y → Y → Option Y
  | none, y => some y
  | some z, _ => some z

lemma once_run_succ {Y : Type*} [Inhabited Y] (o : ℕ → Y) (n : ℕ) :
    run onceAsk onceNext o none (n+1) = (some (o 0),1) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [run, ih]; rfl

lemma once_bounded {Y : Type*} [Inhabited Y] (o : ℕ → Y) :
    Bounded onceAsk onceNext o none 1 := by
  intro n
  cases n with
  | zero => simp [run]
  | succ n => rw [once_run_succ]

lemma zero_query_uses_no_oracle {Y : Type*} [Inhabited Y] (o q : ℕ → Y)
    (initial : ℕ) :
    run (fun _ : ℕ => false) (fun n _ => n+1) o initial =
      run (fun _ : ℕ => false) (fun n _ => n+1) q initial := by
  funext n
  exact bounded_prefix_locality _ _ o q initial 0 (by omega)
    (by intro k; induction k with | zero => rfl | succ k ih => simpa [run,advance] using ih) n

lemma iid_first_symbol {Y : Type*} [Inhabited Y] [Countable Y]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]
    (q : Measure Y) [IsProbabilityMeasure q] (y : Y) :
    iidOracle q {o | o 0 = y} = q {y} := by
  have heq : {o : ℕ → Y | o 0 = y} = Set.pi ({0} : Finset ℕ) (fun _ => ({y} : Set Y)) := by
    ext o
    simp
  rw [heq, iidOracle, Measure.infinitePi_pi _ (fun _ _ => measurableSet_singleton y)]
  simp

lemma trace_dirac_initial_event {Y S : Type*} [Inhabited Y] [Countable Y]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] [MeasurableSpace S]
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ y, Measurable (fun s => next s y))
    (initial : S) (ν : Measure (ℕ → Y)) [SFinite ν]
    (E : Set (Trace S)) (hE : MeasurableSet E) :
    traceLaw ask next (Measure.dirac initial) ν E =
      ν {o | run ask next o initial ∈ E} := by
  rw [traceLaw, Measure.dirac_prod, Measure.map_map (measurable_trajectory ask next ha hn)
    measurable_prodMk_left, Measure.map_apply
    ((measurable_trajectory ask next ha hn).comp measurable_prodMk_left) hE]
  rfl

instance : MeasurableSpace (Option Bool) := ⊤
instance : MeasurableSingletonClass (Option Bool) := ⟨fun _ => trivial⟩

def onceTrueEvent : Set (Trace (Option Bool)) :=
  boundedTrace 1 ∩ {t | (t 1).1 = some true}

lemma measurable_onceTrueEvent : MeasurableSet onceTrueEvent := by
  exact (measurable_boundedTrace 1).inter
    ((measurableSet_singleton (some true)).preimage (measurable_pi_apply 1).fst)

lemma once_event_preimage : {o : ℕ → Bool | run onceAsk onceNext o none ∈ onceTrueEvent} =
    {o | o 0 = true} := by
  ext o
  simp only [onceTrueEvent, Set.mem_setOf_eq, Set.mem_inter_iff, boundedTrace]
  change (Bounded onceAsk onceNext o none 1 ∧ (run onceAsk onceNext o none 1).1 = some true) ↔ _
  rw [once_run_succ o 0]
  simp [once_bounded]

/-- Dropping full support breaks the actual iid-rival endpoint after ONE query. -/
theorem missing_full_support_counterexample :
    traceLaw onceAsk onceNext (Measure.dirac (none : Option Bool))
      (Measure.dirac (fun _ : ℕ => true)) onceTrueEvent = 1 ∧
    traceLaw onceAsk onceNext (Measure.dirac (none : Option Bool))
      (iidOracle (Measure.dirac false)) onceTrueEvent = 0 ∧
    onceTrueEvent ⊆ finiteQueryTrace := by
  have ha : Measurable (@onceAsk Bool) := measurable_of_finite _
  have hn : ∀ y : Bool, Measurable (fun s => onceNext s y) := fun _ => measurable_of_finite _
  constructor
  · rw [trace_dirac_initial_event onceAsk onceNext ha hn none _ _ measurable_onceTrueEvent,
      once_event_preimage]
    simp
  constructor
  · rw [trace_dirac_initial_event onceAsk onceNext ha hn none _ _ measurable_onceTrueEvent,
      once_event_preimage, iid_first_symbol]
    simp
  · intro t ht
    exact Set.mem_iUnion.mpr ⟨1, ht.1⟩

noncomputable def fairBit : Measure Bool := (PMF.bernoulli (1/2) (by norm_num)).toMeasure
instance : IsProbabilityMeasure fairBit := by unfold fairBit; infer_instance
lemma fairBit_singleton (b : Bool) : fairBit {b} = (1/2 : ℝ≥0∞) := by
  rw [fairBit, PMF.toMeasure_apply_singleton _ b (measurableSet_singleton b), PMF.bernoulli_apply]
  cases b <;> norm_num
lemma fairBit_full (b : Bool) : fairBit {b} ≠ 0 := by rw [fairBit_singleton]; norm_num

lemma fair_prefix_mass (N : ℕ) :
    iidOracle fairBit {o | ∀ i < N, o i = true} = (1/2 : ℝ≥0∞)^N := by
  have heq : {o : ℕ → Bool | ∀ i < N, o i = true} =
      Set.pi (Finset.range N : Set ℕ) (fun _ => ({true} : Set Bool)) := by ext o; simp
  rw [heq, iidOracle, Measure.infinitePi_pi _ (fun _ _ => measurableSet_singleton true)]
  simp [fairBit_singleton]

lemma fair_all_true_zero : iidOracle fairBit {o | ∀ i, o i = true} = 0 := by
  have hbound : ∀ N, iidOracle fairBit {o | ∀ i, o i = true} ≤ (1/2 : ℝ≥0∞)^N := by
    intro N
    rw [← fair_prefix_mass]
    exact measure_mono (fun o ho i _ => ho i)
  have ht := ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num : (1/2 : ℝ≥0∞) < 1)
  exact le_antisymm (ge_of_tendsto ht (Filter.Eventually.of_forall hbound)) bot_le

lemma all_query_run_succ (o : ℕ → Bool) (n : ℕ) :
    run (fun _ => true) (fun (_ : Bool) y => y) o false (n+1) = (o n,n+1) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [run, ih]; rfl

lemma all_query_never_bounded (o : ℕ → Bool) :
    ¬ ∃ N, Bounded (fun _ => true) (fun (_ : Bool) y => y) o false N := by
  rintro ⟨N,hN⟩
  have hh := hN (N+1)
  rw [all_query_run_succ] at hh
  exact Nat.not_succ_le_self N hh

def allTrueTrace : Set (Trace Bool) := {t | ∀ n, (t (n+1)).1 = true}
lemma measurable_allTrueTrace : MeasurableSet allTrueTrace := by
  simp only [allTrueTrace, Set.setOf_forall]
  exact MeasurableSet.iInter (fun n => (measurableSet_singleton true).preimage (measurable_pi_apply (n+1)).fst)
lemma allTrueTrace_preimage :
    {o : ℕ → Bool | run (fun _ => true) (fun (_ : Bool) y => y) o false ∈ allTrueTrace} =
      {o | ∀ i, o i = true} := by ext o; simp [allTrueTrace, all_query_run_succ]

/-- Full-support finite prefix laws do NOT dominate an unrestricted infinite-query event. -/
theorem infinite_query_counterexample :
    traceLaw (fun _ => true) (fun (_ : Bool) y => y) (Measure.dirac false)
      (Measure.dirac (fun _ : ℕ => true)) allTrueTrace = 1 ∧
    traceLaw (fun _ => true) (fun (_ : Bool) y => y) (Measure.dirac false)
      (iidOracle fairBit) allTrueTrace = 0 := by
  have ha : Measurable (fun _ : Bool => true) := measurable_const
  have hn : ∀ y : Bool, Measurable (fun _ : Bool => y) := fun _ => measurable_const
  constructor
  · rw [trace_dirac_initial_event _ _ ha hn false _ _ measurable_allTrueTrace, allTrueTrace_preimage]
    simp
  · rw [trace_dirac_initial_event _ _ ha hn false _ _ measurable_allTrueTrace, allTrueTrace_preimage]
    exact fair_all_true_zero

noncomputable def natGeometric : Measure ℕ :=
  ProbabilityTheory.geometricMeasure (p := (1:ℝ)/2) (by norm_num) (by norm_num)
instance : IsProbabilityMeasure natGeometric := ProbabilityTheory.isProbabilityMeasureGeometric _ _
lemma natGeometric_full (n : ℕ) : natGeometric {n} ≠ 0 := by
  rw [natGeometric, ProbabilityTheory.geometricMeasure, PMF.toMeasure_apply_singleton _ n (measurableSet_singleton n)]
  change ENNReal.ofReal (ProbabilityTheory.geometricPMFReal ((1:ℝ)/2) n) ≠ 0
  rw [ENNReal.ofReal_ne_zero_iff]
  unfold ProbabilityTheory.geometricPMFReal
  positivity

/-- A genuinely countably infinite symbol instance, not merely a Boolean renaming. -/
theorem countable_nat_full_prefix (N : ℕ) (w : Fin N → ℕ) :
    ((iidOracle natGeometric).map (prefixSymbols N)) {w} ≠ 0 :=
  iidOracle_prefix_nonzero natGeometric natGeometric_full N w

#print axioms missing_full_support_counterexample
#print axioms infinite_query_counterexample
#print axioms countable_nat_full_prefix
end GenericAuditControls
