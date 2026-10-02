import GenericFiniteQueryMeasure

open MeasureTheory Set

namespace Orthemology.Tranche2.FiniteAlphabetQuery
variable {Y : Type*} [Inhabited Y] [Countable Y]
  [MeasurableSpace Y] [MeasurableSingletonClass Y]

noncomputable def iidOracle (q : Measure Y) [IsProbabilityMeasure q] : Measure (Oracle Y) :=
  Measure.infinitePi (fun _ : ℕ => q)

instance iidOracle_probability (q : Measure Y) [IsProbabilityMeasure q] :
    IsProbabilityMeasure (iidOracle q) := by
  unfold iidOracle
  infer_instance

lemma prefixSymbols_singleton_preimage (N : ℕ) (w : Fin N → Y) :
    prefixSymbols N ⁻¹' {w} = Set.pi (Finset.range N : Set ℕ)
      (fun k => {prefixOracle N w k}) := by
  ext oracle
  simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_pi,
    Finset.mem_coe, Finset.mem_range]
  constructor
  · intro h k hk
    have hv := congrFun h (⟨k,hk⟩ : Fin N)
    simpa [prefixSymbols,prefixOracle,hk] using hv
  · intro h
    funext i
    have hv := h i.val i.isLt
    simpa [prefixSymbols,prefixOracle,i.isLt] using hv

/-- Every finite symbol word has positive mass under a genuinely full-support
rival law. This is the rival's own law, not a merely dominating fair reference. -/
theorem iidOracle_prefix_nonzero (q : Measure Y) [IsProbabilityMeasure q]
    (hq : ∀ y, q {y} ≠ 0) (N : ℕ) (w : Fin N → Y) :
    ((iidOracle q).map (prefixSymbols N)) {w} ≠ 0 := by
  rw [Measure.map_apply (measurable_prefixSymbols N) (measurableSet_singleton w),
    prefixSymbols_singleton_preimage,iidOracle,
    Measure.infinitePi_pi _ (fun k _ => measurableSet_singleton _)]
  exact Finset.prod_ne_zero_iff.mpr (fun k _ => hq _)

/-- Observed finite-query traces under any independent-seed oracle law are
dominated by the actual full-support iid rival's observed traces. -/
theorem finite_query_domination_by_iid_rival
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ y, Measurable (fun s => next s y))
    (ρ : Measure S) [SFinite ρ] (ν : Measure (Oracle Y)) [SFinite ν]
    (q : Measure Y) [IsProbabilityMeasure q] (hq : ∀ y, q {y} ≠ 0) :
    (traceLaw ask next ρ ν).restrict finiteQueryTrace ≪
      (traceLaw ask next ρ (iidOracle q)).restrict finiteQueryTrace :=
  finite_query_trace_domination ask next ha hn ρ ν (iidOracle q)
    (iidOracle_prefix_nonzero q hq)

/-- A positive event of finite informative querying transfers to the actual
rival measure. Two measures merely dominated by a third would not suffice. -/
theorem positive_finite_query_event_transfers
    {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ y, Measurable (fun s => next s y))
    (ρ : Measure S) [SFinite ρ] (ν : Measure (Oracle Y)) [SFinite ν]
    (q : Measure Y) [IsProbabilityMeasure q] (hq : ∀ y, q {y} ≠ 0)
    (E : Set (Trace S)) (hE : E ⊆ finiteQueryTrace)
    (hpos : 0 < traceLaw ask next ρ ν E) :
    0 < traceLaw ask next ρ (iidOracle q) E := by
  have hd := finite_query_domination_by_iid_rival ask next ha hn ρ ν q hq
  by_contra h
  have hz : traceLaw ask next ρ (iidOracle q) E = 0 :=
    le_antisymm (le_of_not_gt h) (zero_le _)
  have hr : ((traceLaw ask next ρ (iidOracle q)).restrict finiteQueryTrace) E = 0 := by
    rw [Measure.restrict_apply' measurable_finiteQueryTrace,Set.inter_eq_left.mpr hE]
    exact hz
  have ht := hd hr
  rw [Measure.restrict_apply' measurable_finiteQueryTrace,Set.inter_eq_left.mpr hE] at ht
  exact (ne_of_gt hpos) ht

end Orthemology.Tranche2.FiniteAlphabetQuery

#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_domination_by_iid_rival
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.positive_finite_query_event_transfers
#check Orthemology.Tranche2.FiniteAlphabetQuery.positive_finite_query_event_transfers
