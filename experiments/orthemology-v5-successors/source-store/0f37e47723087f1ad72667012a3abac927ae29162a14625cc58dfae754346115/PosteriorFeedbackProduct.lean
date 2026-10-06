import ResidualSeedPosterior

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.ResidualSeed

/-- Conditioning a genuine product input on a rectangle preserves product
structure after normalizing each factor. Positivity rules out null conditioning. -/
theorem normalized_product_rectangle
    {Ω Ξ : Type*} [MeasurableSpace Ω] [MeasurableSpace Ξ]
    (μ : Measure Ω) (ν : Measure Ξ) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    (C : Set Ω) (F : Set Ξ) (hC : 0 < μ C) (hF : 0 < ν F) :
    normalizedRestriction (μ.prod ν) (C ×ˢ F) =
      (normalizedRestriction μ C).prod (normalizedRestriction ν F) := by
  haveI : IsProbabilityMeasure (normalizedRestriction μ C) :=
    ProbabilityTheory.cond_isProbabilityMeasure hC.ne'
  haveI : IsProbabilityMeasure (normalizedRestriction ν F) :=
    ProbabilityTheory.cond_isProbabilityMeasure hF.ne'
  apply Eq.symm
  apply Measure.prod_eq
  intro S T hS hT
  simp only [normalizedRestriction, Measure.smul_apply,
    Measure.restrict_apply (hS.prod hT), Set.prod_inter_prod, Measure.prod_prod,
    Measure.restrict_apply hS, Measure.restrict_apply hT, smul_eq_mul]
  rw [ENNReal.mul_inv (Or.inl hC.ne') (Or.inr hF.ne')]
  ac_rfl

universe u v
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

def FeedbackEvent (h : History A Y) : Set (FlatStack A Y × RowOracle A Y) :=
  {ω | FeedbackCompatible ∅ (fun a n => ω.1 (a,n)) ω.2 h}

omit [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
theorem feedbackEvent_measurable (h : History A Y) :
    MeasurableSet (FeedbackEvent h) := by
  induction h with
  | nil => simp [FeedbackEvent, FeedbackCompatible]
  | cons ay h ih =>
      have hc : Measurable (fun ω : FlatStack A Y × RowOracle A Y => ω.2 h.length ay.1) :=
        (measurable_pi_apply ay.1).comp ((measurable_pi_apply h.length).comp measurable_snd)
      have he : FeedbackEvent (ay :: h) = FeedbackEvent h ∩
          {ω : FlatStack A Y × RowOracle A Y | ω.2 h.length ay.1 = ay.2} := by
        ext ω
        simp [FeedbackEvent, FeedbackCompatible, feedback, outsideCount]
      rw [he]
      apply ih.inter
      simpa only [Set.preimage, Set.mem_singleton_iff] using
        (measurableSet_singleton ay.2).preimage hc

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- The entire remaining feedback factor is independent of the residual seed.
Its own law is explicitly conditioned; this does not yet identify a shifted
unused-tail law with a fresh iid oracle. -/
theorem posterior_input_product (π : R → History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) :
    normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h) =
      (commonSeedPosterior π ρ h).prod
        (normalizedRestriction (feedbackLaw P P hP hN hP hN) (FeedbackEvent h)) := by
  have hc := positive_prefix_compatible_seeds π ρ P hP hN h hpos
  have hf : 0 < feedbackLaw P P hP hN hP hN (FeedbackEvent h) := by
    change 0 < feedbackLaw P P hP hN hP hN
      {ω | FeedbackCompatible ∅ (fun a n => ω.1 (a,n)) ω.2 h}
    rw [feedbackCompatible_probability ∅ h P P hP hN hP hN (fun _ _ => rfl)]
    rw [prefix_probability] at hpos
    exact (ENNReal.mul_pos_iff.mp hpos).2
  rw [prefixEvent_fiber]
  exact normalized_product_rectangle ρ (feedbackLaw P P hP hN hP hN)
    (CompatibleSeeds π h) (FeedbackEvent h) hc hf

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Every measurable function of the feedback remains independent of the
posterior seed. The feedback marginal below is the actual conditional one. -/
theorem posterior_seed_feedback_pushforward {T : Type*} [MeasurableSpace T]
    (π : R → History A Y → A) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h))
    (f : FlatStack A Y × RowOracle A Y → T) (hf : Measurable f) :
    (normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)).map
        (fun z => (z.1, f z.2)) =
      (commonSeedPosterior π ρ h).prod
        ((normalizedRestriction (feedbackLaw P P hP hN hP hN) (FeedbackEvent h)).map f) := by
  have hc := positive_prefix_compatible_seeds π ρ P hP hN h hpos
  have hF : 0 < feedbackLaw P P hP hN hP hN (FeedbackEvent h) := by
    change 0 < feedbackLaw P P hP hN hP hN
      {ω | FeedbackCompatible ∅ (fun a n => ω.1 (a,n)) ω.2 h}
    rw [feedbackCompatible_probability ∅ h P P hP hN hP hN (fun _ _ => rfl)]
    rw [prefix_probability] at hpos
    exact (ENNReal.mul_pos_iff.mp hpos).2
  haveI := commonSeedPosterior_probability π ρ h hc
  haveI : IsProbabilityMeasure
      (normalizedRestriction (feedbackLaw P P hP hN hP hN) (FeedbackEvent h)) :=
    ProbabilityTheory.cond_isProbabilityMeasure hF.ne'
  rw [posterior_input_product π ρ P hP hN h hpos]
  simpa only [Measure.map_id] using
    (Measure.map_prod_map (commonSeedPosterior π ρ h)
      (normalizedRestriction (feedbackLaw P P hP hN hP hN) (FeedbackEvent h))
      measurable_id hf).symm

/-- For the canonical all-query experiment, the prefix used rows 0,...,N-1;
these are the unused future row coordinates, with no selected receipt exposed. -/
def unusedOracleTail (N : ℕ) (ω : FlatStack A Y × RowOracle A Y) : RowOracle A Y :=
  fun n => ω.2 (N+n)

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
theorem unusedOracleTail_measurable (N : ℕ) :
    Measurable (unusedOracleTail (A := A) (Y := Y) N) :=
  measurable_pi_lambda _ (fun n => (measurable_pi_apply (N+n)).comp measurable_snd)

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- The entire unused oracle tail is conditionally independent of the seed.
The right marginal is stated honestly as its conditional law; identifying it
with the original iid row law is a further, separate distributional statement. -/
theorem posterior_seed_unused_tail_product
    (π : R → History A Y → A) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) :
    (normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)).map
        (fun z => (z.1, unusedOracleTail h.length z.2)) =
      (commonSeedPosterior π ρ h).prod
        ((normalizedRestriction (feedbackLaw P P hP hN hP hN) (FeedbackEvent h)).map
          (unusedOracleTail h.length)) :=
  posterior_seed_feedback_pushforward π ρ P hP hN h hpos
    (unusedOracleTail h.length) (unusedOracleTail_measurable h.length)

#print axioms posterior_seed_feedback_pushforward
#print axioms posterior_seed_unused_tail_product
#print axioms normalized_product_rectangle
#print axioms posterior_input_product
end HiddenParity.ResidualSeed
