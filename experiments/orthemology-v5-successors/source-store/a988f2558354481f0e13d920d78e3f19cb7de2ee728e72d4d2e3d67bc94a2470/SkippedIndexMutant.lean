import IndexedCoverage
open OrthemicCertificate.Signed
-- Deliberately invalid mutation: replace supplied index by the expected index.
private def mutant (rs : List (Nat × Refutation)) : Bool :=
  indexedCheck (fun (_ : Nat) _ => true) 0 [1,2]
    (rs.zipIdx.map (fun (jr,i) => (i,jr.2)))
-- Must fail. The unmutated checker rejects duplicate index zero.
#guard !(mutant [(0,.leaf),(0,.leaf)])
