import PolicyCylinderProbability
import HistoryPathConsistency

noncomputable section
open MeasureTheory ProbabilityTheory Finset Preorder
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {R : Type v} {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

lemma history_marginal_formula
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (hagree : ∀ a ∈ U, base a = P a) (n : ℕ) (h : History A Y) :
    ((ρ.prod (feedbackLaw base P hb hbn hP hN)).map (fun z => historyTrajectory U π z n)) {h} =
      if n = h.length then
        ρ {r | ActionCompatible π r h} * ∏ i : Fin h.length, ENNReal.ofReal (P h[i].1 h[i].2)
      else 0 := by
  rw [Measure.map_apply (historyTrajectory_coordinate_measurable U π hπ n) (measurableSet_singleton h)]
  change (ρ.prod (feedbackLaw base P hb hbn hP hN)) {z | historyTrajectory U π z n = h} = _
  by_cases hn : n = h.length
  · rw [if_pos hn,hn]
    have hp := private_transcript_cylinder_probability U π ρ base P hb hbn hP hN hagree Set.univ h
    simpa only [Set.mem_univ,true_and,Set.univ_inter] using hp
  · rw [if_neg hn]
    have he : {z : Input R A Y | historyTrajectory U π z n = h} = ∅ := by
      apply Set.eq_empty_iff_forall_not_mem.mpr
      intro z hz
      have hh := congrArg List.length hz
      exact hn (by simpa only [historyTrajectory,observedHistory_length] using hh)
    rw [he,measure_empty]

/-- Every finite observed-history law agrees with the canonical model which
queries a fresh independent action-feedback row at every action. -/
theorem history_marginal_eq_all_query
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (hagree : ∀ a ∈ U, base a = P a) (n : ℕ) :
    (ρ.prod (feedbackLaw base P hb hbn hP hN)).map (fun z => historyTrajectory U π z n) =
      (ρ.prod (feedbackLaw P P hP hN hP hN)).map (fun z => historyTrajectory ∅ π z n) := by
  apply Measure.ext_of_singleton
  intro h
  rw [history_marginal_formula U π hπ ρ base P hb hbn hP hN hagree,
    history_marginal_formula ∅ π hπ ρ P P hP hN hP hN (fun a ha => (Finset.not_mem_empty a ha).elim)]

lemma observed_prefix_map_from_last
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (N : ℕ) :
    (observedTraceLaw U π ρ base P hb hbn hP hN).map (frestrictLe N) =
      ((ρ.prod (feedbackLaw base P hb hbn hP hN)).map (fun z => historyTrajectory U π z N)).map
        (reconstructPrefix (A := A) (Y := Y) N) := by
  unfold observedTraceLaw
  rw [Measure.map_map (measurable_frestrictLe N) (historyTrajectory_measurable U π hπ),
    Measure.map_map (measurable_of_countable (reconstructPrefix (A := A) (Y := Y) N))
      (historyTrajectory_coordinate_measurable U π hπ N)]
  congr 1
  funext z
  exact observedHistory_prefix_from_last U π z.2.2 z.1 (fun a n => z.2.1 (a,n)) N

/-- Exact P3 observed-law equivalence on the entire infinite path sigma-field.
The source policy is arbitrary and measurable; the one common stack law agrees
with P only on U. It is an equality of constructed laws, not an assumed bridge. -/
theorem observedTraceLaw_eq_all_query
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (hagree : ∀ a ∈ U, base a = P a) :
    observedTraceLaw U π ρ base P hb hbn hP hN = observedTraceLaw ∅ π ρ P P hP hN hP hN := by
  haveI : IsFiniteMeasure (observedTraceLaw ∅ π ρ P P hP hN hP hN) := by
    unfold observedTraceLaw
    infer_instance
  apply measure_eq_of_prefix_maps
  intro N
  rw [observed_prefix_map_from_last U π hπ ρ base P hb hbn hP hN,
    observed_prefix_map_from_last ∅ π hπ ρ P P hP hN hP hN,
    history_marginal_eq_all_query U π hπ ρ base P hb hbn hP hN hagree]

end Orthemology.Tranche2.PolicyEmbedding
