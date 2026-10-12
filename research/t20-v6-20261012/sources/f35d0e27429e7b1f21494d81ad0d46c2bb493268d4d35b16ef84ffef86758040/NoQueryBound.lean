import GenericAuditControls
open Orthemology.Tranche2.FiniteAlphabetQuery
example : run (fun _ => true) (fun (_ : Bool) y => y) (fun _ => false) false 1 =
    run (fun _ => true) (fun (_ : Bool) y => y) (fun _ => true) false 1 := by
  decide
