/- Deliberate rejected auditor poison; never imported by mathematical modules. -/
import verification.BooleanKernelAudit
theorem BooleanAuditPoison.root : False := by sorry
#audit_boolean_safe_closure BooleanAuditPoison.root
