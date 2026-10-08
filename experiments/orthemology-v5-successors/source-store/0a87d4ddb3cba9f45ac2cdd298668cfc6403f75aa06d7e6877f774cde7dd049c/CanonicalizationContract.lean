import ClosedProofCanonicalisation
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.ExtensionalRepair
example {Γ : Tel} {r : Poly} {A : Ty} (h : HasE Γ r A) : Scoped Γ.length r :=
  ClosedProofCanonicalisation.has_scope h
example {Γ : Tel} {r : Poly} {A : Ty} (h : HasE Γ r A) : FormE Γ A :=
  ClosedProofCanonicalisation.formed h
example {r : Poly} {A : Ty} {p q : Poly} (h : HasE [] r (.identity A p q)) :
    HasE [] (.atom .i) (.identity A p q) :=
  ClosedProofCanonicalisation.canonical_identity h
example {A : Ty} {p q : Poly} :
    (∃r, HasE [] r (.identity A p q)) ↔ HasE [] (.atom .i) (.identity A p q) :=
  ClosedProofCanonicalisation.closed_identity_exists_iff
