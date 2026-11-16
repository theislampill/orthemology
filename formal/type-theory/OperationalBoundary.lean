/- Operational-to-Hurkens correspondence, not a newly postulated SCUU axiom.
   Authored source; UNCOMPILED. The actual exported calls and their totality/
   returned-value beta condition are specified first. The forbidden full section
   package is then extracted from those operations, using Classical.choice.
   Internal realisability All is NOT any of these unrestricted full sections. -/
import OperationalKernel
import HurkensBoundary

namespace OrthemologyV4
open OrthemologyV2Boundary
universe r u

abbrev FullSections := (X : Type r) → GirardFamily (fun Y : Type r => Y) X

structure SCUUAt (O : API.{max (r+1) u}) where
  «at» : O.State
  small : Type r
  packCall : O.Handle (ULift.{max (r+1) u} FullSections.{r})
    (ULift.{max (r+1) u} small)
  unpackCall : O.Handle (ULift.{max (r+1) u} small)
    (ULift.{max (r+1) u} FullSections.{r})
  packTotal : ∀ f : FullSections.{r}, ∃ x : small,
    O.invoke «at» packCall ⟨f⟩ = some ⟨x⟩
  unpackTotal : ∀ x : small, ∃ f : FullSections.{r},
    O.invoke «at» unpackCall ⟨x⟩ = some ⟨f⟩
  returnedBeta : ∀ (f : FullSections.{r}) (x : small),
    O.invoke «at» packCall ⟨f⟩ = some ⟨x⟩ →
    O.invoke «at» unpackCall ⟨x⟩ = some ⟨f⟩

/-- Full section abstraction and evaluation are extracted from actual calls;
    none of pack/unpack/beta is a custom foundational axiom. -/
theorem not_SCUUAt (O : API.{max (r+1) u}) : ¬ Nonempty (SCUUAt.{r,u} O) := by
  intro existsCapability
  obtain ⟨cap⟩ := existsCapability
  let pack (f : FullSections.{r}) : cap.small := Classical.choose (cap.packTotal f)
  let unpack (x : cap.small) : FullSections.{r} := Classical.choose (cap.unpackTotal x)
  have beta (f : FullSections.{r}) (X : Type r) : unpack (pack f) X = f X := by
    have first := Classical.choose_spec (cap.packTotal f)
    have second := Classical.choose_spec (cap.unpackTotal (pack f))
    have expected := cap.returnedBeta f (pack f) first
    have same := Option.some.inj (second.symm.trans expected)
    exact congrArg (fun q : ULift.{max (r+1) u} FullSections.{r} => q.down X) same
  exact no_self_product (fun X : Type r => X) cap.small pack unpack beta

/-- Ordinary positive and negative constructions are combined only AFTER their
    clauses are proved. This is a formal-source target, NOT a current kernel claim.
    The named positive scope is the Plan schema, not all ambient functions. -/
theorem mainWitnessAt : ∃ O : API.{max (r+1) u}, OWOU O ∧ ¬ Nonempty (SCUUAt.{r,u} O) :=
  ⟨operationalAPI, positive_OWOU, not_SCUUAt operationalAPI⟩

end OrthemologyV4
