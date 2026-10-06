import CommittedOutput

/-! Bounded executable operations used by the policy-synthesis reduction. -/
namespace PolicySynthesis
open EffectiveRenewal

abbrev HasComputablePath (T : Word → Prop) : Prop :=
  ∃ f : Nat → Bool, Computable f ∧ ∀ n, T (prefixWord f n)

def allBelow (f : Nat → Bool) (n : Nat) : Bool :=
  ((List.range n).map f).foldr Bool.and true

private theorem foldr_and_true (bs : List Bool) :
    bs.foldr Bool.and true = true ↔ ∀ b ∈ bs, b = true := by
  induction bs with
  | nil => simp
  | cons b bs ih => simp [ih]

@[simp] theorem allBelow_iff (f : Nat → Bool) (n : Nat) :
    allBelow f n = true ↔ ∀ i < n, f i = true := by
  simp [allBelow, foldr_and_true]

theorem allBelow_primrec {α : Type} [Primcodable α]
    {f : α → Nat → Bool} {n : α → Nat} (hf : Primrec₂ f) (hn : Primrec n) :
    Primrec fun a => allBelow (f a) (n a) := by
  exact Primrec.list_foldr
    (Primrec.list_map (Primrec.list_range.comp hn) hf) (Primrec.const true)
    (Primrec.and.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)).to₂

def slice (w : Word) (b m : Nat) : Word :=
  (List.range m).map fun i => w.getD (b + i) false

@[simp] theorem length_slice (w : Word) (b m : Nat) : (slice w b m).length = m := by
  simp [slice]

@[simp] theorem getD_slice (w : Word) (b : Nat) {m i : Nat} (hi : i < m) :
    (slice w b m).getD i false = w.getD (b + i) false := by
  simp [slice, List.getD_eq_getElem?_getD, List.getElem?_range hi]

theorem word_ext {s t : Word} (hl : s.length = t.length)
    (h : ∀ i < s.length, s.getD i false = t.getD i false) : s = t := by
  apply List.ext_getElem hl
  intro i hi hit
  have he := h i hi
  simpa [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi,
    List.getElem?_eq_getElem hit] using he

theorem getD_of_prefix {s t : Word} (hp : s <+: t) {i : Nat} (hi : i < s.length) :
    s.getD i false = t.getD i false := by
  have hit := lt_of_lt_of_le hi hp.length_le
  simp only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi,
    List.getElem?_eq_getElem hit, Option.getD_some]
  exact hp.getElem hi

theorem prefix_of_getD {s t : Word} (hl : s.length ≤ t.length)
    (h : ∀ i < s.length, s.getD i false = t.getD i false) : s <+: t := by
  apply List.isPrefix_iff.mpr
  intro i hi
  have hit := lt_of_lt_of_le hi hl
  have he := h i hi
  simp only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi,
    List.getElem?_eq_getElem hit, Option.getD_some] at he
  rw [List.getElem?_eq_getElem hit, he]

theorem slice_prefix_source {s t : Word} (hp : s <+: t) {b m : Nat}
    (hm : b + m ≤ s.length) : slice s b m = slice t b m := by
  apply word_ext (by simp)
  intro i hi
  have him : i < m := by simpa using hi
  rw [getD_slice _ _ him, getD_slice _ _ him]
  exact getD_of_prefix hp (by omega)

theorem slice_prefix (w : Word) (b : Nat) {m n : Nat} (hmn : m ≤ n) :
    slice w b m <+: slice w b n := by
  apply prefix_of_getD (by simpa using hmn)
  intro i hi
  have him : i < m := by simpa using hi
  rw [getD_slice _ _ him, getD_slice _ _ (lt_of_lt_of_le him hmn)]

theorem slice_prefixWord (f : Nat → Bool) {n b m : Nat} (hm : b + m ≤ n) :
    slice (prefixWord f n) b m = prefixWord (fun i => f (b + i)) m := by
  apply word_ext (by simp)
  intro i hi
  have him : i < m := by simpa using hi
  rw [getD_slice _ _ him, getD_prefixWord _ (by omega), getD_prefixWord _ him]

theorem slice_primrec : Primrec fun p : Word × Nat × Nat => slice p.1 p.2.1 p.2.2 := by
  exact Primrec.list_map (Primrec.list_range.comp (Primrec.snd.comp Primrec.snd))
    ((Primrec.list_getD false).comp (Primrec.fst.comp Primrec.fst)
      (Primrec.nat_add.comp (Primrec.fst.comp (Primrec.snd.comp Primrec.fst)) Primrec.snd)).to₂

end PolicySynthesis
