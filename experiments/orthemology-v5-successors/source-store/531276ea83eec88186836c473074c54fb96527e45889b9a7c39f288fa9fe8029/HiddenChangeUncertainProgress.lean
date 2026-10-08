import HiddenChangeUncertainPaths

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.Adaptive
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

/-- Progress starts at an actual positive compatible original prefix after
which the governing mode is constant. Every safety and recurrence fact below
comes from the actual arbitrary-policy law. -/
theorem uncertain_progress_at_prefix (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hLaw : PolicyLawful I s π) (d : Pair n k)
    (hWin : ∀ κ, ∀ᵐ H ∂fixedLaw I hI κ s ρ π, TaggedParity I d H)
    (κ : ChangeIndex) (h : PairHistory n k)
    (hp : PositivePrefix I hI κ s ρ π h) (hc : ZeroCompatible I h)
    (hconstant : ∀ t, h.length ≤ t → fixedMode κ t = finalMode κ) :
    UncertainProgress I (policyKnownRegion I hI s ρ π)
      (uncertainAllowed I (policyKnownRegion I hI s ρ π) (policyUncertainRegion I hI s ρ π))
      (finalMode κ) (currentState s h) := by
  let μ := fixedPhysicalLaw I hI κ s ρ π
  let D := uncertainAllowed I (policyKnownRegion I hI s ρ π) (policyUncertainRegion I hI s ρ π)
  let C : Set (PairTrace n k) := {H | H h.length = h ∧ ∀ t, ZeroCompatible I (H t)}
  have hAS := (fixedPhysicalLaw_coherent I hI κ s ρ π hπ).and
    ((fixedPhysicalLaw_supported_path I hI κ s ρ π hπ d).and
      ((fixedPhysicalLaw_positive_successors I hI κ s ρ π hπ d).and
        ((fixedPhysicalLaw_recurrent_component I hI κ s ρ π hπ d).and
          (fixedPhysicalLaw_uncertain_safe I hI κ s ρ π hπ hLaw d))))
  by_cases hCpos : 0 < μ C
  · have hUnion : C = ⋃ E : PairSet n k,
        {H | H h.length = h ∧ (∀ t, ZeroCompatible I (H t)) ∧ recurrentSet (historyAction d H) = E} := by
      ext H
      simp only [Set.mem_iUnion,Set.mem_setOf_eq,C]
      constructor
      · rintro ⟨hh,hcomp⟩; exact ⟨recurrentSet (historyAction d H),hh,hcomp,rfl⟩
      · rintro ⟨E,hh,hcomp,_⟩; exact ⟨hh,hcomp⟩
    rw [hUnion] at hCpos
    obtain ⟨E,hEpos⟩ := exists_measure_pos_of_not_measure_iUnion_null hCpos.ne'
    have hRival : ∀ σ, Match I.row (finalMode κ) σ E → EvenMinimum I σ E :=
      positive_compatible_recurrent_even I hI s ρ π hπ d hWin κ E
        (hEpos.trans_le (measure_mono (fun H hH => ⟨hH.2.2,hH.2.1⟩)))
    obtain ⟨H,hH,hcoh,hSupp,hSucc,hGraph,hSafe⟩ :=
      Measure.exists_mem_of_measure_ne_zero_of_ae hEpos.ne' (ae_restrict_of_ae hAS)
    have hRec : recurrentSet (historyAction d H) = E := hH.2.2
    have hEC : IsEndComponent Prod.fst (succ I (finalMode κ)) E := by rwa [hRec] at hGraph
    have hED : E ⊆ D := by
      rw [← hRec]
      exact recurrentSet_subset_of_eventually_mem _ D
        (Eventually.of_forall (fun t => hSafe t (hH.2.1 t)))
    have hNoExit : ∀ e ∈ E, ∀ y, 0 < I.row (finalMode κ) e y → 0 < I.row 0 e y := by
      intro e he y hy
      have hr : Recurs (historyAction d H) e := (mem_recurrentSet _ _).mp (hRec.symm ▸ he)
      obtain ⟨t,ht,hyEq⟩ := (hSucc e hr y hy).exists
      have he0 := ((coherent_edge_compatible_iff I s d hcoh hSupp.1 t).mp (hH.2.1 (t+1))).1
      simpa only [ht,hyEq] using he0
    obtain ⟨e,he⟩ := hEC.nonempty
    obtain ⟨t,ht,het⟩ := frequently_atTop.mp ((mem_recurrentSet _ e).mp (hRec.symm ▸ he)) h.length
    have hPath := internal_segment_reachable I (finalMode κ) D (historyAction d H) h.length t ht
      (fun j _ _ => hSafe j (hH.2.1 j))
      (fun j hj _ => ⟨by simpa only [hconstant j hj] using hSupp.2.2 j,
        ((coherent_edge_compatible_iff I s d hcoh hSupp.1 j).mp (hH.2.1 (j+1))).1⟩)
    left
    refine ⟨E,Finset.mem_powerset.mpr hED,⟨hEC,hNoExit,hRival⟩,e.1,
      Finset.mem_image.mpr ⟨e,he,rfl⟩,?_⟩
    simpa only [hSupp.1 h.length,hH.1,het] using hPath
  · have hCzero : μ C = 0 := le_antisymm (not_lt.mp hCpos) (zero_le _)
    have hBad : ∀ᵐ H ∂μ, H h.length = h → ¬ ∀ t, ZeroCompatible I (H t) := by
      rw [ae_iff]
      simpa only [_root_.not_imp,not_not,C] using hCzero
    obtain ⟨H,hH,hgood,hbad⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hp.ne'
      (ae_restrict_of_ae (hAS.and hBad))
    change H h.length = h at hH
    have hL : ZeroCompatible I (H h.length) := hH.symm ▸ hc
    have hprog := uncertain_exit_of_trace I hI (finalMode κ)
      (policyKnownRegion I hI s ρ π) (policyUncertainRegion I hI s ρ π)
      s d H h.length hgood.1 hgood.2.1.1 hL
      (fun t ht => by simpa only [hconstant t ht] using hgood.2.1.2.2 t)
      hgood.2.2.2.2 (hbad hH)
    simpa only [hH] using hprog

/-- The uncertain policy-relative region is genuinely postfixed, with both
candidate progress obligations derived from the original fixed-index winner. -/
theorem policyUncertainRegion_postfixed (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hLaw : PolicyLawful I s π) (d : Pair n k)
    (hWin : ∀ κ, ∀ᵐ H ∂fixedLaw I hI κ s ρ π, TaggedParity I d H) :
    policyUncertainRegion I hI s ρ π ⊆
      F I (policyKnownRegion I hI s ρ π) (policyUncertainRegion I hI s ρ π) := by
  intro t ht
  obtain ⟨h,hp,he⟩ := (mem_policyUncertainRegion I hI s ρ π t).mp ht
  apply (mem_F I _ _ t).mpr
  refine ⟨ht,?_⟩
  intro θ
  rw [← he]
  have hc := positive_noChange_compatible I hI s ρ π hπ h hp
  fin_cases θ
  · exact uncertain_progress_at_prefix I hI s ρ π hπ hLaw d hWin none h hp hc (fun _ _ => rfl)
  · have hp' : PositivePrefix I hI (some h.length) s ρ π h := by
      unfold PositivePrefix at hp ⊢
      rwa [← prefix_mass_noChange_switchAt I hI s ρ π hπ h]
    exact uncertain_progress_at_prefix I hI s ρ π hπ hLaw d hWin (some h.length) h hp' hc
      (fun j hj => by simp [fixedMode,finalMode,not_lt.mpr hj])

end HiddenChange
