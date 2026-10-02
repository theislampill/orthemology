import FiniteQueryMeasure

open MeasureTheory Set
open scoped ENNReal

namespace Orthemology.Tranche2.FiniteQuery

/-- A common dominating first marginal and a countable second alphabet imply
joint domination by a full-support product reference. No independence premise. -/
theorem joint_dominated_by_countable_reference
    {S J : Type*} [MeasurableSpace S] [MeasurableSpace J]
    [Countable J] [MeasurableSingletonClass J]
    (η : Measure (S × J)) (ρ : Measure S) (r : Measure J)
    [SFinite ρ] [SFinite r]
    (hseed : η.map Prod.fst ≪ ρ) (hr : ∀ j, r {j} ≠ 0) :
    η ≪ ρ.prod r := by
  apply Measure.AbsolutelyContinuous.mk
  intro A hA hnull
  let B : Set S := ⋃ j : J, (fun s => (s,j)) ⁻¹' A
  have hB : MeasurableSet B :=
    MeasurableSet.iUnion fun j => hA.preimage (measurable_id.prodMk measurable_const)
  have hsections := (Measure.measure_prod_null hA).mp hnull
  have hnot : ∀ᵐ s ∂ρ, s ∉ B := by
    filter_upwards [hsections] with s hs
    intro hmem
    obtain ⟨j,hj⟩ := Set.mem_iUnion.mp hmem
    exact hr j (measure_mono_null (Set.singleton_subset_iff.mpr hj) hs)
  have hBzero : ρ B = 0 := by
    simpa only [ae_iff, not_not] using hnot
  have hm := hseed hBzero
  rw [Measure.map_apply measurable_fst hB] at hm
  apply measure_mono_null _ hm
  intro x hx
  exact Set.mem_iUnion.mpr ⟨x.2,hx⟩

noncomputable def jointTraceLaw {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S) (η : Measure (S × Oracle)) :
    Measure (Trace S) := η.map (fun z => run ask next z.2 z.1)

/-- Exact finite-prefix representation for a general seed/oracle joint law. -/
theorem bounded_joint_trace_factorisation
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (η : Measure (S × Oracle)) (N : ℕ) :
    (jointTraceLaw ask next η).restrict (boundedTrace N) =
      ((η.map (prefixInput N)).restrict
        (finiteTrajectory ask next N ⁻¹' boundedTrace N)).map (finiteTrajectory ask next N) := by
  rw [jointTraceLaw, Measure.restrict_map (measurable_trajectory ask next ha hn)
    (measurable_boundedTrace N), bounded_event_prefix]
  exact restricted_observable_factorisation _ (prefixInput N) _ (finiteTrajectory ask next N)
    (measurable_prefixInput N) (measurable_finiteTrajectory ask next ha hn N) _
    ((measurable_boundedTrace N).preimage (measurable_finiteTrajectory ask next ha hn N))
    (trajectory_prefix_on_bounded ask next N)

/-- Finite-query domination survives arbitrary oracle/seed correlation as long
as the initial-state marginal has a common dominating reference. -/
theorem correlated_finite_query_trace_domination
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (η : Measure (S × Oracle)) (ρ : Measure S) [SFinite ρ]
    (hseed : η.map Prod.fst ≪ ρ) :
    (jointTraceLaw ask next η).restrict finiteQueryTrace ≪
      (traceLaw ask next ρ fairOracle).restrict finiteQueryTrace := by
  apply restrict_iUnion_domination _ _ boundedTrace measurable_boundedTrace
  intro N
  rw [bounded_joint_trace_factorisation ask next ha hn η N,
    bounded_trace_law_factorisation ask next ha hn ρ fairOracle N]
  have hprefixSeed : (η.map (prefixInput N)).map Prod.fst ≪ ρ := by
    rw [Measure.map_map measurable_fst (measurable_prefixInput N)]
    exact hseed
  have hd := joint_dominated_by_countable_reference
    (η.map (prefixInput N)) ρ (fairOracle.map (prefixBits N)) hprefixSeed
    (fairOracle_prefix_nonzero N)
  exact (hd.restrict _).map (measurable_finiteTrajectory ask next ha hn N)

open Filter
open scoped Topology

/-- The full finite-query norm-repair obstruction for arbitrary correlated
oracle laws with one shared initial private-state marginal. -/
theorem countable_positive_shared_seed_query_repairs
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
      0 < jointTraceLaw ask next (inputLaw a)
        (finiteQueryTrace ∩ {t | ∀ᶠ n in atTop, BinaryGood a (e n) (score n (t n).1)})} := by
  let μ : Measure (Trace S) := traceLaw ask next ρ fairOracle
  haveI : IsFiniteMeasure μ := by dsimp [μ,traceLaw]; infer_instance
  exact countable_positive_eventual_binary_repairs μ
    (fun a => jointTraceLaw ask next (inputLaw a)) finiteQueryTrace
    measurable_finiteQueryTrace e he0 he1 he
    (fun n t => score n (t n).1)
    (fun n => (hscore n).comp (measurable_pi_apply n).fst)
    (fun a => correlated_finite_query_trace_domination ask next ha hn (inputLaw a) ρ
      ((hseed a).absolutelyContinuous))

end Orthemology.Tranche2.FiniteQuery

#print axioms Orthemology.Tranche2.FiniteQuery.joint_dominated_by_countable_reference
#print axioms Orthemology.Tranche2.FiniteQuery.correlated_finite_query_trace_domination
#print axioms Orthemology.Tranche2.FiniteQuery.countable_positive_shared_seed_query_repairs
#check Orthemology.Tranche2.FiniteQuery.countable_positive_shared_seed_query_repairs
