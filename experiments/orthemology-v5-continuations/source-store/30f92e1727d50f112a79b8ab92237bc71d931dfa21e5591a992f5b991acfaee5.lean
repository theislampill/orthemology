import MarkovCharge

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset Preorder Function
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {S : Type*} [MeasurableSpace S] [Countable S] [MeasurableSingletonClass S]

lemma trajectory_coordinate_integral (M : Kernel S S) [IsMarkovKernel M]
    (f : S → ℝ≥0∞) (k : ℕ) (s : S) :
    (∫⁻ x, f (x k) ∂markovTrajectory M s) =
      Kernel.lmarginalPartialTraj (markovKernelSequence M) 0 k (fun x => f (x k)) (fun _ => s) := by
  let F : ((i : Iic k) → S) → ℝ≥0∞ := fun h => f (h ⟨k,Finset.mem_Iic.mpr le_rfl⟩)
  have hF : Measurable F := by fun_prop
  calc
    (∫⁻ x, f (x k) ∂markovTrajectory M s) = ∫⁻ x, F (frestrictLe k x) ∂markovTrajectory M s := rfl
    _ = ∫⁻ h, F h ∂(markovTrajectory M s).map (frestrictLe k) :=
      (lintegral_map hF (measurable_frestrictLe k)).symm
    _ = ∫⁻ h, F h ∂Kernel.partialTraj (X := fun _ : ℕ => S)
        (markovKernelSequence M) 0 k (fun _ => s) := by rw [markovTrajectory_finite_law]
    _ = _ := by
      unfold Kernel.lmarginalPartialTraj
      congr 1
      funext h
      simp [F, updateFinset]

/-- A zero one-step nonnegative cost occurs at no positive time, almost surely,
under the actual generated trajectory measure. -/
theorem markov_zero_after_initial (M : Kernel S S) [IsMarkovKernel M]
    (f : S → ℝ≥0∞) (hzero : ∀ s, (∫⁻ t, f t ∂M s) = 0) (s : S) :
    ∀ᵐ x ∂markovTrajectory M s, ∀ n : ℕ, f (x (n+1)) = 0 := by
  apply ae_all_iff.mpr
  intro n
  apply (lintegral_eq_zero_iff (by fun_prop)).mp
  rw [trajectory_coordinate_integral]
  have hi : Kernel.lmarginalPartialTraj (markovKernelSequence M) n (n+1)
      (fun x : ℕ → S => f (x (n+1))) = 0 := by
    funext x
    rw [lmarginal_next_coordinate]
    exact hzero _
  have ht := congrFun (Kernel.lmarginalPartialTraj_self (κ := markovKernelSequence M)
    (a := 0) (b := n) (c := n+1) (Nat.zero_le _) (Nat.le_succ _) (by fun_prop :
      Measurable (fun x : ℕ → S => f (x (n+1))))) (fun _ => s)
  rw [hi] at ht
  rw [← ht]
  simp [Kernel.lmarginalPartialTraj]

end Orthemology.Tranche2
