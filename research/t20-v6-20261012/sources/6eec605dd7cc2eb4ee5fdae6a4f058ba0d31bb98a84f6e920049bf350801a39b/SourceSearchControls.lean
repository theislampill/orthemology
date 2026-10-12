import TypeInhabitationSearch
import Lean
namespace ActualSourceEnumerability.Controls
open Encodable JointCertificates P01AC P01D AuxiliaryCertificates CodedRuleTemplates
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000

def empty : DerivationCertificate := .node .CtxJ_nil []
def raw : DerivationCertificate := .node (.FormJ_raw []) [empty]
def bottom : DerivationCertificate := .node (.FormJ_bottom []) [empty]
def extension : DerivationCertificate := .node (.CtxJ_ext [] .raw) [empty, raw]
def missing : DerivationCertificate := .node (.CtxJ_ext [] .raw) [empty]
def extra : DerivationCertificate := .node (.CtxJ_ext [] .raw) [empty, raw, empty]
def swapped : DerivationCertificate := .node (.CtxJ_ext [] .raw) [raw, empty]
def rawAtom : DerivationCertificate := .node (.HasJ_rawAtom [] .i) [raw]
def falseConversion : DerivationCertificate :=
  .node (.HasJ_conv [] .raw (.atom .i) (.atom .zero) (.refl (.atom .i))) [raw, rawAtom]
def fullSupport : Rule :=
  .HasJ_finite (.arrow (.var 0) (.var 0)) [] .i [.raw, .bottom] (.i (.var 0))
def droppedUnusedImage : DerivationCertificate := .node fullSupport [raw]

local macro "source_decide" : tactic => `(tactic|
  (simp only [check, Certificate.checkRoot, Certificate.check_node,
    empty, raw, bottom, extension, missing, extra, swapped, rawAtom, falseConversion,
    fullSupport, droppedUnusedImage, Certificate.rule, List.map_cons, List.map_nil,
    List.all_cons, List.all_nil, Rule.checkSide, Rule.premises, Rule.conclusion,
    Bool.true_and, Bool.and_true, Bool.false_and, Bool.and_false, decide_true, decide_false] <;> decide))

theorem acceptEmpty : checkCanonical (encode (Claim.ctxJ [])) (encodeCertificate empty) = true := by
  rw [checkCanonical_encode]; source_decide
theorem acceptExtension : checkCanonical (encode (Claim.ctxJ [.raw])) (encodeCertificate extension) = true := by
  rw [checkCanonical_encode]; source_decide
theorem rejectMissing : checkCanonical (encode (Claim.ctxJ [.raw])) (encodeCertificate missing) = false := by
  rw [checkCanonical_encode]; source_decide
theorem rejectExtra : checkCanonical (encode (Claim.ctxJ [.raw])) (encodeCertificate extra) = false := by
  rw [checkCanonical_encode]; source_decide
/-- This swaps DISTINCT claims. No claim is made that swapping interchangeable
    certificates of the same claim must be rejected. -/
theorem rejectDistinctSwap : checkCanonical (encode (Claim.ctxJ [.raw])) (encodeCertificate swapped) = false := by
  rw [checkCanonical_encode]; source_decide
theorem rejectWrongRoot : checkCanonical (encode (Claim.ctxE [])) (encodeCertificate empty) = false := by
  rw [checkCanonical_encode]; source_decide
theorem rejectFalseConversion : checkCanonical (encode (.hasJ [] (.atom .zero) .raw : Claim))
    (encodeCertificate falseConversion) = false := by
  rw [checkCanonical_encode]; source_decide
/-- Both images remain, including the bottom image unused by the finite type. -/
theorem fullSupportPremises : premisesCode (encode fullSupport) =
    ([.formJ [] .raw, .formJ [] .bottom, .formJ [] (.pi .raw .raw)] : List Claim).map encode := by
  rw [premisesCode_exact]; rfl
theorem rejectDroppedUnusedImage : checkCanonical (encode fullSupport.conclusion)
    (encodeCertificate droppedUnusedImage) = false := by
  rw [checkCanonical_encode]; source_decide

theorem rejectInvalidClaim (c : Nat) (h : CertificateCodeValidity.certValid 11 0 = false) :
    checkCanonical 0 c = false := by simp only [checkCanonical, h, Bool.false_and]

theorem rejectClaimZero : CertificateCodeValidity.certValid 11 0 = false := by
  rw [CertificateCodeValidity.certValid, ExactSyntaxValidity.evaluate]
  decide

theorem rejectCertZero : CertificateCodeValidity.certValid 13 0 = false := by
  rw [CertificateCodeValidity.certValid, ExactSyntaxValidity.evaluate]
  decide

theorem malformedClaimRejectsEveryCertificate (c : Nat) : checkCanonical 0 c = false :=
  rejectInvalidClaim c rejectClaimZero

theorem malformedCertificateRejectsEveryClaim (q : Nat) : checkCanonical q 0 = false := by
  simp only [checkCanonical, rejectCertZero, Bool.and_false, Bool.false_and]

theorem invalidClaimSearchUndefined : ¬ (proofSearch 0).Dom := by
  intro h
  obtain ⟨c, hc⟩ := (derivableCode_iff_certificate 0).mp ((proofSearch_dom 0).mp h)
  rw [malformedClaimRejectsEveryCertificate] at hc
  exact Bool.false_ne_true hc

-- Supplied certificate evaluation, not execution of unbounded search.
#eval checkCanonical (encode (Claim.ctxJ [])) (encodeCertificate empty)
#eval checkCanonical (encode (Claim.ctxE [])) (encodeCertificate empty)
#eval checkCanonical 0 (encodeCertificate empty)
#eval checkCanonical (encode (Claim.ctxJ [])) 0
#print axioms acceptEmpty
#print axioms acceptExtension
#print axioms rejectMissing
#print axioms rejectExtra
#print axioms rejectDistinctSwap
#print axioms rejectWrongRoot
#print axioms rejectFalseConversion
#print axioms fullSupportPremises
#print axioms rejectDroppedUnusedImage
#print axioms malformedClaimRejectsEveryCertificate
#print axioms malformedCertificateRejectsEveryClaim
end ActualSourceEnumerability.Controls
