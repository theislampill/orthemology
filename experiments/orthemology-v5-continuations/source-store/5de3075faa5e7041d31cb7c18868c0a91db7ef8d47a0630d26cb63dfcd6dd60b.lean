import KilledAdaptiveHistory
import RecurrentSupport
import PruningKernel

noncomputable section
open MeasureTheory ProbabilityTheory Set
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Stochastic
universe u v
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- The un-killed observed path always selects retained pairs. -/
def HistoryStays (D : Finset A) (d : A) : Set (ℕ → History A Y) :=
  {H | ∀ n, historyAction d H n ∈ D}

omit [DecidableEq A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem historyStays_measurable (D : Finset A) (d : A) :
    MeasurableSet (HistoryStays (Y := Y) D d) := by
  simp only [HistoryStays, Set.setOf_forall]
  exact MeasurableSet.iInter (fun n =>
    D.measurableSet.preimage ((measurable_pi_apply n).comp (historyAction_measurable d)))

omit [Fintype A] [Fintype Y] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem killedHistory_alive_iff (D : Finset A) (d : A) (H : ℕ → History A Y) (n : ℕ) :
    (killedHistory D d H n).1 = true ↔ AlivePrefix D d H n := by
  by_cases h : AlivePrefix D d H n <;> simp [killedHistory, h]

omit [Fintype A] [Fintype Y] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem killedHistory_all_alive_iff (D : Finset A) (d : A) (H : ℕ → History A Y) :
    (∀ n, (killedHistory D d H n).1 = true) ↔ H ∈ HistoryStays D d := by
  constructor
  · intro h n
    exact (killedHistory_alive_iff D d H (n+1)).mp (h (n+1)) n (by simp)
  · intro h n
    apply (killedHistory_alive_iff D d H n).mpr
    exact fun k _ => h k

omit [Fintype A] [Fintype Y] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem killedHistory_records_of_stays (D : Finset A) (d : A)
    (H : ℕ → History A Y) (h : H ∈ HistoryStays D d) :
    (fun n => (killedHistory D d H n).2) = H := by
  funext n
  have hA : AlivePrefix D d H n := fun k _ => h k
  simp [killedHistory, hA]

/-- A measurable event on the killed path that retains all original information
on never-killed paths, and rejects every killed path. -/
def aliveHistoryEvent (C : Set (ℕ → History A Y)) : Set (ℕ → Bool × History A Y) :=
  {K | (∀ n, (K n).1 = true) ∧ (fun n => (K n).2) ∈ C}

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem aliveHistoryEvent_measurable (C : Set (ℕ → History A Y)) (hC : MeasurableSet C) :
    MeasurableSet (aliveHistoryEvent C) := by
  change MeasurableSet ({K : ℕ → Bool × History A Y | ∀ n, (K n).1 = true} ∩
    {K | (fun n => (K n).2) ∈ C})
  apply MeasurableSet.inter
  · simp only [Set.setOf_forall]
    exact MeasurableSet.iInter (fun n =>
      (measurableSet_singleton true).preimage (measurable_pi_apply n).fst)
  · exact hC.preimage (measurable_pi_lambda _ (fun n => (measurable_pi_apply n).snd))

omit [Fintype A] [Fintype Y] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem aliveHistoryEvent_preimage (D : Finset A) (d : A) (C : Set (ℕ → History A Y)) :
    killedHistory D d ⁻¹' aliveHistoryEvent C = C ∩ HistoryStays D d := by
  ext H
  constructor
  · rintro ⟨hA, hC⟩
    have hS := (killedHistory_all_alive_iff D d H).mp hA
    rw [killedHistory_records_of_stays D d H hS] at hC
    exact ⟨hC, hS⟩
  · rintro ⟨hC, hS⟩
    refine ⟨(killedHistory_all_alive_iff D d H).mpr hS, ?_⟩
    rwa [killedHistory_records_of_stays D d H hS]

/-- Any measurable observed-history event, intersected with remaining in the
component forever, has the same probability under equal full rows there. -/
theorem canonical_history_event_eq_on_component
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hagree : ∀ a ∈ D, P a = Q a) (d : A)
    (C : Set (ℕ → History A Y)) (hC : MeasurableSet C) :
    observedTraceLaw ∅ π ρ P P hP hPN hP hPN (C ∩ HistoryStays D d) =
      observedTraceLaw ∅ π ρ Q Q hQ hQN hQ hQN (C ∩ HistoryStays D d) := by
  have heq := canonical_killed_historyLaw_eq D π hπ ρ P Q hP hPN hQ hQN hagree d
  have hm := aliveHistoryEvent_measurable C hC
  have hv := congrArg (fun μ : Measure (ℕ → Bool × History A Y) => μ (aliveHistoryEvent C)) heq
  simpa only [Measure.map_apply (killedHistory_measurable D d) hm, aliveHistoryEvent_preimage] using hv

/-- Equality of actual infinite observed-history measures restricted to surviving
inside the component. No conditioning-to-probability-one assertion is made. -/
theorem canonical_history_restrict_eq
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hagree : ∀ a ∈ D, P a = Q a) (d : A) :
    (observedTraceLaw ∅ π ρ P P hP hPN hP hPN).restrict (HistoryStays D d) =
      (observedTraceLaw ∅ π ρ Q Q hQ hQN hQ hQN).restrict (HistoryStays D d) := by
  apply Measure.ext
  intro C hC
  rw [Measure.restrict_apply hC, Measure.restrict_apply hC]
  exact canonical_history_event_eq_on_component D π hπ ρ P Q hP hPN hQ hQN hagree d C hC

/-- Every retained pair recurs, and no outside pair is ever used. -/
def SurvivingRecurrent (D : Finset A) (d : A) : Set (ℕ → History A Y) :=
  (historyAction d ⁻¹' exactRecurrentEvent id D) ∩ HistoryStays D d

omit [DecidableEq A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem survivingRecurrent_measurable (D : Finset A) (d : A) :
    MeasurableSet (SurvivingRecurrent (Y := Y) D d) :=
  ((measurable_exactRecurrentEvent id (fun n => measurable_pi_apply n) D).preimage
    (historyAction_measurable d)).inter (historyStays_measurable D d)

/-- Measurable exact-recurrence events transfer by equality of constructed laws. -/
theorem canonical_surviving_recurrent_eq
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hagree : ∀ a ∈ D, P a = Q a) (d : A) :
    observedTraceLaw ∅ π ρ P P hP hPN hP hPN (SurvivingRecurrent D d) =
      observedTraceLaw ∅ π ρ Q Q hQ hQN hQ hQN (SurvivingRecurrent D d) := by
  exact canonical_history_event_eq_on_component D π hπ ρ P Q hP hPN hQ hQN hagree d _
    ((measurable_exactRecurrentEvent id (fun n => measurable_pi_apply n) D).preimage
      (historyAction_measurable d))

/-- The actual minimum-recurrent-priority parity event. -/
def ParitySuccess (priority : A → ℕ) (x : ℕ → A) : Prop :=
  ∃ k, IsMinimum priority (recurrentSet x) k ∧ k % 2 = 0

omit [DecidableEq A] in
theorem paritySuccess_measurable (priority : A → ℕ) :
    MeasurableSet {x : ℕ → A | ParitySuccess priority x} := by
  classical
  have heq : {x : ℕ → A | ParitySuccess priority x} =
      ⋃ (U : Finset A) (_ : ∃ k, IsMinimum priority U k ∧ k % 2 = 0), exactRecurrentEvent id U := by
    ext x
    simp only [Set.mem_setOf_eq, Set.mem_iUnion, exactRecurrentEvent, id_eq]
    constructor
    · intro h
      exact ⟨recurrentSet x, h, rfl⟩
    · rintro ⟨U, h, hEq⟩
      change recurrentSet x = U at hEq
      simpa only [ParitySuccess, hEq] using h
  rw [heq]
  exact MeasurableSet.iUnion (fun U => MeasurableSet.iUnion (fun _ =>
    measurable_exactRecurrentEvent id (fun n => measurable_pi_apply n) U))

/-- New parity necessity kernel: a positive surviving recurrent component under P
must have even minimum for any full-row-matching Q under which this same common
policy wins parity almost surely. Law transfer is derived, not hypothesized. -/
theorem matching_model_even_on_positive_surviving_recurrence
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hagree : ∀ a ∈ D, P a = Q a) (d : A) (priority : A → ℕ)
    (hAS : ∀ᵐ H ∂observedTraceLaw ∅ π ρ Q Q hQ hQN hQ hQN,
      ParitySuccess priority (historyAction d H))
    (hPos : 0 < observedTraceLaw ∅ π ρ P P hP hPN hP hPN (SurvivingRecurrent D d)) :
    ∃ k, IsMinimum priority D k ∧ k % 2 = 0 := by
  rw [canonical_surviving_recurrent_eq D π hπ ρ P Q hP hPN hQ hQN hagree d] at hPos
  obtain ⟨H, hH, hParity⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hPos.ne'
    (ae_restrict_of_ae hAS)
  have hRec : recurrentSet (historyAction d H) = D := hH.1
  simpa only [ParitySuccess, hRec] using hParity

end HiddenParity.Stochastic
