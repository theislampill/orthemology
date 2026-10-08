import KernelAudit
partial def renewalPartialHidden (n : Nat) : Nat := renewalPartialHidden n
def renewalSafeWrapper (n : Nat) : Nat := renewalPartialHidden n
#audit_renewal_closure renewalSafeWrapper
