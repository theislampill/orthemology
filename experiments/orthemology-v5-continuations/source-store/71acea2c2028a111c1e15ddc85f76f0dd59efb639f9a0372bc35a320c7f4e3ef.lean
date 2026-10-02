import FiniteChainAvoidance
import MarkovCharge

noncomputable section
set_option maxHeartbeats 800000
open MeasureTheory ProbabilityTheory Finset Preorder Function
open scoped BigOperators ENNReal

namespace HiddenParity.Recurrence
open Orthemology.Tranche2

variable {S : Type*} [Fintype S] [DecidableEq S]
variable [MeasurableSpace S] [MeasurableSingletonClass S]

def transitionPMF (P : FiniteChain S) (s : S) : PMF S :=
  PMF.ofFintype (fun t => ENNReal.ofReal (P.prob s t)) (by
    rw [← ENNReal.ofReal_sum_of_nonneg (fun t _ => P.nonnegative s t), P.normalized, ENNReal.ofReal_one])

def transitionKernel (P : FiniteChain S) : Kernel S S where
  toFun s := (transitionPMF P s).toMeasure
  measurable' := measurable_of_countable _

instance transitionKernel_markov (P : FiniteChain S) : IsMarkovKernel (transitionKernel P) :=
  ⟨fun s => by change IsProbabilityMeasure (transitionPMF P s).toMeasure; infer_instance⟩

omit [DecidableEq S] in
theorem transitionKernel_singleton (P : FiniteChain S) (s t : S) :
    transitionKernel P s {t} = ENNReal.ofReal (P.prob s t) := by
  change (transitionPMF P s).toMeasure {t} = _
  rw [PMF.toMeasure_apply_singleton _ t (measurableSet_singleton t)]
  rfl

omit [DecidableEq S] in
theorem lintegral_transition_ofReal (P : FiniteChain S) (s : S) (f : S → ℝ)
    (hf : ∀ t, 0 ≤ f t) :
    (∫⁻ t, ENNReal.ofReal (f t) ∂transitionKernel P s) =
      ENNReal.ofReal (∑ t, P.prob s t * f t) := by
  rw [lintegral_fintype, ENNReal.ofReal_sum_of_nonneg
    (fun t _ => mul_nonneg (P.nonnegative s t) (hf t))]
  apply Finset.sum_congr rfl
  intro t _
  rw [transitionKernel_singleton, ENNReal.ofReal_mul (P.nonnegative s t), mul_comm]

/-- Indicator of avoiding target for n consecutive coordinates starting at a. -/
def pathAvoid (target : S) (a : ℕ) : ℕ → (ℕ → S) → ℝ≥0∞
  | 0, _ => 1
  | n+1, x => if x a = target then 0 else pathAvoid target (a+1) n x

omit [Fintype S] in
theorem pathAvoid_measurable (target : S) (a n : ℕ) : Measurable (pathAvoid target a n) := by
  induction n generalizing a with
  | zero => exact measurable_const
  | succ n ih =>
      exact Measurable.ite
        ((measurableSet_singleton target).preimage (measurable_pi_apply a)) measurable_const (ih _)

omit [Fintype S] [MeasurableSpace S] [MeasurableSingletonClass S] in
theorem pathAvoid_depends (target : S) (a n : ℕ) :
    DependsOn (pathAvoid target a (n+1)) (Iic (a+n)) := by
  induction n generalizing a with
  | zero =>
      intro x y hxy
      simp only [pathAvoid, hxy a (by simp)]
  | succ n ih =>
      intro x y hxy
      simp only [pathAvoid]
      rw [hxy a (by simp)]
      by_cases hy : y a = target
      · simp [hy]
      · simp only [if_neg hy]
        apply ih
        intro i hi
        exact hxy i (by simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hi)

omit [Fintype S] in
/-- Backward integration leaves the already acquired current coordinate fixed. -/
theorem lmarginal_current_if (M : Kernel S S) [IsMarkovKernel M]
    (target : S) (a b : ℕ) (f : (ℕ → S) → ℝ≥0∞) (hf : Measurable f) (x : ℕ → S) :
    Kernel.lmarginalPartialTraj (markovKernelSequence M) a b
      (fun z => if z a = target then 0 else f z) x =
      if x a = target then 0 else Kernel.lmarginalPartialTraj (markovKernelSequence M) a b f x := by
  have hg : Measurable (fun z : ℕ → S => if z a = target then (0 : ℝ≥0∞) else f z) :=
    Measurable.ite ((measurableSet_singleton target).preimage (measurable_pi_apply a)) measurable_const hf
  rw [Kernel.lmarginalPartialTraj_eq_lintegral_map hg,
    Kernel.lmarginalPartialTraj_eq_lintegral_map hf]
  have he : ∀ z : (i : Ioc a b) → S, updateFinset x (Ioc a b) z a = x a := by
    intro z
    simp [updateFinset]
  simp_rw [he]
  by_cases hx : x a = target <;> simp [hx]

/-- The dynamic program is the integral under the actual finite Markov trajectory
composition, proved from the one-step kernel and composition theorem. -/
theorem lmarginal_pathAvoid (P : FiniteChain S) (target : S) (n a : ℕ) (x : ℕ → S) :
    Kernel.lmarginalPartialTraj (markovKernelSequence (transitionKernel P)) a (a+n)
      (pathAvoid target a (n+1)) x = ENNReal.ofReal (avoid P target (n+1) (x a)) := by
  induction n generalizing a x with
  | zero =>
      rw [Nat.add_zero, Kernel.lmarginalPartialTraj_le _ le_rfl (pathAvoid_measurable target a 1)]
      by_cases hx : x a = target <;> simp [pathAvoid, avoid, hx, P.normalized]
  | succ n ih =>
      change Kernel.lmarginalPartialTraj _ a (a+(n+1))
        (fun z => if z a = target then 0 else pathAvoid target (a+1) (n+1) z) x = _
      rw [lmarginal_current_if _ target a (a+(n+1)) _ (pathAvoid_measurable target (a+1) (n+1))]
      by_cases hx : x a = target
      · simp [hx, avoid]
      · rw [if_neg hx, avoid, if_neg hx]
        have hinner : Kernel.lmarginalPartialTraj (markovKernelSequence (transitionKernel P))
            (a+1) (a+(n+1)) (pathAvoid target (a+1) (n+1)) =
            fun z => ENNReal.ofReal (avoid P target (n+1) (z (a+1))) := by
          funext z
          have heq : a+(n+1) = (a+1)+n := by omega
          rw [heq]
          exact ih (a+1) z
        have ht := congrFun (Kernel.lmarginalPartialTraj_self
          (κ := markovKernelSequence (transitionKernel P))
          (a := a) (b := a+1) (c := a+(n+1)) (by omega) (by omega)
          (pathAvoid_measurable target (a+1) (n+1))) x
        rw [hinner] at ht
        rw [← ht]
        rw [lmarginal_next_coordinate (transitionKernel P)
          (fun t => ENNReal.ofReal (avoid P target (n+1) t)) a x]
        exact lintegral_transition_ofReal P (x a) (avoid P target (n+1))
          (fun t => avoid_nonnegative P target (n+1) t)

omit [Fintype S] [DecidableEq S] [MeasurableSingletonClass S] in
/-- A function of a finite prefix integrates against the constructed infinite
trajectory exactly as against its finite Ionescu-Tulcea marginal. -/
theorem trajectory_integral_prefix (M : Kernel S S) [IsMarkovKernel M]
    (f : (ℕ → S) → ℝ≥0∞) (hf : Measurable f) (b : ℕ) (hdep : DependsOn f (Iic b)) (s : S) :
    (∫⁻ x, f x ∂markovTrajectory M s) =
      Kernel.lmarginalPartialTraj (markovKernelSequence M) 0 b f (fun _ => s) := by
  let F : ((i : Iic b) → S) → ℝ≥0∞ := fun h => f (updateFinset (fun _ => s) (Iic b) h)
  have hF : Measurable F := hf.comp (by fun_prop)
  have heq : (fun x : ℕ → S => F (frestrictLe b x)) = f := by
    funext x
    apply hdep
    intro i hi
    have hle : i ≤ b := Finset.mem_Iic.mp hi
    simp [F, updateFinset, hle, frestrictLe_apply]
  calc
    _ = ∫⁻ x, F (frestrictLe b x) ∂markovTrajectory M s := by rw [heq]
    _ = ∫⁻ h, F h ∂(markovTrajectory M s).map (frestrictLe b) :=
      (lintegral_map hF (measurable_frestrictLe b)).symm
    _ = ∫⁻ h, F h ∂Kernel.partialTraj (X := fun _ : ℕ => S) (markovKernelSequence M) 0 b (fun _ => s) := by
      rw [markovTrajectory_finite_law]
    _ = _ := rfl

/-- Uniform state-wise finite avoidance controls every deterministic future
interval of the actual infinite trajectory, without assuming a Markov property
for a conditioned process. -/
theorem trajectory_interval_avoidance_bound (P : FiniteChain S) (target s : S)
    (a n : ℕ) (r : ℝ) (hUniform : ∀ t, avoid P target n t ≤ r) :
    (∫⁻ x, pathAvoid target a n x ∂markovTrajectory (transitionKernel P) s) ≤ ENNReal.ofReal r := by
  cases n with
  | zero =>
      simpa [pathAvoid, avoid] using ENNReal.ofReal_le_ofReal (hUniform s)
  | succ n =>
      rw [trajectory_integral_prefix _ _ (pathAvoid_measurable target a (n+1))
        (a+n) (pathAvoid_depends target a n)]
      have hinner : Kernel.lmarginalPartialTraj (markovKernelSequence (transitionKernel P)) a (a+n)
          (pathAvoid target a (n+1)) = fun x => ENNReal.ofReal (avoid P target (n+1) (x a)) := by
        funext x
        exact lmarginal_pathAvoid P target n a x
      have ht := congrFun (Kernel.lmarginalPartialTraj_self
        (κ := markovKernelSequence (transitionKernel P))
        (a := 0) (b := a) (c := a+n) (Nat.zero_le _) (by omega)
        (pathAvoid_measurable target a (n+1))) (fun _ => s)
      rw [hinner] at ht
      rw [← ht]
      calc
        _ ≤ Kernel.lmarginalPartialTraj (markovKernelSequence (transitionKernel P)) 0 a
            (fun _ => ENNReal.ofReal r) (fun _ => s) :=
          Kernel.lmarginalPartialTraj_mono 0 a (fun x => ENNReal.ofReal_le_ofReal (hUniform (x a))) _
        _ = ENNReal.ofReal r := by simp [Kernel.lmarginalPartialTraj]

end HiddenParity.Recurrence
