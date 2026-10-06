import Mathlib.Data.List.FinRange
import Mathlib.Data.List.Sublists
import Mathlib.Data.Finset.Powerset

namespace OrthemicCertificate.Signed

/-- Constructive bounded ordered lists; no normalisation discards a list order. -/
def boundedLists {α : Type} (xs : List α) : Nat → List (List α)
  | 0 => [[]]
  | n + 1 => [] :: xs.flatMap (fun x => (boundedLists xs n).map (x :: ·))

@[simp] theorem mem_boundedLists {α : Type} (xs : List α) (n : Nat) (ys : List α) :
    ys ∈ boundedLists xs n ↔ ys.length ≤ n ∧ ∀ y ∈ ys, y ∈ xs := by
  induction n generalizing ys with
  | zero => cases ys <;> simp [boundedLists]
  | succ n ih =>
    cases ys with
    | nil => simp [boundedLists]
    | cons y ys =>
      simp [boundedLists, ih, Nat.succ_le_succ_iff, and_assoc, and_left_comm]

def productList {α β : Type} (xs : List α) (ys : List β) : List (α × β) :=
  xs.flatMap (fun x => ys.map (x, ·))

@[simp] theorem mem_productList {α β : Type} (xs : List α) (ys : List β) (z : α × β) :
    z ∈ productList xs ys ↔ z.1 ∈ xs ∧ z.2 ∈ ys := by
  rcases z with ⟨x,y⟩
  simp [productList]

/-- Enumerates all subsets using list sublists, so it needs no quotient choice. -/
def subsetList {α : Type} [DecidableEq α] (xs : List α) : List (Finset α) :=
  xs.sublists.map List.toFinset

@[simp] theorem mem_subsetList {α : Type} [DecidableEq α] (xs : List α) (s : Finset α) :
    s ∈ subsetList xs ↔ s ⊆ xs.toFinset := by
  constructor
  · intro h
    obtain ⟨ys,hy,rfl⟩ := List.mem_map.mp h
    have hsub := List.mem_sublists.mp hy
    intro a ha
    exact List.mem_toFinset.mpr (hsub.subset (List.mem_toFinset.mp ha))
  · intro h
    refine List.mem_map.mpr ⟨xs.filter (fun a => a ∈ s), ?_, ?_⟩
    · exact List.mem_sublists.mpr List.filter_sublist
    · ext a
      simp only [List.mem_toFinset, List.mem_filter, decide_eq_true_eq]
      constructor
      · exact And.right
      · intro ha
        exact ⟨List.mem_toFinset.mp (h ha),ha⟩

@[simp] theorem mem_subset_finRange (n : Nat) (s : Finset (Fin n)) :
    s ∈ subsetList (List.finRange n) := by
  apply (mem_subsetList _ _).mpr
  intro a _
  exact List.mem_toFinset.mpr (List.mem_finRange a)

end OrthemicCertificate.Signed
