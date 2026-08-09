/-!
Specialist A private Lean draft: hypothesis-class deletion criterion.

Status: source drafted only. No local Lean binary was available in the execution
runtime, so parse, elaboration, kernel checking, project build, and axiom
reporting remain NOT_RUN. This file allocates no repository theorem identifier.
-/

import Mathlib.Data.Set.Basic

universe uX uY

namespace AR8R.SpecialistA.Private

variable {X : Type uX} {Y : Type uY}

/-- Restriction to coordinates in `D` identifies every member of `H`. -/
def RestrictionInjective (H : Set (X → Y)) (D : Set X) : Prop :=
  ∀ ⦃f g : X → Y⦄, f ∈ H → g ∈ H →
    (∀ x : X, x ∈ D → f x = g x) → f = g

/-- Two distinct members of `H` collide on every observed coordinate in `D`. -/
def DeletionCollision (H : Set (X → Y)) (D : Set X) : Prop :=
  ∃ f : X → Y, f ∈ H ∧
    ∃ g : X → Y, g ∈ H ∧ f ≠ g ∧
      ∀ x : X, x ∈ D → f x = g x

/-- Exact restriction-map criterion. -/
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

end AR8R.SpecialistA.Private

#print axioms AR8R.SpecialistA.Private.restrictionInjective_iff_noDeletionCollision
