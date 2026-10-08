import Init

/-! T20 conditional contribution-incidence bridge. No metaphysical axioms are
postulated. All application claims are parameters. This is not Sixth LocalCover. -/
namespace AnchoredSourceBridge
universe u v w

structure Account (S : Type u) (E : Type v) (C : Type w) where
  Field : E → Prop
  ActualOccurrence : E → Prop
  Req : E → C → Prop
  Operative : E → C → Prop
  EntireOrig : S → C → Prop
  ActualOriginal : S → E → Prop
  ModeRole : S → E → Prop
  Qualified : S → Prop
  ModeDefect : S → E → Prop

variable {S : Type u} {E : Type v} {C : Type w} (A : Account S E C)

def RepresentedParticipation (s : S) (e : E) : Prop :=
  ∃ c, A.Req e c ∧ A.EntireOrig s c

def Complete (s : S) (e : E) : Prop := ∀ c, A.Req e c → A.EntireOrig s c

def GlobalCoverage (s : S) : Prop := ∀ e, A.Field e → Complete A s e

def Admissible : Prop := ∀ e, A.Field e → A.ActualOccurrence e

def RequisiteSound : Prop := ∀ e c, A.Field e → A.Req e c → A.Operative e c

def RequisiteExhaustive : Prop := ∀ e c, A.Field e → A.Operative e c → A.Req e c

def UseSound : Prop := ∀ s e, A.Field e → RepresentedParticipation A s e → A.ActualOriginal s e

def RoleApplicable (g : S) : Prop := ∀ e, A.Field e → A.ActualOriginal g e → A.ModeRole g e

def Visible : Prop := ∀ s e, A.Field e → A.ActualOriginal s e → RepresentedParticipation A s e

def Classification (g : S) : Prop :=
  A.Qualified g → ∀ e, A.Field e → A.ModeRole g e → ¬ Complete A g e → A.ModeDefect g e

def Conformance (g : S) : Prop :=
  A.Qualified g → ∀ e, A.Field e → A.ModeRole g e → ¬ A.ModeDefect g e

/-- Actual satisfaction, not the bare normative requirement or all perfection. -/
def ModeSatisfaction (g : S) : Prop := ∀ e, A.Field e → A.ModeRole g e → Complete A g e

/-- Derived participation-to-coverage implication, with use/role bridges exposed. -/
def SourceMode (g : S) : Prop := ∀ e, A.Field e → RepresentedParticipation A g e → Complete A g e

def CND : Prop := ∀ s t c, A.EntireOrig s c → A.EntireOrig t c → s = t

/-- Only field-requisite duplication is relevant to field-scoped uniqueness. -/
def FieldCND : Prop := ∀ e, A.Field e → ∀ s t c, A.Req e c →
  A.EntireOrig s c → A.EntireOrig t c → s = t

def Overlap (e f : E) : Prop := ∃ c, A.Req e c ∧ A.Req f c

/-- An incidence path. Symmetric overlap is not reverse efficient causation. -/
inductive Path : E → E → Prop where
  | refl {e} : A.Field e → Path e e
  | step {e f z} : A.Field e → A.Field f → Overlap A e f → Path f z → Path e z

def ConnectedFrom (a : E) : Prop := ∀ e, A.Field e → Path A a e

def ActualAnchor (g : S) (a : E) : Prop := A.Field a ∧ A.ActualOriginal g a

def Positive (e : E) : Prop := ∃ c, A.Req e c

def ActualUnique (g : S) : Prop := ∀ s e, A.Field e → A.ActualOriginal s e → s = g

theorem overlap_symmetric {e f : E} (h : Overlap A e f) : Overlap A f e := by
  obtain ⟨c, he, hf⟩ := h
  exact ⟨c, hf, he⟩

theorem mode_satisfaction_of_classification_conformance (g : S)
    (qualified : A.Qualified g) (classification : Classification A g)
    (conformance : Conformance A g) : ModeSatisfaction A g := by
  intro e field role
  exact Classical.byContradiction (fun incomplete =>
    conformance qualified e field role (classification qualified e field role incomplete))

theorem source_mode_of_mode_satisfaction (g : S) (use : UseSound A)
    (role : RoleApplicable A g) (mode : ModeSatisfaction A g) : SourceMode A g := by
  intro e field represented
  exact mode e field (role e field (use g e field represented))

theorem represented_across_overlap (g : S) {e f : E}
    (complete : Complete A g e) (edge : Overlap A e f) : RepresentedParticipation A g f := by
  obtain ⟨c, he, hf⟩ := edge
  exact ⟨c, hf, complete c he⟩

theorem complete_along_path (g : S) (sourceMode : SourceMode A g)
    {e f : E} (path : Path A e f) : Complete A g e → Complete A g f := by
  induction path with
  | refl _ => exact fun h => h
  | step _ ff edge _ ih =>
    intro complete
    exact ih (sourceMode _ ff (represented_across_overlap A g complete edge))

/-- Core coverage does not need CND, visibility, rival qualification, finiteness,
or any independently interpreted strict ancestry relation. -/
theorem global_coverage_of_anchor (g : S) (a : E)
    (use : UseSound A) (role : RoleApplicable A g) (mode : ModeSatisfaction A g)
    (anchor : ActualAnchor A g a) (connected : ConnectedFrom A a) : GlobalCoverage A g := by
  intro e field
  exact complete_along_path A g (source_mode_of_mode_satisfaction A g use role mode)
    (connected e field) (mode a anchor.1 (role a anchor.1 anchor.2))

theorem global_coverage_of_qualified_anchor (g : S) (a : E)
    (qualified : A.Qualified g) (classification : Classification A g)
    (conformance : Conformance A g) (use : UseSound A) (role : RoleApplicable A g)
    (anchor : ActualAnchor A g a) (connected : ConnectedFrom A a) : GlobalCoverage A g := by
  exact global_coverage_of_anchor A g a use role
    (mode_satisfaction_of_classification_conformance A g qualified classification conformance)
    anchor connected

theorem field_cnd_of_global_cnd (global : CND A) : FieldCND A := by
  intro _ _ s t c _ hs ht
  exact global s t c hs ht

theorem represented_rivals_equal (g : S) (coverage : GlobalCoverage A g) (cnd : FieldCND A)
    (s : S) (e : E) (field : A.Field e) (represented : RepresentedParticipation A s e) : s = g := by
  obtain ⟨c, req, entire⟩ := represented
  exact cnd e field s g c req entire (coverage e field c req)

theorem actual_rivals_equal (g : S) (coverage : GlobalCoverage A g)
    (cnd : FieldCND A) (visible : Visible A) : ActualUnique A g := by
  intro s e field actual
  exact represented_rivals_equal A g coverage cnd s e field (visible s e field actual)

/-- Transparency equivalence at the fixed actual anchor and connected setup.
It does not identify Classification/Conformance with coverage or warrant them. -/
theorem mode_satisfaction_iff_global_coverage (g : S) (a : E)
    (use : UseSound A) (role : RoleApplicable A g)
    (anchor : ActualAnchor A g a) (connected : ConnectedFrom A a) :
    ModeSatisfaction A g ↔ GlobalCoverage A g := by
  constructor
  · exact fun mode => global_coverage_of_anchor A g a use role mode anchor connected
  · exact fun coverage e field _ => coverage e field

/-- The participation variant needs a represented anchor: visibility supplies it. -/
theorem source_mode_iff_global_coverage (g : S) (a : E)
    (visible : Visible A) (anchor : ActualAnchor A g a) (connected : ConnectedFrom A a) :
    SourceMode A g ↔ GlobalCoverage A g := by
  constructor
  · intro mode e field
    exact complete_along_path A g mode (connected e field)
      (mode a anchor.1 (visible g a anchor.1 anchor.2))
  · exact fun coverage e field _ => coverage e field

theorem positive_along_path {e f : E} (path : Path A e f) : Positive A e → Positive A f := by
  induction path with
  | refl _ => exact fun h => h
  | step _ _ edge _ ih =>
    intro _
    obtain ⟨c, _, req⟩ := edge
    exact ih ⟨c, req⟩

theorem every_field_positive (g : S) (a : E) (visible : Visible A)
    (anchor : ActualAnchor A g a) (connected : ConnectedFrom A a) :
    ∀ e, A.Field e → Positive A e := by
  obtain ⟨c, req, _⟩ := visible g a anchor.1 anchor.2
  exact fun e field => positive_along_path A (connected e field) ⟨c, req⟩

theorem complete_providers_equal_at_positive (g s : S) (e : E) (field : A.Field e) (positive : Positive A e)
    (cg : Complete A g e) (cs : Complete A s e) (cnd : FieldCND A) : s = g := by
  obtain ⟨c, req⟩ := positive
  exact cnd e field s g c req (cs c req) (cg c req)

/-- Existence does not require CND; global coverage explicitly furnishes g. -/
theorem complete_provider_exists (g : S) (coverage : GlobalCoverage A g) :
    ∃ s, GlobalCoverage A s := ⟨g, coverage⟩

/-- Uniqueness of merely Complete-labelled sources additionally needs positivity.
An actual anchor alone does not create a requisite; visibility is used here. -/
theorem unique_complete_provider (g : S) (a : E) (coverage : GlobalCoverage A g)
    (cnd : FieldCND A) (visible : Visible A) (anchor : ActualAnchor A g a)
    (connected : ConnectedFrom A a) :
    (∃ s, GlobalCoverage A s) ∧
    (∀ e, A.Field e → ∀ s, Complete A s e → s = g) := by
  refine ⟨complete_provider_exists A g coverage, ?_⟩
  intro e field s cs
  exact complete_providers_equal_at_positive A g s e field
    (every_field_positive A g a visible anchor connected e field) (coverage e field) cs cnd

/-- General interpreted package: mathematical conclusion plus explicit external
interpretation obligations. Admissibility/soundness/exhaustiveness are not proved
by propagation and are therefore premises of this applied wrapper. -/
theorem guarded_common_original_provider (g : S) (a : E)
    (admissible : Admissible A) (reqSound : RequisiteSound A)
    (reqExhaustive : RequisiteExhaustive A) (qualified : A.Qualified g)
    (classification : Classification A g) (conformance : Conformance A g)
    (use : UseSound A) (role : RoleApplicable A g) (visible : Visible A)
    (anchor : ActualAnchor A g a) (connected : ConnectedFrom A a) (cnd : FieldCND A) :
    Admissible A ∧ RequisiteSound A ∧ RequisiteExhaustive A ∧
    GlobalCoverage A g ∧ ActualUnique A g ∧
    (∀ e, A.Field e → ∀ s, Complete A s e → s = g) := by
  have coverage := global_coverage_of_qualified_anchor A g a qualified classification conformance
    use role anchor connected
  exact ⟨admissible, reqSound, reqExhaustive, coverage,
    actual_rivals_equal A g coverage cnd visible,
    (unique_complete_provider A g a coverage cnd visible anchor connected).2⟩

/-- A global CND hypothesis is a stronger sufficient wrapper, not the principal
field-scoped uniqueness requirement. -/
theorem guarded_common_original_provider_of_global_cnd (g : S) (a : E)
    (admissible : Admissible A) (reqSound : RequisiteSound A)
    (reqExhaustive : RequisiteExhaustive A) (qualified : A.Qualified g)
    (classification : Classification A g) (conformance : Conformance A g)
    (use : UseSound A) (role : RoleApplicable A g) (visible : Visible A)
    (anchor : ActualAnchor A g a) (connected : ConnectedFrom A a) (cnd : CND A) :
    Admissible A ∧ RequisiteSound A ∧ RequisiteExhaustive A ∧
    GlobalCoverage A g ∧ ActualUnique A g ∧
    (∀ e, A.Field e → ∀ s, Complete A s e → s = g) := by
  exact guarded_common_original_provider A g a admissible reqSound reqExhaustive qualified
    classification conformance use role visible anchor connected (field_cnd_of_global_cnd A cnd)
end AnchoredSourceBridge
