import UnaryCertificateSoundness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.UnaryIdentity P01AC.UnaryCertificate
example (p q : Poly)
    (h : ∀ R : REnv, G (.identity .raw p q) R zeroEnv zeroEnv .i .i) :
    ∃ r, HasC [] r (.identity .raw p q) :=
  (fragment_witness_iff_G_identity Expr.variable Expr.variable).mpr h
