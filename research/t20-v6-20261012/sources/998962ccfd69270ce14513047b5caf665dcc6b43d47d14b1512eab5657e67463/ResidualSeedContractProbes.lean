import MarkovSeedPosterior

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.ResidualSeed HiddenParity.Stochastic
namespace IndependentResidualSeedReview

def headOutcome (_r : Unit) (h : History Bool Bool) : Bool := (h.headD (false,false)).2
def oldHistory : History Bool Bool := [(false,false)]
def newHistory : History Bool Bool := [(true,true)]

theorem right_append_readout : restartPolicy headOutcome oldHistory () newHistory = true := rfl
theorem wrong_append_readout : headOutcome () (oldHistory ++ newHistory) = false := rfl
theorem wrong_append_is_different :
    restartPolicy headOutcome oldHistory () newHistory ≠ headOutcome () (oldHistory ++ newHistory) := by
  simp [right_append_readout,wrong_append_readout]

def oldPairHistory : History (Bool × Bool) Bool := [((false,false),true)]
def constantAction (_r : Unit) (_h : History Bool Bool) : Bool := false

theorem correct_restart_source :
    (pairPolicy (currentState false oldPairHistory)
      (restartPolicy constantAction (erasePairSources oldPairHistory)) () []).1 = true := rfl

theorem wrong_restart_source :
    (pairPolicy false (restartPolicy constantAction (erasePairSources oldPairHistory)) () []).1 = false := rfl

/-- Different numerical rows are permitted. Only both actual prefixes' positive
mass is assumed; no model-row equality or posterior identity is a premise. -/
theorem independent_cross_model_contract
    (pi : Bool → History Bool Bool → Bool) (rho : Measure Bool) [IsProbabilityMeasure rho]
    (P Q : Bool → Bool → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y=1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y=1)
    (h : History Bool Bool)
    (hp : 0 < CanonicalInput rho P hP hPN (PrefixEvent pi h))
    (hq : 0 < CanonicalInput rho Q hQ hQN (PrefixEvent pi h)) :
    seedPosterior pi rho P hP hPN h = seedPosterior pi rho Q hQ hQN h :=
  posterior_equality_of_positive_prefixes pi rho P Q hP hPN hQ hQN h hp hq

/-- A null event does not secretly produce a normalized posterior. -/
theorem null_posterior_not_probability
    (pi : Bool → History Bool Bool → Bool) (rho : Measure Bool)
    (P : Bool → Bool → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y=1)
    (h : History Bool Bool)
    (hz : CanonicalInput rho P hP hN (PrefixEvent pi h)=0) :
    ¬ IsProbabilityMeasure (seedPosterior pi rho P hP hN h) := by
  rw [impossible_prefix_seedPosterior pi rho P hP hN h hz]
  intro hp
  haveI := hp
  have hm := measure_univ (μ := (0 : Measure Bool))
  simp at hm

/-- The right factor is expressly the actual conditioned feedback marginal.
It is not replaced by a fresh iid oracle law. -/
theorem independent_tail_contract
    (pi : Bool → History Bool Bool → Bool) (rho : Measure Bool) [IsProbabilityMeasure rho]
    (P : Bool → Bool → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y=1)
    (h : History Bool Bool)
    (hp : 0 < CanonicalInput rho P hP hN (PrefixEvent pi h)) :
    (normalizedRestriction (CanonicalInput rho P hP hN) (PrefixEvent pi h)).map
      (fun z => (z.1,unusedOracleTail h.length z.2)) =
    (commonSeedPosterior pi rho h).prod
      ((normalizedRestriction (feedbackLaw P P hP hN hP hN) (FeedbackEvent h)).map
        (unusedOracleTail h.length)) :=
  posterior_seed_unused_tail_product pi rho P hP hN h hp

set_option pp.explicit true in
#check @independent_cross_model_contract
set_option pp.explicit true in
#check @independent_tail_contract
#print axioms wrong_append_is_different
#print axioms correct_restart_source
#print axioms wrong_restart_source
#print axioms independent_cross_model_contract
#print axioms null_posterior_not_probability
#print axioms independent_tail_contract
end IndependentResidualSeedReview
