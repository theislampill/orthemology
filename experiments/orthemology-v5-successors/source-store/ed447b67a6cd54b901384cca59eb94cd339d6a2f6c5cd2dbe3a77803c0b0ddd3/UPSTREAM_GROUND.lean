import SourceIdentity

/-!
Exact implication tests for upstream source arguments. Productive interpretation,
coverage existence, contingent reception and essential reception require separate
philosophical warrant. No model here certifies metaphysical possibility.
-/
namespace Orthemology.Tranche6.UpstreamGround

open Orthemology.Tranche3.SourceIdentity

variable {D W : Type*}

/-- Complete ancestral coverage, not existence of a complete account. -/
def Coverage (r : D → D → Prop) (g x : D) : Prop :=
  r g x ∧ ∀ y, r y x → y = g ∨ r g y

/-- Independence follows from coverage and strict productive priority.
Global well-foundedness is not assumed. -/
theorem predecessor_free_of_coverage
    (r : D → D → Prop)
    (irrefl : ∀ y, ¬ r y y)
    (trans : ∀ a b c, r a b → r b c → r a c)
    (g x : D) (coverage : Coverage r g x) : ¬ ∃ y, r y g := by
  rintro ⟨y, hyg⟩
  rcases coverage.2 y (trans y g x hyg coverage.1) with h | h
  · subst y
    exact irrefl g hyg
  · exact irrefl g (trans g y g h hyg)

/-- Same actual bearer, with both modal premises displayed unchanged. -/
theorem uniform_of_complete_coverage
    (ex : W → D → Prop) (dep : W → D → D → Prop)
    (actual : W) (g x : D)
    (present : ex actual g)
    (irrefl : ∀ y, ¬ dep actual y y)
    (trans : ∀ a b c, dep actual a b → dep actual b c → dep actual a c)
    (coverage : Coverage (dep actual) g x)
    (contingent_receives : ∀ y, ex actual y → ¬ Necessary ex y → Received dep actual y)
    (essential_reception : GenericReception ex dep) : UniformRoot ex dep g := by
  apply uniform_of_contingent_reception ex dep actual g
  · exact ⟨present, predecessor_free_of_coverage (dep actual) irrefl trans g x coverage⟩
  · exact contingent_receives
  · exact essential_reception

namespace InfiniteControls

/-- Every natural has an actually declared supplying predecessor. -/
def Chain (y x : ℕ) : Prop := x < y

theorem chain_irreflexive : ∀ x, ¬ Chain x x := by
  intro x
  exact Nat.lt_irrefl x

theorem chain_transitive : ∀ a b c, Chain a b → Chain b c → Chain a c := by
  intro a b c hab hbc
  exact Nat.lt_trans hbc hab

theorem chain_every_member_receives : ∀ x, ∃ y, Chain y x := by
  intro x
  exact ⟨x + 1, Nat.lt_succ_self x⟩

theorem chain_has_no_covering_member : ¬ ∃ g x, Coverage Chain g x := by
  rintro ⟨g, x, hc⟩
  exact (predecessor_free_of_coverage Chain chain_irreflexive chain_transitive g x hc)
    (chain_every_member_receives g)

/-- There is no missing first producer. Both frames keep all naturals in the
outer domain; explicit Ex declares which bearers actually exist. -/
def ContingentEx (w : Bool) (_ : ℕ) : Prop := w = true

def ContingentDep (w : Bool) (y x : ℕ) : Prop := w = true ∧ Chain y x

theorem contingent_dependency_factive :
    ∀ w y x, ContingentDep w y x → ContingentEx w y ∧ ContingentEx w x := by
  intro w y x h
  exact ⟨h.1, h.1⟩

theorem contingent_reception :
    ∀ x, ContingentEx true x → ¬ Necessary ContingentEx x →
      Received ContingentDep true x := by
  intro x _ _
  exact ⟨x + 1, rfl, Nat.lt_succ_self x⟩

theorem generic_reception_without_foundation :
    GenericReception ContingentEx ContingentDep := by
  intro x _ w hw
  exact ⟨x + 1, hw, Nat.lt_succ_self x⟩

theorem actual_chain_but_no_root :
    (∀ x, ContingentEx true x) ∧ ¬ ∃ x, Root ContingentEx ContingentDep true x := by
  refine ⟨fun _ => rfl, ?_⟩
  rintro ⟨x, _, hn⟩
  exact hn ⟨x + 1, rfl, Nat.lt_succ_self x⟩

def NecessaryEx (_ : Bool) (_ : ℕ) : Prop := True

def NecessaryDep (_ : Bool) (y x : ℕ) : Prop := Chain y x

theorem all_necessarily_exist_without_root :
    (∀ x, Necessary NecessaryEx x) ∧
      (∀ w, ¬ ∃ x, Root NecessaryEx NecessaryDep w x) := by
  refine ⟨fun _ _ => True.intro, ?_⟩
  rintro w ⟨x, _, hn⟩
  exact hn ⟨x + 1, Nat.lt_succ_self x⟩

/-- A single source plus an infinite subordinate ancestry. -/
def Rooted (y x : Option ℕ) : Prop :=
  match y, x with
  | none, some _ => True
  | some m, some n => n < m
  | _, _ => False

theorem rooted_irreflexive : ∀ x, ¬ Rooted x x := by
  intro x
  cases x <;> simp [Rooted]

theorem rooted_transitive : ∀ a b c, Rooted a b → Rooted b c → Rooted a c := by
  intro a b c hab hbc
  cases a <;> cases b <;> cases c <;> simp only [Rooted] at *
  all_goals first | contradiction | trivial | exact Nat.lt_trans hbc hab

theorem root_covers_infinite_ancestry : Coverage Rooted none (some 0) := by
  refine ⟨True.intro, ?_⟩
  intro y _
  cases y
  · exact Or.inl rfl
  · exact Or.inr True.intro

private theorem not_acc_some (n : ℕ) : ¬ Acc Rooted (some n) := by
  intro h
  generalize he : some n = x at h
  induction h generalizing n with
  | intro x _ ih =>
    exact ih (some (n + 1)) (by subst x; exact Nat.lt_succ_self n) (n + 1) rfl

theorem complete_root_without_global_wellfoundedness :
    Coverage Rooted none (some 0) ∧ ¬ WellFounded Rooted := by
  refine ⟨root_covers_infinite_ancestry, ?_⟩
  intro h
  exact not_acc_some 0 (h.apply (some 0))

end InfiniteControls

namespace FiniteControls

/-- Each of two components has a productive source and its own effect. -/
inductive Item where | leftSource | leftEffect | rightSource | rightEffect
  deriving DecidableEq, Fintype
open Item

def Split (y x : Item) : Prop :=
  (y = leftSource ∧ x = leftEffect) ∨
  (y = rightSource ∧ x = rightEffect)

theorem split_local_coverage :
    Coverage Split leftSource leftEffect ∧ Coverage Split rightSource rightEffect := by
  simp only [Coverage, Split]
  decide

theorem split_no_common_source :
    ¬ ∃ g, Split g leftEffect ∧ Split g rightEffect := by
  simp only [Split]
  decide

def BruteEx (w : Bool) (_ : Unit) : Prop := w = true

def BruteDep (_ : Bool) (_ _ : Unit) : Prop := False

theorem brute_actual_root_without_necessity :
    Root BruteEx BruteDep true () ∧ ¬ Necessary BruteEx () := by
  simp only [Root, Received, Necessary, BruteEx, BruteDep]
  decide

end FiniteControls
end Orthemology.Tranche6.UpstreamGround
