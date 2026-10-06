import PolicyTraceBinding
import RecurrentSupport

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped ENNReal

namespace Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {R : Type v} {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

omit [Fintype Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma run_tail_finitely_queries (U : Finset A) (π : R → History A Y → A)
    (oracle : ℕ → A → Y) (s : EvalState R A Y) (N : ℕ)
    (ht : FiniteAlphabetQuery.run (query U π) (step U π) oracle s ∈
      RecurrentSupport.tailEvent (traceAction π) U N) :
    FiniteAlphabetQuery.run (query U π) (step U π) oracle s ∈ FiniteAlphabetQuery.finiteQueryTrace := by
  have hg : ∀ᶠ n in atTop, query U π (FiniteAlphabetQuery.run (query U π) (step U π) oracle s n).1 = false := by
    apply eventually_atTop.mpr
    refine ⟨N,fun n hn => ?_⟩
    have hm := ht.2 n hn
    simpa only [query,traceAction,decide_eq_false_iff_not,not_not] using hm
  obtain ⟨K,hK⟩ := (FiniteAlphabetQuery.bounded_iff_eventually_no_query (query U π) (step U π) oracle s).mpr hg
  exact Set.mem_iUnion.mpr ⟨K,hK⟩

/-- Tail recurrence transfers under the concrete row evaluator. The event is
restricted to finite-query paths by a proved counter/action correspondence. -/
theorem evaluator_positive_tail_transfers
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure (EvalState R A Y)) [SFinite ρ]
    (ν : Measure (FiniteAlphabetQuery.Oracle (A → Y))) [SFinite ν]
    (q : Measure (A → Y)) [IsProbabilityMeasure q] (hq : ∀ row, q {row} ≠ 0) (N : ℕ)
    (hpos : 0 < FiniteAlphabetQuery.traceLaw (query U π) (step U π) ρ ν
      (RecurrentSupport.tailEvent (traceAction π) U N)) :
    0 < FiniteAlphabetQuery.traceLaw (query U π) (step U π) ρ (FiniteAlphabetQuery.iidOracle q)
      (RecurrentSupport.tailEvent (traceAction π) U N) := by
  let T := RecurrentSupport.tailEvent (traceAction π) U N
  let E := T ∩ FiniteAlphabetQuery.finiteQueryTrace
  have hT : MeasurableSet T := RecurrentSupport.measurable_tailEvent (traceAction π)
    (fun n => (selected_measurable π hπ).comp (measurable_pi_apply n).fst) U N
  have hE : MeasurableSet E := hT.inter FiniteAlphabetQuery.measurable_finiteQueryTrace
  have heq : FiniteAlphabetQuery.traceLaw (query U π) (step U π) ρ ν E =
      FiniteAlphabetQuery.traceLaw (query U π) (step U π) ρ ν T := by
    unfold FiniteAlphabetQuery.traceLaw
    rw [Measure.map_apply (FiniteAlphabetQuery.measurable_trajectory _ _ (query_measurable U π hπ) (step_measurable U π hπ)) hE,
      Measure.map_apply (FiniteAlphabetQuery.measurable_trajectory _ _ (query_measurable U π hπ) (step_measurable U π hπ)) hT]
    congr 1
    ext z
    exact ⟨fun h => h.1,fun ht => ⟨ht,run_tail_finitely_queries U π z.2 z.1 N ht⟩⟩
  have hp : 0 < FiniteAlphabetQuery.traceLaw (query U π) (step U π) ρ ν E := by rwa [heq]
  have hr := FiniteAlphabetQuery.positive_finite_query_event_transfers (query U π) (step U π)
    (query_measurable U π hπ) (step_measurable U π hπ) ρ ν q hq E Set.inter_subset_right hp
  exact hr.trans_le (measure_mono Set.inter_subset_left)

/-- Positive recurrence transfers between the ORIGINAL controlled-iid policy
laws, by the proved policy-row law equivalence. No simulator equality is an input. -/
theorem canonical_positive_tail_transfers
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 < P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 < Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hagree : ∀ a ∈ U, P a = Q a) (d : A) (N : ℕ)
    (hpos : 0 < actionLaw π ρ P (fun a y => (hP a y).le) hPN d
      (RecurrentSupport.tailEvent id U N)) :
    0 < actionLaw π ρ Q (fun a y => (hQ a y).le) hQN d
      (RecurrentSupport.tailEvent id U N) := by
  let ρS := seedLaw ρ P (fun a y => (hP a y).le) hPN
  let ν := FiniteAlphabetQuery.iidOracle (rowMeasure P (fun a y => (hP a y).le) hPN)
  let q := rowMeasure Q (fun a y => (hQ a y).le) hQN
  have hm := RecurrentSupport.measurable_tailEvent (id : (ℕ → A) → ℕ → A)
    (fun n => measurable_pi_apply n) U N
  have hp := traceLaw_action_eq_canonical U π hπ ρ P P (fun a y => (hP a y).le) hPN
    (fun a y => (hP a y).le) hPN (fun _ _ => rfl) d
  have hq := traceLaw_action_eq_canonical U π hπ ρ P Q (fun a y => (hP a y).le) hPN
    (fun a y => (hQ a y).le) hQN hagree d
  rw [← hp,Measure.map_apply (traceAction_measurable π hπ) hm] at hpos
  rw [← hq,Measure.map_apply (traceAction_measurable π hπ) hm]
  exact evaluator_positive_tail_transfers U π hπ ρS ν q (rowMeasure_full_support Q hQ hQN) N hpos

end Orthemology.Tranche2.PolicyEmbedding
