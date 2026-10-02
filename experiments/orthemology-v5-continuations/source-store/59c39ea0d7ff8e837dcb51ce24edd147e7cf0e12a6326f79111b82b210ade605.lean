import NativeDecoderSoundness
namespace P03Source
open OrthemologyV2 OrthemologyV3

/-- Declarative native grammar. Exact key multisets forbid missing, extra and
repeated fields while allowing order variation. Field membership specifies
actual values independently of the decoder's control flow. -/
inductive NativeProofRep : WireValue → SourceProof → Prop where
  | i {fields A rawA}
      (keys : (fields.map Prod.fst).Perm ["rule","A"])
      (rule : ("rule", WireValue.text "i") ∈ fields)
      (arg : ("A",rawA) ∈ fields) (type : rawA = typeTree A) :
      NativeProofRep (.object fields) (.i A)
  | k {fields A B rawA rawB}
      (keys : (fields.map Prod.fst).Perm ["rule","A","B"])
      (rule : ("rule", WireValue.text "k") ∈ fields)
      (argA : ("A",rawA) ∈ fields) (argB : ("B",rawB) ∈ fields)
      (typeA : rawA = typeTree A) (typeB : rawB = typeTree B) :
      NativeProofRep (.object fields) (.k A B)
  | s {fields A B C rawA rawB rawC}
      (keys : (fields.map Prod.fst).Perm ["rule","A","B","C"])
      (rule : ("rule", WireValue.text "s") ∈ fields)
      (argA : ("A",rawA) ∈ fields) (argB : ("B",rawB) ∈ fields) (argC : ("C",rawC) ∈ fields)
      (typeA : rawA = typeTree A) (typeB : rawB = typeTree B) (typeC : rawC = typeTree C) :
      NativeProofRep (.object fields) (.s A B C)
  | app {fields p q rawP rawQ}
      (keys : (fields.map Prod.fst).Perm ["rule","function","argument"])
      (rule : ("rule", WireValue.text "app") ∈ fields)
      (fn : ("function",rawP) ∈ fields) (arg : ("argument",rawQ) ∈ fields)
      (left : NativeProofRep rawP p) (right : NativeProofRep rawQ q) :
      NativeProofRep (.object fields) (.app p q)
  | allI {fields p rawP}
      (keys : (fields.map Prod.fst).Perm ["rule","body"])
      (rule : ("rule", WireValue.text "all_i") ∈ fields)
      (body : ("body",rawP) ∈ fields) (child : NativeProofRep rawP p) :
      NativeProofRep (.object fields) (.allI p)
  | allE {fields p A rawP rawA}
      (keys : (fields.map Prod.fst).Perm ["rule","polymorphic","type"])
      (rule : ("rule", WireValue.text "all_e") ∈ fields)
      (body : ("polymorphic",rawP) ∈ fields) (arg : ("type",rawA) ∈ fields)
      (child : NativeProofRep rawP p) (type : rawA = typeTree A) :
      NativeProofRep (.object fields) (.allE p A)
  | reduce {fields p ts rawP rawT}
      (keys : (fields.map Prod.fst).Perm ["rule","proof","trace"])
      (rule : ("rule", WireValue.text "reduce") ∈ fields)
      (body : ("proof",rawP) ∈ fields) (trace : ("trace",rawT) ∈ fields)
      (child : NativeProofRep rawP p) (terms : rawT = .array (ts.map termTree)) :
      NativeProofRep (.object fields) (.reduce p ts)

end P03Source
