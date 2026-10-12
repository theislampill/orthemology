import Lean
import ExtensionInputControls
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
  let some (.inductInfo hasInfo) := env.find? ``P01AC.ExtensionalRepair.HasE
    | throwError "Actual HasE is not an inductive"
  unless hasInfo.ctors.length == 20 do throwError "Changed HasE grammar"
  let some (.inductInfo formInfo) := env.find? ``P01AC.ExtensionalRepair.FormE
    | throwError "Actual FormE is not an inductive"
  unless formInfo.ctors.length == 7 do throwError "Changed FormE grammar"
  logInfo m!"Actual grammar: {hasInfo.ctors.length} HasE constructors, {formInfo.ctors.length} FormE constructors"
  for target in [``P01AC.ExtensionalRepair.Structural.form_trename,
      ``P01AC.ExtensionalRepair.Structural.form_rename,
      ``P01AC.ExtensionalRepair.Structural.has_closed,
      ``ClosedChurchIdentity.identity_of_observation,
      ``ClosedChurchIdentity.canonicity_at_count,
      ``ClosedChurchIdentity.closed_canonicity,
      ``ClosedChurchIdentity.identity_implies_count_eq,
      ``ClosedChurchIdentity.identity_exists_iff_count_eq,
      ``EffectiveChurchIdentity.identity_iff_original_semantics,
      ``EffectiveChurchIdentity.decideTypedIdentity,
      ``EffectiveChurchIdentity.decideTypedIdentityExists] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"PASS allowed axioms for {target}: {state.axioms}"
  let (_, structural) := ((Lean.CollectAxioms.collect ``P01AC.ExtensionalRepair.Structural.has_closed).run env).run {}
  for forbidden in [``P01AC.has_rename, ``P01AC.form_rename,
      ``P01AC.BooleanPrimitive.closed_has, ``P01AC.ExtensionalRepair.unary_fundamental,
      ``FullPER.fundamental, ``ClosedScalarInstances.source_uniform_iteration] do
    if structural.visited.contains forbidden then throwError "Structural proof relies on {forbidden}"
  for needed in [``P01AC.ExtensionalRepair.Structural.form_rename,
      ``P01AC.ExtensionalRepair.Structural.form_trename,
      ``P01AC.ExtensionalRepair.FormE.rec, ``P01AC.ExtensionalRepair.HasE.piExt,
      ``P01AC.ExtensionalRepair.HasE.allExt] do
    unless structural.visited.contains needed do throwError "Structural proof omitted {needed}"
  let some (.thmInfo construct) := env.find? ``ClosedChurchIdentity.identity_of_observation
    | throwError "Identity construction is not a theorem"
  unless countConstant ``P01AC.ExtensionalRepair.HasE.piExt construct.value == 2 do
    throwError "Expected exactly two direct piExt uses"
  unless countConstant ``P01AC.ExtensionalRepair.HasE.allExt construct.value == 1 do
    throwError "Expected exactly one direct allExt use"
  let (_, canonical) := ((Lean.CollectAxioms.collect ``ClosedChurchIdentity.canonicity_at_count).run env).run {}
  unless canonical.visited.contains ``P01AC.ExtensionalRepair.Structural.closed_church_weaken do
    throwError "Canonicity omitted actual source weakening"
  let (_, negative) := ((Lean.CollectAxioms.collect ``ClosedChurchIdentity.identity_implies_count_eq).run env).run {}
  for needed in [``P01AC.ExtensionalRepair.unary_fundamental, ``P01AC.IdentityComplexity.related_same_index] do
    unless negative.visited.contains needed do throwError "Negative direction omitted {needed}"
  for forbidden in [``ClosedChurchIdentity.identity_of_observation,
      ``P01AC.ExtensionalRepair.Structural.has_closed, ``OpenDevelopments.extractIteration] do
    if negative.visited.contains forbidden then throwError "Negative direction unexpectedly relies on {forbidden}"
  for target in [``EffectiveChurchIdentity.decideTypedIdentity, ``EffectiveChurchIdentity.decideTypedIdentityExists] do
    let (_, decision) := ((Lean.CollectAxioms.collect target).run env).run {}
    for needed in [``OpenDevelopments.extractIteration, ``Nat.find, ``OpenDevelopments.readIteration] do
      unless decision.visited.contains needed do throwError "Decision omitted executable dependency {needed}"
  let some (.thmInfo transported) := env.find? ``ClosedChurchReview.transported_has
    | throwError "J-built input is not a theorem"
  unless countConstant ``P01AC.ExtensionalRepair.HasE.j transported.value == 1 do
    throwError "Expected actual J constructor in transported input"
  let (_, transportedDeps) := ((Lean.CollectAxioms.collect ``ClosedChurchReview.transported_has).run env).run {}
  for needed in [``ClosedChurchIdentity.identity_of_observation,
      ``P01AC.ExtensionalRepair.HasE.piExt, ``P01AC.ExtensionalRepair.HasE.allExt] do
    unless transportedDeps.visited.contains needed do throwError "J input omitted actual extensional proof {needed}"
  logInfo "PASS: exact mutual grammar, source-only actual weakening, two piExt/one allExt, negative semantic separation, executable extraction dependencies."
