import HenkinSoundness

#check HenkinSoundness.F
#check HenkinSoundness.finite_sound
#check HenkinSoundness.form_sound
#check HenkinSoundness.has_sound
#check HenkinSoundness.fundamental
#check HenkinSoundness.formation_eligible
#check HenkinSoundness.formation_coherent

#print axioms HenkinSourceTransport.interp_abstraction_beta
#print axioms HenkinSourceTransport.source_plus_sound
#print axioms HenkinSoundness.fundamental
#print axioms HenkinSoundness.formation_eligible
#print axioms HenkinSoundness.formation_coherent

-- Semantic noninhabitation can be applied directly to any actual source proof.
namespace HenkinSoundness

theorem closed_not_derivable_of_empty {A : P01AC.Ty}
    (ρ : REnv) (hρ : admissible ρ)
    (empty : ∀ t, ¬ F A ρ zeroEnv t t) :
    ∀ p, ¬ P01AC.ExtensionalRepair.HasE [] p A := by
  intro p hp
  exact empty (HenkinSourceTransport.interp p zeroEnv)
    (fundamental hp ρ zeroEnv zeroEnv hρ ⟨rfl,rfl⟩)

#print axioms closed_not_derivable_of_empty
end HenkinSoundness
