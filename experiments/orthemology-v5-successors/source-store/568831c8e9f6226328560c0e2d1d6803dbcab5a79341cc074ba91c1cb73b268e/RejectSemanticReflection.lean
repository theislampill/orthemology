import ClosedProofCanonicalisation
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.ExtensionalRepair
-- Statement mismatch only: semantic endpoint validity is not the required input derivation.
example {A : Ty} {p q : Poly}
    (h : ∀ρ, F (.identity A p q) ρ zeroEnv .i .i) :
    HasE [] (.atom .i) (.identity A p q) :=
  ClosedProofCanonicalisation.canonical_identity h
