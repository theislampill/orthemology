import UnaryCertificateSoundness
import RuntimeBoundaryInventory
open Lean Elab Command EffectiveKernelAudit UnaryIndependentAudit
run_cmd do
  let env ← getEnv
  let roots : Array Name := #[`P01AC.UnaryCertificate.naturalFiniteCode,
    `P01AC.UnaryCertificate.natural_is_finite,
    `P01AC.UnaryCertificate.carrier_is_finite,
    `P01AC.UnaryCertificate.compiled_eval_constant,
    `P01AC.UnaryCertificate.certificate_all_valuations,
    `P01AC.UnaryCertificate.form_sound,
    `P01AC.UnaryCertificate.has_sound,
    `P01AC.UnaryCertificate.context_sound,
    `P01AC.UnaryCertificate.fundamental,
    `P01AC.UnaryCertificate.unary_fundamental,
    `P01AC.UnaryCertificate.strong_diagonal,
    `P01AC.UnaryCertificate.two_sided_invariance,
    `P01AC.UnaryCertificate.certified_identity,
    `P01AC.UnaryCertificate.checked_identity,
    `P01AC.UnaryCertificate.fragment_witness_iff_check,
    `P01AC.UnaryCertificate.fragment_I_iff_check,
    `P01AC.UnaryCertificate.fragment_witness_iff_F_identity,
    `P01AC.UnaryCertificate.fragment_witness_iff_G_identity,
    `P01AC.UnaryCertificate.fragment_witness_iff_denote,
    `P01AC.UnaryCertificate.fragment_rejects_unequal,
    `P01AC.UnaryCertificate.erase_checked_identity,
    `P01AC.UnaryCertificate.j_checked_identity_raw,
    `P01AC.UnaryCertificate.strict_current_extension,
    `P01AC.UnaryCertificate.CtxC,
    `P01AC.UnaryCertificate.FormC,
    `P01AC.UnaryCertificate.HasC,
    `P01AC.UnaryCertificate.has_inclusion,
    `P01AC.UnaryCertificate.form_inclusion,
    `P01AC.UnaryCertificate.ctx_inclusion]
  for n in roots do
    let some info := env.checked.get.find? n | throwError "MISSING_AUTHORED_ROOT {n}"
    if info.isAxiom || info.isUnsafe || info.isPartial then throwError "INVALID_AUTHORED_ROOT {n}"
    if isNoncomputable env n || (Compiler.getImplementedBy? env n).isSome ||
        (getExternAttrData? env n).isSome then throwError "AUTHORED_RUNTIME_OVERRIDE {n}"
  let (count,axes) ← auditClosure roots
  let checked ← auditOpaqueBoundary roots
  logInfo m!"INDEPENDENT_CERTIFICATE_AUTHORED_ROOTS_PASS roots={roots.size}; closure={count}; opaqueChecked={checked}; axioms={axes}"
  let mut excluded := 0
  for (n,info) in env.constants.toList do
    if `P01AC.UnaryCertificate |>.isPrefixOf n then
      if info.isUnsafe || info.isPartial then
        if info.isTheorem then throwError "UNSAFE_EXCLUDED_THEOREM {n}"
        excluded := excluded + 1
        logInfo m!"EXCLUDED_NONPROOF_AUXILIARY {n}; unsafe={info.isUnsafe}; partial={info.isPartial}"
  logInfo m!"INDEPENDENT_CERTIFICATE_AUXILIARIES_INVENTORIED count={excluded}"
