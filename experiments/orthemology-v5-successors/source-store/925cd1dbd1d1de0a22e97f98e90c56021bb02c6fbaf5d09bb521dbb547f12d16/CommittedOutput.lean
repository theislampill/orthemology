import EffectiveTree

/-!
An effective controller is observed after finite computation times. The
observation includes the entire counted technical support. Prefix monotonicity
means committed outputs cannot be revised. Unbounded completion imposes no
uniform waiting-time bound. The extracted bit function is proved computable
using an actual partial-recursive search rather than assumed total in advance.
-/

namespace EffectiveRenewal

abbrev PrefixClosed (T : Word → Prop) : Prop :=
  ∀ {s t}, s <+: t → T t → T s

def Committed (snap : Nat → Word) : Prop :=
  ∀ s t, s ≤ t → snap s <+: snap t

def UnboundedOutput (snap : Nat → Word) : Prop :=
  ∀ n, ∃ t, n ≤ (snap t).length

def observedBit (snap : Nat → Word) (n : Nat) : Part Bool :=
  Nat.rfindOpt fun t => (snap t)[n]?

theorem observedBit_partrec (snap : Nat → Word) (hc : Computable snap) :
    Partrec (observedBit snap) := by
  exact Partrec.rfindOpt
    (Computable.list_getElem?.comp (hc.comp Computable.snd) Computable.fst).to₂

theorem observedBit_total (snap : Nat → Word) (hu : UnboundedOutput snap) (n : Nat) :
    (observedBit snap n).Dom := by
  obtain ⟨t, ht⟩ := hu (n + 1)
  have hn : n < (snap t).length := ht
  apply Nat.rfindOpt_dom.mpr
  exact ⟨t, (snap t)[n], List.getElem?_eq_getElem hn⟩

theorem prefix_lookup {s t : Word} (hp : s <+: t) {n : Nat} {b : Bool}
    (hb : s[n]? = some b) : t[n]? = some b := by
  obtain ⟨hn, he⟩ := List.getElem?_eq_some_iff.mp hb
  rw [List.getElem?_eq_getElem (lt_of_lt_of_le hn hp.length_le), ← hp.getElem hn, he]

theorem committed_lookup_unique {snap : Nat → Word} (hm : Committed snap)
    {t u n : Nat} {b c : Bool} (hb : (snap t)[n]? = some b)
    (hc : (snap u)[n]? = some c) : b = c := by
  rcases le_total t u with h | h
  · have he := prefix_lookup (hm t u h) hb
    exact Option.some.inj (he.symm.trans hc)
  · have he := prefix_lookup (hm u t h) hc
    exact Option.some.inj (hb.symm.trans he)

theorem committed_path_extraction (T : Word → Prop) (hT : PrefixClosed T)
    (snap : Nat → Word) (hc : Computable snap) (hm : Committed snap)
    (hu : UnboundedOutput snap) (hs : ∀ t, T (snap t)) :
    ∃ f : Nat → Bool, Computable f ∧ ∀ n, T (prefixWord f n) := by
  let f : Nat → Bool := fun n => (observedBit snap n).get (observedBit_total snap hu n)
  have hfmem : ∀ n, f n ∈ observedBit snap n := fun n => Part.get_mem _
  have hfc : Computable f := (observedBit_partrec snap hc).of_eq_tot hfmem
  have hflook : ∀ n t, n < (snap t).length → (snap t)[n]? = some (f n) := by
    intro n t hn
    obtain ⟨u, hu⟩ := Nat.rfindOpt_spec (hfmem n)
    have he := committed_lookup_unique hm hu (List.getElem?_eq_getElem hn)
    rw [List.getElem?_eq_getElem hn, he]
  refine ⟨f, hfc, ?_⟩
  intro n
  obtain ⟨t, ht⟩ := hu n
  apply hT (t := snap t) _ (hs t)
  apply List.isPrefix_iff.mpr
  intro e he
  have hen : e < n := by simpa using he
  have het : e < (snap t).length := lt_of_lt_of_le hen ht
  rw [hflook e t het]
  simp [prefixWord, List.getElem_map, List.getElem_range]

theorem no_effective_committed_renewal (snap : Nat → Word) (hc : Computable snap)
    (hm : Committed snap) (hs : ∀ t, diagonalTree (snap t)) :
    ¬ UnboundedOutput snap := by
  intro hu
  obtain ⟨f, hf, hpath⟩ := committed_path_extraction diagonalTree
    (fun hp ht => diagonalTree_prefix_closed hp ht) snap hc hm hu hs
  exact no_computable_path f hf hpath

end EffectiveRenewal
