import ConstructorDescriptors
import StepCode
import PolyCode
import SerializedCertificateCodec
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

def stepCertDescription : Description := [
  [(true, 0)],
  [(true, 0), (true, 0)],
  [(true, 0), (true, 0), (true, 0)],
  [(true, 0), (true, 0), (true, 0), (false, 6)],
  [(true, 0), (true, 0), (true, 0), (false, 6)]]

def redCertDescription : Description := [
  [(true, 0)],
  [(true, 0), (true, 0), (true, 0), (true, 6), (false, 7)]]

@[simp] theorem encode_RedCert_refl (a0 : OrthemologyV2.Term) : encode (AuxiliaryCertificates.RedCert.refl a0) = pack 0 [leaf (encode a0)] := rfl

@[simp] theorem encode_RedCert_tail (a0 : OrthemologyV2.Term) (a1 : OrthemologyV2.Term) (a2 : OrthemologyV2.Term) (a3 : AuxiliaryCertificates.StepCert) (a4 : AuxiliaryCertificates.RedCert) : encode (AuxiliaryCertificates.RedCert.tail a0 a1 a2 a3 a4) = pack 1 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), encode a4] := rfl

def finiteCertDescription : Description := [
  [(true, 1)],
  [(true, 1), (true, 1)],
  [(true, 1), (true, 1), (true, 1)],
  [(true, 0), (true, 0), (true, 1), (true, 1), (false, 8), (false, 8)],
  [(true, 0), (true, 1), (false, 8)],
  [(true, 0), (true, 1), (true, 1), (false, 8)],
  [(true, 0), (true, 0), (true, 1), (false, 8), (true, 7)]]

@[simp] theorem encode_FiniteCert_i (a0 : OrthemologyV2.TypeCode) : encode (AuxiliaryCertificates.FiniteCert.i a0) = pack 0 [leaf (encode a0)] := rfl

@[simp] theorem encode_FiniteCert_k (a0 : OrthemologyV2.TypeCode) (a1 : OrthemologyV2.TypeCode) : encode (AuxiliaryCertificates.FiniteCert.k a0 a1) = pack 1 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_FiniteCert_s (a0 : OrthemologyV2.TypeCode) (a1 : OrthemologyV2.TypeCode) (a2 : OrthemologyV2.TypeCode) : encode (AuxiliaryCertificates.FiniteCert.s a0 a1 a2) = pack 2 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_FiniteCert_app (a0 : OrthemologyV2.Term) (a1 : OrthemologyV2.Term) (a2 : OrthemologyV2.TypeCode) (a3 : OrthemologyV2.TypeCode) (a4 : AuxiliaryCertificates.FiniteCert) (a5 : AuxiliaryCertificates.FiniteCert) : encode (AuxiliaryCertificates.FiniteCert.app a0 a1 a2 a3 a4 a5) = pack 3 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), encode a4, encode a5] := rfl

@[simp] theorem encode_FiniteCert_allI (a0 : OrthemologyV2.Term) (a1 : OrthemologyV2.TypeCode) (a2 : AuxiliaryCertificates.FiniteCert) : encode (AuxiliaryCertificates.FiniteCert.allI a0 a1 a2) = pack 4 [leaf (encode a0), leaf (encode a1), encode a2] := rfl

@[simp] theorem encode_FiniteCert_allE (a0 : OrthemologyV2.Term) (a1 : OrthemologyV2.TypeCode) (a2 : OrthemologyV2.TypeCode) (a3 : AuxiliaryCertificates.FiniteCert) : encode (AuxiliaryCertificates.FiniteCert.allE a0 a1 a2 a3) = pack 5 [leaf (encode a0), leaf (encode a1), leaf (encode a2), encode a3] := rfl

@[simp] theorem encode_FiniteCert_reduce (a0 : OrthemologyV2.Term) (a1 : OrthemologyV2.Term) (a2 : OrthemologyV2.TypeCode) (a3 : AuxiliaryCertificates.FiniteCert) (a4 : AuxiliaryCertificates.RedCert) : encode (AuxiliaryCertificates.FiniteCert.reduce a0 a1 a2 a3 a4) = pack 6 [leaf (encode a0), leaf (encode a1), leaf (encode a2), encode a3, leaf (encode a4)] := rfl

def polyCertDescription : Description := [
  [(true, 2)],
  [(true, 2), (true, 2), (false, 9)],
  [(true, 2), (true, 2), (true, 2), (false, 9), (false, 9)],
  [(true, 2), (true, 2), (true, 2), (true, 2), (false, 9), (false, 9)],
  [(true, 2)],
  [(true, 2), (true, 2)],
  [(true, 2), (true, 2), (true, 2)],
  [(true, 0), (true, 0)]]

def lookupCertDescription : Description := [
  [(true, 5), (true, 3)],
  [(true, 5), (true, 4), (true, 3), (true, 3), (false, 10)]]

@[simp] theorem encode_LookupCert_zero (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (AuxiliaryCertificates.LookupCert.zero a0 a1) = pack 0 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_LookupCert_succ (a0 : P01AC.Tel) (a1 : Nat) (a2 : P01AC.Ty) (a3 : P01AC.Ty) (a4 : AuxiliaryCertificates.LookupCert) : encode (AuxiliaryCertificates.LookupCert.succ a0 a1 a2 a3 a4) = pack 1 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), encode a4] := rfl

def claimDescription : Description := [
  [(true, 5)],
  [(true, 5), (true, 3)],
  [(true, 5), (true, 2), (true, 3)],
  [(true, 5)],
  [(true, 5), (true, 3)],
  [(true, 5), (true, 2), (true, 3)]]

@[simp] theorem encode_Claim_ctxJ (a0 : P01AC.Tel) : encode (JointCertificates.Claim.ctxJ a0) = pack 0 [leaf (encode a0)] := rfl

@[simp] theorem encode_Claim_formJ (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Claim.formJ a0 a1) = pack 1 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Claim_hasJ (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01AC.Ty) : encode (JointCertificates.Claim.hasJ a0 a1 a2) = pack 2 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Claim_ctxE (a0 : P01AC.Tel) : encode (JointCertificates.Claim.ctxE a0) = pack 3 [leaf (encode a0)] := rfl

@[simp] theorem encode_Claim_formE (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Claim.formE a0 a1) = pack 4 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Claim_hasE (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01AC.Ty) : encode (JointCertificates.Claim.hasE a0 a1 a2) = pack 5 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

def ruleDescription : Description := [
  [(true, 5)],
  [],
  [(true, 5), (true, 3)],
  [(true, 5), (true, 3)],
  [(true, 5), (true, 4)],
  [(true, 5)],
  [(true, 5), (true, 3)],
  [(true, 5)],
  [(true, 5), (true, 3), (true, 3)],
  [(true, 5), (true, 3), (true, 3)],
  [(true, 5), (true, 3), (true, 2), (true, 2)],
  [(true, 5), (true, 2), (true, 3)],
  [(true, 5), (true, 3), (true, 4), (true, 10)],
  [(true, 5), (true, 3)],
  [(true, 5), (true, 3), (true, 3)],
  [(true, 5), (true, 3), (true, 3), (true, 3)],
  [(true, 1), (true, 5), (true, 0), (true, 5), (true, 8)],
  [(true, 5), (true, 3), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2)],
  [(true, 5), (true, 0)],
  [(true, 5), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 2), (true, 9)],
  [(true, 5), (true, 3), (true, 2), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 3), (true, 2), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 2), (true, 9)],
  [(true, 5), (true, 3), (true, 3), (true, 2), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 3), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 2)],
  [],
  [(true, 5), (true, 3)],
  [(true, 5), (true, 4)],
  [(true, 5)],
  [(true, 5), (true, 3)],
  [(true, 5)],
  [(true, 5), (true, 3), (true, 3)],
  [(true, 5), (true, 3), (true, 3)],
  [(true, 5), (true, 3), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 4), (true, 10)],
  [(true, 5), (true, 3)],
  [(true, 5), (true, 3), (true, 3)],
  [(true, 5), (true, 3), (true, 3), (true, 3)],
  [(true, 1), (true, 5), (true, 0), (true, 5), (true, 8)],
  [(true, 5), (true, 3), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2)],
  [(true, 5), (true, 0)],
  [(true, 5), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2)],
  [(true, 5), (true, 3), (true, 3), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 2), (true, 9)],
  [(true, 5), (true, 3), (true, 2), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 3), (true, 2), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 2), (true, 9)],
  [(true, 5), (true, 3), (true, 3), (true, 2), (true, 2), (true, 2)],
  [(true, 5), (true, 3), (true, 2), (true, 2), (true, 2)]]

@[simp] theorem encode_Rule_CtxJ_ctxBase (a0 : P01AC.Tel) : encode (JointCertificates.Rule.CtxJ_ctxBase a0) = pack 0 [leaf (encode a0)] := rfl

@[simp] theorem encode_Rule_CtxJ_nil  : encode (JointCertificates.Rule.CtxJ_nil) = pack 1 [] := rfl

@[simp] theorem encode_Rule_CtxJ_ext (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Rule.CtxJ_ext a0 a1) = pack 2 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_FormJ_formBase (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Rule.FormJ_formBase a0 a1) = pack 3 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_FormJ_param (a0 : P01AC.Tel) (a1 : Nat) : encode (JointCertificates.Rule.FormJ_param a0 a1) = pack 4 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_FormJ_bottom (a0 : P01AC.Tel) : encode (JointCertificates.Rule.FormJ_bottom a0) = pack 5 [leaf (encode a0)] := rfl

@[simp] theorem encode_Rule_FormJ_all (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Rule.FormJ_all a0 a1) = pack 6 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_FormJ_raw (a0 : P01AC.Tel) : encode (JointCertificates.Rule.FormJ_raw a0) = pack 7 [leaf (encode a0)] := rfl

@[simp] theorem encode_Rule_FormJ_pi (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) : encode (JointCertificates.Rule.FormJ_pi a0 a1 a2) = pack 8 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_FormJ_sigma (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) : encode (JointCertificates.Rule.FormJ_sigma a0 a1 a2) = pack 9 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_FormJ_identity (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) : encode (JointCertificates.Rule.FormJ_identity a0 a1 a2 a3) = pack 10 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasJ_hasBase (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01AC.Ty) : encode (JointCertificates.Rule.HasJ_hasBase a0 a1 a2) = pack 11 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_HasJ_var (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : Nat) (a3 : AuxiliaryCertificates.LookupCert) : encode (JointCertificates.Rule.HasJ_var a0 a1 a2 a3) = pack 12 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasJ_i (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Rule.HasJ_i a0 a1) = pack 13 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_HasJ_k (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) : encode (JointCertificates.Rule.HasJ_k a0 a1 a2) = pack 14 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_HasJ_s (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) : encode (JointCertificates.Rule.HasJ_s a0 a1 a2 a3) = pack 15 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasJ_finite (a0 : OrthemologyV2.TypeCode) (a1 : P01AC.Tel) (a2 : OrthemologyV2.Term) (a3 : List P01AC.Ty) (a4 : AuxiliaryCertificates.FiniteCert) : encode (JointCertificates.Rule.HasJ_finite a0 a1 a2 a3 a4) = pack 16 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasJ_allIntro (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_allIntro a0 a1 a2) = pack 17 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_HasJ_allElim (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_allElim a0 a1 a2 a3) = pack 18 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasJ_rawAtom (a0 : P01AC.Tel) (a1 : OrthemologyV2.Term) : encode (JointCertificates.Rule.HasJ_rawAtom a0 a1) = pack 19 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_HasJ_rawApp (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_rawApp a0 a1 a2) = pack 20 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_HasJ_piIntro (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_piIntro a0 a1 a2 a3) = pack 21 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasJ_piElim (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_piElim a0 a1 a2 a3 a4) = pack 22 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasJ_sigmaIntro (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_sigmaIntro a0 a1 a2 a3 a4) = pack 23 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasJ_sigmaFst (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_sigmaFst a0 a1 a2 a3) = pack 24 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasJ_sigmaSnd (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_sigmaSnd a0 a1 a2 a3) = pack 25 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasJ_identityIntro (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) : encode (JointCertificates.Rule.HasJ_identityIntro a0 a1 a2 a3 a4) = pack 26 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasJ_proofErase (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_proofErase a0 a1 a2 a3 a4) = pack 27 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasJ_j (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) (a6 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_j a0 a1 a2 a3 a4 a5 a6) = pack 28 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4), leaf (encode a5), leaf (encode a6)] := rfl

@[simp] theorem encode_Rule_HasJ_conv (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) : encode (JointCertificates.Rule.HasJ_conv a0 a1 a2 a3 a4) = pack 29 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasJ_piExt (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) (a5 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_piExt a0 a1 a2 a3 a4 a5) = pack 30 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4), leaf (encode a5)] := rfl

@[simp] theorem encode_Rule_HasJ_allExt (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_allExt a0 a1 a2 a3 a4) = pack 31 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasJ_sigmaElim (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_sigmaElim a0 a1 a2 a3 a4 a5) = pack 32 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4), leaf (encode a5)] := rfl

@[simp] theorem encode_Rule_HasJ_natInduction (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasJ_natInduction a0 a1 a2 a3) = pack 33 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_CtxE_nil  : encode (JointCertificates.Rule.CtxE_nil) = pack 34 [] := rfl

@[simp] theorem encode_Rule_CtxE_ext (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Rule.CtxE_ext a0 a1) = pack 35 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_FormE_param (a0 : P01AC.Tel) (a1 : Nat) : encode (JointCertificates.Rule.FormE_param a0 a1) = pack 36 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_FormE_bottom (a0 : P01AC.Tel) : encode (JointCertificates.Rule.FormE_bottom a0) = pack 37 [leaf (encode a0)] := rfl

@[simp] theorem encode_Rule_FormE_all (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Rule.FormE_all a0 a1) = pack 38 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_FormE_raw (a0 : P01AC.Tel) : encode (JointCertificates.Rule.FormE_raw a0) = pack 39 [leaf (encode a0)] := rfl

@[simp] theorem encode_Rule_FormE_pi (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) : encode (JointCertificates.Rule.FormE_pi a0 a1 a2) = pack 40 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_FormE_sigma (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) : encode (JointCertificates.Rule.FormE_sigma a0 a1 a2) = pack 41 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_FormE_identity (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) : encode (JointCertificates.Rule.FormE_identity a0 a1 a2 a3) = pack 42 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasE_var (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : Nat) (a3 : AuxiliaryCertificates.LookupCert) : encode (JointCertificates.Rule.HasE_var a0 a1 a2 a3) = pack 43 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasE_i (a0 : P01AC.Tel) (a1 : P01AC.Ty) : encode (JointCertificates.Rule.HasE_i a0 a1) = pack 44 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_HasE_k (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) : encode (JointCertificates.Rule.HasE_k a0 a1 a2) = pack 45 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_HasE_s (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) : encode (JointCertificates.Rule.HasE_s a0 a1 a2 a3) = pack 46 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasE_finite (a0 : OrthemologyV2.TypeCode) (a1 : P01AC.Tel) (a2 : OrthemologyV2.Term) (a3 : List P01AC.Ty) (a4 : AuxiliaryCertificates.FiniteCert) : encode (JointCertificates.Rule.HasE_finite a0 a1 a2 a3 a4) = pack 47 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasE_allIntro (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) : encode (JointCertificates.Rule.HasE_allIntro a0 a1 a2) = pack 48 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_HasE_allElim (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasE_allElim a0 a1 a2 a3) = pack 49 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasE_rawAtom (a0 : P01AC.Tel) (a1 : OrthemologyV2.Term) : encode (JointCertificates.Rule.HasE_rawAtom a0 a1) = pack 50 [leaf (encode a0), leaf (encode a1)] := rfl

@[simp] theorem encode_Rule_HasE_rawApp (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01D.Poly) : encode (JointCertificates.Rule.HasE_rawApp a0 a1 a2) = pack 51 [leaf (encode a0), leaf (encode a1), leaf (encode a2)] := rfl

@[simp] theorem encode_Rule_HasE_piIntro (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasE_piIntro a0 a1 a2 a3) = pack 52 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasE_piElim (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) : encode (JointCertificates.Rule.HasE_piElim a0 a1 a2 a3 a4) = pack 53 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasE_sigmaIntro (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) : encode (JointCertificates.Rule.HasE_sigmaIntro a0 a1 a2 a3 a4) = pack 54 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasE_sigmaFst (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasE_sigmaFst a0 a1 a2 a3) = pack 55 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasE_sigmaSnd (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) : encode (JointCertificates.Rule.HasE_sigmaSnd a0 a1 a2 a3) = pack 56 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3)] := rfl

@[simp] theorem encode_Rule_HasE_identityIntro (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) : encode (JointCertificates.Rule.HasE_identityIntro a0 a1 a2 a3 a4) = pack 57 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasE_proofErase (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) : encode (JointCertificates.Rule.HasE_proofErase a0 a1 a2 a3 a4) = pack 58 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasE_j (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) (a6 : P01D.Poly) : encode (JointCertificates.Rule.HasE_j a0 a1 a2 a3 a4 a5 a6) = pack 59 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4), leaf (encode a5), leaf (encode a6)] := rfl

@[simp] theorem encode_Rule_HasE_conv (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) : encode (JointCertificates.Rule.HasE_conv a0 a1 a2 a3 a4) = pack 60 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

@[simp] theorem encode_Rule_HasE_piExt (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) (a5 : P01D.Poly) : encode (JointCertificates.Rule.HasE_piExt a0 a1 a2 a3 a4 a5) = pack 61 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4), leaf (encode a5)] := rfl

@[simp] theorem encode_Rule_HasE_allExt (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) : encode (JointCertificates.Rule.HasE_allExt a0 a1 a2 a3 a4) = pack 62 [leaf (encode a0), leaf (encode a1), leaf (encode a2), leaf (encode a3), leaf (encode a4)] := rfl

def serialCertDescription : Description := [
  [(true, 12), (false, 14)]]

@[simp] theorem encode_SerialCert_node (a0 : JointCertificates.Rule) (a1 : JointCertificates.SerialCertList) : encode (JointCertificates.SerialCert.node a0 a1) = pack 0 [leaf (encode a0), encode a1] := rfl

def serialCertListDescription : Description := [
  [],
  [(false, 13), (false, 14)]]

@[simp] theorem encode_SerialCertList_nil  : encode (JointCertificates.SerialCertList.nil) = pack 0 [] := rfl

@[simp] theorem encode_SerialCertList_cons (a0 : JointCertificates.SerialCert) (a1 : JointCertificates.SerialCertList) : encode (JointCertificates.SerialCertList.cons a0 a1) = pack 1 [encode a0, encode a1] := rfl

end CertificateCodeValidity
