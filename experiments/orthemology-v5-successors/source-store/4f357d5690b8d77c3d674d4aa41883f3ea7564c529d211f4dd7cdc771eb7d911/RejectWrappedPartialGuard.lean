import UnaryCertificateSoundness
import RuntimeBoundaryInventory
partial def attemptedWrappedPartial (n : Nat) : Nat := attemptedWrappedPartial n
def attemptedGuardWrapper (n : Nat) : Nat := attemptedWrappedPartial n
#audit_unary_opaque_boundary attemptedGuardWrapper
