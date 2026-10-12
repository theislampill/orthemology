import Constructive
open P01AC P01D P01AC.ExtensionalRepair SigmaCompletion
-- Conditional construction is not an unconditional source eliminator.
example {Γ A B P d z e} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) (hP : Form (.sigma A B :: Γ) P)
    (hd : Has (B :: A :: Γ) d (branchType P)) (hz : Has Γ z (.sigma A B)) :
    HasE Γ (elim d z e) (inst P z) :=
  elim_of_eta hc hA hB hP hd hz
