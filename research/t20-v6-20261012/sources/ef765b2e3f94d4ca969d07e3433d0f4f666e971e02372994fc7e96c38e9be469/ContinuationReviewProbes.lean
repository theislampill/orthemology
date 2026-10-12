import ConditionalKilledContinuation

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation HiddenParity.Stochastic
namespace IndependentContinuationReview
universe u v
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Expand the conditioning as a function of the original observed law, before
identifying it with the fresh restart. No conditional-law premise is supplied. -/
theorem observable_conditioned_law_is_restart
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hp : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) :
    ((observedTraceLaw ∅ π ρ P P hP hN hP hN {H | H h.length = h})⁻¹ •
      (observedTraceLaw ∅ π ρ P P hP hN hP hN).restrict {H | H h.length = h}).map
      (fun H n => (H (h.length+n)).take n) =
    observedTraceLaw ∅ (fun r tail => π r (tail ++ h))
      ((ρ (CompatibleSeeds π h))⁻¹ • ρ.restrict (CompatibleSeeds π h)) P P hP hN hP hN := by
  change (normalizedRestriction (observedTraceLaw ∅ π ρ P P hP hN hP hN)
    {H | H h.length = h}).map (continuationReadout h) = _
  rw [← conditionalContinuationLaw_eq_conditioned_observation π hπ ρ P hP hN h]
  exact conditionalContinuationLaw_eq_restart π hπ ρ P hP hN h hp

theorem null_prefix_gives_zero
    (π : R → History A Y → A) (ρ : Measure R)
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hz : CanonicalInput ρ P hP hN (PrefixEvent π h) = 0) :
    conditionalContinuationLaw π ρ P hP hN h = 0 := by
  have hr : (CanonicalInput ρ P hP hN).restrict (PrefixEvent π h) = 0 :=
    Measure.restrict_eq_zero.mpr hz
  simp [conditionalContinuationLaw, normalizedRestriction, hr]

theorem invalid_continuation_length_has_zero_mass
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h tail : History A Y)
    (hp : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) (n : ℕ)
    (hn : n ≠ tail.length) :
    ((conditionalContinuationLaw π ρ P hP hN h).map (fun H => H n)) {tail} = 0 := by
  rw [conditional_continuation_marginal π hπ ρ P hP hN h hp, if_neg hn]

abbrev Bit := Fin 2

def policy (r : Bit) : History Bit Bit → Bit
 | [] => r
 | (_,y) :: _ => y

def old : History (Bit × Bit) Bit := [((1,1),0),((1,1),1)]
def oracle (n : Nat) (_ : Bit × Bit) : Bit := if n=1 then 0 else 1
def sample : Input Bit (Bit × Bit) Bit := (1, ((fun _ => 0),oracle))
def observed := historyTrajectory ∅ (pairPolicy (1:Bit) policy) sample
def continued := continuationHistory (pairPolicy (1:Bit) policy) old sample

theorem actual_two_step_prefix : sample ∈ PrefixEvent (pairPolicy (1:Bit) policy) old := by
  change observed old.length = old
  decide

theorem restart_imposes_latest_state :
    pairPolicy (currentState (1:Bit) old) (restartPolicy policy (erasePairSources old)) 1 [] = (0,0) ∧
    pairPolicy (1:Bit) (restartPolicy policy (erasePairSources old)) 1 [] = (1,0) := by decide

theorem actual_removed_prefix_and_reconstruction :
    continued 1 = [((0,0),1)] ∧ observed 3 = continued 1 ++ old := by decide

/-- The old prefix can be outside the retained tail set. The first outside
continuation pair is hidden at its acquisition time; the earlier history remains
present at its own earlier path coordinate. -/
theorem tail_killing_uses_only_postprefix_pairs :
    (killedHistory ({(0,0)} : Finset (Bit × Bit)) (0,0) continued 1) =
      (true,[((0,0),1)]) ∧
    (killedHistory ({(0,0)} : Finset (Bit × Bit)) (0,0) continued 2) = (false,[]) ∧
    (killedHistory ({(0,0)} : Finset (Bit × Bit)) (0,0) observed 1) = (false,[]) := by decide

set_option pp.explicit true in
#check @conditionalContinuationLaw_eq_restart
set_option pp.explicit true in
#check @conditional_markov_surviving_recurrent_eq
#print axioms observable_conditioned_law_is_restart
#print axioms null_prefix_gives_zero
#print axioms invalid_continuation_length_has_zero_mass
#print axioms actual_two_step_prefix
#print axioms restart_imposes_latest_state
#print axioms actual_removed_prefix_and_reconstruction
#print axioms tail_killing_uses_only_postprefix_pairs
end IndependentContinuationReview
