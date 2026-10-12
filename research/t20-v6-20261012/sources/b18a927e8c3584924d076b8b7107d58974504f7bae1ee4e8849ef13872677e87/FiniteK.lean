import Mathlib.Data.Fintype.Card

/- A minimal, classical finite-algebra obstruction. No source typing, full
function spaces, S, I, extensionality, or impredicative quantification is used. -/
namespace FiniteRawObstruction

universe u

structure TotalK (A : Type u) where
  app : A → A → A
  k : A
  k_law : ∀ x y, app (app k x) y = x

namespace TotalK
variable {A : Type u} (M : TotalK A)
include M

theorem left_k_injective : Function.Injective (M.app M.k) := by
  intro x y h
  have e := congrArg (fun z => M.app z M.k) h
  simpa only [M.k_law] using e

/-- A preimage of K would already collapse the entire carrier. -/
theorem subsingleton_of_k_in_range (h : ∃ a, M.app M.k a = M.k) :
    Subsingleton A := by
  obtain ⟨a, ha⟩ := h
  have hc (x : A) : M.app M.k x = a := by
    rw [← ha, M.k_law]
  exact ⟨fun x y => M.left_k_injective ((hc x).trans (hc y).symm)⟩

theorem finite_subsingleton [Finite A] : Subsingleton A :=
  M.subsingleton_of_k_in_range
    (Finite.surjective_of_injective M.left_k_injective M.k)

theorem finite_card_one [Fintype A] [Finite A] : Fintype.card A = 1 := by
  letI : Subsingleton A := M.finite_subsingleton
  letI : Unique A := ⟨⟨M.k⟩, fun _ => Subsingleton.elim _ _⟩
  exact Fintype.card_unique

theorem k_not_in_range [Nontrivial A] : ¬ ∃ a, M.app M.k a = M.k := by
  intro h
  letI : Subsingleton A := M.subsingleton_of_k_in_range h
  exact not_nontrivial A inferInstance

theorem nontrivial_infinite [Nontrivial A] : Infinite A := by
  apply not_finite_iff_infinite.mp
  intro h
  letI : Finite A := h
  exact M.k_not_in_range
    (Finite.surjective_of_injective M.left_k_injective M.k)

/-- The sharp positive boundary: one point satisfies the complete K contract. -/
def singletonModel : TotalK Unit where
  app := fun _ _ => ()
  k := ()
  k_law := fun x _ => Subsingleton.elim _ x

end TotalK

#print axioms TotalK.left_k_injective
#print axioms TotalK.subsingleton_of_k_in_range
#print axioms TotalK.finite_subsingleton
#print axioms TotalK.finite_card_one
#print axioms TotalK.nontrivial_infinite
end FiniteRawObstruction
