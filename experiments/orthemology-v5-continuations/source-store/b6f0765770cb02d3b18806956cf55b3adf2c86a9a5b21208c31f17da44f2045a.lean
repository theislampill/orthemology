import DependentHellinger
import ResidualDeficit
import CanonicalBlockPolicy

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Θ : Type*} {B : Θ → Type*} [Fintype Θ] [∀ a, Fintype (B a)] [DecidableEq Θ]

def dependentTreeMLE (K : (θ a : Θ) → B a → ℝ) (initial : Θ) (h : List (Sigma B)) : Θ := by
  classical
  exact greedyMax (fun σ => dHistoryMass K σ h) initial Finset.univ.toList

omit [(a : Θ) → Fintype (B a)] [DecidableEq Θ] in
lemma dependentTreeMLE_maximizes (K : (θ a : Θ) → B a → ℝ)
    (initial θ : Θ) (h : List (Sigma B)) :
    dHistoryMass K θ h ≤ dHistoryMass K (dependentTreeMLE K initial h) h := by
  classical
  simpa only [dependentTreeMLE] using
    (greedyMax_ge (fun σ => dHistoryMass K σ h) initial Finset.univ.toList θ (Or.inr (by simp)))

section Stopped
variable {A Y : Type*} [Fintype Y] [DecidableEq A]

def stoppedFullKernel (P : Θ → A → Y → ℝ) (acts : Θ → List A) (stay : A → Y → Bool)
    (θ σ : Θ) : StopObs Y (acts σ).length → ℝ := stoppedMass (P θ) stay (acts σ)

def stoppedPhaseKernel (P : Θ → A → Y → ℝ) (acts : Θ → List A) (stay : A → Y → Bool)
    (θ σ : Θ) : StopObs Y (acts σ).length → ℝ :=
  killedLaw (stoppedMass (P θ) stay (acts σ)) stopCompleted

omit [Fintype Θ] [DecidableEq Θ] [Fintype Y] [DecidableEq A] in
theorem stoppedPhaseKernel_nonneg (P : Θ → A → Y → ℝ) (acts : Θ → List A)
    (stay : A → Y → Bool) (hP : ∀ θ a y, 0 ≤ P θ a y) :
    ∀ θ σ w, 0 ≤ stoppedPhaseKernel P acts stay θ σ w := by
  intro θ σ w
  exact killedLaw_nonneg _ _ (stoppedMass_nonneg (P θ) stay (hP θ) (acts σ)) w

omit [Fintype Θ] [DecidableEq Θ] [DecidableEq A] in
theorem stoppedPhaseKernel_subprob (P : Θ → A → Y → ℝ) (acts : Θ → List A)
    (stay : A → Y → Bool) (hP : ∀ θ a y, 0 ≤ P θ a y)
    (hNorm : ∀ θ a, ∑ y, P θ a y = 1) :
    ∀ θ σ, ∑ w, stoppedPhaseKernel P acts stay θ σ w ≤ 1 := by
  intro θ σ
  exact survivalMass_le_one (P θ) stay (hP θ) (hNorm θ) (acts σ)

omit [Fintype Θ] [DecidableEq Θ] [DecidableEq A] in
theorem stoppedPhaseKernel_affinity (P : Θ → A → Y → ℝ) (acts : Θ → List A)
    (stay : A → Y → Bool) (θ σ : Θ) :
    affinity (stoppedPhaseKernel P acts stay θ σ) (stoppedPhaseKernel P acts stay σ σ) =
      survivalAffinity (P θ) (P σ) stay (acts σ) :=
  (survivalAffinity_eq_killed _ _ _ _).symm

omit [Fintype Θ] [DecidableEq Θ] [Fintype Y] [DecidableEq A] in
/-- Along all actually continuing histories, killing changes no likelihood. -/
theorem stoppedPhase_historyMass_eq_full (P : Θ → A → Y → ℝ) (acts : Θ → List A)
    (stay : A → Y → Bool) (θ : Θ)
    (h : List (Σ σ : Θ, StopObs Y (acts σ).length))
    (hsurvive : ∀ x ∈ h, stopCompleted x.2 = true) :
    dHistoryMass (stoppedPhaseKernel P acts stay) θ h =
      dHistoryMass (stoppedFullKernel P acts stay) θ h := by
  induction h with
  | nil => rfl
  | cons x h ih =>
    have hx := hsurvive x (List.mem_cons_self)
    have ht : ∀ y ∈ h, stopCompleted y.2 = true :=
      fun y hy => hsurvive y (List.mem_cons_of_mem _ hy)
    simp only [dHistoryMass, stoppedPhaseKernel, stoppedFullKernel, killedLaw, hx, ↓reduceIte, ih ht]

omit [DecidableEq Θ] [Fintype Y] [DecidableEq A] in
/-- Hence the phase selector is the same shared MLE selector on real, unconditioned
stopped-prefix data. Its killed-tree analysis does not normalize survival. -/
theorem stoppedPhase_MLE_eq_full (P : Θ → A → Y → ℝ) (acts : Θ → List A)
    (stay : A → Y → Bool) (initial : Θ)
    (h : List (Σ σ : Θ, StopObs Y (acts σ).length))
    (hsurvive : ∀ x ∈ h, stopCompleted x.2 = true) :
    dependentTreeMLE (stoppedPhaseKernel P acts stay) initial h =
      dependentTreeMLE (stoppedFullKernel P acts stay) initial h := by
  have hs : (fun θ => dHistoryMass (stoppedPhaseKernel P acts stay) θ h) =
      (fun θ => dHistoryMass (stoppedFullKernel P acts stay) θ h) := by
    funext θ
    exact stoppedPhase_historyMass_eq_full P acts stay θ h hsurvive
  unfold dependentTreeMLE
  rw [hs]

/-- End-to-end finite phase budget from raw action laws and the exact finite
progress-or-self-verification certificate. Zeros are allowed throughout. -/
theorem stoppedPhase_expected_selections_bound (P : Θ → A → Y → ℝ)
    (good : Θ → Finset A) (acts : Θ → List A) (stay : A → Y → Bool)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hNorm : ∀ θ a, ∑ y, P θ a y = 1)
    (hcert : ∀ σ, (∃ a ∈ acts σ, ∃ y, stay a y = false ∧ 0 < P σ a y) ∨
      SelfVerifying good (fun η ζ a => P η a = P ζ a) σ (acts σ).toFinset)
    (θ σ initial : Θ) (hbad : ¬ (acts σ).toFinset ⊆ good θ) (n : ℕ) :
    let ρ := ((acts σ).map (residualActionAffinity (P θ) (P σ) stay)).prod
    0 < 1-ρ ∧
      dSelectedCost (stoppedPhaseKernel P acts stay) θ σ
        (dependentTreeMLE (stoppedPhaseKernel P acts stay) initial) n [] ≤ 1/(1-ρ) := by
  have hpos := certificate_implies_strict_residual P good stay hP hNorm θ σ (acts σ)
    (hcert σ) hbad
  have haff := stoppedPhaseKernel_affinity P acts stay θ σ
  have hprod := survivalAffinity_product (P θ) (P σ) stay (hP θ) (hP σ) (acts σ)
  have hdef : affinity (stoppedPhaseKernel P acts stay θ σ)
      (stoppedPhaseKernel P acts stay σ σ) < 1 := by
    rw [haff]
    exact sub_pos.mp hpos
  have hb := dSelectedCost_subprob_uniform_bound (stoppedPhaseKernel P acts stay)
    (stoppedPhaseKernel_nonneg P acts stay hP) (stoppedPhaseKernel_subprob P acts stay hP hNorm)
    θ σ (dependentTreeMLE (stoppedPhaseKernel P acts stay) initial)
    (fun h heq => by
      have hm := dependentTreeMLE_maximizes (stoppedPhaseKernel P acts stay) initial θ h
      simpa only [heq] using hm) hdef n
  constructor
  · simpa only [hprod] using hpos
  · simpa only [haff, hprod] using hb

end Stopped
end Orthemology.Tranche2
