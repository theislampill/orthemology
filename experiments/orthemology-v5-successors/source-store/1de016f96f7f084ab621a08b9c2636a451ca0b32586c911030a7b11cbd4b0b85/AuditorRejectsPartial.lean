/- Deliberate rejected auditor test fixture; never imported by the mathematics. -/
import verification.KernelAudit
/- Lean gives the public name a safe opaque kernel surrogate. Test the actual
   compiled partial implementation, rather than misclassifying that surrogate. -/
partial def AuditPoison.root (n : Nat) : Nat := AuditPoison.root n
#audit_safe_closure AuditPoison.root._unsafe_rec
