import HiddenChangeTaggedLaw
import ConditionalKilledContinuation

noncomputable section
open MeasureTheory ProbabilityTheory Set Preorder
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} {R : Type*}

/-- Histories are newest-first. The head's governing round is the tail length. -/
def liftMode (κ : ChangeIndex) : PairHistory n k → TaggedHistory n k
  | [] => []
  | (e,y)::h => ((fixedMode κ h.length,e),y)::liftMode κ h

@[simp] theorem liftMode_length (κ : ChangeIndex) (h : PairHistory n k) :
    (liftMode κ h).length = h.length := by induction h <;> simp_all [liftMode]
@[simp] theorem eraseMode_liftMode (κ : ChangeIndex) (h : PairHistory n k) :
    eraseMode (liftMode κ h) = h := by
  induction h with
  | nil => rfl
  | cons z h ih => cases z; simp [liftMode, ih]

theorem liftMode_getElem (κ : ChangeIndex) (h : PairHistory n k)
    (j : ℕ) (hj : j < h.length) :
    (liftMode κ h)[j]'(by simpa using hj) =
      ((fixedMode κ (h.length - 1 - j), h[j].1), h[j].2) := by
  induction h generalizing j with
  | nil => simp at hj
  | cons z h ih =>
    cases j with
    | zero => simp [liftMode]
    | succ j =>
      have hj' : j < h.length := by simpa using hj
      simpa [liftMode, Nat.sub_sub, Nat.add_comm, Nat.add_left_comm] using ih j hj'

theorem fixed_compatible_lift (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (r : R) (h : PairHistory n k) :
    ActionCompatible (fixedPolicy κ s π) r (liftMode κ h) ↔
      ActionCompatible (pairPolicy s π) r h := by
  induction h with
  | nil => rfl
  | cons z h ih =>
    cases z
    simp [liftMode, ActionCompatible, fixedPolicy, ih]

def fixedPrefixLikelihood (I : Input n k) (κ : ChangeIndex)
    (h : PairHistory n k) : ℝ≥0∞ :=
  ∏ i : Fin h.length,
    ENNReal.ofReal (I.row (fixedMode κ (h.length - 1 - i.val)) h[i].1 h[i].2 : ℝ)

theorem fixedPrefixLikelihood_eq_lift (I : Input n k) (κ : ChangeIndex)
    (h : PairHistory n k) :
    fixedPrefixLikelihood I κ h = RowLikelihood (taggedRows I) (liftMode κ h) := by
  unfold RowLikelihood fixedPrefixLikelihood
  apply Fintype.prod_equiv (finCongr (liftMode_length κ h).symm)
  intro j
  simp only [finCongr_apply, Fin.getElem_fin, Fin.coe_cast, taggedRows]
  rw [liftMode_getElem κ h j.val j.isLt]


variable [NeZero n]
theorem fixed_history_lift (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : Orthemology.Tranche2.PolicyEmbedding.Input R (TaggedPair n k) (State n)) (t : ℕ) :
    historyTrajectory ∅ (fixedPolicy κ s π) z t =
      liftMode κ (eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z t)) := by
  induction t with
  | zero => rfl
  | succ t ih =>
    simp only [historyTrajectory, observedHistory] at ih ⊢
    simp only [eraseMode_cons, liftMode, fixedPolicy, eraseMode_length]
    exact congrArg (fun tail =>
      ((fixedMode κ (observedHistory ∅ (fixedPolicy κ s π) z.2.2 z.1
        (fun a n => z.2.1 (a,n)) t).length,
        pairPolicy s π z.1 (eraseMode (observedHistory ∅ (fixedPolicy κ s π) z.2.2 z.1
          (fun a n => z.2.1 (a,n)) t))),
       feedback ∅ (fun a n => z.2.1 (a,n)) z.2.2
         (fixedPolicy κ s π z.1 (observedHistory ∅ (fixedPolicy κ s π) z.2.2 z.1
           (fun a n => z.2.1 (a,n)) t))
         (observedHistory ∅ (fixedPolicy κ s π) z.2.2 z.1 (fun a n => z.2.1 (a,n)) t)) :: tail) ih

theorem fixed_history_eq_lift_iff (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : Orthemology.Tranche2.PolicyEmbedding.Input R (TaggedPair n k) (State n))
    (t : ℕ) (h : PairHistory n k) :
    eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z t) = h ↔
      historyTrajectory ∅ (fixedPolicy κ s π) z t = liftMode κ h := by
  constructor
  · intro hh
    rw [fixed_history_lift κ s π z t, hh]
  · intro hh
    rw [hh, eraseMode_liftMode]

theorem eraseModeTrace_measurable : Measurable (eraseModeTrace (n := n) (k := k)) :=
  measurable_pi_lambda _ (fun t => (measurable_of_countable eraseMode).comp (measurable_pi_apply t))

/-- Exact joint seed and physical-prefix weight for the original constructed law. -/
theorem fixed_seed_prefix_probability [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (D : Set R) (h : PairHistory n k) :
    CanonicalInput ρ (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
      {z | z.1 ∈ D ∧ eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z h.length) = h} =
      ρ (D ∩ CompatibleSeeds (pairPolicy s π) h) * fixedPrefixLikelihood I κ h := by
  have he : {z : Orthemology.Tranche2.PolicyEmbedding.Input R (TaggedPair n k) (State n) |
      z.1 ∈ D ∧ eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z h.length) = h} =
      {z | z.1 ∈ D ∧ historyTrajectory ∅ (fixedPolicy κ s π) z (liftMode κ h).length = liftMode κ h} := by
    ext z
    simp only [Set.mem_setOf_eq, liftMode_length, fixed_history_eq_lift_iff]
  rw [he]
  have hp := private_transcript_cylinder_probability ∅ (fixedPolicy κ s π) ρ
    (taggedRows I) (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI) (fun _ _ => rfl) D (liftMode κ h)
  change _ = _ at hp
  rw [fixedPrefixLikelihood_eq_lift]
  simpa only [CanonicalInput, fixed_compatible_lift, CompatibleSeeds, RowLikelihood] using hp

theorem fixed_prefix_probability [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (h : PairHistory n k) :
    fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h} =
      ρ (CompatibleSeeds (pairPolicy s π) h) * fixedPrefixLikelihood I κ h := by
  have hC : MeasurableSet {H : PairTrace n k | H h.length = h} :=
    (measurableSet_singleton h).preimage (measurable_pi_apply h.length)
  unfold fixedPhysicalLaw fixedLaw observedTraceLaw
  rw [Measure.map_map eraseModeTrace_measurable (historyTrajectory_measurable ∅ _
    (fixedPolicy_measurable κ s π hπ)), Measure.map_apply
      (eraseModeTrace_measurable.comp (historyTrajectory_measurable ∅ _
        (fixedPolicy_measurable κ s π hπ))) hC]
  have hp := fixed_seed_prefix_probability I hI κ s ρ π Set.univ h
  simpa only [CanonicalInput, Set.mem_univ, true_and, Set.univ_inter] using hp

theorem fixedPhysicalLaw_probability [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    IsProbabilityMeasure (fixedPhysicalLaw I hI κ s ρ π) := by
  unfold fixedPhysicalLaw fixedLaw observedTraceLaw
  haveI : IsProbabilityMeasure
      ((ρ.prod (feedbackLaw (taggedRows I) (taggedRows I) (taggedRows_nonnegative I hI)
        (taggedRows_normalized I hI) (taggedRows_nonnegative I hI)
        (taggedRows_normalized I hI))).map (historyTrajectory ∅ (fixedPolicy κ s π))) :=
    isProbabilityMeasure_map (historyTrajectory_measurable ∅ _
      (fixedPolicy_measurable κ s π hπ)).aemeasurable
  exact isProbabilityMeasure_map eraseModeTrace_measurable.aemeasurable

theorem fixedPhysicalLaw_marginal [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (t : ℕ) (h : PairHistory n k) :
    ((fixedPhysicalLaw I hI κ s ρ π).map (fun H => H t)) {h} =
      if t = h.length then ρ (CompatibleSeeds (pairPolicy s π) h) *
        fixedPrefixLikelihood I κ h else 0 := by
  by_cases ht : t = h.length
  · subst t
    rw [if_pos rfl, Measure.map_apply (measurable_pi_apply h.length) (measurableSet_singleton h)]
    exact fixed_prefix_probability I hI κ s ρ π hπ h
  · rw [if_neg ht]
    unfold fixedPhysicalLaw fixedLaw observedTraceLaw
    rw [Measure.map_map eraseModeTrace_measurable (historyTrajectory_measurable ∅ _
      (fixedPolicy_measurable κ s π hπ)), Measure.map_map (measurable_pi_apply t)
      (eraseModeTrace_measurable.comp (historyTrajectory_measurable ∅ _
        (fixedPolicy_measurable κ s π hπ))), Measure.map_apply
      ((measurable_pi_apply t).comp (eraseModeTrace_measurable.comp
        (historyTrajectory_measurable ∅ _ (fixedPolicy_measurable κ s π hπ))))
      (measurableSet_singleton h)]
    have he : {z : Orthemology.Tranche2.PolicyEmbedding.Input R (TaggedPair n k) (State n) |
        eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z t) = h} = ∅ := by
      apply Set.eq_empty_iff_forall_not_mem.mpr
      intro z hz
      apply ht
      have hh := congrArg List.length hz
      simpa only [eraseMode_length, historyTrajectory, observedHistory_length] using hh
    change (ρ.prod (feedbackLaw (taggedRows I) (taggedRows I)
      (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
      (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)))
      {z | eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z t) = h} = 0
    rw [he, measure_empty]

theorem fixed_physical_prefix_map [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (N : ℕ) :
    (fixedPhysicalLaw I hI κ s ρ π).map (frestrictLe N) =
      ((fixedPhysicalLaw I hI κ s ρ π).map (fun H => H N)).map
        (reconstructPrefix (A := Pair n k) (Y := State n) N) := by
  unfold fixedPhysicalLaw fixedLaw observedTraceLaw
  rw [Measure.map_map eraseModeTrace_measurable (historyTrajectory_measurable ∅ _
    (fixedPolicy_measurable κ s π hπ)), Measure.map_map (measurable_frestrictLe N)
      (eraseModeTrace_measurable.comp (historyTrajectory_measurable ∅ _
        (fixedPolicy_measurable κ s π hπ))), Measure.map_map (measurable_pi_apply N)
      (eraseModeTrace_measurable.comp (historyTrajectory_measurable ∅ _
        (fixedPolicy_measurable κ s π hπ))), Measure.map_map
      (measurable_of_countable (reconstructPrefix (A := Pair n k) (Y := State n) N))
      ((measurable_pi_apply N).comp (eraseModeTrace_measurable.comp
        (historyTrajectory_measurable ∅ _ (fixedPolicy_measurable κ s π hπ))))]
  congr 1
  funext z i
  have he := observedHistory_drop ∅ (fixedPolicy κ s π) z.2.2 z.1
    (fun a n => z.2.1 (a,n)) N i.val (Finset.mem_Iic.mp i.property)
  change eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z i.val) =
    (eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z N)).drop (N-i.val)
  simpa only [eraseMode, historyTrajectory, List.map_drop] using (congrArg eraseMode he).symm

theorem fixed_constant_eq_markov [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (σ : Mode)
    (hmode : ∀ t, fixedMode κ t = σ) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    fixedPhysicalLaw I hI κ s ρ π = markovHistoryLaw (I.kernel hI) σ s π ρ := by
  haveI : IsFiniteMeasure (markovHistoryLaw (I.kernel hI) σ s π ρ) := by
    unfold markovHistoryLaw observedTraceLaw
    infer_instance
  apply measure_eq_of_prefix_maps
  intro N
  rw [fixed_physical_prefix_map I hI κ s ρ π hπ N,
    markovHistoryLaw, observed_prefix_map_from_last ∅ (pairPolicy s π)
      (pairPolicy_measurable s π hπ) ρ]
  congr 1
  apply Measure.ext_of_singleton
  intro h
  rw [fixedPhysicalLaw_marginal I hI κ s ρ π hπ N h,
    history_marginal_formula ∅ (pairPolicy s π) (pairPolicy_measurable s π hπ)
      ρ _ _ _ _ _ _ (fun _ _ => rfl)]
  simp only [CompatibleSeeds, fixedPrefixLikelihood, hmode, realRows, OrthemicCertificate.Input.kernel_row]

theorem fixed_none_eq_markov [MeasurableSpace R] (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    fixedPhysicalLaw I hI none s ρ π = markovHistoryLaw (I.kernel hI) 0 s π ρ :=
  fixed_constant_eq_markov I hI none 0 (fun _ => rfl) s ρ π hπ

theorem fixed_zero_eq_markov [MeasurableSpace R] (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    fixedPhysicalLaw I hI (some 0) s ρ π = markovHistoryLaw (I.kernel hI) 1 s π ρ :=
  fixed_constant_eq_markov I hI (some 0) 1 (fun t => by simp [fixedMode]) s ρ π hπ

/-- Residual time starts at zero; a switch already made becomes index zero. -/
def shiftIndex (κ : ChangeIndex) (N : ℕ) : ChangeIndex := κ.map (fun j => j-N)

theorem fixedMode_shiftIndex (κ : ChangeIndex) (N t : ℕ) :
    fixedMode (shiftIndex κ N) t = fixedMode κ (N+t) := by
  cases κ with
  | none => rfl
  | some j =>
    change (if t < j-N then (0 : Mode) else 1) = (if N+t < j then 0 else 1)
    have he : t < j-N ↔ N+t < j := by omega
    simp only [he]

theorem fixed_restartPolicy_shift (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (h : PairHistory n k) :
    restartPolicy (fixedPolicy κ s π) (liftMode κ h) =
      fixedPolicy (shiftIndex κ h.length) (currentState s h)
        (restartPolicy π (erasePairSources h)) := by
  funext r tail
  apply Prod.ext
  · simp only [restartPolicy, fixedPolicy, List.length_append, liftMode_length,
      fixedMode_shiftIndex, Nat.add_comm]
  · simp only [restartPolicy, fixedPolicy, eraseMode, List.map_append]
    change pairPolicy s π r (eraseMode tail ++ eraseMode (liftMode κ h)) = _
    rw [eraseMode_liftMode]
    exact (restart_pairPolicy_agrees s π h (eraseMode tail) r).symm

def constantIndex (σ : Mode) : ChangeIndex := if σ = 0 then none else some 0
@[simp] theorem fixedMode_constantIndex (σ : Mode) (t : ℕ) :
    fixedMode (constantIndex σ) t = σ := by
  fin_cases σ <;> simp [constantIndex, fixedMode]

def fixedConditionalLaw [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) (π : Policy R n k) (h : PairHistory n k) : Measure (PairTrace n k) :=
  (normalizedRestriction (fixedPhysicalLaw I hI κ s ρ π)
    {H | H h.length = h}).map (continuationReadout h)

theorem fixedConditionalLaw_eq_zero [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) (π : Policy R n k) (h : PairHistory n k)
    (hp : fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h} = 0) :
    fixedConditionalLaw I hI κ s ρ π h = 0 := by
  rw [fixedConditionalLaw, normalizedRestriction, Measure.restrict_eq_zero.mpr hp, smul_zero, Measure.map_zero]

/-- Physical conditioning is performed on the original law. Internal tags are
reconstructed only in this proof of its relation to the generic conditioning API. -/
theorem fixedConditionalLaw_eq_tagged [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) :
    fixedConditionalLaw I hI κ s ρ π h =
      (conditionalContinuationLaw (fixedPolicy κ s π) ρ (taggedRows I)
        (taggedRows_nonnegative I hI) (taggedRows_normalized I hI) (liftMode κ h)).map eraseModeTrace := by
  let μ := CanonicalInput ρ (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
  let f := eraseModeTrace ∘ historyTrajectory ∅ (fixedPolicy κ s π)
  have hf : Measurable f := eraseModeTrace_measurable.comp
    (historyTrajectory_measurable ∅ _ (fixedPolicy_measurable κ s π hπ))
  have hC : MeasurableSet {H : PairTrace n k | H h.length = h} :=
    (measurableSet_singleton h).preimage (measurable_pi_apply h.length)
  have hlaw : fixedPhysicalLaw I hI κ s ρ π = μ.map f := by
    unfold fixedPhysicalLaw fixedLaw observedTraceLaw
    rw [Measure.map_map eraseModeTrace_measurable (historyTrajectory_measurable ∅ _
      (fixedPolicy_measurable κ s π hπ))]
    rfl
  have hevent : f ⁻¹' {H | H h.length = h} = PrefixEvent (fixedPolicy κ s π) (liftMode κ h) := by
    ext z
    exact (fixed_history_eq_lift_iff κ s π z h.length h).trans (by simp [PrefixEvent])
  rw [fixedConditionalLaw, hlaw,
    ← normalizedRestriction_map_preimage μ f hf _ hC,
    Measure.map_map (continuationReadout_measurable h) hf, hevent,
    conditionalContinuationLaw, Measure.map_map eraseModeTrace_measurable
      (continuationHistory_measurable _ (fixedPolicy_measurable κ s π hπ) (liftMode κ h))]
  congr 1
  funext z t
  simp only [Function.comp_apply, f, continuationReadout, eraseModeTrace, eraseMode,
    continuationHistory, liftMode_length, List.map_take]

theorem fixed_commonSeedPosterior_lift [MeasurableSpace R]
    (κ : ChangeIndex) (s : State n) (π : Policy R n k) (ρ : Measure R) (h : PairHistory n k) :
    commonSeedPosterior (fixedPolicy κ s π) ρ (liftMode κ h) =
      commonSeedPosterior (pairPolicy s π) ρ h := by
  unfold commonSeedPosterior
  congr 1
  ext r
  exact fixed_compatible_lift κ s π r h

theorem fixed_restartPolicy (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (h : PairHistory n k) (σ : Mode)
    (hconstant : ∀ t, h.length ≤ t → fixedMode κ t = σ) :
    restartPolicy (fixedPolicy κ s π) (liftMode κ h) =
      fixedPolicy (constantIndex σ) (currentState s h) (restartPolicy π (erasePairSources h)) := by
  funext r tail
  apply Prod.ext
  · simp only [restartPolicy, fixedPolicy, List.length_append, liftMode_length,
      fixedMode_constantIndex]
    exact hconstant _ (Nat.le_add_left _ _)
  · simp only [restartPolicy, fixedPolicy, eraseMode, List.map_append]
    change pairPolicy s π r (eraseMode tail ++ eraseMode (liftMode κ h)) = _
    rw [eraseMode_liftMode]
    exact (restart_pairPolicy_agrees s π h (eraseMode tail) r).symm

/-- Conditional continuation under any deterministic schedule keeps the original
policy history and private seed, with the literal residual switch index. -/
theorem fixedConditionalLaw_eq_shifted_restart [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k)
    (hp : 0 < fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h}) :
    fixedConditionalLaw I hI κ s ρ π h =
      fixedPhysicalLaw I hI (shiftIndex κ h.length) (currentState s h)
        (commonSeedPosterior (pairPolicy s π) ρ h) (restartPolicy π (erasePairSources h)) := by
  have he : CanonicalInput ρ (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
      (PrefixEvent (fixedPolicy κ s π) (liftMode κ h)) =
      fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h} := by
    rw [fixed_prefix_probability I hI κ s ρ π hπ]
    have hx := fixed_seed_prefix_probability I hI κ s ρ π Set.univ h
    have hevent : PrefixEvent (fixedPolicy κ s π) (liftMode κ h) =
        {z | eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z h.length) = h} := by
      ext z
      simpa only [PrefixEvent, Set.mem_setOf_eq, liftMode_length] using
        (fixed_history_eq_lift_iff κ s π z h.length h).symm
    rw [hevent]
    simpa only [Set.mem_univ, true_and, Set.univ_inter] using hx
  have hp' : 0 < CanonicalInput ρ (taggedRows I) (taggedRows_nonnegative I hI)
      (taggedRows_normalized I hI) (PrefixEvent (fixedPolicy κ s π) (liftMode κ h)) := by rw [he]; exact hp
  rw [fixedConditionalLaw_eq_tagged I hI κ s ρ π hπ h,
    conditionalContinuationLaw_eq_restart _ (fixedPolicy_measurable κ s π hπ) ρ _ _ _ _ hp',
    fixed_restartPolicy_shift, fixed_commonSeedPosterior_lift]
  rfl

/-- Genuine schedule-conditioned stationary restart, allowing an old prefix
that has zero probability under stationary mode1. -/
theorem fixedConditionalLaw_eq_restart [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (σ : Mode)
    (hp : 0 < fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h})
    (hconstant : ∀ t, h.length ≤ t → fixedMode κ t = σ) :
    fixedConditionalLaw I hI κ s ρ π h =
      markovHistoryLaw (I.kernel hI) σ (currentState s h)
        (restartPolicy π (erasePairSources h)) (commonSeedPosterior (pairPolicy s π) ρ h) := by
  have he : CanonicalInput ρ (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
      (PrefixEvent (fixedPolicy κ s π) (liftMode κ h)) =
      fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h} := by
    rw [fixed_prefix_probability I hI κ s ρ π hπ]
    have hx := fixed_seed_prefix_probability I hI κ s ρ π Set.univ h
    have hevent : PrefixEvent (fixedPolicy κ s π) (liftMode κ h) =
        {z | eraseMode (historyTrajectory ∅ (fixedPolicy κ s π) z h.length) = h} := by
      ext z
      simpa only [PrefixEvent, Set.mem_setOf_eq, liftMode_length] using
        (fixed_history_eq_lift_iff κ s π z h.length h).symm
    rw [hevent]
    simpa only [Set.mem_univ, true_and, Set.univ_inter] using hx
  have hp' : 0 < CanonicalInput ρ (taggedRows I) (taggedRows_nonnegative I hI)
      (taggedRows_normalized I hI) (PrefixEvent (fixedPolicy κ s π) (liftMode κ h)) := by rw [he]; exact hp
  haveI : IsProbabilityMeasure (commonSeedPosterior (pairPolicy s π) ρ h) := by
    rw [← fixed_commonSeedPosterior_lift κ s π ρ h]
    exact commonSeedPosterior_probability _ ρ _
      (positive_prefix_compatible_seeds _ ρ _ _ _ _ hp')
  rw [fixedConditionalLaw_eq_tagged I hI κ s ρ π hπ h,
    conditionalContinuationLaw_eq_restart _ (fixedPolicy_measurable κ s π hπ) ρ _ _ _ _ hp',
    fixed_restartPolicy κ s π h σ hconstant, fixed_commonSeedPosterior_lift]
  change fixedPhysicalLaw I hI (constantIndex σ) (currentState s h)
    (commonSeedPosterior (pairPolicy s π) ρ h) (restartPolicy π (erasePairSources h)) = _
  exact fixed_constant_eq_markov I hI (constantIndex σ) σ (fixedMode_constantIndex σ)
    (currentState s h) _ _ (restartPolicy_measurable π hπ (erasePairSources h))

end HiddenChange
