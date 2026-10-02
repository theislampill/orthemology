import NativeProofGrammar
namespace P03Source
open OrthemologyV2 OrthemologyV3

theorem decodeProof_sound (fuel : Nat) (value : WireValue) (p : SourceProof)
    (h : decodeProof fuel value = some p) : NativeProofRep value p := by
  induction fuel generalizing value p with
  | zero => simp [decodeProof] at h
  | succ fuel ih =>
      unfold decodeProof at h
      split at h
      next => contradiction
      next =>
        rename_i fuel' fields heq
        have hf : fuel' = fuel := by omega
        subst fuel'
        cases hr : lookupField "rule" fields with
        | none => simp [hr] at h
        | some rule =>
          simp only [hr, bind, Option.bind] at h
          split at h
          next =>
            split at h
            next hfields =>
              obtain ⟨rawA,ha,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨A,hA,h⟩ := Option.bind_eq_some.mp h
              cases h
              exact NativeProofRep.i (exactFields_perm hfields) (lookupField_sound hr) (lookupField_sound ha) (decodeType_sound fuel rawA A hA)
            next hbad => contradiction
          next =>
            split at h
            next hfields =>
              obtain ⟨rawA,ha,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨rawB,hb,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨A,hA,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨B,hB,h⟩ := Option.bind_eq_some.mp h
              cases h
              exact NativeProofRep.k (exactFields_perm hfields) (lookupField_sound hr) (lookupField_sound ha) (lookupField_sound hb) (decodeType_sound fuel rawA A hA) (decodeType_sound fuel rawB B hB)
            next hbad => contradiction
          next =>
            split at h
            next hfields =>
              obtain ⟨rawA,ha,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨rawB,hb,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨rawC,hc,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨A,hA,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨B,hB,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨C,hC,h⟩ := Option.bind_eq_some.mp h
              cases h
              exact NativeProofRep.s (exactFields_perm hfields) (lookupField_sound hr) (lookupField_sound ha) (lookupField_sound hb) (lookupField_sound hc) (decodeType_sound fuel rawA A hA) (decodeType_sound fuel rawB B hB) (decodeType_sound fuel rawC C hC)
            next hbad => contradiction
          next =>
            split at h
            next hfields =>
              obtain ⟨rawP,hp,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨rawQ,hq,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨p1,hp1,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨q1,hq1,h⟩ := Option.bind_eq_some.mp h
              cases h
              exact NativeProofRep.app (exactFields_perm hfields) (lookupField_sound hr) (lookupField_sound hp) (lookupField_sound hq) (ih rawP p1 hp1) (ih rawQ q1 hq1)
            next hbad => contradiction
          next =>
            split at h
            next hfields =>
              obtain ⟨rawP,hp,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨p1,hp1,h⟩ := Option.bind_eq_some.mp h
              cases h
              exact NativeProofRep.allI (exactFields_perm hfields) (lookupField_sound hr) (lookupField_sound hp) (ih rawP p1 hp1)
            next hbad => contradiction
          next =>
            split at h
            next hfields =>
              obtain ⟨rawP,hp,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨rawA,ha,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨p1,hp1,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨A,hA,h⟩ := Option.bind_eq_some.mp h
              cases h
              exact NativeProofRep.allE (exactFields_perm hfields) (lookupField_sound hr) (lookupField_sound hp) (lookupField_sound ha) (ih rawP p1 hp1) (decodeType_sound fuel rawA A hA)
            next hbad => contradiction
          next =>
            split at h
            next hfields =>
              obtain ⟨rawP,hp,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨rawT,ht,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨p1,hp1,h⟩ := Option.bind_eq_some.mp h
              obtain ⟨ts,hts,h⟩ := Option.bind_eq_some.mp h
              cases h
              exact NativeProofRep.reduce (exactFields_perm hfields) (lookupField_sound hr) (lookupField_sound hp) (lookupField_sound ht) (ih rawP p1 hp1) (decodeTrace_sound fuel rawT ts hts)
            next hbad => contradiction
          next => contradiction
      next => contradiction
#print axioms decodeProof_sound
end P03Source
