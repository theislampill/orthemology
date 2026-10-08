import HiddenChangeControllerActualLaw
import HiddenChangeControllerParity

set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory ProbabilityTheory Filter
open HiddenParity HiddenParity.Stochastic HiddenParity.Empirical HiddenParity.Sufficiency HiddenParity.Adaptive
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
namespace HiddenChange
variable {n k : ℕ} [NeZero n] [NeZero k]

theorem fixed_steps_action (I : Input n k) (hI : Admissible I) (κ : ChangeIndex)
    (c : PositiveBody n k) (s : State n) (H : TaggedTrace n k) (d : Pair n k)
    (hstep : ∀ t, FixedStep I κ s (compile I hI s c) t (H t) (H (t+1))) :
    historyAction d (eraseModeTrace H) = runPair I hI c s (publicTrace H) := by
  funext t
  unfold historyAction eraseModeTrace
  rw [(hstep t).1]
  simp only [List.headD_cons]
  simp only [runPair,publicTrace,observedState_erase,pairPolicy]

/-- The hidden governing tag is an actual-law fact, never a controller input. -/
theorem fixed_law_action_tags (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (π : Policy Unit n k)
    (hπ : Measurable (fun z : Unit × PublicHistory n k => π z.1 z.2)) (d : Pair n k) :
    ∀ᵐ H ∂fixedLaw I hI κ s (Measure.dirac ()) π,
      ∀ t, historyAction (0,d) H t = (fixedMode κ t, historyAction d (eraseModeTrace H) t) := by
  rw [fixedLaw_eq_stack I hI κ s (Measure.dirac ()) π hπ]
  have hm : MeasurableSet {H : TaggedTrace n k | ∀ t,
      historyAction (0,d) H t = (fixedMode κ t, historyAction d (eraseModeTrace H) t)} := by
    simp only [Set.setOf_forall]
    apply MeasurableSet.iInter
    intro t
    have hc : Measurable (fun H : TaggedTrace n k =>
        (historyAction (0,d) H t, historyAction d (eraseModeTrace H) t)) := by
      unfold historyAction eraseModeTrace
      exact (measurable_of_countable (fun h : TaggedHistory n k =>
        ((h.headD ((0,d),default)).1, ((eraseMode h).headD (d,default)).1))).comp
          (measurable_pi_apply (t+1))
    exact (Set.toFinite {z : TaggedPair n k × Pair n k | z.1 = (fixedMode κ t,z.2)}).measurableSet.preimage hc
  apply (ae_map_iff (stackHistoryTrajectory_measurable _
    (fixedPolicy_measurable κ s π hπ)).aemeasurable hm).mpr
  exact ae_of_all _ (fun z t => by
    rw [physical_stack_action κ s π z d t]
    unfold historyAction
    rw [stackHistoryTrajectory_succ_receipt]
    change stackActionTrajectory (fixedPolicy κ s π) z t = _
    exact Prod.ext (fixed_stack_tag κ s π z t) rfl)

/-- With an eventually fixed governing tag, its departure priority has exactly
same parity as the physical pair path labelled by that final mode. -/
theorem tagged_parity_of_eventual_tag (I : Input n k) (σ : Mode)
    (g : ℕ → TaggedPair n k) (x : ℕ → Pair n k)
    (heq : ∀ᶠ t in atTop, g t = (σ,x t))
    (hp : ParitySuccess (I.priority σ) x) :
    ParitySuccess (fun z : TaggedPair n k => I.priority z.1 z.2) g := by
  have hforward : ∀ e ∈ recurrentSet x, (σ,e) ∈ recurrentSet g := by
    intro e he
    apply (mem_recurrentSet g _).mpr
    exact (((mem_recurrentSet x e).mp he).and_eventually heq).mono (fun t ht => by
      rw [ht.2,ht.1])
  have hback : ∀ z ∈ recurrentSet g, z.1 = σ ∧ z.2 ∈ recurrentSet x := by
    intro z hz
    have hr := ((mem_recurrentSet g z).mp hz).and_eventually heq
    obtain ⟨t,ht,he⟩ := hr.exists
    have htag : z.1 = σ := congrArg Prod.fst (ht.symm.trans he)
    refine ⟨htag,(mem_recurrentSet x z.2).mpr ?_⟩
    exact hr.mono (fun t ht => (congrArg Prod.snd (ht.1.symm.trans ht.2)).symm)
  rcases hp with ⟨p,⟨⟨e,he,hpe⟩,hmin⟩,heven⟩
  refine ⟨p,⟨⟨(σ,e),hforward e he,hpe⟩,?_⟩,heven⟩
  intro z hz
  have hb := hback z hz
  simpa only [hb.1] using hmin z.2 hb.2

/-- Actual fixed-index parity of the new literal deterministic controller.
There are no supplied fairness, stabilizes, recurrence, convergence, or success
premises: every probabilistic regularity event is obtained from fixedLaw. -/
theorem compiled_fixed_parity (I : Input n k) (hI : Admissible I)
    (s : State n) (c : PositiveBody n k) (hc : positiveCheck I s c = true)
    (κ : ChangeIndex) (d : Pair n k) :
    ∀ᵐ H ∂fixedLaw I hI.1 κ s (Measure.dirac ()) (compile I hI s c), TaggedParity I d H := by
  have hb := ((positiveCheck_iff I s c).mp hc).2.1
  have hs := ((positiveCheck_iff I s c).mp hc).2.2
  let π := compile I hI s c
  have hπ := compiled_measurable I hI s c
  filter_upwards [fixed_law_steps I hI.1 κ s π hπ,
    fixed_law_action_tags I hI.1 κ s π hπ d,
    fixed_law_rational_true_gate I hI.1 κ s (Measure.dirac ()) π hπ,
    fixed_law_rational_wrong_row_eventually_rejected I hI.1 κ s (Measure.dirac ()) π hπ d,
    fixed_law_positive_successors_recur I hI.1 κ s (Measure.dirac ()) π hπ d]
      with H hsteps htags htrue hwrong hrec
  have hf := fixed_steps_follows I hI κ c s H hsteps.1 hsteps.2
  have hsupport := fixed_steps_supported I hI κ c s H hsteps.2
  have haug := fixed_steps_augment I hI κ c s H hsteps.1 hsteps.2
  have hx := fixed_steps_action I hI κ c s H d hsteps.2
  obtain ⟨N,hN⟩ := fixed_eventually_final κ
  have hp : ParitySuccess (I.priority (finalMode κ)) (runPair I hI c s (publicTrace H)) := by
    apply run_parity_of_regular I hI c hb s hs (publicTrace H) hf (fixedMode κ)
      (fixedMode_persistent κ) hsupport (finalMode κ) N hN
    · obtain ⟨K,hK⟩ := htrue
      refine ⟨K,fun r hr t => ?_⟩
      rw [haug t]
      exact hK r hr t
    · intro e he θ hrow r
      have hh : ∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e := by
        rw [hx]
        exact (mem_recurrentSet _ e).mp he
      simpa only [haug] using hwrong e hh θ hrow r
    · intro e he y hy
      have hh : ∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e := by
        rw [hx]
        exact (mem_recurrentSet _ e).mp he
      simpa only [hx] using hrec e hh y hy
  apply tagged_parity_of_eventual_tag I (finalMode κ)
    (historyAction (0,d) H) (runPair I hI c s (publicTrace H)) _ hp
  filter_upwards [eventually_ge_atTop N] with t ht
  simpa only [hN t ht,hx] using htags t

/-- The same literal policy wins against every legal measurable private-seed
one-change adversary, by the already constructed fixed-index reduction. -/
theorem compiled_winsAll (I : Input n k) (hI : Admissible I)
    (s : State n) (c : PositiveBody n k) (hc : positiveCheck I s c = true) (d : Pair n k) :
    WinsAll I hI.1 s (Measure.dirac ()) (compile I hI s c) d := by
  apply (winsAll_iff_fixed_indices I hI.1 s (Measure.dirac ()) (compile I hI s c)
    (compiled_measurable I hI s c) d).mpr
  exact fun κ => compiled_fixed_parity I hI s c hc κ d

#print axioms compiled_fixed_parity
#print axioms compiled_winsAll
end HiddenChange
