import TermTypeSubstitution
namespace CodedPolyTransformations
open P01D P01AC Encodable

example : instTyCode (encode (Poly.var 4))
    (encode (Ty.pi .raw (.identity .raw (.var 1) (.var 0)))) =
    encode (Ty.pi .raw (.identity .raw (.var 5) (.var 0))) := by
  rw [instTyCode_exact]; rfl
example : instTyCode (encode (Poly.var 4))
    (encode (Ty.all (.identity .raw (.var 0) (.var 1)))) =
    encode (Ty.all (.identity .raw (.var 4) (.var 0))) := by
  rw [instTyCode_exact]; rfl
example : wkTyCode (encode (Ty.pi .raw (.identity .raw (.var 0) (.var 1)))) =
    encode (Ty.pi .raw (.identity .raw (.var 0) (.var 2))) := by
  rw [wkTyCode_exact]; rfl
/-- Two term binders preserve both bound variables and shift the substituent twice. -/
example : instTyCode (encode (Poly.var 4))
    (encode (Ty.pi .raw (.sigma .raw (.identity .raw (.var 0) (.app (.var 1) (.var 2)))))) =
    encode (Ty.pi .raw (.sigma .raw (.identity .raw (.var 0) (.app (.var 1) (.var 6))))) := by
  rw [instTyCode_exact]; rfl

/-- Empty environment still has a nonzero variable-tail shift. -/
example : substituteCode ([],2) (encode (Poly.var 3)) = encode (Poly.var 5) := by
  change substituteCode (([] : List Poly).map encode,2) _ = _
  rw [substituteCode_exact]; rfl

/-- Beyond a nonempty image list, the explicit tail shift determines the image. -/
example : substituteCode ([encode (Poly.atom .i),encode (Poly.var 7)],3)
    (encode (Poly.app (.var 1) (.var 4))) = encode (Poly.app (.var 7) (.var 5)) := by
  change substituteCode (([Poly.atom .i,Poly.var 7].map encode),3) _ = _
  rw [substituteCode_exact]; rfl

example : substTyCode ([encode (Poly.atom .i),encode (Poly.var 7)],3)
    (encode (Ty.identity .raw (.var 1) (.var 4))) =
    encode (Ty.identity .raw (.var 7) (.var 5)) := by
  change substTyCode (([Poly.atom .i,Poly.var 7].map encode),3) _ = _
  rw [substTyCode_exact]; rfl

example : Computable₂ instTyCode := primrec_instTyCode.to_comp
example : Computable wkTyCode := primrec_wkTyCode.to_comp
end CodedPolyTransformations
