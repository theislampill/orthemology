import UniformVarintPrimrec
import UniformComputabilityExprConstructors
import UniformComputabilityParserBounds

namespace P02.Codec.UniformComputability
open P02.Codec P02A2.ObserverCore

abbrev ExprResult := Option (Expr × List ℕ)

def exprLayer (read : List ℕ → ExprResult) : List ℕ → ExprResult
  | [] => none
  | tag::bs =>
      if tag = 1 then do let (n,rest) ← uvRead bs; return (.constant n,rest)
      else if tag = 2 then do let (n,rest) ← uvRead bs; return (.reg n,rest)
      else if tag = 3 then readBinary read .add bs
      else if tag = 4 then readBinary read .sub bs
      else if tag = 5 then readBinary read .mul bs
      else if tag = 6 then readBinary read .div bs
      else if tag = 7 then readBinary read .mod bs
      else if tag = 8 then readBinary read .le bs
      else if tag = 9 then readBinary read .eq bs
      else if tag = 10 then do let (a,rest) ← read bs; return (.pow2 a,rest)
      else none

theorem readExpr_succ_layer (fuel : ℕ) (bs : List ℕ) :
    readExpr (fuel+1) bs = exprLayer (readExpr fuel) bs := by
  cases bs <;> rfl

def exprLookup (original : List ℕ) (table : List ExprResult) (rest : List ℕ) : ExprResult :=
  table.getD (original.length-rest.length) none

def exprNextTable (original : List ℕ) (table : List ExprResult) : List ExprResult :=
  (List.range (original.length+1)).map (fun i => exprLayer (exprLookup original table) (original.drop i))

def exprTable (original : List ℕ) : ℕ → List ExprResult
  | 0 => List.replicate (original.length+1) none
  | fuel+1 => exprNextTable original (exprTable original fuel)


theorem readBinary_suffix_congr (original bs : List ℕ) (fuel : ℕ)
    (read : List ℕ → ExprResult) (op : Expr → Expr → Expr)
    (hread : ∀ rest, rest <:+ original → read rest = readExpr fuel rest)
    (hbs : bs <:+ original) : readBinary read op bs = readBinary (readExpr fuel) op bs := by
  unfold readBinary
  rw [hread bs hbs]
  cases h : readExpr fuel bs with
  | none => rfl
  | some p =>
      rcases p with ⟨a,rest⟩
      have hr := hread rest ((readExpr_suffix h).trans hbs)
      simp [hr]

theorem exprLayer_suffix_congr (original bs : List ℕ) (fuel : ℕ)
    (read : List ℕ → ExprResult)
    (hread : ∀ rest, rest <:+ original → read rest = readExpr fuel rest)
    (hbs : bs <:+ original) : exprLayer read bs = exprLayer (readExpr fuel) bs := by
  cases bs with
  | nil => rfl
  | cons tag bs =>
      have ht : bs <:+ original := (show bs <:+ tag::bs from ⟨[tag],rfl⟩).trans hbs
      simp only [exprLayer]
      by_cases h1 : tag = 1
      · simp only [if_pos h1]
      simp only [if_neg h1]
      by_cases h2 : tag = 2
      · simp only [if_pos h2]
      simp only [if_neg h2]
      by_cases h3 : tag = 3
      · simp only [if_pos h3]
        exact readBinary_suffix_congr original bs fuel read .add hread ht
      simp only [if_neg h3]
      by_cases h4 : tag = 4
      · simp only [if_pos h4]
        exact readBinary_suffix_congr original bs fuel read .sub hread ht
      simp only [if_neg h4]
      by_cases h5 : tag = 5
      · simp only [if_pos h5]
        exact readBinary_suffix_congr original bs fuel read .mul hread ht
      simp only [if_neg h5]
      by_cases h6 : tag = 6
      · simp only [if_pos h6]
        exact readBinary_suffix_congr original bs fuel read .div hread ht
      simp only [if_neg h6]
      by_cases h7 : tag = 7
      · simp only [if_pos h7]
        exact readBinary_suffix_congr original bs fuel read .mod hread ht
      simp only [if_neg h7]
      by_cases h8 : tag = 8
      · simp only [if_pos h8]
        exact readBinary_suffix_congr original bs fuel read .le hread ht
      simp only [if_neg h8]
      by_cases h9 : tag = 9
      · simp only [if_pos h9]
        exact readBinary_suffix_congr original bs fuel read .eq hread ht
      simp only [if_neg h9]
      by_cases h10 : tag = 10
      · simp only [if_pos h10]
        rw [hread bs ht]
      simp only [if_neg h10]


theorem exprLookup_correct (original : List ℕ) (table : List ExprResult) (fuel : ℕ)
    (ht : ∀ i, i ≤ original.length → table.getD i none = readExpr fuel (original.drop i))
    (rest : List ℕ) (hr : rest <:+ original) : exprLookup original table rest = readExpr fuel rest := by
  rw [exprLookup, ht _ (Nat.sub_le _ _), ← (List.suffix_iff_eq_drop.mp hr)]

theorem exprTable_correct (original : List ℕ) (fuel i : ℕ) (hi : i ≤ original.length) :
    (exprTable original fuel).getD i none = readExpr fuel (original.drop i) := by
  induction fuel generalizing i with
  | zero => simp [exprTable, List.getD_replicate, show i < original.length+1 by omega, readExpr]
  | succ fuel ih =>
      simp only [exprTable, exprNextTable]
      rw [List.getD_eq_getElem _ _ (by simp; omega)]
      simp only [List.getElem_map, List.getElem_range, readExpr_succ_layer]
      apply exprLayer_suffix_congr original _ fuel _ ?_ (List.drop_suffix _ _)
      intro rest hr
      apply exprLookup_correct original _ fuel ?_ rest hr
      intro j hj
      exact ih j hj

end P02.Codec.UniformComputability
