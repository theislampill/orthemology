import JointCompletionAlgebra

namespace JointCompletion.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Finite term scope for the actual joint syntax, including recursive completion inputs. -/
theorem has_scoped {Γ : Tel} {p : Poly} {A : Ty} (h : HasJ Γ p A) :
    Scoped Γ.length p := by
  induction h using HasJ.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun _ _ _ => True) with
  | ctxBase => trivial
  | formBase => trivial
  | hasBase h => exact P01AC.ExtensionalRepair.ClosedProofCanonicalisation.has_scope h
  | nil => trivial
  | ext => trivial
  | param => trivial
  | bottom => trivial
  | all => trivial
  | raw => trivial
  | pi => trivial
  | sigma => trivial
  | identity => trivial
  | var hA hn ih => exact lookup_lt hn
  | i => trivial
  | k => trivial
  | s => trivial
  | finite => trivial
  | allIntro hF hp iF ip => simpa only [twkTel, List.length_map] using ip
  | allElim hF hA hI hp iF iA iI ip => exact ip
  | rawAtom => trivial
  | rawApp hF hf ha iF ihf iha => exact ⟨ihf, iha⟩
  | piIntro hF hb hs iF ihb => exact hs
  | piElim hF hI hf ha iF iI ihf iha => exact ⟨ihf, iha⟩
  | sigmaIntro hF hI ha hb iF iI iha ihb => exact scoped_pair iha ihb
  | sigmaFst hA hF hz iA iF ihz => exact scoped_fst ihz
  | sigmaSnd hF hI hz iF iI ihz => exact scoped_snd ihz
  | identityIntro => trivial
  | proofErase hR hI hp iR iI ihp => exact ihp
  | j hA hB hI hD hE hx hy he hd iA iB iI iD iE ihx ihy ihe ihd =>
      exact scoped_j ihd ihy ihe
  | conv hA hp hc hs iA ihp => exact hs
  | piExt => trivial
  | allExt => trivial
  | sigmaElim hc hA hB hP hd hz ic iA iB iP id iz =>
      exact branchAt_scoped id (scoped_fst iz) (scoped_snd iz)
  | natInduction hc hP hp hs ic iP ip is => exact sectionPoly_scoped ip is

/-- Type-index scope follows syntactically, with all embedded identity terms covered. -/
theorem form_scoped {Γ : Tel} {A : Ty} (h : FormJ Γ A) : TyScoped Γ.length A := by
  induction h using FormJ.rec
    (motive_1 := fun _ _ => True) (motive_3 := fun _ _ _ _ => True) with
  | formBase h => exact P01AC.ExtensionalRepair.Structural.form_scoped h
  | all _ _ _ ih => simpa only [twkTel, List.length_map] using ih
  | pi _ _ ia ib => exact ⟨ia, ib⟩
  | sigma _ _ ia ib => exact ⟨ia, ib⟩
  | identity _ hp hq ia _ _ => exact ⟨ia, has_scoped hp, has_scoped hq⟩
  | _ => trivial

#print axioms has_scoped
#print axioms form_scoped
end JointCompletion.Structural
