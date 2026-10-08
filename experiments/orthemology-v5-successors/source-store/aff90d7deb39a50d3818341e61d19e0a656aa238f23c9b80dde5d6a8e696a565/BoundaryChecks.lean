import ModalAbilityControl
set_option linter.constructorNameAsVariable false
set_option synthInstance.maxSize 100000
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

namespace IndependentAnchoredReview
open AnchoredSourceBridge AnchoredSourceBridge.Controls

/- These tests were authored independently after the candidate was sealed.
They import fresh trust-zero outputs and do not alter candidate sources. -/

-- Independent general reductions expose which hypotheses do actual work.
theorem labels_unique_with_positive_anchor
    {S : Type u} {E : Type v} {C : Type w} (A : Account S E C)
    (g : S) (a : E) (coverage : GlobalCoverage A g)
    (cnd : FieldCND A) (positive : Positive A a)
    (connected : ConnectedFrom A a) :
    ∀ e, A.Field e → ∀ s, Complete A s e → s = g := by
  intro e fe s cs
  exact complete_providers_equal_at_positive A g s e fe
    (positive_along_path A (connected e fe) positive) (coverage e fe) cs cnd

theorem common_source_actually_participates_everywhere
    {S : Type u} {E : Type v} {C : Type w} (A : Account S E C)
    (g : S) (a : E) (coverage : GlobalCoverage A g)
    (use : UseSound A) (positive : Positive A a)
    (connected : ConnectedFrom A a) :
    ∀ e, A.Field e → A.ActualOriginal g e := by
  intro e fe
  obtain ⟨c, req⟩ := positive_along_path A (connected e fe) positive
  exact use g e fe ⟨c, req, coverage e fe c req⟩

-- Without qualification, classification/conformance may both be vacuous.
def unqualified : Account S E C := { split with Qualified := fun _ => False }

-- The graph cannot certify that its named occurrences or requisites are real.
def fictitious : Account S E C :=
  { full with ActualOccurrence := fun _ => False, Operative := fun _ _ => False }

-- Exactly the inventory-exhaustiveness certificate is deleted here.
def omittedRequisite : Account S E C :=
  { faithful singleton oneReq onlyG with Operative := splitReq }

-- The anchor exists in actuality but is invisible in the represented account.
def invisibleAnchor : Account S E C :=
  { unanchored with ActualOriginal := fun s e =>
      (s = .g ∧ e = .e) ∨ tableRep splitReq unanchoredEntire s e }

-- Widening the field changes the exact CND and coverage obligations.
def expanded : Account S E C := { outsideDuplicate with Field := fun _ => True }

-- ConnectedFrom is vacuous on an empty field; it never creates an anchor.
def noField : Account S E C := { duplicate with Field := fun _ => False }

-- Two qualified sources can satisfy the norm in separate components.
def qualifiedSeparated : Account S E C :=
  { separated with Qualified := fun s => s = .g ∨ s = .h }

macro "independent_finite" : tactic => `(tactic|
  (simp only [unqualified, fictitious, omittedRequisite, invisibleAnchor, expanded,
    noField, qualifiedSeparated, Interpretation, FixedMode, Admissible,
    RequisiteSound, RequisiteExhaustive, UseSound, RoleApplicable, Visible,
    Classification, Conformance, ModeSatisfaction, SourceMode, CND, FieldCND,
    GlobalCoverage, ActualAnchor, ActualUnique, Positive, Complete,
    RepresentedParticipation, tableRep, fixture, faithful, Controls.singleton, pairField,
    mixedField, splitReq, splitEntire, split, oneReq, duplicateEntire, duplicate,
    unanchoredEntire, unanchored, separateReq, separated, onlyG, mixedReq,
    fullEntire, full, outsideDuplicateEntire, outsideDuplicate] <;> decide))

theorem qualification_is_not_dispensed_with :
    Interpretation unqualified ∧ Classification unqualified .g ∧
    Conformance unqualified .g ∧ RoleApplicable unqualified .g ∧
    ActualAnchor unqualified .g .e ∧ FieldCND unqualified ∧
    ConnectedFrom unqualified .e ∧ ¬ unqualified.Qualified .g ∧
    ¬ GlobalCoverage unqualified .g := by
  refine ⟨by independent_finite, by independent_finite, by independent_finite,
    by independent_finite, by independent_finite, by independent_finite, ?_,
    by independent_finite, by independent_finite⟩
  exact singleton_connected unqualified (by independent_finite)

theorem valid_graph_does_not_certify_real_occurrences :
    FixedMode fictitious ∧ UseSound fictitious ∧ Visible fictitious ∧
    FieldCND fictitious ∧ ActualAnchor fictitious .g .e ∧
    ConnectedFrom fictitious .e ∧ GlobalCoverage fictitious .g ∧
    ActualUnique fictitious .g ∧ ¬ Admissible fictitious ∧
    ¬ RequisiteSound fictitious := by
  refine ⟨by independent_finite, by independent_finite, by independent_finite,
    by independent_finite, by independent_finite, ?_, by independent_finite,
    by independent_finite, by independent_finite, by independent_finite⟩
  exact hub_connected fictitious .e .k (by independent_finite) (by independent_finite)
    ⟨.a, by independent_finite, by independent_finite⟩ (by
      intro e fe
      cases e with
      | e => exact Or.inl rfl
      | f => exact Or.inr ⟨.b, by independent_finite, by independent_finite⟩
      | k => exact Or.inr ⟨.a, by independent_finite, by independent_finite⟩
      | z => exact False.elim (fe rfl))

theorem coverage_and_visibility_do_not_fill_an_omitted_requisite :
    Admissible omittedRequisite ∧ RequisiteSound omittedRequisite ∧
    UseSound omittedRequisite ∧ Visible omittedRequisite ∧
    FixedMode omittedRequisite ∧ FieldCND omittedRequisite ∧
    ActualAnchor omittedRequisite .g .e ∧ ConnectedFrom omittedRequisite .e ∧
    GlobalCoverage omittedRequisite .g ∧ ActualUnique omittedRequisite .g ∧
    omittedRequisite.Operative .e .b ∧ ¬ omittedRequisite.Req .e .b ∧
    ¬ RequisiteExhaustive omittedRequisite := by
  refine ⟨by independent_finite, by independent_finite, by independent_finite,
    by independent_finite, by independent_finite, by independent_finite,
    by independent_finite, ?_, by independent_finite, by independent_finite,
    by independent_finite, by independent_finite, by independent_finite⟩
  exact singleton_connected omittedRequisite (by independent_finite)

theorem participation_variant_needs_a_visible_anchor :
    ActualAnchor invisibleAnchor .g .e ∧ ConnectedFrom invisibleAnchor .e ∧
    SourceMode invisibleAnchor .g ∧ UseSound invisibleAnchor ∧
    ¬ Visible invisibleAnchor ∧ ¬ GlobalCoverage invisibleAnchor .g := by
  refine ⟨by independent_finite, ?_, by independent_finite,
    by independent_finite, by independent_finite, by independent_finite⟩
  exact singleton_connected invisibleAnchor (by independent_finite)

theorem extending_scope_requires_new_certificates :
    FieldCND outsideDuplicate ∧ ¬ FieldCND expanded ∧
    GlobalCoverage outsideDuplicate .g ∧ ¬ GlobalCoverage expanded .g ∧
    ActualUnique outsideDuplicate .g ∧ ¬ ActualUnique expanded .g := by
  independent_finite

theorem empty_field_neither_anchors_nor_uniquely_identifies :
    ConnectedFrom noField .e ∧ FieldCND noField ∧
    (∀ s, GlobalCoverage noField s) ∧
    ¬ (∃ s e, ActualAnchor noField s e) ∧
    ¬ (∀ s, GlobalCoverage noField s → s = S.g) := by
  refine ⟨?_, by independent_finite, by independent_finite,
    by independent_finite, by independent_finite⟩
  intro e fe
  exact False.elim fe

theorem qualification_does_not_connect_two_components :
    Interpretation qualifiedSeparated ∧ FieldCND qualifiedSeparated ∧
    qualifiedSeparated.Qualified .g ∧ qualifiedSeparated.Qualified .h ∧
    Classification qualifiedSeparated .g ∧ Conformance qualifiedSeparated .g ∧
    Classification qualifiedSeparated .h ∧ Conformance qualifiedSeparated .h ∧
    RoleApplicable qualifiedSeparated .g ∧ RoleApplicable qualifiedSeparated .h ∧
    ActualAnchor qualifiedSeparated .g .e ∧ ActualAnchor qualifiedSeparated .h .f ∧
    S.g ≠ S.h ∧ ¬ (∃ s, GlobalCoverage qualifiedSeparated s) := by
  independent_finite

-- No finite-source assumption creates existence when the source type is empty.
def noSources : Account Empty Unit Unit where
  Field := fun _ => False
  ActualOccurrence := fun _ => True
  Req := fun _ _ => False
  Operative := fun _ _ => False
  EntireOrig := fun s _ => nomatch s
  ActualOriginal := fun s _ => nomatch s
  ModeRole := fun s _ => nomatch s
  Qualified := fun s => nomatch s
  ModeDefect := fun s _ => nomatch s

theorem no_source_witness_no_existence :
    ¬ (∃ s, GlobalCoverage noSources s) := by
  intro ⟨s, _⟩
  exact nomatch s

-- Explicit finite-world witnesses are exclusive solo production in the table,
-- not just labels called ability. Token identity remains history-sensitive.
open AnchoredSourceBridge.Controls.ModalAbility
theorem alternative_witnesses_really_are_exclusive :
    (∀ t p s, supplies .alternativeA s t p ↔ s = S.g) ∧
    (∀ t p s, supplies .alternativeB s t p ↔ s = S.h) ∧
    (∀ s t, Ability s t ↔ s = S.g ∨ s = S.h) ∧
    (∀ s r c, EntireToken s c → EntireToken r c → s = r) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp only [supplies]; decide
  · simp only [supplies]; decide
  · simp only [Ability, ActualSolo, supplies]; decide
  · intro s r c hs hr
    exact intact_finite_power_differentiated_actual_production.1
      c.history s r c.target c.piece hs hr

-- This model is countably infinite, with a separate occurrence and respect type.
structure InfiniteEvent where index : Nat
structure InfiniteRespect where index : Nat
def infiniteAccount : Account S InfiniteEvent InfiniteRespect where
  Field := fun _ => True
  ActualOccurrence := fun _ => True
  Req := fun e c => c.index = e.index ∨ c.index = e.index + 1
  Operative := fun e c => c.index = e.index ∨ c.index = e.index + 1
  EntireOrig := fun s _ => s = .g
  ActualOriginal := fun s _ => s = .g
  ModeRole := fun s _ => s = .g
  Qualified := fun s => s = .g
  ModeDefect := fun _ _ => False

theorem path_append {S : Type u} {E : Type v} {C : Type w}
    (A : Account S E C) {e f z : E} (left : Path A e f) (right : Path A f z) :
    Path A e z := by
  induction left with
  | refl _ => exact right
  | step he hf edge _ ih => exact Path.step he hf edge (ih right)

theorem infinite_chain_connected : ConnectedFrom infiniteAccount ⟨0⟩ := by
  intro e _
  obtain ⟨n⟩ := e
  induction n with
  | zero => exact Path.refl True.intro
  | succ n ih =>
    exact path_append infiniteAccount (ih True.intro)
      (Path.step True.intro True.intro
        ⟨⟨n+1⟩, Or.inr rfl, Or.inl rfl⟩ (Path.refl True.intro))

theorem infinite_field_principal_application :
    GlobalCoverage infiniteAccount .g ∧ ActualUnique infiniteAccount .g ∧
    (∀ e, infiniteAccount.Field e → ∀ s, Complete infiniteAccount s e → s = .g) := by
  have result := guarded_common_original_provider infiniteAccount .g ⟨0⟩
    (fun _ _ => True.intro) (fun _ _ _ req => req) (fun _ _ _ req => req)
    rfl
    (by intro _ e _ _ incomplete; exact incomplete (fun _ _ => rfl))
    (by intro _ _ _ _ defect; exact defect)
    (by intro _ _ _ represented; exact represented.choose_spec.2)
    (fun _ _ actual => actual)
    (fun s e _ actual => ⟨⟨e.index⟩, Or.inl rfl, actual⟩)
    ⟨True.intro, rfl⟩ infinite_chain_connected
    (fun _ _ _ _ _ _ hs ht => hs.trans ht.symm)
  exact result.2.2.2

end IndependentAnchoredReview
