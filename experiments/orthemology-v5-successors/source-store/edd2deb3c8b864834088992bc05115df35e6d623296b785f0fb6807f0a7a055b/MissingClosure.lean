import IntensionalIdentityTheorems
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.Intensional

-- This must fail: the final theorem still requires both endpoint closure proofs.
example {C : Ty} {p q : Poly}
    (hC : Plus.FormPlus [] C)
    (hp : Plus.HasPlus [] p C) (hq : Plus.HasPlus [] q C) :
    (∃ r, Plus.HasPlus [] r (.identity C p q)) ↔
      Conv (eval p zeroEnv) (eval q zeroEnv) :=
  closed_typed_identity_iff hC hp hq
