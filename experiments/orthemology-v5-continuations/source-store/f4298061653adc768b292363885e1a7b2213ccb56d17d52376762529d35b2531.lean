import PruningKernel

/-!
# Concrete directed end components and exact parity target extraction

A pair has a source state and a finite nonempty internal successor set. The
initial pair set supplies admissibility and zero-candidate-exit restrictions.
Graph closure and strong connectivity below are actual graph predicates; they
are not supplied as an abstract preservation premise.
-/
namespace HiddenParity

variable {State Pair Model Row : Type*} [DecidableEq State] [DecidableEq Pair]

/-- States used by at least one retained state/action pair. -/
def usedStates (source : Pair → State) (E : Finset Pair) : Finset State := E.image source

/-- Directed internal support edge enabled by one of the used pairs. -/
def Edge (source : Pair → State) (succ : Pair → Finset State)
    (E : Finset Pair) (s t : State) : Prop :=
  ∃ e ∈ E, source e = s ∧ t ∈ succ e

/-- Ordinary finite directed reachability, allowing a path of length zero. -/
def Reach (source : Pair → State) (succ : Pair → Finset State)
    (E : Finset Pair) (s t : State) : Prop :=
  Relation.ReflTransGen (Edge source succ E) s t

/-- Concrete nonempty closed strongly connected pair component. -/
structure IsEndComponent (source : Pair → State) (succ : Pair → Finset State)
    (E : Finset Pair) : Prop where
  nonempty : E.Nonempty
  successors_nonempty : ∀ e ∈ E, (succ e).Nonempty
  closed : ∀ e ∈ E, succ e ⊆ usedStates source E
  connected : ∀ s ∈ usedStates source E, ∀ t ∈ usedStates source E,
    Reach source succ E s t

omit [DecidableEq Pair] in
theorem usedStates_mono {source : Pair → State} {E D : Finset Pair} (h : E ⊆ D) :
    usedStates source E ⊆ usedStates source D := Finset.image_subset_image h

omit [DecidableEq State] [DecidableEq Pair] in
theorem edge_mono {source : Pair → State} {succ : Pair → Finset State}
    {E D : Finset Pair} (h : E ⊆ D) {s t : State} :
    Edge source succ E s t → Edge source succ D s t := by
  rintro ⟨e, he, hsrc, ht⟩
  exact ⟨e, h he, hsrc, ht⟩

omit [DecidableEq State] [DecidableEq Pair] in
theorem reach_mono {source : Pair → State} {succ : Pair → Finset State}
    {E D : Finset Pair} (h : E ⊆ D) {s t : State} :
    Reach source succ E s t → Reach source succ D s t :=
  Relation.ReflTransGen.mono (fun _ _ => edge_mono h)

/-- Graph-theoretic union is derived for components sharing any state. -/
theorem endComponent_union_of_common_state
    {source : Pair → State} {succ : Pair → Finset State} {E D : Finset Pair}
    (hE : IsEndComponent source succ E) (hD : IsEndComponent source succ D)
    (hi : ∃ s, s ∈ usedStates source E ∧ s ∈ usedStates source D) :
    IsEndComponent source succ (E ∪ D) := by
  obtain ⟨v, hvE, hvD⟩ := hi
  have inclE : usedStates source E ⊆ usedStates source (E ∪ D) :=
    usedStates_mono Finset.subset_union_left
  have inclD : usedStates source D ⊆ usedStates source (E ∪ D) :=
    usedStates_mono Finset.subset_union_right
  refine ⟨hE.nonempty.mono Finset.subset_union_left, ?_, ?_, ?_⟩
  · intro e he
    rcases Finset.mem_union.mp he with he | he
    · exact hE.successors_nonempty e he
    · exact hD.successors_nonempty e he
  · intro e he
    rcases Finset.mem_union.mp he with he | he
    · exact (hE.closed e he).trans inclE
    · exact (hD.closed e he).trans inclD
  · intro s hs t ht
    have hsu : s ∈ usedStates source E ∪ usedStates source D := by
      simpa only [usedStates, Finset.image_union] using hs
    have htu : t ∈ usedStates source E ∪ usedStates source D := by
      simpa only [usedStates, Finset.image_union] using ht
    rcases Finset.mem_union.mp hsu with hsE | hsD <;>
      rcases Finset.mem_union.mp htu with htE | htD
    · exact reach_mono Finset.subset_union_left (hE.connected s hsE t htE)
    · exact (reach_mono Finset.subset_union_left (hE.connected s hsE v hvE)).trans
        (reach_mono Finset.subset_union_right (hD.connected v hvD t htD))
    · exact (reach_mono Finset.subset_union_right (hD.connected s hsD v hvD)).trans
        (reach_mono Finset.subset_union_left (hE.connected v hvE t htE))
    · exact reach_mono Finset.subset_union_right (hD.connected s hsD t htD)

/-- The only abstract graph hypotheses used by the pruning kernel are discharged. -/
def endComponentFamily (source : Pair → State) (succ : Pair → Finset State) :
    ComponentFamily Pair where
  component := IsEndComponent source succ
  nonempty := IsEndComponent.nonempty
  union := by
    intro E D hE hD hi
    obtain ⟨e, heE, heD⟩ := hi
    apply endComponent_union_of_common_state hE hD
    exact ⟨source e, Finset.mem_image.mpr ⟨e, heE, rfl⟩,
      Finset.mem_image.mpr ⟨e, heD, rfl⟩⟩

/-- End-to-end finite graph specialization: no component-family law is assumed. -/
theorem endComponent_output_iff
    (source : Pair → State) (succ : Pair → Finset State) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U D : Finset Pair) :
    D ∈ output (endComponentFamily source succ) B row priority θ U ↔
      MaximalValid (endComponentFamily source succ) B row priority θ U D :=
  output_iff_maximal_valid

/-- Membership in the original target is defined by existence of any qualifying
component, without mentioning pruning or maximality. -/
def IsTargetState (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) (s : State) : Prop :=
  ∃ E, E ⊆ U ∧ Valid (endComponentFamily source succ) B row priority θ E ∧
    s ∈ usedStates source E

noncomputable def targetStates (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) : Finset State := by
  classical
  exact (output (endComponentFamily source succ) B row priority θ U).biUnion
    (usedStates source)

/-- Equality of the state target returned by pruning and the original existential
target definition, including nonmaximal valid components. -/
theorem targetStates_exact
    (source : Pair → State) (succ : Pair → Finset State) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) (s : State) :
    s ∈ targetStates source succ B row priority θ U ↔
      IsTargetState source succ B row priority θ U s := by
  classical
  simp only [targetStates, Finset.mem_biUnion]
  constructor
  · rintro ⟨D, hD, hs⟩
    have hm := output_iff_maximal_valid.mp hD
    exact ⟨D, hm.2.1, hm.1, hs⟩
  · rintro ⟨E, hEU, hV, hs⟩
    obtain ⟨D, hD, hED⟩ := valid_covered_by_output hV hEU
    exact ⟨D, hD, usedStates_mono hED hs⟩

/-- Distinct returned components have disjoint state sets. -/
theorem output_components_state_disjoint
    {source : Pair → State} {succ : Pair → Finset State} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ}
    {θ : Model} {U E D : Finset Pair}
    (hE : E ∈ output (endComponentFamily source succ) B row priority θ U)
    (hD : D ∈ output (endComponentFamily source succ) B row priority θ U)
    (hne : E ≠ D) : Disjoint (usedStates source E) (usedStates source D) := by
  classical
  apply Finset.disjoint_left.mpr
  intro s hsE hsD
  have hmE := mem_maximalComponents.mp hE
  have hmD := mem_maximalComponents.mp hD
  have hUnion := endComponent_union_of_common_state hmE.1 hmD.1 ⟨s, hsE, hsD⟩
  have hu := Finset.union_subset hmE.2.1 hmD.2.1
  have eqE := hmE.2.2 (E ∪ D) hUnion hu Finset.subset_union_left
  have eqD := hmD.2.2 (E ∪ D) hUnion hu Finset.subset_union_right
  exact hne (eqE.symm.trans eqD)

end HiddenParity
