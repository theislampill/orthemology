import UnaryOpaqueBoundaryAudit
partial def reviewPartialRoot (n : Nat) : Nat := reviewPartialRoot n
def reviewWrappedPartial (n : Nat) : Nat := reviewPartialRoot n
#audit_unary_opaque_boundary reviewWrappedPartial
