import ClusterConcentration

namespace ContaminationAlgebra
noncomputable section
open Finset

/-- Exact all-zero word algebra. A is the original total joint word mass;
M is its largest accepted hypothesis mass. No unimodality is required. -/
theorem endpoint_increment (theta s A M : ℝ) :
    theta+s*A-max theta (s*M) = s*(A-M)+min theta (s*M) := by
  rcases le_total theta (s*M) with h|h
  · rw [max_eq_right h,min_eq_left h]
    ring
  · rw [max_eq_left h,min_eq_right h]
    ring

lemma increment_nonnegative {theta s M : ℝ} (ht : 0≤theta) (hs : 0≤s) (hm : 0≤M) :
    0 ≤ min theta (s*M) := le_min ht (mul_nonneg hs hm)

lemma increment_le_theta (theta s M : ℝ) : min theta (s*M)≤theta := min_le_left _ _

/-- The finite-horizon increment is bounded by theta times the true report count. -/
theorem finite_increment_bound (N : ℕ) (theta s : ℝ) (M : ℕ → ℝ)
    (ht : 0≤theta) (hs : 0≤s) (hM : ∀ n, 0≤M n) :
    0≤∑ n ∈ range N, min theta (s*M (n+1)) ∧
    (∑ n ∈ range N, min theta (s*M (n+1)))≤theta*(N:ℝ) := by
  constructor
  · exact sum_nonneg (fun n hn => increment_nonnegative ht hs (hM (n+1)))
  · calc
      _ ≤ ∑ _n ∈ range N, theta := sum_le_sum (fun n hn => min_le_left _ _)
      _ = _ := by simp;ring

/-- Total cost, rather than just the scaled-baseline increment, is continuous
at a fixed horizon once the displayed exact decomposition is established. -/
theorem total_cost_lipschitz {theta N C D T : ℝ} (ht : 0≤theta)
    (hC : 0≤C) (hCN : C≤N) (hD : 0≤D) (hDN : D≤theta*N)
    (hT : T=(1-theta)*C+D) : |T-C|≤theta*N := by
  rw [abs_le]
  have hmul := mul_le_mul_of_nonneg_left hCN ht
  constructor <;> nlinarith [mul_nonneg ht hC]

/-- All scores in a selected small set are charged when the endpoint dominates
them individually, even if a large interior hypothesis wins the word. -/
theorem small_mass_lower {I : Type*} [DecidableEq I] (s small : Finset I)
    (f : I → ℝ) (theta : ℝ) (j : I)
    (hsub : small⊆s) (hj : j∈s) (hf : ∀ i∈s, 0≤f i)
    (ht : 0≤theta) (hsmall : ∀ i∈small, f i≤theta) :
    (∑ i∈small, f i) ≤ theta+(∑ i∈s, f i)-max theta (f j) := by
  by_cases h : f j≤theta
  · rw [max_eq_left h]
    have hsum := sum_le_sum_of_subset_of_nonneg hsub (fun i hi hnot => hf i hi)
    linarith
  · have hjnot : j∉small := by
      intro hmem
      exact h (hsmall j hmem)
    have hsub' : small⊆s.erase j := by
      intro i hi
      exact mem_erase.mpr ⟨by intro h;subst i;exact hjnot hi,hsub hi⟩
    have hsum := sum_le_sum_of_subset_of_nonneg hsub'
      (fun i hi hnot => hf i (mem_of_mem_erase hi))
    have hsplit := sum_erase_add s f hj
    rw [max_eq_right (le_of_not_ge h)]
    linarith

def runningMax (f : ℕ → ℝ) : ℕ → ℝ
  | 0 => f 0
  | n+1 => max (runningMax f n) (f (n+1))

lemma last_le_runningMax (f : ℕ → ℝ) (n : ℕ) : f n≤runningMax f n := by
  cases n with
  | zero => rfl
  | succ n => exact le_max_right _ _

lemma runningMax_dominates (f : ℕ → ℝ) {i n : ℕ} (h : i≤n) : f i≤runningMax f n := by
  induction n with
  | zero =>
    have hi : i=0 := by omega
    subst i
    rfl
  | succ n ih =>
    rcases Nat.eq_or_lt_of_le h with he|hl
    · subst i
      exact last_le_runningMax f (n+1)
    · exact (ih (by omega)).trans (le_max_left _ _)

/-- Arbitrary finite score sequences have only a one-sided adjacent-minimum
bound. This replaces the invalid arbitrary-weight equality shortcut. -/
theorem adjacent_min_lower (f : ℕ → ℝ) (n : ℕ) :
    (∑ i∈range n, min (f i) (f (i+1)))+runningMax f n ≤
      ∑ i∈range (n+1), f i := by
  induction n with
  | zero => simp [runningMax]
  | succ n ih =>
    rw [sum_range_succ,show n+1+1=(n+1)+1 from rfl,sum_range_succ]
    change (∑ i∈range n, min (f i) (f (i+1)))+min (f n) (f (n+1))+
      max (runningMax f n) (f (n+1)) ≤ (∑ i∈range (n+1),f i)+f (n+1)
    have hm := min_le_min_right (f (n+1)) (last_le_runningMax f n)
    have he := min_add_max (runningMax f n) (f (n+1))
    linarith

/-- A concrete non-unimodal zero-prefix score vector rejects equality. -/
theorem adjacency_equality_counterexample :
    ((9/40:ℝ)+(3/40)+(63/160)-max (max (9/40) (3/40)) (63/160)=3/10) ∧
    (min (9/40:ℝ) (3/40)+min (3/40) (63/160)=3/20) := by
  norm_num

#print axioms endpoint_increment
#print axioms finite_increment_bound
#print axioms total_cost_lipschitz
#print axioms small_mass_lower
#print axioms adjacent_min_lower
#print axioms adjacency_equality_counterexample
end
end ContaminationAlgebra
