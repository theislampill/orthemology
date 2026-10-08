import IndexedCoverage
open OrthemicCertificate.Signed
-- Deliberately invalid mutation: an empty transcript is treated as complete.
private def mutant {α : Type} (accept : α → Refutation → Bool)
    (i : Nat) (xs : List α) (rs : List (Nat × Refutation)) : Bool :=
  if rs.isEmpty then true else indexedCheck accept i xs rs
-- Must fail. The unmutated checker rejects this omission.
#guard !(mutant (fun (_ : Nat) _ => true) 0 [1,2] [])
