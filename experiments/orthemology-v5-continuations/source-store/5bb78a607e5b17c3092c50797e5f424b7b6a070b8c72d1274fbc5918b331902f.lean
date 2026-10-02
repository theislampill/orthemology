import FullControllerRuntime
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace Orthemology.RuntimeBridge.PhaseUpdate.FullController.Fixture
open P02.Codec
/-- Literal execution fixture only. No retained-selector certificate is claimed
for these deliberately varied target choices. -/
def config : Config where
  selectors := ⟨44812,37974964734488859377664,65520⟩
  kernel := PhaseUpdate.Fixture.revealingKernel
  toleranceNumerator := 1
  toleranceDenominator := 4
  rowDenominator := 2
  rowNumerator θ e y := if e.2 then 1 else if θ=y then 2 else 0
  initialSupport := Finset.univ
  initialState := false
  fallbackModel := false
  fallbackAction := false
/-- Executable copy of the fixed rational environment row table. -/
def samplerKernel : HiddenParity.RationalKernel Bool (Bool × Bool) Bool where
  row σ e y := if y then (if e.2 = σ then 1/3 else 2/3) else (if e.2 = σ then 2/3 else 1/3)
  nonnegative := by intro σ e y; rcases e with ⟨s,a⟩; cases σ <;> cases s <;> cases a <;> cases y <;> norm_num
  normalized := by intro σ e; rcases e with ⟨s,a⟩; cases σ <;> cases s <;> cases a <;> norm_num [Fintype.sum_bool]

def samplerConfig : Config := { config with
  kernel := samplerKernel
  toleranceDenominator := 6
  rowDenominator := 3
  rowNumerator := PhaseUpdate.Fixture.rowNumerator }

#eval IO.println ("FULL_POLICY_BYTES=" ++ "[" ++ String.intercalate ","
  ((encodeBytes (pack (policyProgram config))).map toString) ++ "]")
#eval IO.println ("SAMPLER_POLICY_BYTES=" ++ "[" ++ String.intercalate ","
  ((encodeBytes (pack (policyProgram samplerConfig))).map toString) ++ "]")
#eval IO.println ("FULL_RUNTIME_0_BYTES=" ++ "[" ++ String.intercalate ","
  ((encodeBytes (Natural.compiled (HistoryRuntime.nextProgram (policyProgram samplerConfig) false)
    (HistoryRuntime.outputProgram (policyProgram samplerConfig) false) HistoryRuntime.initial)).map toString) ++ "]")
#eval IO.println ("FULL_RUNTIME_1_BYTES=" ++ "[" ++ String.intercalate ","
  ((encodeBytes (Natural.compiled (HistoryRuntime.nextProgram (policyProgram samplerConfig) true)
    (HistoryRuntime.outputProgram (policyProgram samplerConfig) true) HistoryRuntime.initial)).map toString) ++ "]")
end Orthemology.RuntimeBridge.PhaseUpdate.FullController.Fixture
