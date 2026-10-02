import Mathlib

/-! UNEXECUTED finite-flow equivalence candidates. No general fixed-point theorem
is postulated. The existence route is separately proved ordinarily by Cesàro
averages and by rational vertex enumeration in proofs/U08_FIXED_POINTS.md. -/
namespace P02A2.Flow
open scoped BigOperators
variable {ι κ : Type*} [Fintype ι] [Fintype κ]

noncomputable def allowed (A : ι → κ → ι → ℚ) (b : ι → κ → ℚ)
    (i : ι) (r : ι → ℚ) : Prop :=
  (∀ j, 0≤r j) ∧ (∑ j, r j)=1 ∧ ∀ l, (∑ j, A i l j*r j)≤b i l

noncomputable def feasibleFlow (A : ι → κ → ι → ℚ) (b : ι → κ → ℚ)
    (p : ι → ℚ) (f : ι → ι → ℚ) : Prop :=
  (∀ i, 0≤p i) ∧ (∑ i, p i)=1 ∧ (∀ i j, 0≤f i j) ∧
  (∀ i, (∑ j, f i j)=p i) ∧ (∀ j, (∑ i, f i j)=p j) ∧
  ∀ i l, (∑ j, A i l j*f i j)≤b i l*p i

theorem stationary_to_flow (A : ι → κ → ι → ℚ) (b : ι → κ → ℚ)
    (p : ι → ℚ) (r : ι → ι → ℚ)
    (hp : ∀ i, 0≤p i) (hpt : (∑ i,p i)=1)
    (hr : ∀ i, allowed A b i (r i))
    (hs : ∀ j, (∑ i,p i*r i j)=p j) :
    feasibleFlow A b p (fun i j => p i*r i j) := by
  refine ⟨hp,hpt,?_,?_,hs,?_⟩
  · intro i j; exact mul_nonneg (hp i) ((hr i).1 j)
  · intro i; rw [← Finset.mul_sum,(hr i).2.1,mul_one]
  · intro i l
    calc
      (∑ j,A i l j*(p i*r i j)) = p i*(∑ j,A i l j*r i j) := by
        rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro j hj; ring
      _ ≤ p i*b i l := mul_le_mul_of_nonneg_left ((hr i).2.2 l) (hp i)
      _ = b i l*p i := mul_comm _ _

theorem zero_row {p : ι → ℚ} {f : ι → ι → ℚ} (hn : ∀ i j, 0≤f i j)
    (hr : ∀ i, (∑ j,f i j)=p i) {i : ι} (hi : p i=0) (j : ι) : f i j=0 := by
  have hle : f i j ≤ ∑ k,f i k := Finset.single_le_sum (fun k hk => hn i k) (Finset.mem_univ j)
  rw [hr i,hi] at hle
  exact le_antisymm hle (hn i j)

theorem flow_to_stationary (A : ι → κ → ι → ℚ) (b : ι → κ → ℚ)
    (p : ι → ℚ) (f : ι → ι → ℚ)
    (hf : feasibleFlow A b p f)
    (hnonempty : ∀ i, ∃ r, allowed A b i r) :
    ∃ r : ι → ι → ℚ, (∀ i, allowed A b i (r i)) ∧
      (∀ i j, f i j=p i*r i j) ∧ (∀ j, (∑ i,p i*r i j)=p j) := by
  classical
  rcases hf with ⟨hp,hpt,hfn,hrow,hcol,hineq⟩
  let r : ι → ι → ℚ := fun i => if 0<p i then (fun j => f i j/p i) else Classical.choose (hnonempty i)
  have hallowed : ∀ i, allowed A b i (r i) := by
    intro i
    by_cases hi : 0<p i
    · simp only [r,if_pos hi]
      refine ⟨fun j => div_nonneg (hfn i j) (hp i),?_,?_⟩
      · rw [← Finset.sum_div,hrow i]; exact div_self (ne_of_gt hi)
      · intro l
        have hsum : (∑ j,A i l j*(f i j/p i))=(∑ j,A i l j*f i j)/p i := by
          rw [Finset.sum_div]; apply Finset.sum_congr rfl; intro j hj; ring
        rw [hsum]
        exact (div_le_iff₀ hi).mpr (hineq i l)
    · simp only [r,if_neg hi]
      exact Classical.choose_spec (hnonempty i)
  have hprod : ∀ i j, f i j=p i*r i j := by
    intro i j
    by_cases hi : 0<p i
    · simp only [r,if_pos hi]
      field_simp [ne_of_gt hi]
    · have hz : p i=0 := le_antisymm (not_lt.mp hi) (hp i)
      rw [hz,zero_mul]
      exact zero_row hfn hrow hz j
  refine ⟨r,hallowed,hprod,?_⟩
  intro j
  simpa only [← hprod] using hcol j
end P02A2.Flow
