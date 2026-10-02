import RecursivePhaseExtraction
import StoppedActionCost

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {Θ A Y : Type*} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

def recursiveFullKernel (p : WinningPhase P good menu) :=
  stoppedFullKernel P (phaseActs P good menu p) (supportStay P p.val)

def recursiveKeep (p : WinningPhase P good menu) (σ : Θ)
    (w : StopObs Y (phaseActs P good menu p σ).length) : Bool := stopCompleted w

def recursivePolicy (p : WinningPhase P good menu) :=
  liveTreeMLE (Obs := fun p σ => StopObs Y (phaseActs P good menu p σ).length) (p := p)
    (continuingKernel (recursiveFullKernel P good menu) (recursiveKeep P good menu) p)
    p.val (phaseInitial P good menu p)

omit [Fintype Y] in
omit [Fintype Θ] in
lemma recursiveFull_nonneg (hP : ∀ θ a y, 0 ≤ P θ a y) :
    ∀ p η σ y, 0 ≤ recursiveFullKernel P good menu p η σ y := fun p η σ y =>
  stoppedMass_nonneg (P η) (supportStay P p.val) (hP η) (phaseActs P good menu p σ) y

omit [Fintype Θ] in
lemma recursiveFull_normalized (hN : ∀ θ a, ∑ y, P θ a y = 1) :
    ∀ p η σ, ∑ y, recursiveFullKernel P good menu p η σ y = 1 := fun p η σ =>
  stoppedMass_normalized (P η) (supportStay P p.val) (hN η) (phaseActs P good menu p σ)

omit [Fintype Y] in
omit [Fintype Θ] in
/-- Every output plan is nonempty and licensed by the actual support menu,
including plans for candidates never selected outside the current live set. -/
theorem recursive_plans_nonempty_licensed (p : WinningPhase P good menu) (σ : Θ) :
    phaseActs P good menu p σ ≠ [] ∧ (phaseActs P good menu p σ).toFinset ⊆ menu p.val :=
  ⟨(phaseActs_spec P good menu p σ).1,(phaseActs_spec P good menu p σ).2.1⟩

def recursiveLaw (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) :=
  markovTrajectory (resetTransitionKernel (recursiveFullKernel P good menu) (recursiveKeep P good menu)
    (phaseNext P good menu) (recursivePolicy P good menu)
    (recursiveFull_nonneg P good menu hP) (recursiveFull_normalized P good menu hN) θ) ⟨p,[]⟩

set_option maxHeartbeats 800000 in
/-- Recursive combinatorial success generates the actual shared infinite
controller. Public menu licensing and nonempty blocks are derived above. -/
theorem recursive_generated_eventually_good
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) :
    ∀ᵐ x ∂recursiveLaw P good menu hP hN θ p, ∀ᶠ n in atTop,
      (phaseActs P good menu (x n).1 (recursivePolicy P good menu (x n).1 (x n).2)).toFinset ⊆ good θ := by
  exact generated_live_controller_eventually_good (Phase := WinningPhase P good menu) P good (fun p => p.val) (phaseActs P good menu)
    (fun p => supportStay P p.val) (phaseInitial P good menu) (phaseNext P good menu) hP hN
    (phaseInitial_mem P good menu) (phaseActs_certificate P good menu) θ (phaseRank P good menu)
    (fun p σ w hθ hw hp => (phaseNext_actual_support P good menu hP θ p σ w hθ hw hp).2.1)
    (phaseNext_rank_decreases P good menu hP θ) p hθ

def recursiveBadCharge (θ : Θ) (p : WinningPhase P good menu) (σ : Θ) : ℕ :=
  if σ ∈ p.val then plannedBadCount (good θ) (phaseActs P good menu p σ) else 0

/-- A finite expected-charge budget follows from the recursive certificate;
no caller supplies progress, rank, retention or cost-drift hypotheses. -/
theorem recursive_finite_budget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) :
    ∃ C : ℝ, ∀ n,
      resetCost (recursiveFullKernel P good menu) (recursiveKeep P good menu)
        (phaseNext P good menu) (recursivePolicy P good menu)
        (fun q σ => (recursiveBadCharge P good menu θ q σ : ℝ)) θ n p [] ≤ C := by
  classical
  let cost := fun q σ => (recursiveBadCharge P good menu θ q σ : ℝ)
  let ρ := fun q σ => survivalAffinity (P θ) (P σ) (supportStay P q.val) (phaseActs P good menu q σ)
  let w := fun q σ => if θ ∈ q.val ∧ 0 < cost q σ then cost q σ / (1-ρ q σ) else 0
  refine ⟨((phaseRank P good menu p : ℝ)+1) * (∑ q, ∑ σ, w q σ), ?_⟩
  intro n
  have hc : ∀ q σ, 0 ≤ cost q σ := fun q σ => Nat.cast_nonneg _
  have hbad : ∀ q σ, 0 < cost q σ → σ ∈ q.val ∧ ¬ (phaseActs P good menu q σ).toFinset ⊆ good θ := by
    intro q σ hp
    dsimp [cost,recursiveBadCharge] at hp
    split_ifs at hp with hs
    · exact ⟨hs,(plannedBadCount_pos_iff _ _).mp (by exact_mod_cast hp)⟩
    · norm_num at hp
  exact (guarded_live_stopped_controller_budget P good (fun q => q.val) (phaseActs P good menu)
    (fun q => supportStay P q.val) (phaseInitial P good menu) (phaseNext P good menu) hP hN
    (phaseInitial_mem P good menu) (phaseActs_certificate P good menu) θ cost hc hbad (phaseRank P good menu)
    (fun q σ w hθ hw hp => (phaseNext_actual_support P good menu hP θ q σ w hθ hw hp).2.1)
    (phaseNext_rank_decreases P good menu hP θ) n p hθ).2

end Orthemology.Tranche2
