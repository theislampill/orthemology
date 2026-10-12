import LoopRenaming
import CodecStmt

/-! Literal lowering of prcodec.py lines 293-310. All variadic Python Seq
nodes use the inherited parser's sequenceList; the source's sorted compressed
register allocation is retained. No alternate selector or program is used. -/
namespace P02.LiteralShift
open P02A2.ObserverCore P02A2.LoopRenaming
open P02.Codec (sequenceList)

abbrev C := Expr.constant
abbrev V := Expr.reg

def initial (n w : ℕ) : Store := fun r => if r = 0 then n else if r = 1 then w else 0

def sourceRegisters (body : Stmt) (output : ℕ) : Finset ℕ :=
  insert 0 (insert 1 (insert output (stmtRegs body)))

def registerList (body : Stmt) (output : ℕ) : List ℕ :=
  (sourceRegisters body output).sort (· ≤ ·)

def registerMap (body : Stmt) (output r : ℕ) : ℕ :=
  12 + (registerList body output).idxOf r

def tailArgs : List (ℕ × Expr) := [(0, .sub (V 9) (C 1)), (1, V 10)]

/-- The exact variadic body emitted by Builder.inline at this call site. -/
def literalInline (body : Stmt) (output : ℕ) : Stmt :=
  let ρ := registerMap body output
  sequenceList ((registerList body output).map (fun r => .set (ρ r) (C 0)) ++
    tailArgs.map (fun a => .set (ρ a.1) a.2) ++
    [renameStmt ρ body, .set 11 (V (ρ output))])

def lengthExpr : Expr := .add (V 0) (C 1)
def depthExpr : Expr := .add (V 3) (C 1)

def scanBody (a b : ℕ) : Stmt :=
  .branch (.eq (V 4) (C 0))
    (sequenceList [
      .set 8 (.pow2 depthExpr),
      .set 7 (.mod (.div (V 1) (.pow2 (.sub lengthExpr depthExpr))) (V 8)),
      .branch (.le (.mul (C b) (.add (V 7) (C 1))) (.mul (C a) (V 8)))
        (sequenceList [.set 4 (C 1), .set 5 (C 0), .set 6 depthExpr])
        (.branch (.le (.mul (C a) (V 8)) (.mul (C b) (V 7)))
          (sequenceList [.set 4 (C 1), .set 5 (C 1), .set 6 depthExpr])
          .skip)]) .skip

def scan (a b : ℕ) : Stmt := .loop 3 lengthExpr (scanBody a b)

def initialise : Stmt := sequenceList [.set 4 (C 0), .set 5 (C 0), .set 6 (C 0)]

def replay (body : Stmt) (output : ℕ) : Stmt :=
  sequenceList [
    .set 9 (.sub lengthExpr (V 6)),
    .set 10 (.add (.pow2 (V 9)) (.mod (V 1) (.pow2 (V 9)))),
    literalInline body output,
    .set 2 (.mod (V 11) (C 2))]

def finish (body : Stmt) (output : ℕ) : Stmt :=
  sequenceList [
    .set 2 (.mod (V 1) (C 2)),
    .branch (V 4) (.branch (V 5)
      (.branch (.le (V 6) (V 0)) (replay body output) .skip) .skip) .skip]

def compileShift (body : Stmt) (output a b : ℕ) : Stmt :=
  sequenceList [
    .set 4 (C 0), .set 5 (C 0), .set 6 (C 0), scan a b,
    .set 2 (.mod (V 1) (C 2)),
    .branch (V 4) (.branch (V 5)
      (.branch (.le (V 6) (V 0)) (replay body output) .skip) .skip) .skip]

/-- Natural arithmetic cell value, before any sentinel restriction. -/
def prefixValue (n w k : ℕ) : ℕ := w / 2^(n+1-k) % 2^k

def classify (a b n w k : ℕ) : Option Bool :=
  let v := prefixValue n w k
  if b * (v+1) ≤ a * 2^k then some false
  else if a * 2^k ≤ b*v then some true else none

structure Cut where
  depth : ℕ
  above : Bool
  deriving DecidableEq, Repr

def scanChoice (a b n w : ℕ) : ℕ → Option Cut
  | 0 => none
  | k+1 => match scanChoice a b n w k with
    | some c => some c
    | none => (classify a b n w (k+1)).map (fun side => ⟨k+1,side⟩)

def foundValue : Option Cut → ℕ
  | none => 0
  | some _ => 1

def branchValue : Option Cut → ℕ
  | none => 0
  | some c => if c.above then 1 else 0

def stopValue : Option Cut → ℕ
  | none => 0
  | some c => c.depth

def ScanAgrees (σ : Store) (n w : ℕ) (choice : Option Cut) : Prop :=
  σ 0 = n ∧ σ 1 = w ∧ σ 4 = foundValue choice ∧
  σ 5 = branchValue choice ∧ σ 6 = stopValue choice

end P02.LiteralShift
