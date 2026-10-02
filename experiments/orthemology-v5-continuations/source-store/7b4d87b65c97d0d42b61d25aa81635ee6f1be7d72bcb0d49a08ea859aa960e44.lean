import NormalizedResetPotential

noncomputable section
set_option linter.unusedSectionVars false
open Finset
open scoped BigOperators
namespace Orthemology.Tranche3
open Orthemology.Tranche2
variable {Θ A Y : Type*} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

abbrev RecursiveMacroState := ResetState (Obs := fun p σ => StopObs Y (phaseActs P good menu p σ).length)

def recursivePhasePotential (θ : Θ) (p : WinningPhase P good menu)
    (h : PhaseHistory (Obs := fun p σ => StopObs Y (phaseActs P good menu p σ).length) p) : ℝ :=
  weightedHellinger (continuingKernel (recursiveFullKernel P good menu) (recursiveKeep P good menu) p)
    θ (recursiveHellingerWeight P good menu θ p) h

def recursiveContinuationPotential (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ)
    (p : WinningPhase P good menu) : ℝ :=
  phaseContinuationBudget (phaseRank P good menu) (recursiveExitEdge P good menu θ)
    (recursiveExitEdge_rank P good menu hP θ)
    (fun q => ∑ σ, recursiveHellingerWeight P good menu θ q σ) p

def recursiveMacroPotential (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ)
    (s : RecursiveMacroState P good menu) : ℝ :=
  normalizedResetPotential (recursiveFullKernel P good menu) (recursiveKeep P good menu) θ
    (recursivePhasePotential P good menu θ) (recursiveContinuationPotential P good menu hP θ) s

def recursiveMacroValid (θ : Θ) (s : RecursiveMacroState P good menu) : Prop :=
  θ ∈ s.1.val ∧ 0 < dHistoryMass
    (continuingKernel (recursiveFullKernel P good menu) (recursiveKeep P good menu) s.1) θ s.2

lemma recursivePhasePotential_nonneg
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu)
    (h : PhaseHistory (Obs := fun p σ => StopObs Y (phaseActs P good menu p σ).length) p) :
    0 ≤ recursivePhasePotential P good menu θ p h :=
  weightedHellinger_nonneg _ θ _ (recursiveHellingerWeight_nonneg P good menu hP hN θ p) h

lemma recursiveMacroPotential_nonneg
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (s : RecursiveMacroState P good menu) :
    0 ≤ recursiveMacroPotential P good menu hP θ s :=
  normalizedResetPotential_nonneg _ _ θ _ _
    (recursivePhasePotential_nonneg P good menu hP hN θ)
    (fun p => phaseContinuationBudget_nonneg _ _ _ _ p) s

omit [Fintype Θ] [Fintype Y] in
/-- The positive-likelihood invariant needed by normalization is propagated
by every actual positive-probability block outcome, including all zero-support exits. -/
theorem recursiveMacroValid_next
    (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ) (s : RecursiveMacroState P good menu)
    (hs : recursiveMacroValid P good menu θ s)
    (w : StopObs Y (phaseActs P good menu s.1 (recursivePolicy P good menu s.1 s.2)).length)
    (hw : 0 < recursiveFullKernel P good menu s.1 θ (recursivePolicy P good menu s.1 s.2) w) :
    recursiveMacroValid P good menu θ
      (resetUpdate (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu) s w) := by
  rcases s with ⟨p,h⟩
  rcases hs with ⟨ht,hm⟩
  cases hs : recursiveKeep P good menu p (recursivePolicy P good menu p h) w
  · have hu : resetUpdate (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu)
      ⟨p,h⟩ w = ⟨phaseNext P good menu p (recursivePolicy P good menu p h) w,[]⟩ := by simp [resetUpdate,hs]
    rw [hu]
    exact ⟨(phaseNext_actual_support P good menu hP θ p _ w ht hs hw).2.1,by simp [dHistoryMass]⟩
  · have hu : resetUpdate (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu)
      ⟨p,h⟩ w = ⟨p,⟨recursivePolicy P good menu p h,w⟩::h⟩ := by simp [resetUpdate,hs]
    rw [hu]
    refine ⟨ht,?_⟩
    simpa only [dHistoryMass,continuingKernel,hs,↓reduceIte] using mul_pos hm hw

/-- The stopped, unnormalized phase drift is reconstructed from the raw laws. -/
theorem recursivePhasePotential_step
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (ht : θ ∈ p.val)
    (h : PhaseHistory (Obs := fun p σ => StopObs Y (phaseActs P good menu p σ).length) p) :
    (recursiveBadCharge P good menu θ p (recursivePolicy P good menu p h) : ℝ) *
        dHistoryMass (continuingKernel (recursiveFullKernel P good menu) (recursiveKeep P good menu) p) θ h +
      (∑ w, if recursiveKeep P good menu p (recursivePolicy P good menu p h) w then
        recursivePhasePotential P good menu θ p (⟨recursivePolicy P good menu p h,w⟩::h) else 0) ≤
      recursivePhasePotential P good menu θ p h := by
  let K := continuingKernel (recursiveFullKernel P good menu) (recursiveKeep P good menu) p
  have hK : ∀ η σ w, 0 ≤ K η σ w := by
    intro η σ w
    unfold K continuingKernel
    split_ifs <;> first | exact recursiveFull_nonneg P good menu hP _ _ _ _ | exact le_rfl
  have hSub : ∀ η σ, ∑ w, K η σ w ≤ 1 := by
    intro η σ
    calc
      _ ≤ ∑ w, recursiveFullKernel P good menu p η σ w := by
        apply Finset.sum_le_sum
        intro w _
        unfold K continuingKernel
        split_ifs <;> first | exact le_rfl | exact recursiveFull_nonneg P good menu hP _ _ _ _
      _ = 1 := recursiveFull_normalized P good menu hN _ _ _
  have hweight : ∀ h, (recursiveBadCharge P good menu θ p (recursivePolicy P good menu p h) : ℝ) ≤
      recursiveHellingerWeight P good menu θ p (recursivePolicy P good menu p h) *
        (1-affinity (K θ (recursivePolicy P good menu p h))
          (K (recursivePolicy P good menu p h) (recursivePolicy P good menu p h))) := by
    intro h
    let σ := recursivePolicy P good menu p h
    change (recursiveBadCharge P good menu θ p σ : ℝ) ≤ recursiveHellingerWeight P good menu θ p σ *
      (1-affinity (stoppedPhaseKernel P (phaseActs P good menu p) (supportStay P p.val) θ σ)
        (stoppedPhaseKernel P (phaseActs P good menu p) (supportStay P p.val) σ σ))
    rw [stoppedPhaseKernel_affinity]
    unfold recursiveHellingerWeight
    by_cases hc : 0 < recursiveBadCharge P good menu θ p σ
    · rw [if_pos ⟨ht,hc⟩]
      obtain ⟨hl,hbad⟩ := recursiveBadCharge_positive P good menu θ p σ hc
      have hd := live_certificate_implies_strict_residual P good (supportStay P p.val) p.val
        hP hN θ σ ht (phaseActs P good menu p σ) (phaseActs_certificate P good menu p σ hl) hbad
      rw [div_mul_cancel₀ _ hd.ne']
    · have hz := Nat.eq_zero_of_not_pos hc
      simp [hz]
  have hb := weightedHellinger_step K hK hSub θ (recursivePolicy P good menu p)
    (recursiveHellingerWeight P good menu θ p) (fun σ => (recursiveBadCharge P good menu θ p σ : ℝ))
    (recursiveHellingerWeight_nonneg P good menu hP hN θ p)
    (fun h => liveTreeMLE_maximizes (Obs := fun p σ => StopObs Y (phaseActs P good menu p σ).length)
      (p := p) _ p.val (phaseInitial P good menu p) θ ht h) hweight h
  have he : (∑ w, if recursiveKeep P good menu p (recursivePolicy P good menu p h) w then
      recursivePhasePotential P good menu θ p (⟨recursivePolicy P good menu p h,w⟩::h) else 0) =
      ∑ w, recursivePhasePotential P good menu θ p (⟨recursivePolicy P good menu p h,w⟩::h) := by
    apply Finset.sum_congr rfl
    intro w _
    cases hs : recursiveKeep P good menu p (recursivePolicy P good menu p h) w
    · simp [hs,recursivePhasePotential,weightedHellinger,dHistoryAffinity,dHistoryMass,continuingKernel]
    · simp [hs]
  rw [he]
  exact hb

/-- The chain-budget potential pays for one complete offered plan and the
actual first-exit/completion continuation, conditional only on a finite history. -/
theorem recursiveMacroPotential_step
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (s : RecursiveMacroState P good menu) (hs : recursiveMacroValid P good menu θ s) :
    (recursiveBadCharge P good menu θ s.1 (recursivePolicy P good menu s.1 s.2) : ℝ) +
      ∑ w, recursiveFullKernel P good menu s.1 θ (recursivePolicy P good menu s.1 s.2) w *
        recursiveMacroPotential P good menu hP θ
          (resetUpdate (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu) s w) ≤
      recursiveMacroPotential P good menu hP θ s := by
  rcases s with ⟨p,h⟩
  unfold recursiveMacroPotential
  apply normalizedResetPotential_step (recursiveFullKernel P good menu) (recursiveKeep P good menu)
    (phaseNext P good menu) (recursivePolicy P good menu)
    (fun p σ => (recursiveBadCharge P good menu θ p σ : ℝ)) θ
    (recursiveFull_nonneg P good menu hP) (fun p σ => recursiveFull_normalized P good menu hN p θ σ)
    (fun p => θ ∈ p.val) _ (recursivePhasePotential_nonneg P good menu hP hN θ)
    (recursivePhasePotential_step P good menu hP hN θ) _
  · intro p σ w hp hw hpos
    have he : recursiveExitEdge P good menu θ p (phaseNext P good menu p σ w) := ⟨hp,σ,w,hw,hpos,rfl⟩
    have hh := phaseChainBudget_le_continuation (phaseRank P good menu) (recursiveExitEdge P good menu θ)
      (recursiveExitEdge_rank P good menu hP θ) (fun q => ∑ σ, recursiveHellingerWeight P good menu θ q σ)
      p (phaseNext P good menu p σ w) he
    rw [phaseChainBudget_eq] at hh
    simpa only [recursivePhasePotential,weightedHellinger_root,recursiveContinuationPotential] using hh
  · exact hs.1
  · exact hs.2

lemma recursiveMacroPotential_root
    (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ) (p : WinningPhase P good menu) :
    recursiveMacroPotential P good menu hP θ ⟨p,[]⟩ = recursiveChainBudget P good menu hP θ p := by
  rw [recursiveChainBudget,phaseChainBudget_eq]
  simp [recursiveMacroPotential,normalizedResetPotential,dHistoryMass,
    recursivePhasePotential,weightedHellinger_root,recursiveContinuationPotential]
end Orthemology.Tranche3
