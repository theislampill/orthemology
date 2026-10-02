import AcyclicPhaseBudget

noncomputable section
open Finset
open scoped BigOperators
namespace Orthemology.Tranche3
open Orthemology.Tranche2

section General
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*}
    [Fintype Phase] [Fintype Θ] [∀ p a, Fintype (Obs p a)]

/-- Phase-specific Hellinger budgets compose along the actual acyclic exit
relation. Branches are maximized, rather than all phases charged at every rank. -/
theorem chain_reset_hellinger_budget
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost w : Phase → Θ → ℝ) (θ : Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p)
    (I : Phase → Prop)
    (hNext : ∀ p a y, I p → stay p a y = false → 0 < K p θ a y → I (next p a y))
    (hEdge : ∀ p a y, I p → stay p a y = false → 0 < K p θ a y → edge p (next p a y))
    (hw : ∀ p σ, 0 ≤ w p σ)
    (hMLE : ∀ p, I p → ∀ h, dHistoryMass (continuingKernel K stay p) θ h ≤
      dHistoryMass (continuingKernel K stay p) (π p h) h)
    (hWeight : ∀ p, I p → ∀ h, cost p (π p h) ≤ w p (π p h) *
      (1-affinity (continuingKernel K stay p θ (π p h))
        (continuingKernel K stay p (π p h) (π p h))))
    (n : ℕ) (p : Phase) (hp : I p) :
    resetCost K stay next π cost θ n p [] ≤
      phaseChainBudget rank edge hRank (fun q => ∑ σ, w q σ) p := by
  classical
  have hcont : ∀ p η a y, 0 ≤ continuingKernel K stay p η a y := by
    intro p η a y
    unfold continuingKernel
    split_ifs <;> first | exact hK p η a y | exact le_rfl
  have hSub : ∀ p η a, ∑ y, continuingKernel K stay p η a y ≤ 1 := by
    intro p η a
    calc
      _ ≤ ∑ y, K p η a y := Finset.sum_le_sum (by
        intro y _
        unfold continuingKernel
        split_ifs <;> first | exact le_rfl | exact hK p η a y)
      _ = 1 := hNorm p η a
  let V := fun p h => weightedHellinger (continuingKernel K stay p) θ (w p) h
  have hV : ∀ p h, 0 ≤ V p h := fun p h =>
    weightedHellinger_nonneg _ θ _ (hw p) h
  have hstep : ∀ p, I p → ∀ h,
      cost p (π p h) * dHistoryMass (continuingKernel K stay p) θ h +
        (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) ≤ V p h := by
    intro p hip h
    have hb := weightedHellinger_step (continuingKernel K stay p) (hcont p) (hSub p)
      θ (π p) (w p) (cost p) (hw p) (hMLE p hip) (hWeight p hip) h
    have heq : (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) =
      ∑ y : Obs p (π p h), V p (⟨π p h,y⟩::h) := by
      apply Finset.sum_congr rfl
      intro y _
      cases hs : stay p (π p h) y
      · simp [hs, V, weightedHellinger, dHistoryAffinity, dHistoryMass, continuingKernel]
      · simp [hs]
    rw [heq]
    exact hb
  let D := phaseContinuationBudget rank edge hRank (fun q => ∑ σ, w q σ)
  have hb := resetCost_continuation_bound K stay next π cost θ hK (fun p a => hNorm p θ a)
    I hNext V (fun p _ h => hV p h) hstep D
    (fun p _ => phaseContinuationBudget_nonneg rank edge hRank _ p)
    (by
      intro p a y hp hs hy
      have he := phaseChainBudget_le_continuation rank edge hRank
        (fun q => ∑ σ, w q σ) p (next p a y) (hEdge p a y hp hs hy)
      rw [phaseChainBudget_eq] at he
      simpa only [V,weightedHellinger_root,D] using he) n p [] hp
  rw [phaseChainBudget_eq]
  simpa only [V,weightedHellinger_root,D,dHistoryMass,mul_one] using hb
end General

section Recursive
variable {Θ A Y : Type*} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

/-- An edge records an actual positive-probability exit under the true model.
The hidden model indexes only this analysis graph and never the controller. -/
def recursiveExitEdge (θ : Θ) (p q : WinningPhase P good menu) : Prop :=
  θ ∈ p.val ∧ ∃ σ, ∃ w : StopObs Y (phaseActs P good menu p σ).length,
    stopCompleted w = false ∧
    0 < stoppedMass (P θ) (supportStay P p.val) (phaseActs P good menu p σ) w ∧
    q = phaseNext P good menu p σ w

omit [Fintype Θ] [Fintype Y] in
lemma recursiveExitEdge_rank
    (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ) (p q : WinningPhase P good menu)
    (he : recursiveExitEdge P good menu θ p q) :
    phaseRank P good menu q < phaseRank P good menu p := by
  obtain ⟨hθ,σ,w,hs,hw,rfl⟩ := he
  exact phaseNext_rank_decreases P good menu hP θ p σ w hθ hs hw

/-- Each positive local cost is charged by a strictly positive residual deficit. -/
def recursiveHellingerWeight (θ : Θ) (p : WinningPhase P good menu) (σ : Θ) : ℝ :=
  if θ ∈ p.val ∧ 0 < recursiveBadCharge P good menu θ p σ then
    (recursiveBadCharge P good menu θ p σ : ℝ) /
      (1 - survivalAffinity (P θ) (P σ) (supportStay P p.val) (phaseActs P good menu p σ))
  else 0

omit [Fintype Θ] [Fintype Y] in
lemma recursiveBadCharge_positive (θ : Θ) (p : WinningPhase P good menu) (σ : Θ)
    (hc : 0 < recursiveBadCharge P good menu θ p σ) :
    σ ∈ p.val ∧ ¬ (phaseActs P good menu p σ).toFinset ⊆ good θ := by
  unfold recursiveBadCharge at hc
  split_ifs at hc with hl
  · exact ⟨hl,(plannedBadCount_pos_iff _ _).mp hc⟩
  · exact (Nat.lt_irrefl 0 hc).elim

omit [Fintype Θ] in
lemma recursiveHellingerWeight_nonneg
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (σ : Θ) :
    0 ≤ recursiveHellingerWeight P good menu θ p σ := by
  classical
  unfold recursiveHellingerWeight
  split_ifs with hc
  · obtain ⟨hl,hbad⟩ := recursiveBadCharge_positive P good menu θ p σ hc.2
    have hd := live_certificate_implies_strict_residual P good (supportStay P p.val) p.val
      hP hN θ σ hc.1 (phaseActs P good menu p σ) (phaseActs_certificate P good menu p σ hl) hbad
    exact div_nonneg (Nat.cast_nonneg _) hd.le
  · exact le_rfl

/-- The support-DAG Hellinger budget uses the maximum cost of a possible phase
chain, replacing the earlier rank times all-winning-phases constant. -/
def recursiveChainBudget (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ)
    (p : WinningPhase P good menu) : ℝ :=
  phaseChainBudget (phaseRank P good menu) (recursiveExitEdge P good menu θ)
    (recursiveExitEdge_rank P good menu hP θ)
    (fun q => ∑ σ, recursiveHellingerWeight P good menu θ q σ) p

/-- The new constant is never larger than the inherited global phase bound. -/
theorem recursiveChainBudget_le_global
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) :
    recursiveChainBudget P good menu hP θ p ≤ recursivePhysicalBudget P good menu θ p := by
  apply phaseChainBudget_le_rank_bound
  · exact Finset.sum_nonneg (fun q _ => Finset.sum_nonneg
      (fun σ _ => recursiveHellingerWeight_nonneg P good menu hP hN θ q σ))
  · intro q
    exact Finset.single_le_sum (fun r _ => Finset.sum_nonneg
      (fun σ _ => recursiveHellingerWeight_nonneg P good menu hP hN θ r σ)) (Finset.mem_univ q)

/-- Raw finite kernels and the recursive certificate yield the chain budget;
no drift, graph-admissibility or rank premise is supplied by the caller. -/
theorem recursive_resetCost_le_chainBudget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (n : ℕ) :
    resetCost (recursiveFullKernel P good menu) (recursiveKeep P good menu)
      (phaseNext P good menu) (recursivePolicy P good menu)
      (fun q σ => (recursiveBadCharge P good menu θ q σ : ℝ)) θ n p [] ≤
        recursiveChainBudget P good menu hP θ p := by
  classical
  apply chain_reset_hellinger_budget
    (recursiveFullKernel P good menu) (recursiveKeep P good menu)
    (phaseNext P good menu) (recursivePolicy P good menu)
    (fun q σ => (recursiveBadCharge P good menu θ q σ : ℝ))
    (recursiveHellingerWeight P good menu θ) θ
    (recursiveFull_nonneg P good menu hP) (recursiveFull_normalized P good menu hN)
    (phaseRank P good menu) (recursiveExitEdge P good menu θ)
    (recursiveExitEdge_rank P good menu hP θ) (fun q => θ ∈ q.val)
  · intro q σ w ht hs hw
    exact (phaseNext_actual_support P good menu hP θ q σ w ht hs hw).2.1
  · intro q σ w ht hs hw
    exact ⟨ht,σ,w,hs,hw,rfl⟩
  · exact recursiveHellingerWeight_nonneg P good menu hP hN θ
  · intro q ht h
    exact liveTreeMLE_maximizes (Obs := fun q σ => StopObs Y (phaseActs P good menu q σ).length)
      (p := q) _ q.val (phaseInitial P good menu q) θ ht h
  · intro q ht h
    let σ := recursivePolicy P good menu q h
    change (recursiveBadCharge P good menu θ q σ : ℝ) ≤
      recursiveHellingerWeight P good menu θ q σ *
        (1 - affinity (stoppedPhaseKernel P (phaseActs P good menu q) (supportStay P q.val) θ σ)
          (stoppedPhaseKernel P (phaseActs P good menu q) (supportStay P q.val) σ σ))
    rw [stoppedPhaseKernel_affinity]
    unfold recursiveHellingerWeight
    by_cases hc : 0 < recursiveBadCharge P good menu θ q σ
    · rw [if_pos ⟨ht,hc⟩]
      obtain ⟨hl,hbad⟩ := recursiveBadCharge_positive P good menu θ q σ hc
      have hd := live_certificate_implies_strict_residual P good (supportStay P q.val) q.val
        hP hN θ σ ht (phaseActs P good menu q σ) (phaseActs_certificate P good menu q σ hl) hbad
      rw [div_mul_cancel₀ _ hd.ne']
    · have hz : recursiveBadCharge P good menu θ q σ = 0 := Nat.eq_zero_of_not_pos hc
      simp [hz]
  · exact hθ
end Recursive
end Orthemology.Tranche3
