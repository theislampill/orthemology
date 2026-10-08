import ConnectedUnity

/-!
An actual infinite control. Unique root ancestor at one target, even a unique
root in a connected field, does not imply complete coverage. No finite cutoff
is used. Productive realizability of this relation is not asserted.
-/
namespace Orthemology.Tranche6.ConnectedUnity.InfiniteControls

inductive Item where
  | ground
  | target
  | branch (n : ℕ)
  deriving DecidableEq

open Item

def Fork (a b : Item) : Prop :=
  match a, b with
  | ground, target => True
  | branch _, target => True
  | branch m, branch n => n < m
  | _, _ => False

theorem fork_irreflexive : ∀ x, ¬ Fork x x := by
  intro x
  cases x <;> simp [Fork]

theorem fork_transitive : ∀ a b c, Fork a b → Fork b c → Fork a c := by
  intro a b c hab hbc
  cases a <;> cases b <;> cases c <;> simp only [Fork] at *
  all_goals first | contradiction | trivial | exact Nat.lt_trans hbc hab

theorem ground_is_root : Root Fork ground := by
  rintro ⟨y,hy⟩
  cases y <;> exact hy

theorem branch_has_predecessor (n : ℕ) : Fork (branch (n+1)) (branch n) := by
  exact Nat.lt_succ_self n

theorem only_ground_is_root : ∀ x, Root Fork x ↔ x = ground := by
  intro x
  constructor
  · intro hr
    cases x with
    | ground => rfl
    | target => exact False.elim (hr ⟨ground,True.intro⟩)
    | branch n => exact False.elim (hr ⟨branch (n+1),branch_has_predecessor n⟩)
  · rintro rfl
    exact ground_is_root

theorem branch_has_no_root_ancestor (n : ℕ) : ¬ ∃ g, RootAncestor Fork g (branch n) := by
  rintro ⟨g,hg⟩
  have eq := (only_ground_is_root g).mp hg.1
  subst g
  simpa [Below,Fork] using hg.2

theorem target_unique_root_ancestor : ∃! g, RootAncestor Fork g target := by
  refine ⟨ground,⟨ground_is_root,Or.inr True.intro⟩,?_⟩
  intro g hg
  exact (only_ground_is_root g).mp hg.1

theorem target_no_local_cover : ¬ ∃ g, LocalCover Fork g target := by
  rintro ⟨g,hg⟩
  have root := root_of_local_cover Fork fork_irreflexive fork_transitive g target hg
  have eq := (only_ground_is_root g).mp root
  subst g
  have h := hg.2 (branch 0) (Or.inr True.intro)
  simp [Below,Fork] at h

theorem fork_connected : Connected Fork := by
  intro x y
  have pty : Path Fork target y := by
    cases y with
    | ground => exact Path.step (y:=ground) (Or.inr True.intro) (Path.refl ground)
    | target => exact Path.refl target
    | branch n => exact Path.step (y:=branch n) (Or.inr True.intro) (Path.refl (branch n))
  cases x with
  | ground => exact Path.step (y:=target) (Or.inl True.intro) pty
  | target => exact pty
  | branch n => exact Path.step (y:=target) (Or.inl True.intro) pty

theorem unique_root_connected_without_least :
    Connected Fork ∧ (∃! g, Root Fork g) ∧ ¬ ∃ g, LeastAncestor Fork g := by
  refine ⟨fork_connected,⟨ground,ground_is_root,fun g hg => (only_ground_is_root g).mp hg⟩,?_⟩
  rintro ⟨g,hg⟩
  exact target_no_local_cover ⟨g,hg target,fun y _ => hg y⟩

theorem pointwise_uniqueness_without_local_completion :
    (∃! g, RootAncestor Fork g target) ∧ ¬ ∃ g, LocalCover Fork g target := by
  exact ⟨target_unique_root_ancestor,target_no_local_cover⟩

def NecessaryEx (_ : Bool) (_ : Item) : Prop := True

theorem all_fork_nodes_necessary : ∀ x w, NecessaryEx w x := by
  intro x w
  trivial

end Orthemology.Tranche6.ConnectedUnity.InfiniteControls
