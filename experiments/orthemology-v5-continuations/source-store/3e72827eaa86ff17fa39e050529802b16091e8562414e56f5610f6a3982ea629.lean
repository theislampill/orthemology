import NativeCheckerBridge
namespace P03Source

theorem noDuplicateFields_iff (fields : List (String × WireValue)) :
    noDuplicateFields fields = true ↔ (fields.map Prod.fst).Nodup := by
  induction fields with
  | nil => simp [noDuplicateFields]
  | cons row rest ih =>
      rcases row with ⟨key,value⟩
      simp [noDuplicateFields, List.nodup_cons, ih, List.any_eq_true, List.mem_map]
      intro _
      constructor
      · intro h x hx
        exact h key x hx rfl
      · intro h a b hab he
        subst a
        exact h b hab

theorem exactFields_complete {fields : List (String × WireValue)} {names : List String}
    (keys : (fields.map Prod.fst).Perm names) (namesUnique : names.Nodup) :
    exactFields fields names = true := by
  have hu : (fields.map Prod.fst).Nodup := keys.nodup_iff.mpr namesUnique
  simp only [exactFields, Bool.and_eq_true]
  exact ⟨(noDuplicateFields_iff fields).mpr hu, List.isPerm_iff.mpr keys⟩

theorem lookupField_complete {key : String} {fields : List (String × WireValue)} {value : WireValue}
    (unique : (fields.map Prod.fst).Nodup) (member : (key,value) ∈ fields) :
    lookupField key fields = some value := by
  induction fields with
  | nil => contradiction
  | cons row rest ih =>
      rcases row with ⟨k,v⟩
      simp only [List.map_cons, List.nodup_cons] at unique
      simp only [List.mem_cons] at member
      cases member with
      | inl he =>
          have hk : key = k := congrArg Prod.fst he
          have hv : value = v := congrArg Prod.snd he
          simp [lookupField,hk,hv]
      | inr hm =>
          have hk : key ≠ k := by
            intro he
            have hmem : k ∈ rest.map Prod.fst := List.mem_map.mpr ⟨(key,value),hm,he⟩
            exact unique.1 hmem
          simp [lookupField,hk,ih unique.2 hm]

#print axioms noDuplicateFields_iff
#print axioms lookupField_complete
end P03Source
