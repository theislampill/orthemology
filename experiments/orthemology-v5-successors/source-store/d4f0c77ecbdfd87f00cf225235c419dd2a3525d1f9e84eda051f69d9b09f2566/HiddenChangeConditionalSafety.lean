import HiddenChangePrefixSafety
import ConditionalAlmostSure

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.Adaptive
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

omit [NeZero n] in
/-- Conditioning is literal restriction and normalization of the original law.
This elementary bridge does not assume preservation of any success property. -/
theorem fixedConditional_ae_of_prefix_imp (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) (π : Policy R n k)
    (h : PairHistory n k) (Before After : PairTrace n k → Prop)
    (hAfter : MeasurableSet {H | After H})
    (hImp : ∀ H, H h.length = h → Before H → After (continuationReadout h H))
    (hAS : ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π, Before H) :
    ∀ᵐ H ∂fixedConditionalLaw I hI κ s ρ π h, After H := by
  unfold fixedConditionalLaw
  apply (ae_map_iff (continuationReadout_measurable h).aemeasurable hAfter).mpr
  have hC : MeasurableSet {H : PairTrace n k | H h.length = h} :=
    (measurableSet_singleton h).preimage (measurable_pi_apply h.length)
  have hBefore : ∀ᵐ H ∂normalizedRestriction (fixedPhysicalLaw I hI κ s ρ π)
      {H | H h.length = h}, Before H := Measure.ae_smul_measure (ae_restrict_of_ae hAS) _
  have hPrefix : ∀ᵐ H ∂normalizedRestriction (fixedPhysicalLaw I hI κ s ρ π)
      {H | H h.length = h}, H h.length = h := Measure.ae_smul_measure (ae_restrict_mem hC) _
  filter_upwards [hBefore,hPrefix] with H hB hH
  exact hImp H hH hB

theorem all_actions_mem_measurable (D : PairSet n k) (d : Pair n k) :
    MeasurableSet {H : PairTrace n k | ∀ t, historyAction d H t ∈ D} := by
  simp only [Set.setOf_forall]
  exact MeasurableSet.iInter (fun t => D.measurableSet.preimage
    ((measurable_pi_apply t).comp (historyAction_measurable d)))

theorem known_restart_safe (I : Input n k) (hI : I.Valid)
    (N : ℕ) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (d : Pair n k) (h : PairHistory n k)
    (hN : N ≤ h.length) (hp : PositivePrefix I hI (some N) s ρ π h) :
    ∀ᵐ H ∂markovHistoryLaw (I.kernel hI) 1 (currentState s h)
      (restartPolicy π (erasePairSources h)) (commonSeedPosterior (pairPolicy s π) ρ h),
      ∀ t, historyAction d H t ∈ knownAllowed I (policyKnownRegion I hI s ρ π) := by
  rw [← fixedConditionalLaw_eq_restart I hI (some N) s ρ π hπ h 1 hp
    (fun t ht => by simp only [fixedMode, if_neg (not_lt.mpr (hN.trans ht))])]
  apply fixedConditional_ae_of_prefix_imp I hI (some N) s ρ π h
    (fun H => ∀ t, N ≤ t → historyAction d H t ∈ knownAllowed I (policyKnownRegion I hI s ρ π))
    _ (all_actions_mem_measurable _ d) _ (fixedPhysicalLaw_known_safe I hI N s ρ π hπ hL d)
  intro H _ hB t
  rw [action_continuationReadout_shift]
  exact hB _ (by omega)

theorem noChange_restart_safe (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (d : Pair n k) (h : PairHistory n k)
    (hp : PositivePrefix I hI none s ρ π h) :
    ∀ᵐ H ∂markovHistoryLaw (I.kernel hI) 0 (currentState s h)
      (restartPolicy π (erasePairSources h)) (commonSeedPosterior (pairPolicy s π) ρ h),
      ∀ t, historyAction d H t ∈ uncertainAllowed I (policyKnownRegion I hI s ρ π)
        (policyUncertainRegion I hI s ρ π) := by
  have hAS : ∀ᵐ H ∂fixedPhysicalLaw I hI none s ρ π,
      ∀ t, historyAction d H t ∈ uncertainAllowed I (policyKnownRegion I hI s ρ π)
        (policyUncertainRegion I hI s ρ π) := by
    filter_upwards [fixedPhysicalLaw_uncertain_safe I hI none s ρ π hπ hL d,
      fixedPhysicalLaw_positive_prefixes I hI none s ρ π hπ] with H hs hpos
    intro t
    exact hs t (positive_noChange_compatible I hI s ρ π hπ _ (hpos t))
  rw [← fixedConditionalLaw_eq_restart I hI none s ρ π hπ h 0 hp (fun _ _ => rfl)]
  apply fixedConditional_ae_of_prefix_imp I hI none s ρ π h _ _
    (all_actions_mem_measurable _ d) _ hAS
  intro H _ hB t
  rw [action_continuationReadout_shift]
  exact hB _

omit [NeZero n] in
theorem coherentTrace_take_append {H : PairTrace n k} (hc : CoherentTrace H) (N t : ℕ) :
    H (N+t) = (H (N+t)).take t ++ H N := by
  induction t with
  | zero => simp
  | succ t ih =>
    obtain ⟨e,y,he⟩ := hc.2 (N+t)
    rw [Nat.add_succ,he]
    simp only [List.take_succ_cons,List.cons_append]
    exact congrArg (List.cons (e,y)) ih

omit [NeZero n] in
theorem zeroCompatible_iff_mem (I : Input n k) (h : PairHistory n k) :
    ZeroCompatible I h ↔ ∀ z ∈ h, 0 < I.row 0 z.1 z.2 := by
  simp only [ZeroCompatible, List.mem_iff_getElem]
  constructor
  · intro hi z hz
    obtain ⟨i,hi',rfl⟩ := hz
    exact hi ⟨i,hi'⟩
  · intro hm i
    exact hm _ ⟨i.val,i.isLt,rfl⟩

omit [NeZero n] in
theorem zeroCompatible_append (I : Input n k) (h q : PairHistory n k) :
    ZeroCompatible I (h++q) ↔ ZeroCompatible I h ∧ ZeroCompatible I q := by
  simp only [zeroCompatible_iff_mem,List.mem_append]
  constructor
  · intro h; exact ⟨fun z hz => h z (Or.inl hz),fun z hz => h z (Or.inr hz)⟩
  · rintro ⟨h,q⟩ z (hz|hz)
    · exact h z hz
    · exact q z hz

theorem unrevealed_actions_mem_measurable (I : Input n k) (D : PairSet n k) (d : Pair n k) :
    MeasurableSet {H : PairTrace n k | ∀ t, ZeroCompatible I (H t) → historyAction d H t ∈ D} := by
  simp only [Set.setOf_forall]
  apply MeasurableSet.iInter
  intro t
  have hm : Measurable (fun H : PairTrace n k => (H t, historyAction d H t)) :=
    (measurable_pi_apply t).prodMk ((measurable_pi_apply t).comp (historyAction_measurable d))
  exact (Set.to_countable {z : PairHistory n k × Pair n k |
    ZeroCompatible I z.1 → z.2 ∈ D}).measurableSet.preimage hm

/-- A candidate1 conditional restart uses D until the first P0-zero receipt.
The old prefix is retained in the original policy and is itself P0-compatible. -/
theorem unrevealed_restart_safe (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (d : Pair n k) (h : PairHistory n k)
    (hp : PositivePrefix I hI none s ρ π h) :
    ∀ᵐ H ∂markovHistoryLaw (I.kernel hI) 1 (currentState s h)
      (restartPolicy π (erasePairSources h)) (commonSeedPosterior (pairPolicy s π) ρ h),
      ∀ t, ZeroCompatible I (H t) → historyAction d H t ∈
        uncertainAllowed I (policyKnownRegion I hI s ρ π) (policyUncertainRegion I hI s ρ π) := by
  have hp' : PositivePrefix I hI (some h.length) s ρ π h := by
    unfold PositivePrefix at hp ⊢
    rwa [← prefix_mass_noChange_switchAt I hI s ρ π hπ h]
  rw [← fixedConditionalLaw_eq_restart I hI (some h.length) s ρ π hπ h 1 hp'
    (fun t ht => by simp only [fixedMode, if_neg (not_lt.mpr ht)])]
  apply fixedConditional_ae_of_prefix_imp I hI (some h.length) s ρ π h
    (fun H => CoherentTrace H ∧ ∀ t, ZeroCompatible I (H t) → historyAction d H t ∈
      uncertainAllowed I (policyKnownRegion I hI s ρ π) (policyUncertainRegion I hI s ρ π))
    _ (unrevealed_actions_mem_measurable _ _ d) _
    ((fixedPhysicalLaw_coherent I hI (some h.length) s ρ π hπ).and
      (fixedPhysicalLaw_uncertain_safe I hI (some h.length) s ρ π hπ hL d))
  intro H hh hB t ht
  rw [action_continuationReadout_shift]
  apply hB.2
  rw [Nat.add_comm,coherentTrace_take_append hB.1 h.length t,hh,zeroCompatible_append]
  exact ⟨ht,positive_noChange_compatible I hI s ρ π hπ h hp⟩

end HiddenChange
