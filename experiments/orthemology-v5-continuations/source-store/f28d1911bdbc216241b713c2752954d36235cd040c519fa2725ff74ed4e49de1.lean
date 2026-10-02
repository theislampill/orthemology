import UniformStmtLayerPrimrec
import UniformExprParserPrimrec

/-! Primitive recursiveness of the unchanged statement parser on every byte
list and every fuel value, including rejection and exact unread suffixes. -/
namespace P02.Codec.UniformComputability
open P02.Codec P02A2.ObserverCore

theorem stmtLookup_primrec :
    Primrec₂ (fun p : List ℕ × List StmtResult => stmtLookup p.1 p.2) := by
  exact ((Primrec.list_getD (none : StmtResult)).comp (Primrec.snd.comp Primrec.fst)
    (Primrec.nat_sub.comp (Primrec.list_length.comp (Primrec.fst.comp Primrec.fst))
      (Primrec.list_length.comp Primrec.snd))).to₂

theorem stmtNextTable_primrec : Primrec
    (fun p : List ℕ × ℕ × List StmtResult => stmtNextTable p.1 p.2.1 p.2.2) := by
  have hr : Primrec₂ (fun p : List ℕ × ℕ × List StmtResult => stmtLookup p.1 p.2.2) :=
    (stmtLookup_primrec.comp
      (Primrec.pair (Primrec.fst.comp Primrec.fst)
        (Primrec.snd.comp (Primrec.snd.comp Primrec.fst))) Primrec.snd).to₂
  have hf : Primrec (fun p : List ℕ × ℕ × List StmtResult => p.2.1) :=
    Primrec.fst.comp Primrec.snd
  have hl := stmtLayer_primrec _ hr _ hf readExpr_primrec
  have hrange : Primrec (fun p : List ℕ × ℕ × List StmtResult => List.range (p.1.length+1)) :=
    Primrec.list_range.comp (Primrec.succ.comp (Primrec.list_length.comp Primrec.fst))
  have hdrop : Primrec (fun p : (List ℕ × ℕ × List StmtResult) × ℕ => p.1.1.drop p.2) :=
    list_drop_primrec.comp Primrec.snd (Primrec.fst.comp Primrec.fst)
  have hcell : Primrec₂ (fun (p : List ℕ × ℕ × List StmtResult) i =>
      stmtLayer p.2.1 (stmtLookup p.1 p.2.2) (p.1.drop i)) :=
    (hl.comp Primrec.fst hdrop).to₂
  exact Primrec.list_map hrange hcell

theorem stmtTable_primrec : Primrec₂ stmtTable := by
  have hi : Primrec (fun original : List ℕ => List.replicate (original.length+1) (none : StmtResult)) :=
    list_replicate_primrec.comp (Primrec.succ.comp Primrec.list_length) (Primrec.const none)
  have hs : Primrec₂ (fun original (p : ℕ × List StmtResult) => stmtNextTable original p.1 p.2) :=
    stmtNextTable_primrec
  apply (Primrec.nat_rec hi hs).of_eq
  intro original fuel
  induction fuel with
  | zero => rfl
  | succ fuel ih => simp only [Nat.rec_add_one, ih, stmtTable]

/-- Exact sealed public parser, without a generated-code or well-formedness premise. -/
theorem readStmt_primrec : Primrec₂ readStmt := by
  have ht : Primrec (fun p : ℕ × List ℕ => stmtTable p.2 p.1) :=
    stmtTable_primrec.comp Primrec.snd Primrec.fst
  apply ((Primrec.list_getD (none : StmtResult)).comp ht (Primrec.const 0)).to₂.of_eq
  intro fuel bs
  simpa only [List.drop_zero] using stmtTable_correct bs fuel 0 (Nat.zero_le _)

#print axioms readStmt_primrec

end P02.Codec.UniformComputability
