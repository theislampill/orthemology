import CodecProgram

/-! Successful parses never escape the suffixes of the supplied byte stream.
These invariants concern the exact sealed parsers, including malformed input. -/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

/-- A stream parser consumes a (possibly empty) initial segment on success. -/
def PreservesSuffix {α : Type} (p : List ℕ → Option (α × List ℕ)) : Prop :=
  ∀ bs a rest, p bs = some (a,rest) → rest <:+ bs

theorem pure_preservesSuffix {α : Type} (a : α) :
    PreservesSuffix (fun bs => some (a,bs)) := by
  intro bs x rest h
  cases h
  exact ⟨[],rfl⟩

theorem bind_preservesSuffix {α β : Type} (p : List ℕ → Option (α × List ℕ))
    (k : α → List ℕ → Option (β × List ℕ))
    (hp : PreservesSuffix p) (hk : ∀ a, PreservesSuffix (k a)) :
    PreservesSuffix (fun bs => do let (a,rest) ← p bs; k a rest) := by
  intro bs b rest h
  cases h1 : p bs with
  | none => simp [h1] at h
  | some ar =>
      rcases ar with ⟨a,mid⟩
      simp only [h1, Option.some_bind] at h
      exact (hk a mid b rest h).trans (hp bs a mid h1)

theorem map_preservesSuffix {α β : Type} (p : List ℕ → Option (α × List ℕ))
    (f : α → β) (hp : PreservesSuffix p) :
    PreservesSuffix (fun bs => do let (a,rest) ← p bs; return (f a,rest)) :=
  bind_preservesSuffix p _ hp (fun a => pure_preservesSuffix (f a))

theorem uvRead_preservesSuffix : PreservesSuffix uvRead := by
  intro bs n rest h
  exact ⟨uv n, ((uvRead_eq_some_iff bs n rest).mp h).symm⟩

theorem readBinary_preservesSuffix (read : List ℕ → Option (Expr × List ℕ))
    (op : Expr → Expr → Expr) (h : PreservesSuffix read) :
    PreservesSuffix (readBinary read op) :=
  bind_preservesSuffix read _ h (fun a => map_preservesSuffix read (op a) h)

theorem readExpr_preservesSuffix (fuel : ℕ) : PreservesSuffix (readExpr fuel) := by
  induction fuel with
  | zero => intro bs a rest h; simp [readExpr] at h
  | succ fuel ih =>
      intro bs a rest h
      cases bs with
      | nil => simp [readExpr] at h
      | cons tag bs =>
          have hs : bs <:+ tag::bs := ⟨[tag],rfl⟩
          suffices rest <:+ bs from this.trans hs
          simp only [readExpr] at h
          by_cases ht1 : tag = 1
          · rw [if_pos ht1] at h
            exact map_preservesSuffix uvRead Expr.constant uvRead_preservesSuffix bs a rest h
          rw [if_neg ht1] at h
          by_cases ht2 : tag = 2
          · rw [if_pos ht2] at h
            exact map_preservesSuffix uvRead Expr.reg uvRead_preservesSuffix bs a rest h
          rw [if_neg ht2] at h
          by_cases ht3 : tag = 3
          · rw [if_pos ht3] at h
            exact readBinary_preservesSuffix _ Expr.add ih bs a rest h
          rw [if_neg ht3] at h
          by_cases ht4 : tag = 4
          · rw [if_pos ht4] at h
            exact readBinary_preservesSuffix _ Expr.sub ih bs a rest h
          rw [if_neg ht4] at h
          by_cases ht5 : tag = 5
          · rw [if_pos ht5] at h
            exact readBinary_preservesSuffix _ Expr.mul ih bs a rest h
          rw [if_neg ht5] at h
          by_cases ht6 : tag = 6
          · rw [if_pos ht6] at h
            exact readBinary_preservesSuffix _ Expr.div ih bs a rest h
          rw [if_neg ht6] at h
          by_cases ht7 : tag = 7
          · rw [if_pos ht7] at h
            exact readBinary_preservesSuffix _ Expr.mod ih bs a rest h
          rw [if_neg ht7] at h
          by_cases ht8 : tag = 8
          · rw [if_pos ht8] at h
            exact readBinary_preservesSuffix _ Expr.le ih bs a rest h
          rw [if_neg ht8] at h
          by_cases ht9 : tag = 9
          · rw [if_pos ht9] at h
            exact readBinary_preservesSuffix _ Expr.eq ih bs a rest h
          rw [if_neg ht9] at h
          by_cases ht10 : tag = 10
          · rw [if_pos ht10] at h
            exact map_preservesSuffix _ Expr.pow2 ih bs a rest h
          rw [if_neg ht10] at h
          cases h

theorem readMany_preservesSuffix {α : Type} (read : List ℕ → Option (α × List ℕ))
    (h : PreservesSuffix read) (n : ℕ) : PreservesSuffix (readMany read n) := by
  induction n with
  | zero => exact pure_preservesSuffix []
  | succ n ih =>
      exact bind_preservesSuffix read _ h
        (fun a => map_preservesSuffix (readMany read n) (List.cons a) ih)

theorem sequenceList_preservesSuffix (read : List ℕ → Option (Stmt × List ℕ))
    (h : PreservesSuffix read) (n : ℕ) :
    PreservesSuffix (fun bs => do
      let (ss,rest) ← readMany read n bs
      return (sequenceList ss,rest)) :=
  map_preservesSuffix _ sequenceList (readMany_preservesSuffix read h n)

theorem readStmt_preservesSuffix (fuel : ℕ) : PreservesSuffix (readStmt fuel) := by
  induction fuel with
  | zero => intro bs a rest h; simp [readStmt] at h
  | succ fuel ih =>
      intro bs a rest h
      cases bs with
      | nil => simp [readStmt] at h
      | cons tag bs =>
          have hs : bs <:+ tag::bs := ⟨[tag],rfl⟩
          suffices rest <:+ bs from this.trans hs
          simp only [readStmt] at h
          split_ifs at h
          · exact bind_preservesSuffix uvRead _ uvRead_preservesSuffix
              (fun r => map_preservesSuffix (readExpr fuel) (Stmt.set r)
                (readExpr_preservesSuffix fuel)) bs a rest h
          · exact bind_preservesSuffix uvRead _ uvRead_preservesSuffix
              (fun n => sequenceList_preservesSuffix _ ih n) bs a rest h
          · exact bind_preservesSuffix uvRead _ uvRead_preservesSuffix
              (fun r => bind_preservesSuffix (readExpr fuel) _ (readExpr_preservesSuffix fuel)
                (fun e => map_preservesSuffix (readStmt fuel) (Stmt.loop r e) ih)) bs a rest h
          · exact bind_preservesSuffix (readExpr fuel) _ (readExpr_preservesSuffix fuel)
              (fun e => bind_preservesSuffix (readStmt fuel) _ ih
                (fun s => map_preservesSuffix (readStmt fuel) (Stmt.branch e s) ih)) bs a rest h

theorem readExpr_suffix {fuel : ℕ} {bs rest : List ℕ} {e : Expr}
    (h : readExpr fuel bs = some (e,rest)) : rest <:+ bs :=
  readExpr_preservesSuffix fuel bs e rest h

theorem readStmt_suffix {fuel : ℕ} {bs rest : List ℕ} {s : Stmt}
    (h : readStmt fuel bs = some (s,rest)) : rest <:+ bs :=
  readStmt_preservesSuffix fuel bs s rest h

end P02.Codec.UniformComputability

namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

theorem readExpr_rest_length_le {fuel : ℕ} {bs rest : List ℕ} {e : Expr}
    (h : readExpr fuel bs = some (e,rest)) : rest.length ≤ bs.length :=
  (readExpr_suffix h).length_le

theorem readStmt_rest_length_le {fuel : ℕ} {bs rest : List ℕ} {s : Stmt}
    (h : readStmt fuel bs = some (s,rest)) : rest.length ≤ bs.length :=
  (readStmt_suffix h).length_le

theorem readExpr_rest_mem_tails {fuel : ℕ} {bs rest : List ℕ} {e : Expr}
    (h : readExpr fuel bs = some (e,rest)) : rest ∈ bs.tails :=
  (List.mem_tails _ _).mpr (readExpr_suffix h)

theorem readStmt_rest_mem_tails {fuel : ℕ} {bs rest : List ℕ} {s : Stmt}
    (h : readStmt fuel bs = some (s,rest)) : rest ∈ bs.tails :=
  (List.mem_tails _ _).mpr (readStmt_suffix h)

/-- Successive parser calls remain in the original finite suffix domain. -/
theorem parser_rest_mem_original_tails {α : Type}
    {p : List ℕ → Option (α × List ℕ)} (hp : PreservesSuffix p)
    {original bs rest : List ℕ} {a : α} (hbs : bs ∈ original.tails)
    (h : p bs = some (a,rest)) : rest ∈ original.tails := by
  exact (List.mem_tails _ _).mpr ((hp bs a rest h).trans ((List.mem_tails _ _).mp hbs))

#print axioms readExpr_preservesSuffix
#print axioms readStmt_preservesSuffix
#print axioms parser_rest_mem_original_tails
end P02.Codec.UniformComputability
