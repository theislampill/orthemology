import UnaryCertificateSoundness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.UnaryCertificate
example {Γ A B x y e d}
    (hA : FormC Γ A) (hB : FormC (theta Γ A x) B) (hId : FormC Γ (.identity A x y))
    (hBase : FormC Γ (motiveAt B x (.atom .i))) (hTarget : FormC Γ (motiveAt B y e))
    (hx : HasC Γ x A) (hy : HasC Γ y A) (he : HasC Γ e (.identity A x y)) :
    HasC Γ (jPoly d y e) (motiveAt B y e) := HasC.j hA hB hId hBase hTarget hx hy he
