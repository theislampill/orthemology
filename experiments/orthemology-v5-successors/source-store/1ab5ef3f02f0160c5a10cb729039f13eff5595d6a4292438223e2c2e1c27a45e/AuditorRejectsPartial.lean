/- Deliberate rejected auditor poison; never imported by mathematical modules. -/
import verification.ComplexityKernelAudit
/- Audit the actual partial implementation; Lean's public opaque surrogate
   alone is not the partial compiler implementation. -/
partial def ComplexityAuditPoison.root (n : Nat) : Nat := ComplexityAuditPoison.root n
#audit_complexity_safe_closure ComplexityAuditPoison.root._unsafe_rec
