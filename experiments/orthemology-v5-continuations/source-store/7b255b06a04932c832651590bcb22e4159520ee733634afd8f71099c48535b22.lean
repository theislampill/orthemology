import PhaseAdvanceSource

namespace Orthemology.RuntimeBridge.PhaseUpdate
open P02A2.ObserverCore P02A2.PRProgram
open HiddenParity HiddenParity.Stochastic HiddenParity.Stage

/-- The full known family determines the receipt's surviving-model mask; the
unknown true model is never an input to this source compiler or runtime. -/
def receiptSupport (P : RationalKernel Bool (Bool × Bool) Bool) (s a y : Bool) : Finset Bool :=
  Finset.univ.filter (fun σ => 0 < P.row σ (s,a) y)

def supportLookup (P : RationalKernel Bool (Bool × Bool) Bool) : Stmt :=
  .branch (.reg 1)
    (.branch (.reg 2)
      (.branch (.reg 3) (.set 4 (.constant (supportCode (receiptSupport P true true true))))
        (.set 4 (.constant (supportCode (receiptSupport P true true false)))))
      (.branch (.reg 3) (.set 4 (.constant (supportCode (receiptSupport P true false true))))
        (.set 4 (.constant (supportCode (receiptSupport P true false false))))))
    (.branch (.reg 2)
      (.branch (.reg 3) (.set 4 (.constant (supportCode (receiptSupport P false true true))))
        (.set 4 (.constant (supportCode (receiptSupport P false true false)))))
      (.branch (.reg 3) (.set 4 (.constant (supportCode (receiptSupport P false false true))))
        (.set 4 (.constant (supportCode (receiptSupport P false false false))))))

def intersectExpr : Expr :=
  .add (.mul (.mod (.reg 0) (.constant 2)) (.mod (.reg 4) (.constant 2)))
    (.mul (.constant 2) (.mul (.mod (.div (.reg 0) (.constant 2)) (.constant 2))
      (.mod (.div (.reg 4) (.constant 2)) (.constant 2))))

def supportProgram (P : RationalKernel Bool (Bool × Bool) Bool) : Program 4 :=
  ⟨.seq (supportLookup P) (.set 5 intersectExpr),5⟩

theorem intersection_bits_exact : ∀ B C : Finset Bool,
    supportCode (B ∩ C) = supportCode B % 2 * (supportCode C % 2) +
      2 * ((supportCode B / 2 % 2) * (supportCode C / 2 % 2)) := by decide

theorem support_lookup_value (P : RationalKernel Bool (Bool × Bool) Bool) (B : ℕ) (s a y : Bool) :
    exec (supportLookup P) (P02A2.LoopPrimrec.extend ![B,bitNat s,bitNat a,bitNat y]) 4 =
      supportCode (receiptSupport P s a y) ∧
    exec (supportLookup P) (P02A2.LoopPrimrec.extend ![B,bitNat s,bitNat a,bitNat y]) 0 = B := by
  cases s <;> cases a <;> cases y <;>
    simp [supportLookup,exec,evalExpr,bitNat,P02A2.LoopPrimrec.extend]

/-- Exact actual live-support update, including zero-probability eliminations. -/
theorem support_source_exact (P : RationalKernel Bool (Bool × Bool) Bool) (B : Finset Bool) (s a y : Bool) :
    denote (supportProgram P) ![supportCode B,bitNat s,bitNat a,bitNat y] =
      supportCode (liveUpdate P B (s,a) y) := by
  have he : liveUpdate P B (s,a) y = B ∩ receiptSupport P s a y := by
    ext σ
    simp [liveUpdate,receiptSupport]
  simp only [denote,supportProgram,exec,evalExpr,intersectExpr,evalExpr,Function.update_self,
    (support_lookup_value P (supportCode B) s a y).1,
    (support_lookup_value P (supportCode B) s a y).2]
  rw [he,intersection_bits_exact]

end Orthemology.RuntimeBridge.PhaseUpdate
