import P02A2.Stationary
import Mathlib

/-! UNEXECUTED finite row-set correspondence, reduced to the proved-source
Cesàro route rather than an assumed Kakutani declaration. -/
namespace P02A2.SimplexStationary
open Set
open scoped BigOperators
variable {ι : Type*} [Fintype ι]

def simplex : Set (ι → ℝ) := {p | (∀ i, 0≤p i) ∧ ∑ i,p i=1}

theorem simplex_closed : IsClosed (simplex (ι := ι)) := by
  have h0 : IsClosed {p : ι → ℝ | ∀ i, 0≤p i} := by
    simp only [setOf_forall]
    exact isClosed_iInter (fun i => isClosed_le continuous_const (continuous_apply i))
  have h1 : IsClosed {p : ι → ℝ | ∑ i,p i=1} :=
    isClosed_eq (by fun_prop) continuous_const
  exact h0.inter h1

theorem simplex_compact : IsCompact (simplex (ι := ι)) := by
  apply (isCompact_Icc : IsCompact (Icc (0 : ι → ℝ) 1)).of_isClosed_subset simplex_closed
  intro p hp
  refine ⟨hp.1,fun j => ?_⟩
  have hs : p j≤∑ i,p i := Finset.single_le_sum (fun i _ => hp.1 i) (Finset.mem_univ j)
  simpa only [hp.2, Pi.one_apply] using hs

theorem simplex_convex : Convex ℝ (simplex (ι := ι)) := by
  intro x hx y hy a b ha hb hab
  refine ⟨fun i => ?_,?_⟩
  · change 0≤a*x i+b*y i
    exact add_nonneg (mul_nonneg ha (hx.1 i)) (mul_nonneg hb (hy.1 i))
  · change ∑ i,(a*x i+b*y i)=1
    rw [Finset.sum_add_distrib,← Finset.mul_sum,← Finset.mul_sum,hx.2,hy.2]
    linarith

noncomputable def rowLinear (r : ι → ι → ℝ) : (ι → ℝ) →ₗ[ℝ] (ι → ℝ) where
  toFun p j := ∑ i,p i*r i j
  map_add' p q := by ext j; simp [add_mul,Finset.sum_add_distrib]
  map_smul' a p := by ext j; simp [mul_assoc,Finset.mul_sum]

noncomputable def rowContinuous (r : ι → ι → ℝ) : (ι → ℝ) →L[ℝ] (ι → ℝ) :=
  (rowLinear r).toContinuousLinearMap

theorem rows_preserve_simplex (r : ι → ι → ℝ) (hr : ∀ i, r i ∈ simplex) :
    MapsTo (rowContinuous r) simplex simplex := by
  intro p hp
  change (∀ j,0≤∑ i,p i*r i j) ∧ (∑ j,∑ i,p i*r i j)=1
  constructor
  · intro j
    exact Finset.sum_nonneg (fun i _ => mul_nonneg (hp.1 i) ((hr i).1 j))
  · rw [Finset.sum_comm]
    simp_rw [← Finset.mul_sum,fun i => (hr i).2,mul_one]
    exact hp.2

theorem stationary_row [Nonempty ι] (r : ι → ι → ℝ) (hr : ∀ i,r i ∈ simplex) :
    ∃ p ∈ simplex, rowLinear r p=p := by
  classical
  let i0 : ι := Classical.choice (inferInstance : Nonempty ι)
  exact Stationary.compact_convex_linear_fixed simplex simplex_compact
    ⟨r i0,hr i0⟩ simplex_convex (rowContinuous r) (rows_preserve_simplex r hr)

noncomputable def correspondence (R : ι → Set (ι → ℝ)) (p : ι → ℝ) : Set (ι → ℝ) :=
  {q | ∃ r : ι → ι → ℝ, (∀ i,r i ∈ R i) ∧ q=rowLinear r p}

theorem finite_correspondence_fixed [Nonempty ι] (R : ι → Set (ι → ℝ))
    (hne : ∀ i,(R i).Nonempty) (hinside : ∀ i,R i ⊆ simplex) :
    ∃ p ∈ simplex, p ∈ correspondence R p := by
  classical
  choose r hr using hne
  obtain ⟨p,hp,hfix⟩ := stationary_row r (fun i => hinside i (hr i))
  exact ⟨p,hp,r,hr,hfix.symm⟩
end P02A2.SimplexStationary
