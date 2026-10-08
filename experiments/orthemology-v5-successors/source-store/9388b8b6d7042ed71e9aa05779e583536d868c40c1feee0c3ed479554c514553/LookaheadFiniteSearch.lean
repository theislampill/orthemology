import EffectiveRenewalBoundary

namespace EffectiveRenewal.Lookahead

/-- Exact finite binary levels. This is an enumeration, not an infinite path. -/
def binaryWords : Nat → List Word
  | 0 => [[]]
  | n + 1 => (binaryWords n).flatMap fun w => [false :: w, true :: w]

theorem binaryWords_primrec : Primrec binaryWords := by
  have hnext : Primrec fun p : Nat × List Word =>
      p.2.flatMap (fun w => [false :: w, true :: w]) :=
    Primrec.list_flatMap Primrec.snd
      (Primrec.list_cons.comp
        (Primrec.list_cons.comp (Primrec.const false) Primrec.snd)
        (Primrec.list_cons.comp
          (Primrec.list_cons.comp (Primrec.const true) Primrec.snd) (Primrec.const []))).to₂
  have h := Primrec.nat_rec' Primrec.id (Primrec.const ([[]] : List Word))
    (hnext.comp Primrec.snd).to₂
  apply h.of_eq
  intro n
  induction n with
  | zero => rfl
  | succ n ih => simpa only [binaryWords] using (congrArg
        (fun ws : List Word => ws.flatMap fun w => [false :: w, true :: w]) ih)

theorem mem_binaryWords_iff (n : Nat) (s : Word) : s ∈ binaryWords n ↔ s.length = n := by
  induction n generalizing s with
  | zero => simp [binaryWords]
  | succ n ih =>
    cases s with
    | nil => simp [binaryWords]
    | cons b s =>
      cases b <;> simp [binaryWords, ih]

/-- Finite scan retaining the first accepted candidate. It never performs
unbounded minimisation, although the supplied predicate may take unbounded
finite computation time at each call. -/
def selectScan (test : Word → Bool) (candidates : List Word) : Nat → Option Word
  | 0 => none
  | k + 1 => (selectScan test candidates k).casesOn (motive := fun _ => Option Word)
      (cond (test (candidates.getD k [])) (some (candidates.getD k [])) none) some

def boundedSelect (test : Word → Bool) (candidates : List Word) : Option Word :=
  selectScan test candidates candidates.length

theorem boundedSelect_computable {α : Type} [Primcodable α]
    (test : α → Word → Bool) (ht : Computable₂ test) :
    Computable fun p : α × List Word => boundedSelect (test p.1) p.2 := by
  have candidate : Computable fun p : (α × List Word) × (Nat × Option Word) =>
      p.1.2.getD p.2.1 [] :=
    (Primrec.list_getD ([] : Word)).to_comp.comp
      (Computable.snd.comp Computable.fst) (Computable.fst.comp Computable.snd)
  have testCandidate : Computable fun p : (α × List Word) × (Nat × Option Word) =>
      test p.1.1 (p.1.2.getD p.2.1 []) :=
    ht.comp (Computable.fst.comp Computable.fst) candidate
  have step : Computable fun p : (α × List Word) × (Nat × Option Word) =>
      p.2.2.casesOn (motive := fun _ => Option Word) (cond (test p.1.1 (p.1.2.getD p.2.1 []))
        (some (p.1.2.getD p.2.1 [])) none) some :=
    Computable.option_casesOn (Computable.snd.comp Computable.snd)
      (Computable.cond testCandidate (Computable.option_some.comp candidate) (Computable.const none))
      (Computable.option_some.comp Computable.snd).to₂
  have h := Computable.nat_rec (Computable.list_length.comp Computable.snd)
    (Computable.const (none : Option Word)) step.to₂
  apply h.of_eq
  intro p
  unfold boundedSelect
  generalize p.2.length = n
  induction n with
  | zero => rfl
  | succ n ih => simpa only [selectScan] using (congrArg
        (fun o : Option Word => o.casesOn (motive := fun _ => Option Word)
          (cond (test p.1 (p.2.getD n [])) (some (p.2.getD n [])) none) some) ih)

theorem selectScan_sound (test : Word → Bool) (candidates : List Word) (k : Nat)
    (hk : k ≤ candidates.length) {w : Word} (hw : selectScan test candidates k = some w) :
    w ∈ candidates ∧ test w = true := by
  induction k generalizing w with
  | zero => simp [selectScan] at hw
  | succ k ih =>
    have hkl : k < candidates.length := hk
    cases prev : selectScan test candidates k with
    | some v =>
      have he : v = w := by simpa only [selectScan, prev, Option.some.injEq] using hw
      exact he ▸ ih (Nat.le_of_lt hkl) prev
    | none =>
      cases ht : test (candidates.getD k []) with
      | false => simp only [selectScan, prev, ht, Bool.cond_false, reduceCtorEq] at hw
      | true =>
        have he : candidates.getD k [] = w := by simpa only [selectScan, prev, ht, Bool.cond_true, Option.some.injEq] using hw
        have hg : candidates.getD k [] = candidates[k] := by
          simp [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hkl]
        exact ⟨he ▸ hg.symm ▸ List.getElem_mem hkl, he ▸ ht⟩

theorem selectScan_none_iff (test : Word → Bool) (candidates : List Word) (k : Nat) :
    selectScan test candidates k = none ↔
      ∀ i < k, test (candidates.getD i []) = false := by
  induction k with
  | zero => simp [selectScan]
  | succ k ih =>
    cases hp : selectScan test candidates k with
    | some w =>
      have hn : ¬ ∀ i < k, test (candidates.getD i []) = false := by
        intro h; have := ih.mpr h; simp [hp] at this
      constructor
      · simp only [selectScan, hp, reduceCtorEq, false_implies]
      · intro h
        exact (hn (fun i hi => h i (Nat.lt_succ_of_lt hi))).elim
    | none =>
      have hall := ih.mp hp
      cases ht : test (candidates.getD k []) with
      | false =>
        simp only [selectScan, hp, ht, Bool.cond_false]
        constructor
        · intro _ i hi
          rcases Nat.lt_succ_iff_lt_or_eq.mp hi with h | rfl
          · exact hall i h
          · exact ht
        · intro _; trivial
      | true =>
        constructor
        · simp only [selectScan, hp, ht, Bool.cond_true, reduceCtorEq, false_implies]
        · intro h; have := h k (Nat.lt_succ_self k); rw [ht] at this; contradiction

theorem boundedSelect_spec (test : Word → Bool) (candidates : List Word) :
    (∀ w, boundedSelect test candidates = some w → w ∈ candidates ∧ test w = true) ∧
    ((boundedSelect test candidates).isSome = true ↔ ∃ w ∈ candidates, test w = true) := by
  refine ⟨fun w hw => selectScan_sound test candidates candidates.length (Nat.le_refl _) hw, ?_⟩
  constructor
  · intro h
    obtain ⟨w, hw⟩ := Option.isSome_iff_exists.mp h
    have hs := selectScan_sound test candidates candidates.length (Nat.le_refl _) hw
    exact ⟨w, hs.1, hs.2⟩
  · rintro ⟨w, hw, ht⟩
    cases hs : boundedSelect test candidates with
    | some v => rfl
    | none =>
      obtain ⟨i, hi, he⟩ := List.mem_iff_getElem.mp hw
      have hfalse := (selectScan_none_iff test candidates candidates.length).mp hs i hi
      have hg : candidates.getD i [] = w := by
        simp [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi, he]
      rw [hg, ht] at hfalse
      contradiction

end EffectiveRenewal.Lookahead
