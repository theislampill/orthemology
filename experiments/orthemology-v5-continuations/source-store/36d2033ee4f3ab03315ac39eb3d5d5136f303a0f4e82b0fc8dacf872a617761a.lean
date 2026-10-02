import GuardedLiveController
import StoppedActionCost
import TrajectoryBudget

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped BigOperators ENNReal
open Finset

namespace Orthemology.Tranche2
variable {Phase Θ A Y : Type*} [Fintype Phase] [Fintype Θ] [Fintype Y]
    [DecidableEq Θ] [DecidableEq A]

/-- Actual generated infinite-path theorem: finite source certificates, raw
normalized action laws, a shared interruptible controller, and almost-sure
eventual target-good planned blocks. There is no caller-supplied cylinder-law,
independence, likelihood-convergence or expected-error premise. -/
theorem generated_live_controller_eventually_good
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (live : Phase → Finset Θ) (acts : Phase → Θ → List A)
    (stay : Phase → A → Y → Bool) (initial : Phase → Θ)
    (next : (p : Phase) → (σ : Θ) → StopObs Y (acts p σ).length → Phase)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hNorm : ∀ θ a, ∑ y, P θ a y = 1)
    (hInitial : ∀ p, initial p ∈ live p)
    (hcert : ∀ p σ, σ ∈ live p →
      (∃ a ∈ acts p σ, ∃ y, stay p a y = false ∧ 0 < P σ a y) ∨
      LiveSelfVerifying P good (live p) σ (acts p σ))
    (θ : Θ)
    (rank : Phase → ℕ)
    (hNext : ∀ p σ y, θ ∈ live p → stopCompleted y = false →
      0 < stoppedFullKernel P (acts p) (stay p) θ σ y → θ ∈ live (next p σ y))
    (hRank : ∀ p σ y, θ ∈ live p → stopCompleted y = false →
      0 < stoppedFullKernel P (acts p) (stay p) θ σ y → rank (next p σ y) < rank p)
    (p : Phase) (hθ : θ ∈ live p) :
    let K := fun p => stoppedFullKernel P (acts p) (stay p)
    let keep := fun p (σ : Θ) (y : StopObs Y (acts p σ).length) => stopCompleted y
    let π := fun p => liveTreeMLE (Obs := fun p σ => StopObs Y (acts p σ).length) (p := p)
      (continuingKernel K keep p) (live p) (initial p)
    let hK := fun p η σ y => stoppedMass_nonneg (P η) (stay p) (hP η) (acts p σ) y
    let hN := fun p η σ => stoppedMass_normalized (P η) (stay p) (hNorm η) (acts p σ)
    let μ := markovTrajectory (resetTransitionKernel K keep next π hK hN θ) ⟨p,[]⟩
    ∀ᵐ x ∂μ, ∀ᶠ n in Filter.atTop,
      (acts (x n).1 (π (x n).1 (x n).2)).toFinset ⊆ good θ := by
  classical
  dsimp only
  let K := fun p => stoppedFullKernel P (acts p) (stay p)
  let keep := fun p (σ : Θ) (y : StopObs Y (acts p σ).length) => stopCompleted y
  let π := fun p => liveTreeMLE (Obs := fun p σ => StopObs Y (acts p σ).length) (p := p)
    (continuingKernel K keep p) (live p) (initial p)
  let hK := fun p η σ y => stoppedMass_nonneg (P η) (stay p) (hP η) (acts p σ) y
  let hN := fun p η σ => stoppedMass_normalized (P η) (stay p) (hNorm η) (acts p σ)
  let μ := markovTrajectory (resetTransitionKernel K keep next π hK hN θ) ⟨p,[]⟩
  let c := fun p σ => if σ ∈ live p then plannedBadCount (good θ) (acts p σ) else 0
  let cost := fun p σ => (c p σ : ℝ)
  let ρ := fun p σ => survivalAffinity (P θ) (P σ) (stay p) (acts p σ)
  let w := fun p σ => if θ ∈ live p ∧ 0 < cost p σ then cost p σ / (1-ρ p σ) else 0
  let C := ((rank p : ℝ)+1) * (∑ q, ∑ σ, w q σ)
  have hcost : ∀ p σ, 0 ≤ cost p σ := fun p σ => Nat.cast_nonneg _
  have hcostBad : ∀ p σ, 0 < cost p σ → σ ∈ live p ∧ ¬ (acts p σ).toFinset ⊆ good θ := by
    intro p σ hp
    dsimp [cost, c] at hp
    split_ifs at hp with hl
    · refine ⟨hl, (plannedBadCount_pos_iff (good θ) (acts p σ)).mp ?_⟩
      exact_mod_cast hp
    · norm_num at hp
  have hbound : ∀ n, resetCost K keep next π cost θ n p [] ≤ C := by
    intro n
    exact (guarded_live_stopped_controller_budget P good live acts stay initial next hP hNorm
      hInitial hcert θ cost hcost hcostBad rank hNext hRank n p hθ).2
  have hFinite : ∀ n, (∫⁻ x, pathCharge (fun s => (c s.1 (π s.1 s.2) : ℝ≥0∞)) 0 n x ∂μ) ≤
      ENNReal.ofReal C := by
    intro n
    have he := trajectory_expected_charge_eq_resetCost K keep next π cost hK hN hcost θ n p
    have hb := ENNReal.ofReal_le_ofReal (hbound n)
    rw [← he] at hb
    simpa only [cost, ENNReal.ofReal_natCast] using hb
  have ha := (trajectory_nat_charge_eventually_zero μ (fun s => c s.1 (π s.1 s.2)) C hFinite).2
  filter_upwards [ha] with x hx
  filter_upwards [hx] with n hn
  have hl : π (x n).1 (x n).2 ∈ live (x n).1 :=
    greedyMax_live_mem _ _ _ (hInitial (x n).1)
  have hz : plannedBadCount (good θ) (acts (x n).1 (π (x n).1 (x n).2)) = 0 := by
    simpa only [c, hl, ↓reduceIte] using hn
  by_contra hb
  have hp := (plannedBadCount_pos_iff (good θ) (acts (x n).1 (π (x n).1 (x n).2))).mpr hb
  rw [hz] at hp
  exact Nat.lt_irrefl 0 hp

end Orthemology.Tranche2
