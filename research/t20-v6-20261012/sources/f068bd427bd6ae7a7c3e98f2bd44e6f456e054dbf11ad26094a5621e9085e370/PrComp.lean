import StepExact
set_option maxHeartbeats 100000
namespace AuxiliaryCodeComputability
open CodedScope
#check primrec_checkStepCode
attribute [local irreducible] checkStepCode
example : Primrec (fun p : Nat × Nat × Nat => checkStepCode p.1 p.2.1 p.2.2) := primrec_checkStepCode
example : Primrec (fun p : Nat × Nat × Nat => checkStepCode p.1 p.2.1 p.2.2) := primrec_checkStepCode.comp Primrec.id
example : Primrec (fun p : Nat × Nat => (v4 p.2, (v1 p.2, v2 p.2))) :=
 ((primrec_v4.comp Primrec.snd).pair ((primrec_v1.comp Primrec.snd).pair (primrec_v2.comp Primrec.snd)))
example : Primrec (fun s : Nat × Nat => checkStepCode (v4 s.2) (v1 s.2) (v2 s.2)) := by
  have hi : Primrec (fun p : Nat × Nat => (v4 p.2, (v1 p.2, v2 p.2))) :=
    ((primrec_v4.comp Primrec.snd).pair ((primrec_v1.comp Primrec.snd).pair (primrec_v2.comp Primrec.snd)))
  have h := Primrec.comp (f := fun p : Nat × Nat × Nat => checkStepCode p.1 p.2.1 p.2.2)
    (g := fun s : Nat × Nat => (v4 s.2,(v1 s.2,v2 s.2))) primrec_checkStepCode hi
  exact h.of_eq (by intro s; dsimp only)
end AuxiliaryCodeComputability
