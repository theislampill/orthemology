import UnaryCertificateSoundness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.UnaryIdentity P01AC.UnaryCertificate
example {Γ} (e f : Expr) (r : Poly)
    (h : HasC Γ r (.identity (arr N N) e.closed f.closed)) : identityCheck e f = true :=
  (fragment_witness_iff_check e f).mp ⟨r,h⟩
