import GenericFiniteQueryLocality
import Mathlib.Probability.ProductMeasure

open MeasureTheory Set
open scoped ENNReal

namespace Orthemology.Tranche2.FiniteAlphabetQuery
variable {Y : Type*} [Inhabited Y] [Countable Y]
  [MeasurableSpace Y] [MeasurableSingletonClass Y]

abbrev Oracle (Y : Type*) := ℕ → Y
abbrev Trace (S : Type*) := ℕ → S × ℕ

section Measurable
variable {S : Type*} [MeasurableSpace S]

lemma measurable_advance_joint (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b)) :
    Measurable (fun z : (S × ℕ) × (Oracle Y) => advance ask next z.2 z.1) := by
  have hnext : Measurable (fun z : S × Y => next z.1 z.2) :=
    measurable_from_prod_countable hn
  have heval : Measurable (fun z : (Oracle Y) × ℕ => z.1 z.2) :=
    measurable_from_prod_countable (fun n => measurable_pi_apply n)
  have hv : Measurable (fun z : (S × ℕ) × (Oracle Y) => z.2 z.1.2) :=
    heval.comp (measurable_snd.prodMk measurable_fst.snd)
  have hc : MeasurableSet {z : (S × ℕ) × (Oracle Y) | ask z.1.1 = true} :=
    (measurableSet_singleton true).preimage (ha.comp measurable_fst.fst)
  unfold advance
  apply Measurable.ite hc
  · exact (hnext.comp (measurable_fst.fst.prodMk hv)).prodMk
      (measurable_fst.snd.add_const 1)
  · exact ((hn default).comp measurable_fst.fst).prodMk measurable_fst.snd

lemma measurable_run (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b)) (n : ℕ) :
    Measurable (fun z : S × (Oracle Y) => run ask next z.2 z.1 n) := by
  induction n with
  | zero => exact measurable_fst.prodMk measurable_const
  | succ n ih =>
      exact (measurable_advance_joint ask next ha hn).comp (ih.prodMk measurable_snd)

lemma measurable_trajectory (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b)) :
    Measurable (fun z : S × (Oracle Y) => run ask next z.2 z.1) := by
  exact measurable_pi_lambda _ (measurable_run ask next ha hn)

def boundedTrace (N : ℕ) : Set (Trace S) := {t | ∀ n, (t n).2 ≤ N}

lemma measurable_boundedTrace (N : ℕ) : MeasurableSet (boundedTrace (S := S) N) := by
  simp only [boundedTrace, setOf_forall]
  apply MeasurableSet.iInter
  intro n
  exact measurableSet_le (measurable_pi_apply n).snd measurable_const

lemma measurable_prefixOracle (N : ℕ) : Measurable (prefixOracle (Y := Y) N) := by
  apply measurable_pi_lambda
  intro k
  by_cases hk : k < N
  · simpa [prefixOracle,hk] using (measurable_pi_apply (⟨k,hk⟩ : Fin N))
  · simpa [prefixOracle,hk] using (measurable_const : Measurable (fun _ : Fin N → Y => default))

def prefixInput (N : ℕ) (z : S × (Oracle Y)) : S × (Fin N → Y) :=
  (z.1, fun i => z.2 i)

lemma measurable_prefixInput (N : ℕ) : Measurable (prefixInput (S := S) (Y := Y) N) := by
  exact measurable_fst.prodMk (measurable_pi_lambda _ fun i =>
    (measurable_pi_apply i.val).comp measurable_snd)

def finiteTrajectory (ask : S → Bool) (next : S → Y → S) (N : ℕ)
    (z : S × (Fin N → Y)) : Trace S := run ask next (prefixOracle N z.2) z.1

lemma measurable_finiteTrajectory (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b)) (N : ℕ) :
    Measurable (finiteTrajectory ask next N) :=
  (measurable_trajectory ask next ha hn).comp
    (measurable_fst.prodMk ((measurable_prefixOracle N).comp measurable_snd))

/-- Both the bounded-query event and every full-run observable factor through
seed plus N oracle bits. This includes never asking query N+1. -/
lemma bounded_event_prefix (ask : S → Bool) (next : S → Y → S) (N : ℕ) :
    (fun z : S × (Oracle Y) => run ask next z.2 z.1) ⁻¹' boundedTrace N =
    prefixInput N ⁻¹' (finiteTrajectory ask next N ⁻¹' boundedTrace N) := by
  ext z
  exact bounded_prefix_equivalence ask next z.2
    (prefixOracle N (fun i => z.2 i)) z.1 N (prefixOracle_agrees z.2 N)

lemma trajectory_prefix_on_bounded (ask : S → Bool) (next : S → Y → S)
    (N : ℕ) (z : S × (Oracle Y))
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

end Orthemology.Tranche2.FiniteAlphabetQuery

namespace Orthemology.Tranche2.FiniteAlphabetQuery
variable {Y : Type*} [Inhabited Y] [Countable Y]
  [MeasurableSpace Y] [MeasurableSingletonClass Y]

lemma absolutelyContinuous_of_singletons {E : Type*} [MeasurableSpace E]
    (μ ν : Measure E) (hν : ∀ x, ν {x} ≠ 0) : μ ≪ ν := by
  intro A hA
  have hEmpty : A = ∅ := by
    apply Set.eq_empty_iff_forall_not_mem.mpr
    intro x hx
    exact hν x (measure_mono_null (Set.singleton_subset_iff.mpr hx) hA)
  simp [hEmpty]

def prefixSymbols (N : ℕ) (oracle : (Oracle Y)) : Fin N → Y := fun i => oracle i

lemma measurable_prefixSymbols (N : ℕ) : Measurable (prefixSymbols (Y := Y) N) :=
  measurable_pi_lambda _ fun i => measurable_pi_apply i.val

section Laws
variable {S : Type*} [MeasurableSpace S]

noncomputable def traceLaw (ask : S → Bool) (next : S → Y → S)
    (ρ : Measure S) (ν : Measure (Oracle Y)) : Measure (Trace S) :=
  (ρ.prod ν).map (fun z => run ask next z.2 z.1)

lemma input_prefix_map (ρ : Measure S) (ν : Measure (Oracle Y))
    [SFinite ρ] [SFinite ν] (N : ℕ) :
    (ρ.prod ν).map (prefixInput N) = ρ.prod (ν.map (prefixSymbols N)) := by
  change (ρ.prod ν).map (Prod.map id (prefixSymbols N)) = _
  rw [← Measure.map_prod_map ρ ν measurable_id (measurable_prefixSymbols N)]
  simp

/-- The restricted observed trace is genuinely a finite-input pushforward;
the event of never querying beyond N is also carried by the finite input. -/
theorem bounded_trace_law_factorisation
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) (ν : Measure (Oracle Y)) [SFinite ρ] [SFinite ν] (N : ℕ) :
    (traceLaw ask next ρ ν).restrict (boundedTrace N) =
      ((ρ.prod (ν.map (prefixSymbols N))).restrict
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
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) (ν reference : Measure (Oracle Y))
    [SFinite ρ] [SFinite ν] [SFinite reference] (N : ℕ)
    (hfull : ∀ w, (reference.map (prefixSymbols N)) {w} ≠ 0) :
    (traceLaw ask next ρ ν).restrict (boundedTrace N) ≪
      (traceLaw ask next ρ reference).restrict (boundedTrace N) := by
  rw [bounded_trace_law_factorisation ask next ha hn ρ ν N,
    bounded_trace_law_factorisation ask next ha hn ρ reference N]
  have hp : ν.map (prefixSymbols N) ≪ reference.map (prefixSymbols N) :=
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
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) (ν reference : Measure (Oracle Y))
    [SFinite ρ] [SFinite ν] [SFinite reference]
    (hfull : ∀ N w, (reference.map (prefixSymbols N)) {w} ≠ 0) :
    (traceLaw ask next ρ ν).restrict finiteQueryTrace ≪
      (traceLaw ask next ρ reference).restrict finiteQueryTrace := by
  exact restrict_iUnion_domination _ _ boundedTrace measurable_boundedTrace
    (fun N => bounded_trace_domination ask next ha hn ρ ν reference N (hfull N))

end Orthemology.Tranche2.FiniteAlphabetQuery

#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_trace_domination
#check Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_trace_domination
