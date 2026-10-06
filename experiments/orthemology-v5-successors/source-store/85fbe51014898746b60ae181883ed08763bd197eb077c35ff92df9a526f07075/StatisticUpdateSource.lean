import PhaseAdvanceSource
import RationalEmpiricalGate

namespace Orthemology.RuntimeBridge.PhaseUpdate
open P02A2.ObserverCore P02A2.PRProgram
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Empirical

def pairCode (e : Bool × Bool) : ℕ := 2*bitNat e.1+bitNat e.2

theorem pair_code_injective : ∀ e f : Bool × Bool, pairCode e = pairCode f ↔ e = f := by decide

theorem bit_nat_injective (y z : Bool) : bitNat y = bitNat z ↔ y = z := by cases y <;> cases z <;> decide

def pairMatch : Expr := .eq (.reg 2) (.reg 4)
def symbolMatch : Expr := .mul pairMatch (.eq (.reg 3) (.reg 5))

/-- Unbounded old counts are incremented only by the actually acquired pair
and receipt. Inputs: old pair count, old symbol count, tracked pair, tracked
receipt, new pair, new receipt. Output registers 6 and 7 are separate. -/
def statisticBody : Stmt :=
  .seq (.set 6 (.add (.reg 0) pairMatch)) (.set 7 (.add (.reg 1) symbolMatch))

def countProgram : Program 6 := ⟨statisticBody,6⟩
def symbolProgram : Program 6 := ⟨statisticBody,7⟩

def statisticArgs (e : Bool × Bool) (y : Bool) (h : History (Bool × Bool) Bool) (f : Bool × Bool) (z : Bool) : Fin 6 → ℕ :=
  ![actionCount e h,RationalGate.symbolCount e y h,pairCode e,bitNat y,pairCode f,bitNat z]

/-- Exact source refinement of the retained acquired pair counter. -/
theorem count_source_exact (e : Bool × Bool) (y : Bool) (h : History (Bool × Bool) Bool) (f : Bool × Bool) (z : Bool) :
    denote countProgram (statisticArgs e y h f z) = actionCount e ((f,z)::h) := by
  by_cases he : e = f
  · subst f
    simp [denote,countProgram,statisticBody,exec,evalExpr,statisticArgs,pairMatch,
      P02A2.LoopPrimrec.extend,actionCount,List.countP_cons]
  · have hc : pairCode e ≠ pairCode f := fun hh => he ((pair_code_injective e f).mp hh)
    have hn : f ≠ e := Ne.symm he
    simp [denote,countProgram,statisticBody,exec,evalExpr,statisticArgs,pairMatch,
      P02A2.LoopPrimrec.extend,actionCount,List.countP_cons,he,hn,hc]

/-- Exact source refinement of the integer statistic underlying the accepted
real-valued empirical receipt frequency. -/
theorem symbol_source_exact (e : Bool × Bool) (y : Bool) (h : History (Bool × Bool) Bool) (f : Bool × Bool) (z : Bool) :
    denote symbolProgram (statisticArgs e y h f z) = RationalGate.symbolCount e y ((f,z)::h) := by
  have hp := pair_code_injective e f
  have hb := bit_nat_injective y z
  by_cases he : e = f <;> by_cases hy : y = z <;>
    simp [denote,symbolProgram,statisticBody,exec,evalExpr,statisticArgs,pairMatch,symbolMatch,
      P02A2.LoopPrimrec.extend,RationalGate.symbolCount,List.countP_cons,hp,hb,he,hy,eq_comm]

/-- The exact integer source output also equals the actual retained real mass. -/
theorem symbol_source_real_mass (e : Bool × Bool) (y : Bool) (h : History (Bool × Bool) Bool) (f : Bool × Bool) (z : Bool) :
    (denote symbolProgram (statisticArgs e y h f z) : ℝ) = historySymbolMass e y ((f,z)::h) := by
  rw [symbol_source_exact,RationalGate.count_eq_mass]

end Orthemology.RuntimeBridge.PhaseUpdate
