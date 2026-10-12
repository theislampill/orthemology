import Lean
import CrossReviewControls
open Lean Elab Command
run_cmd do
  let env ← getEnv
  for target in [``CrossTypedObserver.pair_church_has,
      ``CrossTypedObserver.pair_product_has, ``CrossTypedObserver.run_at,
      ``CrossTypedObserver.observe_via_sigma, ``CrossTypedObserver.observe_via_church,
      ``CrossTypedObserver.same_endpoint_identity,
      ``CrossTypedObserver.zero_source_identity, ``CrossTypedObserver.one_source_identity,
      ``CrossTypedObserver.no_shape_split, ``CrossTypedObserver.no_reverse_shape_split,
      ``CrossTypingReview.dependent_dual_pair, ``CrossTypingReview.dependent_dual_step,
      ``CrossTypingReview.dependent_source_identity,
      ``CrossTypingReview.bare_membership_does_not_identify,
      ``CrossTypingReview.all_positive_counts_agree] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected dependency {ax} in {target}"
    logInfo m!"PASS full dependency closure: {target}; axioms {state.axioms}"
  let some info := env.find? ``CrossTypedObserver.same_endpoint_identity
    | throwError "Missing same_endpoint_identity"
  let some body := info.value? true | throwError "Missing theorem body"
  for required in [``CrossTypedObserver.observe_via_sigma,
      ``CrossTypedObserver.observe_via_church,
      ``P01AC.ExtensionalRepair.HasE.identityIntro,
      ``P01AC.Intensional.Plus.PolyConvPlus.refl] do
    unless body.getUsedConstants.contains required do
      throwError "Missing exact identity-proof dependency {required}"
  logInfo "PASS same_endpoint_identity directly uses both endpoint derivations and actual identityIntro/reflexivity"
  let mut count := 0
  for (name, info) in env.constants.toList do
    if name.getRoot == `CrossTypedObserver then
      if let some value := info.value? true then
        for blocked in [``P01AC.Has.rawApp, ``P01AC.Has.rawAtom,
            ``P01AC.Has.proofErase, ``P01AC.ExtensionalRepair.HasE.rawApp,
            ``P01AC.ExtensionalRepair.HasE.rawAtom,
            ``P01AC.ExtensionalRepair.HasE.proofErase] do
          if value.getUsedConstants.contains blocked then
            throwError "Direct Raw escape {blocked} in {name}"
        count := count + 1
  logInfo m!"PASS {count} direct author declaration bodies; no Raw typing/erasure rules"
#check @CrossTypedObserver.pair_church_has
#check @CrossTypedObserver.same_endpoint_identity
#check @CrossTypedObserver.no_shape_split
