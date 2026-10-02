import UniformExprLayerPrimrec

/-! Primitive recursiveness of the exact fuel-bounded expression parser on all
byte lists. The finite table contains every original input suffix; previous
fuel results are replayed with the proved suffix invariant. -/
namespace P02.Codec.UniformComputability
open P02.Codec P02A2.ObserverCore

theorem exprLookup_primrec :
    Primrec₂ (fun p : List ℕ × List ExprResult => exprLookup p.1 p.2) := by
  exact ((Primrec.list_getD (none : ExprResult)).comp (Primrec.snd.comp Primrec.fst)
    (Primrec.nat_sub.comp (Primrec.list_length.comp (Primrec.fst.comp Primrec.fst))
      (Primrec.list_length.comp Primrec.snd))).to₂

theorem exprNextTable_primrec : Primrec₂ exprNextTable := by
  have hrange : Primrec (fun p : List ℕ × List ExprResult => List.range (p.1.length+1)) :=
    Primrec.list_range.comp (Primrec.succ.comp (Primrec.list_length.comp Primrec.fst))
  have hdrop : Primrec (fun p : (List ℕ × List ExprResult) × ℕ => p.1.1.drop p.2) :=
    list_drop_primrec.comp Primrec.snd (Primrec.fst.comp Primrec.fst)
  have hcell : Primrec₂ (fun (p : List ℕ × List ExprResult) i =>
      exprLayer (exprLookup p.1 p.2) (p.1.drop i)) :=
    ((exprLayer_primrec _ exprLookup_primrec).comp Primrec.fst hdrop).to₂
  exact (Primrec.list_map hrange hcell).to₂

theorem exprTable_primrec : Primrec₂ exprTable := by
  have hi : Primrec (fun original : List ℕ => List.replicate (original.length+1) (none : ExprResult)) :=
    list_replicate_primrec.comp (Primrec.succ.comp Primrec.list_length) (Primrec.const none)
  have hs : Primrec₂ (fun original (p : ℕ × List ExprResult) => exprNextTable original p.2) :=
    (exprNextTable_primrec.comp Primrec.fst (Primrec.snd.comp Primrec.snd)).to₂
  apply (Primrec.nat_rec hi hs).of_eq
  intro original fuel
  induction fuel with
  | zero => rfl
  | succ fuel ih => simp only [Nat.rec_add_one, ih, exprTable]

/-- Exact public parser, with no well-formedness or generated-code assumption. -/
theorem readExpr_primrec : Primrec₂ readExpr := by
  have ht : Primrec (fun p : ℕ × List ℕ => exprTable p.2 p.1) := exprTable_primrec.comp Primrec.snd Primrec.fst
  apply ((Primrec.list_getD (none : ExprResult)).comp ht (Primrec.const 0)).to₂.of_eq
  intro fuel bs
  simpa only [List.drop_zero] using exprTable_correct bs fuel 0 (Nat.zero_le _)

end P02.Codec.UniformComputability
