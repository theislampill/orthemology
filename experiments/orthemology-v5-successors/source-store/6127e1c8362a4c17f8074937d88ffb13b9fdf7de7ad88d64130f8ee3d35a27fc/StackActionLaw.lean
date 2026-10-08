import PolicyTraceBinding

/-!
# The all-stack evaluator has the canonical controlled-iid action law

All probability laws below are constructed from the specified private-seed law
and `stackMeasure P`. No law-equivalence or independence premise is assumed.
-/

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {R : Type v} {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- The pure stack history evaluator, with an arbitrary private seed. -/
def stackHistoryTrajectory (π : R → History A Y → A) (z : R × FlatStack A Y) :
    ℕ → History A Y :=
  observedHistory Finset.univ π (fun _ _ => default) z.1 (fun a n => z.2 (a,n))

/-- The actions chosen from the acquired histories of the pure stack evaluator. -/
def stackActionTrajectory (π : R → History A Y → A) (z : R × FlatStack A Y) : ℕ → A :=
  fun n => π z.1 (stackHistoryTrajectory π z n)

omit [Fintype Y] [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A]
    [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- Every row-oracle argument is unused when all actions consult their stacks. -/
lemma observedHistory_univ_oracle_irrelevant (π : R → History A Y → A)
    (oracle other : RowOracle A Y) (r : R) (X : Stack A Y) :
    observedHistory Finset.univ π oracle r X = observedHistory Finset.univ π other r X := by
  funext n
  induction n with
  | zero => rfl
  | succ n ih => simp only [observedHistory,ih,feedback,Finset.mem_univ,not_true_eq_false,ite_false]

lemma stackHistoryTrajectory_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) :
    Measurable (stackHistoryTrajectory π) := by
  exact (historyTrajectory_measurable Finset.univ π hπ).comp
    (measurable_fst.prodMk (measurable_snd.prodMk measurable_const))

lemma stackActionTrajectory_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) :
    Measurable (stackActionTrajectory π) := by
  apply measurable_pi_lambda
  intro n
  exact hπ.comp (measurable_fst.prodMk
    ((measurable_pi_apply n).comp (stackHistoryTrajectory_measurable π hπ)))

omit [Fintype Y] [MeasurableSpace R] [MeasurableSpace A]
    [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- The existing history readout recovers exactly the causal stack actions. -/
lemma stackActionTrajectory_eq_historyAction (π : R → History A Y → A)
    (z : R × FlatStack A Y) (d : A) :
    stackActionTrajectory π z = historyAction d (stackHistoryTrajectory π z) := by
  have h := action_readout_on_run Finset.univ π (fun _ _ => default)
    (initialState z) d
  have hrun : FiniteAlphabetQuery.run (query Finset.univ π) (step Finset.univ π)
      (fun _ _ => default) (initialState z) =
      policyRun Finset.univ π (fun _ _ => default) z.1 (fun a n => z.2 (a,n)) := rfl
  rw [hrun] at h
  have ht : traceAction π (policyRun Finset.univ π (fun _ _ => default) z.1
      (fun a n => z.2 (a,n))) = stackActionTrajectory π z := by
    funext n
    simp [traceAction,policyRun_eq_observedHistory,selected,stackActionTrajectory,stackHistoryTrajectory]
  have hh : historyReadout (policyRun Finset.univ π (fun _ _ => default) z.1
      (fun a n => z.2 (a,n))) = stackHistoryTrajectory π z := by
    funext n
    simp [historyReadout,policyRun_eq_observedHistory,stackHistoryTrajectory]
  simpa only [ht,hh] using h

/-- Removing the entirely unused oracle factor leaves the actual stack law. -/
theorem observedTraceLaw_univ_eq_stack
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    observedTraceLaw Finset.univ π ρ P P hP hN hP hN =
      (ρ.prod (stackMeasure P hP hN)).map (stackHistoryTrajectory π) := by
  unfold observedTraceLaw feedbackLaw
  rw [← Measure.prodAssoc_prod, Measure.map_map (historyTrajectory_measurable Finset.univ π hπ)
    MeasurableEquiv.prodAssoc.measurable]
  have he : historyTrajectory Finset.univ π ∘ (MeasurableEquiv.prodAssoc : ((R × FlatStack A Y) × RowOracle A Y) ≃ᵐ Input R A Y) =
      stackHistoryTrajectory π ∘ Prod.fst := by
    funext z
    exact observedHistory_univ_oracle_irrelevant π z.2 (fun _ _ => default) z.1.1
      (fun a n => z.1.2 (a,n))
  rw [he, ← Measure.map_map (stackHistoryTrajectory_measurable π hπ) measurable_fst,
    Measure.map_fst_prod,measure_univ,one_smul]

/-- Exact equality with the existing canonical fresh-feedback action law. -/
theorem stackActionTrajectory_law
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (d : A) :
    (ρ.prod (stackMeasure P hP hN)).map (stackActionTrajectory π) =
      actionLaw π ρ P hP hN d := by
  unfold actionLaw
  rw [← observedTraceLaw_eq_all_query Finset.univ π hπ ρ P P hP hN hP hN (fun _ _ => rfl),
    observedTraceLaw_univ_eq_stack π hπ ρ P hP hN,
    Measure.map_map (historyAction_measurable d) (stackHistoryTrajectory_measurable π hπ)]
  exact congrArg (fun f => (ρ.prod (stackMeasure P hP hN)).map f)
    (funext (fun z => stackActionTrajectory_eq_historyAction π z d))

/-- A measurable almost-sure action-path property of the stack evaluator holds
under the very same canonical action law used by the necessity direction. -/
theorem actionLaw_ae_of_stack
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (d : A)
    (Q : (ℕ → A) → Prop) (hQ : MeasurableSet {a | Q a})
    (hstack : ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN), Q (stackActionTrajectory π z)) :
    ∀ᵐ a ∂actionLaw π ρ P hP hN d, Q a := by
  rw [← stackActionTrajectory_law π hπ ρ P hP hN d]
  exact (ae_map_iff (stackActionTrajectory_measurable π hπ).aemeasurable hQ).mpr hstack

omit [Fintype A] [DecidableEq A] in
/-- Eventual membership in a finite good-action set is a measurable path event. -/
lemma measurableSet_eventually_mem (G : Finset A) :
    MeasurableSet {a : ℕ → A | ∀ᶠ n in atTop, a n ∈ G} := by
  have he : {a : ℕ → A | ∀ᶠ n in atTop, a n ∈ G} =
      ⋃ N : ℕ, ⋂ n : ℕ, {a : ℕ → A | N ≤ n → a n ∈ G} := by
    ext a
    simp only [Set.mem_setOf_eq,Set.mem_iUnion,Set.mem_iInter,eventually_atTop]
  rw [he]
  apply MeasurableSet.iUnion
  intro N
  apply MeasurableSet.iInter
  intro n
  by_cases hn : N ≤ n
  · simpa only [hn,true_implies] using G.measurableSet.preimage (measurable_pi_apply n)
  · simp only [hn,false_implies,Set.setOf_true]
    exact MeasurableSet.univ

/-- Direct sufficient-law bridge for eventual goodness, with no additional
measurable-event obligation at the call site. -/
theorem actionLaw_eventually_good_of_stack
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (d : A) (G : Finset A)
    (hstack : ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN),
      ∀ᶠ n in atTop, stackActionTrajectory π z n ∈ G) :
    ∀ᵐ a ∂actionLaw π ρ P hP hN d, ∀ᶠ n in atTop, a n ∈ G :=
  actionLaw_ae_of_stack π hπ ρ P hP hN d _ (measurableSet_eventually_mem G) hstack

/-- A stack theorem proved separately for every private seed also suffices. -/
theorem actionLaw_eventually_good_of_stack_fibers
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (d : A) (G : Finset A)
    (hstack : ∀ r : R, ∀ᵐ X ∂stackMeasure P hP hN,
      ∀ᶠ n in atTop, π r (observedHistory Finset.univ π (fun _ _ => default)
        r (fun a k => X (a,k)) n) ∈ G) :
    ∀ᵐ a ∂actionLaw π ρ P hP hN d, ∀ᶠ n in atTop, a n ∈ G := by
  apply actionLaw_eventually_good_of_stack π hπ ρ P hP hN d G
  apply (Measure.ae_prod_iff_ae_ae
    ((measurableSet_eventually_mem G).preimage (stackActionTrajectory_measurable π hπ))).mpr
  exact Filter.Eventually.of_forall hstack

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
/-- Exact per-coordinate marginal of the specified stack experiment. -/
lemma stack_coordinate_law (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (n : ℕ) :
    (stackMeasure P hP hN).map (fun X => X (a,n)) = actionMeasure P hP hN a :=
  infinite_product_coordinate_law _ (a,n)

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma stack_coordinates_independent (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) :
    iIndepFun (fun an : A × ℕ => fun X : FlatStack A Y => X an) (stackMeasure P hP hN) :=
  infinite_product_coordinates_independent _

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma stack_coordinates_identDistrib (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (n m : ℕ) :
    IdentDistrib (fun X : FlatStack A Y => X (a,n)) (fun X : FlatStack A Y => X (a,m))
      (stackMeasure P hP hN) (stackMeasure P hP hN) := by
  refine ⟨(measurable_pi_apply _).aemeasurable,(measurable_pi_apply _).aemeasurable,?_⟩
  rw [stack_coordinate_law,stack_coordinate_law]

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
lemma stack_coordinate_real_singleton (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (n : ℕ) (y : Y) :
    ((stackMeasure P hP hN).map (fun X => X (a,n))).real {y} = P a y := by
  rw [stack_coordinate_law, measureReal_def,actionMeasure_singleton,ENNReal.toReal_ofReal (hP a y)]

/-- Coordinates on the joint private-seed/stack space used by the controller. -/
def seededStackCoordinate (a : A) (n : ℕ) (z : R × FlatStack A Y) : Y := z.2 (a,n)

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace A]
    [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma seededStackCoordinate_measurable (a : A) (n : ℕ) :
    Measurable (seededStackCoordinate (R := R) (Y := Y) a n) :=
  (measurable_pi_apply (a,n)).comp measurable_snd

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma seededStackCoordinate_law
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (n : ℕ) :
    (ρ.prod (stackMeasure P hP hN)).map (seededStackCoordinate a n) = actionMeasure P hP hN a := by
  change (ρ.prod (stackMeasure P hP hN)).map ((fun X => X (a,n)) ∘ Prod.snd) = _
  rw [← Measure.map_map (measurable_pi_apply _) measurable_snd,Measure.map_snd_prod,
    measure_univ,one_smul,stack_coordinate_law]

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma seededStackCoordinates_independent
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) :
    iIndepFun (fun an : A × ℕ => seededStackCoordinate (R := R) (Y := Y) an.1 an.2)
      (ρ.prod (stackMeasure P hP hN)) := by
  rw [iIndepFun_iff_measure_inter_preimage_eq_mul]
  intro S sets hs
  have he : (⋂ an ∈ S, seededStackCoordinate (R := R) (Y := Y) an.1 an.2 ⁻¹' sets an) =
      Set.univ ×ˢ (⋂ an ∈ S, (fun X : FlatStack A Y => X an) ⁻¹' sets an) := by
    ext z
    simp [seededStackCoordinate]
  rw [he,Measure.prod_prod,measure_univ,one_mul,
    (stack_coordinates_independent P hP hN).measure_inter_preimage_eq_mul S hs]
  apply Finset.prod_congr rfl
  intro an han
  have hc : seededStackCoordinate (R := R) (Y := Y) an.1 an.2 ⁻¹' sets an =
      Set.univ ×ˢ ((fun X : FlatStack A Y => X an) ⁻¹' sets an) := by
    ext z
    simp [seededStackCoordinate]
  rw [hc,Measure.prod_prod,measure_univ,one_mul]

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma seededStackCoordinates_identDistrib
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (n m : ℕ) :
    IdentDistrib (seededStackCoordinate (R := R) (Y := Y) a n) (seededStackCoordinate a m)
      (ρ.prod (stackMeasure P hP hN)) (ρ.prod (stackMeasure P hP hN)) := by
  refine ⟨(seededStackCoordinate_measurable _ _).aemeasurable,
    (seededStackCoordinate_measurable _ _).aemeasurable,?_⟩
  rw [seededStackCoordinate_law,seededStackCoordinate_law]

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
lemma seededStackCoordinate_real_singleton
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (n : ℕ) (y : Y) :
    ((ρ.prod (stackMeasure P hP hN)).map (seededStackCoordinate a n)).real {y} = P a y := by
  rw [seededStackCoordinate_law,measureReal_def,actionMeasure_singleton,ENNReal.toReal_ofReal (hP a y)]

end Orthemology.Tranche2.PolicyEmbedding
