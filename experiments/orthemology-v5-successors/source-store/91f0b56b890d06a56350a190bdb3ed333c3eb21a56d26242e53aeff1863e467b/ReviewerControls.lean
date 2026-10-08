import IndexedCompletionDiameter

set_option autoImplicit false

namespace IndexedReviewer

open IndexedCompletion

universe u
variable {X : ℕ → Type u}

def constantBonds (p : ∀ i, X i) : Bonding X := fun i _ => p i

theorem constant_compatible (p : ∀ i, X i) : Compatible (constantBonds p) p := by
  intro i
  rfl

theorem constant_unique (p : ∀ i, X i) : UniqueRealization (constantBonds p) := by
  refine ⟨p, constant_compatible p, ?_⟩
  intro b hb
  funext i
  exact hb i

theorem constant_survival (p : ∀ i, X i) (i : ℕ) (x : X i) :
    Survives (constantBonds p) i x ↔ x = p i := by
  constructor
  · intro hx
    obtain ⟨z, hz⟩ := hx (i + 1) (Nat.le_succ i)
    simpa only [transport_one, constantBonds] using hz.symm
  · rintro rfl
    exact compatible_survives (constantBonds p) p (constant_compatible p) i

/-- A concrete dependent family with changing finite cardinalities. -/
def movingBonds : Bonding (fun i => Fin (i + 1)) :=
  constantBonds (fun i => ⟨0, Nat.zero_lt_succ i⟩)

theorem moving_unique : UniqueRealization movingBonds :=
  constant_unique (fun i => (⟨0, Nat.zero_lt_succ i⟩ : Fin (i + 1)))

/-- Onto bonding maps are not required even when the coordinate spaces differ. -/
theorem moving_not_surjective : ¬ Function.Surjective (movingBonds 1) := by
  intro h
  obtain ⟨z, hz⟩ := h (⟨1, by decide⟩ : Fin 2)
  have hv := congrArg Fin.val hz
  simp [movingBonds, constantBonds] at hv

def tailBits : Bonding (fun _ => Bool) := fun i x => if i = 0 then false else x

def bitPath (c : Bool) : ℕ → Bool := fun i => if i = 0 then false else c

theorem bitPath_compatible (c : Bool) : Compatible tailBits (bitPath c) := by
  intro i
  cases i <;> simp [bitPath, tailBits]

/-- Coordinate zero can be determined while a later Boolean choice survives. -/
theorem first_coordinate_singleton :
    ∀ x : Bool, Survives tailBits 0 x ↔ x = false := by
  intro x
  constructor
  · intro hx
    obtain ⟨z, hz⟩ := hx 1 (by omega)
    simpa [transport_one, tailBits] using hz.symm
  · rintro rfl
    exact compatible_survives tailBits (bitPath false) (bitPath_compatible false) 0

theorem first_coordinate_does_not_give_unique : ¬ UniqueRealization tailBits := by
  rintro ⟨b, hb, huniq⟩
  have h := (huniq (bitPath true) (bitPath_compatible true)).trans
    (huniq (bitPath false) (bitPath_compatible false)).symm
  have h1 := congrFun h 1
  simp [bitPath] at h1

/-- Empty state spaces make pairwise forgetting vacuous. -/
theorem empty_forgetting [∀ i, MetricSpace (X i)] [∀ i, IsEmpty (X i)]
    (f : Bonding X) : HorizonForgetting f := by
  intro H ε hε
  refine ⟨0, ?_⟩
  intro j hj hH i hi u
  exact isEmptyElim u

theorem empty_has_no_realization [IsEmpty (X 0)] (f : Bonding X) :
    ¬ UniqueRealization f := by
  rintro ⟨b, _⟩
  exact isEmptyElim (b 0)

end IndexedReviewer

#print axioms IndexedReviewer.constant_compatible
#print axioms IndexedReviewer.constant_unique
#print axioms IndexedReviewer.constant_survival
#print axioms IndexedReviewer.moving_unique
#print axioms IndexedReviewer.moving_not_surjective
#print axioms IndexedReviewer.bitPath_compatible
#print axioms IndexedReviewer.first_coordinate_singleton
#print axioms IndexedReviewer.first_coordinate_does_not_give_unique
#print axioms IndexedReviewer.empty_forgetting
#print axioms IndexedReviewer.empty_has_no_realization
