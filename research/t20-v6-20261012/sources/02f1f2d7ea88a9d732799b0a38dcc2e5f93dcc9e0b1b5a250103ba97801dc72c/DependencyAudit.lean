import Lean
import IndependentMixedControls
import IndependentJConversion
import IndependentDependentTarget
open Lean Elab Command
private partial def countConstant (target : Name) : Expr → Nat
  | .const n _ => if n == target then 1 else 0
  | .app f a => countConstant target f + countConstant target a
  | .lam _ t b _ => countConstant target t + countConstant target b
  | .forallE _ t b _ => countConstant target t + countConstant target b
  | .letE _ t v b _ => countConstant target t + countConstant target v + countConstant target b
  | .mdata _ b => countConstant target b
  | .proj _ _ b => countConstant target b
  | _ => 0
run_cmd do
  let env ← getEnv
  for (target, ct) in [( ``P01AC.ExtensionalRepair.CtxE, 2),
      (``P01AC.ExtensionalRepair.FormE, 7), (``P01AC.ExtensionalRepair.HasE, 20),
      (``P01AC.Intensional.Plus.PolyConvPlus, 8)] do
    let some (.inductInfo info) := env.find? target
      | throwError "Expected unchanged inductive {target}"
    unless info.ctors.length == ct do throwError "Changed constructor count for {target}"
    logInfo m!"Unchanged grammar {target}: {info.ctors}"
  let core := ``P01AC.ExtensionalRepair.Structural.form_mixed
  let (_, st) := ((Lean.CollectAxioms.collect core).run env).run {}
  for ax in st.axioms do
    unless [``propext, ``Quot.sound].contains ax do throwError "Unexpected core axiom: {ax}"
  for forbidden in [`P01AC.form_mixed, `P01AC.has_mixed, `P01AC.MixedSubstitution,
      `P01AC.Has, `P01AC.Form, `P01AC.Ctx, `FullPER.fundamental,
      `P01AC.ExtensionalRepair.unary_fundamental] do
    if st.visited.contains forbidden then throwError "Forbidden structural dependency: {forbidden}"
  for needed in [``P01AC.ExtensionalRepair.FormE.rec,
      ``P01AC.ExtensionalRepair.HasE.piExt, ``P01AC.ExtensionalRepair.HasE.allExt,
      ``P01AC.ExtensionalRepair.HasE.j, ``P01AC.ExtensionalRepair.HasE.conv,
      ``P01AC.ExtensionalRepair.Structural.form_scoped,
      ``P01AC.ExtensionalRepair.Structural.MixedSubstitution.lift,
      ``P01AC.ExtensionalRepair.Structural.MixedSubstitution.twk,
      ``P01AC.ExtensionalRepair.Structural.MixedSubstitution.theta] do
    unless st.visited.contains needed do throwError "Missing structural dependency: {needed}"
  for (target, needed) in [( ``HasEMixedReview.pi_ext_input, ``P01AC.ExtensionalRepair.HasE.piExt),
      (``HasEMixedReview.all_ext_input, ``P01AC.ExtensionalRepair.HasE.allExt),
      (``HasEMixedReview.j_input, ``P01AC.ExtensionalRepair.HasE.j),
      (``HasEMixedReview.conv_j_input, ``P01AC.ExtensionalRepair.HasE.conv)] do
    let some (.thmInfo info) := env.find? target | throwError "Missing theorem {target}"
    unless countConstant needed info.value == 1 do
      throwError "Expected exactly one direct use of {needed} in {target}"
  logInfo "PASS: unchanged grammar; actual mutual induction and both binder lifts; no original-Has or semantic-reflection dependency; actual extensional/J/conversion control inputs."
