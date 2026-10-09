import OriginalBearerBridge
import Mathlib.Data.Fintype.EquivFin

/-! Explicit counterinterpretations, not metaphysical possibility certificates.
A controls use all of Nat with strict ancestry x<y (supplier y to receiver x).
No finite truncation, self-edge, or causal cycle is used. -/
namespace Orthemology.Tranche20.OriginalBearerBridge.Controls

open Orthemology.Tranche3.SourceIdentity

set_option synthInstance.maxSize 8192
set_option maxRecDepth 4096

/-- Original source false persists; received effect true is genuinely contingent. -/
def positive : Framework Bool Bool Bool Unit where
  actual := false
  existsAt := fun w g => g = false ∨ w = false
  wholeReceived := fun w g => w = false ∧ g = true
  dep := fun w y x => w = false ∧ y = false ∧ x = true
  resourceActual := fun _ => True
  resourceReceived := fun r => r = true
  intrinsic := fun g r => g = r
  targetReceived := fun _ => True
  relevant := fun r _ => r = false

/-- All seven premises hold together; the effect makes need/receipt nonvacuous. -/
theorem positive_full : FullPremises positive := by
  constructor
  all_goals
    simp only [Completion, Realisation, SupportTransport, ReceiptRepresentation,
      ContingencyNeed, ConstitutiveReception, ActualOriginalResource, positive,
      Received, Necessary]
    decide

theorem positive_nonvacuous :
    positive.targetReceived () ∧
    ActualOriginalResource positive false ∧
    positive.resourceActual true ∧ positive.resourceReceived true ∧
    positive.intrinsic true true ∧ positive.wholeReceived false true ∧
    positive.existsAt false true ∧ ¬ Necessary positive.existsAt true ∧
    ActualWholeOriginal positive false ∧
    Necessary positive.existsAt false ∧ UniformRoot positive.existsAt positive.dep false := by
  simp only [ActualOriginalResource, ActualWholeOriginal, positive,
    Necessary, UniformRoot, Root, Received]
  decide

theorem positive_same_witness :
    ∃ t r g, OriginalWitness positive t r g ∧ Necessary positive.existsAt g ∧
      UniformRoot positive.existsAt positive.dep g ∧ EssentialNonreceipt positive g :=
  abc_same_witness positive positive_full

/-- The common infinite all-received control frame. The resource is a different type. -/
def natFrame (received : Prop) (instantiates : Nat → Prop) : Framework Unit Nat Unit Unit where
  actual := ()
  existsAt := fun _ _ => True
  wholeReceived := fun _ _ => True
  dep := fun _ supplier receiver => receiver < supplier
  resourceActual := fun _ => True
  resourceReceived := fun _ => received
  intrinsic := fun g _ => instantiates g
  targetReceived := fun _ => True
  relevant := fun _ _ => True

theorem nat_representation (received : Prop) (instantiates : Nat → Prop) :
    ReceiptRepresentation (natFrame received instantiates) := by
  intro w g
  constructor
  · intro _
    exact ⟨g + 1, Nat.lt_succ_self g⟩
  · intro _
    trivial

theorem nat_need (received : Prop) (instantiates : Nat → Prop) :
    ContingencyNeed (natFrame received instantiates) := by
  intro g _ _
  trivial

theorem nat_constitution (received : Prop) (instantiates : Nat → Prop) :
    ConstitutiveReception (natFrame received instantiates) := by
  intro g _ w _
  trivial

theorem nat_no_original (received : Prop) (instantiates : Nat → Prop) :
    ¬ ∃ g, ActualWholeOriginal (natFrame received instantiates) g := by
  rintro ⟨g, _, notReceived⟩
  exact notReceived trivial

/-- Every n has an actual supplier n+1; the transitive ancestry is strict.
Strict transitivity rules out all nonempty directed cycles. The carrier is Nat,
not a finite sample; the separate Infinite instance below is kernel checked. -/
theorem nat_ancestry_strict_and_everywhere_supplied (received : Prop)
    (instantiates : Nat → Prop) :
    (∀ w x, ¬ (natFrame received instantiates).dep w x x) ∧
    (∀ w a b c, (natFrame received instantiates).dep w a b →
      (natFrame received instantiates).dep w b c →
      (natFrame received instantiates).dep w a c) ∧
    (∀ w x, (natFrame received instantiates).dep w (x + 1) x) := by
  refine ⟨?_, ?_, ?_⟩
  · intro w x
    exact Nat.lt_irrefl x
  · intro w a b c hab hbc
    exact Nat.lt_trans hbc hab
  · intro w x
    exact Nat.lt_succ_self x

theorem nat_carrier_genuinely_infinite : Infinite Nat := inferInstance

def withoutCompletion := natFrame True (fun g => g = 0)
def withoutRealisation := natFrame False (fun _ => False)
def withoutSupport := natFrame False (fun g => g = 0)

/-- Remove only completion from the six major premises plus occurrence. -/
theorem remove_completion :
    (∃ t, withoutCompletion.targetReceived t) ∧
    Realisation withoutCompletion ∧ SupportTransport withoutCompletion ∧
    ReceiptRepresentation withoutCompletion ∧ ContingencyNeed withoutCompletion ∧
    ConstitutiveReception withoutCompletion ∧ ¬ Completion withoutCompletion ∧
    ¬ ∃ g, ActualWholeOriginal withoutCompletion g := by
  refine ⟨⟨(), trivial⟩, ?_, ?_, nat_representation _ _, nat_need _ _,
    nat_constitution _ _, ?_, nat_no_original _ _⟩
  · intro r _
    exact ⟨0, trivial, rfl⟩
  · intro g r _ _ _
    trivial
  · intro completion
    obtain ⟨r, _, original⟩ := completion () trivial
    exact original.2 trivial

/-- Original resources alone do not realise an original bearer. -/
theorem remove_realisation :
    (∃ t, withoutRealisation.targetReceived t) ∧
    Completion withoutRealisation ∧ SupportTransport withoutRealisation ∧
    ReceiptRepresentation withoutRealisation ∧ ContingencyNeed withoutRealisation ∧
    ConstitutiveReception withoutRealisation ∧ ¬ Realisation withoutRealisation ∧
    ¬ ∃ g, ActualWholeOriginal withoutRealisation g := by
  refine ⟨⟨(), trivial⟩, ?_, ?_, nat_representation _ _, nat_need _ _,
    nat_constitution _ _, ?_, nat_no_original _ _⟩
  · intro t _
    exact ⟨(), trivial, trivial, id⟩
  · intro g r _ intrinsic _
    exact intrinsic
  · intro realisation
    obtain ⟨g, _, intrinsic⟩ := realisation () trivial
    exact intrinsic

/-- A realised locally original resource can have a received bearer if support
transport is omitted; whole originality does not follow from realisation alone. -/
theorem remove_support :
    (∃ t, withoutSupport.targetReceived t) ∧
    Completion withoutSupport ∧ Realisation withoutSupport ∧
    ReceiptRepresentation withoutSupport ∧ ContingencyNeed withoutSupport ∧
    ConstitutiveReception withoutSupport ∧ ¬ SupportTransport withoutSupport ∧
    ¬ ∃ g, ActualWholeOriginal withoutSupport g := by
  refine ⟨⟨(), trivial⟩, ?_, ?_, nat_representation _ _, nat_need _ _,
    nat_constitution _ _, ?_, nat_no_original _ _⟩
  · intro t _
    exact ⟨(), trivial, trivial, id⟩
  · intro r _
    exact ⟨0, trivial, rfl⟩
  · intro support
    exact support 0 () trivial rfl trivial

/-- Both actual bearers can be absent; all A premises and generic reception hold. -/
def withoutNeed : Framework Bool Bool Bool Unit :=
  { positive with existsAt := fun w _ => w = false }

theorem remove_contingency_need :
    (∃ t, withoutNeed.targetReceived t) ∧ Completion withoutNeed ∧
    Realisation withoutNeed ∧ SupportTransport withoutNeed ∧
    ReceiptRepresentation withoutNeed ∧ ConstitutiveReception withoutNeed ∧
    ¬ ContingencyNeed withoutNeed ∧ ¬ ∃ g, Necessary withoutNeed.existsAt g := by
  simp only [Completion, Realisation, SupportTransport, ReceiptRepresentation,
    ConstitutiveReception, ContingencyNeed, ActualOriginalResource,
    withoutNeed, positive, Received, Necessary]
  decide

/-- C's conditional-on-existence target survives even when B's necessity fails. -/
theorem conditional_nonreceipt_without_necessity :
    ActualWholeOriginal withoutNeed false ∧ EssentialNonreceipt withoutNeed false ∧
    ¬ Necessary withoutNeed.existsAt false := by
  simp only [ActualWholeOriginal, EssentialNonreceipt, Necessary, withoutNeed, positive]
  decide

/-- Necessary individuals swap receipt mode; each world remains acyclic. -/
def withoutConstitution : Framework Bool Bool Bool Unit :=
  { positive with
    existsAt := fun _ _ => True
    wholeReceived := fun w g => g = !w
    dep := fun w y x => y = w ∧ x = !w }

theorem remove_constitutive_reception :
    (∃ t, withoutConstitution.targetReceived t) ∧ Completion withoutConstitution ∧
    Realisation withoutConstitution ∧ SupportTransport withoutConstitution ∧
    ReceiptRepresentation withoutConstitution ∧ ContingencyNeed withoutConstitution ∧
    ¬ ConstitutiveReception withoutConstitution ∧
    (∀ g, Necessary withoutConstitution.existsAt g) ∧
    ¬ ∃ g, UniformRoot withoutConstitution.existsAt withoutConstitution.dep g := by
  simp only [Completion, Realisation, SupportTransport, ReceiptRepresentation,
    ConstitutiveReception, ContingencyNeed, ActualOriginalResource,
    withoutConstitution, positive, Received, Necessary, UniformRoot, Root]
  decide

theorem modal_controls_worldwise_acyclic :
    (∀ w x, ¬ withoutNeed.dep w x x) ∧
    (∀ w a b c, withoutNeed.dep w a b → withoutNeed.dep w b c → withoutNeed.dep w a c) ∧
    (∀ w x, ¬ withoutConstitution.dep w x x) ∧
    (∀ w a b c, withoutConstitution.dep w a b → withoutConstitution.dep w b c →
      withoutConstitution.dep w a c) := by
  simp only [withoutNeed, withoutConstitution, positive]
  decide

end Orthemology.Tranche20.OriginalBearerBridge.Controls
