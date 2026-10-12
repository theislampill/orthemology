import SourceResources
import SourceControls
import SourceResourceBounds
set_option pp.universes true
#check @P03Source.sourceScoped_eq
#print axioms P03Source.sourceScoped_eq
#check @P03Source.sourceInstantiate_eq
#print axioms P03Source.sourceInstantiate_eq
#check @P03Source.sourceHeadStep_eq
#print axioms P03Source.sourceHeadStep_eq
#check @P03Source.trace_matches
#print axioms P03Source.trace_matches
#check @P03Source.source_core_export_square
#print axioms P03Source.source_core_export_square
#check @P03Source.sourceRun_refines_core
#print axioms P03Source.sourceRun_refines_core
#check @P03Source.sourceCheck_refines_core
#print axioms P03Source.sourceCheck_refines_core
#check @P03Source.source_checker_export_square
#print P03Source.source_checker_export_square
#print axioms P03Source.source_checker_export_square
#check @P03Source.source_checker_sound
#print P03Source.source_checker_sound
#print axioms P03Source.source_checker_sound
#check @P03SourceControls.erased_checker_acceptance_is_not_source_acceptance
#print axioms P03SourceControls.erased_checker_acceptance_is_not_source_acceptance
#print P03Source.SourceProof
#print P03Source.sourceCheckCore
#print P03Source.sourceRun
#print P03Source.sourceCheck
#print P03Source.encode

#check @P03Source.proofTree_shape
#print axioms P03Source.proofTree_shape
#check @P03Source.sourceCheck_input_guards
#print axioms P03Source.sourceCheck_input_guards

example (p : P03Source.SourceProof) (d : Nat) (t : OrthemologyV2.Term)
    (A : OrthemologyV2.TypeCode) (h : P03Source.sourceCheck d p = some (t,A)) :
    ∃ v, OrthemologyV3.check d (P03Source.encode p) = some v ∧ v.term = t ∧ v.ty = A :=
  P03Source.source_checker_export_square p d (t,A) h
