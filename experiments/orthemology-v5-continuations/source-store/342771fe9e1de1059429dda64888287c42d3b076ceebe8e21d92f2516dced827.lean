import NativeDecoder
namespace P03Source
open OrthemologyV2 OrthemologyV3

theorem typeShape_height_positive (A : TypeCode) : 1 ≤ (typeShape A).height := by
  cases A <;> simp [typeShape]

theorem termShape_height_positive (t : Term) : 1 ≤ (termShape t).height := by
  cases t <;> simp [termShape]

theorem decodeType_roundtrip (A : TypeCode) (fuel : Nat)
    (h : (typeShape A).height ≤ fuel) : decodeType fuel (typeTree A) = some A := by
  induction A generalizing fuel with
  | var n =>
      cases fuel with
      | zero => simp [typeShape] at h
      | succ fuel => rfl
  | bottom =>
      cases fuel with
      | zero => simp [typeShape] at h
      | succ fuel => rfl
  | arrow A B ihA ihB =>
      cases fuel with
      | zero => simp [typeShape] at h
      | succ fuel =>
          simp only [typeShape] at h
          have ha : (typeShape A).height ≤ fuel := by omega
          have hb : (typeShape B).height ≤ fuel := by omega
          simp [typeTree, decodeType, ihA fuel ha, ihB fuel hb]
  | all A ih =>
      cases fuel with
      | zero => simp [typeShape] at h
      | succ fuel =>
          simp only [typeShape] at h
          have ha : (typeShape A).height ≤ fuel := by omega
          simp [typeTree, decodeType, ih fuel ha]

theorem decodeTerm_roundtrip (t : Term) (fuel : Nat)
    (h : (termShape t).height ≤ fuel) : decodeTerm fuel (termTree t) = some t := by
  induction t generalizing fuel with
  | i | k | s | zero | one =>
      cases fuel with
      | zero => simp [termShape] at h
      | succ fuel => rfl
  | app f x ihf ihx =>
      cases fuel with
      | zero => simp [termShape] at h
      | succ fuel =>
          simp only [termShape] at h
          have hf : (termShape f).height ≤ fuel := by omega
          have hx : (termShape x).height ≤ fuel := by omega
          simp [termTree, decodeTerm, ihf fuel hf, ihx fuel hx]

theorem decodeTerms_roundtrip (ts : List Term) (fuel : Nat)
    (h : ∀ t ∈ ts, (termShape t).height ≤ fuel) :
    decodeTerms fuel (ts.map termTree) = some ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
      have ht := h t (by simp)
      have hs : ∀ x ∈ ts, (termShape x).height ≤ fuel := by
        intro x hx
        exact h x (by simp [hx])
      simp [decodeTerms, decodeTerm_roundtrip t fuel ht, ih hs]

theorem foldMax_ge_initial (xs : List Nat) (start : Nat) : start ≤ xs.foldl max start := by
  induction xs generalizing start with
  | nil => exact Nat.le_refl start
  | cons x xs ih =>
      simp only [List.foldl_cons]
      exact Nat.le_trans (Nat.le_max_left start x) (ih (max start x))

theorem foldMax_ge_member (xs : List Nat) (start value : Nat) (h : value ∈ xs) :
    value ≤ xs.foldl max start := by
  induction xs generalizing start with
  | nil => contradiction
  | cons x xs ih =>
      simp only [List.mem_cons] at h
      cases h with
      | inl he =>
          subst value
          simp only [List.foldl_cons]
          exact Nat.le_trans (Nat.le_max_right start x) (foldMax_ge_initial xs (max start x))
      | inr hm => exact ih (max start x) hm

theorem decodeTrace_roundtrip (ts : List Term) (fuel : Nat)
    (h : (traceShape ts).height ≤ fuel) :
    decodeTrace fuel (.array (ts.map termTree)) = some ts := by
  cases ts with
  | nil => cases fuel <;> rfl
  | cons t ts =>
      cases fuel with
      | zero => simp [traceShape] at h
      | succ fuel =>
          have hall : ∀ x ∈ t::ts, (termShape x).height ≤ fuel := by
            intro x hx
            have hm : (termShape x).height ∈ (t::ts).map (fun x => (termShape x).height) :=
              List.mem_map.mpr ⟨x,hx,rfl⟩
            have hb := foldMax_ge_member ((t::ts).map (fun x => (termShape x).height)) 0
              ((termShape x).height) hm
            simp only [traceShape] at h
            omega
          simpa only [List.map_cons, decodeTrace] using decodeTerms_roundtrip (t::ts) fuel hall

theorem decodeProof_roundtrip (p : SourceProof) (fuel : Nat)
    (h : (proofShape p).height ≤ fuel) : decodeProof fuel (proofTree p) = some p := by
  induction p generalizing fuel with
  | i A =>
      cases fuel with
      | zero => simp [proofShape] at h
      | succ fuel =>
          have ha : (typeShape A).height ≤ fuel := by simp only [proofShape] at h; omega
          simp [decodeProof, proofTree, lookupField, exactFields, noDuplicateFields, List.isPerm_iff,
            decodeType_roundtrip A fuel ha]
  | k A B =>
      cases fuel with
      | zero => simp [proofShape] at h
      | succ fuel =>
          have ha : (typeShape A).height ≤ fuel := by simp only [proofShape] at h; omega
          have hb : (typeShape B).height ≤ fuel := by simp only [proofShape] at h; omega
          simp [decodeProof, proofTree, lookupField, exactFields, noDuplicateFields, List.isPerm_iff,
            decodeType_roundtrip A fuel ha, decodeType_roundtrip B fuel hb]
  | s A B C =>
      cases fuel with
      | zero => simp [proofShape] at h
      | succ fuel =>
          have ha : (typeShape A).height ≤ fuel := by simp only [proofShape] at h; omega
          have hb : (typeShape B).height ≤ fuel := by simp only [proofShape] at h; omega
          have hc : (typeShape C).height ≤ fuel := by simp only [proofShape] at h; omega
          simp [decodeProof, proofTree, lookupField, exactFields, noDuplicateFields, List.isPerm_iff,
            decodeType_roundtrip A fuel ha, decodeType_roundtrip B fuel hb, decodeType_roundtrip C fuel hc]
  | app p q ihp ihq =>
      cases fuel with
      | zero => simp [proofShape] at h
      | succ fuel =>
          have hp : (proofShape p).height ≤ fuel := by simp only [proofShape] at h; omega
          have hq : (proofShape q).height ≤ fuel := by simp only [proofShape] at h; omega
          simp [decodeProof, proofTree, lookupField, exactFields, noDuplicateFields, List.isPerm_iff,
            ihp fuel hp, ihq fuel hq]
  | allI p ih =>
      cases fuel with
      | zero => simp [proofShape] at h
      | succ fuel =>
          have hp : (proofShape p).height ≤ fuel := by simp only [proofShape] at h; omega
          simp [decodeProof, proofTree, lookupField, exactFields, noDuplicateFields, List.isPerm_iff, ih fuel hp]
  | allE p A ih =>
      cases fuel with
      | zero => simp [proofShape] at h
      | succ fuel =>
          have hp : (proofShape p).height ≤ fuel := by simp only [proofShape] at h; omega
          have ha : (typeShape A).height ≤ fuel := by simp only [proofShape] at h; omega
          simp [decodeProof, proofTree, lookupField, exactFields, noDuplicateFields, List.isPerm_iff,
            ih fuel hp, decodeType_roundtrip A fuel ha]
  | reduce p ts ih =>
      cases fuel with
      | zero => simp [proofShape] at h
      | succ fuel =>
          have hp : (proofShape p).height ≤ fuel := by simp only [proofShape] at h; omega
          have ht : (traceShape ts).height ≤ fuel := by simp only [proofShape] at h; omega
          simp [decodeProof, proofTree, lookupField, exactFields, noDuplicateFields, List.isPerm_iff,
            ih fuel hp, decodeTrace_roundtrip ts fuel ht]

theorem decodeNativeProof_roundtrip (p : SourceProof) (h : shapeFits (proofShape p) = true) :
    decodeNativeProof (proofTree p) = some p := by
  have hh := h
  simp only [shapeFits, Bool.and_eq_true, decide_eq_true_eq] at hh
  simp [decodeNativeProof, proofTree_shape, h, decodeProof_roundtrip p 100 hh.1.2]

#print axioms decodeProof_roundtrip
#print axioms decodeNativeProof_roundtrip
end P03Source
