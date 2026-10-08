import GroundedSupport
import Mathlib.Data.Finset.Image

namespace T20Grounded

variable {Label Root : Type}

/-- A cut must hit every complete alternative support, not every marginal root. -/
def Hits (family : Finset (Finset Label)) (cut : Finset Label) : Prop :=
  ∀ support ∈ family, ∃ x ∈ support, x ∈ cut

def MinimalCut (family : Finset (Finset Label)) (cut : Finset Label) : Prop :=
  MinimalFor (Hits family) cut

 theorem hits_mono {family : Finset (Finset Label)} {A B : Finset Label}
    (hAB : A ⊆ B) (hA : Hits family A) : Hits family B := by
  intro support hs
  obtain ⟨x, hx, hA⟩ := hA support hs
  exact ⟨x, hx, hAB hA⟩

variable [DecidableEq Root]

def imageFamily (origin : Label → Root) (family : Finset (Finset Label)) :
    Finset (Finset Root) := family.image (fun support => support.image origin)

/-- Every mapped label cut is a root cut; its alleged optimality need not survive. -/
 theorem image_of_cut (origin : Label → Root) (family : Finset (Finset Label))
    (cut : Finset Label) (hcut : Hits family cut) :
    Hits (imageFamily origin family) (cut.image origin) := by
  intro support hs
  obtain ⟨source, hsource, rfl⟩ := Finset.mem_image.mp hs
  obtain ⟨x, hx, hc⟩ := hcut source hsource
  exact ⟨origin x, Finset.mem_image.mpr ⟨x, hx, rfl⟩,
    Finset.mem_image.mpr ⟨x, hc, rfl⟩⟩

 theorem pullback_of_cut (origin : Label → Root) (family : Finset (Finset Label))
    (U : Finset Label) (hbounded : ∀ S ∈ family, S ⊆ U)
    (cut : Finset Root) (hcut : Hits (imageFamily origin family) cut) :
    Hits family (U.filter (fun x => origin x ∈ cut)) := by
  intro support hs
  obtain ⟨y, hy, hc⟩ := hcut (support.image origin)
    (Finset.mem_image.mpr ⟨support, hs, rfl⟩)
  obtain ⟨x, hx, heq⟩ := Finset.mem_image.mp hy
  refine ⟨x, hx, Finset.mem_filter.mpr ⟨hbounded support hs hx, ?_⟩⟩
  simpa only [heq] using hc

/-- Finiteness supplies a minimal label cut inside the pullback. -/
 theorem minimal_root_cut_lifts (origin : Label → Root)
    (family : Finset (Finset Label)) (U : Finset Label)
    (hbounded : ∀ S ∈ family, S ⊆ U) (cut : Finset Root)
    (hmin : MinimalCut (imageFamily origin family) cut) :
    ∃ labels, labels ⊆ U ∧ MinimalCut family labels ∧
      labels.image origin = cut := by
  have hpull := pullback_of_cut origin family U hbounded cut hmin.1
  obtain ⟨labels, hlabels, hminimal⟩ := exists_minimal_subset (Hits family)
    (U.filter (fun x => origin x ∈ cut)) hpull
  have hboundedLabels : labels ⊆ U := by
    intro x hx
    exact (Finset.mem_filter.mp (hlabels hx)).1
  have himage : labels.image origin ⊆ cut := by
    intro y hy
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hy
    exact (Finset.mem_filter.mp (hlabels hx)).2
  have hroot := image_of_cut origin family labels hminimal.1
  exact ⟨labels, hboundedLabels, hminimal,
    Finset.Subset.antisymm himage (hmin.2 _ himage hroot)⟩

/-- Membership in the image of the complete inclusion-minimal label-cut archive. -/
def ArchivedImage (origin : Label → Root) (family : Finset (Finset Label))
    (U : Finset Label) (cut : Finset Root) : Prop :=
  ∃ labels, labels ⊆ U ∧ MinimalCut family labels ∧
    labels.image origin = cut

/-- One label archive is sufficient for every later supplied origin map.
    Minimisation of image cuts is inclusion minimisation, not label cost truncation. -/
 theorem minimal_root_iff_minimal_archived_image (origin : Label → Root)
    (family : Finset (Finset Label)) (U : Finset Label)
    (hbounded : ∀ S ∈ family, S ⊆ U) (cut : Finset Root) :
    MinimalCut (imageFamily origin family) cut ↔
      ArchivedImage origin family U cut ∧
      ∀ other, ArchivedImage origin family U other →
        other ⊆ cut → cut ⊆ other := by
  constructor
  · intro hmin
    refine ⟨minimal_root_cut_lifts origin family U hbounded cut hmin, ?_⟩
    intro other harch hsub
    obtain ⟨labels, _, hlabels, heq⟩ := harch
    apply hmin.2 other hsub
    rw [← heq]
    exact image_of_cut origin family labels hlabels.1
  · rintro ⟨harch, hminimal⟩
    have hcut : Hits (imageFamily origin family) cut := by
      obtain ⟨labels, _, hlabels, heq⟩ := harch
      rw [← heq]
      exact image_of_cut origin family labels hlabels.1
    refine ⟨hcut, ?_⟩
    intro other hother hhit
    obtain ⟨small, hsmall, hsmallMin⟩ := exists_minimal_subset
      (Hits (imageFamily origin family)) other hhit
    have hsmallArchived := minimal_root_cut_lifts origin family U hbounded
      small hsmallMin
    have hcutSmall := hminimal small hsmallArchived
      (Finset.Subset.trans hsmall hother)
    exact Finset.Subset.trans hcutSmall hsmall

end T20Grounded
