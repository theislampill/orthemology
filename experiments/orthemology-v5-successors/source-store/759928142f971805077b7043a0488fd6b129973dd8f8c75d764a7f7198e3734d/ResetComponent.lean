import ProgressCuts

namespace PolicySynthesis
open EffectiveRenewal

/-! Each nonempty prefix of every reset block is checked. In particular the
coordinate just before a cut checks the entire completed preceding block. -/
def componentCheck (cut : Nat → Bool) (w : Word) : Bool :=
  allBelow (fun i => treeCheck (slice w (lastCut cut i) (i+1-lastCut cut i))) w.length

def componentTree (cut : Nat → Bool) (w : Word) : Prop := componentCheck cut w = true

theorem componentTree_iff (cut : Nat → Bool) (w : Word) : componentTree cut w ↔
    ∀ i < w.length, diagonalTree (slice w (lastCut cut i) (i+1-lastCut cut i)) := by
  simp only [componentTree, componentCheck, allBelow_iff, diagonalTree]

@[simp] theorem componentTree_empty (cut : Nat → Bool) : componentTree cut [] := by
  simp [componentTree_iff]

theorem component_completed_block {cut : Nat → Bool} {w : Word} (hw : componentTree cut w)
    {c : Nat} (hc : 0 < c) (hcl : c ≤ w.length) :
    diagonalTree (slice w (lastCut cut (c-1)) (c-lastCut cut (c-1))) := by
  have h := (componentTree_iff cut w).mp hw (c-1) (by omega)
  have he : c-1+1 = c := by omega
  simpa only [he] using h

theorem component_prefix_closed (cut : Nat → Bool) : PrefixClosed (componentTree cut) := by
  intro s t hp ht
  rw [componentTree_iff] at ht ⊢
  intro i hi
  have hb := lastCut_le cut i
  have he := slice_prefix_source hp (b := lastCut cut i) (m := i+1-lastCut cut i) (by omega)
  rw [he]
  exact ht i (hi.trans_le hp.length_le)

theorem componentCheck_primrec {α : Type} [Primcodable α] {cut : α → Nat → Bool}
    (hc : Primrec₂ cut) : Primrec₂ fun a w => componentCheck (cut a) w := by
  have hb : Primrec fun p : (α × Word) × Nat => lastCut (cut p.1.1) p.2 :=
    (lastCut_primrec hc).comp (Primrec.fst.comp Primrec.fst) Primrec.snd
  exact allBelow_primrec
    (treeCheck_primrec.comp (slice_primrec.comp
      ((Primrec.snd.comp Primrec.fst).pair
        (hb.pair (Primrec.nat_sub.comp (Primrec.succ.comp Primrec.snd) hb))))).to₂
    (Primrec.list_length.comp Primrec.snd)

/-! A complete K-plan is committed only after its block endpoint is observed.
The generator is primitive recursive even when no further cut will ever occur. -/
def blockSnapshots (cut : Nat → Bool) : Nat → Word
  | 0 => []
  | s+1 => if cut (s+1) = true then
      blockSnapshots cut s ++ finitePlan (s+1-lastCut cut s)
    else blockSnapshots cut s

theorem blockSnapshots_primrec {α : Type} [Primcodable α] {cut : α → Nat → Bool}
    (hc : Primrec₂ cut) : Primrec₂ fun a s => blockSnapshots (cut a) s := by
  have hn : Primrec fun p : α × (Nat × Word) => p.2.1 + 1 :=
    Primrec.succ.comp (Primrec.fst.comp Primrec.snd)
  have hl : Primrec fun p : α × (Nat × Word) => lastCut (cut p.1) p.2.1 :=
    (lastCut_primrec hc).comp Primrec.fst (Primrec.fst.comp Primrec.snd)
  have hrec := Primrec.nat_rec (Primrec.const ([] : Word))
    (Primrec.ite (Primrec.eq.comp (hc.comp Primrec.fst hn) (Primrec.const true))
      (Primrec.list_append.comp (Primrec.snd.comp Primrec.snd)
        (finitePlan_primrec.comp (Primrec.nat_sub.comp hn hl)))
      (Primrec.snd.comp Primrec.snd)).to₂
  apply hrec.of_eq
  intro a n
  induction n with
  | zero => rfl
  | succ n ih => simp [blockSnapshots, ih]

@[simp] theorem length_blockSnapshots (cut : Nat → Bool) (s : Nat) :
    (blockSnapshots cut s).length = lastCut cut s := by
  induction s with
  | zero => rfl
  | succ s ih =>
    rw [blockSnapshots, lastCut_succ]
    split_ifs <;> simp only [List.length_append, length_finitePlan, ih]
    have := lastCut_le cut s
    omega

theorem blockSnapshots_step_prefix (cut : Nat → Bool) (s : Nat) :
    blockSnapshots cut s <+: blockSnapshots cut (s+1) := by
  rw [blockSnapshots]
  split_ifs
  · exact List.prefix_append _ _
  · exact ⟨[], by simp⟩

theorem blockSnapshots_committed (cut : Nat → Bool) : Committed (blockSnapshots cut) := by
  intro s t hst
  induction t, hst using Nat.le_induction with
  | base => exact ⟨[], by simp⟩
  | succ t hst ih => exact ih.trans (blockSnapshots_step_prefix cut t)

theorem slice_zero_prefix (w : Word) {m : Nat} (hm : m ≤ w.length) :
    slice w 0 m <+: w := by
  apply prefix_of_getD (by simpa using hm)
  intro i hi
  have him : i < m := by simpa using hi
  rw [getD_slice _ _ him, Nat.zero_add]

theorem slice_append_boundary (s t : Word) (m : Nat) :
    slice (s ++ t) s.length m = slice t 0 m := by
  apply word_ext (by simp)
  intro i hi
  have him : i < m := by simpa using hi
  rw [getD_slice _ _ him, getD_slice _ _ him, Nat.zero_add]
  simp only [List.getD_eq_getElem?_getD,
    List.getElem?_append_right (Nat.le_add_right _ _), Nat.add_sub_cancel_left]

theorem blockSnapshots_admitted (cut : Nat → Bool) (h0 : cut 0 = true) (s : Nat) :
    componentTree cut (blockSnapshots cut s) := by
  induction s with
  | zero => exact componentTree_empty _
  | succ s ih =>
    rw [blockSnapshots]
    split_ifs with hc
    · rw [componentTree_iff]
      intro i hi
      have hb := lastCut_le cut s
      have hlen : (blockSnapshots cut s).length = lastCut cut s := length_blockSnapshots cut s
      have hin : i < s+1 := by
        simp only [List.length_append, length_finitePlan, hlen] at hi
        omega
      by_cases hib : i < lastCut cut s
      · have hp := (componentTree_iff _ _).mp ih i (by simpa using hib)
        have hstart := lastCut_le cut i
        rw [← slice_prefix_source (List.prefix_append (blockSnapshots cut s)
          (finitePlan (s+1-lastCut cut s))) (b := lastCut cut i)
          (m := i+1-lastCut cut i) (by omega)]
        exact hp
      · have he : lastCut cut i = lastCut cut s :=
          lastCut_same_interval h0 (by omega) (by omega)
        rw [he, ← hlen, slice_append_boundary]
        apply diagonalTree_prefix_closed (slice_zero_prefix _ _) (finitePlan_admitted _)
        rw [length_finitePlan, hlen]
        omega
    · exact ih

theorem unboundedCuts_component_path (cut : Nat → Bool) (hc : Primrec cut)
    (h0 : cut 0 = true) (hu : ∀ N, ∃ c, N < c ∧ cut c = true) :
    HasComputablePath (componentTree cut) := by
  have hcu : Primrec₂ fun (_ : Unit) i => cut i := hc.comp Primrec.snd
  have hsc : Computable (blockSnapshots cut) :=
    ((blockSnapshots_primrec hcu).comp (Primrec.const ()) Primrec.id).to_comp
  apply committed_path_extraction (componentTree cut) (component_prefix_closed cut)
    (blockSnapshots cut) hsc (blockSnapshots_committed cut) _ (blockSnapshots_admitted cut h0)
  intro n
  obtain ⟨c, hnc, hc⟩ := hu n
  refine ⟨c, ?_⟩
  rw [length_blockSnapshots]
  exact hnc.le.trans (le_lastCut le_rfl hc)

theorem eventuallyLastCut_no_component_path (cut : Nat → Bool)
    (h : ∃ b, ∀ i, b ≤ i → lastCut cut i = b) : ¬ HasComputablePath (componentTree cut) := by
  rintro ⟨f, hf, hp⟩
  obtain ⟨b, hb⟩ := h
  let g : Nat → Bool := fun i => f (b+i)
  have hg : Computable g := hf.comp (Primrec.nat_add.comp (Primrec.const b) Primrec.id).to_comp
  apply no_computable_path g hg
  intro m
  cases m with
  | zero => exact diagonalTree_empty
  | succ k =>
    have hu := (componentTree_iff _ _).mp (hp (b+(k+1))) (b+k) (by simp)
    rw [hb (b+k) (by omega)] at hu
    have he : b+k+1-b = k+1 := by omega
    rw [he, slice_prefixWord f (by omega)] at hu
    exact hu

theorem component_computablePath_iff (p x : Nat) :
    HasComputablePath (componentTree (progressCut (p,x))) ↔ rowTotal p x := by
  classical
  constructor
  · intro h
    by_contra hn
    obtain ⟨b, hb, ht⟩ := not_rowTotal_eventually_lastCut hn
    exact eventuallyLastCut_no_component_path _ ⟨b, ht⟩ h
  · intro h
    exact unboundedCuts_component_path _
      (progressCut_primrec.comp (Primrec.const (p,x)) Primrec.id)
      (progressCut_zero _) ((rowTotal_iff_unbounded_cuts p x).mp h)

end PolicySynthesis
