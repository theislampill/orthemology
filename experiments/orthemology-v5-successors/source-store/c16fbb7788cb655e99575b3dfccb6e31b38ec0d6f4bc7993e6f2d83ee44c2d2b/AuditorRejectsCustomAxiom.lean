/- Deliberate rejected auditor poison; never imported by mathematical modules. -/
import verification.ComplexityKernelAudit
axiom ComplexityAuditPoison.custom : False
theorem ComplexityAuditPoison.bridge : False := ComplexityAuditPoison.custom
theorem ComplexityAuditPoison.root : False := ComplexityAuditPoison.bridge
#audit_complexity_safe_closure ComplexityAuditPoison.root
