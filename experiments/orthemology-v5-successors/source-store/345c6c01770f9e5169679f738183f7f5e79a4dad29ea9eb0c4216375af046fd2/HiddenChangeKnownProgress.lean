import HiddenChangeParityBridge
import StableSupportParityNecessity

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.Adaptive
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

omit [NeZero n] in
theorem real_support_eq_succ (I : Input n k) (hI : I.Valid) (σ : Mode) :
    supportSuccessors (realRows (I.kernel hI) σ) = succ I σ := by
  funext e
  ext y
  simp only [supportSuccessors,succ,Finset.mem_filter,Finset.mem_univ,true_and,
    realRows,OrthemicCertificate.Input.kernel_row]
  exact_mod_cast Iff.rfl

/-- Actual arbitrary-policy recurrence and path laws supply known1 progress.
This helper's allowed-set and parity premises are discharged by the policy-relative
construction below; they are not assumptions of its postfixedness theorem. -/
theorem known_progress_of_stationary (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (d : Pair n k) (D : PairSet n k)
    (hSafe : ∀ᵐ H ∂markovHistoryLaw (I.kernel hI) 1 s π ρ,
      ∀ t, historyAction d H t ∈ D)
    (hParity : ∀ᵐ H ∂markovHistoryLaw (I.kernel hI) 1 s π ρ,
      ParitySuccess (I.priority 1) (historyAction d H)) : KnownProgress I D s := by
  let μ := markovPairLaw (I.kernel hI) 1 s π ρ d
  haveI : IsProbabilityMeasure μ := actionLaw_isProbability (pairPolicy s π)
    (pairPolicy_measurable s π hπ) ρ _ _ _ d
  have hSafe' : ∀ᵐ x ∂μ, ∀ t, x t ∈ D :=
    (ae_map_iff (historyAction_measurable d).aemeasurable (by
      simp only [Set.setOf_forall]
      exact MeasurableSet.iInter (fun t => D.measurableSet.preimage (measurable_pi_apply t)))).mpr hSafe
  have hParity' : ∀ᵐ x ∂μ, ParitySuccess (I.priority 1) x :=
    (ae_map_iff (historyAction_measurable d).aemeasurable (paritySuccess_measurable _)).mpr hParity
  obtain ⟨E,hne,hED,hpos⟩ := exists_positive_recurrent_support μ id D
    (hSafe'.mono (fun _ hx => Eventually.of_forall hx))
  have hGraph := canonical_markov_recurrent_end_component s π hπ ρ
    (realRows (I.kernel hI) 1) (realRows_nonnegative _ _) (realRows_normalized _ _) d
  have hPath := canonical_markov_supported_path s π hπ ρ
    (realRows (I.kernel hI) 1) (realRows_nonnegative _ _) (realRows_normalized _ _) d
  obtain ⟨x,hx,hGraphX,hSafeX,hPathX,hParityX⟩ :=
    Measure.exists_mem_of_measure_ne_zero_of_ae hpos.ne'
      (ae_restrict_of_ae (hGraph.and (hSafe'.and (hPath.and hParity'))))
  have hRec : recurrentSet x = E := hx
  have hEC : IsEndComponent Prod.fst (succ I 1) E := by
    simpa only [hRec,real_support_eq_succ I hI 1] using hGraphX
  have hEven : EvenMinimum I 1 E := by
    apply (evenMinimum_iff I 1 E).mpr
    simpa only [ParitySuccess,hRec] using hParityX
  obtain ⟨e,he⟩ := hne
  have heRec : Recurs x e := (mem_recurrentSet x e).mp (hRec.symm ▸ he)
  obtain ⟨t,ht⟩ := heRec.exists
  have hstep : ∀ j, (x (j+1)).1 ∈ succ I 1 (x j) := by
    intro j
    apply Finset.mem_filter.mpr
    refine ⟨Finset.mem_univ _,?_⟩
    have hp := hPathX.2 j
    change (0 : ℝ) < (I.row 1 (x j) (x (j+1)).1 : ℝ) at hp
    exact_mod_cast hp
  have hr := retained_segment_reachable Prod.fst (succ I 1) x D 0 t
    (Nat.zero_le _) (fun j _ => hSafeX j) hstep
  refine ⟨E,Finset.mem_powerset.mpr hED,⟨hEC,hEven⟩,e.1,
    Finset.mem_image.mpr ⟨e,he,rfl⟩,?_⟩
  simpa only [hPathX.1,ht] using hr

/-- The known region is genuinely postfixed for the one arbitrary original
policy, using only success of its original deterministic fixed-index laws. -/
theorem policyKnownRegion_postfixed (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (d : Pair n k)
    (hWin : ∀ N : ℕ, ∀ᵐ H ∂fixedLaw I hI (some N) s ρ π, TaggedParity I d H) :
    policyKnownRegion I hI s ρ π ⊆ F1 I (policyKnownRegion I hI s ρ π) := by
  intro t ht
  obtain ⟨N,h,hN,hp,he⟩ := (mem_policyKnownRegion I hI s ρ π t).mp ht
  apply (mem_F1 I _ t).mpr
  refine ⟨ht,?_⟩
  rw [← he]
  haveI := commonSeedPosterior_probability (pairPolicy s π) ρ h
    (((positive_prefix_factors I hI (some N) s ρ π hπ h).mp hp).1)
  apply known_progress_of_stationary I hI _ _ _
    (restartPolicy_measurable π hπ (erasePairSources h)) d _
    (known_restart_safe I hI N s ρ π hπ hL d h hN hp)
  exact fixed_restart_ae_parity I hI (some N) s ρ π hπ h hp
    (fun j hj => by simp only [fixedMode,finalMode,if_neg (not_lt.mpr (hN.trans hj))]) d (hWin N)

end HiddenChange
