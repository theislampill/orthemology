import ExtensionalRepairSyntax
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.ExtensionalRepair
example {r : Poly} {A : Ty} {p q : Poly} (h : HasE [] r (.identity A p q)) :
    HasE [] (.atom .i) (.identity A p q) :=
  ClosedProofCanonicalisation.canonical_identity h
