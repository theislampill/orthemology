/- Nonempty construction examples in the NEW dependent replay target.
   Not executions: compilation and all audits remain unverified at 4.19.0. -/
import P01Certificates
namespace P01D
open OrthemologyV2 OrthemologyV3

def constantTy (Γ : Context) (P : PER) : Ty Γ where
  obj := fun _ => P
  coherent := fun _ => rfl

def identity_rel (P : PER) : (ArrPER P P).dom .i := by
  intro x y hxy
  exact P.raw (.symm (.step (.i x))) (.symm (.step (.i y))) hxy

def identity_link {P Q} (R : Link P Q) : (arrowLink R R).rel .i .i := by
  refine ⟨identity_rel P,identity_rel Q,?_⟩
  intro x y hxy
  exact R.raw (.symm (.step (.i x))) (.symm (.step (.i y))) hxy

def idParamFamily : ParamFamily where
  obj := fun P => ArrPER P P
  link := fun R => arrowLink R R
  identity := fun P => arrow_identity P P

def idBodyTy (Γ : Context) : Ty (typeExtend Γ) where
  obj := fun γ => ArrPER γ.2 γ.2
  coherent := fun h => congrArg (fun P => ArrPER P P) h.2

def idAllFormation (Γ : Context) : AllFormation (idBodyTy Γ) where
  family := fun _ => idParamFamily
  body := fun _ _ => rfl
  coherent := fun _ => rfl

def idAllBody (Γ : Context) : Tm (typeExtend Γ) (idBodyTy Γ) where
  code := .atom .i
  valid := fun {γ δ} _ => identity_rel γ.2

noncomputable def polymorphicIdentity (Γ : Context) : Tm Γ (allTy (idAllFormation Γ)) :=
  allIntro (idAllFormation Γ) (idAllBody Γ) (fun _ _ _ R => identity_link R)

noncomputable def polymorphicIdentitySelf (Γ : Context) :=
  allSelf (idAllFormation Γ) (polymorphicIdentity Γ)

def atomIdentity : Tm nilContext (constantTy nilContext rawPER) where
  code := .atom .i
  valid := fun _ => Conv.refl .i

/-- A genuine dependent type, Pi x:A. Id_A(x,x), not a canonical TypeCode arrow
    containing a secretly added identity constructor. -/
noncomputable def dependentReflexivity :=
  lam (reflTm («variable» nilContext (constantTy nilContext rawPER)))

noncomputable def dependentReflexivityEnvelope :
    P01Certificate.DependentEnvelope nilContext
      (piTy (identityTy («variable» nilContext (constantTy nilContext rawPER))
        («variable» nilContext (constantTy nilContext rawPER))))
      (.app (.atom .k) (.atom .i)) :=
  ⟨dependentReflexivity, by simp [dependentReflexivity, lam, reflTm, abstract, freeZero, drop, pren, psub]⟩

def pairBody : Ty (extend nilContext (constantTy nilContext rawPER)) :=
  constantTy _ rawPER

noncomputable def representedPair : Tm nilContext (sigmaTy pairBody) :=
  pair atomIdentity (show Tm nilContext (instanceTy pairBody atomIdentity) from atomIdentity)

theorem representedPair_eta (γ : nilContext.Val) :
    Conv (representedPair.at γ) ((pair (fst representedPair) (snd representedPair)).at γ) :=
  sigma_eta_context representedPair γ

noncomputable def constantMotive : Ty (idContext atomIdentity) := constantTy _ rawPER

noncomputable def basedJExample :=
  j atomIdentity atomIdentity (baseProof atomIdentity) constantMotive
    (show Tm nilContext (constantMotive.pull (baseSub atomIdentity)) from atomIdentity)

theorem basedJExample_computes (γ : nilContext.Val) : Red (basedJExample.at γ) .i :=
  j_computation atomIdentity atomIdentity (baseProof atomIdentity) constantMotive atomIdentity γ

/-- The same finite I program satisfies the uniform hypothesis at every code and
    every endpoint-aware relation. No arbitrary unary membership was promoted. -/
theorem polymorphicIdentity_uniform (P Q : PER) (R : Link P Q) :
    (idParamFamily.link R).rel .i .i := identity_link R
end P01D
