import PolicyTailTransfer

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Set Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3.RelativeTransfer
open Orthemology.Tranche2
open Orthemology.Tranche2.FiniteAlphabetQuery

/-- On a countable output alphabet, relative atom support suffices for absolute
continuity; no global full-support reference is required. -/
theorem absolutelyContinuous_of_atom_support {E : Type*} [Countable E] [MeasurableSpace E]
    (μ ν : Measure E) (h : ∀ x, ν {x} = 0 → μ {x} = 0) : μ ≪ ν := by
  intro S hS
  have he : S = ⋃ x : S, ({x.val} : Set E) := by ext x; simp
  rw [he]
  apply measure_iUnion_null
  intro x
  exact h x.val (measure_mono_null (Set.singleton_subset_iff.mpr x.property) hS)

variable {Y : Type*} [Inhabited Y] [Countable Y]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

lemma iidOracle_prefix_atom (q : Measure Y) [IsProbabilityMeasure q] (N : ℕ) (w : Fin N → Y) :
    ((iidOracle q).map (prefixSymbols N)) {w} =
      ∏ k ∈ Finset.range N, q {prefixOracle N w k} := by
  rw [Measure.map_apply (measurable_prefixSymbols N) (measurableSet_singleton w),
    prefixSymbols_singleton_preimage,iidOracle,
    Measure.infinitePi_pi _ (fun k _ => measurableSet_singleton _)]

/-- Finite iid-prefix domination follows from relative one-symbol domination;
infinite iid product measures are not asserted absolutely continuous. -/
theorem iidOracle_prefix_domination (p q : Measure Y) [IsProbabilityMeasure p] [IsProbabilityMeasure q]
    (hpq : p ≪ q) (N : ℕ) :
    (iidOracle p).map (prefixSymbols N) ≪ (iidOracle q).map (prefixSymbols N) := by
  apply absolutelyContinuous_of_atom_support
  intro w hw
  rw [iidOracle_prefix_atom] at hw ⊢
  obtain ⟨k,hk,hz⟩ := Finset.prod_eq_zero_iff.mp hw
  exact Finset.prod_eq_zero hk (hpq hz)

/-- The existing finite-information factorization only needs relative prefix
absolute continuity, rather than positivity of every reference atom. -/
theorem relative_bounded_trace_domination
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ y, Measurable (fun s => next s y))
    (ρ : Measure S) (ν reference : Measure (Oracle Y))
    [SFinite ρ] [SFinite ν] [SFinite reference] (N : ℕ)
    (hpref : ν.map (prefixSymbols N) ≪ reference.map (prefixSymbols N)) :
    (traceLaw ask next ρ ν).restrict (boundedTrace N) ≪
      (traceLaw ask next ρ reference).restrict (boundedTrace N) := by
  rw [bounded_trace_law_factorisation ask next ha hn ρ ν N,
    bounded_trace_law_factorisation ask next ha hn ρ reference N]
  exact ((Measure.AbsolutelyContinuous.rfl.prod hpref).restrict _).map
    (measurable_finiteTrajectory ask next ha hn N)

theorem relative_finite_query_domination
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ y, Measurable (fun s => next s y))
    (ρ : Measure S) (ν reference : Measure (Oracle Y))
    [SFinite ρ] [SFinite ν] [SFinite reference]
    (hpref : ∀ N, ν.map (prefixSymbols N) ≪ reference.map (prefixSymbols N)) :
    (traceLaw ask next ρ ν).restrict finiteQueryTrace ≪
      (traceLaw ask next ρ reference).restrict finiteQueryTrace :=
  restrict_iUnion_domination _ _ boundedTrace measurable_boundedTrace
    (fun N => relative_bounded_trace_domination ask next ha hn ρ ν reference N (hpref N))

theorem positive_finite_query_event_relative
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ y, Measurable (fun s => next s y))
    (ρ : Measure S) [SFinite ρ] (p q : Measure Y) [IsProbabilityMeasure p] [IsProbabilityMeasure q]
    (hpq : p ≪ q) (E : Set (Trace S)) (hE : E ⊆ finiteQueryTrace)
    (hpos : 0 < traceLaw ask next ρ (iidOracle p) E) :
    0 < traceLaw ask next ρ (iidOracle q) E := by
  have hd := relative_finite_query_domination ask next ha hn ρ (iidOracle p) (iidOracle q)
    (iidOracle_prefix_domination p q hpq)
  by_contra hnpos
  have hz : traceLaw ask next ρ (iidOracle q) E = 0 := le_antisymm (le_of_not_gt hnpos) (zero_le _)
  have hr : ((traceLaw ask next ρ (iidOracle q)).restrict finiteQueryTrace) E = 0 := by
    rw [Measure.restrict_apply' measurable_finiteQueryTrace,Set.inter_eq_left.mpr hE]
    exact hz
  have hh := hd hr
  rw [Measure.restrict_apply' measurable_finiteQueryTrace,Set.inter_eq_left.mpr hE] at hh
  exact hpos.ne' hh

section Rows
open PolicyEmbedding
universe u v
variable {A Z : Type u} {R : Type v} [Fintype A] [Fintype Z] [DecidableEq A] [Inhabited Z]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Z] [MeasurableSingletonClass Z]

/-- Controlled kernels may have zeros; source-positive symbols need only be
rival-positive. This derives the actual row-measure domination. -/
theorem rowMeasure_relative_support
    (P Q : A → Z → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hs : ∀ a y, 0 < P a y → 0 < Q a y) :
    rowMeasure P hP hPN ≪ rowMeasure Q hQ hQN := by
  apply absolutelyContinuous_of_atom_support
  intro w hw
  change (rowPMF Q hQ hQN).toMeasure {w} = 0 at hw
  rw [PMF.toMeasure_apply_singleton _ w (measurableSet_singleton w)] at hw
  change ENNReal.ofReal (rowMass Q w) = 0 at hw
  have hz : rowMass Q w = 0 := le_antisymm (ENNReal.ofReal_eq_zero.mp hw) (rowMass_nonneg Q hQ w)
  obtain ⟨a,ha,hqa⟩ := Finset.prod_eq_zero_iff.mp hz
  have hpa : P a (w a) = 0 := by
    apply le_antisymm _ (hP _ _)
    by_contra! hp
    have hq := hs a (w a) hp
    rw [hqa] at hq
    exact (lt_irrefl 0 hq)
  change (rowPMF P hP hPN).toMeasure {w} = 0
  rw [PMF.toMeasure_apply_singleton _ w (measurableSet_singleton w)]
  change ENNReal.ofReal (rowMass P w) = 0
  rw [show rowMass P w = 0 from Finset.prod_eq_zero ha hpa,ENNReal.ofReal_zero]

/-- Relative support plus equality on the recurrent actions transfers positive
recurrence between the original canonical seeded policy laws. -/
theorem canonical_positive_tail_relative
    (U : Finset A) (π : R → History A Z → A)
    (hπ : Measurable (fun z : R × History A Z => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Z → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hs : ∀ a y, 0 < P a y → 0 < Q a y)
    (hagree : ∀ a ∈ U, P a = Q a) (d : A) (N : ℕ)
    (hpos : 0 < actionLaw π ρ P hP hPN d (RecurrentSupport.tailEvent id U N)) :
    0 < actionLaw π ρ Q hQ hQN d (RecurrentSupport.tailEvent id U N) := by
  let T := RecurrentSupport.tailEvent (traceAction π) U N
  let E := T ∩ finiteQueryTrace
  have hT : MeasurableSet T := RecurrentSupport.measurable_tailEvent (traceAction π)
    (fun n => (selected_measurable π hπ).comp (measurable_pi_apply n).fst) U N
  have hE : MeasurableSet E := hT.inter measurable_finiteQueryTrace
  have hm := RecurrentSupport.measurable_tailEvent (id : (ℕ → A) → ℕ → A) (fun n => measurable_pi_apply n) U N
  let ρS := seedLaw ρ P hP hPN
  let p := rowMeasure P hP hPN
  let q := rowMeasure Q hQ hQN
  have hp := traceLaw_action_eq_canonical U π hπ ρ P P hP hPN hP hPN (fun _ _ => rfl) d
  have hq := traceLaw_action_eq_canonical U π hπ ρ P Q hP hPN hQ hQN hagree d
  rw [← hp,Measure.map_apply (traceAction_measurable π hπ) hm] at hpos
  rw [← hq,Measure.map_apply (traceAction_measurable π hπ) hm]
  have heq : traceLaw (query U π) (step U π) ρS (iidOracle p) E =
      traceLaw (query U π) (step U π) ρS (iidOracle p) T := by
    unfold traceLaw
    rw [Measure.map_apply (measurable_trajectory _ _ (query_measurable U π hπ) (step_measurable U π hπ)) hE,
      Measure.map_apply (measurable_trajectory _ _ (query_measurable U π hπ) (step_measurable U π hπ)) hT]
    congr 1
    ext z
    exact ⟨fun h => h.1,fun ht => ⟨ht,run_tail_finitely_queries U π z.2 z.1 N ht⟩⟩
  have hr := positive_finite_query_event_relative (query U π) (step U π)
    (query_measurable U π hπ) (step_measurable U π hπ) ρS p q
    (rowMeasure_relative_support P Q hP hPN hQ hQN hs) E Set.inter_subset_right (by rwa [heq])
  exact hr.trans_le (measure_mono Set.inter_subset_left)
end Rows
end Orthemology.Tranche3.RelativeTransfer
