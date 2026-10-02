import UniformStmtCodingProgram
import UniformComputabilityReadMany
import UniformParserCombinators
import UniformComputabilityParserBounds

namespace P02.Codec.UniformComputability
open P02.Codec P02A2.ObserverCore

abbrev StmtResult := Option (Stmt × List ℕ)

def stmtLayer (fuel : ℕ) (read : List ℕ → StmtResult) : List ℕ → StmtResult
  | [] => none
  | tag::bs =>
      if tag = 16 then do
        let (r,bs) ← uvRead bs
        let (e,bs) ← readExpr fuel bs
        return (.set r e,bs)
      else if tag = 17 then do
        let (n,bs) ← uvRead bs
        let (ss,bs) ← readMany read n bs
        return (sequenceList ss,bs)
      else if tag = 18 then do
        let (r,bs) ← uvRead bs
        let (e,bs) ← readExpr fuel bs
        let (s,bs) ← read bs
        return (.loop r e s,bs)
      else if tag = 19 then do
        let (e,bs) ← readExpr fuel bs
        let (s,bs) ← read bs
        let (t,bs) ← read bs
        return (.branch e s t,bs)
      else none

theorem readStmt_succ_layer (fuel : ℕ) (bs : List ℕ) :
    readStmt (fuel+1) bs = stmtLayer fuel (readStmt fuel) bs := by
  cases bs <;> rfl

def stmtLookup (original : List ℕ) (table : List StmtResult) (rest : List ℕ) : StmtResult :=
  table.getD (original.length-rest.length) none

def stmtNextTable (original : List ℕ) (fuel : ℕ) (table : List StmtResult) : List StmtResult :=
  (List.range (original.length+1)).map
    (fun i => stmtLayer fuel (stmtLookup original table) (original.drop i))

def stmtTable (original : List ℕ) : ℕ → List StmtResult
  | 0 => List.replicate (original.length+1) none
  | fuel+1 => stmtNextTable original fuel (stmtTable original fuel)

theorem readMany_stmt_suffix_congr (original bs : List ℕ) (fuel : ℕ)
    (read : List ℕ → StmtResult)
    (hread : ∀ rest, rest <:+ original → read rest = readStmt fuel rest)
    (hbs : bs <:+ original) (n : ℕ) :
    readMany read n bs = readMany (readStmt fuel) n bs := by
  induction n generalizing bs with
  | zero => rfl
  | succ n ih =>
      simp only [readMany]
      rw [hread bs hbs]
      cases h : readStmt fuel bs with
      | none => rfl
      | some p =>
          rcases p with ⟨s,rest⟩
          dsimp only [Bind.bind, Option.bind]
          rw [ih rest ((readStmt_suffix h).trans hbs)]

theorem stmtLayer_suffix_congr (original bs : List ℕ) (fuel : ℕ)
    (read : List ℕ → StmtResult)
    (hread : ∀ rest, rest <:+ original → read rest = readStmt fuel rest)
    (hbs : bs <:+ original) :
    stmtLayer fuel read bs = stmtLayer fuel (readStmt fuel) bs := by
  cases bs with
  | nil => rfl
  | cons tag bs =>
      have ht : bs <:+ original := (show bs <:+ tag::bs from ⟨[tag],rfl⟩).trans hbs
      simp only [stmtLayer]
      by_cases h16 : tag = 16
      · simp only [if_pos h16]
      simp only [if_neg h16]
      by_cases h17 : tag = 17
      · simp only [if_pos h17]
        cases h : uvRead bs with
        | none => rfl
        | some p =>
            rcases p with ⟨n,rest⟩
            dsimp only [Bind.bind, Option.bind]
            rw [readMany_stmt_suffix_congr original rest fuel read hread
              ((uvRead_preservesSuffix bs n rest h).trans ht)]
      simp only [if_neg h17]
      by_cases h18 : tag = 18
      · simp only [if_pos h18]
        cases h : uvRead bs with
        | none => rfl
        | some p =>
            rcases p with ⟨r,rest⟩
            dsimp only [Bind.bind, Option.bind]
            cases he : readExpr fuel rest with
            | none => rfl
            | some p =>
                rcases p with ⟨e,last⟩
                dsimp only [Bind.bind, Option.bind]
                rw [hread last ((readExpr_suffix he).trans
                  ((uvRead_preservesSuffix bs r rest h).trans ht))]
      simp only [if_neg h18]
      by_cases h19 : tag = 19
      · simp only [if_pos h19]
        cases he : readExpr fuel bs with
        | none => rfl
        | some p =>
            rcases p with ⟨e,rest⟩
            have hr := (readExpr_suffix he).trans ht
            dsimp only [Bind.bind, Option.bind]
            rw [hread rest hr]
            cases hs : readStmt fuel rest with
            | none => rfl
            | some p =>
                rcases p with ⟨s,last⟩
                dsimp only [Bind.bind, Option.bind]
                rw [hread last ((readStmt_suffix hs).trans hr)]
      simp only [if_neg h19]

theorem stmtLookup_correct (original : List ℕ) (table : List StmtResult) (fuel : ℕ)
    (ht : ∀ i, i ≤ original.length → table.getD i none = readStmt fuel (original.drop i))
    (rest : List ℕ) (hr : rest <:+ original) : stmtLookup original table rest = readStmt fuel rest := by
  rw [stmtLookup, ht _ (Nat.sub_le _ _), ← (List.suffix_iff_eq_drop.mp hr)]

theorem stmtTable_correct (original : List ℕ) (fuel i : ℕ) (hi : i ≤ original.length) :
    (stmtTable original fuel).getD i none = readStmt fuel (original.drop i) := by
  induction fuel generalizing i with
  | zero => simp [stmtTable, List.getD_replicate, show i < original.length+1 by omega, readStmt]
  | succ fuel ih =>
      simp only [stmtTable, stmtNextTable]
      rw [List.getD_eq_getElem _ _ (by simp; omega)]
      simp only [List.getElem_map, List.getElem_range, readStmt_succ_layer]
      apply stmtLayer_suffix_congr original _ fuel _ ?_ (List.drop_suffix _ _)
      intro rest hr
      apply stmtLookup_correct original _ fuel ?_ rest hr
      intro j hj
      exact ih j hj

end P02.Codec.UniformComputability
