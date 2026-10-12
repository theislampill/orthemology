import SourceControls
import FamilyObstructions
import StructuredObserver
import IndependentControls
import Lean.Util.CollectAxioms

open Lean in
run_cmd do
  let env ← getEnv
  let declarations : Array Name := #[
    `TypeIndexedSourceControls.constantAll_form_empty,
    `TypeIndexedSourceControls.constantAll_context,
    `TypeIndexedSourceControls.constantAll_form,
    `TypeIndexedSourceControls.constantAll_direct,
    `TypeIndexedSourceControls.constantAll_at_raw,
    `TypeIndexedSourceControls.constantAll_reabstract,
    `TypeIndexedSourceControls.same_endpoint_identity,
    `TypeIndexedSourceControls.discriminator_form_empty,
    `TypeIndexedSourceControls.discriminator_context,
    `TypeIndexedSourceControls.discriminator_form,
    `TypeIndexedSourceControls.discriminator_var,
    `TypeIndexedSourceControls.discriminator_self_instance,
    `TypeIndexedSourceControls.discriminator_diagonal,
    `TypeIndexedFamilyObstructions.reabstract_coherent_iff,
    `TypeIndexedFamilyObstructions.full_constant_families_incoherent,
    `TypeIndexedFamilyObstructions.constantFamiliesEquiv,
    `TypeIndexedFamilyObstructions.constantFamilies_coherent,
    `TypeIndexedFamilyObstructions.constantFamilies_ext,
    `TypeIndexedFamilyObstructions.constantFamilies_nontrivial,
    `TypeIndexedFamilyObstructions.structured_observer_uniform,
    `TypeIndexedFamilyObstructions.diagonal_not_in_image,
    `TypeIndexedFamilyObstructions.self_projection_not_surjective,
    `TypeIndexedFamilyObstructions.fixedPointFree_of_distinct,
    `TypeIndexedFamilyObstructions.no_full_impredicative_product,
    `TypeIndexedFamilyObstructions.henkin_self_projection_proper,
    `TypeIndexedStructuredObserver.end_form,
    `TypeIndexedStructuredObserver.carrier_form,
    `TypeIndexedStructuredObserver.context,
    `TypeIndexedStructuredObserver.seed_has,
    `TypeIndexedStructuredObserver.body_has,
    `TypeIndexedStructuredObserver.step_has,
    `TypeIndexedStructuredObserver.n_instance,
    `TypeIndexedStructuredObserver.run_has,
    `TypeIndexedStructuredObserver.observe_has,
    `TypeIndexedStructuredObserver.observe_all_has,
    `TypeIndexedStructuredObserver.observe_specialized_has,
    `TypeIndexedStructuredObserver.observe_same_endpoint_identity,
    `TypeIndexedStructuredObserver.raw_zero_observation,
    `TypeIndexedStructuredObserver.raw_one_observation,
    `TypeIndexedStructuredObserver.raw_i_k_distinct,
    `TypeIndexedStructuredObserver.raw_observations_distinct]
  let allowed : Array Name := #[`propext, `Quot.sound, `Classical.choice]
  let forbidden : Array Name := #[
    `sorryAx,
    `FullPER.fundamental,
    `FullPER.Application.scalar_target_valid,
    `P01AC.ExtensionalRepair.fundamental,
    `P01AC.ExtensionalRepair.unary_fundamental,
    `P01AC.EffectiveCompleteness.semantic_church_standardness,
    `OpenTermStandardness.church_standard,
    `ClosedScalarInstances.source_uniform_iteration,
    `ClosedScalarInstances.closed_scalar_instance_exact,
    `EffectiveChurchIdentity.closed_church_identity]
  for n in declarations do
    if !(env.contains n) then throwError "Declaration is absent: {n}"
    let (_, s) := ((Lean.CollectAxioms.collect n).run env).run {}
    for ax in s.axioms do
      if !allowed.contains ax then throwError "Unexpected dependency for {n}: {ax}"
    for bad in forbidden do
      if s.visited.contains bad then throwError "Forbidden dependency of {n}: {bad}"
    logInfo m!"Checked {n}; axioms {s.axioms}"
  let routes : Array (Name × Array Name) := #[
    (`TypeIndexedSourceControls.constantAll_reabstract,
      #[`P01AC.ExtensionalRepair.HasE.var,
        `P01AC.ExtensionalRepair.HasE.allIntro,
        `P01AC.ExtensionalRepair.HasE.allElim]),
    (`TypeIndexedSourceControls.same_endpoint_identity,
      #[`P01AC.ExtensionalRepair.HasE.identityIntro]),
    (`TypeIndexedSourceControls.discriminator_diagonal,
      #[`P01AC.ExtensionalRepair.HasE.piElim,
        `P01AC.ExtensionalRepair.HasE.allElim]),
    (`TypeIndexedStructuredObserver.observe_has,
      #[`P01AC.Has.sigmaFst, `P01AC.Has.sigmaIntro, `P01AC.Has.rawApp,
        `P01AC.Has.piIntro, `P01AC.Has.piElim, `P01AC.Has.allElim,
        `P01AC.ExtensionalRepair.has_inclusion]),
    (`TypeIndexedStructuredObserver.observe_same_endpoint_identity,
      #[`P01AC.ExtensionalRepair.HasE.allIntro,
        `P01AC.ExtensionalRepair.HasE.allElim,
        `P01AC.ExtensionalRepair.HasE.identityIntro]),
    (`TypeIndexedStructuredObserver.raw_observations_distinct,
      #[`P01Source.normal_unique,
        `P01AC.EffectiveCompleteness.inputNumeral_applied,
        `P01D.abstraction_beta])]
  for (n, required) in routes do
    let (_, s) := ((Lean.CollectAxioms.collect n).run env).run {}
    for dep in required do
      if !s.visited.contains dep then throwError "Missing source dependency {dep} of {n}"
      logInfo m!"Required source dependency of {n}: {dep}"
