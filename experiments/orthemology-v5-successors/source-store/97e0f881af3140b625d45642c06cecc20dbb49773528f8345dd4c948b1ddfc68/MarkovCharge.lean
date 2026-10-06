import ResetTrajectory

noncomputable section
open MeasureTheory ProbabilityTheory Finset Preorder Function
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {S : Type*} [MeasurableSpace S] [Countable S] [MeasurableSingletonClass S]

def markovExpectedCharge (M : Kernel S S) (c : S → ℝ≥0∞) : ℕ → S → ℝ≥0∞
  | 0, _ => 0
  | n+1, s => c s + ∫⁻ t, markovExpectedCharge M c n t ∂M s

def pathCharge (c : S → ℝ≥0∞) (a n : ℕ) (x : ℕ → S) : ℝ≥0∞ :=
  ∑ i ∈ Finset.range n, c (x (a+i))

lemma pathCharge_measurable (c : S → ℝ≥0∞) (a n : ℕ) : Measurable (pathCharge c a n) := by
  unfold pathCharge
  fun_prop

omit [MeasurableSpace S] [Countable S] [MeasurableSingletonClass S] in
lemma pathCharge_succ (c : S → ℝ≥0∞) (a n : ℕ) (x : ℕ → S) :
    pathCharge c a (n+1) x = c (x a) + pathCharge c (a+1) n x := by
  unfold pathCharge
  rw [Finset.sum_range_succ']
  simp only [Nat.add_zero]
  rw [add_comm]
  congr 1
  apply Finset.sum_congr rfl
  intro i _
  congr 2
  omega

/-- Backwards integration over one genuine Markov transition. -/
lemma lmarginal_next_coordinate (M : Kernel S S) [IsMarkovKernel M]
    (f : S → ℝ≥0∞) (a : ℕ) (x : ℕ → S) :
    Kernel.lmarginalPartialTraj (markovKernelSequence M) a (a+1)
      (fun z => f (z (a+1))) x = ∫⁻ y, f y ∂M (x a) := by
  rw [Kernel.lmarginalPartialTraj_succ a (by fun_prop)]
  simp [markovKernelSequence, Kernel.comap_apply, frestrictLe_apply]

lemma lmarginal_current_plus (M : Kernel S S) [IsMarkovKernel M]
    (c : S → ℝ≥0∞) (a b : ℕ) (hab : a ≤ b) (f : (ℕ → S) → ℝ≥0∞)
    (_hf : Measurable f) (x : ℕ → S) :
    Kernel.lmarginalPartialTraj (markovKernelSequence M) a b (fun z => c (z a) + f z) x =
      c (x a) + Kernel.lmarginalPartialTraj (markovKernelSequence M) a b f x := by
  unfold Kernel.lmarginalPartialTraj
  have heq : ∀ z : (i : Iic b) → S,
      c (updateFinset x (Iic b) z a) = c (z ⟨a, Finset.mem_Iic.mpr hab⟩) := by
    intro z
    simp [updateFinset, hab]
  simp_rw [heq]
  rw [lintegral_add_left (by fun_prop)]
  congr 1
  have hc : DependsOn (fun z : ℕ → S => c (z a)) (Iic a) := by
    intro u v huv
    exact congrArg c (huv a (Finset.mem_Iic.mpr le_rfl))
  have hh := hc.lmarginalPartialTraj_of_le (κ := markovKernelSequence M) b (by fun_prop) le_rfl
  have hv := congrFun hh x
  simpa only [Kernel.lmarginalPartialTraj, heq] using hv

/-- Backwards dynamic programming is the integral of the actual finite
trajectory law, proved from the one-step kernel and its composition theorem. -/
theorem lmarginal_pathCharge (M : Kernel S S) [IsMarkovKernel M]
    (c : S → ℝ≥0∞) (n a : ℕ) (x : ℕ → S) :
    Kernel.lmarginalPartialTraj (markovKernelSequence M) a (a+n)
      (pathCharge c a (n+1)) x = markovExpectedCharge M c (n+1) (x a) := by
  induction n generalizing a x with
  | zero =>
    rw [Nat.add_zero, Kernel.lmarginalPartialTraj_le _ le_rfl (pathCharge_measurable c a 1)]
    simp [pathCharge, markovExpectedCharge]
  | succ n ih =>
    have hsplit : pathCharge c a (n+1+1) = fun z => c (z a) + pathCharge c (a+1) (n+1) z := by
      funext z
      exact pathCharge_succ c a (n+1) z
    rw [hsplit, lmarginal_current_plus M c a (a+(n+1)) (by omega)
      (pathCharge c (a+1) (n+1)) (pathCharge_measurable c (a+1) (n+1))]
    have hbound : a+(n+1) = (a+1)+n := by omega
    have hinner : Kernel.lmarginalPartialTraj (markovKernelSequence M) (a+1) (a+(n+1))
        (pathCharge c (a+1) (n+1)) = fun z => markovExpectedCharge M c (n+1) (z (a+1)) := by
      funext z
      rw [hbound]
      exact ih (a+1) z
    have ht := congrFun (Kernel.lmarginalPartialTraj_self (κ := markovKernelSequence M)
      (a := a) (b := a+1) (c := a+(n+1)) (by omega) (by omega)
      (pathCharge_measurable c (a+1) (n+1))) x
    rw [hinner] at ht
    rw [← ht, lmarginal_next_coordinate]
    rfl

/-- Finite-prefix cost under the constructed infinite trajectory law equals the
normalized dynamic-programming recurrence. No caller supplies a cylinder law. -/
theorem markovTrajectory_expected_charge (M : Kernel S S) [IsMarkovKernel M]
    (c : S → ℝ≥0∞) (n : ℕ) (s : S) :
    (∫⁻ x, pathCharge c 0 n x ∂markovTrajectory M s) = markovExpectedCharge M c n s := by
  cases n with
  | zero => simp [pathCharge, markovExpectedCharge]
  | succ n =>
    let F : ((i : Iic n) → S) → ℝ≥0∞ := fun h =>
      pathCharge c 0 (n+1) (updateFinset (fun _ => s) (Iic n) h)
    have hF : Measurable F := by
      exact (pathCharge_measurable c 0 (n+1)).comp (by fun_prop)
    have heq : (fun x : ℕ → S => F (frestrictLe n x)) = pathCharge c 0 (n+1) := by
      funext x
      dsimp [F, pathCharge]
      apply Finset.sum_congr rfl
      intro i hi
      have hi' : i ≤ n := Nat.le_of_lt_succ (Finset.mem_range.mp hi)
      simp [updateFinset, hi', frestrictLe_apply]
    calc
      (∫⁻ x, pathCharge c 0 (n+1) x ∂markovTrajectory M s) =
          ∫⁻ x, F (frestrictLe n x) ∂markovTrajectory M s := by rw [heq]
      _ = ∫⁻ h, F h ∂(markovTrajectory M s).map (frestrictLe n) :=
        (lintegral_map hF (measurable_frestrictLe n)).symm
      _ = ∫⁻ h, F h ∂Kernel.partialTraj (X := fun _ : ℕ => S)
          (markovKernelSequence M) 0 n (fun _ => s) := by rw [markovTrajectory_finite_law]
      _ = Kernel.lmarginalPartialTraj (markovKernelSequence M) 0 (0+n)
          (pathCharge c 0 (n+1)) (fun _ => s) := by
        rw [Nat.zero_add]
        rfl
      _ = markovExpectedCharge M c (n+1) s := lmarginal_pathCharge M c n 0 (fun _ => s)

end Orthemology.Tranche2
