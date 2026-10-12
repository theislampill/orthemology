import TaggedPER
import OpenDevelopments
import RigidityDiscriminator

namespace SigmaTagBoundary
open P01AC P01D
open P01AC.ExtensionalRepair (HasE)
open OpenTermStandardness (T Conv)
open TaggedPER
open ImportedOpenTermTransport (interp)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem zero_normal : OpenDevelopments.Normal T.zero := by
  intro u h; cases h; rfl

theorem probe_normal : OpenDevelopments.Normal (T.zero ⬝ T.k ⬝ (T.k ⬝ T.i)) := by
  intro u h
  cases h with
  | app hf hx =>
    cases hf with
    | app h0 hk =>
      cases h0; cases hk
      cases hx with
      | app hk hi => cases hk; cases hi; rfl

theorem ghost_not_tag : ¬ tag T.i := by
  intro h
  have projections : Conv (pair (first T.i) (second T.i)) (pair T.k (T.k ⬝ T.i)) :=
    OpenTermStandardness.pair_congr (.i _) (.i _)
  have eq : Conv T.zero (T.zero ⬝ T.k ⬝ (T.k ⬝ T.i)) :=
    (Conv.i T.zero).symm.trans ((Conv.app (h.trans projections) (.refl _)).trans
      (OpenTermStandardness.pair_application _ _ _))
  have impossible := OpenDevelopments.normal_unique zero_normal probe_normal eq
  cases impossible

def SigmaRaw : Ty := .sigma .raw .raw
def etaBody : Ty := .identity SigmaRaw (.var 0)
  (pairPoly (fstPoly (.var 0)) (sndPoly (.var 0)))
def Eta : Ty := .pi SigmaRaw etaBody

theorem ghost_member (ρ : REnv) (η : TaggedPER.Env) : F SigmaRaw ρ η T.i T.i :=
  ⟨.refl _,.refl _,Iff.rfl⟩

theorem eta_at_ghost_empty (ρ : REnv) (η : TaggedPER.Env) (p q : T) :
    ¬ F etaBody ρ (cons T.i η) p q := by
  intro h
  exact ghost_not_tag (h.1.2.2.mpr (tag_pair _ _))

theorem eta_empty (ρ : REnv) (η : TaggedPER.Env) (p q : T) : ¬ F Eta ρ η p q := by
  intro h
  exact eta_at_ghost_empty ρ η _ _ (h T.i T.i (ghost_member ρ η))

def emptyEnv : REnv := fun _ _ _ => False
theorem empty_admissible : admissible emptyEnv := fun _ =>
  ⟨False.elim,fun h _ => h,fun _ _ h => h⟩

theorem no_eta (p : Poly) : ¬ HasE [] p Eta := by
  intro h
  exact eta_empty _ _ _ _ (fundamental h emptyEnv zeroEnv zeroEnv empty_admissible ⟨rfl,rfl⟩)

theorem rigidity_exact (ρ : REnv) (η : TaggedPER.Env) :
    F SourceRigidity.Rigidity ρ η = FullPER.F SourceRigidity.Rigidity ρ η := rfl

theorem rigidity_valid (ρ : REnv) (η : TaggedPER.Env) :
    F SourceRigidity.Rigidity ρ η
      (interp P01AC.ExtensionalRepair.ExactScalarFusion.c3 η)
      (interp P01AC.ExtensionalRepair.ExactScalarFusion.c3 η) :=
  RigidityDiscriminator.rigidity_valid ρ η

/-- The explicit Rigidity hypothesis does not imply the universal dependent-pair eta type. -/
theorem no_rigidity_to_eta (p : Poly) :
    ¬ HasE [] p (arr SourceRigidity.Rigidity Eta) := by
  intro h
  have v := fundamental h emptyEnv zeroEnv zeroEnv empty_admissible ⟨rfl,rfl⟩
  rw [TaggedPER.F_arr] at v
  exact eta_empty _ _ _ _ (v _ _ (rigidity_valid emptyEnv zeroEnv))

/-- Direct open source form, with both the pair and the explicit Rigidity assumption. -/
theorem no_eta_under_rigidity (p : Poly) :
    ¬ HasE [SigmaRaw, SourceRigidity.Rigidity] p etaBody := by
  intro h
  let r := interp P01AC.ExtensionalRepair.ExactScalarFusion.c3 zeroEnv
  let η := cons T.i (cons r zeroEnv)
  have ee : E [SigmaRaw, SourceRigidity.Rigidity] emptyEnv η η :=
    ⟨⟨⟨rfl,rfl⟩,rigidity_valid emptyEnv zeroEnv⟩,ghost_member _ _⟩
  exact eta_at_ghost_empty _ _ _ _ (fundamental h emptyEnv η η empty_admissible ee)

/-- The original componentwise model validates eta simultaneously with Rigidity. -/
theorem full_eta_valid (ρ : FullPER.REnv) (η : FullPER.Env) :
    FullPER.F Eta ρ η (T.k ⬝ T.i) (T.k ⬝ T.i) := by
  intro z w zw
  exact ⟨⟨(OpenTermStandardness.fst_pair _ _).symm,
    (OpenTermStandardness.snd_pair _ _).symm⟩,.k _ _,.k _ _⟩

theorem no_rigidity_to_not_eta (p : Poly) :
    ¬ HasE [] p (arr SourceRigidity.Rigidity (arr Eta .bottom)) := by
  intro h
  have v := FullPER.fundamental h FullPER.Application.emptyEnv FullPER.zeroEnv FullPER.zeroEnv
    FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
  rw [FullPER.F_arr] at v
  have vn := v _ _ (RigidityDiscriminator.rigidity_valid _ _)
  rw [FullPER.F_arr] at vn
  exact vn _ _ (full_eta_valid _ _)

theorem relative_independence :
    (¬ ∃ p, HasE [] p (arr SourceRigidity.Rigidity Eta)) ∧
    (¬ ∃ p, HasE [] p (arr SourceRigidity.Rigidity (arr Eta .bottom))) :=
  ⟨fun ⟨p,h⟩ => no_rigidity_to_eta p h,
   fun ⟨p,h⟩ => no_rigidity_to_not_eta p h⟩

/-- The two projections cannot observe the tag distinction. -/
theorem matching_observations :
    Conv (first T.i) (first (pair (first T.i) (second T.i))) ∧
    Conv (second T.i) (second (pair (first T.i) (second T.i))) :=
  ⟨(OpenTermStandardness.fst_pair _ _).symm,
   (OpenTermStandardness.snd_pair _ _).symm⟩

theorem matching_observations_not_identity (ρ : REnv) (η : TaggedPER.Env) :
    ¬ F SigmaRaw ρ η T.i (pair (first T.i) (second T.i)) := by
  intro h
  exact ghost_not_tag (h.2.2.mpr (tag_pair _ _))

#print axioms full_eta_valid
#print axioms no_rigidity_to_not_eta
#print axioms relative_independence
#print axioms matching_observations_not_identity
#print axioms ghost_not_tag
#print axioms no_eta
#print axioms rigidity_exact
#print axioms rigidity_valid
#print axioms no_rigidity_to_eta
#print axioms no_eta_under_rigidity
end SigmaTagBoundary
