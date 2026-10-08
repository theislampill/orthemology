import LiteralScalarFusion
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.ExactScalarFusion
example (h : HasE [] c3 (W q)) : Has [] i literalB := literal_reverse h
