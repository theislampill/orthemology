/- Deliberate rejected auditor poison; never imported by mathematical modules. -/
import verification.BooleanKernelAudit
/- Audit the actual partial implementation; Lean's public opaque surrogate
   alone is not the partial compiler implementation. -/
partial def BooleanAuditPoison.root (n : Nat) : Nat := BooleanAuditPoison.root n
#audit_boolean_safe_closure BooleanAuditPoison.root._unsafe_rec
