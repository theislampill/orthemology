import UnaryCertificateSoundness
import RuntimeBoundaryInventory
open Lean Elab Command EffectiveKernelAudit UnaryIndependentAudit
run_cmd do
  let env ← getEnv
  let mut roots : Array Name := #[]
  let mut theorems := 0
  let mut excluded := 0
  for (n, info) in env.constants.toList do
    if `P01AC.UnaryCertificate |>.isPrefixOf n then
      if info.isTheorem then
        roots := roots.push n
        theorems := theorems + 1
      else if info.isUnsafe || info.isPartial then
        excluded := excluded + 1
      else roots := roots.push n
  unless theorems > 0 do throwError "NO_CERTIFICATE_THEOREMS"
  let (count, axes) ← auditClosure roots
  let strictCount ← auditOpaqueBoundary roots
  logInfo m!"CERTIFICATE_ALL_RULES_AUDIT_PASS roots={roots.size}; theorems={theorems}; closure={count}; strictOpaqueClosure={strictCount}; axioms={axes}; excludedNonproofRuntimeAuxiliaries={excluded}"
  inventoryRuntimeBoundary "certificate-all-safe-roots" roots #[`P01AC.UnaryCertificate]
  inventoryRuntimeBoundary "unchanged-computational-certificate-guard"
    #[`P01AC.UnaryIdentity.verifyCertificate, `P01AC.UnaryIdentity.makeCertificate,
      `P01AC.UnaryIdentity.identityCheck] #[`P01AC.UnaryIdentity, `P01AC.UnaryCertificate]

#audit_safe_closure P01AC.UnaryCertificate.has_sound
#audit_safe_closure P01AC.UnaryCertificate.form_sound
#audit_safe_closure P01AC.UnaryCertificate.fragment_witness_iff_check
#audit_safe_closure P01AC.UnaryCertificate.strict_current_extension
#audit_unary_opaque_boundary P01AC.UnaryCertificate.has_sound
#audit_unary_opaque_boundary P01AC.UnaryCertificate.fragment_witness_iff_check
