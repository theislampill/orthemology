import LookaheadFiniteSearch

namespace EffectiveRenewal.Lookahead

def descendants (s : Word) (k : Nat) : List Word :=
  (binaryWords k).map (s ++ ·)

theorem descendants_primrec : Primrec₂ descendants :=
  Primrec.list_map (binaryWords_primrec.comp Primrec.snd)
    (Primrec.list_append.comp (Primrec.fst.comp Primrec.fst) Primrec.snd).to₂

theorem mem_descendants_iff (s w : Word) (k : Nat) :
    w ∈ descendants s k ↔ s <+: w ∧ w.length = s.length + k := by
  constructor
  · intro hw
    obtain ⟨tail, ht, rfl⟩ := List.mem_map.mp hw
    have hlen := (mem_binaryWords_iff k tail).mp ht
    exact ⟨⟨tail, rfl⟩, by simp [hlen]⟩
  · rintro ⟨⟨tail, rfl⟩, hlen⟩
    apply List.mem_map.mpr
    refine ⟨tail, (mem_binaryWords_iff k tail).mpr ?_, rfl⟩
    simpa using hlen

/-- A supplementary witness is in the BASE tree, not recursively in L_h. -/
def BaseWitness (h : Word → Nat) (s w : Word) : Prop :=
  s <+: w ∧ w.length = s.length + h s ∧ diagonalTree w

def supplement (h : Word → Nat) (s : Word) : Option Word :=
  boundedSelect treeCheck (descendants s (h s))

def lookCheck (h : Word → Nat) (s : Word) : Bool := (supplement h s).isSome

theorem supplement_computable (h : Word → Nat) (hc : Computable h) : Computable (supplement h) :=
  (boundedSelect_computable (fun _ : Word => treeCheck)
    (treeCheck_primrec.to_comp.comp Computable.snd)).comp
      (Computable.id.pair (descendants_primrec.to_comp.comp Computable.id hc))

theorem lookCheck_computable (h : Word → Nat) (hc : Computable h) : Computable (lookCheck h) :=
  Primrec.option_isSome.to_comp.comp (supplement_computable h hc)

theorem supplement_sound (h : Word → Nat) (s w : Word) (hw : supplement h s = some w) :
    BaseWitness h s w := by
  obtain ⟨hm, ht⟩ := (boundedSelect_spec treeCheck (descendants s (h s))).1 w hw
  obtain ⟨hp, hl⟩ := (mem_descendants_iff s w (h s)).mp hm
  exact ⟨hp, hl, ht⟩

theorem lookCheck_spec (h : Word → Nat) (s : Word) :
    lookCheck h s = true ↔ ∃ w, BaseWitness h s w := by
  unfold lookCheck supplement
  rw [(boundedSelect_spec treeCheck (descendants s (h s))).2]
  simp only [mem_descendants_iff, BaseWitness, diagonalTree]
  constructor
  · rintro ⟨w, ⟨hp, hl⟩, ht⟩; exact ⟨w, hp, hl, ht⟩
  · rintro ⟨w, hp, hl, ht⟩; exact ⟨w, ⟨hp, hl⟩, ht⟩

theorem lookCheck_zero (h : Word → Nat) (s : Word) (hz : h s = 0) :
    lookCheck h s = true ↔ diagonalTree s := by
  rw [lookCheck_spec]
  constructor
  · rintro ⟨w, hp, hl, ht⟩
    have he : s = w := hp.eq_of_length (by simpa [hz] using hl.symm)
    exact he ▸ ht
  · intro ht
    exact ⟨s, ⟨[], by simp⟩, by simp [hz], ht⟩

def takeWord (s : Word) (k : Nat) : Word :=
  (List.range (min k s.length)).map fun i => s.getD i false

theorem takeWord_primrec : Primrec₂ takeWord :=
  Primrec.list_map
    (Primrec.list_range.comp (Primrec.nat_min.comp Primrec.snd (Primrec.list_length.comp Primrec.fst)))
    ((Primrec.list_getD false).comp (Primrec.fst.comp Primrec.fst) Primrec.snd).to₂

theorem takeWord_eq_take (s : Word) (k : Nat) : takeWord s k = s.take k := by
  apply List.ext_getElem
  · simp [takeWord]
  · intro i hleft hright
    have hi : i < s.length := by simp [takeWord] at hleft; omega
    simp [takeWord, List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]

/-- All prefix lengths 0 through n, INCLUDING the final handoff, are checked. -/
def prefixScan (h : Word → Nat) (s : Word) : Nat → Bool
  | 0 => lookCheck h []
  | n + 1 => prefixScan h s n && lookCheck h (takeWord s (n + 1))

def lookaheadCheck (h : Word → Nat) (s : Word) : Bool :=
  treeCheck s && prefixScan h s s.length

def lookaheadTree (h : Word → Nat) (s : Word) : Prop := lookaheadCheck h s = true

theorem lookaheadCheck_computable (h : Word → Nat) (hc : Computable h) :
    Computable (lookaheadCheck h) := by
  have hlook := lookCheck_computable h hc
  have hstep : Computable fun p : Word × (Nat × Bool) =>
      p.2.2 && lookCheck h (takeWord p.1 (p.2.1 + 1)) :=
    Primrec.and.to_comp.comp (Computable.snd.comp Computable.snd)
      (hlook.comp (takeWord_primrec.to_comp.comp Computable.fst
        (Computable.succ.comp (Computable.fst.comp Computable.snd))))
  have hscan : Computable fun s => prefixScan h s s.length := by
    apply (Computable.nat_rec Computable.list_length (hlook.comp (Computable.const [])) hstep.to₂).of_eq
    intro s
    generalize s.length = n
    induction n with
    | zero => rfl
    | succ n ih => simpa only [prefixScan] using (congrArg
        (fun b => b && lookCheck h (takeWord s (n + 1))) ih)
  exact Primrec.and.to_comp.comp treeCheck_primrec.to_comp hscan

theorem prefixScan_spec (h : Word → Nat) (s : Word) (n : Nat) :
    prefixScan h s n = true ↔ ∀ k ≤ n, lookCheck h (takeWord s k) = true := by
  induction n with
  | zero => simp [prefixScan, takeWord]
  | succ n ih =>
    simp only [prefixScan, Bool.and_eq_true, ih]
    constructor
    · rintro ⟨hall, hlast⟩ k hk
      rcases Nat.le_succ_iff.mp hk with hk | rfl
      · exact hall k hk
      · exact hlast
    · intro hall
      exact ⟨fun k hk => hall k (Nat.le_succ_of_le hk), hall (n + 1) (Nat.le_refl _)⟩

theorem lookaheadTree_iff (h : Word → Nat) (s : Word) :
    lookaheadTree h s ↔ diagonalTree s ∧
      ∀ k ≤ s.length, lookCheck h (takeWord s k) = true := by
  simp [lookaheadTree, lookaheadCheck, diagonalTree, prefixScan_spec]

theorem takeWord_prefix_equal {s t : Word} (hp : s <+: t) (k : Nat) (hk : k ≤ s.length) :
    takeWord s k = takeWord t k := by
  simp only [takeWord_eq_take]
  calc
    s.take k = (t.take s.length).take k := congrArg (fun w : Word => w.take k)
      (List.prefix_iff_eq_take.mp hp)
    _ = t.take k := by simp [List.take_take, Nat.min_eq_left hk]

theorem lookahead_prefix_closed (h : Word → Nat) : PrefixClosed (lookaheadTree h) := by
  intro s t hp ht
  obtain ⟨htT, hlook⟩ := (lookaheadTree_iff h t).mp ht
  refine (lookaheadTree_iff h s).mpr ⟨diagonalTree_prefix_closed hp htT, ?_⟩
  intro k hk
  rw [takeWord_prefix_equal hp k hk]
  exact hlook k (le_trans hk hp.length_le)

theorem lookahead_subset (h : Word → Nat) (s : Word) (hs : lookaheadTree h s) : diagonalTree s :=
  ((lookaheadTree_iff h s).mp hs).1

theorem lookahead_path_iff (h : Word → Nat) (f : Nat → Bool) :
    (∀ n, lookaheadTree h (prefixWord f n)) ↔ ∀ n, diagonalTree (prefixWord f n) := by
  constructor
  · intro hf n; exact lookahead_subset h _ (hf n)
  · intro hf n
    refine (lookaheadTree_iff h _).mpr ⟨hf n, ?_⟩
    intro k hk
    have hkn : k ≤ n := by simpa using hk
    have htake : takeWord (prefixWord f n) k = prefixWord f k := by
      simp [takeWord_eq_take, prefixWord, ← List.map_take, List.take_range, Nat.min_eq_left hkn]
    rw [htake, lookCheck_spec]
    refine ⟨prefixWord f (k + h (prefixWord f k)), ?_, ?_, ?_⟩
    · exact Pruning.prefixWord_committed f k _ (by omega)
    · simp
    · exact hf _

theorem lookahead_mathematical_path (h : Word → Nat) :
    ∃ f : Nat → Bool, ∀ n, lookaheadTree h (prefixWord f n) := by
  obtain ⟨f, hf⟩ := exists_mathematical_path
  exact ⟨f, (lookahead_path_iff h f).mpr hf⟩

theorem lookahead_root (h : Word → Nat) : lookaheadTree h [] := by
  obtain ⟨f, hf⟩ := lookahead_mathematical_path h
  simpa [prefixWord] using hf 0

theorem lookaheadTree_all_prefixes_iff (h : Word → Nat) (s : Word) :
    lookaheadTree h s ↔ diagonalTree s ∧ ∀ t : Word, t <+: s → lookCheck h t = true := by
  rw [lookaheadTree_iff]
  constructor
  · rintro ⟨hs, hall⟩
    refine ⟨hs, ?_⟩
    intro t hp
    have ht := hall t.length hp.length_le
    have he : takeWord s t.length = t := by
      rw [takeWord_eq_take]
      exact (List.prefix_iff_eq_take.mp hp).symm
    exact he ▸ ht
  · rintro ⟨hs, hall⟩
    refine ⟨hs, ?_⟩
    intro k _
    apply hall (takeWord s k)
    rw [takeWord_eq_take]
    exact List.take_prefix _ _

end EffectiveRenewal.Lookahead
