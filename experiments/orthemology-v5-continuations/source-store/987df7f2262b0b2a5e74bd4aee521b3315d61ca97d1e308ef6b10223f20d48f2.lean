import ResidualSeedPosterior

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.ResidualSeed.Continuation
universe u v
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- Likelihood multiplies across the actual newest-first list append. -/
theorem rowLikelihood_cons (P : A → Y → ℝ) (ay : A × Y) (h : History A Y) :
    RowLikelihood P (ay :: h) = ENNReal.ofReal (P ay.1 ay.2) * RowLikelihood P h := by
  simp [RowLikelihood, Fin.prod_univ_succ]

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem rowLikelihood_append (P : A → Y → ℝ) (tail h : History A Y) :
    RowLikelihood P (tail ++ h) = RowLikelihood P tail * RowLikelihood P h := by
  induction tail with
  | nil => simp [RowLikelihood]
  | cons ay tail ih =>
      rw [List.cons_append, rowLikelihood_cons, rowLikelihood_cons, ih, mul_assoc]

omit [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- A fully observed longer prefix entails its actual older suffix. -/
theorem prefixEvent_append_subset (π : R → History A Y → A) (tail h : History A Y) :
    PrefixEvent π (tail ++ h) ⊆ PrefixEvent π h := by
  intro z hz
  have hd := observedHistory_drop ∅ π z.2.2 z.1 (fun a n => z.2.1 (a,n))
    (tail ++ h).length h.length (by simp)
  change (historyTrajectory ∅ π z (tail ++ h).length).drop
      ((tail ++ h).length - h.length) = historyTrajectory ∅ π z h.length at hd
  change historyTrajectory ∅ π z (tail ++ h).length = tail ++ h at hz
  rw [hz] at hd
  simpa using hd.symm

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] [MeasurableSpace R] in
/-- Compatibility splits into the fixed old seed event and the restarted policy's
continuation compatibility event. -/
theorem compatibleSeeds_append (π : R → History A Y → A) (tail h : History A Y) :
    CompatibleSeeds π (tail ++ h) =
      CompatibleSeeds (restartPolicy π h) tail ∩ CompatibleSeeds π h := by
  ext r
  simpa only [CompatibleSeeds, Set.mem_setOf_eq, Set.mem_inter_iff, and_comm] using
    compatible_append π r h tail

/-- Probability of an actual extended prefix under the actual normalized
restriction to the old prefix. Prefix likelihood cancels; no residual-law
identification or posterior-equivalence hypothesis is used. -/
theorem conditional_extension_probability
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h tail : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) :
    normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)
      (PrefixEvent π (tail ++ h)) =
      commonSeedPosterior π ρ h (CompatibleSeeds (restartPolicy π h) tail) *
        RowLikelihood P tail := by
  have hL0 : RowLikelihood P h ≠ 0 := by
    rw [prefix_probability] at hpos
    exact (ENNReal.mul_pos_iff.mp hpos).2.ne'
  have htMeas := prefixEvent_measurable π hπ (tail ++ h)
  have hCMeas := compatibleSeeds_measurable (restartPolicy π h)
    (restartPolicy_measurable π hπ h) tail
  unfold normalizedRestriction
  rw [Measure.smul_apply, Measure.restrict_apply htMeas,
    Set.inter_eq_left.mpr (prefixEvent_append_subset π tail h),
    prefix_probability, prefix_probability, rowLikelihood_append,
    compatibleSeeds_append]
  unfold commonSeedPosterior normalizedRestriction
  rw [Measure.smul_apply, Measure.restrict_apply hCMeas]
  simp only [smul_eq_mul]
  rw [ENNReal.mul_inv (Or.inr (rowLikelihood_ne_top P h)) (Or.inr hL0)]
  calc
    _ = (ρ (CompatibleSeeds π h))⁻¹ *
        ρ (CompatibleSeeds (restartPolicy π h) tail ∩ CompatibleSeeds π h) *
        RowLikelihood P tail * ((RowLikelihood P h)⁻¹ * RowLikelihood P h) := by ac_rfl
    _ = _ := by rw [ENNReal.inv_mul_cancel hL0 (rowLikelihood_ne_top P h), mul_one]

/-- Full-row agreement on the used continuation pairs suffices; old prefix
likelihoods may be different. -/
theorem conditional_extension_eq
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P Q : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (h tail : History A Y)
    (hp : 0 < CanonicalInput ρ P hP hPN (PrefixEvent π h))
    (hq : 0 < CanonicalInput ρ Q hQ hQN (PrefixEvent π h))
    (hrows : ∀ i : Fin tail.length, P tail[i].1 tail[i].2 = Q tail[i].1 tail[i].2) :
    normalizedRestriction (CanonicalInput ρ P hP hPN) (PrefixEvent π h)
      (PrefixEvent π (tail ++ h)) =
    normalizedRestriction (CanonicalInput ρ Q hQ hQN) (PrefixEvent π h)
      (PrefixEvent π (tail ++ h)) := by
  rw [conditional_extension_probability π hπ ρ P hP hPN h tail hp,
    conditional_extension_probability π hπ ρ Q hQ hQN h tail hq]
  congr 1
  exact Finset.prod_congr rfl (fun i _ => congrArg ENNReal.ofReal (hrows i))

#print axioms conditional_extension_probability
#print axioms conditional_extension_eq
end HiddenParity.ResidualSeed.Continuation
