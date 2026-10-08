import ExtensionalRepairTheorems
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.Intensional

-- Expected type rejection only; no logical independence claim.
open P01AC.ExtensionalRepair
example {Γ : Tel} {B : Ty} {p q h : Poly}
    (b : FormE (twkTel Γ) B) (a : FormE Γ (.all B))
    (hp : HasE Γ p (.all B)) (hq : HasE Γ q (.all B))
    (f : FormE (twkTel Γ) (.identity B p q))
    (hh : HasE (twkTel Γ) h (.identity B p q))
    (t : FormE Γ (.identity (.all B) p q)) :
    HasE Γ (.atom .i) (.identity (.all B) p q) :=
  HasE.allExt b a hp hq f hh t
