/-!
Read-only Lean-oriented proposal for the Deep BV common-intervention criterion.

Status in this packet:
* declaration source drafted;
* parser NOT RUN;
* elaborator NOT RUN;
* kernel NOT RUN;
* axiom report NOT RUN.

The core theorem is deliberately independent of intervention eligibility,
source/world transfer, proper function, and metaphysical predicates.
-/

universe uM uP uQ uA uI uS uO uR

namespace BoundedChallengerB

section FibreFactorization

variable {M : Type uM} {Profile : Type uP} {QVal : Type uQ}

/-- Equality of registered profiles induces the observational setoid. -/
def profileSetoid (E : M → Profile) : Setoid M where
  r m m' := E m = E m'
  iseqv := {
    refl := fun _ => rfl
    symm := fun h => h.symm
    trans := fun h₁ h₂ => h₁.trans h₂
  }

/-- The canonical quotient by complete-profile equality. -/
def ProfileQuotient (E : M → Profile) : Type uM :=
  Quotient (profileSetoid E)

/-- The target is constant on every complete experiment-profile fibre. -/
def FiberConstant (E : M → Profile) (Q : M → QVal) : Prop :=
  ∀ ⦃m m' : M⦄, E m = E m' → Q m = Q m'

/-- Exact decoding through the quotient, avoiding off-range codomain choices. -/
def FactorsThroughProfileQuotient (E : M → Profile) (Q : M → QVal) : Prop :=
  ∃ d : ProfileQuotient E → QVal,
    ∀ m : M, d (Quotient.mk (profileSetoid E) m) = Q m

/-- Elementary quotient/fibre factorization. No finiteness assumption is used. -/
theorem factorsThroughProfileQuotient_iff_fiberConstant
    (E : M → Profile) (Q : M → QVal) :
    FactorsThroughProfileQuotient E Q ↔ FiberConstant E Q := by
  constructor
  · rintro ⟨d, hd⟩ m m' hE
    calc
      Q m = d (Quotient.mk (profileSetoid E) m) := (hd m).symm
      _ = d (Quotient.mk (profileSetoid E) m') := congrArg d (Quotient.sound hE)
      _ = Q m' := hd m'
  · intro h
    refine ⟨Quotient.lift Q ?_, ?_⟩
    · intro a b hab
      exact h hab
    · intro m
      rfl

/-- A decoder through the quotient is unique. -/
theorem profileQuotient_decoder_unique
    (E : M → Profile) (Q : M → QVal)
    (d₁ d₂ : ProfileQuotient E → QVal)
    (h₁ : ∀ m : M, d₁ (Quotient.mk (profileSetoid E) m) = Q m)
    (h₂ : ∀ m : M, d₂ (Quotient.mk (profileSetoid E) m) = Q m) :
    d₁ = d₂ := by
  funext x
  refine Quotient.inductionOn x ?_
  intro m
  calc
    d₁ (Quotient.mk (profileSetoid E) m) = Q m := h₁ m
    _ = d₂ (Quotient.mk (profileSetoid E) m) := (h₂ m).symm

/--
Factoring through the entire declared `Profile` codomain is a stronger interface
than factoring through the attained image/quotient. Its converse needs an
off-range extension condition, such as `Nonempty QVal`, or a surjective profile.
-/
def FactorsThroughFullProfileCodomain
    (E : M → Profile) (Q : M → QVal) : Prop :=
  ∃ d : Profile → QVal, ∀ m : M, d (E m) = Q m

theorem fullProfileFactor_implies_fiberConstant
    (E : M → Profile) (Q : M → QVal) :
    FactorsThroughFullProfileCodomain E Q → FiberConstant E Q := by
  rintro ⟨d, hd⟩ m m' hE
  calc
    Q m = d (E m) := (hd m).symm
    _ = d (E m') := congrArg d hE
    _ = Q m' := hd m'

end FibreFactorization

section GuardSpecification

/-- Protocol scope must be frozen rather than silently mixing one-shot and adaptive claims. -/
inductive ProtocolKind where
  | oneShot
  | adaptive

/--
A proposed data/certificate object for the *application guards*. These fields do
not occur in, and are not proved by, the quotient theorem above.
-/
structure CommonInterventionSpec
    (Architecture : Type uA)
    (AbstractIntervention : Type uI)
    (AbstractSemantics : Type uS)
    (ComparableOutput : Type uO) where
  Implementation : Architecture → Type uR
  RawOutput : Architecture → Type uR
  implement : (a : Architecture) → AbstractIntervention → Implementation a
  abstractSemantics : AbstractIntervention → AbstractSemantics
  implementationSemantics :
    (a : Architecture) → Implementation a → AbstractSemantics
  semanticsPreserving :
    ∀ (a : Architecture) (i : AbstractIntervention),
      implementationSemantics a (implement a i) = abstractSemantics i
  encodeOutput : (a : Architecture) → RawOutput a → ComparableOutput
  outputSemanticsComparable : Prop
  sourceEligible : Prop
  versionEligible : Prop
  authorized : Prop
  resourceRealizable : Prop
  physicallyRealizable : Prop
  targetBlindFreezeAudited : Prop
  protocolKind : ProtocolKind

/-- A proof-carrying wrapper for the guard propositions in the specification. -/
structure CommonInterventionCertificate
    (Architecture : Type uA)
    (AbstractIntervention : Type uI)
    (AbstractSemantics : Type uS)
    (ComparableOutput : Type uO) where
  spec : CommonInterventionSpec
    Architecture AbstractIntervention AbstractSemantics ComparableOutput
  outputSemanticsComparableProof : spec.outputSemanticsComparable
  sourceEligibleProof : spec.sourceEligible
  versionEligibleProof : spec.versionEligible
  authorizedProof : spec.authorized
  resourceRealizableProof : spec.resourceRealizable
  physicallyRealizableProof : spec.physicallyRealizable
  targetBlindFreezeAuditedProof : spec.targetBlindFreezeAudited

/--
Source text, translation, morphology, syntax, occurrence meaning, formal
predicate, world truth, bearer applicability, recipient warrant, authority, and
revelation remain independent coordinates. No projection is supplied here.
-/
structure SourceWorldCoordinates
    (SourceText Translation Morphology Syntax OccurrenceMeaning FormalPredicate
      WorldTruth BearerApplicability RecipientWarrant Authority Revelation : Type uR) where
  sourceText : SourceText
  translation : Translation
  morphology : Morphology
  syntax : Syntax
  occurrenceMeaning : OccurrenceMeaning
  formalPredicate : FormalPredicate
  worldTruth : WorldTruth
  bearerApplicability : BearerApplicability
  recipientWarrant : RecipientWarrant
  authority : Authority
  revelation : Revelation

end GuardSpecification

end BoundedChallengerB
