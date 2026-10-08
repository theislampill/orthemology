import LawCompletionCore

set_option autoImplicit false

namespace LawCompletion.ControlA

open Set Filter
open scoped Topology

/-- A fresh infinite type prevents accidental use of Nat's ordinary unbounded metric. -/
def State := Option ℕ

instance : Nonempty State := ⟨none⟩
instance : Infinite State := inferInstanceAs (Infinite (Option ℕ))
instance : DecidableEq State := inferInstanceAs (DecidableEq (Option ℕ))

/-- The complete bounded 0/1 discrete metric used by the counterexample. -/
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
  | none => none
  | some n => some (n + 1)

/-- All self-maps of this discrete metric are continuous; this verifies the specific law. -/
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

@[simp] theorem law_none : law none = none := rfl
@[simp] theorem law_some (k : ℕ) : law (some k) = some (k + 1) := rfl

@[simp] theorem iterate_none (n : ℕ) : law^[n] none = none := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih, law_none]

@[simp] theorem iterate_some (n k : ℕ) : law^[n] (some k) = some (k + n) := by
  induction n with
  | zero => simp
  | succ n ih => rw [Function.iterate_succ_apply', ih, law_some]; congr 1

/-- Exact range membership at every depth, with no finite cutoff. -/
theorem range_formula (n : ℕ) (x : State) :
    x ∈ Set.range (law^[n]) ↔ x = none ∨ ∃ k : ℕ, x = some k ∧ n ≤ k := by
  constructor
  · rintro ⟨y, rfl⟩
    cases y with
    | none => exact Or.inl (iterate_none n)
    | some k => exact Or.inr ⟨k + n, iterate_some n k, by omega⟩
  · rintro (rfl | ⟨k, rfl, hnk⟩)
    · exact ⟨none, iterate_none n⟩
    · refine ⟨some (k - n), ?_⟩
      rw [iterate_some, Nat.sub_add_cancel hnk]

theorem singleton_survival : SingletonSurvival law none := by
  intro x
  constructor
  · intro hx
    cases x with
    | none => rfl
    | some k =>
        obtain ⟨y, hy⟩ := hx (k + 1)
        cases y with
        | none => simp at hy
        | some m =>
            have heq : m + (k + 1) = k := Option.some.inj ((iterate_some (k + 1) m).symm.trans hy)
            omega
  · intro hx
    subst x
    exact fixed_survives law none rfl

theorem unique_backward : UniqueBackward law :=
  singleton_unique_backward law none singleton_survival

/-- Every actual infinite realization is the all-none sequence. -/
theorem backward_exact (b : ℕ → State) : Backward law b ↔ b = fun _ => none := by
  constructor
  · intro hb
    funext i
    exact (singleton_survival (b i)).mp (backward_survives law b hb i)
  · rintro rfl
    intro i
    rfl

/-- Every natural start stays distance exactly 1 from the fixed point at every time. -/
theorem orbit_distance (n k : ℕ) : dist (law^[n] (some k)) none = 1 := by
  rw [iterate_some, dist_formula]
  rfl

theorem orbit_not_tendsto (k : ℕ) :
    ¬ Tendsto (fun n : ℕ => law^[n] (some k)) atTop (𝓝 (none : State)) := by
  intro h
  obtain ⟨N, hN⟩ := Metric.tendsto_atTop.mp h 1 zero_lt_one
  have hbad := hN N le_rfl
  rw [orbit_distance] at hbad
  exact (lt_irrefl 1) hbad

theorem not_pointwise_attraction : ¬ PointwiseAttraction law none := by
  intro h
  exact orbit_not_tendsto 0 (h (some 0))

/-- The same failure holds from a point already in the law's image. -/
theorem image_start_failure : (some 1 : State) ∈ Set.range law ∧
    ¬ Tendsto (fun n : ℕ => law^[n] (some 1)) atTop (𝓝 (none : State)) :=
  ⟨⟨some 0, rfl⟩, orbit_not_tendsto 1⟩

/-- There is no other fixed point to which pointwise attraction could be redirected. -/
theorem no_attracting_fixed_point : ¬ ∃ e : State, law e = e ∧ PointwiseAttraction law e := by
  rintro ⟨e, he, ha⟩
  have heq : e = none := (singleton_unique_fixed law none singleton_survival e).mp he
  rw [heq] at ha
  exact not_pointwise_attraction ha

/-- Packaged infinite complete/bounded/continuous countercontrol. -/
theorem counterexample : CompleteSpace State ∧ Infinite State ∧ Continuous law ∧ Bornology.IsBounded (Set.univ : Set State) ∧
    SingletonSurvival law none ∧ UniqueBackward law ∧ ¬ PointwiseAttraction law none :=
  ⟨inferInstance, inferInstance, law_continuous, bounded, singleton_survival, unique_backward, not_pointwise_attraction⟩

end LawCompletion.ControlA
