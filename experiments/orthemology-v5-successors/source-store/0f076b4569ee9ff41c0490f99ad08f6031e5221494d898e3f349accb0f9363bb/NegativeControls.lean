import CanonicalReplies
import RandomizedSearch

open CoveringKernel Finset
namespace CoveringNegativeControls

def P : Finset (Fin 4) := {0,1,2}
def T : Finset (Fin 4) := {0}

-- The complement direction cannot be reversed or replaced by the path itself.
theorem bad_path_does_not_avoid : ¬Disjoint P T := by decide
theorem bad_set_is_inside_path : T ⊆ P := by decide
theorem bad_set_not_inside_complement : ¬T ⊆ Pᶜ := by decide

-- At the minimum, a proper subfamily of k-blocks leaves its missing world uncovered.
theorem three_blocks_are_not_four_singletons :
    ¬Covers 1 ({({0} : Finset (Fin 4)), {1}, {2}} : Finset (Finset (Fin 4))) := by
  intro h
  have ht := h ({3} : Finset (Fin 4)) (by decide)
  rcases ht with ⟨A, hA, hsub⟩
  simp only [mem_insert, mem_singleton] at hA
  rcases hA with rfl | rfl | rfl <;> simp at hsub

-- Full-path revelation is a strictly richer interface than homogeneous failure.
def F : Finset (Finset (Fin 4)) := {P}
def p : Path F := ⟨P, by simp [F]⟩
def reveal : Finset (Fin 4) → ℕ → Path F → Finset (Fin 4) := fun t _ _ => t

theorem reveal_not_opaque (failedReply : ℕ → Path F → Finset (Fin 4)) :
    ¬Opaque 1 reveal failedReply := by
  intro h
  have h0 := h ({0} : Finset (Fin 4)) (by decide) 0 p (by decide)
  have h1 := h ({1} : Finset (Fin 4)) (by decide) 0 p (by decide)
  have heq : ({0} : Finset (Fin 4)) = {1} := h0.trans h1.symm
  have hn : ({0} : Finset (Fin 4)) ≠ {1} := by decide
  exact hn heq

-- Cardinality equality is necessary: a two-block can cover two distinct singletons.
theorem larger_block_covers_two_worlds :
    ({0} : Finset (Fin 4)) ⊆ {0,1} ∧ ({1} : Finset (Fin 4)) ⊆ {0,1} ∧
      ({0} : Finset (Fin 4)) ≠ {1} := by decide

#print axioms three_blocks_are_not_four_singletons
#print axioms reveal_not_opaque
end CoveringNegativeControls
