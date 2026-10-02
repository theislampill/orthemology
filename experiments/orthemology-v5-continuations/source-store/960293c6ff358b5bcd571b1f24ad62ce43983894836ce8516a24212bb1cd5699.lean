import RelativeTailTransfer

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Set Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3.RelativeTransfer
open Orthemology.Tranche2
open Orthemology.Tranche2.FiniteAlphabetQuery
open Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {A Y : Type u} {R : Type v} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Transfer an arbitrary measurable action event whose paths eventually stay
in the equal-law set. Extra guards, such as all-prefix licensing, are retained. -/
theorem canonical_positive_event_relative
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hs : ∀ a y, 0 < P a y → 0 < Q a y)
    (hagree : ∀ a ∈ U, P a = Q a) (d : A)
    (C : Set (ℕ → A)) (hC : MeasurableSet C) (N : ℕ)
    (hstay : ∀ x ∈ C, ∀ n ≥ N, x n ∈ U)
    (hpos : 0 < actionLaw π ρ P hP hPN d C) :
    0 < actionLaw π ρ Q hQ hQN d C := by
  let T := traceAction π ⁻¹' C
  let E := T ∩ finiteQueryTrace
  have hT : MeasurableSet T := hC.preimage (traceAction_measurable π hπ)
  have hE : MeasurableSet E := hT.inter measurable_finiteQueryTrace
  let ρS := seedLaw ρ P hP hPN
  let p := rowMeasure P hP hPN
  let q := rowMeasure Q hQ hQN
  have hp := traceLaw_action_eq_canonical U π hπ ρ P P hP hPN hP hPN (fun _ _ => rfl) d
  have hq := traceLaw_action_eq_canonical U π hπ ρ P Q hP hPN hQ hQN hagree d
  rw [← hp,Measure.map_apply (traceAction_measurable π hπ) hC] at hpos
  rw [← hq,Measure.map_apply (traceAction_measurable π hπ) hC]
  have hrun : ∀ z : EvalState R A Y × Oracle (A → Y),
      run (query U π) (step U π) z.2 z.1 ∈ T → run (query U π) (step U π) z.2 z.1 ∈ finiteQueryTrace := by
    intro z hz
    have hno : ∀ᶠ n in atTop, query U π (run (query U π) (step U π) z.2 z.1 n).1 = false := by
      apply eventually_atTop.mpr
      refine ⟨N,fun n hn => ?_⟩
      have hh := hstay _ hz n hn
      simpa only [query,traceAction,decide_eq_false_iff_not,not_not] using hh
    obtain ⟨K,hK⟩ := (bounded_iff_eventually_no_query (query U π) (step U π) z.2 z.1).mpr hno
    exact Set.mem_iUnion.mpr ⟨K,hK⟩
  have heq : traceLaw (query U π) (step U π) ρS (iidOracle p) E =
      traceLaw (query U π) (step U π) ρS (iidOracle p) T := by
    unfold traceLaw
    rw [Measure.map_apply (measurable_trajectory _ _ (query_measurable U π hπ) (step_measurable U π hπ)) hE,
      Measure.map_apply (measurable_trajectory _ _ (query_measurable U π hπ) (step_measurable U π hπ)) hT]
    congr 1
    ext z
    exact ⟨fun h => h.1,fun ht => ⟨ht,hrun z ht⟩⟩
  have hr := positive_finite_query_event_relative (query U π) (step U π)
    (query_measurable U π hπ) (step_measurable U π hπ) ρS p q
    (rowMeasure_relative_support P Q hP hPN hQ hQN hs) E Set.inter_subset_right (by rwa [heq])
  exact hr.trans_le (measure_mono Set.inter_subset_left)

def alwaysIn (D : Finset A) : Set (ℕ → A) := {x | ∀ n, x n ∈ D}

lemma measurable_alwaysIn (D : Finset A) : MeasurableSet (alwaysIn D) := by
  simp only [alwaysIn,Set.setOf_forall]
  exact MeasurableSet.iInter (fun n => D.measurableSet.preimage (measurable_pi_apply n))

lemma zero_prefix_map (ν : Measure (Oracle (A → Y))) [IsProbabilityMeasure ν] :
    ν.map (prefixSymbols 0) = Measure.dirac (default : Fin 0 → (A → Y)) := by
  have he : prefixSymbols (Y := A → Y) 0 = fun _ => (default : Fin 0 → (A → Y)) :=
    funext (fun _ => Subsingleton.elim _ _)
  rw [he,Measure.map_const,measure_univ,one_smul]

/-- Zero informative queries leave the oracle law completely unused. -/
lemma zero_query_restricted_law_eq
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρS : Measure (EvalState R A Y)) [SFinite ρS]
    (ν ν' : Measure (Oracle (A → Y))) [IsProbabilityMeasure ν] [IsProbabilityMeasure ν'] :
    (traceLaw (query D π) (step D π) ρS ν).restrict (boundedTrace 0) =
      (traceLaw (query D π) (step D π) ρS ν').restrict (boundedTrace 0) := by
  rw [bounded_trace_law_factorisation _ _ (query_measurable D π hπ) (step_measurable D π hπ),
    bounded_trace_law_factorisation _ _ (query_measurable D π hπ) (step_measurable D π hπ),
    zero_prefix_map,zero_prefix_map]

omit [Fintype Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma all_inside_zero_queries (D : Finset A) (π : R → History A Y → A)
    (s : EvalState R A Y) (oracle : Oracle (A → Y))
    (h : traceAction π (run (query D π) (step D π) oracle s) ∈ alwaysIn D) :
    run (query D π) (step D π) oracle s ∈ boundedTrace 0 := by
  have he : ∀ n, (run (query D π) (step D π) oracle s n).2 = 0 := by
    intro n
    induction n with
    | zero => rfl
    | succ n ih =>
      have hn : query D π (run (query D π) (step D π) oracle s n).1 = false := by
        have hh := h n
        simpa only [query,traceAction,decide_eq_false_iff_not,not_not] using hh
      simp only [run,advance,hn,Bool.false_eq_true,↓reduceIte,ih]
  exact fun n => le_of_eq (he n)

/-- Laws agreeing on D agree on every measurable action event restricted to
staying in D forever, even if all other action laws differ or contain zeros. -/
theorem canonical_event_eq_on_visited
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hagree : ∀ a ∈ D, P a = Q a) (d : A)
    (C : Set (ℕ → A)) (hC : MeasurableSet C) (hstay : C ⊆ alwaysIn D) :
    actionLaw π ρ P hP hPN d C = actionLaw π ρ Q hQ hQN d C := by
  let T := traceAction π ⁻¹' C
  have hT : MeasurableSet T := hC.preimage (traceAction_measurable π hπ)
  let ρS := seedLaw ρ P hP hPN
  have he := zero_query_restricted_law_eq D π hπ ρS
    (iidOracle (rowMeasure P hP hPN)) (iidOracle (rowMeasure Q hQ hQN))
  have hp := traceLaw_action_eq_canonical D π hπ ρ P P hP hPN hP hPN (fun _ _ => rfl) d
  have hq := traceLaw_action_eq_canonical D π hπ ρ P Q hP hPN hQ hQN hagree d
  rw [← hp,← hq,Measure.map_apply (traceAction_measurable π hπ) hC,
    Measure.map_apply (traceAction_measurable π hπ) hC]
  have hres : ∀ (ν : Measure (Oracle (A → Y))) [IsProbabilityMeasure ν],
      (traceLaw (query D π) (step D π) ρS ν).restrict (boundedTrace 0) T =
        traceLaw (query D π) (step D π) ρS ν T := by
    intro ν hν
    rw [Measure.restrict_apply' (measurable_boundedTrace 0)]
    unfold traceLaw
    rw [Measure.map_apply (measurable_trajectory _ _ (query_measurable D π hπ) (step_measurable D π hπ))
      (hT.inter (measurable_boundedTrace 0)),
      Measure.map_apply (measurable_trajectory _ _ (query_measurable D π hπ) (step_measurable D π hπ)) hT]
    congr 1
    ext z
    exact ⟨fun h => h.1,fun h => ⟨h,all_inside_zero_queries D π z.1 z.2 (hstay h)⟩⟩
  have hh := congrArg (fun μ : Measure (Trace (EvalState R A Y)) => μ T) he
  simpa only [hres] using hh

/-- Stable true-model support is needed only on the actions the source path
actually uses. Rival-positive finite information outside the tail is preserved. -/
theorem canonical_positive_tail_on_safe_actions
    (D U : Finset A) (hUD : U ⊆ D) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hs : ∀ a ∈ D, ∀ y, 0 < P a y → 0 < Q a y)
    (hagree : ∀ a ∈ U, P a = Q a) (d : A) (N : ℕ)
    (hpos : 0 < actionLaw π ρ P hP hPN d (RecurrentSupport.tailEvent id U N ∩ alwaysIn D)) :
    0 < actionLaw π ρ Q hQ hQN d (RecurrentSupport.tailEvent id U N ∩ alwaysIn D) := by
  classical
  let F := fun a => if a ∈ D then P a else Q a
  have hf : ∀ a y, 0 ≤ F a y := by intro a y; dsimp [F]; split_ifs <;> first | exact hP a y | exact hQ a y
  have hn : ∀ a, ∑ y, F a y = 1 := by intro a; dsimp [F]; split_ifs <;> first | exact hPN a | exact hQN a
  have hdom : ∀ a y, 0 < F a y → 0 < Q a y := by
    intro a y hy
    by_cases ha : a ∈ D
    · exact hs a ha y (by simpa only [F,if_pos ha] using hy)
    · simpa only [F,if_neg ha] using hy
  have hagF : ∀ a ∈ U, F a = Q a := by
    intro a ha
    simpa only [F,if_pos (hUD ha)] using hagree a ha
  have hm : MeasurableSet (RecurrentSupport.tailEvent id U N ∩ alwaysIn D) :=
    (RecurrentSupport.measurable_tailEvent id (fun n => measurable_pi_apply n) U N).inter (measurable_alwaysIn D)
  have he := canonical_event_eq_on_visited D π hπ ρ P F hP hPN hf hn
    (fun a ha => by simp only [F,if_pos ha]) d _ hm Set.inter_subset_right
  rw [he] at hpos
  exact canonical_positive_event_relative U π hπ ρ F Q hf hn hQ hQN hdom hagF d _ hm N
    (fun x hx n hn => hx.1.2 n hn) hpos
end Orthemology.Tranche3.RelativeTransfer
