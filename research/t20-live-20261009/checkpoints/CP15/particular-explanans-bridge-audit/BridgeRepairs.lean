import Std

/- Local bridge proofs. These expose exactly what the positive inferences use;
   they do not assert the truth or intended interpretation of those premises. -/
namespace ParticularExplanansBridge

variable {Fact : Type}
variable (part : Fact → Fact → Prop)
variable (particular supernatural : Fact → Prop)
variable (E : Fact → (Fact → Prop) → Prop)

def singleton (p : Fact) : Fact → Prop := fun q => q = p

def basic (p : Fact) : Prop := particular p ∧ ¬ supernatural p

def PE (p : Fact) (S : Fact → Prop) : Prop :=
  ∃ y, part p y ∧ E y S

-- The externality in the source is in the opposite direction. This added
-- reverse-part condition alone closes the relevant bridge.
theorem bridge_with_reverse_externality
    (y : Fact)
    (has_particular_part : ∃ p, particular p ∧ part p y)
    (reverse_externality : ∀ p, basic particular supernatural p → ¬ part p y) :
    ∃ p, supernatural p := by
  classical
  obtain ⟨p, hp, hpy⟩ := has_particular_part
  by_cases hs : supernatural p
  · exact ⟨p, hs⟩
  · exact False.elim (reverse_externality p ⟨hp, hs⟩ hpy)

-- E(y,N) and externality are supplied by the displayed restricted PSR.
-- This excludes only the source's proper-part self-explanation; equality is
-- already ruled out by restricted PSR, so a combined stronger ban is unneeded.
theorem bridge_with_no_basic_proper_partial_self
    (y : Fact)
    (explains_all_basic : E y (basic particular supernatural))
    (has_particular_part : ∃ p, particular p ∧ part p y)
    (externality : ∀ p, basic particular supernatural p → y ≠ p)
    (projection : ∀ x S p, E x S → S p → E x (singleton p))
    (no_basic_proper_partial_self : ∀ p, basic particular supernatural p →
      ¬ ∃ z, part p z ∧ p ≠ z ∧ E z (singleton p)) :
    ∃ p, supernatural p := by
  classical
  obtain ⟨p, hp, hpy⟩ := has_particular_part
  by_cases hs : supernatural p
  · exact ⟨p, hs⟩
  · have hb : basic particular supernatural p := ⟨hp, hs⟩
    exact False.elim (no_basic_proper_partial_self p hb
      ⟨y, hpy, Ne.symm (externality p hb),
        projection y _ p explains_all_basic hb⟩)

-- Under the stronger total-all-facts premise, No Extended Circles itself
-- forces every part of the total explainer to be that explainer.
theorem part_of_total_explainer_is_itself
    (F : Fact → Prop) (q p : Fact)
    (total : ∀ x, F x)
    (explains_total : E q F)
    (p_part_q : part p q)
    (antisymmetric : ∀ x y, part x y → part y x → x = y)
    (reflexive : ∀ x, part x x)
    (projection : ∀ x S z, E x S → S z → E x (singleton z))
    (no_extended_circles : ∀ x S z,
      PE part E x S → S z → z ≠ x → ¬ part z x →
        ¬ PE part E z (singleton x)) : p = q := by
  classical
  apply Classical.byContradiction
  intro hne
  have hqne : q ≠ p := Ne.symm hne
  have hnot : ¬ part q p := fun h => hne (antisymmetric p q p_part_q h)
  have hp : PE part E p F := ⟨q, p_part_q, explains_total⟩
  have hq : PE part E q (singleton p) :=
    ⟨q, reflexive q, projection q F p explains_total (total p)⟩
  exact no_extended_circles p F q hp (total q) hqne hnot hq

theorem unrestricted_total_bridge
    (F : Fact → Prop) (q : Fact)
    (total : ∀ x, F x)
    (explains_total : E q F)
    (has_particular_part : ∃ p, particular p ∧ part p q)
    (antisymmetric : ∀ x y, part x y → part y x → x = y)
    (reflexive : ∀ x, part x x)
    (projection : ∀ x S z, E x S → S z → E x (singleton z))
    (no_extended_circles : ∀ x S z,
      PE part E x S → S z → z ≠ x → ¬ part z x →
        ¬ PE part E z (singleton x))
    (no_basic_full_self : ∀ p, basic particular supernatural p →
      ¬ E p (singleton p)) : supernatural q := by
  classical
  obtain ⟨p, hp, hpart⟩ := has_particular_part
  have heq : p = q := part_of_total_explainer_is_itself part E F q p
    total explains_total hpart antisymmetric reflexive projection no_extended_circles
  have hq : particular q := heq ▸ hp
  apply Classical.byContradiction
  intro hs
  exact no_basic_full_self q ⟨hq, hs⟩
    (projection q F q explains_total (total q))

end ParticularExplanansBridge

#print axioms ParticularExplanansBridge.bridge_with_reverse_externality
#print axioms ParticularExplanansBridge.bridge_with_no_basic_proper_partial_self
#print axioms ParticularExplanansBridge.part_of_total_explainer_is_itself
#print axioms ParticularExplanansBridge.unrestricted_total_bridge
