import FinitePolySubstitution
namespace CodedPolyTransformations
open P01D Encodable SourceFamilyComputability

example : abstractCode (encode (Poly.var 0)) = encode (Poly.atom .i) := by
  rw [abstractCode_exact]; simp [abstract,freeZero]
example : abstractCode (encode (Poly.var 1)) = encode (Poly.app (.atom .k) (.var 0)) := by
  rw [abstractCode_exact]; simp [abstract,freeZero,drop,pren,psub]
example : abstractCode (encode (Poly.app (.var 0) (.var 1))) =
    encode (Poly.app (.app (.atom .s) (.atom .i)) (.app (.atom .k) (.var 0))) := by
  rw [abstractCode_exact]; simp [abstract,freeZero,drop,pren,psub]
/-- Constant application uses the literal K branch of the actual compiler. -/
example : abstractCode (encode (Poly.app (.atom .i) (.atom .k))) =
    encode (Poly.app (.atom .k) (.app (.atom .i) (.atom .k))) := by
  rw [abstractCode_exact]; simp [abstract,freeZero,drop,pren,psub]

example : shiftCode 1 (encode (Poly.app (.var 0) (.var 2))) =
    encode (Poly.app (.var 1) (.var 3)) := by rw [shiftCode_one_exact]; rfl
example : dropCode (encode (Poly.app (.var 0) (.var 2))) =
    encode (Poly.app (.var 0) (.var 1)) := by rw [dropCode_exact]; rfl
example : instPolyCode (encode (Poly.atom .i)) (encode (Poly.app (.var 0) (.var 1))) =
    encode (Poly.app (.atom .i) (.var 0)) := by rw [instPolyCode_exact]; rfl

/-- Entering a binder preserves its variable zero and shifts the old image. -/
example : substituteCode (liftEnvCode ([encode (Poly.var 4)],0))
    (encode (Poly.app (.var 0) (.var 1))) = encode (Poly.app (.var 0) (.var 5)) := by
  change substituteCode (liftEnvCode (([Poly.var 4].map encode),0)) _ = _
  rw [lifted_substituteCode_exact]
  rfl

/-- The shifted variable tail also changes under a binder. -/
example : substituteCode (liftEnvCode ([encode (Poly.var 4)],2))
    (encode (Poly.var 3)) = encode (Poly.var 4) := by
  change substituteCode (liftEnvCode (([Poly.var 4].map encode),2)) _ = _
  rw [lifted_substituteCode_exact]
  rfl

example : Computable abstractCode := primrec_abstractCode.to_comp
example : Computable₂ substituteCode := primrec_substituteCode.to_comp
example : Computable liftEnvCode := primrec_liftEnvCode.to_comp
end CodedPolyTransformations
