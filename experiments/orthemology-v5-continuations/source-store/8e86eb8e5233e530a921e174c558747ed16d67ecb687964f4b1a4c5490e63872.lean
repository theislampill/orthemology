import SupportUpdateSource
import CompleteEmpiricalSource
import AcceptedFixtureController
set_option maxRecDepth 20000
namespace Orthemology.RuntimeBridge.PhaseUpdate.Fixture
open P02A2.PRProgram P02.Codec
open HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding

/-- This family has genuinely revealing zeroes in its a=false rows. -/
def revealingKernel : RationalKernel Bool (Bool × Bool) Bool where
  row σ e y := if e.2 then 1/2 else if y = σ then 1 else 0
  nonnegative := by intro σ e y; rcases e with ⟨s,a⟩; cases σ <;> cases s <;> cases a <;> cases y <;> norm_num
  normalized := by intro σ e; rcases e with ⟨s,a⟩; cases σ <;> cases s <;> cases a <;> norm_num [Fintype.sum_bool]

def rowNumerator (θ : Bool) (e : Bool × Bool) (y : Bool) : ℕ :=
  if y then (if e.2 = θ then 1 else 2) else (if e.2 = θ then 2 else 1)

theorem fixture_coefficients : ∀ θ e y,
    Controller.Fixture.kernel.row θ e y = (rowNumerator θ e y : ℚ)/3 := by
  intro θ e y
  rcases e with ⟨s,a⟩
  cases θ <;> cases s <;> cases a <;> cases y <;>
    norm_num [Controller.Fixture.kernel,rowNumerator]

def empiricalFixture (θ : Bool) : Program 13 := empiricalProgram 1 6 3 rowNumerator θ

theorem fixture_empirical_exact (θ : Bool) (k : ℕ) (h : History (Bool × Bool) Bool) :
    denote (empiricalFixture θ) (statisticInputs k h) =
      bitNat (empiricalReject Controller.Fixture.kernel (1/6) θ k h) := by
  have hh := empirical_source_real_exact Controller.Fixture.kernel 1 6 3 (by decide) (by decide)
    rowNumerator fixture_coefficients θ k h
  simpa [empiricalFixture] using hh

theorem reset_precedes_rejection (n : ℕ) :
    denote phaseProgram (args {false,true} {false} false ⟨n,none⟩ true) = 0 := by
  rw [phase_source_exact]
  have hc : ({false} : Finset Bool) ≠ {false,true} := by decide
  simp [advanceMemory,hc]

theorem empty_target_differs_from_none (n : ℕ) :
    denote phaseProgram (args {false} {false} false ⟨n,none⟩ false) = n ∧
    denote phaseProgram (args {false} {false} false ⟨n,some ∅⟩ false) = n+1 := by
  rw [phase_source_exact,phase_source_exact]
  simp [advanceMemory,usedStates]

#eval IO.println ("PHASE_BYTES=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack phaseProgram)).map toString) ++ "]")
#eval IO.println ("TARGET_BYTES=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack targetProgram)).map toString) ++ "]")
#eval IO.println ("SUPPORT_BYTES=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack (supportProgram revealingKernel))).map toString) ++ "]")
#eval IO.println ("COUNT_BYTES=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack countProgram)).map toString) ++ "]")
#eval IO.println ("SYMBOL_BYTES=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack symbolProgram)).map toString) ++ "]")
#eval IO.println ("GATE_BYTES=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack (gateProgram 1 6 1 3))).map toString) ++ "]")
#eval IO.println ("EMPIRICAL_0_BYTES=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack (empiricalFixture false))).map toString) ++ "]")
#eval IO.println ("EMPIRICAL_1_BYTES=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack (empiricalFixture true))).map toString) ++ "]")
end Orthemology.RuntimeBridge.PhaseUpdate.Fixture
