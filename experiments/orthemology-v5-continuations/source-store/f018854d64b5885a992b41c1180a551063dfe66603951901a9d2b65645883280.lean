import FiniteQueryLocality
import RestorationCountability
import Mathlib.Probability.ProductMeasure

open MeasureTheory Set
open scoped ENNReal

namespace Orthemology.Tranche2.FiniteQuery

abbrev Oracle := ℕ → Bool
abbrev Trace (S : Type*) := ℕ → S × ℕ

section Measurable
variable {S : Type*} [MeasurableSpace S]

lemma measurable_advance_joint (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b)) :
    Measurable (fun z : (S × ℕ) × Oracle => advance ask next z.2 z.1) := by
  have hnext : Measurable (fun z : S × Bool => next z.1 z.2) :=
    measurable_from_prod_countable hn
  have heval : Measurable (fun z : Oracle × ℕ => z.1 z.2) :=
    measurable_from_prod_countable (fun n => measurable_pi_apply n)
  have hv : Measurable (fun z : (S × ℕ) × Oracle => z.2 z.1.2) :=
    heval.comp (measurable_snd.prodMk measurable_fst.snd)
  have hc : MeasurableSet {z : (S × ℕ) × Oracle | ask z.1.1 = true} :=
    (measurableSet_singleton true).preimage (ha.comp measurable_fst.fst)
  unfold advance
  apply Measurable.ite hc
  · exact (hnext.comp (measurable_fst.fst.prodMk hv)).prodMk
      (measurable_fst.snd.add_const 1)
  · exact ((hn false).comp measurable_fst.fst).prodMk measurable_fst.snd

lemma measurable_run (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b)) (n : ℕ) :
    Measurable (fun z : S × Oracle => run ask next z.2 z.1 n) := by
  induction n with
  | zero => exact measurable_fst.prodMk measurable_const
  | succ n ih =>
      exact (measurable_advance_joint ask next ha hn).comp (ih.prodMk measurable_snd)

lemma measurable_trajectory (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b)) :
    Measurable (fun z : S × Oracle => run ask next z.2 z.1) := by
  exact measurable_pi_lambda _ (measurable_run ask next ha hn)

def boundedTrace (N : ℕ) : Set (Trace S) := {t | ∀ n, (t n).2 ≤ N}

lemma measurable_boundedTrace (N : ℕ) : MeasurableSet (boundedTrace (S := S) N) := by
  simp only [boundedTrace, setOf_forall]
  apply MeasurableSet.iInter
  intro n
  exact measurableSet_le (measurable_pi_apply n).snd measurable_const

lemma measurable_prefixOracle (N : ℕ) : Measurable (prefixOracle N) := by
  apply measurable_pi_lambda
  intro k
  by_cases hk : k < N
  · simpa [prefixOracle,hk] using (measurable_pi_apply (⟨k,hk⟩ : Fin N))
  · simpa [prefixOracle,hk] using (measurable_const : Measurable (fun _ : Fin N → Bool => false))

def prefixInput (N : ℕ) (z : S × Oracle) : S × (Fin N → Bool) :=
  (z.1, fun i => z.2 i)

lemma measurable_prefixInput (N : ℕ) : Measurable (prefixInput (S := S) N) := by
  exact measurable_fst.prodMk (measurable_pi_lambda _ fun i =>
    (measurable_pi_apply i.val).comp measurable_snd)

def finiteTrajectory (ask : S → Bool) (next : S → Bool → S) (N : ℕ)
    (z : S × (Fin N → Bool)) : Trace S := run ask next (prefixOracle N z.2) z.1

lemma measurable_finiteTrajectory (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b)) (N : ℕ) :
    Measurable (finiteTrajectory ask next N) :=
  (measurable_trajectory ask next ha hn).comp
    (measurable_fst.prodMk ((measurable_prefixOracle N).comp measurable_snd))

/-- Both the bounded-query event and every full-run observable factor through
seed plus N oracle bits. This includes never asking query N+1. -/
lemma bounded_event_prefix (ask : S → Bool) (next : S → Bool → S) (N : ℕ) :
    (fun z : S × Oracle => run ask next z.2 z.1) ⁻¹' boundedTrace N =
    prefixInput N ⁻¹' (finiteTrajectory ask next N ⁻¹' boundedTrace N) := by
  ext z
  exact bounded_prefix_equivalence ask next z.2
    (prefixOracle N (fun i => z.2 i)) z.1 N (prefixOracle_agrees z.2 N)

lemma trajectory_prefix_on_bounded (ask : S → Bool) (next : S → Bool → S)
    (N : ℕ) (z : S × Oracle)
    (hz : finiteTrajectory ask next N (prefixInput N z) ∈ boundedTrace N) :
    run ask next z.2 z.1 = finiteTrajectory ask next N (prefixInput N z) := by
  have hb : Bounded ask next z.2 z.1 N :=
    (bounded_prefix_equivalence ask next z.2
      (prefixOracle N (fun i => z.2 i)) z.1 N (prefixOracle_agrees z.2 N)).mpr hz
  exact funext (bounded_prefix_locality ask next z.2 _ z.1 N (prefixOracle_agrees z.2 N) hb)

end Measurable

/-- A measurable restricted observable agrees with its finite-information factor. -/
theorem restricted_observable_factorisation
    {Ω Ξ Ψ : Type*} [MeasurableSpace Ω] [MeasurableSpace Ξ] [MeasurableSpace Ψ]
    (μ : Measure Ω) (proj : Ω → Ξ) (f : Ω → Ψ) (g : Ξ → Ψ)
    (hp : Measurable proj) (hg : Measurable g) (B : Set Ξ) (hB : MeasurableSet B)
    (hfactor : ∀ x, proj x ∈ B → f x = g (proj x)) :
    (μ.restrict (proj ⁻¹' B)).map f = ((μ.map proj).restrict B).map g := by
  calc
    (μ.restrict (proj ⁻¹' B)).map f =
        (μ.restrict (proj ⁻¹' B)).map (g ∘ proj) := by
      apply Measure.map_congr
      filter_upwards [ae_restrict_mem (hB.preimage hp)] with x hx
      exact hfactor x hx
    _ = ((μ.restrict (proj ⁻¹' B)).map proj).map g := (Measure.map_map hg hp).symm
    _ = ((μ.map proj).restrict B).map g := by rw [Measure.restrict_map hp hB]

end Orthemology.Tranche2.FiniteQuery

namespace Orthemology.Tranche2.FiniteQuery

lemma absolutelyContinuous_of_singletons {E : Type*} [MeasurableSpace E]
    (μ ν : Measure E) (hν : ∀ x, ν {x} ≠ 0) : μ ≪ ν := by
  intro A hA
  have hEmpty : A = ∅ := by
    apply Set.eq_empty_iff_forall_not_mem.mpr
    intro x hx
    exact hν x (measure_mono_null (Set.singleton_subset_iff.mpr hx) hA)
  simp [hEmpty]

def prefixBits (N : ℕ) (oracle : Oracle) : Fin N → Bool := fun i => oracle i

lemma measurable_prefixBits (N : ℕ) : Measurable (prefixBits N) :=
  measurable_pi_lambda _ fun i => measurable_pi_apply i.val

section Laws
variable {S : Type*} [MeasurableSpace S]

noncomputable def traceLaw (ask : S → Bool) (next : S → Bool → S)
    (ρ : Measure S) (ν : Measure Oracle) : Measure (Trace S) :=
  (ρ.prod ν).map (fun z => run ask next z.2 z.1)

lemma input_prefix_map (ρ : Measure S) (ν : Measure Oracle)
    [SFinite ρ] [SFinite ν] (N : ℕ) :
    (ρ.prod ν).map (prefixInput N) = ρ.prod (ν.map (prefixBits N)) := by
  change (ρ.prod ν).map (Prod.map id (prefixBits N)) = _
  rw [← Measure.map_prod_map ρ ν measurable_id (measurable_prefixBits N)]
  simp

/-- The restricted observed trace is genuinely a finite-input pushforward;
the event of never querying beyond N is also carried by the finite input. -/
theorem bounded_trace_law_factorisation
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) (ν : Measure Oracle) [SFinite ρ] [SFinite ν] (N : ℕ) :
    (traceLaw ask next ρ ν).restrict (boundedTrace N) =
      ((ρ.prod (ν.map (prefixBits N))).restrict
        (finiteTrajectory ask next N ⁻¹' boundedTrace N)).map (finiteTrajectory ask next N) := by
  rw [traceLaw, Measure.restrict_map (measurable_trajectory ask next ha hn)
    (measurable_boundedTrace N), bounded_event_prefix]
  rw [restricted_observable_factorisation _ (prefixInput N) _ (finiteTrajectory ask next N)
    (measurable_prefixInput N) (measurable_finiteTrajectory ask next ha hn N) _
    ((measurable_boundedTrace N).preimage (measurable_finiteTrajectory ask next ha hn N))
    (trajectory_prefix_on_bounded ask next N)]
  rw [input_prefix_map]

/-- No assumption of absolute continuity of infinite oracle laws. Only the
finite reference-prefix atoms need positive mass. -/
theorem bounded_trace_domination
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) (ν reference : Measure Oracle)
    [SFinite ρ] [SFinite ν] [SFinite reference] (N : ℕ)
    (hfull : ∀ w, (reference.map (prefixBits N)) {w} ≠ 0) :
    (traceLaw ask next ρ ν).restrict (boundedTrace N) ≪
      (traceLaw ask next ρ reference).restrict (boundedTrace N) := by
  rw [bounded_trace_law_factorisation ask next ha hn ρ ν N,
    bounded_trace_law_factorisation ask next ha hn ρ reference N]
  have hp : ν.map (prefixBits N) ≪ reference.map (prefixBits N) :=
    absolutelyContinuous_of_singletons _ _ hfull
  exact ((Measure.AbsolutelyContinuous.rfl.prod hp).restrict _).map
    (measurable_finiteTrajectory ask next ha hn N)

end Laws

lemma restrict_iUnion_domination
    {E : Type*} [MeasurableSpace E] (μ ν : Measure E)
    (A : ℕ → Set E) (hA : ∀ n, MeasurableSet (A n))
    (hdom : ∀ n, μ.restrict (A n) ≪ ν.restrict (A n)) :
    μ.restrict (⋃ n, A n) ≪ ν.restrict (⋃ n, A n) := by
  intro B hB
  rw [Measure.restrict_apply' (MeasurableSet.iUnion hA)] at hB ⊢
  rw [Set.inter_iUnion]
  apply measure_iUnion_null
  intro n
  have href : ν (B ∩ A n) = 0 :=
    measure_mono_null (Set.inter_subset_inter_right B (Set.subset_iUnion A n)) hB
  have hres : ν.restrict (A n) B = 0 := by rw [Measure.restrict_apply' (hA n)]; exact href
  have hm := hdom n hres
  rwa [Measure.restrict_apply' (hA n)] at hm

def finiteQueryTrace {S : Type*} : Set (Trace S) := ⋃ N, boundedTrace N

lemma measurable_finiteQueryTrace {S : Type*} [MeasurableSpace S] :
    MeasurableSet (finiteQueryTrace (S := S)) :=
  MeasurableSet.iUnion measurable_boundedTrace

/-- End-to-end domination for a concrete causal evaluator's finite-query
OBSERVED traces; unused oracle coordinates have been projected away. -/
theorem finite_query_trace_domination
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) (ν reference : Measure Oracle)
    [SFinite ρ] [SFinite ν] [SFinite reference]
    (hfull : ∀ N w, (reference.map (prefixBits N)) {w} ≠ 0) :
    (traceLaw ask next ρ ν).restrict finiteQueryTrace ≪
      (traceLaw ask next ρ reference).restrict finiteQueryTrace := by
  exact restrict_iUnion_domination _ _ boundedTrace measurable_boundedTrace
    (fun N => bounded_trace_domination ask next ha hn ρ ν reference N (hfull N))

end Orthemology.Tranche2.FiniteQuery

namespace Orthemology.Tranche2.FiniteQuery

/-- A mathematical reference law, not a guessed true hidden norm. -/
noncomputable def fairBit : Measure Bool :=
  (PMF.bernoulli (1/2) (by norm_num)).toMeasure

instance fairBit_probability : IsProbabilityMeasure fairBit := by
  unfold fairBit
  infer_instance

lemma fairBit_singleton (b : Bool) : fairBit {b} = (1/2 : ℝ≥0∞) := by
  unfold fairBit
  rw [PMF.toMeasure_apply_singleton _ b (measurableSet_singleton b), PMF.bernoulli_apply]
  cases b <;> norm_num

noncomputable def fairOracle : Measure Oracle :=
  Measure.infinitePi (fun _ : ℕ => fairBit)

instance fairOracle_probability : IsProbabilityMeasure fairOracle := by
  unfold fairOracle
  infer_instance

lemma prefixBits_singleton_preimage (N : ℕ) (w : Fin N → Bool) :
    prefixBits N ⁻¹' {w} = Set.pi (Finset.range N : Set ℕ)
      (fun k => {prefixOracle N w k}) := by
  ext oracle
  simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_pi, Finset.mem_coe,
    Finset.mem_range]
  constructor
  · intro h k hk
    have hv := congrFun h (⟨k,hk⟩ : Fin N)
    simpa [prefixBits,prefixOracle,hk] using hv
  · intro h
    funext i
    have hv := h i.val i.isLt
    simpa [prefixBits,prefixOracle,i.isLt] using hv

/-- Every finite oracle word has positive mass under the explicit reference. -/
lemma fairOracle_prefix_mass (N : ℕ) (w : Fin N → Bool) :
    (fairOracle.map (prefixBits N)) {w} = (1/2 : ℝ≥0∞)^N := by
  rw [Measure.map_apply (measurable_prefixBits N) (measurableSet_singleton w),
    prefixBits_singleton_preimage]
  rw [fairOracle, Measure.infinitePi_pi _ (fun k _ => measurableSet_singleton _)]
  simp [fairBit_singleton]

lemma fairOracle_prefix_nonzero (N : ℕ) (w : Fin N → Bool) :
    (fairOracle.map (prefixBits N)) {w} ≠ 0 := by
  rw [fairOracle_prefix_mass]
  exact pow_ne_zero _ (by norm_num)

/-- Fully derived finite-query trace domination against a concrete fair reference.
The actual oracle distribution may be singular, dependent over time, or deterministic. -/
theorem finite_query_trace_fair_domination
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) (ν : Measure Oracle) [SFinite ρ] [SFinite ν] :
    (traceLaw ask next ρ ν).restrict finiteQueryTrace ≪
      (traceLaw ask next ρ fairOracle).restrict finiteQueryTrace :=
  finite_query_trace_domination ask next ha hn ρ ν fairOracle fairOracle_prefix_nonzero

end Orthemology.Tranche2.FiniteQuery

#print axioms Orthemology.Tranche2.FiniteQuery.bounded_trace_law_factorisation
#print axioms Orthemology.Tranche2.FiniteQuery.finite_query_trace_domination
#print axioms Orthemology.Tranche2.FiniteQuery.fairOracle_prefix_mass
#print axioms Orthemology.Tranche2.FiniteQuery.finite_query_trace_fair_domination
#check Orthemology.Tranche2.FiniteQuery.finite_query_trace_fair_domination

namespace Orthemology.Tranche2.FiniteQuery
open Filter
open scoped Topology

/-- A concrete causal finite-query controller cannot have positive eventual
correct-repair probability at uncountably many norm parameters. This theorem
derives trace domination from the evaluator and the explicit fair reference;
there is no `hdom` or assumed exact-readout premise. Initial private randomness
has one shared distribution and is independent of the supplied oracle law. -/
theorem countable_positive_causal_finite_query_repairs
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) [IsProbabilityMeasure ρ]
    (oracleLaw : ℝ → Measure Oracle) [∀ a, IsProbabilityMeasure (oracleLaw a)]
    (e : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0))
    (score : ℕ → S → ℝ) (hscore : ∀ n, Measurable (score n)) :
    Set.Countable {a : ℝ | a ∈ Icc 0 1 ∧
      0 < traceLaw ask next ρ (oracleLaw a)
        (finiteQueryTrace ∩ {t | ∀ᶠ n in atTop, BinaryGood a (e n) (score n (t n).1)})} := by
  let μ : Measure (Trace S) := traceLaw ask next ρ fairOracle
  haveI : IsFiniteMeasure μ := by
    dsimp [μ,traceLaw]
    infer_instance
  exact countable_positive_eventual_binary_repairs μ
    (fun a => traceLaw ask next ρ (oracleLaw a)) finiteQueryTrace
    measurable_finiteQueryTrace e he0 he1 he
    (fun n t => score n (t n).1)
    (fun n => (hscore n).comp (measurable_pi_apply n).fst)
    (fun a => finite_query_trace_fair_domination ask next ha hn ρ (oracleLaw a))

end Orthemology.Tranche2.FiniteQuery

#print axioms Orthemology.Tranche2.FiniteQuery.countable_positive_causal_finite_query_repairs
#check Orthemology.Tranche2.FiniteQuery.countable_positive_causal_finite_query_repairs
