import GroundedSupport
import Mathlib.Data.Finset.Image

namespace T20Grounded

variable {Label Root Claim : Type} [DecidableEq Root]

/-- One actual root may support several separately identified carrier facts. -/
def QuotientBase (origin : Label → Root) (U : Finset Label)
    (base : Label → Claim → Prop) : Root → Claim → Prop :=
  fun r c => ∃ label ∈ U, origin label = r ∧ base label c

/-- Folding fixed carrier aliases is exact for grounded inference when availability
    is pulled back to all and only carriers of an available actual root. -/
 theorem quotient_derivable_iff (origin : Label → Root) (U : Finset Label)
    (base : Label → Claim → Prop) (rule : Finset Claim → Claim → Prop)
    (available : Finset Root) (c : Claim) :
    Derivable (QuotientBase origin U base) rule available c ↔
      Derivable base rule (U.filter (fun label => origin label ∈ available)) c := by
  constructor
  · intro h
    induction h with
    | root hav hb =>
      obtain ⟨label, hU, heq, hbase⟩ := hb
      apply Derivable.root (Finset.mem_filter.mpr ⟨hU, ?_⟩) hbase
      simpa only [heq] using hav
    | step hr hp ih => exact .step hr (fun p hm => ih p hm)
  · intro h
    induction h with
    | root hav hb =>
      obtain ⟨hU, hroot⟩ := Finset.mem_filter.mp hav
      exact .root hroot ⟨_, hU, rfl, hb⟩
    | step hr hp ih => exact .step hr (fun p hm => ih p hm)

 theorem image_derivation (origin : Label → Root) (U : Finset Label)
    (base : Label → Claim → Prop) (rule : Finset Claim → Claim → Prop)
    (labels : Finset Label) (hU : labels ⊆ U) (c : Claim)
    (h : Derivable base rule labels c) :
    Derivable (QuotientBase origin U base) rule (labels.image origin) c := by
  induction h with
  | root hav hb =>
    exact .root (Finset.mem_image.mpr ⟨_, hav, rfl⟩) ⟨_, hU hav, rfl, hb⟩
  | step hr hp ih => exact .step hr (fun p hm => ih p hm)

/-- Every minimal actual-root support is the image of some inclusion-minimal
    carrier support. A carrier-cardinality minimum is not asserted. -/
 theorem minimal_root_support_lifts (origin : Label → Root) (U : Finset Label)
    (base : Label → Claim → Prop) (rule : Finset Claim → Claim → Prop)
    (roots : Finset Root) (c : Claim)
    (hmin : MinimalFor (fun A => Derivable (QuotientBase origin U base) rule A c) roots) :
    ∃ labels, labels ⊆ U ∧
      MinimalFor (fun A => Derivable base rule A c) labels ∧
      labels.image origin = roots := by
  have hpull := (quotient_derivable_iff origin U base rule roots c).mp hmin.1
  obtain ⟨labels, hlabels, hminimal⟩ := exists_minimal_subset
    (fun A => Derivable base rule A c)
    (U.filter (fun label => origin label ∈ roots)) hpull
  have hbound : labels ⊆ U := by
    intro label hl
    exact (Finset.mem_filter.mp (hlabels hl)).1
  have himage : labels.image origin ⊆ roots := by
    intro root hr
    obtain ⟨label, hl, rfl⟩ := Finset.mem_image.mp hr
    exact (Finset.mem_filter.mp (hlabels hl)).2
  have hderive := image_derivation origin U base rule labels hbound c hminimal.1
  exact ⟨labels, hbound, hminimal,
    Finset.Subset.antisymm himage (hmin.2 _ himage hderive)⟩

end T20Grounded
