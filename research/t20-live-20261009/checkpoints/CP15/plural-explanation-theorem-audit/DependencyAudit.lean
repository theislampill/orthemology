import Std

/- Bounded audit of the displayed plural principles in Koons and Pruss (2020).
   Facts are already actual. Pluralities are predicates; admitted pluralities
   in the unrestricted corollary are every nonempty predicate. No metaphysical
   interpretation, modal claims, or uniqueness/independence claims are encoded. -/
namespace PluralExplanationAudit

universe u
abbrev Plurality (Fact : Type u) := Fact → Prop

def singleton {Fact : Type u} (q : Fact) : Plurality Fact := fun x => x = q

def CompleteTransitivity {Fact : Type u}
    (E : Fact → Plurality Fact → Prop) : Prop :=
  ∀ x S y T, E x S → S y → E y T → E x T

-- Exact local dependence: a total explainer and an explanation of its singleton.
theorem total_explainer_self {Fact : Type u}
    (E : Fact → Plurality Fact → Prop) (F : Plurality Fact) (q : Fact)
    (total : ∀ r, F r) (explains_total : E q F)
    (singleton_explained : ∃ r, E r (singleton q))
    (trans : CompleteTransitivity E) : E q (singleton q) := by
  obtain ⟨r, hr⟩ := singleton_explained
  exact trans q F r (singleton q) explains_total (total r) hr

-- Nonemptiness is explicit; unrestricted PSR is used only twice.
theorem unrestricted_has_self_explaining_total_explainer
    {Fact : Type u} (inhabited : Nonempty Fact)
    (E : Fact → Plurality Fact → Prop)
    (psr : ∀ S, (∃ x, S x) → ∃ q, E q S)
    (trans : CompleteTransitivity E) :
    ∃ q, E q (fun _ => True) ∧ E q (singleton q) := by
  obtain ⟨a⟩ := inhabited
  obtain ⟨q, hq⟩ := psr (fun _ => True) ⟨a, trivial⟩
  refine ⟨q, hq, total_explainer_self E (fun _ => True) q
    (fun _ => trivial) hq ?_ trans⟩
  exact psr (singleton q) ⟨q, rfl⟩

namespace ChainControl

def Part (x y : Nat) : Prop := y ≤ x

def ProperPart (x y : Nat) : Prop := Part x y ∧ x ≠ y

def Multiple (S : Plurality Nat) : Prop :=
  ∃ a b, S a ∧ S b ∧ a ≠ b

def E (x : Nat) (S : Plurality Nat) : Prop :=
  (∃ n, x = n + 1 ∧ ∀ k, S k ↔ k = n) ∨
  (x = 0 ∧ Multiple S)

-- This is exactly source-side partial explanation, not a free relation.
def PE (x : Nat) (S : Plurality Nat) : Prop :=
  ∃ z, Part x z ∧ E z S

theorem part_reflexive (x : Nat) : Part x x := Nat.le_refl x

theorem part_transitive {x y z : Nat} (hxy : Part x y)
    (hyz : Part y z) : Part x z := Nat.le_trans hyz hxy

theorem part_antisymmetric {x y : Nat} (hxy : Part x y)
    (hyx : Part y x) : x = y := Nat.le_antisymm hyx hxy

theorem next_is_proper_part (n : Nat) : ProperPart (n+1) n := by
  constructor <;> simp [Part]

theorem unrestricted_psr (S : Plurality Nat) (hne : ∃ n, S n) :
    ∃ x, E x S := by
  classical
  obtain ⟨n, hn⟩ := hne
  by_cases hsingle : ∀ k, S k → k = n
  · refine ⟨n+1, Or.inl ⟨n, rfl, ?_⟩⟩
    intro k
    exact ⟨hsingle k, fun h => h ▸ hn⟩
  · have hm : ∃ m, S m ∧ m ≠ n := by
      apply Classical.byContradiction
      intro h
      apply hsingle
      intro m hm
      apply Classical.byContradiction
      intro hmn
      exact h ⟨m, hm, hmn⟩
    obtain ⟨m, hm, hmn⟩ := hm
    exact ⟨0, Or.inr ⟨rfl, m, n, hm, hn, hmn⟩⟩

theorem singleton_explanation_iff (x n : Nat) :
    E x (singleton n) ↔ x = n+1 := by
  constructor
  · intro h
    rcases h with ⟨k, hx, hk⟩ | ⟨_, a, b, ha, hb, hab⟩
    · have hnk : n = k := (hk n).mp rfl
      exact hnk ▸ hx
    · exact False.elim (hab (ha.trans hb.symm))
  · intro hx
    exact Or.inl ⟨n, hx, fun _ => Iff.rfl⟩

theorem full_implies_partial {x : Nat} {S : Plurality Nat}
    (h : E x S) : PE x S := ⟨x, part_reflexive x, h⟩

theorem partial_downward_closed {x y : Nat} {S : Plurality Nat}
    (hxy : Part x y) (h : PE y S) : PE x S := by
  obtain ⟨z, hyz, hz⟩ := h
  exact ⟨z, part_transitive hxy hyz, hz⟩

theorem singleton_partial_iff (x n : Nat) :
    PE x (singleton n) ↔ n+1 ≤ x := by
  constructor
  · rintro ⟨z, hz, he⟩
    have heq := (singleton_explanation_iff z n).mp he
    exact heq ▸ hz
  · intro h
    exact ⟨n+1, h, (singleton_explanation_iff (n+1) n).mpr rfl⟩

theorem every_fact_partially_explains_multiple (x : Nat)
    (S : Plurality Nat) (h : Multiple S) : PE x S :=
  ⟨0, Nat.zero_le x, Or.inr ⟨rfl, h⟩⟩

-- The explicit x≠y premise is redundant since Part is reflexive.
theorem no_extended_circles (x : Nat) (S : Plurality Nat) (y : Nat)
    (_hpartial : PE x S) (_hmember : S y)
    (_hdistinct : y ≠ x) (hnotpart : ¬ Part y x) :
    ¬ PE y (singleton x) := by
  intro hback
  have h := (singleton_partial_iff y x).mp hback
  apply hnotpart
  exact Nat.le_trans (Nat.le_succ x) h

theorem no_self_explanation (n : Nat) : ¬ E n (singleton n) := by
  intro h
  have h := (singleton_explanation_iff n n).mp h
  omega

theorem no_partially_self_explanatory_fact (n : Nat) :
    ¬ ∃ z, ProperPart n z ∧ E z (singleton n) := by
  rintro ⟨z, ⟨hp, _⟩, he⟩
  have hz := (singleton_explanation_iff z n).mp he
  unfold Part at hp
  omega

def pair : Plurality Nat := fun x => x = 0 ∨ x = 1

theorem zero_explains_pair : E 0 pair := by
  exact Or.inr ⟨rfl, 0, 1, Or.inl rfl, Or.inr rfl, by decide⟩

theorem one_explains_zero : E 1 (singleton 0) :=
  (singleton_explanation_iff 1 0).mpr rfl

theorem complete_transitivity_fails : ¬ CompleteTransitivity E := by
  intro ht
  exact no_self_explanation 0
    (ht 0 pair 1 (singleton 0) zero_explains_pair (Or.inr rfl)
      one_explains_zero)

theorem partial_transitivity_fails :
    ¬ (∀ x S y T, PE x S → S y → E y T → PE x T) := by
  intro ht
  have h := ht 0 pair 1 (singleton 0)
    (full_implies_partial zero_explains_pair) (Or.inr rfl) one_explains_zero
  have hbad := (singleton_partial_iff 0 0).mp h
  omega

theorem member_projection_fails :
    ¬ (∀ x S y, E x S → S y → E x (singleton y)) := by
  intro hp
  exact no_self_explanation 0
    (hp 0 pair 0 zero_explains_pair (Or.inl rfl))

end ChainControl
end PluralExplanationAudit

#print axioms PluralExplanationAudit.total_explainer_self
#print axioms PluralExplanationAudit.unrestricted_has_self_explaining_total_explainer
#print axioms PluralExplanationAudit.ChainControl.unrestricted_psr
#print axioms PluralExplanationAudit.ChainControl.no_extended_circles
#print axioms PluralExplanationAudit.ChainControl.no_self_explanation
#print axioms PluralExplanationAudit.ChainControl.complete_transitivity_fails
#print axioms PluralExplanationAudit.ChainControl.partial_transitivity_fails
#print axioms PluralExplanationAudit.ChainControl.member_projection_fails
