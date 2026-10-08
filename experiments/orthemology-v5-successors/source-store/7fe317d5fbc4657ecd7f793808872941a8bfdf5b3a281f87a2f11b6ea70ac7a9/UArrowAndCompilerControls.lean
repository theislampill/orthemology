/- Isolated Eighteenth countercontrol. Frozen syntax and compiler are imported
   without modification. This file does not claim the x/x+0 HasE identity. -/
import ExtensionalRepairSyntax
import UnaryCurrentIdentityBoundary

namespace P01AC.ExtensionalRepair.UArrowControl
open OrthemologyV2 OrthemologyV3 P01D P01R

def U : Ty := .all (.param 0)
def P : Ty := .pi U .raw
def p : Poly := .app (.atom .k) (.atom .i)
def q : Poly := .app (.atom .k) (.atom .k)
def M : Ty := .identity .raw
  (.app (pren Nat.succ p) (.var 0))
  (.app (pren Nat.succ q) (.var 0))

theorem u_form0 : FormE [] U := .all .nil (.param .nil)
theorem ctxU : CtxE [U] := .ext .nil u_form0
theorem u_form1 : FormE [U] U := .all ctxU (.param ctxU)

theorem const_has {Γ : Tel} (c : Term) (hΓ : CtxE Γ) (hU : FormE Γ U) :
    HasE Γ (.app (.atom .k) (.atom c)) P := by
  have ha : abstract (.atom c) = .app (.atom .k) (.atom c) := by
    simp [abstract, freeZero, drop, pren, psub]
  rw [← ha]
  exact .piIntro (.pi hU (.raw (.ext hΓ hU)))
    (.rawAtom (.raw (.ext hΓ hU))) (by rw [ha]; exact ⟨trivial,trivial⟩)

theorem p0 : HasE [] p P := const_has .i .nil u_form0
theorem q0 : HasE [] q P := const_has .k .nil u_form0
theorem p1 : HasE [U] p P := const_has .i ctxU u_form1
theorem q1 : HasE [U] q P := const_has .k ctxU u_form1

theorem p_form0 : FormE [] P := .pi u_form0 (.raw ctxU)
theorem p_form1 : FormE [U] P := .pi u_form1 (.raw (.ext ctxU u_form1))
theorem variable_u : HasE [U] (.var 0) U := .var u_form1 .zero

theorem point_p : HasE [U] (.app (pren Nat.succ p) (.var 0)) .raw :=
  .piElim p_form1 (.raw ctxU) p1 variable_u
theorem point_q : HasE [U] (.app (pren Nat.succ q) (.var 0)) .raw :=
  .piElim p_form1 (.raw ctxU) q1 variable_u
theorem m_form : FormE [U] M := .identity (.raw ctxU) point_p point_q

theorem pointwise : HasE [U] (.var 0) M :=
  .allElim u_form1 m_form m_form variable_u

theorem evidence : HasE [] (.atom .i) (.pi U M) := by
  have ha : abstract (.var 0) = .atom .i := by simp [abstract, freeZero]
  rw [← ha]
  exact .piIntro (.pi u_form0 m_form) pointwise (by rw [ha]; trivial)

theorem u_arrow_identity : HasE [] (.atom .i) (.identity P p q) := by
  exact HasE.piExt u_form0 (.raw ctxU) p_form0 p0 q0 m_form
    (.pi u_form0 m_form) evidence (.identity p_form0 p0 q0)
    ⟨trivial,trivial⟩ ⟨trivial,trivial⟩ trivial trivial trivial

#print axioms u_arrow_identity
end P01AC.ExtensionalRepair.UArrowControl

namespace P01AC.ExtensionalRepair.CompilerBodyControl
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.UnaryIdentity P01AC.UnaryIdentity.IntensionalBoundary
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

/-- These are named views of the retained pair-state source terms. -/
def diagonalStepBody : Poly :=
  pairPoly (.app succPoly (fstPoly (.var 0)))
    (.app succPoly (sndPoly (.var 0)))
def diagonalStep : Poly := abstract diagonalStepBody
def diagonalZero : Poly := pairPoly (inputNumeral 0) (inputNumeral 0)
def literalPairStateBody : Poly :=
  sndPoly (.app (.app (.var 0) diagonalStep) diagonalZero)

/-- Literal equality of compiler output, not semantic replacement. -/
theorem redundant_body_exact : redundantExpr.body = literalPairStateBody := by
  simp [redundantExpr, Expr.body, Expr.toPR, PR.compile,
    P01AC.RestrictedIdentity.binary, P01AC.RestrictedIdentity.addPR,
    P01AC.RestrictedIdentity.constantPR, recPoly, recStep, recStepBody,
    recImages, succPoly, succBody, inputNumeral, iterationPoly,
    abstract, freeZero, drop, pren, psub, pairPoly, fstPoly, sndPoly,
    literalPairStateBody, diagonalStep, diagonalStepBody, diagonalZero]

theorem redundant_closed_exact : redundantExpr.closed = abstract literalPairStateBody := by
  change abstract redundantExpr.body = abstract literalPairStateBody
  rw [redundant_body_exact]

theorem variable_closed_exact : variableExpr.closed = .atom .i := by
  simp [variableExpr, Expr.closed, Expr.body, Expr.toPR, PR.compile,
    P01AC.RestrictedIdentity.closeMany, abstract, freeZero]

#print axioms redundant_body_exact
#print axioms redundant_closed_exact
#print axioms variable_closed_exact
end P01AC.ExtensionalRepair.CompilerBodyControl
