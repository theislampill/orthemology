import UnaryOpaqueBoundaryAudit
partial def reviewPartialRoot (n : Nat) : Nat := reviewPartialRoot n
#audit_unary_opaque_boundary reviewPartialRoot
