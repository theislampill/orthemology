/- Deliberate rejected auditor test fixture; never imported by the mathematics. -/
import verification.KernelAudit
axiom AuditPoison.custom : False
theorem AuditPoison.bridge : False := AuditPoison.custom
theorem AuditPoison.root : False := AuditPoison.bridge
#audit_safe_closure AuditPoison.root
