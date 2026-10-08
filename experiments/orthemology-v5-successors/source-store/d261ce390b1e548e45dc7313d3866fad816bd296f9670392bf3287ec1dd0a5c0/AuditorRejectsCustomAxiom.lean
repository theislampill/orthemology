/- Deliberate rejected auditor poison; never imported by mathematical modules. -/
import verification.BooleanKernelAudit
axiom BooleanAuditPoison.custom : False
theorem BooleanAuditPoison.bridge : False := BooleanAuditPoison.custom
theorem BooleanAuditPoison.root : False := BooleanAuditPoison.bridge
#audit_boolean_safe_closure BooleanAuditPoison.root
