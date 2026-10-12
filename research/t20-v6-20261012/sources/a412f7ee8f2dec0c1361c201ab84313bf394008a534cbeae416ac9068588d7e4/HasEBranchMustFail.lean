import Constructive
open P01AC P01D P01AC.ExtensionalRepair SigmaCompletion
-- The theorem must not silently claim substitution for arbitrary HasE branches.
example {Γ A B P d z e} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) (hP : Form (.sigma A B :: Γ) P)
    (hd : HasE (B :: A :: Γ) d (branchType P)) (hz : Has Γ z (.sigma A B))
    (he : HasE Γ e (.identity (.sigma A B) z (reconstruct z))) :
    HasE Γ (elim d z e) (inst P z) :=
  elim_of_eta hc hA hB hP hd hz he
