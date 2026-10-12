import CertificateDescriptions
import DescriptorLemmas
import TelescopeCodeValidity
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

def allDescriptions : List Description := [stepCertDescription, redCertDescription, finiteCertDescription, polyCertDescription, lookupCertDescription, claimDescription, ruleDescription, serialCertDescription, serialCertListDescription]

def certShape (b : Nat × Nat) : Bool :=
  if b.1 < 4 then valid b.1 b.2
  else if b.1 = 4 then true
  else if b.1 = 5 then validTel b.2
  else localShape (allDescriptions[b.1-6]?.getD []) b.2

def certChildren (b : Nat × Nat) : List (Nat × Nat) :=
  if b.1 < 6 then [] else localChildren (allDescriptions[b.1-6]?.getD []) b.2

def certValid (s c : Nat) : Bool := evaluate certShape certChildren (s,c)

def CertCanonical (b : Nat × Nat) : Prop :=
  if b.1 = 0 then ∃ a : OrthemologyV2.Term, encode a = b.2
  else if b.1 = 1 then ∃ a : OrthemologyV2.TypeCode, encode a = b.2
  else if b.1 = 2 then ∃ a : P01D.Poly, encode a = b.2
  else if b.1 = 3 then ∃ a : P01AC.Ty, encode a = b.2
  else if b.1 = 4 then ∃ a : Nat, encode a = b.2
  else if b.1 = 5 then ∃ a : P01AC.Tel, encode a = b.2
  else if b.1 = 6 then ∃ a : AuxiliaryCertificates.StepCert, encode a = b.2
  else if b.1 = 7 then ∃ a : AuxiliaryCertificates.RedCert, encode a = b.2
  else if b.1 = 8 then ∃ a : AuxiliaryCertificates.FiniteCert, encode a = b.2
  else if b.1 = 9 then ∃ a : AuxiliaryCertificates.PolyCert, encode a = b.2
  else if b.1 = 10 then ∃ a : AuxiliaryCertificates.LookupCert, encode a = b.2
  else if b.1 = 11 then ∃ a : JointCertificates.Claim, encode a = b.2
  else if b.1 = 12 then ∃ a : JointCertificates.Rule, encode a = b.2
  else if b.1 = 13 then ∃ a : JointCertificates.SerialCert, encode a = b.2
  else if b.1 = 14 then ∃ a : JointCertificates.SerialCertList, encode a = b.2
  else False

theorem primrec_certShape : Primrec certShape := by
  have hd : Primrec (fun b : Nat × Nat => allDescriptions[b.1-6]?.getD []) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp (Primrec.const allDescriptions)
      (Primrec.nat_sub.comp Primrec.fst (Primrec.const 6))) (Primrec.const [])
  exact Primrec.ite (Primrec.nat_lt.comp Primrec.fst (Primrec.const 4))
    (primrec_valid.comp Primrec.fst Primrec.snd)
    (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 4)) (Primrec.const true)
      (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 5))
        (primrec_validTel.comp Primrec.snd) (primrec_localShape.comp hd Primrec.snd)))

theorem primrec_certChildren : Primrec certChildren := by
  have hd : Primrec (fun b : Nat × Nat => allDescriptions[b.1-6]?.getD []) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp (Primrec.const allDescriptions)
      (Primrec.nat_sub.comp Primrec.fst (Primrec.const 6))) (Primrec.const [])
  exact Primrec.ite (Primrec.nat_lt.comp Primrec.fst (Primrec.const 6))
    (Primrec.const []) (primrec_localChildren.comp hd Primrec.snd)

theorem primrec_certValid : Primrec₂ certValid :=
  (primrec_evaluate primrec_certShape primrec_certChildren).to₂

end CertificateCodeValidity
