import CanonicalDecoderBridge
import ValidityControls
namespace ExactSyntaxValidity
open Encodable OrthemologyV2 P01D P01AC
#check primrec_evaluate
#check primrec_valid
#check valid_term
#check valid_typeCode
#check valid_poly
#check valid_ty
#check normalize_term
#check normalize_typeCode
#check normalize_poly
#check normalize_ty
#check primrec_term_decode₂_reencode
#check primrec_typeCode_decode₂_reencode
#check primrec_poly_decode₂_reencode
#check primrec_ty_decode₂_reencode
#print axioms primrec_evaluate
#print axioms primrec_valid
#print axioms valid_exact
#print axioms valid_term
#print axioms valid_typeCode
#print axioms valid_poly
#print axioms valid_ty
#print axioms primrec_term_decode₂_reencode
#print axioms primrec_typeCode_decode₂_reencode
#print axioms primrec_poly_decode₂_reencode
#print axioms primrec_ty_decode₂_reencode
end ExactSyntaxValidity
