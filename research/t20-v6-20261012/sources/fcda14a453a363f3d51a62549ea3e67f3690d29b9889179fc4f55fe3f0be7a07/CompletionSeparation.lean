import Boundary

namespace CompletionSeparation
open P01AC P01D
open P01AC.ExtensionalRepair (HasE has_inclusion)
open SourceRigidity
open HenkinSoundness
open CaseOperational (T Conv)
open HenkinSourceTransport (interp)
open HomogeneousOriginalW (emptyTypes emptyTypes_admissible atomPER scalarStep_related atom0_related nu_N)

set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Componentwise semantic eta uses projection beta and saturation, not raw pair eta.
The second component is evaluated in the fixed first-projection environment. -/
theorem componentwise_eta {A B : Ty} {ρ : REnv} {η : HenkinSoundness.Env} {z : T}
    (ha : Laws (F A ρ η)) (hb : Laws (F B ρ (cons (first z) η)))
    (hz : F (.sigma A B) ρ η z z) :
    F (.sigma A B) ρ η z (pair (first z) (second z)) := by
  exact ⟨ha.raw (.refl _) (HenkinSourceTransport.fst_pair _ _).symm hz.1,
    hb.raw (.refl _) (HenkinSourceTransport.snd_pair _ _).symm hz.2⟩

/-- This is the literal retained object-language Raw-pair Eta, not a schema. -/
theorem henkin_eta_valid (ρ : REnv) (η : HenkinSoundness.Env) :
    F SigmaTagBoundary.Eta ρ η (T.k ⬝ T.i) (T.k ⬝ T.i) := by
  intro z w zw
  exact ⟨⟨True.intro, True.intro⟩, .k _ _, .k _ _⟩

/-- The old actual-source compiler witness already empties the identity conclusion. -/
theorem henkin_result_empty (ρ : REnv) (η : HenkinSoundness.Env) (u v : T) :
    ¬ F (ResultAt FullPER.Application.originalQ) ρ η u v := by
  intro h
  have hn := h.1 T.nu T.nu (nu_N ρ η)
  have hs := hn atomPER HomogeneousCounterexample.scalarStep
    HomogeneousCounterexample.scalarStep scalarStep_related T.a0 T.a0 atom0_related
  have bad := hs.1
  change Conv (T.i ⬝ T.nu ⬝ HomogeneousCounterexample.scalarStep ⬝ T.a0)
    (interp FullPER.Application.originalQ η ⬝ T.nu ⬝ HomogeneousCounterexample.scalarStep ⬝ T.a0) at bad
  unfold FullPER.Application.originalQ at bad
  rw [HomogeneousCounterexample.original_q_eval] at bad
  exact HomogeneousCounterexample.scalar_not_convertible
    (((Conv.app (Conv.app (Conv.i T.nu) (.refl _)) (.refl _)).symm).trans bad)

/-- No semantic realizer of literal Rigidity at the closed Henkin environment. -/
theorem henkin_rigidity_empty (u v : T) :
    ¬ F Rigidity emptyTypes HenkinSoundness.zeroEnv u v := by
  intro h
  have transfer := fundamental (has_inclusion rigidity_implies_identity)
    emptyTypes HenkinSoundness.zeroEnv HenkinSoundness.zeroEnv
    emptyTypes_admissible ⟨rfl,rfl⟩
  rw [HenkinSoundness.F_arr] at transfer
  exact henkin_result_empty _ _ _ _ (transfer u v h)

theorem no_eta_to_rigidity (p : Poly) :
    ¬ HasE [] p (arr SigmaTagBoundary.Eta Rigidity) := by
  intro h
  have v := fundamental h emptyTypes HenkinSoundness.zeroEnv HenkinSoundness.zeroEnv
    emptyTypes_admissible ⟨rfl,rfl⟩
  rw [HenkinSoundness.F_arr] at v
  exact henkin_rigidity_empty _ _ (v _ _ (henkin_eta_valid _ _))

/-- FullPER's already established simultaneous witnesses rule out the opposite negation. -/
theorem no_eta_to_not_rigidity (p : Poly) :
    ¬ HasE [] p (arr SigmaTagBoundary.Eta (arr Rigidity .bottom)) := by
  intro h
  have v := FullPER.fundamental h FullPER.Application.emptyEnv FullPER.zeroEnv FullPER.zeroEnv
    FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
  rw [FullPER.F_arr] at v
  have vn := v _ _ (SigmaTagBoundary.full_eta_valid _ _)
  rw [FullPER.F_arr] at vn
  exact vn _ _ (RigidityDiscriminator.rigidity_valid _ _)

theorem reverse_relative_independence :
    (¬ ∃ p, HasE [] p (arr SigmaTagBoundary.Eta Rigidity)) ∧
    (¬ ∃ p, HasE [] p (arr SigmaTagBoundary.Eta (arr Rigidity .bottom))) :=
  ⟨fun ⟨p,h⟩ => no_eta_to_rigidity p h,
   fun ⟨p,h⟩ => no_eta_to_not_rigidity p h⟩

/-- Simultaneous satisfaction in the retained FullPER actual-source model. -/
theorem full_joint_valid (ρ : FullPER.REnv) (η : FullPER.Env) :
    (∃ e, FullPER.F SigmaTagBoundary.Eta ρ η e e) ∧
    (∃ r, FullPER.F Rigidity ρ η r r) :=
  ⟨⟨_, SigmaTagBoundary.full_eta_valid ρ η⟩,
   ⟨_, RigidityDiscriminator.rigidity_valid ρ η⟩⟩

theorem reverse_relative_independence_Has :
    (¬ ∃ p, Has [] p (arr SigmaTagBoundary.Eta Rigidity)) ∧
    (¬ ∃ p, Has [] p (arr SigmaTagBoundary.Eta (arr Rigidity .bottom))) :=
  ⟨fun ⟨p,h⟩ => no_eta_to_rigidity p (has_inclusion h),
   fun ⟨p,h⟩ => no_eta_to_not_rigidity p (has_inclusion h)⟩

#print axioms componentwise_eta
#print axioms full_joint_valid
#print axioms reverse_relative_independence_Has
#print axioms henkin_eta_valid
#print axioms henkin_result_empty
#print axioms henkin_rigidity_empty
#print axioms no_eta_to_rigidity
#print axioms no_eta_to_not_rigidity
#print axioms reverse_relative_independence
end CompletionSeparation
