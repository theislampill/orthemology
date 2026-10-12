import FiniteTypeCodeCompilation
namespace CodedMixedTransformations
open P01D P01AC OrthemologyV2 OrthemologyV3 Encodable CodedPolyTransformations

/-- Nested type binders preserve their parameters, while absent finite images stay Bottom. -/
example : tsubstImagesCode [encode Ty.raw]
    (encode (Ty.all (.all (.pi (.param 0) (.pi (.param 1) (.param 3)))))) =
    encode (Ty.all (.all (.pi (.param 0) (.pi (.param 1) .bottom)))) := by
  change tsubstImagesCode (([Ty.raw].map encode)) _ = _
  rw [tsubstImagesCode_exact]; rfl

/-- The same body under single instantiation has a shifted-param tail, not Bottom. -/
example : tinstCode (encode Ty.raw)
    (encode (Ty.all (.all (.pi (.param 0) (.pi (.param 1) (.param 3)))))) =
    encode (Ty.all (.all (.pi (.param 0) (.pi (.param 1) (.param 2))))) := by
  rw [tinstCode_exact]; rfl

/-- A term binder shifts both polynomial images and term variables inside type images. -/
example : mixedCode
    (encodeEnv ([Poly.var 4],0) ([Ty.identity (.param 3) (.var 0) (.var 2)],true,0))
    (encode (Ty.pi .raw (.identity (.param 0) (.var 1) (.var 0)))) =
    encode (Ty.pi .raw (.identity (.identity (.param 3) (.var 1) (.var 3)) (.var 5) (.var 0))) := by
  rw [mixedCode_exact]; rfl

/-- All lifts type parameters in stored type images and leaves term substitution unchanged. -/
example : mixedCode
    (encodeEnv ([Poly.var 4],0) ([Ty.identity (.param 3) (.var 0) (.var 2)],true,0))
    (encode (Ty.all (.identity (.param 1) (.var 0) (.var 1)))) =
    encode (Ty.all (.identity (.identity (.param 4) (.var 0) (.var 2)) (.var 4) (.var 0))) := by
  rw [mixedCode_exact]; rfl

/-- Two dependent term binders preserve bound zero/one and shift all old images twice. -/
example : mixedCode
    (encodeEnv ([Poly.var 4],0) ([Ty.identity (.param 3) (.var 0) (.var 2)],true,0))
    (encode (Ty.pi .raw (.sigma .raw (.identity (.param 0) (.var 2) (.app (.var 1) (.var 0)))))) =
    encode (Ty.pi .raw (.sigma .raw (.identity (.identity (.param 3) (.var 2) (.var 4))
      (.var 6) (.app (.var 1) (.var 0))))) := by
  rw [mixedCode_exact]; rfl

example : instantiateTypeCode (encode (TypeCode.var 4))
    (encode (TypeCode.all (.arrow (.var 0) (.arrow (.var 1) (.var 2))))) =
    encode (TypeCode.all (.arrow (.var 0) (.arrow (.var 5) (.var 1)))) := by
  rw [instantiateTypeCode_exact]; rfl

example : finSupportCode (encode (TypeCode.all (.var 0))) = 0 := by rw [finSupportCode_exact]; rfl
example : finSupportCode (encode (TypeCode.arrow (.var 1) (.all (.var 4)))) = 4 := by
  rw [finSupportCode_exact]; rfl
example : finCode (encode (TypeCode.arrow (.var 0) (.all (.var 1)))) =
    encode (Ty.pi (.param 0) (.all (.param 1))) := by rw [finCode_exact]; rfl

example : Computable₂ mixedCode := primrec_mixedCode.to_comp
example : Computable₂ instantiateTypeCode := primrec_instantiateTypeCode.to_comp
end CodedMixedTransformations
