/- Bounded consequences of the isolated unadopted candidate.
   Its positive theorem and the frozen current/Plus obstruction use distinct judgments. -/
import ExtensionalRepairLemmas
import ExtensionalRepairSoundness
import ExtensionalRepairWitness
import IntensionalIdentityTheorems

namespace P01AC.ExtensionalRepair
open OrthemologyV2 OrthemologyV3 P01D P01R
open Intensional

/-- Every E derivation of a closed Raw-indexed identity forces raw conversion.
    No scope assumption on the proof polynomial or choice of a final rule is made. -/
theorem closed_raw_identity_conversion {r p q : Poly}
    (h : HasE [] r (.identity .raw p q)) :
    Conv (eval p zeroEnv) (eval q zeroEnv) := by
  have g := fundamental h (diagEnv (fun _ => rawPER)) zeroEnv zeroEnv ⟨rfl,rfl⟩
  exact g.1

/-- The Raw-indexed endpoint identity is formed, despite having no proof. -/
theorem raw_separation_form :
    FormE [] (.identity .raw separationP separationQ) :=
  .identity (.raw .nil) (.rawAtom (.raw .nil)) (.rawAtom (.raw .nil))

/-- All proof polynomials are excluded, including indirect J/elimination routes. -/
theorem raw_separation_no_has (r : Poly) :
    ¬ HasE [] r (.identity .raw separationP separationQ) := by
  intro h
  exact separation_contradiction (closed_raw_identity_conversion h)

theorem raw_separation_uninhabited :
    ¬ ∃ r, HasE [] r (.identity .raw separationP separationQ) := by
  rintro ⟨r,h⟩
  exact raw_separation_no_has r h

/-- The conversion relation is still exactly the imported eight-case relation. -/
theorem separation_not_polyConvPlus : ¬ Plus.PolyConvPlus separationP separationQ := by
  intro h
  exact separation_contradiction (Plus.polyConvPlus_sound h zeroEnv)

/-- Existing current and bridge-only results retain their literal namespaces. -/
theorem preserved_old_noninhabitation (r : Poly) :
    (¬ P01AC.Has [] r separationB) ∧ (¬ Plus.HasPlus [] r separationB) :=
  ⟨Intensional.separation_no_has r, Intensional.separation_no_hasPlus r⟩

/-- This one finite witness establishes increased typing power, not completeness. -/
theorem strict_typed_identity_extension :
    HasE [] separationE separationB ∧
    (¬ ∃ r, P01AC.Has [] r separationB) ∧
    (¬ ∃ r, Plus.HasPlus [] r separationB) ∧
    (¬ ∃ r, HasE [] r (.identity .raw separationP separationQ)) ∧
    (¬ Plus.PolyConvPlus separationP separationQ) := by
  refine ⟨separation_has, ?_, ?_, raw_separation_uninhabited, separation_not_polyConvPlus⟩
  · rintro ⟨r,h⟩
    exact Intensional.separation_no_has r h
  · rintro ⟨r,h⟩
    exact Intensional.separation_no_hasPlus r h

/-- Existing proof erasure remains harmless at the exact positive witness. -/
theorem separation_proof_erases : HasE [] separationE .raw :=
  .proofErase (.raw .nil) (form_inclusion separationB_form) separation_has

end P01AC.ExtensionalRepair
