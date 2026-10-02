/- Finite exact-builtin native-tree decoder. This is not UTF-8 JSON parsing,
not Python object/protocol execution, and not an atomic capture of mutable data.
WireValue.object retains field order and duplicate keys explicitly. Duplicate
keys are refused before lookup, matching strict JSON's pre-dict policy; native
Python dictionaries themselves cannot contain two equal keys. -/
import SourceRepresentation
namespace P03Source
open OrthemologyV2 OrthemologyV3

def lookupField (key : String) : List (String × WireValue) → Option WireValue
  | [] => none
  | (k,v)::rest => if key = k then some v else lookupField key rest

def noDuplicateFields : List (String × WireValue) → Bool
  | [] => true
  | (k,_)::rest => !(rest.any (fun row => row.1 == k)) && noDuplicateFields rest

def exactFields (fields : List (String × WireValue)) (names : List String) : Bool :=
  noDuplicateFields fields && (fields.map Prod.fst).isPerm names

def decodeType : Nat → WireValue → Option TypeCode
  | 0, _ => none
  | _+1, .array [.text "v", .natural n] => some (.var n)
  | _+1, .array [.text "bottom"] => some .bottom
  | fuel+1, .array [.text "arr", A, B] => do
      let a ← decodeType fuel A
      let b ← decodeType fuel B
      pure (.arrow a b)
  | fuel+1, .array [.text "all", A] => do
      let a ← decodeType fuel A
      pure (.all a)
  | _+1, _ => none

def decodeTerm : Nat → WireValue → Option Term
  | 0, _ => none
  | _+1, .array [.text "i"] => some .i
  | _+1, .array [.text "k"] => some .k
  | _+1, .array [.text "s"] => some .s
  | _+1, .array [.text "zero"] => some .zero
  | _+1, .array [.text "one"] => some .one
  | fuel+1, .array [.text "app", f, x] => do
      let a ← decodeTerm fuel f
      let b ← decodeTerm fuel x
      pure (.app a b)
  | _+1, _ => none

def decodeTerms (fuel : Nat) : List WireValue → Option (List Term)
  | [] => some []
  | x::xs => do
      let t ← decodeTerm fuel x
      let ts ← decodeTerms fuel xs
      pure (t::ts)

def decodeTrace : Nat → WireValue → Option (List Term)
  | _, .array [] => some []
  | fuel+1, .array ts => decodeTerms fuel ts
  | _, _ => none

/-- Seven exact rule branches. Missing/extra/duplicate fields and malformed
native type/term/trace shapes are refusals; semantic scope/trace checks follow
in sourceCheck and are never replaced by successful syntax decoding. -/
def decodeProof : Nat → WireValue → Option SourceProof
  | 0, _ => none
  | fuel+1, .object fields => do
      let rule ← lookupField "rule" fields
      match rule with
      | .text "i" =>
          if exactFields fields ["rule","A"] then do
            let A ← lookupField "A" fields
            let a ← decodeType fuel A
            pure (.i a)
          else none
      | .text "k" =>
          if exactFields fields ["rule","A","B"] then do
            let A ← lookupField "A" fields
            let B ← lookupField "B" fields
            let a ← decodeType fuel A
            let b ← decodeType fuel B
            pure (.k a b)
          else none
      | .text "s" =>
          if exactFields fields ["rule","A","B","C"] then do
            let A ← lookupField "A" fields
            let B ← lookupField "B" fields
            let C ← lookupField "C" fields
            let a ← decodeType fuel A
            let b ← decodeType fuel B
            let c ← decodeType fuel C
            pure (.s a b c)
          else none
      | .text "app" =>
          if exactFields fields ["rule","function","argument"] then do
            let F ← lookupField "function" fields
            let X ← lookupField "argument" fields
            let f ← decodeProof fuel F
            let x ← decodeProof fuel X
            pure (.app f x)
          else none
      | .text "all_i" =>
          if exactFields fields ["rule","body"] then do
            let P ← lookupField "body" fields
            let p ← decodeProof fuel P
            pure (.allI p)
          else none
      | .text "all_e" =>
          if exactFields fields ["rule","polymorphic","type"] then do
            let P ← lookupField "polymorphic" fields
            let A ← lookupField "type" fields
            let p ← decodeProof fuel P
            let a ← decodeType fuel A
            pure (.allE p a)
          else none
      | .text "reduce" =>
          if exactFields fields ["rule","proof","trace"] then do
            let P ← lookupField "proof" fields
            let T ← lookupField "trace" fields
            let p ← decodeProof fuel P
            let ts ← decodeTrace fuel T
            pure (.reduce p ts)
          else none
      | _ => none
  | _+1, _ => none

def decodeNativeProof (value : WireValue) : Option SourceProof :=
  if shapeFits (wireShape value) then decodeProof 100 value else none

def nativeCheck (d : Nat) (value : WireValue) : Option (Term × TypeCode) := do
  let p ← decodeNativeProof value
  sourceCheck d p

end P03Source
