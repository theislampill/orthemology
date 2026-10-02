import Mathlib.Analysis.Convex.Combination
import Mathlib.Topology.Sequences
import Mathlib

/-! UNEXECUTED direct compact-convex linear fixed-point route. This is NOT an
assumption named Kakutani. Its approximate fixed points are constructed. -/
namespace P02A2.Stationary
open Set Filter
open scoped Topology BigOperators
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem fixed_of_approximate {K : Set E} (hK : IsCompact K)
    {T : E → E} (hT : Continuous T) {u : ℕ → E} (hu : ∀ n, u n ∈ K)
    (ha : Tendsto (fun n => T (u n)-u n) atTop (𝓝 0)) :
    ∃ p ∈ K, T p=p := by
  obtain ⟨p,hp,φ,hφ,hlim⟩ := hK.tendsto_subseq hu
  refine ⟨p,hp,?_⟩
  have h1 : Tendsto (fun n => T (u (φ n))-u (φ n)) atTop (𝓝 (T p-p)) :=
    (hT.tendsto p |>.comp hlim).sub hlim
  have h0 : Tendsto (fun n => T (u (φ n))-u (φ n)) atTop (𝓝 0) :=
    ha.comp hφ.tendsto_atTop
  exact sub_eq_zero.mp (tendsto_nhds_unique h1 h0)

def orbit (T : E →L[ℝ] E) (x : E) : ℕ → E
  | 0 => x
  | n+1 => T (orbit T x n)

noncomputable def average (T : E →L[ℝ] E) (x : E) (n : ℕ) : E :=
  (1/((n:ℝ)+1)) • ∑ k ∈ Finset.range (n+1), orbit T x k

theorem orbit_mem {K : Set E} (T : E →L[ℝ] E) (hT : MapsTo T K K)
    {x : E} (hx : x ∈ K) (n : ℕ) : orbit T x n ∈ K := by
  induction n with
  | zero => exact hx
  | succ n ih => exact hT ih

theorem average_mem {K : Set E} (hK : Convex ℝ K) (T : E →L[ℝ] E)
    (hT : MapsTo T K K) {x : E} (hx : x ∈ K) (n : ℕ) : average T x n ∈ K := by
  have hpos : (0:ℝ)<(n:ℝ)+1 := by positivity
  have hw : (∑ _k ∈ Finset.range (n+1), (1/((n:ℝ)+1))) = 1 := by
    simp only [Finset.sum_const, Finset.card_range, nsmul_eq_mul, Nat.cast_add, Nat.cast_one]
    field_simp
  have h := hK.sum_mem (t := Finset.range (n+1))
    (w := fun _ => 1/((n:ℝ)+1)) (z := orbit T x)
    (fun _ _ => le_of_lt (one_div_pos.mpr hpos)) hw (fun k _ => orbit_mem T hT hx k)
  simpa only [average, Finset.smul_sum] using h

theorem orbit_sum_difference (T : E →L[ℝ] E) (x : E) (n : ℕ) :
    (∑ k ∈ Finset.range n, T (orbit T x k)) -
      (∑ k ∈ Finset.range n, orbit T x k) = orbit T x n-x := by
  induction n with
  | zero => simp [orbit]
  | succ n ih =>
    rw [Finset.sum_range_succ, Finset.sum_range_succ]
    have hnext : T (orbit T x n)=orbit T x (n+1) := rfl
    rw [hnext]
    calc
      _ = ((∑ k ∈ Finset.range n, T (orbit T x k)) -
        (∑ k ∈ Finset.range n, orbit T x k)) + (orbit T x (n+1)-orbit T x n) := by abel
      _ = _ := by rw [ih]; abel

theorem average_difference (T : E →L[ℝ] E) (x : E) (n : ℕ) :
    T (average T x n)-average T x n =
      (1/((n:ℝ)+1)) • (orbit T x (n+1)-x) := by
  simp only [average, map_smul, map_sum]
  rw [← smul_sub, orbit_sum_difference]

theorem average_difference_norm (T : E →L[ℝ] E) (x : E) (M : ℝ)
    (hM : ∀ n, ‖orbit T x n‖ ≤ M) (n : ℕ) :
    ‖T (average T x n)-average T x n‖ ≤ (2*M)/((n:ℝ)+1) := by
  have hpos : (0:ℝ)<(n:ℝ)+1 := by positivity
  rw [average_difference, norm_smul, Real.norm_eq_abs,
    abs_of_nonneg (le_of_lt (one_div_pos.mpr hpos))]
  have hX : ‖x‖≤M := by simpa [orbit] using hM 0
  have hB : ‖orbit T x (n+1)-x‖ ≤ 2*M :=
    (norm_sub_le _ _).trans (by linarith [hM (n+1)])
  calc
    _ ≤ (1/((n:ℝ)+1))*(2*M) := mul_le_mul_of_nonneg_left hB (by positivity)
    _ = _ := by ring

theorem averages_approximate (T : E →L[ℝ] E) (x : E) (M : ℝ)
    (hM : ∀ n, ‖orbit T x n‖ ≤ M) :
    Tendsto (fun n => T (average T x n)-average T x n) atTop (𝓝 0) := by
  apply Metric.tendsto_atTop.mpr
  intro ε hε
  obtain ⟨N,hN⟩ := exists_nat_gt ((2*M)/ε)
  refine ⟨N,fun n hn => ?_⟩
  rw [dist_zero_right]
  apply lt_of_le_of_lt (average_difference_norm T x M hM n)
  apply (div_lt_iff₀ (by positivity : (0:ℝ)<(n:ℝ)+1)).mpr
  have hN' : 2*M<(N:ℝ)*ε := (div_lt_iff₀ hε).mp hN
  have hcast : (N:ℝ)≤(n:ℝ) := by exact_mod_cast hn
  nlinarith

theorem compact_convex_linear_fixed (K : Set E) (hK : IsCompact K)
    (hne : K.Nonempty) (hc : Convex ℝ K) (T : E →L[ℝ] E) (hT : MapsTo T K K) :
    ∃ p ∈ K, T p=p := by
  obtain ⟨x,hx⟩ := hne
  obtain ⟨z,hz,hmax⟩ := hK.exists_isMaxOn ⟨x,hx⟩ continuous_norm.continuousOn
  apply fixed_of_approximate hK T.continuous (fun n => average_mem hc T hT hx n)
  exact averages_approximate T x ‖z‖ (fun n => hmax (orbit_mem T hT hx n))
end P02A2.Stationary
