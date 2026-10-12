import IndexedControls
namespace IndependentIndexedExecution
open Orthemology.CertifiedObserver.Indexed Orthemology.CertifiedObserver.Indexed.Fixtures
open P02.Codec

def words : Nat → List (List Bool)
  | 0 => [[]]
  | n+1 => (words n).flatMap (fun w => [w++[false],w++[true]])
def stream (w : List Bool) (n : Nat) : Bool := (w[n]?).getD false
def expected (w : List Bool) (k : Nat) : Bool := if k=0 then false else stream w 0 && stream w k
#eval (List.range 8).map (fun n => (n,(words n).length))
#eval (List.range 8).all (fun n => (words n).all (fun w => (List.range n).all (fun k =>
  tick 2 splitIndex (stream w) k == some (expected w k))))
#eval (List.range 7).all (fun n => (words n).all (fun w => (List.range n).all (fun k =>
  runtimeOutput splitIndex (stream w) k == expected w k)))
#eval uniformFuel splitIndex 6
#eval encodeBytes splitProgram
#eval splitIndex
#eval tick 0 splitIndex (fun _ => true) 0
#eval tick 1 splitIndex (fun _ => true) 0
#eval tick 2 splitIndex (fun _ => true) 0
end IndependentIndexedExecution
