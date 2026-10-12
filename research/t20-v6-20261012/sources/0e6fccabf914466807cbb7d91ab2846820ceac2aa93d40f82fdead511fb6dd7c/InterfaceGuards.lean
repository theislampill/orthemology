import LookupCode
import PolyExact
namespace IndependentAuxiliaryInterfaces
open Encodable AuxiliaryCertificates AuxiliaryCodeComputability OrthemologyV2 OrthemologyV3 P01D P01AC
-- Explicit root qualification guards the intended Mathlib class and tuple order.
theorem step_PR : _root_.Primrec (fun p : Nat × (Nat × Nat) => checkStepCode p.1 p.2.1 p.2.2) := primrec_checkStepCode
theorem red_PR : _root_.Primrec (fun p : Nat × (Nat × Nat) => checkRedCode p.1 p.2.1 p.2.2) := primrec_checkRedCode
theorem finite_PR : _root_.Primrec (fun p : Nat × (Nat × Nat) => checkFiniteCode p.1 p.2.1 p.2.2) := primrec_checkFiniteCode
theorem poly_PR : _root_.Primrec (fun p : Nat × (Nat × Nat) => checkPolyCode p.1 p.2.1 p.2.2) := primrec_checkPolyCode
theorem lookup_PR : _root_.Primrec (fun p : Nat × (Nat × (Nat × Nat)) => checkLookupCode p.1 p.2.1 p.2.2.1 p.2.2.2) := primrec_checkLookupCode
-- No malformed-code or decoder claim is substituted for canonical exactness.
theorem step_exact : ∀ (c : StepCert) (t u : Term), checkStepCode (encode c) (encode t) (encode u) = AuxiliaryCertificates.checkStep c t u := checkStepCode_exact
theorem red_exact : ∀ (c : RedCert) (t u : Term), checkRedCode (encode c) (encode t) (encode u) = AuxiliaryCertificates.checkRed c t u := checkRedCode_exact
theorem finite_exact : ∀ (c : FiniteCert) (t : Term) (A : TypeCode), checkFiniteCode (encode c) (encode t) (encode A) = AuxiliaryCertificates.checkFinite c t A := checkFiniteCode_exact
theorem poly_exact : ∀ (c : PolyCert) (p q : Poly), checkPolyCode (encode c) (encode p) (encode q) = AuxiliaryCertificates.checkPoly c p q := checkPolyCode_exact
theorem lookup_exact : ∀ (c : LookupCert) (Γ : Tel) (n : Nat) (A : Ty), checkLookupCode (encode c) (encode Γ) n (encode A) = AuxiliaryCertificates.checkLookup c Γ n A := checkLookupCode_exact
end IndependentAuxiliaryInterfaces
