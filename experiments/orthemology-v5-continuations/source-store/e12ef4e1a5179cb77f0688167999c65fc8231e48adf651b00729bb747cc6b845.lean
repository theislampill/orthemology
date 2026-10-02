import WeightedPotential

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*}
    [Fintype Θ] [∀ p a, Fintype (Obs p a)] [DecidableEq Θ]

omit [DecidableEq Θ] in
/-- End-to-end finite-horizon reset budget. The potential and its decrement are
constructed from the raw full experiment laws; they are not input hypotheses.
The coefficient condition is numerical and is discharged for stopped blocks by
`certificate_implies_strict_residual` and `deficit_weight_certificate`.
The selector may maximize over a current live subset rather than all models. -/
theorem reset_hellinger_budget
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost w : Phase → Θ → ℝ) (θ : Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (rank : Phase → ℕ)
    (hRank : ∀ p a y, stay p a y = false → 0 < K p θ a y → rank (next p a y) < rank p)
    (hw : ∀ p σ, 0 ≤ w p σ)
    (hMLE : ∀ p h, dHistoryMass (continuingKernel K stay p) θ h ≤
      dHistoryMass (continuingKernel K stay p) (π p h) h)
    (hWeight : ∀ p h, cost p (π p h) ≤ w p (π p h) *
      (1-affinity (continuingKernel K stay p θ (π p h))
        (continuingKernel K stay p (π p h) (π p h))))
    (C : ℝ) (hC : 0 ≤ C) (hRoot : ∀ p, ∑ σ, w p σ ≤ C)
    (n : ℕ) (p : Phase) :
    resetCost K stay next π cost θ n p [] ≤ ((rank p : ℝ)+1)*C := by
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
  have hstep : ∀ p h,
      cost p (π p h) * dHistoryMass (continuingKernel K stay p) θ h +
        (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) ≤ V p h := by
    intro p h
    have hb := weightedHellinger_step (continuingKernel K stay p) (hcont p) (hSub p)
      θ (π p) (w p) (cost p) (hw p) (hMLE p) (hWeight p) h
    have heq : (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) =
      ∑ y : Obs p (π p h), V p (⟨π p h,y⟩::h) := by
      apply Finset.sum_congr rfl
      intro y _
      cases hs : stay p (π p h) y
      · simp [hs, V, weightedHellinger, dHistoryAffinity, dHistoryMass, continuingKernel]
      · simp [hs]
    rw [heq]
    exact hb
  exact resetCost_root_bound K stay next π cost θ hK (fun p a => hNorm p θ a)
    rank hRank V hV hstep C hC
    (fun p => by simpa only [V, weightedHellinger_root] using hRoot p) n p

/-- Restricting greedy maximization to a live finite model set preserves the
true-model comparison. Only the current live set is used; permanent exclusion
additionally requires a support-monotonicity certificate for phase updates. -/
def liveTreeMLE (K : (θ a : Θ) → Obs p a → ℝ) (live : Finset Θ) (initial : Θ)
    (h : PhaseHistory (Obs := Obs) p) : Θ :=
  greedyMax (fun σ => dHistoryMass K σ h) initial live.toList

omit [Fintype Θ] [(p : Phase) → (a : Θ) → Fintype (Obs p a)] [DecidableEq Θ] in
theorem liveTreeMLE_maximizes (K : (θ a : Θ) → Obs p a → ℝ)
    (live : Finset Θ) (initial θ : Θ) (hθ : θ ∈ live) (h : PhaseHistory (Obs := Obs) p) :
    dHistoryMass K θ h ≤ dHistoryMass K (liveTreeMLE K live initial h) h := by
  exact greedyMax_ge (fun σ => dHistoryMass K σ h) initial live.toList θ
    (Or.inr (by simpa using hθ))

end Orthemology.Tranche2
