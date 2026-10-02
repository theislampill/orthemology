import Mathlib

namespace HiddenParity.Recurrence
open scoped BigOperators

variable {S : Type*} [Fintype S] [DecidableEq S]

/-- An actual finite normalized transition table. -/
structure FiniteChain (S : Type*) [Fintype S] where
  prob : S → S → ℝ
  nonnegative : ∀ s t, 0 ≤ prob s t
  normalized : ∀ s, ∑ t, prob s t = 1

/-- Probability of avoiding the target at times 0,...,n-1. -/
def avoid (P : FiniteChain S) (target : S) : ℕ → S → ℝ
  | 0, _ => 1
  | n+1, s => if s = target then 0 else ∑ t, P.prob s t * avoid P target n t

theorem avoid_nonnegative (P : FiniteChain S) (target : S) (n : ℕ) (s : S) :
    0 ≤ avoid P target n s := by
  induction n generalizing s with
  | zero => norm_num [avoid]
  | succ n ih =>
      simp only [avoid]
      split_ifs
      · exact le_refl _
      · exact Finset.sum_nonneg (fun t _ => mul_nonneg (P.nonnegative s t) (ih t))

theorem avoid_le_one (P : FiniteChain S) (target : S) (n : ℕ) (s : S) :
    avoid P target n s ≤ 1 := by
  induction n generalizing s with
  | zero => exact le_refl _
  | succ n ih =>
      simp only [avoid]
      split_ifs
      · norm_num
      · calc
          ∑ t, P.prob s t * avoid P target n t ≤ ∑ t, P.prob s t * 1 :=
            Finset.sum_le_sum (fun t _ => mul_le_mul_of_nonneg_left (ih t) (P.nonnegative s t))
          _ = 1 := by simpa using P.normalized s

theorem avoid_succ_le (P : FiniteChain S) (target : S) (n : ℕ) (s : S) :
    avoid P target (n+1) s ≤ avoid P target n s := by
  induction n generalizing s with
  | zero => exact avoid_le_one P target 1 s
  | succ n ih =>
      simp only [avoid]
      split_ifs
      · exact le_refl _
      · exact Finset.sum_le_sum (fun t _ =>
          mul_le_mul_of_nonneg_left (ih t) (P.nonnegative s t))

theorem avoid_antitone (P : FiniteChain S) (target : S) (s : S) :
    Antitone (fun n => avoid P target n s) :=
  antitone_nat_of_succ_le (fun n => avoid_succ_le P target n s)

/-- A positive concrete edge followed by a finite positive chance to hit the
target yields a positive chance to hit from its source. -/
theorem avoid_lt_one_predecessor (P : FiniteChain S) (target : S)
    {s t : S} {n : ℕ} (hEdge : 0 < P.prob s t) (hHit : avoid P target n t < 1) :
    avoid P target (n+1) s < 1 := by
  by_cases hs : s = target
  · simp [avoid, hs]
  · rw [avoid, if_neg hs, ← P.normalized s]
    apply Finset.sum_lt_sum
    · intro u _
      exact (mul_le_mul_of_nonneg_left (avoid_le_one P target n u) (P.nonnegative s u)).trans_eq (mul_one _)
    · exact ⟨t, Finset.mem_univ t, by nlinarith⟩

/-- Finite positive-support reachability derives finite-horizon positive hitting. -/
theorem reachable_avoids_lt_one (P : FiniteChain S) (target s : S)
    (hReach : Relation.ReflTransGen (fun s t => 0 < P.prob s t) s target) :
    ∃ n, avoid P target n s < 1 := by
  induction hReach using Relation.ReflTransGen.head_induction_on with
  | refl => exact ⟨1, by simp [avoid]⟩
  | @head s t hst _ ih =>
      obtain ⟨n, hn⟩ := ih
      exact ⟨n+1, avoid_lt_one_predecessor P target hst hn⟩

/-- A finite family of positive paths gives one common finite block and a strict
numerical avoidance factor. Neither is supplied as an assumption. -/
theorem exists_uniform_avoidance_bound (P : FiniteChain S) (target : S)
    (hReach : ∀ s, Relation.ReflTransGen (fun s t => 0 < P.prob s t) s target) :
    ∃ N : ℕ, 0 < N ∧ ∃ r : ℝ, 0 ≤ r ∧ r < 1 ∧ ∀ s, avoid P target N s ≤ r := by
  classical
  choose n hn using fun s => reachable_avoids_lt_one P target s (hReach s)
  let N := Finset.univ.sup n + 1
  have hN : ∀ s, n s ≤ N := fun s =>
    (Finset.le_sup (Finset.mem_univ s)).trans (Nat.le_succ _)
  have hlt : ∀ s, avoid P target N s < 1 := fun s =>
    (avoid_antitone P target s (hN s)).trans_lt (hn s)
  obtain ⟨s, _, hmax⟩ := (Finset.univ : Finset S).exists_max_image (avoid P target N)
    ⟨target, Finset.mem_univ target⟩
  exact ⟨N, Nat.zero_lt_succ _, avoid P target N s, avoid_nonnegative P target N s,
    hlt s, fun t => hmax t (Finset.mem_univ t)⟩

/-- Uniform future avoidance factors through an arbitrary earlier prefix. -/
theorem avoid_add_bound (P : FiniteChain S) (target : S) (n m : ℕ) (r : ℝ)
    (hUniform : ∀ s, avoid P target m s ≤ r) (s : S) :
    avoid P target (n+m) s ≤ r * avoid P target n s := by
  induction n generalizing s with
  | zero => simpa [avoid] using hUniform s
  | succ n ih =>
      rw [Nat.succ_add]
      simp only [avoid]
      by_cases hs : s = target
      · simp [hs]
      · simp only [if_neg hs]
        calc
          ∑ t, P.prob s t * avoid P target (n+m) t ≤
              ∑ t, P.prob s t * (r * avoid P target n t) :=
            Finset.sum_le_sum (fun t _ => mul_le_mul_of_nonneg_left (ih t) (P.nonnegative s t))
          _ = r * ∑ t, P.prob s t * avoid P target n t := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro t _
            ring

/-- Quantitative geometric hitting bound, derived from the normalized dynamics. -/
theorem avoid_blocks_bound (P : FiniteChain S) (target : S) (N : ℕ) (r : ℝ)
    (hr : 0 ≤ r) (hUniform : ∀ s, avoid P target N s ≤ r) (k : ℕ) (s : S) :
    avoid P target (k*N) s ≤ r^k := by
  induction k with
  | zero => simp [avoid]
  | succ k ih =>
      rw [Nat.succ_mul, pow_succ']
      exact (avoid_add_bound P target (k*N) N r hUniform s).trans
        (mul_le_mul_of_nonneg_left ih hr)

end HiddenParity.Recurrence
