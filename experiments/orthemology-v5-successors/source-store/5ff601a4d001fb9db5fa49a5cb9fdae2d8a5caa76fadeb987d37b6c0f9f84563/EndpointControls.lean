import EndpointFixtures
open HiddenChange HiddenChangeEndpointTests MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenChangeEndpointTests
example : Admissible (one 0) := by decide +kernel
example : Admissible (one 1) := by decide +kernel
example : Admissible mixed := by decide +kernel
example : Admissible changedRows := by decide +kernel
example : Admissible separator := by decide +kernel
example : boundPositiveCheck (one 0) 0 evenSubmission = true := by decide +kernel
example : boundNegativeCheck (one 1) 0 oddSubmission = true := by decide +kernel
example : boundNegativeCheck separator 0 separatorSubmission = true := by decide +kernel
example : positiveCheck mixed 0 mixedBody = true := by decide +kernel
example : positiveCheck changedRows 0 mixedBody = true := by decide +kernel
example : boundPositiveCheck changedRows 0 ⟨mixed,0,mixedBody⟩ = false := by decide +kernel
example : positiveCheck (one 2) 0 evenBody = true := by decide +kernel
example : boundPositiveCheck (one 2) 0 evenSubmission = false := by decide +kernel
example : boundPositiveCheck mixed 1 ⟨mixed,0,mixedBody⟩ = false := by decide +kernel
example : positiveCheck mixed 1 mixedBody = true := by decide +kernel
example : boundNegativeCheck separator 1 separatorSubmission = false := by decide +kernel
example : boundPositiveCheck
    ({one 0 with interpretation := {(one 0).interpretation with modelRevision := "stale"}} : Input 1 1)
    0 evenSubmission = false := by decide +kernel
example : boundNegativeCheck
    ({one 1 with interpretation := {(one 1).interpretation with modelRevision := "stale"}} : Input 1 1)
    0 oddSubmission = false := by decide +kernel
example : boundPositiveCheck ({mixed with menus := mixed.menus.reverse} : Input 2 1)
    0 ⟨mixed,0,mixedBody⟩ = false := by decide +kernel
example : positiveCheck ({mixed with menus := mixed.menus.reverse} : Input 2 1)
    0 mixedBody = true := by decide +kernel
example : negativeCheck (one 0) 0 ⟨[∅,∅],[∅,∅]⟩ = false := by decide +kernel
example : knownRegion separator = {0} := by decide +kernel
example : uncertainRegion separator = ∅ := by decide +kernel

universe uR uZ
example : LawfulMeasurableWinner.{0,uZ} (one 0)
    (by decide +kernel : Admissible (one 0)).1 0 (Measure.dirac ())
    (compile (one 0) (by decide +kernel) 0 evenBody) (0,0) :=
  positive_compiled_semantics _ (by decide +kernel) _ _ (by decide +kernel) _
example : DeterministicWinner.{uZ} (one 0)
    (by decide +kernel : Admissible (one 0)).1 0 (0,0) :=
  (bound_positive_iff_deterministic_winner _ (by decide +kernel) _ _).mp
    ⟨evenSubmission,by decide +kernel⟩
example : ¬ DeterministicWinner.{uZ} (one 1)
    (by decide +kernel : Admissible (one 1)).1 0 (0,0) :=
  (bound_negative_iff_no_deterministic_winner _ (by decide +kernel) _ _).mp
    ⟨oddSubmission,by decide +kernel⟩
example {R : Type uR} [MeasurableSpace R] (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R 2 1) :
    ¬ LawfulMeasurableWinner.{uR,uZ} separator
      (by decide +kernel : Admissible separator).1 0 ρ π (0,0) :=
  (bound_negative_excludes_seeded_winner _ (by decide +kernel) _
    separatorSubmission (by decide +kernel) ρ π (0,0)).2.2
example {R : Type uR} [MeasurableSpace R] (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R 1 1) :
    ¬ LawfulMeasurableWinner.{uR,uZ} (one 1)
      (by decide +kernel : Admissible (one 1)).1 0 ρ π (0,0) :=
  (bound_negative_excludes_seeded_winner _ (by decide +kernel) _
    oddSubmission (by decide +kernel) ρ π (0,0)).2.2
end HiddenChangeEndpointTests
