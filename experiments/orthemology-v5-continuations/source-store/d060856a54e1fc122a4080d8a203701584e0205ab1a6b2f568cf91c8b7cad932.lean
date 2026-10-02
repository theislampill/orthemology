import NativeProofSoundness
import SourceExportBoundary
namespace P03Source
open OrthemologyV2 OrthemologyV3

theorem NativeProofRep.uniqueFields {fields : List (String × WireValue)} {p : SourceProof}
    (h : NativeProofRep (.object fields) p) : (fields.map Prod.fst).Nodup := by
  cases h with
  | i keys rule arg type => exact keys.nodup_iff.mpr (by decide)
  | k keys rule argA argB typeA typeB => exact keys.nodup_iff.mpr (by decide)
  | s keys rule argA argB argC typeA typeB typeC => exact keys.nodup_iff.mpr (by decide)
  | app keys rule fn arg left right => exact keys.nodup_iff.mpr (by decide)
  | allI keys rule body child => exact keys.nodup_iff.mpr (by decide)
  | allE keys rule body arg child type => exact keys.nodup_iff.mpr (by decide)
  | reduce keys rule body trace child terms => exact keys.nodup_iff.mpr (by decide)

theorem decodeNativeProof_sound {value : WireValue} {p : SourceProof}
    (h : decodeNativeProof value = some p) : NativeProofRep value p := by
  unfold decodeNativeProof at h
  split at h
  next hs => exact decodeProof_sound 100 value p h
  next hn => contradiction

/-- Arbitrary native-tree inputs are parsed before the independent source
checker. Successful results have a declarative grammar witness and the same
term/type in the inherited target checker. No raw-text or interpreter claim. -/
theorem native_checker_constructor_erasure_square {d : Nat} {value : WireValue}
    {out : Term × TypeCode} (h : nativeCheck d value = some out) :
    ∃ p v, decodeNativeProof value = some p ∧ NativeProofRep value p ∧
      check d (encode p) = some v ∧ v.term = out.1 ∧ v.ty = out.2 := by
  unfold nativeCheck at h
  obtain ⟨p,hp,hs⟩ := Option.bind_eq_some.mp h
  obtain ⟨v,hv,ht,ha⟩ := source_checker_constructor_erasure_square p d out hs
  exact ⟨p,v,hp,decodeNativeProof_sound hp,hv,ht,ha⟩

theorem native_checker_sound {d : Nat} {value : WireValue} {out : Term × TypeCode}
    (h : nativeCheck d value = some out) (rho : Nat → Code) :
    (interpret out.2 rho).accepts out.1 := by
  unfold nativeCheck at h
  obtain ⟨p,hp,hs⟩ := Option.bind_eq_some.mp h
  exact source_checker_sound p d out hs rho

theorem native_check_rejects_duplicate_fields {d : Nat} {fields : List (String × WireValue)}
    (duplicates : ¬ (fields.map Prod.fst).Nodup) : nativeCheck d (.object fields) = none := by
  cases hr : nativeCheck d (.object fields) with
  | none => rfl
  | some out =>
      obtain ⟨p,v,hp,rep,rest⟩ := native_checker_constructor_erasure_square hr
      exact False.elim (duplicates rep.uniqueFields)

/-- The actual constructor-export budget remains a separate successful phase. -/
theorem native_checker_partial_export_square {value : WireValue} {p : SourceProof}
    {out : Term × TypeCode} {c : Cert}
    (decoded : decodeNativeProof value = some p)
    (sourceAccepted : nativeCheck 0 value = some out)
    (exportSucceeded : partialConstructorExport p = some (c,out)) :
    NativeProofRep value p ∧
      ∃ v, check 0 c = some v ∧ v.term = out.1 ∧ v.ty = out.2 ∧ certNodes c ≤ 512 := by
  refine ⟨decodeNativeProof_sound decoded, ?_⟩
  apply source_checker_export_square _ exportSucceeded
  simpa [nativeCheck, decoded] using sourceAccepted

#print axioms native_checker_constructor_erasure_square
#print axioms native_checker_sound
#print axioms native_check_rejects_duplicate_fields
#print axioms native_checker_partial_export_square
end P03Source
