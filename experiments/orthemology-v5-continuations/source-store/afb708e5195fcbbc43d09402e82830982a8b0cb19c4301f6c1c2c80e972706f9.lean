import NativeDecoderCompleteness
import SourceResourceBounds
namespace P03Source
open OrthemologyV2 OrthemologyV3

theorem NativeProofRep.deterministic {value : WireValue} {p q : SourceProof}
    (left : NativeProofRep value p) (right : NativeProofRep value q) : p = q := by
  let fuel := max (proofShape p).height (proofShape q).height
  have hl := left.decode_complete fuel (Nat.le_max_left _ _)
  have hr := right.decode_complete fuel (Nat.le_max_right _ _)
  exact Option.some.inj (hl.symm.trans hr)

/-- On every bounded native-tree representation, decoding preserves the entire
source-checker outcome, including semantic or resource refusal. This is a
model-level equivalence, not a claim that UTF-8 JSON/CPython has been verified. -/
theorem nativeCheck_representation_equivalence {value : WireValue} {p : SourceProof}
    (rep : NativeProofRep value p) (bounds : shapeFits (wireShape value) = true) (d : Nat) :
    nativeCheck d value = sourceCheck d p := by
  cases hs : sourceCheck d p with
  | none =>
      cases hd : decodeNativeProof value with
      | none => simp [nativeCheck,hd]
      | some q =>
          have hq := decodeNativeProof_sound hd
          have he := rep.deterministic hq
          subst q
          simp [nativeCheck,hd,hs]
  | some out =>
      have hg := sourceCheck_input_guards hs
      have hp : (proofShape p).height ≤ 100 := by
        have hb := hg.2.1
        rw [proofTree_shape] at hb
        simp only [shapeFits, Bool.and_eq_true, decide_eq_true_eq] at hb
        exact hb.1.2
      have hd : decodeNativeProof value = some p := by
        simp [decodeNativeProof,bounds,rep.decode_complete 100 hp]
      simp [nativeCheck,hd,hs]

#print axioms NativeProofRep.deterministic
#print axioms nativeCheck_representation_equivalence
end P03Source
