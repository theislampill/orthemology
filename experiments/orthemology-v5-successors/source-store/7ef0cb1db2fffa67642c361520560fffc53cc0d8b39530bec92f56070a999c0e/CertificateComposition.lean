import CertificateSyntax

/-! Ordinary same-input certificate composition. The algorithms read only
submitted support keys and retain every selected witness literally. They do not
union target components or invoke the semantic solver. -/
namespace OrthemicCertificate
variable {q n k : ℕ}

/-- Child-reference monotonicity needs only support-preserving state inclusion. -/
def BodyCovers (c d : Body q n k) : Prop :=
  ∀ N ∈ c, ∃ M ∈ d, M.support = N.support ∧ N.states ⊆ M.states

theorem Node.valid_body_mono {I : Input q n k} {c d : Body q n k}
    (hcover : BodyCovers c d) {N : Node q n k} (h : N.Valid I c) : N.Valid I d := by
  refine ⟨h.1,h.2.1,?_,h.2.2.2⟩
  intro e he
  obtain ⟨hs,hm,hnext⟩ := h.2.2.1 e he
  refine ⟨hs,hm,?_⟩
  intro y hy
  specialize hnext y hy
  split_ifs at hnext ⊢
  · exact hnext
  · obtain ⟨hlt,C,hC,hCs,hCy⟩ := hnext
    obtain ⟨D,hD,hDs,hsub⟩ := hcover C hC
    exact ⟨hlt,D,hD,hDs.trans hCs,hsub hCy⟩

theorem Component.valid_pairs_mono {I : Input q n k} {B : Support q} {θ : Fin q}
    {A A' : Finset (Pair n k)} (hsub : A ⊆ A') {c : Component n k} {s : Fin n}
    (h : c.Valid I B θ A s) : c.Valid I B θ A' s :=
  ⟨h.1,Finset.Subset.trans h.2.1 hsub,h.2.2⟩

theorem Witness.valid_pairs_mono {I : Input q n k} {B : Support q}
    {A A' : Finset (Pair n k)} (hsub : A ⊆ A') {s : Fin n} {θ : Fin q}
    {w : Witness n k} (h : w.Valid I B A s θ) : w.Valid I B A' s θ := by
  cases w with
  | exit p e y => exact ⟨Path.valid_mono hsub h.1,hsub h.2.1,h.2.2⟩
  | target p c t => exact ⟨Path.valid_mono hsub h.1,Component.valid_pairs_mono hsub h.2⟩

def Obligation.key (o : Obligation q n k) : Fin n × Fin q := (o.state,o.candidate)

/-- Left bias at equal state/candidate keys. Components, paths, and exits are
not reconstructed: the chosen obligation value itself is retained. -/
def mergeObligations (xs ys : List (Obligation q n k)) : List (Obligation q n k) :=
  xs ++ ys.filter (fun o => decide (o.key ∉ xs.map Obligation.key))

/-- Every output obligation is literally one submitted input obligation. -/
theorem mergeObligations_mem_iff (xs ys : List (Obligation q n k)) (o : Obligation q n k) :
    o ∈ mergeObligations xs ys ↔ o ∈ xs ∨ o ∈ ys ∧ o.key ∉ xs.map Obligation.key := by
  simp [mergeObligations]

theorem mergeObligations_keys (xs ys : List (Obligation q n k)) :
    (mergeObligations xs ys).map Obligation.key = xs.map Obligation.key ++
      (ys.map Obligation.key).filter (fun z => decide (z ∉ xs.map Obligation.key)) := by
  simp only [mergeObligations,List.map_append,List.filter_map]
  rfl

theorem mergeObligations_nodup {xs ys : List (Obligation q n k)}
    (hx : (xs.map Obligation.key).Nodup) (hy : (ys.map Obligation.key).Nodup) :
    ((mergeObligations xs ys).map Obligation.key).Nodup := by
  rw [mergeObligations_keys]
  refine hx.append (hy.filter _) ?_
  intro z hz hzy
  exact (List.mem_filter.mp hzy).2 |> of_decide_eq_true |> (fun h => h hz)

theorem mergeObligations_toFinset (xs ys : List (Obligation q n k)) :
    ((mergeObligations xs ys).map Obligation.key).toFinset =
      (xs.map Obligation.key).toFinset ∪ (ys.map Obligation.key).toFinset := by
  rw [mergeObligations_keys]
  ext z
  simp only [List.toFinset_append,Finset.mem_union,List.mem_toFinset,List.mem_filter,decide_eq_true_eq]
  tauto

/-- This operation is used only at equal support keys. -/
def mergeNode (N M : Node q n k) : Node q n k :=
  ⟨N.support,N.states ∪ M.states,N.pairs ∪ M.pairs,mergeObligations N.obligations M.obligations⟩

theorem mergeNode_valid {I : Input q n k} {c : Body q n k} {N M : Node q n k}
    (hNM : M.support = N.support) (hN : N.Valid I c) (hM : M.Valid I c) :
    (mergeNode N M).Valid I c := by
  refine ⟨hN.1,?_,?_,?_⟩
  · refine ⟨mergeObligations_nodup hN.2.1.1 hM.2.1.1,?_⟩
    change ((mergeObligations N.obligations M.obligations).map Obligation.key).toFinset = _
    rw [mergeObligations_toFinset]
    change (N.obligations.map (fun o => (o.state,o.candidate))).toFinset ∪
      (M.obligations.map (fun o => (o.state,o.candidate))).toFinset = _
    rw [hN.2.1.2,hM.2.1.2,hNM]
    ext z
    simp [mergeNode,Finset.mem_product,or_and_right]
  · intro e he
    rcases Finset.mem_union.mp he with he | he
    · obtain ⟨hs,hm,hn⟩ := hN.2.2.1 e he
      refine ⟨Finset.mem_union_left _ hs,hm,?_⟩
      intro y hy
      dsimp only [mergeNode] at hy ⊢
      specialize hn y hy
      split_ifs at hn ⊢
      · exact Finset.mem_union_left _ hn
      · exact hn
    · obtain ⟨hs,hm,hn⟩ := hM.2.2.1 e he
      rw [hNM] at hm hn
      refine ⟨Finset.mem_union_right _ hs,hm,?_⟩
      intro y hy
      dsimp only [mergeNode] at hy ⊢
      specialize hn y hy
      split_ifs at hn ⊢
      · exact Finset.mem_union_right _ hn
      · exact hn
  · intro o ho
    rcases List.mem_append.mp ho with ho | ho
    · exact Witness.valid_pairs_mono Finset.subset_union_left (hN.2.2.2 o ho)
    · have hw := hM.2.2.2 o (List.mem_filter.mp ho).1
      rw [hNM] at hw
      exact Witness.valid_pairs_mono Finset.subset_union_right hw

/-- Empty lookup default preserves the requested support and contributes no
states, pairs, or obligations. It cannot answer a query. -/
def emptyNode (B : Support q) : Node q n k := ⟨B,∅,∅,[]⟩

def lookupNode (B : Support q) : Body q n k → Node q n k
  | [] => emptyNode B
  | N :: c => if N.support = B then N else lookupNode B c

@[simp] theorem lookupNode_support (B : Support q) (c : Body q n k) :
    (lookupNode B c).support = B := by
  induction c with
  | nil => rfl
  | cons N c ih => simp only [lookupNode]; split <;> simp_all

theorem lookupNode_mem_or_empty (B : Support q) (c : Body q n k) :
    lookupNode B c ∈ c ∨ lookupNode B c = emptyNode B := by
  induction c with
  | nil => exact Or.inr rfl
  | cons N c ih =>
    simp only [lookupNode]
    split
    · exact Or.inl (List.mem_cons_self)
    · exact ih.imp (List.mem_cons_of_mem _) id

theorem lookupNode_eq_of_mem {B : Support q} {c : Body q n k} {N : Node q n k}
    (hd : (c.map Node.support).Nodup) (hN : N ∈ c) (hs : N.support = B) :
    lookupNode B c = N := by
  induction c with
  | nil => simp at hN
  | cons M c ih =>
    have hd' := List.nodup_cons.mp hd
    simp only [lookupNode]
    split_ifs with hM
    · exact List.inj_on_of_nodup_map hd (List.mem_cons_self) hN (hM.trans hs.symm)
    · rcases List.mem_cons.mp hN with h | h
      · subst N; exact False.elim (hM hs)
      · exact ih hd'.2 h

theorem emptyNode_valid {I : Input q n k} {c : Body q n k} {B : Support q}
    (hB : B.Nonempty) : (emptyNode B : Node q n k).Valid I c := by
  refine ⟨hB,?_,?_,?_⟩
  · simp [Node.KeysValid,emptyNode]
  · simp [Node.PairsValid,emptyNode]
  · simp [emptyNode]

theorem lookupNode_valid {I : Input q n k} {c d : Body q n k} {B : Support q}
    (hB : B.Nonempty) (hv : ∀ N ∈ c, N.Valid I d) : (lookupNode B c).Valid I d := by
  rcases lookupNode_mem_or_empty B c with h | h
  · exact hv _ h
  · rw [h]; exact emptyNode_valid hB

/-- Only keys explicitly present in the submitted body. -/
def bodySupports (c : Body q n k) : Finset (Support q) := (c.map Node.support).toFinset

@[simp] theorem mem_bodySupports (B : Support q) (c : Body q n k) :
    B ∈ bodySupports c ↔ ∃ N ∈ c, N.support = B := by simp [bodySupports]

/-- Executable merge on actual ASTs. No ambient input is changed or restricted.
Acceptance is asserted only for two independently valid input bodies. -/
def merge (c d : Body q n k) : Body q n k :=
  (sortSupports (bodySupports c ∪ bodySupports d)).map
    (fun B => mergeNode (lookupNode B c) (lookupNode B d))

@[simp] theorem mergeNode_support (N M : Node q n k) : (mergeNode N M).support = N.support := rfl

theorem merge_supports (c d : Body q n k) :
    (merge c d).map Node.support = sortSupports (bodySupports c ∪ bodySupports d) := by
  simp [merge,List.map_map,Function.comp_def]

theorem merge_layout (c d : Body q n k) : Layout (merge c d) := by
  unfold Layout
  rw [merge_supports]
  exact ⟨sortSupports_pairwise _,sortSupports_nodup _⟩

theorem merge_covers_left {c d : Body q n k} (hc : (c.map Node.support).Nodup) :
    BodyCovers c (merge c d) := by
  intro N hN
  refine ⟨mergeNode (lookupNode N.support c) (lookupNode N.support d),?_,by simp,?_⟩
  · apply List.mem_map.mpr
    exact ⟨N.support,(mem_sortSupports _ _).mpr (Finset.mem_union_left _ ((mem_bodySupports _ _).mpr ⟨N,hN,rfl⟩)),rfl⟩
  · change N.states ⊆ (lookupNode N.support c).states ∪ (lookupNode N.support d).states
    rw [lookupNode_eq_of_mem hc hN rfl]
    exact Finset.subset_union_left

theorem merge_covers_right {c d : Body q n k} (hd : (d.map Node.support).Nodup) :
    BodyCovers d (merge c d) := by
  intro N hN
  refine ⟨mergeNode (lookupNode N.support c) (lookupNode N.support d),?_,by simp,?_⟩
  · apply List.mem_map.mpr
    exact ⟨N.support,(mem_sortSupports _ _).mpr (Finset.mem_union_right _ ((mem_bodySupports _ _).mpr ⟨N,hN,rfl⟩)),rfl⟩
  · change N.states ⊆ (lookupNode N.support c).states ∪ (lookupNode N.support d).states
    rw [lookupNode_eq_of_mem hd hN rfl]
    exact Finset.subset_union_right

theorem bodyValid_merge {I : Input q n k} {c d : Body q n k}
    (hc : BodyValid I c) (hd : BodyValid I d) : BodyValid I (merge c d) := by
  refine ⟨hc.1,merge_layout c d,?_⟩
  intro N hN
  obtain ⟨B,hB,rfl⟩ := List.mem_map.mp hN
  have hBn : B.Nonempty := by
    rcases Finset.mem_union.mp ((mem_sortSupports _ _).mp hB) with h | h
    · obtain ⟨M,hM,rfl⟩ := (mem_bodySupports _ _).mp h
      exact (hc.2.2 M hM).1
    · obtain ⟨M,hM,rfl⟩ := (mem_bodySupports _ _).mp h
      exact (hd.2.2 M hM).1
  apply mergeNode_valid (by simp)
  · exact lookupNode_valid hBn (fun M hM => Node.valid_body_mono (merge_covers_left hc.2.1.2) (hc.2.2 M hM))
  · exact lookupNode_valid hBn (fun M hM => Node.valid_body_mono (merge_covers_right hd.2.1.2) (hd.2.2 M hM))

/-- The two premises use the identical actual structured input I. -/
theorem bodyCheck_merge {I : Input q n k} {c d : Body q n k}
    (hc : bodyCheck I c = true) (hd : bodyCheck I d = true) : bodyCheck I (merge c d) = true :=
  (bodyCheck_iff _ _).mpr (bodyValid_merge ((bodyCheck_iff _ _).mp hc) ((bodyCheck_iff _ _).mp hd))

theorem queryLookup_of_covers {c d : Body q n k} (h : BodyCovers c d)
    {B : Support q} {s : Fin n} (hq : queryLookup c B s = true) : queryLookup d B s = true := by
  obtain ⟨hB,N,hN,hs,hw⟩ := (queryLookup_iff _ _ _).mp hq
  obtain ⟨M,hM,hMN,hsub⟩ := h N hN
  exact (queryLookup_iff _ _ _).mpr ⟨hB,M,hM,hMN.trans hs,hsub hw⟩

theorem queryLookup_merge_left {I : Input q n k} {c d : Body q n k}
    (hc : bodyCheck I c = true) {B : Support q} {s : Fin n} (hq : queryLookup c B s = true) :
    queryLookup (merge c d) B s = true :=
  queryLookup_of_covers (merge_covers_left ((bodyCheck_iff _ _).mp hc).2.1.2) hq

theorem queryLookup_merge_right {I : Input q n k} {c d : Body q n k}
    (hd : bodyCheck I d = true) {B : Support q} {s : Fin n} (hq : queryLookup d B s = true) :
    queryLookup (merge c d) B s = true :=
  queryLookup_of_covers (merge_covers_right ((bodyCheck_iff _ _).mp hd).2.1.2) hq

/-- Merge cannot invent a support absent from both inputs, even malformed ones. -/
theorem merge_support_iff (c d : Body q n k) (B : Support q) :
    (∃ N ∈ merge c d, N.support = B) ↔
      (∃ N ∈ c, N.support = B) ∨ (∃ N ∈ d, N.support = B) := by
  have h := congrArg (fun l => B ∈ l) (merge_supports c d)
  simpa only [List.mem_map,mem_sortSupports,Finset.mem_union,mem_bodySupports] using Iff.of_eq h

/-- Canonical reordering, used below only with unique support keys. -/
def sortBody (c : Body q n k) : Body q n k :=
  (sortSupports (bodySupports c)).map (fun B => lookupNode B c)

theorem sortBody_supports (c : Body q n k) :
    (sortBody c).map Node.support = sortSupports (bodySupports c) := by
  simp [sortBody,List.map_map,Function.comp_def]

theorem sortBody_layout (c : Body q n k) : Layout (sortBody c) := by
  unfold Layout
  rw [sortBody_supports]
  exact ⟨sortSupports_pairwise _,sortSupports_nodup _⟩

theorem sortBody_mem_iff {c : Body q n k} (hd : (c.map Node.support).Nodup) (N : Node q n k) :
    N ∈ sortBody c ↔ N ∈ c := by
  constructor
  · intro h
    obtain ⟨B,hB,rfl⟩ := List.mem_map.mp h
    obtain ⟨M,hM,hs⟩ := (mem_bodySupports _ _).mp ((mem_sortSupports _ _).mp hB)
    rw [lookupNode_eq_of_mem hd hM hs]
    exact hM
  · intro h
    apply List.mem_map.mpr
    exact ⟨N.support,(mem_sortSupports _ _).mpr ((mem_bodySupports _ _).mpr ⟨N,h,rfl⟩),lookupNode_eq_of_mem hd h rfl⟩

theorem sortBody_covers {c : Body q n k} (hd : (c.map Node.support).Nodup) : BodyCovers c (sortBody c) := by
  intro N hN
  exact ⟨N,(sortBody_mem_iff hd N).mpr hN,rfl,Finset.Subset.refl _⟩

/-- Parent insertion requires a separately checked new node. Sorting neither
supplies its obligations nor infers its support from unions of children. -/
def linkParent (c : Body q n k) (parent : Node q n k) : Body q n k := sortBody (parent :: c)

theorem linkParent_nodup {c : Body q n k} {parent : Node q n k}
    (hd : (c.map Node.support).Nodup) (ha : parent.support ∉ bodySupports c) :
    ((parent :: c).map Node.support).Nodup := by
  simpa only [List.map_cons,List.nodup_cons,List.mem_toFinset,bodySupports] using And.intro ha hd

theorem bodyValid_linkParent {I : Input q n k} {c : Body q n k} {parent : Node q n k}
    (hc : BodyValid I c) (ha : parent.support ∉ bodySupports c) (hp : parent.Valid I c) :
    BodyValid I (linkParent c parent) := by
  have hnd := linkParent_nodup hc.2.1.2 ha
  have hcover : BodyCovers c (linkParent c parent) := by
    intro N hN
    exact ⟨N,(sortBody_mem_iff hnd N).mpr (List.mem_cons_of_mem _ hN),rfl,Finset.Subset.refl _⟩
  refine ⟨hc.1,sortBody_layout _,?_⟩
  intro N hN
  rcases List.mem_cons.mp ((sortBody_mem_iff hnd N).mp hN) with rfl | hN
  · exact Node.valid_body_mono hcover hp
  · exact Node.valid_body_mono hcover (hc.2.2 N hN)

theorem bodyCheck_linkParent {I : Input q n k} {c : Body q n k} {parent : Node q n k}
    (hc : bodyCheck I c = true) (ha : parent.support ∉ bodySupports c)
    (hp : decide (parent.Valid I c) = true) : bodyCheck I (linkParent c parent) = true := by
  apply (bodyCheck_iff _ _).mpr
  exact bodyValid_linkParent ((bodyCheck_iff _ _).mp hc) ha (of_decide_eq_true hp)

theorem queryLookup_linkParent {I : Input q n k} {c : Body q n k} {parent : Node q n k}
    (hc : bodyCheck I c = true) (ha : parent.support ∉ bodySupports c)
    (hp : decide (parent.Valid I c) = true) {s : Fin n} (hs : s ∈ parent.states) :
    queryLookup (linkParent c parent) parent.support s = true := by
  have hp' : parent.Valid I c := of_decide_eq_true hp
  have hnd := linkParent_nodup ((bodyCheck_iff _ _).mp hc).2.1.2 ha
  exact (queryLookup_iff _ _ _).mpr ⟨hp'.1,parent,(sortBody_mem_iff hnd parent).mpr (by simp),rfl,hs⟩

theorem queryLookup_linkParent_old {I : Input q n k} {c : Body q n k} {parent : Node q n k}
    (hc : bodyCheck I c = true) (ha : parent.support ∉ bodySupports c)
    {B : Support q} {s : Fin n} (hq : queryLookup c B s = true) :
    queryLookup (linkParent c parent) B s = true := by
  apply queryLookup_of_covers (c := c) _ hq
  intro N hN
  have hnd := linkParent_nodup ((bodyCheck_iff _ _).mp hc).2.1.2 ha
  exact ⟨N,(sortBody_mem_iff hnd N).mpr (List.mem_cons_of_mem _ hN),rfl,Finset.Subset.refl _⟩

/-- Untrusted-entry API: validate both entire bodies before canonicalization.
Malformed duplicate records or invalid unused nodes therefore cannot disappear. -/
def checkedMerge (I : Input q n k) (c d : Body q n k) : Option (Body q n k) :=
  if bodyCheck I c && bodyCheck I d then some (merge c d) else none

theorem checkedMerge_some_iff (I : Input q n k) (c d out : Body q n k) :
    checkedMerge I c d = some out ↔
      bodyCheck I c = true ∧ bodyCheck I d = true ∧ merge c d = out := by
  unfold checkedMerge
  split <;> simp_all [Bool.and_eq_true]

theorem checkedMerge_valid {I : Input q n k} {c d out : Body q n k}
    (h : checkedMerge I c d = some out) : bodyCheck I out = true := by
  obtain ⟨hc,hd,rfl⟩ := (checkedMerge_some_iff _ _ _ _).mp h
  exact bodyCheck_merge hc hd

/-- Independently checks absence and all local parent obligations against the
old body. No inferred parent support or cached-check assumption is used. -/
def checkedLinkParent (I : Input q n k) (c : Body q n k) (parent : Node q n k) :
    Option (Body q n k) :=
  if bodyCheck I c && decide (parent.support ∉ bodySupports c) && decide (parent.Valid I c)
  then some (linkParent c parent) else none

theorem checkedLinkParent_some_iff (I : Input q n k) (c : Body q n k)
    (parent : Node q n k) (out : Body q n k) : checkedLinkParent I c parent = some out ↔
      bodyCheck I c = true ∧ parent.support ∉ bodySupports c ∧
      parent.Valid I c ∧ linkParent c parent = out := by
  unfold checkedLinkParent
  split <;> simp_all [Bool.and_eq_true, and_assoc]

theorem checkedLinkParent_valid {I : Input q n k} {c out : Body q n k} {parent : Node q n k}
    (h : checkedLinkParent I c parent = some out) : bodyCheck I out = true := by
  obtain ⟨hc,ha,hp,rfl⟩ := (checkedLinkParent_some_iff _ _ _ _).mp h
  exact bodyCheck_linkParent hc ha (decide_eq_true hp)
end OrthemicCertificate
