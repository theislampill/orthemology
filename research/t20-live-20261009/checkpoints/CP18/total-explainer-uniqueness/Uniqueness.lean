import Std

/- Source-relative conditional results. No metaphysical realization of E,
   productive creation, bearer identity, or necessity is asserted. -/
namespace TotalExplainerUniqueness

universe u
abbrev Plurality (Fact : Type u) := Fact → Prop

def singleton {Fact : Type u} (x : Fact) : Plurality Fact := fun y => y = x

def PE {Fact : Type u} (part : Fact → Fact → Prop)
    (E : Fact → Plurality Fact → Prop) (x : Fact) (S : Plurality Fact) : Prop :=
  ∃ z, part x z ∧ E z S

def NoExtendedCircles {Fact : Type u} (part : Fact → Fact → Prop)
    (P : Fact → Plurality Fact → Prop) : Prop :=
  ∀ x S y, P x S → S y → y ≠ x → ¬ part y x → ¬ P y (singleton x)

def MemberProjection {Fact : Type u} (E : Fact → Plurality Fact → Prop) : Prop :=
  ∀ x S y, E x S → S y → E x (singleton y)

-- P may be any relation. Its source-side definition is not needed here.
theorem mutual_partial_singletons_equal {Fact : Type u}
    (part : Fact → Fact → Prop) (P : Fact → Plurality Fact → Prop)
    (antisymmetric : ∀ x y, part x y → part y x → x = y)
    (no_extended : NoExtendedCircles part P)
    (q r : Fact) (hqr : P q (singleton r)) (hrq : P r (singleton q)) :
    q = r := by
  classical
  apply Classical.byContradiction
  intro hne
  have hqrpart : part q r := by
    apply Classical.byContradiction
    intro hnot
    exact no_extended r (singleton q) q hrq rfl hne hnot hqr
  have hrqnot : ¬ part r q := fun h => hne (antisymmetric q r hqrpart h)
  exact no_extended q (singleton r) r hqr rfl (Ne.symm hne) hrqnot hrq

-- Only cross-membership is used, even when the two targets differ.
theorem cross_target_explainers_equal {Fact : Type u}
    (part : Fact → Fact → Prop) (E : Fact → Plurality Fact → Prop)
    (reflexive : ∀ x, part x x)
    (antisymmetric : ∀ x y, part x y → part y x → x = y)
    (projection : MemberProjection E)
    (no_extended : NoExtendedCircles part (PE part E))
    (F G : Plurality Fact) (q r : Fact)
    (hq : E q F) (hr : E r G) (r_in_F : F r) (q_in_G : G q) : q = r := by
  apply mutual_partial_singletons_equal part (PE part E) antisymmetric no_extended q r
  · exact ⟨q, reflexive q, projection q F r hq r_in_F⟩
  · exact ⟨r, reflexive r, projection r G q hr q_in_G⟩

-- For a common target, q and r must both belong to that target.
-- Neither global totality, PSR, nor either transitivity axiom is assumed.
theorem member_inclusive_target_unique {Fact : Type u}
    (part : Fact → Fact → Prop) (E : Fact → Plurality Fact → Prop)
    (reflexive : ∀ x, part x x)
    (antisymmetric : ∀ x y, part x y → part y x → x = y)
    (projection : MemberProjection E)
    (no_extended : NoExtendedCircles part (PE part E))
    (F : Plurality Fact) (q r : Fact)
    (hq : E q F) (hr : E r F) (q_in_F : F q) (r_in_F : F r) : q = r := by
  exact cross_target_explainers_equal part E reflexive antisymmetric projection
    no_extended F F q r hq hr r_in_F q_in_F

-- This conditional existence-and-uniqueness theorem is unbounded in domain size.
theorem unrestricted_psr_unique_total {Fact : Type u}
    (inhabited : Nonempty Fact)
    (part : Fact → Fact → Prop) (E : Fact → Plurality Fact → Prop)
    (reflexive : ∀ x, part x x)
    (antisymmetric : ∀ x y, part x y → part y x → x = y)
    (projection : MemberProjection E)
    (no_extended : NoExtendedCircles part (PE part E))
    (psr : ∀ S, (∃ x, S x) → ∃ q, E q S) :
    ∃ q, E q (fun _ => True) ∧ ∀ r, E r (fun _ => True) → r = q := by
  obtain ⟨a⟩ := inhabited
  obtain ⟨q, hq⟩ := psr (fun _ => True) ⟨a, trivial⟩
  refine ⟨q, hq, ?_⟩
  intro r hr
  exact member_inclusive_target_unique part E reflexive antisymmetric projection
    no_extended (fun _ => True) r q hr hq trivial trivial

end TotalExplainerUniqueness

#print axioms TotalExplainerUniqueness.mutual_partial_singletons_equal
#print axioms TotalExplainerUniqueness.cross_target_explainers_equal
#print axioms TotalExplainerUniqueness.member_inclusive_target_unique
#print axioms TotalExplainerUniqueness.unrestricted_psr_unique_total
