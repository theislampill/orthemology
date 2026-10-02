import FiniteChainTrajectory
import RecurrentSupport

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped BigOperators ENNReal

namespace HiddenParity.Recurrence
open Orthemology.Tranche2

variable {S : Type*} [Fintype S] [DecidableEq S]
variable [MeasurableSpace S] [MeasurableSingletonClass S]

def AvoidInterval (target : S) (a n : ℕ) : Set (ℕ → S) :=
  {x | ∀ i < n, x (a+i) ≠ target}

instance avoidIntervalDecidable (target : S) (a n : ℕ) (x : ℕ → S) :
    Decidable (x ∈ AvoidInterval target a n) := by
  unfold AvoidInterval
  infer_instance

omit [Fintype S] [MeasurableSpace S] [MeasurableSingletonClass S] in
theorem pathAvoid_eq_ite (target : S) (a n : ℕ) (x : ℕ → S) :
    pathAvoid target a n x = if x ∈ AvoidInterval target a n then 1 else 0 := by
  induction n generalizing a with
  | zero => simp [pathAvoid, AvoidInterval]
  | succ n ih =>
      have hsplit : x ∈ AvoidInterval target a (n+1) ↔
          x a ≠ target ∧ x ∈ AvoidInterval target (a+1) n := by
        constructor
        · intro h
          refine ⟨by simpa using h 0 (Nat.zero_lt_succ n), ?_⟩
          intro i hi
          have hh := h (i+1) (by omega)
          simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hh
        · rintro ⟨h0, htail⟩ i hi
          cases i with
          | zero => simpa using h0
          | succ i =>
              have hh := htail i (by omega)
              simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hh
      rw [pathAvoid, ih]
      by_cases h0 : x a = target <;> by_cases htail : x ∈ AvoidInterval target (a+1) n <;>
        simp [h0, htail, hsplit]

omit [Fintype S] in
theorem avoidInterval_measurable (target : S) (a n : ℕ) :
    MeasurableSet (AvoidInterval target a n) := by
  convert (measurableSet_singleton (1 : ℝ≥0∞)).preimage (pathAvoid_measurable target a n) using 1
  ext x
  by_cases h : x ∈ AvoidInterval target a n <;> simp [pathAvoid_eq_ite, h]

omit [Fintype S] [MeasurableSpace S] [MeasurableSingletonClass S] in
theorem pathAvoid_eq_indicator (target : S) (a n : ℕ) :
    pathAvoid target a n = (AvoidInterval target a n).indicator (fun _ => (1 : ℝ≥0∞)) := by
  funext x
  rw [pathAvoid_eq_ite]
  by_cases h : x ∈ AvoidInterval target a n <;> simp [h]

/-- Actual finite-window avoidance probabilities inherit the dynamic-programming bound. -/
theorem interval_avoidance_probability_le (P : FiniteChain S) (target s : S)
    (a n : ℕ) (r : ℝ) (hUniform : ∀ t, avoid P target n t ≤ r) :
    markovTrajectory (transitionKernel P) s (AvoidInterval target a n) ≤ ENNReal.ofReal r := by
  rw [← lintegral_indicator_one (avoidInterval_measurable target a n)]
  change (∫⁻ x, (AvoidInterval target a n).indicator (fun _ => (1 : ℝ≥0∞)) x
    ∂markovTrajectory (transitionKernel P) s) ≤ _
  rw [← pathAvoid_eq_indicator]
  exact trajectory_interval_avoidance_bound P target s a n r hUniform

def ForeverAvoid (target : S) (a : ℕ) : Set (ℕ → S) :=
  {x | ∀ n, a ≤ n → x n ≠ target}

/-- Finite positive paths and normalized rows imply that eventual permanent
avoidance is a null event under the actual infinite Markov trajectory law. -/
theorem forever_avoid_null (P : FiniteChain S) (target s : S)
    (hReach : ∀ t, Relation.ReflTransGen (fun u v => 0 < P.prob u v) t target) (a : ℕ) :
    markovTrajectory (transitionKernel P) s (ForeverAvoid target a) = 0 := by
  obtain ⟨N, _, r, hr, hr1, hUniform⟩ := exists_uniform_avoidance_bound P target hReach
  have hBound : ∀ k : ℕ, markovTrajectory (transitionKernel P) s (ForeverAvoid target a) ≤
      ENNReal.ofReal (r^k) := by
    intro k
    apply (measure_mono (t := AvoidInterval target a (k*N)) ?_).trans
      (interval_avoidance_probability_le P target s a (k*N) (r^k)
        (fun t => avoid_blocks_bound P target N r hr hUniform k t))
    intro x hx i _
    exact hx (a+i) (Nat.le_add_right _ _)
  have hLim : Tendsto (fun k : ℕ => ENNReal.ofReal (r^k)) atTop (nhds 0) := by
    simpa using ENNReal.tendsto_ofReal (tendsto_pow_atTop_nhds_zero_of_lt_one hr hr1)
  apply le_antisymm _ (zero_le _)
  exact le_of_tendsto_of_tendsto tendsto_const_nhds hLim (Eventually.of_forall hBound)

/-- Every state that is reachable from every state is visited infinitely often
almost surely. Recurrence is a conclusion of finite-path probability bounds. -/
theorem target_recurs_almost_surely (P : FiniteChain S) (target s : S)
    (hReach : ∀ t, Relation.ReflTransGen (fun u v => 0 < P.prob u v) t target) :
    ∀ᵐ x ∂markovTrajectory (transitionKernel P) s, ∃ᶠ n in atTop, x n = target := by
  have hAll : ∀ᵐ x ∂markovTrajectory (transitionKernel P) s,
      ∀ a : ℕ, ∃ n, a ≤ n ∧ x n = target := by
    apply ae_all_iff.mpr
    intro a
    rw [ae_iff]
    have hset : {x : ℕ → S | ¬ ∃ n, a ≤ n ∧ x n = target} = ForeverAvoid target a := by
      ext x
      simp [ForeverAvoid]
    rw [hset]
    exact forever_avoid_null P target s hReach a
  exact hAll.mono (fun _ hx => frequently_atTop.mpr hx)

/-- A finite strongly connected positive-support chain visits every state
infinitely often under its constructed trajectory measure. -/
theorem all_states_recur_almost_surely (P : FiniteChain S) (s : S)
    (hStrong : ∀ u v, Relation.ReflTransGen (fun u v => 0 < P.prob u v) u v) :
    ∀ᵐ x ∂markovTrajectory (transitionKernel P) s, ∀ t, ∃ᶠ n in atTop, x n = t := by
  apply ae_all_iff.mpr
  intro t
  exact target_recurs_almost_surely P t s (fun u => hStrong u t)

end HiddenParity.Recurrence
