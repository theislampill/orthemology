import ClosedScalarInstances

namespace ClosedScalarInstances.Controls
open P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N)
open P01AC.ExtensionalRepair.ExactScalarFusion (A End Leaf c3)
open P01AC.Intensional.Plus (PolyConvPlus)

/-- No inherited Has premise is present in the final theorem's interface. -/
theorem full_HasE_interface : ∀ n : Poly, HasE [] n N →
    HasE [] (.app c3 n)
      (inst (.all (.pi End (.pi A (Leaf FullPER.Application.originalQ)))) n) :=
  fun _ hn => closed_scalar_instance_exact hn

/-- Reification retains both open coordinates and packed source application. -/
theorem packing_open_control (t : OrthemologyV2.Term) (j : Nat) :
    PolyConvPlus (.app (.atom (.app .i t)) (.var j))
      (.app (.atom t) (.var j)) := by
  apply generic_conversion_reflect
  exact OpenTermStandardness.Conv.app (.i _) (.refl _)

/-- The claim includes independently derived closed numerals, without using
    numeral tests as the reason the general statement holds. -/
theorem numeral_instance (k : Nat) :
    HasE [] c2 (scalarInstance (EffectiveCompleteness.inputNumeral k)) :=
  closed_scalar_instance (has_inclusion (EffectiveCompleteness.inputNumeral_has k))

#print axioms full_HasE_interface
#print axioms packing_open_control
#print axioms numeral_instance
end ClosedScalarInstances.Controls
