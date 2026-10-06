import UnaryCurrentIdentityBoundary
import RuntimeBoundaryInventory
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.UnaryIdentity P01AC.UnaryIdentity.IntensionalBoundary
open Lean Elab Command UnaryIndependentAudit
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
namespace CurrentBoundaryIndependent

-- Root and deeply compatible contexts of all three reduction rules are rejected.
example : normalCheck (.app .zero (.app .i .one)) = false := rfl
example : normalCheck (.app (.app .i .one) .zero) = false := rfl
example : normalCheck (.app (.app .k .zero) .one) = false := rfl
example : normalCheck (.app (.app (.app .s .i) .k) .one) = false := rfl
example : normalCheck (.app .s .i) = true := rfl
example : normalCheck (.app (.app .s .i) .k) = true := rfl
example : normalCheck (.app .zero .one) = true := rfl
example (t : OrthemologyV2.Term) (h : normalCheck t = true) (u : OrthemologyV2.Term) : ¬ Step t u :=
  normalCheck_sound h u

-- All proof polynomials and all original current typing derivations are excluded.
example (r : Poly) (h : Has [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed)) : False :=
  endpoints_not_convertible (P01AC.Intensional.closed_identity_conversion h)
example (r : Poly) :
    ¬ P01AC.Intensional.Plus.HasPlus [] r
      (.identity (arr N N) variableExpr.closed redundantExpr.closed) := no_bridge_identity r
example : oldVariable.closed = variableExpr.closed ∧ oldRedundant.closed = redundantExpr.closed :=
  ⟨rfl,rfl⟩
example : P01AC.RestrictedIdentityV2.identityCheck oldVariable oldRedundant = true := by decide
example : identityCheck variableExpr redundantExpr = true := rfl
example : ∃ r : Poly, ∀ R : REnv,
    G (.identity (arr N N) variableExpr.closed redundantExpr.closed) R zeroEnv zeroEnv
      (eval r zeroEnv) (eval r zeroEnv) :=
  (identityCheck_iff_semantic_witness _ _).mp checker_accepts

def termNodes : OrthemologyV2.Term → Nat
  | .app f x => 1 + termNodes f + termNodes x
  | _ => 1
example : termNodes (eval redundantExpr.closed zeroEnv) = 237 := by
  simp [redundantExpr, P01AC.UnaryIdentity.Expr.closed, P01AC.UnaryIdentity.Expr.body,
    P01AC.UnaryIdentity.Expr.toPR, PR.compile, P01AC.RestrictedIdentity.closeMany,
    P01AC.RestrictedIdentity.binary, P01AC.RestrictedIdentity.addPR,
    P01AC.RestrictedIdentity.constantPR, recPoly, recStep, recStepBody, recImages,
    succPoly, succBody, inputNumeral, iterationPoly, abstract, freeZero, drop,
    pren, psub, pairPoly, fstPoly, sndPoly, eval, termNodes]

-- Semantic evidence is insensitive to arbitrary term environments for these closed endpoints.
example (R : REnv) (η ξ : Env) :
    G (.identity (arr N N) variableExpr.closed redundantExpr.closed) R η ξ .i .i := by
  rw [G_identity]
  rw [eval_closed (has_scoped variableExpr.closed_has) η zeroEnv,
      eval_closed (has_scoped redundantExpr.closed_has) η zeroEnv,
      eval_closed (has_scoped variableExpr.closed_has) ξ zeroEnv,
      eval_closed (has_scoped redundantExpr.closed_has) ξ zeroEnv]
  exact ⟨endpoints_semantically_equal R.left, endpoints_semantically_equal R.right, .refl _, .refl _⟩
end CurrentBoundaryIndependent

run_cmd do
  let env ← getEnv
  let mut roots : Array Name := #[]
  for (n,info) in env.constants.toList do
    if `P01AC.UnaryIdentity.IntensionalBoundary |>.isPrefixOf n then
      unless info.isUnsafe || info.isPartial do roots := roots.push n
  let (count,axes) ← EffectiveKernelAudit.auditClosure roots
  let oc ← auditOpaqueBoundary roots
  logInfo m!"SUPPLEMENTAL_ALL_SAFE_CLOSURE_PASS roots={roots.size}; declarations={count}; axioms={axes}; opaqueChecked={oc}"
  inventoryRuntimeBoundary "CurrentIdentityBoundary" #[`P01AC.UnaryIdentity.IntensionalBoundary.rootRedex,
      `P01AC.UnaryIdentity.IntensionalBoundary.normalCheck] #[`P01AC.UnaryIdentity.IntensionalBoundary]

run_cmd do
  let env ← getEnv
  let authored : Array Name := #[`P01AC.UnaryIdentity.IntensionalBoundary.rootRedex,
    `P01AC.UnaryIdentity.IntensionalBoundary.normalCheck,
    `P01AC.UnaryIdentity.IntensionalBoundary.step_normalCheck_false,
    `P01AC.UnaryIdentity.IntensionalBoundary.normalCheck_sound,
    `P01AC.UnaryIdentity.IntensionalBoundary.variableExpr,
    `P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr,
    `P01AC.UnaryIdentity.IntensionalBoundary.variable_raw,
    `P01AC.UnaryIdentity.IntensionalBoundary.variable_normal,
    `P01AC.UnaryIdentity.IntensionalBoundary.redundant_normal,
    `P01AC.UnaryIdentity.IntensionalBoundary.endpoint_syntax_ne,
    `P01AC.UnaryIdentity.IntensionalBoundary.endpoints_not_convertible,
    `P01AC.UnaryIdentity.IntensionalBoundary.checker_accepts,
    `P01AC.UnaryIdentity.IntensionalBoundary.endpoints_semantically_equal,
    `P01AC.UnaryIdentity.IntensionalBoundary.no_current_identity,
    `P01AC.UnaryIdentity.IntensionalBoundary.no_current_identity_witness,
    `P01AC.UnaryIdentity.IntensionalBoundary.no_bridge_identity,
    `P01AC.UnaryIdentity.IntensionalBoundary.compiled_image_counterexample,
    `P01AC.UnaryIdentity.IntensionalBoundary.oldVariable,
    `P01AC.UnaryIdentity.IntensionalBoundary.oldRedundant,
    `P01AC.UnaryIdentity.IntensionalBoundary.old_variable_literal,
    `P01AC.UnaryIdentity.IntensionalBoundary.old_redundant_literal,
    `P01AC.UnaryIdentity.IntensionalBoundary.old_checker_accepts,
    `P01AC.UnaryIdentity.IntensionalBoundary.old_no_current_identity,
    `P01AC.UnaryIdentity.IntensionalBoundary.old_fragment_counterexample]
  for n in authored do
    let some info := env.checked.get.find? n | throwError "MISSING_AUTHORED_ROOT {n}"
    if info.isAxiom || info.isUnsafe || info.isPartial then throwError "INVALID_AUTHORED_ROOT {n}"
    if Lean.isNoncomputable env n || (Lean.Compiler.getImplementedBy? env n).isSome ||
        (Lean.getExternAttrData? env n).isSome then throwError "AUTHORED_RUNTIME_OVERRIDE {n}"
  logInfo m!"SUPPLEMENTAL_AUTHORED_ROOTS_PASS count={authored.size}"
