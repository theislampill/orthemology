import RecursiveCanonicalEquivalence

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Set Finset
open scoped BigOperators ENNReal
attribute [local instance] Classical.propDecidable
namespace Orthemology.Tranche3
open Orthemology.Tranche2
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.Tranche2.FiniteAlphabetQuery
open CanonicalMicro
universe u v
variable {Θ A Y : Type u} {R : Type v}
    [Fintype Θ] [Fintype A] [Fintype Y] [DecidableEq Θ] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Dynamic licensing is an observable-history event. The action-only law
cannot by itself recover the observations needed for support updates. -/
def LicensedHistoryPath (P : Θ → A → Y → ℝ) (menu : Finset Θ → Finset A)
    (B : Finset Θ) (d : A) (H : ℕ → History A Y) : Prop :=
  ∀ n, historyAction d H n ∈ menu (historySupport P B (H n))

lemma measurableSet_licensedHistoryPath (P : Θ → A → Y → ℝ)
    (menu : Finset Θ → Finset A) (B : Finset Θ) (d : A) :
    MeasurableSet {H | LicensedHistoryPath P menu B d H} := by
  simp only [LicensedHistoryPath,Set.setOf_forall]
  apply MeasurableSet.iInter
  intro n
  change MeasurableSet ((fun H : ℕ → History A Y => (H (n+1),H n)) ⁻¹'
    {z : History A Y × History A Y | (z.1.headD (d,default)).1 ∈ menu (historySupport P B z.2)})
  exact ((Set.to_countable {z : History A Y × History A Y |
    (z.1.headD (d,default)).1 ∈ menu (historySupport P B z.2)}).measurableSet).preimage
    ((measurable_pi_apply (n+1)).prodMk (measurable_pi_apply n))

lemma actionCompatible_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (h : History A Y) :
    MeasurableSet {r | ActionCompatible π r h} := by
  induction h with
  | nil => exact MeasurableSet.univ
  | cons ay h ih =>
    exact ih.inter ((measurableSet_singleton ay.1).preimage
      (hπ.comp (measurable_id.prodMk measurable_const)))

lemma actionCompatible_fixed (π : R → History A Y → A) (r : R) (h : History A Y) :
    ActionCompatible (fun (_ : Unit) h => π r h) () h ↔ ActionCompatible π r h := by
  induction h with
  | nil => rfl
  | cons ay h ih => simp only [ActionCompatible,ih]

lemma rowHistory_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (r : R) : Measurable (rowHistory π r) := by
  have hh : Measurable (fun ω : RowOracle A Y => historyTrajectory ∅ π (r,((fun _ => default),ω))) :=
    (historyTrajectory_measurable ∅ π hπ).comp (measurable_const.prodMk (measurable_const.prodMk measurable_id))
  have he : (fun ω : RowOracle A Y => historyTrajectory ∅ π (r,((fun _ => default),ω))) = rowHistory π r := by
    funext ω n
    exact observedHistory_empty_eq_rowHistory π r ω _ n
  rwa [he] at hh

lemma observedTraceLaw_dirac_raw (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    observedTraceLaw ∅ π (Measure.dirac r) P P hP hN hP hN =
      (feedbackLaw P P hP hN hP hN).map (fun ω => historyTrajectory ∅ π (r,ω)) := by
  rw [observedTraceLaw,Measure.dirac_prod,Measure.map_map (historyTrajectory_measurable ∅ π hπ)
    (show Measurable (Prod.mk r) from measurable_const.prodMk measurable_id)]
  rfl

lemma observedTraceLaw_dirac_rows (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    observedTraceLaw ∅ π (Measure.dirac r) P P hP hN hP hN =
      (iidOracle (rowMeasure P hP hN)).map (rowHistory π r) := by
  rw [observedTraceLaw_dirac_raw π hπ r]
  have he : (fun ω : FlatStack A Y × RowOracle A Y => historyTrajectory ∅ π (r,ω)) = rowHistory π r ∘ Prod.snd := by
    funext ω n
    exact observedHistory_empty_eq_rowHistory π r ω.2 _ n
  rw [he,feedbackLaw,← Measure.map_map (rowHistory_measurable π hπ r) measurable_snd,
    Measure.map_snd_prod,measure_univ,one_smul]

lemma rowHistory_marginal_formula (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (n : ℕ) (h : History A Y) :
    ((iidOracle (rowMeasure P hP hN)).map (fun ω => rowHistory π r ω n)) {h} =
      if n = h.length then
        (Measure.dirac r) {r' | ActionCompatible π r' h} *
          ∏ i : Fin h.length, ENNReal.ofReal (P h[i].1 h[i].2) else 0 := by
  have he : (iidOracle (rowMeasure P hP hN)).map (fun ω => rowHistory π r ω n) =
      (observedTraceLaw ∅ π (Measure.dirac r) P P hP hN hP hN).map (fun H => H n) := by
    rw [observedTraceLaw_dirac_rows π hπ r,Measure.map_map (measurable_pi_apply n) (rowHistory_measurable π hπ r)]
    rfl
  rw [he,observedTraceLaw,Measure.map_map (measurable_pi_apply n) (historyTrajectory_measurable ∅ π hπ)]
  exact history_marginal_formula ∅ π hπ (Measure.dirac r) P P hP hN hP hN (fun a ha => (Finset.not_mem_empty a ha).elim) n h

lemma rowHistory_marginal_eq_historyPMF (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (n : ℕ) :
    (iidOracle (rowMeasure P hP hN)).map (fun ω => rowHistory π r ω n) = (historyPMF (π r) P hP hN n).toMeasure := by
  apply Measure.ext_of_singleton
  intro h
  rw [rowHistory_marginal_formula π hπ,PMF.toMeasure_apply_singleton _ h (measurableSet_singleton h),historyPMF_apply,
    Measure.dirac_apply' r (actionCompatible_measurable π hπ h)]
  simp only [actionCompatible_fixed]
  by_cases hn : n = h.length <;> by_cases hc : ActionCompatible π r h <;> simp [hn,hc]

lemma historySupport_positive (P : Θ → A → Y → ℝ) (B : Finset Θ) (h : History A Y) (θ : Θ)
    (ht : θ ∈ historySupport P B h) : ∀ ay ∈ h, 0 < P θ ay.1 ay.2 := by
  induction h with
  | nil => simp
  | cons ay h ih =>
    obtain ⟨ht,hy⟩ := (mem_supportUpdate P (historySupport P B h) ay.1 ay.2 θ).mp ht
    intro az haz
    rcases List.mem_cons.mp haz with rfl | hh
    · exact hy
    · exact ih ht az hh

/-- Every feasible consistent fixed-seed history has positive probability in
EACH of its live models. This is an actual finite-cylinder statement. -/
theorem feasible_rowHistory_positive (P : Θ → A → Y → ℝ)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (B : Finset Θ) (h : History A Y) (hc : ActionCompatible π r h)
    (θ : Θ) (ht : θ ∈ historySupport P B h) :
    0 < iidOracle (rowMeasure (P θ) (hP θ) (hN θ)) {ω | rowHistory π r ω h.length = h} := by
  change 0 < iidOracle (rowMeasure (P θ) (hP θ) (hN θ))
    ((fun ω => rowHistory π r ω h.length) ⁻¹' {h})
  rw [← Measure.map_apply
    (show Measurable (fun ω => rowHistory π r ω h.length) from (measurable_pi_apply h.length).comp (rowHistory_measurable π hπ r))
    (measurableSet_singleton h),rowHistory_marginal_formula π hπ r,if_pos rfl,
    Measure.dirac_apply_of_mem (s := {r' : R | ActionCompatible π r' h}) (a := r) hc,one_mul]
  apply pos_iff_ne_zero.mpr
  apply Finset.prod_ne_zero_iff.mpr
  intro i _
  exact (ENNReal.ofReal_pos.mpr (historySupport_positive P B h θ ht h[i] (List.getElem_mem i.isLt))).ne'

/-- Almost-sure licensing of a deterministic-seed policy implies pointwise
licensing on every feasible consistent public history. It says nothing about
other, null seeds of the original randomized policy. -/
theorem fixed_seed_ae_license_is_pointwise
    (P : Θ → A → Y → ℝ) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B : Finset Θ) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (r : R) (d : A)
    (hsafe : ∀ θ ∈ B, ∀ᵐ H ∂observedTraceLaw ∅ π (Measure.dirac r) (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ),
      LicensedHistoryPath P menu B d H)
    (h : History A Y) (hc : ActionCompatible π r h) (hne : (historySupport P B h).Nonempty) :
    π r h ∈ menu (historySupport P B h) := by
  obtain ⟨θ,ht⟩ := hne
  have hsubset : ∀ h : History A Y, historySupport P B h ⊆ B := by
    intro h
    induction h with
    | nil => exact Finset.Subset.refl _
    | cons ay h ih => exact (supportUpdate_subset P _ _ _).trans ih
  have hs := hsafe θ (hsubset h ht)
  rw [observedTraceLaw_dirac_rows π hπ r] at hs
  have hraw := ae_of_ae_map (rowHistory_measurable π hπ r).aemeasurable hs
  have hp := feasible_rowHistory_positive P hP hN π hπ r B h hc θ ht
  obtain ⟨ω,hω,hlegal⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hp.ne' (ae_restrict_of_ae hraw)
  have hh := hlegal h.length
  change rowHistory π r ω h.length = h at hω
  simpa only [historyAction,rowHistory,List.headD_cons,Prod.fst,hω] using hh

lemma rowHistory_actionCompatible (π : R → History A Y → A) (r : R) (ω : RowOracle A Y) (n : ℕ) :
    ActionCompatible π r (rowHistory π r ω n) := by
  induction n with
  | zero => trivial
  | succ n ih => exact ⟨ih,rfl⟩

/-- The true model survives every actual finite history almost surely, under
arbitrary policies; likelihood-zero symbols are not physically generated. -/
theorem rowHistory_true_live_ae (P : Θ → A → Y → ℝ)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (B : Finset Θ) (θ : Θ) (ht : θ ∈ B) :
    ∀ᵐ ω ∂iidOracle (rowMeasure (P θ) (hP θ) (hN θ)), ∀ n,
      θ ∈ historySupport P B (rowHistory π r ω n) := by
  apply ae_all_iff.mpr
  intro n
  have hi : ∀ h, historyPMF (π r) (P θ) (hP θ) (hN θ) n h ≠ 0 → θ ∈ historySupport P B h :=
    historyPMF_invariant (π r) (P θ) (hP θ) (hN θ) (fun h => θ ∈ historySupport P B h) ht
      (fun h y hh hy => (mem_supportUpdate P (historySupport P B h) (π r h) y θ).mpr ⟨hh,hy⟩) n
  have hm : ∀ᵐ h ∂(historyPMF (π r) (P θ) (hP θ) (hN θ) n).toMeasure, θ ∈ historySupport P B h := by
    rw [ae_iff,PMF.toMeasure_apply_eq_zero_iff _ _ (Set.to_countable _).measurableSet]
    exact Set.disjoint_left.mpr (fun h hh hn => hn (hi h ((PMF.mem_support_iff _ _).mp hh)))
  rw [← rowHistory_marginal_eq_historyPMF π hπ r] at hm
  exact ae_of_ae_map ((measurable_pi_apply n).comp (rowHistory_measurable π hπ r)).aemeasurable hm

/-- Pointwise feasible-history safety implies almost-sure all-time licensing in
the original observed-history law for every initially live model. -/
theorem pointwise_license_implies_ae_license
    (P : Θ → A → Y → ℝ) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B : Finset Θ) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A)
    (hlegal : ∀ r h, ActionCompatible π r h → (historySupport P B h).Nonempty →
      π r h ∈ menu (historySupport P B h))
    (θ : Θ) (ht : θ ∈ B) :
    ∀ᵐ H ∂observedTraceLaw ∅ π ρ (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ),
      LicensedHistoryPath P menu B d H := by
  have hrows : ∀ r, ∀ᵐ ω ∂iidOracle (rowMeasure (P θ) (hP θ) (hN θ)),
      LicensedHistoryPath P menu B d (rowHistory π r ω) := by
    intro r
    filter_upwards [rowHistory_true_live_ae P hP hN π hπ r B θ ht] with ω hω
    intro n
    exact hlegal r _ (rowHistory_actionCompatible π r ω n) ⟨θ,hω n⟩
  have hraw : ∀ r, ∀ᵐ z ∂feedbackLaw (P θ) (P θ) (hP θ) (hN θ) (hP θ) (hN θ),
      LicensedHistoryPath P menu B d (historyTrajectory ∅ π (r,z)) := by
    intro r
    have hm : MeasurableSet {z : FlatStack A Y × RowOracle A Y |
        LicensedHistoryPath P menu B d (historyTrajectory ∅ π (r,z))} :=
      (measurableSet_licensedHistoryPath P menu B d).preimage
        ((historyTrajectory_measurable ∅ π hπ).comp (measurable_const.prodMk measurable_id))
    apply (Measure.ae_prod_iff_ae_ae hm).mpr
    exact Filter.Eventually.of_forall (fun X => by
      have he : (fun ω => historyTrajectory ∅ π (r,(X,ω))) = rowHistory π r := by
        funext ω n
        exact observedHistory_empty_eq_rowHistory π r ω _ n
      filter_upwards [hrows r] with ω hω
      rw [congrFun he ω]
      exact hω)
  unfold observedTraceLaw
  apply (ae_map_iff (historyTrajectory_measurable ∅ π hπ).aemeasurable
    (measurableSet_licensedHistoryPath P menu B d)).mpr
  apply (Measure.ae_prod_iff_ae_ae
    ((measurableSet_licensedHistoryPath P menu B d).preimage (historyTrajectory_measurable ∅ π hπ))).mpr
  exact Filter.Eventually.of_forall hraw
end Orthemology.Tranche3
