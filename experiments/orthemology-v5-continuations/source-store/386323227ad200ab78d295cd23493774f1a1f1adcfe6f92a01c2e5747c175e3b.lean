import LiveSourceCertificate

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Phase Θ A Y : Type*} [Fintype Phase] [Fintype Θ] [Fintype Y]
    [DecidableEq Θ] [DecidableEq A]

omit [DecidableEq Θ] in
/-- Finite-horizon source-linked theorem for a live-model, interruptible,
equal-weight-reset controller. The true model appears only in the proof's costs
and bound, never in the policy. `next` is the public phase update; its strict
rank decrease is an explicit finite-state certificate. -/
theorem live_stopped_controller_budget
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (live : Phase → Finset Θ) (acts : Phase → Θ → List A)
    (stay : Phase → A → Y → Bool) (initial : Phase → Θ)
    (next : (p : Phase) → (σ : Θ) → StopObs Y (acts p σ).length → Phase)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hNorm : ∀ θ a, ∑ y, P θ a y = 1)
    (hInitial : ∀ p, initial p ∈ live p)
    (hcert : ∀ p σ, σ ∈ live p →
      (∃ a ∈ acts p σ, ∃ y, stay p a y = false ∧ 0 < P σ a y) ∨
      LiveSelfVerifying P good (live p) σ (acts p σ))
    (θ : Θ) (hθ : ∀ p, θ ∈ live p)
    (cost : Phase → Θ → ℝ) (hcost : ∀ p σ, 0 ≤ cost p σ)
    (hcostBad : ∀ p σ, 0 < cost p σ → σ ∈ live p ∧ ¬ (acts p σ).toFinset ⊆ good θ)
    (rank : Phase → ℕ)
    (hRank : ∀ p σ y, stopCompleted y = false →
      0 < stoppedFullKernel P (acts p) (stay p) θ σ y → rank (next p σ y) < rank p)
    (n : ℕ) (p : Phase) :
    let K := fun p => stoppedFullKernel P (acts p) (stay p)
    let keep := fun p (σ : Θ) (y : StopObs Y (acts p σ).length) => stopCompleted y
    let π := fun p => liveTreeMLE (Obs := fun p σ => StopObs Y (acts p σ).length) (p := p) (continuingKernel K keep p) (live p) (initial p)
    let ρ := fun p σ => survivalAffinity (P θ) (P σ) (stay p) (acts p σ)
    let w := fun p σ => if 0 < cost p σ then cost p σ / (1-ρ p σ) else 0
    (∀ q h, π q h ∈ live q) ∧
    resetCost K keep next π cost θ n p [] ≤
      ((rank p : ℝ)+1) * (∑ q, ∑ σ, w q σ) := by
  classical
  dsimp only
  let K := fun p => stoppedFullKernel P (acts p) (stay p)
  let keep := fun p (σ : Θ) (y : StopObs Y (acts p σ).length) => stopCompleted y
  let π := fun p => liveTreeMLE (Obs := fun p σ => StopObs Y (acts p σ).length) (p := p) (continuingKernel K keep p) (live p) (initial p)
  let ρ := fun p σ => survivalAffinity (P θ) (P σ) (stay p) (acts p σ)
  let w := fun p σ => if 0 < cost p σ then cost p σ / (1-ρ p σ) else 0
  have hkilled : ∀ p, continuingKernel K keep p = stoppedPhaseKernel P (acts p) (stay p) := by
    intro p
    rfl
  have hDef : ∀ p σ, 0 < cost p σ → ρ p σ < 1 := by
    intro p σ hp
    obtain ⟨hl, hb⟩ := hcostBad p σ hp
    exact sub_pos.mp (live_certificate_implies_strict_residual P good (stay p) (live p)
      hP hNorm θ σ (hθ p) (acts p σ) (hcert p σ hl) hb)
  have hw : ∀ p σ, 0 ≤ w p σ := fun p σ =>
    (deficit_weight_certificate (ρ p) (cost p) (hcost p) (hDef p) σ).1
  have hWeight : ∀ p h, cost p (π p h) ≤ w p (π p h) *
      (1-affinity (continuingKernel K keep p θ (π p h))
        (continuingKernel K keep p (π p h) (π p h))) := by
    intro p h
    rw [hkilled p, stoppedPhaseKernel_affinity]
    exact (deficit_weight_certificate (ρ p) (cost p) (hcost p) (hDef p) (π p h)).2
  constructor
  · intro q h
    exact greedyMax_live_mem _ (live q) (initial q) (hInitial q)
  apply reset_hellinger_budget (Obs := fun p σ => StopObs Y (acts p σ).length) K keep next π cost w θ
  · exact fun p η σ y => stoppedMass_nonneg (P η) (stay p) (hP η) (acts p σ) y
  · exact fun p η σ => stoppedMass_normalized (P η) (stay p) (hNorm η) (acts p σ)
  · exact hRank
  · exact hw
  · intro p h
    exact liveTreeMLE_maximizes (Obs := fun p σ => StopObs Y (acts p σ).length) (p := p) _ (live p) (initial p) θ (hθ p) h
  · exact hWeight
  · exact Finset.sum_nonneg (fun p _ => Finset.sum_nonneg (fun σ _ => hw p σ))
  · intro p
    exact Finset.single_le_sum (fun q _ => Finset.sum_nonneg (fun σ _ => hw q σ)) (Finset.mem_univ p)

end Orthemology.Tranche2
