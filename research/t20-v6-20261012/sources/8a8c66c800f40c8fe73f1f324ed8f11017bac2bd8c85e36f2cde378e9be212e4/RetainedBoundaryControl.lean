import FullESectionApplication
import UniquenessIndependence
namespace FullEIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.EffectiveCompleteness SourceRigidity RigidityInitiality

/-- The section is literally the retained raw fold's second projection. -/
theorem literal_polynomial (p s n : Poly) : sectionBody p s n =
    sndPoly (.app (.app n (totalStep (uncurriedStep s))) (totalSeed p)) := rfl

theorem literal_rigidity : Rigidity = .pi (arr N N)
    (arr (ZeroAt (.var 0)) (arr (StepAt (.var 0)) (ResultAt (.var 0)))) := rfl

/-- Rechecks coexistence with the unchanged independent metatheoretic boundary. -/
theorem closed_rigidity_boundary :
    (¬ ∃ p, HasE [] p Rigidity) ∧ (¬ ∃ p, HasE [] p (arr Rigidity .bottom)) :=
  ⟨fun ⟨p, hp⟩ => RigidityDiscriminator.rigidity_uninhabited p hp,
   fun ⟨p, hp⟩ => RigidityDiscriminator.no_internal_negation p hp⟩

theorem closed_uniqueness_boundary :
    (¬ ∃ p, HasE [] p InternalRecursorPrinciple.Uniqueness) ∧
    (¬ ∃ p, HasE [] p (arr InternalRecursorPrinciple.Uniqueness .bottom)) :=
  RigidityInitiality.internal_uniqueness_independence

#print axioms closed_rigidity_boundary
#print axioms closed_uniqueness_boundary
end FullEIndependentReview
