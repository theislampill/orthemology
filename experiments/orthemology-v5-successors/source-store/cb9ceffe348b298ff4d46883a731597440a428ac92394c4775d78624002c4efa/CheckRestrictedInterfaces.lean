import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
namespace IndependentV2Controls
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

def s0 : Mask 2 := fun _ => false
def s1 : Mask 2 := fun i => i.val == 1
def s2 : Mask 2 := fun i => i.val == 0
def s3 : Mask 2 := fun _ => true
def a0 : Exponent 2 := fun _ => 0
def aX : Exponent 2 := fun i => if i.val = 0 then 1 else 0
def aY : Exponent 2 := fun i => if i.val = 1 then 1 else 0
def x : Expr 2 := .variable ⟨0, by decide⟩
def y : Expr 2 := .variable ⟨1, by decide⟩
def c (n : Nat) : Expr 2 := .constant n

-- Noncanonical sparse lists are intentional: equality sums repeated exponents.
example : coeffEqual [(aX, 2), (aY, 0), (aX, 3)] [(aX, 5)] = true := by decide
example : coeffEqual [(aX, 2), (aX, 3)] [(aX, 4)] = false := by decide
example : coeffEqual ([] : Sparse 2) [(aX, 1)] = false := by decide
example : coeffEqual [(aX, 1)] ([] : Sparse 2) = false := by decide
example : coeffEqual [(aX, 0), (aY, 0)] ([] : Sparse 2) = true := by decide
example : coeffEqual [(aX, 1)] [(aY, 1)] = false := by decide
example : coeffEqual [(fun i : Fin 2 => i.val + 0, 3)] [(fun i => i.val, 3)] = true := by decide
example : zeroTest [(aX, 0), (aY, 0)] = true := by decide
example : zeroTest [(aX, 0), (aY, 1)] = false := by decide
example : zeroTest (normalise s3 (c 0)) = true := by decide
example : (normalise s3 (c 0)).isEmpty = false := by decide
example : coeffEqual (multiply [(aX, 2), (aX, 0)] [(aY, 3)])
    [(fun _ => 1, 6)] = true := by decide

-- Dead variables disappear before branch selection or coefficient comparison.
example : zeroTest (normalise s1 x) = true := by decide
example : identityCheck (.ifZero (.mul x (c 0)) y (c 91)) y = true := by decide
example : coeffEqual (normalise s0 x) [(aX, 1)] = false := by decide
example : coeffEqual (normalise s0 x) [(aX, 0)] = true := by decide
example : coeffEqual (normalise s1 (.ifZero (.add x y) (c 7) (c 9))) [(a0, 9)] = true := by decide

def piece : Expr 2 := .ifZero x (.ifZero y (c 4) (c 5)) (.ifZero y (c 6) (c 7))
def good : Certificate 2 := makeCertificate piece
def duplicateOnly : Certificate 2 := [(s0, [(a0, 4)]), (s0, [(a0, 4)]),
    (s0, [(a0, 4)]), (s0, [(a0, 4)])]
def wrongLabels : Certificate 2 := [(s3, [(a0, 4)]), (s2, [(a0, 5)]),
    (s1, [(a0, 6)]), (s0, [(a0, 7)])]
def splitCoefficients : Certificate 2 := [(s0, [(a0, 1), (a0, 3), (aX, 0)]),
    (s1, [(a0, 2), (a0, 3)]), (s2, [(a0, 0), (a0, 6)]),
    (s3, [(a0, 2), (a0, 5)])]
example : verifyCertificate piece piece good = true := by decide
example : verifyCertificate piece piece good.reverse = true := by decide
example : verifyCertificate piece piece (good ++ [(s0, [(a0, 999)])]) = true := by decide
example : verifyCertificate piece piece (good ++ good) = true := by decide
example : verifyCertificate piece piece duplicateOnly = false := by decide
example : verifyCertificate piece piece wrongLabels = false := by decide
example : verifyCertificate piece piece splitCoefficients = true := by decide
example : verifyCertificate piece (c 0) good = false := by decide
example : verifyCertificate piece piece [] = false := by decide
example : verifyCertificate piece piece [(s0, [(a0, 4)]), (s1, [(a0, 5)]), (s2, [(a0, 6)])] = false := by decide

-- Empty arity is one mask and one coefficient, not no work.
example : (masks 0).length = 1 := by decide
example : (masks 4).length = 16 := by decide
example : identityCheck (.constant 0 : Expr 0) (.mul (.constant 83) (.constant 0)) = true := by decide
example : identityCheck (.constant 0 : Expr 0) (.constant 1) = false := by decide
example : verifyCertificate (.constant 0 : Expr 0) (.constant 0) [] = false := by decide
example : coeffEqual ([(fun i : Fin 0 => Fin.elim0 i, 2), (fun i => Fin.elim0 i, 3)] : Sparse 0)
    [(fun i => Fin.elim0 i, 5)] = true := by decide

-- Whole generic claims have no separation, standardness or external-oracle premise.
example {r} (e f : Expr r) : identityCheck e f = true ↔
    (∀ ρ, F (Curried r) ρ zeroEnv (eval e.closed zeroEnv) (eval f.closed zeroEnv)) :=
  identityCheck_iff_fragmentValid e f
example {r} (e f : Expr r) :
    (∃ cert : Certificate r, verifyCertificate e f cert = true) ↔ FragmentValid e f :=
  finite_certificate_complete e f
example {r} (p q : MvPolynomial (Fin r) Nat)
    (h : ∀ v : Fin r → Nat, (∀ i, 0 < v i) → MvPolynomial.eval v p = MvPolynomial.eval v q) :
    p = q := nat_polynomial_eq_of_positive_eval h

-- Actual VM execution, separately from kernel-reduced examples above.
#eval [coeffEqual [(aX, 2), (aX, 3)] [(aX, 5)],
  zeroTest [(aX, 0), (aY, 0)],
  identityCheck (.ifZero (.mul x (c 0)) y (c 91)) y,
  verifyCertificate piece piece splitCoefficients,
  verifyCertificate piece piece duplicateOnly,
  verifyCertificate piece piece wrongLabels,
  verifyCertificate piece (c 0) good]
#eval match fragmentIdentityDecidable x (.mul x x) with
  | isTrue _ => true
  | isFalse _ => false

#print P01AC.RestrictedIdentityV2.identityCheck
#print P01AC.RestrictedIdentityV2.coeffEqual
#print P01AC.RestrictedIdentityV2.rowMatches
#print P01AC.RestrictedIdentityV2.fragmentIdentityDecidable
#print axioms P01AC.RestrictedIdentityV2.identityCheck
#print axioms P01AC.RestrictedIdentityV2.verifyCertificate
#print axioms P01AC.RestrictedIdentityV2.makeCertificate
end IndependentV2Controls
