import SourceIdentity
import CompleteControl
import ProductiveCompleteness
import IntegratedContingency

namespace IndependentOrthabilityControls
open Orthemology.Tranche3
open SourceIdentity ProductiveCompleteness

set_option synthInstance.maxSize 4096

def bothComplete (_ : Bool) (_ : Unit) : Prop := True
def allModes (_ : Unit) (_ : Bool) : Prop := True
def own (s m : Bool) : Prop := s=m

theorem closure_is_indispensable :
    UnborrowedActs own own ∧ ProductiveWitness bothComplete allModes own ∧
    bothComplete false () ∧ bothComplete true () ∧
    ¬ HistoryComplete bothComplete allModes own := by
  simp only [UnborrowedActs,ProductiveWitness,HistoryComplete,bothComplete,allModes,own]
  decide

theorem unborrowed_is_indispensable :
    HistoryComplete bothComplete allModes (fun _ _ => True) ∧
    ProductiveWitness bothComplete allModes own ∧
    bothComplete false () ∧ bothComplete true () ∧
    ¬ UnborrowedActs own (fun _ _ => True) := by
  simp only [UnborrowedActs,ProductiveWitness,HistoryComplete,bothComplete,allModes,own]
  decide

theorem witness_is_indispensable :
    HistoryComplete bothComplete (fun (_ : Unit) (_ : Bool) => False) (fun _ _ => False) ∧
    UnborrowedActs (fun (_ : Bool) (_ : Bool) => False) (fun _ _ => False) ∧
    bothComplete false () ∧ bothComplete true () ∧
    ¬ ProductiveWitness bothComplete (fun (_ : Unit) (_ : Bool) => False) (fun _ _ => False) := by
  simp only [UnborrowedActs,ProductiveWitness,HistoryComplete,bothComplete]
  decide

theorem generic_reception_is_not_necessity :
    GenericReception (fun w (_ : Unit) => w=false) (fun (_ : Bool) (_ _ : Unit) => False) ∧
    Root (fun w (_ : Unit) => w=false) (fun (_ : Bool) (_ _ : Unit) => False) false () ∧
    ¬ Necessary (fun w (_ : Unit) => w=false) () := by
  simp only [GenericReception,Root,Received,Necessary]
  decide

theorem actual_root_is_indispensable :
    GenericReception (fun (_ : Bool) (_ : Unit) => True) (fun _ _ _ => True) ∧
    Necessary (fun (_ : Bool) (_ : Unit) => True) () ∧
    ¬ UniformRoot (fun (_ : Bool) (_ : Unit) => True) (fun _ _ _ => True) () := by
  simp only [GenericReception,Necessary,UniformRoot,Root,Received]
  decide

theorem uniform_roothood_is_not_uniqueness :
    GenericReception (fun (_ : Bool) (_ : Bool) => True) (fun _ _ _ => False) ∧
    UniformRoot (fun (_ : Bool) (_ : Bool) => True) (fun _ _ _ => False) false ∧
    UniformRoot (fun (_ : Bool) (_ : Bool) => True) (fun _ _ _ => False) true ∧
    (false : Bool) ≠ true := by
  simp only [GenericReception,UniformRoot,Root,Received]
  decide

theorem empty_compatibility_allows_variation :
    CompleteControl.CompatibleOutcomes (fun (_ _ : Bool) => False) id id ∧
    (id false : Bool) ≠ id true := by
  simp only [CompleteControl.CompatibleOutcomes]
  decide

theorem rectangular_nonempty_is_essential :
    (∀ a : Bool, ∀ b : Empty, id a = Empty.elim b) ∧ (id false : Bool) ≠ id true := by
  constructor
  · intro a b; exact b.elim
  · decide

theorem model_has_actual_effect : IntegratedContingency.Ex true 1 ∧
    ¬ IntegratedContingency.Ex false 1 := by
  simp only [IntegratedContingency.Ex]
  decide

theorem power_does_not_fix_will :
    (∀ w, IntegratedContingency.Power w) ∧
    ¬ (∀ w, IntegratedContingency.Will w) := by
  simp only [IntegratedContingency.Power,IntegratedContingency.Will]
  decide

end IndependentOrthabilityControls
