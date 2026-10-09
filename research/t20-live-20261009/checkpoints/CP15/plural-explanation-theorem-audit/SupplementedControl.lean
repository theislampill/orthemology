import Std

/- The relational control needs only a bounded partial order in which every
   element has a strict subelement. A nonzero atomless complete Boolean algebra
   is a concrete instance, additionally supplying classical supplementation and
   fusion. No topological or Boolean-algebra realization is claimed formalized. -/
namespace SupplementedPluralControl

structure Frame (Fact : Type) where
  part : Fact → Fact → Prop
  reflexive : ∀ x, part x x
  transitive : ∀ {x y z}, part x y → part y z → part x z
  antisymmetric : ∀ {x y}, part x y → part y x → x = y
  top : Fact
  below_top : ∀ x, part x top
  strict_part : ∀ x, ∃ z, part z x ∧ z ≠ x

variable {Fact : Type} (M : Frame Fact)

def singleton (x : Fact) : Fact → Prop := fun y => y = x

def multiple (S : Fact → Prop) : Prop :=
  ∃ x y, S x ∧ S y ∧ x ≠ y

def E (x : Fact) (S : Fact → Prop) : Prop :=
  (∃ y, (∀ z, S z ↔ z = y) ∧ M.part x y ∧ x ≠ y) ∨
  (x = M.top ∧ multiple S)

def PE (x : Fact) (S : Fact → Prop) : Prop :=
  ∃ z, M.part x z ∧ E M z S

theorem singleton_full_iff (x y : Fact) :
    E M x (singleton y) ↔ M.part x y ∧ x ≠ y := by
  constructor
  · rintro (⟨z, hs, hp, hn⟩ | ⟨_, a, b, ha, hb, hab⟩)
    · have hyz : y = z := (hs y).mp rfl
      exact hyz ▸ ⟨hp, hn⟩
    · exact False.elim (hab (ha.trans hb.symm))
  · intro h
    exact Or.inl ⟨y, fun _ => Iff.rfl, h⟩

theorem singleton_partial_iff (x y : Fact) :
    PE M x (singleton y) ↔ M.part x y ∧ x ≠ y := by
  constructor
  · rintro ⟨z, hxz, hz⟩
    obtain ⟨hzy, hne⟩ := (singleton_full_iff M z y).mp hz
    refine ⟨M.transitive hxz hzy, ?_⟩
    intro heq
    have hyz : M.part y z := heq ▸ hxz
    exact hne (M.antisymmetric hzy hyz)
  · intro h
    exact ⟨x, M.reflexive x, (singleton_full_iff M x y).mpr h⟩

theorem unrestricted_psr (S : Fact → Prop) (hne : ∃ x, S x) :
    ∃ z, E M z S := by
  classical
  obtain ⟨x, hx⟩ := hne
  by_cases hsingle : ∀ y, S y → y = x
  · obtain ⟨z, hp, hn⟩ := M.strict_part x
    refine ⟨z, Or.inl ⟨x, ?_, hp, hn⟩⟩
    intro y
    exact ⟨hsingle y, fun h => h ▸ hx⟩
  · have hm : ∃ y, S y ∧ y ≠ x := by
      apply Classical.byContradiction
      intro h
      apply hsingle
      intro y hy
      apply Classical.byContradiction
      intro hne
      exact h ⟨y, hy, hne⟩
    obtain ⟨y, hy, hn⟩ := hm
    exact ⟨M.top, Or.inr ⟨rfl, y, x, hy, hx, hn⟩⟩

theorem no_self (x : Fact) : ¬ E M x (singleton x) := by
  intro h
  exact ((singleton_full_iff M x x).mp h).2 rfl

theorem full_is_partial {x : Fact} {S : Fact → Prop}
    (h : E M x S) : PE M x S := ⟨x, M.reflexive x, h⟩

theorem partial_downward_closed {x y : Fact} {S : Fact → Prop}
    (hxy : M.part x y) (h : PE M y S) : PE M x S := by
  obtain ⟨z, hyz, hz⟩ := h
  exact ⟨z, M.transitive hxy hyz, hz⟩

theorem all_partially_explain_multiple (x : Fact) (S : Fact → Prop)
    (hm : multiple S) : PE M x S :=
  ⟨M.top, M.below_top x, Or.inr ⟨rfl, hm⟩⟩

theorem no_extended_circles (x : Fact) (S : Fact → Prop) (y : Fact)
    (_hpartial : PE M x S) (_hmember : S y) (_hne : y ≠ x)
    (hnotpart : ¬ M.part y x) : ¬ PE M y (singleton x) := by
  intro h
  exact hnotpart ((singleton_partial_iff M y x).mp h).1

theorem complete_transitivity_fails :
    ¬ (∀ x S y T, E M x S → S y → E M y T → E M x T) := by
  intro ht
  obtain ⟨z, hp, hn⟩ := M.strict_part M.top
  let S : Fact → Prop := fun x => x = M.top ∨ x = z
  have hS : E M M.top S := Or.inr
    ⟨rfl, z, M.top, Or.inr rfl, Or.inl rfl, hn⟩
  have hz : E M z (singleton M.top) :=
    (singleton_full_iff M z M.top).mpr ⟨hp, hn⟩
  exact no_self M M.top
    (ht M.top S z (singleton M.top) hS (Or.inr rfl) hz)

theorem partial_transitivity_fails :
    ¬ (∀ x S y T, PE M x S → S y → E M y T → PE M x T) := by
  intro ht
  obtain ⟨z, hp, hn⟩ := M.strict_part M.top
  let S : Fact → Prop := fun x => x = M.top ∨ x = z
  have hS : E M M.top S := Or.inr
    ⟨rfl, z, M.top, Or.inr rfl, Or.inl rfl, hn⟩
  have hz : E M z (singleton M.top) :=
    (singleton_full_iff M z M.top).mpr ⟨hp, hn⟩
  have h := ht M.top S z (singleton M.top)
    (full_is_partial M hS) (Or.inr rfl) hz
  exact ((singleton_partial_iff M M.top M.top).mp h).2 rfl

theorem member_projection_fails :
    ¬ (∀ x S y, E M x S → S y → E M x (singleton y)) := by
  intro hproj
  obtain ⟨z, _hp, hn⟩ := M.strict_part M.top
  let S : Fact → Prop := fun x => x = M.top ∨ x = z
  have hS : E M M.top S := Or.inr
    ⟨rfl, z, M.top, Or.inr rfl, Or.inl rfl, hn⟩
  exact no_self M M.top (hproj M.top S M.top hS (Or.inl rfl))

end SupplementedPluralControl

#print axioms SupplementedPluralControl.singleton_partial_iff
#print axioms SupplementedPluralControl.unrestricted_psr
#print axioms SupplementedPluralControl.no_extended_circles
#print axioms SupplementedPluralControl.no_self
#print axioms SupplementedPluralControl.complete_transitivity_fails
#print axioms SupplementedPluralControl.partial_transitivity_fails
#print axioms SupplementedPluralControl.member_projection_fails
