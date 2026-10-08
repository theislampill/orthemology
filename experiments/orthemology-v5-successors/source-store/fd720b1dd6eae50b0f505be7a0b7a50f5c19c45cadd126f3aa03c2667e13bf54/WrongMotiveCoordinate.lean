/- Expected rejection: var 0 is the proof coordinate, not the endpoint. -/
import InhabitedEndpointControl
open OrthemologyV2 P01D P01AC
open P01AC.ExtensionalRepair.InhabitedControl
example : motiveAt (.identity Q Fp (.app H (.var 0))) q (.atom .i) =
    .identity Q Fp Fq := target_substitution
