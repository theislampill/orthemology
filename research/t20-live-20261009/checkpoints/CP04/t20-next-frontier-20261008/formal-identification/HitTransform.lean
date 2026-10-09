import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Finset.BooleanAlgebra
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# Finite hit-transform identification

A histogram records the multiplicity of every finite effect set.  A hit query
counts all effects intersecting its argument.  For an arbitrary finite effect
universe, all nonempty hit queries identify the histogram once its invisible
empty-effect coordinate is fixed.
-/

namespace CalibratedIdentification

open scoped BigOperators

variable {E : Type*} [Fintype E] [DecidableEq E]

/-- Number of histogram entries whose effect set intersects the query. -/
def hit (n : Finset E → ℕ) (U : Finset E) : ℕ :=
  ∑ T : Finset E, if (T ∩ U).Nonempty then n T else 0

/-- This definition is exactly the powerset-indexed hit sum. -/
theorem hit_eq_powerset_filter_sum (n : Finset E → ℕ) (U : Finset E) :
    hit n U = ∑ T ∈ (Finset.univ : Finset E).powerset.filter
      (fun T => (T ∩ U).Nonempty), n T := by
  simp [hit, Finset.sum_filter]

/-- The subset (zeta) transform of a histogram. -/
def subsetMass (n : Finset E → ℕ) (S : Finset E) : ℕ :=
  ∑ T : Finset E, if T ⊆ S then n T else 0

@[simp] theorem hit_empty (n : Finset E → ℕ) : hit n ∅ = 0 := by
  simp [hit]

/-- The zeta transform is equivalently a sum over the powerset. -/
theorem subsetMass_eq_powerset_sum (n : Finset E → ℕ) (S : Finset E) :
    subsetMass n S = ∑ T ∈ S.powerset, n T := by
  classical
  have hf : Finset.univ.filter (fun T : Finset E => T ⊆ S) = S.powerset := by
    ext T
    simp
  rw [subsetMass, ← Finset.sum_filter, hf]

@[simp] theorem subsetMass_empty (n : Finset E → ℕ) : subsetMass n ∅ = n ∅ := by
  rw [subsetMass_eq_powerset_sum]
  simp

/-- Hitting the complement and being contained in the set partition all effects. -/
theorem hit_compl_add_subsetMass (n : Finset E → ℕ) (S : Finset E) :
    hit n Sᶜ + subsetMass n S = ∑ T : Finset E, n T := by
  classical
  unfold hit subsetMass
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro T _
  by_cases h : T ⊆ S
  · have hn : ¬(T ∩ Sᶜ).Nonempty := by
      rintro ⟨x, hx⟩
      have hx' := Finset.mem_inter.mp hx
      exact (Finset.mem_compl.mp hx'.2) (h hx'.1)
    simp [h, hn]
  · obtain ⟨x, hx, hxs⟩ := Finset.not_subset.mp h
    have hy : (T ∩ Sᶜ).Nonempty :=
      ⟨x, Finset.mem_inter.mpr ⟨hx, Finset.mem_compl.mpr hxs⟩⟩
    simp [h, hy]

/-- The subset transform is injective by strong induction on finite subsets. -/
theorem subsetMass_injective : Function.Injective (subsetMass (E := E)) := by
  classical
  intro n m hnm
  funext S
  refine Finset.strongInductionOn S ?_
  intro S ih
  have hp : (∑ T ∈ S.powerset.erase S, n T) =
      ∑ T ∈ S.powerset.erase S, m T := by
    apply Finset.sum_congr rfl
    intro T hT
    obtain ⟨hne, hmem⟩ := Finset.mem_erase.mp hT
    exact ih T (Finset.ssubset_iff_subset_ne.mpr ⟨Finset.mem_powerset.mp hmem, hne⟩)
  have hs := congrFun hnm S
  rw [subsetMass_eq_powerset_sum, subsetMass_eq_powerset_sum] at hs
  have hself : S ∈ S.powerset := Finset.mem_powerset.mpr (Finset.Subset.refl S)
  rw [← Finset.sum_erase_add _ n hself, ← Finset.sum_erase_add _ m hself] at hs
  rw [hp] at hs
  exact Nat.add_left_cancel hs

/-- Agreement on nonempty queries extends to every query. -/
theorem hit_eq_of_nonempty_eq {n m : Finset E → ℕ}
    (h : ∀ U : Finset E, U.Nonempty → hit n U = hit m U) : hit n = hit m := by
  funext U
  by_cases hu : U.Nonempty
  · exact h U hu
  · have he : U = ∅ := Finset.not_nonempty_iff_eq_empty.mp hu
    simp [he]

/-- The only coordinate invisible to hit queries is the empty-effect coordinate. -/
theorem hit_injective_of_empty_eq {n m : Finset E → ℕ}
    (hempty : n ∅ = m ∅)
    (hhit : ∀ U : Finset E, U.Nonempty → hit n U = hit m U) : n = m := by
  have hhitall : hit n = hit m := hit_eq_of_nonempty_eq hhit
  have htotal : (∑ T : Finset E, n T) = ∑ T : Finset E, m T := by
    have hn := hit_compl_add_subsetMass n ∅
    have hm := hit_compl_add_subsetMass m ∅
    simp only [Finset.compl_empty, subsetMass_empty] at hn hm
    rw [← hn, ← hm, hhitall, hempty]
  apply subsetMass_injective
  funext S
  have hn := hit_compl_add_subsetMass n S
  have hm := hit_compl_add_subsetMass m S
  rw [hhitall, htotal] at hn
  exact Nat.add_left_cancel (hn.trans hm.symm)

/-- Normalized histograms are identified by all nonempty hit queries. -/
theorem hit_injective_of_empty_zero {n m : Finset E → ℕ}
    (hn : n ∅ = 0) (hm : m ∅ = 0)
    (hhit : ∀ U : Finset E, U.Nonempty → hit n U = hit m U) : n = m :=
  hit_injective_of_empty_eq (hn.trans hm.symm) hhit

/-- Changing the empty-effect multiplicity never changes any hit query. -/
theorem hit_update_empty (n : Finset E → ℕ) (k : ℕ) :
    hit (Function.update n ∅ k) = hit n := by
  classical
  funext U
  unfold hit
  apply Finset.sum_congr rfl
  intro T _
  by_cases ht : T = ∅
  · subst T
    simp
  · simp [Function.update_of_ne ht]

/-- Exact observational equivalence, without normalizing the empty coordinate. -/
theorem hit_eq_iff_nonempty_eq {n m : Finset E → ℕ} :
    hit n = hit m ↔ ∀ T : Finset E, T.Nonempty → n T = m T := by
  classical
  constructor
  · intro h
    have hnorm : Function.update n ∅ 0 = Function.update m ∅ 0 :=
      hit_injective_of_empty_zero (by simp) (by simp) (by
        intro U _
        rw [hit_update_empty, hit_update_empty]
        exact congrFun h U)
    intro T ht
    have hne : T ≠ ∅ := Finset.nonempty_iff_ne_empty.mp ht
    simpa [Function.update_of_ne hne] using congrFun hnorm T
  · intro h
    funext U
    unfold hit
    apply Finset.sum_congr rfl
    intro T _
    by_cases hi : (T ∩ U).Nonempty
    · rw [if_pos hi, if_pos hi]
      exact h T (Finset.Nonempty.mono Finset.inter_subset_left hi)
    · simp [hi]

#print axioms hit_injective_of_empty_zero
#print axioms hit_eq_iff_nonempty_eq

end CalibratedIdentification
