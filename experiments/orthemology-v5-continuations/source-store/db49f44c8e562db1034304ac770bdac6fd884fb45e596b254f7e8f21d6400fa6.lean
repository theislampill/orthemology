import Mathlib

/-!
P02 separate research candidate. NOT EXECUTED at any Lean version.
Finite n=3 bridge only. The ordinary all-n proof is in analysis/Q1c_FINITE_PROBABILITY.md.
These exact rational tables are not claimed to be an already checked PMF development.
-/
namespace P02.T300
open scoped BigOperators
set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

def parity3 (x : Fin 8) : Nat := (x.val / 4 + x.val / 2 + x.val) % 2

def evenWeight (x : Fin 8) : ℚ := if parity3 x = 0 then 1/4 else 0
def oddWeight (x : Fin 8) : ℚ := if parity3 x = 1 then 1/4 else 0
def mixtureWeight (x : Fin 8) : ℚ := evenWeight x / 2 + if x.val = 0 then 1/2 else 0

def profile (w : Fin 8 → ℚ) (mask pattern : Nat) : ℚ :=
  ∑ x : Fin 8, if Nat.land x.val mask = pattern then w x else 0

def evenTarget (w : Fin 8 → ℚ) : ℚ :=
  ∑ x : Fin 8, if parity3 x = 0 then w x else 0

def flipLowBit (x : Fin 8) : Fin 8 :=
  ⟨(x.val / 2) * 2 + (1 - x.val % 2), by omega⟩

theorem normalised :
    (∑ x : Fin 8, evenWeight x) = 1 ∧
    (∑ x : Fin 8, oddWeight x) = 1 ∧
    (∑ x : Fin 8, mixtureWeight x) = 1 := by decide +kernel

theorem weights_nonnegative :
    ∀ x : Fin 8, 0 ≤ evenWeight x ∧ 0 ≤ oddWeight x ∧ 0 ≤ mixtureWeight x := by decide +kernel

theorem all_proper_marginals_equal :
    ∀ mask : Fin 7, ∀ pattern : Fin 8,
      profile evenWeight mask.val pattern.val = profile oddWeight mask.val pattern.val := by decide +kernel

theorem parity_target_changes : evenTarget oddWeight = 0 ∧ evenTarget evenWeight = 1 := by decide +kernel

theorem declared_flip :
    (∀ x : Fin 8, flipLowBit (flipLowBit x) = x) ∧
    (∀ x : Fin 8, oddWeight x = evenWeight (flipLowBit x)) := by decide +kernel

theorem mixture_target_retained : evenTarget evenWeight = 1 ∧ evenTarget mixtureWeight = 1 := by decide +kernel

theorem every_pair_profile_changes :
    ∀ mask : Fin 8, (mask.val = 3 ∨ mask.val = 5 ∨ mask.val = 6) →
      profile evenWeight mask.val 0 = 1/4 ∧ profile mixtureWeight mask.val 0 = 5/8 := by decide +kernel

end P02.T300
