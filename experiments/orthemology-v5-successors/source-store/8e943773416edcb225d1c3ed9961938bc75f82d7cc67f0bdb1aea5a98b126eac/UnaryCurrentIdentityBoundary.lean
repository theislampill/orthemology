/- An exact pair in the literal compiler image: complete semantic equality but
   no identity inhabitant in unchanged current Has, under all its rules. -/
import UnaryNormalForm
import IdentityChecker
import IntensionalIdentitySoundness

namespace P01AC.UnaryIdentity.IntensionalBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness
open P01AC.BooleanPrimitive
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

def rootRedex : Term → Bool
  | .app .i _ => true
  | .app (.app .k _) _ => true
  | .app (.app (.app .s _) _) _ => true
  | _ => false

def normalCheck : Term → Bool
  | .app f x => !rootRedex (.app f x) && normalCheck f && normalCheck x
  | _ => true

theorem step_normalCheck_false {t u : Term} (h : Step t u) : normalCheck t = false := by
  induction h with
  | i x => rfl
  | k x y => rfl
  | s f g x => rfl
  | left h x ih => simp [normalCheck, ih]
  | right f h ih => simp [normalCheck, ih]

theorem normalCheck_sound {t : Term} (h : normalCheck t = true) : P01Source.Normal t := by
  intro u hu
  have hf := step_normalCheck_false hu
  rw [h] at hf
  cases hf

def variableExpr : Expr := .variable
def redundantExpr : Expr := .add .variable (.constant 0)

theorem variable_raw : eval variableExpr.closed zeroEnv = .i := by
  simp [variableExpr, Expr.closed, Expr.body, Expr.toPR, PR.compile,
    P01AC.RestrictedIdentity.closeMany, abstract, freeZero, eval]

theorem variable_normal : P01Source.Normal (eval variableExpr.closed zeroEnv) :=
  normalCheck_sound (by rw [variable_raw]; rfl)

theorem redundant_normal : P01Source.Normal (eval redundantExpr.closed zeroEnv) :=
  normalCheck_sound (by
    simp [redundantExpr, Expr.closed, Expr.body, Expr.toPR, PR.compile,
      P01AC.RestrictedIdentity.closeMany, P01AC.RestrictedIdentity.binary,
      P01AC.RestrictedIdentity.addPR, P01AC.RestrictedIdentity.constantPR,
      recPoly, recStep, recStepBody, recImages, succPoly, succBody,
      inputNumeral, iterationPoly, abstract, freeZero, drop, pren, psub,
      pairPoly, fstPoly, sndPoly, eval, normalCheck, rootRedex])

theorem endpoint_syntax_ne :
    eval variableExpr.closed zeroEnv ≠ eval redundantExpr.closed zeroEnv := by
  rw [variable_raw]
  simp [redundantExpr, Expr.closed, Expr.body, Expr.toPR, PR.compile,
    P01AC.RestrictedIdentity.closeMany, P01AC.RestrictedIdentity.binary,
    P01AC.RestrictedIdentity.addPR, P01AC.RestrictedIdentity.constantPR,
    recPoly, recStep, recStepBody, recImages, succPoly, succBody,
    inputNumeral, iterationPoly, abstract, freeZero, drop, pren, psub,
    pairPoly, fstPoly, sndPoly, eval]

theorem endpoints_not_convertible :
    ¬ Conv (eval variableExpr.closed zeroEnv) (eval redundantExpr.closed zeroEnv) := by
  intro h
  exact endpoint_syntax_ne (P01Source.normal_unique variable_normal redundant_normal h)

theorem checker_accepts : identityCheck variableExpr redundantExpr = true := rfl

theorem endpoints_semantically_equal : Valid variableExpr redundantExpr :=
  (identityCheck_iff_valid _ _).mp checker_accepts

theorem no_current_identity (r : Poly) :
    ¬ Has [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed) := by
  intro h
  exact endpoints_not_convertible (P01AC.Intensional.closed_identity_conversion h)

theorem no_current_identity_witness :
    ¬ ∃ r : Poly, Has [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed) := by
  rintro ⟨r,hr⟩
  exact no_current_identity r hr

theorem no_bridge_identity (r : Poly) :
    ¬ P01AC.Intensional.Plus.HasPlus [] r
      (.identity (arr N N) variableExpr.closed redundantExpr.closed) := by
  intro h
  exact endpoints_not_convertible (P01AC.Intensional.plus_closed_identity_conversion h)

theorem compiled_image_counterexample :
    Has [] variableExpr.closed (arr N N) ∧
    Has [] redundantExpr.closed (arr N N) ∧
    Form [] (.identity (arr N N) variableExpr.closed redundantExpr.closed) ∧
    identityCheck variableExpr redundantExpr = true ∧
    (∀ ρ, F (.identity (arr N N) variableExpr.closed redundantExpr.closed) ρ zeroEnv .i .i) ∧
    (∀ R : REnv, G (.identity (arr N N) variableExpr.closed redundantExpr.closed)
      R zeroEnv zeroEnv .i .i) ∧
    ¬ ∃ r : Poly, Has [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed) :=
  ⟨variableExpr.closed_has, redundantExpr.closed_has, identity_formed _ _, checker_accepts,
    (identityCheck_iff_F_identity _ _).mp checker_accepts,
    (identityCheck_iff_G_identity _ _).mp checker_accepts, no_current_identity_witness⟩

/-- These are literally in the old accepted fragment as well, not just
    extensionally simulated by its source language. -/
def oldVariable : P01AC.RestrictedIdentity.Expr 1 := .variable ⟨0, by decide⟩
def oldRedundant : P01AC.RestrictedIdentity.Expr 1 := .add oldVariable (.constant 0)

theorem old_variable_literal : oldVariable.closed = variableExpr.closed := rfl
theorem old_redundant_literal : oldRedundant.closed = redundantExpr.closed := rfl

theorem old_checker_accepts :
    P01AC.RestrictedIdentityV2.identityCheck oldVariable oldRedundant = true := by decide

theorem old_no_current_identity (r : Poly) :
    ¬ Has [] r (.identity (P01AC.RestrictedIdentity.Curried 1)
      oldVariable.closed oldRedundant.closed) := no_current_identity r

theorem old_fragment_counterexample :
    P01AC.RestrictedIdentityV2.identityCheck oldVariable oldRedundant = true ∧
    Has [] oldVariable.closed (P01AC.RestrictedIdentity.Curried 1) ∧
    Has [] oldRedundant.closed (P01AC.RestrictedIdentity.Curried 1) ∧
    (∀ R : REnv, G (.identity (P01AC.RestrictedIdentity.Curried 1)
      oldVariable.closed oldRedundant.closed) R zeroEnv zeroEnv .i .i) ∧
    ¬ ∃ r : Poly, Has [] r (.identity (P01AC.RestrictedIdentity.Curried 1)
      oldVariable.closed oldRedundant.closed) :=
  ⟨old_checker_accepts, oldVariable.closed_has, oldRedundant.closed_has,
    (identityCheck_iff_G_identity _ _).mp checker_accepts,
    no_current_identity_witness⟩

#print axioms normalCheck_sound
#print axioms endpoints_not_convertible
#print axioms no_current_identity
#print axioms no_bridge_identity
#print axioms old_fragment_counterexample
end P01AC.UnaryIdentity.IntensionalBoundary
