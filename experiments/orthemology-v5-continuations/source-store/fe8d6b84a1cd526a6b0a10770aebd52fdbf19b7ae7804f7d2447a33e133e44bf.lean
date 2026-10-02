import PolicyObservedLaw

noncomputable section
open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {R : Type v} {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

def initialState (z : R × FlatStack A Y) : EvalState R A Y := (z.1,((fun a n => z.2 (a,n)),[]))
omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma initialState_measurable : Measurable (initialState (R := R) (A := A) (Y := Y)) :=
  measurable_fst.prodMk ((measurable_pi_lambda _ (fun a => measurable_pi_lambda _ (fun n =>
    (measurable_pi_apply (a,n)).comp measurable_snd))).prodMk measurable_const)

def seedLaw (ρ : Measure R) (base : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1) : Measure (EvalState R A Y) :=
  (ρ.prod (stackMeasure base hb hbn)).map initialState
instance seedLaw_probability (ρ : Measure R) [IsProbabilityMeasure ρ] (base : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1) :
    IsProbabilityMeasure (seedLaw ρ base hb hbn) := by
  unfold seedLaw
  exact isProbabilityMeasure_map initialState_measurable.aemeasurable

def historyReadout (tr : FiniteAlphabetQuery.Trace (EvalState R A Y)) (n : ℕ) : History A Y :=
  (tr n).1.2.2
omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma historyReadout_measurable : Measurable (historyReadout (R := R) (A := A) (Y := Y)) :=
  measurable_pi_lambda _ (fun n => (measurable_pi_apply n).fst.snd.snd)

/-- The observable projection of the generic finite-query trace is exactly the
constructed observed-history law, including the common seed product measure. -/
theorem traceLaw_historyReadout
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    (FiniteAlphabetQuery.traceLaw (query U π) (step U π) (seedLaw ρ base hb hbn)
      (FiniteAlphabetQuery.iidOracle (rowMeasure P hP hN))).map historyReadout =
        observedTraceLaw U π ρ base P hb hbn hP hN := by
  let ν := FiniteAlphabetQuery.iidOracle (rowMeasure P hP hN)
  have hprod : (seedLaw ρ base hb hbn).prod ν =
      ((ρ.prod (stackMeasure base hb hbn)).prod ν).map (Prod.map initialState id) := by
    simpa only [seedLaw,Measure.map_id] using Measure.map_prod_map
      (ρ.prod (stackMeasure base hb hbn)) ν initialState_measurable measurable_id
  have htr := FiniteAlphabetQuery.measurable_trajectory (query U π) (step U π)
    (query_measurable U π hπ) (step_measurable U π hπ)
  unfold FiniteAlphabetQuery.traceLaw
  change (((seedLaw ρ base hb hbn).prod ν).map
    (fun z => FiniteAlphabetQuery.run (query U π) (step U π) z.2 z.1)).map historyReadout = _
  rw [hprod, Measure.map_map historyReadout_measurable htr,
    Measure.map_map (historyReadout_measurable.comp htr) (initialState_measurable.prodMap measurable_id)]
  unfold observedTraceLaw feedbackLaw
  rw [← Measure.prodAssoc_prod, Measure.map_map (historyTrajectory_measurable U π hπ)
    MeasurableEquiv.prodAssoc.measurable]
  congr 1
  funext z n
  change (policyRun U π z.2 z.1.1 (fun a k => z.1.2 (a,k)) n).1.2.2 =
    observedHistory U π z.2 z.1.1 (fun a k => z.1.2 (a,k)) n
  rw [policyRun_eq_observedHistory]

def traceAction (π : R → History A Y → A) (tr : FiniteAlphabetQuery.Trace (EvalState R A Y)) (n : ℕ) : A :=
  selected π (tr n).1

def historyAction (d : A) (H : ℕ → History A Y) (n : ℕ) : A :=
  ((H (n+1)).headD (d,default)).1

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma traceAction_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) : Measurable (traceAction π) :=
  measurable_pi_lambda _ (fun n => (selected_measurable π hπ).comp (measurable_pi_apply n).fst)
omit [DecidableEq A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma historyAction_measurable (d : A) : Measurable (historyAction (Y := Y) d) :=
  measurable_pi_lambda _ (fun n => (measurable_of_countable (fun h : History A Y => (h.headD (d,default)).1)).comp
    (measurable_pi_apply (n+1)))

omit [Fintype A] [Fintype Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- An action is selected before its observation and is recorded as the next
history head. This readout identity holds for every initial evaluator state. -/
theorem action_readout_on_run (U : Finset A) (π : R → History A Y → A)
    (oracle : ℕ → A → Y) (s : EvalState R A Y) (d : A) :
    traceAction π (FiniteAlphabetQuery.run (query U π) (step U π) oracle s) =
      historyAction d (historyReadout (FiniteAlphabetQuery.run (query U π) (step U π) oracle s)) := by
  funext n
  simp only [traceAction,historyAction,historyReadout,FiniteAlphabetQuery.run,FiniteAlphabetQuery.advance]
  split_ifs <;> rfl

lemma traceLaw_actionReadout (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure (EvalState R A Y)) (ν : Measure (FiniteAlphabetQuery.Oracle (A → Y))) (d : A) :
    (FiniteAlphabetQuery.traceLaw (query U π) (step U π) ρ ν).map (traceAction π) =
      ((FiniteAlphabetQuery.traceLaw (query U π) (step U π) ρ ν).map historyReadout).map (historyAction d) := by
  have htr := FiniteAlphabetQuery.measurable_trajectory (query U π) (step U π)
    (query_measurable U π hπ) (step_measurable U π hπ)
  unfold FiniteAlphabetQuery.traceLaw
  rw [Measure.map_map (traceAction_measurable π hπ) htr,
    Measure.map_map historyReadout_measurable htr,
    Measure.map_map (historyAction_measurable d) (historyReadout_measurable.comp htr)]
  congr 1
  funext z
  exact action_readout_on_run U π z.2 z.1 d

/-- Canonical law of the original shared causal policy with fresh P-feedback
at every action. Only the chosen coordinate of each fresh row is exposed. -/
def actionLaw (π : R → History A Y → A) (ρ : Measure R) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (d : A) : Measure (ℕ → A) :=
  (observedTraceLaw ∅ π ρ P P hP hN hP hN).map (historyAction d)

/-- Complete policy-row law embedding into the finite-query primitive. -/
theorem traceLaw_action_eq_canonical
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (hagree : ∀ a ∈ U, base a = P a) (d : A) :
    (FiniteAlphabetQuery.traceLaw (query U π) (step U π) (seedLaw ρ base hb hbn)
      (FiniteAlphabetQuery.iidOracle (rowMeasure P hP hN))).map (traceAction π) =
        actionLaw π ρ P hP hN d := by
  rw [traceLaw_actionReadout U π hπ _ _ d,traceLaw_historyReadout U π hπ,
    observedTraceLaw_eq_all_query U π hπ ρ base P hb hbn hP hN hagree]
  rfl

end Orthemology.Tranche2.PolicyEmbedding
