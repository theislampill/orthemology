import FiniteReachability

/-! Quantitative finite-chain hitting from actual normalized row weights and a
positive directed path. No almost-sure hitting, fairness, termination, or
hitting-probability bound is assumed. The remaining law adapter must identify
these finite-step probabilities with the relevant history process. -/
noncomputable section
open scoped BigOperators
namespace HiddenParity.Cost.FiniteChainHitting
variable {Q : Type*} [Fintype Q]

structure Rows (Q : Type*) [Fintype Q] where
  row : Q → Q → ℝ
  nonneg : ∀ s t, 0 ≤ row s t
  normalized : ∀ s, ∑ t, row s t = 1

inductive Path (edge : Q → Q → Prop) : Q → Q → ℕ → Prop
  | nil (s : Q) : Path edge s s 0
  | cons {s u t : Q} {n : ℕ} : edge s u → Path edge u t n → Path edge s t (n+1)

def hit (P : Rows Q) (goal : Q → Prop) [DecidablePred goal] : ℕ → Q → ℝ
  | 0, s => if goal s then 1 else 0
  | n+1, s => if goal s then 1 else ∑ t, P.row s t * hit P goal n t

def survive (P : Rows Q) (goal : Q → Prop) [DecidablePred goal] : ℕ → Q → ℝ
  | 0, s => if goal s then 0 else 1
  | n+1, s => if goal s then 0 else ∑ t, P.row s t * survive P goal n t

@[simp] theorem hit_of_goal (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (n : ℕ) (s : Q) (hs : goal s) : hit P goal n s = 1 := by
  cases n <;> simp [hit,hs]

@[simp] theorem survive_of_goal (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (n : ℕ) (s : Q) (hs : goal s) : survive P goal n s = 0 := by
  cases n <;> simp [survive,hs]

theorem hit_nonneg (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (n : ℕ) (s : Q) : 0 ≤ hit P goal n s := by
  induction n generalizing s with
  | zero => simp only [hit]; split_ifs <;> norm_num
  | succ n ih =>
      simp only [hit]; split_ifs
      · norm_num
      · exact Finset.sum_nonneg (fun t _ => mul_nonneg (P.nonneg s t) (ih t))

theorem survive_nonneg (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (n : ℕ) (s : Q) : 0 ≤ survive P goal n s := by
  induction n generalizing s with
  | zero => simp only [survive]; split_ifs <;> norm_num
  | succ n ih =>
      simp only [survive]; split_ifs
      · norm_num
      · exact Finset.sum_nonneg (fun t _ => mul_nonneg (P.nonneg s t) (ih t))

theorem hit_add_survive (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (n : ℕ) (s : Q) : hit P goal n s + survive P goal n s = 1 := by
  induction n generalizing s with
  | zero => simp only [hit,survive]; split_ifs <;> norm_num
  | succ n ih =>
      simp only [hit,survive]; split_ifs
      · norm_num
      · rw [← Finset.sum_add_distrib]
        simp_rw [← mul_add,ih,mul_one]
        exact P.normalized s

theorem hit_le_one (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (n : ℕ) (s : Q) : hit P goal n s ≤ 1 := by
  have h := hit_add_survive P goal n s
  have h0 := survive_nonneg P goal n s
  linarith

theorem survive_le_one (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (n : ℕ) (s : Q) : survive P goal n s ≤ 1 := by
  have h := hit_add_survive P goal n s
  have h0 := hit_nonneg P goal n s
  linarith

theorem hit_mono (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (s : Q) : Monotone (fun n => hit P goal n s) := by
  apply monotone_nat_of_le_succ
  intro n
  induction n generalizing s with
  | zero =>
      by_cases hs : goal s
      · simp [hit,hs]
      · simpa only [hit,if_neg hs] using hit_nonneg P goal 1 s
  | succ n ih =>
      by_cases hs : goal s
      · simp [hit,hs]
      · simp only [hit,if_neg hs]
        exact Finset.sum_le_sum (fun t _ => mul_le_mul_of_nonneg_left (ih t) (P.nonneg s t))

/-- A particular n-edge path with each edge at least p forces hitting
probability at least p^n. Goals reached earlier can only help. -/
theorem path_probability_lower (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    {s t : Q} {n : ℕ} (path : Path (fun s t => p ≤ P.row s t) s t n)
    (ht : goal t) : p^n ≤ hit P goal n s := by
  induction path with
  | nil s => simp [hit,ht]
  | @cons s u t n he hpath ih =>
      by_cases hs : goal s
      · rw [hit_of_goal P goal _ _ hs]
        exact pow_le_one₀ hp hp1
      · simp only [hit,if_neg hs]
        calc
          p^(n+1) = p*p^n := by ring
          _ ≤ P.row s u * hit P goal n u := mul_le_mul he (ih ht) (pow_nonneg hp _) (P.nonneg s u)
          _ ≤ ∑ t, P.row s t * hit P goal n t :=
            Finset.single_le_sum (fun t _ => mul_nonneg (P.nonneg s t) (hit_nonneg P goal n t))
              (Finset.mem_univ u)

/-- Uniform lower transition probabilities turn a bounded positive path into
an explicit one-block hitting bound. This is not an assumed probability bound. -/
theorem positive_path_hitting_bound (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ s t, 0 < P.row s t → p ≤ P.row s t)
    (D : ℕ) (s : Q)
    (hpath : ∃ t n, goal t ∧ n ≤ D ∧ Path (fun u v => 0 < P.row u v) s t n) :
    p^D ≤ hit P goal D s := by
  obtain ⟨t,n,ht,hn,path⟩ := hpath
  have path' : Path (fun s t => p ≤ P.row s t) s t n := by
    clear ht hn
    induction path with
    | nil s => exact Path.nil s
    | cons he _ ih => exact Path.cons (hmin _ _ he) ih
  calc
    p^D ≤ p^n := pow_le_pow_of_le_one hp hp1 hn
    _ ≤ hit P goal n s := path_probability_lower P goal p hp hp1 path' ht
    _ ≤ hit P goal D s := hit_mono P goal s hn

/-- A uniform D-step survival bound propagates after any preceding n steps.
The proof uses normalized nonnegative rows, not independence of separate blocks. -/
theorem survive_add_le (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (D : ℕ) (b : ℝ) (hD : ∀ s, survive P goal D s ≤ b) :
    ∀ n s, survive P goal (n+D) s ≤ b * survive P goal n s := by
  intro n
  induction n with
  | zero =>
      intro s
      by_cases hs : goal s
      · simp [hs]
      · simpa [survive,hs] using hD s
  | succ n ih =>
      intro s
      by_cases hs : goal s
      · simp [hs]
      · rw [Nat.succ_add]
        simp only [survive,if_neg hs]
        calc
          (∑ t, P.row s t * survive P goal (n+D) t) ≤
              ∑ t, P.row s t * (b * survive P goal n t) :=
            Finset.sum_le_sum (fun t _ => mul_le_mul_of_nonneg_left (ih t) (P.nonneg s t))
          _ = b * ∑ t, P.row s t * survive P goal n t := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro t _
            ring

/-- Geometric survival tail from positive paths in the actual row graph.
Every state may have a different path; no deterministic fixed path or iid
block assertion is needed. -/
theorem geometric_survival_bound (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ s t, 0 < P.row s t → p ≤ P.row s t)
    (D : ℕ) (hpaths : ∀ s, ∃ t n, goal t ∧ n ≤ D ∧ Path (fun u v => 0 < P.row u v) s t n) :
    ∀ k s, survive P goal (k*D) s ≤ (1-p^D)^k := by
  have hr : 0 ≤ 1-p^D := by have := pow_le_one₀ hp hp1 (n:=D); linarith
  have hD : ∀ s, survive P goal D s ≤ 1-p^D := by
    intro s
    have hh := positive_path_hitting_bound P goal p hp hp1 hmin D s (hpaths s)
    have he := hit_add_survive P goal D s
    linarith
  intro k
  induction k with
  | zero => intro s; simpa using survive_le_one P goal 0 s
  | succ k ih =>
      intro s
      rw [Nat.succ_mul]
      calc
        survive P goal (k*D+D) s ≤ (1-p^D)*survive P goal (k*D) s :=
          survive_add_le P goal D (1-p^D) hD (k*D) s
        _ ≤ (1-p^D)*(1-p^D)^k := mul_le_mul_of_nonneg_left (ih s) hr
        _ = (1-p^D)^(k+1) := by ring

end HiddenParity.Cost.FiniteChainHitting
