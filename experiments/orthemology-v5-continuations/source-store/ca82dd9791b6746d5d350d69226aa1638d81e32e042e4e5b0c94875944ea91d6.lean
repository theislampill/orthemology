import NativeFieldLemmas
namespace P03Source
open OrthemologyV2 OrthemologyV3

/-- Completeness for every declaratively valid field ordering, with sufficient
structural recursion depth. Canonical field ordering is not a hidden premise. -/
theorem NativeProofRep.decode_complete {value : WireValue} {p : SourceProof}
    (rep : NativeProofRep value p) (fuel : Nat) (height : (proofShape p).height ≤ fuel) :
    decodeProof fuel value = some p := by
  induction rep generalizing fuel with
  | @i fields A rawA keys rule arg repA =>
      have hu := keys.nodup_iff.mpr (by decide)
      have hf := exactFields_complete keys (by decide)
      have hr := lookupField_complete hu rule
      have ha := lookupField_complete hu arg
      cases fuel with
      | zero => simp [proofShape] at height
      | succ fuel =>
          have ht : decodeType fuel rawA = some A := by
            rw [repA]; apply decodeType_roundtrip
            simp only [proofShape] at height; omega
          simp [decodeProof,hr,hf,ha,ht]
  | @k fields A B rawA rawB keys rule argA argB repA repB =>
      have hu := keys.nodup_iff.mpr (by decide)
      have hf := exactFields_complete keys (by decide)
      have hr := lookupField_complete hu rule
      have ha := lookupField_complete hu argA
      have hb := lookupField_complete hu argB
      cases fuel with
      | zero => simp [proofShape] at height
      | succ fuel =>
          have hta : decodeType fuel rawA = some A := by
            rw [repA]; apply decodeType_roundtrip
            simp only [proofShape] at height; omega
          have htb : decodeType fuel rawB = some B := by
            rw [repB]; apply decodeType_roundtrip
            simp only [proofShape] at height; omega
          simp [decodeProof,hr,hf,ha,hb,hta,htb]
  | @s fields A B C rawA rawB rawC keys rule argA argB argC repA repB repC =>
      have hu := keys.nodup_iff.mpr (by decide)
      have hf := exactFields_complete keys (by decide)
      have hr := lookupField_complete hu rule
      have ha := lookupField_complete hu argA
      have hb := lookupField_complete hu argB
      have hc := lookupField_complete hu argC
      cases fuel with
      | zero => simp [proofShape] at height
      | succ fuel =>
          have hta : decodeType fuel rawA = some A := by
            rw [repA]; apply decodeType_roundtrip
            simp only [proofShape] at height; omega
          have htb : decodeType fuel rawB = some B := by
            rw [repB]; apply decodeType_roundtrip
            simp only [proofShape] at height; omega
          have htc : decodeType fuel rawC = some C := by
            rw [repC]; apply decodeType_roundtrip
            simp only [proofShape] at height; omega
          simp [decodeProof,hr,hf,ha,hb,hc,hta,htb,htc]
  | @app fields p q rawP rawQ keys rule fn arg left right ihL ihR =>
      have hu := keys.nodup_iff.mpr (by decide)
      have hf := exactFields_complete keys (by decide)
      have hr := lookupField_complete hu rule
      have hp := lookupField_complete hu fn
      have hq := lookupField_complete hu arg
      cases fuel with
      | zero => simp [proofShape] at height
      | succ fuel =>
          have hl := ihL fuel (by simp only [proofShape] at height; omega)
          have hh := ihR fuel (by simp only [proofShape] at height; omega)
          simp [decodeProof,hr,hf,hp,hq,hl,hh]
  | @allI fields p rawP keys rule body child ih =>
      have hu := keys.nodup_iff.mpr (by decide)
      have hf := exactFields_complete keys (by decide)
      have hr := lookupField_complete hu rule
      have hp := lookupField_complete hu body
      cases fuel with
      | zero => simp [proofShape] at height
      | succ fuel =>
          have hc := ih fuel (by simp only [proofShape] at height; omega)
          simp [decodeProof,hr,hf,hp,hc]
  | @allE fields p A rawP rawA keys rule body arg child repA ih =>
      have hu := keys.nodup_iff.mpr (by decide)
      have hf := exactFields_complete keys (by decide)
      have hr := lookupField_complete hu rule
      have hp := lookupField_complete hu body
      have ha := lookupField_complete hu arg
      cases fuel with
      | zero => simp [proofShape] at height
      | succ fuel =>
          have hc := ih fuel (by simp only [proofShape] at height; omega)
          have ht : decodeType fuel rawA = some A := by
            rw [repA]; apply decodeType_roundtrip
            simp only [proofShape] at height; omega
          simp [decodeProof,hr,hf,hp,ha,hc,ht]
  | @reduce fields p ts rawP rawT keys rule body trace child repT ih =>
      have hu := keys.nodup_iff.mpr (by decide)
      have hf := exactFields_complete keys (by decide)
      have hr := lookupField_complete hu rule
      have hp := lookupField_complete hu body
      have ht := lookupField_complete hu trace
      cases fuel with
      | zero => simp [proofShape] at height
      | succ fuel =>
          have hc := ih fuel (by simp only [proofShape] at height; omega)
          have htrace : decodeTrace fuel rawT = some ts := by
            rw [repT]; apply decodeTrace_roundtrip
            simp only [proofShape] at height; omega
          simp [decodeProof,hr,hf,hp,ht,hc,htrace]

#print axioms NativeProofRep.decode_complete
end P03Source
