import FiniteOutputTable
import UniformDecoderPrimrec

/-! Finite list presentations of the exact variable-depth source and output
word tables. The equivalence proofs preserve the existing observer semantics. -/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore P02A2.FiniteOutputTable

def allWords : ℕ → List (List Bool)
  | 0 => [[]]
  | n+1 => (allWords n).map (false :: ·) ++ (allWords n).map (true :: ·)

def outputList (e : ℕ) (v : List Bool) : List Bool :=
  (List.range v.length).map (fun i =>
    decide (evaluateIndex e i (sentinel (v.take (i+1))) % 2 = 1))

def wordCount (e N : ℕ) (w : List Bool) : ℕ :=
  ((allWords N).filter (fun v => decide (outputList e v = w))).length

def heavyCount (e k N : ℕ) : ℕ :=
  ((allWords N).map (fun w =>
    if 2^N ≤ wordCount e N w * 2^k then wordCount e N w else 0)).sum

@[simp] theorem mem_allWords (n : ℕ) (v : List Bool) : v ∈ allWords n ↔ v.length = n := by
  induction n generalizing v with
  | zero => simp [allWords]
  | succ n ih =>
      cases v with
      | nil => simp [allWords]
      | cons b v => cases b <;> simp [allWords, ih]

theorem allWords_nodup (n : ℕ) : (allWords n).Nodup := by
  induction n with
  | zero => simp [allWords]
  | succ n ih =>
      rw [allWords, List.nodup_append]
      refine ⟨ih.map (fun _ _ h => (List.cons.inj h).2),
        ih.map (fun _ _ h => (List.cons.inj h).2), ?_⟩
      intro v hv hw
      rcases List.mem_map.mp hv with ⟨a,_,ha⟩
      rcases List.mem_map.mp hw with ⟨b,_,hb⟩
      have := (List.cons.inj (ha.trans hb.symm)).1
      contradiction

theorem allWords_toFinset (n : ℕ) :
    (allWords n).toFinset = Finset.univ.image (List.ofFn : (Fin n → Bool) → List Bool) := by
  ext v
  simp only [List.mem_toFinset, mem_allWords, Finset.mem_image, Finset.mem_univ, true_and]
  constructor
  · intro h
    subst n
    exact ⟨fun i => v[i.val], List.ofFn_getElem v⟩
  · rintro ⟨w,rfl⟩
    simp

theorem sum_allWords {β : Type*} [AddCommMonoid β] (n : ℕ) (f : List Bool → β) :
    ((allWords n).map f).sum = ∑ w : Fin n → Bool, f (List.ofFn w) := by
  rw [← List.sum_toFinset f (allWords_nodup n), allWords_toFinset]
  exact Finset.sum_image (fun _ _ _ _ h => List.ofFn_injective h)

theorem ofFn_take_extend (N : ℕ) (v : Fin N → Bool) (m : ℕ) (hm : m ≤ N) :
    (List.ofFn v).take m = List.ofFn (fun j : Fin m => extendWord N v j.val) := by
  apply List.ext_getElem
  · simp [hm, Nat.min_eq_left]
  · intro i hi hj
    have hiN : i < N := by simpa using (lt_of_lt_of_le (by simpa using hj) hm)
    simp [extendWord, hiN]

theorem outputList_ofFn (e N : ℕ) (v : Fin N → Bool) :
    outputList e (List.ofFn v) = List.ofFn (finiteOutput (evaluateIndex e) N v) := by
  apply List.ext_getElem
  · simp [outputList]
  · intro i hi hj
    have hiN : i < N := by simpa using hj
    simp only [outputList, List.getElem_map, List.getElem_range, List.getElem_ofFn,
      finiteOutput, AtomicMembership.bitsPrefix, output]
    rw [ofFn_take_extend N v (i+1) (by omega)]

theorem wordCount_exact (e N : ℕ) (w : Fin N → Bool) :
    wordCount e N (List.ofFn w) = (preimageWords (evaluateIndex e) N w).card := by
  unfold wordCount
  rw [← List.toFinset_card_of_nodup ((allWords_nodup N).filter _),
    List.toFinset_filter, allWords_toFinset, Finset.filter_image,
    Finset.card_image_of_injective _ List.ofFn_injective]
  congr 1
  ext v
  simp [preimageWords, outputList_ofFn]

#print axioms sum_allWords
#print axioms outputList_ofFn
#print axioms wordCount_exact

end P02.Codec.UniformComputability
