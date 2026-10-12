import Lean
import RawImages

/- Executable kernel-environment inspection only; no new mathematical axiom. -/
open Lean Elab Command

/-- Deliberately follows declaration bodies, not declaration types. A theorem
whose signature mentions a mutual inductive grammar can have the entire
grammar in its type/axiom dependency closure without using every rule. -/
private def valueDependencies (env : Environment) (todo : List Name)
    (seen : NameSet) : Nat → Option NameSet
  | 0 => none
  | n + 1 => match todo with
    | [] => some seen
    | name :: rest =>
      if seen.contains name then valueDependencies env rest seen n
      else
        let more := match env.find? name with
          | some info => match info.value? true with
            | some e => e.getUsedConstants.toList
            | none => []
          | none => []
        valueDependencies env (more ++ rest) (seen.insert name) n

run_cmd do
  let env ← getEnv
  let blocked := [
    ``P01AC.Intensional.Plus.PolyConvPlus.i,
    ``P01AC.Intensional.Plus.PolyConvPlus.s,
    ``P01AC.Intensional.Plus.PolyConvPlus.bridge,
    ``P01AC.ExtensionalRepair.HasE.allIntro,
    ``P01AC.ExtensionalRepair.HasE.allElim,
    ``P01AC.ExtensionalRepair.HasE.piExt,
    ``P01AC.ExtensionalRepair.HasE.allExt,
    ``P01AC.ExtensionalRepair.HasE.j,
    ``OrthemologyV2.Step.i,
    ``OrthemologyV2.Step.s]
  for target in [
      ``FiniteRawObstruction.TotalK.finite_subsingleton,
      ``FiniteRawObstruction.Source.RawDenotation.toTotalK,
      ``FiniteRawObstruction.Source.finite_raw_subsingleton,
      ``FiniteRawObstruction.Source.finite_raw_congruence_universal] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"PASS full axiom closure: {target}; axioms {state.axioms}"

    let some deps := valueDependencies env [target] {} 100000
      | throwError "Declaration-body dependency traversal exhausted its bound"
    for name in blocked do
      if deps.contains name then
        throwError "Forbidden declaration-body dependency {name} in {target}"
    logInfo m!"PASS declaration-body graph: {target}; no I/S reduction, atom/app bridge, All, typed extensionality, or J rule use"

  let target := ``FiniteRawObstruction.Source.RawDenotation.toTotalK
  let some deps := valueDependencies env [target] {} 100000
    | throwError "Declaration-body dependency traversal exhausted its bound"
  for name in [``P01AC.ExtensionalRepair.HasE.rawAtom,
      ``P01AC.ExtensionalRepair.HasE.rawApp,
      ``P01AC.ExtensionalRepair.HasE.var,
      ``P01AC.Intensional.Plus.PolyConvPlus.k] do
    unless deps.contains name do
      throwError "Missing actual-source dependency {name} in {target}"
    logInfo m!"PASS required actual-source dependency: {name}"
