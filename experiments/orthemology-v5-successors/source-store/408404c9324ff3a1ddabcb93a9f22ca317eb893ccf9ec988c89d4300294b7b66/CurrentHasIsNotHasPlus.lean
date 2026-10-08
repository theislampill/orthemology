import IntensionalIdentityTheorems
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.Intensional

-- This must fail: the exact equivalence is stated for the hypothetical syntax.
example {C : Ty} {p q : Poly}
    (hC : P01AC.Form [] C)
    (hp : P01AC.Has [] p C) (hq : P01AC.Has [] q C)
    (sp : Scoped 0 p) (sq : Scoped 0 q) :
    (∃ r, P01AC.Has [] r (.identity C p q)) ↔
      Conv (eval p zeroEnv) (eval q zeroEnv) :=
  closed_typed_identity_iff hC hp hq sp sq
