import RuleConclusionCode
import RulePremisesCode
import RuleSideCode
namespace CodedRuleTemplates
open P01D P01AC Encodable JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000

def ctrlAtom : Poly := .atom .i
def ctrlFinite : Rule := .HasJ_finite (.arrow .bottom .bottom) [] .i [.raw,.bottom] (.i .bottom)
def ctrlLookup : Rule := .HasJ_var [.raw] .raw 0 (.zero [] .raw)
def ctrlBadLookup : Rule := .HasJ_var [.raw] .raw 1 (.zero [] .raw)
def ctrlPoly : Rule := .HasJ_identityIntro [] .raw ctrlAtom ctrlAtom (.refl ctrlAtom)
def ctrlBadPoly : Rule := .HasJ_identityIntro [] .raw ctrlAtom (.atom .k) (.refl ctrlAtom)
def ctrlPiIntro : Rule := .HasJ_piIntro [] .raw .raw (.var 0)
def ctrlBadPiIntro : Rule := .HasJ_piIntro [] .raw .raw (.var 1)
def ctrlBadConv : Rule := .HasJ_conv [] .raw (.var 0) (.var 0) (.refl (.var 0))
def ctrlPiExt : Rule := .HasJ_piExt [] .raw (.identity .raw (.var 0) (.var 0)) ctrlAtom ctrlAtom ctrlAtom
def ctrlAllExt : Rule := .HasJ_allExt [] (.identity .raw (.var 0) (.var 0)) ctrlAtom ctrlAtom ctrlAtom

/-- Every supplied image remains a formation obligation, even if unused by C. -/
theorem finite_premises_length (C : TypeCode) (Γ : Tel) (t : Term) (τ : List Ty) (c : FiniteCert) :
    (premisesCode (encode (Rule.HasJ_finite C Γ t τ c))).length = τ.length + 1 := by
  rw [premisesCode_exact]
  simp only [Rule.premises,List.length_map,List.length_append,List.length_ofFn,List.length_singleton]

theorem finite_premises_order (C : TypeCode) (Γ : Tel) (t : Term) (τ : List Ty) (c : FiniteCert) :
    premisesCode (encode (Rule.HasJ_finite C Γ t τ c)) =
      (τ.map (fun A => encode (Claim.formJ Γ A))) ++ [encode (Claim.formJ Γ (tsubst (typeImages τ) (fin C)))] := by
  rw [premisesCode_exact]
  simp only [Rule.premises,List.map_append,List.map_cons,List.map_nil,ofFn_typeImages,List.map_map,Function.comp_def]

theorem unused_image_retained : (premisesCode (encode ctrlFinite)).length = 3 := by
  exact finite_premises_length _ _ _ _ _

theorem section_symbolic (p s : Poly) : sectionPolyCode (encode p) (encode s) = encode (RigidityInitiality.sectionPoly p s) := sectionPolyCode_exact p s

#eval [
  decide (conclusionCode (encode Rule.CtxJ_nil) = encode (Claim.ctxJ [])),
  decide (premisesCode (encode Rule.CtxJ_nil) = []),
  checkSideCode (encode ctrlFinite),
  decide ((premisesCode (encode ctrlFinite)).length = 3),
  decide (premisesCode (encode ctrlFinite) =
    [encode (Claim.formJ [] .raw),encode (Claim.formJ [] .bottom),encode (Claim.formJ [] (tsubst (typeImages [.raw,.bottom]) (fin (.arrow .bottom .bottom))))]),
  checkSideCode (encode ctrlLookup),
  !(checkSideCode (encode ctrlBadLookup)),
  checkSideCode (encode ctrlPoly),
  !(checkSideCode (encode ctrlBadPoly)),
  checkSideCode (encode ctrlPiIntro),
  !(checkSideCode (encode ctrlBadPiIntro)),
  !(checkSideCode (encode ctrlBadConv)),
  checkSideCode (encode ctrlPiExt),
  !(checkSideCode (encode ctrlAllExt)),
  decide (branchAtCode (encode (Poly.app (.var 0) (.var 1))) (encode (Poly.atom .k)) (encode ctrlAtom) = encode (Poly.app ctrlAtom (.atom .k))),
  decide (motiveAtCode (encode (Ty.identity .raw (.var 0) (.var 1))) (encode (Poly.atom .k)) (encode ctrlAtom) = encode (Ty.identity .raw ctrlAtom (.atom .k))),
  decide (conclusionCode (encode (.HasE_piExt [] .raw .raw ctrlAtom ctrlAtom ctrlAtom : Rule)) = encode ((.HasE_piExt [] .raw .raw ctrlAtom ctrlAtom ctrlAtom : Rule).conclusion))]

end CodedRuleTemplates
