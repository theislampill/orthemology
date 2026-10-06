import PolicyTraceBinding

/-!
# Finite-prefix residual seed cancellation

The likelihood factorization is derived from the retained actual history fiber
and independent feedback product law. The posterior uses restriction and
normalization on the actual finite history event, not an abstract posterior axiom.
-/
noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.ResidualSeed
universe u v
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

def CompatibleSeeds (π : R → History A Y → A) (h : History A Y) : Set R :=
  {r | ActionCompatible π r h}

instance compatibleSeedsDecidable (π : R → History A Y → A) (h : History A Y) (r : R) :
    Decidable (r ∈ CompatibleSeeds π h) := Classical.propDecidable _

def PrefixEvent (π : R → History A Y → A) (h : History A Y) : Set (Input R A Y) :=
  {z | historyTrajectory ∅ π z h.length = h}

def CanonicalInput (ρ : Measure R) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) : Measure (Input R A Y) :=
  ρ.prod (feedbackLaw P P hP hN hP hN)

def RowLikelihood (P : A → Y → ℝ) (h : History A Y) : ℝ≥0∞ :=
  ∏ i : Fin h.length, ENNReal.ofReal (P h[i].1 h[i].2)

def normalizedRestriction {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) (E : Set Ω) : Measure Ω := (μ E)⁻¹ • μ.restrict E

def seedPosterior (π : R → History A Y → A) (ρ : Measure R)
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) : Measure R :=
  (normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)).map Prod.fst

def commonSeedPosterior (π : R → History A Y → A) (ρ : Measure R)
    (h : History A Y) : Measure R := normalizedRestriction ρ (CompatibleSeeds π h)

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem compatibleSeeds_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (h : History A Y) :
    MeasurableSet (CompatibleSeeds π h) := by
  induction h with
  | nil => simp [CompatibleSeeds, ActionCompatible]
  | cons ay h ih =>
      exact ih.inter ((measurableSet_singleton ay.1).preimage
        (hπ.comp (measurable_id.prodMk measurable_const)))

theorem prefixEvent_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (h : History A Y) :
    MeasurableSet (PrefixEvent π h) :=
  (measurableSet_singleton h).preimage (historyTrajectory_coordinate_measurable ∅ π hπ h.length)

omit [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace R]
    [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- The observed prefix imposes separate seed and actual feedback constraints. -/
theorem prefixEvent_fiber (π : R → History A Y → A) (h : History A Y) :
    PrefixEvent π h = CompatibleSeeds π h ×ˢ
      {ω : FlatStack A Y × RowOracle A Y |
        FeedbackCompatible ∅ (fun a n => ω.1 (a,n)) ω.2 h} := by
  ext z
  exact observedHistory_fiber ∅ π z.2.2 z.1 (fun a n => z.2.1 (a,n)) h

omit [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Fixed-seed likelihood is the consistency indicator times the row product. -/
theorem fixed_seed_likelihood (π : R → History A Y → A) (r : R)
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) :
    feedbackLaw P P hP hN hP hN
      {ω | historyTrajectory ∅ π (r,ω) h.length = h} =
      if r ∈ CompatibleSeeds π h then RowLikelihood P h else 0 := by
  classical
  by_cases hc : r ∈ CompatibleSeeds π h
  · have he : {ω : FlatStack A Y × RowOracle A Y |
          historyTrajectory ∅ π (r,ω) h.length = h} =
        {ω | FeedbackCompatible ∅ (fun a n => ω.1 (a,n)) ω.2 h} := by
      ext ω
      simp only [historyTrajectory, observedHistory_fiber]
      exact and_iff_right hc
    rw [he, if_pos hc]
    exact feedbackCompatible_probability ∅ h P P hP hN hP hN (fun _ _ => rfl)
  · have he : {ω : FlatStack A Y × RowOracle A Y |
          historyTrajectory ∅ π (r,ω) h.length = h} = ∅ := by
      ext ω
      simp only [historyTrajectory, observedHistory_fiber, Set.mem_setOf_eq, Set.mem_empty_iff_false]
      exact iff_false_intro (fun hh => hc hh.1)
    rw [he, measure_empty, if_neg hc]

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Actual joint finite-history probability, obtained from the retained product
fiber theorem. No posterior or model-equivalence premise is supplied. -/
theorem seed_history_joint_probability (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) (D : Set R) :
    CanonicalInput ρ P hP hN {z | z.1 ∈ D ∧ z ∈ PrefixEvent π h} =
      ρ (D ∩ CompatibleSeeds π h) * RowLikelihood P h :=
  private_transcript_cylinder_probability ∅ π ρ P P hP hN hP hN (fun _ _ => rfl) D h

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
theorem prefix_probability (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) :
    CanonicalInput ρ P hP hN (PrefixEvent π h) =
      ρ (CompatibleSeeds π h) * RowLikelihood P h := by
  simpa only [Set.mem_univ, true_and, Set.univ_inter] using
    seed_history_joint_probability π ρ P hP hN h Set.univ

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- The unnormalized seed law after observing the prefix. -/
theorem restricted_seed_law (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) :
    ((CanonicalInput ρ P hP hN).restrict (PrefixEvent π h)).map Prod.fst =
      RowLikelihood P h • ρ.restrict (CompatibleSeeds π h) := by
  apply Measure.ext
  intro D hD
  rw [Measure.map_apply measurable_fst hD,
    Measure.restrict_apply (hD.preimage measurable_fst), Measure.smul_apply,
    Measure.restrict_apply hD]
  exact (seed_history_joint_probability π ρ P hP hN h D).trans (mul_comm _ _)

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem rowLikelihood_ne_top (P : A → Y → ℝ) (h : History A Y) :
    RowLikelihood P h ≠ ∞ := by
  exact ENNReal.prod_ne_top (fun _ _ => ENNReal.ofReal_ne_top)

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Model likelihood cancels on a positive actual prefix. -/
theorem seedPosterior_eq_common (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) :
    seedPosterior π ρ P hP hN h = commonSeedPosterior π ρ h := by
  have hfactor := prefix_probability π ρ P hP hN h
  have hL0 : RowLikelihood P h ≠ 0 := by
    intro hz
    rw [hfactor, hz, mul_zero] at hpos
    exact (lt_irrefl 0) hpos
  unfold seedPosterior normalizedRestriction commonSeedPosterior
  rw [Measure.map_smul, restricted_seed_law, smul_smul, hfactor]
  rw [ENNReal.mul_inv (Or.inr (rowLikelihood_ne_top P h))
    (Or.inr hL0), mul_assoc,
    ENNReal.inv_mul_cancel hL0 (rowLikelihood_ne_top P h), mul_one]
  rfl


instance canonicalInput_probability (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    IsProbabilityMeasure (CanonicalInput ρ P hP hN) := by
  unfold CanonicalInput
  infer_instance

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
theorem positive_prefix_compatible_seeds (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) :
    0 < ρ (CompatibleSeeds π h) := by
  rw [prefix_probability] at hpos
  exact (CanonicallyOrderedAdd.mul_pos.mp hpos).1

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem rowLikelihood_pos (P : A → Y → ℝ) (h : History A Y)
    (hsurvives : ∀ i : Fin h.length, 0 < P h[i].1 h[i].2) :
    0 < RowLikelihood P h := by
  exact pos_iff_ne_zero.mpr (Finset.prod_ne_zero_iff.mpr
    (fun i _ => (ENNReal.ofReal_pos.mpr (hsurvives i)).ne'))

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Survival is positivity of every observed full-row transition; rows need not
agree numerically across models for seed cancellation. -/
theorem surviving_model_prefix_positive (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hc : 0 < ρ (CompatibleSeeds π h))
    (hsurvives : ∀ i : Fin h.length, 0 < P h[i].1 h[i].2) :
    0 < CanonicalInput ρ P hP hN (PrefixEvent π h) := by
  rw [prefix_probability]
  exact CanonicallyOrderedAdd.mul_pos.mpr ⟨hc, rowLikelihood_pos P h hsurvives⟩

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem commonSeedPosterior_probability (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History A Y)
    (hc : 0 < ρ (CompatibleSeeds π h)) :
    IsProbabilityMeasure (commonSeedPosterior π ρ h) :=
  ProbabilityTheory.cond_isProbabilityMeasure hc.ne'

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
theorem posterior_equality_of_positive_prefixes (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P Q : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1) (h : History A Y)
    (hp : 0 < CanonicalInput ρ P hP hPN (PrefixEvent π h))
    (hq : 0 < CanonicalInput ρ Q hQ hQN (PrefixEvent π h)) :
    seedPosterior π ρ P hP hPN h = seedPosterior π ρ Q hQ hQN h := by
  rw [seedPosterior_eq_common π ρ P hP hPN h hp,
    seedPosterior_eq_common π ρ Q hQ hQN h hq]

/-- Histories are newest-first, so restarting appends the fixed old prefix on
its right. This definition exposes no model index or hidden priority. -/
def restartPolicy (π : R → History A Y → A) (h : History A Y)
    (r : R) (tail : History A Y) : A := π r (tail ++ h)

omit [DecidableEq A] [Inhabited Y] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem restartPolicy_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (h : History A Y) :
    Measurable (fun z : R × History A Y => restartPolicy π h z.1 z.2) :=
  hπ.comp (measurable_fst.prodMk
    ((measurable_of_countable (fun tail : History A Y => tail ++ h)).comp measurable_snd))

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace R]
    [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem compatible_append (π : R → History A Y → A) (r : R)
    (h tail : History A Y) :
    ActionCompatible π r (tail ++ h) ↔
      ActionCompatible π r h ∧ ActionCompatible (restartPolicy π h) r tail := by
  induction tail with
  | nil => simp [ActionCompatible]
  | cons ay tail ih => simp only [List.cons_append, ActionCompatible, ih, restartPolicy]; tauto

/-- Link the latent finite event to the actual acquired-history law. -/
theorem observed_prefix_mass_eq_input (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) :
    observedTraceLaw ∅ π ρ P P hP hN hP hN {H | H h.length = h} =
      CanonicalInput ρ P hP hN (PrefixEvent π h) := by
  unfold observedTraceLaw
  have hs : MeasurableSet {H : ℕ → History A Y | H h.length = h} := by
    simpa only [Set.preimage, Set.mem_singleton_iff] using
      (measurableSet_singleton h).preimage (measurable_pi_apply h.length)
  rw [Measure.map_apply (historyTrajectory_measurable ∅ π hπ) hs]
  rfl

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Empty history leaves the original seed law unchanged. -/
theorem empty_prefix_seedPosterior (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) : seedPosterior π ρ P hP hN [] = ρ := by
  have hp : 0 < CanonicalInput ρ P hP hN (PrefixEvent π []) := by
    rw [prefix_probability]
    simp [CompatibleSeeds, ActionCompatible, RowLikelihood]
  rw [seedPosterior_eq_common π ρ P hP hN [] hp]
  simp [commonSeedPosterior, normalizedRestriction, CompatibleSeeds, ActionCompatible]

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
/-- A zero-probability prefix produces the zero normalized-restriction measure,
not a probability posterior. This is why positive conditioning is required. -/
theorem impossible_prefix_seedPosterior (π : R → History A Y → A)
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hz : CanonicalInput ρ P hP hN (PrefixEvent π h) = 0) :
    seedPosterior π ρ P hP hN h = 0 := by
  have hr : (CanonicalInput ρ P hP hN).restrict (PrefixEvent π h) = 0 :=
    Measure.restrict_eq_zero.mpr hz
  simp [seedPosterior, normalizedRestriction, hr]

#print axioms empty_prefix_seedPosterior
#print axioms impossible_prefix_seedPosterior
#print axioms fixed_seed_likelihood
#print axioms restricted_seed_law
#print axioms seedPosterior_eq_common
#print axioms posterior_equality_of_positive_prefixes
#print axioms commonSeedPosterior_probability
#print axioms compatible_append
end HiddenParity.ResidualSeed

