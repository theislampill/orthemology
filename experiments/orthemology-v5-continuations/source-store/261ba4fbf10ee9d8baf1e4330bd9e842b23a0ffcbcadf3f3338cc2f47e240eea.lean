import ProductiveCompleteness

/-! Source unity from local complete ancestry and undirected connectedness.
The productive reading, local-completion existence and full field scope are
substantive. Reflexive coverage is not self-production. -/
namespace Orthemology.Tranche6.ConnectedUnity

variable {D : Type*}

def Below (r : D → D → Prop) (a b : D) : Prop := a = b ∨ r a b

def Root (r : D → D → Prop) (g : D) : Prop := ¬ ∃ y, r y g

def LocalCover (r : D → D → Prop) (g x : D) : Prop :=
  Below r g x ∧ ∀ y, Below r y x → Below r g y

def LocallyComplete (r : D → D → Prop) : Prop := ∀ x, ∃ g, LocalCover r g x

def LeastAncestor (r : D → D → Prop) (g : D) : Prop := ∀ x, Below r g x

inductive Path (r : D → D → Prop) : D → D → Prop where
  | refl (x : D) : Path r x x
  | step {x y z : D} : (r x y ∨ r y x) → Path r y z → Path r x z

def Connected (r : D → D → Prop) : Prop := ∀ x y, Path r x y

theorem below_transitive (r : D → D → Prop)
    (trans : ∀ a b c, r a b → r b c → r a c) :
    ∀ a b c, Below r a b → Below r b c → Below r a c := by
  intro a b c hab hbc
  rcases hab with rfl | hab
  · exact hbc
  rcases hbc with rfl | hbc
  · exact Or.inr hab
  · exact Or.inr (trans a b c hab hbc)

theorem below_root_eq (r : D → D → Prop) (a g : D)
    (root : Root r g) (h : Below r a g) : a = g := by
  rcases h with h | h
  · exact h
  · exact False.elim (root ⟨a,h⟩)

theorem root_of_local_cover (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (g x : D) (cover : LocalCover r g x) : Root r g := by
  rintro ⟨y,hyg⟩
  have hyx := below_transitive r trans y g x (Or.inr hyg) cover.1
  rcases cover.2 y hyx with h | h
  · subst y
    exact irrefl g hyg
  · exact irrefl g (trans g y g h hyg)

theorem local_cover_unique (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (g h x : D) (cg : LocalCover r g x) (ch : LocalCover r h x) : g = h := by
  exact below_root_eq r g h (root_of_local_cover r irrefl trans h x ch) (cg.2 h ch.1)

theorem root_covers_itself (r : D → D → Prop) (g : D)
    (root : Root r g) : LocalCover r g g := by
  refine ⟨Or.inl rfl, ?_⟩
  intro y hy
  exact Or.inl (below_root_eq r y g root hy).symm

theorem roots_agree_on_edge (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (g h x y : D) (cx : LocalCover r g x) (cy : LocalCover r h y)
    (edge : r x y) : g = h := by
  have gBelowY := below_transitive r trans g x y cx.1 (Or.inr edge)
  exact (below_root_eq r h g (root_of_local_cover r irrefl trans g x cx)
    (cy.2 g gBelowY)).symm

theorem roots_agree_on_path (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (source : D → D) (covers : ∀ x, LocalCover r (source x) x)
    (x y : D) (path : Path r x y) : source x = source y := by
  induction path with
  | refl _ => rfl
  | @step x y z edge _ ih =>
    have e : source x = source y := by
      rcases edge with h | h
      · exact roots_agree_on_edge r irrefl trans (source x) (source y) x y (covers x) (covers y) h
      · exact (roots_agree_on_edge r irrefl trans (source y) (source x) y x (covers y) (covers x) h).symm
    exact e.trans ih

theorem common_cover_of_connected_local (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (base : D) (hlocal : LocallyComplete r) (connected : Connected r) :
    ∃ g, ∀ x, LocalCover r g x := by
  classical
  let source : D → D := fun x => Classical.choose (hlocal x)
  have covers : ∀ x, LocalCover r (source x) x := fun x => Classical.choose_spec (hlocal x)
  refine ⟨source base, ?_⟩
  intro x
  have h := roots_agree_on_path r irrefl trans source covers base x (connected base x)
  rw [h]
  exact covers x

theorem least_of_connected_local (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (base : D) (hlocal : LocallyComplete r) (connected : Connected r) :
    ∃ g, LeastAncestor r g := by
  obtain ⟨g,hg⟩ := common_cover_of_connected_local r irrefl trans base hlocal connected
  exact ⟨g,fun x => (hg x).1⟩

theorem least_implies_local_and_connected (r : D → D → Prop)
    (g : D) (least : LeastAncestor r g) : LocallyComplete r ∧ Connected r := by
  constructor
  · intro x
    exact ⟨g,least x,fun y _ => least y⟩
  · intro x y
    have pgy : Path r g y := by
      rcases least y with h | h
      · subst y
        exact Path.refl g
      · exact Path.step (Or.inl h) (Path.refl y)
    rcases least x with h | h
    · subst x
      exact pgy
    · exact Path.step (Or.inr h) pgy

theorem local_connected_iff_least (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c) (base : D) :
    (LocallyComplete r ∧ Connected r) ↔ ∃ g, LeastAncestor r g := by
  constructor
  · rintro ⟨hl,hc⟩
    exact least_of_connected_local r irrefl trans base hl hc
  · rintro ⟨g,hg⟩
    exact least_implies_local_and_connected r g hg

theorem unique_root_of_connected_local (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (base : D) (hlocal : LocallyComplete r) (connected : Connected r) :
    ∃ g, Root r g ∧ ∀ h, Root r h → h = g := by
  obtain ⟨g,hg⟩ := common_cover_of_connected_local r irrefl trans base hlocal connected
  refine ⟨g,root_of_local_cover r irrefl trans g base (hg base), ?_⟩
  intro h hr
  exact (below_root_eq r g h hr (hg h).1).symm

def RootAncestor (r : D → D → Prop) (g x : D) : Prop := Root r g ∧ Below r g x

/-- For one target, a unique root ancestor is not enough: its other ancestors
may have no root ancestors at all. Root support throughout this target's cone
is the exact additional condition; it follows from global root existence. -/
theorem local_cover_iff_unique_root_and_ancestral_support (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c) (x : D) :
    (∃ g, LocalCover r g x) ↔
      ((∃! g, RootAncestor r g x) ∧
        ∀ y, Below r y x → ∃ h, RootAncestor r h y) := by
  constructor
  · rintro ⟨g,hg⟩
    have root := root_of_local_cover r irrefl trans g x hg
    constructor
    · refine ⟨g,⟨root,hg.1⟩,?_⟩
      intro h hh
      exact (below_root_eq r g h hh.1 (hg.2 h hh.2)).symm
    · intro y hy
      exact ⟨g,root,hg.2 y hy⟩
  · rintro ⟨⟨g,hg,unique⟩,support⟩
    refine ⟨g,hg.2,?_⟩
    intro y hy
    obtain ⟨h,hh⟩ := support y hy
    have hx : RootAncestor r h x :=
      ⟨hh.1,below_transitive r trans h y x hh.2 hy⟩
    have eq := unique h hx
    rw [← eq]
    exact hh.2

theorem local_iff_unique_root_ancestors (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c) :
    LocallyComplete r ↔ ∀ x, ∃! g, RootAncestor r g x := by
  constructor
  · intro hl x
    obtain ⟨g,hg⟩ := hl x
    refine ⟨g,⟨root_of_local_cover r irrefl trans g x hg,hg.1⟩,?_⟩
    intro h hh
    exact (below_root_eq r g h hh.1 (hg.2 h hh.2)).symm
  · intro hu x
    obtain ⟨g,hg,unique⟩ := hu x
    refine ⟨g,hg.2,?_⟩
    intro y hy
    obtain ⟨h,hh,_⟩ := hu y
    have hx : RootAncestor r h x :=
      ⟨hh.1,below_transitive r trans h y x hh.2 hy⟩
    have eq := unique h hx
    rw [← eq]
    exact hh.2

theorem strict_descendant_of_nontrivial_field (r : D → D → Prop)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (g : D) (least : LeastAncestor r g) (nontrivial : ∃ a b, r a b) :
    ∃ x, r g x := by
  obtain ⟨a,b,hab⟩ := nontrivial
  rcases least a with h | h
  · subst a
    exact ⟨b,hab⟩
  · exact ⟨b,trans g a b h hab⟩

namespace Controls

def Merge (a b : Fin 3) : Prop := (a=0 ∨ a=1) ∧ b=2

theorem merge_strict :
    (∀ x, ¬ Merge x x) ∧ (∀ a b c, Merge a b → Merge b c → Merge a c) := by
  simp only [Merge]
  decide

theorem merge_connected : Connected Merge := by
  intro x y
  fin_cases x <;> fin_cases y
  all_goals first
    | exact Path.refl _
    | exact Path.step (Or.inl (by simp only [Merge]; decide)) (Path.refl _)
    | exact Path.step (Or.inr (by simp only [Merge]; decide)) (Path.refl _)
    | exact Path.step (y:=2) (Or.inl (by simp only [Merge]; decide))
        (Path.step (Or.inr (by simp only [Merge]; decide)) (Path.refl _))

theorem merge_two_roots_no_local_completion :
    Root Merge 0 ∧ Root Merge 1 ∧ (0:Fin 3) ≠ 1 ∧ ¬ ∃ g, LocalCover Merge g 2 := by
  simp only [Root,LocalCover,Below,Merge]
  decide

def Split (a b : Fin 4) : Prop := (a=0 ∧ b=1) ∨ (a=2 ∧ b=3)

theorem split_strict :
    (∀ x, ¬ Split x x) ∧ (∀ a b c, Split a b → Split b c → Split a c) := by
  simp only [Split]
  decide

theorem split_local_no_global : LocallyComplete Split ∧ ¬ ∃ g, LeastAncestor Split g := by
  simp only [LocallyComplete,LocalCover,LeastAncestor,Below,Split]
  decide

theorem split_disconnected : ¬ Connected Split := by
  intro hc
  exact split_local_no_global.2
    (least_of_connected_local Split split_strict.1 split_strict.2 0 split_local_no_global.1 hc)

def NecessaryEx (_ : Bool) (_ : Fin 3) : Prop := True

theorem merge_all_necessary : ∀ x w, NecessaryEx w x := by
  intro x w
  trivial

theorem singleton_reflexive_no_productivity :
    LocalCover (fun (_ _ : Unit) => False) () () ∧
      ¬ ∃ x, (fun (_ _ : Unit) => False) () x := by
  simp only [LocalCover,Below]
  decide

/-- Nonemptiness cannot be dropped from the field-level existence theorem. -/
theorem empty_vacuous_local_connected_no_least :
    LocallyComplete (fun (_ _ : Empty) => False) ∧
      Connected (fun (_ _ : Empty) => False) ∧
      ¬ ∃ g, LeastAncestor (fun (_ _ : Empty) => False) g := by
  refine ⟨?_,?_,?_⟩
  · intro x
    exact x.elim
  · intro x
    exact x.elim
  · rintro ⟨g,_⟩
    exact g.elim

end Controls
end Orthemology.Tranche6.ConnectedUnity
