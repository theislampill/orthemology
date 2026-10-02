import MicroPhysical
import HistoryLikelihood

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators
namespace Orthemology.Tranche2.MicroPolicy
open PolicyEmbedding
variable {Θ A Y Ω : Type*} [Fintype Θ] [Fintype A] [DecidableEq A]

def chooseMLE (P : Θ → A → Y → ℝ) (initial : Θ) (h : History A Y) : Θ :=
  greedyMax (fun σ => historyScore (P σ) h) initial Finset.univ.toList

omit [Fintype A] [DecidableEq A] in
lemma chooseMLE_maximizes (P : Θ → A → Y → ℝ) (initial : Θ) (h : History A Y) (σ : Θ) :
    historyScore (P σ) h ≤ historyScore (P (chooseMLE P initial h)) h := by
  classical
  simpa only [chooseMLE] using
    greedyMax_ge (fun η => historyScore (P η) h) initial Finset.univ.toList σ
      (Or.inr (by simp))

def supportPlan (support : Θ → Finset A) (σ : Θ) : List A := (support σ).toList

omit [Fintype Θ] [Fintype A] [DecidableEq A] in
lemma supportPlan_nonempty (support : Θ → Finset A) (hne : ∀ σ, (support σ).Nonempty) :
    ∀ σ, supportPlan support σ ≠ [] := by
  intro σ
  obtain ⟨a,ha⟩ := hne σ
  intro he
  have : a ∈ supportPlan support σ := by simpa [supportPlan] using ha
  rw [he] at this
  exact List.not_mem_nil this

omit [Fintype Θ] [Fintype A] in
lemma macro_count (support : Θ → Finset A) (choose : History A Y → Θ)
    (X : A → ℕ → Y) (n : ℕ) (a : A) :
    actionCount a (macroHistory (supportPlan support) choose X n) =
      blockCount support (macroSelected (supportPlan support) choose X) a n := by
  classical
  induction n with
  | zero => simp [macroHistory,blockCount,Nat.count]
  | succ n ih =>
    change actionCount a (feed X _ ((support _).toList)) = _
    rw [feed_count_finset,ih]
    simp only [blockCount,Nat.count_succ,macroSelected]
    by_cases ha : a ∈ support (choose (macroHistory (supportPlan support) choose X n))
    · simp [ha,macroSelected]
    · simp [ha,macroSelected]

omit [Fintype Θ] in
lemma macro_score (p : A → Y → ℝ) (plan : Θ → List A) (choose : History A Y → Θ)
    (X : A → ℕ → Ω → Y) (ω : Ω) (n : ℕ) :
    historyScore p (macroHistory plan choose (fun a i => X a i ω) n) =
      prefixLikelihood p X (fun a => actionCount a
        (macroHistory plan choose (fun a i => X a i ω) n)) ω := by
  induction n with
  | zero => simp [macroHistory,prefixLikelihood]
  | succ n ih => exact historyScore_feed p X _ ω _ ih

/-- The history-only selector supplies the exact stochastic block-controller
MLE inequality, with the actual acquired observation counters. -/
theorem micro_macro_maximizes (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (initial : Θ) (X : A → ℕ → Ω → Y) (ω : Ω) (n : ℕ) (σ : Θ) :
    prefixLikelihood (P σ) X (fun a => blockCount support
      (macroSelected (supportPlan support) (chooseMLE P initial) (fun a i => X a i ω)) a n) ω ≤
    prefixLikelihood (P (macroSelected (supportPlan support) (chooseMLE P initial)
      (fun a i => X a i ω) n)) X (fun a => blockCount support
        (macroSelected (supportPlan support) (chooseMLE P initial) (fun a i => X a i ω)) a n) ω := by
  simp_rw [← macro_count support (chooseMLE P initial) (fun a i => X a i ω) n]
  rw [← macro_score (P σ),← macro_score]
  exact chooseMLE_maximizes P initial _ σ

section Probability
variable [Fintype Y] [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]
/-- An actual micro-policy sequence is eventually good under the declared
independent action-stack experiment. Its history replay is explicit. -/
theorem micro_policy_stack_eventually_good
    (P : Θ → A → Y → ℝ) (good support : Θ → Finset A) (θ initial : Θ) (d : A)
    (X : A → ℕ → Ω → Y)
    (hP : ∀ σ a y, 0 < P σ a y) (hPsum : ∀ σ a, ∑ y, P σ a y = 1)
    (hne : ∀ σ, (support σ).Nonempty)
    (hsv : ∀ σ, SelfVerifying good (fun η ζ a => P η a = P ζ a) σ (support σ))
    (hX : ∀ a n, Measurable (X a n))
    (hindep : iIndepFun (fun an : A × ℕ => X an.1 an.2) μ)
    (hident : ∀ a n, IdentDistrib (X a n) (X a 0) μ μ)
    (hLaw : ∀ a y, (Measure.map (X a 0) μ).real {y} = P θ a y) :
    ∀ᵐ ω ∂μ, ∀ᶠ t in atTop,
      policy (supportPlan support) (chooseMLE P initial) d ()
        (microRun (supportPlan support) (chooseMLE P initial) d
          (fun a i => X a i ω) [] t) ∈ good θ := by
  have hb := likelihood_block_controller_eventually_good P good support θ X
    (fun ω => macroSelected (supportPlan support) (chooseMLE P initial) (fun a i => X a i ω))
    hP hPsum hne hsv hX hindep hident hLaw (micro_macro_maximizes P support initial X)
  filter_upwards [hb] with ω hω
  apply micro_eventually_good _ _ d (supportPlan_nonempty support hne) _ (fun a => a ∈ good θ)
  filter_upwards [hω] with n hn a ha
  apply hn.2
  simpa [macroBlocks,supportPlan] using ha
end Probability
end Orthemology.Tranche2.MicroPolicy
