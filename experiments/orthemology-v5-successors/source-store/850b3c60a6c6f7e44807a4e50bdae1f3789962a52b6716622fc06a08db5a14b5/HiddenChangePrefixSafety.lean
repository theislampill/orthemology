import HiddenChangePolicyRegions

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

/-- P0 compatibility concerns receipts, not seed likelihood or P1 survival. -/
def ZeroCompatible (I : Input n k) (h : PairHistory n k) : Prop :=
  ∀ i : Fin h.length, 0 < I.row 0 h[i].1 h[i].2

omit [NeZero n] in
theorem fixedPrefixLikelihood_positive_iff (I : Input n k) (κ : ChangeIndex)
    (h : PairHistory n k) :
    0 < fixedPrefixLikelihood I κ h ↔
      ∀ i : Fin h.length, 0 < I.row (fixedMode κ (h.length-1-i.val)) h[i].1 h[i].2 := by
  rw [pos_iff_ne_zero, fixedPrefixLikelihood, Finset.prod_ne_zero_iff]
  simp only [Finset.mem_univ, forall_const]
  apply forall_congr'
  intro i
  rw [← pos_iff_ne_zero, ENNReal.ofReal_pos]
  exact_mod_cast Iff.rfl

theorem positive_noChange_compatible (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (hp : PositivePrefix I hI none s ρ π h) : ZeroCompatible I h := by
  have hl := ((positive_prefix_factors I hI none s ρ π hπ h).mp hp).2
  exact (fixedPrefixLikelihood_positive_iff I none h).mp hl

/-- Common action-compatible seed mass makes every P0-compatible original
fixed-index prefix positive under the original no-change law. -/
theorem compatible_prefix_noChange (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (hp : PositivePrefix I hI κ s ρ π h)
    (hc : ZeroCompatible I h) : PositivePrefix I hI none s ρ π h := by
  apply (positive_prefix_factors I hI none s ρ π hπ h).mpr
  exact ⟨((positive_prefix_factors I hI κ s ρ π hπ h).mp hp).1,
    (fixedPrefixLikelihood_positive_iff I none h).mpr hc⟩

/-- Until a P0-zero receipt, positively used mode1 pairs obey the same complete
uncertain safety predicate as original no-change pairs. -/
theorem selected_unrevealed_uncertainAllowed (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (h : PairHistory n k) (e : Pair n k)
    (hp : PositivePrefix I hI κ s ρ π h) (hc : ZeroCompatible I h)
    (he : PositiveSelected s ρ π h e) :
    e ∈ uncertainAllowed I (policyKnownRegion I hI s ρ π)
      (policyUncertainRegion I hI s ρ π) :=
  selected_uncertainAllowed I hI s ρ π hπ hL h e
    (compatible_prefix_noChange I hI κ s ρ π hπ h hp hc) he

/-- A countable-valued observation almost surely belongs to a positive fiber.
No independence, stationarity, or conditional-measure assumption is needed. -/
theorem ae_positive_fiber {Ω A : Type*} [MeasurableSpace Ω] [Countable A]
    (μ : Measure Ω) (f : Ω → A) : ∀ᵐ ω ∂μ, 0 < μ {z | f z = f ω} := by
  have hEach : ∀ a : A, ∀ᵐ ω ∂μ, f ω = a → 0 < μ {z | f z = a} := by
    intro a
    by_cases hp : 0 < μ {z | f z = a}
    · exact ae_of_all μ (fun _ _ => hp)
    · have hz : μ {z | f z = a} = 0 := le_antisymm (not_lt.mp hp) (zero_le _)
      rw [ae_iff]
      simpa only [hp, imp_false, not_not] using hz
  filter_upwards [ae_all_iff.mpr hEach] with ω hω
  exact hω (f ω) rfl

/-- Minimal consistency of newest-first physical history traces. -/
def CoherentTrace (H : PairTrace n k) : Prop :=
  H 0 = [] ∧ ∀ t, ∃ e y, H (t+1) = (e,y)::H t

omit [NeZero n] in
theorem coherentTrace_measurable : MeasurableSet {H : PairTrace n k | CoherentTrace H} := by
  simp only [CoherentTrace, Set.setOf_and]
  apply MeasurableSet.inter
  · exact (measurableSet_singleton []).preimage (measurable_pi_apply 0)
  · simp only [Set.setOf_forall]
    apply MeasurableSet.iInter
    intro t
    have hm : Measurable (fun H : PairTrace n k => (H t, H (t+1))) :=
      (measurable_pi_apply t).prodMk (measurable_pi_apply (t+1))
    exact (Set.to_countable {z : PairHistory n k × PairHistory n k |
      ∃ e y, z.2 = (e,y)::z.1}).measurableSet.preimage hm

omit [NeZero n] in
theorem coherentTrace_length {H : PairTrace n k} (hH : CoherentTrace H) (t : ℕ) :
    (H t).length = t := by
  induction t with
  | zero => simp [hH.1]
  | succ t ih => obtain ⟨e,y,he⟩ := hH.2 t; simp [he,ih]

theorem fixedPhysicalLaw_coherent (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π, CoherentTrace H := by
  unfold fixedPhysicalLaw fixedLaw observedTraceLaw
  rw [Measure.map_map eraseModeTrace_measurable
    (historyTrajectory_measurable ∅ _ (fixedPolicy_measurable κ s π hπ))]
  apply (ae_map_iff (eraseModeTrace_measurable.comp
    (historyTrajectory_measurable ∅ _ (fixedPolicy_measurable κ s π hπ))).aemeasurable
      coherentTrace_measurable).mpr
  exact ae_of_all _ (fun z => ⟨rfl, fun t => ⟨_,_,rfl⟩⟩)

/-- The countable exceptional union is removed on the actual law itself. -/
theorem fixedPhysicalLaw_positive_prefixes (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π,
      ∀ t, PositivePrefix I hI κ s ρ π (H t) := by
  have ha : ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π,
      ∀ t, 0 < fixedPhysicalLaw I hI κ s ρ π {G | G t = H t} :=
    ae_all_iff.mpr (fun t => ae_positive_fiber (fixedPhysicalLaw I hI κ s ρ π) (fun H : PairTrace n k => H t))
  filter_upwards [ha, fixedPhysicalLaw_coherent I hI κ s ρ π hπ] with H hpos hc
  intro t
  unfold PositivePrefix
  rw [coherentTrace_length hc t]
  exact hpos t

theorem positive_cons_selected (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (e : Pair n k) (y : State n)
    (hp : PositivePrefix I hI κ s ρ π ((e,y)::h)) : PositiveSelected s ρ π h e :=
  ((positive_prefix_factors I hI κ s ρ π hπ _).mp hp).1

/-- Almost surely every actual next pair has a positive compatible-seed branch. -/
theorem fixedPhysicalLaw_selected (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (d : Pair n k) :
    ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π,
      ∀ t, PositiveSelected s ρ π (H t) (historyAction d H t) := by
  filter_upwards [fixedPhysicalLaw_positive_prefixes I hI κ s ρ π hπ,
    fixedPhysicalLaw_coherent I hI κ s ρ π hπ] with H hp hc
  intro t
  obtain ⟨e,y,he⟩ := hc.2 t
  have hp' := hp (t+1)
  rw [he] at hp'
  have ha : historyAction d H t = e := by simp [historyAction,he]
  rw [ha]
  exact positive_cons_selected I hI κ s ρ π hπ (H t) e y hp'

/-- All actual post-switch selected pairs are known-safe almost surely. -/
theorem fixedPhysicalLaw_known_safe (I : Input n k) (hI : I.Valid)
    (N : ℕ) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (d : Pair n k) :
    ∀ᵐ H ∂fixedPhysicalLaw I hI (some N) s ρ π,
      ∀ t, N ≤ t → historyAction d H t ∈ knownAllowed I (policyKnownRegion I hI s ρ π) := by
  filter_upwards [fixedPhysicalLaw_positive_prefixes I hI (some N) s ρ π hπ,
    fixedPhysicalLaw_coherent I hI (some N) s ρ π hπ,
    fixedPhysicalLaw_selected I hI (some N) s ρ π hπ d] with H hp hc he
  intro t ht
  apply selected_knownAllowed I hI s ρ π hπ hL N (H t) _ _ (hp t) (he t)
  rwa [coherentTrace_length hc t]

/-- All actual unrevealed pairs are uncertain-safe under every original fixed law. -/
theorem fixedPhysicalLaw_uncertain_safe (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (d : Pair n k) :
    ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π,
      ∀ t, ZeroCompatible I (H t) → historyAction d H t ∈
        uncertainAllowed I (policyKnownRegion I hI s ρ π) (policyUncertainRegion I hI s ρ π) := by
  filter_upwards [fixedPhysicalLaw_positive_prefixes I hI κ s ρ π hπ,
    fixedPhysicalLaw_selected I hI κ s ρ π hπ d] with H hp he
  intro t ht
  exact selected_unrevealed_uncertainAllowed I hI κ s ρ π hπ hL (H t) _ (hp t) ht (he t)

end HiddenChange
