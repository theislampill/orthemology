import MatrixEndpointChecks

/-! Supplemental compiled execution vectors, not substitutes for kernel proofs. -/
namespace MatrixIndependentAudit
open P02.Codec P02.Codec.UniformComputability AtomicMembership

def vectorPrograms : List (String × ℕ) :=
  [("invalid",0),("echo",programIndex echoProgram),("mixed",programIndex mixedProgram)]

def vectorRationals : List (ℕ × ℕ) :=
  [(0,0),(7,0),(0,3),(1,4),(2,4),(1,2),(3,4),(1,1),(3,2),(6,8)]

def vectorRows : List String :=
  vectorPrograms.flatMap (fun p => (List.range 4).flatMap (fun N =>
    (List.range 4).flatMap (fun k => vectorRationals.map (fun q =>
      String.intercalate "," [p.1,toString N,toString k,toString q.1,toString q.2,
        toString (heavyCount p.2 k N),toString (integerMatrix (p.2,Nat.pair q.1 q.2,k,N)),
        toString (decide (membershipMatrix p.2 (Nat.pair q.1 q.2) k N))]))))

#eval vectorRows.forM IO.println
end MatrixIndependentAudit
