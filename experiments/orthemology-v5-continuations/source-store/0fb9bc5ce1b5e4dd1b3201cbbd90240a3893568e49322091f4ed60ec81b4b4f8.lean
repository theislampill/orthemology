import ExecutablePruning

/-! Finite SCC-based end-component elimination without powerset enumeration.
The graph predicates and reference selector are imported unchanged. -/
set_option linter.unusedSectionVars false

namespace HiddenParity.SCCPruning
variable {State Pair : Type*} [Fintype State] [DecidableEq State] [DecidableEq Pair]

/-- Retain a pair only if its successors exist as sources and remain in its SCC. -/
def Keep (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) (e : Pair) : Prop :=
  (succ e).Nonempty ∧ ∀ t ∈ succ e,
    t ∈ usedStates source U ∧
      source e ∈ FiniteReachability.reachable (Edge source succ U) t

instance keepDecidable (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) (e : Pair) : Decidable (Keep source succ U e) := by
  unfold Keep
  infer_instance

def step (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) : Finset Pair := U.filter (Keep source succ U)

omit [DecidableEq Pair] in
theorem step_subset (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) : step source succ U ⊆ U := Finset.filter_subset _ _

omit [DecidableEq Pair] in
/-- The deletion invariant is proved for every genuine end component. -/
theorem step_preserves {source : Pair → State} {succ : Pair → Finset State}
    {E U : Finset Pair} (hE : IsEndComponent source succ E) (hEU : E ⊆ U) :
    E ⊆ step source succ U := by
  intro e he
  refine Finset.mem_filter.mpr ⟨hEU he, hE.successors_nonempty e he, ?_⟩
  intro t ht
  have htE := hE.closed e he ht
  refine ⟨usedStates_mono hEU htE, ?_⟩
  apply (FiniteReachability.reachable_iff _ _ _).mpr
  exact reach_mono hEU (hE.connected t htE (source e)
    (Finset.mem_image.mpr ⟨e, he, rfl⟩))

def iterate (source : Pair → State) (succ : Pair → Finset State) :
    Nat → Finset Pair → Finset Pair
  | 0, U => U
  | n+1, U => iterate source succ n (step source succ U)

theorem iterate_subset (source : Pair → State) (succ : Pair → Finset State)
    (n : Nat) (U : Finset Pair) : iterate source succ n U ⊆ U := by
  induction n generalizing U with
  | zero => exact Finset.Subset.refl U
  | succ n ih => exact (ih _).trans (step_subset source succ U)

theorem iterate_preserves {source : Pair → State} {succ : Pair → Finset State}
    {E U : Finset Pair} (hE : IsEndComponent source succ E) (hEU : E ⊆ U) (n : Nat) :
    E ⊆ iterate source succ n U := by
  induction n generalizing U with
  | zero => exact hEU
  | succ n ih => exact ih (step_preserves hE hEU)

omit [DecidableEq Pair] in
theorem iterate_eq_of_stable {source : Pair → State} {succ : Pair → Finset State}
    {U : Finset Pair} (h : step source succ U = U) (n : Nat) :
    iterate source succ n U = U := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [iterate, h] using ih

/-- At most the initial pair count many strict deletion rounds are possible. -/
theorem iterate_stable (source : Pair → State) (succ : Pair → Finset State)
    (n : Nat) (U : Finset Pair) (hBound : U.card ≤ n) :
    step source succ (iterate source succ n U) = iterate source succ n U := by
  induction n generalizing U with
  | zero =>
      have hU : U = ∅ := Finset.card_eq_zero.mp (by omega)
      subst U
      simp [iterate, step]
  | succ n ih =>
      by_cases hs : step source succ U = U
      · rw [iterate_eq_of_stable hs]
        exact hs
      · have hStrict : step source succ U ⊂ U :=
          Finset.ssubset_iff_subset_ne.mpr ⟨step_subset source succ U, hs⟩
        have hCard := Finset.card_lt_card hStrict
        exact ih (step source succ U) (by omega)

/-- All pairs whose source shares the anchor's SCC in the current graph. -/
def cluster (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) (anchor : State) : Finset Pair :=
  U.filter (fun e => source e ∈ FiniteReachability.reachable (Edge source succ U) anchor ∧
    anchor ∈ FiniteReachability.reachable (Edge source succ U) (source e))

omit [DecidableEq Pair] in
theorem mem_cluster {source : Pair → State} {succ : Pair → Finset State}
    {U : Finset Pair} {anchor : State} {e : Pair} :
    e ∈ cluster source succ U anchor ↔ e ∈ U ∧
      Reach source succ U anchor (source e) ∧ Reach source succ U (source e) anchor := by
  simp only [cluster, Finset.mem_filter, FiniteReachability.reachable_iff]
  rfl

omit [DecidableEq Pair] in
theorem cluster_subset (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) (anchor : State) : cluster source succ U anchor ⊆ U :=
  Finset.filter_subset _ _

theorem anchor_mem_cluster {source : Pair → State} {succ : Pair → Finset State}
    {U : Finset Pair} {a : Pair} (ha : a ∈ U) : a ∈ cluster source succ U (source a) :=
  mem_cluster.mpr ⟨ha, Relation.ReflTransGen.refl, Relation.ReflTransGen.refl⟩

/-- A path between states in one SCC can be restricted to pairs of that SCC.
No connectivity of the restricted graph is assumed. -/
theorem reach_restrict {source : Pair → State} {succ : Pair → Finset State}
    {U : Finset Pair} {anchor s t : State}
    (hStart : Reach source succ U anchor s) (hPath : Reach source succ U s t)
    (hBack : Reach source succ U t anchor) :
    Reach source succ (cluster source succ U anchor) s t := by
  revert hBack
  induction hPath with
  | refl => intro _; exact Relation.ReflTransGen.refl
  | @tail b c hab hbc ih =>
      intro hc
      have hb : Reach source succ U b anchor := (Relation.ReflTransGen.single hbc).trans hc
      apply (ih hb).tail
      obtain ⟨e, he, hsrc, ht⟩ := hbc
      refine ⟨e, mem_cluster.mpr ⟨he, ?_, ?_⟩, hsrc, ht⟩
      · simpa only [hsrc] using hStart.trans hab
      · simpa only [hsrc] using hb

/-- Every original component belongs to one current SCC cluster. -/
theorem component_subset_cluster {source : Pair → State} {succ : Pair → Finset State}
    {E U : Finset Pair} {a : Pair} (hE : IsEndComponent source succ E)
    (hEU : E ⊆ U) (ha : a ∈ E) : E ⊆ cluster source succ U (source a) := by
  intro e he
  have haS : source a ∈ usedStates source E := Finset.mem_image.mpr ⟨a, ha, rfl⟩
  have heS : source e ∈ usedStates source E := Finset.mem_image.mpr ⟨e, he, rfl⟩
  exact mem_cluster.mpr ⟨hEU he, reach_mono hEU (hE.connected _ haS _ heS),
    reach_mono hEU (hE.connected _ heS _ haS)⟩

/-- Stability supplies successor closure; SCC path restriction supplies connectivity. -/
theorem stable_cluster_component {source : Pair → State} {succ : Pair → Finset State}
    {U : Finset Pair} {a : Pair} (hStable : step source succ U = U) (ha : a ∈ U) :
    IsEndComponent source succ (cluster source succ U (source a)) := by
  have hKeep : ∀ e ∈ U, Keep source succ U e := by
    intro e he
    have hs : e ∈ step source succ U := hStable.symm ▸ he
    exact (Finset.mem_filter.mp hs).2
  refine ⟨⟨a, anchor_mem_cluster ha⟩, ?_, ?_, ?_⟩
  · intro e he
    exact (hKeep e (mem_cluster.mp he).1).1
  · intro e he t ht
    obtain ⟨heU, hAe, heA⟩ := mem_cluster.mp he
    obtain ⟨htU, hte⟩ := (hKeep e heU).2 t ht
    have heT : Reach source succ U (source e) t :=
      Relation.ReflTransGen.single ⟨e, heU, rfl, ht⟩
    have htA : Reach source succ U t (source a) :=
      ((FiniteReachability.reachable_iff _ _ _).mp hte).trans heA
    obtain ⟨f, hfU, hft⟩ := Finset.mem_image.mp htU
    refine Finset.mem_image.mpr ⟨f, mem_cluster.mpr ⟨hfU, ?_, ?_⟩, hft⟩
    · simpa only [hft] using hAe.trans heT
    · simpa only [hft] using htA
  · intro s hs t ht
    obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp hs
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp ht
    have he' := mem_cluster.mp he
    have hf' := mem_cluster.mp hf
    exact reach_restrict he'.2.1 (he'.2.2.trans hf'.2.1) hf'.2.2

theorem stable_cluster_maximal {source : Pair → State} {succ : Pair → Finset State}
    {U : Finset Pair} {a : Pair} (hStable : step source succ U = U) (ha : a ∈ U) :
    MaximalComponent (endComponentFamily source succ) U (cluster source succ U (source a)) := by
  refine ⟨stable_cluster_component hStable ha, cluster_subset _ _ _ _, ?_⟩
  intro E hE hEU hCE
  exact Finset.Subset.antisymm (component_subset_cluster hE hEU (hCE (anchor_mem_cluster ha))) hCE

/-- SCC finite reference: deletion, then one SCC cluster per retained pair.
The only family construction is image, never powerset. -/
def mecs (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) : Finset (Finset Pair) :=
  let K := iterate source succ U.card U
  K.image (fun a => cluster source succ K (source a))

theorem mem_mecs_iff {source : Pair → State} {succ : Pair → Finset State}
    {U D : Finset Pair} :
    D ∈ mecs source succ U ↔ MaximalComponent (endComponentFamily source succ) U D := by
  let K := iterate source succ U.card U
  have hK : step source succ K = K := iterate_stable source succ U.card U (le_refl _)
  have hKU : K ⊆ U := iterate_subset source succ U.card U
  change D ∈ K.image (fun a => cluster source succ K (source a)) ↔ _
  constructor
  · intro hD
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hD
    have hm := stable_cluster_maximal hK ha
    refine ⟨hm.1, hm.2.1.trans hKU, ?_⟩
    intro E hE hEU hDE
    exact hm.2.2 E hE (iterate_preserves hE hEU U.card) hDE
  · intro hD
    have hDK : D ⊆ K := iterate_preserves hD.1 hD.2.1 U.card
    obtain ⟨a, haD⟩ := hD.1.nonempty
    have haK := hDK haD
    have hComp := stable_cluster_component hK haK
    have hDC := component_subset_cluster hD.1 hDK haD
    have hCU := (cluster_subset source succ K (source a)).trans hKU
    have hEq := hD.2.2 _ hComp hCU hDC
    exact Finset.mem_image.mpr ⟨a, haK, hEq⟩

/-- The returned family has at most as many members as original retained pairs. -/
theorem mecs_card_le (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) : (mecs source succ U).card ≤ U.card := by
  exact (Finset.card_image_le).trans (Finset.card_le_card (iterate_subset source succ U.card U))

/-- Exact equality with the previous independently defined exhaustive selector. -/
theorem mecs_eq_executable (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) : mecs source succ U = executableMECs source succ U := by
  rw [executableMECs_eq]
  ext D
  rw [mem_mecs_iff, mem_maximalComponents]

end HiddenParity.SCCPruning
