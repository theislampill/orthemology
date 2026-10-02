import NativeRepresentationEquivalence
import NativeDecoderControls
set_option pp.universes true
#check @P03Source.decodeType_sound
#print axioms P03Source.decodeType_sound
#check @P03Source.decodeTerm_sound
#print axioms P03Source.decodeTerm_sound
#check @P03Source.decodeTrace_sound
#print axioms P03Source.decodeTrace_sound
#check @P03Source.decodeProof_sound
#print axioms P03Source.decodeProof_sound
#check @P03Source.decodeNativeProof_roundtrip
#print axioms P03Source.decodeNativeProof_roundtrip
#check @P03Source.NativeProofRep.decode_complete
#print axioms P03Source.NativeProofRep.decode_complete
#check @P03Source.NativeProofRep.deterministic
#print axioms P03Source.NativeProofRep.deterministic
#check @P03Source.nativeCheck_representation_equivalence
#print P03Source.nativeCheck_representation_equivalence
#print axioms P03Source.nativeCheck_representation_equivalence
#check @P03Source.native_checker_constructor_erasure_square
#print axioms P03Source.native_checker_constructor_erasure_square
#check @P03Source.native_checker_sound
#print axioms P03Source.native_checker_sound
#check @P03Source.native_check_rejects_duplicate_fields
#print axioms P03Source.native_check_rejects_duplicate_fields
#check @P03Source.native_checker_partial_export_square
#print P03Source.native_checker_partial_export_square
#print axioms P03Source.native_checker_partial_export_square
#print P03Source.WireValue
#print P03Source.NativeProofRep
#print P03Source.decodeProof
#print P03Source.nativeCheck

example (d : Nat) (value : P03Source.WireValue) (out : OrthemologyV2.Term × OrthemologyV2.TypeCode)
    (h : P03Source.nativeCheck d value = some out) (rho : Nat → OrthemologyV2.Code) :
    (OrthemologyV2.interpret out.2 rho).accepts out.1 :=
  P03Source.native_checker_sound h rho
