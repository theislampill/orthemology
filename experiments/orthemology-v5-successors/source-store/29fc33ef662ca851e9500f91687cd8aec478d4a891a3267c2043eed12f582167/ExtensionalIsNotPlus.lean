import ExtensionalRepairTheorems
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.Intensional

-- Expected type rejection only; no logical independence claim.
example : Plus.HasPlus [] separationE separationB :=
  P01AC.ExtensionalRepair.separation_has
