import CommittedOutput

/-! An exact effective witness criterion. Enumeration is computational data;
rootedness, containment and pruning are mathematical obligations on its range.
No procedure deciding those obligations from arbitrary source code is asserted. -/

namespace EffectiveRenewal.Pruning

open Encodable

def RootedPruned (R : Word → Prop) : Prop :=
  R [] ∧ PrefixClosed R ∧ ∀ s, R s → ∃ b : Bool, R (s ++ [b])

def Enumerable (R : Word → Prop) : Prop :=
  ∃ enum : Nat → Option Word, Computable enum ∧ ∀ s, R s ↔ ∃ n, enum n = some s

def ComputablyDecidable (R : Word → Prop) : Prop :=
  ∃ test : Word → Bool, Computable test ∧ ∀ s, test s = true ↔ R s

def Child (s w : Word) : Prop := w = s ++ [false] ∨ w = s ++ [true]

instance (s w : Word) : Decidable (Child s w) := by
  unfold Child
  infer_instance

def childCheck (s w : Word) : Bool := decide (Child s w)

theorem childCheck_primrec : Primrec₂ childCheck := by
  exact (Primrec.eq.comp Primrec.snd
      (Primrec.list_concat.comp Primrec.fst (Primrec.const false))).or
    (Primrec.eq.comp Primrec.snd
      (Primrec.list_concat.comp Primrec.fst (Primrec.const true)))

def childCandidate (enum : Nat → Option Word) (s : Word) (time : Nat) : Option Word :=
  (enum time).bind fun w => cond (childCheck s w) (some w) none

theorem childCandidate_computable (enum : Nat → Option Word) (hc : Computable enum) :
    Computable₂ (childCandidate enum) := by
  exact Computable.option_bind (hc.comp Computable.snd)
    (Computable.cond
      (childCheck_primrec.to_comp.comp (Computable.fst.comp Computable.fst) Computable.snd)
      (Computable.option_some.comp Computable.snd) (Computable.const none)).to₂

theorem childCandidate_spec (enum : Nat → Option Word) (s w : Word) (time : Nat) :
    w ∈ childCandidate enum s time ↔ enum time = some w ∧ Child s w := by
  simp [childCandidate, childCheck, Option.bind_eq_some_iff, Bool.cond_decide]

def nextChild (enum : Nat → Option Word) (s : Word) : Part Word :=
  Nat.rfindOpt (childCandidate enum s)

theorem nextChild_partrec (enum : Nat → Option Word) (hc : Computable enum) :
    Partrec (nextChild enum) := Partrec.rfindOpt (childCandidate_computable enum hc)

theorem nextChild_spec (enum : Nat → Option Word) (s w : Word)
    (hw : w ∈ nextChild enum s) : (∃ time, enum time = some w) ∧ Child s w := by
  obtain ⟨time, ht⟩ := Nat.rfindOpt_spec hw
  obtain ⟨he, hchild⟩ := (childCandidate_spec enum s w time).mp ht
  exact ⟨⟨time, he⟩, hchild⟩

theorem nextChild_good (R : Word → Prop) (enum : Nat → Option Word)
    (he : ∀ s, R s ↔ ∃ time, enum time = some s)
    (hp : ∀ s, R s → ∃ b : Bool, R (s ++ [b])) (s : Word) (hs : R s) :
    ∃ w, w ∈ nextChild enum s ∧ R w ∧ Child s w := by
  obtain ⟨b, hb⟩ := hp s hs
  obtain ⟨time, ht⟩ := (he _).mp hb
  have hchild : Child s (s ++ [b]) := by cases b <;> simp [Child]
  have hd : (nextChild enum s).Dom :=
    Nat.rfindOpt_dom.mpr ⟨time, s ++ [b], (childCandidate_spec _ _ _ _).mpr ⟨ht, hchild⟩⟩
  let w := (nextChild enum s).get hd
  have hw : w ∈ nextChild enum s := Part.get_mem _
  have hspec := nextChild_spec enum s w hw
  exact ⟨w, hw, (he _).mpr hspec.1, hspec.2⟩

def enumRun (enum : Nat → Option Word) : Nat → Part Word
  | 0 => Part.some []
  | n + 1 => (enumRun enum n).bind (nextChild enum)

theorem enumRun_partrec (enum : Nat → Option Word) (hc : Computable enum) :
    Partrec (enumRun enum) := by
  have h := Partrec.nat_rec Computable.id (Computable.const ([] : Word)).partrec
    ((nextChild_partrec enum hc).comp (Computable.snd.comp Computable.snd)).to₂
  apply h.of_eq
  intro n
  induction n with
  | zero => rfl
  | succ n ih => simpa [enumRun] using congrArg (fun x : Part Word => x.bind (nextChild enum)) ih

theorem enumRun_good (R : Word → Prop) (enum : Nat → Option Word)
    (he : ∀ s, R s ↔ ∃ time, enum time = some s) (hp : RootedPruned R) (n : Nat) :
    ∃ s, s ∈ enumRun enum n ∧ R s ∧ s.length = n := by
  induction n with
  | zero => exact ⟨[], Part.mem_some _, hp.1, rfl⟩
  | succ n ih =>
    obtain ⟨s, hs, hRs, hlen⟩ := ih
    obtain ⟨w, hw, hRw, hchild⟩ := nextChild_good R enum he hp.2.2 s hRs
    refine ⟨w, ?_, hRw, ?_⟩
    · exact Part.mem_bind_iff.mpr ⟨s, hs, hw⟩
    · rcases hchild with rfl | rfl <;> simp [hlen]

theorem child_prefix {s w : Word} (h : Child s w) : s <+: w := by
  rcases h with rfl | rfl <;> exact ⟨_, rfl⟩

theorem enumerable_pruned_extracts_path (T R : Word → Prop)
    (hsub : ∀ s, R s → T s) (hp : RootedPruned R) (he : Enumerable R) :
    ∃ f : Nat → Bool, Computable f ∧ ∀ n, T (prefixWord f n) := by
  obtain ⟨enum, hc, he⟩ := he
  have hd : ∀ n, (enumRun enum n).Dom := fun n =>
    (enumRun_good R enum he hp n).choose_spec.1.1
  let snap : Nat → Word := fun n => (enumRun enum n).get (hd n)
  have hmem : ∀ n, snap n ∈ enumRun enum n := fun n => Part.get_mem _
  have hsnap : Computable snap := (enumRun_partrec enum hc).of_eq_tot hmem
  have hgood : ∀ n, R (snap n) ∧ (snap n).length = n := by
    intro n
    obtain ⟨s, hs, hRs, hlen⟩ := enumRun_good R enum he hp n
    have hsame := Part.mem_unique hs (hmem n)
    exact hsame ▸ ⟨hRs, hlen⟩
  have hnext : ∀ n, snap n <+: snap (n + 1) := by
    intro n
    have h := hmem (n + 1)
    obtain ⟨s, hs, hw⟩ := Part.mem_bind_iff.mp h
    have heq := Part.mem_unique hs (hmem n)
    subst s
    exact child_prefix (nextChild_spec enum (snap n) (snap (n + 1)) hw).2
  have hm : Committed snap := by
    intro s t hst
    induction t, hst using Nat.le_induction with
    | base => exact ⟨[], by simp⟩
    | succ t hst ih => exact ih.trans (hnext t)
  have hu : UnboundedOutput snap := fun n => ⟨n, (hgood n).2.ge⟩
  obtain ⟨f, hf, hpath⟩ := committed_path_extraction R hp.2.1 snap hsnap hm hu
    (fun n => (hgood n).1)
  exact ⟨f, hf, fun n => hsub _ (hpath n)⟩

theorem prefixWord_succ (f : Nat → Bool) (n : Nat) :
    prefixWord f (n + 1) = prefixWord f n ++ [f n] := by
  simp [prefixWord, List.range_succ]

theorem prefixWord_computable (f : Nat → Bool) (hf : Computable f) :
    Computable (prefixWord f) := by
  have h := Computable.nat_rec Computable.id (Computable.const ([] : Word))
    (Computable.list_concat.comp (Computable.snd.comp Computable.snd)
      (hf.comp (Computable.fst.comp Computable.snd))).to₂
  apply h.of_eq
  intro n
  induction n with
  | zero => rfl
  | succ n ih => simpa [prefixWord_succ] using congrArg (fun w : Word => w ++ [f n]) ih

def pathPrefixes (f : Nat → Bool) (s : Word) : Prop := s = prefixWord f s.length

theorem pathPrefixes_rooted_pruned (f : Nat → Bool) : RootedPruned (pathPrefixes f) := by
  refine ⟨?_, ?_, ?_⟩
  · simp [pathPrefixes, prefixWord]
  · intro s t hpre ht
    change s = prefixWord f s.length
    calc
      s = t.take s.length := List.prefix_iff_eq_take.mp hpre
      _ = (prefixWord f t.length).take s.length := congrArg (fun w : Word => w.take s.length) ht
      _ = prefixWord f s.length := by simp [prefixWord, ← List.map_take, List.take_range, Nat.min_eq_left hpre.length_le]
  · intro s hs
    refine ⟨f s.length, ?_⟩
    change s ++ [f s.length] = prefixWord f (s ++ [f s.length]).length
    simpa [prefixWord_succ] using congrArg (fun w : Word => w ++ [f s.length]) hs

theorem pathPrefixes_decidable (f : Nat → Bool) (hf : Computable f) :
    ComputablyDecidable (pathPrefixes f) := by
  refine ⟨fun s => decide (s = prefixWord f s.length), ?_, ?_⟩
  · exact Primrec.eq.to_comp.comp Computable.id
      ((prefixWord_computable f hf).comp Computable.list_length)
  · intro s; simp [pathPrefixes]

def filteredDecode (test : Word → Bool) (n : Nat) : Option Word :=
  (decode (α := Word) n).bind fun s => cond (test s) (some s) none

theorem filteredDecode_computable (test : Word → Bool) (hc : Computable test) :
    Computable (filteredDecode test) := by
  exact Computable.option_bind Computable.decode
    (Computable.cond (hc.comp Computable.snd)
      (Computable.option_some.comp Computable.snd) (Computable.const none)).to₂

theorem filteredDecode_spec (test : Word → Bool) (n : Nat) (s : Word) :
    filteredDecode test n = some s ↔ decode (α := Word) n = some s ∧ test s = true := by
  simp [filteredDecode, Option.bind_eq_some_iff, Bool.cond_eq_ite]

theorem decidable_enumerable (R : Word → Prop) (hd : ComputablyDecidable R) : Enumerable R := by
  obtain ⟨test, hc, ht⟩ := hd
  refine ⟨filteredDecode test, filteredDecode_computable test hc, ?_⟩
  intro s
  constructor
  · intro hs
    exact ⟨encode s, (filteredDecode_spec test (encode s) s).mpr ⟨encodek s, (ht s).mpr hs⟩⟩
  · rintro ⟨n, hn⟩
    exact (ht s).mp ((filteredDecode_spec test n s).mp hn).2

theorem computable_path_iff_decidable_pruned (T : Word → Prop) :
    (∃ f : Nat → Bool, Computable f ∧ ∀ n, T (prefixWord f n)) ↔
    ∃ R : Word → Prop, (∀ s, R s → T s) ∧ RootedPruned R ∧ ComputablyDecidable R := by
  constructor
  · rintro ⟨f, hf, hpath⟩
    refine ⟨pathPrefixes f, ?_, pathPrefixes_rooted_pruned f, pathPrefixes_decidable f hf⟩
    intro s hs
    exact hs ▸ hpath s.length
  · rintro ⟨R, hsub, hp, hd⟩
    exact enumerable_pruned_extracts_path T R hsub hp (decidable_enumerable R hd)

theorem computable_path_iff_enumerable_pruned (T : Word → Prop) :
    (∃ f : Nat → Bool, Computable f ∧ ∀ n, T (prefixWord f n)) ↔
    ∃ R : Word → Prop, (∀ s, R s → T s) ∧ RootedPruned R ∧ Enumerable R := by
  constructor
  · intro h
    obtain ⟨R, hsub, hp, hd⟩ := (computable_path_iff_decidable_pruned T).mp h
    exact ⟨R, hsub, hp, decidable_enumerable R hd⟩
  · rintro ⟨R, hsub, hp, he⟩
    exact enumerable_pruned_extracts_path T R hsub hp he

theorem diagonal_no_enumerable_pruned :
    ¬ ∃ R : Word → Prop, (∀ s, R s → diagonalTree s) ∧ RootedPruned R ∧ Enumerable R := by
  intro h
  obtain ⟨f, hf, hpath⟩ := (computable_path_iff_enumerable_pruned diagonalTree).mpr h
  exact no_computable_path f hf hpath

theorem diagonal_computably_decidable : ComputablyDecidable diagonalTree :=
  ⟨treeCheck, treeCheck_primrec.to_comp, fun _ => Iff.rfl⟩

theorem diagonal_not_rooted_pruned : ¬ RootedPruned diagonalTree := by
  intro hp
  exact diagonal_no_enumerable_pruned
    ⟨diagonalTree, fun _ h => h, hp, decidable_enumerable _ diagonal_computably_decidable⟩

theorem prefixWord_committed (f : Nat → Bool) : Committed (prefixWord f) := by
  intro m n hmn
  apply List.prefix_iff_eq_take.mpr
  simp [prefixWord, ← List.map_take, List.take_range, Nat.min_eq_left hmn]

theorem finitePlans_not_committed : ¬ Committed finitePlan := by
  intro hm
  exact no_effective_committed_renewal finitePlan finitePlan_primrec.to_comp hm
    finitePlan_admitted (fun n => ⟨n, by simp⟩)

end EffectiveRenewal.Pruning
