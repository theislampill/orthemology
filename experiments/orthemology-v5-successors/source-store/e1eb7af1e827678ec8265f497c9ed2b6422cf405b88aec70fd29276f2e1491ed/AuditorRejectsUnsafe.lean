/- Deliberate rejected auditor poison; never imported by mathematical modules. -/
import verification.ComplexityKernelAudit
unsafe def ComplexityAuditPoison.root : Nat := 0
#audit_complexity_safe_closure ComplexityAuditPoison.root
