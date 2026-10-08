import UnaryCurrentIdentityBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.UnaryIdentity P01AC.UnaryIdentity.IntensionalBoundary
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000
namespace CurrentIdentityControls
def literalRedundant : Term := (Term.app (Term.app Term.s (Term.app (Term.app Term.s (Term.app (Term.app Term.s Term.i) (Term.app Term.k (Term.app (Term.app Term.s (Term.app (Term.app Term.s (Term.app Term.k Term.s)) (Term.app (Term.app Term.s (Term.app Term.k (Term.app Term.s Term.i))) (Term.app (Term.app Term.s (Term.app Term.k Term.k)) (Term.app (Term.app Term.s (Term.app Term.k (Term.app (Term.app Term.s (Term.app Term.k (Term.app Term.s (Term.app (Term.app Term.s (Term.app Term.k Term.s)) (Term.app (Term.app Term.s (Term.app Term.k Term.k)) Term.i))))) (Term.app (Term.app Term.s (Term.app (Term.app Term.s (Term.app Term.k Term.s)) (Term.app (Term.app Term.s (Term.app Term.k (Term.app Term.s (Term.app Term.k Term.s)))) (Term.app (Term.app Term.s (Term.app Term.k (Term.app Term.s (Term.app Term.k Term.k)))) (Term.app (Term.app Term.s (Term.app (Term.app Term.s (Term.app Term.k Term.s)) (Term.app (Term.app Term.s (Term.app Term.k Term.k)) Term.i))) (Term.app Term.k Term.i)))))) (Term.app Term.k (Term.app Term.k Term.i)))))) (Term.app (Term.app Term.s Term.i) (Term.app Term.k Term.k))))))) (Term.app (Term.app Term.s (Term.app Term.k Term.k)) (Term.app (Term.app Term.s (Term.app Term.k (Term.app (Term.app Term.s (Term.app Term.k (Term.app Term.s (Term.app (Term.app Term.s (Term.app Term.k Term.s)) (Term.app (Term.app Term.s (Term.app Term.k Term.k)) Term.i))))) (Term.app (Term.app Term.s (Term.app (Term.app Term.s (Term.app Term.k Term.s)) (Term.app (Term.app Term.s (Term.app Term.k (Term.app Term.s (Term.app Term.k Term.s)))) (Term.app (Term.app Term.s (Term.app Term.k (Term.app Term.s (Term.app Term.k Term.k)))) (Term.app (Term.app Term.s (Term.app (Term.app Term.s (Term.app Term.k Term.s)) (Term.app (Term.app Term.s (Term.app Term.k Term.k)) Term.i))) (Term.app Term.k Term.i)))))) (Term.app Term.k (Term.app Term.k Term.i)))))) (Term.app (Term.app Term.s Term.i) (Term.app Term.k (Term.app Term.k Term.i))))))))) (Term.app Term.k (Term.app (Term.app Term.s (Term.app (Term.app Term.s Term.i) (Term.app Term.k (Term.app Term.k Term.i)))) (Term.app Term.k (Term.app Term.k Term.i)))))) (Term.app Term.k (Term.app Term.k Term.i)))
example : eval redundantExpr.closed zeroEnv = literalRedundant := by
  simp [literalRedundant, redundantExpr, Expr.closed, Expr.body, Expr.toPR, PR.compile,
    P01AC.RestrictedIdentity.closeMany, P01AC.RestrictedIdentity.binary,
    P01AC.RestrictedIdentity.addPR, P01AC.RestrictedIdentity.constantPR,
    recPoly, recStep, recStepBody, recImages, succPoly, succBody,
    inputNumeral, iterationPoly, abstract, freeZero, drop, pren, psub,
    pairPoly, fstPoly, sndPoly, eval]
example : normalCheck literalRedundant = true := by decide
example : literalRedundant ≠ .i := by decide
example (r : Poly) :
    ¬ Has [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed) := no_current_identity r
example (r : Poly) :
    ¬ P01AC.Intensional.Plus.HasPlus [] r
      (.identity (arr N N) variableExpr.closed redundantExpr.closed) := no_bridge_identity r
example : oldVariable.closed = variableExpr.closed := old_variable_literal
example : oldRedundant.closed = redundantExpr.closed := old_redundant_literal
example : P01AC.RestrictedIdentityV2.identityCheck oldVariable oldRedundant = true := old_checker_accepts
example (ρ : OEnv) :
    F (.identity (arr N N) variableExpr.closed redundantExpr.closed) ρ zeroEnv .i .i :=
  (identityCheck_iff_F_identity _ _).mp checker_accepts ρ
example (R : REnv) :
    G (.identity (arr N N) variableExpr.closed redundantExpr.closed) R zeroEnv zeroEnv .i .i :=
  (identityCheck_iff_G_identity _ _).mp checker_accepts R
-- Distinct syntax without normality does not imply nonconversion.
example : Term.i ≠ Term.app Term.i Term.i := by decide
example : Conv Term.i (Term.app Term.i Term.i) := .symm (.step (.i .i))
end CurrentIdentityControls
