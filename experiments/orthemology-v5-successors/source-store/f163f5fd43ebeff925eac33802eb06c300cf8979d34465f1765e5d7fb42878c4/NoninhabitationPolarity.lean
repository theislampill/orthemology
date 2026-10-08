import IntensionalIdentityTheorems
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.Intensional

-- This must fail: the theorem supplies noninhabitation, not an inhabitant.
example (r : Poly) : P01AC.Has [] r separationB := separation_no_has r
