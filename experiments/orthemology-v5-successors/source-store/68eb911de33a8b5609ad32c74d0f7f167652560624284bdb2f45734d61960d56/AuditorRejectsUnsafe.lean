/- Deliberate rejected auditor poison; never imported by mathematical modules. -/
import verification.BooleanKernelAudit
unsafe def BooleanAuditPoison.root : Nat := 0
#audit_boolean_safe_closure BooleanAuditPoison.root
