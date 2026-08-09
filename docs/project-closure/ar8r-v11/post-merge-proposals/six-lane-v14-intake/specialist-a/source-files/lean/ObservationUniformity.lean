/-!
Specialist A private Lean draft: observation-uniform strategy interface.

Status: source drafted only. No local Lean binary was available in the execution
runtime, so parse, elaboration, kernel checking, project build, and axiom
reporting remain NOT_RUN. The factorization statement is deliberately classified
inside the existing fibre/quotient family and receives no new theorem identity.
-/

import Mathlib.Logic.Function.Basic

universe uS uO uA

namespace AR8R.SpecialistA.Private

variable {S : Type uS} {O : Type uO} {A : Type uA}

/-- A state strategy cannot choose different actions inside one observation fibre. -/
def ObservationUniform (obs : S → O) (sigma : S → A) : Prop :=
  ∀ ⦃s t : S⦄, obs s = obs t → sigma s = sigma t

/-- Every observation strategy induces an observation-uniform state strategy. -/
theorem observationStrategy_is_uniform (obs : S → O) (tau : O → A) :
    ObservationUniform obs (fun s => tau (obs s)) := by
  intro s t h
  exact congrArg tau h

/--
Under a surjective observation map, every observation-uniform state strategy has
an observation-level decoder. This is a specialization of ordinary fibre
factorization, not a new mechanism.
-/
theorem uniformStrategy_factors_through_observation
    (obs : S → O) (sigma : S → A)
    (hsurj : Function.Surjective obs)
    (huniform : ObservationUniform obs sigma) :
    ∃ tau : O → A, ∀ s : S, tau (obs s) = sigma s := by
  classical
  choose representative hrepresentative using hsurj
  refine ⟨fun o => sigma (representative o), ?_⟩
  intro s
  apply huniform
  exact hrepresentative (obs s)

end AR8R.SpecialistA.Private

#print axioms AR8R.SpecialistA.Private.observationStrategy_is_uniform
#print axioms AR8R.SpecialistA.Private.uniformStrategy_factors_through_observation
