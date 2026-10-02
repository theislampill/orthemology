import ObservedPhaseController
import CodecProgram

/-! Literal P02 programs for the accepted advanceMemory update, specialized to
finite Boolean model/state/action carriers but with an unbounded phase index.
These are callable arity-six source components, not binary observer indices. -/
namespace Orthemology.RuntimeBridge.PhaseUpdate
open P02A2.ObserverCore P02A2.PRProgram
open HiddenParity HiddenParity.Sufficiency
open scoped BigOperators

def bitNat (b : Bool) : ℕ := if b then 1 else 0

def supportCode (B : Finset Bool) : ℕ := ∑ b ∈ B, 2^bitNat b

def targetCode (E : Finset (Bool × Bool)) : ℕ := ∑ e ∈ E, 2^(2*bitNat e.1+bitNat e.2)

def retainedCode : Option (Finset (Bool × Bool)) → ℕ
  | none => 0
  | some E => targetCode E+1

theorem support_code_injective : ∀ B C : Finset Bool, supportCode B = supportCode C ↔ B = C := by decide

theorem target_state_bit_exact : ∀ E : Finset (Bool × Bool), ∀ y : Bool,
    targetCode E / 2^(2*bitNat y) % 4 = 0 ↔ y ∉ usedStates Prod.fst E := by decide

def incrementClear : Stmt :=
  .seq (.set 6 (.add (.reg 0) (.constant 1))) (.set 7 (.constant 0))

def resetClear : Stmt := .seq (.set 6 (.constant 0)) (.set 7 (.constant 0))

def targetRow : Expr :=
  .mod (.div (.sub (.reg 1) (.constant 1)) (.pow2 (.mul (.constant 2) (.reg 4)))) (.constant 4)

/-- Inputs: phase, optional target code, old support, new support, receipt state,
reject bit. Outputs: phase register6 and optional-target register7. -/
def body : Stmt :=
  .seq (.set 6 (.reg 0)) (.seq (.set 7 (.reg 1))
    (.branch (.eq (.reg 2) (.reg 3))
      (.branch (.reg 5) incrementClear
        (.branch (.eq (.reg 1) (.constant 0)) .skip
          (.branch (.eq targetRow (.constant 0)) incrementClear .skip)))
      resetClear))

def phaseProgram : Program 6 := ⟨body,6⟩
def targetProgram : Program 6 := ⟨body,7⟩

def args (B C : Finset Bool) (y : Bool) (m : PhaseMemory Bool Bool) (reject : Bool) : Fin 6 → ℕ :=
  ![m.index,retainedCode m.retained,supportCode B,supportCode C,bitNat y,bitNat reject]

/-- Exact local source refinement of the retained controller's actual update. -/
theorem phase_source_exact (B C : Finset Bool) (y : Bool) (m : PhaseMemory Bool Bool) (reject : Bool) :
    denote phaseProgram (args B C y m reject) = (advanceMemory B C y m reject).index := by
  have hsup := support_code_injective B C
  rcases m with ⟨n,t⟩
  by_cases hc : C = B
  · subst C
    cases reject
    · cases t with
      | none => simp [denote,phaseProgram,body,exec,evalExpr,args,P02A2.LoopPrimrec.extend,retainedCode,advanceMemory,bitNat]
      | some E =>
          have hr : (targetCode E / (if y then 4 else 1)) % 4 = 0 ↔ y ∉ usedStates Prod.fst E := by
            cases y
            · simpa [bitNat] using target_state_bit_exact E false
            · simpa [bitNat] using target_state_bit_exact E true
          by_cases hy : y ∈ usedStates Prod.fst E <;>
            simp [denote,phaseProgram,body,exec,evalExpr,args,P02A2.LoopPrimrec.extend,retainedCode,
              advanceMemory,bitNat,incrementClear,targetRow,hr,hy]
    · simp [denote,phaseProgram,body,exec,evalExpr,args,P02A2.LoopPrimrec.extend,
        advanceMemory,bitNat,incrementClear]
  · have hcode : supportCode B ≠ supportCode C := fun h => hc ((hsup.mp h).symm)
    simp [denote,phaseProgram,body,exec,evalExpr,args,P02A2.LoopPrimrec.extend,
      advanceMemory,bitNat,resetClear,hcode,hc]

theorem target_source_exact (B C : Finset Bool) (y : Bool) (m : PhaseMemory Bool Bool) (reject : Bool) :
    denote targetProgram (args B C y m reject) = retainedCode (advanceMemory B C y m reject).retained := by
  have hsup := support_code_injective B C
  rcases m with ⟨n,t⟩
  by_cases hc : C = B
  · subst C
    cases reject
    · cases t with
      | none => simp [denote,targetProgram,body,exec,evalExpr,args,P02A2.LoopPrimrec.extend,retainedCode,advanceMemory,bitNat]
      | some E =>
          have hr : (targetCode E / (if y then 4 else 1)) % 4 = 0 ↔ y ∉ usedStates Prod.fst E := by
            cases y
            · simpa [bitNat] using target_state_bit_exact E false
            · simpa [bitNat] using target_state_bit_exact E true
          by_cases hy : y ∈ usedStates Prod.fst E <;>
            simp [denote,targetProgram,body,exec,evalExpr,args,P02A2.LoopPrimrec.extend,retainedCode,
              advanceMemory,bitNat,incrementClear,targetRow,hr,hy]
    · simp [denote,targetProgram,body,exec,evalExpr,args,P02A2.LoopPrimrec.extend,
        advanceMemory,bitNat,incrementClear,retainedCode]
  · have hcode : supportCode B ≠ supportCode C := fun h => hc ((hsup.mp h).symm)
    simp [denote,targetProgram,body,exec,evalExpr,args,P02A2.LoopPrimrec.extend,
      advanceMemory,bitNat,resetClear,hcode,hc,retainedCode]

end Orthemology.RuntimeBridge.PhaseUpdate
