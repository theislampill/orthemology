import JointSoundness
import Boundary

namespace JointCompletion.Controls
open P01AC P01D
open P01AC.ExtensionalRepair (CtxE FormE HasE)
open SigmaTagBoundary (SigmaRaw Eta etaBody)
open RigidityInitiality
open P01AC.EffectiveCompleteness (N)
open SourceRigidity (zero)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- The external schema uses the same actual source Ty/Poly, but genuinely
ranges over the recursively extended formation and typing judgments. -/
theorem full_sigma_schema (Γ : Tel) (A B P : Ty) (d z : Poly)
    (hc : CtxJ Γ) (ha : FormJ Γ A) (hb : FormJ (A :: Γ) B)
    (hp : FormJ (.sigma A B :: Γ) P)
    (hd : HasJ (B :: A :: Γ) d (SigmaCompletion.branchType P))
    (hz : HasJ Γ z (.sigma A B)) :
    ∃ t, HasJ Γ t (inst P z) ∧
      P01DF.PolyConv t (SigmaCompletion.branchAt d (fstPoly z) (sndPoly z)) :=
  ⟨_,.sigmaElim hc ha hb hp hd hz,.refl _⟩

theorem full_induction_schema (Γ : Tel) (P : Ty) (p s : Poly)
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero)) (hs : HasJ Γ s (dependentStepType P)) :
    ∃ t, HasJ Γ t (.pi N P) := ⟨_,.natInduction hc hP hp hs⟩

theorem sigma_form {Γ} (hc : Ctx Γ) : Form Γ SigmaRaw :=
  .sigma (.raw hc) (.raw (.ext hc (.raw hc)))

theorem eta_form {Γ} (hc : Ctx Γ) : Form Γ Eta := by
  have hs := sigma_form hc
  have hm := SigmaCompletion.eta_motive_formed hc (.raw hc) (.raw (.ext hc (.raw hc)))
  exact .pi hs hm

/-- New source witness of the exact literal Eta that unchanged HasE lacks. -/
theorem eta_has_in {Γ} (hc : Ctx Γ) : HasJ Γ (abstract (.atom .i)) Eta := by
  have c : Ctx (SigmaRaw :: Γ) := .ext hc (sigma_form hc)
  have a : Form (SigmaRaw :: Γ) .raw := .raw c
  have b : Form (.raw :: SigmaRaw :: Γ) .raw := .raw (.ext c a)
  have hP := SigmaCompletion.eta_motive_formed c a b
  have hd := SigmaCompletion.canonical_eta_branch c a b
  have hz : Has (SigmaRaw :: Γ) (.var 0) SigmaRaw := .var (sigma_form c) .zero
  have h := HasJ.sigmaElim (.ctxBase (P01AC.ExtensionalRepair.ctx_inclusion c))
    (.formBase (P01AC.ExtensionalRepair.form_inclusion a))
    (.formBase (P01AC.ExtensionalRepair.form_inclusion b))
    (.formBase (P01AC.ExtensionalRepair.form_inclusion hP))
    (.hasBase (P01AC.ExtensionalRepair.has_inclusion hd))
    (.hasBase (P01AC.ExtensionalRepair.has_inclusion hz))
  have body : HasJ (SigmaRaw :: Γ) (.atom .i) etaBody := by
    simpa only [SigmaCompletion.eta_motive_at] using h
  exact .piIntro (.formBase (P01AC.ExtensionalRepair.form_inclusion (eta_form hc)))
    body (by simp [abstract,freeZero,drop,Scoped,pren,psub])

theorem eta_has : HasJ [] (abstract (.atom .i)) Eta := eta_has_in Ctx.nil

theorem eta_strict : ¬ ∃ p, HasE [] p Eta := fun ⟨p,h⟩ => SigmaTagBoundary.no_eta p h

def etaWitness : Poly := abstract (.atom .i)
def etaStep : Poly := abstract (.atom .i)

theorem constant_eta_family : FormE [N] (wk Eta) := by
  have hc : Ctx [N] := .ext .nil (P01AC.EffectiveCompleteness.N_form Ctx.nil)
  exact P01AC.ExtensionalRepair.form_inclusion (eta_form hc)

theorem constant_eta_step : HasE [] etaStep (dependentStepType (wk Eta)) := by
  have c : Ctx [N] := .ext .nil (P01AC.EffectiveCompleteness.N_form Ctx.nil)
  have hE := eta_form c
  have hi : Has [N] (.atom .i) (arr Eta Eta) :=
    .i hE (P01AC.form_arr hE hE)
  have hform : Form [] (.pi N (arr Eta Eta)) :=
    .pi (P01AC.EffectiveCompleteness.N_form Ctx.nil) (P01AC.form_arr hE hE)
  have h : Has [] etaStep (.pi N (arr Eta Eta)) := .piIntro hform hi (by simp [abstract,freeZero,drop,Scoped,pren,psub])
  exact P01AC.ExtensionalRepair.has_inclusion h

/-- The induction premise here is the genuinely new Sigma-elimination result.
This witnesses interaction of the two rules in one finite source derivation. -/
theorem combined_section : HasJ [] (sectionPoly etaWitness etaStep) (.pi N (wk Eta)) :=
  .natInduction .nil (.formBase constant_eta_family)
    (show HasJ [] etaWitness (inst (wk Eta) zero) by simpa only [inst_wk] using eta_has)
    (.hasBase constant_eta_step)

theorem combined_section_not_old (p : Poly) : ¬ HasE [] p (.pi N (wk Eta)) := by
  intro h
  have hc : CtxE [] := .nil
  have he : FormE [] Eta := P01AC.ExtensionalRepair.form_inclusion (eta_form Ctx.nil)
  have hf : FormE [] (.pi N (wk Eta)) := .pi (RigidityInitiality.FullE.N_form hc) constant_eta_family
  have hh := HasE.piElim hf (show FormE [] (inst (wk Eta) zero) by simpa only [inst_wk] using he)
    h (RigidityInitiality.FullE.zero_has_N hc)
  exact SigmaTagBoundary.no_eta _ (by simpa only [inst_wk] using hh)

/-- This source-syntax motive is formed using a genuinely new endpoint typing. -/
def newMotive : Ty := .identity Eta etaWitness etaWitness

theorem newMotive_subst (σ : Nat → Poly) : subst σ newMotive = newMotive := by
  simp [newMotive,Eta,etaBody,SigmaRaw,etaWitness,abstract,freeZero,drop,pren,psub,
    subst,pup,pairPoly,fstPoly,sndPoly]

theorem new_motive_form {Γ} (hc : Ctx Γ) : FormJ Γ newMotive :=
  .identity (.formBase (P01AC.ExtensionalRepair.form_inclusion (eta_form hc)))
    (eta_has_in hc) (eta_has_in hc)

theorem new_motive_proof {Γ} (hc : Ctx Γ) : HasJ Γ (.atom .i) newMotive :=
  .identityIntro (new_motive_form hc) (eta_has_in hc) (eta_has_in hc) (.refl _)

theorem new_motive_not_old : ¬ FormE [] newMotive := by
  intro h
  cases h with
  | identity _ hp _ => exact SigmaTagBoundary.no_eta _ hp

theorem new_motive_at_N : FormJ [N] newMotive :=
  new_motive_form (.ext .nil (P01AC.EffectiveCompleteness.N_form Ctx.nil))

theorem new_motive_at_N_not_old : ¬ FormE [N] newMotive := by
  intro h
  cases h with
  | identity _ hp _ =>
    have hf : FormE [] (.pi N (wk Eta)) :=
      .pi (RigidityInitiality.FullE.N_form .nil) constant_eta_family
    have hpi := HasE.piIntro hf hp
      (show Scoped 0 (abstract etaWitness) by simp [etaWitness,abstract,freeZero,drop,Scoped,pren,psub])
    exact combined_section_not_old _ hpi

/-- Re-enter Sigma elimination with both a newly formed motive and a newly
available branch. This is not merely a wrapper around old FormE/HasE inputs. -/
theorem new_motive_reentry : HasJ [] (.atom .i) newMotive := by
  have cS : Ctx [SigmaRaw] := .ext .nil (sigma_form .nil)
  have cR : Ctx [.raw] := .ext .nil (.raw .nil)
  have cRR : Ctx [.raw,.raw] := .ext cR (.raw cR)
  have hi : Has [] (.atom .i) .raw := .rawAtom (.raw .nil)
  have hz : Has [] (pairPoly (.atom .i) (.atom .i)) SigmaRaw :=
    .sigmaIntro (sigma_form .nil) (.raw .nil) hi hi
  have h := HasJ.sigmaElim .nil (.formBase (.raw .nil))
    (.formBase (.raw (P01AC.ExtensionalRepair.ctx_inclusion cR)))
    (new_motive_form cS)
    (show HasJ [.raw,.raw] (.atom .i) (SigmaCompletion.branchType newMotive) by
      simpa only [SigmaCompletion.branchType,newMotive_subst] using new_motive_proof cRR)
    (.hasBase (P01AC.ExtensionalRepair.has_inclusion hz))
  simpa only [inst,newMotive_subst] using h

theorem nested_new_formation : FormJ [] (.identity newMotive (.atom .i) (.atom .i)) :=
  .identity (new_motive_form .nil) new_motive_reentry new_motive_reentry

/-- A concrete projection-equivalent pair remains distinct at faithful Raw. -/
theorem raw_pair_eta_fails :
    ¬ OpenTermStandardness.Conv OpenTermStandardness.T.i
      (FullPER.pair (FullPER.first OpenTermStandardness.T.i)
        (FullPER.second OpenTermStandardness.T.i)) := SigmaTagBoundary.ghost_not_tag

theorem sigma_eta_at_same_ghost (ρ : FullPER.REnv) (η : FullPER.Env) :
    FullPER.F SigmaRaw ρ η OpenTermStandardness.T.i
      (FullPER.pair (FullPER.first OpenTermStandardness.T.i)
        (FullPER.second OpenTermStandardness.T.i)) :=
  ⟨(OpenTermStandardness.fst_pair _ _).symm,(OpenTermStandardness.snd_pair _ _).symm⟩

#print axioms new_motive_at_N_not_old
#print axioms new_motive_reentry
#print axioms nested_new_formation
#print axioms full_sigma_schema
#print axioms full_induction_schema
#print axioms eta_has
#print axioms combined_section
#print axioms combined_section_not_old
#print axioms raw_pair_eta_fails
#print axioms sigma_eta_at_same_ghost
end JointCompletion.Controls
