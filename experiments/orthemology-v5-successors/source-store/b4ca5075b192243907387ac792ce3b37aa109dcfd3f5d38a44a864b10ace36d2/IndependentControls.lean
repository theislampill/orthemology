import GroundedQuotient
import AliasCuts
import OccurrenceControls
import Mathlib.Data.Fintype.Powerset

namespace T20IndependentReview
open T20Grounded

/-- The finite archive is selected before any origin map is supplied. -/
theorem archive_before_origin {Label Root : Type} [DecidableEq Label] [DecidableEq Root]
    (family : Finset (Finset Label)) (U : Finset Label)
    (hbounded : ∀ S ∈ family, S ⊆ U) :
    ∃ archive : Finset (Finset Label),
      (∀ labels, labels ∈ archive ↔ labels ⊆ U ∧ MinimalCut family labels) ∧
      ∀ (origin : Label → Root) (cut : Finset Root),
        MinimalCut (imageFamily origin family) cut ↔
          (∃ labels ∈ archive, labels.image origin = cut) ∧
          ∀ other, (∃ labels ∈ archive, labels.image origin = other) →
            other ⊆ cut → cut ⊆ other := by
  classical
  let archive := U.powerset.filter (MinimalCut family)
  have hmem (labels : Finset Label) :
      labels ∈ archive ↔ labels ⊆ U ∧ MinimalCut family labels := by
    simp [archive]
  have harch (origin : Label → Root) (cut : Finset Root) :
      (∃ labels ∈ archive, labels.image origin = cut) ↔
        ArchivedImage origin family U cut := by
    constructor
    · rintro ⟨labels, hl, heq⟩
      obtain ⟨hb, hm⟩ := (hmem labels).mp hl
      exact ⟨labels, hb, hm, heq⟩
    · rintro ⟨labels, hb, hm, heq⟩
      exact ⟨labels, (hmem labels).mpr ⟨hb, hm⟩, heq⟩
  refine ⟨archive, hmem, ?_⟩
  intro origin cut
  simpa only [harch] using
    minimal_root_iff_minimal_archived_image origin family U hbounded cut

/-- A family containing the empty support has no defeating root-only cut. -/
theorem empty_support_has_no_cut {Label : Type} (cut : Finset Label) :
    ¬ Hits ({∅} : Finset (Finset Label)) cut := by
  intro h
  obtain ⟨x, hx, _⟩ := h ∅ (Finset.mem_singleton.mpr rfl)
  exact Finset.not_mem_empty x hx

/-- The only minimal cut of an empty family is the empty cut. -/
theorem empty_family_minimal_cut {Label : Type} (cut : Finset Label) :
    MinimalCut (∅ : Finset (Finset Label)) cut ↔ cut = ∅ := by
  constructor
  · intro h
    have hhit : Hits (∅ : Finset (Finset Label)) ∅ := by
      intro S hs
      exact False.elim (Finset.not_mem_empty S hs)
    exact Finset.Subset.antisymm (h.2 ∅ (Finset.empty_subset cut) hhit)
      (Finset.empty_subset cut)
  · intro h
    subst cut
    constructor
    · intro S hs
      exact False.elim (Finset.not_mem_empty S hs)
    · intro T _ _
      exact Finset.empty_subset T

inductive EmptyRule : Finset Bool → Bool → Prop
  | explicitAxiom : EmptyRule ∅ true

/-- Grounded means finitely rule-generated; explicit nullary rules are allowed. -/
theorem explicit_axiom_has_empty_support :
    Derivable (fun (_ : Unit) (_ : Bool) => False) EmptyRule ∅ true := by
  apply Derivable.step EmptyRule.explicitAxiom
  intro p hp
  exact False.elim (Finset.not_mem_empty p hp)

/-- Soundness is one-way: an underivable claim need not be false. -/
theorem underivable_can_have_true_meaning :
    (¬ Derivable (fun (_ : Unit) (_ : Bool) => False)
      (fun (_ : Finset Bool) (_ : Bool) => False) ∅ true) ∧
      (fun (_ : Bool) => True) true := by
  constructor
  · intro h
    exact derivable_sound (fun _ => False)
      (fun _ _ _ hb => hb) (fun _ _ hr _ => False.elim hr) h
  · trivial

#print axioms archive_before_origin
#print axioms empty_support_has_no_cut
#print axioms empty_family_minimal_cut
#print axioms explicit_axiom_has_empty_support
#print axioms underivable_can_have_true_meaning
end T20IndependentReview
