import NativeDecoderProofs
namespace P03Source
open OrthemologyV2 OrthemologyV3

theorem decodeType_sound (fuel : Nat) (value : WireValue) (A : TypeCode)
    (h : decodeType fuel value = some A) : value = typeTree A := by
  induction fuel generalizing value A with
  | zero => simp [decodeType] at h
  | succ fuel ih =>
      unfold decodeType at h
      split at h
      next => contradiction
      next => cases h; rfl
      next => cases h; rfl
      next =>
        rename_i fuel' left right heq
        have hf : fuel' = fuel := by omega
        subst fuel'
        cases ha : decodeType fuel left with
        | none => simp [ha] at h
        | some a =>
          cases hb : decodeType fuel right with
          | none => simp [ha,hb] at h
          | some b =>
            simp [ha,hb] at h
            subst A
            simp [typeTree, ih left a ha, ih right b hb]
      next =>
        rename_i fuel' body heq
        have hf : fuel' = fuel := by omega
        subst fuel'
        cases ha : decodeType fuel body with
        | none => simp [ha] at h
        | some a =>
          simp [ha] at h
          subst A
          simp [typeTree, ih body a ha]
      next => contradiction
theorem decodeTerm_sound (fuel : Nat) (value : WireValue) (t : Term)
    (h : decodeTerm fuel value = some t) : value = termTree t := by
  induction fuel generalizing value t with
  | zero => simp [decodeTerm] at h
  | succ fuel ih =>
      unfold decodeTerm at h
      split at h
      next => contradiction
      next => cases h; rfl
      next => cases h; rfl
      next => cases h; rfl
      next => cases h; rfl
      next => cases h; rfl
      next =>
        rename_i fuel' left right heq
        have hf : fuel' = fuel := by omega
        subst fuel'
        cases ha : decodeTerm fuel left with
        | none => simp [ha] at h
        | some a =>
          cases hb : decodeTerm fuel right with
          | none => simp [ha,hb] at h
          | some b =>
            simp [ha,hb] at h
            subst t
            simp [termTree, ih left a ha, ih right b hb]
      next => contradiction

theorem decodeTerms_sound (fuel : Nat) (values : List WireValue) (ts : List Term)
    (h : decodeTerms fuel values = some ts) : values = ts.map termTree := by
  induction values generalizing ts with
  | nil => simp [decodeTerms] at h; subst ts; rfl
  | cons value values ih =>
      simp only [decodeTerms] at h
      cases hv : decodeTerm fuel value with
      | none => simp [hv] at h
      | some t =>
        cases hs : decodeTerms fuel values with
        | none => simp [hv,hs] at h
        | some rest =>
          simp [hv,hs] at h
          subst ts
          simp [decodeTerm_sound fuel value t hv, ih rest hs]

theorem decodeTrace_sound (fuel : Nat) (value : WireValue) (ts : List Term)
    (h : decodeTrace fuel value = some ts) : value = .array (ts.map termTree) := by
  unfold decodeTrace at h
  split at h
  next => cases h; rfl
  next =>
    rename_i fuel' values heq
    have hv := decodeTerms_sound fuel' values ts h
    rw [hv]
  next => contradiction

theorem exactFields_perm {fields : List (String × WireValue)} {names : List String}
    (h : exactFields fields names = true) : (fields.map Prod.fst).Perm names := by
  simp only [exactFields, Bool.and_eq_true] at h
  exact List.isPerm_iff.mp h.2

theorem lookupField_sound {key : String} {fields : List (String × WireValue)} {value : WireValue}
    (h : lookupField key fields = some value) : (key,value) ∈ fields := by
  induction fields with
  | nil => simp [lookupField] at h
  | cons row rest ih =>
      rcases row with ⟨k,v⟩
      simp only [lookupField] at h
      split at h
      next he =>
        simp only [Option.some.injEq] at h
        subst key
        subst value
        exact List.mem_cons_self
      next hn => exact List.mem_cons_of_mem _ (ih h)

end P03Source
