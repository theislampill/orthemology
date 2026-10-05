import LawCompletionCore

set_option autoImplicit false

namespace LawCompletion.ControlB

open Set Filter
open scoped Topology

/-- Branch n has n+1 points, numbered 0 through n; point 0 maps to r. -/
inductive State where
  | e
  | r
  | branch (n k : ℕ) (hk : k ≤ n)
  deriving DecidableEq

open State

instance : Nonempty State := ⟨e⟩

instance : MetricSpace State where
  dist x y := if x = y then 0 else 1
  dist_self x := by simp
  dist_comm x y := by
    obtain h | h := eq_or_ne x y
    · simp [h]
    · simp [h, h.symm]
  dist_triangle x y z := by
    by_cases x = y <;> by_cases x = z <;> by_cases y = z <;> simp_all
  eq_of_dist_eq_zero := by simp

@[simp] theorem dist_formula (x y : State) : dist x y = if x = y then 0 else 1 := rfl

instance : CompleteSpace State := by
  refine Metric.complete_of_cauchySeq_tendsto fun u hu => ?_
  obtain ⟨N, hN⟩ := Metric.cauchySeq_iff'.mp hu 1 zero_lt_one
  refine ⟨u N, tendsto_atTop_of_eventually_const (i₀ := N) ?_⟩
  intro n hn
  specialize hN n hn
  by_contra h
  simp [h] at hN

theorem bounded : Bornology.IsBounded (Set.univ : Set State) := by
  apply Metric.isBounded_iff.mpr
  refine ⟨1, fun x _ y _ => ?_⟩
  by_cases h : x = y <;> simp [h]

def law : State → State
  | e => e
  | r => e
  | branch n k hk => if h : k = 0 then r else branch n (k - 1) (by omega)

theorem law_continuous : Continuous law := by
  apply Metric.continuous_iff.mpr
  intro x ε hε
  refine ⟨1, zero_lt_one, ?_⟩
  intro y hy
  have hyx : y = x := by
    by_contra h
    simp [h] at hy
  subst y
  simpa using hε

private def tag : State → ℕ
  | branch n _ _ => n
  | _ => 0

private def height : State → ℕ
  | branch _ k _ => k
  | _ => 0

instance : Infinite State := Infinite.of_injective
  (fun n : ℕ => branch n 0 (Nat.zero_le n)) (fun _ _ h => congrArg tag h)

/-- A branch-point predecessor stays on that same finite branch and increases its index. -/
theorem branch_predecessor (x : State) (n k : ℕ) (hk : k ≤ n)
    (h : law x = branch n k hk) :
    ∃ j, ∃ hj : j ≤ n, x = branch n j hj ∧ j = k + 1 := by
  cases x with
  | e => simp [law] at h
  | r => simp [law] at h
  | branch m j hj =>
      by_cases hj0 : j = 0
      · simp [law, hj0] at h
      · have h' : branch m (j - 1) (by omega) = branch n k hk := by
          simpa [law, hj0] using h
        have hmn : m = n := congrArg tag h'
        have hjk : j - 1 = k := congrArg height h'
        subst m
        exact ⟨j, hj, rfl, by omega⟩

/-- An arbitrary depth-t predecessor cannot exceed the finite branch's capacity. -/
theorem branch_capacity (t : ℕ) (x : State) (n k : ℕ) (hk : k ≤ n)
    (h : law^[t] x = branch n k hk) : k + t ≤ n := by
  induction t generalizing n k with
  | zero => omega
  | succ t ih =>
      rw [Function.iterate_succ_apply'] at h
      obtain ⟨j, hj, hpred, hjk⟩ := branch_predecessor (law^[t] x) n k hk h
      have hcap := ih n j hj hpred
      omega

theorem branch_not_survives (n k : ℕ) (hk : k ≤ n) : ¬ Survives law (branch n k hk) := by
  intro h
  obtain ⟨x, hx⟩ := h (n + 1)
  have hcap := branch_capacity (n + 1) x n k hk hx
  omega

/-- Point k reaches r in exactly k+1 iterations, uniformly in the branch label. -/
theorem branch_reaches_r (n k : ℕ) (hk : k ≤ n) : law^[k + 1] (branch n k hk) = r := by
  induction k with
  | zero => simp [law]
  | succ k ih =>
      rw [Function.iterate_succ_apply]
      have hstep : law (branch n (k + 1) hk) = branch n k (by omega) := by simp [law]
      rw [hstep]
      exact ih (by omega)

theorem r_survives : Survives law r := by
  intro t
  cases t with
  | zero => exact ⟨r, rfl⟩
  | succ t => exact ⟨branch t t le_rfl, branch_reaches_r t t le_rfl⟩

/-- Exact finite-depth survival set: both e and r survive, and no branch point does. -/
theorem survival_exact (x : State) : Survives law x ↔ x = e ∨ x = r := by
  constructor
  · intro hx
    cases x with
    | e => exact Or.inl rfl
    | r => exact Or.inr rfl
    | branch n k hk => exact False.elim (branch_not_survives n k hk hx)
  · rintro (rfl | rfl)
    · exact fixed_survives law e rfl
    · exact r_survives

/-- Compatibility removes r as well: only the constant e sequence realizes the law. -/
theorem backward_exact (b : ℕ → State) : Backward law b ↔ b = fun _ => e := by
  constructor
  · intro hb
    funext i
    have hnext := (survival_exact (b (i + 1))).mp (backward_survives law b hb (i + 1))
    rw [hb i]
    rcases hnext with h | h <;> rw [h] <;> rfl
  · rintro rfl
    intro i
    rfl

theorem unique_backward : UniqueBackward law := by
  refine ⟨fun _ => e, (backward_exact _).mpr rfl, ?_⟩
  intro b hb
  exact (backward_exact b).mp hb

theorem not_singleton_survival : ¬ ∃ x, SingletonSurvival law x := by
  rintro ⟨x, hx⟩
  have he : e = x := (hx e).mp (fixed_survives law e rfl)
  have hr : r = x := (hx r).mp r_survives
  have : e = r := he.trans hr.symm
  cases this

/-- Every point reaches e after finitely many forward steps. -/
theorem eventually_fixed (x : State) : ∃ N : ℕ, law^[N] x = e := by
  cases x with
  | e => exact ⟨0, rfl⟩
  | r => exact ⟨1, rfl⟩
  | branch n k hk =>
      refine ⟨(k + 1) + 1, ?_⟩
      rw [Function.iterate_succ_apply', branch_reaches_r]
      rfl

theorem pointwise_attraction : PointwiseAttraction law e := by
  intro x
  obtain ⟨N, hN⟩ := eventually_fixed x
  apply tendsto_atTop_of_eventually_const (i₀ := N)
  intro n hn
  obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_le hn
  rw [add_comm N m, Function.iterate_add_apply, hN]
  clear hn
  induction m with
  | zero => rfl
  | succ m ih => rw [Function.iterate_succ_apply', ih]; rfl

/-- Complete/bounded/continuous countercontrol with pointwise attraction and unique realization,
    but with two finite-depth surviving states. -/
theorem counterexample : CompleteSpace State ∧ Infinite State ∧ Continuous law ∧ Bornology.IsBounded (Set.univ : Set State) ∧
    UniqueBackward law ∧ PointwiseAttraction law e ∧ ¬ ∃ x, SingletonSurvival law x :=
  ⟨inferInstance, inferInstance, law_continuous, bounded, unique_backward, pointwise_attraction, not_singleton_survival⟩

end LawCompletion.ControlB
