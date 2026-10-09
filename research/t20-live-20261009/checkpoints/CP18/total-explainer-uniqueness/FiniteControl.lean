import Std

/- A four-fact relational control, with all nonempty predicate pluralities.
   This does not claim that the stipulated relation is a metaphysical world. -/
namespace TotalExplainerFiniteControl

inductive Fact where
  | q | a | b | e
  deriving DecidableEq, Repr
open Fact
abbrev Plurality := Fact → Prop

def singleton (x : Fact) : Plurality := fun y => y = x
def Part (x y : Fact) : Prop := x = y

def E (x : Fact) (S : Plurality) : Prop :=
  (∃ y, S y) ∧ (x = q ∨ ((x = a ∨ x = b) ∧ ∀ y, S y → y = e))

def PE (x : Fact) (S : Plurality) : Prop :=
  ∃ z, Part x z ∧ E z S

theorem part_order :
    (∀ x, Part x x) ∧
    (∀ x y z, Part x y → Part y z → Part x z) ∧
    (∀ x y, Part x y → Part y x → x = y) := by
  exact ⟨fun _ => rfl, fun _ _ _ hxy hyz => hxy.trans hyz, fun _ _ hxy _ => hxy⟩

theorem partial_iff_full (x : Fact) (S : Plurality) : PE x S ↔ E x S := by
  constructor
  · rintro ⟨z, hxz, hz⟩
    exact hxz.symm ▸ hz
  · intro h
    exact ⟨x, rfl, h⟩

theorem full_implies_partial (x : Fact) (S : Plurality) (h : E x S) : PE x S := by
  exact (partial_iff_full x S).mpr h

theorem partial_source_closure (x y : Fact) (S : Plurality)
    (hpart : Part x y) (h : PE y S) : PE x S := by
  exact hpart.symm ▸ h

theorem unrestricted_psr (S : Plurality) (hne : ∃ x, S x) : ∃ x, E x S := by
  exact ⟨q, hne, Or.inl rfl⟩

theorem no_empty_explanation (x : Fact) : ¬ E x (fun _ => False) := by
  rintro ⟨⟨y, hy⟩, _⟩
  exact hy

theorem e_explains_nothing (S : Plurality) : ¬ E e S := by
  simp [E]

theorem complete_transitivity (x : Fact) (S : Plurality) (y : Fact) (T : Plurality)
    (hx : E x S) (hy : S y) (hyt : E y T) : E x T := by
  rcases hx with ⟨_, hq | ⟨hab, hlocal⟩⟩
  · exact ⟨hyt.1, Or.inl hq⟩
  · have hye := hlocal y hy
    exact False.elim (e_explains_nothing T (hye ▸ hyt))

theorem partial_transitivity (x : Fact) (S : Plurality) (y : Fact) (T : Plurality)
    (hx : PE x S) (hy : S y) (hyt : E y T) : PE x T := by
  exact (partial_iff_full x T).mpr
    (complete_transitivity x S y T ((partial_iff_full x S).mp hx) hy hyt)

theorem member_projection (x : Fact) (S : Plurality) (y : Fact)
    (hx : E x S) (hy : S y) : E x (singleton y) := by
  refine ⟨⟨y, rfl⟩, ?_⟩
  rcases hx.2 with hq | ⟨hab, hlocal⟩
  · exact Or.inl hq
  · refine Or.inr ⟨hab, ?_⟩
    intro z hz
    exact hz.trans (hlocal y hy)

-- The full displayed distribution principle: members AND parts of members.
theorem distribution (x : Fact) (S : Plurality) (y z : Fact)
    (hx : E x S) (hy : S y) (hz : z = y ∨ Part z y) : E x (singleton z) := by
  have hzy : z = y := hz.elim id id
  exact hzy.symm ▸ member_projection x S y hx hy

theorem no_extended_circles (x : Fact) (S : Plurality) (y : Fact)
    (hx : PE x S) (hy : S y) (hne : y ≠ x) (_hnotpart : ¬ Part y x) :
    ¬ PE y (singleton x) := by
  intro hback
  have hxfull := (partial_iff_full x S).mp hx
  have hyfull := (partial_iff_full y (singleton x)).mp hback
  rcases hxfull.2 with hq | ⟨hab, hlocal⟩
  · rcases hyfull.2 with hyq | ⟨_, htarget⟩
    · exact hne (hyq.trans hq.symm)
    · have hxe := htarget x rfl
      have hqe : q = e := hq.symm.trans hxe
      cases hqe
  · have hye := hlocal y hy
    exact e_explains_nothing (singleton x) (hye ▸ hyfull)

theorem unique_total_explainer :
    E q (fun _ => True) ∧ ∀ x, E x (fun _ => True) → x = q := by
  constructor
  · exact ⟨⟨q, trivial⟩, Or.inl rfl⟩
  · intro x hx
    rcases hx.2 with hq | ⟨_, hlocal⟩
    · exact hq
    · have hqe := hlocal q trivial
      cases hqe

theorem two_distinct_explainers_of_narrow_target :
    a ≠ b ∧ E a (singleton e) ∧ E b (singleton e) ∧
    ¬ singleton e a ∧ ¬ singleton e b := by
  simp [E, singleton]

-- There are THREE full explainers of {e}: q, a, b. Do not say exactly two.
theorem local_explainers_exactly (x : Fact) :
    E x (singleton e) ↔ x = q ∨ x = a ∨ x = b := by
  simp [E, singleton, or_assoc]

-- The local explainers are external to the narrow target, even by parthood.
theorem restricted_external_explainers :
    ∀ S, (∃ y, S y) → (∀ y, S y → y = e) →
      E a S ∧ E b S ∧ (∀ y, S y → a ≠ y ∧ ¬ Part a y ∧ b ≠ y ∧ ¬ Part b y) := by
  intro S hne hlocal
  refine ⟨⟨hne, Or.inr ⟨Or.inl rfl, hlocal⟩⟩,
    ⟨hne, Or.inr ⟨Or.inr rfl, hlocal⟩⟩, ?_⟩
  intro y hy
  have hye := hlocal y hy
  subst y
  simp [Part]

end TotalExplainerFiniteControl

#print axioms TotalExplainerFiniteControl.part_order
#print axioms TotalExplainerFiniteControl.partial_iff_full
#print axioms TotalExplainerFiniteControl.partial_source_closure
#print axioms TotalExplainerFiniteControl.unrestricted_psr
#print axioms TotalExplainerFiniteControl.no_empty_explanation
#print axioms TotalExplainerFiniteControl.complete_transitivity
#print axioms TotalExplainerFiniteControl.partial_transitivity
#print axioms TotalExplainerFiniteControl.distribution
#print axioms TotalExplainerFiniteControl.no_extended_circles
#print axioms TotalExplainerFiniteControl.unique_total_explainer
#print axioms TotalExplainerFiniteControl.two_distinct_explainers_of_narrow_target
#print axioms TotalExplainerFiniteControl.local_explainers_exactly
#print axioms TotalExplainerFiniteControl.restricted_external_explainers
