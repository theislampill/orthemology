import Mathlib

/-! UNEXECUTED observer/reduction primitives. The byte-code semantics and full
hierarchy/measure correspondence are ordinary proofs, not supplied here as
assumed axioms. The formal coverage file records the exact uncovered targets. -/
namespace P02A2.ObserverCore

abbrev Store := ℕ → ℕ
inductive Expr where
  | constant : ℕ → Expr
  | reg : ℕ → Expr
  | add : Expr → Expr → Expr
  | sub : Expr → Expr → Expr
  | mul : Expr → Expr → Expr
  | div : Expr → Expr → Expr
  | mod : Expr → Expr → Expr
  | le : Expr → Expr → Expr
  | eq : Expr → Expr → Expr
  | pow2 : Expr → Expr
  deriving DecidableEq, Repr

def evalExpr : Expr → Store → ℕ
  | .constant n,_ => n
  | .reg r,σ => σ r
  | .add a b,σ => evalExpr a σ+evalExpr b σ
  | .sub a b,σ => evalExpr a σ-evalExpr b σ
  | .mul a b,σ => evalExpr a σ*evalExpr b σ
  | .div a b,σ => evalExpr a σ/evalExpr b σ
  | .mod a b,σ => evalExpr a σ%evalExpr b σ
  | .le a b,σ => if evalExpr a σ≤evalExpr b σ then 1 else 0
  | .eq a b,σ => if evalExpr a σ=evalExpr b σ then 1 else 0
  | .pow2 a,σ => 2^evalExpr a σ

-- Binary sequence is the fold of the Python codec's finite sequence list.
inductive Stmt where
  | skip : Stmt
  | set : ℕ → Expr → Stmt
  | seq : Stmt → Stmt → Stmt
  | loop : ℕ → Expr → Stmt → Stmt
  | branch : Expr → Stmt → Stmt → Stmt
  deriving DecidableEq, Repr

def runLoop (body : Store → Store) (r : ℕ) : ℕ → Store → Store
  | 0,σ => σ
  | n+1,σ => body (Function.update (runLoop body r n σ) r n)

def exec : Stmt → Store → Store
  | .skip,σ => σ
  | .set r e,σ => Function.update σ r (evalExpr e σ)
  | .seq s t,σ => exec t (exec s σ)
  | .loop r e s,σ => runLoop (exec s) r (evalExpr e σ) σ
  | .branch e s t,σ => if evalExpr e σ=0 then exec t σ else exec s σ

theorem loop_zero (s : Stmt) (r : ℕ) (σ : Store) :
    runLoop (exec s) r 0 σ=σ := rfl

theorem loop_successor (s : Stmt) (r n : ℕ) (σ : Store) :
    runLoop (exec s) r (n+1) σ=exec s (Function.update (runLoop (exec s) r n σ) r n) := rfl

theorem sequence_execution (s t : Stmt) (σ : Store) :
    exec (.seq s t) σ=exec t (exec s σ) := rfl

def sentinel : List Bool → ℕ := List.foldl (fun n b => 2*n+if b then 1 else 0) 1

def output (P : ℕ → ℕ → ℕ) (x : ℕ → Bool) (n : ℕ) : Bool :=
  decide (P n (sentinel (List.ofFn (fun i : Fin (n+1) => x i.val)))%2=1)

theorem prefix_causal (P : ℕ → ℕ → ℕ) (x y : ℕ → Bool) (n : ℕ)
    (h : ∀ i≤n, x i=y i) : output P x n=output P y n := by
  have he : (fun i : Fin (n+1) => x i.val)=(fun i : Fin (n+1) => y i.val) := by
    funext i
    exact h i.val (by omega)
  unfold output
  rw [he]

def diagonal (q : ℕ → ℕ → Bool) (n : ℕ) : Bool := !(q n n)

theorem diagonal_differs (q : ℕ → ℕ → Bool) (e : ℕ) : diagonal q ≠ q e := by
  intro h
  have he := congrFun h e
  unfold diagonal at he
  cases hq : q e e <;> simp [hq] at he

theorem shift_eq_threshold (q d : ℝ) (hq : q<1) :
    q+(1-q)*d=q ↔ d=0 := by constructor <;> intro h <;> nlinarith

theorem shift_le_threshold (q d : ℝ) (hq : q<1) (hd : 0≤d) :
    q+(1-q)*d≤q ↔ d=0 := by constructor <;> intro h <;> nlinarith

theorem shift_gt_threshold (q d : ℝ) (hq : q<1) :
    q+(1-q)*d>q ↔ d>0 := by constructor <;> intro h <;> nlinarith

-- Exact index normal forms. These definitions do not assert completeness.
def Sigma2Normal (R : ℕ → ℕ → ℕ → Prop) (e : ℕ) : Prop := ∃ s,∀ t,R e s t
def Pi3Normal (R : ℕ → ℕ → ℕ → ℕ → Prop) (e : ℕ) : Prop := ∀ i,∃ s,∀ t,R e i s t
end P02A2.ObserverCore
