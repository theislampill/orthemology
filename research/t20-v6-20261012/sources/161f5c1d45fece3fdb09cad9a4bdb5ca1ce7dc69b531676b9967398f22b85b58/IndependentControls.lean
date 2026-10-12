import ClosedScalarInstances

namespace ClosedScalarReview
open OrthemologyV2 P01D P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.ExactScalarFusion (A End W Leaf c3 i)
open P01AC.EffectiveCompleteness (N inputNumeral inputNumeral_has)
open P01AC.Intensional.Plus (PolyConvPlus)
open ImportedOpenTermTransport (interp)
open ClosedScalarInstances
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

theorem generic_reflection_exact (p q : Poly) :
    PolyConvPlus p q ↔ OpenTermStandardness.Conv
      (interp p OpenTermStandardness.T.var) (interp q OpenTermStandardness.T.var) :=
  ⟨fun h => ImportedOpenTermTransport.source_plus_sound h _, generic_conversion_reflect⟩

theorem every_variable_survives (j : Nat) :
    reify (interp (.var j) OpenTermStandardness.T.var) = .var j := rfl

theorem packed_atom_control (f a : Term) :
    PolyConvPlus (.atom (.app f a)) (.app (.atom f) (.atom a)) := by
  apply generic_conversion_reflect
  exact .refl _

theorem exact_q_binding :
    FullPER.Application.originalQ =
      P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed := rfl

theorem exact_endpoint_syntax (n : Poly) :
    scalarLeft n = .app (.app n (.var 1)) (.var 0) ∧
    scalarRight n = .app (.app (.app
      P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed n) (.var 1)) (.var 0) :=
  ⟨rfl,rfl⟩

def frozenBody : Ty := match W FullPER.Application.originalQ with
  | .pi _ B => B
  | _ => .bottom

theorem exact_W_shape : W FullPER.Application.originalQ = .pi N frozenBody := rfl

theorem independently_checked_instantiation {n : Poly} (h : Scoped 0 n) :
    inst frozenBody n = scalarInstance n := by
  have hq := has_scoped P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed_has
  simp [frozenBody,W,Leaf,ExactScalarFusion.scalarL,ExactScalarFusion.scalarR,
    scalarInstance,scalarLeft,scalarRight,A,End,arr,inst,wk,subst,psub,pup,
    P01F.cons,pren,ExactScalarFusion.psub_closed h,ExactScalarFusion.psub_closed hq,
    FullPER.Application.originalQ]

theorem exact_c2_syntax : c2 = .app (.atom .k) (.app (.atom .k) (.atom .i)) := by
  simp [c2,i,abstract,freeZero,drop,pren,psub]
theorem exact_c3_syntax : c3 = .app (.atom .k) c2 := by
  simp [c3,c2,i,abstract,freeZero,drop,pren,psub]

theorem original_witness_contracts (n : Poly) : PolyConvPlus (.app c3 n) c2 := by
  rw [exact_c3_syntax]
  exact .k c2 n

/-- This test is a theorem for every actual closed HasE derivation, not a numeral list. -/
theorem all_closed_source_inputs {n : Poly} (hn : HasE [] n N) :
    HasE [] (.app c3 n) (inst frozenBody n) := closed_scalar_instance_exact hn

/-- Universal input quantification here is in Lean, and the conclusion remains
    a family of separately closed source instances. -/
theorem external_closed_family : ∀ n, HasE [] n N →
    HasE [] c2 (.all (.pi End (.pi A
      (.identity A (.app (.app n (.var 1)) (.var 0))
        (.app (.app (.app FullPER.Application.originalQ n) (.var 1)) (.var 0)))))) :=
  fun _ hn => closed_scalar_instance hn

theorem variable_is_typable_open : HasE [N] (.var 0) N := by
  apply has_inclusion
  exact .var (EffectiveCompleteness.N_form (.ext .nil (EffectiveCompleteness.N_form .nil))) .zero

theorem variable_is_not_closed (j : Nat) : ¬ HasE [] (.var j) N := by
  intro h
  exact Nat.not_lt_zero j (ClosedProofCanonicalisation.has_scope h)

def wrappedNumeral (k : Nat) : Poly := .app (.atom .i) (inputNumeral k)

theorem wrapped_numeral_has (k : Nat) : HasE [] (wrappedNumeral k) N := by
  have hn := has_inclusion (inputNumeral_has k)
  exact .conv (ClosedProofCanonicalisation.formed hn) hn
    (PolyConvPlus.i (inputNumeral k)).symm ⟨trivial,has_scoped (inputNumeral_has k)⟩

theorem nonliteral_input_control (k : Nat) :
    HasE [] (.app c3 (wrappedNumeral k)) (inst frozenBody (wrappedNumeral k)) :=
  all_closed_source_inputs (wrapped_numeral_has k)

theorem no_closed_bottom (p : Poly) : ¬ HasE [] p .bottom :=
  FullPER.Application.no_closed_bottom p

theorem original_raw_separation : ¬ PolyConvPlus
    FullPER.Application.originalP FullPER.Application.originalQ := by
  intro h
  exact FullPER.Application.original_raw_distinct OpenTermStandardness.T.var
    (ImportedOpenTermTransport.source_plus_sound h _)

#print axioms generic_reflection_exact
#print axioms packed_atom_control
#print axioms independently_checked_instantiation
#print axioms original_witness_contracts
#print axioms all_closed_source_inputs
#print axioms external_closed_family
#print axioms variable_is_typable_open
#print axioms variable_is_not_closed
#print axioms nonliteral_input_control
#print axioms no_closed_bottom
#print axioms original_raw_separation
end ClosedScalarReview
