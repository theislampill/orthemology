import MicroLikelihood
import StackActionLaw
import SeededPolicyNecessity

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators
namespace Orthemology.Tranche2.MicroPolicy
open PolicyEmbedding
universe u v w
variable {R : Type v} {A Y : Type u} {Θ : Type w}
    [Fintype Θ] [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- One shared physical-time policy. Its only input is the acquired history;
private randomness is permitted by the interface but is not needed. -/
def sharedPolicy (P : Θ → A → Y → ℝ) (support : Θ → Finset A) (initial : Θ) (d : A)
    (_ : R) (h : History A Y) : A := policy (supportPlan support) (chooseMLE P initial) d () h

omit [Inhabited Y] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma sharedPolicy_measurable (P : Θ → A → Y → ℝ) (support : Θ → Finset A) (initial : Θ) (d : A) :
    Measurable (fun z : R × History A Y => sharedPolicy P support initial d z.1 z.2) := by
  exact (measurable_of_countable (fun h => policy (supportPlan support) (chooseMLE P initial) d () h)).comp
    measurable_snd

omit [Fintype Y] [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma shared_history_eq_micro (P : Θ → A → Y → ℝ) (support : Θ → Finset A) (initial : Θ) (d : A)
    (X : A → ℕ → Y) (oracle : ℕ → A → Y) (r : R) (n : ℕ) :
    observedHistory Finset.univ (sharedPolicy P support initial d) oracle r X n =
      microRun (supportPlan support) (chooseMLE P initial) d X [] n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [observedHistory,microRun,ih,sharedPolicy,feedback]

/-- End-to-end sufficiency in the exact canonical causal action law used by
necessity: the queue, likelihood choice, feedback experiment and action clock
are all constructed, for arbitrary nonempty finite multi-action supports. -/
theorem shared_policy_actionLaw_eventually_good
    (P : Θ → A → Y → ℝ) (good support : Θ → Finset A) (θ initial : Θ) (d : A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (hP : ∀ σ a y, 0 < P σ a y) (hN : ∀ σ a, ∑ y, P σ a y = 1)
    (hne : ∀ σ, (support σ).Nonempty)
    (hsv : ∀ σ, SelfVerifying good (fun η ζ a => P η a = P ζ a) σ (support σ)) :
    ∀ᵐ x ∂actionLaw (sharedPolicy P support initial d) ρ (P θ)
      (fun a y => (hP θ a y).le) (hN θ) d, ∀ᶠ t in atTop, x t ∈ good θ := by
  apply actionLaw_eventually_good_of_stack _ (sharedPolicy_measurable P support initial d)
    ρ (P θ) (fun a y => (hP θ a y).le) (hN θ) d (good θ)
  have hb := micro_policy_stack_eventually_good P good support θ initial d
    (seededStackCoordinate (R := R)) hP hN hne hsv
    seededStackCoordinate_measurable
    (seededStackCoordinates_independent ρ (P θ) (fun a y => (hP θ a y).le) (hN θ))
    (fun a n => seededStackCoordinates_identDistrib ρ (P θ) (fun a y => (hP θ a y).le) (hN θ) a n 0)
    (fun a y => seededStackCoordinate_real_singleton ρ (P θ) (fun a y => (hP θ a y).le) (hN θ) a 0 y)
  filter_upwards [hb] with z hz
  simpa only [stackActionTrajectory,stackHistoryTrajectory,shared_history_eq_micro,sharedPolicy,
    seededStackCoordinate] using hz

/-- Exact full-support CIRS existence iff in one declared seeded-history policy
and action-law interface. No policy realization or transfer premise remains. -/
theorem seeded_policy_exists_iff_self_verifying
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (initial : Θ) (d : A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (hP : ∀ σ a y, 0 < P σ a y) (hN : ∀ σ a, ∑ y, P σ a y = 1) :
    (∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      ∀ θ, ∀ᵐ x ∂actionLaw π ρ (P θ) (fun a y => (hP θ a y).le) (hN θ) d,
        ∀ᶠ t in atTop, x t ∈ good θ) ↔
      ∀ θ, ∃ U : Finset A, U.Nonempty ∧
        SelfVerifying good (fun η ζ a => P η a = P ζ a) θ U := by
  constructor
  · rintro ⟨π,hπ,hgood⟩ θ
    exact seeded_policy_self_verifying_necessity P good hP hN π hπ ρ d hgood θ
  · intro hs
    choose support hne hsv using hs
    refine ⟨sharedPolicy P support initial d,sharedPolicy_measurable P support initial d,?_⟩
    intro θ
    exact shared_policy_actionLaw_eventually_good P good support θ initial d ρ hP hN hne hsv

/-- Equivalent greatest-support-kernel characterization, with the same literal
physical policy class on the left. The real-data comparison remains classical. -/
theorem seeded_policy_exists_iff_kernel_nonempty
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (initial : Θ) (d : A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (hP : ∀ σ a y, 0 < P σ a y) (hN : ∀ σ a, ∑ y, P σ a y = 1) :
    (∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      ∀ θ, ∀ᵐ x ∂actionLaw π ρ (P θ) (fun a y => (hP θ a y).le) (hN θ) d,
        ∀ᶠ t in atTop, x t ∈ good θ) ↔
      ∀ θ, (supportKernel good (fun η ζ a => P η a = P ζ a) θ).Nonempty := by
  rw [seeded_policy_exists_iff_self_verifying P good initial d ρ hP hN]
  exact forall_congr' (fun θ => (supportKernel_nonempty_iff good _ θ).symm)

end Orthemology.Tranche2.MicroPolicy
