import BlockKernel
import CanonicalBlockPolicy

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Θ B A Y : Type*} [Fintype Θ] [Fintype B] [DecidableEq Θ]

/-- One fixed shared maximum-likelihood decision rule on the actual recorded history. -/
def treeMLE (K : Θ → Θ → B → ℝ) (initial : Θ) (h : List (Θ × B)) : Θ := by
  classical
  exact greedyMax (fun σ => historyMass K σ h) initial Finset.univ.toList

omit [Fintype B] [DecidableEq Θ] in
lemma treeMLE_maximizes (K : Θ → Θ → B → ℝ) (initial θ : Θ) (h : List (Θ × B)) :
    historyMass K θ h ≤ historyMass K (treeMLE K initial h) h := by
  classical
  simpa only [treeMLE] using
    (greedyMax_ge (fun σ => historyMass K σ h) initial Finset.univ.toList θ (Or.inr (by simp)))

theorem treeMLE_expected_selections_bound (K : Θ → Θ → B → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y) (hNorm : ∀ θ a, ∑ y, K θ a y = 1)
    (θ σ initial : Θ) (hne : K θ σ ≠ K σ σ) (n : ℕ) :
    selectedCost K θ σ (treeMLE K initial) n [] ≤
      1 / (1-affinity (K θ σ) (K σ σ)) := by
  classical
  apply selectedCost_uniform_bound K hK hNorm θ σ (treeMLE K initial) ?_ hne n
  intro h heq
  have hm := treeMLE_maximizes K initial θ h
  simpa only [heq] using hm

lemma affinity_self_one (p : B → ℝ) (hp : ∀ y, 0 ≤ p y) (hs : ∑ y, p y = 1) :
    affinity p p = 1 := by
  unfold affinity
  simpa only [Real.mul_self_sqrt, hp] using hs

section Block
variable [Fintype A] [Fintype Y] [DecidableEq A]

/-- Exact conditional law of the action-support block selected by candidate σ. -/
def supportBlockKernel (P : Θ → A → Y → ℝ) (support : Θ → Finset A) (filler : Y)
    (θ σ : Θ) : (A → Y) → ℝ := blockMass (P θ) (support σ) filler

/-- A concrete finite-horizon expected harmful-block bound from raw action laws
and self-verifying target supports. The denominator is strictly positive. -/
theorem supportBlock_expected_selections_bound (P : Θ → A → Y → ℝ)
    (good support : Θ → Finset A) (filler : Y)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hNorm : ∀ θ a, ∑ y, P θ a y = 1)
    (hsupport : ∀ σ, SelfVerifying good (fun η ζ a => P η a = P ζ a) σ (support σ))
    (θ σ initial : Θ) (hbad : ¬ support σ ⊆ good θ) (n : ℕ) :
    let ρ := ∏ a ∈ support σ, affinity (P θ a) (P σ a)
    0 < 1-ρ ∧
      selectedCost (supportBlockKernel P support filler) θ σ
        (treeMLE (supportBlockKernel P support filler) initial) n [] ≤ 1/(1-ρ) := by
  classical
  have hinfo : ∃ a ∈ support σ, P θ a ≠ P σ a := by
    by_contra! h
    apply hbad
    apply (hsupport σ).2 θ
    intro a ha
    exact (h a ha).symm
  have hlt := blockMass_affinity_lt_one (P θ) (P σ) (support σ) filler
    (hP θ) (hP σ) (hNorm θ) (hNorm σ) hinfo
  have heq := blockMass_affinity (P θ) (P σ) (support σ) filler (hP θ) (hP σ)
  have hneq : supportBlockKernel P support filler θ σ ≠
      supportBlockKernel P support filler σ σ := by
    intro hk
    have hone := affinity_self_one (supportBlockKernel P support filler σ σ)
      (blockMass_nonneg _ _ _ (hP σ)) (blockMass_normalized _ _ _ (hNorm σ))
    change affinity (supportBlockKernel P support filler θ σ)
      (supportBlockKernel P support filler σ σ) < 1 at hlt
    rw [hk, hone] at hlt
    exact (lt_irrefl _ hlt)
  have hb := treeMLE_expected_selections_bound (supportBlockKernel P support filler)
    (fun η ζ w => blockMass_nonneg _ _ _ (hP η) w)
    (fun η ζ => blockMass_normalized _ _ _ (hNorm η)) θ σ initial hneq n
  change _ ∧ _
  constructor
  · rw [← heq]
    exact sub_pos.mpr hlt
  · simpa only [supportBlockKernel, heq] using hb

end Block
end Orthemology.Tranche2
