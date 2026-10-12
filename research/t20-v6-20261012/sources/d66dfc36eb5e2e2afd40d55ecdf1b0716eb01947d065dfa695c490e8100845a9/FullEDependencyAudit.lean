import Lean
import FullEInductionControls
import IndependentBinderJControl
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
  let main := [``RigidityInitiality.FullE.dependent_section_curried,
      ``RigidityInitiality.FullE.section_has, ``RigidityInitiality.FullE.rigidity_implies_section,
      ``RigidityInitiality.FullE.section_zero_law, ``RigidityInitiality.FullE.section_successor_law,
      ``RigidityInitiality.FullE.section_application_identity]
  for root in main do
    let some ci := env.find? root | throwError "Missing theorem {root}"
    for old in [``P01AC.Ctx, ``P01AC.Form, ``P01AC.Has] do
      unless countConstant old ci.type == 0 do throwError "Hidden original premise: {root} {old}"
    let (_, st) := ((Lean.CollectAxioms.collect root).run env).run {}
    for ax in st.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom in {root}: {ax}"
    let forbidden := st.visited.toList.filter fun n =>
      n.toString.startsWith "RigidityDiscriminator." ||
      n.toString.startsWith "FullPER." ||
      n.toString.startsWith "HomogeneousOriginal." ||
      n.toString == "P01AC.ExtensionalRepair.unary_fundamental" ||
      n.toString == "RigidityInitiality.dependent_section_from_rigidity" ||
      n.toString == "RigidityInitiality.dependent_section_curried" ||
      n.toString == "RigidityInitiality.section_has" ||
      n.toString == "RigidityInitiality.rigidity_implies_section"
    unless forbidden.isEmpty do throwError "Forbidden dependency in {root}: {forbidden}"
    logInfo m!"PASS actual-E premise interface, source-only construction and foundation axioms: {root}"
  for (root, needed) in [
      (``RigidityInitiality.FullE.fold_has, ``P01AC.ExtensionalRepair.Structural.allElim_formed),
      (``RigidityInitiality.FullE.dependent_section_curried, ``RigidityInitiality.FullE.rigidity_elim),
      (``RigidityInitiality.FullE.section_has, ``P01AC.ExtensionalRepair.Structural.has_wk),
      (``RigidityInitiality.FullE.rigidity_implies_section, ``P01AC.ExtensionalRepair.HasE.piIntro),
      (``RigidityInitiality.FullE.section_successor_law, ``RigidityInitiality.FullE.projection_returns_input),
      (``RigidityInitiality.FullE.section_successor_law, ``P01AC.ExtensionalRepair.HasE.j),
      (``FullEIndependentReview.j_transport_control, ``RigidityInitiality.FullE.transport_source)] do
    let (_, st) := ((Lean.CollectAxioms.collect root).run env).run {}
    unless st.visited.contains needed do throwError "Missing intended dependency {root}: {needed}"
  let some (.thmInfo rawBeta) := env.find? ``RigidityInitiality.FullE.section_application_beta
    | throwError "Missing raw beta alias"
  unless countConstant ``RigidityInitiality.section_application_beta rawBeta.value == 1 do
    throwError "Raw beta alias did not use literal retained theorem"
  let (_, zero) := ((Lean.CollectAxioms.collect ``RigidityInitiality.FullE.section_zero_law).run env).run {}
  if zero.visited.contains ``RigidityInitiality.FullE.rigidity_elim then
    throwError "Zero law unexpectedly consumes rigidity"
  logInfo "PASS exact retained beta alias; actual substitution, All elimination, Pi binding and J; zero law independent of R."
