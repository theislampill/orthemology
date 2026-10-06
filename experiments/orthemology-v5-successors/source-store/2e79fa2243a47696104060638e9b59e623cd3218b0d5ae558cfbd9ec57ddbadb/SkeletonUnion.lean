import ResetComponent

namespace PolicySynthesis
open EffectiveRenewal

/-! The permanent exit marker occupies a control position, never a data
position. Bounded obligations stop after the first true control bit. -/
def skeletonWord (w : Word) (x : Nat) : Word :=
  (List.range x).map fun i => w.getD (2*i+1) false

def controlsClear (w : Word) (x : Nat) : Bool :=
  allBelow (fun i => !(w.getD (2*i) false)) x

@[simp] theorem length_skeletonWord (w : Word) (x : Nat) :
    (skeletonWord w x).length = x := by simp [skeletonWord]

@[simp] theorem getD_skeletonWord (w : Word) {x i : Nat} (hi : i < x) :
    (skeletonWord w x).getD i false = w.getD (2*i+1) false := by
  simp [skeletonWord, List.getD_eq_getElem?_getD, List.getElem?_range hi]

theorem controlsClear_iff (w : Word) (x : Nat) :
    controlsClear w x = true ↔ ∀ i < x, w.getD (2*i) false = false := by
  simp [controlsClear]

def synthesisClause (p : Nat) (w : Word) (x : Nat) : Bool :=
  (if 2*x ≤ w.length ∧ controlsClear w x = true then treeCheck (skeletonWord w x) else true) &&
  (if 2*x < w.length ∧ controlsClear w x = true ∧ w.getD (2*x) false = true then
    componentCheck (progressCut (p,x)) (slice w (2*x+1) (w.length-(2*x+1))) else true)

def synthesisCheck (p : Nat) (w : Word) : Bool :=
  allBelow (synthesisClause p w) (w.length+1)

def synthesisTree (p : Nat) (w : Word) : Prop := synthesisCheck p w = true

theorem synthesisClause_iff (p : Nat) (w : Word) (x : Nat) :
    synthesisClause p w x = true ↔
    (2*x ≤ w.length → controlsClear w x = true → diagonalTree (skeletonWord w x)) ∧
    (2*x < w.length → controlsClear w x = true → w.getD (2*x) false = true →
      componentTree (progressCut (p,x)) (slice w (2*x+1) (w.length-(2*x+1)))) := by
  have hif (P : Prop) [Decidable P] (b : Bool) :
      (if P then b else true) = true ↔ (P → b = true) := by
    by_cases h : P <;> simp [h]
  simp only [synthesisClause, Bool.and_eq_true, hif, diagonalTree, componentTree]
  tauto

theorem synthesisTree_iff (p : Nat) (w : Word) : synthesisTree p w ↔
    (∀ x, 2*x ≤ w.length → controlsClear w x = true → diagonalTree (skeletonWord w x)) ∧
    (∀ x, 2*x < w.length → controlsClear w x = true → w.getD (2*x) false = true →
      componentTree (progressCut (p,x)) (slice w (2*x+1) (w.length-(2*x+1)))) := by
  change allBelow (synthesisClause p w) (w.length+1) = true ↔ _
  rw [allBelow_iff]
  constructor
  · intro h
    constructor
    · intro x hx hc
      exact ((synthesisClause_iff p w x).mp (h x (by omega))).1 hx hc
    · intro x hx hc hb
      exact ((synthesisClause_iff p w x).mp (h x (by omega))).2 hx hc hb
  · rintro ⟨h1,h2⟩ x hx
    exact (synthesisClause_iff p w x).mpr ⟨h1 x, h2 x⟩

theorem skeletonWord_primrec : Primrec₂ skeletonWord := by
  exact Primrec.list_map (Primrec.list_range.comp Primrec.snd)
    ((Primrec.list_getD false).comp (Primrec.fst.comp Primrec.fst)
      (Primrec.nat_double_succ.comp Primrec.snd)).to₂

theorem controlsClear_primrec : Primrec₂ controlsClear := by
  exact allBelow_primrec
    (Primrec.not.comp ((Primrec.list_getD false).comp (Primrec.fst.comp Primrec.fst)
      (Primrec.nat_double.comp Primrec.snd))).to₂ Primrec.snd

theorem synthesisCheck_primrec : Primrec₂ synthesisCheck := by
  have hp : Primrec fun a : (Nat × Word) × Nat => a.1.1 := Primrec.fst.comp Primrec.fst
  have hw : Primrec fun a : (Nat × Word) × Nat => a.1.2 := Primrec.snd.comp Primrec.fst
  have hx : Primrec fun a : (Nat × Word) × Nat => a.2 := Primrec.snd
  have hlen := Primrec.list_length.comp hw
  have htwo := Primrec.nat_double.comp hx
  have hclear := controlsClear_primrec.comp hw hx
  have hskeleton := treeCheck_primrec.comp (skeletonWord_primrec.comp hw hx)
  have htail := slice_primrec.comp (hw.pair
    ((Primrec.succ.comp htwo).pair (Primrec.nat_sub.comp hlen (Primrec.succ.comp htwo))))
  have hcomponent := (componentCheck_primrec progressCut_primrec).comp (hp.pair hx) htail
  have hclause : Primrec fun a : (Nat × Word) × Nat => synthesisClause a.1.1 a.1.2 a.2 :=
    Primrec.and.comp
      (Primrec.ite (PrimrecPred.and (Primrec.nat_le.comp htwo hlen)
        (Primrec.eq.comp hclear (Primrec.const true))) hskeleton (Primrec.const true))
      (Primrec.ite (PrimrecPred.and (Primrec.nat_lt.comp htwo hlen)
        (PrimrecPred.and (Primrec.eq.comp hclear (Primrec.const true))
          (Primrec.eq.comp ((Primrec.list_getD false).comp hw htwo) (Primrec.const true))))
        hcomponent (Primrec.const true))
  exact allBelow_primrec hclause.to₂ (Primrec.succ.comp (Primrec.list_length.comp Primrec.snd))

@[simp] theorem synthesisTree_empty (p : Nat) : synthesisTree p [] := by
  rw [synthesisTree_iff]
  constructor
  · intro x hx hc
    have : x = 0 := by simp at hx; omega
    subst x
    exact diagonalTree_empty
  · intro x hx
    simp at hx

theorem skeletonWord_prefix_source {s t : Word} (hp : s <+: t) {x : Nat}
    (hx : 2*x ≤ s.length) : skeletonWord s x = skeletonWord t x := by
  apply word_ext (by simp)
  intro i hi
  have hix : i < x := by simpa using hi
  rw [getD_skeletonWord _ hix, getD_skeletonWord _ hix]
  exact getD_of_prefix hp (by omega)

theorem controlsClear_prefix_source {s t : Word} (hp : s <+: t) {x : Nat}
    (hx : 2*x ≤ s.length) : controlsClear s x = controlsClear t x := by
  apply Bool.eq_iff_iff.mpr
  rw [controlsClear_iff, controlsClear_iff]
  constructor
  · intro h i hi
    rw [← getD_of_prefix hp (by omega)]
    exact h i hi
  · intro h i hi
    rw [getD_of_prefix hp (by omega)]
    exact h i hi

theorem suffix_prefix_source {s t : Word} (hp : s <+: t) {b : Nat} (hb : b ≤ s.length) :
    slice s b (s.length-b) <+: slice t b (t.length-b) := by
  rw [slice_prefix_source hp (by omega)]
  exact slice_prefix _ _ (Nat.sub_le_sub_right hp.length_le _)

theorem synthesis_prefix_closed (p : Nat) : PrefixClosed (synthesisTree p) := by
  intro s t hp ht
  rw [synthesisTree_iff] at ht ⊢
  constructor
  · intro x hx hc
    rw [skeletonWord_prefix_source hp hx]
    apply ht.1 x (hx.trans hp.length_le)
    rwa [← controlsClear_prefix_source hp hx]
  · intro x hx hc hb
    apply component_prefix_closed _ (suffix_prefix_source hp (by omega))
    apply ht.2 x (hx.trans_le hp.length_le)
    · rwa [← controlsClear_prefix_source hp hx.le]
    · rwa [← getD_of_prefix hp hx]


theorem skeletonWord_prefixWord (f : Nat → Bool) {n x : Nat} (hx : 2*x ≤ n) :
    skeletonWord (prefixWord f n) x = prefixWord (fun i => f (2*i+1)) x := by
  apply word_ext (by simp)
  intro i hi
  have hix : i < x := by simpa using hi
  rw [getD_skeletonWord _ hix, getD_prefixWord _ (by omega), getD_prefixWord _ hix]

theorem controlsClear_prefixWord (f : Nat → Bool) {n x : Nat} (hx : 2*x ≤ n) :
    controlsClear (prefixWord f n) x = true ↔ ∀ i < x, f (2*i) = false := by
  rw [controlsClear_iff]
  constructor <;> intro h i hi
  · have h' := h i hi
    rwa [getD_prefixWord _ (by omega)] at h'
  · rw [getD_prefixWord _ (by omega)]
    exact h i hi

def pairEncode (f : Nat → Bool) (n : Nat) : Bool :=
  if n % 2 = 0 then false else f (n / 2)

@[simp] theorem pairEncode_even (f : Nat → Bool) (i : Nat) : pairEncode f (2*i) = false := by
  simp [pairEncode]

@[simp] theorem pairEncode_odd (f : Nat → Bool) (i : Nat) : pairEncode f (2*i+1) = f i := by
  have hm : (2*i+1)%2 = 1 := by omega
  have hd : (2*i+1)/2 = i := by omega
  simp [pairEncode, hm, hd]

theorem pairEncode_path (p : Nat) (f : Nat → Bool)
    (hf : ∀ n, diagonalTree (prefixWord f n)) :
    ∀ n, synthesisTree p (prefixWord (pairEncode f) n) := by
  intro n
  rw [synthesisTree_iff]
  constructor
  · intro x hx hc
    have hxn : 2*x ≤ n := by simpa using hx
    rw [skeletonWord_prefixWord _ hxn]
    simpa using hf x
  · intro x hx hc hb
    have hxn : 2*x < n := by simpa using hx
    rw [getD_prefixWord _ hxn, pairEncode_even] at hb
    contradiction

theorem synthesis_mathematical_path (p : Nat) :
    ∃ f : Nat → Bool, ∀ n, synthesisTree p (prefixWord f n) := by
  obtain ⟨f, hf⟩ := exists_mathematical_path
  exact ⟨pairEncode f, pairEncode_path p f hf⟩

theorem neverExit_decodes_K {p : Nat} {f : Nat → Bool}
    (hf : ∀ n, synthesisTree p (prefixWord f n))
    (hz : ∀ i, f (2*i) = false) :
    ∀ n, diagonalTree (prefixWord (fun i => f (2*i+1)) n) := by
  intro n
  have h := (synthesisTree_iff p _).mp (hf (2*n))
  have hc : controlsClear (prefixWord f (2*n)) n = true :=
    (controlsClear_prefixWord f le_rfl).mpr (fun i _ => hz i)
  have hk := h.1 n (by simp) hc
  rwa [skeletonWord_prefixWord f le_rfl] at hk

theorem exit_tail_component {p x : Nat} {f : Nat → Bool}
    (hf : ∀ n, synthesisTree p (prefixWord f n))
    (hx : f (2*x) = true) (hearlier : ∀ i < x, f (2*i) = false) :
    ∀ m, componentTree (progressCut (p,x)) (prefixWord (fun i => f (2*x+1+i)) m) := by
  intro m
  have h := (synthesisTree_iff p _).mp (hf (2*x+1+m))
  have hc : controlsClear (prefixWord f (2*x+1+m)) x = true :=
    (controlsClear_prefixWord f (by omega)).mpr hearlier
  have hu := h.2 x (by simp; omega) hc (by rw [getD_prefixWord _ (by omega)]; exact hx)
  simp only [length_prefixWord] at hu
  have he : 2*x+1+m-(2*x+1) = m := by omega
  rw [he, slice_prefixWord f (by omega)] at hu
  exact hu

theorem synthesis_path_has_total_row {p : Nat} (h : HasComputablePath (synthesisTree p)) :
    ∃ x, rowTotal p x := by
  classical
  obtain ⟨f, hf, hp⟩ := h
  by_cases hexit : ∃ x, f (2*x) = true
  · let x := Nat.find hexit
    have hx : f (2*x) = true := Nat.find_spec hexit
    have hearlier : ∀ i < x, f (2*i) = false := by
      intro i hi
      have hn := Nat.find_min hexit hi
      cases hb : f (2*i) <;> simp_all
    refine ⟨x, (component_computablePath_iff p x).mp ?_⟩
    refine ⟨fun i => f (2*x+1+i), ?_, exit_tail_component hp hx hearlier⟩
    exact hf.comp (Primrec.nat_add.comp (Primrec.const (2*x+1)) Primrec.id).to_comp
  · have hz : ∀ i, f (2*i) = false := by
      intro i
      have hn : f (2*i) ≠ true := fun hi => hexit ⟨i,hi⟩
      cases hb : f (2*i) <;> simp_all
    have hd : Computable fun i => f (2*i+1) := hf.comp Primrec.nat_double_succ.to_comp
    exact False.elim (no_computable_path _ hd (neverExit_decodes_K hp hz))


/-! A finite admitted skeleton followed by one permanent exit and a component
path. The programme hardcodes only the finite skeleton word. -/
def exitPath (σ : Word) (g : Nat → Bool) (n : Nat) : Bool :=
  if n < 2*σ.length then pairEncode (fun i => σ.getD i false) n
  else if n = 2*σ.length then true else g (n-(2*σ.length+1))

theorem pairEncode_computable (f : Nat → Bool) (hf : Computable f) :
    Computable (pairEncode f) := by
  have h := Computable.cond
    (Primrec.eq.comp (Primrec.nat_mod.comp Primrec.id (Primrec.const 2)) (Primrec.const 0)).to_comp
    (Computable.const false)
    (hf.comp (Primrec.nat_div.comp Primrec.id (Primrec.const 2)).to_comp)
  apply h.of_eq
  intro n
  by_cases hn : n%2 = 0 <;> simp [pairEncode, hn]

theorem exitPath_computable (σ : Word) (g : Nat → Bool) (hg : Computable g) :
    Computable (exitPath σ g) := by
  have hh := pairEncode_computable (fun i => σ.getD i false)
    ((Primrec.list_getD false).comp (Primrec.const σ) Primrec.id).to_comp
  have ht := hg.comp (Primrec.nat_sub.comp Primrec.id (Primrec.const (2*σ.length+1))).to_comp
  have h := Computable.cond
    (Primrec.nat_lt.comp Primrec.id (Primrec.const (2*σ.length))).to_comp hh
    (Computable.cond (Primrec.eq.comp Primrec.id (Primrec.const (2*σ.length))).to_comp
      (Computable.const true) ht)
  apply h.of_eq
  intro n
  by_cases hn : n < 2*σ.length <;> by_cases he : n = 2*σ.length <;> simp [exitPath, hn, he]

@[simp] theorem exitPath_even_before (σ : Word) (g : Nat → Bool) {i : Nat}
    (hi : i < σ.length) : exitPath σ g (2*i) = false := by
  simp [exitPath, show 2*i < 2*σ.length by omega]

@[simp] theorem exitPath_odd_before (σ : Word) (g : Nat → Bool) {i : Nat}
    (hi : i < σ.length) : exitPath σ g (2*i+1) = σ.getD i false := by
  simp [exitPath, show 2*i+1 < 2*σ.length by omega]

@[simp] theorem exitPath_exit (σ : Word) (g : Nat → Bool) :
    exitPath σ g (2*σ.length) = true := by simp [exitPath]

@[simp] theorem exitPath_tail (σ : Word) (g : Nat → Bool) (i : Nat) :
    exitPath σ g (2*σ.length+1+i) = g i := by
  simp [exitPath, show ¬ 2*σ.length+1+i < 2*σ.length by omega,
    show 2*σ.length+1+i ≠ 2*σ.length by omega]

theorem exitPath_clear_bound (σ : Word) (g : Nat → Bool) {n x : Nat}
    (hx : 2*x ≤ n) (hc : controlsClear (prefixWord (exitPath σ g) n) x = true) :
    x ≤ σ.length := by
  by_contra h
  have he := (controlsClear_prefixWord _ hx).mp hc σ.length (by omega)
  simp at he

theorem exitPath_skeleton (σ : Word) (g : Nat → Bool) {n x : Nat}
    (hx : 2*x ≤ n) (hxs : x ≤ σ.length) :
    skeletonWord (prefixWord (exitPath σ g) n) x = slice σ 0 x := by
  apply word_ext (by simp)
  intro i hi
  have hix : i < x := by simpa using hi
  rw [getD_skeletonWord _ hix, getD_prefixWord _ (by omega),
    getD_slice _ _ hix, Nat.zero_add, exitPath_odd_before _ _ (by omega)]

theorem exitPath_suffix (σ : Word) (g : Nat → Bool) {n : Nat} (hn : 2*σ.length+1 ≤ n) :
    slice (prefixWord (exitPath σ g) n) (2*σ.length+1) (n-(2*σ.length+1)) =
      prefixWord g (n-(2*σ.length+1)) := by
  rw [slice_prefixWord _ (by omega)]
  congr 1
  funext i
  exact exitPath_tail σ g i

theorem exitPath_admitted {p : Nat} (σ : Word) (hσ : diagonalTree σ) (g : Nat → Bool)
    (hg : ∀ m, componentTree (progressCut (p,σ.length)) (prefixWord g m)) :
    ∀ n, synthesisTree p (prefixWord (exitPath σ g) n) := by
  intro n
  rw [synthesisTree_iff]
  constructor
  · intro x hx hc
    have hxn : 2*x ≤ n := by simpa using hx
    have hxs := exitPath_clear_bound σ g hxn hc
    rw [exitPath_skeleton σ g hxn hxs]
    exact diagonalTree_prefix_closed (slice_zero_prefix σ hxs) hσ
  · intro x hx hc hb
    have hxn : 2*x < n := by simpa using hx
    have hxs := exitPath_clear_bound σ g hxn.le hc
    have he : x = σ.length := by
      by_contra hne
      have hlt : x < σ.length := by omega
      rw [getD_prefixWord _ hxn, exitPath_even_before σ g hlt] at hb
      contradiction
    subst x
    simp only [length_prefixWord]
    rw [exitPath_suffix σ g (by omega)]
    exact hg _

theorem synthesis_computablePath_iff (p : Nat) :
    HasComputablePath (synthesisTree p) ↔ ∃ x, rowTotal p x := by
  constructor
  · exact synthesis_path_has_total_row
  · rintro ⟨x, hx⟩
    obtain ⟨g, hg, hp⟩ := (component_computablePath_iff p x).mpr hx
    refine ⟨exitPath (finitePlan x) g, exitPath_computable _ _ hg, ?_⟩
    apply exitPath_admitted _ (finitePlan_admitted x) g
    simpa using hp


/-- Once the root exit marker is read, every remaining bit is component data.
In particular later true bits are not reparsed as control markers. -/
theorem synthesis_root_exit_iff (p : Nat) (τ : Word) :
    synthesisTree p (true :: τ) ↔ componentTree (progressCut (p,0)) τ := by
  have htail : slice (true :: τ) 1 τ.length = τ := by
    change slice ([true] ++ τ) [true].length τ.length = τ
    rw [slice_append_boundary]
    apply word_ext (by simp)
    intro i hi
    have hit : i < τ.length := by simpa using hi
    rw [getD_slice _ _ hit, Nat.zero_add]
  have hclear : ∀ x, controlsClear (true :: τ) x = true → x = 0 := by
    intro x hx
    by_contra hn
    have h := (controlsClear_iff _ _).mp hx 0 (by omega)
    simp at h
  rw [synthesisTree_iff]
  constructor
  · rintro ⟨h1,h2⟩
    have h := h2 0 (by simp) (by rfl) (by rfl)
    simpa only [Nat.mul_zero, Nat.zero_add, List.length_cons, Nat.add_sub_cancel,
      htail] using h
  · intro h
    constructor
    · intro x hx hc
      have := hclear x hc
      subst x
      exact diagonalTree_empty
    · intro x hx hc hb
      have := hclear x hc
      subst x
      simpa only [Nat.mul_zero, Nat.zero_add, List.length_cons, Nat.add_sub_cancel,
        htail] using h

end PolicySynthesis
