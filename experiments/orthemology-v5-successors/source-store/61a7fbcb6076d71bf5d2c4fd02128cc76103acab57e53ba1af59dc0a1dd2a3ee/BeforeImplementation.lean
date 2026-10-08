import EffectiveObserver
import ExtensionalRepairSyntax
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.ExtensionalRepair
example : Has [N] (.atom .i)
    (.identity .raw (.app (.app (.var 0) (.atom .i)) (.atom .i)) (.atom .i)) :=
  GenericIdentityCarrierProbe.raw_unit_probe
