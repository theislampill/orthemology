import Lake
open Lake DSL

package fifteenth_semantic_identity

require mathlib from git "https://github.com/leanprover-community/mathlib4.git" @ "c44e0c8ee63ca166450922a373c7409c5d26b00b"

@[default_target]
lean_lib InheritedBaseline where
  roots := #[
    `AllBaseLaws,
    `AllBinderLaws,
    `AllConstants,
    `AllFiniteComparison,
    `AllInheritedPositiveControls,
    `AllInstantiation,
    `AllMixedAlgebra,
    `AllNucleusSyntax,
    `AllPiLaws,
    `AllPredicates,
    `AllRawRenaming,
    `AllRawSubstitution,
    `AllSemanticSubstitution,
    `AllSigmaLaws,
    `AllSoundness,
    `AllStructural,
    `AllStructuralBase,
    `AllStructuralRename,
    `AllSyntax,
    `AllTermAlgebra,
    `AllTermLemmas,
    `BoundaryResults,
    `EffectsAndDependence,
    `FiniteBridge,
    `InternalPolymorphism,
    `NormalisationAndNumerals,
    `P01Candidates,
    `P01CanonicalCarrierProjection,
    `P01Certificates,
    `P01Confluence,
    `P01ContextualJ,
    `P01CurryParametricity,
    `P01DependentControls,
    `P01DependentCore,
    `P01DependentFundamental,
    `P01DependentModel,
    `P01DependentRepresentation,
    `P01DependentSubstitution,
    `P01Examples,
    `P01LambdaSyntax,
    `P01ModelWitnesses,
    `P01Omega,
    `P01PER,
    `P01Polynomials,
    `P01RecursiveModel,
    `P01SNReflection,
    `P01SystemF,
    `P01Translation,
    `P01TypeAlgebra,
    `SubstitutionSyntax,
    `TypedAlgebra,
    `TypedStructural,
    `TypedSyntax
  ]

@[default_target]
lean_lib IdentityVerification where
  roots := #[`IntensionalIdentityBridge, `IntensionalIdentityModel,
    `IntensionalIdentitySoundness, `IntensionalIdentityRelations,
    `IntensionalIdentityWitness, `IntensionalIdentityTheorems]

@[default_target]
lean_lib ExtensionalRepairVerification where
  roots := #[`ExtensionalRepairSyntax, `ExtensionalRepairLemmas,
    `ExtensionalRepairSoundness, `ExtensionalRepairWitness,
    `ExtensionalRepairTheorems, `ExtensionalRepairAudit]

@[default_target]
lean_lib EffectiveCompletenessVerification where
  roots := #[`EffectiveStandardness, `EffectiveObserver, `EffectiveReduction, `EffectiveRuleBoundary]

@[default_target]
lean_lib IdentityComplexityVerification where
  roots := #[`EffectiveCanonicalTests, `EffectivePartialObserver]

@[default_target]
lean_lib BooleanIdentityVerification where
  roots := #[`EffectiveBooleanStandardness, `EffectiveBooleanCertificates,
    `EffectivePrimitiveRecursion, `EffectiveBooleanInterfaces, `EffectiveBooleanControls]

@[default_target]
lean_lib GateAndRestrictedVerification where
  roots := #[`BareBooleanGatePositive, `BareBooleanGateSyntax, `CheckerControls, `CheckerKernelAudit, `ComputablePrelude, `IdentityChecker, `MaskNormalisation, `PositiveSeparation, `RestrictedCompiler, `SparsePolynomial]

lean_lib AuditSupport where
  roots := #[`verification.KernelAudit]

@[default_target]
lean_lib PolynomialTestVerification where
  roots := #[`PolynomialTestBoundary, `PolynomialTestAudit]
