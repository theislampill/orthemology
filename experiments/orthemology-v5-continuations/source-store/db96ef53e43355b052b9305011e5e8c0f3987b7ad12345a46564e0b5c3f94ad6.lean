import InfiniteRootlessBranch

/- Reviewer-owned proofs and adversarial controls. Author definitions are imported,
   but the core local-to-global proof does not invoke author's unity theorems. -/
namespace ConnectedReview
open Orthemology.Tranche6.ConnectedUnity
variable {D : Type*} (r : D → D → Prop)

theorem reviewer_root_of_cover
    (hi : ∀ x, ¬ r x x) (ht : ∀ a b c, r a b → r b c → r a c)
    {g x : D} (h : LocalCover r g x) : Root r g := by
  rintro ⟨y,hy⟩
  have yx : Below r y x := by
    rcases h.1 with hg | hg
    · exact Or.inr (hg ▸ hy)
    · exact Or.inr (ht y g x hy hg)
  rcases h.2 y yx with eq | gy
  · subst y
    exact hi g hy
  · exact hi g (ht g y g gy hy)

theorem reviewer_edge_cover_eq
    (hi : ∀ x, ¬ r x x) (ht : ∀ a b c, r a b → r b c → r a c)
    {g h x y : D} (cx : LocalCover r g x) (cy : LocalCover r h y)
    (xy : r x y) : g = h := by
  have gy : Below r g y := by
    rcases cx.1 with gx | gx
    · exact Or.inr (gx ▸ xy)
    · exact Or.inr (ht g x y gx xy)
  have rg := reviewer_root_of_cover r hi ht cx
  rcases cy.2 g gy with eq | hg
  · exact eq.symm
  · exact False.elim (rg ⟨h,hg⟩)

theorem reviewer_path_cover
    (hi : ∀ x, ¬ r x x) (ht : ∀ a b c, r a b → r b c → r a c)
    (hl : LocallyComplete r) {x y : D} (p : Path r x y) :
    ∀ g, LocalCover r g x → LocalCover r g y := by
  induction p with
  | refl => intro g hg; exact hg
  | @step x z y xz _ ih =>
    intro g hg
    obtain ⟨h,hh⟩ := hl z
    have eq : g = h := by
      rcases xz with e | e
      · exact reviewer_edge_cover_eq r hi ht hg hh e
      · exact (reviewer_edge_cover_eq r hi ht hh hg e).symm
    subst h
    exact ih g hh

/-- Independent constructive proof: no selected global source function. -/
theorem reviewer_constructive_local_to_least
    (hi : ∀ x, ¬ r x x) (ht : ∀ a b c, r a b → r b c → r a c)
    (base : D) (hl : LocallyComplete r) (hc : Connected r) :
    ∃ g, LeastAncestor r g := by
  obtain ⟨g,hg⟩ := hl base
  exact ⟨g, fun x => (reviewer_path_cover r hi ht hl (hc base x) g hg).1⟩

/-- Existence is the field theorem; strictness separately fixes the bearer. -/
theorem reviewer_least_unique
    (hi : ∀ x, ¬ r x x) (ht : ∀ a b c, r a b → r b c → r a c)
    {g h : D} (hg : LeastAncestor r g) (hh : LeastAncestor r h) : g = h := by
  rcases hg h with eq | gh
  · exact eq
  rcases hh g with eq | hgr
  · exact eq.symm
  · exact False.elim (hi g (ht g h g gh hgr))

/-- Every node's root support plus globally unique root suffices without
    separately assuming connectivity. The support premise does actual work. -/
theorem reviewer_global_unique_supported_to_least
    (unique : ∃! g, Root r g)
    (supported : ∀ x, ∃ g, RootAncestor r g x) : ∃ g, LeastAncestor r g := by
  obtain ⟨g,_,hu⟩ := unique
  refine ⟨g, ?_⟩
  intro x
  obtain ⟨h,hh⟩ := supported x
  have eq := hu h hh.1
  subst h
  exact hh.2

/-- A target's local cover cannot skip a productive predecessor of itself. -/
theorem reviewer_pointwise_forward
    (hi : ∀ x, ¬ r x x) (ht : ∀ a b c, r a b → r b c → r a c)
    {g x : D} (hx : LocalCover r g x) :
    (∃! h, RootAncestor r h x) ∧ ∀ y, Below r y x → ∃ h, RootAncestor r h y := by
  have hr := reviewer_root_of_cover r hi ht hx
  constructor
  · refine ⟨g,⟨hr,hx.1⟩,?_⟩
    intro h hh
    rcases hx.2 h hh.2 with eq | gh
    · exact eq.symm
    · exact False.elim (hh.1 ⟨g,gh⟩)
  · intro y hy
    exact ⟨g,hr,hx.2 y hy⟩

theorem reviewer_pointwise_reverse
    (ht : ∀ a b c, r a b → r b c → r a c) {x : D}
    (unique : ∃! g, RootAncestor r g x)
    (support : ∀ y, Below r y x → ∃ h, RootAncestor r h y) :
    ∃ g, LocalCover r g x := by
  obtain ⟨g,hg,hu⟩ := unique
  refine ⟨g,hg.2,?_⟩
  intro y hy
  obtain ⟨h,hh⟩ := support y hy
  have hx : Below r h x := by
    rcases hh.2 with hhy | hhy
    · exact hhy ▸ hy
    rcases hy with hyx | hyx
    · exact Or.inr (hyx ▸ hhy)
    · exact Or.inr (ht h y x hhy hyx)
  have eq := hu h ⟨hh.1,hx⟩
  subst h
  exact hh.2

def ChainWithoutClosure (a b : Fin 3) : Prop := (a=0 ∧ b=1) ∨ (a=1 ∧ b=2)

theorem reviewer_transitivity_is_material :
    (∀ x, ¬ ChainWithoutClosure x x) ∧
    LocallyComplete ChainWithoutClosure ∧
    ¬ ∃ g, LeastAncestor ChainWithoutClosure g := by
  simp only [ChainWithoutClosure, LocallyComplete, LocalCover, LeastAncestor, Below]
  decide

theorem reviewer_unclosed_chain_connected : Connected ChainWithoutClosure := by
  intro x y
  fin_cases x <;> fin_cases y
  · exact Orthemology.Tranche6.ConnectedUnity.Path.refl _
  · exact Orthemology.Tranche6.ConnectedUnity.Path.step (y:=1) (Or.inl (by simp only [ChainWithoutClosure]; decide)) (Orthemology.Tranche6.ConnectedUnity.Path.refl _)
  · exact Orthemology.Tranche6.ConnectedUnity.Path.step (y:=1) (Or.inl (by simp only [ChainWithoutClosure]; decide))
      (Orthemology.Tranche6.ConnectedUnity.Path.step (y:=2) (Or.inl (by simp only [ChainWithoutClosure]; decide)) (Orthemology.Tranche6.ConnectedUnity.Path.refl _))
  · exact Orthemology.Tranche6.ConnectedUnity.Path.step (y:=0) (Or.inr (by simp only [ChainWithoutClosure]; decide)) (Orthemology.Tranche6.ConnectedUnity.Path.refl _)
  · exact Orthemology.Tranche6.ConnectedUnity.Path.refl _
  · exact Orthemology.Tranche6.ConnectedUnity.Path.step (y:=2) (Or.inl (by simp only [ChainWithoutClosure]; decide)) (Orthemology.Tranche6.ConnectedUnity.Path.refl _)
  · exact Orthemology.Tranche6.ConnectedUnity.Path.step (y:=1) (Or.inr (by simp only [ChainWithoutClosure]; decide))
      (Orthemology.Tranche6.ConnectedUnity.Path.step (y:=0) (Or.inr (by simp only [ChainWithoutClosure]; decide)) (Orthemology.Tranche6.ConnectedUnity.Path.refl _))
  · exact Orthemology.Tranche6.ConnectedUnity.Path.step (y:=1) (Or.inr (by simp only [ChainWithoutClosure]; decide)) (Orthemology.Tranche6.ConnectedUnity.Path.refl _)
  · exact Orthemology.Tranche6.ConnectedUnity.Path.refl _

/-- Transitivity without strictness still allows duplicate least witnesses. -/
theorem reviewer_irreflexivity_is_material_to_uniqueness :
    LocalCover (fun (_ _ : Bool) => True) false true ∧
    LocalCover (fun (_ _ : Bool) => True) true true ∧
    false ≠ true ∧ ¬ Root (fun (_ _ : Bool) => True) false := by
  simp only [LocalCover, Below, Root]
  decide

/-- Ambient and induced relations disagree about roothood when a predecessor
    is dropped. The induced singleton is not predecessor-closed. -/
theorem reviewer_scope_roothood_control :
    ¬ Root (fun (a b : Bool) => a=false ∧ b=true) true ∧
    Root (fun (_ _ : Unit) => False) () := by
  simp only [Root]
  decide

/-- Rooted infinite descending subordinate ancestry still has a least source. -/
def Rooted (a b : Option ℕ) : Prop :=
  match a,b with
  | none, some _ => True
  | some m, some n => n < m
  | _,_ => False

theorem reviewer_rooted_strict :
    (∀ x, ¬ Rooted x x) ∧
    (∀ a b c, Rooted a b → Rooted b c → Rooted a c) := by
  constructor
  · intro x; cases x <;> simp [Rooted]
  · intro a b c hab hbc
    cases a <;> cases b <;> cases c <;> simp only [Rooted] at *
    all_goals first | contradiction | trivial | exact Nat.lt_trans hbc hab

theorem reviewer_rooted_least : LeastAncestor Rooted none := by
  intro x; cases x
  · exact Or.inl rfl
  · exact Or.inr True.intro

theorem reviewer_rooted_no_accessible_branch (n : ℕ) : ¬ Acc Rooted (some n) := by
  intro h
  generalize eq : some n = x at h
  induction h generalizing n with
  | intro x _ ih =>
    subst x
    exact ih (some (n+1)) (Nat.lt_succ_self n) (n+1) rfl

theorem reviewer_rooted_not_well_founded : ¬ WellFounded Rooted := by
  intro h
  exact reviewer_rooted_no_accessible_branch 0 (h.apply (some 0))

/-- The infinite Fork counterexample defeats the added support clause exactly
    at an actual predecessor of its target, not merely at an unrelated node. -/
theorem reviewer_fork_support_failure_inside_cone :
    ∃ y, Below InfiniteControls.Fork y InfiniteControls.Item.target ∧
      ¬ ∃ h, RootAncestor InfiniteControls.Fork h y := by
  exact ⟨InfiniteControls.Item.branch 0,Or.inr True.intro,
    InfiniteControls.branch_has_no_root_ancestor 0⟩

/-- Source-mode predicates remain separate data. A graph's least source cannot
    force HistoryComplete for an arbitrary complete-source interpretation. -/
theorem reviewer_graph_does_not_supply_act_bridge :
    LeastAncestor Rooted none ∧
    ¬ Orthemology.Tranche3.ProductiveCompleteness.HistoryComplete
      Orthemology.Tranche3.ProductiveCompleteness.Controls.endpointOnly
      Orthemology.Tranche3.ProductiveCompleteness.Controls.everyMode
      Orthemology.Tranche3.ProductiveCompleteness.Controls.ownMode := by
  refine ⟨reviewer_rooted_least,?_⟩
  simp only [Orthemology.Tranche3.ProductiveCompleteness.HistoryComplete,
    Orthemology.Tranche3.ProductiveCompleteness.Controls.endpointOnly,
    Orthemology.Tranche3.ProductiveCompleteness.Controls.everyMode,
    Orthemology.Tranche3.ProductiveCompleteness.Controls.ownMode]
  decide

#print axioms reviewer_constructive_local_to_least
#print axioms reviewer_least_unique
#print axioms reviewer_global_unique_supported_to_least
#print axioms reviewer_pointwise_forward
#print axioms reviewer_pointwise_reverse
#print axioms reviewer_transitivity_is_material
#print axioms reviewer_unclosed_chain_connected
#print axioms reviewer_irreflexivity_is_material_to_uniqueness
#print axioms reviewer_scope_roothood_control
#print axioms reviewer_rooted_strict
#print axioms reviewer_rooted_least
#print axioms reviewer_rooted_no_accessible_branch
#print axioms reviewer_rooted_not_well_founded
#print axioms reviewer_fork_support_failure_inside_cone
#print axioms reviewer_graph_does_not_supply_act_bridge
end ConnectedReview
