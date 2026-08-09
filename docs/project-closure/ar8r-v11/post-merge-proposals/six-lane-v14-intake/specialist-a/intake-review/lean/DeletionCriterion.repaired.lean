import Mathlib.Data.Set.Basic

/-!
Independent intake repair of the Specialist A deletion-criterion draft.

The supplied source placed a module documentation command before its import,
which Lean 4.32.2 rejects.  This copy changes only that command order and keeps
the theorem content separate from the supplied bytes.
-/

universe uX uY

namespace AR8R.SpecialistA.IntakeReview

variable {X : Type uX} {Y : Type uY}

def RestrictionInjective (H : Set (X → Y)) (D : Set X) : Prop :=
  ∀ ⦃f g : X → Y⦄, f ∈ H → g ∈ H →
    (∀ x : X, x ∈ D → f x = g x) → f = g

def DeletionCollision (H : Set (X → Y)) (D : Set X) : Prop :=
  ∃ f : X → Y, f ∈ H ∧
    ∃ g : X → Y, g ∈ H ∧ f ≠ g ∧
      ∀ x : X, x ∈ D → f x = g x

theorem restrictionInjective_iff_noDeletionCollision
    (H : Set (X → Y)) (D : Set X) :
    RestrictionInjective H D ↔ ¬ DeletionCollision H D := by
  constructor
  · intro hinj hcoll
    rcases hcoll with ⟨f, hf, g, hg, hne, hagree⟩
    exact hne (hinj hf hg hagree)
  · intro hno f g hf hg hagree
    by_contra hne
    exact hno ⟨f, hf, g, hg, hne, hagree⟩

end AR8R.SpecialistA.IntakeReview

#print axioms AR8R.SpecialistA.IntakeReview.restrictionInjective_iff_noDeletionCollision
