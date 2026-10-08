import HistoryPolicyRuntime
import RationalEmpiricalGate
import AcceptedFixtureController

namespace Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.Tranche2.PolicyEmbedding
open P02A2.ObserverCore P02A2.PRProgram

/-- Retained newest-first history convention; no timing or rejected symbols. -/
def encodeHistory : History Bool Bool → ℕ
  | [] => 1
  | (a,y)::h => appendHistory (encodeHistory h) a y

theorem encoded_positive (h : History Bool Bool) : 0 < encodeHistory h := by
  induction h with
  | nil => decide
  | cons z h ih =>
      change 0 < 4*encodeHistory h + 2*bitNat z.1 + bitNat z.2
      omega

theorem append_tail (h : ℕ) (a y : Bool) : appendHistory h a y / 4 = h := by
  cases a <;> cases y <;> simp only [appendHistory,bitNat,Bool.false_eq_true,↓reduceIte] <;> omega

theorem append_receipt (h : ℕ) (a y : Bool) : appendHistory h a y % 2 = bitNat y := by
  cases a <;> cases y <;> simp [appendHistory,bitNat,Nat.add_mod,Nat.mul_mod]

/-- The program sees exactly the most recent receipt encoded in the history. -/
theorem observed_history_exact (h : History Bool Bool) :
    observedState (encodeHistory h) = HiddenParity.Sufficiency.observedState false h := by
  cases h with
  | nil => rfl
  | cons z h =>
      rcases z with ⟨a,y⟩
      have hp := encoded_positive h
      have hn : appendHistory (encodeHistory h) a y ≠ 1 := by unfold appendHistory; omega
      change observedState (appendHistory (encodeHistory h) a y) = y
      simp only [observedState,hn,↓reduceIte,append_receipt]
      cases y <;> rfl

/-- A concrete common policy program with the accepted singleton-menu behavior. -/
def selectorProgram : Program 1 :=
  ⟨.branch (.eq (.reg 0) (.constant 1)) (.set 1 (.constant 0))
    (.set 1 (.mod (.reg 0) (.constant 2))),1⟩

theorem selector_program_exact : PolicyImplements selectorProgram observedState := by
  intro h
  by_cases he : h = 1
  · simp [selectorProgram,denote,exec,evalExpr,P02A2.LoopPrimrec.extend,observedState,he,bitNat]
  · simp [selectorProgram,denote,exec,evalExpr,P02A2.LoopPrimrec.extend,observedState,he,bitNat_mod]

/-- Equality with the retained policy on every actual encoded observed history,
not merely on tested histories or marginal state distributions. -/
theorem selector_retained_policy (h : History Bool Bool) :
    observedState (encodeHistory h) =
      Controller.selectedPolicy id false () h := by
  rw [observed_history_exact]
  rfl

end Orthemology.RuntimeBridge.HistoryRuntime

namespace Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.Tranche2.PolicyEmbedding

/-- The policy's natural input loses no action/receipt history information. -/
theorem encode_history_injective : Function.Injective encodeHistory := by
  intro h
  induction h with
  | nil =>
      intro g he
      cases g with
      | nil => rfl
      | cons z g =>
          have hp := encoded_positive g
          change 1 = 4*encodeHistory g + 2*bitNat z.1 + bitNat z.2 at he
          omega
  | cons z h ih =>
      intro g he
      cases g with
      | nil =>
          have hp := encoded_positive h
          change 4*encodeHistory h + 2*bitNat z.1 + bitNat z.2 = 1 at he
          omega
      | cons t g =>
          have ht := congrArg (fun n : ℕ => n/4) he
          change appendHistory (encodeHistory h) z.1 z.2 / 4 =
            appendHistory (encodeHistory g) t.1 t.2 / 4 at ht
          rw [append_tail,append_tail] at ht
          have hg : h = g := ih ht
          subst g
          have hz : z = t := by
            rcases z with ⟨a,y⟩
            rcases t with ⟨c,d⟩
            cases a <;> cases y <;> cases c <;> cases d <;>
              simp [encodeHistory,appendHistory,bitNat] at he ⊢ <;> omega
          rw [hz]

theorem encoded_length_lower (h : History Bool Bool) : 4^h.length ≤ encodeHistory h := by
  induction h with
  | nil => rfl
  | cons z h ih =>
      simp only [List.length_cons,pow_succ,encodeHistory,appendHistory]
      omega

end Orthemology.RuntimeBridge.HistoryRuntime
