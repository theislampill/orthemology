import GenericIdentityCarrierProbe
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.ExtensionalRepair
namespace T20ProbeStatementContract
example : Has [N] (.atom .i)
    (.identity .raw (.app (.app (.var 0) (.atom .i)) (.atom .i)) (.atom .i)) :=
  GenericIdentityCarrierProbe.raw_unit_probe
example : Has [] (abstract (.app (.app (.var 0) (.atom .i)) (.atom .i))) (arr N .raw) :=
  GenericIdentityCarrierProbe.F_has
example : Has [] (abstract (.atom .i)) (arr N .raw) :=
  GenericIdentityCarrierProbe.G_has
example : HasE [] (.atom .i)
    (.identity (arr N .raw)
      (abstract (.app (.app (.var 0) (.atom .i)) (.atom .i)))
      (abstract (.atom .i))) :=
  GenericIdentityCarrierProbe.closed_probe_identity
example : Has [] (inputNumeral 0) N := GenericIdentityCarrierProbe.domain_inhabited
example : Has [] (abstract (.atom .i)) (arr N .raw) :=
  GenericIdentityCarrierProbe.carrier_inhabited
end T20ProbeStatementContract
