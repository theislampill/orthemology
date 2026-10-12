import LookupCode
import PolyExact
import GrammarImage
namespace AuxiliaryCodeComputability.Controls
open Encodable AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC
open AuxiliaryCodeComputability ExactSyntaxValidity SourceFamilyComputability CodedScope
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair

/-- The source I step, and its contextual lifting, remain accepted. -/
example (x f : Term) :
    checkStepCode (encode (.right f (.app .i x) x (.i x) : StepCert))
      (encode (.app f (.app .i x) : Term)) (encode (.app f x : Term)) = true := by
  rw [checkStepCode_exact]; simp [checkStep]

/-- Duplicate source claims are checked, rather than trusted. -/
example : checkStepCode (encode (StepCert.left .i .k .s (.i .k)))
    (encode (Term.app .i .s)) (encode (Term.app .k .s)) = false := by
  rw [checkStepCode_exact]; decide

/-- A reduction tail retains the intermediate term connecting step and rest. -/
example (x : Term) : checkRedCode
    (encode (.tail (.app .i x) x x (.i x) (.refl x) : RedCert))
    (encode (.app .i x : Term)) (encode x) = true := by
  rw [checkRedCode_exact]; simp [checkRed,checkStep]
example : checkRedCode
    (encode (.tail (.app .i .k) .k .s (.i .k) (.refl .s) : RedCert))
    (encode (.app .i .k : Term)) (encode Term.s) = false := by
  rw [checkRedCode_exact]; decide

/-- Symmetry reverses outer endpoints while preserving child orientation. -/
example (p : Poly) : checkPolyCode
    (encode (PolyCert.symm (.app (.atom .i) p) p (.i p)))
    (encode p) (encode (.app (.atom .i) p : Poly)) = true := by
  rw [checkPolyCode_exact]; simp [checkPoly]
example : checkPolyCode
    (encode (PolyCert.symm (.var 0) (.var 1) (.refl (.var 0))))
    (encode (Poly.var 1)) (encode (Poly.var 0)) = false := by
  rw [checkPolyCode_exact]; decide

/-- Matching outer endpoints cannot hide a mismatched transitivity middle. -/
example : checkPolyCode
    (encode (PolyCert.trans (.var 0) (.var 1) (.var 0) (.refl (.var 0)) (.refl (.var 0))))
    (encode (Poly.var 0)) (encode (Poly.var 0)) = false := by
  rw [checkPolyCode_exact]; decide

/-- Term application inside an atom and polynomial application stay distinct. -/
example (r t : Term) : checkPolyCode (encode (PolyCert.bridge r t))
    (encode (Poly.atom (.app r t))) (encode (.app (.atom r) (.atom t) : Poly)) = true := by
  rw [checkPolyCode_exact]; simp [checkPoly]
example : checkPolyCode (encode (PolyCert.bridge .i .k))
    (encode (Poly.app (.atom .i) (.atom .k))) (encode (Poly.app (.atom .i) (.atom .k))) = false := by
  rw [checkPolyCode_exact]; decide

/-- Polymorphic finite certificates use the actual type instantiation. -/
example (A : TypeCode) : checkFiniteCode
    (encode (FiniteCert.allE .i (.arrow (.var 0) (.var 0)) A
      (.allI .i (.arrow (.var 0) (.var 0)) (.i (.var 0)))))
    (encode Term.i) (encode (instantiateType (.arrow (.var 0) (.var 0)) A)) = true := by
  rw [checkFiniteCode_exact]; simp [checkFinite]

/-- A finite reduction certificate cannot use a reduction with a wrong start. -/
example : checkFiniteCode
    (encode (FiniteCert.reduce .i .k (.arrow .bottom .bottom) (.i .bottom) (.refl .k)))
    (encode Term.k) (encode (TypeCode.arrow .bottom .bottom)) = false := by
  rw [checkFiniteCode_exact]; decide

/-- Lookup preserves the actual weakening in identity endpoints. -/
example (Γ : Tel) (A : Ty) : checkLookupCode (encode (LookupCert.zero Γ A))
    (encode (A :: Γ)) 0 (encode (wk A)) = true := by
  rw [checkLookupCode_exact]; simp [checkLookup]
example : checkLookupCode
    (encode (LookupCert.zero [] (.identity .raw (.var 0) (.var 0))))
    (encode ([.identity .raw (.var 0) (.var 0)] : Tel)) 0
    (encode (Ty.identity .raw (.var 0) (.var 0))) = false := by
  rw [checkLookupCode_exact]; decide

/-- This deliberately ungated total extension accepts a malformed polynomial
    payload. The separate canonical membership gate is therefore necessary. -/
example : checkPolyCode (pack 0 [leaf 0]) 0 0 = true := by
  rw [checkPolyCode,evaluate]
  simp [polyShape,polyChildren,pack,tag,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,
    arg1,arg2,arg3,unpair_leaf]
example : valid 2 0 = false := by
  rw [valid,evaluate]
  norm_num [shape,ExactSyntaxValidity.polyShape,tag,first,rest,arg1,unary,node,leaf,Nat.pair]

end AuxiliaryCodeComputability.Controls
