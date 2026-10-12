import MixedTypeSubstitution
namespace CodedMixedTransformations
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000

theorem finiteEnv_identity : finiteEnv [] 0 = Poly.var := by funext n; simp [finiteEnv]

theorem finiteTyEnv_typeImages (images : List Ty) :
    finiteTyEnv images false 0 = typeImages images := by
  funext n
  induction images generalizing n with
  | nil => simp [finiteTyEnv,typeImages]
  | cons a images ih => cases n <;> simp [finiteTyEnv,typeImages,P01F.cons,← ih]

theorem finiteTyEnv_single (A : Ty) : finiteTyEnv [A] true 0 = P01F.cons A Ty.param := by
  funext n
  cases n <;> simp [finiteTyEnv,P01F.cons]

def tinstCode (replacement body : Nat) : Nat := mixedCode (([],0),([replacement],true,0)) body

theorem primrec_tinstCode : Primrec₂ tinstCode :=
  primrec_mixedCode.comp ((Primrec.const ([],0)).pair
    ((Primrec.list_cons.comp Primrec.fst (.const [])).pair (.const (true,0)))) Primrec.snd

theorem tinstCode_exact (A B : Ty) : tinstCode (encode A) (encode B) = encode (tinst B A) := by
  have h := mixedCode_exact ([],0) ([A],true,0) B
  simpa only [encodeEnv,List.map_nil,List.map_cons,finiteEnv_identity,finiteTyEnv_single,tinst,tsubst,tinstCode] using h

def tsubstImagesCode (images : List Nat) (body : Nat) : Nat := mixedCode (([],0),(images,false,0)) body

theorem primrec_tsubstImagesCode : Primrec₂ tsubstImagesCode :=
  primrec_mixedCode.comp ((Primrec.const ([],0)).pair (Primrec.fst.pair (.const (false,0)))) Primrec.snd

theorem tsubstImagesCode_exact (images : List Ty) (B : Ty) :
    tsubstImagesCode (images.map encode) (encode B) = encode (tsubst (typeImages images) B) := by
  have h := mixedCode_exact ([],0) (images,false,0) B
  simpa only [encodeEnv,List.map_nil,finiteEnv_identity,finiteTyEnv_typeImages,tsubst,tsubstImagesCode] using h

def twkListCode (images : List Nat) : List Nat := images.map twkCode

theorem primrec_twkListCode : Primrec twkListCode := Primrec.list_map Primrec.id (primrec_twkCode.comp Primrec.snd).to₂

theorem twkListCode_exact (images : List Ty) :
    twkListCode (images.map encode) = (twkTel images).map encode := by
  simp [twkListCode,twkTel,List.map_map,Function.comp_def,twkCode_exact]

#print axioms tinstCode_exact
#print axioms tsubstImagesCode_exact
end CodedMixedTransformations
