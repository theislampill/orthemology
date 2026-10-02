import UniformComputabilitySyntax

/-! Explicit, surjective, effective syntax and task codings for the unchanged
statement/repeat stack machine. These codes are separate from serialized bytes. -/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

def stmtEncode : Stmt → ℕ
  | .skip => 0
  | .set r e => 4 * Nat.pair r (exprEncode e) + 1
  | .seq s t => 4 * Nat.pair (stmtEncode s) (stmtEncode t) + 2
  | .loop r e s => 4 * Nat.pair r (Nat.pair (exprEncode e) (stmtEncode s)) + 3
  | .branch e s t => 4 * Nat.pair (exprEncode e) (Nat.pair (stmtEncode s) (stmtEncode t)) + 4

def stmtOfNat (n : ℕ) : Stmt :=
  if hn : n = 0 then .skip
  else
    let p := (n-1)/4
    have hp : p < n := by omega
    have hl : p.unpair.1 < n := lt_of_le_of_lt p.unpair_left_le hp
    have hr : p.unpair.2 < n := lt_of_le_of_lt p.unpair_right_le hp
    have hrl : p.unpair.2.unpair.1 < n := lt_of_le_of_lt p.unpair.2.unpair_left_le hr
    have hrr : p.unpair.2.unpair.2 < n := lt_of_le_of_lt p.unpair.2.unpair_right_le hr
    match (n-1)%4 with
    | 0 => .set p.unpair.1 (exprOfNat p.unpair.2)
    | 1 => .seq (stmtOfNat p.unpair.1) (stmtOfNat p.unpair.2)
    | 2 => .loop p.unpair.1 (exprOfNat p.unpair.2.unpair.1)
        (stmtOfNat p.unpair.2.unpair.2)
    | _ => .branch (exprOfNat p.unpair.1) (stmtOfNat p.unpair.2.unpair.1)
        (stmtOfNat p.unpair.2.unpair.2)
termination_by n

@[simp] theorem stmtOfNat_stmtEncode (s : Stmt) : stmtOfNat (stmtEncode s) = s := by
  induction s <;> rw [stmtEncode, stmtOfNat] <;>
    simp [Nat.mul_add_div, Nat.add_mul_div_left, *]

@[simp] theorem stmtEncode_stmtOfNat (n : ℕ) : stmtEncode (stmtOfNat n) = n := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
      rw [stmtOfNat]
      split_ifs with hn
      · simp [stmtEncode, hn]
      · have hp : (n-1)/4 < n := by omega
        have hl := lt_of_le_of_lt ((n-1)/4).unpair_left_le hp
        have hr := lt_of_le_of_lt ((n-1)/4).unpair_right_le hp
        have hrl := lt_of_le_of_lt ((n-1)/4).unpair.2.unpair_left_le hr
        have hrr := lt_of_le_of_lt ((n-1)/4).unpair.2.unpair_right_le hr
        have hm : (n-1)%4 < 4 := Nat.mod_lt _ (by omega)
        dsimp only
        generalize ht : (n-1)%4 = t at *
        interval_cases t <;> simp_all [stmtEncode, Nat.pair_unpair]
        all_goals omega

instance stmtDenumerable : Denumerable Stmt :=
  Denumerable.mk' ⟨stmtEncode, stmtOfNat, stmtOfNat_stmtEncode, stmtEncode_stmtOfNat⟩

@[simp] theorem stmt_encode_eq : Encodable.encode (α := Stmt) = stmtEncode := rfl
@[simp] theorem stmt_ofNat_eq : Denumerable.ofNat Stmt = stmtOfNat := rfl

def taskEncode : Task → ℕ
  | .stmt s => 2 * stmtEncode s
  | .repeat r k n s => 2 * Nat.pair r (Nat.pair k (Nat.pair n (stmtEncode s))) + 1

def taskOfNat (n : ℕ) : Task :=
  if n%2 = 0 then .stmt (stmtOfNat (n/2))
  else
    let p := (n/2).unpair
    .repeat p.1 p.2.unpair.1 p.2.unpair.2.unpair.1 (stmtOfNat p.2.unpair.2.unpair.2)

@[simp] theorem taskOfNat_taskEncode (t : Task) : taskOfNat (taskEncode t) = t := by
  cases t <;> simp [taskEncode, taskOfNat, Nat.mul_add_div, Nat.add_mul_div_left]

@[simp] theorem taskEncode_taskOfNat (n : ℕ) : taskEncode (taskOfNat n) = n := by
  simp only [taskOfNat]
  split_ifs <;> simp only [taskEncode, stmtEncode_stmtOfNat, Nat.pair_unpair] <;> omega

instance taskDenumerable : Denumerable Task :=
  Denumerable.mk' ⟨taskEncode, taskOfNat, taskOfNat_taskEncode, taskEncode_taskOfNat⟩

@[simp] theorem task_encode_eq : Encodable.encode (α := Task) = taskEncode := rfl
@[simp] theorem task_ofNat_eq : Denumerable.ofNat Task = taskOfNat := rfl

theorem stmtOfNat_primrec : Primrec stmtOfNat := Primrec.ofNat Stmt
theorem taskOfNat_primrec : Primrec taskOfNat := Primrec.ofNat Task

theorem stmtSet_primrec : Primrec₂ Stmt.set := by
  apply Primrec.encode_iff.mp
  change Primrec (fun p : ℕ × Expr => 4 * Nat.pair p.1 (exprEncode p.2) + 1)
  exact Primrec.nat_add.comp
    (Primrec.nat_mul.comp (Primrec.const 4)
      (Primrec₂.natPair.comp Primrec.fst (Primrec.encode.comp Primrec.snd))) (Primrec.const 1)

theorem stmtSeq_primrec : Primrec₂ Stmt.seq := by
  apply Primrec.encode_iff.mp
  change Primrec (fun p : Stmt × Stmt => 4 * Nat.pair (stmtEncode p.1) (stmtEncode p.2) + 2)
  exact Primrec.nat_add.comp
    (Primrec.nat_mul.comp (Primrec.const 4)
      (Primrec₂.natPair.comp (Primrec.encode.comp Primrec.fst)
        (Primrec.encode.comp Primrec.snd))) (Primrec.const 2)

theorem stmtLoop_primrec : Primrec (fun p : ℕ × Expr × Stmt => Stmt.loop p.1 p.2.1 p.2.2) := by
  apply Primrec.encode_iff.mp
  change Primrec (fun p : ℕ × Expr × Stmt =>
    4 * Nat.pair p.1 (Nat.pair (exprEncode p.2.1) (stmtEncode p.2.2)) + 3)
  exact Primrec.nat_add.comp
    (Primrec.nat_mul.comp (Primrec.const 4)
      (Primrec₂.natPair.comp Primrec.fst
        (Primrec₂.natPair.comp (Primrec.encode.comp (Primrec.fst.comp Primrec.snd))
          (Primrec.encode.comp (Primrec.snd.comp Primrec.snd))))) (Primrec.const 3)

theorem stmtBranch_primrec :
    Primrec (fun p : Expr × Stmt × Stmt => Stmt.branch p.1 p.2.1 p.2.2) := by
  apply Primrec.encode_iff.mp
  change Primrec (fun p : Expr × Stmt × Stmt =>
    4 * Nat.pair (exprEncode p.1) (Nat.pair (stmtEncode p.2.1) (stmtEncode p.2.2)) + 4)
  exact Primrec.nat_add.comp
    (Primrec.nat_mul.comp (Primrec.const 4)
      (Primrec₂.natPair.comp (Primrec.encode.comp Primrec.fst)
        (Primrec₂.natPair.comp (Primrec.encode.comp (Primrec.fst.comp Primrec.snd))
          (Primrec.encode.comp (Primrec.snd.comp Primrec.snd))))) (Primrec.const 4)

theorem taskStmt_primrec : Primrec Task.stmt := by
  apply Primrec.encode_iff.mp
  change Primrec (fun s => 2 * stmtEncode s)
  exact Primrec.nat_mul.comp (Primrec.const 2) Primrec.encode

theorem taskRepeat_primrec :
    Primrec (fun p : ℕ × ℕ × ℕ × Stmt => Task.repeat p.1 p.2.1 p.2.2.1 p.2.2.2) := by
  apply Primrec.encode_iff.mp
  change Primrec (fun p : ℕ × ℕ × ℕ × Stmt =>
    2 * Nat.pair p.1 (Nat.pair p.2.1 (Nat.pair p.2.2.1 (stmtEncode p.2.2.2))) + 1)
  exact Primrec.nat_add.comp
    (Primrec.nat_mul.comp (Primrec.const 2)
      (Primrec₂.natPair.comp Primrec.fst
        (Primrec₂.natPair.comp (Primrec.fst.comp Primrec.snd)
          (Primrec₂.natPair.comp (Primrec.fst.comp (Primrec.snd.comp Primrec.snd))
            (Primrec.encode.comp (Primrec.snd.comp (Primrec.snd.comp Primrec.snd)))))))
      (Primrec.const 1)

end P02.Codec.UniformComputability
