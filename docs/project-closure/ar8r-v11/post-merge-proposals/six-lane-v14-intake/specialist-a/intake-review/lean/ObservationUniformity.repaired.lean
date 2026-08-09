import Mathlib.Logic.Function.Basic

/-!
Independent intake repair of the Specialist A observation-uniformity draft.

The supplied source placed a module documentation command before its import,
which Lean 4.32.2 rejects.  This copy changes only that command order and keeps
the theorem content separate from the supplied bytes.
-/

universe uS uO uA

namespace AR8R.SpecialistA.IntakeReview

variable {S : Type uS} {O : Type uO} {A : Type uA}

def ObservationUniform (obs : S → O) (sigma : S → A) : Prop :=
  ∀ ⦃s t : S⦄, obs s = obs t → sigma s = sigma t

theorem observationStrategy_is_uniform (obs : S → O) (tau : O → A) :
    ObservationUniform obs (fun s => tau (obs s)) := by
  intro s t h
  exact congrArg tau h

theorem uniformStrategy_factors_through_observation
    (obs : S → O) (sigma : S → A)
    (hsurj : Function.Surjective obs)
    (huniform : ObservationUniform obs sigma) :
    ∃ tau : O → A, ∀ s : S, tau (obs s) = sigma s := by
  classical
  let representative : O → S := fun o => Classical.choose (hsurj o)
  have hrepresentative : ∀ o : O, obs (representative o) = o := by
    intro o
    exact Classical.choose_spec (hsurj o)
  refine ⟨fun o => sigma (representative o), ?_⟩
  intro s
  apply huniform
  exact hrepresentative (obs s)

end AR8R.SpecialistA.IntakeReview

#print axioms AR8R.SpecialistA.IntakeReview.observationStrategy_is_uniform
#print axioms AR8R.SpecialistA.IntakeReview.uniformStrategy_factors_through_observation
