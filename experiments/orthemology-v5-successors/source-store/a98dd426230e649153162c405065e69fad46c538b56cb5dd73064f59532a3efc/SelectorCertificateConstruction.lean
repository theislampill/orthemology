import FiniteSelectorSource
import Mathlib.Data.Nat.Digits
set_option autoImplicit false

namespace Orthemology.Eighth.SemanticControls
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.FiniteSelectorSource
open HiddenParity HiddenParity.Sufficiency

/-- Base expansion of a finite digit vector. The input values need not be computable. -/
def packDigits {n : ℕ} (b : ℕ) (f : Fin n → ℕ) : ℕ := Nat.ofDigits b (List.ofFn f)

theorem packDigits_exact {n : ℕ} (b : ℕ) (hb : 0 < b) (f : Fin n → ℕ)
    (hf : ∀ i, f i < b) (i : Fin n) :
    packDigits b f / b ^ i.val % b = f i := by
  unfold packDigits
  rw [Nat.ofDigits_div_pow_eq_ofDigits_drop i.val hb]
  · rw [Nat.ofDigits_mod_eq_head!]
    have he : ((List.ofFn f).drop i.val).head! = f i := by
      apply List.head!_of_head?
      simp [List.head?_drop, List.getElem?_ofFn, i.isLt]
    rw [he, Nat.mod_eq_of_lt (hf i)]
  · intro d hd
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hd
    exact hf j

def supportAt (i : Fin 4) : Finset Bool := ![∅, {false}, {true}, Finset.univ] i

theorem supportCode_lt (B : Finset Bool) : supportCode B < 4 := by
  exact (by decide : ∀ B : Finset Bool, supportCode B < 4) B

theorem supportAt_code (B : Finset Bool) :
    supportAt ⟨supportCode B, supportCode_lt B⟩ = B := by
  exact (by decide : ∀ B : Finset Bool, supportAt ⟨supportCode B, supportCode_lt B⟩ = B) B

def cellSupport (i : Fin 16) : Finset Bool := supportAt ⟨i.val / 4, by omega⟩
def cellFirst (i : Fin 16) : Bool := decide (i.val / 2 % 2 = 1)
def cellSecond (i : Fin 16) : Bool := decide (i.val % 2 = 1)
def cellIndex (B : Finset Bool) (x y : Bool) : Fin 16 :=
  ⟨4*supportCode B + 2*bitNat x + bitNat y, by
    have hb := supportCode_lt B
    cases x <;> cases y <;> simp [bitNat] <;> omega⟩

theorem cell_roundtrip (B : Finset Bool) (x y : Bool) :
    cellSupport (cellIndex B x y) = B ∧
    cellFirst (cellIndex B x y) = x ∧ cellSecond (cellIndex B x y) = y := by
  exact (by decide : ∀ B : Finset Bool, ∀ x y : Bool,
    cellSupport (cellIndex B x y) = B ∧ cellFirst (cellIndex B x y) = x ∧
      cellSecond (cellIndex B x y) = y) B x y

noncomputable def cycleValues (i : Fin 16) : ℕ :=
  bitNat (cycleAction (cellSupport i) (cellFirst i) (bitNat (cellSecond i)))
noncomputable def targetValues (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (i : Fin 16) : ℕ :=
  retainedCode (actualTarget P menu priority (cellSupport i) (cellFirst i) (cellSecond i))
noncomputable def stageValues (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (i : Fin 4) : ℕ := targetCode (stageActions P menu priority (supportAt i))

theorem bitNat_lt (b : Bool) : bitNat b < 2 := by cases b <;> decide

theorem targetCode_lt (E : Finset (Bool × Bool)) : targetCode E < 16 := by
  exact (by decide : ∀ E : Finset (Bool × Bool), targetCode E < 16) E

theorem retainedCode_lt (E : Option (Finset (Bool × Bool))) : retainedCode E < 32 := by
  cases E with
  | none => decide
  | some E => have h := targetCode_lt E; simp only [retainedCode]; omega

/-- Exact table existence for all retained choices, including off-target cells.
This is a classical existence construction, not an executable table extractor. -/
noncomputable def certifiedData (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ) : Data :=
  ⟨packDigits 2 cycleValues, packDigits 32 (targetValues P menu priority),
    packDigits 16 (stageValues P menu priority)⟩

theorem certifiedData_certificate (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ) :
    Certificate (certifiedData P menu priority) P menu priority := by
  constructor
  · intro B x y
    have hr := cell_roundtrip B x y
    have he := packDigits_exact 2 (by decide) cycleValues (fun i => bitNat_lt _) (cellIndex B x y)
    unfold cycleValues at he
    rw [hr.1, hr.2.1, hr.2.2] at he
    exact he
  · intro B x y
    have hr := cell_roundtrip B x y
    have he := packDigits_exact 32 (by decide) (targetValues P menu priority)
      (fun i => retainedCode_lt _) (cellIndex B x y)
    unfold targetValues at he
    rw [hr.1, hr.2.1, hr.2.2] at he
    have hp : 32 ^ (cellIndex B x y).val = 2 ^ (5*(cellIndex B x y).val) := by
      rw [show (32 : ℕ) = 2^5 by decide, pow_mul]
    rw [hp] at he
    exact he
  · intro B
    have he := packDigits_exact 16 (by decide) (stageValues P menu priority)
      (fun i => targetCode_lt _) ⟨supportCode B, supportCode_lt B⟩
    have hp : 16 ^ supportCode B = 2 ^ (4*supportCode B) := by
      rw [show (16 : ℕ) = 2^4 by decide, pow_mul]
    rw [hp] at he
    unfold stageValues at he
    rw [supportAt_code] at he
    exact he

end Orthemology.Eighth.SemanticControls
