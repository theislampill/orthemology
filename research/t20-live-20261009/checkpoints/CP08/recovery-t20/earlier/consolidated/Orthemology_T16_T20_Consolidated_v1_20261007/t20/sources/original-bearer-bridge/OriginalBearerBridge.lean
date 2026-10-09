import SourceIdentityDerived

/-!
# T20 original-resource/bearer interface

The new work is the typed A bridge. B and C below call the retained T3 theorems;
they are not new deductions or machine proofs of metaphysical premise warrant.
`wholeReceived` is broad whole-existence reception. Its correspondence to the
binary inherited `dep` is an explicit, restricted representation assumption.
Resource tokens are concrete intrinsic instantiations in the SAME existential
respect. There is no fact-to-bearer theorem and no bearer-to-attribute causal edge.
-/
namespace Orthemology.Tranche20.OriginalBearerBridge


structure Framework (W B R T : Type*) where
  actual : W
  existsAt : W → B → Prop
  wholeReceived : W → B → Prop
  dep : W → B → B → Prop
  resourceActual : R → Prop
  resourceReceived : R → Prop
  intrinsic : B → R → Prop
  targetReceived : T → Prop
  relevant : R → T → Prop

variable {W B R T : Type*}

def ActualOriginalResource (s : Framework W B R T) (r : R) : Prop :=
  s.resourceActual r ∧ ¬ s.resourceReceived r

def ActualWholeOriginal (s : Framework W B R T) (g : B) : Prop :=
  s.existsAt s.actual g ∧ ¬ s.wholeReceived s.actual g

def Completion (s : Framework W B R T) : Prop :=
  ∀ t, s.targetReceived t → ∃ r, s.relevant r t ∧ ActualOriginalResource s r

def Realisation (s : Framework W B R T) : Prop :=
  ∀ r, s.resourceActual r → ∃ g, s.existsAt s.actual g ∧ s.intrinsic g r

def SupportTransport (s : Framework W B R T) : Prop :=
  ∀ g r, s.existsAt s.actual g → s.intrinsic g r →
    s.wholeReceived s.actual g → s.resourceReceived r

/-- A representation/adoption restriction; not a theorem about arbitrary grounds. -/
def ReceiptRepresentation (s : Framework W B R T) : Prop :=
  ∀ w g, s.wholeReceived w g ↔ Orthemology.Tranche3.SourceIdentity.Received s.dep w g

/-- The inherited interface is general; its particular g-instance does the work. -/
def ContingencyNeed (s : Framework W B R T) : Prop :=
  ∀ g, s.existsAt s.actual g → ¬ Orthemology.Tranche3.SourceIdentity.Necessary s.existsAt g →
    s.wholeReceived s.actual g

/-- Generic constitution, not a conclusion-specific backward-transfer axiom. -/
def ConstitutiveReception (s : Framework W B R T) : Prop :=
  ∀ g, (∃ w, s.wholeReceived w g) →
    ∀ v, s.existsAt v g → s.wholeReceived v g

def EssentialNonreceipt (s : Framework W B R T) (g : B) : Prop :=
  ∀ w, s.existsAt w g → ¬ s.wholeReceived w g

def OriginalWitness (s : Framework W B R T) (t : T) (r : R) (g : B) : Prop :=
  s.targetReceived t ∧ s.relevant r t ∧ ActualOriginalResource s r ∧
    s.intrinsic g r ∧ ActualWholeOriginal s g

structure FullPremises (s : Framework W B R T) : Prop where
  occurrence : ∃ t, s.targetReceived t
  completion : Completion s
  realisation : Realisation s
  support : SupportTransport s
  representation : ReceiptRepresentation s
  need : ContingencyNeed s
  constitution : ConstitutiveReception s

/-- A's new resource/bearer bridge. No modal or representation premise is used. -/
theorem original_bearer_of_resource (s : Framework W B R T) (r : R)
    (original : ActualOriginalResource s r)
    (realisation : Realisation s) (support : SupportTransport s) :
    ∃ g, s.intrinsic g r ∧ ActualWholeOriginal s g := by
  obtain ⟨g, actual, intrinsic⟩ := realisation r original.1
  exact ⟨g, intrinsic, actual, fun received =>
    original.2 (support g r actual intrinsic received)⟩

/-- Positive actual completion supplies the resource to which realisation applies. -/
theorem original_bearer_of_completion (s : Framework W B R T) (t : T)
    (occurrence : s.targetReceived t) (completion : Completion s)
    (realisation : Realisation s) (support : SupportTransport s) :
    ∃ r g, OriginalWitness s t r g := by
  obtain ⟨r, relevant, original⟩ := completion t occurrence
  obtain ⟨g, intrinsic, bearer⟩ :=
    original_bearer_of_resource s r original realisation support
  exact ⟨r, g, occurrence, relevant, original, intrinsic, bearer⟩

/-- Typed adapter only: broad roothood enters the retained binary interface. -/
theorem root_to_inherited (s : Framework W B R T)
    (representation : ReceiptRepresentation s) (g : B)
    (original : ActualWholeOriginal s g) :
    Orthemology.Tranche3.SourceIdentity.Root s.existsAt s.dep s.actual g :=
  ⟨original.1, fun received => original.2 ((representation s.actual g).mpr received)⟩

theorem need_to_inherited (s : Framework W B R T)
    (representation : ReceiptRepresentation s) (need : ContingencyNeed s) :
    ∀ g, s.existsAt s.actual g → ¬ Orthemology.Tranche3.SourceIdentity.Necessary s.existsAt g →
      Orthemology.Tranche3.SourceIdentity.Received s.dep s.actual g := by
  intro g actual contingent
  exact (representation s.actual g).mp (need g actual contingent)

theorem constitution_to_inherited (s : Framework W B R T)
    (representation : ReceiptRepresentation s)
    (constitution : ConstitutiveReception s) :
    Orthemology.Tranche3.SourceIdentity.GenericReception s.existsAt s.dep := by
  rintro g ⟨w, received⟩ v hex
  exact (representation v g).mp
    (constitution g ⟨w, (representation w g).mpr received⟩ v hex)

/-- Elementary C re-expression: necessity is unnecessary for nonreceipt
conditional on existence. This is no new philosophical warrant. -/
theorem essential_nonreceipt_of_actual_original (s : Framework W B R T) (g : B)
    (original : ActualWholeOriginal s g)
    (constitution : ConstitutiveReception s) : EssentialNonreceipt s g := by
  intro w _ received
  exact original.2 (constitution g ⟨w, received⟩ s.actual original.1)

/-- Composition, keeping the SAME resource and bearer witnesses throughout.
The B and C inferential cores are explicitly inherited function calls. -/
theorem abc_same_witness (s : Framework W B R T) (premises : FullPremises s) :
    ∃ t r g, OriginalWitness s t r g ∧
      Orthemology.Tranche3.SourceIdentity.Necessary s.existsAt g ∧ Orthemology.Tranche3.SourceIdentity.UniformRoot s.existsAt s.dep g ∧
      EssentialNonreceipt s g := by
  obtain ⟨t, occurrence⟩ := premises.occurrence
  obtain ⟨r, g, witness⟩ := original_bearer_of_completion s t occurrence
    premises.completion premises.realisation premises.support
  have root := root_to_inherited s premises.representation g witness.2.2.2.2
  have necessary := Orthemology.Tranche3.SourceIdentity.necessary_of_actual_root s.existsAt s.dep s.actual g root
    (need_to_inherited s premises.representation premises.need)
  have uniform := Orthemology.Tranche3.SourceIdentity.uniform_of_necessary_actual_root s.existsAt s.dep s.actual g root
    necessary (constitution_to_inherited s premises.representation premises.constitution)
  exact ⟨t, r, g, witness, necessary, uniform,
    essential_nonreceipt_of_actual_original s g witness.2.2.2.2 premises.constitution⟩

end Orthemology.Tranche20.OriginalBearerBridge
