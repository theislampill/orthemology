import TypeTemplates
import CertificateDescriptions
import ListNatCodeTransport
namespace CodedRuleTemplates
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
open AuxiliaryCodeComputability CertificateCodeValidity TelescopeCodeValidity JointCertificates
set_option maxRecDepth 8192
set_option maxHeartbeats 10000000
attribute [local irreducible] Nat.pair

def ruleField (c i : Nat) := rest (slot c i)
theorem primrec_ruleField : Primrec₂ ruleField := primrec_rest.comp₂ primrec_slot

def telConsCode (A Γ : Nat) := encode (A :: listNatDecode Γ)
def twkTelCode (Γ : Nat) := encode (twkListCode (listNatDecode Γ))
def thetaCode (Γ A x : Nat) := encode (thetaListCode (listNatDecode Γ) A x)
def telLengthCode (Γ : Nat) := (listNatDecode Γ).length

theorem primrec_telConsCode : Primrec₂ telConsCode :=
  Primrec.encode.comp (Primrec.list_cons.comp Primrec.fst (primrec_listNatDecode.comp Primrec.snd))
theorem primrec_twkTelCode : Primrec twkTelCode := Primrec.encode.comp (primrec_twkListCode.comp primrec_listNatDecode)
theorem primrec_thetaCode : Primrec (fun s : Nat × Nat × Nat => thetaCode s.1 s.2.1 s.2.2) :=
  Primrec.encode.comp (primrec_thetaListCode.comp ((primrec_listNatDecode.comp Primrec.fst).pair Primrec.snd))
theorem primrec_telLengthCode : Primrec telLengthCode := Primrec.list_length.comp primrec_listNatDecode

@[simp] theorem telConsCode_exact (A : Ty) (Γ : Tel) : telConsCode (encode A) (encode Γ) = encode (A :: Γ) := by
  unfold telConsCode
  rw [listNatDecode_encode]
  exact encode_map_encode (A :: Γ)
@[simp] theorem twkTelCode_exact (Γ : Tel) : twkTelCode (encode Γ) = encode (twkTel Γ) := by
  rw [twkTelCode,listNatDecode_encode,twkListCode_exact,encode_map_encode]
@[simp] theorem thetaCode_exact (Γ : Tel) (A : Ty) (x : Poly) : thetaCode (encode Γ) (encode A) (encode x) = encode (theta Γ A x) := by
  rw [thetaCode,listNatDecode_encode,thetaListCode_exact,encode_map_encode]
@[simp] theorem telLengthCode_exact (Γ : Tel) : telLengthCode (encode Γ) = Γ.length := by
  simp [telLengthCode,listNatDecode_encode]

def ctxCode (t Γ : Nat) := pack t [leaf Γ]
def formCode (t Γ A : Nat) := pack t [leaf Γ,leaf A]
def hasCode (t Γ p A : Nat) := pack t [leaf Γ,leaf p,leaf A]

theorem primrec_ctxCode (t : Nat) : Primrec (ctxCode t) :=
  primrec_pack.comp (.const t) (Primrec.list_cons.comp primrec_leaf (.const []))
theorem primrec_formCode (t : Nat) : Primrec₂ (formCode t) :=
  primrec_pack.comp (.const t) (Primrec.list_cons.comp (primrec_leaf.comp Primrec.fst)
    (Primrec.list_cons.comp (primrec_leaf.comp Primrec.snd) (.const [])))
theorem primrec_hasCode (t : Nat) : Primrec (fun s : Nat × Nat × Nat => hasCode t s.1 s.2.1 s.2.2) :=
  primrec_pack.comp (.const t) (Primrec.list_cons.comp (primrec_leaf.comp Primrec.fst)
    (Primrec.list_cons.comp (primrec_leaf.comp (Primrec.fst.comp Primrec.snd))
      (Primrec.list_cons.comp (primrec_leaf.comp (Primrec.snd.comp Primrec.snd)) (.const []))))

@[simp] theorem ctxJCode_exact (Γ : Tel) : ctxCode 0 (encode Γ) = encode (Claim.ctxJ Γ) := rfl
@[simp] theorem ctxECode_exact (Γ : Tel) : ctxCode 3 (encode Γ) = encode (Claim.ctxE Γ) := rfl
@[simp] theorem formJCode_exact (Γ : Tel) (A : Ty) : formCode 1 (encode Γ) (encode A) = encode (Claim.formJ Γ A) := rfl
@[simp] theorem formECode_exact (Γ : Tel) (A : Ty) : formCode 4 (encode Γ) (encode A) = encode (Claim.formE Γ A) := rfl
@[simp] theorem hasJCode_exact (Γ : Tel) (p : Poly) (A : Ty) : hasCode 2 (encode Γ) (encode p) (encode A) = encode (Claim.hasJ Γ p A) := rfl
@[simp] theorem hasECode_exact (Γ : Tel) (p : Poly) (A : Ty) : hasCode 5 (encode Γ) (encode p) (encode A) = encode (Claim.hasE Γ p A) := rfl

theorem typeImages_eq_get (τ : List Ty) (i : Nat) (h : i < τ.length) : typeImages τ i = τ[i] := by
  induction τ generalizing i with
  | nil => simp at h
  | cons A τ ih => cases i with
    | zero => rfl
    | succ i => simpa [typeImages,P01F.cons] using ih i (Nat.lt_of_succ_lt_succ h)

theorem ofFn_typeImages {α : Type*} (τ : List Ty) (f : Ty → α) :
    List.ofFn (fun i : Fin τ.length => f (typeImages τ i.val)) = τ.map f := by
  have h : (fun i : Fin τ.length => f (typeImages τ i.val)) = (fun i : Fin τ.length => f τ[i.val]) := by
    funext i; rw [typeImages_eq_get τ i.val i.isLt]
  rw [h,List.ofFn_getElem_eq_map]

def formImagesCode (t Γ τ : Nat) : List Nat := (listNatDecode τ).map (formCode t Γ)

theorem primrec_formImagesCode (t : Nat) : Primrec₂ (formImagesCode t) :=
  Primrec.list_map (primrec_listNatDecode.comp Primrec.snd)
    ((primrec_formCode t).comp (Primrec.fst.comp Primrec.fst) Primrec.snd).to₂

@[simp] theorem formJImagesCode_exact (Γ : Tel) (τ : List Ty) :
    formImagesCode 1 (encode Γ) (encode τ) =
      (List.ofFn (fun i : Fin τ.length => Claim.formJ Γ (typeImages τ i.val))).map encode := by
  rw [ofFn_typeImages]
  simp only [formImagesCode,listNatDecode_encode,List.map_map,Function.comp_def,formJCode_exact]
@[simp] theorem formEImagesCode_exact (Γ : Tel) (τ : List Ty) :
    formImagesCode 4 (encode Γ) (encode τ) =
      (List.ofFn (fun i : Fin τ.length => Claim.formE Γ (typeImages τ i.val))).map encode := by
  rw [ofFn_typeImages]
  simp only [formImagesCode,listNatDecode_encode,List.map_map,Function.comp_def,formECode_exact]

def allTyCode := unary 2
def sigmaTyCode := binary 5
def tsubstTelCode (τ B : Nat) := tsubstImagesCode (listNatDecode τ) B

theorem primrec_allTyCode : Primrec allTyCode := primrec_unary_fixed 2
theorem primrec_sigmaTyCode : Primrec₂ sigmaTyCode := primrec_binary_fixed 5
theorem primrec_tsubstTelCode : Primrec₂ tsubstTelCode := primrec_tsubstImagesCode.comp (primrec_listNatDecode.comp Primrec.fst) Primrec.snd
@[simp] theorem allTyCode_exact (A : Ty) : allTyCode (encode A) = encode A.all := rfl
@[simp] theorem sigmaTyCode_exact (A B : Ty) : sigmaTyCode (encode A) (encode B) = encode (A.sigma B) := rfl
@[simp] theorem tsubstTelCode_exact (τ : List Ty) (B : Ty) : tsubstTelCode (encode τ) (encode B) = encode (tsubst (typeImages τ) B) := by
  rw [tsubstTelCode,listNatDecode_encode,tsubstImagesCode_exact]

@[simp] theorem paramCode_exact (n : Nat) : paramCode n = encode (Ty.param n) := rfl

end CodedRuleTemplates
