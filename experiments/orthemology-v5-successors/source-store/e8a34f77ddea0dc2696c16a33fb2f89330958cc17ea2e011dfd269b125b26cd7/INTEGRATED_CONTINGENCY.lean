import SourceIdentity
import ProductiveCompleteness

/-!
A two-world non-vacuity witness for the declared source package. This shows
compatibility of the formal assumptions with a contingent effect; it does not
establish the interpretation premises in actual metaphysics.
-/

namespace Orthemology.Tranche3.IntegratedContingency
open SourceIdentity ProductiveCompleteness

set_option synthInstance.maxSize 4096

/-- 0 is the source, 1 a particular derivative bearer. -/
def Ex (w : Bool) (x : Fin 2) : Prop := x = 0 ∨ w = true

def Dep (w : Bool) (y x : Fin 2) : Prop :=
  w = true ∧ y = 0 ∧ x = 1

def Will (w : Bool) : Prop := w = true

def Power (_ : Bool) : Prop := True

/-- Both source power and the particular complete will suffice for the effect.
Power alone does not necessitate that this particular will occurs. -/
theorem source_with_contingent_effect :
    Root Ex Dep true 0 ∧
    (∀ x, Ex true x → ¬ Necessary Ex x → Received Dep true x) ∧
    GenericReception Ex Dep ∧
    UniformRoot Ex Dep 0 ∧
    Ex true 1 ∧ ¬ Ex false 1 ∧
    (∀ w, Power w) ∧
    (∀ w, Power w ∧ Will w → Ex w 1) ∧
    (¬ ∀ w, Will w) := by
  simp only [Root, Necessary, Received, GenericReception, UniformRoot, Ex, Dep,
    Power, Will]
  decide

/-- In the actual world each production mode has the single unborrowed source.
The source is not counted as a product of its own act. -/
def Complete (s : Fin 2) (_ : Unit) : Prop := s = 0

def Mode (_ _ : Unit) : Prop := True

def Proper (s : Fin 2) (_ : Unit) : Prop := s = 0

def Account (s : Fin 2) (_ : Unit) : Prop := s = 0

theorem productive_package_is_inhabited :
    Complete 0 () ∧
    HistoryComplete Complete Mode Account ∧
    UnborrowedActs Proper Account ∧
    ProductiveWitness Complete Mode Proper := by
  simp only [Complete, HistoryComplete, UnborrowedActs, ProductiveWitness,
    Mode, Account, Proper]
  decide

/-- A single named theorem supplies both positive witnesses at once; neither
part is true solely because there are no actual sources/effects. -/
theorem integrated_noncollapse_witness :
    UniformRoot Ex Dep 0 ∧ Ex true 1 ∧ ¬ Ex false 1 ∧
    Complete 0 () ∧ HistoryComplete Complete Mode Account ∧
    UnborrowedActs Proper Account ∧ ProductiveWitness Complete Mode Proper := by
  exact ⟨source_with_contingent_effect.2.2.2.1,
    source_with_contingent_effect.2.2.2.2.1,
    source_with_contingent_effect.2.2.2.2.2.1,
    productive_package_is_inhabited.1,
    productive_package_is_inhabited.2.1,
    productive_package_is_inhabited.2.2.1,
    productive_package_is_inhabited.2.2.2⟩

#print axioms source_with_contingent_effect
#print axioms productive_package_is_inhabited
#print axioms integrated_noncollapse_witness

end Orthemology.Tranche3.IntegratedContingency
