import LiteralShiftEndpoints
import LiteralShiftPrefix

namespace P02.LiteralShift.Controls
open P02A2.ObserverCore P02.LiteralShift

def zeroBody : Stmt := .set 2 (C 0)
def oneBody : Stmt := .set 2 (C 1)
def indexBody : Stmt := .set 2 (V 0)
def sentinelBody : Stmt := .set 2 (.div (V 1) (.pow2 (.add (V 0) (C 1))))

/-- The source keeps the stopping bit even if an early base call would differ. -/
theorem stopping_zero :
    exec (compileShift oneBody 2 1 2) (initial 0 2) 2 = 0 := by decide

theorem stopping_one :
    exec (compileShift zeroBody 2 1 2) (initial 0 3) 2 = 1 := by decide

theorem zero_endpoint_copies_first :
    exec (compileShift zeroBody 2 0 1) (initial 0 3) 2 = 1 := by decide

theorem one_endpoint_copies :
    exec (compileShift zeroBody 2 1 1) (initial 1 7) 2 = 1 := by decide

/-- The first fresh suffix bit is base stage zero. -/
theorem fresh_tail_index_zero :
    exec (compileShift indexBody 2 1 2) (initial 1 6) 2 = 0 := by
  rw [compileShift_correct]
  norm_num [specifiedValue, scanChoice, classify, prefixValue, indexBody,
    exec, evalExpr, initial, C, V]

/-- The fresh suffix contains its high sentinel even when its payload is zero. -/
theorem fresh_tail_sentinel :
    exec (compileShift sentinelBody 2 1 2) (initial 1 6) 2 = 1 := by
  rw [compileShift_correct]
  norm_num [specifiedValue, scanChoice, classify, prefixValue, sentinelBody,
    exec, evalExpr, initial, C, V]

/-- Prefix 01 straddles 1/3 and therefore cannot call a constant-zero base. -/
theorem unresolved_boundary_prefix :
    exec (compileShift zeroBody 2 1 3) (initial 1 5) 2 = 1 := by decide

end P02.LiteralShift.Controls
